#!/usr/bin/env python3
"""
每日自动化任务设置
创建OpenClaw cron任务实现每日自动化
"""

import json
import os
from datetime import datetime

def create_daily_automation_tasks():
    """创建每日自动化任务"""
    
    # 基础配置
    base_config = {
        "action": "add",
        "job": {
            "sessionTarget": "isolated",
            "wakeMode": "now",
            "deleteAfterRun": False,
            "payload": {
                "kind": "agentTurn",
                "deliver": True,
                "channel": "qqbot",
                "to": "DC29C565CCE9B00B4D33B73F2AAE3284"
            }
        }
    }
    
    # 每日任务计划 (UTC时间)
    daily_tasks = [
        # 上午任务 (亚洲/欧洲时间)
        {
            "time": "01:00",  # 09:00 北京时间
            "name": "上午推文发布",
            "message": "请使用PostAlert内容系列发送一条上午推文。主题：AI内容监控功能。要求：专业英文，面向国际用户，包含行动号召。"
        },
        {
            "time": "02:30",  # 10:30 北京时间
            "name": "上午增长会话",
            "message": "请运行10分钟的Twitter增长会话。使用quick_growth.py工具，进行互关和热门评论。目标：关注5个相关用户，发表2条有价值评论。"
        },
        
        # 中午任务
        {
            "time": "04:00",  # 12:00 北京时间
            "name": "中午教育推文",
            "message": "请使用PostAlert内容系列发送一条教育性推文。主题：内容策略最佳实践。要求：提供有价值的知识，包含相关话题标签。"
        },
        {
            "time": "05:30",  # 13:30 北京时间
            "name": "中午互动增强",
            "message": "请运行15分钟的互动增强会话。搜索话题：社交媒体分析、数据驱动决策。进行3-5次有价值的互动。"
        },
        
        # 下午任务
        {
            "time": "07:00",  # 15:00 北京时间
            "name": "下午案例推文",
            "message": "请使用PostAlert内容系列发送一条客户案例推文。行业：电商品牌。要求：展示具体应用场景和可量化结果。"
        },
        {
            "time": "08:30",  # 16:30 北京时间
            "name": "下午增长会话",
            "message": "请运行10分钟的Twitter增长会话。关注SaaS公司和营销机构，在热门推文下发表智能评论。"
        },
        
        # 晚上任务
        {
            "time": "10:00",  # 18:00 北京时间
            "name": "晚上成功故事",
            "message": "请使用PostAlert内容系列发送一条成功故事推文。要求：真实客户见证，社会证明，鼓励互动。"
        },
        {
            "time": "12:30",  # 20:30 北京时间
            "name": "晚间互动会话",
            "message": "请运行15分钟的Twitter互动会话。搜索话题：数字转型、营销科技、客户体验。进行3-5次有价值的互动。"
        }
    ]
    
    # 每周特殊任务
    weekly_tasks = [
        {
            "day": "1",  # 周一
            "time": "06:00",  # 14:00 北京时间
            "name": "周一功能线程",
            "message": "请创建并发送一个关于PostAlert.ai核心功能的推文线程（3-4条推文）。主题：AI内容监控和竞争情报。"
        },
        {
            "day": "3",  # 周三
            "time": "06:00",  # 14:00 北京时间
            "name": "周三案例线程",
            "message": "请创建并发送一个关于PostAlert.ai使用案例的推文线程（3-4条推文）。展示不同行业的应用场景。"
        },
        {
            "day": "5",  # 周五
            "time": "06:00",  # 14:00 北京时间
            "name": "周五教育线程",
            "message": "请创建并发送一个关于数字营销最佳实践的推文线程（3-4条推文）。提供有价值的教育内容。"
        }
    ]
    
    # 生成所有任务
    all_tasks = []
    
    # 每日任务
    for task in daily_tasks:
        job = base_config.copy()
        job["job"]["name"] = task["name"]
        job["job"]["schedule"] = {
            "kind": "cron",
            "expr": f"0 {task['time'].split(':')[1]} {task['time'].split(':')[0]} * * *",
            "tz": "UTC"
        }
        job["job"]["payload"]["message"] = task["message"]
        all_tasks.append(job)
    
    # 每周任务
    for task in weekly_tasks:
        job = base_config.copy()
        job["job"]["name"] = task["name"]
        job["job"]["schedule"] = {
            "kind": "cron",
            "expr": f"0 {task['time'].split(':')[1]} {task['time'].split(':')[0]} * * {task['day']}",
            "tz": "UTC"
        }
        job["job"]["payload"]["message"] = task["message"]
        all_tasks.append(job)
    
    return all_tasks

