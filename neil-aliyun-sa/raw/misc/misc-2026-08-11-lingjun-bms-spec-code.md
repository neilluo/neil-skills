# 灵骏裸金属 产品 code × 实例规格 × 列表价（钉钉表格）

> **来源**：内部钉钉文档（alidocs）
> **URL**：https://alidocs.dingtalk.com/i/nodes/vy20BglGWOxjGpq0CgBKlr4bVA7depqY
> **文档标题**：灵骏产品规格code ｜ **nodeId**：vy20BglGWOxjGpq0CgBKlr4bVA7depqY ｜ **workspaceId**：nb9XJNnNrd5BDXyA ｜ **extension**：axls
> **SHA256（正文 = 三段 CSV 按 sheet 顺序以单个换行拼接后的字符串，非整个文件）**：ccafb9ad2b142b92928b75f7a52f869c46602c6eef863480e5f99a07faa223fb
> **归档日期**：2026-08-11 ｜ **状态**：raw（不可变）
> **抓取方式**：`dws sheet csv-get`（钉钉在线表格 API），逐 sheet 导出非空区域为 CSV。三次调用分别为 `--sheet-id kgqie6hm --range A1:F134`、`--sheet-id st-9936411f-53171 --range A1:N99`、`--sheet-id st-1868fd7e-13856 --range A1:I24`，`--format raw`。`[row=N]` 行号前缀为 API 原样输出，已保留；合并单元格未补全（沿用原表的空值继承语义）。
>
> 🔴 **敏感级别：内部（Alibaba Internal）— 严禁对外**
> 本文件含：①内部固费分期目录价（月单价 / 半年月价 / 一年月价 / 两年月价 / 三年月价 / 四年月价）；②内部卡型代号 L20A / L20B / L20C / L20D / L20P / L20X / L20Y / L20Z 及其与 H800 / H100 / H200 的对应；③加白标签（`zone_id-*` / `hpn-zone-*` / `bcc-region-*` / `code-*` / `exclusivecloud` / `Hypernode` / 研发 uid 可见性）；④专属云与蚂蚁专属可用区、政务云 / 金融云可用区；⑤受出口管制加速卡的分地域可售状态。
> **对客使用前必须脱敏**：对外不得出现内部卡型代号解码、固费分期目录价、加白标签、集群编号与专属 / 政务 / 金融云可用区信息。

---

## Sheet 1：产品code&实例规格（sheetId=`kgqie6hm`，range=A1:F134）

