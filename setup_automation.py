#!/usr/bin/env python3
"""
设置自动化发布系统
创建OpenClaw cron任务实现每小时自动发布
"""

import json
from datetime import datetime

def create_hourly_cron_jobs():
    """创建每小时发布任务"""
    
    # 基础cron配置
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
    
    # 定义不同时间的发布内容
    hourly_schedule = [
        {
            "hour": 9,
            "name": "上午功能推文",
            "message": "请使用PostAlert内容系列发送一条功能推文。主题：AI内容监控。要求：专业英文，面向国际用户，包含行动号召。"
        },
        {
            "hour": 10,
            "name": "行业洞察推文",
            "message": "请使用PostAlert内容系列发送一条教育性推文。主题：内容策略趋势。要求：提供有价值的知识，包含相关话题标签。"
        },
        {
            "hour": 11,
            "name": "使用案例推文",
            "message": "请使用PostAlert内容系列发送一条使用案例推文。行业：电商品牌。要求：展示具体应用场景和结果。"
        },
        {
            "hour": 12,
            "name": "成功故事推文",
            "message": "请使用PostAlert内容系列发送一条成功案例推文。要求：真实客户故事，可量化结果，社会证明。"
        },
        {
            "hour": 13,
            "name": "问题解决方案",
            "message": "请使用PostAlert内容系列发送一条问题解决推文。问题：社交媒体监控困难。要求：展示PostAlert.ai的解决方案。"
        },
        {
            "hour": 14,
            "name": "功能深度介绍",
            "message": "请使用PostAlert内容系列发送一条功能深度介绍推文。功能：竞争情报。要求：详细说明价值和优势。"
        },
        {
            "hour": 15,
            "name": "教育内容推文",
            "message": "请使用PostAlert内容系列发送一条教育性推文。主题：数据驱动决策。要求：专业见解，行动建议。"
        },
        {
            "hour": 16,
            "name": "客户见证推文",
            "message": "请使用PostAlert内容系列发送一条客户见证推文。要求：真实引用，可信结果，鼓励互动。"
        },
        {
            "hour": 17,
            "name": "产品更新推文",
            "message": "请使用PostAlert内容系列发送一条产品更新推文。主题：新功能或改进。要求：兴奋语气，明确价值。"
        },
        {
            "hour": 18,
            "name": "行业趋势推文",
            "message": "请使用PostAlert内容系列发送一条行业趋势推文。主题：AI在营销中的应用。要求：前瞻性见解，专业分析。"
        }
    ]
    
    cron_jobs = []
    
    for schedule in hourly_schedule:
        job = base_config.copy()
        job["job"]["name"] = schedule["name"]
        job["job"]["schedule"] = {
            "kind": "cron",
            "expr": f"0 {schedule['hour']} * * *",
            "tz": "UTC"
        }
        job["job"]["payload"]["message"] = schedule["message"]
        
        cron_jobs.append(job)
    
    return cron_jobs

def create_engagement_sessions():
    """创建互动会话任务"""
    
    engagement_sessions = [
        {
            "name": "上午互动会话",
            "time": "10:30",
            "duration": 15,
            "message": "请运行15分钟的Twitter互动会话。搜索话题：AI营销、内容监控、竞争情报。进行3-5次有价值的互动。"
        },
        {
            "name": "下午互动会话", 
            "time": "15:30",
            "duration": 15,
            "message": "请运行15分钟的Twitter互动会话。搜索话题：社交媒体分析、数据驱动决策、B2B营销。进行3-5次有价值的互动。"
        },
        {
            "name": "晚间互动会话",
            "time": "20:30",
            "duration": 15,
            "message": "请运行15分钟的Twitter互动会话。搜索话题：数字转型、营销科技、客户体验。进行3-5次有价值的互动。"
        }
    ]
    
    sessions = []
    
    for session in engagement_sessions:
        job = {
            "action": "add",
            "job": {
                "name": session["name"],
                "schedule": {
                    "kind": "cron",
                    "expr": f"30 {session['time'].split(':')[0]} * * *",
                    "tz": "UTC"
                },
                "sessionTarget": "isolated",
                "wakeMode": "now",
                "deleteAfterRun": False,
                "payload": {
                    "kind": "agentTurn",
                    "message": session["message"],
                    "deliver": True,
                    "channel": "qqbot",
                    "to": "DC29C565CCE9B00B4D33B73F2AAE3284"
                }
            }
        }
        sessions.append(job)
    
    return sessions

