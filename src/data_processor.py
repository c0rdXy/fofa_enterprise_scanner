import pandas as pd
import configparser
from collections import Counter

class DataProcessor:
    def __init__(self, config_path):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        
        self.min_title_count = self.config.getint('SETTINGS', 'min_title_count')
        self.min_ip_count = self.config.getint('SETTINGS', 'min_ip_count')
    
    def process_results(self, results, company_name):
        """
        处理FOFA搜索结果，分析标题和IP
        """
        if not results or len(results) == 0:
            print("没有找到搜索结果")
            return None
        
        # 转换为DataFrame便于处理
        columns = ['host', 'title', 'ip', 'domain', 'port', 'country', 'city']
        df = pd.DataFrame(results, columns=columns)
        
        # 统计标题出现次数
        title_counts = Counter(df['title'].str.strip())
        
        # 统计独立IP数量
        unique_ips = df['ip'].nunique()
        
        print(f"找到 {len(title_counts)} 个不同的标题")
        print(f"找到 {unique_ips} 个独立IP")
        
        # 判断是否符合条件
        meets_criteria = (len(title_counts) >= self.min_title_count and 
                          unique_ips >= self.min_ip_count)
        
        # 获取出现频率最高的标题
        common_titles = title_counts.most_common(10)
        
        result = {
            'company_name': company_name,
            'meets_criteria': meets_criteria,
            'title_count': len(title_counts),
            'ip_count': unique_ips,
            'common_titles': common_titles,
            'data': df
        }
        
        return result