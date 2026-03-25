# OpenClaw 接入思路（示例）

目标：让 OpenClaw 收到一条消息后，自动调用 Codex 写文章，并把结果返回。

## 入口形式

例如收到：

- 写一篇关于 AI Agent 自动化写作的文章
- 根据今天的素材整理一篇公众号草稿

## 推荐链路

1. OpenClaw 解析用户意图
2. OpenClaw 收集素材并保存到某个 refs 目录
3. OpenClaw 调用 `writer.py --mode full`
4. `writer.py` 执行：
   - generate：生成初稿
   - review：审稿压缩
   - format：格式整理
5. OpenClaw 返回最终 markdown，或者写入某个文档/待发布目录

## 建议的消息触发参数

- topic: 文章主题
- refs: 素材目录
- audience: 读者画像
- style: 风格要求
- length: 目标字数
- mode: draft / full

## 发布前建议

不要默认自动发布。

更稳妥的是：
- 先生成文章
- 人工确认一次
- 再进入发布环节
