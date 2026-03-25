# 全流程运行

现在可以用一个 job 文件串起来执行：

1. normalize
2. preprocess
3. write
4. prepublish-check（可选）

运行方式：

```bash
python3 run_full_flow.py --job ./jobs/example_full_flow_job.json
```

## 输入要求

`raw_input` 目录中放原始抓取 json。

参考模板：`templates/raw_source_template.json`

## 输出结果

- `normalized_dir`：标准化 markdown 素材
- `processed_dir`：逐篇处理结果
- `bundle_output`：最终写作输入包
- `article_output`：生成好的文章
- `check_output`：发布前检查报告（如果配置）

## 适用场景

- 你已经有一批 URL 抓取结果
- 你想把采集、预处理、写稿串成固定链路
- 你准备后续挂到 OpenClaw 消息触发或定时任务上
