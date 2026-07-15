# 安冉求职 · 项目交接文档

> 本目录包含**安冉**(AI 音乐产品 / 应用方向求职)的全部求职资产:简历(PDF/Word 八个版本)+ 求职主页(单文件 HTML,部署于 Netlify)。
> 本文档面向接手者:读完即可独立修改、构建、部署。

---

## 一、目录结构

```
job/
├── README.md                      ← 本文件
├── anran-resume-site-netlify.zip  ← 网页部署包(拖拽上传 Netlify 即可)
├── resume/                        ← 简历成品(直接投递用)
│   ├── 安冉-简历-AI音乐产品与应用.pdf / .docx            (一页 · 有照片)
│   ├── 安冉-简历-AI音乐产品与应用-无照片.pdf / .docx     (一页 · 无照片)
│   ├── 安冉-简历-AI音乐产品与应用-两页.pdf / .docx       (两页 · 有照片)
│   ├── 安冉-简历-AI音乐产品与应用-两页-无照片.pdf / .docx(两页 · 无照片)
│   └── 安冉-证件照.jpg
├── src/                           ← 简历构建源(单一内容源)
│   ├── resume_print.html          ← ★ 简历唯一内容源(改简历 = 只改这个文件)
│   ├── build.sh                   ← ★ 一键重建 8 个成品:bash build.sh
│   ├── build_2p.py                ← 两页版派生(CSS 值替换、自然分流、孤行保护)
│   ├── gen_docx.py                ← 同版式 DOCX 生成(python-docx 解析 resume_print.html)
│   ├── fix_punct.py               ← 全角标点修复器(见「关键机制」)
│   ├── photo.jpg / photo_b64.txt  ← 证件照资源
│   └── .venv/                     ← 自带 Python 环境(python-docx、Pillow、fonttools)
├── web/                           ← 求职主页源码
│   ├── index.html                 ← ★ 整站(单文件,全部 CSS/JS 内联,约 2000 行)
│   ├── build_fonts.py             ← ★ 字体子集化构建器(改中文文案后必须重跑)
│   ├── fonts/                     ← 自托管字体子集(woff2 ×7,约 900KB)
│   ├── fonts.gen.css              ← build_fonts.py 产物(@font-face,已内联进 index.html)
│   ├── audio/                     ← 六首本地 mp3(勿改名,TRACKS 数据引用)
│   ├── cover/                     ← 六张专辑封面
│   ├── img/                       ← 印章 seal.png + favicon
│   ├── anran-resume.pdf           ← 网页「下载简历」指向的 PDF(build.sh 自动同步)
│   └── moodboard.html             ← 历史风格选型页(存档,不部署)
└── netlify-deploy/                ← 部署暂存(全 ASCII 文件名)+ netlify.toml(缓存策略)
```

## 二、两条工作流

### A. 改简历(PDF / Word)
1. 编辑 `src/resume_print.html`(唯一内容源;两页版、DOCX 全部由它派生,**不要单独改某个成品**)
2. `bash src/build.sh` → 自动重建 8 个成品到 `resume/`、校验页数(应 1/1/2/2)、同步 `web/anran-resume.pdf`
3. 渲染引擎是 playwright 缓存的 chrome-headless-shell;若缺失:`npx playwright install chromium`
4. DOCX 已知边界:字号按 0.5pt 取整、苹方字体在 Windows 回退——**投递一律优先 PDF**

### B. 改网页并部署
1. 编辑 `web/index.html`
2. **改了可见中文文案** → 必须 `python3 web/build_fonts.py`(重建字体子集,否则新字符缺字形显示为方框;脚本会同时扫描 `web/plan-*.html` 方案稿,若存在)
3. 同步与打包:
   ```bash
   cp web/index.html netlify-deploy/index.html
   # 若字体重建过:rm -rf netlify-deploy/fonts && cp -R web/fonts netlify-deploy/fonts
   cd netlify-deploy && zip -r -X ../anran-resume-site-netlify.zip . -x '.*'
   ```
4. 把 zip 拖到 Netlify(Deploys 页)上传;URL 不变(anran-resume-musical.netlify.app)
5. 部署文件名**必须全 ASCII**(历史约束)

## 三、网页架构速览(index.html)

- **8 页 slides**:我是谁(两面宣言)→ 写代码的我 ×2 → 转场页 → 写歌的我 → 交汇的我 → 履历 → 终章
- **翻页引导体系**(v2 新增,三类页面形态):
  - 首页 / 转场页:居中青色仪式按钮(「开始 · 认识我的两面」/「继续 · 我的另一面」),角落控件隐藏;首页 CTA 行 = 金色下载主按钮 + 青色开始按钮 + 静态翻页提示小字
  - 内容页:右下「继续 → 下一页名」青色胶囊(右缘对齐 `--gutter`,翻页后延迟 0.28s 进场动画)+ 左下「‹ 上一页」轻文字(灰字+青箭头,自左滑入);末页只留上一页
  - 顶栏右簇:章节 tabs · 页码 │ 金色「⬇ 下载简历」胶囊(全页常显,右缘对齐内容边界)
- **三端模式**(JS `isDesktop()` = 宽≥1024 且横屏):
  - 桌面 / iPad 横屏:横向翻页(左右箭头、方向键、滚轮、触屏横滑),`body.slides`
  - iPad 竖屏 / iPhone:纵向翻页(顶部上箭头、页内可滚、抵边界续滑翻页),`body.mslides`;转场页在移动端跳过(`MOBILE_SKIP`)
  - 移动端下翻提示:**页底胶囊**「⌄ 上滑或点击 · 下一页」——`updEndCue()` 判定滑到页底(余量≤16px)才浮现,首/末页隐藏(`body.nocont` 同步收回底部余量);iPad 竖屏页面一屏放下,胶囊常显
