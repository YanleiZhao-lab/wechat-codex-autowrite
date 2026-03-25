# 从 URL 到文章

现在可以通过一个 job，把以下流程串起来：

1. crawl URLs
2. normalize raw json
3. preprocess normalized markdown
4. bundle writing inputs
5. write article
6. prepublish check（可选）

运行方式：

```bash
python3 run_pipeline_from_urls.py --job ./jobs/example_full_pipeline_from_urls.json
```

## 适用场景

- 你已经有一批文章链接
- 你想先抓成原始素材
- 再走统一的预处理和写作链路

## 提醒

这个版本的 crawl 还是轻量骨架：
- 对普通网页可用
- 对复杂动态网页和公众号页面不一定稳定
- 失败会落失败 json，方便人工补素材
