---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/front-end-grayscale-plug-in
fetch_date: 2026-09-21
product: AI Gateway
slug: front-end-grayscale-plug-in
body_sha256: 1f82fc2feef7f0cf55510b9073a44670dcba1d835dbd9299f45b1eeb93906a10
body_bytes: 16020
migration_status: current
---

`frontend-gray`插件实现了前端用户灰度的功能，通过此插件，不但可以用于业务`A/B实验`，同时通过`可灰度`配合`可监控`、`可回滚`策略保证系统发布运维稳定性。  

## **运行属性**
插件执行阶段：`认证阶段` 插件执行优先级：`1000`

## 配置字段
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>grayKey</code></p></td> <td><p>string</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>用户ID的唯一标识，可以来自Cookie或者Header中，比如 userid，如果没有填写则使用<code>rules\[\].grayTagKey</code>和<code>rules\[\].grayTagValue</code>过滤灰度规则</p></td> </tr> <tr> <td><p><code>useManifestAsEntry</code></p></td> <td><p>boolean</p></td> <td><p>非必填</p></td> <td><p><code>false</code></p></td> <td><p>是否使用manifest作为入口。当设置为true时，系统将使用manifest文件作为应用入口，适用于微前端架构。在这种模式下，系统会根据manifest文件的内容来加载不同版本的前端资源。</p></td> </tr> <tr> <td><p><code>localStorageGrayKey</code></p></td> <td><p>string</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>使用JWT鉴权方式，用户ID的唯一标识来自<code>localStorage</code>中，如果配置了当前参数，则<code>grayKey</code>失效</p></td> </tr> <tr> <td><p><code>graySubKey</code></p></td> <td><p>string</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>用户身份信息可能以JSON形式透出，比如：<code>userInfo:{ userCode:"001" }</code>,当前例子<code>graySubKey</code>取值为<code>userCode</code></p></td> </tr> <tr> <td><p><code>storeMaxAge</code></p></td> <td><p>int</p></td> <td><p>非必填</p></td> <td><p><code>60 \* 60 \* 24 \* 365</code></p></td> <td><p>网关设置Cookie最大存储时长：单位为秒，默认为1年</p></td> </tr> <tr> <td><p><code>cookieDomain</code></p></td> <td><p>string</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>Cookie的Domain设置，可用于跨子域共享Cookie。例如：".example.com"</p></td> </tr> <tr> <td><p><code>indexPaths</code></p></td> <td><p>array of strings</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>强制处理的路径，支持\&nbsp;<code>Glob</code>\&nbsp;模式匹配。例如：在微前端场景下，XHR 接口如：\&nbsp;<code>/resource/\*\*/manifest-main.json</code>本质是一个资源请求，需要走插件转发逻辑。</p></td> </tr> <tr> <td><p><code>skippedPaths</code></p></td> <td><p>array of strings</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>用于排除特定路径，避免当前插件处理这些请求，支持\&nbsp;<code>Glob</code>\&nbsp;模式匹配。例如，在 rewrite 场景下，XHR 接口请求\&nbsp;<code>/api/\*\*</code>\&nbsp;如果经过插件转发逻辑，可能会导致非预期的结果。</p></td> </tr> <tr> <td><p><code>skippedByHeaders</code></p></td> <td><p>map of string to string</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>用于通过请求头过滤，指定哪些请求不被当前插件处理。<code>skippedPaths</code>\&nbsp;的优先级高于当前配置，且页面HTML请求不受本配置的影响。</p></td> </tr> <tr> <td><p><code>rules</code></p></td> <td><p>array of object</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>用户定义不同的灰度规则，适配不同的灰度场景</p></td> </tr> <tr> <td><p><code>rewrite</code></p></td> <td><p>object</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>重写配置，一般用于OSS/CDN前端部署的重写配置</p></td> </tr> <tr> <td><p><code>baseDeployment</code></p></td> <td><p>object</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>配置Base基线规则的配置</p></td> </tr> <tr> <td><p><code>grayDeployments</code></p></td> <td><p>array of object</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>配置Gray灰度的生效规则，以及生效版本</p></td> </tr> <tr> <td><p><code>backendGrayTag</code></p></td> <td><p>string</p></td> <td><p>非必填</p></td> <td><p><code>x-mse-tag</code></p></td> <td><p>后端灰度版本Tag，如果配置了，cookie中将携带值为<code>${backendGrayTag}:${grayDeployments\[\].backendVersion}</code></p></td> </tr> <tr> <td><p><code>uniqueGrayTag</code></p></td> <td><p>string</p></td> <td><p>非必填</p></td> <td><p><code>x-higress-uid</code></p></td> <td><p>开启按照比例灰度时候，网关会生成一个唯一标识存在<code>cookie</code>中，一方面用于session黏贴，另一方面后端也可以使用这个值用于全链路的灰度串联</p></td> </tr> <tr> <td><p><code>injection</code></p></td> <td><p>object</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>往首页HTML中注入全局信息，比如<code>\&lt;script\&gt;window.global = {...}\&lt;/script\&gt;</code></p></td> </tr> </tbody> </table>

