#!/bin/bash
# Twitter自动化执行脚本
# 由OpenClaw cron调用

echo "🚀 执行Twitter自动化任务 - $(date)"
echo "=" * 50

# 设置环境变量
export TWITTER_CONSUMER_KEY="tjEyhVfb4tLIg8hCFXiq50bsk"
export TWITTER_CONSUMER_SECRET="f6KdjKLGjXEG61bOGFOytO3WlnRyXLxFy2uVN9kQ6NZfkLhCWk"
export TWITTER_ACCESS_TOKEN="1005387576-3yyHKgPFR5hfXUMdhkueWGJcmICpaJSD8ZWo7U1"
export TWITTER_ACCESS_TOKEN_SECRET="Yeg9TI2qzDKWTIDXVml9Kcqe2AHTA2xRDtQ50YeBg1u7H"

# 切换到技能目录
cd /root/.openclaw/workspace/skills/twitter-publish

# 根据参数执行不同任务
case "$1" in
    "morning_tweet")
        echo "📝 执行上午推文发布..."
        python3 postalert_content_series.py --feature 0
        ;;
    
    "morning_growth")
        echo "🤝 执行上午增长会话..."
        python3 quick_growth.py --session --duration 10
        ;;
    
    "noon_educational")
        echo "💡 执行中午教育推文..."
        python3 postalert_content_series.py --educational 1
        ;;
    
    "noon_engagement")
        echo "💬 执行中午互动增强..."
        python3 engagement_enhancer.py --session --duration 15
        ;;
    
    "afternoon_case")
        echo "🎯 执行下午案例推文..."
        python3 postalert_content_series.py --usecase 2
        ;;
    
    "afternoon_growth")
        echo "🚀 执行下午增长会话..."
        python3 quick_growth.py --session --duration 10
        ;;
    
    "evening_success")
        echo "🏆 执行晚上成功故事..."
        python3 postalert_content_series.py --success 3
        ;;
    
    "evening_engagement")
        echo "🌟 执行晚间互动会话..."
        python3 engagement_enhancer.py --session --duration 15
        ;;
    
    "monday_thread")
        echo "🧵 执行周一功能线程..."
        python3 postalert_content_series.py --thread core_features --thread-length 3
        ;;
    
    "wednesday_thread")
        echo "📊 执行周三案例线程..."
        python3 postalert_content_series.py --thread use_cases --thread-length 3
        ;;
    
    "friday_thread")
        echo "🎓 执行周五教育线程..."
        python3 postalert_content_series.py --thread educational --thread-length 3
        ;;
    
    *)
        echo "❌ 未知任务: $1"
        echo "可用任务:"
        echo "  morning_tweet, morning_growth, noon_educational, noon_engagement"
        echo "  afternoon_case, afternoon_growth, evening_success, evening_engagement"
        echo "  monday_thread, wednesday_thread, friday_thread"
        exit 1
        ;;
esac

echo ""
echo "✅ 任务执行完成 - $(date)"
echo "=" * 50
