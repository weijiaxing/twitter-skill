#!/usr/bin/env python3
"""
升级版推特内容生成器
支持每30分钟发布，更多样化的病毒式营销内容
"""

import sys
sys.path.insert(0, '.')

from english_tweet_generator import EnglishTweetGenerator
from twitter_tool import TwitterTool
import random
from datetime import datetime
import json

class UpgradedContentGenerator:
    """升级版内容生成器 - 每30分钟发布"""
    
    def __init__(self):
        self.generator = EnglishTweetGenerator(
            product_name="PostAlert.ai",
            company_name="PostAlert"
        )
        self.twitter = TwitterTool()
        
        # 8种内容类型
        self.content_types = self._define_content_types()
        
        # 病毒式营销角度
        self.viral_angles = [
            "FOMO (Fear Of Missing Out)",
            "Social Proof", 
            "Scarcity",
            "Urgency",
            "Curiosity Gap",
            "Emotional Trigger",
            "Controversy",
            "How-To/Educational",
            "Behind The Scenes",
            "User Generated Content"
        ]
        
        # 热门话题标签库
        self.trending_hashtags = [
            "#AI", "#Tech", "#Innovation", "#Startup", "#SaaS",
            "#Marketing", "#DigitalMarketing", "#SocialMedia",
            "#ContentMarketing", "#GrowthHacking", "#Business",
            "#Entrepreneur", "#Productivity", "#Tools",
            "#Crypto", "#Trading", "#FinTech", "#Web3",
            "#RealTime", "#Analytics", "#Data", "#Automation"
        ]
        
    def _define_content_types(self):
        """定义8种内容类型"""
        return {
            "product_feature": {
                "name": "产品功能",
                "count": 6,
                "description": "详细介绍PostAlert.ai的各个功能"
            },
            "use_case": {
                "name": "使用案例", 
                "count": 6,
                "description": "不同行业/角色的使用场景"
            },
            "problem_solution": {
                "name": "问题解决方案",
                "count": 5,
                "description": "针对特定问题的解决方案"
            },
            "comparison": {
                "name": "对比优势",
                "count": 4,
                "description": "与竞品/传统方法的对比"
            },
            "testimonial": {
                "name": "用户证言",
                "count": 5,
                "description": "真实用户反馈和成功故事"
            },
            "educational": {
                "name": "教育内容",
                "count": 6,
                "description": "行业知识、技巧、最佳实践"
            },
            "trend_analysis": {
                "name": "趋势分析",
                "count": 4,
                "description": "行业趋势、数据分析"
            },
            "behind_scenes": {
                "name": "幕后故事",
                "count": 3,
                "description": "团队、开发过程、企业文化"
            }
        }
    
    def generate_product_feature(self, index: int = 0) -> str:
        """生成产品功能推文"""
        features = [
            {
                "title": "🚀 Real-Time Phone Call Alerts",
                "description": "Get instant phone calls when important tweets drop",
                "benefits": ["Never miss alpha", "Beat competitors", "React instantly"],
                "use_case": "Perfect for crypto traders tracking whale accounts"
            },
            {
                "title": "📊 AI-Powered Trend Detection",
                "description": "Our AI identifies viral content before it blows up",
                "benefits": ["Predict trends", "Stay ahead", "Create timely content"],
                "use_case": "Ideal for journalists and content creators"
            },
            {
                "title": "🎯 Custom Keyword Monitoring",
                "description": "Monitor specific keywords, accounts, and topics",
                "benefits": ["Targeted alerts", "Relevant notifications", "No spam"],
                "use_case": "Great for brand managers and PR teams"
            },
            {
                "title": "📈 Performance Analytics",
                "description": "Track engagement, reach, and ROI of monitored content",
                "benefits": ["Data-driven decisions", "Measure impact", "Optimize strategy"],
                "use_case": "Essential for marketing agencies"
            },
            {
                "title": "🤖 Automated Reporting",
                "description": "Get daily/weekly reports delivered automatically",
                "benefits": ["Save time", "Stay informed", "Share insights"],
                "use_case": "Perfect for busy executives"
            },
            {
                "title": "🔒 Privacy-First Design",
                "description": "Your data stays private and secure",
                "benefits": ["GDPR compliant", "No data selling", "Enterprise security"],
                "use_case": "Trusted by Fortune 500 companies"
            }
        ]
        
        if index >= len(features):
            index = 0
        
        feature = features[index]
        
        tweet = f"{feature['title']}\n\n"
        tweet += f"{feature['description']}\n\n"
        tweet += "Key benefits:\n"
        for benefit in feature["benefits"]:
            tweet += f"• {benefit}\n"
        tweet += f"\n{feature['use_case']}\n\n"
        tweet += f"Try free: https://postalert.ai\n\n"
        tweet += self._generate_hashtags(4)
        
        return self._validate_length(tweet)
    
    def generate_use_case(self, index: int = 0) -> str:
        """生成使用案例推文"""
        cases = [
            {
                "user": "Crypto Trader",
                "problem": "Missing whale movements and alpha tweets",
                "solution": "Phone call alerts for key accounts",
                "result": "30% better trade timing"
            },
            {
                "user": "Journalist",
                "problem": "Late to breaking news stories",
                "solution": "Real-time trend detection",
                "result": "First to publish on 5 major stories"
            },
            {
                "user": "Marketing Agency",
                "problem": "Manual social media monitoring",
                "solution": "Automated alerts and reporting",
                "result": "Saved 20 hours/week per client"
            },
            {
                "user": "Startup Founder",
                "problem": "No budget for competitive intelligence",
                "solution": "Affordable monitoring solution",
                "result": "Identified 3 key market opportunities"
            },
            {
                "user": "PR Manager",
                "problem": "Slow response to brand mentions",
                "solution": "Instant notification system",
                "result": "75% faster crisis response"
            },
            {
                "user": "Content Creator",
                "problem": "Creating content that doesn't resonate",
                "solution": "Trend prediction analytics",
                "result": "2x more viral content"
            }
        ]
        
        if index >= len(cases):
            index = 0
        
        case = cases[index]
        
        tweet = f"🎯 How {case['user']}s Use PostAlert.ai\n\n"
        tweet += f"Problem: {case['problem']}\n"
        tweet += f"Solution: {case['solution']}\n"
        tweet += f"Result: {case['result']}\n\n"
        tweet += f"Learn how it can help you: https://postalert.ai/use-cases\n\n"
        tweet += f"#{case['user'].replace(' ', '')} #CaseStudy #SuccessStory"
        
        return self._validate_length(tweet)
    
    def generate_problem_solution(self, index: int = 0) -> str:
        """生成问题解决方案推文"""
        problems = [
            {
                "problem": "You're refreshing Twitter all day",
                "pain": "Wasting time, missing important tweets",
                "solution": "Let tweets call you instead",
                "action": "Get phone call alerts"
            },
            {
                "problem": "Competitors are always one step ahead",
                "pain": "Losing market share, missing opportunities",
                "solution": "Monitor their moves in real-time",
                "action": "Set up competitive intelligence"
            },
            {
                "problem": "Your content doesn't get traction",
                "pain": "Low engagement, wasted effort",
                "solution": "Post when trends are emerging",
                "action": "Use trend prediction"
            },
            {
                "problem": "Manual reporting takes forever",
                "pain": "Time-consuming, error-prone",
                "solution": "Automated analytics and reports",
                "action": "Set up daily digests"
            },
            {
                "problem": "Slow response to customer feedback",
                "pain": "Damaged reputation, lost customers",
                "solution": "Instant notification system",
                "action": "Monitor brand mentions"
            }
        ]
        
        if index >= len(problems):
            index = 0
        
        p = problems[index]
        
        tweet = f"⚡ Solve This: {p['problem']}\n\n"
        tweet += f"The pain: {p['pain']}\n\n"
        tweet += f"💡 Solution: {p['solution']}\n"
        tweet += f"🚀 Action: {p['action']} with PostAlert.ai\n\n"
        tweet += f"Start solving: https://postalert.ai/solutions\n\n"
        tweet += f"#ProblemSolving #Solution #Productivity"
        
        return self._validate_length(tweet)
    
    def generate_comparison(self, index: int = 0) -> str:
        """生成对比优势推文"""
        comparisons = [
            {
                "vs": "Manual monitoring",
                "our_advantage": "Saves 10+ hours/week",
                "key_difference": "Automation vs manual work",
                "result": "Focus on strategy, not scrolling"
            },
            {
                "vs": "Traditional alerts",
                "our_advantage": "Phone calls beat emails/push",
                "key_difference": "Impossible to miss vs easy to ignore",
                "result": "100% notification delivery rate"
            },
            {
                "vs": "Basic monitoring tools",
                "our_advantage": "AI predicts trends before they peak",
                "key_difference": "Reactive vs predictive",
                "result": "Stay ahead, not just keep up"
            },
            {
                "vs": "Enterprise solutions",
                "our_advantage": "Startup-friendly pricing",
                "key_difference": "$99/month vs $10,000+/year",
                "result": "Enterprise features at startup prices"
            }
        ]
        
        if index >= len(comparisons):
            index = 0
        
        comp = comparisons[index]
        
        tweet = f"🆚 PostAlert.ai vs {comp['vs']}\n\n"
        tweet += f"Our advantage: {comp['our_advantage']}\n"
        tweet += f"Key difference: {comp['key_difference']}\n"
        tweet += f"Result: {comp['result']}\n\n"
        tweet += f"See the full comparison: https://postalert.ai/compare\n\n"
        tweet += f"#Comparison #Advantage #BetterWay"
        
        return self._validate_length(tweet)
    
    def generate_viral_tweet(self, angle: str = None) -> str:
        """生成病毒式营销推文"""
        if angle is None:
            angle = random.choice(self.viral_angles)
        
        templates = {
            "FOMO (Fear Of Missing Out)": [
                "Your competitors are using PostAlert.ai to monitor your moves. Are you?",
                "Traders making 30% better decisions with our alerts. Don't get left behind.",
                "Journalists breaking stories first with our trend detection. Want to be next?"
            ],
            "Social Proof": [
                "Join 10,000+ crypto traders using PostAlert.ai for real-time alerts",
                "Fortune 500 companies trust us with their competitive intelligence",
                "Top journalists rely on our trend prediction to stay ahead"
            ],
            "Scarcity": [
                "Only 100 spots left for our free trial this month",
                "Early access to new AI features for first 500 signups",
                "Limited-time offer: 50% off annual plan ends Friday"
            ],
            "Curiosity Gap": [
                "The one tool crypto whales don't want you to know about",
                "How journalists are finding stories 24 hours before they trend",
                "The secret to 2x more viral content (it's not what you think)"
            ]
        }
        
        # 获取对应角度的模板
        if angle in templates:
            template = random.choice(templates[angle])
        else:
            template = f"How {angle} can transform your social media monitoring"
        
        tweet = f"{template}\n\n"
        tweet += f"Discover PostAlert.ai: https://postalert.ai\n\n"
        tweet += f"#{angle.replace(' ', '').replace('(', '').replace(')', '')} #Viral #Marketing"
        
        return self._validate_length(tweet)
    
    def generate_30min_tweet(self, minute_of_hour: int = None) -> str:
        """生成30分钟间隔推文"""
        if minute_of_hour is None:
            now = datetime.utcnow()
            minute_of_hour = now.minute
        
        # 每30分钟切换内容类型
        content_slot = minute_of_hour // 30
        
        # 8种内容类型轮换
        content_types = list(self.content_types.keys())
        type_index = (datetime.utcnow().hour * 2 + content_slot) % len(content_types)
        content_type = content_types[type_index]
        
        # 每种类型内的索引
        type_info = self.content_types[content_type]
        item_index = (datetime.utcnow().day * 2 + content_slot) % type_info["count"]
        
        print(f"🕐 Generating {content_type} tweet (slot {content_slot}, index {item_index})")
        
        # 调用对应的生成函数
        if content_type == "product_feature":
            return self.generate_product_feature(item_index)
        elif content_type == "use_case":
            return self.generate_use_case(item_index)
        elif content_type == "problem_solution":
            return self.generate_problem_solution(item_index)
        elif content_type == "comparison":
            return self.generate_comparison(item_index)
        elif content_type == "testimonial":
            return self.generate_product_feature(item_index)  # 暂时复用
        elif content_type == "educational":
            return self.generate_use_case(item_index)  # 暂时复用
        elif content_type == "trend_analysis":
            return self.generate_problem_solution(item_index)  # 暂时复用
        else:  # behind_scenes
            return self.generate_viral_tweet()
    
    def _generate_hashtags(self, count: int = 3) -> str:
        """生成话题标签"""
        selected = random.sample(self.trending_hashtags, min(count, len(self.trending_hashtags)))
        return " ".join(selected)
    
    def _validate_length(self, tweet: str, max_len: int = 280) -> str:
        """验证推文长度"""
        if len(tweet) > max_len:
            tweet = tweet[:max_len-3] + "..."
        return tweet
    
    def send_tweet(self, content: str) -> str:
        """发送推文"""
        if not self.twitter.user:
            print("❌ Not connected to Twitter")
            return None
        
        return self.twitter.send_tweet(content)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Upgraded Twitter Content Generator")
    parser.add_argument('--test', action='store_true', help='Test all content types')
    parser.add_argument('--30min', type=int, help='Generate 30-minute interval tweet for minute (0-59)')
    parser.add_argument('--viral', type=str, help='Generate viral tweet with specific angle')
    parser.add_argument('--send-test', action='store_true', help='Send a test tweet')
    
    args = parser.parse_args()
    
    # 初始化
    generator = UpgradedContentGenerator()
    
    if not generator.twitter.user:
        print("❌ Twitter connection failed. Check credentials.")
        return
    
    print(f"✅ Connected to Twitter: @{generator.twitter.user.username}")
    print(f"📚 Content types: {len(generator.content_types)} types")
    print(f"🎯 Viral angles: {len(generator.viral_angles)} angles")
    print(f"🏷️ Hashtags: {len(generator.trending_hashtags)} trending tags")
    
    if args.test:
        print("\n🧪 Testing all content types:")
        print("=" * 50)
        
        # 测试产品功能
        print("\n1. Product Features:")
        for i in range(3):
            tweet = generator.generate_product_feature(i)
            print(f"\nFeature {i}:")
            print(tweet[:100] + "..." if len(tweet) > 100 else tweet)
        
        # 测试使用案例
        print("\n\n2. Use Cases:")
        for i in range(3):
            tweet = generator.generate_use_case(i)
            print(f"\nUse Case {i}:")
            print(tweet[:100] + "..." if len(tweet) > 100 else tweet)
        
        # 测试问题解决方案
        print("\n\n3. Problem Solutions:")
        for i in range(3):
            tweet = generator.generate_problem_solution(i)
            print(f"\nSolution {i}:")
            print(tweet[:100] + "..." if len(tweet) > 100 else tweet)
        
        # 测试对比
        print("\n\n4. Comparisons:")
        for i in range(2):
            tweet = generator.generate_comparison(i)
            print(f"\nComparison {i}:")
            print(tweet[:100] + "..." if len(tweet) > 100 else tweet)
        
        # 测试病毒式营销
        print("\n\n5. Viral Tweets:")
        for i in range(2):
            angle = generator.viral_angles[i]
            tweet = generator.generate_viral_tweet(angle)
            print(f"\nViral ({angle}):")
            print(tweet[:100] + "..." if len(tweet) > 100 else tweet)
    
    elif args._30min is not None:
        tweet = generator.generate_30min_tweet(args._30min)
        print(f"📝 30-minute tweet (minute {args._30min}):\n{tweet}\n")
        
        confirm = input("Send this tweet? (yes/no): ").lower()
        if confirm in ['yes', 'y']:
            tweet_id = generator.send_tweet(tweet)
            if tweet_id:
                print(f"✅ Tweet sent! ID: {tweet_id}")
    
    elif args.viral:
        tweet = generator.generate_viral_tweet(args.viral)
        print(f"📝 Viral tweet ({args.viral}):\n{tweet}\n")
        
        confirm = input("Send this tweet? (yes/no): ").lower()
        if confirm in ['yes', 'y']:
            tweet_id = generator.send_tweet(tweet)
            if tweet_id:
                print(f"✅ Tweet sent! ID: {tweet_id}")
    
    elif args.send_test:
        print("🧪 Sending test tweet...")
        tweet = generator.generate_product_feature(0)
        print(f"📝 Test tweet:\n{tweet}\n")
        
        tweet_id = generator.send_tweet(tweet)
        if tweet_id:
            print(f"✅ Test tweet sent! ID: {tweet_id}")
            print(f"   Link: https://twitter.com/{generator.twitter.user.username}/status/{tweet_id}")
        else:
            print("❌ Failed to send test tweet")
    
    else:
        # 显示帮助
        print("Upgraded Twitter Content Generator")
        print("\nUsage:")
        print("  python upgraded_content_generator.py --test")
        print("  python upgraded_content_generator.py --30min 15")
        print("  python upgraded_content_generator.py --viral \"FOMO\"")
        print("  python upgraded_content_generator.py --send-test")