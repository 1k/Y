import os
import re

def remove_styles_link(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 删除 /styles.css 的链接
    content = re.sub(r'<link rel="stylesheet" href="/styles\.css">\s*', '', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'index.html':
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}")
                remove_styles_link(file_path)

# 处理上海和北京的景点
process_directory('d:/A/cities/shanghai/attractions')
process_directory('d:/A/cities/beijing/attractions')

print("处理完成！")
