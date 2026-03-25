# crawl + normalize 固定方式

## 推荐分工

### crawl
职责：抓内容，原样落盘。

输出到 `raw/`，每个文件一个 json，建议结构：
- url
- source_name
- topic
- fetched_at
- title
- content
- notes

参考模板：`templates/raw_source_template.json`

### normalize
职责：把 raw json 统一成 markdown，方便后续 preprocess。

运行方式：

```bash
python3 normalize_sources.py \
  --input ./samples/output/raw \
  --output-dir ./samples/output/normalized
```

normalize 后的文件会统一包含：
- 来源名称
- 来源 URL
- 抓取时间
- 主题
- 正文
- 备注

## 为什么要分开

因为 crawl 层经常不稳定：
- 有的来源抓得到正文
- 有的来源只能抓标题和摘要
- 有的来源需要登录态

把 crawl 和 normalize 分开后，后面 preprocess / write 不需要关心抓取细节。
