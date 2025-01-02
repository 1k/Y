import os
import re

def clean_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 删除 footer-content
    content = re.sub(r'<div class="footer-content">\s*<p>.*?</p>\s*</div>', '', content, flags=re.DOTALL)
    
    # 删除 styles.css 链接
    content = re.sub(r'<link rel="stylesheet" href="styles\.css">\s*', '', content)
    
    # 删除 top-home-link
    content = re.sub(r'<a href="/" class="top-home-link">首页</a>', '', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'index.html':
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}")
                clean_html_file(file_path)

# 处理上海和北京的景点
process_directory('d:/A/cities/shanghai/attractions')
process_directory('d:/A/cities/beijing/attractions')

print("处理完成！")
