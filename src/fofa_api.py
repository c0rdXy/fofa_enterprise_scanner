import requests
import base64
import json
import configparser
import os
from tqdm import tqdm

class FofaAPI:
    def __init__(self, config_path):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        
        self.email = self.config.get('FOFA', 'email')
        self.key = self.config.get('FOFA', 'key')
        self.base_url = "https://fofa.info/api/v1/search/all"
        self.max_results = self.config.getint('SETTINGS', 'max_results')
    
    def search_by_company(self, company_name):
        """
        通过公司名称在FOFA上搜索相关资产
        """
        # 移除这行打印
        # print(f"正在搜索公司 '{company_name}' 的相关资产...")
        
        # 构建更智能的查询语句，处理中国公司名称特点
        company_variants = [
            company_name,  # 完整名称，如"大华技术"
            company_name.split('技术')[0],  # 简称，如"大华"
            f"{company_name}股份",  # 股份公司形式
            f"{company_name}科技",  # 科技公司形式
            f"{company_name}有限公司"  # 有限公司形式
        ]
        
        # 移除空字符串和重复项
        company_variants = list(set(filter(None, company_variants)))
        
        # 构建查询语句
        query_parts = []
        for variant in company_variants:
            query_parts.extend([
                f'title="{variant}"',
                f'body="{variant}"'
            ])
        
        # 组合查询语句并添加国家和状态码条件
        query = f'({" || ".join(query_parts)}) && country="CN" && status_code="200"'
        
        encoded_query = base64.b64encode(query.encode()).decode()
        
        params = {
            'email': self.email,
            'key': self.key,
            'qbase64': encoded_query,
            'size': self.max_results,
            'fields': 'host,title,ip,domain,port,country_name,city'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['error']:
                print(f"API错误: {data['errmsg']}")
                return None
            
            # 移除这行打印
            # print(f"找到 {data['size']} 条结果")
            return {
                'company': company_name,
                'data': data['results'],
                'query': query,
                'total_size': data['size']  # 添加总结果数
            }
        
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
            return None
        except json.JSONDecodeError:
            print("解析响应数据失败")
            return None

    def search_companies_from_file(self, file_path, exporter=None):
        results = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                companies = [line.strip() for line in f if line.strip()]
            
            print(f"从文件中读取到 {len(companies)} 个公司名称")
            
            for company in companies:
                print(f"\n正在搜索公司 '{company}' 的相关资产...")
                result = self.search_by_company(company)
                if result:
                    if exporter:
                        exporter.export_single_result(result)
                    results.append(result)
            
            return results
            
        except FileNotFoundError:
            print(f"错误: 找不到文件 {file_path}")
            return None
        except Exception as e:
            print(f"读取文件时出错: {e}")
            return None
        
        # 在返回结果时，将查询语句也包含进去
        if results:
            return {
                'company': company_name,
                'data': results,
                'query': query  # 添加查询语句
            }
        
        return None
            