```csv
[row=1] 地域,可用区,集群编号,机型(不显示）,节点,模块值(规格code)
[row=2] ,,,,,
[row=3] 乌兰察布,可用区A,A1,A100-80G,gu7ef-80G-机型2,efg1.nvga1n
[row=4] ,,,A800-80G,gu7xf-80G-机型2,efg1.nvga8n
[row=5] ,,A2,H800,gu8xf-机型2,efg2.nvgh8bn
[row=6] ,,A5,L20C,gn9c.cn8,efg2.GN9C.cn8
[row=7] ,可用区B,B1,A100-40G,gu7ef-40G,efg1.nvga4
[row=8] ,,,A100-80G,gu7ef-80G-机型1,efg1.nvga1
[row=9] ,可用区C,C1,H800,gu8xf-机型2,efg2.nvgh8bn
[row=10] ,,C2,H20-3e,gu8tef,efg2.C48eNH3ebn
[row=11] ,,C1,H800,gu8xf-机型2,efg2.nvgh8bn
[row=12] ,"可用区D
标签：zone_id-wulanchabu-d",D1,PPU810E,p16en,efg2.p16en
[row=13] ,,D2,PPU810E,p16en,efg2.p16en
[row=14] ,,D3,L20D,gn9de,efg2.GN9De.cn8
[row=15] 上海,"可用区B【加白】
标签：zone_id-shanghai-b",B1,L20Y,gu8xf-C48v,efg2.C48vNHmcn
[row=16] ,,,L20Y,gu8xf-C48v2,efg2.C48vNHm2cn
[row=17] ,,B2,L20Z,gu8xf-C48emr,efg2.C48emrNHxcn
[row=18] ,,B3,L20X,gs8xf-C48emr,efg2.C48emrNH2bn
[row=19] ,,B4,L20X,gs8xf-e,efg2.NH2cn
[row=20] ,,B5,L20Z,gu8ef-e,efg2.NHxcn
[row=21] ,,B6,L20X,gs8xf-e,efg2.NH2cn
[row=22] ,"可用区C【加白】
标签：zone_id-shanghai-c",C1,L20X,gs8xf-e,efg2.NH2cn
[row=23] ,,C2,L20D,gn9d,efg2.GN9D.cn8
[row=24] ,,,L20D,"gn9dz【加白】
标签：code-gn9dz",efg2.GN9Dz.cn8
[row=25] ,可用区F,F1,H20-3e,gu8tef,efg2.C48eNH3ebn
[row=26] ,"可用区N【加白可见】
标签：zone_id-shanghai-n",N2,L20X,gs8xf-e,efg2.NH2cn
[row=27] ,,N4,L20C,gn9cx.cn8,efg2.GN9Cx.cn8
[row=28] "河源【加白】
河源标签：bcc-region-heyuan","蚂蚁可用区A
",A1,H20,gu8tf,efg2.C48vNHsbn
[row=29] ,,,H20-3e,gu8tef,efg2.C48eNH3ebn
[row=30] ,"蚂蚁可用区C
",C1,A100-80G,gu7ef-80G-机型2,efg1.nvga1n
[row=31] ,,,A800,gu7xf-80G-机型2,efg1.nvga8n
[row=32] ,,,PPU810,P888,efg2.p8bn
[row=33] 新加坡,"可用区A
【时长展示：12/36个月】",A1,A100-80G,gu7ef-80G-机型2,efg1.nvga1n
[row=34] ,,A2,H100,"gu8ef【加白】
标签：code-gu8ef",efg2.nvgh1bn
[row=35] ,,,H20,gu8tf,efg2.C48vNHsbn
[row=36] ,,,H20-3e,gu8tef,efg2.C48eNH3ebn
[row=37] ,,A3,H800,gu8xf-C56c,efg2.C56cNHmbn
[row=38] ,,A4,H100,gu8ef-C56c,efg2.C56cNHxbn
[row=39] ,,A5,H100,gu8ef-C56c,efg2.C56cNHxbn
[row=40] ,,A6,L20X（H200）,gx8sf,efg2.C56cNH2bn
[row=41] ,,A7,L20X（H200）,gs8xf-e,efg2.NH2cn
[row=42] ,,A8,L20X（H200）,gx8sf,efg2.C56cNH2bn
[row=43] ,,A9,L20A,gn9ax.ch72,efg3.GN9Ax.ch72
[row=44] ,,A10,L20A,gn9ax.ch72,efg3.GN9Ax.ch72
[row=45] ,,A11,L20A,gn9ax.ch72,efg3.GN9Ax.ch72
[row=46] ,,A12,H20-3e,gu8tef,efg2.C48eNH3ebn
[row=47] ,,A13,H20-3e,gu8tef,efg2.C48eNH3ebn
[row=48] 深圳,"可用区C【加白】
标签：zone_id-shenzhen-c",C2,L20X（H200）,gs8xf-e,efg2.NH2cn
[row=49] ,可用区D,D1,H20-3e,gu8tef,efg2.C48eNH3ebn
[row=50] 杭州,可用区B1,B1,H20,gu8tf,efg2.C48vNHsbn
[row=51] ,,,PPU810E,"p16en【仅加白可见】
标签：p16en",efg2.p16en
[row=52] ,,B2,L20X,gs8xf-d,efg2.D48NH2cn
[row=53] ,,B3,L20X,gs8xf-e,efg2.NH2cn
[row=54] ,可用区F,F1,H20-3e,gu8tef,efg2.C48eNH3ebn
[row=55] 北京,可用区D,D1,PPU810E,"p16en【加白】
标签：p16en",efg2.p16en
[row=56] ,,,H20,gu8tf,efg2.C48vNHsbn
[row=57] ,,D2,H20-3e,gu8tef,efg2.C48eNH3ebn
[row=58] ,可用区I,I1,L20X,gs8xf-e,efg2.NH2cn
[row=59] ,,I2,H20-3e,gu8tef,efg2.C48eNH3ebn
[row=60] ,,I3,H20,gu8tf,efg2.C48vNHsbn
[row=61] ,,,H20-3e,gu8tef,efg2.C48eNH3ebn
[row=62] ,,I4,L20D,gn9d,efg2.GN9D.cn8
[row=63] ,"可用区L
标签：zone_id-beijing-l",L1,L20C,gn9c.cn8,efg2.GN9C.cn8
[row=64] ,,,L20C,gn9cx.cn8,efg2.GN9Cx.cn8
[row=65] "法兰克福【需加白】
标签：bcc-region-eu-central-1",可用区C,C1,H20-3e,gu8tef,efg2.C48eNH3ebn
[row=66] 香港,可用区D,D1,H20-3e,gu8tef,efg2.C48eNH3ebn
[row=67] ,,D2,H20-3e,gu8tef,efg2.C48eNH3ebn
[row=68] "泰国【加白】
标签：bcc-region-southeast-7",可用区A,A1,L20A,gn9a.ch72,efg3.GN9A.ch72
[row=69] "美国亚特兰大【加白】
标签：bcc-region-us-southeast-1",可用区A,A1,L20X（H200）,gn8x.cn8,efg2.GN8X.cn8
[row=70] ,,A2,L20X（H200）,gn8x.cn8,efg2.GN8X.cn8
[row=71] 马来西亚,"可用区A【加白】
标签：zone_id-ap-southeast-3a",A1,L20D,gn9d,efg2.GN9D.cn8
[row=72] ,可用区B,B1,H20-3e,gu8tef,efg2.C48eNH3ebn
[row=73] 迪拜,可用区A,A1,H20-3e,gu8tef,efg2.C48eNH3ebn
[row=74] "中卫【加白】
标签：bcc-region-zhongwei",可用区A,A1,L20D,gn9dx,efg2.GN9Dx.cn8
[row=75] ,,,L20D,gn9dw,efg2.GN9Dw.cn8
[row=76] ,,A2,L20D,gn9dq,efg2.GN9Dq.cn8
[row=77] "柔佛【加白】
标签：bcc-region-southeast-8",可用区A,A1,L20B,gn9b.ch72,efg3.GN9B.ch72
[row=78] "日本【加白】
标签：bcc-region-northeast-1",可用区E,E1,L20D,gn9dz,efg2.GN9Dz.cn8
[row=79] ,,,,,
[row=80] ,,,,,
[row=81] ,,,,,
[row=82] 灵骏裸金属商品 code：,,,,,
[row=83] 中国站：bccluster_eflocomputing_public_cn,,,,,
[row=84] 国际站：bccluster_eflocomputing_public_intl,,,,,
[row=85] ,,,,,
[row=86] ,,,,,
[row=87] ,,,,,
[row=88] ,,,,,
[row=89] ,,,,,
[row=90] ,,,,,
[row=91] ,,,,,
[row=92] ,,,,,
[row=93] ,,,,,
[row=94] ,,,,,
[row=95] ,,,,,
[row=96] ,,,,,
[row=97] ,,,,,
[row=98] ,,,,,
[row=99] ,,,,,
[row=100] ,,,,,
[row=101] ,,,,,
[row=102] PPU/H卡/B卡及以上规格系统盘使用云盘,,,,,
[row=103] 系统盘是云盘，配置折扣方法：选择“按照计费项优惠”，然后选择“系统盘（云盘）systemdisk”，模块名称选择“地域”，不要选择“可用区”和”节点型号“。,,,,,
[row=104] ,,,,,
[row=105] ,,,,,
[row=106] ,,,,,
[row=107] ,,,,,
[row=108] ,,,,,
[row=109] ,,,,,
[row=110] ,,,,,
[row=111] ,,,,,
[row=112] ,,,,,
[row=113] ,,,,,
[row=114] ,,,,,
[row=115] ,,,,,
[row=116] ,,,,,
[row=117] ,,,,,
[row=118] ,,,,,
[row=119] ,,,,,
[row=120] ,,,,,
[row=121] ,,,,,
[row=122] ,,,,,
[row=123] ,,,,,
[row=124] ,,,,,
[row=125] 系统盘计费是按量计费，价格和通用计算中的云盘一致。,,,,,
[row=126] 和灵骏加速计算节点的计费在同一个商品 code 下，价格详情：https://www.aliyun.com/price/product#/commodity/disk,,,,,
[row=127] 由于灵骏加速计算节点采用固费分期，系统盘采用按量付费，每小时进行扣费，如果扣费没有成功，会触发灵骏加速计算节点停服。,,,,,
[row=128] ,,,,,
[row=129] ,,,,,
[row=130] A100及A800产品系统盘使用本地SATA盘,,,,,
[row=131] A100及A800系统盘使用本地sata硬盘，不需要单独购买云盘装系统，但需要单独配置灵骏连接产品打通VPC，可以看做是CEN专线的一种产品形态,,,,,
[row=132] ,,,,,
[row=133] 名称,商品名称（商品code）,商业模式,备注,,
[row=134] 灵骏链接,灵骏连接 bccluster_cloudconnectionpre_public_cn,预付费,列表价默认1G带宽5000元/月，可按日提升/降低带宽大小,,
```

