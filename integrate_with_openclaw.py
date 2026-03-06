#!/usr/bin/env python3
"""
集成Twitter自动化到OpenClaw
创建cron任务并设置完整系统
"""

import json
import os
import subprocess
from datetime import datetime

class OpenClawIntegrator:
    """OpenClaw集成器"""
    
    def __init__(self):
        self.workspace_path = "/root/.openclaw/workspace"
        self.skill_path = os.path.join(self.workspace_path, "skills/twitter-publish")
        
    def create_cron_tasks(self):
        """创建OpenClaw cron任务"""
        
        # 读取自动化配置
        config_file = os.path.join(self.skill_path, "daily_automation_tasks.json")
        
        try:
            with open(config_file, 'r') as f:
                tasks = json.load(f)
        except FileNotFoundError:
            print(f"❌ 配置文件不存在: {config_file}")
            return False
        
        print(f"📋 找到 {len(tasks)} 个自动化任务")
        
        # 创建执行脚本
        self._create_execution_script()
        
        # 显示任务详情
        print("\n🎯 自动化任务详情:")
        for i, task in enumerate(tasks, 1):
            job = task.get("job", {})
            name = job.get("name", f"任务{i}")
            schedule = job.get("schedule", {})
            
            if schedule.get("kind") == "cron":
                expr = schedule.get("expr", "")
                print(f"  {i}. {name}")
                print(f"     计划: {expr} UTC")
            
            elif schedule.get("kind") == "at":
                at_time = datetime.fromtimestamp(schedule.get("atMs", 0) / 1000)
                print(f"  {i}. {name}")
                print(f"     时间: {at_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
    
    def _create_execution_script(self):
        """创建执行脚本"""
        script_content = """#!/bin/bash
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
"""
        
        script_path = os.path.join(self.skill_path, "run_twitter_task.sh")
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        os.chmod(script_path, 0o755)
        print(f"📜 执行脚本已创建: {script_path}")
        
        return script_path
    
    def create_openclaw_cron_commands(self):
        """生成OpenClaw cron命令"""
        
        commands = [
            "# 🚀 Twitter自动化cron命令",
            "# 在OpenClaw中执行以下命令创建定时任务",
            "",
            "# 上午任务",
            "openclaw cron add --name '上午推文发布' --expr '0 1 * * *' --command 'cd /root/.openclaw/workspace/skills/twitter-publish && ./run_twitter_task.sh morning_tweet'",
            "openclaw cron add --name '上午增长会话' --expr '30 2 * * *' --command 'cd /root/.openclaw/workspace/skills/twitter-publish && ./run_twitter_task.sh morning_growth'",
            "",
            "# 中午任务",
            "openclaw cron add --name '中午教育推文' --expr '0 4 * * *' --command 'cd /root/.openclaw/workspace/skills/twitter-publish && ./run_twitter_task.sh noon_educational'",
            "openclaw cron add --name '中午互动增强' --expr '30 5 * * *' --command 'cd /root/.openclaw/workspace/skills/twitter-publish && ./run_twitter_task.sh noon_engagement'",
            "",
            "# 下午任务",
            "openclaw cron add --name '下午案例推文' --expr '0 7 * * *' --command 'cd /root/.openclaw/workspace/skills/twitter-publish && ./run_twitter_task.sh afternoon_case'",
            "openclaw cron add --name '下午增长会话' --expr '30 8 * * *' --command 'cd /root/.openclaw/workspace/skills/twitter-publish && ./run_twitter_task.sh afternoon_growth'",
            "",
            "# 晚上任务",
            "openclaw cron add --name '晚上成功故事' --expr '0 10 * * *' --command 'cd /root/.openclaw/workspace/skills/twitter-publish && ./run_twitter_task.sh evening_success'",
            "openclaw cron add --name '晚间互动会话' --expr '30 12 * * *' --command 'cd /root/.openclaw/workspace/skills/twitter-publish && ./run_twitter_task.sh evening_engagement'",
            "",
            "# 每周线程任务",
            "openclaw cron add --name '周一功能线程' --expr '0 6 * * 1' --command 'cd /root/.openclaw/workspace/skills/twitter-publish && ./run_twitter_task.sh monday_thread'",
            "openclaw cron add --name '周三案例线程' --expr '0 6 * * 3' --command 'cd /root/.openclaw/workspace/skills/twitter-publish && ./run_twitter_task.sh wednesday_thread'",
            "openclaw cron add --name '周五教育线程' --expr '0 6 * * 5' --command 'cd /root/.openclaw/workspace/skills/twitter-publish && ./run_twitter_task.sh friday_thread'",
            "",
            "# 查看所有任务",
            "openclaw cron list",
            "",
            "# 测试单个任务",
            "openclaw cron run --name '上午推文发布'",
            "",
            "# 删除任务（如果需要）",
            "# openclaw cron remove --name '任务名称'",
        ]
        
        commands_file = os.path.join(self.skill_path, "openclaw_cron_commands.txt")
        
        with open(commands_file, 'w') as f:
            f.write('\n'.join(commands))
        
        print(f"📝 OpenClaw命令已保存: {commands_file}")
        
        return commands_file
    
    def test_system(self):
        """测试系统"""
        print("🧪 测试Twitter自动化系统...")
        
        tests = [
            ("测试推文生成", "python3 postalert_content_series.py --feature 0 --dry-run"),
            ("测试增长工具", "python3 quick_growth.py --plan"),
            ("测试互动增强", "python3 engagement_enhancer.py --stats"),
            ("测试执行脚本", "./run_twitter_task.sh morning_tweet"),
        ]
        
        for test_name, command in tests:
            print(f"\n🔍 {test_name}...")
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    cwd=self.skill_path,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    print(f"✅ {test_name} 成功")
                    if result.stdout:
                        print(f"   输出: {result.stdout[:100]}...")
                else:
                    print(f"❌ {test_name} 失败")
                    if result.stderr:
                        print(f"   错误: {result.stderr[:100]}")
                        
            except subprocess.TimeoutExpired:
                print(f"⏰ {test_name} 超时")
            except Exception as e:
                print(f"⚠️ {test_name} 异常: {e}")
        
        print("\n✅ 系统测试完成")
    
    def show_summary(self):
        """显示总结"""
        print("🎯 Twitter自动化系统总结")
        print("=" * 50)
        
        print("\n📁 已创建文件:")
        files = [
            "run_twitter_task.sh - 执行脚本",
            "daily_automation_tasks.json - 任务配置",
            "openclaw_cron_commands.txt - OpenClaw命令",
            "setup_daily_automation.sh - 设置脚本",
        ]
        
        for file in files:
            print(f"  • {file}")
        
        print("\n🛠️ 可用工具:")
        tools = [
            "quick_growth.py - 快速增长工具",
            "follow_growth.py - 高级增长工具",
            "engagement_enhancer.py - 互动增强",
            "postalert_content_series.py - 内容系列",
            "hourly_scheduler.py - 定时发布",
        ]
        
        for tool in tools:
            print(f"  • {tool}")
        
        print("\n⏰ 每日计划 (北京时间):")
        schedule = [
            "09:00 - 上午推文发布",
            "10:30 - 上午增长会话",
            "12:00 - 中午教育推文",
            "13:30 - 中午互动增强",
            "15:00 - 下午案例推文",
            "16:30 - 下午增长会话",
            "18:00 - 晚上成功故事",
            "20:30 - 晚间互动会话",
        ]
        
        for item in schedule:
            print(f"  • {item}")
        
        print("\n🚀 立即开始:")
        print("  1. 运行设置脚本:")
        print("     cd /root/.openclaw/workspace/skills/twitter-publish")
        print("     chmod +x setup_daily_automation.sh")
        print("     ./setup_daily_automation.sh")
        
        print("\n  2. 创建OpenClaw cron任务:")
        print("     # 执行 openclaw_cron_commands.txt 中的命令")
        
        print("\n  3. 测试系统:")
        print("     python3 integrate_with_openclaw.py --test")
        
        print("\n✅ 系统已准备就绪!")
        print("=" * 50)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="集成Twitter自动化到OpenClaw")
    parser.add_argument('--setup', action='store_true', help='设置完整系统')
    parser.add_argument('--test', action='store_true', help='测试系统')
    parser.add_argument('--summary', action='store_true', help='显示总结')
    
    args = parser.parse_args()
    
    integrator = OpenClawIntegrator()
    
    if args.setup:
        print("🚀 设置Twitter自动化系统")
        print("=" * 50)
        
        integrator.create_cron_tasks()
        integrator.create_openclaw_cron_commands()
        integrator.test_system()
        integrator.show_summary()
    
    elif args.test:
        integrator.test_system()
    
    elif args.summary:
        integrator.show_summary()
    
    else:
        print("🤖 Twitter自动化集成工具")
        print("\n使用方法:")
        print("  python integrate_with_openclaw.py --setup    # 设置完整系统")
        print("  python integrate_with_openclaw.py --test     # 测试系统")
        print("  python integrate_with_openclaw.py --summary  # 显示总结")
        print("\n功能:")
        print("  • 创建OpenClaw cron任务")
        print("  • 生成执行脚本")
        print("  • 测试所有组件")
        print("  • 显示完整总结")

if __name__ == "__main__":
    main()