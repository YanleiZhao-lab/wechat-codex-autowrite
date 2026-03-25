# URL 抓取器

`crawl_urls.py` 负责把 URL 列表抓成 raw json，供后续 normalize / preprocess / write 使用。

## 输入方式

### 方式 1：纯 URL 列表

```bash
python3 crawl_urls.py \
  --input ./jobs/example_url_list.txt \
  --raw-dir ./samples/output/raw \
  --topic "AI Agent 自动写文章工作流"
```

### 方式 2：job json

```bash
python3 crawl_urls.py --input ./jobs/example_crawl_job.json
```

## 输出

每个 URL 对应一个 raw json，字段包括：
- url
- source_name
- topic
- fetched_at
- title
- content
- notes

## 当前策略

- 先用轻量 HTML 抓取
- 从 `<title>` 提取标题
- 用简单 HTML 去标签得到正文文本
- 抓取失败也会落一个失败 json，方便后续补救

## 已知限制

- 复杂站点正文抽取质量一般
- 动态渲染页面可能抓不到正文
- 微信公众号等反爬页面不一定稳定

所以它现在的定位是：**通用 URL 列表抓取骨架**，不是最终版采集器。
