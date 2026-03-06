#!/usr/bin/env python3
"""
English Tweet Generator for Product Promotion
专门为英文用户和产品宣传设计的推文生成器
"""

import random
from datetime import datetime
from typing import List, Dict, Optional

class EnglishTweetGenerator:
    """英文推文生成器"""
    
    def __init__(self, product_name: str = "Our Product", company_name: str = "Our Company"):
        self.product_name = product_name
        self.company_name = company_name
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        
        # 内容模板库
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict:
        """加载推文模板"""
        return {
            "product_launch": [
                {
                    "emoji": "🚀",
                    "template": "{emoji} New Feature: {feature}\n\n{description}\n\nTry it now: {link}\n\n{hashtags}",
                    "hashtags": ["#ProductUpdate", "#Tech", "#Innovation"]
                },
                {
                    "emoji": "🎉",
                    "template": "{emoji} Just Launched: {feature}\n\n{description}\n\nLearn more: {link}\n\n{hashtags}",
                    "hashtags": ["#NewFeature", "#Launch", "#Technology"]
                }
            ],
            "educational": [
                {
                    "emoji": "💡",
                    "template": "{emoji} Quick Tip: {tip}\n\n{explanation}\n\nHow {product} helps: {solution}\n\n{hashtags}",
                    "hashtags": ["#TechTips", "#HowTo", "#Productivity"]
                },
                {
                    "emoji": "📚",
                    "template": "{emoji} Did You Know?\n\n{tip}\n\n{explanation}\n\n{hashtags}",
                    "hashtags": ["#IndustryInsights", "#Learning", "#Knowledge"]
                }
            ],
            "success_story": [
                {
                    "emoji": "🏆",
                    "template": "{emoji} Customer Success!\n\n{company} achieved {result} using {product}.\n\n\"{quote}\"\n\nCase study: {link}\n\n{hashtags}",
                    "hashtags": ["#CustomerSuccess", "#CaseStudy", "#Results"]
                },
                {
                    "emoji": "✅",
                    "template": "{emoji} Real Results:\n\n{result} improvement for {company}\n\nHow: using {product}\n\nLearn how: {link}\n\n{hashtags}",
                    "hashtags": ["#SuccessStory", "#BusinessGrowth", "#Metrics"]
                }
            ],
            "industry_insights": [
                {
                    "emoji": "📊",
                    "template": "{emoji} Industry Trend: {trend}\n\n{analysis}\n\nOur perspective: {perspective}\n\nWhat's your take? 👇\n\n{hashtags}",
                    "hashtags": ["#IndustryAnalysis", "#Trends", "#Future"]
                },
                {
                    "emoji": "🤔",
                    "template": "{emoji} Question for {audience}:\n\n{question}\n\nWe think: {answer}\n\nShare your thoughts below! 👇\n\n{hashtags}",
                    "hashtags": ["#Discussion", "#Community", "#Engagement"]
                }
            ],
            "problem_solution": [
                {
                    "emoji": "🔧",
                    "template": "Struggling with {problem}?\n\n{product} helps by:\n✓ {solution1}\n✓ {solution2}\n✓ {solution3}\n\nFree trial: {link}\n\n{hashtags}",
                    "hashtags": ["#ProblemSolved", "#Solution", "#Efficiency"]
                }
            ]
        }
    
    def generate_product_launch(self, feature: str, description: str, link: str = "") -> str:
        """生成产品发布推文"""
        template = random.choice(self.templates["product_launch"])
        
        # 确保链接格式正确
        if link and not link.startswith("http"):
            link = f"https://{link}"
        
        tweet = template["template"].format(
            emoji=template["emoji"],
            feature=feature,
            description=description,
            link=link if link else f"https://example.com/{feature.lower().replace(' ', '-')}",
            hashtags=" ".join(template["hashtags"])
        )
        
        return self._validate_length(tweet)
    
    def generate_educational_tweet(self, topic: str, tip: str, explanation: str) -> str:
        """生成教育性推文"""
        template = random.choice(self.templates["educational"])
        
        tweet = template["template"].format(
            emoji=template["emoji"],
            tip=tip,
            explanation=explanation,
            product=self.product_name,
            solution=f"making {topic} easier and more efficient",
            hashtags=" ".join(template["hashtags"])
        )
        
        return self._validate_length(tweet)
    
    def generate_success_story(self, company: str, result: str, quote: str = "", link: str = "") -> str:
        """生成成功案例推文"""
        template = random.choice(self.templates["success_story"])
        
        if not quote:
            quote = f"\"{self.product_name} transformed our workflow and delivered measurable results.\""
        
        tweet = template["template"].format(
            emoji=template["emoji"],
            company=company,
            result=result,
            product=self.product_name,
            quote=quote,
            link=link if link else f"https://example.com/case-studies/{company.lower().replace(' ', '-')}",
            hashtags=" ".join(template["hashtags"])
        )
        
        return self._validate_length(tweet)
    
    def generate_industry_insight(self, trend: str, analysis: str, perspective: str) -> str:
        """生成行业洞察推文"""
        template = random.choice(self.templates["industry_insights"])
        
        tweet = template["template"].format(
            emoji=template["emoji"],
            trend=trend,
            analysis=analysis,
            perspective=perspective,
            audience="tech professionals",
            question=f"How is {trend.lower()} affecting your business?",
            answer=f"{trend} presents both challenges and opportunities for innovation",
            hashtags=" ".join(template["hashtags"])
        )
        
        return self._validate_length(tweet)
    
    def generate_problem_solution(self, problem: str, solutions: List[str], link: str = "") -> str:
        """生成问题解决方案推文"""
        template = random.choice(self.templates["problem_solution"])
        
        # 确保有3个解决方案
        while len(solutions) < 3:
            solutions.append(f"Streamlining your {problem.lower()} workflow")
        
        tweet = template["template"].format(
            emoji=template["emoji"],
            problem=problem,
            product=self.product_name,
            solution1=solutions[0],
            solution2=solutions[1] if len(solutions) > 1 else solutions[0],
            solution3=solutions[2] if len(solutions) > 2 else solutions[0],
            link=link if link else f"https://example.com/solve-{problem.lower().replace(' ', '-')}",
            hashtags=" ".join(template["hashtags"])
        )
        
        return self._validate_length(tweet)
    
    def generate_daily_tweet(self, day_of_week: Optional[str] = None) -> str:
        """根据星期几生成每日推文"""
        if not day_of_week:
            day_of_week = datetime.now().strftime("%A")
        
        day_themes = {
            "Monday": ("product_launch", "Start the week with a product update"),
            "Tuesday": ("educational", "Tech tip Tuesday"),
            "Wednesday": ("success_story", "Midweek motivation with a success story"),
            "Thursday": ("industry_insights", "Industry insights for Thursday"),
            "Friday": ("problem_solution", "Solve problems before the weekend"),
            "Saturday": ("educational", "Weekend learning"),
            "Sunday": ("industry_insights", "Sunday insights for the week ahead")
        }
        
        theme, description = day_themes.get(day_of_week, ("educational", "Daily update"))
        
        # 根据主题生成推文
        if theme == "product_launch":
            features = [
                "AI-powered analytics dashboard",
                "Real-time collaboration tools",
                "Advanced reporting features",
                "Mobile optimization update",
                "Integration with popular platforms"
            ]
            return self.generate_product_launch(
                feature=random.choice(features),
                description=f"Our latest update helps teams work smarter and faster.",
                link=""
            )
        
        elif theme == "educational":
            topics = [
                "data analysis",
                "team collaboration",
                "project management",
                "business intelligence",
                "workflow optimization"
            ]
            topic = random.choice(topics)
            return self.generate_educational_tweet(
                topic=topic,
                tip=f"Best practices for {topic}",
                explanation=f"Effective {topic} can increase productivity by up to 40%."
            )
        
        elif theme == "success_story":
            companies = [
                "TechCorp Inc.",
                "StartupXYZ",
                "GlobalSolutions Ltd.",
                "InnovateCo",
                "FutureTech Partners"
            ]
            results = [
                "increased efficiency by 35%",
                "reduced operational costs by 25%",
                "improved team collaboration by 50%",
                "accelerated decision-making by 60%",
                "boosted customer satisfaction by 40%"
            ]
            return self.generate_success_story(
                company=random.choice(companies),
                result=random.choice(results)
            )
        
        elif theme == "industry_insights":
            trends = [
                "Remote work optimization",
                "AI integration in business",
                "Data-driven decision making",
                "Sustainable technology",
                "Digital transformation"
            ]
            trend = random.choice(trends)
            return self.generate_industry_insight(
                trend=trend,
                analysis=f"{trend} is reshaping how businesses operate in 2026.",
                perspective=f"Embracing {trend.lower()} is key to staying competitive."
            )
        
        else:  # problem_solution
            problems = [
                "inefficient workflows",
                "data silos",
                "poor team collaboration",
                "slow decision-making",
                "lack of actionable insights"
            ]
            problem = random.choice(problems)
            return self.generate_problem_solution(
                problem=problem,
                solutions=[
                    f"Automating repetitive tasks",
                    f"Centralizing data access",
                    f"Enabling real-time collaboration",
                    f"Providing predictive analytics"
                ]
            )
    
    def _validate_length(self, tweet: str) -> str:
        """验证推文长度，确保不超过280字符"""
        if len(tweet) > 280:
            # 尝试缩短
            tweet = tweet[:277] + "..."
            if len(tweet) > 280:
                tweet = tweet[:280]
        
        return tweet
    
    def add_hashtags(self, tweet: str, additional_tags: List[str] = None) -> str:
        """添加额外的话题标签"""
        if additional_tags:
            # 移除现有的标签行
            lines = tweet.split('\n')
            if lines[-1].startswith('#'):
                lines = lines[:-1]
            
            # 添加新标签
            all_tags = ["#" + tag.replace("#", "").replace(" ", "") for tag in additional_tags]
            lines.append(" ".join(all_tags[:3]))  # 最多添加3个
            
            tweet = '\n'.join(lines)
        
        return self._validate_length(tweet)
    
    def generate_thread(self, topic: str, num_tweets: int = 3) -> List[str]:
        """生成推文线程"""
        tweets = []
        
        # 第一条推文：介绍
        intro_tweet = self.generate_educational_tweet(
            topic=topic,
            tip=f"Complete guide to {topic}",
            explanation=f"Thread 🧵: {num_tweets} key insights about {topic}"
        )
        tweets.append(intro_tweet)
        
        # 中间推文：要点
        insights = [
            f"1️⃣ Key insight about {topic}",
            f"2️⃣ Practical application of {topic}",
            f"3️⃣ Common mistakes with {topic}",
            f"4️⃣ Best practices for {topic}",
            f"5️⃣ Future trends in {topic}"
        ]
        
        for i in range(1, min(num_tweets, len(insights) + 1)):
            tweet = f"{insights[i-1]}\n\n{self._get_insight_detail(topic, i)}\n\n#{topic.replace(' ', '')} #Thread"
            tweets.append(self._validate_length(tweet))
        
        return tweets
    
    def _get_insight_detail(self, topic: str, point_num: int) -> str:
        """获取洞察详情"""
        details = {
            1: f"Understanding {topic} fundamentals is crucial for effective implementation.",
            2: f"Apply {topic} principles to solve real-world business challenges.",
            3: f"Avoid overlooking the human element when implementing {topic} solutions.",
            4: f"Regular assessment and adaptation are key to {topic} success.",
            5: f"{topic.title()} will continue evolving with emerging technologies."
        }
        return details.get(point_num, f"Important aspect of {topic} to consider.")

