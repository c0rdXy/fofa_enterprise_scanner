# FOFA 企业资产扫描器

一个基于 FOFA API 的企业资产搜索工具，用于快速发现和分析企业的互联网资产。

## 功能特点

- 支持单个公司名称搜索
- 支持批量导入公司名称进行搜索
- 智能处理公司名称变体（如：技术、股份、科技等后缀）
- 自动统计和分析搜索结果
- 支持多种输出格式（控制台、TXT、Excel）
- 智能判断资产归属可能性

## 项目结构


```plaintext

fofa_enterprise_scanner/
├── config.ini          # 配置文件
├── main.py            # 主程序入口
├── company.txt        # 公司名称列表
├── requirements.txt   # 项目依赖
├── README.md         # 项目说明
└── src/              # 源代码目录
   ├── fofa_api.py   # FOFA API 接口
   ├── exporter.py   # 结果导出模块
   └── data_processor.py  # 数据处理模块

```

## 使用要求

- Python 3.6+
- FOFA 会员账号

## 快速开始

1. 克隆项目
```bash
git clone https://github.com/yourusername/fofa_enterprise_scanner.git
cd fofa_enterprise_scanner

```

2. 安装依赖
3. 配置 FOFA API
   编辑 config.ini 文件：
4. 运行程序
单个公司搜索：

```bash
python main.py -c "公司名称"
 ```

批量公司搜索：

```bash
python main.py -f company.txt
 ```

导出结果：

```bash
# 导出为TXT格式
python main.py -f company.txt -o txt

# 导出为Excel格式
python main.py -f company.txt -o excel
 ```

## 输出示例
### 控制台输出
```plaintext
==================================================
正在搜索公司 'XX科技股份有限公司' 的相关资产...
找到 50 条结果

FOFA查询语句:
(title="XX科技股份有限公司" || body="XX科技股份有限公司") && country="CN" && status_code="200"

标题总数: 15
独立IP数: 8
结果: 符合条件，可能是目标公司的资产

常见标题:
1. XX科技股份有限公司 (出现 10 次)
2. XX科技-登录系统 (出现 5 次)
...
==================================================

```

### 导出文件
- TXT文件：按公司分组，包含详细的资产信息
- Excel文件：表格形式，便于筛选和分析
## 使用建议
1. 公司名称处理
   
   - 建议使用完整的公司名称
   - 支持自动处理常见的公司名称后缀
2. 结果分析
   
   - 标题数量和IP数量是判断资产归属的重要指标
   - 建议结合人工验证最终结果
3. 使用限制
   
   - 请遵守 FOFA 的 API 使用政策
   - 建议控制查询频率，避免触发限制

## 常见问题
1. API 调用失败
   
   - 检查 API 密钥是否正确
   - 确认账号是否有足够的积分
2. 搜索结果不准确
   
   - 尝试使用更精确的公司名称
   - 调整配置文件中的判断阈值
## 版本历史
### v1.0 (2025-03-07)
- 实现基础搜索功能
- 支持批量导入公司名称
- 添加多种导出格式
- 实现智能资产判断
## 待实现功能
- 多线程支持
- 资产存活性检测
- 更多导出格式
- 自定义搜索规则
- 资产分类功能
## 贡献指南
欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证
MIT License

## 免责声明
本工具仅用于安全研究和企业资产管理，请勿用于非法用途。使用本工具所产生的一切后果由使用者自行承担。
