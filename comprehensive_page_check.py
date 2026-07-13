import os
import re
import sys

def analyze_homepage_link(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 详细的分析模式
    analysis = {
        'filepath': filepath,
        'homepage_link_exists': False,
        'homepage_link_location': None,
        'footer_status': None,
        'link_details': None
    }
    
    # 查找返回首页链接
    homepage_link_match = re.search(r'<a\s+href="/"[^>]*class="back-to-home"[^>]*>返回首页</a>', content)
    if homepage_link_match:
        analysis['homepage_link_exists'] = True
        
        # 确定链接位置
        link_pos = homepage_link_match.start()
        main_end_pos = content.find('</main>')
        footer_pos = content.find('<footer>')
        
        if main_end_pos != -1 and link_pos > main_end_pos:
            analysis['homepage_link_location'] = 'after_main'
        elif footer_pos != -1 and link_pos > footer_pos and link_pos < content.find('</footer>'):
            analysis['homepage_link_location'] = 'inside_footer'
        else:
            analysis['homepage_link_location'] = 'other'
        
        analysis['link_details'] = homepage_link_match.group(0)
    
    # 检查 footer 状态
    footer_match = re.search(r'<footer>(.*?)</footer>', content, re.DOTALL)
    if footer_match:
        footer_content = footer_match.group(1).strip()
        if not footer_content:
            analysis['footer_status'] = 'empty'
        else:
            analysis['footer_status'] = 'non_empty'
    else:
        analysis['footer_status'] = 'no_footer'
    
    return analysis

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
        result = analyze_homepage_link(page)
        
        # 判断是否存在不一致情况
        is_inconsistent = False
        inconsistency_reasons = []
        
        if not result['homepage_link_exists']:
            is_inconsistent = True
            inconsistency_reasons.append("缺少返回首页链接")
        
        if result['homepage_link_location'] != 'after_main':
            is_inconsistent = True
            inconsistency_reasons.append(f"返回首页链接位置异常：{result['homepage_link_location']}")
        
        if result['footer_status'] != 'no_footer':
            is_inconsistent = True
            inconsistency_reasons.append(f"footer状态异常：{result['footer_status']}")
        
        if is_inconsistent:
            result['inconsistency_reasons'] = inconsistency_reasons
            inconsistent_pages.append(result)
    
    # 输出结果
    sys.stdout.buffer.write("不一致的页面：\n".encode('utf-8'))
    for page in inconsistent_pages:
        sys.stdout.buffer.write(f"\n文件：{page['filepath']}\n".encode('utf-8'))
        for reason in page['inconsistency_reasons']:
            sys.stdout.buffer.write(f"- {reason}\n".encode('utf-8'))

if __name__ == '__main__':
    main()
