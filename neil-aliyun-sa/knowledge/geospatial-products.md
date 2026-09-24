# 时空 / GIS（GEO）能力地图 — 阿里云地理空间能力全景

> 创建：2026-08-25（Query 回写，4 路 subagent 并行核验 help.aliyun.com / aliyun.com / lbs.amap.com）
> 触发问题：Neil 问「阿里云上有没有什么 GEO 的功能」（确认方向=地理位置/时空能力）
> 证据等级标注：[官方]=文档明文 / [推断]=基于官方文档的合理推断

## 0. 一句话全景

阿里云**没有名为"GEO/LBS"的独立云产品**（aliyun.com/product/lbs 已 404），地理时空能力以**引擎组件形式内嵌在数据库产品线**中：核心是 **GanosBase（Ganos）时空引擎**（PG 系 + Lindorm），辅以通用产品内置 geo 能力（TairGIS / Tablestore / ES）、大数据生态（Sedona / Hive GIS UDF）与可视化（DataV）；地图基础服务（地理编码/路径规划）出口在**高德开放平台**（独立平台，非阿里云产品）。

## 1. 能力分层总表

| 层 | 能力 | 载体产品 | 计费 | 状态 | 证据 |
|---|---|---|---|---|---|
| 专业时空引擎 | GanosBase 全模型（几何/栅格/轨迹/点云/网格/路网/三维） | PolarDB PostgreSQL | 随实例免费自带 | ✅ 在售 | [官方] |
| 专业时空引擎 | Ganos（含 PostGIS 插件，"Ganos PostGIS+"） | RDS PostgreSQL | 随实例免费自带 | ✅ 在售 | [官方] |
| 专业时空引擎 | Ganos 时空引擎 | AnalyticDB PostgreSQL | 不单独计费；🔴 Serverless 模式暂不支持 | ✅ 在售 | [官方] |
| 海量时空服务 | Lindorm Ganos 时空服务（点/线/面/三种轨迹模型，Z-ORDER/S2/xz2t 索引，GeoMesa 兼容接口） | Lindorm 宽表引擎组件（须宽表≥2.6.5） | 免费开通，仅收宽表引擎费 | ✅ 在售 | [官方] |
| 专业时空引擎 | HBase Ganos 时空引擎 | 云数据库 HBase | — | 🔴 **已下线** | [官方] |
| 轻量 LBS | TairGIS：R-Tree 索引，WKT 点/线/面，GIS.ADD/GET/CONTAINS/WITHIN/INTERSECTS/SEARCH/DEL（支持半径/多边形搜索） | Tair **企业版内存型**（磁盘型/开源版不支持） | 随实例 | ✅ 在售 | [官方] |
| 轻量 LBS | Redis 原生 GEO 命令（GeoHash+ZSet，仅点） | 云数据库 Redis/Tair 全系 | 随实例 | ✅ | [官方] |
| 轻量 LBS | 多元索引地理查询：GeoDistanceQuery / GeoBoundingBoxQuery / GeoPolygonQuery（坐标"纬度,经度"格式） | 表格存储 Tablestore | 随索引 | ✅ 在售 | [官方] |
| 轻量 LBS | geo_point / geo_shape / geo_distance；8.5 新增 Geo grid | 阿里云 Elasticsearch | 随实例 | ✅ 在售 | [官方]+[推断] |
| 轻量 LBS | Distance Cava 排序插件（球面距离算分/排序；范围过滤能力未证实） | OpenSearch 行业算法版 | 随实例 | ⚠️ 部分 | [官方]+存疑 |
| 标准 GIS | MySQL 内核标准空间能力（GEOMETRY 类型/SPATIAL 索引/ST_* 函数），无阿里云专页 | RDS MySQL / PolarDB MySQL | 随实例 | ✅（内核自带） | [推断] |
| 大数据时空 | EMR Serverless Spark 集成 Apache Sedona 1.8.1（引擎 esr-4.7.0，200+ 空间函数） | EMR Serverless Spark | 随 Spark 资源 | ✅ 官方支持 | [官方] |
| 大数据时空 | Hive 地理空间 UDF（esri-geometry-api 注册 ST_* 函数） | MaxCompute | 随计算 | ✅ 有方案 | [官方] |
| 大数据时空 | GeoMesa / Flink 地理函数 | — | — | 🔴 未查到官方支持 | [官方缺失] |
| 可视化 | DataV：100+ 地理图元、动态轨迹层、三维城市构建器+三维轨迹层（专业/尊享版）、对接 Ganos | DataV（Board/Atlas/TwinFabric/Note 四件套） | 个人版 84.15 元/年～尊享版 42 万/年 | ✅ 在售 | [官方] |
| IoT 位置 | 设备位置服务（GPS/WiFi/基站/IP 定位、轨迹回放、地理围栏报警） | 物联网平台 | 免费增值 | 🔴 **不再支持新开通**（仅存量） | [官方] |
| 地图基础服务 | 地理/逆地理编码、路径规划、定位、围栏、猎鹰轨迹、MCP Server | **高德开放平台**（lbs.amap.com，独立平台非阿里云产品） | 高德侧计费 | ✅ | [官方] |

