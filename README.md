# 简介
本项目是一个基于 Flask 框架构建的 Gemini API 代理服务器，用于解决跨域问题，支持多api轮询，移除了安全过滤。

## 使用方法
在项目根目录.env文件中添加以下环境变量：
```
GOOGLE_API_KEY_1=YOUR_API_KEY_1
GOOGLE_API_KEY_2=YOUR_API_KEY_2
GOOGLE_API_KEY_3=YOUR_API_KEY_3
PORT=YOUR_PORT #默认8000
```
在客户端填入你的URL，任意API_KEY
支持docker部署：
```bash
docker pull quathor/proxy-gemini:latest
```
## 注意
本项目仅供个人学习交流使用，请注意防止隐私泄露
