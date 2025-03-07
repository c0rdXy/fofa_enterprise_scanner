import os
import pandas as pd
from datetime import datetime
from colorama import Fore, Style

class ResultExporter:
    def __init__(self, output_dir="results"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def export_to_console(self, results):
        """输出结果到控制台"""
        for company_result in results:
            company = company_result['company']
            data = company_result['data']
            query = company_result.get('query', '未获取到查询语句')
            total_size = company_result.get('total_size', len(data))
            
            print("\n" + "="*50)
            print(f"正在搜索公司 '{company}' 的相关资产...")
            print(f"找到 {total_size} 条结果")
            
            # 显示FOFA查询语句
            print(Fore.CYAN + "\nFOFA查询语句:" + Style.RESET_ALL)
            print(query)
            print("-"*50)
            
            print(f"找到 {len(data)} 条结果")
            
            # 统计标题和IP
            titles = set(item[1] for item in data)
            ips = set(item[2] for item in data)
            
            print(f"标题总数: {len(titles)}")
            print(f"独立IP数: {len(ips)}")
            
            # 判断是否符合条件
            meets_criteria = (len(titles) >= 5 and len(ips) >= 3)
            if meets_criteria:
                print(Fore.GREEN + "结果: 符合条件，可能是目标公司的资产" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + "结果: 不符合条件，可能不是目标公司的资产" + Style.RESET_ALL)
            
            # 显示常见标题
            print("\n常见标题:")
            from collections import Counter
            title_counts = Counter(item[1] for item in data)
            for i, (title, count) in enumerate(title_counts.most_common(10), 1):
                print(f"{i}. {title} (出现 {count} 次)")
            
            print("\n" + "="*50)  # 结果分隔符
    
    def export_to_txt(self, results):
        """导出结果到TXT文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"fofa_results_{timestamp}.txt")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")  # 开始分隔符
            
            for company_result in results:
                company = company_result['company']
                data = company_result['data']
                
                f.write(f"\n公司名称: {company}\n")
                f.write(f"找到 {len(data)} 条结果\n")
                f.write("-"*50 + "\n")
                
                for item in data:
                    f.write(f"标题: {item[1]}\n")
                    f.write(f"地址: {item[0]}\n")
                    f.write(f"IP: {item[2]}\n")
                    f.write(f"域名: {item[3]}\n")
                    f.write(f"位置: {item[5]}, {item[6]}\n")
                    f.write("-"*30 + "\n")
                
                f.write("\n" + "="*80 + "\n")  # 公司之间的分隔符
        
        print(f"\n结果已保存到: {filename}")
    
    def export_to_excel(self, results):
        """导出结果到Excel文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"fofa_results_{timestamp}.xlsx")
        
        all_data = []
        for company_result in results:
            company = company_result['company']
            for item in company_result['data']:
                all_data.append({
                    '公司名称': company,
                    '网站标题': item[1],
                    '地址': item[0],
                    'IP': item[2],
                    '域名': item[3],
                    '端口': item[4],
                    '国家': item[5],
                    '城市': item[6]
                })
        
        df = pd.DataFrame(all_data)
        df.to_excel(filename, index=False)
        print(f"\n结果已保存到: {filename}")
    def export_single_result(self, company_result):
        """
        立即输出单个公司的搜索结果
        """
        company = company_result['company']
        data = company_result['data']
        query = company_result.get('query', '未获取到查询语句')
        total_size = company_result.get('total_size', len(data))
        
        print("\n" + "="*50)
        # 移除这行，因为已经在搜索前显示了
        # print(f"正在搜索公司 '{company}' 的相关资产...")
        print(f"找到 {total_size} 条结果")
        
        # 显示FOFA查询语句
        print(Fore.CYAN + "\nFOFA查询语句:" + Style.RESET_ALL)
        print(query)
        print("-"*50)
        
        # 统计标题和IP
        titles = set(item[1] for item in data)
        ips = set(item[2] for item in data)
        
        print(f"标题总数: {len(titles)}")
        print(f"独立IP数: {len(ips)}")
        
        # 判断是否符合条件
        meets_criteria = (len(titles) >= 5 and len(ips) >= 3)
        if meets_criteria:
            print(Fore.GREEN + "结果: 符合条件，可能是目标公司的资产" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "结果: 不符合条件，可能不是目标公司的资产" + Style.RESET_ALL)
        
        # 显示常见标题
        print("\n常见标题:")
        from collections import Counter
        title_counts = Counter(item[1] for item in data)
        for i, (title, count) in enumerate(title_counts.most_common(10), 1):
            print(f"{i}. {title} (出现 {count} 次)")
        
        print("\n" + "="*50)  # 结果分隔符