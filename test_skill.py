#!/usr/bin/env python3
"""
测试Twitter技能 - 安全版本（不包含硬编码凭证）
"""

import os
import sys

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from twitter_tool import TwitterTool

def test_skill():
    """测试Twitter技能功能"""
    print("🧪 测试Twitter技能...")
    print("=" * 50)
    print("注意：此测试需要预先设置环境变量：")
    print("  TWITTER_CONSUMER_KEY")
    print("  TWITTER_CONSUMER_SECRET")
    print("  TWITTER_ACCESS_TOKEN")
    print("  TWITTER_ACCESS_TOKEN_SECRET")
    print("=" * 50)
    
    # 检查环境变量
    required_vars = [
        'TWITTER_CONSUMER_KEY',
        'TWITTER_CONSUMER_SECRET',
        'TWITTER_ACCESS_TOKEN',
        'TWITTER_ACCESS_TOKEN_SECRET'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ 缺少环境变量: {', '.join(missing_vars)}")
        print("请设置环境变量后再运行测试。")
        return False
    
    try:
        # 创建工具实例
        tool = TwitterTool()
        
        if not tool.user:
            print("❌ 无法初始化Twitter客户端")
            return False
        
        print(f"✅ 用户: @{tool.user.username}")
        
        # 测试1: 发送测试推文
        print("\n1. 测试发送推文...")
        test_tweet = f"🧪 Twitter技能测试\n时间: 2026-03-06\n这是技能测试推文 🐦\n#OpenClaw #测试 #技能"
        
        tweet_id = tool.send_tweet(test_tweet)
        if tweet_id:
            print(f"   ✅ 测试推文发送成功: {tweet_id}")
        else:
            print("   ❌ 测试推文发送失败")
            return False
        
        # 测试2: 获取推文详情
        print("\n2. 测试获取推文详情...")
        if tweet_id:
            info = tool.get_tweet_info(tweet_id)
            if info:
                print(f"   ✅ 推文详情获取成功")
                print(f"   内容: {info['text'][:50]}...")
            else:
                print("   ⚠️ 推文详情获取失败（可能还未索引）")
        
        # 测试3: 搜索测试
        print("\n3. 测试搜索功能...")
        tweets = tool.search_tweets("OpenClaw", max_results=3)
        if tweets:
            print(f"   ✅ 搜索成功，找到 {len(tweets)} 条推文")
        else:
            print("   ⚠️ 搜索未找到结果")
        
        # 测试4: 获取时间线
        print("\n4. 测试获取时间线...")
        timeline = tool.get_user_timeline(max_results=3)
        if timeline:
            print(f"   ✅ 时间线获取成功，最近 {len(timeline)} 条推文")
        else:
            print("   ⚠️ 时间线为空")
        
        print("\n" + "=" * 50)
        print("🎉 Twitter技能测试完成!")
        print("=" * 50)
        print("✅ 核心功能测试通过")
        print(f"📝 测试推文ID: {tweet_id}")
        print("\n技能已准备好使用!")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_skill()
    sys.exit(0 if success else 1)