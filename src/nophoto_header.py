# -*- coding: utf-8 -*-
"""
无照片版抬头重排:把「到岗计划」从底部行搬到名字行右侧,填补照片原来的右上角留白。
build.sh(一页版)与 build_2p.py(两页版)共用本函数,避免两处逻辑漂移。
输入 = 已删除照片 img 的 HTML;输出 = 重排后的 HTML。找不到目标则原样返回(安全)。
"""
import re


def rebalance_nophoto_header(html):
    # 1. 提取「到岗计划」整行及其正文
    m = re.search(r'<div class="avail"><span class="avail-tag">到岗计划</span>(.*?)</div>', html)
    if not m:
        return html
    hire_full, hire_inner = m.group(0), m.group(1)
    # 2. 从底部移除该行(连同前导空白)
    html = re.sub(r'\s*' + re.escape(hire_full), '', html, count=1)
    # 3. 注入到名字行右侧(margin-left:auto 靠右)
    def inject(mm):
        return (mm.group(1)
                + '<span class="hire-inline"><span class="avail-tag">到岗计划</span>'
                + hire_inner + '</span>' + mm.group(2))
    html, n = re.subn(
        r'(<div class="name-row">\s*<span class="name">[^<]*</span>)(\s*</div>)',
        inject, html, count=1)
    assert n == 1, '未定位到 name-row,抬头重排失败'
    return html
