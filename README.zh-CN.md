# 摄像头检测服务

[English](README.md) | [简体中文](README.zh-CN.md)

该仓库包含一个基于 FastAPI 的摄像头画面分析服务，用于识别黑屏、遮挡、异常破坏等常见问题。服务会从 Redis 流中异步拉取帧数据进行处理，并可将关键帧保存到 MinIO 以便后续回溯。

## 功能特性

- 基于 Redis 流的 JPEG 帧采集。
- 使用 OpenCV 与 NumPy 的异步画面分析流水线。
- 通过 WebSocket 将分析结果实时推送给已连接的客户端。
- 可选将帧保存至 MinIO，并支持周期性清理策略。

## 环境要求

- Python 3.10 或更高版本。
- 可访问的 Redis 实例，用于消费摄像头帧数据。
- （可选）MinIO 或兼容 S3 的对象存储，用于保存异常帧。

安装依赖：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 配置说明

运行时行为由环境变量控制。复制 [`.env.example`](.env.example) 为 `.env`，根据实际环境修改配置：

```bash
cp .env.example .env
```

主要变量包括：

- `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`, `REDIS_DB`：Redis 连接信息，用于消费帧数据。
- `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`：MinIO/S3 对象存储的连接凭证。
- `MINIO_SAVE_MODE`：控制帧保存策略（`all`、`abnormal`、`sample` 或 `none`）。
- `ENABLE_TEST_VIDEO`：开启本地开发用的测试视频生成功能。

更多设置可参考 [`configs/settings.py`](configs/settings.py) 与 [`src/main.py`](src/main.py)。

## 运行服务

使用 Uvicorn 启动 FastAPI 应用：

```bash
uvicorn src.main:app --host 0.0.0.0 --port 5020 --reload
```

接口统一挂载在 `/pushhub` 路径下，主要端点包括：

- `POST /pushhub/start`：启动后台任务。
- `POST /pushhub/stop`：停止任务并释放资源。
- `POST /pushhub/subscribe`：订阅需要分析的流并可覆盖默认阈值。
- `GET  /docs`：Swagger UI 在线文档。
- `WS   /pushhub/ws/results`：通过 WebSocket 接收实时分析结果。

## 开发者提示

- 默认的分析阈值位于 [`camera_check_fastapi/src/settings.py`](camera_check_fastapi/src/settings.py)，可通过订阅请求或环境变量覆盖。
- CPU/IO 线程池大小可在 [`src/main.py`](src/main.py) 中通过 `EXECUTOR_CPU` 和 `EXECUTOR_IO` 调整，以匹配可用硬件资源。
- 推送到 Redis 的帧数据需符合预期结构（包含 `meta` 与 `jpeg` 字段）。

## 许可证

本项目暂未指定许可证，如有需要可在此处补充相关信息。
