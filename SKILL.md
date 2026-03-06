---
name: twitter
description: Twitter/X全能助手 — 推文生成、内容发布与管理。当用户要求写推文、生成Twitter内容、发推、搜索Twitter、点赞转发等任何Twitter相关操作时使用。支持一站式从内容创作到自动发布的完整流程。
metadata: {"openclaw": {"emoji": "🐦", "requires": {"bins": ["python3"], "env": ["TWITTER_CONSUMER_KEY", "TWITTER_CONSUMER_SECRET", "TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_TOKEN_SECRET"]}}}
---

# 🐦 Twitter全能助手

两大核心能力：**内容创作**（推文生成）和 **平台操作**（发布+搜索+互动）。

内容创作默认使用当前对话的主模型，无需额外配置。

---

## 零、环境配置

### 必需的环境变量：
```bash
export TWITTER_CONSUMER_KEY="你的Consumer Key"
export TWITTER_CONSUMER_SECRET="你的Consumer Secret"
export TWITTER_ACCESS_TOKEN="你的Access Token"
export TWITTER_ACCESS_TOKEN_SECRET="你的Access Token Secret"
```

### 检查环境：
```bash
# 检查Python环境
python3 --version

# 检查tweepy库
python3 -c "import tweepy; print(f'tweepy版本: {tweepy.__version__}')"

# 检查环境变量
echo "Consumer Key: ${TWITTER_CONSUMER_KEY:0:10}..."
echo "Access Token: ${TWITTER_ACCESS_TOKEN:0:10}..."
```

---

## 一、内容创作流程

当用户要求写推文、生成Twitter内容时，按以下流程执行：

### 1.1 生成推文内容

**使用当前对话模型直接生成**，参考以下规范：

**核心要求**：
- 长度：280字符以内（Twitter限制）
- 风格：简洁、有吸引力、适合目标受众
- 标签：1-3个相关话题标签
- 表情：适当使用emoji增加互动性
- 链接：可包含相关链接（缩短后）
- 媒体：可提及图片/视频内容

**内容类型**：
1. **信息分享**：新闻、知识、技巧
2. **观点表达**：评论、看法、分析
3. **互动提问**：问题、投票、讨论
4. **推广宣传**：产品、服务、活动
5. **娱乐内容**：笑话、趣事、梗

**输出后询问用户**：是否需要修改？确认后发布。

### 1.2 生成多条推文（线程）

对于较长内容，可生成推文线程：

```python
# 示例：将长内容分割为线程
def create_thread(content, max_length=280):
    """将长内容分割为推文线程"""
    tweets = []
    # 分割逻辑...
    return tweets
```

---

## 二、平台操作流程

### 2.1 发布推文

**基本发布**：
```python
#!/usr/bin/env python3
import tweepy
import os

def send_tweet(text):
    """发送单条推文"""
    client = tweepy.Client(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token=os.environ['TWITTER_ACCESS_TOKEN'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET']
    )
    
    response = client.create_tweet(text=text)
    return response.data['id']
```

**带媒体发布**：
```python
def send_tweet_with_media(text, media_path):
    """发送带媒体的推文"""
    # 需要tweepy v1.1 API或额外处理
    pass
```

### 2.2 发布线程

```python
def send_thread(tweets):
    """发布推文线程"""
    client = tweepy.Client(...)
    
    previous_tweet_id = None
    tweet_ids = []
    
    for i, tweet_text in enumerate(tweets, 1):
        if previous_tweet_id:
            # 回复上一条推文创建线程
            response = client.create_tweet(
                text=tweet_text,
                in_reply_to_tweet_id=previous_tweet_id
            )
        else:
            # 第一条推文
            response = client.create_tweet(text=tweet_text)
        
        tweet_id = response.data['id']
        tweet_ids.append(tweet_id)
        previous_tweet_id = tweet_id
        
        print(f"第{i}条推文发布成功: {tweet_id}")
    
    return tweet_ids
```

### 2.3 互动操作

**点赞**：
```python
def like_tweet(tweet_id):
    """点赞推文"""
    client = tweepy.Client(...)
    response = client.like(tweet_id)
    return response.data['liked']
```

