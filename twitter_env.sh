#!/bin/bash
export TWITTER_CONSUMER_KEY="tjEyhVfb4tLIg8hCFXiq50bsk"
export TWITTER_CONSUMER_SECRET="f6KdjKLGjXEG61bOGFOytO3WlnRyXLxFy2uVN9kQ6NZfkLhCWk"
export TWITTER_ACCESS_TOKEN="1005387576-3yyHKgPFR5hfXUMdhkueWGJcmICpaJSD8ZWo7U1"
export TWITTER_ACCESS_TOKEN_SECRET="Yeg9TI2qzDKWTIDXVml9Kcqe2AHTA2xRDtQ50YeBg1u7H"

# 启动24小时调度器
cd /root/.openclaw/workspace/skills/twitter-publish
nohup python3 24hour_scheduler.py --run --interval 2 > 24hour_scheduler.log 2>&1 &

echo "Twitter调度器已启动"
echo "PID: $!"
echo "日志: 24hour_scheduler.log"