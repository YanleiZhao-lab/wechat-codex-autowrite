# 固定流水线

## 推荐固定套路

1. `crawl`
   - 输入主题、关键词、URL
   - 产出 raw 素材

2. `normalize`
   - 把 raw 统一成 markdown 文本
   - 保留来源、时间、URL

3. `preprocess`
   - 对每份素材做摘要、抽事实、抽观点、抽案例
   - 再汇总成 bundle

4. `write`
   - 用 bundle 驱动 Codex 生成文章
   - 再 review / format / prepublish-check

5. `human-review`
   - 人工确认

6. `publish`
   - 最后再进发布环节

## 关键原则

- 抓取和写作解耦
- 原始素材和处理结果分层存放
- prompt 输入尽量来自 bundle，而不是直接塞原始长文
- 默认保留人工确认
