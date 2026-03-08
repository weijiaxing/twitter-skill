#!/bin/bash
# 启动每小时推特调度器

echo "🚀 启动Twitter每小时调度器..."
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
echo "检查Python环境..."
python3 --version

# 运行调度器
echo ""
echo "启动每小时调度器..."
echo "按 Ctrl+C 停止"
echo ""

python3 hourly_scheduler.py --run --interval 5