**转发**：
```python
def retweet(tweet_id):
    """转发推文"""
    client = tweepy.Client(...)
    response = client.retweet(tweet_id)
    return response.data['retweeted']
```

**引用推文**：
```python
def quote_tweet(tweet_id, text):
    """引用推文"""
    client = tweepy.Client(...)
    response = client.create_tweet(
        text=text,
        quote_tweet_id=tweet_id
    )
    return response.data['id']
```

### 2.4 搜索与监控

**搜索推文**：
```python
def search_tweets(query, max_results=10):
    """搜索推文"""
    client = tweepy.Client(...)
    response = client.search_recent_tweets(
        query=query,
        max_results=max_results,
        tweet_fields=["created_at", "public_metrics", "author_id"]
    )
    return response.data
```

**获取用户时间线**：
```python
def get_user_timeline(username, max_results=20):
    """获取用户时间线"""
    client = tweepy.Client(...)
    
    # 先获取用户ID
    user_response = client.get_user(username=username)
    user_id = user_response.data.id
    
    # 获取时间线
    timeline = client.get_users_tweets(
        id=user_id,
        max_results=max_results,
        tweet_fields=["created_at", "public_metrics"]
    )
    
    return timeline.data
```

---

## 三、完整工作流示例

### 3.1 自动化发推流程

```python
#!/usr/bin/env python3
"""
完整的Twitter自动化发推流程
"""

import tweepy
import os
import time
from datetime import datetime

class TwitterAutomation:
    def __init__(self):
        self.client = tweepy.Client(
            consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
            consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
            access_token=os.environ['TWITTER_ACCESS_TOKEN'],
            access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET']
        )
        
        # 获取用户信息
        user_response = self.client.get_me()
        self.user = user_response.data
        print(f"登录用户: @{self.user.username}")
    
    def generate_tweet_content(self, topic):
        """生成推文内容（实际中可调用AI模型）"""
        # 这里可以集成AI内容生成
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        templates = [
            f"关于{topic}的思考 💭\n\n时间: {current_time}\n\n#思考 #{topic} #每日分享",
            f"🚀 {topic}的最新动态！\n\n{current_time}\n\n#新闻 #{topic} #更新",
            f"分享一个{topic}的小技巧 🔧\n\n{current_time}\n\n#技巧 #{topic} #学习",
            f"大家对{topic}有什么看法？🤔\n\n{current_time}\n\n#讨论 #{topic} #互动",
            f"📊 {topic}的数据分析\n\n{current_time}\n\n#数据 #{topic} #分析"
        ]
        
        import random
        return random.choice(templates)
    
    def send_tweet(self, content):
        """发送推文"""
        print(f"准备发送推文: {content}")
        print(f"长度: {len(content)}/280 字符")
        
        try:
            response = self.client.create_tweet(text=content)
            tweet_id = response.data['id']
            
            print(f"✅ 推文发送成功!")
            print(f"推文ID: {tweet_id}")
            print(f"永久链接: https://twitter.com/{self.user.username}/status/{tweet_id}")
            
            return tweet_id
            
        except tweepy.TweepyException as e:
            print(f"❌ 发送失败: {e}")
            return None
    
    def schedule_tweet(self, content, delay_minutes=0):
        """定时发送推文"""
        if delay_minutes > 0:
            print(f"等待 {delay_minutes} 分钟后发送...")
            time.sleep(delay_minutes * 60)
        
        return self.send_tweet(content)

# 使用示例
if __name__ == "__main__":
    bot = TwitterAutomation()
    
    # 生成并发送推文
    topic = "人工智能"
    content = bot.generate_tweet_content(topic)
    bot.send_tweet(content)
```

### 3.2 定时发布系统

结合 `qqbot-cron` 技能实现定时发布：

```json
{
  "action": "add",
  "job": {
    "name": "每日推文发布",
    "schedule": { "kind": "cron", "expr": "0 9 * * *", "tz": "Asia/Shanghai" },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "deleteAfterRun": false,
    "payload": {
      "kind": "agentTurn",
      "message": "请使用twitter技能生成并发布一条关于科技趋势的推文。要求：1. 简洁有吸引力 2. 包含相关话题标签 3. 适当使用emoji 4. 长度不超过280字符",
      "deliver": true,
      "channel": "qqbot",
      "to": "用户ID"
    }
  }
}
```

