#!/usr/bin/env python3
"""
升级版30分钟调度器
每30分钟自动发布一条推文，支持更多样化的内容
"""

import sys
sys.path.insert(0, '.')

from upgraded_content_generator import UpgradedContentGenerator
import time
from datetime import datetime, timedelta
import json
import os
import random

class Upgraded30MinScheduler:
    """升级版30分钟调度器"""
    
    def __init__(self):
        self.generator = UpgradedContentGenerator()
        self.schedule_file = "upgraded_schedule.json"
        self.schedule = self._load_schedule()
        
        # 发布时段配置（UTC时间）
        self.active_hours = list(range(8, 23))  # 8:00-22:59 UTC (更长的活跃时段)
        
        # 30分钟发布槽位
        self.active_slots = [0, 30]  # 每小时的第0分钟和第30分钟
        
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
            "post_count": 0,
            "daily_stats": {},
            "content_rotation": {
                "next_viral_angle": 0,
                "last_30min_slot": None
            }
        }
    
    def _save_schedule(self):
        """保存发布计划"""
        with open(self.schedule_file, 'w') as f:
            json.dump(self.schedule, f, indent=2)
    
    def should_post_now(self) -> bool:
        """判断当前是否应该发布"""
        now = datetime.utcnow()
        current_hour = now.hour
        current_minute = now.minute
        
        # 检查是否在活跃时段
        if current_hour not in self.active_hours:
            print(f"⏰ {current_hour:02d}:{current_minute:02d} UTC is outside active hours")
            return False
        
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
            
            # 如果30分钟内已经发布过，跳过
            if time_diff < 25:  # 25分钟最小间隔
                print(f"⏰ Too soon since last post ({time_diff:.1f} minutes ago)")
                return False
        
        return True
    
    def generate_30min_tweet(self) -> str:
        """生成30分钟间隔推文"""
        now = datetime.utcnow()
        current_minute = now.minute
        
        print(f"🕐 Generating 30-minute tweet for {now.hour:02d}:{current_minute:02d} UTC")
        
        # 每4小时插入一条病毒式营销推文
        if now.hour % 4 == 0 and current_minute < 5:
            viral_angle = self.generator.viral_angles[
                self.schedule["content_rotation"]["next_viral_angle"] % len(self.generator.viral_angles)
            ]
            self.schedule["content_rotation"]["next_viral_angle"] += 1
            self._save_schedule()
            
            print(f"   Viral angle: {viral_angle}")
            tweet = self.generator.generate_viral_tweet(viral_angle)
        else:
            # 正常30分钟内容
            tweet = self.generator.generate_30min_tweet(current_minute)
        
        # 添加时间标记
        time_str = f"{now.hour:02d}:{current_minute:02d} UTC"
        tweet = tweet.replace("\n\n", f"\n\n⏰ Posted at {time_str}\n\n", 1)
        
        return self.generator._validate_length(tweet)
    
    def post_30min_tweet(self) -> bool:
        """发布30分钟推文"""
        if not self.should_post_now():
            return False
        
        now = datetime.utcnow()
        
        print(f"🚀 Preparing to post 30-minute tweet for {now.hour:02d}:{now.minute:02d} UTC...")
        
        # 生成推文
        tweet = self.generate_30min_tweet()
        print(f"📝 Tweet content:\n{tweet}\n")
        
        # 发送推文
        tweet_id = self.generator.send_tweet(tweet)
        
        if tweet_id:
            # 更新统计
            self.schedule["last_post_time"] = now.isoformat()
            self.schedule["post_count"] += 1
            
            date_key = now.date().isoformat()
            if date_key not in self.schedule["daily_stats"]:
                self.schedule["daily_stats"][date_key] = 0
            self.schedule["daily_stats"][date_key] += 1
            
            self._save_schedule()
            
            print(f"✅ 30-minute tweet posted successfully!")
            print(f"   Tweet ID: {tweet_id}")
            print(f"   Total posts today: {self.schedule['daily_stats'].get(now.date().isoformat(), 0)}")
            
            return True
        else:
            print("❌ Failed to post 30-minute tweet")
            return False
    
    def run_continuous_schedule(self, check_interval_minutes: int = 2):
        """运行连续调度（每X分钟检查一次）"""
        print("⏰ Starting upgraded 30-minute scheduler...")
        print(f"   Active hours: {self.active_hours[0]:02d}:00-{self.active_hours[-1]:02d}:59 UTC")
        print(f"   Post slots: {self.active_slots} minutes past each hour")
        print(f"   Check interval: {check_interval_minutes} minutes")
        print(f"   Max daily posts: {len(self.active_hours) * len(self.active_slots)}")
        print("-" * 50)
        
        try:
            while True:
                now = datetime.utcnow()
                current_minute = now.minute
                
                # 检查是否是发布槽位（±2分钟窗口）
                should_check = False
                for slot in self.active_slots:
                    if abs(current_minute - slot) <= 2:
                        should_check = True
                        break
                
                if should_check:
                    print(f"\n🕐 Check at {now.hour:02d}:{current_minute:02d} UTC")
                    
                    if self.post_30min_tweet():
                        # 发布成功后等待到下一个槽位
                        minutes_to_next_slot = 30 - (current_minute % 30)
                        if minutes_to_next_slot == 0:
                            minutes_to_next_slot = 30
                        
                        print(f"⏳ Waiting {minutes_to_next_slot} minutes until next slot...")
                        time.sleep(minutes_to_next_slot * 60)
                    else:
                        print(f"⏳ Not posting now. Next check in {check_interval_minutes} minutes...")
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
                    
                    status = f"⏳ Next check: {next_check.hour:02d}:{next_check.minute:02d} | Next slot: {next_slot.hour:02d}:{next_slot.minute:02d} UTC"
                    
                    # 清除行并显示状态
                    print(f"\r{status}", end="", flush=True)
                    
                    time.sleep(60)  # 每分钟更新一次显示
                    
        except KeyboardInterrupt:
            print("\n\n🛑 Scheduler stopped by user")
            self.show_stats()
    
    def show_stats(self):
        """显示统计信息"""
        print("\n📊 Upgraded Scheduler Statistics:")
        print(f"   Total posts: {self.schedule['post_count']}")
        
        last_post = self.schedule.get('last_post_time')
        if last_post:
            last_time = datetime.fromisoformat(last_post)
            print(f"   Last post: {last_time.strftime('%Y-%m-%d %H:%M UTC')}")
        else:
            print(f"   Last post: Never")
        
        if self.schedule['daily_stats']:
            print(f"   Daily posts:")
            sorted_days = sorted(self.schedule['daily_stats'].items(), reverse=True)[:7]  # 最近7天
            for date_str, count in sorted_days:
                print(f"     {date_str}: {count} posts")
    
    def simulate_day(self):
        """模拟一天的发布计划"""
        print("📅 Simulating daily 30-minute posting schedule:")
        print("-" * 50)
        
        posts_today = 0
        
        for hour in self.active_hours:
            for slot in self.active_slots:
                # 模拟时间
                simulated_time = datetime.utcnow().replace(hour=hour, minute=slot, second=0)
                
                # 临时设置当前时间
                original_should_post = self.should_post_now
                
                # 模拟检查
                self.schedule["last_post_time"] = (simulated_time - timedelta(minutes=35)).isoformat()
                
                if self.should_post_now():
                    tweet = self.generate_30min_tweet()
                    print(f"\n{hour:02d}:{slot:02d} UTC - WOULD POST:")
                    print(f"   {tweet[:80]}...")
                    
                    posts_today += 1
                    
                    # 更新为已发布
                    self.schedule["last_post_time"] = simulated_time.isoformat()
                else:
                    print(f"{hour:02d}:{slot:02d} UTC - No post")
        
        # 重置
        self.schedule["last_post_time"] = None
        
        print(f"\n✅ Daily simulation complete")
        print(f"   Total posts simulated: {posts_today}")
        print(f"   Maximum possible: {len(self.active_hours) * len(self.active_slots)}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Upgraded 30-Minute Twitter Scheduler")
    parser.add_argument('--run', action='store_true', help='Run continuous scheduler')
    parser.add_argument('--post-now', action='store_true', help='Post immediately if due')
    parser.add_argument('--simulate', action='store_true', help='Simulate daily schedule')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--test', action='store_true', help='Test tweet generation')
    parser.add_argument('--interval', type=int, default=2, help='Check interval in minutes')
    
    args = parser.parse_args()
    
    # 初始化
    scheduler = Upgraded30MinScheduler()
    
    if not scheduler.generator.twitter.user:
        print("❌ Twitter connection failed. Check credentials.")
        return
    
    print(f"✅ Connected to Twitter: @{scheduler.generator.twitter.user.username}")
    print(f"⏰ Schedule: Every 30 minutes, {scheduler.active_hours[0]:02d}:00-{scheduler.active_hours[-1]:02d}:59 UTC")
    print(f"📊 Max daily posts: {len(scheduler.active_hours) * len(scheduler.active_slots)}")
    
    if args.run:
        scheduler.run_continuous_schedule(args.interval)
    
    elif args.post_now:
        if scheduler.post_30min_tweet():
            print("✅ Posted successfully!")
        else:
            print("⏸️ Not posting now (not due or outside hours)")
    
    elif args.simulate:
        scheduler.simulate_day()
    
    elif args.stats:
        scheduler.show_stats()
    
    elif args.test:
        print("🧪 Testing 30-minute tweet generation:")
        for i in range(6):  # 测试6个时间点
            minute = i * 10  # 0, 10, 20, 30, 40, 50
            tweet = scheduler.generator.generate_30min_tweet(minute)
            print(f"\nTest {i+1} (minute {minute:02d}):")
            print(tweet[:150] + "..." if len(tweet) > 150 else tweet)
            print(f"Length: {len(tweet)}/280 characters")
            print("-" * 50)
    
    else:
        # 显示帮助
        print("Upgraded 30-Minute Scheduler for PostAlert.ai")
        print("\n🚀 UPGRADE FEATURES:")
        print("  • Every 30 minutes (not just hourly)")
        print("  • 8 content types (was 4)")
        print("  • Viral marketing angles")
        print("  • Longer active hours: 8:00-22:59 UTC")
        print("  • More hashtags and engagement")
        print("\nUsage:")
        print("  python upgraded_30min_scheduler.py --run")
        print("  python upgraded_30min_scheduler.py --post-now")
        print("  python upgraded_30min_scheduler.py --simulate")
        print("  python upgraded_30min_scheduler.py --stats")
        print("  python upgraded_30min_scheduler.py --test")

if __name__ == "__main__":
    main()