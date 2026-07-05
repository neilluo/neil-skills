---
name: neil-coding
description: "Enforces DDD + Hexagonal architecture standards and Alibaba Java coding standards for Java projects. Covers 7-module Maven structure, Gateway pattern, anti-corruption layer, naming conventions, testing rules, and API documentation. Also serves as the authoritative code review rule source based on the Alibaba Java Development Manual (Taishan Edition), covering naming, OOP, exceptions, concurrency, SQL, security, and logging. MANDATORY for all Java code changes including new features, refactoring, bug fixes, and code reviews."
---

# Neil Coding Style — DDD + Hexagonal Architecture

> **MANDATORY**: Apply to ALL Java code changes. For detailed code examples, see [ddd-patterns.md](ddd-patterns.md).

---

## 1. Module Structure & Dependency Hierarchy

### 7-Module Maven Layout

```
{project}/
├── pom.xml                               # Parent POM (packaging: pom)
├── {project}-common/                     # Shared utilities — NO internal dependencies
│   └── com.{company}.{project}.common/
│       ├── io/                           # I/O utilities
│       └── util/                         # General utility classes
├── {project}-domain/                     # Core domain: models + gateways + domain services
│   └── com.{company}.{project}.domain/
│       ├── common/model/                 # Cross-context shared models & interfaces
│       └── {context}/                    # Bounded context (e.g., image, video, order)
│           ├── gateway/                  # Gateway interfaces (implemented by infrastructure)
│           ├── model/                    # Domain models (rich, with behavior)
│           └── service/                  # Domain services (concrete classes wrapping gateways)
├── {project}-api/                        # Pure interfaces + DTOs — NO internal dependencies
│   └── com.{company}.{project}.api/{context}/
│       ├── XxxService.java              # Service interface (API contract)
│       ├── request/XxxReq.java          # Request DTO (Req suffix)
│       └── response/XxxResp.java        # Response DTO (Resp suffix)
├── {project}-service/                    # Business logic kernel — orchestration + implementations
│   └── com.{company}.{project}.service/{context}/
│       ├── XxxService.java              # Service interface (internal contract)
│       ├── dto/                          # Internal DTOs (Request/Response suffix)
│       ├── base/                         # Abstract base classes
│       └── impl/                         # Concrete implementations (XxxServiceImpl)
├── {project}-infrastructure/             # External adapters — implements domain gateways
│   └── com.{company}.{project}.infrastructure/
│       ├── client/                       # Client factories
│       ├── config/                       # Cloud/external service configuration
│       └── {concern}/                    # Adapters grouped by concern (moderation/, storage/)
├── {project}-biz/                        # HTTP layer — REST controllers + HTTP DTOs
│   └── com.{company}.{project}.biz/
│       ├── controller/{context}/         # Thin controllers
│       └── dto/                          # HTTP DTOs (common/, {context}/)
└── {project}-application/                # Spring Boot entry point — composition root
    └── com.{company}.{project}.application/
        ├── {ProjectName}Application.java # @SpringBootApplication
        └── config/                       # Startup validation, CORS, bean wiring
```

### Dependency Direction (STRICT — No Circular Dependencies)

```
{project}-application
    └─► {project}-biz
         ├─► {project}-service
         │    ├─► {project}-api
         │    ├─► {project}-domain
         │    └─► {project}-common
         ├─► {project}-infrastructure
         │    ├─► {project}-domain
         │    └─► {project}-common
         └─► {project}-common
{project}-api → (nothing)
{project}-domain → {project}-common
{project}-common → (nothing)
```

### Layer Rules

| Layer | Allowed Dependencies | Forbidden |
|-------|---------------------|-----------|
| **common** | Java stdlib, logging, testing | Everything else |
| **domain** | common, slf4j-api | Service, Infrastructure, Application, any SDK |
| **api** | (none) | Everything (pure interfaces + DTOs) |
| **service** | api, domain, common, spring-context | Infrastructure, Application, any SDK |
| **infrastructure** | domain, common, SDKs, Spring Boot | Service, Application |
| **biz** | service, infrastructure, common, Spring Web | Direct SDK imports |
| **application** | biz, Spring Boot | Business logic |

