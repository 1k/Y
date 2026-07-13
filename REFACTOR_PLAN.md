# 重构方案 · 梓航城市发现之旅（rzuc.com）

> 本次为**架构级重构**：在完整保留全部 21 城 / 111 个景点原始文案的前提下，
> 将原本「111 个手工编写、互相复制的 HTML 文件」体系，升级为**数据驱动的静态站点生成架构**。
> 视觉语言亦彻底重做（见下文「设计语言」），与上一版「深墨鎏金」方向完全相反。

---

## 1. 旧架构的问题

| 问题 | 说明 |
| --- | --- |
| 内容分散 | 111 个 HTML 文件各自内联标题/正文/实用信息，改一处要改 111 处 |
| 不可维护 | 新增城市/景点需复制整页 HTML，易出错、难统一 |
| 样式割裂 | 首页 `styles.css` 与详情页 `attractions.css` 两套规则，且存在无人引用的 `responsive.css` |
| 交互脆弱 | `script.js` 依赖页面里并不存在的按钮，加载即报错，拖垮其余交互 |
| 一致性差 | 部分城市（大连/南通/徐州）磁盘上有详情页但首页未收录，内容遗漏 |

## 2. 新架构总览

```
rzuc.com (仓库 1K/Y)
├── data/site.json          ← 唯一内容源（21 城 × 111 景点，结构化）
├── src/
│   ├── templates/          ← Jinja2 模板：base / home / attraction
│   └── static/             ← 设计资产：css/main.css、js/main.js
├── extract.py              ← 一次性：旧 HTML → data/site.json（提取脚本，已用完）
├── build.py                ← 核心：site.json → 全站静态文件
├── assets/                 ← 构建产物（CSS/JS），被全站引用
├── index.html              ← 构建产物（首页）
├── cities/<城>/attractions/<景点>/index.html  ← 构建产物（详情页，URL 不变）
└── .github/workflows/deploy.yml  ← 推送到 main 即自动构建并发布
```

**核心思想：内容（data/site.json）与表现（templates + static）分离。**
改文案 → 改 JSON；改视觉 → 改模板/CSS；`python build.py` 一键重生成全站。
GitHub Actions 在每次 push 时自动构建并部署，无需手动上传。

## 3. 模块说明

| 模块 | 职责 |
| --- | --- |
| `data/site.json` | 单一事实源。含站点信息、每城描述、每景点名称/副标题/正文/亮点/实用信息/SEO |
| `src/templates/base.html` | 公共骨架：字体、CSS/JS 引用、吸顶导航、城市目录浮层、页脚、返回顶部 |
| `src/templates/home.html` | 首页：Hero + 21 城分区 + 景点卡片网格（数据循环渲染） |
| `src/templates/attraction.html` | 详情页：头图 + 面包屑 + 正文 + 亮点 + 实用信息面板 |
| `src/static/css/main.css` | 全新设计系统（CSS 变量、响应式、动效） |
| `src/static/js/main.js` | 交互：吸顶阴影、目录浮层、平滑锚点、滚动入场、返回顶部（全部空值保护） |
| `build.py` | 读取 JSON → 渲染模板 → 写出首页/详情页 → 拷贝 assets → 清理旧文件 |

## 4. 技术选型与理由

| 选型 | 理由 |
| --- | --- |
| **静态站点 + 生成器**（非 SPA/框架） | 部署目标为 GitHub Pages/rzuc.com，纯静态最快、最稳、零运行时依赖；SEO 友好 |
| **Jinja2（Python）** | 模板表达力强、无前端构建链；与 Python 生态无缝，运维成本低 |
| **单 JSON 数据源** | 内容结构化后，未来可换数据库/API/CMS 前端零改动；可扩展性强 |
| **CSS 自定义属性 + 单文件** | 一套变量统一全站配色/间距；单文件避免多 CSS 互相覆盖 |
| **原生 JS（无框架）** | 交互轻量（浮层/滚动），原生即可，免打包、免依赖 |
| **保留原 URL 结构** | `cities/<城>/attractions/<景点>/` 不变，已收录的外链/搜索引擎权重不丢失 |
| **GitHub Actions 自动部署** | 内容改完 push 即上线，消除「本地改了没传」的人为风险 |

## 5. 设计语言（全新，刻意区别于上一版）

- **方向**：纸感暖白底 + 墨黑字 + 单一陶土色（clay `#B5532E`）点缀 + 细金线，留白克制。
  上一版是「深墨 + 鎏金」的暗色编辑风；本版是「画廊杂志（Gallery Journal）」的明亮气质。
- **字体**：标题 Noto Serif SC（衬线，大气）；正文 Noto Sans SC；序号/英文用 Cormorant Garamond（衬线斜体，编辑感）。
- **版式**：超大序号描边（01–21）、衬线大标题、斜体描述、卡片悬浮上浮 + 顶部色条扫入、首字下沉。
- **动效**：IntersectionObserver 滚动入场、吸顶导航毛玻璃、目录抽屉（Esc/遮罩关闭）。
- **响应式**：桌面多列网格 → 平板单列 → 移动端全宽，断点 980 / 760，并尊重 `prefers-reduced-motion`。

## 6. 内容完整性核对

- 提取并重建 **21 城 / 111 景点**，全部原始文案（正文、亮点、开放时间/门票/交通）逐字保留。
- 额外修复：大连、南通、徐州磁盘上原本存在但首页未收录的景点，现已一并纳入首页。
- 清理历史遗留：删除无人引用的 `responsive.css` 及被新架构取代的 `styles.css`/`attractions.css`/`script.js`。

## 7. 部署（GitHub Pages，目录 1K/Y）

1. `git add -A && git commit -m "refactor: data-driven static architecture + new design"`
2. `git push` → `.github/workflows/deploy.yml` 自动 `python build.py` 并发布到 Pages。
3. 自定义域名 rzuc.com 的 CNAME 维持不变。

本地预览：`python build.py && python -m http.server 8140`，访问 `http://127.0.0.1:8140/`。

## 8. 后续可扩展项

- 接入真实图片（卡片封面/详情头图），目前用渐变 + 首字水印占位。
- JSON 增加 `region`/`tags` 字段，做城市筛选/搜索。
- 详情页增加结构化数据（JSON-LD），进一步提升 SEO。
- 内容可迁移到 Headless CMS，前端模板无需改动。
