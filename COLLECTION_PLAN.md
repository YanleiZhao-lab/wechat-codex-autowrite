# 素材采集与预处理固定套路

目标：在正式写文章前，先完成一套稳定的前处理链路：

1. **crawl**：采集原始素材
2. **normalize**：统一格式
3. **preprocess**：摘要、去重、提取观点
4. **bundle**：形成写作输入包
5. **write**：交给 Codex 生成文章

## 推荐目录结构

```text
wechat-codex-autowrite/
├─ collected/
│  └─ 2026-03-25-topic-a/
│     ├─ raw/
│     ├─ normalized/
│     ├─ processed/
│     └─ bundle/
```

## 固定套路

### Step 1. crawl

输入：主题、关键词、URL 列表、来源清单
输出：`raw/` 原始素材

建议保存格式：
- 一个文件对应一个来源
- 文件名包含时间和来源标识
- 尽量保留原 URL

### Step 2. normalize

把采集结果统一成 Markdown 文本，结构建议：
- 标题
- 来源 URL
- 抓取时间
- 正文
- 备注

输出到：`normalized/`

### Step 3. preprocess

对 normalized 素材做三件事：
1. 摘要
2. 去重
3. 抽取结构化信息
   - 事实
   - 观点
   - 案例
   - 可用标题角度

输出到：`processed/`

### Step 4. bundle

把 processed 结果汇总成一份写作输入包：
- 主题
- 读者
- 写作角度
- 核心论点
- 可引用事实
- 风险点

输出到：`bundle/`

### Step 5. write

把 bundle 目录交给 `writer.py` 或 `run_job.py`。

## 建议原则

- 原始素材和处理后素材分开存
- 每篇文章保留来源链路，方便回溯
- 长文先压缩再生成，避免 prompt 过长
- 默认不直接发布