## Sheet 2：列表价明细（sheetId=`st-9936411f-53171`，range=A1:N99）

```csv
[row=1] 地域,可用区,形态,集群编号,机型(不显示）,节点,模块值,固费分期,,,,,,备注
[row=2] 乌兰察布,,,,,,,月单价,半年月价,一年月价,两年月价,三年月价,四年月价,上架时间
[row=3] ,可用区A,实例,A1,A100-80G,gu7ef-80G-机型2,efg1.nvga1n,"¥153,258","¥131,366","¥114,939","¥91,958","¥76,629","¥59,465","2024/3/1（1/3年时长）
2023/11/24"
[row=4] ,,,,A800,gu7xf-80G-机型2,efg1.nvga8n,"¥137,932","¥118,229","¥103,445","¥82,762","¥68,966","¥53,519","2024/3/1（1/3年时长）
2023/11/24"
[row=5] ,,,A2,H800,gu8xf-机型2,efg2.nvgh8bn,"¥407,973","¥349,696","¥305,968","¥244,793","¥203,987","¥158,297","2026/4/16 调价
2024/3/1（1/3年时长）
2023/11/24"
[row=6] ,,AmazingPod-512,A2,H800,gu8xf-机型2,efg2.nvgh8bn,"¥26,110,290","¥22,380,547","¥19,581,943","¥15,666,732","¥13,055,145","¥10,131,011","2024/3/1（1/3年时长）
2023/11/24"
[row=7] ,,实例,A3,H20,gu8tf,efg2.C48vNHsbn,"¥169,316",,"¥124,717",,"¥84,618","¥74,651",2024/10/23 新增
[row=8] ,,,,H20-3e,gu8tef,efg2.C48eNH3ebn,"¥194,713",,"¥143,425",,"¥97,311","¥85,848",2025/6/27 新增
[row=9] ,,,,PPU810E,"p16en【加白】
标签：p16en",efg2.p16en,"¥184,215",,"¥138,155",,"¥92,108","¥71,478",2025/8/1 新增
[row=10] ,,,"A5【加白】
标签：hpn-zone-wlcb-a5",L20C,gn9c.cn8,efg2.GN9C.cn8,"¥776,781",,"¥582,563",,"¥388,391","¥301,398",2025/8/27新增
[row=11] ,可用区B,实例,B1,A100-40G,gu7ef-40G,efg1.nvga4,"¥127,596","¥109,376","¥95,696","¥76,566","¥63,798","¥49,508","2024/3/1（1/3年时长）
2023/11/24"
[row=12] ,,,,A100-80G,gu7ef-80G-机型1,efg1.nvga1,"¥153,258","¥131,366","¥114,939","¥91,958","¥76,629","¥59,465","2024/3/1（1/3年时长）
2023/11/24"
[row=13] ,,,,A100-80G,"gu7ef-80G-机型2
【仅研发uid：1111156667137893可见】",efg1.nvga1n,"¥153,258","¥131,366","¥114,939","¥91,958","¥76,629","¥59,465","2024/3/1（1/3年时长）
2023/11/24"
[row=14] ,可用区C,实例,C1,H800,gu8xf-机型2,efg2.nvgh8bn,"¥407,973","¥349,696","¥305,968","¥244,793","¥203,987","¥158,297","2026/4/16 调价
2024/3/1（1/3年时长）
2023/11/24"
[row=15] ,,,,L20Y（H800）,"gu8xf-C48c【加白】
专属云标签：exclusivecloud",efg2.C48cNHmcn,"¥407,973","¥349,696","¥305,968","¥244,793","¥203,987","¥158,297","2026/4/16 调价
2024/4/28 新增"
[row=16] ,,,,H20,gu8tf,efg2.C48vNHsbn,"¥169,316",,"¥124,717",,"¥84,618","¥74,651",2024/7/15 新增
[row=17] ,,,,H20,gu8tf,efg2.C48vNHsbn,"¥169,316",,"¥124,717",,"¥84,618","¥74,651",2024/7/15 新增
[row=18] ,,,,H20-3e,gu8tef,efg2.C48eNH3ebn,"¥194,713",,"¥143,425",,"¥97,311","¥85,848",2025/4/11 新增
[row=19] ,,,"C3【加白】
标签：p16en",PPU810E,p16en,efg2.p16en,"¥184,215","¥157,900","¥138,155","¥110,533","¥92,108","¥71,478",2024/10/6 新增
[row=20] ,,AmazingPod-1088,C1,H800,gu8xf-机型2,efg2.nvgh8bn,"¥55,484,366","¥47,558,663","¥41,611,629","¥33,291,804","¥27,742,183","¥21,528,397","2024/3/1（1/3年时长）
2023/11/24"
[row=21] ,,,,L20Y（H800）,"gu8xf-C48c【加白】
专属云标签：exclusivecloud",efg2.C48cNHmcn,"¥55,484,366","¥47,558,663","¥41,611,629","¥33,291,804","¥27,742,183","¥21,528,397","2026/4/16 调价
2024/4/28 新增"
[row=22] ,"可用区D
标签：zone_id-wulanchabu-d",实例,D1,PPU810E,p16en,efg2.p16en,"¥184,215",,"¥138,155",,"¥92,108","¥71,478",2025/12/8 新增
[row=23] ,,,D2,PPU810E,p16en,efg2.p16en,"¥184,215",,"¥138,155",,"¥92,108","¥71,478",2026/3/13 新增
[row=24] ,,,"D3【加白】
标签：hpn-zone-wulanchabu-d3",L20D,gn9de,efg2.GN9De.cn8,"¥916,600",,"¥687,400",,"¥458,300","¥355,600",2026/4/3 新增
[row=25] ,,,"D99【加白】
标签：hpn-zone-wulanchabu-d99",L20P,gn9p,efg.GN9P.n8,"¥270,225",,"¥199,046",,"¥135,050","¥119,142",2026/6/25 新增
[row=26] 上海,"可用区B【加白】
标签：zone_id-shanghai-b",实例,B1,L20Y（H800）,gu8xf-C48v,efg2.C48vNHmcn,"¥456,930","¥391,660","¥342,684","¥274,168","¥228,465","¥177,293","2026/4/16 调价
2024/5/10 新增"
[row=27] ,,,,L20Y（H800）,gu8xf-C48v2,efg2.C48vNHm2cn,"¥456,930","¥391,660","¥342,684","¥274,168","¥228,465","¥177,293","2026/4/16 调价
2024/6/20 新增"
[row=28] ,,,"B2【加白】
标签：SH-B-B2-group",L20Z,gu8xf-C48emr,efg2.C48emrNHxcn,"¥377,628","¥323,686","¥283,210","¥226,585","¥188,814","¥146,523",2024/7/15 新增
[row=29] ,,,"B3【加白】
标签：hpn-zone-shanghai-b3",L20X,gs8xf-C48emr,efg2.C48emrNH2bn,"¥456,930","¥391,660","¥342,684","¥274,168","¥228,465","¥177,293",2025/01/08 新增
[row=30] ,,,"B4【加白】
标签：hpn-zone-shanghai-b4",L20X,gs8xf-e,efg2.NH2cn,"¥456,930",,"¥342,684",,"¥228,465","¥177,293",2025/6/20 新增
[row=31] ,,,"B5【加白】
标签：hpn-zone-shanghai-b5",L20Z,gu8ef-e,efg2.NHxcn,"¥415,391",,"¥311,531",,"¥207,695","¥161,175",2025/7/10 新增
[row=32] ,,,"B6【加白】
标签：hpn-zone-shanghai-b6",L20X,gs8xf-e,efg2.NH2cn,"¥456,930",,"¥342,684",,"¥228,465","¥177,293",2025/7/30 新增
[row=33] ,"可用区C【加白】
标签：zone_id-shanghai-c",实例,C1,L20X,gs8xf-e,efg2.NH2cn,"¥456,930",,"¥342,684",,"¥228,465","¥177,293",2026/1/23 新增
[row=34] ,,,"C2【加白】
标签：hpn-zone-shanghai-c2",L20D,gn9d,efg2.GN9D.cn8,"¥916,600",,"¥687,400",,"¥458,300","¥355,600",2026/1/23 新增
[row=35] ,,,,L20D,"gn9dz【加白】
标签：code-gn9dz",efg2.GN9Dz.cn8,"¥916,600",,"¥687,400",,"¥458,300","¥355,600",2026/6/1 新增
[row=36] ,可用区F,实例,F1,PPU810E,"p16en【加白】
标签：p16en",efg2.p16en,"¥184,215","¥157,900","¥138,155","¥110,533","¥92,108","¥71,478",2025/01/08 新增
[row=37] ,,,,H20,gu8tf,efg2.C48vNHsbn,"¥180,903",,"¥133,252",,"¥90,410","¥79,760",2025/01/08 新增
[row=38] ,,,,H20-3e,gu8tef,efg2.C48eNH3ebn,"¥208,039",,"¥153,240",,"¥103,972","¥91,724",2025/4/11 新增
[row=39] ,可用区N,实例,N1,H20,gu8tf,efg2.C48vNHsbn,"¥180,903",,"¥133,252",,"¥90,410","¥79,760",2024/12/4 新增
[row=40] ,,,"N2【加白】
标签：hpn-zone-shanghai-n2",L20X,gs8xf-e,efg2.NH2cn,"¥456,930",,"¥342,684",,"¥228,465","¥177,293",2025/6/20 新增
[row=41] ,,,N3,H20-3e,gu8tef,efg2.C48eNH3ebn,"¥208,039",,"¥153,240",,"¥103,972","¥91,724",2025/8/1 新增
[row=42] ,,,"N4【加白】
标签：hpn-zone-shanghai-n4",L20C,gn9cx.cn8,efg2.GN9Cx.cn8,"¥776,781",,"¥582,563",,"¥388,391","¥301,398",2025/11/12 新增
[row=43] ,"可用区O【加白】
标签：zone_id-shanghai-o",实例,O1,PPU810E,p16en,efg2.p16en,"¥184,215","¥157,900","¥138,155","¥110,533","¥92,108","¥71,478",2025/4/2 新增
[row=44] 新加坡,"可用区A
【时长展示：1/12/36个月】",实例,A1,A100-80G,gu7ef-80G-机型2,efg1.nvga1n,"¥256,887","¥220,192","¥192,658","¥154,137","¥128,443","¥99,673","2024/3/1（1/3年时长）
2023/11/24"
[row=45] ,,,A2,H100,"gu8ef【加白】
标签：code-gu8ef",efg2.nvgh1bn,"¥642,218",,"¥400,896",,"¥287,026","¥223,667","2024/3/1（1/3年时长）
2024/1/25"
[row=46] ,,,,H20,gu8tf,efg2.C48vNHsbn,"¥240,848",,"¥177,407",,"¥120,368","¥106,190",2024/12/26 新增
[row=47] ,,,,H20-3e,gu8tef,efg2.C48eNH3ebn,"¥301,656",,"¥222,198",,"¥150,759","¥133,000",2025/4/11 新增
[row=48] ,,,"A3【加白】
马来标签：region-Malaysia",L20Y（H800）,gu8xf-C56c,efg2.C56cNHmbn,"¥591,302",,"¥443,459",,"¥295,651","¥229,431","2026/4/16 调价
2024/7/25 新增"
[row=49] ,,,"A4【加白】
马来标签：region-Malaysia",L20Z,gu8ef-C56c,efg2.C56cNHxbn,"¥642,218",,"¥400,896",,"¥287,026","¥223,667",2024/9/6 新增
[row=50] ,,,"A5【加白】
马来标签：region-Malaysia",L20Z,gu8ef-C56c,efg2.C56cNHxbn,"¥642,218",,"¥400,896",,"¥287,026","¥223,667",2024/9/6 新增
[row=51] ,,,"A6【加白】
标签：hpn-zone-southeast-a6",L20X,gx8sf,efg2.C56cNH2bn,"¥591,302",,"¥443,459",,"¥295,651","¥229,431",2024/12/26 新增
[row=52] ,,,"A7【加白】
标签：hpn-zone-southeast-a7",L20X,gs8xf-e,efg2.NH2cn,"¥591,302",,"¥443,459",,"¥295,651","¥229,431",2025/6/20 新增
[row=53] ,,,"A8【加白】
标签：hpn-zone-southeast-a8",L20X,gx8sf,efg2.C56cNH2bn,"¥591,302",,"¥443,459",,"¥295,651","¥229,431",2025/6/20 新增
[row=54] ,,"超节点实例【加白】
标签：Hypernode",A9,L20A,gn9ax.ch72,efg3.GN9Ax.ch72,"¥10,600,000",,"¥8,000,000",,"¥5,300,000","¥4,100,000","2025/10/23（定价更改）
2025/10/11 新增"
[row=55] ,,,A10,L20A,gn9ax.ch72,efg3.GN9Ax.ch72,"¥10,600,000",,"¥8,000,000",,"¥5,300,000","¥4,100,000",2025/11/17 新增
[row=56] ,,,"A11【加白】
标签：hpn-zone-southeast-a11",L20A,gn9ax.ch72,efg3.GN9Ax.ch72,"¥10,600,000",,"¥8,000,000",,"¥5,300,000","¥4,100,000",2026/4/15 新增
[row=57] ,,实例,A12,H20-3e,gu8tef,efg2.C48eNH3ebn,"¥301,656",,"¥222,198",,"¥150,759","¥133,000",2026/3/26 新增
[row=58] ,,,A13,H20-3e,gu8tef,efg2.C48eNH3ebn,"¥301,656",,"¥222,198",,"¥150,759","¥133,000",2026/4/23 新增
[row=59] 深圳,"可用区C【加白】
标签：zone_id-shenzhen-c",实例,C1,L20Y（H800）,gu8xf-C56,efg2.C56NHmcn,"¥468,287",,"¥351,201",,"¥234,143","¥181,700","2026/4/16 调价
2024/8/28"
[row=60] ,,,,L20Y（H800）,gu8xf-D48v,efg2.D48vNHmcn,"¥468,287",,"¥351,201",,"¥234,143","¥181,700","2026/4/16 调价
2024/11/14"
[row=61] ,,,,L20Y（H800）,gu8xf-48v,efg2.48vNHmcn,"¥468,287",,"¥351,201",,"¥234,143","¥181,700","2026/4/16 调价
2024/11/14"
[row=62] ,,,,L20Y（H800）,gu8xf-56,efg2.56NHmcn,"¥468,287",,"¥351,201",,"¥234,143","¥181,700","2026/4/16 调价
2024/11/14"
[row=63] ,,,C2,L20X,gs8xf-e,efg2.NH2cn,"¥456,930","¥391,660","¥342,684","¥274,168","¥228,465","¥177,293",2025/6/10 新增
[row=64] ,可用区D,实例,D1,H20-3e,gu8tef,efg2.C48eNH3ebn,"¥208,039",,"¥153,240",,"¥103,972","¥91,724",2025/4/11 新增
[row=65] ,,,A2,H20-3e,gu8tef,efg2.C48eNH3ebn,"¥194,713",,"¥143,425",,"¥97,311","¥85,848",2025/08/14 新增
[row=66] 杭州,,,,H20,gu8tf,efg2.C48vNHsbn,"¥180,903",,"¥133,252",,"¥90,410","¥79,760",2025/01/08 新增
[row=67] ,,,,PPU810E,"p16en【仅加白可见】
标签：p16en",efg2.p16en,"¥184,215","¥157,900","¥138,155","¥110,533","¥92,108","¥71,478",2025/03/12 新增
[row=68] ,,,"B2【加白】
标签：hpn-zone-hangzhou-b2",L20X,gs8xf-d,efg2.D48NH2cn,"¥456,930",,"¥342,684",,"¥228,465","¥177,293",2025/7/10 新增
[row=69] ,,,"B3【加白】
标签：hpn-zone-hangzhou-b3",L20X,gs8xf-e,efg2.NH2cn,"¥456,930",,"¥342,684",,"¥228,465","¥177,293",2025/6/20 新增
[row=70] ,可用区F,实例,F1,H20-3e,gu8tef,efg2.C48eNH3ebn,"¥208,039",,"¥153,240",,"¥103,972","¥91,724",2025/4/11 新增
[row=71] ,"蚂蚁可用区J【加白】
标签：zone_id-hangzhou-j-alipay",实例,J1,PPU810E,p16en,efg2.p16en,"¥350,009",,"¥262,495",,"¥175,004","¥135,807",2025/7/30 新增
[row=72] 北京,可用区D,实例,D1,PPU810E,"p16en【加白】
标签：p16en",efg2.p16en,"¥184,215","¥157,900","¥138,155","¥110,533","¥92,108","¥71,478",2025/01/08 新增
[row=73] ,,,,H20,gu8tf,efg2.C48vNHsbn,"¥180,903",,"¥133,252",,"¥90,410","¥79,760",2025/01/08 新增
[row=74] ,,,D2,H20-3e,gu8tef,efg2.C48eNH3ebn,"¥208,039",,"¥153,240",,"¥103,972","¥91,724",2025/4/11 新增
[row=75] ,可用区I,实例,"I1 怀来【加白】
标签：hpn-zone-beijing-i1",L20X,gs8xf-e,efg2.NH2cn,"¥456,930",,"¥342,684",,"¥228,465","¥177,293",2025/6/20 新增
[row=76] ,,,I2,H20-3e,gu8tef,efg2.C48eNH3ebn,"¥208,039",,"¥153,240",,"¥103,972","¥91,724",2025/9/10 新增
[row=77] ,,,I3,H20,gu8tf,efg2.C48vNHsbn,"¥180,903",,"¥133,252",,"¥90,410","¥79,760",2025/9/15 新增
[row=78] ,,,,H20-3e,gu8tef,efg2.C48eNH3ebn,"¥208,039",,"¥153,240",,"¥103,972","¥91,724",2025/9/10 新增
[row=79] ,,,"I4【加白】
标签：hpn-zone-beijing-i4",L20D,gn9d,efg2.GN9D.cn8,"¥916,600",,"¥687,400",,"¥458,300","¥355,600",2026/2/25 新增
[row=80] ,"可用区L【加白】
标签：zone_id-beijing-l",实例,L1,L20C,gn9c.cn8,efg2.GN9C.cn8,"¥776,781",,"¥582,563",,"¥388,391","¥301,398",2025/12/23 新增
[row=81] ,,,,L20C,gn9cx.cn8,efg2.GN9Cx.cn8,"¥776,781",,"¥582,563",,"¥388,391","¥301,398",2026/5/1 新增
[row=82] "法兰克福【加白】
标签：bcc-region-eu-central-1",可用区C,实例,C1,H20-3e,gu8tef,efg2.C48eNH3ebn,"¥312,058",,"¥229,860",,"¥155,958","¥137,586",2025/4/11 新增
[row=83] ,可用区D,实例,D1,H20-3e,gu8tef,efg2.C48eNH3ebn,"¥280,852",,"¥206,874",,"¥140,362","¥123,827",2025/4/11 新增
[row=84] ,,,D2,H20-3e,gu8tef,efg2.C48eNH3ebn,"¥280,852",,"¥206,874",,"¥140,362","¥123,827",2025/12/8 新增
[row=85] "泰国【加白】
标签：bcc-region-southeast-7",可用区A,"超节点实例【加白】
标签：Hypernode",A1,L20A,gn9a.ch72,efg3.GN9A.ch72,"¥10,600,000",,"¥8,000,000",,"¥5,300,000","¥4,100,000","2025/10/23（定价更改）
2025/9/16 新增"
[row=86] ,,实例,A1,L20D,gn9d,efg2.GN9D.cn8,"¥1,044,924",,"¥783,636",,"¥522,462","¥405,384",2026/6/30 新增
[row=87] "美国亚特兰大【加白】
标签：bcc-region-us-southeast-1",可用区A,实例,A1,L20X,gn8x.cn8,efg2.GN8X.cn8,"¥591,302",,"¥443,459",,"¥295,651","¥229,431",2025/10/03 新增
[row=88] ,,,A2,L20X,gn8x.cn8,efg2.GN8X.cn8,"¥591,302",,"¥443,459",,"¥295,651","¥229,431",2026/2/25 新增
[row=89] 马来西亚,"可用区A【加白】
标签：zone_id-ap-southeast-3a",实例,A1,L20D,gn9d,efg2.GN9D.cn8,"¥1,044,924",,"¥783,636",,"¥522,462","¥405,384",2026/3/18 新增
[row=90] ,可用区B,实例,B1,H20-3e,gu8tef,efg2.C48eNH3ebn,"¥285,013",,"¥209,939",,"¥142,442","¥125,662",2025/10/22 新增
[row=91] 迪拜,可用区A,实例,A1,H20-3e,gu8tef,efg2.C48eNH3ebn,"¥374,469",,"¥275,832",,"¥187,150","¥165,103",2025/10/22 新增
[row=92] "中卫【加白】
标签：bcc-region-zhongwei",可用区A,实例,A1,L20D,gn9dx,efg2.GN9Dx.cn8,"¥916,600",,"¥687,400",,"¥458,300","¥355,600",2026/1/23 新增
[row=93] ,,,,L20D,gn9dw,efg2.GN9Dw.cn8,"¥916,600",,"¥687,400",,"¥458,300","¥355,600",2026/4/20新增
[row=94] ,,,"A2【加白】
标签：hpn-zone-zhongwei-a2",L20D,gn9dq,efg2.GN9Dq.cn8,"¥916,600",,"¥687,400",,"¥458,300","¥355,600",2026/5/19新增
[row=95] "柔佛【加白】
标签：bcc-region-southeast-8",可用区A,超节点实例,A1,L20B,gn9b.ch72,efg3.GN9B.ch72,"¥13,250,000",,"¥10,000,000",,"¥6,625,000","¥5,125,000",2026/4/20新增
[row=96] "日本【加白】
标签：bcc-region-northeast-1",可用区E,实例,E1,L20D,gn9dz,efg2.GN9Dz.cn8,"¥962,000",,"¥721,400",,"¥480,900","¥373,200",2026/5/1 新增
[row=97] ,,,,PPU810,pxen,efg2.pxen,"¥257,495",,"¥193,113",,"¥128,748",,2025/12/5 新增
[row=98] "上海金融云【加白】
标签：bcc-region-shanghai-finance-1",可用区Z,实例,Z1,PPU810E,p16en,efg2.p16en,"¥350,009","¥300,010","¥262,495","¥210,012","¥175,004","¥135,807",2025/6/10 新增
[row=99] "北京政务云【加白】
标签：bcc-region-north-2-gov-1",可用区B,实例,B1,PPU810E,"p16en【仅加白可见】
标签：p16en",efg2.p16en,"¥368,430",,"¥276,310",,"¥184,215","¥142,955",2025/9/22 新增
```

