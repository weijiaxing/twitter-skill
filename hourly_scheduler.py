#!/usr/bin/env python3
"""
每小时定时发布系统
每小时自动发布一条PostAlert.ai营销推文
"""

import sys
sys.path.insert(0, '.')

from postalert_content_series import PostAlertContentSeries
import time
from datetime import datetime, timedelta
import json
import os

class HourlyScheduler:
    """每小时发布调度器"""
    
    def __init__(self):
        self.series = PostAlertContentSeries()
        self.schedule_file = "hourly_schedule.json"
        self.schedule = self._load_schedule()
        
        # 发布时段配置（UTC时间）
        self.active_hours = list(range(9, 22))  # 9:00-21:59 UTC (对应不同时区的白天)
        
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
            "last_post_hour": None,
            "post_count": 0,
            "hourly_stats": {},
            "content_rotation": {
                "next_type": "feature",
                "rotation_index": 0
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
        
        # 检查是否在活跃时段
        if current_hour not in self.active_hours:
            print(f"⏰ Hour {current_hour}:00 UTC is outside active hours ({self.active_hours[0]}:00-{self.active_hours[-1]}:59)")
            return False
        
        # 检查是否已经在本小时发布过
        if self.schedule["last_post_hour"] == current_hour:
            print(f"⏰ Already posted this hour ({current_hour}:00 UTC)")
            return False
        
        # 检查最小间隔（至少55分钟）
        if self.schedule["last_post_hour"] is not None:
            last_hour = self.schedule["last_post_hour"]
            hour_diff = (current_hour - last_hour) % 24
            if hour_diff < 1 and (now.minute < 55):  # 确保至少55分钟间隔
                print(f"⏰ Too soon since last post (hour {last_hour}:00)")
                return False
        
        return True
    
    def get_next_content_type(self) -> tuple:
        """获取下一个内容类型"""
        rotation = self.schedule["content_rotation"]
        types = ["feature", "usecase", "educational", "success"]
        
        current_type = rotation["next_type"]
        current_index = rotation["rotation_index"]
        
        # 计算下一个
        next_index = (types.index(current_type) + 1) % len(types)
        next_type = types[next_index]
        
        # 更新计划
        rotation["next_type"] = next_type
        rotation["rotation_index"] = (current_index + 1) % 4
        
        self._save_schedule()
        
        return current_type, current_index
    
    def generate_hourly_tweet(self) -> str:
        """生成每小时推文"""
        content_type, content_index = self.get_next_content_type()
        now = datetime.utcnow()
        
        print(f"🕐 Generating tweet for {now.hour}:00 UTC")
        print(f"   Content type: {content_type}, Index: {content_index}")
        
        if content_type == "feature":
            tweet = self.series.generate_feature_tweet(content_index)
        elif content_type == "usecase":
            tweet = self.series.generate_usecase_tweet(content_index)
        elif content_type == "educational":
            tweet = self.series.generate_educational_tweet(content_index)
        else:  # success
            tweet = self.series.generate_success_tweet(content_index)
        
        # 添加时间标记
        tweet = tweet.replace("\n\n", f"\n\n🕐 Posted at {now.hour}:00 UTC\n\n", 1)
        
        return self.series._validate_length(tweet)
    
    def post_hourly_tweet(self) -> bool:
        """发布每小时推文"""
        if not self.should_post_now():
            return False
        
        now = datetime.utcnow()
        current_hour = now.hour
        
        print(f"🚀 Preparing to post hourly tweet for {current_hour}:00 UTC...")
        
        # 生成推文
        tweet = self.generate_hourly_tweet()
        print(f"📝 Tweet content:\n{tweet}\n")
        
        # 发送推文
        tweet_id = self.series.send_tweet(tweet)
        
        if tweet_id:
            # 更新统计
            self.schedule["last_post_hour"] = current_hour
            self.schedule["post_count"] += 1
            
            hour_key = f"{now.date()}_{current_hour}"
            if hour_key not in self.schedule["hourly_stats"]:
                self.schedule["hourly_stats"][hour_key] = 0
            self.schedule["hourly_stats"][hour_key] += 1
            
            self._save_schedule()
            
            print(f"✅ Hourly tweet posted successfully!")
            print(f"   Tweet ID: {tweet_id}")
            print(f"   Total posts today: {self.schedule['post_count']}")
            
            return True
        else:
            print("❌ Failed to post hourly tweet")
            return False
    
    def run_continuous_schedule(self, check_interval_minutes: int = 5):
        """运行连续调度（每X分钟检查一次）"""
        print("⏰ Starting continuous hourly scheduler...")
        print(f"   Active hours: {self.active_hours[0]}:00-{self.active_hours[-1]}:59 UTC")
        print(f"   Check interval: {check_interval_minutes} minutes")
        print(f"   Next check in {check_interval_minutes} minutes")
        print("-" * 50)
        
        try:
            while True:
                now = datetime.utcnow()
                
                # 只在整点附近检查（±2分钟）
                if 58 <= now.minute <= 2 or now.minute == 0:
                    print(f"\n🕐 Check at {now.hour}:{now.minute:02d} UTC")
                    
                    if self.post_hourly_tweet():
                        # 发布成功后等待到下个小时
                        wait_minutes = 60 - now.minute
                        print(f"⏳ Waiting {wait_minutes} minutes until next hour...")
                        time.sleep(wait_minutes * 60)
                    else:
                        print(f"⏳ Not posting now. Next check in {check_interval_minutes} minutes...")
                        time.sleep(check_interval_minutes * 60)
                else:
                    # 非整点时间，等待到下一个检查点
                    minutes_to_next_check = check_interval_minutes - (now.minute % check_interval_minutes)
                    if minutes_to_next_check == 0:
                        minutes_to_next_check = check_interval_minutes
                    
                    # 显示状态
                    next_check_time = now + timedelta(minutes=minutes_to_next_check)
                    status = f"⏳ Next check at {next_check_time.hour}:{next_check_time.minute:02d} UTC"
                    
                    # 清除行并显示状态
                    print(f"\r{status}", end="", flush=True)
                    
                    time.sleep(60)  # 每分钟更新一次显示
                    
        except KeyboardInterrupt:
            print("\n\n🛑 Scheduler stopped by user")
            self.show_stats()
    
    def show_stats(self):
        """显示统计信息"""
        print("\n📊 Hourly Scheduler Statistics:")
        print(f"   Total posts: {self.schedule['post_count']}")
        print(f"   Last post hour: {self.schedule.get('last_post_hour', 'Never')}:00 UTC")
        
        if self.schedule['hourly_stats']:
            print(f"   Today's posts by hour:")
            today = datetime.utcnow().date()
            for hour in self.active_hours:
                hour_key = f"{today}_{hour}"
                count = self.schedule['hourly_stats'].get(hour_key, 0)
                if count > 0:
                    print(f"     {hour}:00 UTC: {count} post{'s' if count != 1 else ''}")
    
    def simulate_day(self):
        """模拟一天的发布计划"""
        print("📅 Simulating daily posting schedule:")
        print("-" * 50)
        
        for hour in self.active_hours:
            # 临时设置当前小时
            original_method = self.should_post_now
            
            # 模拟检查
            self.schedule["last_post_hour"] = hour - 1 if hour > self.active_hours[0] else None
            
            if self.should_post_now():
                tweet = self.generate_hourly_tweet()
                print(f"\n{hour:02d}:00 UTC - WOULD POST:")
                print(f"   {tweet[:80]}...")
                
                # 更新为已发布
                self.schedule["last_post_hour"] = hour
                self.schedule["post_count"] += 1
            else:
                print(f"{hour:02d}:00 UTC - No post (outside window or too soon)")
        
        # 重置
        self.schedule["last_post_hour"] = None
        self.schedule["post_count"] = 0
        print("\n✅ Daily simulation complete")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Hourly Twitter Scheduler for PostAlert.ai")
    parser.add_argument('--run', action='store_true', help='Run continuous scheduler')
    parser.add_argument('--post-now', action='store_true', help='Post immediately if due')
    parser.add_argument('--simulate', action='store_true', help='Simulate daily schedule')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--test', action='store_true', help='Test tweet generation')
    parser.add_argument('--interval', type=int, default=5, help='Check interval in minutes')
    
    args = parser.parse_args()
    
    # 初始化
    scheduler = HourlyScheduler()
    
    if not scheduler.series.twitter.user:
        print("❌ Twitter connection failed. Check credentials.")
        return
    
    print(f"✅ Connected to Twitter: @{scheduler.series.twitter.user.username}")
    
    if args.run:
        scheduler.run_continuous_schedule(args.interval)
    
    elif args.post_now:
        if scheduler.post_hourly_tweet():
            print("✅ Posted successfully!")
        else:
            print("⏸️ Not posting now (not due or outside hours)")
    
    elif args.simulate:
        scheduler.simulate_day()
    
    elif args.stats:
        scheduler.show_stats()
    
    elif args.test:
        print("🧪 Testing hourly tweet generation:")
        for i in range(4):
            tweet = scheduler.generate_hourly_tweet()
            print(f"\nTest {i+1}:")
            print(tweet)
            print(f"Length: {len(tweet)}/280 characters")
            print("-" * 50)
            
            # 手动旋转内容类型
            scheduler.get_next_content_type()
    
    else:
        # 显示帮助
        print("Hourly Scheduler for PostAlert.ai")
        print("\nUsage:")
        print("  python hourly_scheduler.py --run          # 运行连续调度")
        print("  python hourly_scheduler.py --post-now     # 立即发布（如果到时间）")
        print("  python hourly_scheduler.py --simulate     # 模拟一天发布计划")
        print("  python hourly_scheduler.py --stats        # 显示统计")
        print("  python hourly_scheduler.py --test         # 测试推文生成")
        print("\nActive hours: 9:00-21:59 UTC (对应不同时区的白天时间)")

if __name__ == "__main__":
    main()