- **高分屏自适应缩放**(`zoomFit()`):以 1440×900 为基准,z = min(2.4, min(宽/1500, 高/955));窗口高 841–899 时 z = 高/925(轻缩保比例);经 `documentElement.style.zoom` 整页等比放缩
- **音频**:单一 `#trackAudio`,六首本地 mp3;竞态用 `playGen` 令牌(播放回调先比对代号,过期即弃);曲末自动连播循环;三处播放器(首页迷你 / 舞台 / 底部常驻)状态互通;播放前强制 `muted=false`(防上次"静音进入"残留)
- **CREDITS 浮层**:挂 `document.body` 的 fixed 面板,JS 定位锚定 CREDITS 按钮,`pointer-events:none` 防悬停闪烁环

## 四、关键机制与已知坑(改代码前必读)

1. **全角标点**:AI 助手输出的全角`,;:()`会被工具链归一化为半角。写中文文案先用半角,再跑 `python3 src/fix_punct.py <文件>`(它会连 `<script>` 内注释一起转——实测安全,但**跑完必须做 JS 语法校验**)。
2. **坐标系约定(zoom 相关,最大坑源)**:
   - `innerWidth/innerHeight`、`getBoundingClientRect()`、`vw/vh/dvh` 均为**物理值,不随 zoom 缩放**(已实验证实)
   - 元素样式里的 CSS px 是**逻辑值**,渲染时 ×zoom
   - 因此:fixed 元素 JS 定位 = 物理系计算、写入样式前 ÷PZ;页面高度用 `--vhpx`(=物理高/z,JS 下发)而非 dvh;页眉页脚对齐用 `--gutter`(JS 算好下发)
   - **resize 幂等**:任何缩放逻辑改动后,必须验证"连发 3 次 resize 后系数不变"(曾因反推公式每次 resize 放大一轮,2K 上雪球到 1.8 倍导致大面积遮挡)
3. **flex 容器内含 `overflow:hidden` 的卡片必须 `flex-shrink:0`**(否则被压进一屏+自我裁切,症状是"内容只显示一半且无法滚动")
4. **垂直居中一律用 auto-margin 法**(首子 `margin-top:auto` + 末子 `margin-bottom:auto`),禁用 `justify-content:center`(内容超高时上下均裁,且溢出检测测不出来)
5. **验证方法**(无头 chrome-headless-shell,路径见 build.sh 内 HS 变量):
   - 布局:注入脚本逐页 `show(k)` 量 `scrollHeight-clientHeight`(FIT);**zoom 类问题 FIT 免疫**,必须量"元素 rect vs 播放器/视口 rect"
   - 运行时:注入 `window.onerror` 探针置于业务脚本前(纯语法校验抓不到 TDZ/运行时崩溃;本项目两次栽在 TDZ:初始化区之前的代码不得调用引用末尾 const 的函数)
   - 无头截图假象:进场动画会让内容停在透明帧(注入 `animation:none`);程序化滚动后截图会黑屏(避免)
   - 平台差异:Mac 字体度量加 `--force-device-scale-factor=2` 模拟;Windows 行高普遍更高,布局按最坏情况留 30px 级余量
6. **本地模拟高分屏**:Chrome DevTools 设备模式(Cmd/Ctrl+Shift+M)选 Responsive 填 2560×1440 / 3840×2160;或无头 `--window-size=WxH`。测完务必**拖动窗口再看一遍**(resize 幂等)。
7. 调试期可在 gate 提示行加临时 `BUILD x.y` 徽记(+console.log)以分辨用户端版本;交付版移除。

## 五、内容口径(数据均经本人确认,不得虚构)

- 求职意向:AI 音乐产品 / AI 音乐应用;杭州 / 上海;2026.12 毕业回国,2027.01 起可全职长期实习
- 教育:新南威尔士大学 信息科技·硕士(2025.02–2026.12,2027 届,QS 世界前 20);中国计量大学 信息管理与信息系统(2020.09–2024.06)
- 音乐:线上发表 **100+ 首**;艺名 X紫 / 萧冉紫(网页不展示艺名,印章图为「萧冉紫」);六首代表作角色——听闻=统筹、泽陂=策划、终焉之刻=作曲/统筹、天涯咫尺=制作人、云舒=作曲、Goose Goose Duck=作曲/统筹(完整制作名单在 TRACKS.credits)
- 核心数据:泽陂 B 站播放 35 万+、听闻网易云评论 4,100+、音乐流派分类 CCMusic 验证集 92%+(AST 最优,10+ 方案对比;FMA Top-3 86%+ / Top-1 60.9%)、手写数字识别 94%+
- 遥感项目**无量化数值**(素材未提供),只写 4 分割模型 × 4 骨干网络系统对比,**不得编造 IoU 数字**
- 联系:1378206785@qq.com / 19819509890(终章为点击复制按钮,非 mailto/tel 链接)
- 《鹅鸭杀》为非官方合作;阴阳师/鹅鸭杀为同人、泽陂为官媒合作,与商业作品(云舒/听闻)区分标注

## 六、待办

- [ ] 印章篆体矢量化(现为图片 img/seal.png;候选:崇羲篆体 / 峄山碑篆体,fonttools 子集化「萧冉紫」三字,.venv 已装 fonttools)
