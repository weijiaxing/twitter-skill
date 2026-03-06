# 发布到ClawHub指南

## 发布前准备

### 1. 创建GitHub仓库
```bash
# 在GitHub上创建新仓库
# 名称建议: twitter-skill 或 openclaw-twitter-skill
# 描述: Twitter Skill for OpenClaw - 推文生成和自动化发布
# 许可证: MIT
# 添加README: 是
```

### 2. 上传代码到GitHub
```bash
# 初始化本地仓库
cd twitter-publish
git init
git add .
git commit -m "初始提交: Twitter Skill v1.0.0"

# 连接到GitHub仓库
git remote add origin https://github.com/你的用户名/twitter-skill.git
git branch -M main
git push -u origin main
```

### 3. 创建GitHub Release
1. 访问仓库的Releases页面
2. 点击 "Create a new release"
3. 标签: `v1.0.0`
4. 标题: `Twitter Skill v1.0.0`
5. 描述: 包含功能列表和更新说明
6. 发布!

## 发布到ClawHub

### 方法A: 通过ClawHub网站（推荐）

1. **访问ClawHub网站**
   - 打开 https://clawhub.ai
   - 登录你的账户（如果没有，需要注册）

2. **提交技能**
   - 点击 "Submit a Skill" 或 "发布技能"
   - 填写技能信息：
     - **技能名称**: `twitter` 或 `twitter-skill`
     - **显示名称**: `Twitter Skill`
     - **描述**: `Twitter/X全能助手 — 推文生成、内容发布与管理`
     - **版本**: `1.0.0`
     - **GitHub仓库URL**: `https://github.com/你的用户名/twitter-skill`
     - **许可证**: `MIT`
     - **分类**: `Social Media` 或 `Automation`

3. **上传技能文件**
   - 上传 `clawhub.json` 文件
   - 或直接提供GitHub仓库链接

4. **等待审核**
   - ClawHub团队会审核你的技能
   - 审核通过后技能将出现在技能市场

### 方法B: 通过ClawHub CLI（如果可用）

```bash
# 安装clawhub CLI（需要Node.js >= 22）
npm install -g @clawhub/cli

# 登录
clawhub login

# 发布技能
clawhub publish --name twitter --version 1.0.0 --repo https://github.com/你的用户名/twitter-skill

# 或从本地目录发布
clawhub publish --dir ./twitter-publish
```

## 技能信息核对

### 必需信息
- [x] **技能标识符**: `twitter`
- [x] **版本号**: `1.0.0`
- [x] **描述**: 清晰说明技能功能
- [x] **作者信息**: 你的名字或组织
- [x] **许可证**: MIT
- [x] **依赖项**: Python 3.8+, tweepy>=4.0.0
- [x] **环境变量**: 列出所有必需的变量
- [x] **GitHub仓库**: 有效的公开仓库

### 推荐信息
- [x] **标签**: `twitter`, `social-media`, `automation`, `api`
- [x] **图标/表情**: 🐦
- [x] **截图/示例**: 可添加使用示例截图
- [x] **文档链接**: 指向SKILL.md和INSTALL.md
- [x] **支持信息**: 如何获取帮助

## 发布后操作

### 1. 测试安装
```bash
# 从ClawHub安装技能
clawhub install twitter

# 或使用skillhub（如果已配置）
skillhub install twitter
```

### 2. 验证功能
```bash
# 设置环境变量
export TWITTER_CONSUMER_KEY="..."
export TWITTER_CONSUMER_SECRET="..."
export TWITTER_ACCESS_TOKEN="..."
export TWITTER_ACCESS_TOKEN_SECRET="..."

# 测试技能
cd ~/.openclaw/skills/twitter
python test_skill.py
```

### 3. 更新维护
- 定期更新技能以适应API变化
- 及时修复报告的问题
- 添加新功能时更新版本号

## 推广技能

### 1. 在社区分享
- OpenClaw Discord社区
- GitHub Discussions
- 相关技术论坛

### 2. 收集反馈
- 鼓励用户评分和评论
- 收集使用反馈
- 根据需求改进功能

### 3. 版本更新
```bash
# 更新版本号
# 在_meta.json中更新版本
# 在clawhub.json中更新版本
# 创建新的GitHub Release
# 提交ClawHub更新
```

## 常见问题

### Q: 发布需要多长时间？
A: 通常1-3个工作日，取决于审核队列。

### Q: 需要付费吗？
A: ClawHub技能发布通常是免费的。

### Q: 可以发布私有技能吗？
A: 通常需要公开仓库，但可以联系ClawHub团队了解私有技能选项。

### Q: 如何更新已发布的技能？
A: 创建新版本并提交更新申请。

### Q: 技能被拒绝怎么办？
A: 根据反馈修改后重新提交。

## 联系方式

- **技能作者**: 你的名字
- **GitHub**: https://github.com/你的用户名
- **问题报告**: https://github.com/你的用户名/twitter-skill/issues
- **ClawHub**: https://clawhub.ai/skills/twitter

---

**发布成功提示**: 技能发布后，记得在OpenClaw社区分享，让更多用户知道这个有用的技能！ 🎉