import re

def modify_suzhou_attractions(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换拙政园的链接和描述
    pattern = r'(<div class="attraction">\s*<h3><a href=")[^"]*(">[^<]*</a></h3>\s*<p>)[^<]*'
    replacement = r'\1/cities/suzhou/attractions/zhouzheng-garden/\2世界文化遗产，园林艺术巅峰之作，展现江南园林精妙设计，体现中国传统美学与生活智慧。</p>'
    
    new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"已修改 {file_path}")

modify_suzhou_attractions('d:/A/index.html')
