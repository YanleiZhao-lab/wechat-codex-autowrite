# 抓取适配器设计

目标：不要把所有站点都交给一个通用 HTML 去标签器，而是做成：

- 通用提取器
- 特定来源适配器

## 当前已支持

### generic
- 默认适配器
- 适用于普通 HTML 页面
- 策略：title + 基础去标签提取正文

### wechat
- 针对 `mp.weixin.qq.com`
- 优先尝试提取：
  - `og:title`
  - `#js_content`
- 失败则回退到 basic 提取

## 后续可扩展

- zhihu
- sspai
- medium
- substack
- github blog / docs

## 设计原则

1. 适配器只负责“提取标题和正文”
2. 抓取和提取分离
3. 失败要能 fallback
4. notes 要记录用了哪个 adapter
