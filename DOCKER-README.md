# 🐳 Docker 一键部署指南

## 快速开始

### 1. 准备工作
确保已安装 Docker 和 Docker Compose：
```bash
# 检查版本
docker --version
docker-compose --version
```

### 2. 配置环境
复制环境变量模板并填写配置：
```bash
cp .env.example .env
```

编辑 `.env` 文件，至少需要配置：
- `XHS_COOKIE`: 小红书登录后的Cookie（必需）

### 3. 一键启动
```bash
# 构建并启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 4. 访问应用
打开浏览器访问: http://localhost:8501

## 📁 数据持久化

项目会自动创建以下持久化目录：
- `./datas/excel_datas/` - Excel文件存储
- `./datas/media_datas/` - 媒体文件存储  
- `./env_config/` - 配置文件存储

## 🔧 常用命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f spider-xhs

# 进入容器
docker-compose exec spider-xhs bash

# 重新构建镜像
docker-compose build --no-cache
```

## 🛠️ 开发模式

如需本地开发，可以修改 `docker-compose.yml`：
```yaml
volumes:
  - .:/app  # 取消注释这行
```

这样代码修改会实时同步到容器中。

## 📝 Cookie获取方法

1. 登录 [小红书网页版](https://www.xiaohongshu.com)
2. 按 F12 打开开发者工具
3. 点击 Network 标签
4. 刷新页面，找到任意请求
5. 复制 Request Headers 中的 Cookie 值
6. 粘贴到 `.env` 文件的 `XHS_COOKIE` 字段

## ⚠️ 注意事项

- Cookie会过期，需要定期更新
- 首次启动可能需要几分钟时间构建镜像
- 确保端口8501未被其他程序占用
- 数据文件会保存在本地，删除容器不会丢失数据

## 🔍 故障排除

### 端口占用
```bash
# 查看端口占用
lsof -i :8501

# 修改端口（编辑docker-compose.yml）
ports:
  - "8502:8501"  # 改为8502端口
```

### 重置数据
```bash
# 停止服务并删除数据
docker-compose down
rm -rf datas/
```

### 查看详细日志
```bash
docker-compose logs --tail=100 spider-xhs
```