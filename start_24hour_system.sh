#!/bin/bash
# 启动24小时全天候推特营销系统

echo "🌍🌍🌍 启动24小时全天候Twitter营销系统 🌍🌍🌍"
echo "=================================================="
echo "启动时间: $(date)"
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

# 停止所有旧调度器
echo ""
echo "🛑 停止所有旧调度器..."
pkill -f "hourly_scheduler.py" || true
pkill -f "upgraded_30min_scheduler.py" || true
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
    print('   准备启动24小时营销系统...')
else:
    print('❌ 连接失败')
    exit(1)
"

# 显示24小时系统详情
echo ""
echo "📈 24小时系统配置:"
echo "  • 发布频率: 每30分钟，24/7不间断"
echo "  • 每日最大推文: 48条"
echo "  • 时段策略: 智能分时段优化"
echo ""
echo "⏰ 时段策略详情:"
echo "  🔥 高峰时段 (UTC 9:00-20:59):"
echo "     内容: 产品功能、对比优势、病毒营销"
echo "     目标: 最大化曝光和转化"
echo ""
echo "  ⚡ 正常时段 (UTC 8:00, 21:00-23:59):"
echo "     内容: 问题解决方案、用户证言"
echo "     目标: 建立信任和权威"
echo ""
echo "  🌙 低谷时段 (UTC 0:00-7:59):"
echo "     内容: 趋势分析、幕后故事、教育内容"
echo "     目标: 培养忠实粉丝和品牌认知"
echo ""
echo "🔄 对应北京时间: 全天候覆盖"
echo "   高峰: 17:00-04:59"
echo "   正常: 16:00, 05:00-07:59"  
echo "   低谷: 08:00-15:59"

# 询问是否立即测试发布
echo ""
read -p "是否立即测试发布一条24小时系统推文？(y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧪 测试发布24小时系统推文..."
    python3 24hour_scheduler.py --post-now
fi

# 启动24小时系统
echo ""
echo "🚀 启动24小时全天候营销系统..."
echo "系统将24小时不间断运行，每30分钟发布一条推文"
echo "按 Ctrl+C 停止系统"
echo "=================================================="

python3 24hour_scheduler.py --run --interval 2