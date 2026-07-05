# Java Code Review 审查清单

> 基于《阿里巴巴 Java 开发手册（泰山版）》提炼，仅保留**强制级**和部分**推荐级**高频问题。
> 完整规范见 `references/ali_coding.md`。

---

## 命名规范（强制级）

- [强制] 命名不以下划线或美元符号开始/结束 → 使用规范的驼峰命名
- [强制] 禁止拼音与英文混合命名 → 使用正确的英文单词
- [强制] 类名使用 UpperCamelCase（DO/BO/DTO/VO 等缩写例外） → `ForceCode`, `UserDO`
- [强制] 方法名、参数名、变量名使用 lowerCamelCase → `localValue`, `getHttpMessage()`
- [强制] 常量全大写，下划线分隔 → `MAX_STOCK_COUNT`
- [强制] 抽象类用 Abstract/Base 开头；异常类用 Exception 结尾；测试类用 Test 结尾
- [强制] POJO 布尔属性不加 is 前缀 → 避免框架序列化解析错误
- [强制] 包名全小写，点分隔符间仅一个单词，使用单数形式
- [强制] 杜绝不规范缩写 → `AbstractClass` 而非 `AbsClass`
- [强制] Service/DAO 实现类用 Impl 后缀 → `CacheServiceImpl`
- [强制] 不允许魔法值直接出现在代码中 → 提取为有意义的常量

---

## OOP 设计（强制级）

- [强制] 通过类名访问静态变量/方法，禁止通过实例引用
- [强制] 所有覆写方法必须加 @Override 注解
- [强制] 过时接口必须加 @Deprecated 并说明替代方案
- [强制] equals 使用常量或确定有值的对象调用 → `"test".equals(object)`
- [强制] 整型包装类比较全部使用 equals，禁止用 ==
- [强制] 浮点数等值判断禁止用 == 或 equals → 使用 BigDecimal 或误差范围
- [强制] 禁止 `new BigDecimal(double)` → 用 `new BigDecimal("0.1")` 或 `BigDecimal.valueOf()`
- [强制] POJO 属性必须使用包装数据类型；RPC 返回值和参数必须使用包装类型
- [强制] DO/DTO/VO 类不设定属性默认值
- [强制] 构造方法禁止加入业务逻辑 → 初始化放 init 方法
- [强制] POJO 类必须写 toString 方法
- [强制] 禁止同时存在 isXxx() 和 getXxx() 方法

---

## 异常处理（强制级）

- [强制] 可预检查的 RuntimeException 禁止用 catch 处理 → `if (obj != null)` 而非 try-catch NPE
- [强制] 异常不要用来做流程控制/条件控制
- [强制] catch 时区分异常类型，禁止大段 try-catch
- [强制] 捕获异常必须处理，禁止 catch 后吞掉 → 不处理则向上抛出
- [强制] 事务中 catch 异常后需回滚的，必须手动回滚
- [强制] finally 块必须关闭资源对象/流对象（JDK7+ 用 try-with-resources）
- [强制] 禁止在 finally 块中 return
- [强制] 异常日志必须包含案发现场信息 + 异常堆栈 → `log.error("context: {}", param, e)`
- [强制] 调用 RPC/二方包/动态生成类方法时，用 Throwable 捕获

---

## 并发安全（强制级）

- [强制] 单例对象及其方法必须保证线程安全
- [强制] 创建线程/线程池时指定有意义的线程名称 → 方便 jstack 排查
- [强制] 线程资源必须通过线程池提供，禁止显式 new Thread
- [强制] 线程池禁止用 Executors 创建 → 用 ThreadPoolExecutor 明确参数
- [强制] SimpleDateFormat 线程不安全，禁止定义为 static 共享 → 用 DateTimeFormatter (JDK8+)
- [强制] ThreadLocal 变量必须回收（try-finally 中 remove），防止线程池复用时内存泄漏
- [强制] 能锁区块就不锁方法体；能用对象锁就不用类锁
- [强制] 多资源加锁必须保持一致的加锁顺序 → 防止死锁
- [强制] lock.lock() 必须在 try 之外，unlock 在 finally 中
- [强制] 并发修改同一记录需加锁（应用层/缓存/乐观锁 version）
- [强制] 高并发场景避免用"等于"判断作为中断条件 → 用大于/小于区间判断

