import os
import re

def add_adsense_tag(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已存在 AdSense 标记
    if 'name="google-adsense-account"' in content:
        print(f"已存在 AdSense 标记: {file_path}")
        return False
    
    # 在 <head> 标签内插入 AdSense 标记
    pattern = r'(<head>)'
    replacement = r'\1\n    <meta name="google-adsense-account" content="ca-pub-4610974633549137">'
    
    new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"已添加 AdSense 标记: {file_path}")
    return True

def find_and_process_html_files(directory):
    modified_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                if add_adsense_tag(file_path):
                    modified_files.append(file_path)
    
    return modified_files

# 处理 d:/A 目录下的所有 HTML 文件
modified_files = find_and_process_html_files('d:/A')
print("\n总共修改的文件:")
for file in modified_files:
    print(file)