## 2. Ganos 选型三分法（核心判据）

| 场景 | 选择 | 理由 |
|---|---|---|
| OLTP 时空事务 + PostGIS 生态（GIS 应用、自然资源、CIM） | **PolarDB PG + Ganos** | 文档最全、模块最全（含栅格/点云/三维/路网）、官方宣称大规模矢量查询较 PostGIS 提升 5 倍[官方宣称] |
| 分析型时空（HTAP/OLAP） | **ADB PG + Ganos** | MPP 并行分析；🔴 勿选 Serverless 形态（不支持 Ganos） |
| 海量轨迹/IoV/电子围栏（百亿级点、高吞吐写） | **Lindorm Ganos 时空服务** | NoSQL 扩展性；官方对标 GeoMesa(HBase)：写≈2 倍、存储≈80%、查询≈1/3 耗时[官方测试页]；围栏链路=宽表存围栏+流引擎订 Kafka+ST_Contains 实时判定，进出事件须自行状态对比[推断] |
| 毫秒级"附近的人/店"、实时围栏判定（小数据量热路径） | **TairGIS** | 内存 R-Tree；注意仅企业版内存型 |

**PostGIS 关系**：Ganos 几何引擎全面兼容 PostGIS 函数接口、遵循 OpenGIS 标准；RDS PG 文档原文"Ganos 时空引擎插件包括阿里云自研 Ganos 插件和 PostGIS 插件"，部分 11/12 实例 PostGIS 即以 Ganos 实现 → 定性**兼容并增强**[官方]。

## 3. 场景 × 产品速查

| 业务场景 | 推荐组合 |
|---|---|
| 车联网（T-Box 轨迹+围栏+车况） | Lindorm（宽表 Ganos 时空服务+时序+流引擎）；参考 cloud-solutions S7 |
| 出行/物流（路径+轨迹分析） | PolarDB PG Ganos（路网 Network 模块支持 TSP/K 最短/双向 Dijkstra）+ 高德路径规划 API |
| 附近搜索/同城零售 | TairGIS（热路径）+ Tablestore/ES（大表召回）+ OpenSearch Distance（排序） |
| 电子围栏告警 | TairGIS GIS.CONTAINS（小/实时）或 Lindorm 流引擎+ST_Contains（大/流式） |
| 自然资源/CIM/实景三维 | PolarDB PG Ganos（栅格/点云/osgb/gltf 三维）+ DataV TwinFabric |
| 遥感影像分析 | PolarDB PG / ADB PG Ganos Raster |
| 时空大数据离线计算 | EMR Serverless Spark + Sedona；MaxCompute Hive GIS UDF |
| 大屏时空可视化 | DataV（动态轨迹层/三维城市，Ganos 数据源） |
| 地理编码/路径规划等基础 API | 高德开放平台（或云市场高德商品/IQS 高德基础接口） |

## 4. 避坑清单（🔴 红线）