def create_thread_creation_tasks():
    """创建线程生成任务"""
    
    thread_tasks = [
        {
            "name": "周一功能线程",
            "day": "1",  # 周一
            "time": "14:00",
            "topic": "core_features",
            "message": "请创建并发送一个关于PostAlert.ai核心功能的推文线程（3-4条推文）。主题：AI内容监控和竞争情报。"
        },
        {
            "name": "周三案例线程",
            "day": "3",  # 周三
            "time": "14:00",
            "topic": "use_cases",
            "message": "请创建并发送一个关于PostAlert.ai使用案例的推文线程（3-4条推文）。展示不同行业的应用场景。"
        },
        {
            "name": "周五教育线程",
            "day": "5",  # 周五
            "time": "14:00",
            "topic": "educational",
            "message": "请创建并发送一个关于数字营销最佳实践的推文线程（3-4条推文）。提供有价值的教育内容。"
        }
    ]
    
    tasks = []
    
    for task in thread_tasks:
        job = {
            "action": "add",
            "job": {
                "name": task["name"],
                "schedule": {
                    "kind": "cron",
                    "expr": f"0 {task['time'].split(':')[1]} {task['time'].split(':')[0]} * * {task['day']}",
                    "tz": "UTC"
                },
                "sessionTarget": "isolated",
                "wakeMode": "now",
                "deleteAfterRun": False,
                "payload": {
                    "kind": "agentTurn",
                    "message": task["message"],
                    "deliver": True,
                    "channel": "qqbot",
                    "to": "DC29C565CCE9B00B4D33B73F2AAE3284"
                }
            }
        }
        tasks.append(job)
    
    return tasks

def main():
    """主函数"""
    print("🤖 创建自动化发布系统")
    print("=" * 50)
    
    # 创建所有任务
    hourly_jobs = create_hourly_cron_jobs()
    engagement_sessions = create_engagement_sessions()
    thread_tasks = create_thread_creation_tasks()
    
    all_tasks = hourly_jobs + engagement_sessions + thread_tasks
    
    print(f"📅 已创建 {len(all_tasks)} 个自动化任务:")
    print(f"   • {len(hourly_jobs)} 个每小时发布任务")
    print(f"   • {len(engagement_sessions)} 个互动会话任务")
    print(f"   • {len(thread_tasks)} 个线程创建任务")
    
    print("\n⏰ 发布计划 (UTC时间):")
    print("   9:00  - 功能推文")
    print("   10:00 - 教育内容")
    print("   10:30 - 互动会话")
    print("   11:00 - 使用案例")
    print("   12:00 - 成功故事")
    print("   13:00 - 问题解决")
    print("   14:00 - 功能深度")
    print("   15:00 - 教育内容")
    print("   15:30 - 互动会话")
    print("   16:00 - 客户见证")
    print("   17:00 - 产品更新")
    print("   18:00 - 行业趋势")
    print("   20:30 - 互动会话")
    
    print("\n🧵 每周线程计划:")
    print("   周一 14:00 - 核心功能线程")
    print("   周三 14:00 - 使用案例线程")
    print("   周五 14:00 - 教育内容线程")
    
    # 保存配置文件
    config_file = "automation_config.json"
    with open(config_file, 'w') as f:
        json.dump(all_tasks, f, indent=2)
    
    print(f"\n💾 配置文件已保存: {config_file}")
    
    print("\n🚀 立即执行命令:")
    print("   1. 测试自动化系统:")
    print("      python hourly_scheduler.py --test")
    print("   2. 运行互动演示:")
    print("      python engagement_enhancer.py --session")
    print("   3. 创建更多线程:")
    print("      python postalert_content_series.py --thread use_cases")
    
    print("\n📋 自动化系统已就绪!")
    print("=" * 50)

if __name__ == "__main__":
    main()