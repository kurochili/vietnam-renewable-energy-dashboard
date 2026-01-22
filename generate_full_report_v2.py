# -*- coding: utf-8 -*-
"""
越南可再生能源厂商综合报告生成器 - 完整版V2
- 下载Logo
- 显示全部项目
- 字母索引导航
- 公司官网链接
- 搜索功能
- 自动更新时间显示
"""

import pandas as pd
import os
import requests
import json
import base64
from io import BytesIO
from datetime import datetime

# 创建logos文件夹
os.makedirs('logos', exist_ok=True)

# ==================== 完整的公司数据（包含官网） ====================

# ==================== 中国EPC子模块 ====================
# 中国电建（PowerChina）子公司
powerchina_subsidiaries = [
    {
        "name": "PowerChina Huadong (HDEC/华东院)",
        "parent": "中国电建",
        "logo_url": "https://www.hdec.com/images/logo.png",
        "website": "https://www.hdec.com",
        "country": "China",
        "address": "Hangzhou, China / Vietnam Office",
        "employees": "10,000+",
        "description": "华东勘测设计研究院，中国电建核心子公司",
        "remarks": "Monsoon 600MW Laos, Ca Mau offshore wind, multiple Vietnam offshore projects",
        "projects": [
            {"name": "Monsoon Wind Farm", "location": "Laos", "capacity": "600MW", "status": "Completed"},
            {"name": "Ca Mau 1 Offshore Wind", "location": "Ca Mau, Vietnam", "capacity": "350MW", "status": "Under Construction"},
            {"name": "Tra Vinh II Offshore", "location": "Tra Vinh, Vietnam", "capacity": "54MW", "status": "Completed"},
            {"name": "Soc Trang Offshore Wind", "location": "Soc Trang, Vietnam", "capacity": "100MW", "status": "Completed"},
            {"name": "Bac Lieu Offshore Wind", "location": "Bac Lieu, Vietnam", "capacity": "71MW", "status": "Completed"},
            {"name": "Binh Dai Offshore Wind", "location": "Ben Tre, Vietnam", "capacity": "310MW", "status": "Completed"},
        ]
    },
    {
        "name": "PowerChina Zhongnan (中南院)",
        "parent": "中国电建",
        "logo_url": "",
        "website": "https://www.cspdri.com",
        "country": "China",
        "address": "Changsha, China",
        "employees": "6,000+",
        "description": "中南勘测设计研究院有限公司",
        "remarks": "与春桥合作越南风电项目，专注水电和新能源设计",
        "partner_projects": ["Spring Bridge Vietnam Wind (with 春桥)"],
        "projects": [
            {"name": "春桥越南风电项目", "location": "Vietnam", "capacity": "50MW", "status": "Under Construction", "partner": "春桥集团"},
            {"name": "Xiang Ling 3 Wind", "location": "Vietnam", "capacity": "30MW", "status": "Completed"},
            {"name": "Xiang Ling 4 Wind", "location": "Vietnam", "capacity": "30MW", "status": "Completed"},
        ]
    },
    {
        "name": "PowerChina Nuclear (核工院)",
        "parent": "中国电建",
        "logo_url": "",
        "website": "https://www.bine.com.cn",
        "country": "China",
        "address": "Beijing, China",
        "employees": "3,000+",
        "description": "北京国核工程有限公司",
        "remarks": "核电与新能源工程设计",
        "projects": []
    },
    {
        "name": "PowerChina Jiangxi (江西院)",
        "parent": "中国电建",
        "logo_url": "",
        "website": "https://www.jxsdi.com.cn",
        "country": "China",
        "address": "Nanchang, China",
        "employees": "2,500+",
        "description": "江西省勘察设计研究院",
        "remarks": "与WTO合作越南风电项目",
        "partner_projects": ["Vietnam Wind Project (with WTO)"],
        "projects": [
            {"name": "WTO合作越南风电", "location": "Vietnam", "capacity": "48MW", "status": "Awarded", "partner": "WTO"},
        ]
    },
    {
        "name": "PowerChina Chengdu (成都院)",
        "parent": "中国电建",
        "logo_url": "",
        "website": "https://www.chidi.com.cn",
        "country": "China",
        "address": "Chengdu, China",
        "employees": "4,000+",
        "description": "成都勘测设计研究院",
        "remarks": "水电与风电设计专家",
        "projects": []
    },
    {
        "name": "PowerChina Guiyang (贵阳院)",
        "parent": "中国电建",
        "logo_url": "",
        "website": "https://www.gyedi.com.cn",
        "country": "China",
        "address": "Guiyang, China",
        "employees": "3,000+",
        "description": "贵阳勘测设计研究院",
        "remarks": "越南BIM2光伏项目EPC",
        "projects": [
            {"name": "BIM2 Solar 18NX", "location": "Ninh Thuan, Vietnam", "capacity": "75MW", "status": "Completed"},
        ]
    },
]

# 中国能建（CEEC）子公司
ceec_subsidiaries = [
    {
        "name": "CEEC GEDI (广东院)",
        "parent": "中国能建",
        "logo_url": "https://en.ceec.net.cn/images/logo.png",
        "website": "https://www.gedi.com.cn",
        "country": "China",
        "address": "Guangzhou, China",
        "employees": "5,000+",
        "description": "广东省电力设计研究院",
        "remarks": "Vietnam Hung Hai 100MW, Philippines Alabat+Tanay 163MW wind projects",
        "projects": [
            {"name": "Hung Hai 100MW Wind", "location": "Gia Lai, Vietnam", "capacity": "100MW", "status": "Completed"},
            {"name": "Gia Lai 150MW Wind", "location": "Gia Lai, Vietnam", "capacity": "150MW", "status": "Completed"},
            {"name": "Ninh Thuan 117MW Wind", "location": "Ninh Thuan, Vietnam", "capacity": "117MW", "status": "Completed"},
            {"name": "V1-3 Phase 2 Wind Cluster", "location": "Vinh Long, Vietnam", "capacity": "128MW", "status": "Awarded"},
            {"name": "Alabat + Tanay Wind", "location": "Philippines", "capacity": "163MW", "status": "Under Construction"},
        ]
    },
    {
        "name": "CEEC Southwest (西南院)",
        "parent": "中国能建",
        "logo_url": "",
        "website": "https://www.swepdi.com",
        "country": "China",
        "address": "Chengdu, China",
        "employees": "3,500+",
        "description": "西南电力设计院",
        "remarks": "专注水电与新能源EPC",
        "projects": [
            {"name": "Southeast Asia Wind Project", "location": "Vietnam/Laos", "capacity": "100MW", "status": "Awarded"},
        ]
    },
    {
        "name": "CEEC Yunnan (云南院)",
        "parent": "中国能建",
        "logo_url": "",
        "website": "https://www.ynpdi.com",
        "country": "China",
        "address": "Kunming, China",
        "employees": "2,000+",
        "description": "云南省电力设计院",
        "remarks": "东南亚市场拓展中，越南老挝项目",
        "projects": [
            {"name": "Laos Border Wind Project", "location": "Laos", "capacity": "50MW", "status": "Under Construction"},
        ]
    },
    {
        "name": "CEEC Shanxi (山西院)",
        "parent": "中国能建",
        "logo_url": "",
        "website": "https://www.sxpdi.com.cn",
        "country": "China",
        "address": "Taiyuan, China",
        "employees": "2,500+",
        "description": "山西省电力勘测设计院",
        "remarks": "风电与光伏设计，富安华会项目",
        "projects": [
            {"name": "Phu An Hoa Hoi Solar", "location": "Phu Yen, Vietnam", "capacity": "257MW", "status": "Completed"},
        ]
    },
    {
        "name": "CEEC East China (华东院)",
        "parent": "中国能建",
        "logo_url": "",
        "website": "https://www.ecepdi.com",
        "country": "China",
        "address": "Shanghai, China",
        "employees": "4,000+",
        "description": "华东电力设计院",
        "remarks": "海上风电设计领先",
        "projects": [
            {"name": "Vietnam Offshore Wind Study", "location": "Vietnam", "capacity": "500MW", "status": "Planning"},
        ]
    },
    {
        "name": "CEEC Gezhouba (葛洲坝)",
        "parent": "中国能建",
        "logo_url": "",
        "website": "https://www.gzbgroup.com",
        "country": "China",
        "address": "Wuhan, China",
        "employees": "30,000+",
        "description": "葛洲坝集团，中国能建核心子公司",
        "remarks": "越南汉巴拉姆117MW风电EPC总承包",
        "projects": [
            {"name": "Hanbaram Wind Farm", "location": "Ninh Thuan, Vietnam", "capacity": "117MW", "status": "Completed", "partner": "Landville Energy (Korea)"},
            {"name": "Ben Tre 30MW Wind", "location": "Ben Tre, Vietnam", "capacity": "30MW", "status": "Completed"},
            {"name": "Ben Tre 125MW Wind", "location": "Ben Tre, Vietnam", "capacity": "125MW", "status": "Under Construction"},
        ]
    },
    {
        "name": "CEEC International (电建国际)",
        "parent": "中国能建",
        "logo_url": "",
        "website": "https://www.cpeic.ceec.net.cn",
        "country": "China",
        "address": "Beijing, China",
        "employees": "5,000+",
        "description": "中国能建国际工程公司",
        "remarks": "越南虹峰光伏325MW、油汀500MW",
        "projects": [
            {"name": "Hong Phong 1A&1B Solar", "location": "Binh Thuan, Vietnam", "capacity": "325MW", "status": "Completed"},
            {"name": "Dau Tieng 500MW Solar", "location": "Tay Ninh, Vietnam", "capacity": "500MW", "status": "Completed"},
            {"name": "Dong Hai 300MW Wind", "location": "Bac Lieu, Vietnam", "capacity": "300MW", "status": "Awarded"},
        ]
    },
]

# 越南本地EPC承包商
vietnam_epc_companies = [
    {
        "name": "IPC E&C",
        "logo_url": "https://ipcenc.com.vn/wp-content/uploads/2022/05/logo-ipc.png",
        "website": "https://ipcenc.com.vn",
        "country": "Vietnam",
        "address": "15FL, Charmvit Tower, 117 Tran Duy Hung, Ha Noi",
        "employees": "750+",
        "description": "No. 1 local EPC contractor of solar & wind power. 1.4GW track record by 2022.",
        "remarks": "Experience in overseas: 100MW wind in Philippines, 495MW wind in Laos with Goldwind."
    },
    {
        "name": "PC1 Group",
        "logo_url": "https://pc1epc.vn/wp-content/uploads/2022/01/logo.png",
        "website": "https://pc1epc.vn",
        "country": "Vietnam",
        "address": "18 Ly Van Phuc, Ba Dinh, Hanoi",
        "employees": "2000+",
        "description": "EPC contractor of wind power (over 500MW), substations & T/L.",
        "remarks": "Former EVN subsidiary. Listed in stock market since 2016. Philippines expansion 2024."
    },
    {
        "name": "FECON",
        "logo_url": "https://fecon.com.vn/wp-content/uploads/2021/01/logo-fecon.png",
        "website": "https://fecon.com.vn",
        "country": "Vietnam",
        "address": "Hanoi, Vietnam",
        "employees": "2000+",
        "description": "Foundation engineering specialist for wind power.",
        "remarks": "Quang Binh BT1&2 (252MW), expanding into offshore foundations."
    },
    {
        "name": "Trung Nam E&C",
        "logo_url": "https://trungnamgroup.com.vn/wp-content/uploads/2020/10/trungnam_logo.png",
        "website": "https://trungnamgroup.com.vn",
        "country": "Vietnam",
        "address": "Ho Chi Minh City, Vietnam",
        "employees": "1000+",
        "description": "Integrated renewable energy developer and EPC contractor.",
        "remarks": "Ea Nam 400MW wind, built 500kV transmission line."
    },
    {
        "name": "PECC2",
        "logo_url": "https://pecc2.com.vn/wp-content/uploads/2020/01/logo.png",
        "website": "https://pecc2.com.vn",
        "country": "Vietnam",
        "address": "32 Ngo Thoi Nhiem, District 1, HCMC",
        "employees": "1200+",
        "description": "Power plant consulting and EPC contractor.",
        "remarks": "EVN affiliate (51.33%), strong engineering capabilities."
    },
    {
        "name": "TOJI Group",
        "logo_url": "https://tojigroup.com.vn/wp-content/uploads/2021/01/logo-toji.png",
        "website": "https://tojigroup.com.vn",
        "country": "Vietnam",
        "address": "Bac Ha Urban Area, Mo Lao, Ha Dong, Ha Noi",
        "employees": "200+",
        "description": "No. 1 EPC contractor of substations & T/L for renewables.",
        "remarks": "Floating solar developer: Gia Hoet (35MWp), Tam Bo (35MWp)."
    },
    {
        "name": "Vu Phong Energy Group",
        "logo_url": "https://vuphong.com/wp-content/uploads/2020/11/logo.png",
        "website": "https://vuphong.com",
        "country": "Vietnam",
        "address": "Ho Chi Minh City, Vietnam",
        "employees": "500+",
        "description": "Solar EPC + O&M + PPA model provider.",
        "remarks": "Best EPC Contractor 2022 by TotalEnergies. Zero Capex pioneer."
    },
    {
        "name": "Minh Hung M&C",
        "logo_url": "https://minhhungmc.com/wp-content/uploads/2021/01/logo.png",
        "website": "https://minhhungmc.com",
        "country": "Vietnam",
        "address": "Ho Chi Minh City, Vietnam",
        "employees": "500+",
        "description": "Large-scale solar EPC contractor.",
        "remarks": "Loc Ninh 550MWp, Van Giao 100MW, uses BIM technology."
    },
    {
        "name": "PTSC M&C",
        "logo_url": "https://ptsc.com.vn/wp-content/uploads/2020/01/logo.png",
        "website": "https://ptsc.com.vn",
        "country": "Vietnam",
        "address": "Vung Tau, Vietnam",
        "employees": "3000+",
        "description": "Offshore engineering and fabrication.",
        "remarks": "Petrovietnam subsidiary. Taiwan Fengmiao offshore substation."
    },
    {
        "name": "EPC Solar Vietnam",
        "logo_url": "https://epcsolar.vn/wp-content/uploads/2021/01/logo.png",
        "website": "https://epcsolar.vn",
        "country": "Vietnam",
        "address": "Ho Chi Minh City, Vietnam",
        "employees": "200+",
        "description": "Specialized solar EPC contractor.",
        "remarks": "Sao Mai Solar 106MWp, partnerships with Longi, Jinko, Sungrow."
    },
    {
        "name": "REEPRO (REE Group)",
        "logo_url": "https://reepro.vn/wp-content/uploads/2021/01/logo.png",
        "website": "https://reepro.vn",
        "country": "Vietnam",
        "address": "Ho Chi Minh City, Vietnam",
        "employees": "300+",
        "description": "Rooftop solar EPC specialist.",
        "remarks": "REE Corporation subsidiary. 100+ C&I projects."
    },
    {
        "name": "INS Energy (Insenergy)",
        "logo_url": "https://insenergy.vn/wp-content/uploads/2021/01/logo.png",
        "website": "https://insenergy.vn",
        "country": "Vietnam",
        "address": "Ho Chi Minh City, Vietnam",
        "employees": "200+",
        "description": "Industrial solar EPC contractor.",
        "remarks": "Fast-growing since 2018, energy efficiency focus."
    },
    {
        "name": "Bac Phuong JSC",
        "logo_url": "",
        "website": "",
        "country": "Vietnam",
        "address": "Vietnam",
        "employees": "N/A",
        "description": "Wind power EPC contractor.",
        "remarks": "Dong Hai 1 wind project with Vestas."
    },
]

