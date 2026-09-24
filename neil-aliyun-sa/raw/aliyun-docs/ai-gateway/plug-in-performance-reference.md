---
source_url: https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/plug-in-performance-reference
fetch_date: 2026-09-21
product: AI Gateway
slug: plug-in-performance-reference
body_sha256: 8bed33aefe6ea1250f9a0a57f84ff1047ecb4666e32507bf8b6e87af42426171
body_bytes: 4051
migration_status: current
---

本文介绍AI 网关平台提供的插件和您使用不同语言开发自己的插件对请求延时的影响。  

## 平台插件性能
平台提供的插件对请求延迟的影响都是微秒级的，例如key-auth插件只会为每个请求增加20微秒左右的延时，basic-auth插件只会为每个请求增加30微秒左右的延时。

## 自定义插件性能
下面例子用不同语言实现了相同的处理逻辑，并比较了性能。具体处理逻辑是：循环执行20次请求头设置，循环执行20次请求头获取，循环执行20次请求头移除。

* C++实现：

  ```
  HELPCODEESCAPE-c++
  FilterHeadersStatus PluginContext::onRequestHeaders(uint32_t, bool) {
    std::string fake_header_key_prefix = "fake_key_";
    std::string fake_header_value_prefix = "fake_value_";
    // Add 20 headers to request headers
    for (size_t i = 0; i < 20; i++) {
      addRequestHeader(fake_header_key_prefix + std::to_string(i),
                       fake_header_value_prefix + std::to_string(i));
    }

    // Check 20 times headers.
    for (size_t i = 0; i < 20; i++) {
      getRequestHeader(fake_header_key_prefix + std::to_string(i));
    }

    // remove add headers
    for (size_t i = 0; i < 20; i++) {
      removeRequestHeader(fake_header_key_prefix + std::to_string(i));
    }
    return FilterHeadersStatus::Continue;
  }
  ```

* Golang实现：

  ```
  HELPCODEESCAPE-go
  func (ctx *httpContext) OnHttpRequestHeaders(numHeaders int, endOfStream bool) types.Action {
          fake_header_key_prefix := "fake_key_"
          fake_header_value_prefix := "fake_value_"
          for i := 0; i < 20; i++ {
                  proxywasm.AddHttpRequestHeader(fake_header_key_prefix+strconv.Itoa(i),
                          fake_header_value_prefix+strconv.Itoa(i))
          }
          for i := 0; i < 20; i++ {
                  proxywasm.GetHttpRequestHeader(fake_header_key_prefix + strconv.Itoa(i))
          }
          for i := 0; i < 20; i++ {
                  proxywasm.RemoveHttpRequestHeader(fake_header_key_prefix + strconv.Itoa(i))
          }
          return types.ActionContinue
  }
  ```

* Rust实现：

  ```
  HELPCODEESCAPE-rust
  fn on_http_request_headers(&mut self, _: usize, _: bool) -> Action {
      for i in 0..20 {
          let key = "fake_key_".to_string() + &i.to_string();
          let value = "fake_value_".to_string() + &i.to_string();
          self.set_http_request_header(&key, Some(&value));
      }
      for i in 0..20 {
          let key = "fake_key_".to_string() + &i.to_string();
          self.get_http_request_header(&key);
      }
      for i in 0..20 {
          let key = "fake_key_".to_string() + &i.to_string();
          self.set_http_request_header(&key, None);
      }
      Action::Continue
  }
  ```

* AssemblyScript实现：

  ```
  HELPCODEESCAPE-javascript
  function onRequestHeaders(a: u32, end_of_stream: bool): FilterHeadersStatusValues {
    let fake_header_key_prefix: string = "fake_key_";
    let fake_header_value_prefix: string = "fake_value_";
    for (let i = 0; i < 20; i++) {
       stream_context.headers.request.add(fake_header_key_prefix + i.toString(), fake_header_value_prefix + i.toString())
    }
    for (let i = 0; i < 20; i++) {
       stream_context.headers.request.get(fake_header_key_prefix + i.toString())
    }
    for (let i = 0; i < 20; i++) {
       stream_context.headers.request.remove(fake_header_key_prefix + i.toString())
    }
    return FilterHeadersStatusValues.Continue;
  }
  ```

## 不同语言实现性能对比
<table> <thead> <tr> <td><p><b>实现语言</b></p></td> <td><p><b>请求延时增加</b></p></td> </tr> </thead> <colgroup></colgroup> <colgroup></colgroup> <tbody> <tr> <td><p>C++</p></td> <td><p>0.19毫秒</p></td> </tr> <tr> <td><p>Golang</p></td> <td><p>0.20毫秒</p></td> </tr> <tr> <td><p>Rust</p></td> <td><p>0.21毫秒</p></td> </tr> <tr> <td><p>AssemblyScript</p></td> <td><p>0.21毫秒</p></td> </tr> </tbody> </table>

可以看到不同语言实现的性能差距不大。