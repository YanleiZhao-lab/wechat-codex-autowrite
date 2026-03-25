# 抓取失败 fallback 策略

## 目标

即使抓取失败，也不要让整条流水线断掉。

## 当前策略

### 1. URL 抓取失败
- 仍然写一个失败 raw json
- notes 里记录 `fetch_failed: ...`
- 方便后续人工补内容

### 2. 特定适配器提取失败
- 自动回退到 generic/basic 提取
- notes 中记录 `fallback=basic`

### 3. 正文为空
- 保留标题和 URL
- 后续可人工补素材

## 后续建议

- 增加 browser/manual 模式作为重试路径
- 增加“只抓标题和摘要”的降级模式
- 增加人工补录模板
