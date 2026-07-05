# DDD Patterns Reference

Detailed code examples and patterns for DDD + Hexagonal Architecture. Companion to [SKILL.md](SKILL.md).

---

## 1. Anti-Corruption Layer — The Core Rule

The anti-corruption layer is the **single most important DDD boundary**. It prevents vendor SDK types from leaking into domain and service layers.

### Where Mapping Happens

```
Vendor SDK DTO ──► Infrastructure Adapter ──► Domain Object ──► Service Layer ──► BIZ/HTTP
                   ^^^^^^^^^^^^^^^^^^^^^^^^
                   ALL mapping lives HERE
```

### Complete Adapter Pattern

```java
// Infrastructure adapter — the ONLY place that touches vendor types
// Implements domain gateway interface
public class AliyunImageModerationAdapter implements ImageModerationGateway {

    private final Client client;        // vendor type, confined to this class
    private final String service;       // service code (e.g., "baselineCheckByVL")

    @Override
    public ImageModerationResult moderateImage(String imageUrl) throws Exception {
        // 1. Build vendor-specific parameters internally
        Map<String, String> serviceParameters = new HashMap<>();
        serviceParameters.put("imageUrl", imageUrl);
        serviceParameters.put("dataId", UUID.randomUUID().toString());

        // 2. Call vendor API (vendor types)
        ImageModerationResponse response = doModeration(serviceParameters);

        // 3. Create domain object
        ImageModerationResult result = new ImageModerationResult();
        result.setUrl(imageUrl);
        result.setTimestamp(LocalDateTime.now());

        // 4. Null-safe vendor response mapping
        if (response == null) {
            result.markError("HTTP request failed: null response");
            return result;
        }

        ImageModerationResponseBody body = response.getBody();
        if (body == null) {
            result.markError("Null response body");
            return result;
        }

        // 5. Map vendor fields -> domain fields
        result.setRequestId(body.getRequestId());
        result.setCode(body.getCode());
        result.setMessage(body.getMsg());

        // 6. Map nested vendor results -> domain value objects
        if (body.getCode() == 200 && body.getData() != null) {
            List<ModerationLabel> labels = new ArrayList<>();
            for (var apiResult : body.getData().getResult()) {
                ModerationLabel label = new ModerationLabel();
                label.setLabel(apiResult.getLabel());

                // Float -> Double conversion (SDK compatibility)
                Float conf = apiResult.getConfidence();
                label.setConfidence(conf != null ? conf.doubleValue() : null);

                labels.add(label);
            }
            result.setLabels(labels);
        }

        return result;
    }
}
```

### What NOT To Do

```java
// NEVER expose vendor types through gateway interfaces
public interface ImageModerationGateway {
    ImageModerationResponseBody moderateWithBody(Map<String, String> params);  // WRONG
}

// NEVER import vendor types in domain or service layers
import com.aliyun.green20220302.models.ImageModerationResponseBody;  // FORBIDDEN

// NEVER let service layer parse vendor DTOs
if (body.getData().getResult().get(0).getLabel().equals("nonLabel")) { ... }  // WRONG

// NEVER construct vendor Config/Client objects outside infrastructure
Config config = new Config();
config.setAccessKeyId(key);
Client client = new Client(config);  // WRONG — must be in infrastructure
```

---

## 2. Gateway & Domain Service Design

### Gateway Interface Rules

1. **Return domain types only** — never vendor DTOs
2. **Accept domain-friendly parameters** — `String imageUrl`, not `Map<String, String> params`
3. **Javadoc the contract** — document what it does, not how
4. **Declare `throws Exception`** — gateway calls are inherently fallible

```java
// domain/{context}/gateway/
public interface ImageModerationGateway {
    ImageModerationResult moderateImage(String imageUrl) throws Exception;
}

public interface VideoStorageGateway {
    String uploadVideo(String localFilePath);
    List<String> uploadVideosFromDirectory(String directoryPath);
}
```

### Domain Service (Concrete Class)

Domain services are **concrete classes** wrapping a gateway with error handling and fallback. **Plain Java** — no Spring annotations.

