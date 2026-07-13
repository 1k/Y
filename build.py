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
