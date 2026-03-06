# Twitter技能安装指南

## 安装步骤

### 1. 安装Python依赖
```bash
pip3 install tweepy --break-system-packages
```

### 2. 设置环境变量
将你的Twitter API凭证设置为环境变量：

```bash
# 临时设置（当前会话有效）
export TWITTER_CONSUMER_KEY="你的Consumer Key"
export TWITTER_CONSUMER_SECRET="你的Consumer Secret"
export TWITTER_ACCESS_TOKEN="你的Access Token"
export TWITTER_ACCESS_TOKEN_SECRET="你的Access Token Secret"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export TWITTER_CONSUMER_KEY="你的Consumer Key"' >> ~/.bashrc
echo 'export TWITTER_CONSUMER_SECRET="你的Consumer Secret"' >> ~/.bashrc
echo 'export TWITTER_ACCESS_TOKEN="你的Access Token"' >> ~/.bashrc
echo 'export TWITTER_ACCESS_TOKEN_SECRET="你的Access Token Secret"' >> ~/.bashrc
source ~/.bashrc
```

### 3. 可选：创建凭证文件
如果你不想使用环境变量，可以创建凭证文件：

```bash
cat > ~/.twitter_credentials.json << EOF
{
  "consumer_key": "你的Consumer Key",
  "consumer_secret": "你的Consumer Secret",
  "access_token": "你的Access Token",
  "access_token_secret": "你的Access Token Secret"
}
EOF
chmod 600 ~/.twitter_credentials.json
```

## 验证安装

### 运行测试
```bash
cd /root/.openclaw/workspace/skills/twitter
python3 test_skill.py
```

### 测试命令行工具
```bash
# 发送测试推文
python3 twitter_tool.py --send "测试推文 🐦"

# 搜索推文
python3 twitter_tool.py --search "OpenClaw" --max-results 5

# 获取时间线
python3 twitter_tool.py --timeline --max-results 10
```

## 在OpenClaw中使用

### 作为技能调用
在OpenClaw会话中，你可以：
1. 直接使用Python代码调用
2. 通过命令行工具调用
3. 集成到自动化工作流中

### 示例：在OpenClaw中发推
```python
import os
import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/twitter')
from twitter_tool import TwitterTool

# 创建实例
tool = TwitterTool()

# 发送推文
tweet_id = tool.send_tweet("来自OpenClaw的推文 🦞")
print(f"推文发送成功: {tweet_id}")
```

### 示例：定时发布
结合 `qqbot-cron` 技能实现定时发布：

```json
{
  "action": "add",
  "job": {
    "name": "每日推文",
    "schedule": { "kind": "cron", "expr": "0 9 * * *", "tz": "Asia/Shanghai" },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "deleteAfterRun": false,
    "payload": {
      "kind": "agentTurn",
      "message": "请使用twitter技能发送一条推文，内容关于今日科技新闻。",
      "deliver": true,
      "channel": "qqbot",
      "to": "用户ID"
    }
  }
}
```

## 故障排除

### 常见问题

1. **认证失败**
   ```bash
   # 检查环境变量
   echo $TWITTER_CONSUMER_KEY
   echo $TWITTER_ACCESS_TOKEN
   
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
   ```

2. **权限不足**
   - 确认API访问层级为Elevated
   - 确认已购买API v2付费订阅
   - 检查账号信用额度

3. **频率限制**
   - 等待15分钟后重试
   - 减少API调用频率
   - 使用指数退避重试

### 调试命令
```bash
# 检查Python环境
python3 --version
python3 -c "import tweepy; print(f'tweepy: {tweepy.__version__}')"

# 检查技能文件
ls -la /root/.openclaw/workspace/skills/twitter/

# 运行完整测试
cd /root/.openclaw/workspace/skills/twitter
python3 test_skill.py
```

## 安全建议

1. **保护API凭证**
   - 不要硬编码在脚本中
   - 使用环境变量或加密文件
   - 定期轮换凭证

2. **监控API使用**
   - 关注API调用频率
   - 设置使用警报
   - 定期检查账单

3. **遵守Twitter政策**
   - 不要发送垃圾信息
   - 尊重用户隐私
   - 遵守开发者协议

## 更新日志

### v1.0.0 (2026-03-06)
- 初始版本发布
- 支持基本推文操作
- 包含搜索和监控功能
- 提供命令行工具