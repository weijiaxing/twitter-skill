#!/usr/bin/env python3
"""
Twitter工具 - 命令行接口
支持：发推、搜索、监控、定时发布等
"""

import tweepy
import os
import sys
import json
import time
import argparse
from datetime import datetime
from typing import Optional, List, Dict, Any

class TwitterTool:
    def __init__(self):
        """初始化Twitter客户端"""
        self.load_credentials()
        self.client = tweepy.Client(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret
        )
        
        # 获取用户信息
        try:
            user_response = self.client.get_me()
            self.user = user_response.data
            print(f"✅ 登录用户: @{self.user.username} ({self.user.name})")
        except Exception as e:
            print(f"❌ 获取用户信息失败: {e}")
            self.user = None
    
    def load_credentials(self):
        """加载凭证，优先使用环境变量"""
        self.consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
        self.consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
        self.access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
        
        # 如果没有环境变量，尝试从文件加载
        if not all([self.consumer_key, self.consumer_secret, self.access_token, self.access_token_secret]):
            self.load_from_file()
    
    def load_from_file(self, filepath="~/.twitter_credentials.json"):
        """从文件加载凭证"""
        try:
            import json
            path = os.path.expanduser(filepath)
            if os.path.exists(path):
                with open(path, 'r') as f:
                    creds = json.load(f)
                    self.consumer_key = creds.get('consumer_key')
                    self.consumer_secret = creds.get('consumer_secret')
                    self.access_token = creds.get('access_token')
                    self.access_token_secret = creds.get('access_token_secret')
                    print(f"✅ 从文件加载凭证: {filepath}")
        except Exception as e:
            print(f"❌ 加载凭证文件失败: {e}")
    
    def send_tweet(self, text: str, reply_to: Optional[str] = None) -> Optional[str]:
        """发送单条推文"""
        try:
            print(f"📝 发送推文: {text[:50]}...")
            print(f"   长度: {len(text)}/280 字符")
            
            if reply_to:
                response = self.client.create_tweet(
                    text=text,
                    in_reply_to_tweet_id=reply_to
                )
            else:
                response = self.client.create_tweet(text=text)
            
            if response.data:
                tweet_id = response.data['id']
                print(f"✅ 推文发送成功!")
                print(f"   推文ID: {tweet_id}")
                if self.user:
                    print(f"   永久链接: https://twitter.com/{self.user.username}/status/{tweet_id}")
                return tweet_id
            else:
                print(f"❌ 发送失败: {response}")
                return None
                
        except tweepy.TweepyException as e:
            print(f"❌ Twitter API错误: {e}")
            return None
        except Exception as e:
            print(f"❌ 未知错误: {e}")
            return None
    
    def send_thread(self, tweets: List[str]) -> List[str]:
        """发送推文线程"""
        tweet_ids = []
        previous_tweet_id = None
        
        for i, tweet_text in enumerate(tweets, 1):
            print(f"\n📝 发送线程第{i}/{len(tweets)}条...")
            
            try:
                if previous_tweet_id:
                    response = self.client.create_tweet(
                        text=tweet_text,
                        in_reply_to_tweet_id=previous_tweet_id
                    )
                else:
                    response = self.client.create_tweet(text=tweet_text)
                
                if response.data:
                    tweet_id = response.data['id']
                    tweet_ids.append(tweet_id)
                    previous_tweet_id = tweet_id
                    print(f"✅ 第{i}条发送成功: {tweet_id}")
                else:
                    print(f"❌ 第{i}条发送失败")
                    break
                    
                # 线程间短暂延迟
                if i < len(tweets):
                    time.sleep(1)
                    
            except Exception as e:
                print(f"❌ 第{i}条发送错误: {e}")
                break
        
        return tweet_ids
    
    def search_tweets(self, query: str, max_results: int = 10) -> List[Dict]:
        """搜索推文"""
        try:
            print(f"🔍 搜索: {query}")
            response = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=["created_at", "public_metrics", "author_id", "text"]
            )
            
            if response.data:
                tweets = []
                for tweet in response.data:
                    tweets.append({
                        'id': tweet.id,
                        'text': tweet.text,
                        'created_at': tweet.created_at,
                        'author_id': tweet.author_id,
                        'metrics': tweet.public_metrics
                    })
                
                print(f"✅ 找到 {len(tweets)} 条推文")
                return tweets
            else:
                print("❌ 未找到相关推文")
                return []
                
        except Exception as e:
            print(f"❌ 搜索失败: {e}")
            return []
    
    def get_tweet_info(self, tweet_id: str) -> Optional[Dict]:
        """获取推文详情"""
        try:
            response = self.client.get_tweet(
                tweet_id,
                tweet_fields=["created_at", "public_metrics", "author_id", "text", "conversation_id"],
                expansions=["author_id"]
            )
            
            if response.data:
                tweet = response.data
                info = {
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at,
                    'author_id': tweet.author_id,
                    'conversation_id': tweet.conversation_id,
                    'metrics': tweet.public_metrics
                }
                
                # 获取作者信息
                if response.includes and 'users' in response.includes:
                    author = response.includes['users'][0]
                    info['author'] = {
                        'username': author.username,
                        'name': author.name
                    }
                
                return info
            else:
                return None
                
        except Exception as e:
            print(f"❌ 获取推文详情失败: {e}")
            return None
    
    def like_tweet(self, tweet_id: str) -> bool:
        """点赞推文"""
        try:
            response = self.client.like(tweet_id)
            if response.data:
                print(f"✅ 点赞成功: {tweet_id}")
                return True
            else:
                print(f"❌ 点赞失败: {response}")
                return False
        except Exception as e:
            print(f"❌ 点赞错误: {e}")
            return False
    
    def retweet(self, tweet_id: str) -> bool:
        """转发推文"""
        try:
            response = self.client.retweet(tweet_id)
            if response.data:
                print(f"✅ 转发成功: {tweet_id}")
                return True
            else:
                print(f"❌ 转发失败: {response}")
                return False
        except Exception as e:
            print(f"❌ 转发错误: {e}")
            return False
    
    def get_user_timeline(self, username: Optional[str] = None, max_results: int = 20) -> List[Dict]:
        """获取用户时间线"""
        try:
            user_id = None
            
            if username:
                # 获取指定用户
                user_response = self.client.get_user(username=username)
                if user_response.data:
                    user_id = user_response.data.id
                    print(f"📊 获取用户 @{username} 的时间线")
                else:
                    print(f"❌ 用户 @{username} 不存在")
                    return []
            else:
                # 获取当前用户
                if self.user:
                    user_id = self.user.id
                    username = self.user.username
                    print(f"📊 获取当前用户 @{username} 的时间线")
                else:
                    print("❌ 无法获取用户信息")
                    return []
            
            # 获取时间线
            response = self.client.get_users_tweets(
                id=user_id,
                max_results=max_results,
                tweet_fields=["created_at", "public_metrics", "text"]
            )
            
            if response.data:
                tweets = []
                for tweet in response.data:
                    tweets.append({
                        'id': tweet.id,
                        'text': tweet.text,
                        'created_at': tweet.created_at,
                        'metrics': tweet.public_metrics
                    })
                
                print(f"✅ 获取到 {len(tweets)} 条推文")
                return tweets
            else:
                print("❌ 时间线为空")
                return []
                
        except Exception as e:
            print(f"❌ 获取时间线失败: {e}")
            return []
    
    def monitor_tweet(self, tweet_id: str, interval_seconds: int = 300, duration_minutes: int = 60):
        """监控推文表现"""
        print(f"📊 开始监控推文: {tweet_id}")
        print(f"   间隔: {interval_seconds}秒, 时长: {duration_minutes}分钟")
        
        end_time = time.time() + (duration_minutes * 60)
        check_count = 0
        
        while time.time() < end_time:
            check_count += 1
            print(f"\n📈 第{check_count}次检查 ({datetime.now().strftime('%H:%M:%S')})")
            
            info = self.get_tweet_info(tweet_id)
            if info:
                metrics = info.get('metrics', {})
                print(f"   点赞: {metrics.get('like_count', 0)}")
                print(f"   转发: {metrics.get('retweet_count', 0)}")
                print(f"   回复: {metrics.get('reply_count', 0)}")
                print(f"   引用: {metrics.get('quote_count', 0)}")
                print(f"   展示: {metrics.get('impression_count', 'N/A')}")
            else:
                print("   无法获取推文信息")
            
            # 等待下一次检查
            if time.time() + interval_seconds < end_time:
                time.sleep(interval_seconds)
            else:
                break
        
        print(f"\n✅ 监控完成，共检查 {check_count} 次")

