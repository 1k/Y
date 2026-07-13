import os
import re

def modify_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换 footer 中的返回首页链接
    modified_content = re.sub(
        r'<footer>\s*<a href="/" class="back-to-home">返回首页</a>\s*</footer>', 
        '<a href="/" class="back-to-home">返回首页</a>', 
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    print(f"Modified: {filepath}")

files = [
    'd:/A/cities/beijing/attractions/forbidden-city/index.html',
    'd:/A/cities/beijing/attractions/great-wall/index.html',
    'd:/A/cities/beijing/attractions/national-museum/index.html',
    'd:/A/cities/beijing/attractions/tiananmen-square/index.html',
    'd:/A/cities/shanghai/attractions/bund/index.html',
    'd:/A/cities/shanghai/attractions/city-god-temple/index.html',
    'd:/A/cities/shanghai/attractions/disneyland/index.html',
    'd:/A/cities/shanghai/attractions/east-pearl-tower/index.html',
    'd:/A/cities/shanghai/attractions/lujiazui/index.html',
    'd:/A/cities/shanghai/attractions/science-museum/index.html',
    'd:/A/cities/shanghai/attractions/shanghai-museum/index.html',
    'd:/A/cities/shanghai/attractions/wild-zoo/index.html',
    'd:/A/cities/shanghai/attractions/yu-garden/index.html'
]

for file in files:
    modify_file(file)