# 中国EPC主体公司（不含子公司）
china_epc_companies = [
    {
        "name": "PowerChina (中国电建)",
        "logo_url": "https://www.powerchina.cn/images/logo.png",
        "website": "https://www.powerchina.cn",
        "country": "China",
        "address": "Beijing, China",
        "employees": "200,000+",
        "description": "中国电力建设集团有限公司，全球最大电力建设企业",
        "remarks": "下属华东院、中南院、核工院、江西院、成都院等设计院",
        "subsidiaries": ["华东院(HDEC)", "中南院", "核工院", "江西院", "成都院"]
    },
    {
        "name": "China Energy Engineering (中国能建)",
        "logo_url": "https://en.ceec.net.cn/images/logo.png",
        "website": "https://en.ceec.net.cn",
        "country": "China",
        "address": "Beijing, China",
        "employees": "150,000+",
        "description": "中国能源建设集团有限公司",
        "remarks": "下属广东院(GEDI)、西南院、云南院、山西院、华东院、葛洲坝等",
        "subsidiaries": ["广东院(GEDI)", "西南院", "云南院", "山西院", "华东院", "葛洲坝"]
    },
    {
        "name": "CPECC International",
        "logo_url": "https://www.cpecc.com.cn/images/logo.png",
        "website": "https://www.cpecc.com.cn",
        "country": "China",
        "address": "Beijing, China / Vietnam Office",
        "employees": "8,000+",
        "description": "中国石油工程建设有限公司",
        "remarks": "CNPC subsidiary, expanding into renewables."
    },
    {
        "name": "China Huadian",
        "logo_url": "https://www.chd.com.cn/images/logo.png",
        "website": "https://www.chd.com.cn",
        "country": "China",
        "address": "Beijing, China",
        "employees": "90,000+",
        "description": "中国华电集团有限公司",
        "remarks": "Developer and investor in Vietnam renewable market."
    },
    {
        "name": "China Nuclear Industry 23",
        "logo_url": "https://www.cnnc.com.cn/images/logo.png",
        "website": "https://www.cnnc.com.cn",
        "country": "China",
        "address": "Beijing, China",
        "employees": "5,000+",
        "description": "中核二三建设有限公司",
        "remarks": "CNNC subsidiary, active in Vietnam."
    },
    {
        "name": "SEPCO3 (山东电建三公司)",
        "logo_url": "",
        "website": "https://www.sepco3.com",
        "country": "China",
        "address": "Qingdao, China",
        "employees": "10,000+",
        "description": "山东电力建设第三工程公司",
        "remarks": "沙特、埃及大型风电EPC项目"
    },
]

# 国际EPC承包商
international_epc_companies = [
    {
        "name": "Sterling & Wilson",
        "logo_url": "https://www.sterlingandwilson.com/images/logo.png",
        "website": "https://www.sterlingandwilson.com",
        "country": "India",
        "address": "Mumbai, India / ASEAN",
        "employees": "8,000+",
        "description": "Global solar EPC contractor.",
        "remarks": "Active in ASEAN solar market."
    },
    {
        "name": "Aboitiz Power",
        "logo_url": "https://www.aboitizpower.com/images/logo.png",
        "website": "https://www.aboitizpower.com",
        "country": "Philippines",
        "address": "Taguig, Philippines",
        "employees": "3,000+",
        "description": "Philippine power generation company.",
        "remarks": "Partner with PC1 for Philippines wind projects."
    },
    {
        "name": "Alternergy",
        "logo_url": "https://www.alternergy.com.ph/images/logo.png",
        "website": "https://www.alternergy.com.ph",
        "country": "Philippines",
        "address": "Makati, Philippines",
        "employees": "500+",
        "description": "Philippine renewable energy developer.",
        "remarks": "Kalayaan 2, Alabat, Tanay wind projects."
    },
]

# 主机厂商EPC（OEM兼做EPC）- 放在最后，明阳排第一
oem_epc_companies = [
    {
        "name": "Mingyang Smart Energy (明阳智能)",
        "logo_url": "https://www.myse.com.cn/images/logo.png",
        "website": "https://www.myse.com.cn",
        "country": "China",
        "address": "Zhongshan, China",
        "employees": "8,000+",
        "description": "中国第二大风机制造商，海上风电领先",
        "remarks": "越南Bac Lieu、Tra Vinh海上风电项目，东南亚市场扩张中",
        "is_oem": True,
        "oem_projects": [
            {"name": "Bac Lieu Offshore Wind Phase 3", "location": "Bac Lieu, Vietnam", "capacity": "141MW", "status": "Under Construction"},
            {"name": "Tra Vinh V1-3", "location": "Tra Vinh, Vietnam", "capacity": "128MW", "status": "Awarded"},
            {"name": "Thailand Offshore Wind", "location": "Thailand", "capacity": "200MW", "status": "Planning"},
        ]
    },
    {
        "name": "Goldwind (金风科技)",
        "logo_url": "https://www.goldwind.com/en/images/logo.png",
        "website": "https://www.goldwind.com",
        "country": "China",
        "address": "Beijing, China / ASEAN Offices",
        "employees": "10,000+",
        "description": "Major wind turbine manufacturer and EPC provider.",
        "remarks": "Savan 1 (300MW) in Laos, Thailand 286MW portfolio with GULF.",
        "is_oem": True,
        "oem_projects": [
            {"name": "Savan 1 Wind Farm", "location": "Laos", "capacity": "300MW", "status": "Completed"},
            {"name": "Monsoon Wind Farm", "location": "Laos", "capacity": "600MW", "status": "Completed"},
            {"name": "GULF Thailand Portfolio", "location": "Thailand", "capacity": "286MW", "status": "Under Construction"},
            {"name": "Cho Long Wind Farm", "location": "Gia Lai, Vietnam", "capacity": "155MW", "status": "Completed"},
        ]
    },
    {
        "name": "Vestas",
        "logo_url": "https://www.vestas.com/content/dam/vestas-com/global/images/logos/Vestas-logo.png",
        "website": "https://www.vestas.com",
        "country": "Denmark",
        "address": "Aarhus, Denmark / Vietnam Office",
        "employees": "29,000+",
        "description": "World's largest wind turbine manufacturer.",
        "remarks": "First full-scope EPC in Vietnam 2019, multiple Tra Vinh projects.",
        "is_oem": True,
        "oem_projects": [
            {"name": "Tra Vinh V1-1", "location": "Tra Vinh, Vietnam", "capacity": "48MW", "status": "Completed"},
            {"name": "Dong Hai 1 Phase 1", "location": "Bac Lieu, Vietnam", "capacity": "50MW", "status": "Completed"},
            {"name": "Lien Lap Wind Farm", "location": "Quang Tri, Vietnam", "capacity": "48MW", "status": "Completed"},
        ]
    },
    {
        "name": "Siemens Gamesa",
        "logo_url": "https://www.siemensgamesa.com/-/media/siemensgamesa/images/logos/sg-logo.svg",
        "website": "https://www.siemensgamesa.com",
        "country": "Spain",
        "address": "Zamudio, Spain / Vietnam Office",
        "employees": "27,000+",
        "description": "Leading offshore wind turbine manufacturer.",
        "remarks": "Hiep Thanh nearshore wind project, partnership with HDEC.",
        "is_oem": True,
        "oem_projects": [
            {"name": "Hiep Thanh Nearshore Wind", "location": "Soc Trang, Vietnam", "capacity": "78MW", "status": "Completed"},
        ]
    },
    {
        "name": "Envision Energy (远景能源)",
        "logo_url": "https://www.envision-group.com/images/logo.png",
        "website": "https://www.envision-group.com",
        "country": "China",
        "address": "Shanghai, China",
        "employees": "6,000+",
        "description": "Wind turbine and smart energy solutions.",
        "remarks": "Growing presence in Vietnam market.",
        "is_oem": True,
        "oem_projects": [
            {"name": "Hoa Dong 2 Wind Farm", "location": "Soc Trang, Vietnam", "capacity": "72MW", "status": "Completed"},
        ]
    },
]

# 合并所有EPC公司列表（用于兼容旧代码）
epc_companies = vietnam_epc_companies + china_epc_companies + international_epc_companies + oem_epc_companies