---

## SQL 规范（强制级）

- [强制] 表必备三字段：id, gmt_create, gmt_modified
- [强制] 表名、字段名全小写，禁止大写字母 → `aliyun_admin`
- [强制] 小数类型用 decimal，禁止 float/double
- [强制] 业务唯一字段必须建唯一索引
- [强制] 超过三个表禁止 join；join 字段类型必须一致且有索引
- [强制] 禁止左模糊或全模糊查询 → 走搜索引擎
- [强制] 不使用 count(列名) 替代 count(*)
- [强制] sum() 注意 NPE → `SELECT IFNULL(SUM(col), 0)`
- [强制] 禁止使用外键与级联 → 在应用层解决
- [强制] 禁止使用存储过程
- [强制] 查询禁止 SELECT * → 明确列出所需字段
- [强制] sql.xml 参数使用 #{} 绑定，禁止 ${} 拼接 → 防止 SQL 注入
- [强制] 更新记录时必须同时更新 gmt_modified

---

## 安全漏洞（强制级）

- [强制] 用户页面/功能必须做权限控制校验 → 防止水平越权
- [强制] 用户敏感数据必须脱敏展示 → 手机号 `137****0969`
- [强制] SQL 参数严格使用参数绑定，禁止字符串拼接 → 防止 SQL 注入
- [强制] 用户请求参数必须做有效性验证 → 防止内存溢出、慢查询、SSRF、注入等
- [强制] 禁止向 HTML 输出未过滤/未转义的用户数据 → 防止 XSS
- [强制] 表单/AJAX 提交必须执行 CSRF 安全验证
- [强制] URL 外部重定向必须白名单过滤
- [强制] 平台资源（短信/邮件/支付）必须实现防重放机制 → 频率限制 + 验证码

---

## 日志规范（推荐级）

- [强制] 禁止直接使用 Log4j/Logback API → 使用 SLF4J 门面
- [强制] 日志字符串拼接使用占位符 → `logger.debug("id: {}", id)`
- [强制] trace/debug/info 级别日志必须判断开关 → `if (logger.isDebugEnabled())`
- [强制] 生产环境禁止 System.out/err 和 e.printStackTrace()
- [强制] 日志打印禁止直接用 JSON 工具转对象 → 用 toString() 或业务属性
- [推荐] 生产环境禁止输出 debug 日志；info 日志有选择地输出
- [推荐] 用户输入参数错误用 warn 记录；error 仅用于系统逻辑出错/异常
- [推荐] 日志描述尽量用英文，描述不清时可用中文

---

## 其它高频检查项

- [强制] 正则表达式必须预编译（Pattern 定义为类成员） → 禁止方法内 Pattern.compile
- [强制] 禁止用 Apache BeanUtils 做属性 copy → 用 Spring BeanUtils 或 MapStruct
- [强制] foreach 中禁止 remove/add → 使用 Iterator 或 Stream filter
- [强制] Comparator 实现必须满足自反性、传递性、对称性
- [强制] 集合转数组用 `toArray(new T[0])` → 禁止无参 toArray 强转
- [强制] switch 每个 case 必须 break/return/continue，必须包含 default
- [强制] if/else/for/while/do 必须使用大括号
- [推荐] 单个方法不超过 80 行 → 超出则拆分子方法
- [推荐] if-else 不超过 3 层 → 用卫语句/策略模式重构
- [推荐] 集合初始化指定容量 → `new HashMap<>(16)`