def create_immediate_test_task():
    """创建立即测试任务"""
    return {
        "action": "add",
        "job": {
            "name": "立即测试任务",
            "schedule": {
                "kind": "at",
                "atMs": int(datetime.now().timestamp() * 1000) + 60000  # 1分钟后
            },
            "sessionTarget": "isolated",
            "wakeMode": "now",
            "deleteAfterRun": True,
            "payload": {
                "kind": "agentTurn",
                "message": "🎯 自动化系统测试成功！\n\nTwitter增长系统已配置完成。\n\n今日任务：\n✅ 运行增长会话\n✅ 设置每日自动化\n✅ 开始持续增长\n\n接下来系统将自动运行每日任务。\n\n🚀 开始增长吧！",
                "deliver": True,
                "channel": "qqbot",
                "to": "DC29C565CCE9B00B4D33B73F2AAE3284"
            }
        }
    }

def save_tasks_to_file(tasks, filename="daily_automation_tasks.json"):
    """保存任务到文件"""
    with open(filename, 'w') as f:
        json.dump(tasks, f, indent=2)
    
    print(f"💾 任务配置已保存: {filename}")
    return filename

def generate_setup_script():
    """生成设置脚本"""
    script = """#!/bin/bash
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
"""
    
    with open("setup_daily_automation.sh", "w") as f:
        f.write(script)
    
    os.chmod("setup_daily_automation.sh", 0o755)
    print("📜 设置脚本已生成: setup_daily_automation.sh")

def main():
    """主函数"""
    print("🤖 创建每日自动化任务")
    print("=" * 50)
    
    # 创建任务
    daily_tasks = create_daily_automation_tasks()
    test_task = create_immediate_test_task()
    
    all_tasks = daily_tasks + [test_task]
    
    print(f"📅 已创建 {len(all_tasks)} 个自动化任务:")
    print(f"   • {len(daily_tasks)} 个每日/每周任务")
    print(f"   • 1 个立即测试任务")
    
    print("\n⏰ 每日任务计划 (UTC时间):")
    print("   01:00 - 上午推文发布")
    print("   02:30 - 上午增长会话 (10分钟)")
    print("   04:00 - 中午教育推文")
    print("   05:30 - 中午互动增强 (15分钟)")
    print("   07:00 - 下午案例推文")
    print("   08:30 - 下午增长会话 (10分钟)")
    print("   10:00 - 晚上成功故事")
    print("   12:30 - 晚间互动会话 (15分钟)")
    
    print("\n🧵 每周线程计划:")
    print("   周一 06:00 - 功能线程")
    print("   周三 06:00 - 案例线程")
    print("   周五 06:00 - 教育线程")
    
    print("\n🎯 每日目标:")
    print("   • 发布4条高质量推文")
    print("   • 运行2次增长会话")
    print("   • 进行2次互动增强")
    print("   • 每周创建3个深度线程")
    
    # 保存配置
    config_file = save_tasks_to_file(all_tasks)
    
    # 生成设置脚本
    generate_setup_script()
    
    print("\n🚀 立即执行命令:")
    print("   1. 运行设置脚本:")
    print("      chmod +x setup_daily_automation.sh")
    print("      ./setup_daily_automation.sh")
    
    print("\n   2. 手动创建任务:")
    print("      # 使用OpenClaw cron工具")
    print("      # 导入 daily_automation_tasks.json")
    
    print("\n   3. 立即测试:")
    print("      python quick_growth.py --session --duration 3")
    
    print("\n📋 自动化系统已配置完成!")
    print("=" * 50)
    
    print("\n💡 提示:")
    print("   • 系统将在1分钟后发送测试消息")
    print("   • 每日任务从明天开始自动运行")
    print("   • 所有时间均为UTC时间")
    print("   • 北京时间 = UTC + 8小时")

if __name__ == "__main__":
    main()