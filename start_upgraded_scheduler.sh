#!/bin/bash
# 启动升级版30分钟推特调度器

echo "🚀🚀🚀 启动升级版Twitter营销系统 🚀🚀🚀"
echo "=========================================="
echo "当前时间: $(date)"
echo "UTC时间: $(date -u)"
echo ""

# 设置环境变量
export TWITTER_CONSUMER_KEY="tjEyhVfb4tLIg8hCFXiq50bsk"
export TWITTER_CONSUMER_SECRET="f6KdjKLGjXEG61bOGFOytO3WlnRyXLxFy2uVN9kQ6NZfkLhCWk"
export TWITTER_ACCESS_TOKEN="1005387576-3yyHKgPFR5hfXUMdhkueWGJcmICpaJSD8ZWo7U1"
export TWITTER_ACCESS_TOKEN_SECRET="Yeg9TI2qzDKWTIDXVml9Kcqe2AHTA2xRDtQ50YeBg1u7H"

# 切换到脚本目录
cd /root/.openclaw/workspace/skills/twitter-publish

# 检查Python环境
echo "📦 检查环境..."
python3 --version

# 停止旧的调度器（如果有）
echo ""
echo "🛑 停止旧调度器..."
pkill -f "hourly_scheduler.py" || true
sleep 2

# 测试推特连接
echo ""
echo "🔗 测试推特连接..."
python3 -c "
import sys
sys.path.insert(0, '.')
from twitter_tool import TwitterTool
import os

os.environ.update({
    'TWITTER_CONSUMER_KEY': 'tjEyhVfb4tLIg8hCFXiq50bsk',
    'TWITTER_CONSUMER_SECRET': 'f6KdjKLGjXEG61bOGFOytO3WlnRyXLxFy2uVN9kQ6NZfkLhCWk',
    'TWITTER_ACCESS_TOKEN': '1005387576-3yyHKgPFR5hfXUMdhkueWGJcmICpaJSD8ZWo7U1',
    'TWITTER_ACCESS_TOKEN_SECRET': 'Yeg9TI2qzDKWTIDXVml9Kcqe2AHTA2xRDtQ50YeBg1u7H'
})

twitter = TwitterTool()
if twitter.user:
    print(f'✅ 连接正常: @{twitter.user.username}')
    print(f'   粉丝数: {twitter.user.followers_count if hasattr(twitter.user, \"followers_count\") else \"N/A\"}')
else:
    print('❌ 连接失败')
    exit(1)
"

# 显示升级信息
echo ""
echo "📈 升级详情:"
echo "  • 发布频率: 每30分钟 (原: 每小时)"
echo "  • 每日最大推文: 30条 (原: 13条)"
echo "  • 内容类型: 8种 (原: 4种)"
echo "  • 活跃时段: UTC 8:00-22:59 (原: 9:00-21:59)"
echo "  • 新增功能: 病毒式营销角度、更多话题标签"
echo ""
echo "⏰ 对应北京时间: 16:00-06:59 (第二天)"
echo "   (每30分钟发布一次，每天最多30条)"

# 询问是否立即测试发布
echo ""
read -p "是否立即测试发布一条升级版推文？(y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧪 测试发布升级版推文..."
    python3 upgraded_30min_scheduler.py --post-now
fi

# 启动升级版调度器
echo ""
echo "🚀 启动升级版30分钟调度器..."
echo "按 Ctrl+C 停止"
echo "=========================================="

python3 upgraded_30min_scheduler.py --run --interval 2