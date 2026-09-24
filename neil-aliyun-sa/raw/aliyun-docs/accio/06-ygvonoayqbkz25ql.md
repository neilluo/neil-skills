# 权限与安全

> **来源**：Accio Work 知识库（公开语雀）
> **URL**：https://acciowork.yuque.com/rfmg8t/ieb85b/ygvonoayqbkz25ql
> **TOC 层级**：lvl2
> **SHA256**：69aa71a0ca842ce9e74a61b337acae82ad59054d00c0254247f0be55d240ef64
> **归档日期**：2026-08-10 ｜ **状态**：raw（不可变）

---

<font style="color:rgb(75, 85, 99);">Accio Work 提供精细的权限控制机制，确保 Agent 在安全可控的范围内执行任务。</font>

### **<font style="color:rgb(17, 24, 39);">权限策略有哪些类型？</font>**
| **策略** | **说明** |
| :--- | :--- |
| **<font style="color:rgb(17, 24, 39);">allow</font>** | <font style="color:rgb(75, 85, 99);">直接执行，无需确认</font> |
| **<font style="color:rgb(17, 24, 39);">ask</font>** | <font style="color:rgb(75, 85, 99);">每次执行前都需要你确认</font> |
| **<font style="color:rgb(17, 24, 39);">ask_once</font>** | <font style="color:rgb(75, 85, 99);">首次确认后，后续自动批准</font> |
| **<font style="color:rgb(17, 24, 39);">deny</font>** | <font style="color:rgb(75, 85, 99);">始终拒绝，不允许执行</font> |


### **<font style="color:rgb(17, 24, 39);">默认权限配置是什么？</font>**
| **操作类型** | **默认策略** |
| :--- | :--- |
| <font style="color:rgb(75, 85, 99);">文件读取</font> | <font style="color:rgb(75, 85, 99);">✅</font><font style="color:rgb(75, 85, 99);"> 通常允许</font> |
| <font style="color:rgb(75, 85, 99);">网络访问</font> | <font style="color:rgb(75, 85, 99);">✅</font><font style="color:rgb(75, 85, 99);"> 通常允许</font> |
| <font style="color:rgb(75, 85, 99);">文件写入</font> | <font style="color:rgb(75, 85, 99);">⚠️</font><font style="color:rgb(75, 85, 99);"> 通常需要确认</font> |
| <font style="color:rgb(75, 85, 99);">Shell 执行</font> | <font style="color:rgb(75, 85, 99);">⚠️</font><font style="color:rgb(75, 85, 99);"> 通常需要确认</font> |
| <font style="color:rgb(75, 85, 99);">浏览器使用</font> | <font style="color:rgb(75, 85, 99);">⚠️</font><font style="color:rgb(75, 85, 99);"> 通常需要确认</font> |


### **<font style="color:rgb(17, 24, 39);">可以为特定命令设置白名单吗？</font>**
<font style="color:rgb(75, 85, 99);">可以。你可以将常用的安全命令配置为自动允许，例如：</font>

+ `<font style="color:rgb(17, 24, 39);background-color:rgba(15, 23, 42, 0.06);">npm test</font>`
+ `<font style="color:rgb(17, 24, 39);background-color:rgba(15, 23, 42, 0.06);">npm run build</font>`
+ <font style="color:rgb(75, 85, 99);">其他你信任的命令</font>

### **<font style="color:rgb(17, 24, 39);">授权有效期有多长？</font>**
| **有效期** | **说明** |
| :--- | :--- |
| **<font style="color:rgb(17, 24, 39);">once</font>** | <font style="color:rgb(75, 85, 99);">仅当前操作有效</font> |
| **<font style="color:rgb(17, 24, 39);">session</font>** | <font style="color:rgb(75, 85, 99);">当前会话有效</font> |
| **<font style="color:rgb(17, 24, 39);">persistent</font>** | <font style="color:rgb(75, 85, 99);">永久有效，直到手动撤销</font> |


### **<font style="color:rgb(17, 24, 39);">Agent 可以在工作区之外访问文件吗？</font>**
<font style="color:rgb(75, 85, 99);">不可以。系统通过以下方式确保 Agent 只能在授权工作区内操作：</font>

+ **<font style="color:rgb(17, 24, 39);">路径白名单</font>**<font style="color:rgb(75, 85, 99);">：限制可访问的目录范围</font>
+ **<font style="color:rgb(17, 24, 39);">符号链接保护</font>**<font style="color:rgb(75, 85, 99);">：防止通过符号链接绕过限制</font>
+ **<font style="color:rgb(17, 24, 39);">边界检查</font>**<font style="color:rgb(75, 85, 99);">：确保所有文件操作不超出工作区</font>

### **<font style="color:rgb(17, 24, 39);">所有权限决策都有记录吗？</font>**
<font style="color:rgb(75, 85, 99);">有。无论自动还是手动产生的权限决策，都会被记录到</font>**<font style="color:rgb(17, 24, 39);">审计日志</font>**<font style="color:rgb(75, 85, 99);">中，便于追溯和排查问题。</font>

### **<font style="color:rgb(17, 24, 39);">如何设置敏感目录的黑名单？</font>**
<font style="color:rgb(75, 85, 99);">可以通过创建 </font>**<font style="color:rgb(17, 24, 39);">deny</font>**<font style="color:rgb(75, 85, 99);"> 规则，对特定工具和路径前缀进行限制。例如：禁止写入 </font>`<font style="color:rgb(17, 24, 39);background-color:rgba(15, 23, 42, 0.06);">/etc</font>`<font style="color:rgb(75, 85, 99);"> 目录。</font>