# 详细项目列表
projects = [
    # IPC E&C Projects (9)
    {"project_name": "Cho Long Wind Farm", "epc": "IPC E&C", "location": "Gia Lai, Vietnam", "capacity": 155, "type": "Onshore Wind", "status": "Completed", "year": "2021",
     "developer": "TSV Investment", "oem": "Goldwind", "bank": "BIDV", "om": "IPC E&C", "installer": "IPC E&C", "logistics": "INFINITY LOGISTICS"},
    {"project_name": "Cu An Wind Farm", "epc": "IPC E&C", "location": "Gia Lai, Vietnam", "capacity": 46, "type": "Onshore Wind", "status": "Completed", "year": "2021",
     "developer": "TSV Investment", "oem": "Goldwind", "bank": "BIDV", "om": "IPC E&C", "installer": "IPC E&C", "logistics": "N/A"},
    {"project_name": "Hoa Dong 2 Wind Farm", "epc": "IPC E&C", "location": "Soc Trang, Vietnam", "capacity": 72, "type": "Onshore Wind", "status": "Completed", "year": "2021",
     "developer": "N/A", "oem": "Envision", "bank": "Vietcombank", "om": "IPC E&C", "installer": "IPC E&C", "logistics": "N/A"},
    {"project_name": "Adani Phuoc Minh Solar", "epc": "IPC E&C", "location": "Ninh Thuan, Vietnam", "capacity": 27, "type": "Solar", "status": "Completed", "year": "2020",
     "developer": "Adani", "oem": "N/A", "bank": "N/A", "om": "IPC E&C", "installer": "IPC E&C", "logistics": "N/A"},
    {"project_name": "Phuoc Huu Duyen Hai 1", "epc": "IPC E&C", "location": "Ninh Thuan, Vietnam", "capacity": 30, "type": "Onshore Wind", "status": "Completed", "year": "2021",
     "developer": "N/A", "oem": "N/A", "bank": "N/A", "om": "IPC E&C", "installer": "IPC E&C", "logistics": "N/A"},
    {"project_name": "Savan 1 Wind Farm", "epc": "IPC E&C", "location": "Laos", "capacity": 300, "type": "Onshore Wind", "status": "Completed", "year": "2025",
     "developer": "Impact Energy Asia Development", "oem": "Goldwind", "bank": "ADB, Norfund", "om": "Goldwind", "installer": "IPC E&C", "logistics": "N/A"},
    {"project_name": "Kalayaan 2 Wind Farm", "epc": "IPC E&C", "location": "Laguna, Philippines", "capacity": 100.8, "type": "Onshore Wind", "status": "Under Construction", "year": "2026",
     "developer": "Alternergy", "oem": "Goldwind", "bank": "N/A", "om": "Goldwind", "installer": "IPC E&C", "logistics": "N/A"},
    {"project_name": "Solar Farms Portfolio", "epc": "IPC E&C", "location": "Various, Vietnam", "capacity": 600, "type": "Solar", "status": "Completed", "year": "2019-2021",
     "developer": "Various", "oem": "Various", "bank": "Various", "om": "IPC E&C", "installer": "IPC E&C", "logistics": "N/A"},
    {"project_name": "Rooftop Solar Portfolio", "epc": "IPC E&C", "location": "Various, Vietnam", "capacity": 100, "type": "Rooftop Solar", "status": "Completed", "year": "2019-2022",
     "developer": "Various", "oem": "Various", "bank": "N/A", "om": "IPC E&C", "installer": "IPC E&C", "logistics": "N/A"},
    
    # PC1 Projects (12)
    {"project_name": "Ia Bang 1 Wind Farm", "epc": "PC1 Group", "location": "Gia Lai, Vietnam", "capacity": 50, "type": "Onshore Wind", "status": "Completed", "year": "2021",
     "developer": "N/A", "oem": "Vestas", "bank": "BIDV", "om": "PC1 Group", "installer": "PC1 Group", "logistics": "N/A"},
    {"project_name": "Tan Phu Dong 2 Wind Farm", "epc": "PC1 Group", "location": "Tien Giang, Vietnam", "capacity": 50, "type": "Nearshore Wind", "status": "Completed", "year": "2021",
     "developer": "N/A", "oem": "Vestas", "bank": "SHB Bank", "om": "PC1 Group", "installer": "PC1 Group", "logistics": "N/A"},
    {"project_name": "Lien Lap Wind Farm", "epc": "PC1 Group", "location": "Quang Tri, Vietnam", "capacity": 48, "type": "Onshore Wind", "status": "Completed", "year": "2021",
     "developer": "RENOVA", "oem": "Vestas", "bank": "N/A", "om": "Vestas", "installer": "PC1 Group", "logistics": "INFINITY LOGISTICS"},
    {"project_name": "Phong Huy Wind Farm", "epc": "PC1 Group", "location": "Quang Tri, Vietnam", "capacity": 48, "type": "Onshore Wind", "status": "Completed", "year": "2021",
     "developer": "RENOVA", "oem": "Vestas", "bank": "N/A", "om": "Vestas", "installer": "PC1 Group", "logistics": "N/A"},
    {"project_name": "Phong Nguyen Wind Farm", "epc": "PC1 Group", "location": "Quang Tri, Vietnam", "capacity": 48, "type": "Onshore Wind", "status": "Completed", "year": "2021",
     "developer": "RENOVA", "oem": "Vestas", "bank": "N/A", "om": "Vestas", "installer": "PC1 Group", "logistics": "N/A"},
    {"project_name": "Hung Hai Gia Lai Wind Farm", "epc": "PC1 Group", "location": "Gia Lai, Vietnam", "capacity": 100, "type": "Onshore Wind", "status": "Completed", "year": "2021",
     "developer": "N/A", "oem": "N/A", "bank": "BIDV", "om": "PC1 Group", "installer": "PC1 Group", "logistics": "N/A"},
    {"project_name": "Dai Phong Wind Farm", "epc": "PC1 Group", "location": "Binh Thuan, Vietnam", "capacity": 50, "type": "Onshore Wind", "status": "Completed", "year": "2020",
     "developer": "N/A", "oem": "N/A", "bank": "N/A", "om": "PC1 Group", "installer": "PC1 Group", "logistics": "N/A"},
    {"project_name": "Hanbaram Wind Farm", "epc": "PC1 Group", "location": "Vietnam", "capacity": 48, "type": "Onshore Wind", "status": "Completed", "year": "2021",
     "developer": "N/A", "oem": "N/A", "bank": "N/A", "om": "PC1 Group", "installer": "PC1 Group", "logistics": "N/A"},
    {"project_name": "Iapet Dak Doa Wind Farm", "epc": "PC1 Group", "location": "Gia Lai, Vietnam", "capacity": 50, "type": "Onshore Wind", "status": "Completed", "year": "2021",
     "developer": "N/A", "oem": "N/A", "bank": "N/A", "om": "PC1 Group", "installer": "PC1 Group", "logistics": "N/A"},
    {"project_name": "Dau Tieng Solar Farm", "epc": "PC1 Group", "location": "Tay Ninh, Vietnam", "capacity": 500, "type": "Solar", "status": "Completed", "year": "2019",
     "developer": "N/A", "oem": "Various", "bank": "ADB", "om": "PC1 Group", "installer": "PC1 Group", "logistics": "N/A"},
    {"project_name": "Camarines Sur Wind Farm", "epc": "PC1 Group", "location": "Philippines", "capacity": 58.5, "type": "Onshore Wind", "status": "Under Construction", "year": "2026",
     "developer": "Aboitiz Power", "oem": "N/A", "bank": "N/A", "om": "N/A", "installer": "PC1 Group", "logistics": "N/A"},
    {"project_name": "DENZAI Partnership Projects", "epc": "PC1 Group", "location": "Vietnam & Philippines", "capacity": 300, "type": "Wind", "status": "Awarded", "year": "2026-2029",
     "developer": "DENZAI", "oem": "N/A", "bank": "N/A", "om": "N/A", "installer": "PC1 Group", "logistics": "N/A"},
    
    # PowerChina Projects (6)
    {"project_name": "Monsoon Wind Farm", "epc": "PowerChina Huadong (HDEC)", "location": "Sekong & Attapeu, Laos", "capacity": 600, "type": "Onshore Wind", "status": "Completed", "year": "2025",
     "developer": "Impact Energy Asia", "oem": "Goldwind", "bank": "ADB, AIIB", "om": "PowerChina", "installer": "PowerChina", "logistics": "N/A"},
    {"project_name": "Tra Vinh II Offshore Wind", "epc": "PowerChina Huadong (HDEC)", "location": "Tra Vinh, Vietnam", "capacity": 54, "type": "Offshore Wind", "status": "Completed", "year": "2022",
     "developer": "N/A", "oem": "Goldwind", "bank": "N/A", "om": "N/A", "installer": "PowerChina", "logistics": "N/A"},
    {"project_name": "Ca Mau 1 Offshore Wind", "epc": "PowerChina Huadong (HDEC)", "location": "Ca Mau, Vietnam", "capacity": 350, "type": "Offshore Wind", "status": "Under Construction", "year": "2025-2026",
     "developer": "N/A", "oem": "N/A", "bank": "N/A", "om": "N/A", "installer": "PowerChina", "logistics": "N/A"},
    {"project_name": "Soc Trang Offshore Wind", "epc": "PowerChina Huadong (HDEC)", "location": "Soc Trang, Vietnam", "capacity": 100, "type": "Offshore Wind", "status": "Completed", "year": "2023",
     "developer": "N/A", "oem": "N/A", "bank": "N/A", "om": "N/A", "installer": "PowerChina", "logistics": "N/A"},
    {"project_name": "Bac Lieu Offshore Wind", "epc": "PowerChina Huadong (HDEC)", "location": "Bac Lieu, Vietnam", "capacity": 71, "type": "Offshore Wind", "status": "Completed", "year": "2023",
     "developer": "N/A", "oem": "N/A", "bank": "N/A", "om": "N/A", "installer": "PowerChina", "logistics": "N/A"},
    {"project_name": "Binh Dai Offshore Wind", "epc": "PowerChina Huadong (HDEC)", "location": "Ben Tre, Vietnam", "capacity": 310, "type": "Offshore Wind", "status": "Completed", "year": "2023",
     "developer": "Gulf Energy", "oem": "N/A", "bank": "N/A", "om": "N/A", "installer": "PowerChina", "logistics": "N/A"},
    
    # Energy China Projects (6)
    {"project_name": "Hung Hai 100MW Wind", "epc": "Energy China (CEEC/GEDI)", "location": "Gia Lai, Vietnam", "capacity": 100, "type": "Onshore Wind", "status": "Completed", "year": "2021",
     "developer": "N/A", "oem": "N/A", "bank": "N/A", "om": "N/A", "installer": "Energy China", "logistics": "N/A"},
    {"project_name": "Gia Lai 150MW Wind", "epc": "Energy China (CEEC/GEDI)", "location": "Gia Lai, Vietnam", "capacity": 150, "type": "Onshore Wind", "status": "Completed", "year": "2021",
     "developer": "N/A", "oem": "N/A", "bank": "N/A", "om": "N/A", "installer": "Energy China", "logistics": "N/A"},
    {"project_name": "Ninh Thuan 117MW Wind", "epc": "Energy China (CEEC/GEDI)", "location": "Ninh Thuan, Vietnam", "capacity": 117, "type": "Onshore Wind", "status": "Completed", "year": "2021",
     "developer": "N/A", "oem": "N/A", "bank": "N/A", "om": "N/A", "installer": "Energy China", "logistics": "N/A"},
    {"project_name": "V1-3 Phase 2 Wind Cluster", "epc": "Energy China (CEEC/GEDI)", "location": "Vinh Long, Vietnam", "capacity": 128, "type": "Nearshore Wind", "status": "Awarded", "year": "2026",
     "developer": "N/A", "oem": "N/A", "bank": "N/A", "om": "N/A", "installer": "Energy China", "logistics": "N/A"},
    {"project_name": "Alabat + Tanay Wind Farms", "epc": "Energy China (CEEC/GEDI)", "location": "Quezon & Rizal, Philippines", "capacity": 163, "type": "Onshore Wind", "status": "Under Construction", "year": "2025",
     "developer": "Alternergy", "oem": "N/A", "bank": "N/A", "om": "N/A", "installer": "GEDI", "logistics": "N/A"},
    {"project_name": "MTerra Solar + Storage", "epc": "Energy China (CEEC/GEDI)", "location": "Nueva Ecija, Philippines", "capacity": 1050, "type": "Solar + Storage", "status": "Under Construction", "year": "2026",
     "developer": "MTerra", "oem": "N/A", "bank": "N/A", "om": "N/A", "installer": "GEDI", "logistics": "N/A"},
    
    # Goldwind Projects (4)
    {"project_name": "Savan 1 Wind Farm (OEM)", "epc": "Goldwind", "location": "Laos", "capacity": 300, "type": "Onshore Wind", "status": "Completed", "year": "2025",
     "developer": "Impact Energy", "oem": "Goldwind", "bank": "ADB", "om": "Goldwind", "installer": "IPC E&C", "logistics": "N/A"},
    {"project_name": "Kalayaan 2 Wind Farm (OEM)", "epc": "Goldwind", "location": "Laguna, Philippines", "capacity": 100.8, "type": "Onshore Wind", "status": "Under Construction", "year": "2026",
     "developer": "Alternergy", "oem": "Goldwind", "bank": "N/A", "om": "Goldwind", "installer": "IPC E&C", "logistics": "N/A"},
    {"project_name": "Thailand 286MW Wind Portfolio", "epc": "Goldwind", "location": "Thailand", "capacity": 286, "type": "Onshore Wind", "status": "Awarded", "year": "2027",
     "developer": "GULF Energy", "oem": "Goldwind", "bank": "N/A", "om": "Goldwind", "installer": "N/A", "logistics": "N/A"},
    {"project_name": "Kosy Bac Lieu Wind Farm", "epc": "Goldwind", "location": "Bac Lieu, Vietnam", "capacity": 40, "type": "Onshore Wind", "status": "Completed", "year": "2021",
     "developer": "KOSY", "oem": "Goldwind", "bank": "N/A", "om": "IPC E&C", "installer": "IPC E&C", "logistics": "N/A"},
    
    # Vestas Projects (6)
    {"project_name": "Tra Vinh Intertidal 50MW", "epc": "Vestas", "location": "Tra Vinh, Vietnam", "capacity": 50, "type": "Intertidal Wind", "status": "Completed", "year": "2019",
     "developer": "TWPC", "oem": "Vestas", "bank": "N/A", "om": "Vestas", "installer": "Vestas", "logistics": "N/A"},
    {"project_name": "Tra Vinh V1-3 48MW", "epc": "Vestas", "location": "Tra Vinh, Vietnam", "capacity": 48, "type": "Intertidal Wind", "status": "Completed", "year": "2021",
     "developer": "TTVN Group", "oem": "Vestas", "bank": "N/A", "om": "Vestas", "installer": "Vestas", "logistics": "N/A"},
    {"project_name": "Dong Hai 1 Phase 1", "epc": "Vestas", "location": "Bac Lieu, Vietnam", "capacity": 50, "type": "Intertidal Wind", "status": "Completed", "year": "2020",
     "developer": "Bac Phuong JSC", "oem": "Vestas", "bank": "N/A", "om": "Vestas", "installer": "Bac Phuong", "logistics": "N/A"},
    {"project_name": "Dong Hai 1 Phase 2", "epc": "Vestas", "location": "Bac Lieu, Vietnam", "capacity": 50, "type": "Intertidal Wind", "status": "Completed", "year": "2021",
     "developer": "Bac Phuong JSC", "oem": "Vestas", "bank": "N/A", "om": "Vestas", "installer": "Bac Phuong", "logistics": "N/A"},
    {"project_name": "Phong Lieu Wind Farm", "epc": "Vestas", "location": "Quang Tri, Vietnam", "capacity": 48, "type": "Onshore Wind", "status": "Completed", "year": "2021",
     "developer": "N/A", "oem": "Vestas", "bank": "N/A", "om": "Vestas", "installer": "N/A", "logistics": "N/A"},
    {"project_name": "Phu Lac Phase 2 + Loi Hai 2", "epc": "Vestas", "location": "Vietnam", "capacity": 53, "type": "Onshore Wind", "status": "Completed", "year": "2021",
     "developer": "TBW", "oem": "Vestas", "bank": "N/A", "om": "Vestas", "installer": "N/A", "logistics": "N/A"},
    
    # Siemens Gamesa Projects (1)
    {"project_name": "Hiep Thanh Nearshore Wind", "epc": "Siemens Gamesa", "location": "Vietnam", "capacity": 78, "type": "Nearshore Wind", "status": "Completed", "year": "2021",
     "developer": "N/A", "oem": "Siemens Gamesa", "bank": "N/A", "om": "Siemens Gamesa", "installer": "PowerChina", "logistics": "N/A"},
    
    # FECON Projects (2)
    {"project_name": "Quang Binh BT 1&2 Wind Cluster", "epc": "FECON", "location": "Quang Binh, Vietnam", "capacity": 252, "type": "Onshore Wind", "status": "Completed", "year": "2021",
     "developer": "FECON", "oem": "N/A", "bank": "N/A", "om": "N/A", "installer": "FECON", "logistics": "N/A"},
    {"project_name": "Tra Vinh V1-3 Foundation", "epc": "FECON", "location": "Tra Vinh, Vietnam", "capacity": 48, "type": "Foundation", "status": "Completed", "year": "2021",
     "developer": "TTVN Group", "oem": "Vestas", "bank": "N/A", "om": "N/A", "installer": "FECON", "logistics": "N/A"},
    
    # Trung Nam Projects (3)
    {"project_name": "Ea Nam Wind Farm", "epc": "Trung Nam E&C", "location": "Dak Lak, Vietnam", "capacity": 400, "type": "Onshore Wind", "status": "Completed", "year": "2021",
     "developer": "Trung Nam Group", "oem": "N/A", "bank": "BIDV", "om": "Trung Nam", "installer": "Trung Nam E&C", "logistics": "N/A"},
    {"project_name": "Trung Nam Solar Farm", "epc": "Trung Nam E&C", "location": "Ninh Thuan, Vietnam", "capacity": 204, "type": "Solar", "status": "Completed", "year": "2019",
     "developer": "Trung Nam Group", "oem": "N/A", "bank": "BIDV", "om": "Trung Nam", "installer": "Trung Nam E&C", "logistics": "N/A"},
    {"project_name": "500kV Ninh Thuan-Binh Duong T/L", "epc": "Trung Nam E&C", "location": "Vietnam", "capacity": 0, "type": "Transmission Line", "status": "Completed", "year": "2020",
     "developer": "Trung Nam Group", "oem": "N/A", "bank": "BIDV", "om": "EVN", "installer": "Trung Nam E&C", "logistics": "N/A"},
    
    # Minh Hung Projects (3)
    {"project_name": "Loc Ninh Solar Farm", "epc": "Minh Hung M&C", "location": "Binh Phuoc, Vietnam", "capacity": 550, "type": "Solar", "status": "Completed", "year": "2020",
     "developer": "N/A", "oem": "Longi", "bank": "N/A", "om": "N/A", "installer": "Minh Hung M&C", "logistics": "N/A"},
    {"project_name": "Van Giao 1&2 Solar Farm", "epc": "Minh Hung M&C", "location": "Vietnam", "capacity": 100, "type": "Solar", "status": "Completed", "year": "2019",
     "developer": "N/A", "oem": "N/A", "bank": "N/A", "om": "N/A", "installer": "Minh Hung M&C", "logistics": "N/A"},
    {"project_name": "Phan Lam Solar Farm", "epc": "Minh Hung M&C", "location": "Vietnam", "capacity": 50, "type": "Solar", "status": "Completed", "year": "2019",
     "developer": "N/A", "oem": "N/A", "bank": "N/A", "om": "N/A", "installer": "Minh Hung M&C", "logistics": "N/A"},
]

