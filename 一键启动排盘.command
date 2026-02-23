#!/bin/bash
# 获取脚本所在的当前目录
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR/qimen-dunjia" || exit

# 清理可能残存的旧后台服务，确保端口被干净释放
pkill -f "qimen_web.py" >/dev/null 2>&1 || true

echo "==================================="
echo "    正在启动 奇门遁甲 排盘引擎     "
echo "==================================="

# 检查虚拟环境，如果没有则自动创建并安装依赖（如 lunar-python）
if [ ! -d ".venv" ]; then
    echo "首次运行新版本：正在为您配置独立且极其精准的天文学及历法运行环境(lunar-python)..."
    python3 -m venv .venv
    .venv/bin/pip install lunar-python
fi

echo "==================================="
echo "环境配置检测完毕，启动服务器！请勿关闭此黑色窗口！"
echo "(如果想完全退出，关闭此窗口即可)"
echo "..."

.venv/bin/python scripts/qimen_web.py
