# Gemini-Reverse-Proxy
## 简介

本项目是一个使用 Flask 框架构建的 Google AI API 代理服务器。它主要用于：

*   **统一管理 API 密钥：** 从环境变量中读取 API 密钥，并将其添加到转发给 Google AI API 的请求中。
*   **解决跨域问题 (CORS)：**  通过设置 `Access-Control-Allow-Origin` 响应头，允许来自任何域的请求访问 Google AI API。
*   **简化客户端请求：**  客户端只需要向代理服务器发送请求，而不需要关心 Google AI API 的具体细节。
*   **灵活的 API 密钥轮换：**  支持从多个环境变量中随机选择 API 密钥，方便进行密钥轮换和负载均衡。

## 目录结构

```
.
├── .dockerignore     # 指定 Docker 构建时忽略的文件和目录
├── .env.example     # .env 文件的示例
├── Dockerfile        # Docker 镜像构建配置文件
├── proxy.py          # Flask 应用程序代码
└── requirements.txt  # 项目依赖的 Python 包列表
```

## 快速开始

### 前提条件

*   Python 3.9+
*   Docker

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

*   在项目根目录下创建 `.env` 文件，并添加以下环境变量：

    ```
    GOOGLE_API_KEY_1=YOUR_API_KEY_1
    GOOGLE_API_KEY_2=YOUR_API_KEY_2
    GOOGLE_API_KEY_3=YOUR_API_KEY_3
    OUTPUT_API_KEY=YOUR_OUTPUT_API_KEY
    PORT=8000
    ```

    *   `GOOGLE_API_KEY_1`, `GOOGLE_API_KEY_2`, `GOOGLE_API_KEY_3`:  Google AI API 密钥，可以设置多个，用于密钥轮换。
    *   `OUTPUT_API_KEY`:  用于客户端调用的输出 API 密钥（可选）。
    *   `PORT`:  代理服务器监听的端口（默认为 8000）。
    *   **注意：**  请将 `YOUR_API_KEY_1`, `YOUR_API_KEY_2`, `YOUR_API_KEY_3` 和 `YOUR_OUTPUT_API_KEY` 替换为你的实际值。
    *   **安全提示：**  请将 `.env` 文件添加到 `.gitignore` 文件中，防止 API 密钥泄露。

### 3. 运行代理服务器

```bash
python proxy.py
```

代理服务器将在 `http://localhost:8000` 启动。

### 4. 使用 Docker 部署

1.  **构建 Docker 镜像：**

    ```bash
    docker build -t google-ai-proxy .
    ```

2.  **运行 Docker 容器：**

    ```bash
    docker run -d -p 8000:8000 --name google-ai-proxy-container --env-file .env google-ai-proxy
    ```

    *   这将创建一个名为 `google-ai-proxy-container` 的 Docker 容器，并将宿主机的 8000 端口映射到容器的 8000 端口。
    *   `--env-file .env` 参数用于从 `.env` 文件中读取环境变量。

### 5. 测试代理服务器

使用 `curl` 或其他 HTTP 客户端发送 POST 请求：

```bash
curl -X POST \
  http://localhost:8000/v1beta/models/gemini-2.0-flash:generateContent?temperature=0.2 \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "Write a short story",
    "temperature": 0.8,
    "max_output_tokens": 100
  }'
```

如果一切正常，你应该能够收到 Google AI API 的响应。

## 环境变量

| 变量名            | 描述                                                                                                                                                           | 默认值 |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| `GOOGLE_API_KEY_*` | Google AI API 密钥。可以设置多个，用于密钥轮换。例如：`GOOGLE_API_KEY_1=YOUR_API_KEY_1`, `GOOGLE_API_KEY_2=YOUR_API_KEY_2`                                           |        |
| `OUTPUT_API_KEY`    | 用于客户端调用的输出 API 密钥（可选）。                                                                                                                              |        |
| `PORT`              | 代理服务器监听的端口。                                                                                                                                             | 8000   |

## 错误处理

*   如果 `get_api_key()` 函数无法获取 API 密钥，则会返回 401 状态码和 JSON 错误信息。
*   如果发生 `requests.exceptions.RequestException` 异常，则会返回 500 状态码和 JSON 错误信息。
*   如果请求的路径不存在，则会返回 404 状态码和 JSON 错误信息。

## 安全注意事项

*   请勿将真实的 API 密钥提交到公共代码仓库中。
*   请将 `.env` 文件添加到 `.gitignore` 文件中，防止 API 密钥泄露。
*   在生产环境中，请将 `Access-Control-Allow-Origin` 设置为具体的域名，而不是 `*`。

## 贡献

欢迎提交 issue 和 pull request！
