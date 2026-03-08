#!/bin/bash
# 一键永久启动Twitter 24小时营销系统
# 只需运行一次，系统将永久运行（即使重启也会自动恢复）

echo "🚀 Twitter 24小时营销系统 - 一键永久启动"
echo "=========================================="

SCRIPT_DIR="/root/.openclaw/workspace/skills/twitter-publish"
SERVICE_NAME="twitter-24hour-auto"

# 1. 创建启动脚本
echo "1. 创建启动脚本..."
cat > /usr/local/bin/start_twitter_marketing << 'EOF'
#!/bin/bash
# Twitter营销系统启动脚本

cd /root/.openclaw/workspace/skills/twitter-publish

export TWITTER_CONSUMER_KEY="tjEyhVfb4tLIg8hCFXiq50bsk"
export TWITTER_CONSUMER_SECRET="f6KdjKLGjXEG61bOGFOytO3WlnRyXLxFy2uVN9kQ6NZfkLhCWk"
export TWITTER_ACCESS_TOKEN="1005387576-3yyHKgPFR5hfXUMdhkueWGJcmICpaJSD8ZWo7U1"
export TWITTER_ACCESS_TOKEN_SECRET="Yeg9TI2qzDKWTIDXVml9Kcqe2AHTA2xRDtQ50YeBg1u7H"

# 停止可能存在的旧进程
pkill -f "24hour_scheduler.py" 2>/dev/null
sleep 2

# 启动24小时调度器
echo "启动Twitter 24小时营销系统..."
python3 24hour_scheduler.py --run --interval 2
EOF

chmod +x /usr/local/bin/start_twitter_marketing

# 2. 创建systemd服务
echo "2. 创建systemd服务..."
cat > /etc/systemd/system/twitter-24hour.service << EOF
[Unit]
Description=Twitter 24-Hour Marketing System
After=network.target
Wants=network.target

[Service]
Type=simple
Restart=always
RestartSec=10
User=root
WorkingDirectory=/root/.openclaw/workspace/skills/twitter-publish
Environment="TWITTER_CONSUMER_KEY=tjEyhVfb4tLIg8hCFXiq50bsk"
Environment="TWITTER_CONSUMER_SECRET=f6KdjKLGjXEG61bOGFOytO3WlnRyXLxFy2uVN9kQ6NZfkLhCWk"
Environment="TWITTER_ACCESS_TOKEN=1005387576-3yyHKgPFR5hfXUMdhkueWGJcmICpaJSD8ZWo7U1"
Environment="TWITTER_ACCESS_TOKEN_SECRET=Yeg9TI2qzDKWTIDXVml9Kcqe2AHTA2xRDtQ50YeBg1u7H"
ExecStart=/usr/bin/python3 /root/.openclaw/workspace/skills/twitter-publish/24hour_scheduler.py --run --interval 2
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# 3. 启用并启动服务
echo "3. 启用并启动服务..."
systemctl daemon-reload
systemctl enable twitter-24hour.service
systemctl start twitter-24hour.service

# 4. 检查状态
echo "4. 检查服务状态..."
sleep 3
systemctl status twitter-24hour.service --no-pager

# 5. 创建监控脚本
echo "5. 创建监控和管理脚本..."
cat > /usr/local/bin/twitter-status << 'EOF'
#!/bin/bash
echo "📊 Twitter营销系统状态"
echo "======================"
systemctl status twitter-24hour.service --no-pager | head -20

echo ""
echo "📝 最近发布的推文:"
cd /root/.openclaw/workspace/skills/twitter-publish
if [ -f "24hour_schedule.json" ]; then
    python3 -c "
import json
with open('24hour_schedule.json') as f:
    data = json.load(f)
print(f'总发布数: {data.get(\"total_posts\", 0)}')
last = data.get('last_post_time')
if last:
    from datetime import datetime
    dt = datetime.fromisoformat(last.replace('Z', '+00:00'))
    print(f'最后发布: {dt.strftime(\"%Y-%m-%d %H:%M UTC\")}')
else:
    print('最后发布: 从未')
"
fi
EOF

chmod +x /usr/local/bin/twitter-status

cat > /usr/local/bin/twitter-restart << 'EOF'
#!/bin/bash
echo "🔄 重启Twitter营销系统..."
systemctl restart twitter-24hour.service
sleep 2
twitter-status
EOF

chmod +x /usr/local/bin/twitter-restart

# 6. 设置cron监控（备用）
echo "6. 设置备用监控..."
(crontab -l 2>/dev/null | grep -v "twitter_monitor"; echo "*/10 * * * * systemctl is-active --quiet twitter-24hour.service || systemctl start twitter-24hour.service") | crontab -

echo ""
echo "🎉 一键永久启动完成！"
echo "=========================================="
echo ""
echo "✅ 系统已配置为:"
echo "   • 开机自动启动"
echo "   • 崩溃自动重启"
echo "   • 24小时不间断运行"
echo ""
echo "📋 管理命令:"
echo "   twitter-status    # 查看系统状态"
echo "   twitter-restart   # 重启系统"
echo "   systemctl stop twitter-24hour.service    # 停止"
echo "   systemctl start twitter-24hour.service   # 启动"
echo ""
echo "🚀 系统正在启动中..."
echo "   每30分钟自动发布一条营销推文"
echo "   24小时不间断，每日最多48条"
echo ""
echo "⏰ 首次启动可能需要几秒钟，请稍候..."