#!/bin/bash
# Twitter每日自动化设置脚本

echo "🚀 设置Twitter每日自动化任务"
echo "=" * 50

# 1. 检查环境
echo "🔍 检查环境..."
if [ -z "$TWITTER_CONSUMER_KEY" ]; then
    echo "❌ 请设置Twitter API环境变量"
    exit 1
fi

echo "✅ 环境检查通过"

# 2. 创建OpenClaw cron任务
echo "📅 创建自动化任务..."
python3 daily_automation.py --create-tasks

# 3. 测试系统
echo "🧪 测试系统..."
python3 quick_growth.py --session --duration 2

# 4. 显示任务计划
echo "📋 每日任务计划:"
echo "   01:00 UTC - 上午推文发布"
echo "   02:30 UTC - 上午增长会话"
echo "   04:00 UTC - 中午教育推文"
echo "   05:30 UTC - 中午互动增强"
echo "   07:00 UTC - 下午案例推文"
echo "   08:30 UTC - 下午增长会话"
echo "   10:00 UTC - 晚上成功故事"
echo "   12:30 UTC - 晚间互动会话"

echo "📅 每周线程计划:"
echo "   周一 06:00 UTC - 功能线程"
echo "   周三 06:00 UTC - 案例线程"
echo "   周五 06:00 UTC - 教育线程"

echo ""
echo "✅ 自动化系统设置完成!"
echo "=" * 50
