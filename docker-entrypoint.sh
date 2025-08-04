#!/bin/bash
set -e

echo "🚀 启动 Spider_XHS 应用..."

# 安装Node.js依赖
echo "📦 安装Node.js依赖..."
npm install

# 检查必要的目录是否存在
echo "📁 检查数据目录..."
mkdir -p datas/excel_datas
mkdir -p datas/media_datas
mkdir -p env_config

# 检查配置文件
if [ ! -f "env_config/user_profile" ]; then
    echo "🔧 创建默认配置文件..."
    echo "/app/datas" > env_config/user_profile
fi

# 启动应用
echo "🌟 启动Streamlit应用..."
exec streamlit run app.py --server.port=8501 --server.address=0.0.0.0