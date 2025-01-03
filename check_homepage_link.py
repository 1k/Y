import os
import re
import sys

def check_homepage_link(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查返回首页链接的不同模式
    patterns = [
        r'<footer>\s*<a href="/" class="back-to-home">返回首页</a>\s*</footer>',  # 原始模式
        r'<a href="/" class="back-to-home">返回首页</a>',  # 新模式
        r'<footer>\s*</footer>',  # 空的 footer
        r'<footer>.*?</footer>'  # 任何 footer
    ]
    
    matches = [re.search(pattern, content, re.DOTALL) for pattern in patterns]
    
    return {
        'filepath': filepath,
        'original_footer': bool(matches[0]),
        'new_style': bool(matches[1]),
        'empty_footer': bool(matches[2]),
        'any_footer': bool(matches[3])
    }

def find_attraction_pages(root_dir):
    attraction_pages = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == 'index.html' and 'attractions' in root:
                attraction_pages.append(os.path.join(root, file))
    return attraction_pages

def main():
    root_dir = 'd:/A'
    attraction_pages = find_attraction_pages(root_dir)
    
    inconsistent_pages = []
    for page in attraction_pages:
        result = check_homepage_link(page)
        
        # 判断是否不符合预期
        if result['original_footer'] or result['empty_footer'] or result['any_footer']:
            inconsistent_pages.append(result)
    
    # 使用 sys.stdout.buffer 确保正确输出
    sys.stdout.buffer.write("不一致的页面：\n".encode('utf-8'))
    for page in inconsistent_pages:
        sys.stdout.buffer.write(f"\n文件：{page['filepath']}\n".encode('utf-8'))
        if page['original_footer']:
            sys.stdout.buffer.write("- 仍使用原始的 <footer> 包裹返回首页链接\n".encode('utf-8'))
        if page['empty_footer']:
            sys.stdout.buffer.write("- 存在空的 <footer> 标签\n".encode('utf-8'))
        if page['any_footer']:
            sys.stdout.buffer.write("- 存在非空的 <footer> 标签\n".encode('utf-8'))

if __name__ == '__main__':
    main()