`rules`字段配置说明：
<table> <thead> <tr> <td><p>名称</p></td> <td><p>数据类型</p></td> <td><p>填写要求</p></td> <td><p>默认值</p></td> <td><p>描述</p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>name</code></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>规则名称唯一标识，和<code>deploy.gray\[\].name</code>进行关联生效</p></td> </tr> <tr> <td><p><code>grayKeyValue</code></p></td> <td><p>array of string</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>用户ID 白名单列表</p></td> </tr> <tr> <td><p><code>grayTagKey</code></p></td> <td><p>string</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>用户分类打标的标签key值，来自Cookie</p></td> </tr> <tr> <td><p><code>grayTagValue</code></p></td> <td><p>array of string</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>用户分类打标的标签value值，来自Cookie</p></td> </tr> </tbody> </table>

`rewrite`字段配置说明：

`indexRouting`首页重写和`fileRouting`文件重写，本质都是前缀匹配，比如`/app1`：`/mfe/app1/{version}/index.html`代表/app1为前缀的请求，路由到`/mfe/app1/{version}/index.html`页面上，其中`{version}`代表版本号，在运行过程中会被`baseDeployment.version`或者`grayDeployments[].version`动态替换。

`{version}` 作为保留字段，在执行过程中会被`baseDeployment.version`或者`grayDeployments[].version`动态替换前端版本。
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>host</code></p></td> <td><p>string</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>host地址，如果是OSS则设置为 VPC 内网访问地址。</p></td> </tr> <tr> <td><p><code>indexRouting</code></p></td> <td><p>map of string to string</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>用于定义首页重写路由规则。每个键 (Key) 表示首页的路由路径，值 (Value) 则指向重定向的目标文件。例如，键为\&nbsp;<code>/app1</code>\&nbsp;对应的值为\&nbsp;<code>/mfe/app1/{version}/index.html</code>。生效version为<code>0.0.1</code>， 访问路径为\&nbsp;<code>/app1</code>，则重定向到\&nbsp;<code>/mfe/app1/0.0.1/index.html</code>。</p></td> </tr> <tr> <td><p><code>fileRouting</code></p></td> <td><p>map of string to string</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>用于定义资源文件重写路由规则。每个键 (Key) 表示资源访问路径，值 (Value) 则指向重定向的目标文件。例如，键为\&nbsp;<code>/app1/</code>\&nbsp;对应的值为\&nbsp;<code>/mfe/app1/{version}</code>。生效version为<code>0.0.1</code>，访问路径为\&nbsp;<code>/app1/js/a.js</code>，则重定向到\&nbsp;<code>/mfe/app1/0.0.1/js/a.js</code>。</p></td> </tr> </tbody> </table>

`baseDeployment`字段配置说明：
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>version</code></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>Base版本的版本号，作为兜底的版本</p></td> </tr> <tr> <td><p><code>backendVersion</code></p></td> <td><p>string</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>后端灰度版本，配合<code>key</code>为<code>${backendGrayTag}</code>，写入cookie中</p></td> </tr> <tr> <td><p><code>versionPredicates</code></p></td> <td><p>string</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>和<code>version</code>含义相同，但是满足多版本的需求：根据不同路由映射不同的<code>Version</code>版本。一般用于微前端的场景：一个主应用需要管理多个微应用</p></td> </tr> </tbody> </table>

`grayDeployments`字段配置说明：
<table> <thead> <tr> <td><p><b>名称</b></p></td> <td><p><b>数据类型</b></p></td> <td><p><b>填写要求</b></p></td> <td><p><b>默认值</b></p></td> <td><p><b>描述</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p><code>version</code></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>Gray版本的版本号，如果命中灰度规则，则使用此版本。如果是非CDN部署，在header添加<code>x-higress-tag</code></p></td> </tr> <tr> <td><p><code>versionPredicates</code></p></td> <td><p>string</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>和<code>version</code>含义相同，但是满足多版本的需求：根据不同路由映射不同的<code>Version</code>版本。一般用于微前端的场景：一个主应用需要管理多个微应用</p></td> </tr> <tr> <td><p><code>backendVersion</code></p></td> <td><p>string</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>后端灰度版本，会在<code>XHR/Fetch</code>请求的header头添加\&nbsp;<code>x-mse-tag</code>到后端</p></td> </tr> <tr> <td><p><code>name</code></p></td> <td><p>string</p></td> <td><p>必填</p></td> <td><p>-</p></td> <td><p>规则名称和<code>rules\[\].name</code>关联，</p></td> </tr> <tr> <td><p><code>enabled</code></p></td> <td><p>boolean</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>是否启动当前灰度规则</p></td> </tr> <tr> <td><p><code>weight</code></p></td> <td><p>int</p></td> <td><p>非必填</p></td> <td><p>-</p></td> <td><p>按照比例灰度，比如50。</p></td> </tr> </tbody> </table>

## 配置示例
### 基础配置（按用户灰度）

```
HELPCODEESCAPE-yaml
grayKey: userid
rules:
- name: inner-user
  grayKeyValue:
  - '00000001'
  - '00000005'
- name: beta-user
  grayKeyValue:
  - '00000002'
  - '00000003'
  grayTagKey: level
  grayTagValue:
  - level3
  - level5
baseDeployment:
  version: base
grayDeployments:
  - name: beta-user
    version: gray
    enabled: true
```

