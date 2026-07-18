# -*- coding: utf-8 -*-
"""
无照片版抬头:按信息逻辑分组的通栏版头,替换掉带照片的原抬头。
  版头:  安 冉                          求职意向：...(两端对齐)
  分隔线(通栏)
  行1:   到岗计划 ... · 意向城市 ...        (何时/何地能来,同组)
  行2:   电话 · 邮箱 · 年龄 · 学历          (联系与基本情况,同组)
  行3:   作品站 ... · 备用 ...              (作品入口,主备一起)
build.sh(一页)与 build_2p.py(两页)共用。输入=含照片 img 的原始 HTML(可含 __PHOTO_B64__)。
"""
import re


def rebalance_nophoto_header(html):
    # 1. 抽取各字段值
    im = re.search(r'<div class="intent">(.*?)<span class="city">(?:&nbsp;)*(.*?)</span></div>', html)
    objective = im.group(1).strip()                       # 求职意向：AI 音乐产品 / AI 音乐应用
    city = im.group(2).strip()                            # 意向城市：杭州 / 上海
    contact = re.search(r'<div class="contact">\s*(.*?)\s*</div>', html, re.S).group(1).strip()
    works = re.search(r'<div class="avail"><span class="avail-tag">作品站</span>(.*?)</div>', html).group(1).strip()
    hire = re.search(r'<div class="avail"><span class="avail-tag">到岗计划</span>(.*?)</div>', html).group(1).strip()
    # 联系行分隔符 | → ·(与版头其余行统一)
    contact = contact.replace('<span class="sep">|</span>', '<span class="sep">·</span>')
    # 意向城市拆「标签 值」
    clabel, cval = city.split('：', 1) if '：' in city else ('意向城市', city)

    new = (
        '<div class="header nh">\n'
        '    <div class="hx">\n'
        '      <div class="hx-top"><span class="name">安 冉</span>'
        '<span class="intent">' + objective + '</span></div>\n'
        '      <div class="hx-rule"></div>\n'
        '      <div class="hx-line">' + contact + '</div>\n'
        '      <div class="hx-line"><span class="avail-tag">到岗计划</span>' + hire +
        '<span class="sep">·</span><b>' + clabel + '</b> ' + cval + '</div>\n'
        '      <div class="hx-line"><span class="avail-tag">作品站</span>' + works + '</div>\n'
        '    </div>\n'
        '  </div>'
    )
    html, n = re.subn(r'<div class="header">.*?<img class="photo"[^>]*>\s*</div>',
                      new, html, count=1, flags=re.S)
    assert n == 1, '未定位到 header 块'
    assert 'class="photo"' not in html
    return html
