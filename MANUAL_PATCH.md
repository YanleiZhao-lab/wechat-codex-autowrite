# 人工补录说明

当 crawl 失败、正文缺失或提取质量很差时，可以手动补一份 raw json，再继续走后续流水线。

参考模板：`templates/manual_patch_template.json`

## 典型场景

- 微信公众号正文抓取失败
- 页面只抓到标题，正文为空
- 动态页面内容缺失
- 原文需要人工筛选摘录

## 原则

- 保留原 URL
- notes 标注 `manual_patch`
- 内容尽量写成可预处理的正文，不要只放一句摘要
