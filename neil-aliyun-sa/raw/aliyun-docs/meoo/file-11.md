> ## Documentation Index
> Fetch the complete documentation index at: https://docs.meoo.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 文件上传/下载/存储

# 文件上传

✨秒悟对话框支持上传文件、图片和视频，可根据上传的内容和提示词要求进行解析和处理。

* 支持上传文件：PDF、Word、Excel、PPT、TXT、Markdown、CSV、HTML、CSS、SVG
* 支持上传图片和视频

<Warning>
  请将单个文件大小控制在5MB以内，否则可能出现无法存储的情况；

  最多支持上传10个文件。
</Warning>

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/RAM3KsEGPI3GqBwa/images/image-228.png?fit=max&auto=format&n=RAM3KsEGPI3GqBwa&q=85&s=0f455dc11e9f1cf019b52fc74d4e2ff4" alt="Image" width="1551" height="910" data-path="images/image-228.png" />
</Frame>

✨应用举例

* 上传开发文档，要求秒悟按照开发文档进行应用开发
* 上传数据，生成可视化PPT
* 上传Excel，生成可交互的网页Demo
* 上传PPT课件，生成在线演示网页
* 上传个人简历，生成个人网站

# 文件/代码下载

✨秒悟支持对生成的应用代码或文档内容进行下载。

1. **代码下载**：点击 **代码** 中的下载图标，即可进行应用代码下载。
   <Note>
     PRO套餐和MAX套餐支持代码下载功能，如需代码下载，请进行套餐订阅
   </Note>
   <Frame>
     <img src="https://mintcdn.com/alibaba-b47c397f/sV0952-W53noSJwo/images/e946b6de857de081a34a2ee47ebf1fd9.png?fit=max&auto=format&n=sV0952-W53noSJwo&q=85&s=31220b421898a4410920ac11234621ac" alt="E946b6de857de081a34a2ee47ebf1fd9" width="2256" height="1264" data-path="images/e946b6de857de081a34a2ee47ebf1fd9.png" />
   </Frame>
2. **文件下载**：如果是通过秒悟进行文档生成，例如在秒悟对话框上传数据生成可视化PPT，在秒悟完成创建后，可在 **文件-AI生成** 中进行查看，同时可对生成的文档进行 **下载**。
   <Note>
     AI生成文件暂不支持.zip和.json格式的下载
   </Note>
   <Frame>
     <img src="https://mintcdn.com/alibaba-b47c397f/sV0952-W53noSJwo/images/44335b0fd8e9549e937c715c239106b5.png?fit=max&auto=format&n=sV0952-W53noSJwo&q=85&s=8a09c6d82965268f9b2d680a3a3e2d60" alt="44335b0fd8e9549e937c715c239106b5" width="2256" height="1264" data-path="images/44335b0fd8e9549e937c715c239106b5.png" />
   </Frame>

# 文件存储

✨在秒悟生成应用的过程中，对于大于5MB的单个文件会在沙箱中临时存储，不会上传至秒悟云端代码库。

* **临时存储阈值**：单个文件大小超过5MB。
* **适用范围**：包括但不限于上传的大型文件/图片、AI 生成的文件/图片，以及通过网络下载的资源。
* **存储机制**：超过5MB的大文件仅存储在当前的沙箱环境中，属于临时数据，系统不会将此类文件提交到云端代码库进行长期存储。当沙箱实例销毁（如会话超时、手动停止、项目关闭），超过 5MB 的临时文件将被清除。**请提前做好信息备份。**
  <Frame>
    <img src="https://mintcdn.com/alibaba-b47c397f/pyv3EkV9rBZPAe_b/images/33.png?fit=max&auto=format&n=pyv3EkV9rBZPAe_b&q=85&s=aebd3df41149b1e0b69d8b2a758b26d5" alt="33" width="2248" height="1286" data-path="images/33.png" />
  </Frame>
* **最佳实践**：

  <Accordion title="图片上传" defaultOpen>
    * 秒悟对话框上传的图片大小建议控制在5MB以内。
    * 如需上传大于5MB的图片构建到应用中，可将图片存储到云服务文件中，获取图片CDN URL，然后采用图片URL的方式引用。如需上传大文件，可用同样的方式将其上传至云服务文件中。

    <Steps>
      <Step title="告知AI开启秒悟云服务">
        若已开启，忽略此步骤
      </Step>

      <Step title="告知AI创建存储桶">
        若已存在合适可用的存储桶，忽略此步骤
      </Step>

      <Step title="在云服务文件的对应存储桶中上传图片文件，获取CDN URL">
        <Frame>
          <img src="https://mintcdn.com/alibaba-b47c397f/CS6ZFixaMvUmvFEN/images/image-249.png?fit=max&auto=format&n=CS6ZFixaMvUmvFEN&q=85&s=472f56cc4eab026aee08ebd19592e06f" alt="Image" width="1569" height="486" data-path="images/image-249.png" />
        </Frame>
      </Step>

      <Step title="复制图片URL，告知AI图片使用位置" />
    </Steps>
  </Accordion>
