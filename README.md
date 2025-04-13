# Gemini-Reverse-Proxy
本项目是一个基于 Flask 框架构建的 Google AI API 代理服务器，用于解决跨域问题。

## 环境变量

| 变量名           | 描述                                                                                                 | 默认值 |
| --------------- | ---------------------------------------------------------------------------------------------------- | ----- |
| GOOGLE_API_KEY_* | Google AI API 密钥。 你可以设置多个以 `GOOGLE_API_KEY_` 开头的环境变量，用于密钥轮换。                                          | 无    |
| OUTPUT_API_KEY   | 用于在根路径 `/` 的响应中显示的 API 密钥，方便客户端调用。                                                        | 无    |
| PORT            | 代理服务器监听的端口。                                                                                              | 8000  |

### 拉取 Docker 镜像 (推荐)

```bash
docker pull quathor/proxy-gemini:latest
```