# 银行/金融机构
banks = [
    {"name": "ADB (Asian Development Bank)", "website": "https://www.adb.org", "type": "Development Bank", "description": "Major financier of Vietnam renewable projects"},
    {"name": "AIIB", "website": "https://www.aiib.org", "type": "Development Bank", "description": "Asian Infrastructure Investment Bank"},
    {"name": "BIDV", "website": "https://www.bidv.com.vn", "type": "Commercial Bank", "description": "Vietnam's largest commercial bank"},
    {"name": "Climate Fund Managers", "website": "https://www.climatefundmanagers.com", "type": "Investment Fund", "description": "Climate investment fund"},
    {"name": "DEG", "website": "https://www.deginvest.de", "type": "DFI", "description": "German development finance institution"},
    {"name": "HSTC Funding", "website": "", "type": "Funding", "description": "Investment funding"},
    {"name": "IFC", "website": "https://www.ifc.org", "type": "Development Finance", "description": "World Bank Group member"},
    {"name": "ING Bank", "website": "https://www.ing.com", "type": "Commercial Bank", "description": "International bank in Vietnam energy sector"},
    {"name": "Nomura", "website": "https://www.nomura.com", "type": "Investment Bank", "description": "Japanese investment bank"},
    {"name": "Norfund", "website": "https://www.norfund.no", "type": "DFI", "description": "Norwegian development finance institution"},
    {"name": "SHB Bank", "website": "https://www.shb.com.vn", "type": "Commercial Bank", "description": "Commercial bank active in energy financing"},
    {"name": "UK Export Finance", "website": "https://www.gov.uk/government/organisations/uk-export-finance", "type": "Export Credit", "description": "UK government export credit agency"},
    {"name": "VIB", "website": "https://www.vib.com.vn", "type": "Commercial Bank", "description": "Vietnam International Bank"},
    {"name": "VinaCapital", "website": "https://www.vinacapital.com", "type": "Investment Fund", "description": "Vietnam investment management"},
    {"name": "Vietcombank", "website": "https://www.vietcombank.com.vn", "type": "Commercial Bank", "description": "Major Vietnamese bank"},
]

# 风机主机厂商
oems = [
    {"name": "CRRC Corporation", "website": "https://www.crrcgc.cc", "type": "Wind Turbine", "description": "Chinese manufacturer expanding into wind"},
    {"name": "Envision Energy", "website": "https://www.envision-group.com", "type": "Wind Turbine", "description": "Chinese smart energy company"},
    {"name": "GE Renewable Energy", "website": "https://www.ge.com/renewableenergy", "type": "Wind Turbine", "description": "Global wind turbine manufacturer"},
    {"name": "Goldwind", "website": "https://www.goldwind.com", "type": "Wind Turbine", "description": "Chinese wind turbine manufacturer"},
    {"name": "Mingyang Smart Energy", "website": "https://www.myse.com.cn", "type": "Wind Turbine", "description": "Chinese wind turbine manufacturer"},
    {"name": "Nordex", "website": "https://www.nordex-online.com", "type": "Wind Turbine", "description": "German wind turbine manufacturer"},
    {"name": "SANY Group", "website": "https://www.sanygroup.com", "type": "Wind Turbine", "description": "Chinese heavy machinery manufacturer"},
    {"name": "Siemens Gamesa", "website": "https://www.siemensgamesa.com", "type": "Wind Turbine", "description": "Leading offshore wind manufacturer"},
    {"name": "Suzlon Group", "website": "https://www.suzlon.com", "type": "Wind Turbine", "description": "Indian wind turbine manufacturer"},
    {"name": "Vestas", "website": "https://www.vestas.com", "type": "Wind Turbine", "description": "World's largest wind turbine manufacturer"},
]

# 运维厂商
om_contractors = [
    # 越南本地运维公司（参与风电项目）
    {"name": "IPC E&C O&M", "website": "https://ipcenc.com.vn", "type": "Full O&M", "country": "Vietnam",
     "description": "越南本土风电运维领导者", "projects": ["Cho Long", "Cu An", "Hoa Dong 2", "Kosy Bac Lieu"]},
    {"name": "PC1 O&M Services", "website": "https://pc1epc.vn", "type": "Full O&M", "country": "Vietnam",
     "description": "越南风电运维主力", "projects": ["Ia Bang", "Tan Phu Dong", "Hung Hai", "Multiple wind farms"]},
    {"name": "Trung Nam O&M", "website": "https://trungnamgroup.com.vn", "type": "Full O&M", "country": "Vietnam",
     "description": "Trung Nam集团运维部门", "projects": ["Ea Nam 400MW", "Ninh Thuan solar"]},
    {"name": "Vu Phong O&M", "website": "https://vuphong.com", "type": "Solar O&M", "country": "Vietnam",
     "description": "太阳能运维专家", "projects": ["Multiple rooftop and ground-mount solar"]},
    {"name": "PECC2 O&M", "website": "https://pecc2.com.vn", "type": "Full O&M", "country": "Vietnam",
     "description": "EVN关联运维服务商", "projects": ["Multiple power plants"]},
    {"name": "EVN Services", "website": "https://evn.com.vn", "type": "Grid O&M", "country": "Vietnam",
     "description": "电网和变电站运维", "projects": ["500kV transmission lines", "Substations"]},
    # 主机厂商运维服务
    {"name": "Goldwind O&M", "website": "https://www.goldwind.com", "type": "OEM O&M", "country": "China",
     "description": "金风科技运维服务", "projects": ["Cho Long", "Cu An", "Savan 1", "Monsoon"]},
    {"name": "Vestas AOM Services", "website": "https://www.vestas.com", "type": "OEM O&M", "country": "Denmark",
     "description": "AOM 4000/5000全生命周期服务", "projects": ["Lien Lap", "Phong Huy", "Tra Vinh projects"]},
    {"name": "Siemens Gamesa Service", "website": "https://www.siemensgamesa.com", "type": "OEM O&M", "country": "Spain",
     "description": "西门子歌美飒运维", "projects": ["Hiep Thanh nearshore"]},
    {"name": "Envision Service", "website": "https://www.envision-group.com", "type": "OEM O&M", "country": "China",
     "description": "远景能源运维服务", "projects": ["Hoa Dong 2"]},
    {"name": "Mingyang Service", "website": "https://www.myse.com.cn", "type": "OEM O&M", "country": "China",
     "description": "明阳智能运维中心", "projects": ["Southeast Asia wind projects"]},
    # 国际第三方运维
    {"name": "Global Wind Service (GWS)", "website": "https://www.globalwindservice.com", "type": "ISP O&M", "country": "Denmark",
     "description": "全球独立风电运维服务商", "projects": ["International wind farms"]},
    {"name": "Deutsche Windtechnik", "website": "https://www.deutsche-windtechnik.com", "type": "ISP O&M", "country": "Germany",
     "description": "德国独立风电运维", "projects": ["Multi-brand O&M"]},
    {"name": "协合运维 (Xiehe O&M)", "website": "https://www.xh-service.com", "type": "ISP O&M", "country": "China",
     "description": "中国最大独立风电运维商，40GW+运维容量", "projects": ["China and overseas wind farms"]},
    {"name": "PowerChina O&M", "website": "https://www.powerchina.cn", "type": "Full O&M", "country": "China",
     "description": "中国电建运维服务", "projects": ["Monsoon 600MW", "Multiple offshore"]},
]