---

## 2. Core Architecture Patterns

> Full code examples in [ddd-patterns.md](ddd-patterns.md).

### Gateway Pattern

Domain defines `XxxGateway` interfaces. Infrastructure implements them as `{Vendor}{Xxx}Adapter`.

```java
// domain/{context}/gateway/ — returns domain types ONLY
public interface ImageModerationGateway {
    ImageModerationResult moderateImage(String imageUrl) throws Exception;
}
```

- Adapters implement gateway, confine ALL vendor SDK types to infrastructure
- `grep -r "import com.aliyun" {project}-domain/ {project}-service/` must return ZERO results

### Domain Service

**Concrete classes** (not interfaces) wrapping gateways with error handling. Plain Java — no Spring annotations. Wired as beans in composition root.

### Anti-Corruption Layer

ALL vendor SDK mapping happens **exclusively in infrastructure adapters**. See [ddd-patterns.md Section 1](ddd-patterns.md) for the complete adapter pattern.

### Rich Domain Models

Domain objects MUST have behavior, not just getters/setters:
- Value objects: `isNonLabel()`, `isAboveThreshold(double)`
- Aggregates: `getRiskLabels()`, `getTopLabel()`, `markError(msg)`
- Derived properties: `getFileName()`, `getRiskFrameCount()`
- Base interfaces with default methods: `isApiCallSuccess()`

### Bounded Contexts

Each context gets its own package subtree in every layer. Cross-context shared types in `domain/common/model/`.

---

## 3. Service Layer

> Full patterns (Delegator, Strategy, Orchestration, Routing) in [ddd-patterns.md Section 4](ddd-patterns.md).

- **Interfaces** in `service/{context}/` root
- **Implementations** in `service/{context}/impl/` with `@Service("beanName")`
- **Abstract base classes** in `service/{context}/base/` for shared algorithms
- **Bean wiring** in composition root (application config), NOT in domain layer

---

## 4. HTTP Layer (BIZ Module)

Controllers are thin HTTP adapters: transform DTOs at boundary, delegate to service interfaces only.

```java
@RestController
@RequestMapping("/api/{context}")
public class XxxController {
    private final XxxService xxxService;  // constructor injection

    @PostMapping("/action")
    public GenericResp<XxxResp> doAction(@RequestBody XxxReq request) {
        XxxRequest serviceReq = /* biz DTO -> service DTO */;
        XxxResponse serviceResp = xxxService.doAction(serviceReq);
        return GenericResp.success(convertToBizResponse(serviceResp));
    }
}
```

All endpoints return `GenericResp<T>` with fields: `success`, `code`, `message`, `error`, `data`, `timestamp`.

---

## 5. DTO Transformation Flow

```
HTTP Request (Biz Req) → Service Request (Service Request) → Domain Model
HTTP Response (Biz Resp) ← Service Response (Service Response) ← Domain Model
```

| Layer | Request Suffix | Response Suffix | Example |
|-------|---------------|----------------|---------|
| **API / BIZ** (HTTP) | `Req` | `Resp` | `ImageModerateReq`, `ImageModerateResp` |
| **Service** (internal) | `Request` | `Response` | `ImageModerateRequest`, `ImageModerateResponse` |

---

## 6. Naming Conventions (STRICT)