## Sheet 3：灵骏实例规格配置（sheetId=`st-1868fd7e-13856`，range=A1:I24）

```csv
[row=1] 卡型,Commonbuy规格,实例规格（模块值）,CPU,内存(未考虑满插降频),GPU,硬盘,网卡,售卖Region/可用区/集群编号/IAAS架构
[row=2] 8卡A100-80G,gu7ef-80G-机型1,efg1.nvga1,2xIntel Icelake 8369B 32C CPU,32x64GB DDR4 3200 Memory,8xNVIDIA SXM4 80GB A100 GPU,"2x480GB SATA SSD

4x3.84TB NVMe SSD","1x 25Gbps DP Ethernet NIC

4x100Gbps DP RoCE NIC","乌兰/可用区B/B1【HPN6.0, NIC mode】"
[row=3] 8卡A100-80G,gu7ef-80G-机型2,efg1.nvga1n,2xIntel Icelake 8369B 32C CPU,32x64GB DDR4 3200 Memory,8xNVIDIA SXM4 80GB A100 GPU,"2x480GB SATA SSD

4x3.84TB NVMe SSD","1x100Gbps DP NIC for VPC

4x100Gbps DP RoCE NIC","乌兰/可用区A/A1【HPN6.2, NIC mode】

新加坡/可用区A/A1【HPN7.0，NIC mode】

河源/蚂蚁专属C/C1【HPN6.2, NIC mode】"
[row=4] 8卡A100-40G,gu7ef-40G机型,efg1.nvga4,2x Intel Icelake 8369B 32C CPU,16x 64GB DDR4 3200 Memory,8x NVIDIA SXM4 40GB A100 GPU,"1x 480GB SATA SSD

2x 3.84TB NVMe SSD","1x 25Gbps DP Ethernet NIC

2x 100Gbps DP RoCE NIC","乌兰/可用区B/B1【HPN6.0, NIC mode】"
[row=5] 8卡A800-80G,gu7xf-80G-机型2,efg1.nvga8n,2xIntel Icelake 8369B 32C CPU,32x64GB DDR4 3200 Memory,8xNVIDIA SXM4 80GB A800 GPU,"2x480GB SATA SSD

4x3.84TB NVMe SSD","1x100Gbps DP NIC for VPC

4x100Gbps DP RoCE NIC","乌兰/可用区A/A1【HPN6.2, NIC mode】

河源/蚂蚁专属C/C1【HPN6.2, NIC mode】"
[row=6] 8卡H800-80G,gu8xf-机型2,efg2.nvgh8bn,2x Intel Saphhire Rapid 8469C 48C CPU,32x 64GB DDR5 4800 Memory,8x NVIDIA SXM5 80GB H800 GPU,4x 3.84TB NVMe SSD,"1x 200Gbps Dual Port BF3 DPU for VPC

8x 200Gbps Dual Port RoCE BF3","乌兰/可用区A/A2 【HPN6.2多轨, NIC mode】

乌兰/可用区C/C1【HPN7.0, DPU mode】"
[row=7] "8卡H100

【加白可见】",gu8ef-机型,efg2.nvgh1bn,2x Intel Saphhire Rapid 8469C 48C CPU,32x 64GB DDR5 4800 Memory,8x NVIDIA SXM5 80GB H800 GPU,"
4x 3.84TB NVMe SSD","1x 200Gbps Dual Port BF3 DPU for VPC

8x 200Gbps Dual Port RoCE BF3","新加坡/可用区A/A2【HPN7.0，NIC mode】

新加坡/可用区A/A2【HPN7.0，DPU mode】

新加坡/蚂蚁专属B/B1【HPN6.2，DPU mode】"
[row=8] "8卡L20Y

【特殊客户加白】",gu8xf-C48c,efg2.C48cNHmcn,2x Intel Saphhire Rapid 8469C 48C CPU,32x 64GB DDR5 4800 Memory,8* L20Y,"
4x 3.84TB NVMe SSD","1x 200Gbps Dual Port BF3 DPU for VPC

8x 200Gbps Dual Port RoCE CX7","乌兰/可用区C/C1【HPN7.0, DPU mode】"
[row=9] ,gu8xf-C48v,efg2.C48vNHmcn,2x Intel Saphhire Rapid 8468V 48C CPU,32x 64GB DDR5 4800 Memory,8* L20Y,"
4x 3.84TB NVMe SSD","1x 200Gbps Dual Port BF3 DPU for VPC

8x 200Gbps Dual Port RoCE CX7","上海/可用区B/B1【HPN7.0, DPU mode】"
[row=10] ,gu8xf-C48v2,efg2.C48vNHm2cn,2x Intel Saphhire Rapid 8468V 48C CPU,32x 64GB DDR5 4800 Memory,8* L20Y,"
4x 3.84TB NVMe SSD","1x 200Gbps Dual Port BF3 DPU for VPC

8x 200Gbps Dual Port RoCE CX7","上海/可用区B/B1【HPN7.0, DPU mode】"
[row=11] ,gu8xf-C56C,efg2.C56cNHmbn,2x Intel Saphhire Rapid 8480C 56C CPU,32x 64GB DDR5 4800 Memory,8* L20Y,"
4x 3.84TB NVMe SSD","1x 200Gbps Dual Port BF3 DPU for VPC

8x 200Gbps Dual Port RoCE BF3",新加坡/可用区A/A3【HPN7.0，DPU mode】
[row=12] ,gu8xf-C56,efg2.C56NHmcn,2x Intel Saphhire Rapid 8480+ 56C CPU,32x 64GB DDR5 4800 Memory,,"
4x 3.84TB NVMe SSD","1x 200Gbps Dual Port BF3 DPU for VPC

8x 200Gbps Dual Port RoCE CX7",深圳/可用区C/C1【HPN7.0，DPU mode】
[row=13] "8卡L20Z

【特殊客户加白】",gu8xf-C48emr,efg2.C48emrNHxcn,2x Intel EMR 8558 48C CPU,32x 64GB DDR5 4800 Memory,8* L20Z,"
4x 3.84TB NVMe SSD","1x 200Gbps Dual Port BF3 DPU for VPC

8x 200Gbps Dual Port RoCE CX7","上海/可用区B/B2【HPN7.0, DPU mode】"
[row=14] ,gu8ef-e,efg2.NHxcn,2x Intel EMR 8558 48C CPU,32x 64GB DDR5 4800 Memory,8* L20Z,4x 3.84TB NVMe SSD,"1x 200Gbps Dual Port BF3 DPU for VPC

8x 200Gbps Dual Port RoCE CX7","上海/可用区B/B5【HPN7.0, DPU mode】"
[row=15] ,gu8ef-C56c,efg2.C56cNHxbn,2x Intel Saphhire Rapid 8480C 56C CPU,32x 64GB DDR5 4800 Memory,8* L20Z,"
4x 3.84TB NVMe SSD","1x 200Gbps Dual Port BF3 DPU for VPC

8x 200Gbps Dual Port RoCE BF3L","新加坡/可用区A/A4【HPN7.0，DPU mode】

新加坡/可用区A/A5【HPN7.0，DPU mode】"
[row=16] "8卡L20X

【特殊客户加白】",gs8xf-C48emr,efg2.C48emrNH2bn (非自研),2x Intel EMR 8558 48C CPU,32x 64GB DDR5 5400 Memory,8* L20X,"
4x 3.84TB NVMe SSD","1x 200Gbps Dual Port BF3 DPU for VPC

8x 200Gbps Dual Port RoCE CX7","上海/可用区B/B3【HPN7.0, DPU mode】"
[row=17] ,gs8xf-e,efg2.NH2cn,2x Intel EMR 8558 48C CPU,32x 64GB DDR5 5400 Memory,8* L20X,"仅支持云盘OS启动

4x 3.84TB NVMe SSD","1x 200Gbps Dual Port BF3 DPU for VPC

8x 200Gbps Dual Port RoCE CX7","北京/可用区I/I1【HPN7.0+DC7.1, DPU mode】

杭州/可用区B/B3【HPN7.0+DC7.1, DPU mode】

上海/可用区B/B4【HPN7.0+DC7.1, DPU mode】

上海/可用区B/B6【HPN7.0+DC7.1, DPU mode】

上海/可用区N/N2【HPN7.0+DC7.1, DPU mode】

深圳/可用区C/C2【HPN7.0+DC7.1, DPU mode】

新加坡/可用区A/A7【HPN7.0+DC7.1, DPU mode】"
[row=18] ,"gs8xf-d

（DELL机型）",efg2.D48NH2bn,2x Intel EMR 8558 48C CPU,32x 64GB DDR5 5400 Memory,8* L20X,"仅支持云盘OS启动

不支持数据盘，不支持弹性ENI

4x 3.84TB NVMe SSD","1x 200Gbps Dual Port BF3 DPU for VPC

8x 200Gbps Dual Port RoCE CX7","杭州/可用区B/B2【HPN7.0+DC7.1, DPU mode】"
[row=19] ,gx8sf,efg2.C56cNH2bn,2x Intel Saphhire Rapid 8480C 56C CPU,32x 64GB DDR5 4800 Memory,8* L20X,"
4x 3.84TB NVMe SSD","1x 200Gbps Dual Port BF3 DPU for VPC

8x 200Gbps Dual Port RoCE BF3L","新加坡/可用区A/A6【HPN7.0，DPU mode】

新加坡/可用区A/A8【HPN7.0，DPU mode】"
[row=20] "8卡L20C

【特殊客户加白】",GN9C.cn8,efg2.GN9C.cn8,2x Intel GNR 6960P 64C CPU,24x 64GB DDR6 6400 Memory,8* L20C,8x 3.84TB NVMe SSD,"1x 200Gbps Dual Port BF3 DPU for VPC

8x 200Gbps Dual Port RoCE CX7","乌兰/可用区A/A5【HPN7.0+DC7.1, DPU mode】"
[row=21] PPU,p16en,efg2.p16en,2x Intel EMR 8575C 48C CPU,64G 5400MHz *32,16x OAM PPU810e,"
4x 3.84TB NVMe SSD","1x 200Gbps Dual Port BF3 DPU for VPC

4x 200Gbps Dual Port EIC RoCE NIC","乌兰/可用区C/C3【HPN7.0, DPU mode】

上海/可用区F/F1【HPN7.0, DPU mode】

杭州/可用区B/B1【HPN7.0, DPU mode】

北京/可用区D/D1【HPN7.0, DPU mode】"
[row=22] "8卡H20-96G
",gu8tf,efg2.C48vNHsbn,2x Intel Saphhire Rapid 8469C 48C CPU,64G 4800MHz *32,8* H20,"2x 480GB SATA SSD

4x 3.84TB NVMe SSD","1x 200Gbps Dual Port BF3 DPU for VPC

4x 200Gbps Dual Port BF3 RoCE NIC","河源/蚂蚁专属B/B1【HPN7.0, DPU mode】"
[row=23] ,gu8tf,efg2.C48vNHsbn,2x Intel Saphhire Rapid 8469C 48C CPU,64G 4800MHz *32,8* H20,"
4x 3.84TB NVMe SSD","1x 200Gbps Dual Port BF3 DPU for VPC

4x 200Gbps Dual Port BF3L RoCE NIC","河源/蚂蚁专属B/B1【HPN7.0, DPU mode】

乌兰/可用区C/C2【HPN7.0, DPU mode】

乌兰/可用区A/A3【HPN7.0, DPU mode】

上海/可用区N/N1【HPN7.0, DPU mode】

上海/可用区F/F1【HPN7.0, DPU mode】

杭州/可用区B/B1【HPN7.0, DPU mode】

北京/可用区D/D1【HPN7.0, DPU mode】

新加坡/可用区A/A2【HPN7.0，DPU mode】"
[row=24] "8卡H20-141G
",gu8tef,efg2.C48eNH3ebn,2x Intel EMR 8575C 48C CPU,64G 5400MHz *32,8* H20-3e,4x 3.84TB NVMe SSD,"1x 200Gbps Dual Port BF3 DPU for VPC

4x 200Gbps Dual Port BF3L RoCE NIC",
```
