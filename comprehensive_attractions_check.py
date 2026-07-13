import os
import re
import sys
import html.parser

class AttractionPageAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.content = self.read_file()
        self.analysis = {
            'filepath': filepath,
            'inconsistencies': [],
            'structure': {
                'head_elements': self.check_head_elements(),
                'header_structure': self.check_header(),
                'main_sections': self.check_main_sections(),
                'homepage_link': self.check_homepage_link(),
                'metadata_elements': self.check_metadata()
            }
        }
    
    def read_file(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def check_head_elements(self):
        head_checks = {
            'charset': bool(re.search(r'<meta\s+charset="UTF-8"', self.content)),
            'viewport': bool(re.search(r'<meta\s+name="viewport"\s+content="width=device-width, initial-scale=1.0"', self.content)),
            'title_exists': bool(re.search(r'<title>.*?</title>', self.content)),
            'description_exists': bool(re.search(r'<meta\s+name="description"\s+content=".+?"', self.content)),
            'keywords_exists': bool(re.search(r'<meta\s+name="keywords"\s+content=".+?"', self.content)),
            'attractions_css': bool(re.search(r'<link\s+rel="stylesheet"\s+href="/attractions.css"', self.content))
        }
        return head_checks
    
    def check_header(self):
        header_checks = {
            'header_exists': bool(re.search(r'<header>.*?</header>', self.content, re.DOTALL)),
            'header_container': bool(re.search(r'<div\s+class="header-container">.*?</div>', self.content, re.DOTALL)),
            'h1_exists': bool(re.search(r'<h1>.*?</h1>', self.content))
        }
        return header_checks
    
    def check_main_sections(self):
        main_sections = {
            'attraction_header': bool(re.search(r'<section\s+class="attraction-header">.*?</section>', self.content, re.DOTALL)),
            'attraction_meta': bool(re.search(r'<div\s+class="attraction-meta">.*?</div>', self.content, re.DOTALL)),
            'attraction_intro': bool(re.search(r'<section\s+class="attraction-intro">.*?</section>', self.content, re.DOTALL)),
            'attraction_details': bool(re.search(r'<section\s+class="attraction-details">.*?</section>', self.content, re.DOTALL)),
            'highlight_points': bool(re.search(r'<div\s+class="highlight-points">.*?</div>', self.content, re.DOTALL))
        }
        return main_sections
    
    def check_homepage_link(self):
        homepage_link = {
            'exists': bool(re.search(r'<a\s+href="/"[^>]*class="back-to-home"[^>]*>返回首页</a>', self.content)),
            'location': None
        }
        
        if homepage_link['exists']:
            link_match = re.search(r'<a\s+href="/"[^>]*class="back-to-home"[^>]*>返回首页</a>', self.content)
            link_pos = link_match.start()
            main_end_pos = self.content.find('</main>')
            
            if main_end_pos != -1 and link_pos > main_end_pos:
                homepage_link['location'] = 'after_main'
            else:
                homepage_link['location'] = 'other'
        
        return homepage_link
    
    def check_metadata(self):
        metadata_checks = {
            'location_icon': bool(re.search(r'📍', self.content)),
            'world_heritage_icon': bool(re.search(r'🏛️', self.content))
        }
        return metadata_checks
    
    def analyze_inconsistencies(self):
        # 详细检查并记录具体缺失的内容
        def check_element_details(section_name, section_dict):
            missing_elements = [key for key, value in section_dict.items() if not value]
            if missing_elements:
                self.analysis['inconsistencies'].append(f"{section_name}缺失元素: {', '.join(missing_elements)}")
        
        # 检查 head 元素
        head_elements = self.analysis['structure']['head_elements']
        check_element_details('Head元素', head_elements)
        
        # 检查 header 结构
        header_structure = self.analysis['structure']['header_structure']
        check_element_details('Header结构', header_structure)
        
        # 检查主要区块
        main_sections = self.analysis['structure']['main_sections']
        check_element_details('主要区块', main_sections)
        
        # 检查返回首页链接
        homepage_link = self.analysis['structure']['homepage_link']
        if not homepage_link['exists']:
            self.analysis['inconsistencies'].append("缺少返回首页链接")
        elif homepage_link['location'] != 'after_main':
            self.analysis['inconsistencies'].append(f"返回首页链接位置异常: {homepage_link['location']}")
        
        # 检查元数据
        metadata = self.analysis['structure']['metadata_elements']
        check_element_details('元数据图标', metadata)
        
        return self.analysis

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
    
    all_page_analyses = []
    for page in attraction_pages:
        analyzer = AttractionPageAnalyzer(page)
        page_analysis = analyzer.analyze_inconsistencies()
        if page_analysis['inconsistencies']:
            all_page_analyses.append(page_analysis)
    
    # 输出结果
    sys.stdout.buffer.write("不一致的页面：\n".encode('utf-8'))
    for page_analysis in all_page_analyses:
        sys.stdout.buffer.write(f"\n文件：{page_analysis['filepath']}\n".encode('utf-8'))
        for inconsistency in page_analysis['inconsistencies']:
            sys.stdout.buffer.write(f"- {inconsistency}\n".encode('utf-8'))
        
        # 额外输出具体文件内容以便调试
        with open(page_analysis['filepath'], 'r', encoding='utf-8') as f:
            sys.stdout.buffer.write("\n文件内容预览：\n".encode('utf-8'))
            preview = f.read(1000)  # 读取前1000个字符
            sys.stdout.buffer.write(preview.encode('utf-8'))
            sys.stdout.buffer.write("\n".encode('utf-8'))

if __name__ == '__main__':
    main()