| Type | Pattern | Example |
|------|---------|---------|
| Gateway interface | `XxxGateway` | `ImageModerationGateway`, `VideoStorageGateway` |
| Infrastructure adapter | `{Vendor}{Xxx}Adapter` | `AliyunImageModerationAdapter` |
| Domain service | `XxxDomainService` | `ImageDomainService`, `VideoDomainService` |
| Domain model | `Xxx`, `XxxResult` | `ImageModerationResult`, `ModerationLabel` |
| Base interface | `BaseXxx` | `BaseModerationResult` |
| Service interface | `XxxService` | `ImageModerationService` |
| Service impl | `XxxServiceImpl` | `ImageModerationServiceImpl` |
| Abstract base | `AbstractXxxService` | `AbstractModerationService` |
| Controller | `XxxController` | `ImageModerationController` |
| Factory | `XxxFactory` | `AliCloudModerationClientFactory` |
| Config properties | `XxxProperties` | `AlibabaCloudProperties` |

**Package**: `com.{company}.{project}.{module}` with bounded contexts as subpackages. Implementations always in `impl/`, base classes in `base/`.

---

## 7. Coding Conventions

### Constructor Injection (Always)

```java
@Service("xxxService")
public class XxxServiceImpl implements XxxService {
    private final SomeDependency dependency;
    public XxxServiceImpl(SomeDependency dependency) { this.dependency = dependency; }
}
```

No `@Autowired` on fields. No setter injection.

### Constants, Logging, Error Handling

```java
private static final String ENDPOINT = "...";
private static final Logger log = LoggerFactory.getLogger(XxxClass.class);
log.info("[{}/{}] Processing: {}", current, total, name);
log.error("Error processing: {}", context, exception);
```

**Fallback pattern**: `createFallbackResult(input, errorMessage)` returns a failed domain object with timestamp.

### Strong Typing

- NO `Map<String, Object>` for business data
- Strong-typed DTOs everywhere
- Generic response wrappers: `GenericResp<T>`, `Page<T>`

### Null-Safe Processing

```java
if (body == null) { result.markError("Null response"); return result; }
```

---

## 8. Testing Standards

> Full test code patterns in [ddd-patterns.md Section 6](ddd-patterns.md).

### After Every Change

```bash
mvn compile && mvn test
```

### Test Structure Rules

- Test class = `{ClassName}Test` (e.g., `ModerationResultTest`)
- **MUST** use `@DisplayName` on class and `@Nested` inner classes to group tests
- Method name: `shouldXxx` or `xxxShouldXxxWhenXxx`
- AssertJ preferred: `assertThat(result).isNotNull()`
- Float/Double tolerance: `assertThat(val).isCloseTo(0.95, within(0.001))`

### What to Mock Per Layer

| Layer | Mock Target | Stub With |
|-------|------------|----------|
| Domain model tests | Nothing | Pure logic assertions |
| Domain service tests | Gateway interfaces | Domain objects |
| Service tests | Domain services / Gateways | Domain objects |
| Infrastructure tests | SDK clients | Vendor DTOs |
| Common utility tests | Nothing (or `@TempDir`) | Pure assertions |

### Mandatory Test Coverage Per Feature

- [ ] Happy path — normal successful behavior
- [ ] Null inputs — null / empty parameters
- [ ] Error paths — exception handling, fallback results
- [ ] Edge cases — zero values, empty lists, boundary conditions
- [ ] Interface compliance — base interface default methods
- [ ] Derived properties — computed fields
- [ ] Inner classes — dedicated `@Nested` blocks for inner types

---

## 9. API Documentation (BIZ Module)

> Full API doc template and format in [ddd-patterns.md Section 7](ddd-patterns.md).

### Location

```
{project}-biz/
└── API_DOC.md       # Complete REST API documentation for frontend
```

### Mandatory Rule

> **CRITICAL**: Any code change that affects an API endpoint — adding, removing, or modifying a controller method, changing request/response DTOs, altering URL paths, or modifying the response wrapper — **MUST** update `API_DOC.md` in the same commit. Inconsistency between code and API doc is a **blocking defect**.

### Consistency Checklist (MANDATORY on every API change)