# 运输/物流厂商
logistics_companies = [
    # 越南本地陆运公司（参与风电项目）
    {"name": "PC1 Group (Logistics)", "website": "https://pc1epc.vn", "type": "Wind Equipment Transport", "country": "Vietnam",
     "description": "越南风电设备运输吊装，EPC承包商兼运输", "projects": ["Ia Bang blade transport", "Lien Lap tower transport", "Multiple wind farm logistics"]},
    {"name": "DENZAI (Logistics)", "website": "https://denzai.co.jp", "type": "Wind Equipment Transport & Lifting", "country": "Japan/Vietnam",
     "description": "日本风电运输吊装专家，与PC1合作", "projects": ["Vietnam-Philippines wind logistics", "Heavy lift crane services", "Turbine installation support"]},
    {"name": "INFINITY LOGISTICS", "website": "https://infinitylogistics.com.vn", "type": "Wind Project Logistics", "country": "Vietnam",
     "description": "越南风电项目专业物流", "projects": ["Cho Long Wind Farm", "Lien Lap Wind Farm"]},
    {"name": "PL Logistics Corp", "website": "https://pllogistics.com.vn", "type": "Heavy Transport", "country": "Vietnam",
     "description": "越南重型设备运输专家", "projects": ["Multiple wind turbine blade transport"]},
    {"name": "Gemadept Logistics", "website": "https://www.gemadept.com.vn", "type": "Integrated Logistics", "country": "Vietnam",
     "description": "越南最大物流企业之一，港口+内陆运输", "projects": ["Wind equipment port handling"]},
    {"name": "Transimex Corporation", "website": "https://www.transimex.com.vn", "type": "Project Cargo", "country": "Vietnam",
     "description": "越南项目货物运输", "projects": ["Renewable energy equipment logistics"]},
    {"name": "Vietrans JSC", "website": "https://vietrans.com.vn", "type": "Forwarding", "country": "Vietnam",
     "description": "越南货运代理，风电设备运输", "projects": ["Wind turbine components"]},
    {"name": "ITL Corporation", "website": "https://www.itlcorp.com.vn", "type": "Integrated Logistics", "country": "Vietnam",
     "description": "越南综合物流服务商", "projects": ["Solar and wind equipment"]},
    {"name": "Saigon Newport Corporation", "website": "https://www.saigonnewport.com.vn", "type": "Port & Logistics", "country": "Vietnam",
     "description": "西贡新港，风机进口主要港口", "projects": ["Wind turbine import handling"]},
    {"name": "Tan Cang Logistics", "website": "https://tancanglogistics.com.vn", "type": "Container & Project", "country": "Vietnam",
     "description": "新港物流，军方背景", "projects": ["Heavy lift equipment"]},
    # 国际重型运输公司
    {"name": "Mammoet", "website": "https://www.mammoet.com", "type": "Heavy Lift", "country": "Netherlands",
     "description": "全球重型吊装和运输领导者", "projects": ["Vietnam offshore wind installation"]},
    {"name": "Sarens", "website": "https://www.sarens.com", "type": "Heavy Lift", "country": "Belgium",
     "description": "全球重型吊装解决方案", "projects": ["Crane services Vietnam wind"]},
    {"name": "Boskalis", "website": "https://www.boskalis.com", "type": "Marine Services", "country": "Netherlands",
     "description": "海上工程和物流", "projects": ["Offshore wind marine logistics"]},
    {"name": "Combi Lift Asia", "website": "https://www.combilift-asia.com", "type": "Heavy Lift", "country": "Singapore",
     "description": "亚洲重型吊装运输", "projects": ["Wind farm equipment transport"]},
    {"name": "ALE (Mammoet)", "website": "https://www.ale-heavylift.com", "type": "Heavy Transport", "country": "UK",
     "description": "超重型运输专家", "projects": ["Turbine component transport"]},
    {"name": "COSCO Shipping Special", "website": "https://www.coscoshipping.com", "type": "Marine Transport", "country": "China",
     "description": "中远海运特运，风电大件海运", "projects": ["Offshore wind equipment shipping"]},
    {"name": "BBC Chartering", "website": "https://www.bbc-chartering.com", "type": "Project Cargo", "country": "Germany",
     "description": "项目货物船运", "projects": ["Wind turbine sea transport"]},
]

# 安装厂商（参与越南风电项目）
installers = [
    # 越南本地安装公司
    {"name": "PC1 Group", "website": "https://pc1epc.vn", "type": "Wind Installation & Lifting", "country": "Vietnam",
     "description": "越南风电安装/吊装主力，EPC兼运输吊装", "projects": ["Ia Bang 50MW", "Lien Lap 48MW", "Hung Hai 100MW", "500+ MW wind installation"]},
    {"name": "DENZAI", "website": "https://denzai.co.jp", "type": "Wind Installation & Lifting", "country": "Japan/Vietnam",
     "description": "日本风电安装吊装专家，与PC1合作", "projects": ["Vietnam 300MW partnership", "Philippines wind projects", "DENZAI-PC1 JV projects"]},
    {"name": "IPC E&C (Installation)", "website": "https://ipcenc.com.vn", "type": "Wind Installation", "country": "Vietnam",
     "description": "越南本土风电安装领导者", "projects": ["Cho Long 155MW", "Cu An 46MW", "Savan 1 300MW"]},
    {"name": "FECON (Foundation)", "website": "https://fecon.com.vn", "type": "Foundation", "country": "Vietnam",
     "description": "风电基础工程专家", "projects": ["Quang Binh BT1&2 252MW foundation", "Tra Vinh V1-3 foundation"]},
    {"name": "PTSC M&C", "website": "https://ptsc.com.vn", "type": "Offshore Installation", "country": "Vietnam",
     "description": "海上风电安装和制造", "projects": ["Taiwan Fengmiao substation"]},
    {"name": "Trung Nam E&C", "website": "https://trungnamgroup.com.vn", "type": "Wind Installation", "country": "Vietnam",
     "description": "Trung Nam集团安装部门", "projects": ["Ea Nam 400MW"]},
    {"name": "Bac Phuong JSC", "website": "", "type": "Wind Installation", "country": "Vietnam",
     "description": "Dong Hai风电安装", "projects": ["Dong Hai 1 Phase 1&2"]},
    {"name": "TDEC Thai Duong Electrics", "website": "https://tdecd.com.vn", "type": "Electrical", "country": "Vietnam",
     "description": "电气安装承包商", "projects": ["Multiple wind farm electrical systems"]},
    # 中国安装公司
    {"name": "PowerChina (Installation)", "website": "https://www.powerchina.cn", "type": "Full Installation", "country": "China",
     "description": "中国电建安装部门", "projects": ["Monsoon 600MW", "Ca Mau offshore", "Tra Vinh offshore"]},
    {"name": "Energy China (Installation)", "website": "https://en.ceec.net.cn", "type": "Full Installation", "country": "China",
     "description": "中国能建安装部门", "projects": ["Hung Hai 100MW", "Gia Lai 150MW"]},
    {"name": "XCMG (徐工)", "website": "https://www.xcmg.com", "type": "Crane & Lifting", "country": "China",
     "description": "风电吊装设备和服务", "projects": ["Multiple wind farm crane services"]},
    {"name": "Sany Heavy Industry", "website": "https://www.sany.com.cn", "type": "Crane & Lifting", "country": "China",
     "description": "三一重工吊装设备", "projects": ["Wind turbine installation"]},
    # 国际安装公司
    {"name": "EEW Group", "website": "https://www.eew-group.com", "type": "Foundation", "country": "Germany",
     "description": "海上风电单桩制造", "projects": ["Offshore wind foundations"]},
    {"name": "Seajacks", "website": "https://www.seajacks.com", "type": "Offshore Installation", "country": "UK",
     "description": "海上风电安装船", "projects": ["Offshore wind vessel services"]},
    {"name": "Fred. Olsen Windcarrier", "website": "https://www.windcarrier.com", "type": "Offshore Installation", "country": "Norway",
     "description": "海上风电安装运输", "projects": ["Offshore wind installation"]},
    {"name": "VIVABLAST Group", "website": "https://www.vivablast.com", "type": "Surface Treatment", "country": "International",
     "description": "表面处理和涂装", "projects": ["Wind tower coating"]},
]

# 开发商/业主
developers = [
    {"name": "AC Energy Vietnam", "website": "https://www.acenergy.com.ph", "type": "Developer", "description": "420MW wind COD"},
    {"name": "Adani", "website": "https://www.adani.com", "type": "Developer", "description": "Indian conglomerate"},
    {"name": "AMACCAO Group", "website": "", "type": "Developer", "description": "Quang Tri 49.2MW owner"},
    {"name": "Asia Energy JSC", "website": "", "type": "Developer", "description": "Dak Song 1 50MW developer"},
    {"name": "Bac Phuong JSC", "website": "", "type": "Developer", "description": "Dong Hai wind project owner"},
    {"name": "BANPU Power", "website": "https://www.banpu.com", "type": "Developer", "description": "Thai energy company"},
    {"name": "Baywa r.e.", "website": "https://www.baywa-re.com", "type": "Developer", "description": "German renewable developer"},
    {"name": "BIM Group", "website": "https://www.bimgroup.com.vn", "type": "Developer", "description": "Vietnamese conglomerate"},
    {"name": "Copenhagen Offshore Partners", "website": "https://www.cop.dk", "type": "Developer", "description": "Offshore wind developer"},
    {"name": "Corio Generation", "website": "https://www.coriogeneration.com", "type": "Developer", "description": "Offshore wind developer"},
    {"name": "EDF Renewables", "website": "https://www.edf-re.com", "type": "Developer", "description": "French renewable developer"},
    {"name": "Enel Green Power", "website": "https://www.enelgreenpower.com", "type": "Developer", "description": "Italian renewable developer"},
    {"name": "ENERTRAG", "website": "https://www.enertrag.com", "type": "Developer", "description": "German wind developer"},
    {"name": "Gelex Infrastructure", "website": "https://www.gelex.com.vn", "type": "Developer", "description": "Vietnamese developer"},
    {"name": "Gulf Energy Vietnam", "website": "https://www.gulf.co.th", "type": "Developer", "description": "Binh Dai 1,2,3 (128MW)"},
    {"name": "Hacom Holdings", "website": "", "type": "Developer", "description": "Local developer 80MW"},
    {"name": "Impact Energy Asia", "website": "", "type": "Developer", "description": "Monsoon/Savan project developer"},
    {"name": "KOSY", "website": "https://www.kosy.vn", "type": "Developer", "description": "400MW project owner"},
    {"name": "Levanta Renewables", "website": "", "type": "Developer", "description": "Kon Tum 103.5MW owner"},
    {"name": "LICOGI 13", "website": "", "type": "Developer", "description": "LIG Huong Hoa 96MW owner"},
    {"name": "Mainstream Renewable Power", "website": "https://www.mainstreamrp.com", "type": "Developer", "description": "Irish renewable developer"},
    {"name": "NEXIF Energy", "website": "https://www.nexifenergy.com", "type": "Developer", "description": "Singapore renewable developer"},
    {"name": "NOVA International", "website": "", "type": "Developer", "description": "Vietnamese developer"},
    {"name": "NOVASIA Energy", "website": "", "type": "Developer", "description": "Yen Dung 150MW developer"},
    {"name": "Orsted", "website": "https://www.orsted.com", "type": "Developer", "description": "Danish offshore wind developer"},
    {"name": "Pacifico Energy", "website": "https://www.pacificoenergy.com", "type": "Developer", "description": "30MW onshore wind"},
    {"name": "PNE", "website": "https://www.pne.com", "type": "Developer", "description": "German wind developer"},
    {"name": "REE Corporation", "website": "https://www.reecorp.com", "type": "Developer", "description": "Phu Lac 1, Tra Vinh 3 owner"},
    {"name": "RENOVA", "website": "https://www.renovainc.com", "type": "Developer", "description": "Japanese renewable developer"},
    {"name": "Super Energy", "website": "", "type": "Developer", "description": "Thai energy company"},
    {"name": "T&T Group", "website": "https://www.ttgroupvn.com", "type": "Developer", "description": "Vietnam major private enterprise"},
    {"name": "The Blue Circle", "website": "https://www.thebluecircle.sg", "type": "Developer", "description": "Singapore renewable developer"},
    {"name": "Tokyo Gas", "website": "https://www.tokyo-gas.co.jp", "type": "Developer", "description": "Japanese energy company"},
    {"name": "TotalEnergies", "website": "https://www.totalenergies.com", "type": "Developer", "description": "French energy major"},
    {"name": "Trung Nam Group", "website": "https://www.trungnamgroup.com.vn", "type": "Developer", "description": "Vietnam largest private renewable developer"},
    {"name": "TSV Investment", "website": "", "type": "Developer", "description": "Kong Yang 175MW, Cu An 175MW"},
    {"name": "TTVN Group", "website": "", "type": "Developer", "description": "Tra Vinh V1-2 wind owner"},
    {"name": "UPC Renewables", "website": "https://www.upc-renewables.com", "type": "Developer", "description": "Global renewable developer"},
    {"name": "Vietracimex", "website": "", "type": "Developer", "description": "100MW project owner"},
    {"name": "Vingroup/VinEnergo", "website": "https://www.vingroup.net", "type": "Developer", "description": "Vietnam largest conglomerate"},
    {"name": "WPD", "website": "https://www.wpd.de", "type": "Developer", "description": "German wind developer"},
]

