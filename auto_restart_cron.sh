#!/bin/bash
# 自动重启脚本 - 通过cron定时检查并重启调度器

SCRIPT_DIR="/root/.openclaw/workspace/skills/twitter-publish"
PID_FILE="/tmp/twitter_scheduler.pid"
LOG_FILE="/var/log/twitter_auto_restart.log"

# 环境变量
export TWITTER_CONSUMER_KEY="tjEyhVfb4tLIg8hCFXiq50bsk"
export TWITTER_CONSUMER_SECRET="f6KdjKLGjXEG61bOGFOytO3WlnRyXLxFy2uVN9kQ6NZfkLhCWk"
export TWITTER_ACCESS_TOKEN="1005387576-3yyHKgPFR5hfXUMdhkueWGJcmICpaJSD8ZWo7U1"
export TWITTER_ACCESS_TOKEN_SECRET="Yeg9TI2qzDKWTIDXVml9Kcqe2AHTA2xRDtQ50YeBg1u7H"

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

check_and_restart() {
    log_message "🔍 检查Twitter调度器状态..."
    
    # 检查进程是否在运行
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 $PID 2>/dev/null; then
            log_message "✅ 调度器运行正常 (PID: $PID)"
            return 0
        else
            log_message "⚠️  进程不存在 (PID: $PID)，需要重启"
            rm -f "$PID_FILE"
        fi
    else
        log_message "⚠️  PID文件不存在，调度器可能未运行"
    fi
    
    # 重启调度器
    log_message "🚀 启动Twitter 24小时调度器..."
    
    cd "$SCRIPT_DIR"
    
    # 停止可能存在的旧进程
    pkill -f "24hour_scheduler.py" 2>/dev/null
    sleep 2
    
    # 启动新进程
    nohup python3 24hour_scheduler.py --run --interval 2 > /dev/null 2>&1 &
    NEW_PID=$!
    
    echo $NEW_PID > "$PID_FILE"
    log_message "✅ 调度器已启动 (PID: $NEW_PID)"
    
    # 验证启动
    sleep 5
    if kill -0 $NEW_PID 2>/dev/null; then
        log_message "🎉 24小时营销系统启动成功"
        return 0
    else
        log_message "❌ 调度器启动失败"
        rm -f "$PID_FILE"
        return 1
    fi
}

setup_cron() {
    echo "🔧 设置自动重启cron任务..."
    
    CRON_JOB="*/5 * * * * $SCRIPT_DIR/auto_restart_cron.sh check >> $LOG_FILE 2>&1"
    
    # 添加到当前用户的crontab
    (crontab -l 2>/dev/null | grep -v "auto_restart_cron.sh"; echo "$CRON_JOB") | crontab -
    
    echo "✅ cron任务已设置: 每5分钟检查一次"
    echo "📝 日志文件: $LOG_FILE"
    echo ""
    echo "当前cron任务:"
    crontab -l | grep "auto_restart_cron"
}

show_status() {
    echo "📊 Twitter营销系统状态检查"
    echo "=============================="
    
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 $PID 2>/dev/null; then
            echo "✅ 状态: 运行中 (PID: $PID)"
            
            # 检查进程信息
            if ps -p $PID > /dev/null; then
                echo "⏰ 运行时间: $(ps -p $PID -o etime=)"
                echo "📝 命令行: $(ps -p $PID -o cmd= | head -1)"
            fi
        else
            echo "❌ 状态: PID存在但进程未运行"
        fi
    else
        echo "❌ 状态: 未运行"
    fi
    
    echo ""
    echo "📋 最近日志:"
    tail -20 "$LOG_FILE" 2>/dev/null || echo "无日志记录"
}

case "$1" in
    check)
        check_and_restart
        ;;
    setup)
        setup_cron
        ;;
    status)
        show_status
        ;;
    start)
        check_and_restart
        ;;
    stop)
        log_message "🛑 手动停止调度器..."
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            kill $PID 2>/dev/null
            rm -f "$PID_FILE"
            log_message "✅ 调度器已停止"
        fi
        pkill -f "24hour_scheduler.py" 2>/dev/null
        echo "✅ 调度器已停止"
        ;;
    *)
        echo "Twitter营销系统自动重启管理"
        echo ""
        echo "用法: $0 {check|setup|status|start|stop}"
        echo ""
        echo "选项:"
        echo "  check   检查并重启调度器（cron调用）"
        echo "  setup   设置cron自动重启任务"
        echo "  status  查看系统状态"
        echo "  start   启动调度器"
        echo "  stop    停止调度器"
        echo ""
        echo "推荐步骤:"
        echo "  1. $0 setup    # 设置自动重启"
        echo "  2. $0 start    # 立即启动"
        echo "  3. $0 status   # 查看状态"
        echo ""
        echo "设置后，系统会每5分钟自动检查并确保调度器运行"
        exit 1
        ;;
esac