> ## Documentation Index
> Fetch the complete documentation index at: https://docs.meoo.com/llms.txt
> Use this file to discover all available pages before exploring further.

# 成员与角色

秒悟（Meoo）团队版采用**席位制订阅**，需购买席位后邀请成员使用。当团队邀请成员成功并且成员处于正常状态时，该成员将占用一个席位，每个被邀请进团队的成员均有自己角色。

## 角色权限

秒悟（Meoo）团队版的团队成员目前共包含3种角色：

* 所有者（Owner）：团队的所有者，仅可有一位。具有团队的组织管理、计费管理等全部权限，可使用团队对应的权益、功能和资源。
* 管理员（Admin）：团队的管理员，可设置多位。具有团队的组织管理、计费查看等相关权限，无法使用订阅升级、加购、退订等计费管理能力，可使用团队对应的权益、功能和资源。
* 成员（Member）：团队的普通成员，可设置多位。不具备团队维度的管理权限，可使用团队对应的权益、功能和资源。

不同角色对应权限如下：

| 功能       | 所有者 | 管理员 | 成员 |
| -------- | --- | --- | -- |
| 可用团队积分   | ✓   | ✓   | ✓  |
| 管理个人应用   | ✓   | ✓   | ✓  |
| 管理团队应用   | ✓   | ✓   | -  |
| 管理团队信息   | ✓   | ✓   | -  |
| 邀请添加成员   | ✓   | ✓   | -  |
| 修改成员角色   | ✓   | ✓   | -  |
| 修改成员积分额度 | ✓   | ✓   | -  |
| 移除成员     | ✓   | ✓   | -  |
| 查看个人积分用量 | ✓   | ✓   | ✓  |
| 管理团队积分用量 | ✓   | ✓   | -  |
| 查看订单     | ✓   | ✓   | -  |
| 购买订阅套餐   | ✓   | -   | -  |
| 变更团队席位   | ✓   | -   | -  |
| 增购积分包    | ✓   | -   | -  |

## 成员状态

秒悟（Meoo）团队版的团队成员目前共包含2种角色：

* 正常：正常状态成员可正常登陆并使用秒悟团队版，并按角色权限使用团队权益、功能和资源。
* 冻结：冻结状态成员登陆后不可正常使用秒悟团队版，需联系团队管理员或团队拥有者处理。冻结状态成员应用和技能等数据资产均保留，可被团队拥有者和管理员恢复和删除。

<Note>
  成员冻结状态仅在套餐权益过期失效、当前团队人数超过席位数等异常情况下出现。
</Note>

## 成员管理

### 查看成员

团队拥有者和管理员可在**管理员控制台>成员管理**中查看当前团队内已有席位数量、已占用席位数量和对应团队内成员情况。当席位将要或已经完全占用时，请及时关注团队席位使用情况，避免影响您邀请新成员加入当前团队。

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/bK4onMBYGvMER6id/images/13403DB4-074B-4293-8760-FD5FFF20EA1B.png?fit=max&auto=format&n=bK4onMBYGvMER6id&q=85&s=ac9be24b98bb34874336dbfba636e5a9" alt="13403DB4 074B 4293 8760 FD5FFF20EA1B" width="2730" height="1328" data-path="images/13403DB4-074B-4293-8760-FD5FFF20EA1B.png" />
</Frame>

### 添加成员

<Note>
  邀请前，请确保您已经为期望邀请成员在您的阿里云主账号下创建 RAM 账号，否则期望邀请成员无法登陆和成功加入团队。参考：[团队账号创建与登陆](https://docs.meoo.com/team-login)。
</Note>

秒悟（Meoo）团队版可通过分享邀请链接的形式添加团队成员，可通过**管理员控制台>成员管理**右上角的“**邀请成员**”入口进入。

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/sS5mGogX_QkqbmfA/images/59B1C3B9-73A7-4BC0-932A-B03A5CB523C2.png?fit=max&auto=format&n=sS5mGogX_QkqbmfA&q=85&s=ffc3b87913930069f19a0d0e1242adef" alt="59B1C3B9 73A7 4BC0 932A B03A5CB523C2" width="2724" height="1286" data-path="images/59B1C3B9-73A7-4BC0-932A-B03A5CB523C2.png" />
</Frame>

团队拥有者和管理员可设置邀请链接有效期、被邀请人角色、被邀请人额度上限等配置项，并生成分享链接，可将链接或文案分享给期望邀请的用户或群组。

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/sS5mGogX_QkqbmfA/images/01E754E1-EB03-44CE-B4DB-2E8966ED12D3.png?fit=max&auto=format&n=sS5mGogX_QkqbmfA&q=85&s=fb8521a2c9104968eba6f1bab1a4455d" alt="01E754E1 EB03 44CE B4DB 2E8966ED12D3" width="2676" height="1278" data-path="images/01E754E1-EB03-44CE-B4DB-2E8966ED12D3.png" />
</Frame>

成员在有效期内点击邀请链接即可加入团队。超过有效期后，邀请链接失效。

### 修改成员

团队拥有者和管理员可对团队成员（除团队拥有者和自己以外）进行修改。

* 正常态员工支持修改角色和每月积分额度上限。前往**管理员控制台>成员管理**，选中正常状态员工，点击列表最右侧 ··· ，选择修改角色或修改积分额度选项。

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/sS5mGogX_QkqbmfA/images/150B803D-F98C-45D6-BC4C-39AC738E1187.png?fit=max&auto=format&n=sS5mGogX_QkqbmfA&q=85&s=9103dfa6aa4f8c6b6fc4b37e6787835f" alt="150B803D F98C 45D6 BC4C 39AC738E1187" width="2714" height="1294" data-path="images/150B803D-F98C-45D6-BC4C-39AC738E1187.png" />
</Frame>

* 冻结态员工支持恢复成员状态至正常状态（席位数量需满足恢复后团队人数）。前往**管理员控制台>成员管理**，选中冻结状态员工，点击列表最右侧 ··· ，选择恢复成员选项。
  <Frame>
    <img src="https://mintcdn.com/alibaba-b47c397f/sS5mGogX_QkqbmfA/images/33FED2F3-70A9-4DEB-96D1-F81DC9006A5E.png?fit=max&auto=format&n=sS5mGogX_QkqbmfA&q=85&s=49280c70c671351c7c732018b13c39a1" alt="33FED2F3 70A9 4DEB 96D1 F81DC9006A5E" width="2706" height="1318" data-path="images/33FED2F3-70A9-4DEB-96D1-F81DC9006A5E.png" />
  </Frame>

### 移除成员

团队拥有者和管理员可对团队成员（除团队拥有者和自己以外）进行移除。前往**管理员控制台>成员管理**，选中目标成员，点击列表最右侧 ··· ，选中移除成员选项。选中后，需转交被移除成员名下的应用和技能给指定接收人。

<Frame>
  <img src="https://mintcdn.com/alibaba-b47c397f/bK4onMBYGvMER6id/images/AF3C466B-9D69-404E-BE5D-CD945E0EC388.png?fit=max&auto=format&n=bK4onMBYGvMER6id&q=85&s=aa5646a822b3ec284f0d85389010a8f3" alt="AF3C466B 9D69 404E BE5D CD945E0EC388" width="2676" height="1304" data-path="images/AF3C466B-9D69-404E-BE5D-CD945E0EC388.png" />
</Frame>

移除成员后，该成员将离开当前团队并无法登陆，同时不再在成员列表中展示，名下应用和技能将转交给指定接收人。此操作不可逆。