- [ ] New endpoint -> add complete section to `API_DOC.md`
- [ ] Modified request/response DTO -> update field table and JSON example
- [ ] Changed URL path -> update endpoint path in doc
- [ ] Removed endpoint -> remove from doc
- [ ] Changed `GenericResp` fields -> update common wrapper section
- [ ] Changed DTO inner classes -> update nested object documentation

---

## 10. New Project Bootstrap

### Steps to Create a New Project

1. Create parent POM with `<packaging>pom</packaging>`, Java 21, Spring Boot 3.2.x
2. Create 7 modules in order: common -> domain -> api -> service -> infrastructure -> biz -> application
3. Set dependency hierarchy in each module POM (see Section 1)
4. Configure `@SpringBootApplication(scanBasePackages = "com.{company}")` in application module
5. Add `ARCHITECTURE_GUIDE.md` to project root as the canonical architecture reference
6. Add `API_DOC.md` to biz module root
7. Create first bounded context following the New Feature Checklist (Section 11)

> Detailed POM templates and composition root wiring in [ddd-patterns.md Section 11](ddd-patterns.md).

---

## 11. Quick Reference Checklists

### New Feature Checklist

- [ ] Domain model with behavior in `domain/{context}/model/`
- [ ] Gateway interface in `domain/{context}/gateway/` (if external dependency needed)
- [ ] Domain service in `domain/{context}/service/` wrapping gateway
- [ ] Infrastructure adapter in `infrastructure/` implementing gateway
- [ ] Service interface in `service/{context}/`
- [ ] Service impl in `service/{context}/impl/` with `@Service("beanName")`
- [ ] Service DTOs (Request/Response suffix) in `service/{context}/dto/`
- [ ] API interface + DTOs (Req/Resp suffix) in `api/{context}/`
- [ ] BIZ DTOs (Req/Resp suffix) in `biz/dto/{context}/`
- [ ] Controller in `biz/controller/{context}/`
- [ ] DTO transformation at every layer boundary
- [ ] Zero vendor imports in domain + service + application
- [ ] Tests for all layers (see Section 8)
- [ ] **API_DOC.md updated** if any endpoint was added/changed/removed
- [ ] Tests pass: `mvn test`

### Layer Violation Audit

```bash
# Domain — zero vendor/framework imports (slf4j allowed)
grep -r "import com.aliyun\|import com.alibaba\|import org.springframework" {project}-domain/

# Service — zero vendor imports
grep -r "import com.aliyun\|import com.alibaba" {project}-service/

# Infrastructure — must NOT import service layer
grep -r "import com.{company}.{project}.service" {project}-infrastructure/
```

---

## 12. Anti-Patterns to Avoid

| Anti-Pattern | Correct Approach |
|-------------|------------------|
| Vendor types in domain/service | Confine to infrastructure adapters |
| Infrastructure bean in controller | Delegate through service layer |
| `Map<String, Object>` for business data | Strong-typed DTOs |
| Anemic domain models (getters/setters only) | Rich models with behavior methods |
| Skipping DTO transformations between layers | Transform at every boundary |
| Circular dependencies between modules | Strict downward dependency flow |
| Hardcoded configuration values | Externalize via `@ConfigurationProperties` |
| `@Autowired` field injection | Constructor injection only |
| Business logic in controllers | Thin controllers, delegate to service |
| Implementations in root packages | Use `impl/` subpackage |
| Tests without `@Nested`/`@DisplayName` | Always use structured test grouping |
| Tests without edge cases | Cover null, empty, error, boundary |
| API changes without updating API_DOC.md | **Always update doc in same commit** |
| Stale API documentation | Treat doc inconsistency as blocking defect |

---

## Code Review 规范

当作为 Code Review 规范源使用时，参考 `rules/review-checklist.md`（精简审查清单）。
完整规范见 `references/ali_coding.md`（阿里巴巴Java开发手册泰山版）。
