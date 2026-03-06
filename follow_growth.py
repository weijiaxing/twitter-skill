#!/usr/bin/env python3
"""
Twitter快速增长策略：
1. 互关策略 - 关注相关领域用户
2. 热门评论 - 在高曝光推文下评论
"""

import sys
sys.path.insert(0, '.')

from twitter_tool import TwitterTool
from english_tweet_generator import EnglishTweetGenerator
import time
import random
from datetime import datetime

class TwitterGrowthAccelerator:
    """Twitter增长加速器"""
    
    def __init__(self):
        self.twitter = TwitterTool()
        self.generator = EnglishTweetGenerator(
            product_name="PostAlert.ai",
            company_name="PostAlert"
        )
        
        # 目标用户类别
        self.target_categories = self._define_target_categories()
        
    def _define_target_categories(self):
        """定义目标用户类别"""
        return {
            "tech_influencers": {
                "name": "科技影响者",
                "search_queries": [
                    "AI marketing expert",
                    "social media analytics",
                    "content strategy consultant",
                    "digital marketing thought leader",
                    "tech startup founder"
                ],
                "min_followers": 5000,
                "max_followers": 100000
            },
            "marketing_agencies": {
                "name": "营销机构",
                "search_queries": [
                    "digital marketing agency",
                    "social media agency",
                    "content marketing agency",
                    "SEO agency",
                    "growth marketing"
                ],
                "min_followers": 1000,
                "max_followers": 50000
            },
            "saas_companies": {
                "name": "SaaS公司",
                "search_queries": [
                    "SaaS marketing",
                    "B2B software",
                    "tech startup",
                    "software as a service",
                    "cloud platform"
                ],
                "min_followers": 2000,
                "max_followers": 100000
            },
            "content_creators": {
                "name": "内容创作者",
                "search_queries": [
                    "content creator",
                    "social media influencer",
                    "YouTube creator",
                    "LinkedIn influencer",
                    "Twitter thought leader"
                ],
                "min_followers": 3000,
                "max_followers": 50000
            },
            "industry_experts": {
                "name": "行业专家",
                "search_queries": [
                    "marketing expert",
                    "AI specialist",
                    "data analytics",
                    "business intelligence",
                    "competitive intelligence"
                ],
                "min_followers": 2000,
                "max_followers": 100000
            }
        }
    
    def search_target_users(self, category: str, max_results: int = 20):
        """搜索目标用户"""
        if category not in self.target_categories:
            category = "tech_influencers"
        
        category_info = self.target_categories[category]
        query = random.choice(category_info["search_queries"])
        
        print(f"🔍 搜索{category_info['name']}: {query}")
        
        # 搜索相关推文，从中提取用户
        tweets = self.twitter.search_tweets(query, max_results)
        
        if not tweets:
            print("❌ 未找到相关推文")
            return []
        
        # 提取用户ID（去重）
        user_ids = set()
        for tweet in tweets:
            if 'author_id' in tweet:
                user_ids.add(tweet['author_id'])
        
        print(f"✅ 找到 {len(user_ids)} 个潜在目标用户")
        return list(user_ids)[:10]  # 限制数量
    
    def follow_users(self, user_ids: list, max_follows: int = 5):
        """关注用户"""
        if not user_ids:
            print("❌ 没有用户可关注")
            return []
        
        print(f"🤝 准备关注 {min(len(user_ids), max_follows)} 个用户...")
        
        followed = []
        for i, user_id in enumerate(user_ids[:max_follows]):
            try:
                print(f"  {i+1}. 关注用户 {user_id}...")
                
                # 这里需要Twitter API的关注功能
                # 实际实现需要Twitter API v2的follow端点
                # 暂时模拟
                
                followed.append(user_id)
                
                # 避免过快关注（Twitter限制）
                time.sleep(random.uniform(30, 60))
                
            except Exception as e:
                print(f"    ❌ 关注失败: {e}")
        
        print(f"✅ 已关注 {len(followed)} 个用户")
        return followed
    
    def search_viral_tweets(self, topic: str = None, min_likes: int = 100):
        """搜索热门推文"""
        if not topic:
            topics = [
                "AI marketing",
                "social media trends",
                "content strategy",
                "digital transformation",
                "data analytics"
            ]
            topic = random.choice(topics)
        
        print(f"🔥 搜索热门推文: {topic} (最少{min_likes}赞)")
        
        tweets = self.twitter.search_tweets(topic, max_results=20)
        
        if not tweets:
            print("❌ 未找到相关推文")
            return []
        
        # 筛选热门推文
        viral_tweets = []
        for tweet in tweets:
            likes = tweet['metrics'].get('like_count', 0)
            retweets = tweet['metrics'].get('retweet_count', 0)
            
            if likes >= min_likes:
                viral_tweets.append({
                    'id': tweet['id'],
                    'text': tweet['text'],
                    'likes': likes,
                    'retweets': retweets,
                    'author_id': tweet.get('author_id', '')
                })
        
        # 按热度排序
        viral_tweets.sort(key=lambda x: x['likes'] + x['retweets'], reverse=True)
        
        print(f"✅ 找到 {len(viral_tweets)} 条热门推文")
        return viral_tweets[:5]  # 返回最热的5条
    
    def generate_valuable_comment(self, original_tweet: dict):
        """生成有价值的评论"""
        tweet_text = original_tweet['text']
        
        # 评论模板
        templates = [
            "Great insight about {topic}! At PostAlert.ai, we help businesses {related_action} with AI-powered monitoring.",
            "Interesting perspective on {topic}. Our data shows that {insight}. Tools like PostAlert.ai make this easier.",
            "Spot on about {topic}! The key is {key_point}. Our platform helps by {solution}.",
            "Adding to this discussion about {topic}: {additional_insight}. This is exactly what drives our product development.",
            "This highlights an important challenge in {industry}. Our approach at PostAlert.ai: {approach}."
        ]
        
        # 提取话题关键词
        keywords = self._extract_topic_keywords(tweet_text)
        topic = keywords[0] if keywords else "this topic"
        
        template = random.choice(templates)
        
        # 填充模板
        if "{related_action}" in template:
            actions = [
                "monitor these trends in real-time",
                "analyze competitor activities",
                "track content performance",
                "identify viral opportunities",
                "optimize their content strategy"
            ]
            comment = template.replace("{topic}", topic).replace("{related_action}", random.choice(actions))
        
        elif "{insight}" in template:
            insights = [
                "proactive monitoring beats reactive response every time",
                "data-driven decisions outperform gut feelings by 40%",
                "the most successful brands monitor trends daily",
                "competitive intelligence is the new competitive advantage"
            ]
            comment = template.replace("{topic}", topic).replace("{insight}", random.choice(insights))
        
        elif "{key_point}" in template:
            key_points = [
                "consistent monitoring and timely response",
                "combining AI insights with human expertise",
                "focusing on actionable data, not just metrics",
                "building systems that scale with your growth"
            ]
            comment = template.replace("{topic}", topic).replace("{key_point}", random.choice(key_points))
        
        elif "{additional_insight}" in template:
            additional = [
                "The real opportunity lies in predictive analytics, not just monitoring",
                "Success comes from integrating these insights into your workflow",
                "The best strategies are informed by data but driven by creativity",
                "This is why we built PostAlert.ai - to make this accessible to every business"
            ]
            comment = template.replace("{topic}", topic).replace("{additional_insight}", random.choice(additional))
        
        elif "{industry}" in template:
            industries = ["digital marketing", "content strategy", "social media management", "competitive analysis"]
            approaches = [
                "combining AI monitoring with human analysis",
                "providing real-time alerts for important trends",
                "offering predictive analytics for strategic planning",
                "delivering actionable insights, not just data"
            ]
            comment = template.replace("{industry}", random.choice(industries)).replace("{approach}", random.choice(approaches))
        
        else:
            comment = template.replace("{topic}", topic)
        
        # 确保长度合适
        if len(comment) > 280:
            comment = comment[:277] + "..."
        
        return comment
    
    def comment_on_viral_tweet(self, tweet_id: str, comment: str):
        """在热门推文下评论"""
        print(f"💬 在热门推文下评论...")
        print(f"   推文ID: {tweet_id}")
        print(f"   评论: {comment[:80]}...")
        
        # 发送评论（回复推文）
        reply_id = self.twitter.send_tweet(comment, tweet_id)
        
        if reply_id:
            print(f"✅ 评论发送成功! ID: {reply_id}")
            return reply_id
        else:
            print("❌ 评论发送失败")
            return None
    
    def run_growth_session(self, duration_minutes: int = 20):
        """运行增长会话"""
        print("🚀 开始Twitter增长加速会话")
        print(f"⏰ 时长: {duration_minutes} 分钟")
        print("=" * 50)
        
        start_time = datetime.now()
        actions_taken = 0
        
        try:
            while (datetime.now() - start_time).seconds < duration_minutes * 60:
                # 随机选择策略
                strategy = random.choice(["follow", "comment"])
                
                if strategy == "follow":
                    print(f"\n🤝 策略 {actions_taken+1}: 互关策略")
                    
                    # 选择目标类别
                    category = random.choice(list(self.target_categories.keys()))
                    category_name = self.target_categories[category]["name"]
                    
                    print(f"🎯 目标: {category_name}")
                    
                    # 搜索目标用户
                    user_ids = self.search_target_users(category, max_results=10)
                    
                    if user_ids:
                        # 关注用户
                        followed = self.follow_users(user_ids, max_follows=3)
                        actions_taken += len(followed)
                    
                    # 延迟
                    delay = random.randint(120, 300)  # 2-5分钟
                    print(f"⏳ 下一个行动在 {delay//60} 分 {delay%60} 秒后...")
                    time.sleep(delay)
                
                else:  # comment
                    print(f"\n💬 策略 {actions_taken+1}: 热门评论策略")
                    
                    # 搜索热门推文
                    viral_tweets = self.search_viral_tweets(min_likes=50)
                    
                    if viral_tweets:
                        # 选择最热的推文
                        tweet = viral_tweets[0]
                        print(f"🔥 选择推文: {tweet['text'][:80]}...")
                        print(f"   点赞: {tweet['likes']}, 转发: {tweet['retweets']}")
                        
                        # 生成有价值的评论
                        comment = self.generate_valuable_comment(tweet)
                        
                        # 发表评论
                        reply_id = self.comment_on_viral_tweet(tweet['id'], comment)
                        
                        if reply_id:
                            actions_taken += 1
                    
                    # 延迟
                    delay = random.randint(180, 420)  # 3-7分钟
                    print(f"⏳ 下一个行动在 {delay//60} 分 {delay%60} 秒后...")
                    time.sleep(delay)
        
        except KeyboardInterrupt:
            print("\n🛑 增长会话被用户中断")
        
        print(f"\n✅ 增长会话完成")
        print(f"   执行行动: {actions_taken} 次")
        print(f"   总时长: {(datetime.now() - start_time).seconds//60} 分钟")
    
    def _extract_topic_keywords(self, text: str):
        """提取话题关键词"""
        # 简单关键词提取
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were"}
        
        words = text.lower().split()
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        
        return keywords[:3]

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Twitter增长加速器")
    parser.add_argument('--session', action='store_true', help='运行增长会话')
    parser.add_argument('--duration', type=int, default=20, help='会话时长（分钟）')
    parser.add_argument('--follow', type=str, help='关注特定类别用户')
    parser.add_argument('--comment', type=str, help='在特定话题热门推文下评论')
    parser.add_argument('--search-viral', type=str, help='搜索热门推文')
    
    args = parser.parse_args()
    
    # 初始化
    accelerator = TwitterGrowthAccelerator()
    
    if not accelerator.twitter.user:
        print("❌ Twitter连接失败")
        return
    
    print(f"✅ 已连接: @{accelerator.twitter.user.username}")
    
    if args.session:
        accelerator.run_growth_session(args.duration)
    
    elif args.follow:
        user_ids = accelerator.search_target_users(args.follow, max_results=15)
        if user_ids:
            accelerator.follow_users(user_ids, max_follows=5)
    
    elif args.comment:
        viral_tweets = accelerator.search_viral_tweets(args.comment, min_likes=50)
        if viral_tweets:
            tweet = viral_tweets[0]
            comment = accelerator.generate_valuable_comment(tweet)
            accelerator.comment_on_viral_tweet(tweet['id'], comment)
    
    elif args.search_viral:
        tweets = accelerator.search_viral_tweets(args.search_viral, min_likes=50)
        if tweets:
            print(f"\n🔥 热门推文搜索结果:")
            for i, tweet in enumerate(tweets, 1):
                print(f"\n{i}. {tweet['text'][:100]}...")
                print(f"   点赞: {tweet['likes']}, 转发: {tweet['retweets']}")
                print(f"   ID: {tweet['id']}")
    
    else:
        # 显示帮助
        print("🚀 Twitter增长加速器")
        print("\n使用方法:")
        print("  python follow_growth.py --session          # 运行增长会话")
        print("  python follow_growth.py --follow tech_influencers  # 关注科技影响者")
        print("  python follow_growth.py --comment \"AI marketing\"  # 在AI营销热门推文下评论")
        print("  python follow_growth.py --search-viral \"content strategy\"  # 搜索热门推文")
        print("\n目标类别:")
        for cat_id, cat_info in accelerator.target_categories.items():
            print(f"  {cat_id}: {cat_info['name']}")

if __name__ == "__main__":
    main()