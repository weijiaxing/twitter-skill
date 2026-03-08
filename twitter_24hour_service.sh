#!/bin/bash
# Twitter 24小时营销系统 - 系统服务脚本
# 可以注册为systemd服务，实现开机自启和自动恢复

SERVICE_NAME="twitter-24hour-marketing"
SCRIPT_DIR="/root/.openclaw/workspace/skills/twitter-publish"
LOG_FILE="/var/log/twitter_marketing.log"
PID_FILE="/var/run/twitter_marketing.pid"

# 环境变量
export TWITTER_CONSUMER_KEY="tjEyhVfb4tLIg8hCFXiq50bsk"
export TWITTER_CONSUMER_SECRET="f6KdjKLGjXEG61bOGFOytO3WlnRyXLxFy2uVN9kQ6NZfkLhCWk"
export TWITTER_ACCESS_TOKEN="1005387576-3yyHKgPFR5hfXUMdhkueWGJcmICpaJSD8ZWo7U1"
export TWITTER_ACCESS_TOKEN_SECRET="Yeg9TI2qzDKWTIDXVml9Kcqe2AHTA2xRDtQ50YeBg1u7H"

start_service() {
    echo "🚀 启动Twitter 24小时营销系统服务..."
    
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "⚠️  服务已在运行 (PID: $(cat $PID_FILE))"
        return 1
    fi
    
    cd "$SCRIPT_DIR"
    
    # 启动调度器（后台运行，记录日志）
    nohup python3 24hour_scheduler.py --run --interval 2 >> "$LOG_FILE" 2>&1 &
    PID=$!
    
    echo $PID > "$PID_FILE"
    echo "✅ 服务已启动 (PID: $PID)"
    echo "📝 日志文件: $LOG_FILE"
    
    # 等待几秒检查是否启动成功
    sleep 3
    if kill -0 $PID 2>/dev/null; then
        echo "🎉 24小时营销系统运行中..."
        echo "   • 每30分钟自动发布"
        echo "   • 24小时不间断"
        echo "   • 每日最大48条推文"
        return 0
    else
        echo "❌ 服务启动失败，检查日志: $LOG_FILE"
        rm -f "$PID_FILE"
        return 1
    fi
}

stop_service() {
    echo "🛑 停止Twitter营销系统服务..."
    
    if [ ! -f "$PID_FILE" ]; then
        echo "⚠️  PID文件不存在，服务可能未运行"
        return 1
    fi
    
    PID=$(cat "$PID_FILE")
    
    if kill -0 $PID 2>/dev/null; then
        kill $PID
        sleep 2
        
        if kill -0 $PID 2>/dev/null; then
            kill -9 $PID
            echo "⚠️  强制终止服务 (PID: $PID)"
        else
            echo "✅ 服务已停止 (PID: $PID)"
        fi
        
        rm -f "$PID_FILE"
        return 0
    else
        echo "⚠️  进程不存在 (PID: $PID)，清理PID文件"
        rm -f "$PID_FILE"
        return 1
    fi
}

restart_service() {
    stop_service
    sleep 2
    start_service
}

status_service() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 $PID 2>/dev/null; then
            echo "✅ Twitter营销系统运行中 (PID: $PID)"
            echo "📊 查看最新日志: tail -f $LOG_FILE"
            
            # 显示最后几条日志
            echo ""
            echo "最近日志:"
            tail -10 "$LOG_FILE" 2>/dev/null || echo "无日志记录"
        else
            echo "❌ 服务PID存在但进程未运行"
            rm -f "$PID_FILE"
        fi
    else
        echo "❌ 服务未运行"
    fi
}

# 创建systemd服务文件
create_systemd_service() {
    echo "🔧 创建systemd服务文件..."
    
    SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
    
    cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Twitter 24-Hour Marketing System
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=10
User=root
WorkingDirectory=$SCRIPT_DIR
Environment="TWITTER_CONSUMER_KEY=tjEyhVfb4tLIg8hCFXiq50bsk"
Environment="TWITTER_CONSUMER_SECRET=f6KdjKLGjXEG61bOGFOytO3WlnRyXLxFy2uVN9kQ6NZfkLhCWk"
Environment="TWITTER_ACCESS_TOKEN=1005387576-3yyHKgPFR5hfXUMdhkueWGJcmICpaJSD8ZWo7U1"
Environment="TWITTER_ACCESS_TOKEN_SECRET=Yeg9TI2qzDKWTIDXVml9Kcqe2AHTA2xRDtQ50YeBg1u7H"
ExecStart=/usr/bin/python3 $SCRIPT_DIR/24hour_scheduler.py --run --interval 2
StandardOutput=append:$LOG_FILE
StandardError=append:$LOG_FILE

[Install]
WantedBy=multi-user.target
EOF

    echo "✅ systemd服务文件已创建: $SERVICE_FILE"
    echo ""
    echo "使用以下命令管理服务:"
    echo "  sudo systemctl daemon-reload"
    echo "  sudo systemctl enable $SERVICE_NAME  # 开机自启"
    echo "  sudo systemctl start $SERVICE_NAME   # 启动服务"
    echo "  sudo systemctl status $SERVICE_NAME  # 查看状态"
    echo "  sudo systemctl stop $SERVICE_NAME    # 停止服务"
}

case "$1" in
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        restart_service
        ;;
    status)
        status_service
        ;;
    install)
        create_systemd_service
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|install}"
        echo ""
        echo "Twitter 24小时营销系统管理脚本"
        echo ""
        echo "选项:"
        echo "  start    启动24小时营销系统"
        echo "  stop     停止营销系统"
        echo "  restart  重启营销系统"
        echo "  status   查看系统状态"
        echo "  install  安装为systemd服务（推荐）"
        echo ""
        echo "推荐使用:"
        echo "  $0 install    # 安装为系统服务"
        echo "  systemctl start twitter-24hour-marketing  # 启动服务"
        echo "  systemctl enable twitter-24hour-marketing # 开机自启"
        exit 1
        ;;
esac