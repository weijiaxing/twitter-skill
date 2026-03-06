#!/usr/bin/env python3
"""
PostAlert.ai 内容系列优化
创建系统化的英文推广内容系列
"""

import sys
sys.path.insert(0, '.')

from english_tweet_generator import EnglishTweetGenerator
from twitter_tool import TwitterTool
import time
from datetime import datetime

class PostAlertContentSeries:
    """PostAlert.ai 内容系列"""
    
    def __init__(self):
        self.generator = EnglishTweetGenerator(
            product_name="PostAlert.ai",
            company_name="PostAlert"
        )
        self.twitter = TwitterTool()
        
        # 内容系列定义
        self.series = self._define_content_series()
        
    def _define_content_series(self):
        """定义内容系列"""
        return {
            "core_features": {
                "name": "核心功能系列",
                "description": "详细介绍PostAlert.ai的核心功能",
                "tweets": [
                    {
                        "title": "AI-Powered Content Monitoring",
                        "key_points": [
                            "Real-time trend detection",
                            "Cross-platform monitoring",
                            "Predictive analytics"
                        ],
                        "benefit": "Stay ahead of viral content"
                    },
                    {
                        "title": "Competitive Intelligence",
                        "key_points": [
                            "Monitor competitor activities",
                            "Benchmark performance",
                            "Identify opportunities"
                        ],
                        "benefit": "Make data-driven decisions"
                    },
                    {
                        "title": "Custom Alert System",
                        "key_points": [
                            "Keyword-based alerts",
                            "Sentiment analysis",
                            "Priority notifications"
                        ],
                        "benefit": "Never miss important updates"
                    },
                    {
                        "title": "Analytics Dashboard",
                        "key_points": [
                            "Performance metrics",
                            "Engagement analytics",
                            "ROI tracking"
                        ],
                        "benefit": "Measure and optimize results"
                    }
                ]
            },
            "use_cases": {
                "name": "使用场景系列",
                "description": "展示不同行业的使用案例",
                "tweets": [
                    {
                        "industry": "Marketing Agencies",
                        "challenge": "Managing multiple client campaigns",
                        "solution": "Centralized monitoring dashboard",
                        "result": "40% time savings"
                    },
                    {
                        "industry": "E-commerce Brands",
                        "challenge": "Tracking product mentions and reviews",
                        "solution": "Real-time sentiment analysis",
                        "result": "25% increase in customer satisfaction"
                    },
                    {
                        "industry": "Media Companies",
                        "challenge": "Identifying trending topics",
                        "solution": "AI-powered trend prediction",
                        "result": "30% more viral content"
                    },
                    {
                        "industry": "Startups",
                        "challenge": "Limited marketing budget",
                        "solution": "Cost-effective competitive intelligence",
                        "result": "2x faster market entry"
                    }
                ]
            },
            "educational": {
                "name": "教育内容系列",
                "description": "分享行业知识和最佳实践",
                "tweets": [
                    {
                        "topic": "Content Strategy",
                        "tip": "How to identify viral content patterns",
                        "insight": "Timing and relevance are key factors",
                        "action": "Use data to inform your strategy"
                    },
                    {
                        "topic": "Social Listening",
                        "tip": "Monitor beyond direct mentions",
                        "insight": "Industry conversations reveal opportunities",
                        "action": "Engage with relevant discussions"
                    },
                    {
                        "topic": "Competitive Analysis",
                        "tip": "Track competitor content performance",
                        "insight": "Learn from both successes and failures",
                        "action": "Adapt winning strategies"
                    },
                    {
                        "topic": "ROI Measurement",
                        "tip": "Link social metrics to business outcomes",
                        "insight": "Quality engagement beats quantity",
                        "action": "Focus on conversion-driving content"
                    }
                ]
            },
            "success_stories": {
                "name": "成功案例系列",
                "description": "展示客户成功故事",
                "tweets": [
                    {
                        "client": "TechGrowth Inc.",
                        "problem": "Missed important industry trends",
                        "solution": "PostAlert.ai monitoring system",
                        "result": "Identified 3 key trends before competitors"
                    },
                    {
                        "client": "BrandBoost Agency",
                        "problem": "Inefficient client reporting",
                        "solution": "Automated analytics dashboard",
                        "result": "Reduced reporting time by 60%"
                    },
                    {
                        "client": "EcomSuccess Store",
                        "problem": "Slow response to customer feedback",
                        "solution": "Real-time alert system",
                        "result": "Improved response time by 75%"
                    },
                    {
                        "client": "MediaMasters Network",
                        "problem": "Content hit-or-miss performance",
                        "solution": "Predictive trend analysis",
                        "result": "Increased engagement by 45%"
                    }
                ]
            }
        }
    
    def generate_feature_tweet(self, feature_index: int = 0) -> str:
        """生成功能介绍推文"""
        series = self.series["core_features"]
        if feature_index >= len(series["tweets"]):
            feature_index = 0
        
        feature = series["tweets"][feature_index]
        
        # 构建推文内容
        tweet = f"🚀 {feature['title']}\n\n"
        tweet += f"Key capabilities:\n"
        for point in feature["key_points"]:
            tweet += f"• {point}\n"
        tweet += f"\nBenefit: {feature['benefit']}\n\n"
        tweet += f"Learn more: https://postalert.ai/features\n\n"
        tweet += f"#AI #ContentMonitoring #MarketingTech"
        
        return self._validate_length(tweet)
    
    def generate_usecase_tweet(self, usecase_index: int = 0) -> str:
        """生成使用案例推文"""
        series = self.series["use_cases"]
        if usecase_index >= len(series["tweets"]):
            usecase_index = 0
        
        case = series["tweets"][usecase_index]
        
        tweet = f"🎯 {case['industry']} Case Study\n\n"
        tweet += f"Challenge: {case['challenge']}\n"
        tweet += f"Solution: {case['solution']}\n"
        tweet += f"Result: {case['result']}\n\n"
        tweet += f"How PostAlert.ai helps: https://postalert.ai/cases\n\n"
        tweet += f"#{case['industry'].replace(' ', '')} #CaseStudy #BusinessResults"
        
        return self._validate_length(tweet)
    
    def generate_educational_tweet(self, edu_index: int = 0) -> str:
        """生成教育内容推文"""
        series = self.series["educational"]
        if edu_index >= len(series["tweets"]):
            edu_index = 0
        
        content = series["tweets"][edu_index]
        
        tweet = f"💡 {content['topic']} Tip\n\n"
        tweet += f"{content['tip']}\n\n"
        tweet += f"Insight: {content['insight']}\n"
        tweet += f"Action: {content['action']}\n\n"
        tweet += f"#ContentStrategy #SocialMediaTips #DigitalMarketing"
        
        return self._validate_length(tweet)
    
    def generate_success_tweet(self, success_index: int = 0) -> str:
        """生成成功案例推文"""
        series = self.series["success_stories"]
        if success_index >= len(series["tweets"]):
            success_index = 0
        
        story = series["tweets"][success_index]
        
        tweet = f"🏆 Success Story: {story['client']}\n\n"
        tweet += f"Problem: {story['problem']}\n"
        tweet += f"Solution: {story['solution']}\n"
        tweet += f"Result: {story['result']}\n\n"
        tweet += f"Read full story: https://postalert.ai/success\n\n"
        tweet += f"#CustomerSuccess #Testimonial #BusinessGrowth"
        
        return self._validate_length(tweet)
    
    def generate_daily_series_tweet(self, hour_of_day: int = None) -> str:
        """根据时间生成每日系列推文"""
        if hour_of_day is None:
            hour_of_day = datetime.now().hour
        
        # 根据小时选择内容类型
        if 9 <= hour_of_day < 12:  # 上午：功能介绍
            return self.generate_feature_tweet(hour_of_day % 4)
        elif 12 <= hour_of_day < 15:  # 中午：使用案例
            return self.generate_usecase_tweet((hour_of_day - 12) % 4)
        elif 15 <= hour_of_day < 18:  # 下午：教育内容
            return self.generate_educational_tweet((hour_of_day - 15) % 4)
        else:  # 晚上：成功案例
            return self.generate_success_tweet(hour_of_day % 4)
    
    def generate_thread(self, series_name: str, thread_length: int = 3) -> list:
        """生成推文线程"""
        if series_name not in self.series:
            series_name = "core_features"
        
        series = self.series[series_name]
        tweets = []
        
        # 第一条：介绍
        intro = f"🧵 Thread: {series['name']}\n\n"
        intro += f"{series['description']}\n\n"
        intro += f"Following {thread_length} key insights 👇\n\n"
        intro += f"#Thread #{series_name.replace('_', '')} #PostAlertAI"
        tweets.append(self._validate_length(intro))
        
        # 后续推文
        for i in range(1, min(thread_length + 1, len(series["tweets"]) + 1)):
            if series_name == "core_features":
                tweet = self.generate_feature_tweet(i-1)
            elif series_name == "use_cases":
                tweet = self.generate_usecase_tweet(i-1)
            elif series_name == "educational":
                tweet = self.generate_educational_tweet(i-1)
            else:  # success_stories
                tweet = self.generate_success_tweet(i-1)
            
            # 添加线程标记
            tweet = tweet.replace("\n\n", f"\n\n({i}/{thread_length}) ", 1)
            tweets.append(self._validate_length(tweet))
        
        return tweets
    
    def send_tweet(self, content: str) -> str:
        """发送推文"""
        if not self.twitter.user:
            print("❌ Not connected to Twitter")
            return None
        
        return self.twitter.send_tweet(content)
    
    def send_thread(self, tweets: list) -> list:
        """发送推文线程"""
        tweet_ids = []
        previous_id = None
        
        for i, tweet in enumerate(tweets, 1):
            print(f"📤 Sending thread tweet {i}/{len(tweets)}...")
            
            tweet_id = self.send_tweet(tweet)
            if tweet_id:
                tweet_ids.append(tweet_id)
                previous_id = tweet_id
                
                # 线程间延迟
                if i < len(tweets):
                    time.sleep(2)
            else:
                print(f"❌ Failed to send tweet {i}")
                break
        
        return tweet_ids
    
    def _validate_length(self, tweet: str, max_len: int = 280) -> str:
        """验证推文长度"""
        if len(tweet) > max_len:
            # 简单截断
            tweet = tweet[:max_len-3] + "..."
        return tweet
    
    def preview_series(self):
        """预览内容系列"""
        print("📚 PostAlert.ai Content Series Preview")
        print("=" * 50)
        
        for series_name, series_info in self.series.items():
            print(f"\n{series_info['name']}:")
            print(f"  {series_info['description']}")
            print(f"  Contains {len(series_info['tweets'])} tweets")
            
            # 预览第一条
            if series_info['tweets']:
                first = series_info['tweets'][0]
                if 'title' in first:
                    print(f"  Sample: {first['title'][:40]}...")
                elif 'industry' in first:
                    print(f"  Sample: {first['industry'][:40]}...")
                elif 'topic' in first:
                    print(f"  Sample: {first['topic'][:40]}...")
                elif 'client' in first:
                    print(f"  Sample: {first['client'][:40]}...")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="PostAlert.ai Content Series")
    parser.add_argument('--preview', action='store_true', help='Preview content series')
    parser.add_argument('--feature', type=int, help='Send feature tweet (0-3)')
    parser.add_argument('--usecase', type=int, help='Send use case tweet (0-3)')
    parser.add_argument('--educational', type=int, help='Send educational tweet (0-3)')
    parser.add_argument('--success', type=int, help='Send success story tweet (0-3)')
    parser.add_argument('--daily', type=int, help='Send daily series tweet for hour (0-23)')
    parser.add_argument('--thread', type=str, choices=['core_features', 'use_cases', 'educational', 'success_stories'], help='Generate and send thread')
    parser.add_argument('--thread-length', type=int, default=3, help='Number of tweets in thread')
    
    args = parser.parse_args()
    
    # 初始化
    series = PostAlertContentSeries()
    
    if not series.twitter.user:
        print("❌ Twitter connection failed. Check credentials.")
        return
    
    print(f"✅ Connected to Twitter: @{series.twitter.user.username}")
    
    if args.preview:
        series.preview_series()
    
    elif args.feature is not None:
        tweet = series.generate_feature_tweet(args.feature)
        print(f"📝 Feature Tweet:\n{tweet}\n")
        
        confirm = input("Send this tweet? (yes/no): ").lower()
        if confirm in ['yes', 'y']:
            tweet_id = series.send_tweet(tweet)
            if tweet_id:
                print(f"✅ Tweet sent! ID: {tweet_id}")
    
    elif args.usecase is not None:
        tweet = series.generate_usecase_tweet(args.usecase)
        print(f"📝 Use Case Tweet:\n{tweet}\n")
        
        confirm = input("Send this tweet? (yes/no): ").lower()
        if confirm in ['yes', 'y']:
            tweet_id = series.send_tweet(tweet)
            if tweet_id:
                print(f"✅ Tweet sent! ID: {tweet_id}")
    
    elif args.educational is not None:
        tweet = series.generate_educational_tweet(args.educational)
        print(f"📝 Educational Tweet:\n{tweet}\n")
        
        confirm = input("Send this tweet? (yes/no): ").lower()
        if confirm in ['yes', 'y']:
            tweet_id = series.send_tweet(tweet)
            if tweet_id:
                print(f"✅ Tweet sent! ID: {tweet_id}")
    
    elif args.success is not None:
        tweet = series.generate_success_tweet(args.success)
        print(f"📝 Success Story Tweet:\n{tweet}\n")
        
        confirm = input("Send this tweet? (yes/no): ").lower()
        if confirm in ['yes', 'y']:
            tweet_id = series.send_tweet(tweet)
            if tweet_id:
                print(f"✅ Tweet sent! ID: {tweet_id}")
    
    elif args.daily is not None:
        tweet = series.generate_daily_series_tweet(args.daily)
        print(f"📝 Daily Tweet (hour {args.daily}):\n{tweet}\n")
        
        confirm = input("Send this tweet? (yes/no): ").lower()
        if confirm in ['yes', 'y']:
            tweet_id = series.send_tweet(tweet)
            if tweet_id:
                print(f"✅ Tweet sent! ID: {tweet_id}")
    
    elif args.thread:
        print(f"🧵 Generating {args.thread} thread ({args.thread_length} tweets)...")
        thread = series.generate_thread(args.thread, args.thread_length)
        
        print("\nThread Preview:")
        for i, tweet in enumerate(thread, 1):
            print(f"\nTweet {i}:")
            print(tweet[:100] + "..." if len(tweet) > 100 else tweet)
        
        confirm = input(f"\nSend this {len(thread)}-tweet thread? (yes/no): ").lower()
        if confirm in ['yes', 'y']:
            tweet_ids = series.send_thread(thread)
            if tweet_ids:
                print(f"✅ Thread sent! {len(tweet_ids)} tweets posted")
                print(f"   First tweet: https://twitter.com/{series.twitter.user.username}/status/{tweet_ids[0]}")
    
    else:
        # 默认：预览
        series.preview_series()
        print("\nUsage examples:")
        print("  python postalert_content_series.py --preview")
        print("  python postalert_content_series.py --feature 0")
        print("  python postalert_content_series.py --thread core_features --thread-length 3")

if __name__ == "__main__":
    main()