```java
// domain/{context}/service/
public class ImageDomainService {
    private static final Logger log = LoggerFactory.getLogger(ImageDomainService.class);
    private final ImageModerationGateway moderationGateway;

    public ImageDomainService(ImageModerationGateway moderationGateway) {
        this.moderationGateway = moderationGateway;
    }

    public ImageModerationResult moderateImage(String imageUrl) {
        try {
            ImageModerationResult result = moderationGateway.moderateImage(imageUrl);
            if (result == null) {
                return createFallbackResult(imageUrl, "Gateway returned null");
            }
            return result;
        } catch (Exception e) {
            log.error("Error moderating image: {}", imageUrl, e);
            return createFallbackResult(imageUrl, "Exception: " + e.getMessage());
        }
    }
}
```

### Naming Convention

```
{Context}ModerationGateway  — for external moderation operations
{Context}StorageGateway     — for storage operations
{Context}RepositoryGateway  — for persistence (if needed)
{Context}DomainService      — concrete class wrapping a gateway
```

---

## 3. Rich Domain Model Patterns

### Anemic vs. Rich — Decision Guide

| Aspect | Anemic (Avoid) | Rich (Prefer) |
|--------|----------------|---------------|
| State queries | External `if` checks | `entity.isRiskDetected()` |
| Filtering | Caller filters lists | `aggregate.getRiskLabels()` |
| State transitions | Caller sets fields | `entity.markError(msg)` |
| Validation | Service validates | Entity self-validates |
| Derived data | Caller computes | `entity.getFileName()` |

### Value Object with Domain Logic

```java
public class ModerationLabel {
    private String label;
    private Double confidence;

    public boolean isNonLabel() { return "nonLabel".equals(label); }
    public boolean isAboveThreshold(double threshold) {
        return confidence != null && confidence >= threshold;
    }
}
```

### Aggregate with Query Methods

```java
public class ImageModerationResult implements BaseModerationResult {
    private List<ModerationLabel> labels;
    private boolean success;

    public List<ModerationLabel> getRiskLabels() {
        if (labels == null) return List.of();
        return labels.stream().filter(label -> !label.isNonLabel()).toList();
    }

    public ModerationLabel getTopLabel() {
        if (labels == null || labels.isEmpty()) return null;
        return labels.stream()
                .max(Comparator.comparingDouble(l ->
                        l.getConfidence() != null ? l.getConfidence() : 0.0))
                .orElse(null);
    }

    public void markError(String errorMsg) {
        this.success = false;
        this.errorMessage = errorMsg;
    }
}
```

### Derived Properties

```java
public class VideoModerationResult implements BaseModerationResult {
    public String getFileName() {
        String source = videoPath != null ? videoPath : videoUrl;
        return UrlUtils.getFileName(source);
    }
    public boolean isHighRisk() { return "high".equalsIgnoreCase(riskLevel); }
    public int getRiskFrameCount() {
        if (frameResults == null) return 0;
        return (int) frameResults.stream()
            .filter(f -> f.getLabels() != null && !f.getLabels().isEmpty()).count();
    }
}
```

### Base Interface with Default Methods

```java
// domain/common/model/
public interface BaseModerationResult {
    Integer getCode();
    String getSourceUrl();
    boolean hasRisk();
    default boolean isApiCallSuccess() { return getCode() != null && getCode() == 200; }
}
```

---

## 4. Service Layer Patterns

### Pattern 1: Simple Delegator

```java
@Service("videoModerationService")
public class VideoModerationServiceImpl implements VideoModerationService {
    private final VideoDomainService videoDomainService;

    @Override
    public VideoModerateResponse moderateVideo(VideoModerateRequest request) {
        VideoModerationResult domainResult = videoDomainService.moderateVideo(request.getVideoUrl());
        return convertToResponse(domainResult);  // domain -> service DTO
    }
}
```

### Pattern 2: Strategy via Abstract Base Class

```java
// service/{context}/base/
public abstract class AbstractModerationService {
    protected final ImageDomainService imageDomainService;
    public AbstractModerationService(ImageDomainService domainService) {
        this.imageDomainService = domainService;
    }
    public ImageModerationResult moderateImage(String imageUrl) {
        return imageDomainService.moderateImage(imageUrl);
    }
    public abstract String getServiceCode();
}

// service/{context}/impl/
public class BaselineCheckServiceImpl extends AbstractModerationService {
    private static final String SERVICE_CODE = "baselineCheckByVL";
    @Override
    public String getServiceCode() { return SERVICE_CODE; }
}
```

### Pattern 3: Orchestration Service

