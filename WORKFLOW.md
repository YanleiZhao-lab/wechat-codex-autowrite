# wechat-codex-autowrite 工作流说明

## 目标

把这个项目变成一个能被 OpenClaw 或其他自动化系统稳定调用的“文章生成模块”。

## 推荐目录规范

```text
project/
├─ jobs/
│  └─ some_job.json
├─ refs/
│  ├─ 2026-03-25-topic-a/
│  │  ├─ source-01.md
│  │  └─ source-02.md
│  └─ 2026-03-25-topic-b/
└─ output/
   └─ ...
```

## 单次任务输入

建议使用 JSON 文件描述任务，字段如下：

- `topic`: 文章主题
- `refs`: 素材目录或单个文件
- `audience`: 目标读者
- `style`: 写作风格
- `length`: 目标长度
- `mode`: `draft` 或 `full`
- `output`: 输出路径
- `save_prompt_dir`: 可选，保存调试 prompt

参考：`jobs/example_job.json`

## 运行方式

```bash
python3 run_job.py --job ./jobs/example_job.json
```

## OpenClaw 接入推荐方式

### 方式 1：消息触发

- 用户发来写作任务
- OpenClaw 将素材落到 refs 目录
- OpenClaw 生成 job.json
- OpenClaw 调用 `run_job.py`
- 完成后将输出 markdown 返回给用户

### 方式 2：定时批处理

- 每天抓取信息源
- 自动整理到 refs/日期-主题/
- 定时生成多个 job 文件
- 批量运行 `run_job.py`

## 风险控制建议

1. 默认只生成草稿，不默认自动发布
2. 发布前最好再跑一次“发布前检查”
3. 对敏感主题加人工确认
4. 长素材先做摘要，否则 prompt 可能过长
5. 输出文章最好保留来源目录，方便回溯
