# 摄像头巡检服务

本仓库提供一个基于 FastAPI 的服务，用于分析摄像头画面中常见的问题，例如黑屏、遮挡和人为篡改。服务会从 Redis 流中拉取图像帧，异步处理并将可选的快照存入 MinIO 以供后续查看。

## 功能特性

- 使用 Redis 作为 JPEG 图像帧的输入通道。
- 借助 OpenCV 与 NumPy 异步分析画面异常。
- 通过 WebSocket 将分析结果实时广播给已连接客户端。
- 可选地将异常帧持久化到 MinIO，并支持周期性清理策略。

## 环境要求

- Python 3.10 或更高版本。
- 可用的 Redis 实例，用于消费摄像头帧数据。
- （可选）若需保存异常帧，需要 MinIO 或兼容 S3 的对象存储。

安装依赖方式如下：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 配置说明

运行时行为通过环境变量控制。复制 [`.env.example`](.env.example) 为 `.env` 并根据实际环境调整：

```bash
cp .env.example .env
```

关键配置包括：

- `REDIS_HOST`、`REDIS_PORT`、`REDIS_PASSWORD`、`REDIS_DB`：服务消费帧数据时所需的 Redis 连接信息。
- `MINIO_ENDPOINT`、`MINIO_ACCESS_KEY`、`MINIO_SECRET_KEY`：用于存储异常帧的 MinIO/S3 凭据。
- `MINIO_SAVE_MODE`：控制帧数据的保存策略（`all`、`abnormal`、`sample` 或 `none`）。
- `ENABLE_TEST_VIDEO`：是否启用随仓库提供的测试视频工具，方便本地开发。

完整配置项可参考 [`configs/settings.py`](configs/settings.py) 与 [`src/main.py`](src/main.py)。

## 启动服务

使用 Uvicorn 运行 FastAPI 应用：

```bash
uvicorn src.main:app --host 0.0.0.0 --port 5020 --reload
```

接口均以 `/pushhub` 作为前缀，主要端点如下：

- `POST /pushhub/start`：启动后台任务。
- `POST /pushhub/stop`：停止所有任务并释放资源。
- `POST /pushhub/subscribe`：提交需要分析的流名称以及可选的阈值覆盖配置。
- `GET  /docs`：查看 Swagger UI，交互式调试接口。
- `WS   /pushhub/ws/results`：以 WebSocket 形式获取实时分析结果。

## 开发提示

- 默认分析阈值位于 [`camera_check_fastapi/src/settings.py`](camera_check_fastapi/src/settings.py)，可通过 subscribe 接口或环境变量覆盖。
- 可以通过 [`src/main.py`](src/main.py) 中的 `EXECUTOR_CPU` 与 `EXECUTOR_IO` 调整工作线程池大小，以匹配实际硬件资源。
- 向 Redis 推送数据时，请确保流结构包含 `meta` 与 `jpeg` 字段以符合预期格式。

## 许可证

本项目暂未附带具体许可协议，如有需要请自行补充相关信息。