def download_logo(url, name):
    """下载logo并保存"""
    if not url:
        return None
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            ext = url.split('.')[-1].split('?')[0][:4]
            if ext not in ['png', 'jpg', 'jpeg', 'svg', 'webp']:
                ext = 'png'
            filename = f"logos/{name.replace(' ', '_').replace('/', '_')}.{ext}"
            with open(filename, 'wb') as f:
                f.write(response.content)
            return filename
    except Exception as e:
        print(f"Failed to download logo for {name}: {e}")
    return None

def count_projects(company_name, all_projects):
    return len([p for p in all_projects if p.get('epc') == company_name])

def get_letter_index(companies, key='name'):
    """获取字母索引"""
    letters = sorted(set(c[key][0].upper() for c in companies if c[key]))
    return letters

def generate_html():
    """生成HTML看板"""
    
    print("Downloading logos...")
    logo_files = {}
    for epc in epc_companies:
        if epc.get('logo_url'):
            logo_files[epc['name']] = download_logo(epc['logo_url'], epc['name'])
    
    # 按项目数量排序各类EPC
    def add_project_counts(companies):
        result = []
        for c in companies:
            count = count_projects(c['name'], projects)
            result.append({**c, 'project_count': count, 'logo_file': logo_files.get(c['name'])})
        return sorted(result, key=lambda x: -x['project_count'])
    
    # 分类EPC
    vietnam_epc_sorted = add_project_counts(vietnam_epc_companies)
    china_epc_sorted = add_project_counts(china_epc_companies)
    international_epc_sorted = add_project_counts(international_epc_companies)
    oem_epc_sorted = add_project_counts(oem_epc_companies)
    
    # 中国电建子公司
    powerchina_subs_sorted = sorted(powerchina_subsidiaries, key=lambda x: x['name'])
    # 中国能建子公司
    ceec_subs_sorted = sorted(ceec_subsidiaries, key=lambda x: x['name'])
    
    # 合并所有EPC用于兼容
    epc_sorted = vietnam_epc_sorted + china_epc_sorted + international_epc_sorted + oem_epc_sorted
    
    # 按首字母排序其他公司
    banks_sorted = sorted(banks, key=lambda x: x['name'].upper())
    oems_sorted = sorted(oems, key=lambda x: x['name'].upper())
    om_sorted = sorted(om_contractors, key=lambda x: x['name'].upper())
    logistics_sorted = sorted(logistics_companies, key=lambda x: x['name'].upper())
    installers_sorted = sorted(installers, key=lambda x: x['name'].upper())
    developers_sorted = sorted(developers, key=lambda x: x['name'].upper())
    
    # 统计
    total_projects = len(projects)
    completed = len([p for p in projects if p['status'] == 'Completed'])
    ongoing = len([p for p in projects if p['status'] == 'Under Construction'])
    awarded = len([p for p in projects if p['status'] == 'Awarded'])
    total_mw = sum([p['capacity'] for p in projects])
    
    # 获取当前时间
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vietnam Renewable Energy Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #1e40af;
            --primary-light: #3b82f6;
            --accent: #f59e0b;
            --bg-dark: #0f172a;
            --bg-card: #1e293b;
            --bg-hover: #334155;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --border: #334155;
            --success: #10b981;
            --warning: #f59e0b;
            --info: #3b82f6;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', 'Noto Sans SC', sans-serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            line-height: 1.5;
        }}
        
        /* Header */
        header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
            padding: 2rem;
            text-align: center;
        }}
        header h1 {{ font-size: 2rem; margin-bottom: 0.5rem; }}
        
        /* Search Box */
        .search-container {{
            max-width: 600px;
            margin: 1rem auto;
            position: relative;
        }}
        .search-input {{
            width: 100%;
            padding: 0.8rem 1rem 0.8rem 3rem;
            border: 2px solid var(--border);
            border-radius: 50px;
            background: rgba(255,255,255,0.1);
        }}
        
        /* Download Button */
        .download-btn {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            margin-top: 1rem;
            padding: 0.6rem 1.2rem;
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 500;
            text-decoration: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        }}
        .download-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
            background: linear-gradient(135deg, #059669, #047857);
            color: white;
            font-size: 1rem;
            outline: none;
        }}
        .search-input::placeholder {{ color: rgba(255,255,255,0.6); }}
        .search-input:focus {{ border-color: var(--accent); }}
        .search-icon {{
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            font-size: 1.2rem;
        }}
        
        /* Navigation */
        .nav-container {{
            background: var(--bg-card);
            padding: 1rem;
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 1px solid var(--border);
        }}
        .nav-tabs {{
            display: flex;
            justify-content: center;
            gap: 0.4rem;
            flex-wrap: wrap;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .nav-tab {{
            padding: 0.5rem 1rem;
            background: transparent;
            border: 2px solid var(--border);
            border-radius: 25px;
            color: var(--text-secondary);
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 500;
            transition: all 0.2s;
        }}
        .nav-tab:hover {{ border-color: var(--accent); color: var(--accent); }}
        .nav-tab.active {{ background: var(--accent); border-color: var(--accent); color: white; }}
        
        /* Letter Index */
        .letter-index {{
            display: flex;
            justify-content: center;
            gap: 0.3rem;
            padding: 0.8rem;
            background: var(--bg-hover);
            flex-wrap: wrap;
            margin-bottom: 1rem;
            border-radius: 8px;
        }}
        .letter-btn {{
            width: 30px;
            height: 30px;
            border: 1px solid var(--border);
            border-radius: 4px;
            background: var(--bg-card);
            color: var(--text-secondary);
            cursor: pointer;
            font-size: 0.8rem;
            font-weight: 600;
            transition: all 0.2s;
        }}
        .letter-btn:hover {{ background: var(--accent); color: white; }}
        .letter-btn.active {{ background: var(--primary); color: white; }}
        
        /* Stats */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 1rem;
            padding: 1.5rem;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .stat-card {{
            background: var(--bg-card);
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            border: 1px solid var(--border);
        }}
        .stat-number {{ font-size: 1.8rem; font-weight: 700; color: var(--accent); }}
        .stat-label {{ font-size: 0.8rem; color: var(--text-secondary); }}
        
        /* Main Content */
        main {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 1rem;
        }}
        .section {{ display: none; }}
        .section.active {{ display: block; }}
        .section-title {{
            font-size: 1.4rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--accent);
            display: inline-block;
        }}
        
        /* Company Grid */
        .company-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 1rem;
        }}
        .company-card {{
            background: var(--bg-card);
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid var(--border);
            transition: all 0.2s;
        }}
        .company-card:hover {{
            border-color: var(--accent);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }}
        .card-header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
            padding: 1rem;
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }}
        .company-logo {{
            width: 50px;
            height: 50px;
            background: white;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            color: var(--primary);
            font-size: 1rem;
            overflow: hidden;
            flex-shrink: 0;
        }}
        .company-logo img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            padding: 3px;
        }}
        .company-name {{ font-size: 1rem; font-weight: 600; }}
        .company-country {{ font-size: 0.75rem; opacity: 0.8; }}
        .project-badge {{
            background: var(--accent);
            padding: 0.15rem 0.5rem;
            border-radius: 10px;
            font-size: 0.7rem;
            margin-left: auto;
            font-weight: 600;
        }}
        .card-body {{ padding: 1rem; }}
        .card-info {{ font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 0.4rem; }}
        .card-desc {{ font-size: 0.85rem; margin-bottom: 0.6rem; }}
        .website-link {{
            display: inline-block;
            color: var(--info);
            font-size: 0.8rem;
            text-decoration: none;
            margin-bottom: 0.8rem;
        }}
        .website-link:hover {{ text-decoration: underline; }}
        
        /* Project List - Show ALL */
        .project-list {{
            max-height: 400px;
            overflow-y: auto;
            margin-top: 0.8rem;
            padding-top: 0.8rem;
            border-top: 1px solid var(--border);
        }}
        .project-list::-webkit-scrollbar {{ width: 6px; }}
        .project-list::-webkit-scrollbar-track {{ background: var(--bg-hover); border-radius: 3px; }}
        .project-list::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 3px; }}
        
        .project-item {{
            background: var(--bg-hover);
            border-radius: 6px;
            padding: 0.6rem;
            margin-bottom: 0.4rem;
            cursor: pointer;
            transition: all 0.2s;
            border-left: 3px solid var(--success);
        }}
        .project-item.ongoing {{ border-left-color: var(--warning); }}
        .project-item.awarded {{ border-left-color: var(--info); }}
        .project-item:hover {{ background: var(--border); }}
        .project-title {{ font-weight: 600; font-size: 0.85rem; }}
        .project-meta {{ font-size: 0.75rem; color: var(--text-secondary); }}
        .status-badge {{
            display: inline-block;
            padding: 0.1rem 0.3rem;
            border-radius: 3px;
            font-size: 0.6rem;
            font-weight: 600;
            text-transform: uppercase;
        }}
        .status-badge.completed {{ background: rgba(16, 185, 129, 0.2); color: var(--success); }}
        .status-badge.ongoing {{ background: rgba(245, 158, 11, 0.2); color: var(--warning); }}
        .status-badge.awarded {{ background: rgba(59, 130, 246, 0.2); color: var(--info); }}
        
        /* Simple Cards */
        .simple-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 0.8rem;
        }}
        .simple-card {{
            background: var(--bg-card);
            border-radius: 8px;
            padding: 1rem;
            border: 1px solid var(--border);
            display: flex;
            align-items: center;
            gap: 0.8rem;
            transition: all 0.2s;
        }}
        .simple-card:hover {{ border-color: var(--accent); }}
        .simple-logo {{
            width: 40px;
            height: 40px;
            background: white;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            color: var(--primary);
            font-size: 0.9rem;
            flex-shrink: 0;
        }}
        .simple-info h4 {{ font-size: 0.9rem; margin-bottom: 0.2rem; }}
        .simple-info p {{ font-size: 0.75rem; color: var(--text-secondary); }}
        .type-badge {{
            display: inline-block;
            padding: 0.1rem 0.4rem;
            background: var(--primary);
            border-radius: 3px;
            font-size: 0.65rem;
            margin-right: 0.2rem;
        }}
        
        /* Modal */
        .modal {{
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.85);
            z-index: 1000;
            justify-content: center;
            align-items: center;
            padding: 1rem;
        }}
        .modal.active {{ display: flex; }}
        .modal-content {{
            background: var(--bg-card);
            border-radius: 12px;
            max-width: 650px;
            width: 100%;
            max-height: 85vh;
            overflow-y: auto;
            border: 1px solid var(--border);
        }}
        .modal-header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
            padding: 1.2rem;
            position: sticky;
            top: 0;
        }}
        .modal-title {{ font-size: 1.1rem; font-weight: 700; }}
        .modal-close {{
            position: absolute;
            top: 0.8rem; right: 1rem;
            background: none;
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
        }}
        .modal-body {{ padding: 1.2rem; }}
        .detail-section {{ margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid var(--border); }}
        .detail-title {{ font-size: 0.85rem; color: var(--accent); margin-bottom: 0.5rem; font-weight: 600; }}
        .detail-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.6rem; }}
        .detail-item {{ background: var(--bg-hover); padding: 0.6rem; border-radius: 6px; }}
        .detail-label {{ font-size: 0.7rem; color: var(--text-secondary); }}
        .detail-value {{ font-size: 0.85rem; font-weight: 500; }}
        
        footer {{
            text-align: center;
            padding: 1.5rem;
            background: var(--bg-card);
            margin-top: 2rem;
            border-top: 1px solid var(--border);
            font-size: 0.9rem;
            font-size: 0.8rem;
            color: var(--text-secondary);
        }}
        
        @media (max-width: 768px) {{
            .company-grid, .simple-grid {{ grid-template-columns: 1fr; }}
            .nav-tab {{ padding: 0.4rem 0.7rem; font-size: 0.75rem; }}
            .detail-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>Vietnam Renewable Energy Dashboard</h1>
        <p>EPC / Developers / OEM / Banks / O&M / Logistics / Installation</p>
        <div class="search-container">
            <span class="search-icon">🔍</span>
            <input type="text" class="search-input" id="searchInput" placeholder="Search companies or projects...">
        </div>
        <a href="Vietnam_Renewable_Energy_Report.xlsx" download class="download-btn">
            📥 下载完整Excel报告
        </a>
    </header>
    
    <div class="nav-container">
        <div class="nav-tabs">
            <button class="nav-tab active" data-section="epc">EPC ({len(epc_sorted)})</button>
            <button class="nav-tab" data-section="developers">Developers ({len(developers_sorted)})</button>
            <button class="nav-tab" data-section="oems">OEM ({len(oems_sorted)})</button>
            <button class="nav-tab" data-section="banks">Banks ({len(banks_sorted)})</button>
            <button class="nav-tab" data-section="om">O&M ({len(om_sorted)})</button>
            <button class="nav-tab" data-section="logistics">Logistics ({len(logistics_sorted)})</button>
            <button class="nav-tab" data-section="installers">Installers ({len(installers_sorted)})</button>
        </div>
    </div>
    
    <div class="stats-grid">
        <div class="stat-card"><div class="stat-number">{len(epc_sorted)}</div><div class="stat-label">EPC</div></div>
        <div class="stat-card"><div class="stat-number">{total_projects}</div><div class="stat-label">Projects</div></div>
        <div class="stat-card"><div class="stat-number">{completed}</div><div class="stat-label">Completed</div></div>
        <div class="stat-card"><div class="stat-number">{ongoing}</div><div class="stat-label">Ongoing</div></div>
        <div class="stat-card"><div class="stat-number">{awarded}</div><div class="stat-label">Awarded</div></div>
        <div class="stat-card"><div class="stat-number">{total_mw:,.0f}</div><div class="stat-label">Total MW</div></div>
    </div>
    
    <main>
        <!-- EPC Section -->
        <section id="epc" class="section active">
            <h2 class="section-title">EPC Contractors</h2>
            
            <!-- EPC国家分类导航 - 简洁版 -->
            <div class="epc-category-nav" style="display:flex;gap:0.8rem;flex-wrap:wrap;margin-bottom:1.5rem;padding:1rem;background:var(--bg-card);border-radius:12px;justify-content:center;">
                <button class="epc-cat-btn" onclick="scrollToEpcSection('vietnam-epc')" style="padding:0.6rem 1.2rem;border:2px solid var(--accent);border-radius:8px;cursor:pointer;font-weight:700;background:var(--accent);color:var(--bg-primary);font-size:0.95rem;">🇻🇳 越南EPC</button>
                <button class="epc-cat-btn" onclick="scrollToEpcSection('china-epc')" style="padding:0.6rem 1.2rem;border:2px solid #dc2626;border-radius:8px;cursor:pointer;font-weight:700;background:transparent;color:#dc2626;font-size:0.95rem;">🇨🇳 中国EPC</button>
                <button class="epc-cat-btn" onclick="scrollToEpcSection('intl-epc')" style="padding:0.6rem 1.2rem;border:2px solid #2563eb;border-radius:8px;cursor:pointer;font-weight:700;background:transparent;color:#2563eb;font-size:0.95rem;">🌍 国际EPC</button>
                <button class="epc-cat-btn" onclick="scrollToEpcSection('oem-epc')" style="padding:0.6rem 1.2rem;border:2px solid #f59e0b;border-radius:8px;cursor:pointer;font-weight:700;background:transparent;color:#f59e0b;font-size:0.95rem;">⚙️ 主机厂商EPC</button>
            </div>
'''
    
    # Helper function to generate EPC cards
    def generate_epc_cards(companies, show_oem_badge=False, show_oem_projects=False):
        cards_html = ""
        for epc in companies:
            logo_init = epc['name'][:2].upper()
            logo_html = f'<img src="{epc.get("logo_file", "")}" alt="{epc["name"]}">' if epc.get('logo_file') and os.path.exists(epc.get('logo_file', '')) else logo_init
            
            epc_projects = [p for p in projects if p['epc'] == epc['name']]
            
            projects_html = ""
            # 显示常规项目
            for p in epc_projects:
                status_class = 'completed' if p['status'] == 'Completed' else ('ongoing' if p['status'] == 'Under Construction' else 'awarded')
                escaped_name = p['project_name'].replace("'", "\\'")
                projects_html += f'''
                    <div class="project-item {status_class}" onclick="showModal('{escaped_name}')">
                        <div class="project-title">{p['project_name']}</div>
                        <div class="project-meta">{p['location']} | {p['capacity']}MW <span class="status-badge {status_class}">{p['status']}</span></div>
                    </div>'''
            
            # 显示OEM项目（如果有）
            if show_oem_projects and epc.get('oem_projects'):
                for op in epc['oem_projects']:
                    status_class = 'completed' if op['status'] == 'Completed' else ('ongoing' if op['status'] == 'Under Construction' else 'awarded')
                    projects_html += f'''
                    <div class="project-item {status_class}">
                        <div class="project-title">{op['name']}</div>
                        <div class="project-meta">{op['location']} | {op['capacity']} <span class="status-badge {status_class}">{op['status']}</span></div>
                    </div>'''
            
            total_projects = len(epc_projects) + (len(epc.get('oem_projects', [])) if show_oem_projects else 0)
            
            website_html = f'<a href="{epc.get("website", "")}" target="_blank" class="website-link">🌐 {epc.get("website", "")}</a>' if epc.get('website') else ''
            oem_badge = '<span style="background:#f59e0b;color:#000;padding:2px 6px;border-radius:4px;font-size:0.7rem;margin-left:5px;">OEM</span>' if show_oem_badge else ''
            subs_html = f'<div style="font-size:0.75rem;color:var(--accent);margin-top:0.3rem;">子公司: {", ".join(epc.get("subsidiaries", []))}</div>' if epc.get('subsidiaries') else ''
            
            cards_html += f'''
                <div class="company-card" data-name="{epc['name'].lower()}">
                    <div class="card-header">
                        <div class="company-logo">{logo_html}</div>
                        <div>
                            <div class="company-name">{epc['name']}{oem_badge}</div>
                            <div class="company-country">{epc.get('country', 'N/A')}</div>
                        </div>
                        <div class="project-badge">{total_projects} projects</div>
                    </div>
                    <div class="card-body">
                        <div class="card-info">{epc.get('employees', 'N/A')} employees</div>
                        <div class="card-desc">{epc.get('description', '')}</div>
                        {subs_html}
                        {website_html}
                        <div class="project-list">
                            <div style="font-weight:600;margin-bottom:0.5rem;color:var(--accent);">Projects ({total_projects})</div>
                            {projects_html if projects_html else '<div style="color:var(--text-secondary)">No project data</div>'}
                        </div>
                    </div>
                </div>'''
        return cards_html
    
    # Helper for subsidiary cards (smaller) - 含项目列表
    def generate_subsidiary_cards(subs, parent_name):
        cards_html = ""
        for sub in subs:
            partner_html = f'<div style="color:#10b981;font-size:0.75rem;margin-top:0.3rem;">🤝 {", ".join(sub.get("partner_projects", []))}</div>' if sub.get('partner_projects') else ''
            website_html = f'<a href="{sub.get("website", "")}" target="_blank" style="color:var(--accent);font-size:0.75rem;">🌐 官网</a>' if sub.get('website') else ''
            
            # 生成项目列表
            sub_projects = sub.get('projects', [])
            projects_html = ""
            for p in sub_projects:
                status_class = 'completed' if p['status'] == 'Completed' else ('ongoing' if p['status'] == 'Under Construction' else 'awarded')
                partner_info = f" (与{p['partner']}合作)" if p.get('partner') else ""
                projects_html += f'''
                    <div style="display:flex;justify-content:space-between;align-items:center;padding:0.3rem 0;border-bottom:1px solid var(--border);">
                        <span style="font-size:0.7rem;color:var(--text-primary);">{p['name']}{partner_info}</span>
                        <span style="font-size:0.65rem;background:{"#10b981" if status_class == "completed" else ("#f59e0b" if status_class == "ongoing" else "#3b82f6")};color:white;padding:1px 4px;border-radius:3px;">{p['capacity']}</span>
                    </div>'''
            
            project_count = len(sub_projects)
            project_section = f'''
                <div style="margin-top:0.5rem;padding-top:0.5rem;border-top:1px dashed var(--border);">
                    <div style="font-size:0.7rem;color:var(--accent);font-weight:600;margin-bottom:0.3rem;">📋 项目 ({project_count})</div>
                    {projects_html if projects_html else '<div style="font-size:0.7rem;color:var(--text-secondary);">暂无项目数据</div>'}
                </div>''' if sub_projects else ''
            
            cards_html += f'''
                <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:0.8rem;margin-bottom:0.5rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div style="font-weight:600;color:var(--text-primary);">{sub['name']}</div>
                        <span style="font-size:0.65rem;background:var(--accent);color:var(--bg-primary);padding:2px 6px;border-radius:4px;">{project_count} 项目</span>
                    </div>
                    <div style="font-size:0.75rem;color:var(--text-secondary);margin:0.3rem 0;">{sub.get('description', '')}</div>
                    <div style="font-size:0.75rem;color:var(--text-secondary);">{sub.get('remarks', '')}</div>
                    {partner_html}
                    {website_html}
                    {project_section}
                </div>'''
        return cards_html
    
    # 1. Vietnam Local EPC
    html += f'''
            <div class="category-section" id="vietnam-epc">
                <h3 style="color:var(--accent);margin:1.5rem 0 1rem;border-bottom:2px solid var(--accent);padding-bottom:0.5rem;">
                    🇻🇳 越南本地EPC ({len(vietnam_epc_sorted)})
                </h3>
                <div class="company-grid" id="vietnam-epc-grid">
                    {generate_epc_cards(vietnam_epc_sorted)}
                </div>
            </div>
    '''
    
    # 2. China EPC - 整合显示
    # 计算总项目数
    powerchina_total_projects = sum(len(s.get('projects', [])) for s in powerchina_subsidiaries)
    ceec_total_projects = sum(len(s.get('projects', [])) for s in ceec_subsidiaries)
    
    html += f'''
            <div class="category-section" id="china-epc">
                <h3 style="color:#dc2626;margin:1.5rem 0 1rem;border-bottom:3px solid #dc2626;padding-bottom:0.5rem;font-size:1.3rem;">
                    🇨🇳 中国EPC承包商
                </h3>
                
                <!-- 中国电建集团 -->
                <div style="background:linear-gradient(135deg,rgba(220,38,38,0.08),rgba(220,38,38,0.02));border:2px solid #dc2626;border-radius:16px;padding:1.5rem;margin-bottom:1.5rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
                        <div>
                            <h4 style="color:#dc2626;font-size:1.2rem;margin:0;">⚡ 中国电力建设集团 (PowerChina)</h4>
                            <p style="color:var(--text-secondary);font-size:0.85rem;margin:0.3rem 0 0 0;">全球最大电力建设企业 | 员工200,000+ | <a href="https://www.powerchina.cn" target="_blank" style="color:#dc2626;">🌐 官网</a></p>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:1.5rem;font-weight:700;color:#dc2626;">{powerchina_total_projects}</div>
                            <div style="font-size:0.75rem;color:var(--text-secondary);">越南/东南亚项目</div>
                        </div>
                    </div>
                    <div style="font-size:0.8rem;color:var(--text-secondary);margin-bottom:1rem;">下属设计院：华东院(HDEC)、中南院、核工院、江西院、成都院、贵阳院</div>
                    <details style="cursor:pointer;">
                        <summary style="font-weight:600;color:#dc2626;padding:0.5rem;background:rgba(220,38,38,0.1);border-radius:8px;">📋 展开查看各院项目详情 ({len(powerchina_subs_sorted)}个子公司)</summary>
                        <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:0.5rem;margin-top:1rem;">
                            {generate_subsidiary_cards(powerchina_subs_sorted, "中国电建")}
                        </div>
                    </details>
                </div>
                
                <!-- 中国能源建设集团 -->
                <div style="background:linear-gradient(135deg,rgba(37,99,235,0.08),rgba(37,99,235,0.02));border:2px solid #2563eb;border-radius:16px;padding:1.5rem;margin-bottom:1.5rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
                        <div>
                            <h4 style="color:#2563eb;font-size:1.2rem;margin:0;">🔋 中国能源建设集团 (CEEC)</h4>
                            <p style="color:var(--text-secondary);font-size:0.85rem;margin:0.3rem 0 0 0;">国家电力建设龙头 | 员工150,000+ | <a href="https://en.ceec.net.cn" target="_blank" style="color:#2563eb;">🌐 官网</a></p>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:1.5rem;font-weight:700;color:#2563eb;">{ceec_total_projects}</div>
                            <div style="font-size:0.75rem;color:var(--text-secondary);">越南/东南亚项目</div>
                        </div>
                    </div>
                    <div style="font-size:0.8rem;color:var(--text-secondary);margin-bottom:1rem;">下属设计院：广东院(GEDI)、西南院、云南院、山西院、华东院、葛洲坝、电建国际</div>
                    <details style="cursor:pointer;">
                        <summary style="font-weight:600;color:#2563eb;padding:0.5rem;background:rgba(37,99,235,0.1);border-radius:8px;">📋 展开查看各院项目详情 ({len(ceec_subs_sorted)}个子公司)</summary>
                        <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:0.5rem;margin-top:1rem;">
                            {generate_subsidiary_cards(ceec_subs_sorted, "中国能建")}
                        </div>
                    </details>
                </div>
                
                <!-- 其他中国EPC -->
                <h4 style="color:#dc2626;margin:1rem 0 0.8rem;">其他中国EPC公司</h4>
                <div class="company-grid" id="china-epc-grid">
                    {generate_epc_cards(china_epc_sorted)}
                </div>
            </div>
    '''
    
    # 3. International EPC
    html += f'''
            <div class="category-section" id="intl-epc">
                <h3 style="color:#2563eb;margin:1.5rem 0 1rem;border-bottom:2px solid #2563eb;padding-bottom:0.5rem;">
                    🌍 国际EPC ({len(international_epc_sorted)})
                </h3>
                <div class="company-grid" id="intl-epc-grid">
                    {generate_epc_cards(international_epc_sorted)}
                </div>
            </div>
    '''
    
    # 4. OEM EPC (last) - 明阳排第一
    html += f'''
            <div class="category-section" id="oem-epc">
                <h3 style="color:#f59e0b;margin:1.5rem 0 1rem;border-bottom:2px solid #f59e0b;padding-bottom:0.5rem;">
                    ⚙️ 主机厂商EPC ({len(oem_epc_sorted)})
                </h3>
                <div class="company-grid" id="oem-epc-grid">
                    {generate_epc_cards(oem_epc_sorted, show_oem_badge=True, show_oem_projects=True)}
                </div>
            </div>
        </section>
'''
    
    # Generate other sections with letter index
    def gen_section(sid, title, items, emoji):
        letters = get_letter_index(items)
        letter_btns = ''.join([f'<button class="letter-btn" onclick="filterByLetter(\'{sid}\', \'{l}\')">{l}</button>' for l in letters])
        
        cards = ""
        for c in items:
            website_html = f'<a href="{c.get("website", "")}" target="_blank" style="color:var(--info);font-size:0.7rem;">🌐</a>' if c.get('website') else ''
            country_html = f'<span style="font-size:0.65rem;color:var(--text-secondary);margin-left:5px;">{c.get("country", "")}</span>' if c.get('country') else ''
            
            # 项目列表（运输和安装公司使用）
            projects_list = c.get('projects', [])
            projects_html = ""
            if projects_list:
                projects_html = f'<div style="margin-top:0.5rem;padding-top:0.3rem;border-top:1px dashed var(--border);"><span style="font-size:0.65rem;color:var(--accent);">📋 参与项目:</span><div style="font-size:0.65rem;color:var(--text-secondary);">{", ".join(projects_list[:3])}{"..." if len(projects_list) > 3 else ""}</div></div>'
            
            cards += f'''
                <div class="simple-card" data-name="{c['name'].lower()}" data-letter="{c['name'][0].upper()}">
                    <div class="simple-logo">{c['name'][:2].upper()}</div>
                    <div class="simple-info">
                        <span class="type-badge">{c.get('type', 'N/A')}</span>{country_html} {website_html}
                        <h4>{c['name']}</h4>
                        <p>{c.get('description', '')}</p>
                        {projects_html}
                    </div>
                </div>'''
        
        return f'''
        <section id="{sid}" class="section">
            <h2 class="section-title">{emoji} {title} (A-Z)</h2>
            <div class="letter-index" id="{sid}-letters">
                <button class="letter-btn active" onclick="filterByLetter('{sid}', 'ALL')">ALL</button>
                {letter_btns}
            </div>
            <div class="simple-grid" id="{sid}-grid">{cards}</div>
        </section>
'''
    
    html += gen_section('developers', 'Developers', developers_sorted, '🌱')
    html += gen_section('oems', 'OEM / Wind Turbine', oems_sorted, '⚙️')
    html += gen_section('banks', 'Banks / Finance', banks_sorted, '🏦')
    html += gen_section('om', 'O&M Contractors', om_sorted, '🔧')
    html += gen_section('logistics', 'Logistics / Transport', logistics_sorted, '🚛')
    html += gen_section('installers', 'Installation', installers_sorted, '🔩')
    
    html += '''
    </main>
    
    <div class="modal" id="projectModal">
        <div class="modal-content">
            <div class="modal-header">
                <button class="modal-close" onclick="closeModal()">&times;</button>
                <div class="modal-title" id="modalTitle">Project Details</div>
            </div>
            <div class="modal-body" id="modalBody"></div>
        </div>
    </div>
    
    <footer>
        <p>Data: ASEAN Wind and Energy Storage Conference 2026 & Vietnam EPC Contractor List</p>
        <p>🕐 最后更新时间: <span id="lastUpdate">__UPDATE_TIME__</span></p>
        <p style="font-size: 0.75rem; color: #666;">自动更新周期: 每季度（1月/4月/7月/10月第一天）</p>
    </footer>
    
    <script>
'''
    # 替换更新时间占位符
    html = html.replace('__UPDATE_TIME__', update_time)
    
    html += f'const projectsData = {json.dumps(projects, ensure_ascii=False)};'
    html += '''
        // Tab navigation
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
                tab.classList.add('active');
                document.getElementById(tab.dataset.section).classList.add('active');
            });
        });
        
        // EPC Category Navigation - 滚动到指定分类
        function scrollToEpcSection(sectionId) {
            const element = document.getElementById(sectionId);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth', block: 'start' });
                // Update button styles
                document.querySelectorAll('.epc-cat-btn').forEach(btn => {
                    btn.style.background = 'var(--bg-secondary)';
                    btn.style.color = 'var(--text-primary)';
                });
                event.target.style.background = 'var(--accent)';
                event.target.style.color = 'var(--bg-primary)';
            }
        }
        
        // Search
        document.getElementById('searchInput').addEventListener('input', (e) => {
            const q = e.target.value.toLowerCase();
            document.querySelectorAll('.company-card, .simple-card').forEach(card => {
                const name = card.dataset.name || '';
                card.style.display = name.includes(q) ? '' : 'none';
            });
        });
        
        // Letter filter
        function filterByLetter(section, letter) {
            const grid = document.getElementById(section + '-grid');
            const btns = document.querySelectorAll('#' + section + '-letters .letter-btn');
            btns.forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            
            grid.querySelectorAll('.simple-card').forEach(card => {
                if (letter === 'ALL' || card.dataset.letter === letter) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        }
        
        // Modal
        function showModal(projectName) {
            const p = projectsData.find(x => x.project_name === projectName);
            if (!p) return;
            
            const sc = p.status === 'Completed' ? 'completed' : (p.status === 'Under Construction' ? 'ongoing' : 'awarded');
            
            document.getElementById('modalTitle').innerHTML = `${p.project_name} <span class="status-badge ${sc}">${p.status}</span>`;
            document.getElementById('modalBody').innerHTML = `
                <div class="detail-section">
                    <div class="detail-title">Basic Info</div>
                    <div class="detail-grid">
                        <div class="detail-item"><div class="detail-label">Location</div><div class="detail-value">${p.location}</div></div>
                        <div class="detail-item"><div class="detail-label">Capacity</div><div class="detail-value">${p.capacity} MW</div></div>
                        <div class="detail-item"><div class="detail-label">Type</div><div class="detail-value">${p.type}</div></div>
                        <div class="detail-item"><div class="detail-label">Year</div><div class="detail-value">${p.year}</div></div>
                    </div>
                </div>
                <div class="detail-section">
                    <div class="detail-title">Related Parties</div>
                    <div class="detail-grid">
                        <div class="detail-item"><div class="detail-label">EPC</div><div class="detail-value">${p.epc}</div></div>
                        <div class="detail-item"><div class="detail-label">Developer</div><div class="detail-value">${p.developer || 'N/A'}</div></div>
                        <div class="detail-item"><div class="detail-label">OEM</div><div class="detail-value">${p.oem || 'N/A'}</div></div>
                        <div class="detail-item"><div class="detail-label">Bank</div><div class="detail-value">${p.bank || 'N/A'}</div></div>
                        <div class="detail-item"><div class="detail-label">O&M</div><div class="detail-value">${p.om || 'N/A'}</div></div>
                        <div class="detail-item"><div class="detail-label">Installer</div><div class="detail-value">${p.installer || 'N/A'}</div></div>
                        <div class="detail-item"><div class="detail-label">Logistics</div><div class="detail-value">${p.logistics || 'N/A'}</div></div>
                    </div>
                </div>
            `;
            document.getElementById('projectModal').classList.add('active');
        }
        
        function closeModal() {
            document.getElementById('projectModal').classList.remove('active');
        }
        
        document.getElementById('projectModal').addEventListener('click', (e) => {
            if (e.target.id === 'projectModal') closeModal();
        });
        document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeModal(); });
    </script>
