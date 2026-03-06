#!/usr/bin/env python3
"""
互动增强功能
优化推文互动性，增加回复、引用、点赞等
"""

import sys
sys.path.insert(0, '.')

from twitter_tool import TwitterTool
from english_tweet_generator import EnglishTweetGenerator
import time
from datetime import datetime, timedelta
import random
import json
import os

class EngagementEnhancer:
    """互动增强器"""
    
    def __init__(self):
        self.twitter = TwitterTool()
        self.generator = EnglishTweetGenerator(
            product_name="PostAlert.ai",
            company_name="PostAlert"
        )
        
        self.engagement_file = "engagement_stats.json"
        self.stats = self._load_stats()
        
        # 互动策略
        self.strategies = self._define_strategies()
    
    def _load_stats(self):
        """加载互动统计"""
        if os.path.exists(self.engagement_file):
            try:
                with open(self.engagement_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # 默认统计
        return {
            "total_engagements": 0,
            "likes_given": 0,
            "retweets_given": 0,
            "replies_sent": 0,
            "quotes_sent": 0,
            "last_engagement": None,
            "engagement_by_hour": {},
            "best_performing_tweets": []
        }
    
    def _save_stats(self):
        """保存互动统计"""
        with open(self.engagement_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def _define_strategies(self):
        """定义互动策略"""
        return {
            "reply_to_trending": {
                "name": "回复热门推文",
                "description": "在热门推文下回复，增加曝光",
                "search_queries": [
                    "content monitoring",
                    "social media analytics",
                    "AI marketing",
                    "trend detection",
                    "competitive intelligence"
                ],
                "reply_templates": [
                    "Great insight! At PostAlert.ai, we help businesses {related_topic} with AI-powered monitoring.",
                    "Interesting perspective! Our platform takes this further by {value_add}.",
                    "This is exactly why we built PostAlert.ai - to {solve_problem} for marketers.",
                    "Spot on! We've seen similar trends in our data. Key takeaway: {insight}.",
                    "Adding to this: {additional_insight} This is what drives our product development."
                ]
            },
            "quote_tweet_insights": {
                "name": "引用推文分享见解",
                "description": "引用相关推文并添加专业见解",
                "quote_templates": [
                    "Building on this excellent point about {topic}:\n\n{insight}\n\nAt PostAlert.ai, we {solution}.",
                    "This highlights a key challenge in {industry}:\n\n{analysis}\n\nOur approach: {approach}",
                    "Important discussion about {topic}. My take:\n\n{perspective}\n\nLearn more: https://postalert.ai",
                    "Great thread! Summarizing key points about {topic}:\n\n1. {point1}\n2. {point2}\n3. {point3}\n\n{conclusion}"
                ]
            },
            "engage_with_followers": {
                "name": "与粉丝互动",
                "description": "回复粉丝的推文和评论",
                "engagement_types": [
                    "thank_you",
                    "answer_question",
                    "share_resource",
                    "ask_follow_up"
                ]
            },
            "participate_in_threads": {
                "name": "参与相关话题线程",
                "description": "在相关话题的线程中添加有价值的内容",
                "thread_topics": [
                    "AI in marketing",
                    "Social media trends",
                    "Content strategy",
                    "Data analytics",
                    "Digital transformation"
                ]
            }
        }
    
    def search_relevant_tweets(self, query: str, max_results: int = 10):
        """搜索相关推文"""
        print(f"🔍 Searching for tweets about: {query}")
        
        tweets = self.twitter.search_tweets(query, max_results)
        
        if tweets:
            print(f"✅ Found {len(tweets)} relevant tweets")
            
            # 按互动数排序
            sorted_tweets = sorted(tweets, 
                key=lambda x: x['metrics'].get('like_count', 0) + 
                            x['metrics'].get('retweet_count', 0), 
                reverse=True)
            
            return sorted_tweets
        else:
            print("❌ No relevant tweets found")
            return []
    
    def generate_insightful_reply(self, original_tweet: dict, strategy: str = "reply_to_trending") -> str:
        """生成有洞察力的回复"""
        strategy_config = self.strategies.get(strategy, self.strategies["reply_to_trending"])
        
        # 分析原推文内容
        tweet_text = original_tweet.get('text', '')
        tweet_author = original_tweet.get('author_id', '')
        
        # 提取关键词
        keywords = self._extract_keywords(tweet_text)
        
        # 选择回复模板
        template = random.choice(strategy_config["reply_templates"])
        
        # 填充模板
        if "{related_topic}" in template:
            related = random.choice(["monitor trends", "analyze performance", "track competitors", "optimize content"])
            reply = template.replace("{related_topic}", related)
        elif "{value_add}" in template:
            value = random.choice([
                "providing real-time alerts",
                "offering predictive analytics",
                "delivering actionable insights",
                "automating competitive analysis"
            ])
            reply = template.replace("{value_add}", value)
        elif "{solve_problem}" in template:
            problem = random.choice([
                "automate trend detection",
                "simplify content monitoring",
                "enhance competitive intelligence",
                "streamline social listening"
            ])
            reply = template.replace("{solve_problem}", problem)
        elif "{insight}" in template:
            insight = random.choice([
                "proactive monitoring beats reactive response",
                "data-driven decisions outperform gut feelings",
                "automation frees up time for creative strategy",
                "real-time insights enable faster adaptation"
            ])
            reply = template.replace("{insight}", insight)
        elif "{additional_insight}" in template:
            additional = random.choice([
                "The key is combining AI with human expertise",
                "Success comes from consistent monitoring and adaptation",
                "Tools should augment, not replace, human judgment",
                "The best strategies are data-informed, not data-driven"
            ])
            reply = template.replace("{additional_insight}", additional)
        else:
            reply = template
        
        # 添加礼貌性结尾
        if not reply.endswith((".", "!", "?")):
            reply += "."
        
        # 确保长度合适
        if len(reply) > 280:
            reply = reply[:277] + "..."
        
        return reply
    
    def reply_to_tweet(self, tweet_id: str, reply_text: str) -> bool:
        """回复推文"""
        print(f"💬 Replying to tweet {tweet_id}...")
        print(f"   Reply: {reply_text[:80]}...")
        
        reply_id = self.twitter.send_tweet(reply_text, tweet_id)
        
        if reply_id:
            # 更新统计
            self.stats["total_engagements"] += 1
            self.stats["replies_sent"] += 1
            self.stats["last_engagement"] = datetime.now().isoformat()
            
            hour = datetime.now().hour
            hour_key = f"hour_{hour}"
            if hour_key not in self.stats["engagement_by_hour"]:
                self.stats["engagement_by_hour"][hour_key] = 0
            self.stats["engagement_by_hour"][hour_key] += 1
            
            self._save_stats()
            
            print(f"✅ Reply sent! ID: {reply_id}")
            return True
        else:
            print("❌ Failed to send reply")
            return False
    
    def like_relevant_tweet(self, tweet_id: str) -> bool:
        """点赞相关推文"""
        print(f"👍 Liking tweet {tweet_id}...")
        
        success = self.twitter.like_tweet(tweet_id)
        
        if success:
            self.stats["total_engagements"] += 1
            self.stats["likes_given"] += 1
            self._save_stats()
            
            print(f"✅ Liked tweet {tweet_id}")
            return True
        else:
            print(f"❌ Failed to like tweet {tweet_id}")
            return False
    
    def retweet_with_comment(self, tweet_id: str, comment: str = None) -> bool:
        """带评论转发"""
        if comment:
            print(f"🔁 Quote retweeting {tweet_id} with comment...")
            print(f"   Comment: {comment[:80]}...")
            
            # 引用推文
            quote_tweet = f"{comment}\n\n(Quoting @user)"
            quote_id = self.twitter.send_tweet(quote_tweet)  # 注意：需要实现引用功能
            
            if quote_id:
                self.stats["total_engagements"] += 1
                self.stats["quotes_sent"] += 1
                self._save_stats()
                
                print(f"✅ Quote tweet sent! ID: {quote_id}")
                return True
            else:
                print("❌ Failed to send quote tweet")
                return False
        else:
            print(f"🔁 Retweeting {tweet_id}...")
            
            success = self.twitter.retweet(tweet_id)
            
            if success:
                self.stats["total_engagements"] += 1
                self.stats["retweets_given"] += 1
                self._save_stats()
                
                print(f"✅ Retweeted {tweet_id}")
                return True
            else:
                print(f"❌ Failed to retweet {tweet_id}")
                return False
    
    def engage_with_trending_topic(self, topic: str = None):
        """与热门话题互动"""
        if not topic:
            # 随机选择话题
            topics = [
                "AI in digital marketing",
                "Social media analytics",
                "Content strategy trends",
                "Competitive intelligence"
            ]
            topic = random.choice(topics)
        
        print(f"🎯 Engaging with trending topic: {topic}")
        
        # 搜索相关推文
        tweets = self.search_relevant_tweets(topic, max_results=5)
        
        if not tweets:
            print("⏭️ No tweets found for engagement")
            return
        
        # 选择最佳推文（互动数最高）
        best_tweet = tweets[0]
        tweet_id = best_tweet['id']
        tweet_text = best_tweet['text'][:100] + "..." if len(best_tweet['text']) > 100 else best_tweet['text']
        
        print(f"📝 Selected tweet: {tweet_text}")
        print(f"   Likes: {best_tweet['metrics'].get('like_count', 0)}, RTs: {best_tweet['metrics'].get('retweet_count', 0)}")
        
        # 决定互动类型
        engagement_type = random.choice(["reply", "like", "retweet"])
        
        if engagement_type == "reply":
            reply_text = self.generate_insightful_reply(best_tweet)
            self.reply_to_tweet(tweet_id, reply_text)
        
        elif engagement_type == "like":
            self.like_relevant_tweet(tweet_id)
        
        elif engagement_type == "retweet":
            # 30%概率带评论转发
            if random.random() < 0.3:
                comment = self.generate_insightful_reply(best_tweet, "quote_tweet_insights")
                self.retweet_with_comment(tweet_id, comment)
            else:
                self.retweet_with_comment(tweet_id)
        
        # 短暂延迟
        time.sleep(2)
    
    def run_engagement_session(self, duration_minutes: int = 15, engagements_per_session: int = 3):
        """运行互动会话"""
        print(f"🤝 Starting engagement session ({duration_minutes} minutes, max {engagements_per_session} engagements)")
        print("-" * 50)
        
        start_time = datetime.now()
        engagements_done = 0
        
        try:
            while (datetime.now() - start_time).seconds < duration_minutes * 60:
                if engagements_done >= engagements_per_session:
                    print(f"✅ Reached engagement limit ({engagements_per_session})")
                    break
                
                # 选择互动策略
                strategy = random.choice(list(self.strategies.keys()))
                strategy_name = self.strategies[strategy]["name"]
                
                print(f"\n🎯 Strategy: {strategy_name}")
                
                if strategy == "reply_to_trending":
                    query = random.choice(self.strategies[strategy]["search_queries"])
                    self.engage_with_trending_topic(query)
                    engagements_done += 1
                
                elif strategy == "engage_with_followers":
                    # 这里可以添加与粉丝互动的逻辑
                    print("⏭️ Follower engagement strategy (to be implemented)")
                    time.sleep(5)
                
                else:
                    # 默认使用话题互动
                    self.engage_with_trending_topic()
                    engagements_done += 1
                
                # 随机延迟（1-3分钟）
                delay = random.randint(60, 180)
                print(f"⏳ Next engagement in {delay//60} minutes {delay%60} seconds...")
                time.sleep(delay)
        
        except KeyboardInterrupt:
            print("\n🛑 Engagement session interrupted")
        
        print(f"\n✅ Engagement session complete")
        print(f"   Engagements performed: {engagements_done}")
        print(f"   Duration: {(datetime.now() - start_time).seconds//60} minutes")
    
    def _extract_keywords(self, text: str) -> list:
        """提取关键词（简化版）"""
        # 常见停用词
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        
        # 简单分词和过滤
        words = text.lower().split()
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        
        return keywords[:5]  # 返回前5个关键词
    
    def show_stats(self):
        """显示互动统计"""
        print("\n📊 Engagement Statistics:")
        print(f"   Total engagements: {self.stats['total_engagements']}")
        print(f"   Likes given: {self.stats['likes_given']}")
        print(f"   Retweets given: {self.stats['retweets_given']}")
        print(f"   Replies sent: {self.stats['replies_sent']}")
        print(f"   Quote tweets: {self.stats['quotes_sent']}")
        
        if self.stats['last_engagement']:
            last_time = datetime.fromisoformat(self.stats['last_engagement'])
            print(f"   Last engagement: {last_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self.stats['engagement_by_hour']:
            print(f"   Engagements by hour (last 24h):")
            for hour in range(24):
                hour_key = f"hour_{hour}"
                count = self.stats['engagement_by_hour'].get(hour_key, 0)
                if count > 0:
                    print(f"     {hour:02d}:00 - {count} engagement{'s' if count != 1 else ''}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Engagement Enhancer for PostAlert.ai")
    parser.add_argument('--session', action='store_true', help='Run engagement session')
    parser.add_argument('--duration', type=int, default=15, help='Session duration in minutes')
    parser.add_argument('--engagements', type=int, default=3, help='Max engagements per session')
    parser.add_argument('--engage-topic', type=str, help='Engage with specific topic')
    parser.add_argument('--stats', action='store_true', help='Show engagement statistics')
    parser.add_argument('--test-reply', action='store_true', help='Test reply generation')
    parser.add_argument('--search', type=str, help='Search for tweets on topic')
    
    args = parser.parse_args()
    
    # 初始化
    enhancer = EngagementEnhancer()
    
    if not enhancer.twitter.user:
        print("❌ Twitter connection failed. Check credentials.")
        return
    
    print(f"✅ Connected to Twitter: @{enhancer.twitter.user.username}")
    
    if args.session:
        enhancer.run_engagement_session(args.duration, args.engagements)
    
    elif args.engage_topic:
        enhancer.engage_with_trending_topic(args.engage_topic)
    
    elif args.stats:
        enhancer.show_stats()
    
    elif args.test_reply:
        print("🧪 Testing reply generation:")
        
        # 模拟推文
        test_tweet = {
            "text": "AI-powered content monitoring is revolutionizing how brands track their online presence and competitor activities.",
            "author_id": "test_user",
            "metrics": {"like_count": 50, "retweet_count": 20}
        }
        
        for i in range(3):
            reply = enhancer.generate_insightful_reply(test_tweet)
            print(f"\nTest reply {i+1}:")
            print(reply)
            print(f"Length: {len(reply)}/280 characters")
    
    elif args.search:
        tweets = enhancer.search_relevant_tweets(args.search, 5)
        if tweets:
            print(f"\n📊 Search results for '{args.search}':")
            for i, tweet in enumerate(tweets, 1):
                print(f"\n{i}. {tweet['text'][:100]}...")
                print(f"   ID: {tweet['id']}")
                print(f"   Likes: {tweet['metrics'].get('like_count', 0)}, RTs: {tweet['metrics'].get('retweet_count', 0)}")
    
    else:
        # 显示帮助
        print("Engagement Enhancer for PostAlert.ai")
        print("\nUsage:")
        print("  python engagement_enhancer.py --session          # 运行互动会话")
        print("  python engagement_enhancer.py --engage-topic TOPIC  # 与特定话题互动")
        print("  python engagement_enhancer.py --stats            # 显示互动统计")
        print("  python engagement_enhancer.py --test-reply       # 测试回复生成")
        print("  python engagement_enhancer.py --search QUERY     # 搜索相关推文")
        print("\nOptions:")
        print("  --duration MINUTES   会话时长（默认15）")
        print("  --engagements COUNT  每次会话最大互动数（默认3）")

if __name__ == "__main__":
    main()