```java
@Service("videoWorkflowService")
public class VideoWorkflowServiceImpl implements VideoModerationService {
    private final VideoStorageGateway storageGateway;
    private final VideoDomainService videoDomainService;

    @Override
    public List<VideoModerateResponse> uploadAndModerateAll(VideoUploadAndModerateRequest request) {
        List<String> uploaded = storageGateway.uploadVideosFromDirectory(request.getDirectoryPath());
        List<String> allUrls = mergeUrls(request.getExistingUrls(), uploaded);
        return moderateVideos(allUrls);
    }
}
```

### Pattern 4: Routing Service

```java
@Service("imageModerationService")
public class ImageModerationServiceImpl implements ImageModerationService {
    private final BaselineCheckServiceImpl baselineCheckService;
    private final PostImageCheckServiceImpl postImageCheckService;

    @Override
    public ImageModerateResponse moderateImage(ImageModerateRequest request) {
        AbstractModerationService service = switch (request.getServiceCode()) {
            case "baselineCheckByVL" -> baselineCheckService;
            case "postImageCheckByVL" -> postImageCheckService;
            default -> null;
        };
        ImageModerationResult domainResult = service.moderateImage(request.getImageUrl());
        return convertToServiceResponse(domainResult);
    }
}
```

---

## 5. DTO Transformation Patterns

### Three-Layer Transformation

```java
// BIZ layer: HTTP DTO -> Service DTO
ImageModerateRequest serviceRequest = new ImageModerateRequest();
serviceRequest.setImageUrl(request.getImageUrl());
serviceRequest.setServiceCode(request.getServiceCode());

// Service layer: Domain Model -> Service DTO
ImageModerateResponse response = new ImageModerateResponse();
response.setUrl(domainResult.getUrl());
response.setSuccess(domainResult.isSuccess());
response.setLabels(domainResult.getLabels().stream().map(this::convertLabel).toList());

// BIZ layer: Service DTO -> HTTP DTO
ImageModerateResp bizResp = new ImageModerateResp();
bizResp.setUrl(serviceResponse.getUrl());
```

### Static Factory Methods on Response DTOs

```java
public class VideoModerateResp {
    public static VideoModerateResp fromServiceResponse(VideoModerateResponse serviceResponse) {
        VideoModerateResp resp = new VideoModerateResp();
        resp.setVideoUrl(serviceResponse.getVideoUrl());
        resp.setRiskLevel(serviceResponse.getRiskLevel());
        return resp;
    }
}
```

---

## 6. Testing Patterns

### Service Test (Mock Gateway + Real Domain Service)

The key architecture-specific pattern: create a **real domain service** backed by a **mock gateway** to test the full chain.

```java
@ExtendWith(MockitoExtension.class)
@DisplayName("AbstractModerationService")
class AbstractModerationServiceTest {

    @Mock
    private ImageModerationGateway mockGateway;
    private TestModerationService service;

    @BeforeEach
    void setUp() {
        ImageDomainService domainService = new ImageDomainService(mockGateway);
        service = new TestModerationService(domainService);
    }

    // Concrete test-only subclass for abstract base classes
    private static class TestModerationService extends AbstractModerationService {
        public TestModerationService(ImageDomainService ds) { super(ds); }
        @Override
        public String getServiceCode() { return "testService"; }
    }

    @Nested
    @DisplayName("moderateImage")
    class ModerateImageTest {

        @Test
        @DisplayName("should return success result when API returns risk label")
        void shouldReturnSuccessWhenApiReturnsRiskLabel() throws Exception {
            ImageModerationResult mockResult = createDomainResult(200, "risk", 0.95, true);
            when(mockGateway.moderateImage(anyString())).thenReturn(mockResult);

            ImageModerationResult result = service.moderateImage("http://example.com/img.jpg");

            assertThat(result.getCode()).isEqualTo(200);
            assertThat(result.isSuccess()).isTrue();
            assertThat(result.getLabels().get(0).getConfidence()).isCloseTo(0.95, within(0.001));
        }

        @Test
        @DisplayName("should return error result when client returns null")
        void shouldReturnErrorWhenClientReturnsNull() throws Exception {
            when(mockGateway.moderateImage(anyString())).thenReturn(null);
            ImageModerationResult result = service.moderateImage("http://example.com/img.jpg");
            assertThat(result.isSuccess()).isFalse();
            assertThat(result.getErrorMessage()).contains("null");
        }

        @Test
        @DisplayName("should handle exception from client")
        void shouldHandleExceptionFromClient() throws Exception {
            when(mockGateway.moderateImage(anyString())).thenThrow(new RuntimeException("Network error"));
            ImageModerationResult result = service.moderateImage("http://example.com/img.jpg");
            assertThat(result.isSuccess()).isFalse();
        }
    }

    private ImageModerationResult createDomainResult(int code, String label, double confidence, boolean success) {
        ImageModerationResult result = new ImageModerationResult();
        result.setCode(code);
        result.setRequestId("test-request-id");
        result.setTimestamp(LocalDateTime.now());
        result.setSuccess(success);
        if (label != null) {
            result.setLabels(List.of(new ModerationLabel(label, confidence)));
        }
        return result;
    }
}
```

