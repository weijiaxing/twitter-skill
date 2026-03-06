#!/usr/bin/env python3
"""
Automated English Tweets for Product Promotion
自动英文推文发布系统 - 专为产品宣传设计
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from twitter_tool import TwitterTool
    from english_tweet_generator import EnglishTweetGenerator
except ImportError:
    print("❌ 需要先安装依赖: pip install tweepy")
    sys.exit(1)

class EnglishTweetAutomation:
    """英文推文自动化系统"""
    
    def __init__(self, product_name: str = "OpenClaw AI", company_name: str = "OpenClaw"):
        """初始化"""
        self.product_name = product_name
        self.company_name = company_name
        
        # 初始化组件
        self.generator = EnglishTweetGenerator(product_name, company_name)
        self.twitter_tool = TwitterTool()
        
        # 内容日历
        self.content_calendar = self._create_content_calendar()
        
        # 状态跟踪
        self.stats_file = "tweet_stats.json"
        self.stats = self._load_stats()
    
    def _create_content_calendar(self) -> Dict:
        """创建内容日历"""
        return {
            "Monday": {
                "theme": "Product Focus",
                "types": ["product_launch", "feature_highlight"],
                "time_slots": ["09:00", "14:00", "19:00"]
            },
            "Tuesday": {
                "theme": "Educational Content",
                "types": ["educational", "how_to", "tutorial"],
                "time_slots": ["10:00", "15:00", "20:00"]
            },
            "Wednesday": {
                "theme": "Customer Success",
                "types": ["success_story", "testimonial", "case_study"],
                "time_slots": ["08:00", "13:00", "18:00"]
            },
            "Thursday": {
                "theme": "Industry Insights",
                "types": ["industry_insights", "trend_analysis", "thought_leadership"],
                "time_slots": ["11:00", "16:00", "21:00"]
            },
            "Friday": {
                "theme": "Problem Solving",
                "types": ["problem_solution", "qna", "tips"],
                "time_slots": ["09:30", "14:30", "19:30"]
            },
            "Saturday": {
                "theme": "Community Engagement",
                "types": ["question", "poll", "discussion"],
                "time_slots": ["12:00", "17:00"]
            },
            "Sunday": {
                "theme": "Weekly Recap",
                "types": ["recap", "insights", "preview"],
                "time_slots": ["10:00", "15:00"]
            }
        }
    
    def _load_stats(self) -> Dict:
        """加载统计数据"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # 默认统计
        return {
            "total_tweets": 0,
            "last_tweet_date": None,
            "daily_count": {},
            "engagement": {"likes": 0, "retweets": 0, "replies": 0},
            "best_performing": []
        }
    
    def _save_stats(self):
        """保存统计数据"""
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def generate_tweet_for_today(self) -> str:
        """生成今日推文"""
        day_of_week = datetime.now().strftime("%A")
        
        print(f"📅 Generating tweet for {day_of_week}...")
        
        # 根据星期几选择内容类型
        if day_of_week == "Monday":
            return self.generator.generate_product_launch(
                feature="AI-Powered Workflow Automation",
                description="Streamline your processes with intelligent automation.",
                link="https://openclaw.ai/automation"
            )
        
        elif day_of_week == "Tuesday":
            return self.generator.generate_educational_tweet(
                topic="automating repetitive tasks",
                tip="Start with email processing",
                explanation="Email automation can save 5+ hours per week for knowledge workers."
            )
        
        elif day_of_week == "Wednesday":
            return self.generator.generate_success_story(
                company="DataTech Solutions",
                result="reduced manual data entry by 80%",
                quote="\"OpenClaw's automation transformed our data processing workflow.\""
            )
        
        elif day_of_week == "Thursday":
            return self.generator.generate_industry_insight(
                trend="AI-assisted decision making",
                analysis="Businesses using AI for decisions see 25% better outcomes.",
                perspective="The future is augmented intelligence, not replacement."
            )
        
        elif day_of_week == "Friday":
            return self.generator.generate_problem_solution(
                problem="inefficient workflow management",
                solutions=[
                    "Automating task assignments",
                    "Streamlining approval processes",
                    "Providing real-time progress tracking"
                ],
                link="https://openclaw.ai/workflow"
            )
        
        elif day_of_week == "Saturday":
            # 社区互动问题
            return self.generator.generate_industry_insight(
                trend="Remote team collaboration",
                analysis="Effective remote work requires the right tools and processes.",
                perspective="What's your biggest challenge with remote collaboration? 👇"
            )
        
        else:  # Sunday
            return self.generator.generate_educational_tweet(
                topic="preparing for the week ahead",
                tip="Review and plan your automation opportunities",
                explanation="Identify 2-3 repetitive tasks to automate this week for maximum impact."
            )
    
    def generate_thread_for_topic(self, topic: str, num_tweets: int = 3) -> List[str]:
        """为特定主题生成线程"""
        print(f"🧵 Generating thread about '{topic}' ({num_tweets} tweets)...")
        return self.generator.generate_thread(topic, num_tweets)
    
    def send_tweet(self, content: str, reply_to: Optional[str] = None) -> Optional[str]:
        """发送推文"""
        print(f"📤 Sending tweet: {content[:50]}...")
        
        tweet_id = self.twitter_tool.send_tweet(content, reply_to)
        
        if tweet_id:
            # 更新统计
            today = datetime.now().strftime("%Y-%m-%d")
            self.stats["total_tweets"] += 1
            self.stats["last_tweet_date"] = today
            
            if today not in self.stats["daily_count"]:
                self.stats["daily_count"][today] = 0
            self.stats["daily_count"][today] += 1
            
            self._save_stats()
            
            print(f"✅ Tweet sent successfully! ID: {tweet_id}")
            return tweet_id
        else:
            print("❌ Failed to send tweet")
            return None
    
    def send_thread(self, tweets: List[str]) -> List[str]:
        """发送推文线程"""
        tweet_ids = []
        previous_tweet_id = None
        
        for i, tweet_content in enumerate(tweets, 1):
            print(f"\n📤 Sending thread tweet {i}/{len(tweets)}...")
            
            tweet_id = self.send_tweet(tweet_content, previous_tweet_id)
            if tweet_id:
                tweet_ids.append(tweet_id)
                previous_tweet_id = tweet_id
                
                # 线程间短暂延迟
                if i < len(tweets):
                    time.sleep(2)
            else:
                print(f"❌ Failed to send tweet {i}, stopping thread")
                break
        
        return tweet_ids
    
    def schedule_daily_tweet(self, scheduled_time: str = "09:00"):
        """安排每日推文（模拟）"""
        print(f"⏰ Scheduling daily tweet for {scheduled_time}...")
        
        # 在实际使用中，这里会集成到OpenClaw的cron系统
        # 现在只是生成推文内容
        
        tweet_content = self.generate_tweet_for_today()
        print(f"📝 Scheduled tweet content:\n{tweet_content}")
        
        return tweet_content
    
    def get_weekly_schedule(self) -> Dict:
        """获取每周发布计划"""
        schedule = {}
        
        for day, info in self.content_calendar.items():
            schedule[day] = {
                "theme": info["theme"],
                "tweet_count": len(info["time_slots"]),
                "times": info["time_slots"],
                "example": self._get_example_for_day(day)
            }
        
        return schedule
    
    def _get_example_for_day(self, day: str) -> str:
        """获取某天的示例推文"""
        # 临时设置日期来生成示例
        original_date = datetime.now()
        
        # 模拟该日期
        day_map = {
            "Monday": 0, "Tuesday": 1, "Wednesday": 2,
            "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6
        }
        
        # 生成示例（简化版）
        examples = {
            "Monday": "🚀 New AI feature launch for workflow automation...",
            "Tuesday": "💡 Tip: Automate email processing to save 5+ hours weekly...",
            "Wednesday": "🏆 Customer success: 80% reduction in manual work...",
            "Thursday": "📊 Industry insight: AI-assisted decisions improve outcomes by 25%...",
            "Friday": "🔧 Solve inefficient workflows with smart automation...",
            "Saturday": "🤔 Question: What's your biggest remote work challenge?...",
            "Sunday": "📚 Weekly prep: Identify 2-3 tasks to automate this week..."
        }
        
        return examples.get(day, "Daily update about AI automation")
    
    def show_stats(self):
        """显示统计信息"""
        print("\n📊 Tweet Statistics:")
        print(f"   Total Tweets: {self.stats['total_tweets']}")
        print(f"   Last Tweet: {self.stats.get('last_tweet_date', 'Never')}")
        
        if self.stats['daily_count']:
            print(f"   Daily Count (last 7 days):")
            dates = sorted(self.stats['daily_count'].keys(), reverse=True)[:7]
            for date in dates:
                count = self.stats['daily_count'][date]
                print(f"     {date}: {count} tweet{'s' if count != 1 else ''}")
    
    def run_demo(self):
        """运行演示"""
        print("🇬🇧 English Tweet Automation Demo")
        print("=" * 50)
        
        # 检查Twitter连接
        if not self.twitter_tool.user:
            print("❌ Twitter connection failed. Check credentials.")
            return
        
        print(f"✅ Connected to Twitter as: @{self.twitter_tool.user.username}")
        
        # 显示每周计划
        print("\n📅 Weekly Content Schedule:")
        schedule = self.get_weekly_schedule()
        for day, info in schedule.items():
            print(f"   {day}: {info['theme']} ({info['tweet_count']} tweets)")
            print(f"      Example: {info['example'][:60]}...")
        
        # 生成今日推文
        print("\n🎯 Today's Recommended Tweet:")
        today_tweet = self.generate_tweet_for_today()
        print(today_tweet)
        print(f"   Length: {len(today_tweet)}/280 characters")
        
        # 显示统计
        self.show_stats()
        
        print("\n" + "=" * 50)
        print("🚀 Ready for English tweet automation!")
        print("\nNext steps:")
        print("1. Review today's tweet above")
        print("2. Use send_tweet() to post it")
        print("3. Set up cron scheduling with OpenClaw")
        print("4. Monitor engagement and adjust strategy")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Automated English Tweets for Product Promotion")
    parser.add_argument('--demo', action='store_true', help='Run demonstration')
    parser.add_argument('--send-today', action='store_true', help='Send today\'s recommended tweet')
    parser.add_argument('--generate', type=str, help='Generate tweet for specific day (e.g., Monday)')
    parser.add_argument('--thread', type=str, help='Generate thread about topic')
    parser.add_argument('--thread-count', type=int, default=3, help='Number of tweets in thread')
    parser.add_argument('--schedule', action='store_true', help='Show weekly schedule')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    
    args = parser.parse_args()
    
    # 初始化自动化系统
    automation = EnglishTweetAutomation(
        product_name="OpenClaw AI",
        company_name="OpenClaw"
    )
    
    # 检查Twitter连接
    if not automation.twitter_tool.user:
        print("❌ Twitter connection failed. Please check:")
        print("   1. Environment variables are set")
        print("   2. Twitter API credentials are valid")
        print("   3. API has write permissions")
        return
    
    # 执行命令
    if args.demo:
        automation.run_demo()
    
    elif args.send_today:
        tweet = automation.generate_tweet_for_today()
        print(f"📝 Today's tweet:\n{tweet}\n")
        
        confirm = input("Send this tweet? (yes/no): ").lower()
        if confirm in ['yes', 'y']:
            tweet_id = automation.send_tweet(tweet)
            if tweet_id:
                print(f"✅ Tweet sent! ID: {tweet_id}")
        else:
            print("Tweet not sent.")
    
    elif args.generate:
        # 临时设置日期来生成特定日期的推文
        print(f"📝 Generating tweet for {args.generate}:")
        
        # 简单映射
        day_map = {
            'monday': 'Monday', 'tuesday': 'Tuesday', 'wednesday': 'Wednesday',
            'thursday': 'Thursday', 'friday': 'Friday', 'saturday': 'Saturday', 'sunday': 'Sunday'
        }
        
        day = day_map.get(args.generate.lower(), args.generate)
        tweet = automation.generate_tweet_for_today()  # 注意：这实际上生成今日推文
        
        print(tweet)
        print(f"\nLength: {len(tweet)}/280 characters")
    
    elif args.thread:
        thread = automation.generate_thread_for_topic(args.thread, args.thread_count)
        print(f"🧵 Thread about '{args.thread}':\n")
        
        for i, tweet in enumerate(thread, 1):
            print(f"Tweet {i}:")
            print(tweet)
            print(f"Length: {len(tweet)}/280 characters")
            print()
    
    elif args.schedule:
        print("📅 Weekly Content Schedule:")
        schedule = automation.get_weekly_schedule()
        for day, info in schedule.items():
            print(f"\n{day}:")
            print(f"  Theme: {info['theme']}")
            print(f"  Tweets: {info['tweet_count']} at {', '.join(info['times'])}")
            print(f"  Example: {info['example']}")
    
    elif args.stats:
        automation.show_stats()
    
    else:
        # 默认运行演示
        automation.run_demo()

if __name__ == "__main__":
    main()