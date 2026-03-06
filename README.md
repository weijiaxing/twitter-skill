# Twitter Skill for OpenClaw

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Twitter API v2](https://img.shields.io/badge/Twitter-API_v2-blue.svg)](https://developer.twitter.com/en/docs/twitter-api)

Twitter/X全能助手 — 推文生成、内容发布与管理。当用户要求写推文、生成Twitter内容、发推、搜索Twitter、点赞转发等任何Twitter相关操作时使用。支持一站式从内容创作到自动发布的完整流程。

## 🚀 功能特性

- ✅ **发送推文** - 支持单条推文和线程发布
- ✅ **内容搜索** - 搜索相关推文和话题
- ✅ **互动操作** - 点赞、转发、引用推文
- ✅ **时间线管理** - 获取用户时间线
- ✅ **推文监控** - 监控推文表现数据
- ✅ **错误处理** - 完整的错误处理和重试机制
- ✅ **命令行接口** - 支持各种操作的CLI工具
- ✅ **定时发布** - 可结合OpenClaw的cron技能实现定时发布

## 📦 安装

### 前提条件
1. Python 3.8+
2. Twitter API v2付费订阅
3. Twitter开发者账号和API凭证

### 安装步骤

1. **安装Python依赖**
   ```bash
   pip install tweepy>=4.0.0
   ```

2. **设置环境变量**
   ```bash
   export TWITTER_CONSUMER_KEY="你的Consumer Key"
   export TWITTER_CONSUMER_SECRET="你的Consumer Secret"
   export TWITTER_ACCESS_TOKEN="你的Access Token"
   export TWITTER_ACCESS_TOKEN_SECRET="你的Access Token Secret"
   ```

3. **下载技能文件**
   ```bash
   git clone https://github.com/your-username/twitter-skill.git
   cd twitter-skill
   ```

## 🛠️ 使用方法

### 命令行工具
```bash
# 发送单条推文
python twitter_tool.py --send "你的推文内容"

# 发送推文线程
python twitter_tool.py --thread "第一条" "第二条" "第三条"

# 搜索推文
python twitter_tool.py --search "OpenClaw" --max-results 10

# 获取用户时间线
python twitter_tool.py --timeline --max-results 20

# 点赞推文
python twitter_tool.py --tweet-id "1234567890" --like

# 转发推文
python twitter_tool.py --tweet-id "1234567890" --retweet

# 监控推文表现
python twitter_tool.py --tweet-id "1234567890" --monitor --interval 300 --duration 60
```

### Python API
```python
import os
from twitter_tool import TwitterTool

# 初始化
tool = TwitterTool()

# 发送推文
tweet_id = tool.send_tweet("Hello Twitter! 🐦")

# 搜索推文
tweets = tool.search_tweets("python programming", max_results=5)

# 获取时间线
timeline = tool.get_user_timeline(max_results=10)

# 点赞推文
tool.like_tweet("1234567890")
```

### 在OpenClaw中使用
```python
import sys
sys.path.insert(0, '/path/to/twitter-skill')
from twitter_tool import TwitterTool

# 创建实例并发送推文
tool = TwitterTool()
tweet_id = tool.send_tweet("来自OpenClaw的自动化推文 🦞")
```

## 📖 详细文档

完整的技能文档请查看 [SKILL.md](SKILL.md)，包含：
- 完整的功能说明
- API参考
- 错误处理指南
- 最佳实践
- 故障排除

安装指南请查看 [INSTALL.md](INSTALL.md)。

## 🔧 配置

### 环境变量
| 变量名 | 说明 | 必需 |
|--------|------|------|
| `TWITTER_CONSUMER_KEY` | Twitter API Consumer Key | ✅ |
| `TWITTER_CONSUMER_SECRET` | Twitter API Consumer Secret | ✅ |
| `TWITTER_ACCESS_TOKEN` | Twitter Access Token | ✅ |
| `TWITTER_ACCESS_TOKEN_SECRET` | Twitter Access Token Secret | ✅ |

### 可选配置
- 凭证文件：`~/.twitter_credentials.json`
- 自定义日志级别
- API调用频率限制

## 🧪 测试

运行测试前请确保已设置所有必需的环境变量：

```bash
# 运行完整测试
python test_skill.py

# 测试特定功能
python -c "from twitter_tool import TwitterTool; tool = TwitterTool(); print(f'用户: @{tool.user.username}')"
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开Pull Request

## 📄 许可证

本项目基于MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## ⚠️ 注意事项

1. **遵守Twitter开发者协议** - 合理使用API，避免滥用
2. **保护API凭证** - 不要硬编码在代码中
3. **监控API使用** - 关注调用频率和费用
4. **定期备份数据** - 重要数据定期备份

## 📞 支持

- 问题报告：[GitHub Issues](https://github.com/your-username/twitter-skill/issues)
- 功能请求：[GitHub Discussions](https://github.com/your-username/twitter-skill/discussions)
- 文档：[SKILL.md](SKILL.md)

---

**Twitter Skill** - 让OpenClaw成为你的Twitter自动化助手！ 🐦🦞