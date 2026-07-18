# -*- coding: utf-8 -*-
"""
无照片版抬头重排:整个抬头改为居中,每行左右留白对称,消除照片留下的右侧空洞。
build.sh(一页版)与 build_2p.py(两页版)共用本函数,避免两处逻辑漂移。
输入 = 含或不含照片 img 的 HTML;输出 = 无照片、居中重排后的 HTML。
"""
import re


def rebalance_nophoto_header(html):
    # 1. 移除照片 img(若还在)
    html = re.sub(r'\s*<img class="photo"[^>]*>', '', html)
    # 2. 给 header 加 nh 类 → 触发居中样式
    html, n = re.subn(r'<div class="header">', '<div class="header nh">', html, count=1)
    assert n == 1, '未定位到 header'
    assert 'class="photo"' not in html
    return html