---

## 四、错误处理与监控

### 4.1 常见错误处理

```python
def safe_send_tweet(content, max_retries=3):
    """安全的推文发送，包含重试机制"""
    for attempt in range(max_retries):
        try:
            return send_tweet(content)
            
        except tweepy.TooManyRequests as e:
            wait_time = 15 * 60  # 15分钟
            print(f"API限制，等待{wait_time/60}分钟后重试...")
            time.sleep(wait_time)
            
        except tweepy.TweepyException as e:
            print(f"尝试 {attempt+1}/{max_retries} 失败: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 指数退避
            else:
                raise
    
    return None
```

### 4.2 监控推文表现

```python
def monitor_tweet_performance(tweet_id, interval_minutes=60, duration_hours=24):
    """监控推文表现"""
    client = tweepy.Client(...)
    
    start_time = time.time()
    end_time = start_time + (duration_hours * 3600)
    
    while time.time() < end_time:
        try:
            tweet_response = client.get_tweet(
                tweet_id,
                tweet_fields=["public_metrics", "created_at"]
            )
            
            if tweet_response.data:
                metrics = tweet_response.data.public_metrics
                print(f"推文 {tweet_id} 表现:")
                print(f"  点赞: {metrics.get('like_count', 0)}")
                print(f"  转发: {metrics.get('retweet_count', 0)}")
                print(f"  回复: {metrics.get('reply_count', 0)}")
                print(f"  引用: {metrics.get('quote_count', 0)}")
            
            time.sleep(interval_minutes * 60)
            
        except Exception as e:
            print(f"监控错误: {e}")
            time.sleep(300)  # 5分钟后重试
```

---

## 五、最佳实践

### 5.1 内容策略
- **一致性**：保持账号定位一致
- **价值性**：提供有价值的内容
- **互动性**：鼓励用户互动
- **多样性**：混合不同类型的内容
- **时机性**：在用户活跃时间发布

### 5.2 频率控制
- 避免短时间内发布过多推文
- 根据账号类型调整发布频率
- 监控互动率调整策略

### 5.3 安全建议
1. **保护API凭证**：不要硬编码在脚本中
2. **使用环境变量**：安全存储敏感信息
3. **定期轮换凭证**：定期更新Access Token
4. **监控API使用**：避免超出限制
5. **备份重要数据**：定期备份推文和互动数据

---

## 六、快速开始

### 6.1 一键测试
```bash
# 设置环境变量后运行测试
python3 << 'EOF'
import os
import tweepy

client = tweepy.Client(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token=os.environ['TWITTER_ACCESS_TOKEN'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET']
)

response = client.create_tweet(text="Twitter Skill测试 🐦\n时间: $(date)")
print(f"测试成功! 推文ID: {response.data['id']}")
EOF
```

### 6.2 日常使用
```bash
# 生成并发布推文
python3 twitter_tool.py --generate --topic "科技" --publish

# 定时发布
python3 twitter_tool.py --schedule --time "09:00" --topic "每日新闻"

# 监控表现
python3 twitter_tool.py --monitor --tweet-id "1234567890"
```

---

## 七、故障排除

### 7.1 常见问题
1. **认证失败**：检查环境变量是否正确
2. **权限不足**：确认API访问层级和付费状态
3. **频率限制**：等待15分钟后重试
4. **网络问题**：检查网络连接和代理设置

### 7.2 调试命令
```bash
# 检查Python环境
python3 -c "import tweepy; print('tweepy:', tweepy.__version__)"

# 测试API连接
python3 -c "
import os, tweepy
client = tweepy.Client(
    consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
    consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
    access_token=os.environ.get('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
)
user = client.get_me()
print(f'用户: @{user.data.username}')
"

# 检查环境变量
env | grep TWITTER
```

---

**注意**：使用Twitter API需遵守Twitter开发者协议，合理使用API资源，避免滥用。