import os
import re

def find_files_with_pattern(directory):
    matching_files = []
    pattern = r'<footer>\s*<a href="/" class="back-to-home">返回首页</a>\s*</footer>'
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if re.search(pattern, content):
                        matching_files.append(filepath)
    
    return matching_files

files = find_files_with_pattern('d:/A')
for file in files:
    print(file)