### Utility Test (@TempDir for File I/O)

```java
class UrlFileReaderTest {
    @Test
    void readUrls_shouldReturnEmptyList_whenFileDoesNotExist() {
        List<String> urls = UrlFileReader.readImageUrls("/non/existent/file.txt");
        assertThat(urls).isEmpty();
    }

    @Test
    void readUrls_shouldFilterCommentsAndEmptyLines(@TempDir Path tempDir) throws IOException {
        Path file = tempDir.resolve("urls.txt");
        Files.writeString(file, "# Comment\n\nhttp://example.com/image.jpg\n\n");
        List<String> urls = UrlFileReader.readImageUrls(file.toString());
        assertThat(urls).containsExactly("http://example.com/image.jpg");
    }
}
```

### Comprehensive Utility Test (One @Nested per Method)

```java
@DisplayName("UrlUtils")
class UrlUtilsTest {
    @Nested
    @DisplayName("getFileName")
    class GetFileNameTest {
        @Test
        @DisplayName("should extract filename from simple URL")
        void shouldExtractFilenameFromSimpleUrl() {
            assertThat(UrlUtils.getFileName("https://example.com/video.mp4")).isEqualTo("video.mp4");
        }
        @Test
        @DisplayName("should return unknown for null input")
        void shouldReturnUnknownForNullInput() {
            assertThat(UrlUtils.getFileName(null)).isEqualTo("unknown");
        }
    }

    @Nested
    @DisplayName("isValidUrl")
    class IsValidUrlTest {
        @Test
        @DisplayName("should return true for https URL")
        void shouldReturnTrueForHttpsUrl() {
            assertThat(UrlUtils.isValidUrl("https://example.com")).isTrue();
        }
    }
}
```

---

## 7. API Documentation Format

Every project maintains `{project}-biz/API_DOC.md`. Use this template:

```markdown
# {Project} API Documentation

Base URL: `http://localhost:{port}`

## Common Response Wrapper

All endpoints return `GenericResp<T>`:

| Field     | Type          | Description                     |
|-----------|---------------|---------------------------------|
| success   | boolean       | Whether the request succeeded   |
| code      | String        | Status code ("200" for success)  |
| message   | String        | Human-readable message          |
| error     | String        | Error description (failure only) |
| data      | T             | Response payload                |
| timestamp | LocalDateTime | Server timestamp                |

## {Context} APIs

### {Action Name}

**Endpoint**: `{METHOD} /api/{context}/{action}`

**Description**: What this endpoint does.

**Request Body**:

| Field       | Type   | Required | Description          |
|-------------|--------|----------|----------------------|
| fieldName   | String | Yes      | Description of field |

**Request Example**:
{json block with concrete example}

**Response `data` Payload** (`XxxResp`):

| Field       | Type          | Description                 |
|-------------|---------------|-----------------------------|
| fieldName   | String        | Description of field        |

**Response Example**:
{json block with full response including wrapper}

**Error Response Example**:
{json block with failure response}
```

### Documentation Rules

1. Every endpoint: method + path, description, request fields, request example, response fields, response example, error example
2. Nested objects (e.g., inner classes) documented as sub-tables
3. GET endpoints with no body still document query parameters if any
4. List responses document the element type fully

---

## 8. Forbidden Patterns

### Vendor Type Leakage

```java
// Service parsing vendor response — FORBIDDEN
ImageModerationResponseBody body = client.moderateWithBody(params);
```

### Infrastructure in Controller

```java
// Controller directly using infrastructure bean — FORBIDDEN
@RestController
public class VideoController {
    private final AliyunOssStorageAdapter ossAdapter;  // infrastructure leak!
}
```

### Anemic Domain

```java
// Caller doing what the entity should do — AVOID
if (result.getLabels().stream().anyMatch(l -> !"nonLabel".equals(l.getLabel()))) { ... }