1. **IoT 平台设备位置服务不再支持新开通**——新项目不可依赖，存量维护态（围栏文档约 2020 年后停更）。
2. **HBase Ganos 已下线**——引用旧资料时注意。
3. **ADB PG Ganos 不支持 Serverless 模式**——采购形态核验（呼应 pricing-verification-checklist）。
4. **TairGIS 仅企业版内存型**——磁盘型/持久内存型/开源版 Redis 均无；Redis 原生 GEO 只支持点，线/面/围栏必须 TairGIS。
5. **阿里云无独立 LBS 产品**（product/lbs 404）——位置 API 需求引导到高德开放平台，注意高德不是阿里云产品（计费/合同主体不同）。
6. **Ganos 不独立售卖**——随宿主数据库实例付费，报价时不单列。
7. **名称混淆**：`aliyun.com/database/ganos`（GanosBase，PG 系时空引擎）与 Lindorm「Ganos 时空服务」同名不同产品线，能力范围差异大（后者无栅格/点云）。
8. **Tablestore geo 坐标格式是"纬度,经度"（纬度在前）**——与常见"经度,纬度"相反，易错。
9. **MySQL 系 GIS 无阿里云专页**——语义以 MySQL 官方文档为准[推断]，对客口径标注清楚。

## 5. 关键文档链接（2026-08-25 全部实测可访问）

**Ganos / PG 系**
- PolarDB PG GanosBase 简介：help.aliyun.com/zh/polardb/polardb-for-postgresql/overview-51
- RDS PG Ganos 简介：help.aliyun.com/zh/rds/apsaradb-rds-for-postgresql/overview-7
- ADB PG Ganos：help.aliyun.com/zh/analyticdb/analyticdb-for-postgresql/user-guide/overview-ganos
- Ganos 产品页：www.aliyun.com/database/ganos
- PolarDB Ganos 最佳实践：help.aliyun.com/zh/polardb/polardb-for-postgresql/best-practices-11/

**Lindorm**
- Ganos 时空服务目录：help.aliyun.com/zh/lindorm/user-guide/lindorm-ganos-service/
- 开通与计费说明：help.aliyun.com/zh/lindorm/enable-spatio-temporal-service
- 时空索引（Z-ORDER/S2）：help.aliyun.com/zh/lindorm/introduction-to-spatio-temporal-index
- 轨迹存储模型（点/线/分段线）：help.aliyun.com/zh/lindorm/user-guide/time-series-terms
- 电子围栏最佳实践：help.aliyun.com/zh/lindorm/user-guide/electronic-fence
- GeoMesa 兼容 API：help.aliyun.com/zh/lindorm/user-guide/usage
- 性能对比页：help.aliyun.com/zh/lindorm/user-guide/performance-test

**轻量 LBS**
- TairGIS 命令：help.aliyun.com/zh/redis/developer-reference/tairgis-command
- TairGIS 电子围栏：help.aliyun.com/zh/redis/use-cases/user-trajectory-monitoring-using-tairgis
- TairGIS 同城购：help.aliyun.com/zh/redis/use-cases/implementation-of-the-same-city-purchase-business-based-on-tairgis
- Tablestore GeoDistanceQuery：help.aliyun.com/zh/tablestore/geo-distance-query
- ES 版本特性（Geo grid）：help.aliyun.com/zh/es/product-overview/overview-6
- ES 检索增强版 geo 白名单：help.aliyun.com/zh/es/user-guide/retrieve-enhanced-supported-parameter-configurations
- OpenSearch Distance 插件：help.aliyun.com/zh/open-search/industry-algorithm-edition/distance

**大数据 / 可视化 / 生态**
- MaxCompute 地理空间 UDF：www.alibabacloud.com/help/zh/maxcompute/user-guide/geospatial-udfs
- EMR Spark 集成 Sedona：help.aliyun.com/zh/emr/emr-serverless-spark/use-cases/integrating-apache-sedona-for-spatial-data-analysis
- DataV 文档：help.aliyun.com/zh/datav/
- IoT 设备位置服务（含"不再支持新开通"）：help.aliyun.com/zh/iot/user-guide/service-introduction-1
- 高德开放平台 API：lbs.amap.com/api（MCP Server：lbs.amap.com/api/mcp-server）
- IQS 高德基础接口：help.aliyun.com/zh/document_detail/2990718.html
- 云市场高德店：market.aliyun.com/store/4925914/index.html

## 6. 交叉引用

- 车联网方案（Lindorm 时序+轨迹链路）→ [cloud-solutions.md S7](cloud-solutions.md)
- TairGIS 游戏围栏用法 → [aliyun-products.md Tair 卡](aliyun-products.md)
- ADB PG / PolarDB PG 产品卡 → [aliyun-products.md](aliyun-products.md)
- 采购形态核验（ADB Serverless 不支持 Ganos）→ [../references/pricing-verification-checklist.md](../references/pricing-verification-checklist.md)
