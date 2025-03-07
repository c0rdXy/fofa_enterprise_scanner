import os
import sys
import argparse
from colorama import init, Fore, Style
from src.fofa_api import FofaAPI
from src.data_processor import DataProcessor
from src.exporter import ResultExporter

def parse_args():
    parser = argparse.ArgumentParser(description='FOFA企业资产扫描器')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--company', help='单个公司名称')
    group.add_argument('-f', '--file', help='包含公司名称的文件路径')
    parser.add_argument('-o', '--output', choices=['console', 'txt', 'excel'],
                      default='console', help='输出格式 (默认: console)')
    return parser.parse_args()

def print_banner():
    banner = """
    ███████╗ ██████╗ ███████╗ █████╗     ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
    ██╔════╝██╔═══██╗██╔════╝██╔══██╗    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
    █████╗  ██║   ██║█████╗  ███████║    ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
    ██╔══╝  ██║   ██║██╔══╝  ██╔══██║    ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
    ██║     ╚██████╔╝██║     ██║  ██║    ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
    ╚═╝      ╚═════╝ ╚═╝     ╚═╝  ╚═╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
                                                                                                      
    企业资产扫描器 v1.0
    """
    print(Fore.CYAN + banner + Style.RESET_ALL)

def main():
    init()  # 初始化colorama
    args = parse_args()
    
    # 检查配置文件
    config_path = "config.ini"
    if not os.path.exists(config_path):
        print(Fore.RED + "错误: 配置文件不存在" + Style.RESET_ALL)
        return
    
    print_banner()
    
    # 初始化模块
    fofa_api = FofaAPI(config_path)
    exporter = ResultExporter("results")
    # 获取结果
    if args.company:
        print(f"\n正在搜索公司 '{args.company}' 的相关资产...")
        result = fofa_api.search_by_company(args.company)
        if result:
            results = [result]
            if args.output == 'console':
                exporter.export_single_result(results[0])
    else:
        results = fofa_api.search_companies_from_file(args.file, exporter if args.output == 'console' else None)
    
    if not results:
        return
    
    # 导出结果（仅用于txt和excel格式）
    if args.output == 'txt':
        exporter.export_to_txt(results)
    elif args.output == 'excel':
        exporter.export_to_excel(results)
    # 移除这个else分支，因为console模式的结果已经在搜索过程中显示了
    # else:
    #     exporter.export_to_console(results)

if __name__ == "__main__":
    main()