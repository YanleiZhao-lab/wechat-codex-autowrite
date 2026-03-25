#!/usr/bin/env python3
import re
from urllib.parse import urlparse


def strip_html_basic(html: str):
    html = re.sub(r'(?is)<script.*?>.*?</script>', ' ', html)
    html = re.sub(r'(?is)<style.*?>.*?</style>', ' ', html)
    title_match = re.search(r'(?is)<title[^>]*>(.*?)</title>', html)
    title = re.sub(r'\s+', ' ', title_match.group(1)).strip() if title_match else ''
    text = re.sub(r'(?s)<[^>]+>', ' ', html)
    text = re.sub(r'&nbsp;?', ' ', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return title, text


def extract_wechat_article(html: str):
    title = ''
    body = ''

    m_title = re.search(r'(?is)<meta\s+property=["\']og:title["\']\s+content=["\'](.*?)["\']', html)
    if m_title:
        title = m_title.group(1).strip()
    if not title:
        m_title = re.search(r'(?is)<title[^>]*>(.*?)</title>', html)
        if m_title:
            title = re.sub(r'\s+', ' ', m_title.group(1)).strip()

    m_body = re.search(r'(?is)<div[^>]+id=["\']js_content["\'][^>]*>(.*?)</div>', html)
    if m_body:
        body_html = m_body.group(1)
        _, body = strip_html_basic(body_html)

    return title, body


def extract_generic(url: str, html: str):
    parsed = urlparse(url)
    host = parsed.netloc.lower()

    if 'mp.weixin.qq.com' in host:
        title, content = extract_wechat_article(html)
        notes = 'adapter=wechat'
        if content:
            return title, content, notes
        title2, content2 = strip_html_basic(html)
        return title or title2, content2, notes + ';fallback=basic'

    title, content = strip_html_basic(html)
    return title, content, 'adapter=generic'
