#!/usr/bin/env python3
"""
24小时全天候推特营销系统
每30分钟发布一条推文，24小时不间断
"""

import sys
sys.path.insert(0, '.')

from upgraded_content_generator import UpgradedContentGenerator
import time
from datetime import datetime, timedelta
import json
import os
import random

class TwentyFourHourScheduler:
    """24小时全天候调度器"""
    
    def __init__(self):
        self.generator = UpgradedContentGenerator()
        self.schedule_file = "24hour_schedule.json"
        self.schedule = self._load_schedule()
        
        # 24小时不间断发布
        self.active_hours = list(range(0, 24))  # 0-23点，全天
        
        # 30分钟发布槽位
        self.active_slots = [0, 30]  # 每小时的第0分钟和第30分钟
        
        # 不同时段的发布策略
        self.time_strategies = {
            "peak": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],  # 高峰时段
            "normal": [8, 21, 22, 23],  # 正常时段
            "off_peak": [0, 1, 2, 3, 4, 5, 6, 7]  # 低谷时段
        }
        
        # 不同时段的内容策略
        self.content_strategies = {
            "peak": {
                "types": ["product_feature", "use_case", "comparison", "viral"],
                "hashtags": 5,
                "engagement": "high"
            },
            "normal": {
                "types": ["problem_solution", "educational", "testimonial"],
                "hashtags": 4,
                "engagement": "medium"
            },
            "off_peak": {
                "types": ["trend_analysis", "behind_scenes", "educational"],
                "hashtags": 3,
                "engagement": "low"
            }
        }
    
    def _load_schedule(self):
        """加载发布计划"""
        if os.path.exists(self.schedule_file):
            try:
                with open(self.schedule_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # 默认计划
        return {
            "last_post_time": None,
            "total_posts": 0,
            "daily_stats": {},
            "hourly_stats": {},
            "content_rotation": {
                "peak_index": 0,
                "normal_index": 0,
                "off_peak_index": 0,
                "viral_angle_index": 0
            }
        }
    
    def _save_schedule(self):
        """保存发布计划"""
        with open(self.schedule_file, 'w') as f:
            json.dump(self.schedule, f, indent=2)
    
    def get_time_strategy(self, hour: int) -> str:
        """获取当前时段的策略"""
        for strategy, hours in self.time_strategies.items():
            if hour in hours:
                return strategy
        return "normal"
    
    def generate_24hour_tweet(self, hour: int, minute: int) -> str:
        """生成24小时推文"""
        strategy = self.get_time_strategy(hour)
        strategy_config = self.content_strategies[strategy]
        
        print(f"🕐 Generating 24-hour tweet for {hour:02d}:{minute:02d} UTC")
        print(f"   Strategy: {strategy} | Types: {strategy_config['types']}")
        
        # 根据策略选择内容类型
        content_type = random.choice(strategy_config["types"])
        
        # 如果是病毒式营销，使用特定角度
        if content_type == "viral":
            angle_index = self.schedule["content_rotation"]["viral_angle_index"]
            angle = self.generator.viral_angles[angle_index % len(self.generator.viral_angles)]
            self.schedule["content_rotation"]["viral_angle_index"] += 1
            tweet = self.generator.generate_viral_tweet(angle)
        else:
            # 根据内容类型生成推文
            if content_type == "product_feature":
                index = self.schedule["content_rotation"]["peak_index"] % 6
                self.schedule["content_rotation"]["peak_index"] += 1
                tweet = self.generator.generate_product_feature(index)
            elif content_type == "use_case":
                index = self.schedule["content_rotation"]["peak_index"] % 6
                self.schedule["content_rotation"]["peak_index"] += 1
                tweet = self.generator.generate_use_case(index)
            elif content_type == "comparison":
                index = self.schedule["content_rotation"]["peak_index"] % 4
                self.schedule["content_rotation"]["peak_index"] += 1
                tweet = self.generator.generate_comparison(index)
            elif content_type == "problem_solution":
                index = self.schedule["content_rotation"]["normal_index"] % 5
                self.schedule["content_rotation"]["normal_index"] += 1
                tweet = self.generator.generate_problem_solution(index)
            elif content_type == "testimonial":
                index = self.schedule["content_rotation"]["normal_index"] % 5
                self.schedule["content_rotation"]["normal_index"] += 1
                tweet = self.generator.generate_product_feature(index)  # 暂时复用
            elif content_type == "educational":
                index = self.schedule["content_rotation"]["normal_index"] % 6
                self.schedule["content_rotation"]["normal_index"] += 1
                tweet = self.generator.generate_use_case(index)  # 暂时复用
            elif content_type == "trend_analysis":
                index = self.schedule["content_rotation"]["off_peak_index"] % 4
                self.schedule["content_rotation"]["off_peak_index"] += 1
                tweet = self.generator.generate_problem_solution(index)  # 暂时复用
            else:  # behind_scenes
                index = self.schedule["content_rotation"]["off_peak_index"] % 3
                self.schedule["content_rotation"]["off_peak_index"] += 1
                tweet = self.generator.generate_viral_tweet()
        
        self._save_schedule()
        
        # 添加时间标记和策略信息
        time_str = f"{hour:02d}:{minute:02d} UTC"
        strategy_emoji = {"peak": "🔥", "normal": "⚡", "off_peak": "🌙"}[strategy]
        
        tweet = tweet.replace("\n\n", f"\n\n{strategy_emoji} Posted at {time_str} ({strategy} hours)\n\n", 1)
        
        return self.generator._validate_length(tweet)
    
    def should_post_now(self) -> bool:
        """判断当前是否应该发布"""
        now = datetime.utcnow()
        current_hour = now.hour
        current_minute = now.minute
        
        # 检查是否是30分钟槽位
        current_slot = None
        for slot in self.active_slots:
            if abs(current_minute - slot) <= 2:  # ±2分钟窗口
                current_slot = slot
                break
        
        if current_slot is None:
            return False
        
        # 检查是否已经在当前槽位发布过
        last_post = self.schedule.get("last_post_time")
        if last_post:
            last_time = datetime.fromisoformat(last_post)
            time_diff = (now - last_time).total_seconds() / 60  # 分钟
            
            # 如果25分钟内已经发布过，跳过
            if time_diff < 25:
                print(f"⏰ Too soon since last post ({time_diff:.1f} minutes ago)")
                return False
        
        return True
    
    def post_24hour_tweet(self) -> bool:
        """发布24小时推文"""
        if not self.should_post_now():
            return False
        
        now = datetime.utcnow()
        current_hour = now.hour
        current_minute = now.minute
        
        print(f"🚀 Preparing to post 24-hour tweet for {current_hour:02d}:{current_minute:02d} UTC...")
        
        # 生成推文
        tweet = self.generate_24hour_tweet(current_hour, current_minute)
        print(f"📝 Tweet content:\n{tweet}\n")
        
        # 发送推文
        tweet_id = self.generator.send_tweet(tweet)
        
        if tweet_id:
            # 更新统计
            self.schedule["last_post_time"] = now.isoformat()
            self.schedule["total_posts"] += 1
            
            date_key = now.date().isoformat()
            hour_key = f"{date_key}_{current_hour}"
            
            if date_key not in self.schedule["daily_stats"]:
                self.schedule["daily_stats"][date_key] = 0
            self.schedule["daily_stats"][date_key] += 1
            
            if hour_key not in self.schedule["hourly_stats"]:
                self.schedule["hourly_stats"][hour_key] = 0
            self.schedule["hourly_stats"][hour_key] += 1
            
            self._save_schedule()
            
            print(f"✅ 24-hour tweet posted successfully!")
            print(f"   Tweet ID: {tweet_id}")
            print(f"   Strategy: {self.get_time_strategy(current_hour)}")
            print(f"   Today's posts: {self.schedule['daily_stats'].get(date_key, 0)}")
            print(f"   Total posts: {self.schedule['total_posts']}")
            
            return True
        else:
            print("❌ Failed to post 24-hour tweet")
            return False
    
    def run_24hour_schedule(self, check_interval_minutes: int = 2):
        """运行24小时调度"""
        print("🌍 启动24小时全天候推特营销系统")
        print("=" * 60)
        print("📅 发布策略:")
        print(f"   高峰时段 (🔥): UTC {self.time_strategies['peak'][0]:02d}:00-{self.time_strategies['peak'][-1]:02d}:59")
        print(f"   正常时段 (⚡): UTC {self.time_strategies['normal'][0]:02d}:00-{self.time_strategies['normal'][-1]:02d}:59")
        print(f"   低谷时段 (🌙): UTC {self.time_strategies['off_peak'][0]:02d}:00-{self.time_strategies['off_peak'][-1]:02d}:59")
        print(f"   发布频率: 每30分钟")
        print(f"   每日最大推文: {len(self.active_hours) * len(self.active_slots)} 条")
        print(f"   检查间隔: {check_interval_minutes} 分钟")
        print("=" * 60)
        
        try:
            while True:
                now = datetime.utcnow()
                current_hour = now.hour
                current_minute = now.minute
                
                # 检查是否是发布槽位（±2分钟窗口）
                should_check = False
                for slot in self.active_slots:
                    if abs(current_minute - slot) <= 2:
                        should_check = True
                        break
                
                if should_check:
                    print(f"\n🕐 检查时间: {current_hour:02d}:{current_minute:02d} UTC")
                    print(f"   时段策略: {self.get_time_strategy(current_hour)}")
                    
                    if self.post_24hour_tweet():
                        # 发布成功后等待到下一个槽位
                        minutes_to_next_slot = 30 - (current_minute % 30)
                        if minutes_to_next_slot == 0:
                            minutes_to_next_slot = 30
                        
                        print(f"⏳ 等待 {minutes_to_next_slot} 分钟到下一个发布槽位...")
                        time.sleep(minutes_to_next_slot * 60)
                    else:
                        print(f"⏳ 当前不发布，{check_interval_minutes} 分钟后再次检查...")
                        time.sleep(check_interval_minutes * 60)
                else:
                    # 计算到下一个检查点的时间
                    minutes_to_next_check = check_interval_minutes - (current_minute % check_interval_minutes)
                    if minutes_to_next_check == 0:
                        minutes_to_next_check = check_interval_minutes
                    
                    # 计算到下一个槽位的时间
                    minutes_to_next_slot = min([(slot - current_minute) % 60 for slot in self.active_slots])
                    
                    # 显示状态
                    next_check = now + timedelta(minutes=minutes_to_next_check)
                    next_slot = now + timedelta(minutes=minutes_to_next_slot)
                    
                    strategy = self.get_time_strategy(current_hour)
                    emoji = {"peak": "🔥", "normal": "⚡", "off_peak": "🌙"}[strategy]
                    
                    status = f"{emoji} {current_hour:02d}:{current_minute:02d} UTC ({strategy}) | 下次检查: {next_check.hour:02d}:{next_check.minute:02d} | 下次发布: {next_slot.hour:02d}:{next_slot.minute:02d}"
                    
                    # 清除行并显示状态
                    print(f"\r{status}", end="", flush=True)
                    
                    time.sleep(60)  # 每分钟更新一次显示
                    
        except KeyboardInterrupt:
            print("\n\n🛑 24小时调度器已停止")
            self.show_stats()
    
    def show_stats(self):
        """显示统计信息"""
        print("\n📊 24小时营销系统统计:")
        print(f"   总发布数: {self.schedule['total_posts']}")
        
        last_post = self.schedule.get('last_post_time')
        if last_post:
            last_time = datetime.fromisoformat(last_post)
            print(f"   最后发布: {last_time.strftime('%Y-%m-%d %H:%M UTC')}")
        else:
            print(f"   最后发布: 从未")
        
        if self.schedule['daily_stats']:
            print(f"   每日发布统计:")
            sorted_days = sorted(self.schedule['daily_stats'].items(), reverse=True)[:5]
            for date_str, count in sorted_days:
                print(f"     {date_str}: {count} 条推文")
        
        # 显示时段策略统计
        print(f"\n   时段策略分布:")
        for strategy, hours in self.time_strategies.items():
            count = 0
            for hour in hours:
                for date_str in self.schedule['daily_stats'].keys():
                    hour_key = f"{date_str}_{hour}"
                    count += self.schedule['hourly_stats'].get(hour_key, 0)
            
            emoji = {"peak": "🔥", "normal": "⚡", "off_peak": "🌙"}[strategy]
            print(f"     {emoji} {strategy}: {count} 条推文")
    
    def simulate_24hours(self):
        """模拟24小时发布计划"""
        print("📅 模拟24小时发布计划:")
        print("=" * 60)
        
        total_posts = 0
        
        for hour in range(24):
            for slot in self.active_slots:
                strategy = self.get_time_strategy(hour)
                emoji = {"peak": "🔥", "normal": "⚡", "off_peak": "🌙"}[strategy]
                
                print(f"{emoji} {hour:02d}:{slot:02d} UTC ({strategy}) - 发布")
                total_posts += 1
        
        print("=" * 60)
        print(f"✅ 24小时模拟完成")
        print(f"   总发布数: {total_posts} 条")
        print(f"   高峰时段: {len(self.time_strategies['peak']) * 2} 条")
        print(f"   正常时段: {len(self.time_strategies['normal']) * 2} 条")
        print(f"   低谷时段: {len(self.time_strategies['off_peak']) * 2} 条")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="24-Hour Twitter Marketing System")
    parser.add_argument('--run', action='store_true', help='Run 24-hour scheduler')
    parser.add_argument('--post-now', action='store_true', help='Post immediately if due')
    parser.add_argument('--simulate', action='store_true', help='Simulate 24-hour schedule')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--test', action='store_true', help='Test tweet generation')
    parser.add_argument('--interval', type=int, default=2, help='Check interval in minutes')
    
    args = parser.parse_args()
    
    # 初始化
    scheduler = TwentyFourHourScheduler()
    
    if not scheduler.generator.twitter.user:
        print("❌ Twitter connection failed. Check credentials.")
        return
    
    print(f"✅ Connected to Twitter: @{scheduler.generator.twitter.user.username}")
    print(f"🌍 24-Hour Marketing System")
    print(f"⏰ Schedule: Every 30 minutes, 24/7")
    print(f"📊 Max daily posts: {len(scheduler.active_hours) * len(scheduler.active_slots)}")
    
    if args.run:
        scheduler.run_24hour_schedule(args.interval)
    
    elif args.post_now:
        if scheduler.post_24hour_tweet():
            print("✅ Posted successfully!")
        else:
            print("⏸️ Not posting now (not due)")
    
    elif args.simulate:
        scheduler.simulate_24hours()
    
    elif args.stats:
        scheduler.show_stats()
    
    elif args.test:
        print("🧪 Testing 24-hour tweet generation:")
        # 测试不同时段的推文
        test_hours = [9, 15, 22, 3]  # 高峰、正常、低谷各测试一个
        for hour in test_hours:
            strategy = scheduler.get_time_strategy(hour)
            emoji = {"peak": "🔥", "normal": "⚡", "off_peak": "🌙"}[strategy]
            
            print(f"\n{emoji} Testing hour {hour:02d}:00 ({strategy}):")
            tweet = scheduler.generate_24hour_tweet(hour, 0)
            print(tweet[:150] + "..." if len(tweet) > 150 else tweet)
            print(f"Length: {len(tweet)}/280 characters")
    
    else:
        # 显示帮助
        print("24-Hour Twitter Marketing System for PostAlert.ai")
        print("\n🚀 ULTIMATE UPGRADE FEATURES:")
        print("  • 24/7 non-stop posting")
        print("  • Every 30 minutes")
        print("  • Smart time-based strategies")
        print("  • Peak/Normal/Off-peak optimization")
        print("  • Max 48 tweets per day")
        print("\n📅 Time Strategies:")
        print("  🔥 Peak (9:00-20:59 UTC): Product features, comparisons, viral")
        print("  ⚡ Normal (8:00, 21:00-23:59 UTC): Problem solutions, testimonials")
        print("  🌙 Off-peak (0:00-7:59 UTC): Trend analysis, behind scenes")
        print("\nUsage:")
        print("  python 24hour_scheduler.py --run")
        print("  python 24hour_scheduler.py --post-now")
        print("  python 24hour_scheduler.py --simulate")
        print("  python 24hour_scheduler.py --stats")
        print("  python 24hour_scheduler.py --test")

if __name__ == "__main__":
    main()
