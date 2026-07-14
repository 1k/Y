#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the static site from data/site.json using Jinja2 templates.

Output (all written under dist/ so the Pages artifact is self-contained):
  - dist/index.html                                 (home: city directory + featured + search)
  - dist/cities/<city>/index.html                   (city hub pages; NEW tier)
  - dist/cities/<city>/attractions/<id>/index.html  (detail pages; URL preserved)
  - dist/assets/css/main.css, dist/assets/js/main.js (copied from src/static)
"""
import json
import os
import re
import shutil
from jinja2 import Environment, FileSystemLoader

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(ROOT, "src", "templates")
STATIC = os.path.join(ROOT, "src", "static")
DIST = os.path.join(ROOT, "dist")
ASSETS = os.path.join(DIST, "assets")
DATA = os.path.join(ROOT, "data", "site.json")

# 区域分组（展示用，可按需调整）
REGION_MAP = {
    "beijing": "华北", "tianjin": "华北",
    "dalian": "东北",
    "chengdu": "西南",
    "xian": "西北",
    "shanghai": "华东", "hangzhou": "华东", "suzhou": "华东", "wuxi": "华东",
    "changzhou": "华东", "nantong": "华东", "xuzhou": "华东", "huaian": "华东",
    "lianyungang": "华东", "yangzhou": "华东", "qingdao": "华东", "jinan": "华东",
    "weifang": "华东", "zibo": "华东", "zaozhuang": "华东", "rizhao": "华东",
}

# 编辑精选：取若干城市的第一个景点（避免依赖具体景点 id）
FEATURED_CITIES = ["beijing", "xian", "chengdu", "hangzhou", "shanghai", "suzhou"]


def city_tint(index_num):
    hue = (index_num * 23) % 360
    return "hsl(%d, 46%%, 42%%)" % hue


# 将扁平的 intro 段落数组解析为带层级的小节（内容不改动 site.json 原文）
_ORD_RE = re.compile(r'^([一二三四五六七八九十]+[、.．]|[（(][一二三四五六七八九十]+[)）]|[0-9]+[.．、])')
# 标题与正文之间的分隔符：强分隔优先（： 。），弱分隔兜底（， 、 ； 空白）
_STRONG_SEP = re.compile(r'[：:。]')
_WEAK_SEP = re.compile(r'[，、；\s]')


def _strip_ordinal(text):
    return _ORD_RE.sub("", text).strip()


def parse_intro_sections(attraction):
    """返回 [{heading, toc, paras, anchor}, ...]；heading 为 None 表示开篇引言段。

    处理两种写法：
      (a) 短标题段「一、概览与地理位置」后接正文段；
      (b) 标题与正文同段「一、概览与地理位置。正文……」，按首个分隔符拆分
          （强分隔 ： 。 优先；弱分隔 ， 、 ； 空白 兜底），分隔符不计入标题。
    """
    intro = attraction.get("intro") or []
    sections = []
    cur = None
    for p in intro:
        m = _ORD_RE.match(p)
        if m:
            rest = p[m.end():]
            sm = _STRONG_SEP.search(rest) or _WEAK_SEP.search(rest)
            if sm:
                heading = p[:m.end() + sm.start()]   # 含序号+标题，不含分隔符
                body = rest[sm.end():]
            else:
                # 无分隔符：整段作标题（正文在后续段落），避免把正文截成标题
                heading, body = p, ""
            cur = {"heading": heading, "toc": _strip_ordinal(heading), "paras": []}
            sections.append(cur)
            if body:
                cur["paras"].append(body)
        else:
            if cur is None:
                cur = {"heading": None, "toc": None, "paras": []}
                sections.append(cur)
            cur["paras"].append(p)
    for i, s in enumerate(sections, 1):
        s["anchor"] = "sec-%d" % i
    return sections


def prepare(data):
    for c in data["cities"]:
        try:
            idx = int(c["index"])
        except (ValueError, TypeError):
            idx = 0
        tint = city_tint(idx)
        c["tint"] = tint
        c["region"] = REGION_MAP.get(c["id"], "其他")
        for a in c["attractions"]:
            a["tint"] = tint
            a["intro_sections"] = parse_intro_sections(a)
            if not a.get("short"):
                a["short"] = a.get("subtitle") or (a["intro"][0][:30] + "…" if a.get("intro") else "")
            if not a.get("no"):
                a["no"] = c["index"]
    return data


def build_regions(data):
    groups = {}
    order = []
    for c in data["cities"]:
        r = c["region"]
        if r not in groups:
            groups[r] = []
            order.append(r)
        groups[r].append(c)
    # 保持城市原顺序
    for r in groups:
        groups[r].sort(key=lambda x: x["index"])
    return [(r, groups[r]) for r in order]


def build_featured(data):
    out = []
    by_id = {c["id"]: c for c in data["cities"]}
    for cid in FEATURED_CITIES:
        c = by_id.get(cid)
        if not c or not c["attractions"]:
            continue
        a = c["attractions"][0]
        out.append({
            "city": c["name"],
            "name": a["display_name"],
            "url": "/cities/%s/attractions/%s/" % (c["id"], a["id"]),
            "tint": a["tint"],
        })
    return out


def build_search_index(data):
    idx = []
    for c in data["cities"]:
        idx.append({
            "t": "city", "name": c["name"],
            "sub": c["desc"], "region": c["region"],
            "url": "/cities/%s/" % c["id"],
        })
        for a in c["attractions"]:
            idx.append({
                "t": "attr", "name": a["display_name"],
                "sub": a.get("subtitle") or a.get("short", ""),
                "city": c["name"],
                "url": "/cities/%s/attractions/%s/" % (c["id"], a["id"]),
            })
    return idx


def main():
    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)
    data = prepare(data)

    regions = build_regions(data)
    featured = build_featured(data)
    search_index = build_search_index(data)

    env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=False)
    base_ctx = {
        "site": data["site"],
        "cities": data["cities"],
        "regions": regions,
        "featured": featured,
        "search_index": search_index,
    }

    # homepage
    os.makedirs(DIST, exist_ok=True)
    home_tpl = env.get_template("home.html")
    with open(os.path.join(DIST, "index.html"), "w", encoding="utf-8") as f:
        f.write(home_tpl.render(**base_ctx))
    print("wrote dist/index.html")

    # city hub pages (NEW tier)
    city_tpl = env.get_template("city.html")
    city_count = 0
    for c in data["cities"]:
        out_dir = os.path.join(DIST, "cities", c["id"])
        os.makedirs(out_dir, exist_ok=True)
        ctx = dict(base_ctx)
        ctx["city"] = c
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(city_tpl.render(**ctx))
        city_count += 1
    print("wrote %d city pages" % city_count)

    # detail pages (preserve existing URL structure)
    attr_tpl = env.get_template("attraction.html")
    count = 0
    for c in data["cities"]:
        attrs = c["attractions"]
        for i, a in enumerate(attrs):
            out_dir = os.path.join(DIST, "cities", c["id"], "attractions", a["id"])
            os.makedirs(out_dir, exist_ok=True)
            ctx = dict(base_ctx)
            ctx["city"] = c
            ctx["attraction"] = a
            ctx["prev"] = {"href": "/cities/%s/attractions/%s/" % (c["id"], attrs[i - 1]["id"]),
                           "name": attrs[i - 1]["display_name"]} if i > 0 else None
            ctx["next"] = {"href": "/cities/%s/attractions/%s/" % (c["id"], attrs[i + 1]["id"]),
                           "name": attrs[i + 1]["display_name"]} if i < len(attrs) - 1 else None
            ctx["siblings"] = [x for x in attrs if x["id"] != a["id"]]
            with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(attr_tpl.render(**ctx))
            count += 1
    print("wrote %d attraction pages" % count)

    # static assets
    if os.path.isdir(ASSETS):
        shutil.rmtree(ASSETS)
    shutil.copytree(STATIC, ASSETS)
    print("copied assets/")

    # remove legacy orphaned assets now superseded by /assets
    for legacy in ("styles.css", "attractions.css", "script.js", "responsive.css"):
        p = os.path.join(ROOT, legacy)
        if os.path.isfile(p):
            os.remove(p)
            print("removed legacy %s" % legacy)


if __name__ == "__main__":
    main()