def main():
    parser = argparse.ArgumentParser(description="Twitter工具 - 命令行接口")
    parser.add_argument('--send', type=str, help='发送单条推文')
    parser.add_argument('--thread', type=str, nargs='+', help='发送推文线程（多条内容）')
    parser.add_argument('--search', type=str, help='搜索推文')
    parser.add_argument('--max-results', type=int, default=10, help='搜索结果数量')
    parser.add_argument('--tweet-id', type=str, help='推文ID（用于点赞、转发、监控等）')
    parser.add_argument('--like', action='store_true', help='点赞推文')
    parser.add_argument('--retweet', action='store_true', help='转发推文')
    parser.add_argument('--info', action='store_true', help='获取推文详情')
    parser.add_argument('--timeline', type=str, nargs='?', const='', help='获取用户时间线（不指定用户则获取当前用户）')
    parser.add_argument('--monitor', action='store_true', help='监控推文表现')
    parser.add_argument('--interval', type=int, default=300, help='监控间隔（秒）')
    parser.add_argument('--duration', type=int, default=60, help='监控时长（分钟）')
    parser.add_argument('--json', action='store_true', help='输出JSON格式')
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    tool = TwitterTool()
    
    # 检查凭证
    if not all([tool.consumer_key, tool.consumer_secret, tool.access_token, tool.access_token_secret]):
        print("❌ 缺少Twitter API凭证")
        print("请设置以下环境变量：")
        print("  TWITTER_CONSUMER_KEY")
        print("  TWITTER_CONSUMER_SECRET")
        print("  TWITTER_ACCESS_TOKEN")
        print("  TWITTER_ACCESS_TOKEN_SECRET")
        return
    
    # 执行对应操作
    if args.send:
        tweet_id = tool.send_tweet(args.send)
        if args.json and tweet_id:
            print(json.dumps({'tweet_id': tweet_id}, indent=2))
    
    elif args.thread:
        tweet_ids = tool.send_thread(args.thread)
        if args.json and tweet_ids:
            print(json.dumps({'tweet_ids': tweet_ids}, indent=2))
    
    elif args.search:
        tweets = tool.search_tweets(args.search, args.max_results)
        if args.json:
            print(json.dumps(tweets, indent=2, default=str))
        else:
            for i, tweet in enumerate(tweets, 1):
                print(f"\n{i}. {tweet['text'][:100]}...")
                print(f"   ID: {tweet['id']} | 时间: {tweet['created_at']}")
                print(f"   点赞: {tweet['metrics'].get('like_count', 0)} | 转发: {tweet['metrics'].get('retweet_count', 0)}")
    
    elif args.tweet_id:
        if args.like:
            tool.like_tweet(args.tweet_id)
        elif args.retweet:
            tool.retweet(args.tweet_id)
        elif args.info:
            info = tool.get_tweet_info(args.tweet_id)
            if args.json:
                print(json.dumps(info, indent=2, default=str))
            elif info:
                print(f"\n推文详情:")
                print(f"  ID: {info['id']}")
                print(f"  内容: {info['text']}")
                print(f"  时间: {info['created_at']}")
                if 'author' in info:
                    print(f"  作者: @{info['author']['username']} ({info['author']['name']})")
                metrics = info['metrics']
                print(f"  数据: 👍{metrics.get('like_count', 0)} 🔄{metrics.get('retweet_count', 0)} 💬{metrics.get('reply_count', 0)}")
        elif args.monitor:
            tool.monitor_tweet(args.tweet_id, args.interval, args.duration)
        else:
            print("❌ 请指定操作：--like, --retweet, --info, 或 --monitor")
    
    elif args.timeline is not None:
        username = args.timeline if args.timeline else None
        tweets = tool.get_user_timeline(username, args.max_results)
        if args.json:
            print(json.dumps(tweets, indent=2, default=str))
        else:
            for i, tweet in enumerate(tweets, 1):
                print(f"\n{i}. {tweet['text'][:100]}...")
                print(f"   ID: {tweet['id']} | 时间: {tweet['created_at']}")
                print(f"   点赞: {tweet['metrics'].get('like_count', 0)} | 转发: {tweet['metrics'].get('retweet_count', 0)}")

if __name__ == "__main__":
    main()