</body>
</html>
'''
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Dashboard created: index.html")

def generate_excel():
    """生成Excel报告供下载"""
    from datetime import datetime
    
    # 创建Excel写入器
    excel_file = 'Vietnam_Renewable_Energy_Report.xlsx'
    
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        # 1. EPC承包商
        epc_data = []
        for epc in epc_companies:
            project_list = [p['project_name'] for p in projects if p['epc'] == epc['name']]
            epc_data.append({
                '公司名称': epc['name'],
                '国家': epc.get('country', 'N/A'),
                '地址': epc.get('address', 'N/A'),
                '员工数': epc.get('employees', 'N/A'),
                '官网': epc.get('website', 'N/A'),
                '项目数量': len(project_list),
                '项目列表': ', '.join(project_list) if project_list else 'N/A',
                '其他业务': epc.get('other_biz', 'N/A'),
                '备注': epc.get('remarks', 'N/A')
            })
        pd.DataFrame(epc_data).to_excel(writer, sheet_name='EPC承包商', index=False)
        
        # 2. 项目信息
        project_data = []
        for p in projects:
            project_data.append({
                '项目名称': p['project_name'],
                'EPC承包商': p['epc'],
                '位置': p['location'],
                '容量(MW)': p['capacity'],
                '类型': p['type'],
                '状态': p['status'],
                '年份': p['year'],
                '开发商': p.get('developer', 'N/A'),
                '主机厂商': p.get('oem', 'N/A'),
                '银行': p.get('bank', 'N/A'),
                '运维': p.get('om', 'N/A'),
                '安装商': p.get('installer', 'N/A'),
                '物流': p.get('logistics', 'N/A')
            })
        pd.DataFrame(project_data).to_excel(writer, sheet_name='项目信息', index=False)
        
        # 3. 开发商
        dev_data = [{'公司名称': d['name'], '国家': d.get('country', 'N/A'), 
                     '官网': d.get('website', 'N/A'), '备注': d.get('remarks', 'N/A')} 
                    for d in developers]
        pd.DataFrame(dev_data).to_excel(writer, sheet_name='开发商', index=False)
        
        # 4. 主机厂商
        oem_data = [{'公司名称': o['name'], '国家': o.get('country', 'N/A'),
                     '官网': o.get('website', 'N/A'), '产品': o.get('products', 'N/A')} 
                    for o in oems]
        pd.DataFrame(oem_data).to_excel(writer, sheet_name='主机厂商(OEM)', index=False)
        
        # 5. 银行
        bank_data = [{'银行名称': b['name'], '国家': b.get('country', 'N/A'),
                      '官网': b.get('website', 'N/A'), '业务范围': b.get('focus', 'N/A')} 
                     for b in banks]
        pd.DataFrame(bank_data).to_excel(writer, sheet_name='银行金融', index=False)
        
        # 6. 运维厂商
        om_data = [{'公司名称': o['name'], '国家': o.get('country', 'N/A'),
                    '官网': o.get('website', 'N/A'), '服务': o.get('services', 'N/A')} 
                   for o in om_contractors]
        pd.DataFrame(om_data).to_excel(writer, sheet_name='运维厂商(O&M)', index=False)
        
        # 7. 物流厂商
        log_data = [{'公司名称': l['name'], '国家': l.get('country', 'N/A'),
                     '官网': l.get('website', 'N/A'), '服务': l.get('services', 'N/A')} 
                    for l in logistics_companies]
        pd.DataFrame(log_data).to_excel(writer, sheet_name='物流运输', index=False)
        
        # 8. 安装厂商
        inst_data = [{'公司名称': i['name'], '国家': i.get('country', 'N/A'),
                      '官网': i.get('website', 'N/A'), '服务': i.get('services', 'N/A')} 
                     for i in installers]
        pd.DataFrame(inst_data).to_excel(writer, sheet_name='安装厂商', index=False)
    
    print(f"Excel report created: {excel_file}")

if __name__ == "__main__":
    print("="*50)
    print("Vietnam Renewable Energy Dashboard Generator V2")
    print("="*50)
    generate_html()
    generate_excel()
    print("="*50)
    print("Done!")