cookie中的用户唯一标识为 `userid`，当前灰度规则配置了`beta-user`的规则。

当满足下面调试的时候，会使用`version: gray`版本，否则使用`version: base`版本。

* cookie中`userid`等于`00000002`或者`00000003`

* cookie中`level`等于`level3`或者`level5`的用户

### 按比例灰度

```
HELPCODEESCAPE-yaml
grayKey: userid
rules:
- name: inner-user
  grayKeyValue:
  - '00000001'
  - '00000005'
baseDeployment:
  version: base
grayDeployments:
  - name: inner-user
    version: gray
    enabled: true
    weight: 80
```

总的灰度规则为100%，其中灰度版本的权重为80%，基线版本为20%。

### 用户信息存在JSON中

```
HELPCODEESCAPE-yaml
grayKey: appInfo
graySubKey: userId
rules:
- name: inner-user
  grayKeyValue:
  - '00000001'
  - '00000005'
- name: beta-user
  grayKeyValue:
  - '00000002'
  - '00000003'
  grayTagKey: level
  grayTagValue:
  - level3
  - level5
baseDeployment:
  version: base
grayDeployments:
  - name: beta-user
    version: gray
    enabled: true
```

cookie存在`appInfo`的JSON数据，其中包含`userId`字段作为当前的唯一标识。当前灰度规则配置了`beta-user`的规则。 当满足下面的调试条件时，会使用`version: gray`版本，否则使用`version: base`版本。

* cookie中`userid`等于`00000002`或者`00000003`

* cookie中`level`等于`level3`或者`level5`的用户

### 用户信息存储在LocalStorage

由于网关插件需要识别用户为唯一身份信息，HTTP协议进行信息传输，只能在Header中传递。如果用户信息存储在LocalStorage，在首页注入一段脚本将LocalStorage中的用户信息设置到cookie中。

```
HELPCODEESCAPE-javascript
(function() {
var grayKey = '@@X_GRAY_KEY';
var cookies = document.cookie.split('; ').filter(function(row) {
	return row.indexOf(grayKey + '=') === 0;
});

try {
	if (typeof localStorage !== 'undefined' && localStorage !== null) {
		var storageValue = localStorage.getItem(grayKey);
		var cookieValue = cookies.length > 0 ? decodeURIComponent(cookies[0].split('=')[1]) : null;
		if (storageValue && storageValue.indexOf('=') < 0 && cookieValue !== storageValue) {
			document.cookie = grayKey + '=' + encodeURIComponent(storageValue) + '; path=/;';
			window.location.reload();
		}
	}
} catch (error) {
	// xx
}
})();
```

### rewrite重写配置

一般用于CDN部署场景，`{version}`会在运行过程中动态替换为真正的版本。

```
HELPCODEESCAPE-yaml
grayKey: userid
rules:
- name: inner-user
  grayKeyValue:
  - '00000001'
  - '00000005'
- name: beta-user
  grayKeyValue:
  - '00000002'
  - '00000003'
  grayTagKey: level
  grayTagValue:
  - level3
  - level5
rewrite:
  host: frontend-gray.oss-cn-shanghai-internal.aliyuncs.com
  notFoundUri: /mfe/app1/dev/404.html
  indexRouting:
    /app1: '/mfe/app1/{version}/index.html'
    /: '/mfe/app1/{version}/index.html',
  fileRouting:
    /: '/mfe/app1/{version}'
    /app1/: '/mfe/app1/{version}'
baseDeployment:
  version: base
grayDeployments:
  - name: beta-user
    version: gray
    enabled: true
```

#### **indexRouting：首页路由配置**

访问 `/app1`, `/app123`,`/app1/index.html`, `/app1/xxx`, `/xxxx` 都会路由到/mfe/app1/{version}/index.html

#### **fileRouting：文件路由配置**

下面文件映射均生效

* `/js/a.js` =\> `/mfe/app1/v1.0.0/js/a.js`

* `/js/template/a.js` =\> `/mfe/app1/v1.0.0/js/template/a.js`

* `/app1/js/a.js` =\> `/mfe/app1/v1.0.0/js/a.js`

* `/app1/js/template/a.js` =\> `/mfe/app1/v1.0.0/js/template/a.js`

### 在HTML首页注入代码

```
HELPCODEESCAPE-javascript
grayKey: userid
rules:
- name: inner-user
  grayKeyValue:
  - '00000001'
  - '00000005'
baseDeployment:
  version: base
grayDeployments:
  - name: beta-user
    version: gray
    enabled: true
injection:
  head: 
    - <script>console.log('Header')</script>
  body:
    first:
      - <script>console.log('hello world before')</script>
      - <script>console.log('hello world before1')</script>
    last:
      - <script>console.log('hello world after')</script>
      - <script>console.log('hello world after2')</script>
```

通过 `injection`往HTML首页注入代码，可以在`head`标签注入代码，也可以在`body`标签的`first`和`last`位置注入代码。