def main():
    """测试英文推文生成器"""
    print("🇬🇧 English Tweet Generator Test")
    print("=" * 50)
    
    generator = EnglishTweetGenerator(product_name="OpenClaw AI", company_name="OpenClaw")
    
    # 测试各种类型的推文
    print("\n1. Product Launch Tweet:")
    tweet1 = generator.generate_product_launch(
        feature="Smart Automation Suite",
        description="Automate repetitive tasks with AI-powered workflows.",
        link="https://openclaw.ai/features/automation"
    )
    print(tweet1)
    print(f"Length: {len(tweet1)}/280 characters")
    
    print("\n2. Educational Tweet:")
    tweet2 = generator.generate_educational_tweet(
        topic="AI automation",
        tip="Start with small, repetitive tasks",
        explanation="Begin automation with tasks that follow clear patterns for quick wins."
    )
    print(tweet2)
    print(f"Length: {len(tweet2)}/280 characters")
    
    print("\n3. Success Story Tweet:")
    tweet3 = generator.generate_success_story(
        company="TechStart Inc.",
        result="reduced manual work by 70%",
        quote="\"OpenClaw transformed our workflow from chaotic to streamlined.\" - CEO"
    )
    print(tweet3)
    print(f"Length: {len(tweet3)}/280 characters")
    
    print("\n4. Daily Tweet (Today):")
    tweet4 = generator.generate_daily_tweet()
    print(tweet4)
    print(f"Length: {len(tweet4)}/280 characters")
    
    print("\n5. Thread Example (first tweet):")
    thread = generator.generate_thread("AI Automation", 3)
    for i, tweet in enumerate(thread, 1):
        print(f"\nTweet {i}:")
        print(tweet)
        print(f"Length: {len(tweet)}/280 characters")

if __name__ == "__main__":
    main()