// Push into entity — CORRECT
if (!result.getRiskLabels().isEmpty()) { ... }
```

### Skipped DTO Transformation

```java
// Passing domain model directly to HTTP — FORBIDDEN
return GenericResp.success(domainResult);

// Transform at boundary — CORRECT
return GenericResp.success(convertToBizResponse(serviceResult));
```

### Circular Dependencies

```java
// Infrastructure importing service — FORBIDDEN
import com.company.project.service.SomeService;
```

---

## 9. Provider Swap Readiness

The architecture should allow swapping providers by **only changing infrastructure**:

```
Current:  AliyunImageModerationAdapter  implements ImageModerationGateway
Swap to:  AwsRekognitionAdapter         implements ImageModerationGateway

Current:  AliyunOssStorageAdapter       implements VideoStorageGateway
Swap to:  AwsS3StorageAdapter           implements VideoStorageGateway
```

No changes needed in domain, service, biz, or application layers.

---

## 10. Configuration Patterns

### @ConfigurationProperties

```java
@Component
@ConfigurationProperties(prefix = "vendor.cloud")
public class CloudProperties {
    private String accessKey;
    private String secretKey;

    public String resolveAccessKey() {
        if (accessKey != null && !accessKey.isBlank()) return accessKey;
        return System.getenv("CLOUD_ACCESS_KEY");
    }
}
```

### Startup Validation

```java
@Component
public class StartupValidator {
    @PostConstruct
    public void validate() {
        if (accessKey == null || accessKey.isBlank()) {
            throw new IllegalStateException("Missing credentials");
        }
    }
}
```

---

## 11. New Project Setup Guide

### Step-by-Step

1. **Create parent POM**:
   ```xml
   <packaging>pom</packaging>
   <properties>
       <maven.compiler.source>21</maven.compiler.source>
       <maven.compiler.target>21</maven.compiler.target>
       <spring-boot.version>3.2.2</spring-boot.version>
   </properties>
   <modules>
       <module>{project}-common</module>
       <module>{project}-domain</module>
       <module>{project}-api</module>
       <module>{project}-service</module>
       <module>{project}-infrastructure</module>
       <module>{project}-biz</module>
       <module>{project}-application</module>
   </modules>
   ```

2. **Create modules in dependency order**:
   - `{project}-common` — no internal dependencies
   - `{project}-domain` — depends on common
   - `{project}-api` — no internal dependencies
   - `{project}-service` — depends on api, domain, common
   - `{project}-infrastructure` — depends on domain, common, vendor SDKs
   - `{project}-biz` — depends on service, infrastructure, common
   - `{project}-application` — depends on biz only

3. **Application entry point**:
   ```java
   @SpringBootApplication(scanBasePackages = "com.{company}")
   public class {ProjectName}Application {
       public static void main(String[] args) {
           SpringApplication.run({ProjectName}Application.class, args);
       }
   }
   ```

4. **Composition root** (application/config/):
   ```java
   @Bean
   public XxxServiceImpl xxxService(XxxClientFactory factory) {
       XxxAdapter adapter = factory.create("serviceCode");
       XxxDomainService domainService = new XxxDomainService(adapter);
       return new XxxServiceImpl(domainService);
   }
   ```

5. **Add project docs**:
   - `ARCHITECTURE_GUIDE.md` in project root (canonical architecture reference)
   - `API_DOC.md` in `{project}-biz/` root
   - `application.yml` in `{project}-biz/src/main/resources/`

6. **First bounded context**: Follow the New Feature Checklist in [SKILL.md Section 11](SKILL.md).

### Each Module POM Template

```xml
<!-- {project}-service/pom.xml -->
<parent>
    <groupId>com.{company}</groupId>
    <artifactId>{project}-parent</artifactId>
    <version>1.0-SNAPSHOT</version>
</parent>
<artifactId>{project}-service</artifactId>

<dependencies>
    <dependency>
        <groupId>com.{company}</groupId>
        <artifactId>{project}-api</artifactId>
    </dependency>
    <dependency>
        <groupId>com.{company}</groupId>
        <artifactId>{project}-domain</artifactId>
    </dependency>
    <dependency>
        <groupId>com.{company}</groupId>
        <artifactId>{project}-common</artifactId>
    </dependency>
    <!-- Spring Context for @Service -->
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-context</artifactId>
    </dependency>
    <!-- Testing -->
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.mockito</groupId>
        <artifactId>mockito-junit-jupiter</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.assertj</groupId>
        <artifactId>assertj-core</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```
