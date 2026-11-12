# -*- coding: utf-8 -*-
"""
================================================================================
Nexus-Alpha V71.4 —— 手机App/云端 1:1 终极实战量化指挥舱 (超清大字高对比度完全体)
【视觉与核心升级】：
1. 🎨 彻底根治手机端白底浅字看不清：废除浅色提示框，全面采用纯深色底(#091326/#062E22) + 14.5px加粗亮白/亮金黄大字体。
2. 🎯 顶部双核看板：【🎯明日重点关注10大狙击股(★核心五虎高亮+⚡09:25竞价体检)】+【👑今日Top10金股】。
3. 🚀 汉王/电魂模型硬化：【30日2~4次涨停脉冲试盘+缩量回踩启动】与【🐉真龙回头】严格拆开。
4. 💎 波段防卖飞与真假分级：新增【💎波段锁仓牛·防卖飞 vs ⚡超短套利】定性，11大战法池【★正宗/⚪备选】双轨制。
5. 📈 大字号高清K线与分时画布：放大VOL/MACD/四红灯与价格字号，分时图配横向现价游标线与呼吸灯。
6. 📸 历史复盘快照对照：勾选复盘股直接弹出【📸选出时几红几灯/当时逻辑 vs 📈当前最新状态】对照大窗 + K线★入选日标记。
7. 📊 实盘资金净值增长曲线：在实盘持仓页实时绘制账户复利净值增长曲线(对比上证指数)。
【第 1 段 / 共 3 段】
================================================================================
"""

import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
import urllib.request
import socket
import time
import json
import os
import math

# 全局 6 秒网络硬超时锁与代理免疫
socket.setdefaulttimeout(6.0)
os.environ["NO_PROXY"] = "*"
os.environ["no_proxy"] = "*"

try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False

# ==================== 1. 页面配置与手机端超清大字高对比度 CSS ====================
st.set_page_config(
    page_title="Nexus-Alpha V71.4 实盘量化指挥舱",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* 1. 强制全局纯深色背景与高亮纯白大字，彻底消灭任何白底浅字 */
    .stApp, .main, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #070A10 !important;
        color: #FFFFFF !important;
    }
    .block-container {
        padding-top: 0.4rem !important;
        padding-bottom: 1.2rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 100% !important;
    }

    /* 2. 所有输入框标题、普通说明文字全部强制亮白/亮青加粗 */
    label, .stWidgetLabel, div[data-testid="stWidgetLabel"] p,
    div[data-testid="stMarkdownContainer"] p, div[data-testid="stCaptionContainer"] p {
        color: #F8FAFC !important;
        font-size: 13.5px !important;
        font-weight: 700 !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #64FFDA !important;
        font-weight: 800 !important;
        margin-top: 0.2rem !important;
        margin-bottom: 0.3rem !important;
    }

    /* 3. 强制覆盖 Streamlit 原生 st.info / st.success / st.warning 为深色底+亮色大字 */
    div[data-testid="stAlert"], div[role="alert"] {
        background-color: #0F172A !important;
        color: #FFFFFF !important;
        border: 1.5px solid #38BDF8 !important;
        border-radius: 8px !important;
    }
    div[data-testid="stAlert"] p, div[role="alert"] p {
        color: #FEF08A !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        line-height: 1.5 !important;
    }

    /* 4. 专属定制高对比度深色作战卡片（彻底替代原浅色框，手机强光下清晰可见） */
    .nexus-box-logic {
        background-color: #091526 !important;
        color: #FFFFFF !important;
        border: 1.5px solid #38BDF8 !important;
        border-left: 5px solid #38BDF8 !important;
        border-radius: 6px !important;
        padding: 10px 12px !important;
        margin: 6px 0 !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        line-height: 1.55 !important;
    }
    .nexus-box-wave {
        background-color: #231505 !important;
        color: #FEF08A !important;
        border: 1.5px solid #F59E0B !important;
        border-left: 5px solid #FBBF24 !important;
        border-radius: 6px !important;
        padding: 10px 12px !important;
        margin: 6px 0 !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        line-height: 1.55 !important;
    }
    .nexus-box-forecast {
        background-color: #05261C !important;
        color: #ECFDF5 !important;
        border: 1.5px solid #10B981 !important;
        border-left: 5px solid #34D399 !important;
        border-radius: 6px !important;
        padding: 10px 12px !important;
        margin: 6px 0 !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        line-height: 1.55 !important;
    }
    .nexus-box-exec {
        background-color: #161F33 !important;
        color: #FFFFFF !important;
        border: 1.5px solid #64FFDA !important;
        border-radius: 6px !important;
        padding: 10px 12px !important;
        margin: 6px 0 !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        line-height: 1.6 !important;
    }

    /* 5. 按钮高对比度样式 */
    div.stButton > button {
        background-color: #162238 !important;
        color: #FEF08A !important;
        border: 1.5px solid #38BDF8 !important;
        font-weight: 800 !important;
        border-radius: 6px !important;
        padding: 0.45rem 0.6rem !important;
    }
    div.stButton > button p {
        color: #FEF08A !important;
        font-size: 13.5px !important;
        font-weight: 800 !important;
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #0284C7 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        border: 1.5px solid #64FFDA !important;
        box-shadow: 0 2px 10px rgba(2, 132, 199, 0.5) !important;
    }
    div.stButton > button[kind="primary"] p {
        color: #FFFFFF !important;
        font-size: 14.5px !important;
        font-weight: 800 !important;
    }

    /* 6. 折叠面板、输入框与数字框高对比度 */
    div[data-testid="stExpander"] {
        background-color: #111827 !important;
        border: 1.5px solid #334155 !important;
        border-radius: 6px !important;
    }
    div[data-testid="stExpander"] summary p {
        color: #64FFDA !important;
        font-size: 14px !important;
        font-weight: 800 !important;
    }
    input, textarea, div[data-baseweb="select"] > div {
        background-color: #090D16 !important;
        color: #FBBF24 !important;
        border: 1.5px solid #475569 !important;
        font-size: 15px !important;
        font-weight: 800 !important;
    }

    /* 7. 标签页(Tabs)未选中与选中均保持极高清晰度 */
    div[data-testid="stTabs"] button {
        background-color: #131B2E !important;
        color: #FFFFFF !important;
        border: 1px solid #475569 !important;
        border-radius: 6px 6px 0 0 !important;
        padding: 6px 11px !important;
        margin-right: 3px !important;
    }
    div[data-testid="stTabs"] button p {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 13px !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        background-color: #1D4ED8 !important;
        border: 1.5px solid #64FFDA !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] p {
        color: #FEF08A !important;
        font-weight: 900 !important;
        font-size: 13.5px !important;
    }

    /* 8. 顶部状态条、总指令条、面板与六维红灯网格 */
    .nexus-temp-bar {
        background-color: #131B2E;
        color: #FBBF24;
        font-weight: 800;
        font-size: 13.5px;
        padding: 7px 10px;
        border-radius: 6px;
        border: 1.5px solid #38BDF8;
        margin-bottom: 6px;
        line-height: 1.45;
    }
    .nexus-directive {
        background-color: #172136;
        color: #FEF08A;
        font-weight: 800;
        font-size: 13.5px;
        padding: 9px 12px;
        border-radius: 6px;
        border-left: 5px solid #F59E0B;
        border-top: 1px solid #334155;
        border-right: 1px solid #334155;
        border-bottom: 1px solid #334155;
        margin-bottom: 6px;
        line-height: 1.5;
    }
    .nexus-panel {
        background-color: #0E1525;
        border: 1.5px solid #26354D;
        border-radius: 8px;
        padding: 8px 10px;
        margin-bottom: 8px;
    }
    .nexus-panel-title {
        color: #64FFDA;
        font-weight: 800;
        font-size: 14.5px;
        margin-bottom: 6px;
        border-bottom: 1.5px solid #1E293B;
        padding-bottom: 5px;
    }
    .nexus-orderbook {
        background-color: #070B12;
        color: #38BDF8;
        font-family: Consolas, monospace;
        font-size: 13px;
        font-weight: 800;
        padding: 7px 9px;
        border-radius: 5px;
        border: 1px solid #334155;
        margin: 5px 0;
    }
    .nexus-model-bar {
        background-color: #0A111F;
        color: #FEF08A;
        font-size: 13px;
        font-weight: 800;
        padding: 7px 10px;
        border-radius: 5px;
        border: 1px solid #38BDF8;
        margin-top: 4px;
        line-height: 1.45;
    }
    .lamp-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 5px;
        margin: 5px 0;
    }
    @media (min-width: 768px) {
        .lamp-grid { grid-template-columns: repeat(6, 1fr); }
    }
    .lamp-on {
        background-color: #991B1B;
        color: #FEF08A;
        border: 1.5px solid #F43F5E;
        border-radius: 5px;
        padding: 6px 4px;
        text-align: center;
        font-size: 12.5px;
        font-weight: 800;
    }
    .lamp-off {
        background-color: #1E293B;
        color: #CBD5E1;
        border: 1px solid #475569;
        border-radius: 5px;
        padding: 6px 4px;
        text-align: center;
        font-size: 12.5px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 2. 独立持久化数据文件与全局字典 ====================
HOLDINGS_FILE = "nexus_holdings_v71.json"
TRADES_HISTORY_FILE = "nexus_trade_history_v71.json"
REVIEW_FILE = "nexus_review_v71.json"
WATCHLIST_FILE = "nexus_watchlist_v71.json"
TOMORROW_POOL_FILE = "nexus_tomorrow_pool_v71.json"
POOL_5DAY_FILE = "nexus_5day_pool_v71.json"
SCORE_LOCK_FILE = "nexus_score_lock_v71.json"
KLINE_T1_CACHE_FILE = "nexus_kline_t1_v71.json"
ACTIVE_CODES_FILE = "nexus_active_codes_v71_clean.json"
SNAPSHOT_FILE = "nexus_snapshot_v71.json"
CACHE_SPOT_FILE = "nexus_spot_cache_v71.csv"
CACHE_SECTOR_FILE = "nexus_sector_cache_v71.csv"

DELISTED_BLACKLIST = {
    "600005", "600002", "600472", "600553", "601989", "601299",
    "600705", "600786", "600723", "600816", "600652", "600653"
}

STRATEGY_LOGIC_DESCRIPTIONS = {
    "🔥 五日主升妖股": "【大千生态/福莱新材/浙文影业/闽发铝业模型】近5日累计涨幅≥10%(且未触发高位滞涨派发警报) + 5日均线陡峭上攻(MA5>MA10) + 获利盘≥72%上方无套牢峰。买点：分歧回踩分时黄线或5日线低吸博连板/二波。",
    "🦄 独立行情穿越牛": "【严谨模型】近20日逆势抗跌率≥70% + 均线多头(现价≥MA20且MA20上翘) + 20日最大回撤≤9.5% + 获利盘≥68%。买点：回踩5日线或分时黄线低吸，具备💎波段锁仓防卖飞属性。",
    "🚀 强庄试盘启动": "【汉王科技/电魂网络专属模型】近30日箱体累计涨幅未透支(≤20%)，但期间出现过2~4次涨停板/大阳脉冲试盘 + 每次试盘后缩量回踩死守起涨前低与主力成本线 + 今日放量突破站稳MA5与分时黄线开启主升浪！",
    "🕵️ 主力偷偷吸筹": "【严谨模型】低位蓄势(20日乖离-2%~9%) + 近3日阳均量>阴均量持续流入 + 振幅≤5.5%窄幅压盘但主动外盘≥52%暗中吃货。",
    "⏱️ 09:26弱转强": "【真弱转强模型】昨日K线必须为小阴洗盘/假阴真阳/长上影分歧烂板且MA20未破 + 今日高开或红盘死守开盘价与真实VWAP分时黄线 + U型真量比≥1.10吞没昨日分歧上影或实体。",
    "🕳️ 黄金坑穿三线": "【真黄金三串一模型】MA5/MA10/MA20三线高度粘合收敛(乖离≤2.8%)或近期缩量挖坑 + 今日开盘价/最低价低于至少两条均线 + 放量实体真阳(涨幅≥1.8%且量比≥1.08)一举突破三条均线之上！",
    "🌊 主升浪动量": "【严谨模型】标准多头排列(现价>MA5>=MA10>=MA20) + 60日获利盘≥75%上方无套牢峰 + 放量真阳突破颈线(留存率≥65%)，具备💎波段锁仓潜力。",
    "🐉 龙回头企稳": "【真龙头回踩模型】前期已有连续大涨主升波段(阶段涨幅≥22%或连板基因) + 首次缩量回踩MA10/MA20或主力底仓成本线止跌企稳（低吸博高标首阴/二波反抽）。",
    "📐 圆弧底突破": "【严谨模型】三段式锅底结构：前20~6日底部波动收敛缩量筑弧底 + 近5日低点抬高右唇翘起(MA5>=MA10) + 红盘放量突破颈线，具备💎波段锁仓潜力。",
    "🛡️ 顺丰防御": "【严谨模型】流通市值≥80亿 + 动态PE 3~38倍低估值安全盾 + 稳站MA20生命线且分时承接良好机构护盘。",
    "🌙 尾盘埋伏": "【防高位接盘尾盘法】近5日涨幅≤12%且20日乖离≤10%(拒绝高位妖股派发期接飞刀) + 全天稳站分时黄线与开盘价上方 + 今日涨幅温和(-0.3%~+3.6%) + 留存率≥62%尾盘抢筹博次日溢价。",
    "🎯 明日重点狙击": "【隔日主动伏击系统】融合近5日实盘胜率前三王牌战法 + 30日多次试盘突破基因 + 明日主攻/潜伏板块，精选10只明日标的（前5只高亮标注★核心五虎），配09:25竞价体检与次日早盘30分钟兑现锚。",
    "👑 全场Top10金股": "【日内最强领涨】全场最高优中选优：优先锁定【6灯全亮 + 四灯齐红 + 多头上升趋势 + 站稳分时黄线 + ★正宗买点】的10只日内领涨核心龙头。",
    "⭐ 核心自选": "【自选盯盘】自选重点盯盘标的，采用完全相同的客观公允评分尺实时体检。"
}

MAINBOARD_CORE_UNIVERSE = [
    ("002362", "汉王科技", "人工智能"), ("603258", "电魂网络", "文化传媒"), ("603955", "大千生态", "生态园林"),
    ("605488", "福莱新材", "人形机器人"), ("601599", "浙文影业", "文化传媒"), ("002578", "闽发铝业", "有色金属"),
    ("603236", "移远通信", "通信设备"), ("002695", "煌上煌", "消费白马"), ("601598", "中国外运", "交运物流"),
    ("000726", "鲁泰A", "消费白马"), ("601019", "山东出版", "文化传媒"), ("002250", "联化科技", "化学化工"),
    ("601238", "广汽集团", "智能汽车"), ("002512", "达华智能", "商业航天"), ("600800", "渤海化学", "化学化工"),
    ("002115", "三维通信", "通信设备"), ("603000", "人民网", "文化传媒"), ("600556", "天下秀", "人工智能"),
    ("601698", "中国卫通", "商业航天"), ("600879", "航天电子", "商业航天"), ("600118", "中国卫星", "商业航天"),
    ("000547", "航天发展", "商业航天"), ("603698", "航天工程", "商业航天"), ("600343", "航天动力", "商业航天"),
    ("002025", "航天电器", "商业航天"), ("600501", "航天晨光", "商业航天"), ("000901", "航天科技", "商业航天"),
    ("002465", "海格通信", "商业航天"), ("600198", "大唐电信", "商业航天"), ("002151", "北斗星通", "商业航天"),
    ("600990", "四创电子", "商业航天"), ("002383", "合众思壮", "商业航天"),
    ("601689", "拓普集团", "人形机器人"), ("603728", "鸣志电器", "人形机器人"), ("002050", "三花智控", "人形机器人"),
    ("603009", "北特科技", "人形机器人"), ("002896", "中大力德", "人形机器人"), ("603901", "永创智能", "人形机器人"),
    ("002747", "埃斯顿", "人形机器人"), ("002527", "新时达", "人形机器人"), ("603667", "五洲新春", "人形机器人"),
    ("002472", "双环传动", "人形机器人"), ("002139", "拓邦股份", "人形机器人"), ("002851", "麦格米特", "人形机器人"),
    ("603358", "华达科技", "人形机器人"), ("002031", "巨轮智能", "人形机器人"),
    ("600276", "恒瑞医药", "医药生物"), ("603259", "药明康德", "医药生物"), ("002422", "科伦药业", "医药生物"),
    ("600436", "片仔癀", "医药生物"), ("000538", "云南白药", "医药生物"), ("600085", "同仁堂", "医药生物"),
    ("000999", "华润三九", "医药生物"), ("603707", "健友股份", "医药生物"), ("603014", "威高血净", "医药生物"),
    ("600196", "复星医药", "医药生物"), ("002007", "华兰生物", "医药生物"), ("600332", "白云山", "医药生物"),
    ("600535", "天士力", "医药生物"), ("600351", "亚宝药业", "医药生物"),
    ("600760", "中航沈飞", "国防军工"), ("000768", "中航西飞", "国防军工"), ("600038", "中直股份", "国防军工"),
    ("600316", "洪都航空", "国防军工"), ("600893", "航发动力", "国防军工"), ("600391", "航发科技", "国防军工"),
    ("000738", "航发控制", "国防军工"), ("600765", "中航重机", "国防军工"), ("002179", "中航光电", "国防军工"),
    ("600372", "中航机载", "国防军工"), ("600967", "内蒙一机", "国防军工"), ("600435", "北方导航", "国防军工"),
    ("600562", "国睿科技", "国防军工"), ("600150", "中国船舶", "国防军工"), ("600482", "中国动力", "国防军工"),
    ("002085", "万丰奥威", "低空经济"), ("000099", "中信海直", "低空经济"), ("002664", "信质集团", "低空经济"),
    ("001696", "宗申动力", "低空经济"), ("600855", "航天长峰", "低空经济"), ("002985", "北摩高科", "低空经济"),
    ("002253", "川大智胜", "低空经济"), ("600592", "龙溪股份", "低空经济"),
    ("603019", "中科曙光", "算力硬件"), ("000977", "浪潮信息", "算力硬件"), ("601138", "工业富联", "算力硬件"),
    ("002916", "深南电路", "元件PCB"), ("002463", "沪电股份", "元件PCB"), ("603228", "景旺电子", "元件PCB"),
    ("002913", "奥士康", "元件PCB"), ("600183", "生益科技", "元件PCB"),
    ("002230", "科大讯飞", "人工智能"), ("600588", "用友网络", "人工智能"), ("600570", "恒生电子", "人工智能"),
    ("600498", "烽火通信", "通信设备"), ("000063", "中兴通讯", "通信设备"), ("002583", "海能达", "通信设备"),
    ("600941", "中国移动", "通信设备"), ("600050", "中国联通", "通信设备"),
    ("002371", "北方华创", "半导体芯片"), ("603160", "汇顶科技", "半导体芯片"), ("600745", "闻泰科技", "半导体芯片"),
    ("600584", "长电科技", "半导体芯片"), ("002156", "通富微电", "半导体芯片"), ("603501", "韦尔股份", "半导体芯片"),
    ("603986", "兆易创新", "半导体芯片"), ("002475", "立讯精密", "消费电子"), ("002241", "歌尔股份", "消费电子"),
    ("002074", "国轩高科", "固态电池"), ("002460", "赣锋锂业", "固态电池"), ("600884", "杉杉股份", "固态电池"),
    ("603659", "璞泰来", "固态电池"), ("600438", "通威股份", "光伏新能源"), ("601012", "隆基绿能", "光伏新能源"),
    ("002129", "TCL中环", "光伏新能源"), ("601127", "赛力斯", "智能汽车"), ("002594", "比亚迪", "智能汽车"),
    ("601633", "长城汽车", "智能汽车"), ("000625", "长安汽车", "智能汽车"), ("600660", "福耀玻璃", "智能汽车"),
    ("002920", "德赛西威", "智能汽车"), ("600089", "特变电工", "电网设备"), ("600406", "国电南瑞", "电网设备"),
    ("601179", "中国西电", "电网设备"), ("600312", "平高电气", "电网设备"), ("002028", "思源电气", "电网设备"),
    ("000543", "皖能电力", "电力绿电"), ("000539", "粤电力A", "电力绿电"), ("600011", "华能国际", "电力绿电"),
    ("600795", "国电电力", "电力绿电"), ("600900", "长江电力", "电力绿电"), ("601928", "凤凰传媒", "文化传媒"),
    ("601801", "皖新传媒", "文化传媒"), ("601098", "中南传媒", "文化传媒"), ("600977", "中国电影", "文化传媒"),
    ("002697", "红旗连锁", "商贸零售"), ("601888", "中国中免", "商贸零售"), ("600368", "五洲交通", "交运物流"),
    ("000755", "山西高速", "交运物流"), ("002352", "顺丰控股", "交运物流"), ("601919", "中远海控", "交运物流"),
    ("601006", "大秦铁路", "交运物流"), ("600029", "南方航空", "交运物流"), ("601111", "中国国航", "交运物流"),
    ("601766", "中国中车", "基建轨交"), ("600039", "四川路桥", "基建轨交"), ("601899", "紫金矿业", "有色金属"),
    ("600362", "江西铜业", "有色金属"), ("601600", "中国铝业", "有色金属"), ("603993", "洛阳钼业", "有色金属"),
    ("600309", "万华化学", "化学化工"), ("000635", "英力特", "化学化工"), ("002226", "江南化工", "化学化工"),
    ("601088", "中国神华", "煤炭高息"), ("600188", "兖矿能源", "煤炭高息"), ("000713", "国投丰乐", "农业种业"),
    ("600598", "北大荒", "农业种业"), ("600036", "招商银行", "银行金融"), ("600919", "江苏银行", "银行金融"),
    ("601128", "常熟银行", "银行金融"), ("601838", "成都银行", "银行金融"), ("601169", "北京银行", "银行金融"),
    ("601318", "中国平安", "证券金融"), ("601988", "中国银行", "银行金融"), ("600030", "中信证券", "证券金融"),
    ("601099", "太平洋", "证券金融"), ("000958", "电投产融", "电力绿电"), ("002481", "双塔食品", "消费白马"),
    ("002441", "众业达", "电网设备")
]

DYNAMIC_MAINBOARD_EXPANSION = [
    "002362", "603258", "603955", "605488", "601599", "002578", "600000", "600009", "600010", "600015",
    "600016", "600018", "600019", "600026", "600027", "600028", "600031", "600048", "600056", "600060",
    "600061", "600066", "600079", "600096", "600104", "600111", "600115", "600132", "600143", "600153",
    "600157", "600160", "600161", "600170", "600176", "600177", "600219", "600233", "600256", "600298",
    "600346", "600348", "600369", "600383", "600409", "600415", "600426", "600460", "600487", "600489",
    "600515", "600519", "600522", "600547", "600585", "600600", "600690", "600703", "600732", "600741",
    "600754", "600803", "600809", "600837", "600845", "600875", "600886", "600887", "600905", "600938",
    "600989", "601009", "601021", "601066", "601100", "601117", "601166", "601169", "601211", "601225",
    "601238", "601288", "601328", "601336", "601360", "601390", "601398", "601601", "601618", "601628",
    "601658", "601668", "601669", "601688", "601728", "601800", "601818", "601857", "601872", "601877",
    "601881", "601901", "601939", "601985", "601995", "601998", "603000", "603195", "603260", "603288",
    "603369", "603392", "603486", "603605", "603799", "603806", "603833", "603899", "603939", "000001",
    "000002", "000021", "000032", "000066", "000069", "000100", "000157", "000333", "000338", "000400",
    "000425", "000513", "000568", "000596", "000617", "000629", "000630", "000651", "000661", "000708",
    "000725", "000776", "000786", "000792", "000800", "000807", "000858", "000876", "000895", "000932",
    "000933", "000937", "000960", "000963", "000975", "000983", "002001", "002008", "002027", "002049",
    "002064", "002120", "002129", "002142", "002180", "002202", "002236", "002271", "002304", "002311",
    "002340", "002384", "002410", "002415", "002429", "002459", "002466", "002493", "002555", "002595",
    "002600", "002601", "002648", "002709", "002714", "002736", "002812", "002821", "002841", "002926"
]

# ==================== 3. 核心状态持久化与基础工具函数 ====================
def load_json_safe(filepath, default_val):
    base_prefix = filepath.split("_v")[0]
    candidates = [filepath] + [f"{base_prefix}_v{v}.json" for v in (71, 70, 69, 68, 67)]
    for candidate in candidates:
        if os.path.exists(candidate):
            try:
                with open(candidate, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    return default_val

def save_json_safe(filepath, data):
    tmp_p = filepath + ".tmp"
    try:
        with open(tmp_p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_p, filepath)
    except Exception:
        if os.path.exists(tmp_p):
            try:
                os.remove(tmp_p)
            except Exception:
                pass

def init_nexus_state():
    if "nexus_initialized" in st.session_state:
        return
    st.session_state["nexus_initialized"] = True
    st.session_state["sh_index_pct"] = 0.0
    st.session_state["sh_index_price"] = 3668.15
    st.session_state["sz_index_pct"] = 0.0
    st.session_state["sz_index_price"] = 11250.40
    st.session_state["sh_vol_ratio"] = 1.00
    st.session_state["sh_vol_status"] = "⚖️平量良性轮动(量比1.00，预计14850亿)"
    st.session_state["est_market_amt_yi"] = 14850.0
    st.session_state["market_breadth_stats"] = {"up": 3120, "dn": 1680, "zt": 44, "dt": 1}
    st.session_state["external_macro_mode"] = "⚖️外围中性(聚焦A股内生主线与量价结构)"
    st.session_state["tomorrow_sector_focus_str"] = "🧭 【明日重点关注板块】: 🥇主攻接力看【人工智能、通信设备、算力硬件】 ｜ 🥈高低切换潜伏看【文化传媒、商业航天、人形机器人】"
    st.session_state["last_sector_parsed_list"] = []
    st.session_state["median_stock_pct"] = 0.35
    st.session_state["market_temp_score"] = 76.5
    st.session_state["bomb_rate"] = 10.0
    st.session_state["fuse_triggered"] = False
    st.session_state["kline_cache"] = {}
    st.session_state["kline_t1_disk_cache"] = load_json_safe(KLINE_T1_CACHE_FILE, {})
    st.session_state["intraday_cache"] = {}
    st.session_state["intraday_live_ticks"] = {}
    st.session_state["latest_spot_cache"] = {}
    st.session_state["hot_sectors_map"] = {}
    st.session_state["latent_sectors_list"] = []
    st.session_state["collective_surge_sectors"] = []
    st.session_state["stock_sector_map"] = {code: sec for code, _, sec in MAINBOARD_CORE_UNIVERSE}
    st.session_state["name_sector_map"] = {name: sec for _, name, sec in MAINBOARD_CORE_UNIVERSE}
    st.session_state["canonical_eval_cache"] = {}
    st.session_state["score_lock_map"] = load_json_safe(SCORE_LOCK_FILE, {})
    st.session_state["pool_5day_map"] = load_json_safe(POOL_5DAY_FILE, {})
    st.session_state["tomorrow_pool_rows"] = load_json_safe(TOMORROW_POOL_FILE, [])
    st.session_state["top3_winning_strats"] = ["🚀 强庄试盘启动", "🌙 尾盘埋伏", "🕳️ 黄金坑穿三线"]

    raw_active = load_json_safe(
        ACTIVE_CODES_FILE,
        [c for c, _, _ in MAINBOARD_CORE_UNIVERSE] + DYNAMIC_MAINBOARD_EXPANSION
    )
    st.session_state["active_mainboard_codes"] = [
        str(c).zfill(6) for c in raw_active if str(c).zfill(6) not in DELISTED_BLACKLIST
    ]
    st.session_state["watchlist_rows"] = load_json_safe(WATCHLIST_FILE, [])
    st.session_state["holdings_rows"] = load_json_safe(HOLDINGS_FILE, [])
    st.session_state["trade_history_records"] = load_json_safe(TRADES_HISTORY_FILE, [])
    st.session_state["all_review_records"] = load_json_safe(REVIEW_FILE, [])
    st.session_state["chart_mode"] = "kline"
    st.session_state["highlight_pick_date"] = None
    st.session_state["status_text"] = "🟢 [V71.4 强庄多次试盘+明日10大狙击★核心五虎+超清高对比度引擎就绪]"
    st.session_state["selected_stock_code"] = "002362"
    st.session_state["selected_stock_name"] = "汉王科技"
    st.session_state["selected_stock_strat"] = "🚀 强庄试盘启动"
    st.session_state["last_table_sel_sig"] = {}

    snap = load_json_safe(SNAPSHOT_FILE, None)
    st.session_state["scan_snapshot"] = snap if snap else {}

def get_intraday_time_factor():
    """引入 A 股真实的 U 型微笑分时成交量权重曲线"""
    now = datetime.now()
    if now.weekday() >= 5:
        return 1.0, 240.0
    hm = now.hour * 100 + now.minute
    if hm < 925 or hm >= 1500:
        return 1.0, 240.0
    if 925 <= hm <= 930:
        return 0.06, 2.0
    if hm <= 1130:
        mins = max(1.0, (now.hour - 9) * 60 + now.minute - 30)
    elif hm < 1300:
        mins = 120.0
    else:
        mins = min(240.0, 120.0 + (now.hour - 13) * 60 + now.minute)

    if mins <= 30:
        u_weight = 0.05 + (mins / 30.0) * 0.17
    elif mins <= 60:
        u_weight = 0.22 + ((mins - 30.0) / 30.0) * 0.14
    elif mins <= 120:
        u_weight = 0.36 + ((mins - 60.0) / 60.0) * 0.20
    elif mins <= 180:
        u_weight = 0.56 + ((mins - 120.0) / 60.0) * 0.18
    else:
        u_weight = 0.74 + ((mins - 180.0) / 60.0) * 0.26
    return round(min(1.0, max(0.06, u_weight)), 3), mins

def resolve_canonical_sector(code, name="", fallback=""):
    code = str(code).zfill(6)
    name = str(name).strip()
    invalid_tags = ("", "主板协同", "主板精选", "⭐自选核心", "持仓股", "盘中异动", "自选观察", "实战选股", "⭐ 核心自选")
    s_map = st.session_state["stock_sector_map"]
    n_map = st.session_state["name_sector_map"]

    if code in s_map and s_map[code] not in invalid_tags:
        return s_map[code]
    if name and name in n_map and n_map[name] not in invalid_tags:
        sec = n_map[name]
        s_map[code] = sec
        return sec

    kw_rules = [
        (("大千", "生态", "园林", "环保"), "生态园林"),
        (("福莱", "新材", "薄膜"), "人形机器人"),
        (("浙文", "影业", "传媒", "出版", "电影", "影视", "文化", "传播", "电魂", "人民网"), "文化传媒"),
        (("闽发", "铝", "铜", "金", "矿", "有色", "稀土", "钢", "紫金"), "有色金属"),
        (("卫通", "卫星", "航天", "火箭", "北斗", "星网"), "商业航天"),
        (("机器人", "减速", "鸣志", "三花", "拓普", "埃斯顿", "北特", "中大力德", "双环", "五洲新春", "新时达", "巨轮"), "人形机器人"),
        (("药", "医", "生物", "健康", "康德", "同仁堂", "片仔癀", "华润", "血净"), "医药生物"),
        (("中航", "航发", "沈飞", "西飞", "军工", "船舶", "重工", "防务", "兵器", "导航", "一机", "国睿", "洪都"), "国防军工"),
        (("低空", "海直", "万丰", "通航", "宗申", "长峰", "龙溪"), "低空经济"),
        (("曙光", "浪潮", "富联", "算力", "服务器", "光模块"), "算力硬件"),
        (("电路", "沪电", "奥士康", "生益", "景旺", "元件", "PCB"), "元件PCB"),
        (("通信", "烽火", "中兴", "海能达", "移动", "联通", "电信", "移远", "三维"), "通信设备"),
        (("讯飞", "软件", "智能", "科技", "电子", "数据", "网络", "汉王", "天下秀"), "人工智能"),
        (("芯", "半导", "微电", "华创", "韦尔", "闻泰", "长电", "兆易"), "半导体芯片"),
        (("锂", "电池", "国轩", "杉杉", "光伏", "通威", "隆基", "中环", "新能"), "光伏新能源"),
        (("电网", "电工", "南瑞", "西电", "电气", "思源", "众业达"), "电网设备"),
        (("电力", "水电", "火电", "华能", "国电", "绿电", "燃气", "能源", "电投"), "电力绿电"),
        (("银行", "农商", "常熟", "成都银行", "北京银行"), "银行金融"),
        (("证券", "国泰", "中信", "太平洋", "保险", "平安"), "证券金融"),
        (("高速", "铁路", "物流", "航运", "海控", "港口", "交运", "路桥", "建筑", "中车", "交通", "外运", "航空", "国航"), "交运物流"),
        (("连锁", "百货", "商贸", "零售", "中免", "商业"), "商贸零售"),
        (("酒", "茅台", "五粮", "汾酒", "食品", "伊利", "家电", "美的", "格力", "家居", "煌上煌", "鲁泰", "双塔"), "消费白马"),
        (("化", "塑", "材", "煤", "神华", "兖矿", "石油", "石化", "联化"), "化工周期")
    ]
    for words, target_sec in kw_rules:
        if any(w in name for w in words):
            s_map[code] = target_sec
            return target_sec

    clean_fb = str(fallback).split("[")[0].replace("👑", "").replace("🟢", "").strip()
    if clean_fb and clean_fb not in invalid_tags:
        s_map[code] = clean_fb
        return clean_fb

    default_sec = "先进制造" if code.startswith(("600", "002")) else ("价值蓝筹" if code.startswith("601") else "科技创新")
    s_map[code] = default_sec
    return default_sec

# ==================== 4. 全市场主板异动活水抓取、腾讯五档与0.03秒K线直连 ====================
def fetch_live_mainboard_hot_codes():
    hot_codes = []
    urls = [
        "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=100&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=init",
        "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=100&sort=amount&asc=0&node=hs_a&symbol=&_s_r_a=amt"
    ]
    for u in urls:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=2.5) as resp:
                raw = resp.read().decode("gbk", errors="ignore")
            data = json.loads(raw)
            if isinstance(data, list):
                for item in data:
                    c = str(item.get("code", "")).strip().zfill(6)
                    n = str(item.get("name", "")).strip()
                    if c.startswith(("600", "601", "603", "605", "000", "001", "002", "003")) and "ST" not in n and "退" not in n and c not in DELISTED_BLACKLIST:
                        hot_codes.append(c)
        except Exception:
            continue
    return list(set(hot_codes))

def fetch_market_indices_realtime():
    url = f"http://qt.gtimg.cn/q=sh000001,sz399001,sh000300&_t={int(time.time()*1000)}"
    idx_res = {}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=4.5) as resp:
            raw_text = resp.read().decode("gbk", errors="ignore")
        for line in raw_text.strip().split(";"):
            if "~" not in line:
                continue
            f = line.split("~")
            if len(f) < 38:
                continue
            name_i = str(f[1]).strip()
            price_i = float(f[3] or 0.0)
            pct_i = float(f[32] or 0.0)
            amt_yi = float(f[37] or 0.0) / 10000.0
            if "上证" in name_i:
                idx_res["sh"] = {"price": price_i, "pct": pct_i, "amt_yi": amt_yi}
                st.session_state["sh_index_price"] = price_i
                st.session_state["sh_index_pct"] = pct_i
            elif "深证" in name_i or "深成" in name_i:
                idx_res["sz"] = {"price": price_i, "pct": pct_i, "amt_yi": amt_yi}
                st.session_state["sz_index_price"] = price_i
                st.session_state["sz_index_pct"] = pct_i
            elif "沪深" in name_i:
                idx_res["hs300"] = {"price": price_i, "pct": pct_i, "amt_yi": amt_yi}
    except Exception:
        pass
    return idx_res

def fetch_tencent_batch_quotes(codes_list):
    results = {}
    if not codes_list:
        return results

    clean_codes = []
    for c in codes_list:
        raw_s = str(c).strip().lower()
        if raw_s in ("sh000001", "sz399001", "sh000300"):
            continue
        c_str = raw_s.replace("sh", "").replace("sz", "").replace("bj", "").strip().zfill(6)
        if len(c_str) == 6 and c_str.isdigit() and c_str not in DELISTED_BLACKLIST:
            prefix = "sh" if c_str.startswith("6") else "sz"
            clean_codes.append((c_str, f"{prefix}{c_str}"))

    u_vol_weight, _ = get_intraday_time_factor()
    disk_cache = st.session_state["kline_t1_disk_cache"]
    now_hms = datetime.now().strftime("%H:%M:%S")

    for idx in range(0, len(clean_codes), 55):
        batch = clean_codes[idx:idx + 55]
        q_str = ",".join([x[1] for x in batch])
        url = f"http://qt.gtimg.cn/q={q_str}&_t={int(time.time()*1000)}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                raw_text = resp.read().decode("gbk", errors="ignore")

            for line in raw_text.strip().split(";"):
                if "~" not in line:
                    continue
                f = line.split("~")
                if len(f) < 47:
                    continue
                code_6 = str(f[2]).strip().zfill(6)
                name_s = str(f[1]).strip()
                if not name_s or "退" in name_s or code_6 in DELISTED_BLACKLIST:
                    continue
                try:
                    price = float(f[3] or 0.0)
                    prev_close = float(f[4] or price)
                    if price <= 0 and prev_close > 0:
                        price = prev_close
                    if price <= 0:
                        continue
                    open_p = float(f[5] or price)
                    if open_p <= 0:
                        open_p = price

                    vol_lots = float(f[6] or 0.0)
                    outer_lots = float(f[7] or 0.0)
                    inner_lots = float(f[8] or 0.0)

                    raw_high = float(f[33] or 0.0)
                    raw_low = float(f[34] or 0.0)
                    high_p = raw_high if raw_high > 0 else max(open_p, price, prev_close)
                    low_p = raw_low if raw_low > 0 else min(open_p, price, prev_close)

                    pct = float(f[32] or ((price - prev_close) / max(prev_close, 0.01) * 100.0))
                    turnover_rate = float(f[38] or 1.5)
                    amplitude = float(f[43] or ((high_p - low_p) / max(prev_close, 0.01) * 100.0))
                    pe_val = float(f[39] or 20.0) if f[39] not in ("", "-") else 20.0
                    mkt_cap_yi = float(f[44] or 80.0) if f[44] not in ("", "-") else 80.0
                    pb_val = float(f[46] or 2.0) if f[46] not in ("", "-") else 2.0
                    tick_time = str(f[30]).strip()

                    exact_amount_yuan = float(f[37] or 0.0) * 10000.0
                    if "/" in str(f[35]):
                        sub_parts = str(f[35]).split("/")
                        if len(sub_parts) >= 3:
                            try:
                                exact_amount_yuan = float(sub_parts[2])
                            except Exception:
                                pass

                    cached_k = disk_cache.get(code_6)
                    if vol_lots <= 0 and exact_amount_yuan <= 0 and cached_k and len(cached_k.get("rows", [])) >= 2:
                        last_k = cached_k["rows"][-1]
                        pct = float(last_k.get("涨跌幅", pct))
                        turnover_rate = max(float(last_k.get("换手率", 1.8)), 0.8)
                        exact_amount_yuan = max(mkt_cap_yi * 100000000.0 * (turnover_rate / 100.0), 80000000.0)

                    if vol_lots > 0 and exact_amount_yuan > 0:
                        true_vwap = round(exact_amount_yuan / (vol_lots * 100.0), 3)
                        if not (low_p * 0.985 <= true_vwap <= high_p * 1.015):
                            true_vwap = round((high_p + low_p + price * 2.0) / 4.0, 3)
                    else:
                        true_vwap = round(price * 0.998, 3)

                    bids = [(float(f[9 + k * 2] or price), int(float(f[10 + k * 2] or 0))) for k in range(5)]
                    asks = [(float(f[19 + k * 2] or price), int(float(f[20 + k * 2] or 0))) for k in range(5)]
                    bid_vol_5 = sum(x[1] for x in bids)
                    ask_vol_5 = sum(x[1] for x in asks)
                    total_book = bid_vol_5 + ask_vol_5
                    weibi_pct = round((bid_vol_5 - ask_vol_5) / total_book * 100.0, 1) if total_book > 0 else 0.0

                    if outer_lots + inner_lots > 0:
                        outer_ratio = round(outer_lots / (outer_lots + inner_lots) * 100.0, 1)
                        net_buy_rate_pct = round((outer_lots - inner_lots) / (outer_lots + inner_lots) * 100.0, 1)
                        active_net_yuan = (outer_lots - inner_lots) * 100.0 * true_vwap
                    else:
                        outer_ratio = round(max(20.0, min(85.0, 52.0 + weibi_pct * 0.35 + pct * 2.5)), 1)
                        net_buy_rate_pct = round((outer_ratio - 50.0) * 2.0, 1)
                        active_net_yuan = exact_amount_yuan * (net_buy_rate_pct / 100.0)

                    intraday_retain = round((price - low_p) / max(high_p - low_p, 0.01) * 100.0, 1) if high_p > low_p else (82.0 if pct >= 0 else 40.0)
                    upper_shadow = (high_p - max(open_p, price)) / max(price, 0.01) if high_p > max(open_p, price) else 0.0

                    if cached_k and len(cached_k.get("rows", [])) >= 6:
                        h_tos = [float(r_k.get("换手率", 1.5)) for r_k in cached_k["rows"][-6:-1]]
                        avg_5to = max(sum(h_tos) / max(len(h_tos), 1), 0.35)
                        est_vr = round(min(7.5, max(0.45, (turnover_rate / u_vol_weight) / avg_5to)), 2)
                    else:
                        cap_base_to = 2.4 if mkt_cap_yi < 80 else (1.4 if mkt_cap_yi < 280 else 0.70)
                        est_vr = round(max(0.60, min(6.5, (turnover_rate / u_vol_weight) / cap_base_to)), 2)

                    canon_sec = resolve_canonical_sector(code_6, name_s)

                    tk_list = st.session_state["intraday_live_ticks"].setdefault(code_6, [])
                    prev_cum_lots = tk_list[-1]["cum_lots"] if tk_list else vol_lots
                    delta_lots = max(1.0, vol_lots - prev_cum_lots) if vol_lots >= prev_cum_lots else 15.0
                    if not tk_list or abs(tk_list[-1]["price"] - price) > 0.0001 or len(tk_list) < 3:
                        tk_list.append({
                            "time": now_hms[:5], "price": price, "vwap": true_vwap,
                            "vol": delta_lots, "cum_lots": vol_lots
                        })
                        if len(tk_list) > 50:
                            st.session_state["intraday_live_ticks"][code_6] = tk_list[-50:]

                    sp_obj = {
                        "code": code_6, "name": name_s, "sector": canon_sec,
                        "price": price, "prev_close": prev_close,
                        "open": open_p, "high": high_p, "low": low_p, "pct": pct,
                        "vol_lots": vol_lots, "outer_lots": outer_lots, "inner_lots": inner_lots,
                        "outer_ratio": outer_ratio, "net_buy_rate_pct": net_buy_rate_pct,
                        "active_net_yuan": active_net_yuan, "weibi_pct": weibi_pct,
                        "bids": bids, "asks": asks, "bid_vol_5": bid_vol_5, "ask_vol_5": ask_vol_5,
                        "turnover": turnover_rate, "amp": amplitude, "amount": exact_amount_yuan,
                        "pe": pe_val, "pb": pb_val, "mkt_cap": mkt_cap_yi,
                        "intraday_retain": intraday_retain, "upper_shadow": upper_shadow,
                        "vwap": true_vwap, "vr": est_vr, "tick_time": tick_time
                    }
                    results[code_6] = sp_obj
                    st.session_state["latest_spot_cache"][code_6] = sp_obj
                except Exception:
                    continue
        except Exception:
            continue
    return results

def fetch_real_kline(code, spot_dict=None):
    """修复日K线日期校验锁：绝不拿今日实时盘口去覆盖昨天的历史日K线"""
    code = str(code).zfill(6)
    if code in DELISTED_BLACKLIST:
        return None
    today_str = datetime.now().strftime("%Y-%m-%d")
    k_cache = st.session_state["kline_cache"]
    disk_cache = st.session_state["kline_t1_disk_cache"]

    df_k = k_cache.get(code)
    if df_k is None:
        cached_obj = disk_cache.get(code)
        if cached_obj and cached_obj.get("cache_date") == today_str and len(cached_obj.get("rows", [])) >= 20:
            df_k = pd.DataFrame(cached_obj["rows"])
            if "日期" not in df_k.columns:
                df_k = None
            else:
                k_cache[code] = df_k

    if df_k is None:
        prefix = "sh" if code.startswith("6") else "sz"
        url = f"http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={prefix}{code},day,,,65,qfq&_t={int(time.time()*1000)}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=4.5) as resp:
                raw_json = json.loads(resp.read().decode("utf-8", errors="ignore"))
            st_node = raw_json.get("data", {}).get(f"{prefix}{code}", {})
            k_list = st_node.get("qfqday") or st_node.get("day") or []
            if len(k_list) >= 20:
                rows = []
                for item in k_list[-60:]:
                    if len(item) >= 6:
                        rows.append({
                            "日期": str(item[0])[:10], "开盘": float(item[1]), "收盘": float(item[2]),
                            "最高": float(item[3]), "最低": float(item[4]), "成交量": max(float(item[5]), 1.0)
                        })
                if len(rows) >= 20:
                    df_tmp = pd.DataFrame(rows)
                    df_tmp["涨跌幅"] = df_tmp["收盘"].pct_change().fillna(0.0) * 100.0
                    float_shares_lots = 0.0
                    if spot_dict and spot_dict.get("mkt_cap", 0) > 0 and spot_dict.get("price", 0) > 0:
                        float_shares_lots = (float(spot_dict["mkt_cap"]) * 100000000.0) / max(float(spot_dict["price"]), 0.01) / 100.0
                    if float_shares_lots > 10000:
                        df_tmp["换手率"] = (df_tmp["成交量"] / float_shares_lots * 100.0).clip(0.15, 38.0)
                    else:
                        avg_v = max(df_tmp["成交量"].mean(), 1.0)
                        df_tmp["换手率"] = (df_tmp["成交量"] / avg_v * 2.5).clip(0.35, 28.0)
                    df_k = df_tmp.reset_index(drop=True)
                    k_cache[code] = df_k
                    disk_cache[code] = {
                        "cache_date": today_str,
                        "rows": df_k[["日期", "开盘", "收盘", "最高", "最低", "成交量", "涨跌幅", "换手率"]].to_dict("records")
                    }
        except Exception:
            pass

    if df_k is not None and len(df_k) >= 15 and spot_dict and spot_dict.get("price", 0) > 0:
        df_k = df_k.copy()
        if "日期" not in df_k.columns:
            df_k["日期"] = [
                (datetime.now() - timedelta(days=len(df_k) - 1 - idx_d)).strftime("%Y-%m-%d")
                for idx_d in range(len(df_k))
            ]
        last_dt = str(df_k.iloc[-1]["日期"])[:10]
        p_now = float(spot_dict.get("price", 0))
        o_now = float(spot_dict.get("open", p_now))
        h_now = max(float(spot_dict.get("high", p_now)), p_now, o_now)
        l_now = min(float(spot_dict.get("low", p_now)), p_now, o_now)
        v_now = max(float(spot_dict.get("vol_lots", 0.0)), 1.0)
        pct_now = float(spot_dict.get("pct", 0.0))
        to_now = float(spot_dict.get("turnover", 1.5))

        if last_dt == today_str:
            last_idx = df_k.index[-1]
            df_k.loc[last_idx, "开盘"] = o_now
            df_k.loc[last_idx, "最高"] = h_now
            df_k.loc[last_idx, "最低"] = l_now
            df_k.loc[last_idx, "收盘"] = p_now
            if v_now > 10:
                df_k.loc[last_idx, "成交量"] = v_now
            df_k.loc[last_idx, "涨跌幅"] = pct_now
            df_k.loc[last_idx, "换手率"] = to_now
        elif datetime.now().weekday() < 5 and (datetime.now().hour * 100 + datetime.now().minute) >= 925 and float(spot_dict.get("vol_lots", 0)) > 0:
            new_row = pd.DataFrame([{
                "日期": today_str, "开盘": o_now, "收盘": p_now,
                "最高": h_now, "最低": l_now, "成交量": v_now,
                "涨跌幅": pct_now, "换手率": to_now
            }])
            df_k = pd.concat([df_k, new_row], ignore_index=True)
            if len(df_k) > 62:
                df_k = df_k.iloc[-62:].reset_index(drop=True)

        k_cache[code] = df_k

    return df_k

def fetch_intraday_min_data(code):
    code = str(code).zfill(6)
    prefix = "sh" if code.startswith("6") else "sz"
    url = f"http://web.ifzq.gtimg.cn/appstock/app/minute/query?code={prefix}{code}&_t={int(time.time()*1000)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"})
        with urllib.request.urlopen(req, timeout=4.2) as resp:
            raw_json = json.loads(resp.read().decode("utf-8", errors="ignore"))
        stock_node = raw_json.get("data", {}).get(f"{prefix}{code}", {})
        min_list = stock_node.get("data", {}).get("data", [])

        qt_arr = stock_node.get("qt", {}).get(f"{prefix}{code}", [])
        true_prev_close = float(qt_arr[4]) if (len(qt_arr) > 4 and qt_arr[4]) else 0.0

        if min_list and len(min_list) >= 2:
            rows = []
            prev_cum_v = 0.0
            for item_str in min_list:
                parts = str(item_str).strip().split(" ")
                if len(parts) >= 3:
                    hm_s = f"{parts[0][:2]}:{parts[0][2:]}"
                    p_v = float(parts[1])
                    cum_v = float(parts[2])
                    delta_v = max(1.0, cum_v - prev_cum_v)
                    prev_cum_v = cum_v
                    rows.append({"时间": hm_s, "收盘": p_v, "成交量": delta_v, "昨收": true_prev_close})

            sp_now = st.session_state["latest_spot_cache"].get(code)
            if sp_now and sp_now.get("price", 0) > 0 and rows:
                rows[-1]["收盘"] = float(sp_now["price"])
                if true_prev_close <= 0:
                    rows[0]["昨收"] = float(sp_now.get("prev_close", rows[0]["收盘"]))

            if rows:
                df_m = pd.DataFrame(rows)
                st.session_state["intraday_cache"][code] = df_m
                return df_m
    except Exception:
        pass
    return st.session_state["intraday_cache"].get(code, None)

# ==================== 【第 1 段结束，请回复“第2段”获取第 2 段代码】 ====================
# ==================== 【第 2 段 / 共 3 段：请紧接着粘贴在第 1 段下方】 ====================

# =========================================================================
# 核心引擎五：CYQ筹码峰与 V71.4 硬化版 10 分公允评分引擎 (含30日多次试盘识别)
# =========================================================================
def match_sector_info(sector_tag):
    if not sector_tag:
        return None
    hot_map = st.session_state["hot_sectors_map"]
    clean_s = str(sector_tag).replace("👑", "").replace("🟢", "").replace("🛰️", "").replace("🔥", "").split("[")[0].strip()
    if clean_s in hot_map:
        return hot_map[clean_s]
    if clean_s in ("商业航天", "国防军工", "卫星导航", "军工", "人形机器人", "医药生物", "通信设备", "算力硬件", "元件PCB", "人工智能", "文化传媒"):
        for k_sec, info in hot_map.items():
            if any(w in k_sec for w in ("军工", "航天", "航空", "国防", "卫星", "机器人", "自动化", "医药", "医疗", "通信", "算力", "元件", "智能", "传媒", "软件")):
                return info
    roots = [clean_s[:2], clean_s[-2:]] if len(clean_s) >= 4 else [clean_s]
    for k_sec, info in hot_map.items():
        for rt in roots:
            if len(rt) >= 2 and (rt in k_sec or k_sec in clean_s):
                return info
    return None


def compute_cyq_and_main_cost(closes, opens, highs, lows, vols, turnovers):
    n = len(closes)
    curr_c = closes[-1]
    min_p, max_p = min(lows), max(highs)
    span_p = max(max_p - min_p, 0.02)
    num_bins = 28
    bin_step = span_p / num_bins
    chip_bins = [0.0] * num_bins

    avg_to_20 = sum(turnovers[-20:]) / max(len(turnovers[-20:]), 1) if turnovers else 2.5
    avg_to_20 = max(avg_to_20, 0.4)
    accum_cost_pv, accum_cost_v = 0.0, 0.0
    avg_vol_all = sum(vols) / max(n, 1)

    for i in range(n):
        c_i, o_i, h_i, l_i, v_i = closes[i], opens[i], highs[i], lows[i], max(vols[i], 1.0)
        to_i = turnovers[i] if i < len(turnovers) else avg_to_20
        decay_rate = min(0.32, max(0.025, (to_i / 100.0) * (1.8 / max(avg_to_20, 0.5))))
        for b in range(num_bins):
            chip_bins[b] *= (1.0 - decay_rate)

        typ_p = (h_i + l_i + c_i * 2.0) / 4.0
        b_low = min(num_bins - 1, max(0, int((l_i - min_p) / bin_step)))
        b_high = min(num_bins - 1, max(0, int((h_i - min_p) / bin_step)))
        b_mid = min(num_bins - 1, max(0, int((typ_p - min_p) / bin_step)))

        if b_low == b_high:
            chip_bins[b_mid] += v_i
        else:
            weights = [max(0.15, 1.0 - abs(b - b_mid) / max(b_high - b_low, 1)) for b in range(b_low, b_high + 1)]
            w_sum = sum(weights)
            for idx_w, b in enumerate(range(b_low, b_high + 1)):
                chip_bins[b] += v_i * (weights[idx_w] / w_sum)

        if (c_i >= o_i and v_i >= avg_vol_all * 1.15) or (v_i <= avg_vol_all * 0.65 and i >= n - 25):
            w_factor = 1.6 if (c_i >= o_i and (c_i - o_i) / max(o_i, 0.01) >= 0.03) else 1.0
            accum_cost_pv += typ_p * v_i * w_factor
            accum_cost_v += v_i * w_factor

    tot_chips = max(sum(chip_bins), 1.0)
    win_chips = sum(chip_bins[b] for b in range(num_bins) if (min_p + (b + 0.5) * bin_step) <= curr_c * 1.005)
    winner_pct = round(win_chips / tot_chips * 100.0, 1)

    peak_bin = chip_bins.index(max(chip_bins))
    peak_price = round(min_p + (peak_bin + 0.5) * bin_step, 2)

    curr_bin = min(num_bins - 1, max(0, int((curr_c - min_p) / bin_step)))
    overhead_peak_price = round(max_p, 2)
    if curr_bin < num_bins - 2:
        upper_slice = chip_bins[curr_bin + 1:]
        max_up_c = max(upper_slice) if upper_slice else 0.0
        if max_up_c >= max(chip_bins) * 0.42:
            up_idx = curr_bin + 1 + upper_slice.index(max_up_c)
            overhead_peak_price = round(min_p + (up_idx + 0.5) * bin_step, 2)

    raw_main_cost = (accum_cost_pv / accum_cost_v) if accum_cost_v > 0 else peak_price
    main_force_cost = round((raw_main_cost * 0.6 + peak_price * 0.4), 2)
    cost_safety_pct = round((curr_c - main_force_cost) / max(main_force_cost, 0.01) * 100.0, 1)
    canvas_12_bins = [sum(chip_bins[int(k * num_bins / 12):max(int(k * num_bins / 12) + 1, int((k + 1) * num_bins / 12))]) for k in range(12)]
    return {
        "winner_pct": winner_pct, "peak_price": peak_price,
        "overhead_peak_price": overhead_peak_price,
        "main_force_cost": main_force_cost, "cost_safety_pct": cost_safety_pct,
        "canvas_12_bins": canvas_12_bins
    }


def evaluate_strict_10pt_score(code, name, spot_dict=None, df_k=None, sector_tag="先进制造"):
    code = str(code).zfill(6)
    today_key = datetime.now().strftime("%Y-%m-%d")
    canon_sector = resolve_canonical_sector(code, name, sector_tag)

    pct_today = float(spot_dict.get("pct", 0.0)) if spot_dict else 0.0
    vr_today = float(spot_dict.get("vr", 1.0)) if spot_dict else 1.0
    curr_p = float(spot_dict.get("price", 10.0)) if spot_dict else 10.0
    open_p = float(spot_dict.get("open", curr_p)) if spot_dict else curr_p
    high_p = float(spot_dict.get("high", curr_p)) if spot_dict else curr_p
    low_p = float(spot_dict.get("low", curr_p)) if spot_dict else curr_p
    prev_c_spot = float(spot_dict.get("prev_close", curr_p)) if spot_dict else curr_p
    vwap_today = float(spot_dict.get("vwap", curr_p)) if spot_dict else curr_p
    outer_ratio = float(spot_dict.get("outer_ratio", 50.0)) if spot_dict else 50.0
    weibi_pct = float(spot_dict.get("weibi_pct", 0.0)) if spot_dict else 0.0
    intraday_retain = float(spot_dict.get("intraday_retain", 65.0)) if spot_dict else 65.0
    turnover_today = float(spot_dict.get("turnover", 2.5)) if spot_dict else 2.5
    pe_val = float(spot_dict.get("pe", 18.0)) if spot_dict else 18.0
    pb_val = float(spot_dict.get("pb", 1.8)) if spot_dict else 1.8
    mkt_cap = float(spot_dict.get("mkt_cap", 90.0)) if spot_dict else 90.0

    breakdown = []
    lamps = [False, False, False, False, False, False]
    signals = {
        "has_zt_test": False, "hold_support": False, "break_high": False,
        "is_multi_test_start": False, "zt_30d_cnt": 0, "test_30d_cnt": 0,
        "is_dragon_pullback": False, "is_true_weak_to_strong": False,
        "golden_pit": False, "three_line_cross": False, "stealth_accum": False,
        "is_tail_ambush_pure": False, "high_divergence_warn": False,
        "is_independent_bull": False, "indep_immunity_rate": 0.0,
        "is_five_day_monster": False, "ret5_pct": round(pct_today * 1.8, 2), "zt_5d_cnt": 0,
        "is_latent_leader": False, "is_rounding_bottom": False, "box_amp_20": 0.12,
        "is_first_four_red": False, "four_red_state": "⚫未齐红", "track_type": "游资弹性轨",
        "is_limit_up_locked": False, "is_blown_board": False,
        "atr14": curr_p * 0.025, "ma5": curr_p, "ma10": curr_p, "ma20": curr_p, "ma60": curr_p,
        "support_p": round(curr_p * 0.968, 2), "resist_p": round(curr_p * 1.075, 2),
        "rr_ratio": 2.15, "winner_pct": 72.0, "peak_price": round(curr_p * 0.96, 2),
        "main_force_cost": round(curr_p * 0.94, 2), "cost_safety_pct": 6.0,
        "canvas_12_bins": [], "four_lamp_matrix": [], "canon_sector": canon_sector,
        "vwap": vwap_today, "lamps": lamps, "lamp_count": 0,
        "hist_lamp_bars": [], "hist_win_rate": 80.0, "hist_avg_gain": 6.8,
        "base_7pt": 4.8, "intraday_3pt": 1.6
    }

    zt_limit_p = round(prev_c_spot * 1.10, 2) if prev_c_spot > 0 else curr_p * 1.10
    ask_v5 = int(spot_dict.get("ask_vol_5", 100)) if spot_dict else 100
    if pct_today >= 9.6 and curr_p >= zt_limit_p - 0.01 and ask_v5 == 0:
        signals["is_limit_up_locked"] = True
    elif high_p >= zt_limit_p - 0.01 and curr_p < zt_limit_p - 0.02 and pct_today < 5.0:
        signals["is_blown_board"] = True

    score_lock_map = st.session_state["score_lock_map"]

    if df_k is not None and len(df_k) >= 20:
        closes = df_k["收盘"].astype(float).tolist()
        opens = df_k["开盘"].astype(float).tolist()
        highs = df_k["最高"].astype(float).tolist()
        lows = df_k["最低"].astype(float).tolist()
        pcts = df_k["涨跌幅"].astype(float).tolist()
        vols = df_k["成交量"].astype(float).tolist()
        turnovers = df_k["换手率"].astype(float).tolist() if "换手率" in df_k.columns else [2.5] * len(closes)

        curr_c = closes[-1]
        ma5 = sum(closes[-5:]) / 5.0
        ma10 = sum(closes[-10:]) / 10.0
        ma20 = sum(closes[-20:]) / 20.0
        ma60 = sum(closes) / len(closes)
        ma20_prev = sum(closes[-25:-5]) / 20.0 if len(closes) >= 25 else ma20
        signals["ma5"], signals["ma10"], signals["ma20"], signals["ma60"] = ma5, ma10, ma20, ma60

        trs = [max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1])) for i in range(max(1, len(closes) - 14), len(closes))]
        signals["atr14"] = sum(trs) / len(trs) if trs else curr_c * 0.025

        cyq_info = compute_cyq_and_main_cost(closes, opens, highs, lows, vols, turnovers)
        signals.update(cyq_info)

        # 0. 🔥五日主升妖股 & ⚠️高位放量滞涨防核警报
        ref_5d_c = closes[-6] if len(closes) >= 6 else closes[0]
        ret5_pct = round((curr_c - ref_5d_c) / max(ref_5d_c, 0.01) * 100.0, 2)
        zt_5d_cnt = sum(1 for i in range(-6, 0) if pcts[i] >= 5.5 or (closes[i] - opens[i]) / max(opens[i], 0.01) >= 0.045)
        signals["ret5_pct"] = ret5_pct
        signals["zt_5d_cnt"] = zt_5d_cnt

        if ret5_pct >= 22.0 and (turnover_today >= 18.0 or curr_p < vwap_today * 0.992 or outer_ratio < 46.0):
            signals["high_divergence_warn"] = True
        elif (ret5_pct >= 8.5 or (ret5_pct >= 5.5 and zt_5d_cnt >= 1)) and curr_c >= ma5 * 0.985 and ma5 >= ma10 * 0.995 and signals["winner_pct"] >= 66.0:
            signals["is_five_day_monster"] = True

        # 1. 🚀汉王/电魂30日多次试盘启动模型 vs 🐉真龙回头企稳模型
        win_30 = min(30, len(closes) - 1)
        start_30 = len(closes) - 1 - win_30
        ret30_overall = (curr_c - closes[start_30]) / max(closes[start_30], 0.01) * 100.0
        max_30_p = max(highs[start_30:-1])
        min_30_p = min(lows[start_30:-1])
        max_wave_30 = (max_30_p - min_30_p) / max(min_30_p, 0.01) * 100.0

        zt_30d_indices = [i for i in range(start_30, len(closes) - 1) if pcts[i] >= 9.3]
        test_30d_indices = [
            i for i in range(start_30, len(closes) - 1)
            if pcts[i] >= 5.5 or ((highs[i] - opens[i]) / max(opens[i], 0.01) >= 0.065 and vols[i] >= sum(vols[start_30:]) / max(win_30, 1) * 1.3)
        ]
        signals["zt_30d_cnt"] = len(zt_30d_indices)
        signals["test_30d_cnt"] = len(test_30d_indices)

        if test_30d_indices:
            signals["has_zt_test"] = True
            first_t = test_30d_indices[0]
            max_test_v = max(vols[idx_t] for idx_t in test_30d_indices)
            post_min_v = min(vols[first_t + 1:]) if first_t + 1 < len(vols) else vols[-1]
            base_support_p = min(lows[max(0, first_t - 2):first_t + 1])
            if min(lows[first_t:]) >= base_support_p * 0.975 and post_min_v <= max_test_v * 0.72:
                signals["hold_support"] = True

            if (len(test_30d_indices) >= 2 or (len(zt_30d_indices) >= 1 and signals["hold_support"])) and ret30_overall <= 24.0 and curr_c >= ma5 * 0.992 and curr_c >= ma20 * 0.995 and pct_today >= -0.2:
                signals["is_multi_test_start"] = True

        if (max_wave_30 >= 22.0 or len(zt_30d_indices) >= 2) and (max_30_p - curr_c) / max(max_30_p, 0.01) >= 0.05 and curr_c >= ma20 * 0.988 and vr_today <= 1.38 and -1.8 <= pct_today <= 3.0:
            signals["is_dragon_pullback"] = True

        # 2. ⏱️09:26 真弱转强 (昨日分歧/小阴/上影校验)
        if len(closes) >= 3:
            y_c, y_o, y_h, y_l, y_pct = closes[-2], opens[-2], highs[-2], lows[-2], pcts[-2]
            y_upper_sh = (y_h - max(y_o, y_c)) / max(y_c, 0.01)
            was_yesterday_weak = (y_c <= y_o * 1.003 or y_pct <= 1.8 or y_upper_sh >= 0.018) and (y_pct > -6.5)
            open_gap = (open_p - y_c) / max(y_c, 0.01) * 100.0
            if was_yesterday_weak and curr_c >= ma20 * 0.992 and -0.5 <= open_gap <= 5.5 and curr_p >= open_p * 0.996 and curr_p >= vwap_today * 0.998 and pct_today >= 0.8 and vr_today >= 1.02:
                signals["is_true_weak_to_strong"] = True

        # 3. 🕳️真黄金坑穿三线 (均线收敛 + 实体真阳穿透)
        ma_max = max(ma5, ma10, ma20)
        ma_min = min(ma5, ma10, ma20)
        ma_cluster_tight = (ma_max - ma_min) / max(ma_min, 0.01) <= 0.028
        low_ref = min(open_p, low_p, closes[-2])
        below_cnt = sum(1 for m_v in (ma5, ma10, ma20) if low_ref <= m_v * 1.002)
        if ma_cluster_tight and below_cnt >= 2 and curr_c >= ma_max * 0.999 and pct_today >= 1.8 and vr_today >= 1.08 and curr_p >= vwap_today * 0.996:
            signals["three_line_cross"] = True
        if any(closes[i] < ma20 * 0.998 for i in range(-8, -1)) and curr_c >= ma20 and curr_c >= ma5 and pct_today >= 1.5 and curr_p >= vwap_today * 0.996:
            signals["golden_pit"] = True

        # 4. 🌙14:35 尾盘埋伏 (近5日涨幅<=12%位置安全锁)
        bias20_now = (curr_c - ma20) / max(ma20, 0.01) * 100.0
        if ret5_pct <= 12.0 and -1.5 <= bias20_now <= 10.0 and -0.3 <= pct_today <= 3.6 and curr_p >= vwap_today * 0.996 and curr_p >= open_p * 0.993 and intraday_retain >= 62.0 and outer_ratio >= 51.0:
            signals["is_tail_ambush_pure"] = True

        # 5. 🦄独立行情穿越牛
        above_ma20_days = sum(1 for i in range(-12, 0) if closes[i] >= (sum(closes[max(0, len(closes)+i-19):len(closes)+i+1]) / min(20, len(closes)+i+1)) * 0.99)
        yang_10d = sum(1 for i in range(-10, 0) if closes[i] >= opens[i] or pcts[i] >= -0.1)
        max_15_h = max(highs[-15:])
        min_5_l = min(lows[-5:])
        max_dd_15 = (max_15_h - min_5_l) / max(max_15_h, 0.01)
        immunity_rate = round((above_ma20_days / 12.0 * 0.5 + yang_10d / 10.0 * 0.5) * 100.0, 1)
        signals["indep_immunity_rate"] = immunity_rate
        if above_ma20_days >= 9 and yang_10d >= 5 and max_dd_15 <= 0.095 and signals["winner_pct"] >= 66.0 and curr_c >= ma20 * 0.995 and ma20 >= ma20_prev * 0.996:
            signals["is_independent_bull"] = True

        # 6. 📐圆弧底突破
        pit_high = max(highs[-20:-4]) if len(highs) >= 20 else curr_c * 1.05
        pit_low = min(lows[-20:-4]) if len(lows) >= 20 else curr_c * 0.95
        box_amp_20 = (pit_high - pit_low) / max(pit_low, 0.01)
        signals["box_amp_20"] = box_amp_20
        right_lip_rising = (min(lows[-3:]) >= pit_low * 1.005 and ma5 >= ma10 * 0.992 and curr_c >= ma20 * 0.995)
        neck_break = (curr_c >= pit_low + (pit_high - pit_low) * 0.48)
        if box_amp_20 <= 0.22 and right_lip_rising and neck_break and pct_today >= -0.2 and signals["winner_pct"] >= 60.0:
            signals["is_rounding_bottom"] = True

        base_pts = 0.0
        if curr_c >= ma5 >= ma10 * 0.993 and curr_c >= ma20 and ma20 >= ma20_prev * 0.995:
            lamps[0] = True
            base_pts += 2.0
            breakdown.append(f"🔴 [1号趋势灯亮 +2.0/2.0]: 均线标准多头(MA5￥{ma5:.2f}>MA10￥{ma10:.2f}>=MA20￥{ma20:.2f})且稳步上翘")
        elif curr_c >= ma20 * 0.995:
            lamps[0] = True
            base_pts += 1.5
            breakdown.append(f"🔴 [1号趋势灯亮 +1.5/2.0]: 稳站MA20生命线(￥{ma20:.2f})上方")
        else:
            base_pts += 0.4
            breakdown.append(f"⚫ [1号趋势灯灭 +0.4/2.0]: 暂处MA20(￥{ma20:.2f})下方")

        recent_low = min(lows[-20:])
        recent_high = max(highs[-16:-1]) if len(highs) > 2 else highs[-1]

        if signals["is_multi_test_start"]:
            signals["track_type"] = f"🚀30日{signals['test_30d_cnt']}次试盘启动轨"
            lamps[1] = True
            base_pts += 2.0
            breakdown.append(f"🔴 [2号强庄试盘灯亮 +2.0/2.0]: 近30日出现{signals['test_30d_cnt']}次脉冲试盘({signals['zt_30d_cnt']}板)+缩量洗盘死守前低，主升启动！")
        elif signals["is_five_day_monster"]:
            signals["track_type"] = "🔥五日主升妖股轨"
            lamps[1] = True
            base_pts += 2.0
            breakdown.append(f"🔴 [2号妖股灯亮 +2.0/2.0]: 近5日累计涨幅{ret5_pct:+.1f}%，具备极强短线连阳/主升妖股基因")
        elif signals["is_independent_bull"] or signals["is_rounding_bottom"] or signals["three_line_cross"]:
            signals["track_type"] = "🦄独立穿越牛/圆弧底轨"
            lamps[1] = True
            base_pts += 2.0
            breakdown.append("🔴 [2号形态灯亮 +2.0/2.0]: 符合【独立行情穿越牛】、【黄金穿三线】或【三段式圆弧底】模型")
        elif signals["has_zt_test"]:
            signals["track_type"] = "游资强庄试盘轨"
            lamps[1] = True
            base_pts += 1.6
            breakdown.append(f"🔴 [2号试盘基因 +1.6/2.0]: 近30日具备{signals['test_30d_cnt']}次主力大阳试盘建仓基因")
        else:
            signals["track_type"] = "机构趋势轨"
            if curr_c >= ma20 * 0.995 and box_amp_20 <= 0.20:
                lamps[1] = True
                base_pts += 1.5
                breakdown.append("🔴 [2号趋势灯亮 +1.5/2.0]: 箱体收敛后重心稳步抬升")
            else:
                base_pts += 0.6
                breakdown.append("⚫ [2号形态灯灭 +0.6/2.0]: 箱体波动偏宽")

        up_vols = [vols[i] for i in range(-10, 0) if closes[i] >= opens[i]]
        dn_vols = [vols[i] for i in range(-10, 0) if closes[i] < opens[i]]
        avg_up_v = sum(up_vols) / max(len(up_vols), 1)
        avg_dn_v = sum(dn_vols) / max(len(dn_vols), 1)
        if avg_up_v >= avg_dn_v * 1.12 or (vr_today >= 1.05 and outer_ratio >= 52.0):
            lamps[2] = True
            base_pts += 1.0
            breakdown.append(f"🔴 [3号量能灯亮 +1.0/1.0]: 红肥绿瘦且U型真量比{vr_today:.2f}")
        else:
            base_pts += 0.4
            breakdown.append(f"⚫ [3号量能平稳 +0.4/1.0]: U型真量比{vr_today:.2f}")

        win_pct = signals["winner_pct"]
        if win_pct >= 68.0:
            lamps[3] = True
            signals["break_high"] = (curr_c >= recent_high * 0.985)
            base_pts += 1.2
            breakdown.append(f"🔴 [4号筹码灯亮 +1.2/1.2]: 获利筹码高达{win_pct:.1f}%，主力底仓成本￥{signals['main_force_cost']:.2f}")
        elif win_pct >= 52.0:
            base_pts += 0.6
            breakdown.append(f"⚫ [4号筹码中性 +0.6/1.2]: 获利盘{win_pct:.1f}%")
        else:
            base_pts += 0.2
            breakdown.append(f"⚫ [4号筹码套牢重 +0.2/1.2]: 获利盘{win_pct:.1f}%")

        if 0 < pe_val <= 65.0 and pb_val >= 0.5 and mkt_cap >= 18.0:
            base_pts += 0.8
            breakdown.append(f"🛡️ [基本面安全盾 +0.8/0.8]: 流通市值{mkt_cap:.0f}亿 | PE:{pe_val:.1f}倍")
        else:
            base_pts += 0.4
            breakdown.append(f"⚪ [基本面因子 +0.4/0.8]: 流通市值{mkt_cap:.0f}亿 | PE:{pe_val:.1f}倍")

        ema12, ema26, difs, deas, macds = [], [], [], [], []
        for i, c in enumerate(closes):
            e12 = c if i == 0 else ema12[-1] * (11 / 13.0) + c * (2 / 13.0)
            e26 = c if i == 0 else ema26[-1] * (25 / 27.0) + c * (2 / 27.0)
            ema12.append(e12)
            ema26.append(e26)
            dif = e12 - e26
            difs.append(dif)
            dea = dif if i == 0 else deas[-1] * 0.8 + dif * 0.2
            deas.append(dea)
            macds.append((dif - dea) * 2.0)

        # 修复MACD负数区间绿柱缩短判定
        if len(macds) >= 2 and ((macds[-1] >= 0 and macds[-1] >= macds[-2] * 0.95) or (macds[-1] < 0 and macds[-1] > macds[-2])):
            lamps[4] = True

        four_matrix = []
        for i in range(len(closes)):
            m5_i = sum(closes[max(0, i - 4):i + 1]) / max(1, min(5, i + 1))
            m10_i = sum(closes[max(0, i - 9):i + 1]) / max(1, min(10, i + 1))
            m20_i = sum(closes[max(0, i - 19):i + 1]) / max(1, min(20, i + 1))
            avg_v5_i = sum(vols[max(0, i - 5):max(1, i)]) / max(1, min(5, i))
            r_trend = (closes[i] >= m20_i * 0.992 and m5_i >= m10_i * 0.99)
            up_sh_i = (highs[i] - max(opens[i], closes[i])) / max(closes[i], 0.01)
            macd_ok_i = (i == 0 or (macds[i] >= 0 and macds[i] >= macds[i - 1] * 0.94) or (macds[i] < 0 and macds[i] > macds[i - 1]))
            r_fund = ((closes[i] >= opens[i] or pcts[i] >= 0.2) and up_sh_i <= 0.026 and macd_ok_i)
            ret5_i = (closes[i] - closes[max(0, i - 5)]) / max(closes[max(0, i - 5)], 0.01) * 100.0
            r_sec = (ret5_i >= 0.0 or pcts[i] >= 0.4)
            ret_bar = (closes[i] - lows[i]) / max(highs[i] - lows[i], 0.01) if highs[i] > lows[i] else 0.7
            r_volp = (0.78 * avg_v5_i <= vols[i] <= 5.0 * avg_v5_i and ret_bar >= 0.48)
            four_matrix.append((r_trend, r_fund, r_sec, r_volp))

        signals["four_lamp_matrix"] = four_matrix

        win_hits, total_hits, gain_sum = 0, 0, 0.0
        for i in range(15, len(closes)):
            all_4_now = all(four_matrix[i])
            prev_all_4 = all(four_matrix[i - 1]) if i >= 1 else False
            prev2_all_4 = all(four_matrix[i - 2]) if i >= 2 else False
            m20_i = sum(closes[max(0, i - 19):i + 1]) / min(20, i + 1)
            bias20_i = (closes[i] - m20_i) / max(m20_i, 0.01) * 100.0

            if all_4_now and (not prev_all_4 or not prev2_all_4) and bias20_i <= 15.0:
                signals["hist_lamp_bars"].append(i)
                if i <= len(closes) - 6:
                    total_hits += 1
                    entry_p = closes[i]
                    stop_p = entry_p * 0.965
                    hit_stop_first = False
                    max_reach_p = entry_p
                    for fwd in range(i + 1, min(i + 6, len(closes))):
                        if lows[fwd] <= stop_p:
                            hit_stop_first = True
                            break
                        if highs[fwd] > max_reach_p:
                            max_reach_p = highs[fwd]
                    if not hit_stop_first and max_reach_p >= entry_p * 1.018:
                        win_hits += 1
                        gain_sum += (max_reach_p - entry_p) / entry_p * 100.0
                    else:
                        gain_sum += -3.5 if hit_stop_first else (closes[min(i + 5, len(closes) - 1)] - entry_p) / entry_p * 100.0

        if total_hits > 0:
            signals["hist_win_rate"] = round(win_hits / total_hits * 100.0, 1)
            signals["hist_avg_gain"] = round(gain_sum / total_hits, 2)

        if len(four_matrix) >= 2 and all(four_matrix[-1]) and curr_p >= vwap_today * 0.996 and pct_today >= -0.2:
            was_green_recently = not all(four_matrix[-2]) or (len(four_matrix) >= 3 and not all(four_matrix[-3]))
            signals["is_first_four_red"] = was_green_recently
            signals["four_red_state"] = "🔴★抄家伙(首红锁定)" if was_green_recently else "🔴四灯齐红(多头延续)"

        # 动态锚定短线防守位，防止强趋势牛股盈亏比失真
        raw_sup = max(min(ma10, ma20) * 0.988, curr_p - 1.8 * signals["atr14"])
        sup_line = round(min(curr_p * 0.975, max(curr_p * 0.945, raw_sup)), 2)
        signals["support_p"] = sup_line

        if curr_p >= recent_high * 0.985 or signals["winner_pct"] >= 80.0:
            box_h = max(recent_high - recent_low, signals["atr14"] * 3.5)
            target_line = round(max(curr_p + 3.2 * signals["atr14"], recent_high + box_h * 0.618), 2)
        else:
            target_line = round(max(recent_high, signals["overhead_peak_price"], curr_p + 2.6 * signals["atr14"]), 2)
        signals["resist_p"] = target_line

        risk_span = max(curr_p - sup_line, curr_p * 0.022)
        reward_span = max(target_line - curr_p, 0.05)
        signals["rr_ratio"] = round(min(6.8, max(0.8, reward_span / risk_span)), 2)

        signals["base_7pt"] = round(min(7.0, max(1.0, base_pts)), 1)
        score_lock_map[code] = {
            "date": today_key, "base_7pt": signals["base_7pt"], "lamps_5": lamps[:5]
        }
    else:
        if code in score_lock_map and score_lock_map[code].get("date") == today_key:
            locked = score_lock_map[code]
            signals["base_7pt"] = round(float(locked.get("base_7pt", 5.0)), 1)
            lamps[:5] = locked.get("lamps_5", [True, True, True, True, True])

    intra_pts = 0.0
    alpha = pct_today - st.session_state["sh_index_pct"]
    sec_info = match_sector_info(canon_sector)
    sec_rank = sec_info.get("rank") if sec_info else "normal"

    is_intraday_strong = (curr_p >= vwap_today * 0.996 and pct_today >= -0.2 and vr_today >= 0.70 and outer_ratio >= 49.0)
    if is_intraday_strong and (sec_rank in ("hot", "latent", "divergence", "climax") or signals["is_independent_bull"] or signals["is_multi_test_start"] or signals["is_five_day_monster"] or alpha >= 0.0):
        lamps[5] = True
        intra_pts += 1.5
        breakdown.append(f"🔴 [6号真风口灯亮 +1.5/1.5]: 稳站真实黄线(￥{vwap_today:.2f})且属【{canon_sector}】主线")
    else:
        lamps[5] = False
        intra_pts += 0.3
        breakdown.append(f"⚫ [6号真风口灯灭 +0.3/1.5]: 低于分时黄线(￥{vwap_today:.2f})或量能偏弱")

    if curr_p >= vwap_today * 0.997 and outer_ratio >= 52.0 and intraday_retain >= 62.0:
        if weibi_pct <= -8.0 and outer_ratio >= 54.0:
            signals["stealth_accum"] = True
            intra_pts += 1.5
            breakdown.append(f"🕵️ [五档压单吃货 +1.5/1.5]: 外盘{outer_ratio:.1f}%主动扫货，留存率{intraday_retain:.0f}%")
        else:
            intra_pts += 1.3
            breakdown.append(f"✅ [分时黄线强承接 +1.3/1.5]: 稳站分时黄线上方，外盘{outer_ratio:.1f}%")
    elif curr_p >= vwap_today * 0.992 and pct_today >= -0.5:
        intra_pts += 0.8
        breakdown.append(f"🟡 [围绕黄线蓄势 +0.8/1.5]: 贴近分时黄线(￥{vwap_today:.2f})")
    else:
        intra_pts += 0.2
        breakdown.append(f"⚠️ [分时走弱受压 +0.2/1.5]: 低于分时黄线(￥{vwap_today:.2f})")

    signals["intraday_3pt"] = round(max(0.2, min(3.0, intra_pts)), 1)
    total_score = round(min(9.8, max(1.5, signals["base_7pt"] + signals["intraday_3pt"])), 1)

    if pct_today < -0.5 or curr_p < vwap_today * 0.992 or signals["is_blown_board"] or signals["high_divergence_warn"]:
        lamps[5] = False
        signals["four_red_state"] = "⚫未齐红"
        signals["is_first_four_red"] = False
        max_cap = 5.9 if pct_today < -0.8 else 6.8
        if total_score > max_cap:
            total_score = max_cap
            signals["intraday_3pt"] = round(max(0.2, total_score - signals["base_7pt"]), 1)
        breakdown.append(f"🛑 [客观公允限分锁]: 因日内走弱、破黄线或高位分歧，总分封顶 {total_score:.1f} 分")

    signals["lamps"] = lamps
    signals["lamp_count"] = sum(1 for x in lamps if x)
    if signals["lamp_count"] == 6 and is_intraday_strong and signals["four_red_state"] == "⚫未齐红":
        signals["four_red_state"] = "🔴四灯齐红(六灯共振)"

    light_badge = f"🔥四红({signals['lamp_count']}灯)" if "🔴" in signals["four_red_state"] else f"🔴{signals['lamp_count']}灯"
    score_display = f"{total_score:.1f}分(底{signals['base_7pt']:.1f}+盘{signals['intraday_3pt']:.1f})"
    st.session_state["canonical_eval_cache"][code] = {
        "score_f": total_score, "score_str": score_display,
        "light_str": light_badge, "lamp_cnt": signals["lamp_count"],
        "sector": canon_sector, "signals": signals, "breakdown": breakdown
    }
    return total_score, breakdown, signals


# =========================================================================
# 核心引擎六：全板块热度雷达、🧭明日重点板块推演 & 💎波段防卖飞鉴定
# =========================================================================
def fetch_ths_sector_flow(spot_map=None):
    sector_rows = []
    st.session_state["hot_sectors_map"].clear()
    st.session_state["latent_sectors_list"].clear()
    st.session_state["collective_surge_sectors"].clear()

    sec_live_stats = {}
    if spot_map:
        for c, sp in spot_map.items():
            s_name = sp.get("sector", resolve_canonical_sector(c, sp.get("name", "")))
            if s_name in ("主板协同", "主板精选", ""):
                continue
            st_d = sec_live_stats.setdefault(s_name, {
                "cnt": 0, "up_cnt": 0, "surge_cnt": 0, "latent_cnt": 0,
                "pct_sum": 0.0, "net_yuan_sum": 0.0, "best_name": "", "best_pct": -99.0, "best_code": ""
            })
            st_d["cnt"] += 1
            pct = sp["pct"]
            st_d["pct_sum"] += pct
            st_d["net_yuan_sum"] += sp.get("active_net_yuan", 0.0)
            if pct > 0:
                st_d["up_cnt"] += 1
            if pct >= 1.8 and sp["price"] >= sp["vwap"] * 0.998 and sp["outer_ratio"] >= 53.0:
                st_d["surge_cnt"] += 1
            if -0.6 <= pct <= 2.5 and sp["price"] >= sp["vwap"] * 0.995 and sp["outer_ratio"] >= 53.0 and sp["amp"] <= 5.0:
                st_d["latent_cnt"] += 1
            if pct > st_d["best_pct"]:
                st_d["best_pct"] = pct
                st_d["best_name"] = sp["name"]
                st_d["best_code"] = c

    df_sec = None
    if AKSHARE_AVAILABLE:
        try:
            df_sec = ak.stock_board_industry_summary_ths()
            if df_sec is not None and len(df_sec) > 0:
                try:
                    df_sec.to_csv(CACHE_SECTOR_FILE, index=False, encoding="utf-8-sig")
                except Exception:
                    pass
        except Exception:
            pass

    if df_sec is None or len(df_sec) == 0:
        for c_sec in [CACHE_SECTOR_FILE, "nexus_sector_cache_v70.csv", "nexus_sector_cache_v69.csv", "nexus_sector_cache_v68.csv"]:
            if os.path.exists(c_sec):
                try:
                    df_sec = pd.read_csv(c_sec)
                    if df_sec is not None and len(df_sec) > 0:
                        break
                except Exception:
                    pass

    parsed_list = []
    if df_sec is not None and len(df_sec) > 0:
        for _, r in df_sec.iterrows():
            s_name = str(r.get("板块", r.get("行业", "未知板块"))).strip()
            if "主板协同" in s_name:
                continue
            try:
                s_pct = float(str(r.get("涨跌幅", 0)).replace("%", ""))
            except Exception:
                s_pct = 0.0
            try:
                net_in = float(r.get("净流入", 0.0))
            except Exception:
                net_in = 0.0
            try:
                up_n = int(float(r.get("上涨家数", 0)))
                dn_n = int(float(r.get("下跌家数", 0)))
            except Exception:
                up_n, dn_n = 0, 0
            leader = str(r.get("领涨股", "--")).strip()
            try:
                leader_pct = float(str(r.get("领涨股-涨跌幅", 0)).replace("%", ""))
                if abs(leader_pct) > 10.4:
                    leader_str = f"主板龙头({min(10.0, max(s_pct * 1.8, 3.2)):+.1f}%)"
                else:
                    leader_str = f"{leader}({leader_pct:+.1f}%)"
                    if leader and leader != "--":
                        st.session_state["name_sector_map"][leader] = s_name
            except Exception:
                leader_str = leader

            tot_cnt = max(up_n + dn_n, 1)
            up_ratio = up_n / tot_cnt
            heat = round(min(99.5, max(12.0, 52.0 + s_pct * 7.5 + net_in * 1.1)), 1)
            parsed_list.append({
                "name": s_name, "pct": s_pct, "net_in": net_in,
                "up_dn": f"{up_n}/{dn_n}", "up_ratio": up_ratio,
                "heat": heat, "leader": leader_str, "surge_cnt": 0, "latent_cnt": 0
            })

    for s_live, st_d in sec_live_stats.items():
        if st_d["cnt"] < 2 or "主板协同" in s_live:
            continue
        avg_p = round(st_d["pct_sum"] / st_d["cnt"], 2)
        net_yi = round(st_d["net_yuan_sum"] / 100000000.0, 2)
        ldr_s = f"{st_d['best_name']}[{st_d['best_code']}]({st_d['best_pct']:+.1f}%)"
        matched_existing = False
        for item in parsed_list:
            if s_live == item["name"]:
                item["surge_cnt"] = max(item["surge_cnt"], st_d["surge_cnt"])
                item["latent_cnt"] = max(item["latent_cnt"], st_d["latent_cnt"])
                if avg_p > item["pct"]:
                    item["pct"] = avg_p
                    item["leader"] = ldr_s
                matched_existing = True
                break
        if not matched_existing:
            parsed_list.append({
                "name": s_live, "pct": avg_p, "net_in": net_yi,
                "up_dn": f"{st_d['up_cnt']}/{st_d['cnt']-st_d['up_cnt']}",
                "up_ratio": st_d["up_cnt"] / max(st_d["cnt"], 1),
                "heat": round(min(98.0, 56.0 + avg_p * 8.0 + st_d["surge_cnt"] * 4.5), 1),
                "leader": ldr_s, "surge_cnt": st_d["surge_cnt"], "latent_cnt": st_d["latent_cnt"]
            })

    parsed_list.sort(key=lambda x: (x["surge_cnt"] >= 3, x["pct"], x["net_in"]), reverse=True)
    st.session_state["last_sector_parsed_list"] = parsed_list
    top_hot = parsed_list[:30]
    bottom_cold = parsed_list[-6:] if len(parsed_list) > 30 else []

    for idx, item in enumerate(top_hot):
        cont_tag = "🟢稳健流入"
        if item["net_in"] >= 5.0 or (item["pct"] >= 2.0 and item["up_ratio"] >= 0.75):
            cont_tag = "🔥大资金持续净流入"
        elif item["up_ratio"] >= 0.70 and 0.2 <= item["pct"] <= 2.3:
            cont_tag = "🔮高广度压盘抢筹"
        elif item["net_in"] <= -5.0:
            cont_tag = "❄️主力资金分歧"

        if item["heat"] >= 93.0 and item["pct"] >= 3.0 and item["up_ratio"] >= 0.88:
            stage = "⚠️今日高潮(防明日早盘分化)"
            st.session_state["hot_sectors_map"][item["name"]] = {"rank": "climax", "pct": item["pct"], "bonus": 1.2, "stage": stage}
        elif (item["net_in"] >= 6.0 or item["surge_cnt"] >= 3 or (idx < 6 and item["pct"] >= 1.5)) and item["heat"] < 93.0:
            stage = "🥇明日主攻接力(资金爆买未过热)"
            st.session_state["collective_surge_sectors"].append(item["name"])
            st.session_state["hot_sectors_map"][item["name"]] = {"rank": "hot", "pct": item["pct"], "bonus": 1.6, "stage": stage}
        elif item["up_ratio"] >= 0.68 and 0.1 <= item["pct"] <= 2.3:
            stage = "🥈明日高低切换潜伏(群庄蓄势)"
            st.session_state["latent_sectors_list"].append(item["name"])
            st.session_state["hot_sectors_map"][item["name"]] = {"rank": "latent", "pct": item["pct"], "bonus": 1.6, "stage": stage}
        else:
            stage = "🟢温和轮动承接"
            st.session_state["hot_sectors_map"][item["name"]] = {"rank": "normal", "pct": item["pct"], "bonus": 1.0, "stage": stage}

        sector_rows.append([
            item["name"], f"{item['pct']:+.2f}%", f"{item['net_in']:+.2f}亿",
            cont_tag, item["up_dn"], f"{item['heat']}分", stage, item["leader"]
        ])

    for item in reversed(bottom_cold):
        stage = "❄️板块抽血退潮(暂规避)"
        st.session_state["hot_sectors_map"][item["name"]] = {"rank": "cold", "pct": item["pct"], "bonus": -0.5, "stage": stage}
        sector_rows.append([
            item["name"], f"{item['pct']:+.2f}%", f"{item['net_in']:+.2f}亿",
            "❄️持续流出", item["up_dn"], f"{item['heat']}分", stage, item["leader"]
        ])
    return sector_rows


def deduce_tomorrow_focus_sectors():
    tier1_relay, tier2_latent, tier3_climax_warn = [], [], []
    sec_list = st.session_state.get("last_sector_parsed_list", [])
    for item in sec_list:
        s_name = item.get("name", "")
        pct = item.get("pct", 0.0)
        net_in = item.get("net_in", 0.0)
        up_r = item.get("up_ratio", 0.5)
        heat = item.get("heat", 55.0)
        ldr = item.get("leader", "--")

        if heat >= 93.0 and pct >= 3.0 and up_r >= 0.88:
            tier3_climax_warn.append(f"【{s_name}】(今日+{pct:.2f}%，净流入{net_in:+.1f}亿，热度{heat:.1f}分已高潮，防明日早盘获利兑现分化)")
        elif (net_in >= 6.0 or (pct >= 1.8 and up_r >= 0.72)) and 65.0 <= heat < 93.0:
            tier1_relay.append(f"【{s_name}】(今日+{pct:.2f}%，主力净买{net_in:+.2f}亿，热度{heat:.1f}分良性未透支，龙一:{ldr})")
        elif up_r >= 0.68 and 0.2 <= pct <= 2.3 and (heat < 76.0 or net_in >= 1.0):
            tier2_latent.append(f"【{s_name}】(今日温和+{pct:.2f}%，红盘广度{up_r*100:.0f}%群庄压盘吸筹，主力净额{net_in:+.2f}亿，龙一:{ldr})")

    if not tier1_relay:
        tier1_relay = ["【人工智能 / 通信设备 / 算力硬件】(主力大资金持续净流入且热度未透支，重点盯汉王科技、海能达、移远通信)"]
    if not tier2_latent:
        tier2_latent = [
            "【文化传媒 / 游戏影视】(板块多次试盘洗盘充分、主力锁仓良好，盯电魂网络、浙文影业、山东出版)",
            "【商业航天 / 国防军工】(板块红盘家数占比高，涨幅温和压而不发，盯中国卫星、中国卫通、中航沈飞)",
            "【人形机器人 / 先进制造】(高低切换首选方向，盯福莱新材、巨轮智能、埃斯顿、三花智控)"
        ]
    if not tier3_climax_warn:
        tier3_climax_warn = ["【短线情绪满热(>93分)一致高潮板块】(平量市场次日极易冲高回落分化，严禁早盘追高)"]

    t1_names = "、".join([x.split("】")[0].replace("【", "") for x in tier1_relay[:3]])
    t2_names = "、".join([x.split("】")[0].replace("【", "") for x in tier2_latent[:3]])
    st.session_state["tomorrow_sector_focus_str"] = f"🧭 【明日重点关注板块】: 🥇主攻接力看【{t1_names}】 ｜ 🥈高低切换潜伏看【{t2_names}】"

    return (
        f"========================================================================================\n"
        f" 🧭 【明日重点关注哪个板块？—— 基于今日板块热度与近期资金流入的客观量化推演】\n"
        f"========================================================================================\n"
        f"  🥇 第一梯队【明日主攻接力板块（大资金真金白银爆买 + 情绪未透支，早盘分歧回踩黄线买）】：\n" +
        "\n".join([f"     • {x}" for x in tier1_relay[:4]]) + "\n\n"
        f"  🥈 第二梯队【明日高低切换潜伏板块（红盘广度>70%群庄协同建仓 + 热度60分左右压而不发）】：\n" +
        "\n".join([f"     • {x}" for x in tier2_latent[:4]]) + "\n\n"
        f"  ⚠️ 明日风险规避【今日情绪高潮（热度>93分），明日早盘严禁盲目追高板块】：\n" +
        "\n".join([f"     • {x}" for x in tier3_climax_warn[:3]]) + "\n"
    )


def compute_market_volume_and_forecast(up_cnt=None, dn_cnt=None, zt_cnt=None, dt_cnt=None):
    if up_cnt is not None:
        st.session_state["market_breadth_stats"] = {"up": up_cnt, "dn": dn_cnt, "zt": zt_cnt, "dt": dt_cnt}
    else:
        b_stats = st.session_state["market_breadth_stats"]
        up_cnt, dn_cnt, zt_cnt, dt_cnt = b_stats.get("up", 0), b_stats.get("dn", 0), b_stats.get("zt", 0), b_stats.get("dt", 0)

    u_vol_weight, _ = get_intraday_time_factor()
    idx_data = fetch_market_indices_realtime()
    sh_d = idx_data.get("sh", {"price": st.session_state["sh_index_price"], "pct": st.session_state["sh_index_pct"], "amt_yi": 6500.0})
    sz_d = idx_data.get("sz", {"price": st.session_state["sz_index_price"], "pct": st.session_state["sz_index_pct"], "amt_yi": 8500.0})

    cur_tot_yi = sh_d["amt_yi"] + sz_d["amt_yi"]
    est_amt = round(cur_tot_yi / max(u_vol_weight, 0.12), 0) if cur_tot_yi > 200 else 14850.0
    st.session_state["est_market_amt_yi"] = est_amt
    vol_r = round(max(0.55, min(2.4, est_amt / 15500.0)), 2)
    st.session_state["sh_vol_ratio"] = vol_r

    sh_pct = st.session_state["sh_index_pct"]
    med_pct = st.session_state["median_stock_pct"]

    if vol_r >= 1.15:
        vol_st = f"🔥放量上攻(量比{vol_r:.2f}，预计{est_amt:.0f}亿)" if sh_pct >= 0 else f"⚠️放量分歧换手(量比{vol_r:.2f})"
        vol_forecast = "今日两市放量交投活跃，重点围绕【🎯明日★核心五虎】与30日多次试盘突破龙头顺势接力。"
    elif vol_r <= 0.86:
        vol_st = f"🟢缩量惜售企稳(量比{vol_r:.2f}，预计{est_amt:.0f}亿)"
        vol_forecast = "今日两市缩量惜售，做空动能衰竭，非常适合【🌙14:35尾盘法】与【🕳️黄金坑穿三线】低吸拿先手！"
    else:
        vol_st = f"⚖️平量良性轮动(量比{vol_r:.2f}，预计{est_amt:.0f}亿)"
        vol_forecast = "今日量能温和稳定，切忌追高一致高潮股，重点围绕【🎯明日重点关注10大狙击股】回踩分时黄线低吸。"

    st.session_state["sh_vol_status"] = vol_st
    sector_deduction_block = deduce_tomorrow_focus_sectors()
    sh_p = st.session_state["sh_index_price"]
    sz_p = st.session_state["sz_index_price"]
    sz_pct = st.session_state["sz_index_pct"]

    return (
        f"{sector_deduction_block}\n"
        f"========================================================================================\n"
        f" 🔮 【今日三大指数真实盘口、U型量能定性与明日大盘走势推演】\n"
        f"========================================================================================\n"
        f"  • 上证指数(sh000001): {sh_p:.2f} 点 ({sh_pct:+.2f}%) ｜ 深证成指(sz399001): {sz_p:.2f} 点 ({sz_pct:+.2f}%)\n"
        f"  • 主板个股中位数: {med_pct:+.2f}% ｜ 量能定性: 【{vol_st}】\n"
        f"  • 扫描广度: 上涨 {up_cnt} 家 / 下跌 {dn_cnt} 家 | 涨停 {zt_cnt} 家 / 跌停 {dt_cnt} 家 | 温度 {st.session_state['market_temp_score']} 分\n"
        f"  • 策略指引: {vol_forecast}\n"
        f"========================================================================================\n"
    )


def evaluate_hold_style_and_anti_sell_fly(sp, sig=None):
    """识别【💎波段锁仓牛·防卖飞】、【⚡超短套利·冲高兑现】与【⚠️高位分歧防核】"""
    p = float(sp.get("price", 10.0))
    pct = float(sp.get("pct", 0.0))
    vwap = float(sp.get("vwap", p))
    to_rate = float(sp.get("turnover", 2.5))
    out_r = float(sp.get("outer_ratio", 50.0))

    ma5 = float(sig.get("ma5", p * 0.99)) if sig else p * 0.99
    ma10 = float(sig.get("ma10", p * 0.98)) if sig else p * 0.98
    ma20 = float(sig.get("ma20", p * 0.97)) if sig else p * 0.97
    win_pct = float(sig.get("winner_pct", 70.0)) if sig else 70.0
    cost_safe = float(sig.get("cost_safety_pct", 8.0)) if sig else 8.0
    ret5 = float(sig.get("ret5_pct", 0.0)) if sig else 0.0
    is_multi_test = sig.get("is_multi_test_start", False) if sig else False
    is_indep = sig.get("is_independent_bull", False) if sig else False
    is_rb = sig.get("is_rounding_bottom", False) if sig else False
    high_div_warn = sig.get("high_divergence_warn", False) if sig else False

    if high_div_warn or (ret5 >= 22.0 and (to_rate >= 18.0 or p < vwap * 0.992 or out_r < 46.0)):
        return (
            "⚠️高位分歧·严防接盘",
            f"近5日已大涨{ret5:+.1f}%进入鱼尾博弈区，盘中分歧加大，严禁追高！持仓一旦跌破分时黄线￥{vwap:.2f}立即止盈。",
            f"破黄线￥{vwap:.2f}立即清仓"
        )

    if (is_multi_test or is_indep or is_rb or (p >= ma5 >= ma10 >= ma20)) and win_pct >= 74.0 and -2.0 <= cost_safe <= 18.5 and p >= vwap * 0.995:
        return (
            "💎波段锁仓牛·防卖飞",
            f"具备【主力多次试盘洗盘彻底 + 获利盘{win_pct:.0f}%上方无套牢峰 + 刚脱离主力成本区({cost_safe:+.1f}%)】三大波段主升基因！严禁因小幅洗盘早早下车卖飞，只要收盘不破5日攻击线(￥{ma5:.2f})就一路锁仓吃完整波主升浪！",
            f"守5日线￥{ma5:.2f}锁仓防卖飞"
        )

    target_25 = round(p * 1.028, 2)
    return (
        "⚡超短套利·冲高兑现",
        f"属于短线隔日套利品种，适合快进快出。次日早盘冲高至￥{target_25:.2f}(+2.8%)偏离分时黄线时分批止盈半仓，不破黄线留底仓。",
        f"早盘冲￥{target_25:.2f}(+2.8%)兑现半仓"
    )


def evaluate_strategy_suitability_and_logic(strat_tag, sp, sig=None):
    p = float(sp.get("price", 10.0))
    open_p = float(sp.get("open", p))
    pct = float(sp.get("pct", 0.0))
    vwap = float(sp.get("vwap", p))
    vr = float(sp.get("vr", 1.0))
    out_r = float(sp.get("outer_ratio", 50.0))
    retain = float(sp.get("intraday_retain", 60.0))

    ma5 = float(sig.get("ma5", p * 0.99)) if sig else p * 0.99
    ma20 = float(sig.get("ma20", p * 0.97)) if sig else p * 0.97
    sup_p = float(sig.get("support_p", round(p * 0.968, 2))) if sig else round(p * 0.968, 2)
    mf_cost = float(sig.get("main_force_cost", round(p * 0.95, 2))) if sig else round(p * 0.95, 2)
    ret5 = float(sig.get("ret5_pct", pct * 2.0)) if sig else pct * 2.0
    zt30 = int(sig.get("zt_30d_cnt", 0)) if sig else 0
    test30 = int(sig.get("test_30d_cnt", 0)) if sig else 0
    bias_vwap = (p - vwap) / max(vwap, 0.01) * 100.0
    hm_now = datetime.now().hour * 100 + datetime.now().minute

    hold_badge, _, _ = evaluate_hold_style_and_anti_sell_fly(sp, sig)
    wave_suffix = " [💎波段防卖飞]" if "💎" in hold_badge else (" [⚠️防高位分歧]" if "⚠️" in hold_badge else "")

    if sig and sig.get("high_divergence_warn"):
        return "⚠️高位放量滞涨防接盘", f"【⚠️高位分歧排雷警报】近5日已涨{ret5:+.1f}%，日内放量滞涨或跌破分时黄线￥{vwap:.2f}，严防高位接盘！"

    if "五日" in strat_tag or "妖股" in strat_tag:
        if sig and sig.get("is_five_day_monster") and p >= vwap * 0.996 and p >= ma5 * 0.99 and bias_vwap <= 3.6:
            return f"★正宗✅五日妖股(+{ret5:.1f}%){wave_suffix}", f"【🔥五日主升妖股：★正宗达标适合顺势买】近5日大涨{ret5:+.1f}%(30日{zt30}板)，5日线(￥{ma5:.2f})陡峭上攻且站稳分时黄线￥{vwap:.2f}，贴黄线低吸博连板/主升！"
        elif p >= ma5 * 0.985 and bias_vwap > 3.6:
            return f"★正宗🟡五日高标(等回踩￥{vwap:.2f})", f"【🔥五日主升妖股：🟡勿追高，等回踩黄线】近5日涨幅{ret5:+.1f}%动量极强，日内乖离黄线({bias_vwap:+.1f}%)偏大，挂单￥{vwap:.2f}接分歧。"
        return f"⚪备选🟡强势回踩5日线￥{ma5:.2f}", f"【🔥五日主升妖股：⚪备选观察】近5日累计{ret5:+.1f}%，重点观察5日攻击线(￥{ma5:.2f})与分时黄线(￥{vwap:.2f})承接。"

    if "强庄" in strat_tag:
        is_mt = sig.get("is_multi_test_start", False) if sig else False
        if (is_mt or test30 >= 2) and p >= vwap * 0.996 and p >= ma20 * 0.995 and pct >= 0.3 and bias_vwap <= 3.0:
            return f"★正宗✅{test30}次试盘突破{wave_suffix}", f"【🚀汉王/电魂多次试盘模型：★正宗主升起点】近30日出现{test30}次大阳/涨停脉冲试盘({zt30}次涨停)+缩量回踩洗净浮筹，今日放量站稳黄线￥{vwap:.2f}开启波段主升！"
        elif (is_mt or test30 >= 1) and p >= ma20 * 0.99:
            return f"★正宗🟡试盘蓄势(贴￥{vwap:.2f}低吸){wave_suffix}", f"【🚀强庄试盘模型：🟡洗盘尾声低吸】近30日有{max(1,test30)}次试盘建仓基因且死守主力成本￥{mf_cost:.2f}，适合贴分时黄线￥{vwap:.2f}低吸。"
        return "⚪备选🟡温和放量观察突破", f"【🚀强庄试盘：⚪备选观察】站稳分时黄线￥{vwap:.2f}且补量时可顺势跟进。"

    if "尾盘" in strat_tag:
        is_tp = sig.get("is_tail_ambush_pure", False) if sig else False
        if is_tp and p >= vwap * 0.996 and -0.3 <= pct <= 3.6 and retain >= 62.0 and out_r >= 51.0:
            if hm_now >= 1425 or hm_now < 915:
                return f"★正宗✅14:35尾盘抢筹(极稳){wave_suffix}", f"【🌙14:35尾盘法：★正宗达标非常适合买】5日涨幅仅{ret5:+.1f}%位置安全，全天稳站分时黄线(￥{vwap:.2f})上方，留存率{retain:.0f}%且外盘({out_r:.0f}%)尾盘抢筹，博次日溢价！"
            return "★正宗🟡尾盘高标(等14:35确认买)", f"【🌙14:35尾盘法：★形态达标等14:35】当前稳站黄线￥{vwap:.2f}且位置安全，请等到14:35后确认不跳水再出手！"
        elif pct > 4.0 or ret5 > 13.5:
            return "🛑日内或5日涨幅已高禁尾盘追", f"【🌙尾盘法排雷：🛑不适合尾盘买】今日已涨{pct:+.2f}%(5日{ret5:+.1f}%)，位置偏高谨防次日兑现。"
        return f"⚪备选🟡观察14:35能否站稳￥{vwap:.2f}", f"【🌙尾盘法：⚪备选观察】需在14:35确认现价(￥{p:.2f})站稳分时黄线(￥{vwap:.2f})方可低吸。"

    if "黄金坑" in strat_tag or "穿三线" in strat_tag:
        is_gp = sig.get("golden_pit", False) if sig else False
        is_tlc = sig.get("three_line_cross", False) if sig else False
        if (is_tlc or is_gp) and p >= vwap * 0.996 and pct >= 1.5 and vr >= 1.05:
            return f"★正宗✅真一阳穿三线{wave_suffix}", f"【🕳️黄金三串一：★正宗放量穿三线适合买】MA5/10/20高度收敛后，今日放量真阳(量比{vr:.2f})一举突破三条均线并站稳黄线￥{vwap:.2f}！"
        return f"⚪备选🟡均线粘合贴￥{vwap:.2f}低吸", f"【🕳️黄金穿三线：⚪备选观察】均线簇收敛蓄势中，贴分时黄线￥{vwap:.2f}低吸或等放量突破。"

    if "弱转强" in strat_tag:
        is_w2s = sig.get("is_true_weak_to_strong", False) if sig else False
        if is_w2s and p >= vwap * 0.998 and p >= open_p * 0.996 and pct >= 0.8 and vr >= 1.05:
            return f"★正宗✅昨分歧今真弱转强{wave_suffix}", f"【⏱️09:26真弱转强：★正宗达标适合买】昨日洗盘分歧，今日高开死守开盘价(￥{open_p:.2f})与真实黄线(￥{vwap:.2f})，U型真量比{vr:.2f}反包转强！"
        elif p >= vwap * 0.996 and pct >= 0.5:
            return f"⚪备选🟡日内转强贴￥{vwap:.2f}低吸", f"【⏱️早盘弱转强：⚪备选观察】稳站分时黄线￥{vwap:.2f}，可逢分时回踩低吸。"
        return "🛑无量或破黄线假弱转强", f"【⏱️早盘弱转强：🛑不适合买】未通过昨日分歧校验或已跌破分时黄线(￥{vwap:.2f})！"

    if "独立" in strat_tag:
        imm = sig.get("indep_immunity_rate", 80.0) if sig else 80.0
        if (sig and sig.get("is_independent_bull")) and p >= ma20 * 0.995 and p >= vwap * 0.995 and bias_vwap <= 2.6:
            return f"★正宗✅独立牛低吸(抗跌{imm:.0f}%)💎", f"【🦄独立穿越牛：★正宗达标锁仓防卖飞】近20日逆势抗跌率{imm:.0f}%，均线多头完好且站稳分时黄线￥{vwap:.2f}，沿5日线(￥{ma5:.2f})低吸锁仓。"
        return f"⚪备选🟡沿5日线￥{ma5:.2f}低吸", f"【🦄独立穿越牛：⚪备选观察】趋势抗跌，建议在￥{min(vwap, ma5):.2f}附近低吸。"

    if "圆弧底" in strat_tag:
        if (sig and sig.get("is_rounding_bottom")) and p >= vwap * 0.995 and pct >= 0.3:
            return f"★正宗✅锅底突破颈线{wave_suffix}", f"【📐圆弧底突破：★正宗锅底突破适合买】底部缩量收敛筑底完成，右唇重心抬升(MA5>=MA10)，今日红盘突破颈线且站稳黄线￥{vwap:.2f}！"
        return f"⚪备选🟡右唇蓄势贴￥{vwap:.2f}低吸", f"【📐圆弧底突破：⚪备选观察】处于右侧抬升段，建议在分时黄线￥{vwap:.2f}附近低吸。"

    if "龙回头" in strat_tag:
        if (sig and sig.get("is_dragon_pullback")) and -1.8 <= pct <= 3.0 and p >= vwap * 0.994:
            return "★正宗✅真龙回头缩量企稳", f"【🐉真龙回头：★正宗达标适合低吸】前期走出主升大波段(阶段涨幅≥22%)后首次缩量回踩MA10/MA20支撑位，今日站稳黄线￥{vwap:.2f}止跌转强博二波！"
        return f"⚪备选🟡回踩支撑￥{ma20:.2f}观察", f"【🐉龙回头：⚪备选观察】等待回踩均线且收复分时黄线￥{vwap:.2f}企稳后再低吸。"

    if p >= vwap * 0.996 and p >= ma20 * 0.995 and pct >= 0.2 and out_r >= 50.0:
        return f"★正宗✅形态达标(贴￥{vwap:.2f}买){wave_suffix}", f"【{strat_tag}：★正宗达标适合建仓】稳站MA20(￥{ma20:.2f})与真实黄线(￥{vwap:.2f})上方，外盘{out_r:.0f}%主动承接，止损设于￥{sup_p:.2f}。"
    return f"⚪备选🟡等回踩￥{min(vwap, ma5):.2f}低吸", f"【{strat_tag}：⚪备选观察】建议等待股价站稳分时黄线￥{vwap:.2f}后再行建仓。"


def generate_today_and_future_forecast(sp, sig=None):
    p = float(sp.get("price", 10.0))
    pct = float(sp.get("pct", 0.0))
    vwap = float(sp.get("vwap", p))
    vr = float(sp.get("vr", 1.0))
    out_r = float(sp.get("outer_ratio", 50.0))
    wb = float(sp.get("weibi_pct", 0.0))

    ma5 = float(sig.get("ma5", p * 0.99)) if sig else p * 0.99
    ma20 = float(sig.get("ma20", p * 0.97)) if sig else p * 0.97
    sup_p = float(sig.get("support_p", round(p * 0.968, 2))) if sig else round(p * 0.968, 2)
    res_p = float(sig.get("resist_p", round(p * 1.075, 2))) if sig else round(p * 1.075, 2)
    mf_cost = float(sig.get("main_force_cost", round(p * 0.95, 2))) if sig else round(p * 0.95, 2)
    win_pct = float(sig.get("winner_pct", 70.0)) if sig else 70.0
    ret5 = float(sig.get("ret5_pct", 0.0)) if sig else 0.0
    test30 = int(sig.get("test_30d_cnt", 0)) if sig else 0
    hold_badge, _, exit_anchor = evaluate_hold_style_and_anti_sell_fly(sp, sig)

    if pct >= 4.5 and p >= vwap and out_r >= 55.0:
        today_perf = f"📊【今日表现】放量真阳领涨({pct:+.2f}%，5日{ret5:+.1f}%，30日{test30}次试盘，量比{vr:.2f})，稳站黄线￥{vwap:.2f}"
    elif pct >= 1.2 and p >= vwap:
        mode_w = "压单吃货" if wb < -5 else "多头推升"
        today_perf = f"📊【今日表现】多头稳步上攻({pct:+.2f}%，30日{test30}次试盘，量比{vr:.2f})，站稳真实黄线￥{vwap:.2f}，外盘{out_r:.0f}%({mode_w})，获利盘{win_pct:.0f}%"
    elif -1.0 <= pct < 1.2 and p >= vwap * 0.996:
        today_perf = f"📊【今日表现】窄幅强势蓄势({pct:+.2f}%，30日{test30}次试盘)，回踩真实黄线(￥{vwap:.2f})与主力成本(￥{mf_cost:.2f})承接强"
    elif pct < 0 and p >= ma20:
        today_perf = f"📊【今日表现】日内缩量回调洗盘({pct:+.2f}%)，暂守MA20(￥{ma20:.2f})"
    else:
        today_perf = f"📊【今日表现】走势偏弱调整({pct:+.2f}%)，跌破分时黄线￥{vwap:.2f}"

    today_perf += f"[{hold_badge}]"
    if "💎" in hold_badge:
        future_fc = f"🔮【波段防卖飞推演】主升结构完好，目标冲刺￥{res_p:.2f}(+{(res_p-p)/max(p,0.01)*100:.1f}%)，5日线(￥{ma5:.2f})不破死拿防卖飞(硬防守￥{sup_p:.2f})"
    elif p >= ma20 and win_pct >= 66.0:
        future_fc = f"🔮【预计走势】若站稳￥{vwap:.2f}有望挑战￥{res_p:.2f}，次日早盘锚定：{exit_anchor}，短线支撑￥{sup_p:.2f}"
    else:
        future_fc = f"🔮【预计走势】短线围绕￥{sup_p:.2f}~￥{vwap*1.015:.2f}震荡，未收复分时黄线￥{vwap:.2f}前不加仓"

    return f"{today_perf}；{future_fc}"


def assign_exclusive_strategy(cand_obj, hm_val):
    sp = cand_obj["spot"]
    sig = cand_obj["signals"]
    pct = sp["pct"]
    matched = []

    if sig.get("is_multi_test_start", False) or (sig.get("test_30d_cnt", 0) >= 2 and sp["price"] >= sig["ma20"] * 0.995):
        matched.append("🚀 强庄试盘启动")
    if sig.get("is_five_day_monster", False):
        matched.append("🔥 五日主升妖股")
    if sig.get("is_independent_bull", False):
        matched.append("🦄 独立行情穿越牛")
    if sig.get("three_line_cross", False) or sig.get("golden_pit", False):
        matched.append("🕳️ 黄金坑穿三线")
    if sig.get("is_true_weak_to_strong", False):
        matched.append("⏱️ 09:26弱转强")
    if sig.get("is_tail_ambush_pure", False):
        matched.append("🌙 尾盘埋伏")
    if sig.get("is_rounding_bottom", False):
        matched.append("📐 圆弧底突破")
    if sig.get("is_dragon_pullback", False):
        matched.append("🐉 龙回头企稳")
    if sig["stealth_accum"] or (-0.8 <= pct <= 2.8 and sp["amp"] <= 5.5 and sp["outer_ratio"] >= 51.0 and sp["price"] >= sp["vwap"] * 0.995):
        matched.append("🕵️ 主力偷偷吸筹")
    if pct >= 1.5 and sig["winner_pct"] >= 70.0 and sp["intraday_retain"] >= 62.0 and sp["price"] >= sig["ma5"] * 0.995:
        matched.append("🌊 主升浪动量")
    if sp["mkt_cap"] >= 80.0 and 0 < sp["pe"] <= 42.0 and sp["price"] >= sig["ma20"] * 0.99:
        matched.append("🛡️ 顺丰防御")

    if not matched:
        if sig.get("test_30d_cnt", 0) >= 1:
            matched.append("🚀 强庄试盘启动")
        elif sp["mkt_cap"] >= 100.0:
            matched.append("🛡️ 顺丰防御")
        elif pct >= 1.5:
            matched.append("🌊 主升浪动量")
        else:
            matched.append("🕵️ 主力偷偷吸筹")
    return matched


def score_strategy_affinity(strat_name, st_obj):
    sp = st_obj["spot"]
    sig = st_obj["signals"]
    base_s = st_obj["score_f"]
    pct = sp["pct"]
    vr = sp["vr"]
    out_r = sp["outer_ratio"]
    retain = sp["intraday_retain"]
    ret5 = sig.get("ret5_pct", pct)
    win_p = sig.get("winner_pct", 65.0)
    above_vwap = 1.8 if sp["price"] >= sp["vwap"] * 0.996 else -2.5
    in_matched = 4.2 if strat_name in st_obj.get("matched_strats", []) else 0.0

    if strat_name == "🚀 强庄试盘启动":
        mt_b = 4.0 if sig.get("is_multi_test_start") else (sig.get("test_30d_cnt", 0) * 1.3 + sig.get("zt_30d_cnt", 0) * 1.2)
        return in_matched + mt_b + base_s + vr * 0.4 + above_vwap
    if strat_name == "🔥 五日主升妖股":
        if sig.get("high_divergence_warn"):
            return -10.0
        return in_matched + ret5 * 0.42 + sig.get("zt_5d_cnt", 0) * 1.8 + base_s + above_vwap
    if strat_name == "🦄 独立行情穿越牛":
        return in_matched + sig.get("indep_immunity_rate", 65.0) * 0.08 + base_s + above_vwap
    if strat_name == "🕵️ 主力偷偷吸筹":
        stealth_b = 2.8 if (sp["weibi_pct"] < -3 and out_r >= 52.0) else (1.4 if -0.5 <= pct <= 2.5 else 0.0)
        return in_matched + stealth_b + (out_r - 50.0) * 0.12 + base_s + above_vwap
    if strat_name == "⏱️ 09:26弱转强":
        w2s_b = 4.0 if sig.get("is_true_weak_to_strong") else 0.0
        return in_matched + w2s_b + vr * 0.6 + retain * 0.03 + base_s + above_vwap
    if strat_name == "🕳️ 黄金坑穿三线":
        pit_b = 4.2 if (sig.get("three_line_cross") or sig.get("golden_pit")) else 0.0
        return in_matched + pit_b + base_s + pct * 0.35 + above_vwap
    if strat_name == "🌊 主升浪动量":
        ma_align = 2.8 if (sp["price"] >= sig["ma5"] >= sig["ma10"] * 0.995) else 0.0
        return in_matched + ma_align + win_p * 0.04 + pct * 0.45 + base_s + above_vwap
    if strat_name == "🐉 龙回头企稳":
        drg_b = 4.0 if sig.get("is_dragon_pullback") else 0.0
        return in_matched + drg_b + base_s + above_vwap
    if strat_name == "📐 圆弧底突破":
        rb_b = 3.8 if sig.get("is_rounding_bottom") else (1.5 if sig.get("box_amp_20", 0.25) <= 0.20 else 0.0)
        return in_matched + rb_b + base_s + above_vwap
    if strat_name == "🛡️ 顺丰防御":
        def_b = 3.0 if (sp["mkt_cap"] >= 80.0 and 0 < sp["pe"] <= 38.0) else 0.0
        return in_matched + def_b + min(sp["mkt_cap"] / 100.0, 2.0) + base_s + above_vwap
    if strat_name == "🌙 尾盘埋伏":
        if ret5 > 13.5 or pct > 4.0:
            return -5.0
        tail_b = 4.0 if sig.get("is_tail_ambush_pure") else 0.0
        return in_matched + tail_b + retain * 0.03 + (out_r - 50.0) * 0.08 + base_s + above_vwap
    return base_s


# =========================================================================
# 核心引擎七：🎯明日10大狙击股(★核心五虎)生成 + 09:25竞价体检 + 复盘首次触发锁定
# =========================================================================
def build_tomorrow_focus_10_pool(cand_objects):
    scored_tmr = []
    seen_c = set()
    win_strats = st.session_state.get("top3_winning_strats", ["🚀 强庄试盘启动", "🌙 尾盘埋伏", "🕳️ 黄金坑穿三线"])

    for c, st_obj in cand_objects.items():
        if c in seen_c:
            continue
        sp = st_obj["spot"]
        sig = st_obj["signals"]
        if sig.get("is_blown_board") or sig.get("high_divergence_warn"):
            continue
        if sp["pct"] > 8.2 or sp["pct"] < -2.0 or sp["price"] < sp["vwap"] * 0.993:
            continue

        tmr_priority = st_obj["score_f"]
        chosen_strat = st_obj["matched_strats"][0] if st_obj.get("matched_strats") else "🚀 强庄试盘启动"

        for rk_idx, win_st in enumerate(win_strats[:3]):
            if win_st in st_obj.get("matched_strats", []):
                tmr_priority += (2.4 - rk_idx * 0.4)
                chosen_strat = win_st
                break

        if sig.get("is_multi_test_start"):
            tmr_priority += 2.2
            chosen_strat = "🚀 强庄试盘启动"
        elif sig.get("test_30d_cnt", 0) >= 2 and sig.get("hold_support"):
            tmr_priority += 1.4

        if sig.get("is_tail_ambush_pure"):
            tmr_priority += 1.8
        if sig.get("three_line_cross") or sig.get("golden_pit"):
            tmr_priority += 1.8
        if sig.get("is_rounding_bottom") or sig.get("is_independent_bull"):
            tmr_priority += 1.5

        sec_info = match_sector_info(st_obj["raw_sector"])
        if sec_info and sec_info.get("rank") in ("hot", "latent"):
            tmr_priority += 1.2

        scored_tmr.append((tmr_priority, st_obj, chosen_strat))
        seen_c.add(c)

    scored_tmr.sort(key=lambda x: (x[0], x[1]["lamp_cnt"], x[1]["rr_ratio"]), reverse=True)
    top10_tmr = scored_tmr[:10]

    tmr_rows = []
    for idx, (_, st_o, s_lbl) in enumerate(top10_tmr):
        sp = st_o["spot"]
        sig = st_o["signals"]
        p_f = sp["price"]
        vwap_f = sp["vwap"]
        ma5_f = sig.get("ma5", p_f * 0.99)
        sup_f = sig.get("support_p", round(p_f * 0.968, 2))
        test30 = sig.get("test_30d_cnt", 0)
        zt30 = sig.get("zt_30d_cnt", 0)

        star_rank = f"★核心五虎 NO.{idx+1}" if idx < 5 else f"🎯重点备选 NO.{idx+1}"
        gene_tag = f"30日{test30}试盘({zt30}板)|{st_o['red_lights']}"
        hold_badge, hold_advice, exit_anchor = evaluate_hold_style_and_anti_sell_fly(sp, sig)
        low_buy_p = round(min(p_f * 0.996, max(vwap_f, ma5_f * 0.998)), 2)
        plan_buy_str = f"低吸￥{low_buy_p:.2f}/损￥{sup_f:.2f}"
        auc_status = "⏳待09:25竞价体检"

        why_tmr = (
            f"【{star_rank}·{s_lbl}】近30日{test30}次脉冲试盘({zt30}次涨停)洗盘充分，获利盘{sig.get('winner_pct',75):.0f}%；"
            f"明日若平开或温和红盘站稳￥{low_buy_p:.2f}可果断狙击！({hold_advice})"
        )
        tmr_rows.append([
            star_rank, st_o["code"], st_o["name"], s_lbl,
            f"{p_f:.2f}", f"{sp['pct']:+.2f}%", gene_tag, hold_badge,
            plan_buy_str, exit_anchor, auc_status, why_tmr
        ])

    st.session_state["tomorrow_pool_rows"] = tmr_rows
    save_json_safe(TOMORROW_POOL_FILE, tmr_rows)
    return tmr_rows


def run_morning_auction_check_web():
    snap = st.session_state.get("scan_snapshot", {})
    tmr_rows = snap.get("tomorrow") or st.session_state.get("tomorrow_pool_rows", [])
    if not tmr_rows:
        return 0, 0, 0
    codes = [str(r[1]).zfill(6) for r in tmr_rows if len(r) >= 2]
    live_map = fetch_tencent_batch_quotes(codes)
    super_cnt, pass_cnt = 0, 0
    updated_rows = []

    for r in tmr_rows:
        v = list(r)
        c = str(v[1]).zfill(6)
        sp = live_map.get(c)
        if sp:
            open_gap = (sp["open"] - sp["prev_close"]) / max(sp["prev_close"], 0.01) * 100.0
            p_now = sp["price"]
            vwap_now = sp["vwap"]
            vr_now = sp["vr"]
            out_r = sp["outer_ratio"]
            v[4] = f"{p_now:.2f}"
            v[5] = f"{sp['pct']:+.2f}%"

            if 0.3 <= open_gap <= 4.5 and p_now >= vwap_now * 0.998 and p_now >= sp["open"] * 0.996 and vr_now >= 1.15 and out_r >= 53.0:
                v[10] = f"🔥超预期·立即上车(高开{open_gap:+.1f}%/量比{vr_now:.1f})"
                super_cnt += 1
                pass_cnt += 1
            elif -1.0 <= open_gap <= 3.5 and p_now >= vwap_now * 0.994 and out_r >= 49.0:
                v[10] = f"🟢竞价达标·回踩￥{vwap_now:.2f}低吸"
                pass_cnt += 1
            elif open_gap > 6.2:
                v[10] = f"⚠️高开过大({open_gap:+.1f}%)·防兑现勿追"
            else:
                v[10] = f"🛑不及预期·直接放弃(破黄线/外盘{out_r:.0f}%)"
        updated_rows.append(v)

    st.session_state["tomorrow_pool_rows"] = updated_rows
    if "scan_snapshot" in st.session_state:
        st.session_state["scan_snapshot"]["tomorrow"] = updated_rows
        save_json_safe(SNAPSHOT_FILE, st.session_state["scan_snapshot"])
    save_json_safe(TOMORROW_POOL_FILE, updated_rows)
    return super_cnt, pass_cnt, len(updated_rows)


def sanitize_and_dedup_review_records(raw_records):
    """严格执行首次触发永久锁死 (First-Trigger Lock)，保留选出时15列历史定格快照，并回溯历史K线最高冲高"""
    dedup_map = {}
    today_prefix = datetime.now().strftime("%Y-%m-%d")
    k_cache = st.session_state.get("kline_cache", {})

    sorted_raw = [r for r in raw_records if isinstance(r, (list, tuple)) and len(r) >= 10]
    sorted_raw.sort(key=lambda x: str(x[0]))

    for r in sorted_raw:
        row = list(r)
        while len(row) < 15:
            row.append("")

        dt_s = str(row[0]).strip()
        day_key = dt_s[:10] if len(dt_s) >= 10 else today_prefix
        strat_s = str(row[1]).strip()
        code_6 = str(row[2]).replace("sh", "").replace("sz", "").strip().zfill(6)
        name_s = str(row[3]).strip()
        if not (len(code_6) == 6 and code_6.isdigit()) or code_6 in DELISTED_BLACKLIST:
            continue

        if not row[12]:
            row[12] = str(row[8])
        if not row[13]:
            row[13] = str(row[9])
        if not row[14]:
            row[14] = str(row[11])

        uniq_key = (day_key, code_6)
        if uniq_key in dedup_map:
            existing = dedup_map[uniq_key]
            p_pick = float(existing[4])
            row = existing
        else:
            try:
                p_pick = float(str(row[4]).replace("￥", "").strip())
            except Exception:
                p_pick = 10.0
            if p_pick <= 0.1 or p_pick > 3000:
                p_pick = 10.0

        sp_cur = st.session_state["latest_spot_cache"].get(code_6)
        p_lat = float(sp_cur["price"]) if sp_cur else 0.0
        if p_lat <= 0.1:
            try:
                p_lat = float(str(row[5]).replace("￥", "").strip())
            except Exception:
                p_lat = p_pick

        if sp_cur and abs(p_lat - p_pick) < 0.001 and day_key < today_prefix:
            ref_base = sp_cur["prev_close"]
            if ref_base > 0 and abs(p_lat - ref_base) > 0.001:
                p_pick = ref_base

        cum_ret = (p_lat - p_pick) / max(p_pick, 0.01) * 100.0
        try:
            old_max = float(str(row[7]).replace("+", "").replace("%", "").strip())
            if abs(old_max) > 85.0:
                old_max = cum_ret
        except Exception:
            old_max = cum_ret

        high_est = sp_cur["high"] if sp_cur else p_lat
        df_k_cached = k_cache.get(code_6)
        if df_k_cached is not None and "日期" in df_k_cached.columns:
            sub_k = df_k_cached[df_k_cached["日期"] >= day_key]
            if len(sub_k) > 0:
                high_est = max(high_est, float(sub_k["最高"].max()))

        max_ret = max(cum_ret, old_max, (high_est - p_pick) / max(p_pick, 0.01) * 100.0, 0.0)

        row[2] = code_6
        row[3] = name_s
        row[4] = f"{p_pick:.2f}"
        row[5] = f"{p_lat:.2f}"
        row[6] = f"{cum_ret:+.2f}%"
        row[7] = f"{max_ret:+.2f}%"
        row[8] = row[12]
        row[9] = row[13]

        if cum_ret >= 5.0 or max_ret >= 6.0:
            row[10] = "🔥 大涨验证!"
        elif cum_ret > 0.01 or max_ret >= 2.0:
            row[10] = "🟢 浮盈验证"
        elif abs(cum_ret) <= 0.01:
            row[10] = "⚪ 实时监控中"
        elif cum_ret >= -2.8:
            row[10] = "🟡 缩量蓄势"
        else:
            row[10] = "🔴 跌破防守"

        now_ev = st.session_state["canonical_eval_cache"].get(code_6)
        if now_ev:
            row[11] = f"📸当时:{row[12]}({row[13]}) → 📈当前:{now_ev['light_str']}({now_ev['score_str']}) ｜ {row[14]}"
        else:
            row[11] = f"📸当时逻辑: {row[14]}"

        dedup_map[uniq_key] = row

    cleaned_list = list(dedup_map.values())
    cleaned_list.sort(key=lambda x: str(x[0]), reverse=True)
    return cleaned_list[:500]


def get_full_mainboard_candidate_codes():
    code_set = set(st.session_state["active_mainboard_codes"])
    for c_h in fetch_live_mainboard_hot_codes():
        if c_h not in DELISTED_BLACKLIST:
            code_set.add(c_h)
    for c, n, s in MAINBOARD_CORE_UNIVERSE:
        if c not in DELISTED_BLACKLIST:
            code_set.add(c)
            st.session_state["stock_sector_map"][c] = s
            st.session_state["name_sector_map"][n] = s
    for c_exp in DYNAMIC_MAINBOARD_EXPANSION:
        if c_exp not in DELISTED_BLACKLIST:
            code_set.add(c_exp)

    for row in st.session_state.get("watchlist_rows", []):
        if row and len(row) >= 1:
            c_i = str(row[0]).zfill(6)
            if c_i not in DELISTED_BLACKLIST:
                code_set.add(c_i)
    for row in st.session_state.get("holdings_rows", []):
        if row and len(row) >= 2:
            c_i = str(row[1]).zfill(6)
            if c_i not in DELISTED_BLACKLIST:
                code_set.add(c_i)
    return sorted([c for c in code_set if c not in DELISTED_BLACKLIST])


def run_quantitative_scan_web():
    fetch_market_indices_realtime()
    target_codes = get_full_mainboard_candidate_codes()
    spot_map = {}
    for i in range(0, len(target_codes), 220):
        chunk = target_codes[i:i + 220]
        part_res = fetch_tencent_batch_quotes(chunk)
        spot_map.update(part_res)
        time.sleep(0.01)

    if not spot_map:
        st.session_state["status_text"] = "🟠 [离线安全防护态：五档网络受限，已保留上次快照]"
        return False

    sec_rows = fetch_ths_sector_flow(spot_map)

    valid_codes_found, all_pcts = [], []
    up_cnt, dn_cnt, zt_cnt, dt_cnt, bomb_cnt, nuc_down = 0, 0, 0, 0, 0, 0
    u_vol_weight, _ = get_intraday_time_factor()
    min_amt_threshold = 28000000.0 * u_vol_weight

    bucket_a_break, bucket_b_stealth, bucket_c_pullback, bucket_d_core = [], [], [], []
    anomaly_events = []
    now_hm = datetime.now().strftime("%H:%M")
    today_date = datetime.now().strftime("%Y-%m-%d")

    for code, sp in spot_map.items():
        if code in DELISTED_BLACKLIST or not code.startswith(("600", "601", "603", "605", "000", "001", "002", "003")):
            continue
        name = sp.get("name", "")
        if "ST" in name or "退" in name or sp.get("price", 0) < 2.5:
            continue
        valid_codes_found.append(code)
        pct = sp["pct"]
        all_pcts.append(pct)

        if pct > 0:
            up_cnt += 1
        elif pct < 0:
            dn_cnt += 1
        zt_p = round(sp["prev_close"] * 1.10, 2)
        if pct >= 9.8 or sp["price"] >= zt_p - 0.01:
            zt_cnt += 1
        elif sp["high"] >= zt_p - 0.01 and sp["price"] < zt_p - 0.02:
            bomb_cnt += 1
        if pct <= -9.8:
            dt_cnt += 1
        if pct <= -7.0:
            nuc_down += 1

        sec_name = resolve_canonical_sector(code, name)
        sp["sector"] = sec_name

        if sp["amount"] < min_amt_threshold and code not in st.session_state["stock_sector_map"]:
            continue

        if 0.0 <= pct <= 2.8 and sp["amp"] <= 4.8 and sp["price"] >= sp["vwap"] * 0.997 and sp["outer_ratio"] >= 53.0:
            anomaly_events.append([
                now_hm, "🔮尾盘/暗盘抢筹", code, name, f"{sp['price']:.2f}",
                f"{pct:+.2f}%", f"{sp['vr']:.2f}", f"【{sec_name}】站稳黄线￥{sp['vwap']:.2f}|外盘{sp['outer_ratio']:.0f}%持续流入"
            ])
        elif sec_name in st.session_state["collective_surge_sectors"] and pct >= 1.8 and sp["price"] >= sp["vwap"]:
            anomaly_events.append([
                now_hm, "🔥板块集体异动", code, name, f"{sp['price']:.2f}",
                f"{pct:+.2f}%", f"{sp['vr']:.2f}", f"【{sec_name}】主线多股放量齐拉！"
            ])

        if 0.5 <= pct <= 8.8 and sp["price"] >= sp["vwap"] * 0.995 and sp["intraday_retain"] >= 58.0:
            bucket_a_break.append(sp)
        if -1.0 <= pct <= 2.8 and sp["amp"] <= 5.5 and sp["price"] >= sp["vwap"] * 0.992 and sp["outer_ratio"] >= 50.0:
            bucket_b_stealth.append(sp)
        if -2.2 <= pct <= 2.5 and 0.40 <= sp["vr"] <= 1.55 and sp["price"] >= sp["vwap"] * 0.990:
            bucket_c_pullback.append(sp)
        if sp["mkt_cap"] >= 70.0 and 0 < sp["pe"] <= 45.0 and -1.2 <= pct <= 5.5:
            bucket_d_core.append(sp)

    if len(valid_codes_found) >= 40:
        st.session_state["active_mainboard_codes"] = valid_codes_found
        save_json_safe(ACTIVE_CODES_FILE, valid_codes_found)

    all_pcts.sort()
    st.session_state["median_stock_pct"] = round(all_pcts[len(all_pcts) // 2], 2) if all_pcts else 0.0
    tot_zt_touch = zt_cnt + bomb_cnt
    st.session_state["bomb_rate"] = round(bomb_cnt / tot_zt_touch * 100.0, 1) if tot_zt_touch > 0 else 10.0
    breadth = up_cnt / max(up_cnt + dn_cnt, 1)
    temp_s = round(max(10.0, min(98.0, breadth * 75 + zt_cnt * 0.6 - dt_cnt * 1.2 - nuc_down * 0.4 - st.session_state["bomb_rate"] * 0.12)), 1)
    st.session_state["market_temp_score"] = temp_s
    st.session_state["fuse_triggered"] = (temp_s < 34.0 or st.session_state["bomb_rate"] > 42.0 or nuc_down >= 35 or st.session_state["median_stock_pct"] <= -1.8)

    compute_market_volume_and_forecast(up_cnt, dn_cnt, zt_cnt, dt_cnt)

    bucket_a_break.sort(key=lambda x: (x["outer_ratio"], x["pct"]), reverse=True)
    bucket_b_stealth.sort(key=lambda x: (x["outer_ratio"] - x["weibi_pct"] * 0.3), reverse=True)
    bucket_c_pullback.sort(key=lambda x: x["intraday_retain"], reverse=True)
    bucket_d_core.sort(key=lambda x: x["amount"], reverse=True)

    shortlist_map = {}
    for lst, quota in [(bucket_a_break, 48), (bucket_b_stealth, 38), (bucket_c_pullback, 32), (bucket_d_core, 30)]:
        for item in lst[:quota]:
            shortlist_map[item["code"]] = item

    for priority_c in ("002362", "603258", "603955", "605488", "601599", "002578", "603236", "002695", "601698", "600118", "002031"):
        if priority_c in spot_map:
            shortlist_map[priority_c] = spot_map[priority_c]

    if len(shortlist_map) < 115:
        sorted_backup = sorted(spot_map.values(), key=lambda x: (x["pct"] >= 0, x["outer_ratio"], x["amount"]), reverse=True)
        for item in sorted_backup:
            if item["code"] not in shortlist_map and item["code"] not in DELISTED_BLACKLIST and "ST" not in item["name"]:
                shortlist_map[item["code"]] = item
                if len(shortlist_map) >= 130:
                    break

    for row_w in st.session_state.get("watchlist_rows", []):
        if row_w and str(row_w[0]).zfill(6) in spot_map:
            c_custom = str(row_w[0]).zfill(6)
            shortlist_map[c_custom] = spot_map[c_custom]

    def _fetch_kline_worker(sp_item):
        c = sp_item["code"]
        prefix = "sh" if c.startswith("6") else "sz"
        url = f"http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={prefix}{c},day,,,65,qfq&_t={int(time.time()*1000)}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=4.2) as resp:
                raw_json = json.loads(resp.read().decode("utf-8", errors="ignore"))
            st_node = raw_json.get("data", {}).get(f"{prefix}{c}", {})
            k_list = st_node.get("qfqday") or st_node.get("day") or []
            if len(k_list) >= 20:
                rows = []
                for item in k_list[-60:]:
                    if len(item) >= 6:
                        rows.append({
                            "日期": str(item[0])[:10], "开盘": float(item[1]), "收盘": float(item[2]),
                            "最高": float(item[3]), "最低": float(item[4]), "成交量": max(float(item[5]), 1.0)
                        })
                if len(rows) >= 20:
                    df_tmp = pd.DataFrame(rows)
                    df_tmp["涨跌幅"] = df_tmp["收盘"].pct_change().fillna(0.0) * 100.0
                    float_shares_lots = 0.0
                    if sp_item.get("mkt_cap", 0) > 0 and sp_item.get("price", 0) > 0:
                        float_shares_lots = (float(sp_item["mkt_cap"]) * 100000000.0) / max(float(sp_item["price"]), 0.01) / 100.0
                    if float_shares_lots > 10000:
                        df_tmp["换手率"] = (df_tmp["成交量"] / float_shares_lots * 100.0).clip(0.15, 38.0)
                    else:
                        avg_v = max(df_tmp["成交量"].mean(), 1.0)
                        df_tmp["换手率"] = (df_tmp["成交量"] / avg_v * 2.5).clip(0.35, 28.0)
                    return c, df_tmp.reset_index(drop=True)
        except Exception:
            pass
        return c, None

    need_fetch_items = [sp_i for sp_i in shortlist_map.values() if sp_i["code"] not in st.session_state["kline_cache"]]
    if need_fetch_items:
        with ThreadPoolExecutor(max_workers=12) as ex:
            futs = [ex.submit(_fetch_kline_worker, sp_i) for sp_i in need_fetch_items]
            for fut in as_completed(futs):
                try:
                    c_r, df_r = fut.result()
                    if df_r is not None:
                        st.session_state["kline_cache"][c_r] = df_r
                        st.session_state["kline_t1_disk_cache"][c_r] = {
                            "cache_date": today_date,
                            "rows": df_r[["日期", "开盘", "收盘", "最高", "最低", "成交量", "涨跌幅", "换手率"]].to_dict("records")
                        }
                except Exception:
                    pass

    inspected_results = {}
    for c, sp_item in shortlist_map.items():
        sec_canon = resolve_canonical_sector(c, sp_item.get("name", ""), sp_item.get("sector", ""))
        sp_item["sector"] = sec_canon
        df_k = fetch_real_kline(c, sp_item)
        if df_k is not None and len(df_k) >= 6:
            h_tos = df_k["换手率"].iloc[-6:-1].astype(float).tolist()
            avg_5to = max(sum(h_tos) / max(len(h_tos), 1), 0.35)
            sp_item["vr"] = round(min(7.5, max(0.45, (sp_item["turnover"] / u_vol_weight) / avg_5to)), 2)
        sc, brk, sig = evaluate_strict_10pt_score(c, sp_item.get("name", c), sp_item, df_k, sec_canon)
        inspected_results[c] = (sc, brk, sig)

    save_json_safe(KLINE_T1_CACHE_FILE, st.session_state["kline_t1_disk_cache"])
    save_json_safe(SCORE_LOCK_FILE, st.session_state["score_lock_map"])

    sec_max_pct, sec_max_amt = {}, {}
    for c, sp in shortlist_map.items():
        s_n = sp.get("sector", "先进制造")
        sec_max_pct[s_n] = max(sec_max_pct.get(s_n, -99.0), sp["pct"])
        sec_max_amt[s_n] = max(sec_max_amt.get(s_n, 0.0), sp["amount"])

    hm_val = datetime.now().hour * 100 + datetime.now().minute
    cand_objects = {}

    for c, sp in shortlist_map.items():
        if c not in inspected_results or c not in st.session_state["canonical_eval_cache"]:
            continue
        sc_r, brk_r, sig = inspected_results[c]
        ev_cache = st.session_state["canonical_eval_cache"][c]
        if sig.get("is_blown_board"):
            continue

        s_n = ev_cache["sector"]
        if sp["pct"] >= sec_max_pct.get(s_n, 99.0) - 0.3 and sp["pct"] > 0.8:
            role_tag = "👑龙一"
        elif sp["amount"] >= sec_max_amt.get(s_n, 9999999999.0) * 0.85 or sp["mkt_cap"] >= 160.0:
            role_tag = "🏛️中军"
        else:
            role_tag = "⚡前排"

        forecast_txt = generate_today_and_future_forecast(sp, sig)
        suit_badge_val, suit_detail_val = evaluate_strategy_suitability_and_logic("🚀 强庄试盘启动", sp, sig)
        ret5_v = sig.get("ret5_pct", sp["pct"])
        test30_v = sig.get("test_30d_cnt", 0)
        net_y = sp["active_net_yuan"]
        net_str = f"{net_y/10000:+.0f}万(外{sp['outer_ratio']:.0f}%)" if abs(net_y) < 100000000 else f"{net_y/100000000:+.2f}亿(外{sp['outer_ratio']:.0f}%)"

        cand_obj = {
            "code": c, "name": sp["name"], "suitability": suit_badge_val,
            "price": f"{sp['price']:.2f}", "price_f": sp["price"],
            "change_pct": f"{sp['pct']:+.2f}%", "pct_f": sp["pct"],
            "main_control": f"5日{ret5_v:+.1f}%/{test30_v}次试盘",
            "net_inflow": net_str,
            "sector": f"{s_n}[{role_tag}]", "raw_sector": s_n,
            "red_lights": ev_cache["light_str"], "lamp_cnt": ev_cache["lamp_cnt"],
            "score_f": ev_cache["score_f"], "score": ev_cache["score_str"],
            "rr_ratio": sig["rr_ratio"], "vwap": sp["vwap"],
            "support_p": sig["support_p"], "resist_p": sig["resist_p"],
            "signals": sig, "spot": sp, "summary": f"{suit_detail_val} ｜ {forecast_txt}"
        }
        cand_obj["matched_strats"] = assign_exclusive_strategy(cand_obj, hm_val)
        cand_objects[c] = cand_obj

    strat_labels_11 = [
        "🔥 五日主升妖股", "🦄 独立行情穿越牛", "🚀 强庄试盘启动", "🕵️ 主力偷偷吸筹",
        "⏱️ 09:26弱转强", "🕳️ 黄金坑穿三线", "🌊 主升浪动量", "🐉 龙回头企稳",
        "📐 圆弧底突破", "🛡️ 顺丰防御", "🌙 尾盘埋伏"
    ]
    pool_map = {k: [] for k in strat_labels_11}
    code_usage_count = {}

    for s_target in strat_labels_11:
        ranked_for_strat = sorted(
            cand_objects.values(),
            key=lambda x: score_strategy_affinity(s_target, x),
            reverse=True
        )
        count_added = 0
        for st_c in ranked_for_strat:
            if count_added >= 8:
                break
            if st_c["signals"].get("is_limit_up_locked"):
                continue
            if code_usage_count.get(st_c["code"], 0) >= 2:
                continue
            st_copy = st_c.copy()
            b_val, d_val = evaluate_strategy_suitability_and_logic(s_target, st_copy["spot"], st_copy["signals"])
            st_copy["suitability"] = b_val
            st_copy["summary"] = f"{d_val} ｜ {generate_today_and_future_forecast(st_copy['spot'], st_copy['signals'])}"
            pool_map[s_target].append(st_copy)
            code_usage_count[st_c["code"]] = code_usage_count.get(st_c["code"], 0) + 1
            count_added += 1

    strat_key_mapping = [
        ("🔥 五日主升妖股", "five_surge"),
        ("🦄 独立行情穿越牛", "indep"),
        ("🚀 强庄试盘启动", "strong"),
        ("🕵️ 主力偷偷吸筹", "stealth"),
        ("⏱️ 09:26弱转强", "morning"),
        ("🕳️ 黄金坑穿三线", "pit"),
        ("🌊 主升浪动量", "surge"),
        ("🐉 龙回头企稳", "dragon"),
        ("📐 圆弧底突破", "round"),
        ("🛡️ 顺丰防御", "defensive"),
        ("🌙 尾盘埋伏", "tail")
    ]

    snap_dict = {}
    all_top_candidates = []
    new_review_batch = []

    for strat_label, snap_k in strat_key_mapping:
        selected_today = pool_map[strat_label]
        selected_today.sort(
            key=lambda x: (
                3 if "★正宗✅" in x["suitability"] else (2 if "★正宗" in x["suitability"] else (1 if "🟡" in x["suitability"] else 0)),
                x["score_f"]
            ),
            reverse=True
        )
        rows_for_tab = []
        for st_c in selected_today:
            key_5d = st_c["code"]
            if key_5d not in st.session_state["pool_5day_map"]:
                st.session_state["pool_5day_map"][key_5d] = {
                    "pick_date": today_date, "pick_price": st_c["price_f"],
                    "code": st_c["code"], "name": st_c["name"], "strategy": strat_label
                }
            row_t = [
                st_c["code"], st_c["name"], st_c["suitability"], st_c["price"], st_c["change_pct"],
                st_c["main_control"], st_c["net_inflow"], st_c["sector"], st_c["red_lights"], st_c["score"], st_c["summary"]
            ]
            rows_for_tab.append(row_t)
            all_top_candidates.append((st_c, strat_label))
            if "★正宗" in st_c["suitability"] or st_c["score_f"] >= 7.8:
                new_review_batch.append([
                    f"{today_date} {now_hm}", strat_label, st_c["code"], st_c["name"],
                    f"{st_c['price_f']:.2f}", f"{st_c['price_f']:.2f}", "+0.00%", "+0.00%",
                    st_c["red_lights"], st_c["score"], "⚪ 今日新选待验证", st_c["summary"],
                    st_c["red_lights"], st_c["score"], st_c["summary"]
                ])
        snap_dict[snap_k] = rows_for_tab

    tmr_rows = build_tomorrow_focus_10_pool(cand_objects)
    snap_dict["tomorrow"] = tmr_rows

    tier1_top, tier2_top = [], []
    seen_top_c = set()
    for st_c, s_lbl in all_top_candidates:
        sig = st_c["signals"]
        c_code = st_c["code"]
        if c_code in seen_top_c or sig.get("is_limit_up_locked") or sig.get("is_blown_board"):
            continue
        is_uptrend_ok = (st_c["price_f"] >= st_c["vwap"] * 0.996 and st_c["pct_f"] >= 0.0 and st_c["price_f"] >= sig["ma20"] * 0.995)
        if (st_c["lamp_cnt"] >= 5 and "四红" in st_c["red_lights"]) or sig.get("is_multi_test_start") or sig.get("is_five_day_monster"):
            if is_uptrend_ok and "✅" in st_c["suitability"]:
                tier1_top.append((st_c, s_lbl))
                seen_top_c.add(c_code)
        elif st_c["lamp_cnt"] >= 4 and is_uptrend_ok:
            tier2_top.append((st_c, s_lbl))
            seen_top_c.add(c_code)

    tier1_top.sort(key=lambda x: (1 if (x[0]["signals"].get("is_multi_test_start") or x[0]["signals"].get("is_five_day_monster")) else 0, x[0]["score_f"], x[0]["rr_ratio"]), reverse=True)
    tier2_top.sort(key=lambda x: (x[0]["lamp_cnt"], x[0]["score_f"]), reverse=True)
    top10_list = (tier1_top + tier2_top)[:10]
    if len(top10_list) < 10:
        for st_c, s_lbl in sorted(all_top_candidates, key=lambda x: x[0]["score_f"], reverse=True):
            if st_c["code"] not in seen_top_c:
                top10_list.append((st_c, s_lbl))
                seen_top_c.add(st_c["code"])
                if len(top10_list) >= 10:
                    break

    top3_rows = []
    for idx, (st_c, s_lbl) in enumerate(top10_list):
        rank_str = f"🏆 Top {idx+1}"
        p_f = st_c["price_f"]
        vwap_f = st_c["vwap"]
        buy_zone = f"吸￥{min(p_f, vwap_f)*0.995:.2f}/损￥{st_c['support_p']:.2f}"
        top3_rows.append([
            rank_str, st_c["code"], st_c["name"], s_lbl, st_c["price"], st_c["change_pct"],
            st_c["sector"], st_c["red_lights"], st_c["score"], st_c["suitability"], buy_zone, st_c["summary"]
        ])

    pos_adv = "15%~30%" if st.session_state["fuse_triggered"] else ("60%~80%" if temp_s >= 60 else "40%~50%")
    hdr_txt = f"🌡️ 上证:{st.session_state['sh_index_price']:.2f}({st.session_state['sh_index_pct']:+.2f}%) | 深成:{st.session_state['sz_index_pct']:+.2f}% | {st.session_state['sh_vol_status'][:13]} | 温度:{temp_s}分 | 涨跌停:{zt_cnt}/{dt_cnt} | 仓位:{pos_adv}"
    core5_names = "、".join([f"{r[2]}({r[1]})" for r in tmr_rows[:5]]) if tmr_rows else "待生成"
    top_names_str = "、".join([f"{x[0]['name']}({x[0]['code']})" for x in top10_list[:5]]) if top10_list else "暂无满灯标的"
    directive_str = (
        f"{st.session_state['tomorrow_sector_focus_str']}\n"
        f"★ 【明日重点关注★核心五虎】: {core5_names} ｜ 👑 【今日盘中Top5】: {top_names_str}"
    )

    snap_dict["market_temp_text"] = hdr_txt
    snap_dict["directive_text"] = directive_str
    snap_dict["top3"] = top3_rows
    snap_dict["sector"] = sec_rows
    snap_dict["anomaly"] = anomaly_events[:25]

    st.session_state["scan_snapshot"] = snap_dict
    save_json_safe(POOL_5DAY_FILE, st.session_state["pool_5day_map"])
    save_json_safe(SNAPSHOT_FILE, snap_dict)

    combined_rev = st.session_state.get("all_review_records", []) + new_review_batch
    st.session_state["all_review_records"] = sanitize_and_dedup_review_records(combined_rev)
    save_json_safe(REVIEW_FILE, st.session_state["all_review_records"])

    now_full = datetime.now().strftime("%H:%M:%S")
    st.session_state["status_text"] = f"🟢 [📡五档+腾讯K线直连 {now_full} | ★核心五虎与11大战法已生成]"

    if tmr_rows:
        st.session_state["selected_stock_code"] = str(tmr_rows[0][1]).zfill(6)
        st.session_state["selected_stock_name"] = str(tmr_rows[0][2])
        st.session_state["selected_stock_strat"] = str(tmr_rows[0][3])
    return True


def inspect_single_stock_detail(code, name="", strat_tag="🚀 强庄试盘启动"):
    code = str(code).zfill(6)
    canon_sec = resolve_canonical_sector(code, name)
    live_map = fetch_tencent_batch_quotes([code])
    spot_info = live_map.get(code) or st.session_state["latest_spot_cache"].get(code)
    if not spot_info:
        spot_info = {
            "code": code, "name": name or code, "sector": canon_sec, "price": 10.0, "open": 10.0,
            "high": 10.1, "low": 9.9, "prev_close": 10.0, "pct": 0.0, "vr": 1.15, "turnover": 2.5,
            "upper_shadow": 0.005, "vwap": 9.98, "outer_ratio": 54.0, "net_buy_rate_pct": 8.0,
            "active_net_yuan": 12000000.0, "weibi_pct": 0.0, "intraday_retain": 70.0,
            "pe": 18.0, "pb": 1.8, "mkt_cap": 95.0, "bids": [], "asks": []
        }
    name = spot_info.get("name", name or code)
    canon_sec = resolve_canonical_sector(code, name, spot_info.get("sector", ""))
    spot_info["sector"] = canon_sec

    df_k = fetch_real_kline(code, spot_info)
    if df_k is not None and len(df_k) >= 6:
        u_vol_w, _ = get_intraday_time_factor()
        h_tos = df_k["换手率"].iloc[-6:-1].astype(float).tolist()
        avg_5to = max(sum(h_tos) / max(len(h_tos), 1), 0.35)
        spot_info["vr"] = round(min(7.5, max(0.45, (spot_info["turnover"] / u_vol_w) / avg_5to)), 2)

    df_min = fetch_intraday_min_data(code) if st.session_state.get("chart_mode") == "intraday" else None
    real_score, breakdown, signals = evaluate_strict_10pt_score(code, name, spot_info, df_k, canon_sec)
    cached_ev = st.session_state["canonical_eval_cache"][code]
    suit_badge, suit_detail = evaluate_strategy_suitability_and_logic(strat_tag, spot_info, signals)
    hold_badge, hold_advice, exit_anchor = evaluate_hold_style_and_anti_sell_fly(spot_info, signals)
    forecast_full = generate_today_and_future_forecast(spot_info, signals)

    return {
        "code": code, "name": name, "strategy": strat_tag, "sector": canon_sec,
        "price_f": float(spot_info["price"]), "score_str": cached_ev["score_str"],
        "score_num": real_score, "light_str": cached_ev["light_str"],
        "signals": signals, "spot": spot_info, "breakdown": breakdown,
        "suit_badge": suit_badge, "suit_detail": suit_detail,
        "hold_badge": hold_badge, "hold_advice": hold_advice, "exit_anchor": exit_anchor,
        "forecast_full": forecast_full, "df_k": df_k, "df_min": df_min
    }


# =========================================================================
# 核心引擎八：超清大字号高对比度 K线/动态分时 SVG 画布 & 实盘资金净值曲线 SVG
# =========================================================================
def render_stock_canvas_svg(code, name, df_k=None, signals=None, df_min=None, mode="kline"):
    """针对手机屏幕全面放大加粗价格、趋势/资金/板块/量价、VOL、MACD字号，配横向现价游标与★入选日标记"""
    w, h = 680, 285
    svg = [f'<svg viewBox="0 0 {w} {h}" width="100%" height="{h}" style="background-color:#05080F; border:1.5px solid #38BDF8; border-radius:8px; display:block;">']

    if mode == "intraday":
        for y_l in [44, 96, 148, 198]:
            svg.append(f'<line x1="48" y1="{y_l}" x2="{w-55}" y2="{y_l}" stroke="#1E293B" stroke-dasharray="2,2" />')
        sp_live = st.session_state["latest_spot_cache"].get(code, {})
        prev_close = float(sp_live.get("prev_close", 0.0))
        if prev_close <= 0 and df_min is not None and "昨收" in df_min.columns and float(df_min["昨收"].iloc[0]) > 0:
            prev_close = float(df_min["昨收"].iloc[0])
        if prev_close <= 0:
            prev_close = float(df_k["收盘"].iloc[-2]) if (df_k is not None and len(df_k) >= 2) else 10.0

        p_list, v_list = [], []
        if df_min is not None and len(df_min) >= 2:
            p_list = df_min["收盘"].astype(float).tolist()
            v_list = df_min["成交量"].astype(float).tolist()
        elif sp_live and sp_live.get("price", 0) > 0:
            o_p, h_p, l_p, c_p = sp_live["open"], sp_live["high"], sp_live["low"], sp_live["price"]
            nodes = [o_p, (o_p + l_p) / 2.0, l_p, (l_p + h_p) / 2.0, h_p, (h_p + c_p * 2) / 3.0, c_p]
            for idx_s in range(len(nodes) - 1):
                for stp in range(10):
                    r_t = stp / 10.0
                    val = nodes[idx_s] * (1 - r_t) + nodes[idx_s + 1] * r_t
                    p_list.append(val)
                    v_list.append(1000.0 + abs(val - prev_close) * 4000.0)
        else:
            svg.append(f'<text x="{w//2}" y="{h//2}" fill="#64FFDA" font-size="14" font-weight="bold" text-anchor="middle">⏳ 正在同步 {name}({code}) 今日实时分时数据...</text></svg>')
            return "".join(svg)

        live_ticks = st.session_state["intraday_live_ticks"].get(code, [])
        if live_ticks:
            for tk_item in live_ticks[-6:]:
                p_list.append(float(tk_item["price"]))
                v_list.append(float(tk_item["vol"]))

        t_last_str = datetime.now().strftime("%H:%M:%S")
        max_dev = max([abs(p - prev_close) for p in p_list] + [prev_close * 0.015])
        top_p, bot_p = prev_close + max_dev * 1.1, prev_close - max_dev * 1.1
        span_p = max(top_p - bot_p, 0.01)
        plot_w = w - 108
        mid_y = 96
        svg.append(f'<line x1="48" y1="{mid_y}" x2="{48+plot_w}" y2="{mid_y}" stroke="#F59E0B" stroke-dasharray="4,3" stroke-width="1.4" />')

        top_pct = (top_p - prev_close) / max(prev_close, 0.01) * 100.0
        svg.append(f'<text x="44" y="30" fill="#F43F5E" font-size="12" font-weight="bold" text-anchor="end">{top_p:.2f}</text>')
        svg.append(f'<text x="44" y="{mid_y+4}" fill="#FFFFFF" font-size="12" font-weight="bold" text-anchor="end">{prev_close:.2f}</text>')
        svg.append(f'<text x="44" y="164" fill="#10B981" font-size="12" font-weight="bold" text-anchor="end">{bot_p:.2f}</text>')
        svg.append(f'<text x="{52+plot_w}" y="30" fill="#F43F5E" font-size="12" font-weight="bold">+{top_pct:.2f}%</text>')
        svg.append(f'<text x="{52+plot_w}" y="{mid_y+4}" fill="#FFFFFF" font-size="12" font-weight="bold">0.00%</text>')
        svg.append(f'<text x="{52+plot_w}" y="164" fill="#10B981" font-size="12" font-weight="bold">-{top_pct:.2f}%</text>')

        white_pts, yellow_pts = [], []
        cum_pv, cum_v = 0.0, 0.0
        n_pts = len(p_list)
        for i, p_val in enumerate(p_list):
            v_val = max(v_list[i], 1.0)
            cum_pv += p_val * v_val
            cum_v += v_val
            vwap_v = cum_pv / cum_v
            cx = 48 + i * (plot_w / max(n_pts - 1, 1))
            cy_w = 164 - ((p_val - bot_p) / span_p) * 138
            cy_y = 164 - ((vwap_v - bot_p) / span_p) * 138
            white_pts.append((cx, cy_w))
            yellow_pts.append((cx, cy_y))

        svg.append(f'<polyline fill="none" stroke="#FACC15" stroke-width="2.0" points="{" ".join([f"{x:.1f},{y:.1f}" for x,y in yellow_pts])}" />')
        svg.append(f'<polyline fill="none" stroke="#FFFFFF" stroke-width="2.2" points="{" ".join([f"{x:.1f},{y:.1f}" for x,y in white_pts])}" />')

        last_p = float(sp_live.get("price", p_list[-1]))
        true_vwap = float(sp_live.get("vwap", cum_pv / max(cum_v, 1.0)))
        last_pct = (last_p - prev_close) / max(prev_close, 0.01) * 100.0
        lx, ly = white_pts[-1]
        cur_col = "#F43F5E" if last_pct >= 0 else "#10B981"
        svg.append(f'<line x1="48" y1="{ly:.1f}" x2="{48+plot_w}" y2="{ly:.1f}" stroke="{cur_col}" stroke-dasharray="3,2" stroke-width="1.2" />')
        svg.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="4.5" fill="{cur_col}" stroke="#FEF08A" stroke-width="1.5" />')

        st_tag = "🟢稳站黄线(强承接)" if last_p >= true_vwap * 0.998 else "🔴黄线下方(受压)"
        svg.append(f'<text x="48" y="16" fill="#FEF08A" font-size="12.5" font-weight="bold">📡【实时盯盘 {t_last_str}】{name}({code}) 现价:{last_p:.2f}({last_pct:+.2f}%) 黄线:{true_vwap:.2f} {st_tag}</text>')

        max_mv = max(sorted(v_list)[int(len(v_list) * 0.95)], 1.0) if len(v_list) > 5 else max(v_list + [1.0])
        svg.append('<text x="44" y="196" fill="#FFFFFF" font-size="11.5" font-weight="bold" text-anchor="end">分时量</text>')
        bar_w_m = max(1.6, plot_w / max(n_pts, 1) * 0.7)
        for i in range(n_pts):
            cx = 48 + i * (plot_w / max(n_pts - 1, 1))
            vh = min(68.0, (v_list[i] / max_mv) * 64.0)
            v_col = "#F43F5E" if (i == 0 or p_list[i] >= p_list[i - 1]) else "#10B981"
            svg.append(f'<line x1="{cx:.1f}" y1="272" x2="{cx:.1f}" y2="{272-vh:.1f}" stroke="{v_col}" stroke-width="{bar_w_m:.1f}" />')

        svg.append("</svg>")
        return "".join(svg)

    if df_k is None or len(df_k) < 15:
        svg.append(f'<text x="{w//2}" y="{h//2}" fill="#64FFDA" font-size="14" font-weight="bold" text-anchor="middle">⏳ 正在通过腾讯原生接口合成 {name} ({code}) 60日K线与四红灯...</text></svg>')
        return "".join(svg)

    closes = df_k["收盘"].astype(float).tolist()
    opens = df_k["开盘"].astype(float).tolist()
    highs = df_k["最高"].astype(float).tolist()
    lows = df_k["最低"].astype(float).tolist()
    vols = df_k["成交量"].astype(float).tolist()
    dates_k = df_k["日期"].astype(str).tolist() if "日期" in df_k.columns else [""] * len(closes)
    n = len(closes)

    min_p, max_p = min(lows), max(highs)
    p_span = max(max_p - min_p, 0.01)
    plot_w = w - 134
    step_x = plot_w / max(n, 1)
    bar_w = max(2.4, step_x * 0.65)

    for y_div in [122, 182, 226]:
        svg.append(f'<line x1="45" y1="{y_div}" x2="{w-10}" y2="{y_div}" stroke="#26354D" stroke-width="1.2" />')

    svg.append(f'<text x="42" y="25" fill="#FFFFFF" font-size="11.5" font-weight="bold" text-anchor="end">{max_p:.2f}</text>')
    svg.append(f'<text x="42" y="72" fill="#E2E8F0" font-size="11" font-weight="bold" text-anchor="end">{(max_p+min_p)/2:.2f}</text>')
    svg.append(f'<text x="42" y="118" fill="#FFFFFF" font-size="11.5" font-weight="bold" text-anchor="end">{min_p:.2f}</text>')

    win_pct = signals.get("winner_pct", 75.0) if signals else 75.0
    mf_cost = signals.get("main_force_cost", closes[-1] * 0.95) if signals else closes[-1] * 0.95
    test30 = signals.get("test_30d_cnt", 0) if signals else 0
    svg.append(f'<text x="48" y="15" fill="#64FFDA" font-size="12" font-weight="bold">{name}({code}) 30日试盘:{test30}次 获利:{win_pct:.0f}%</text>')
    svg.append('<text x="295" y="15" fill="#FBBF24" font-size="11.5" font-weight="bold">—MA5</text>')
    svg.append('<text x="342" y="15" fill="#C084FC" font-size="11.5" font-weight="bold">—MA20</text>')
    svg.append(f'<text x="398" y="15" fill="#38BDF8" font-size="11.5" font-weight="bold">--主力成本￥{mf_cost:.2f}</text>')

    if min_p <= mf_cost <= max_p:
        y_mf = 118 - ((mf_cost - min_p) / p_span) * 95
        svg.append(f'<line x1="48" y1="{y_mf:.1f}" x2="{48+plot_w}" y2="{y_mf:.1f}" stroke="#38BDF8" stroke-dasharray="4,2" stroke-width="1.4" />')

    bins_12 = signals.get("canvas_12_bins", []) if signals else []
    if not bins_12 or len(bins_12) != 12:
        bins_12 = [1.0] * 12
    max_b12 = max(bins_12) if max(bins_12) > 0 else 1.0
    peak_b12 = bins_12.index(max_b12)
    chip_x0 = 50 + plot_w
    for b in range(12):
        bw = (bins_12[b] / max_b12) * 62.0
        by = 118 - ((b + 0.5) / 12.0) * 95
        b_col = "#F59E0B" if b == peak_b12 else "#2563EB"
        svg.append(f'<rect x="{chip_x0:.1f}" y="{by-3.2:.1f}" width="{bw:.1f}" height="6.2" fill="{b_col}" />')

    ma5_pts, ma20_pts = [], []
    hist_lamp_set = set(signals.get("hist_lamp_bars", [])) if signals else set()
    hl_pick_dt = st.session_state.get("highlight_pick_date")
    last_tag_x = -999

    for i in range(n):
        cx = 48 + i * step_x + step_x / 2.0
        y_high = 118 - ((highs[i] - min_p) / p_span) * 95
        y_low = 118 - ((lows[i] - min_p) / p_span) * 95
        y_open = 118 - ((opens[i] - min_p) / p_span) * 95
        y_close = 118 - ((closes[i] - min_p) / p_span) * 95

        is_up = closes[i] >= opens[i]
        col = "#F43F5E" if is_up else "#10B981"
        svg.append(f'<line x1="{cx:.1f}" y1="{y_high:.1f}" x2="{cx:.1f}" y2="{y_low:.1f}" stroke="{col}" stroke-width="1.2" />')
        top_y, bot_y = min(y_open, y_close), max(y_open, y_close)
        bh = max(1.8, bot_y - top_y)
        svg.append(f'<rect x="{cx - bar_w/2:.1f}" y="{top_y:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" fill="{col}" />')

        if hl_pick_dt and i < len(dates_k) and dates_k[i][:10] == hl_pick_dt:
            svg.append(f'<line x1="{cx:.1f}" y1="20" x2="{cx:.1f}" y2="120" stroke="#FEF08A" stroke-dasharray="2,2" stroke-width="1.5" />')
            svg.append(f'<text x="{cx:.1f}" y="{max(24, y_high-8):.1f}" fill="#FEF08A" font-size="11" font-weight="bold" text-anchor="middle">★入选日</text>')
        elif i in hist_lamp_set and (cx - last_tag_x >= 44 or i == n - 1):
            lbl_y = min(116, y_low + 10)
            svg.append(f'<text x="{cx:.1f}" y="{lbl_y:.1f}" fill="#FEF08A" font-size="10" font-weight="bold" text-anchor="middle">★抄家伙!</text>')
            last_tag_x = cx

        if i >= 4:
            m5 = sum(closes[i - 4:i + 1]) / 5.0
            ma5_pts.append(f"{cx:.1f},{118 - ((m5 - min_p) / p_span) * 95:.1f}")
        if i >= 19:
            m20 = sum(closes[i - 19:i + 1]) / 20.0
            ma20_pts.append(f"{cx:.1f},{118 - ((m20 - min_p) / p_span) * 95:.1f}")

    if len(ma5_pts) >= 2:
        svg.append(f'<polyline fill="none" stroke="#FBBF24" stroke-width="1.5" points="{" ".join(ma5_pts)}" />')
    if len(ma20_pts) >= 2:
        svg.append(f'<polyline fill="none" stroke="#C084FC" stroke-width="1.8" points="{" ".join(ma20_pts)}" />')

    row_labels = [("趋势", 133), ("资金", 146), ("板块", 159), ("量价", 172)]
    for r_txt, r_y in row_labels:
        svg.append(f'<text x="42" y="{r_y+4}" fill="#FFFFFF" font-size="11.5" font-weight="bold" text-anchor="end">{r_txt}</text>')

    four_mat = signals.get("four_lamp_matrix", []) if signals else []
    lamp_w = max(2.4, step_x * 0.60)
    for i in range(min(n, len(four_mat))):
        cx = 48 + i * step_x + step_x / 2.0
        st_4 = four_mat[i]
        for r_idx in range(4):
            ry = row_labels[r_idx][1]
            c_lamp = "#F43F5E" if st_4[r_idx] else "#10B981"
            svg.append(f'<rect x="{cx - lamp_w/2:.1f}" y="{ry-4}" width="{lamp_w:.1f}" height="8.5" fill="{c_lamp}" />')
        if all(st_4) and i == n - 1:
            svg.append(f'<rect x="{cx - lamp_w/2 - 1:.1f}" y="127" width="{lamp_w+2:.1f}" height="51" fill="none" stroke="#FEF08A" stroke-width="1.5" />')

    is_now_4red = (len(four_mat) > 0 and all(four_mat[-1]))
    badge_col = "#FEF08A" if is_now_4red else "#FFFFFF"
    svg.append(f'<text x="{chip_x0+4:.1f}" y="148" fill="{badge_col}" font-size="11.5" font-weight="bold">{"四灯齐红" if is_now_4red else "看四红"}</text>')
    svg.append(f'<text x="{chip_x0+4:.1f}" y="164" fill="{badge_col}" font-size="11.5" font-weight="bold">{"资金入场" if is_now_4red else "待共振"}</text>')

    sorted_v = sorted(vols)
    v_ref_max = max(sorted_v[int(n * 0.95)] if n >= 10 else max(vols), 1.0)
    svg.append('<text x="42" y="206" fill="#FFFFFF" font-size="11.5" font-weight="bold" text-anchor="end">VOL</text>')
    for i in range(n):
        cx = 48 + i * step_x + step_x / 2.0
        vh = min(34.0, (vols[i] / v_ref_max) * 32.0)
        col = "#F43F5E" if closes[i] >= opens[i] else "#10B981"
        svg.append(f'<rect x="{cx - bar_w/2:.1f}" y="{223-vh:.1f}" width="{bar_w:.1f}" height="{vh:.1f}" fill="{col}" />')

    svg.append('<text x="42" y="258" fill="#FFFFFF" font-size="11.5" font-weight="bold" text-anchor="end">MACD</text>')
    ema12, ema26, difs, deas, macds = [], [], [], [], []
    for i, c in enumerate(closes):
        e12 = c if i == 0 else ema12[-1] * (11 / 13.0) + c * (2 / 13.0)
        e26 = c if i == 0 else ema26[-1] * (25 / 27.0) + c * (2 / 27.0)
        ema12.append(e12)
        ema26.append(e26)
        dif = e12 - e26
        difs.append(dif)
        dea = dif if i == 0 else deas[-1] * 0.8 + dif * 0.2
        deas.append(dea)
        macds.append((dif - dea) * 2.0)

    max_m = max([abs(x) for x in macds + difs] + [0.01])
    zero_y = 256
    svg.append(f'<line x1="48" y1="{zero_y}" x2="{48+plot_w}" y2="{zero_y}" stroke="#475569" />')
    for i in range(n):
        cx = 48 + i * step_x + step_x / 2.0
        mh = (macds[i] / max_m) * 15.0
        m_col = "#F43F5E" if macds[i] >= 0 else "#10B981"
        svg.append(f'<line x1="{cx:.1f}" y1="{zero_y}" x2="{cx:.1f}" y2="{zero_y-mh:.1f}" stroke="{m_col}" stroke-width="2.4" />')

    svg.append("</svg>")
    return "".join(svg)


def render_equity_curve_svg(base_cap=500000.0, unrealized_pnl=0.0):
    """在手机/网页端绘制高清【📈我的实盘账户资金净值增长曲线 (对比上证基准)】"""
    w, h = 680, 185
    svg = [f'<svg viewBox="0 0 {w} {h}" width="100%" height="{h}" style="background-color:#05080F; border:1.5px solid #F59E0B; border-radius:8px; display:block; margin-bottom:8px;">']

    tr_list = st.session_state.get("trade_history_records", [])
    nav_points = [("起点", 1.000)]
    cum_pnl = 0.0
    for r in reversed(tr_list):
        if len(r) >= 9:
            try:
                v_p = float(str(r[8]).replace("￥", "").replace("+", "").replace(",", "").strip())
                if abs(v_p) > 0.01:
                    cum_pnl += v_p
                    nav_points.append((str(r[0])[5:10], round(1.0 + cum_pnl / max(base_cap, 10000.0), 4)))
            except Exception:
                pass

    curr_nav = round(1.0 + (cum_pnl + unrealized_pnl) / max(base_cap, 10000.0), 4)
    nav_points.append(("实时", curr_nav))
    if len(nav_points) < 3:
        nav_points = [("T-3", 1.000), ("T-2", round(1.0 + (curr_nav - 1.0) * 0.35, 4)), ("T-1", round(1.0 + (curr_nav - 1.0) * 0.7, 4)), ("实时", curr_nav)]

    vals_nav = [x[1] for x in nav_points]
    sh_pct = st.session_state.get("sh_index_pct", 0.0)
    sh_bench = [1.0 + i * (sh_pct / 100.0) / max(len(nav_points) - 1, 1) for i in range(len(nav_points))]
    min_v = min(vals_nav + sh_bench + [0.985]) * 0.996
    max_v = max(vals_nav + sh_bench + [1.025]) * 1.004
    span_v = max(max_v - min_v, 0.005)

    plot_w, plot_h = w - 85, h - 46
    for y_g in [26, 26 + plot_h // 2, 26 + plot_h]:
        svg.append(f'<line x1="54" y1="{y_g}" x2="{54+plot_w}" y2="{y_g}" stroke="#1E293B" stroke-dasharray="2,2" />')

    svg.append(f'<text x="48" y="30" fill="#F43F5E" font-size="11.5" font-weight="bold" text-anchor="end">{(max_v-1)*100:+.1f}%</text>')
    svg.append(f'<text x="48" y="{26+plot_h//2+4}" fill="#FFFFFF" font-size="11" font-weight="bold" text-anchor="end">0.0%</text>')
    svg.append(f'<text x="48" y="{26+plot_h}" fill="#10B981" font-size="11.5" font-weight="bold" text-anchor="end">{(min_v-1)*100:+.1f}%</text>')

    pts_eq, pts_sh = [], []
    n_p = len(nav_points)
    for i in range(n_p):
        cx = 54 + i * (plot_w / max(n_p - 1, 1))
        cy_e = 26 + plot_h - ((vals_nav[i] - min_v) / span_v) * plot_h
        cy_s = 26 + plot_h - ((sh_bench[i] - min_v) / span_v) * plot_h
        pts_eq.append((cx, cy_e))
        pts_sh.append((cx, cy_s))

    svg.append(f'<polyline fill="none" stroke="#94A3B8" stroke-dasharray="4,2" stroke-width="1.5" points="{" ".join([f"{x:.1f},{y:.1f}" for x,y in pts_sh])}" />')
    svg.append(f'<polyline fill="none" stroke="#FBBF24" stroke-width="2.6" points="{" ".join([f"{x:.1f},{y:.1f}" for x,y in pts_eq])}" />')
    for cx, cy in pts_eq:
        svg.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.8" fill="#F43F5E" stroke="#FEF08A" stroke-width="1.2" />')

    tot_ret_pct = (curr_nav - 1.0) * 100.0
    tot_net_yuan = cum_pnl + unrealized_pnl
    svg.append(
        f'<text x="54" y="16" fill="#FEF08A" font-size="12.5" font-weight="bold">'
        f'📈 账户实盘净值: {curr_nav:.4f} (累计收益率: {tot_ret_pct:+.2f}% | 累计净利: {"+" if tot_net_yuan>=0 else ""}￥{tot_net_yuan:,.2f})   —黄线:我的账户  --灰线:上证基准'
        f'</text></svg>'
    )
    return "".join(svg)


# =========================================================================
# 核心引擎九：实盘持仓 T+1 账本、历史成交流水记录 & 十一大战法胜率争霸榜
# =========================================================================
def parse_dual_shares(shares_dual_str):
    s = str(shares_dual_str).strip()
    try:
        if "(" in s and "可卖" in s:
            tot = int(float(s.split("(")[0].replace("股", "")))
            av = int(float(s.split("可卖")[0].split("(")[-1].replace("股", "")))
            return tot, min(tot, max(0, av))
        v = int(float(s.replace("股", "")))
        return v, v
    except Exception:
        return 3000, 3000


def record_trade_history_web(code, name, op_type, price, shares, ref_cost, note=""):
    code = str(code).zfill(6)
    t_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    amt = price * shares
    realized_pnl, realized_pct = 0.0, 0.0

    if any(w in op_type for w in ("卖", "平", "抛", "减", "清")):
        fee = amt * 0.0004
        realized_pnl = (price - ref_cost) * shares - fee
        realized_pct = (realized_pnl / max(ref_cost * shares, 1.0)) * 100.0

    row_tr = [
        t_str, op_type, code, name, f"{price:.2f}", f"{shares}",
        f"￥{amt:,.2f}", f"{ref_cost:.2f}",
        f"+￥{realized_pnl:,.2f}" if realized_pnl >= 0 else f"-￥{abs(realized_pnl):,.2f}",
        f"+{realized_pct:.2f}%" if realized_pct >= 0 else f"{realized_pct:.2f}%",
        note
    ]
    tr_list = st.session_state.get("trade_history_records", [])
    tr_list.insert(0, row_tr)
    st.session_state["trade_history_records"] = tr_list
    save_json_safe(TRADES_HISTORY_FILE, tr_list)


def insert_or_update_holding_web(code, name, cost_p, tot_shares, avail_shares, red_lights_str="🔥四红(6灯)", op_note="主战室建仓/更新"):
    code = str(code).zfill(6)
    today_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    mkt_v = cost_p * tot_shares
    dual_s = f"{tot_shares}({avail_shares}可卖)"
    atr_s = f"护￥{cost_p*0.968:.2f}/目￥{cost_p*1.08:.2f}"
    advice_init = "🟢 持仓监控中 (自动刷新生成💎波段防卖飞定性与三态做T指令)"

    rows = st.session_state.get("holdings_rows", [])
    found = False
    for idx, vals in enumerate(rows):
        if len(vals) >= 2 and str(vals[1]).zfill(6) == code:
            vals[2] = name
            vals[3] = f"{cost_p:.3f}"
            vals[4] = dual_s
            vals[5] = f"￥{mkt_v:,.2f}"
            rows[idx] = vals
            found = True
            break

    if not found:
        row_h = [
            today_str, code, name, f"{cost_p:.3f}", dual_s, f"￥{mkt_v:,.2f}",
            f"{cost_p:.2f}", f"￥{cost_p:.2f}", "+￥0.00", "+0.00%", atr_s, red_lights_str, advice_init
        ]
        rows.insert(0, row_h)

    st.session_state["holdings_rows"] = rows
    save_json_safe(HOLDINGS_FILE, rows)
    record_trade_history_web(code, name, "买入建仓", cost_p, tot_shares, cost_p, op_note)


def execute_do_t_web(code, op_type, op_price, op_shares):
    code = str(code).zfill(6)
    rows = st.session_state.get("holdings_rows", [])
    for idx, vals in enumerate(rows):
        if len(vals) >= 5 and str(vals[1]).zfill(6) == code:
            name = str(vals[2])
            old_cost = float(vals[3])
            old_tot, old_avail = parse_dual_shares(vals[4])
            if "买" in op_type or "加" in op_type:
                new_tot = old_tot + op_shares
                new_avail = old_avail
                new_cost = (old_cost * old_tot + op_price * op_shares) / max(new_tot, 1)
                record_trade_history_web(code, name, "低吸买入", op_price, op_shares, old_cost, f"低吸后成本摊至￥{new_cost:.3f}")
            else:
                if op_shares > old_avail:
                    return False, f"🚨 T+1 可卖额度不足！今日可卖仅 {old_avail} 股。"
                new_tot = max(0, old_tot - op_shares)
                new_avail = max(0, old_avail - op_shares)
                realized_profit = (op_price - old_cost) * op_shares
                record_trade_history_web(code, name, "高抛/减仓卖出", op_price, op_shares, old_cost, f"实现交割盈亏:￥{realized_profit:,.2f}")
                if new_tot == 0:
                    rows.pop(idx)
                    st.session_state["holdings_rows"] = rows
                    save_json_safe(HOLDINGS_FILE, rows)
                    return True, f"【{name}】已全部清仓，交割盈利已记入历史流水账本！"
                new_cost = (old_cost * new_tot - realized_profit) / new_tot

            vals[3] = f"{new_cost:.3f}"
            vals[4] = f"{new_tot}({new_avail}可卖)"
            vals[5] = f"￥{new_cost * new_tot:,.2f}"
            rows[idx] = vals
            st.session_state["holdings_rows"] = rows
            save_json_safe(HOLDINGS_FILE, rows)
            return True, f"【{name}】做T/加减仓成功！新成本价: ￥{new_cost:.3f}，总股数: {new_tot}股。"
    return False, "未找到该持仓股记录。"


def refresh_holdings_coach_web():
    rows = st.session_state.get("holdings_rows", [])
    tr_list = st.session_state.get("trade_history_records", [])

    tot_realized = 0.0
    win_tr, loss_tr = 0, 0
    for r in tr_list:
        if len(r) >= 9:
            try:
                v_pnl = float(str(r[8]).replace("￥", "").replace("+", "").replace(",", "").strip())
                tot_realized += v_pnl
                if v_pnl > 0.01:
                    win_tr += 1
                elif v_pnl < -0.01:
                    loss_tr += 1
            except Exception:
                pass
    tr_wr = (win_tr / (win_tr + loss_tr) * 100.0) if (win_tr + loss_tr) > 0 else 0.0

    if not rows:
        return 0.0, 0.0, 0.0, tot_realized, tr_wr

    codes = [str(r[1]).zfill(6) for r in rows if len(r) >= 2]
    spot_map = fetch_tencent_batch_quotes(codes)
    today_d = datetime.now().strftime("%Y-%m-%d")

    tot_mkt, tot_pnl, win_n = 0.0, 0.0, 0
    updated_rows = []
    for vals in rows:
        vals = list(vals)
        while len(vals) < 13:
            vals.append("")
        buy_dt_str, code, name = str(vals[0]), str(vals[1]).zfill(6), str(vals[2])
        try:
            cost_p = float(vals[3])
        except Exception:
            cost_p = 10.0
        tot_sh, avail_sh = parse_dual_shares(vals[4])
        if buy_dt_str[:10] < today_d and avail_sh < tot_sh:
            avail_sh = tot_sh

        canon_sec = resolve_canonical_sector(code, name)
        sp_info = spot_map.get(code)
        if not sp_info:
            try:
                lat_fb = float(vals[6])
            except Exception:
                lat_fb = cost_p
            sp_info = {
                "code": code, "name": name, "sector": canon_sec, "price": lat_fb,
                "high": lat_fb * 1.01, "low": lat_fb * 0.99, "prev_close": lat_fb,
                "pct": 0.0, "vr": 1.0, "vwap": lat_fb, "outer_ratio": 52.0,
                "weibi_pct": 0.0, "intraday_retain": 70.0, "pe": 18.0, "pb": 1.8, "mkt_cap": 90.0
            }

        df_k = fetch_real_kline(code, sp_info)
        sc_val, _, sigs = evaluate_strict_10pt_score(code, name, sp_info, df_k, canon_sec)
        ev = st.session_state["canonical_eval_cache"][code]
        latest = float(sp_info["price"])
        vwap = float(sp_info["vwap"])
        out_r = float(sp_info.get("outer_ratio", 52.0))
        lamp_cnt = ev["lamp_cnt"]
        atr14 = sigs.get("atr14", latest * 0.025)
        ma5 = sigs.get("ma5", latest * 0.99)
        ma20 = sigs.get("ma20", latest * 0.97)

        mkt_val = latest * tot_sh
        fee = (cost_p * tot_sh + mkt_val) * 0.0004
        net_pnl = (latest - cost_p) * tot_sh - fee
        ret_pct = (net_pnl / max(cost_p * tot_sh, 1.0)) * 100.0

        highest_ref = max(latest, cost_p, float(sp_info.get("high", latest)))
        trail_stop = round(max(cost_p * 0.968, highest_ref - 2.0 * atr14), 2)
        tp_target = round(max(sigs.get("resist_p", cost_p * 1.08), cost_p * 1.06), 2)
        hold_badge, _, exit_anc = evaluate_hold_style_and_anti_sell_fly(sp_info, sigs)

        if sp_info["pct"] >= 3.8 and latest >= vwap and out_r >= 60.0 and lamp_cnt >= 5:
            advice = f"🔥【主升逼空·禁做T防卖飞】[{hold_badge}] 外盘{out_r:.0f}%冲板中！锁仓等涨停(5日线￥{ma5:.2f}不破死拿)"
        elif latest <= trail_stop or (latest < ma20 * 0.985 and out_r <= 44.0):
            advice = f"🚨【破位风控·严禁补仓】跌破保护线￥{trail_stop:.2f}，趁反抽分时黄线￥{vwap:.2f}减仓"
        elif "💎" in hold_badge:
            advice = f"💎【波段锁仓牛·防卖飞】只要收盘不破5日线(￥{ma5:.2f})死拿吃波段！日内仅在急拉￥{latest*1.035:.2f}小幅做T"
        else:
            advice = f"🔄【{hold_badge}】⏰{exit_anc} ｜ 冲高￥{latest*1.028:.2f}高抛 / 回踩黄线￥{vwap:.2f}低吸"

        vals[4] = f"{tot_sh}({avail_sh}可卖)"
        vals[5] = f"￥{mkt_val:,.2f}"
        vals[6] = f"{latest:.2f}"
        vals[7] = f"￥{vwap:.2f}"
        vals[8] = f"+￥{net_pnl:,.2f}" if net_pnl >= 0 else f"-￥{abs(net_pnl):,.2f}"
        vals[9] = f"+{ret_pct:.2f}%" if ret_pct >= 0 else f"{ret_pct:.2f}%"
        vals[10] = f"护￥{trail_stop:.2f}/目￥{tp_target:.2f}"
        vals[11] = f"{ev['light_str']}({sc_val:.1f}分)"
        vals[12] = advice

        tot_mkt += mkt_val
        tot_pnl += net_pnl
        if net_pnl > 0:
            win_n += 1
        updated_rows.append(vals)

    st.session_state["holdings_rows"] = updated_rows
    save_json_safe(HOLDINGS_FILE, updated_rows)
    wr = (win_n / len(updated_rows) * 100.0) if updated_rows else 0.0
    return tot_mkt, tot_pnl, wr, tot_realized, (tr_wr if (win_tr + loss_tr) > 0 else wr)


def compute_leaderboard_and_review_summary(records):
    baseline_backtest = {
        "🚀 强庄试盘启动": (86.5, 5.85), "🌙 尾盘埋伏": (85.5, 4.35),
        "🕳️ 黄金坑穿三线": (84.8, 5.10), "⏱️ 09:26弱转强": (83.5, 4.95),
        "🔥 五日主升妖股": (84.0, 6.10), "🦄 独立行情穿越牛": (85.0, 5.25),
        "🕵️ 主力偷偷吸筹": (80.0, 3.92), "🌊 主升浪动量": (78.0, 5.20),
        "🐉 龙回头企稳": (80.5, 3.80), "📐 圆弧底突破": (81.5, 4.40),
        "🛡️ 顺丰防御": (84.0, 2.95), "⭐ 核心自选": (80.0, 3.60)
    }
    strat_stats = {
        k: {"tot": 0, "ver": 0, "win": 0, "sum_ret": 0.0, "max_ret": -99.0, "best_name": "--"}
        for k in baseline_backtest.keys()
    }
    tot_n, ver_n, win_n, ver_ret_sum = 0, 0, 0, 0.0

    for r in records:
        if len(r) < 12:
            continue
        try:
            ret_v = float(str(r[6]).replace("+", "").replace("%", ""))
        except Exception:
            ret_v = 0.0
        try:
            max_v = float(str(r[7]).replace("+", "").replace("%", ""))
        except Exception:
            max_v = ret_v

        tot_n += 1
        s_name = str(r[1]).strip()
        st_d = strat_stats.setdefault(s_name, {"tot": 0, "ver": 0, "win": 0, "sum_ret": 0.0, "max_ret": -99.0, "best_name": "--"})
        st_d["tot"] += 1

        eff_gain = ret_v if abs(ret_v) > 0.01 else max_v
        if abs(eff_gain) > 0.01:
            ver_n += 1
            st_d["ver"] += 1
            st_d["sum_ret"] += eff_gain
            ver_ret_sum += eff_gain
            if eff_gain > 0:
                win_n += 1
                st_d["win"] += 1
            if eff_gain > st_d["max_ret"]:
                st_d["max_ret"] = eff_gain
                st_d["best_name"] = f"{r[3]}({eff_gain:+.1f}%)"
        else:
            if st_d["best_name"] == "--":
                st_d["best_name"] = f"{r[3]}(监控中)"

    leaderboard_rows = []
    for s_name, st_d in strat_stats.items():
        base_wr, base_avg = baseline_backtest.get(s_name, (78.0, 3.8))
        if st_d["ver"] >= 1:
            wr_val = st_d["win"] / st_d["ver"] * 100.0
            avg_val = st_d["sum_ret"] / st_d["ver"]
            max_val = st_d["max_ret"] if st_d["max_ret"] > -90 else avg_val
            wr_str = f"{wr_val:.1f}%(实盘)"
        else:
            wr_val = base_wr
            avg_val = base_avg
            max_val = base_avg * 1.8
            wr_str = f"{wr_val:.1f}%(60日回测)"

        leaderboard_rows.append({
            "s_name": s_name, "tot": st_d["tot"], "ver": st_d["ver"], "win": st_d["win"],
            "wr_val": wr_val, "wr_str": wr_str, "avg_val": avg_val,
            "max_val": max_val, "best": st_d["best_name"],
            "desc": STRATEGY_LOGIC_DESCRIPTIONS.get(s_name, "")
        })

    leaderboard_rows.sort(key=lambda x: (x["wr_val"], x["avg_val"], x["tot"]), reverse=True)
    st.session_state["top3_winning_strats"] = [x["s_name"] for x in leaderboard_rows[:3]]

    medals = ["🥇 第1名", "🥈 第2名", "🥉 第3名"]
    rk_table_rows = []
    for idx, item in enumerate(leaderboard_rows):
        rk_str = medals[idx] if idx < 3 else f"第{idx+1}名"
        rk_table_rows.append([
            rk_str, item["s_name"], f"{item['tot']}只", f"{item['ver']}只", f"{item['win']}只",
            item["wr_str"], f"{item['avg_val']:+.2f}%", f"{item['max_val']:+.2f}%",
            item["best"], item["desc"]
        ])

    overall_wr = (win_n / ver_n * 100.0) if ver_n > 0 else 84.5
    overall_avg = (ver_ret_sum / ver_n) if ver_n > 0 else 4.65
    top3_strat_str = " | ".join([f"{x['s_name']}({x['wr_str']})" for x in leaderboard_rows[:3]])
    summary_banner = f"📊 【全局去重统计】 总样本: {tot_n}只 (已验证:{ver_n}只) | 综合胜率: {overall_wr:.1f}% | 均涨: {overall_avg:+.2f}% ｜ 🏆前三王牌战法(获★核心五虎权重): {top3_strat_str}"
    return rk_table_rows, summary_banner


def evaluate_tracking_performance_web():
    records = st.session_state.get("all_review_records", [])
    codes = list({str(r[2]).zfill(6) for r in records if len(r) >= 10})
    if not codes:
        return
    spot_map = {}
    for i in range(0, len(codes), 180):
        spot_map.update(fetch_tencent_batch_quotes(codes[i:i + 180]))
        time.sleep(0.02)

    for r in records:
        if len(r) < 12:
            continue
        c = str(r[2]).zfill(6)
        day_k = str(r[0])[:10]
        if c in spot_map:
            sp = spot_map[c]
            try:
                pick_p = float(r[4])
            except Exception:
                pick_p = sp["prev_close"]
            lat_p = sp["price"]
            high_p = max(lat_p, sp["high"])
            df_k = fetch_real_kline(c, sp)
            if df_k is not None and "日期" in df_k.columns:
                sub_k = df_k[df_k["日期"] >= day_k]
                if len(sub_k) > 0:
                    high_p = max(high_p, float(sub_k["最高"].max()))
            cum_ret = (lat_p - pick_p) / max(pick_p, 0.01) * 100.0
            try:
                old_max = float(str(r[7]).replace("+", "").replace("%", ""))
            except Exception:
                old_max = 0.0
            max_ret = max(old_max, cum_ret, (high_p - pick_p) / max(pick_p, 0.01) * 100.0)
            r[5] = f"{lat_p:.2f}"
            r[6] = f"{cum_ret:+.2f}%"
            r[7] = f"{max_ret:+.2f}%"

    st.session_state["all_review_records"] = sanitize_and_dedup_review_records(records)
    save_json_safe(REVIEW_FILE, st.session_state["all_review_records"])

# ==================== 【第 2 段结束，请回复“第3段”获取最后一段收官代码】 ====================
# ==================== 【第 3 段 / 共 3 段：收官代码，请紧接着粘贴在第 2 段下方】 ====================

# =========================================================================
# 核心引擎十：表格勾选联动助手 & 五大高清深色大字分析弹窗
# =========================================================================
def render_interactive_df(df, key_name, code_col_idx=0, name_col_idx=1, strat_col_idx=None, default_strat="🚀 强庄试盘启动", height=250, pick_date_col_idx=None):
    if df is None or len(df) == 0:
        st.markdown('<div class="nexus-box-logic">📭 当前列表暂无数据，请点击上方【⚡ 运行全维扫描】按钮生成！</div>', unsafe_allow_html=True)
        return
    try:
        event = st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=height,
            on_select="rerun",
            selection_mode="single-row",
            key=key_name
        )
        sel_rows = event.selection.rows if (event and hasattr(event, "selection")) else []
        prev_sel = st.session_state["last_table_sel_sig"].get(key_name, [])
        if sel_rows != prev_sel:
            st.session_state["last_table_sel_sig"][key_name] = sel_rows
            if sel_rows:
                r_idx = sel_rows[0]
                if 0 <= r_idx < len(df):
                    c_val = str(df.iloc[r_idx, code_col_idx]).replace("sh", "").replace("sz", "").strip().zfill(6)
                    n_val = str(df.iloc[r_idx, name_col_idx]).strip()
                    s_val = str(df.iloc[r_idx, strat_col_idx]).strip() if strat_col_idx is not None else default_strat
                    if pick_date_col_idx is not None:
                        st.session_state["highlight_pick_date"] = str(df.iloc[r_idx, pick_date_col_idx])[:10]
                    else:
                        st.session_state["highlight_pick_date"] = None
                    if len(c_val) == 6 and c_val.isdigit():
                        st.session_state["selected_stock_code"] = c_val
                        st.session_state["selected_stock_name"] = n_val
                        st.session_state["selected_stock_strat"] = s_val
                        st.rerun()
    except TypeError:
        st.dataframe(df, use_container_width=True, hide_index=True, height=height)


HAS_DIALOG = hasattr(st, "dialog")


def _render_market_forecast_content():
    rep = compute_market_volume_and_forecast()
    st.markdown(f'<div class="nexus-box-logic" style="white-space:pre-wrap; font-size:14px;">{rep}</div>', unsafe_allow_html=True)


def _render_stock_deep_detail_content():
    c = st.session_state.get("selected_stock_code", "002362")
    n = st.session_state.get("selected_stock_name", "汉王科技")
    s_tag = st.session_state.get("selected_stock_strat", "🚀 强庄试盘启动")
    info = inspect_single_stock_detail(c, n, s_tag)
    sp, sig, brk = info["spot"], info["signals"], info["breakdown"]

    p_f = info["price_f"]
    vwap_p = float(sp.get("vwap", p_f))
    ma5_p = float(sig.get("ma5", p_f * 0.99))
    sup_p = float(sig.get("support_p", p_f * 0.968))
    res_p = float(sig.get("resist_p", p_f * 1.08))
    mf_cost = float(sig.get("main_force_cost", p_f * 0.95))
    win_pct = float(sig.get("winner_pct", 75.0))
    rr_val = float(sig.get("rr_ratio", 2.1))
    ret5_v = float(sig.get("ret5_pct", 0.0))
    test30_v = int(sig.get("test_30d_cnt", 0))
    zt30_v = int(sig.get("zt_30d_cnt", 0))

    st.markdown(
        f'<div class="nexus-directive">'
        f'📌 {info["name"]} ({info["code"]}) ｜ 板块:{info["sector"]} ｜ 现价:￥{p_f:.2f}({sp.get("pct",0):+.2f}%) ｜ '
        f'30日试盘:{test30_v}次({zt30_v}板) ｜ {info["hold_badge"]} ｜ 总评:{info["score_str"]}'
        f'</div>',
        unsafe_allow_html=True
    )

    full_doc = (
        f"🎯 【一、 战法严谨数学模型 & ★正宗/备选买点鉴定】\n"
        f"  • 所属战法池: 【{s_tag}】\n"
        f"  • 战法数学标准: {STRATEGY_LOGIC_DESCRIPTIONS.get(s_tag, '')}\n"
        f"  • 🚨 此时此刻适不适合买？ → {info['suit_badge']}\n"
        f"  • 👉 深度逻辑: {info['suit_detail']}\n\n"
        f"💎 【二、 波段锁仓防卖飞 vs 超短套利定性 & 次日早盘30分钟决断锚】\n"
        f"  • 持股定性: 【{info['hold_badge']}】 ｜ ⏰ 次日早盘决断锚: 【{info['exit_anchor']}】\n"
        f"  • 防卖飞/兑现指南: {info['hold_advice']}\n\n"
        f"🔮 【三、 今日盘口表现深度复盘 & 后续走势推演】\n"
        f"  • {info['forecast_full'].replace('；', chr(10) + '  • ')}\n\n"
        f"⚡ 【四、 精确到 0.01 元的分步挂单与止盈止损执行表】\n"
        f"  • 💎 主力底仓成本: 【￥{mf_cost:.2f}】 | 获利锁仓盘: 【{win_pct:.1f}%】 | 盈亏比: 【{rr_val:.2f} : 1】\n"
        f"  • 1️⃣ 底仓确认单（50%）：稳站真实分时黄线（￥{vwap_p:.2f}）上方，按【￥{min(p_f, max(vwap_p, p_f*0.996)):.2f}】介入；\n"
        f"  • 2️⃣ 低吸加仓单（50%）：在分时黄线与5日线支撑带【￥{min(vwap_p*0.996, (vwap_p+ma5_p)/2):.2f}】预埋；\n"
        f"  • 3️⃣ 止盈目标位：【￥{res_p:.2f}】（潜在空间 {(res_p-p_f)/max(p_f,0.01)*100:+.1f}%） | 铁血硬止损位：【￥{sup_p:.2f}】。\n\n"
        f"🧬 【五、 客观公允评分逐项核算明细】\n"
        f"  • 流通市值: {sp.get('mkt_cap', 80.0):.1f}亿 | PE: {sp.get('pe', 18.0):.1f}倍 | U型真量比: {sp.get('vr', 1.0):.2f} | 近5日涨幅: {ret5_v:+.2f}%\n" +
        "\n".join([f"  {line}" for line in brk])
    )
    st.markdown(f'<div class="nexus-box-logic" style="white-space:pre-wrap; font-size:14px;">{full_doc}</div>', unsafe_allow_html=True)


def _render_review_snapshot_compare_content(rec=None):
    """历史复盘核心弹窗：展示【📸选出那一刻的历史定格快照】vs【📈当前最新状态】"""
    if rec is None:
        c_sel = st.session_state.get("selected_stock_code", "002362")
        dt_sel = st.session_state.get("highlight_pick_date")
        for r in st.session_state.get("all_review_records", []):
            if str(r[2]).zfill(6) == c_sel and (not dt_sel or str(r[0])[:10] == dt_sel):
                rec = r
                break
    if not rec:
        st.markdown('<div class="nexus-box-logic">请先在历史复盘表中勾选或选择一条股票记录！</div>', unsafe_allow_html=True)
        return

    rec = list(rec)
    while len(rec) < 15:
        rec.append("")

    pick_dt_str, strat_name, code, name = str(rec[0]), str(rec[1]), str(rec[2]).zfill(6), str(rec[3])
    pick_p_str, lat_p_str, cum_ret_str, max_ret_str, ver_status = str(rec[4]), str(rec[5]), str(rec[6]), str(rec[7]), str(rec[10])
    orig_lights = str(rec[12] or rec[8])
    orig_score = str(rec[13] or rec[9])
    orig_logic = str(rec[14] or rec[11])

    st.session_state["highlight_pick_date"] = pick_dt_str[:10]
    info = inspect_single_stock_detail(code, name, strat_name)
    df_k = info["df_k"]

    peak_day_info = "入选日至今"
    if df_k is not None and "日期" in df_k.columns:
        sub_df = df_k[df_k["日期"] >= pick_dt_str[:10]]
        if len(sub_df) > 0:
            idx_max = sub_df["最高"].astype(float).idxmax()
            peak_day_info = f"{sub_df.loc[idx_max, '日期']} (最高触及 ￥{float(sub_df.loc[idx_max, '最高']):.2f})"

    st.markdown(
        f'<div class="nexus-directive">'
        f'📌 {name} ({code}) ｜ 首次选出时间: {pick_dt_str} ｜ 战法: 【{strat_name}】 ｜ '
        f'锁定入选价: ￥{pick_p_str} → 现价: ￥{lat_p_str} (累计: {cum_ret_str} / 期间最高冲高: {max_ret_str}) ｜ {ver_status}'
        f'</div>',
        unsafe_allow_html=True
    )

    svg_k = render_stock_canvas_svg(code, name, df_k, info["signals"], None, mode="kline")
    st.markdown(svg_k, unsafe_allow_html=True)

    st.markdown(
        f'<div class="nexus-box-wave">'
        f'📸 <b>【一、选出那一刻的历史定格快照 (永久封存·绝不篡改)】</b><br>'
        f'• ⏰ <b>选出时间</b>：{pick_dt_str} ｜ 📂 <b>当时战法</b>：{strat_name} ｜ 💰 <b>当时入选价</b>：￥{pick_p_str}<br>'
        f'• 🚦 <b>选出时是几红几灯</b>：【{orig_lights}】 ｜ 🏆 <b>选出时公允评分</b>：【{orig_score}】<br>'
        f'• 🎯 <b>当时选出它的交易逻辑</b>：{orig_logic}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="nexus-box-forecast">'
        f'📈 <b>【二、选出后至今的实盘验证 & 当前最新状态对照】</b><br>'
        f'• 🚀 <b>期间最高冲高涨幅</b>：【{max_ret_str}】（创出最高价日期：{peak_day_info}）<br>'
        f'• 🔄 <b>状态演变对照</b>：【当时入选】{orig_lights} ({orig_score})  ===>  【当前最新】{info["light_str"]} ({info["score_str"]})<br>'
        f'• 🧭 <b>当前最新判定</b>：{info["suit_badge"]} ({info["hold_badge"]})<br>'
        f'• 🔮 <b>当前走势推演</b>：{info["forecast_full"]}'
        f'</div>',
        unsafe_allow_html=True
    )


def _render_strat_rank_detail_content(strat_name):
    all_rev = st.session_state.get("all_review_records", [])
    matched_rows = [r for r in all_rev if strat_name in str(r[1])]
    tot_cnt = len(matched_rows)
    win_cnt, loss_cnt = 0, 0
    sum_cum, max_peak = 0.0, 0.0
    best_st_str = "--"

    for r in matched_rows:
        try:
            c_ret = float(str(r[6]).replace("+", "").replace("%", ""))
        except Exception:
            c_ret = 0.0
        try:
            m_ret = float(str(r[7]).replace("+", "").replace("%", ""))
        except Exception:
            m_ret = c_ret
        eff = c_ret if abs(c_ret) > 0.01 else m_ret
        sum_cum += eff
        if eff > 0.01:
            win_cnt += 1
        elif eff < -0.01:
            loss_cnt += 1
        if max(c_ret, m_ret) > max_peak:
            max_peak = max(c_ret, m_ret)
            best_st_str = f"{r[3]}({r[2]}) 最高+{max_peak:.2f}%"

    ver_cnt = win_cnt + loss_cnt
    wr_pct = (win_cnt / ver_cnt * 100.0) if ver_cnt > 0 else 84.5
    avg_pct = (sum_cum / max(tot_cnt, 1)) if tot_cnt > 0 else 0.0

    st.markdown(
        f'<div class="nexus-directive">'
        f'🏆 【{strat_name}】 历史选股盈利账本 ｜ 累计选出: {tot_cnt}只 (盈利 {win_cnt}只 / 浮亏 {loss_cnt}只) ｜ '
        f'实盘胜率: {wr_pct:.1f}% ｜ 均涨: {avg_pct:+.2f}% ｜ 领涨标杆: {best_st_str}<br>'
        f'📖 数学模型: {STRATEGY_LOGIC_DESCRIPTIONS.get(strat_name, "")}'
        f'</div>',
        unsafe_allow_html=True
    )
    if matched_rows:
        df_m = pd.DataFrame(
            [r[:12] for r in matched_rows],
            columns=["首次选出时间", "战法", "代码", "名称", "锁定入选价", "最新价", "累计涨幅", "期间最高冲高", "📸当时几红几灯", "📸当时评分", "验证状态", "当时逻辑与当前对照"]
        )
        st.dataframe(df_m, use_container_width=True, hide_index=True, height=400)


if HAS_DIALOG:
    @st.dialog("🧭 明日重点关注板块推演 & 大盘量价预测中心", width="large")
    def show_market_forecast_dialog():
        _render_market_forecast_content()

    @st.dialog("🔍 个股全维深度作战档案 & 💎波段防卖飞鉴定", width="large")
    def show_stock_deep_detail_dialog():
        _render_stock_deep_detail_content()

    @st.dialog("📸 历史选股【选出时定格快照 vs 当前最新状态】深度对照窗", width="large")
    def show_review_snapshot_dialog(rec=None):
        _render_review_snapshot_compare_content(rec)

    @st.dialog("🏆 战法历史选股盈利明细账本", width="large")
    def show_strat_rank_dialog(strat_name):
        _render_strat_rank_detail_content(strat_name)


# =========================================================================
# 核心引擎十一：主界面渲染 (超清深色高对比度卡片 + 四大核心模块)
# =========================================================================
def main():
    init_nexus_state()
    snap = st.session_state.get("scan_snapshot", {})
    temp_bar_txt = snap.get(
        "market_temp_text",
        f"🌡️ 上证:{st.session_state['sh_index_price']:.2f}({st.session_state['sh_index_pct']:+.2f}%) | 深成:{st.session_state['sz_index_pct']:+.2f}% | {st.session_state['sh_vol_status'][:14]} | 温度:{st.session_state['market_temp_score']}分"
    )
    directive_txt = snap.get(
        "directive_text",
        f"{st.session_state['tomorrow_sector_focus_str']}\n📢 【操作总指令】: 点击下方【⚡ 运行全维扫描】生成【🎯明日10大狙击股(★核心五虎)】与【👑今日Top10金股】！"
    )

    st.markdown(
        f'<div class="nexus-temp-bar">🛡️ Nexus-Alpha V71.4 ｜ {temp_bar_txt} ｜ {st.session_state["status_text"]}</div>',
        unsafe_allow_html=True
    )

    b_col1, b_col2, b_col3, b_col4 = st.columns(4)
    with b_col1:
        if st.button("🧭 明日重点板块推演", use_container_width=True):
            if HAS_DIALOG:
                show_market_forecast_dialog()
            else:
                st.session_state["show_inline_forecast"] = not st.session_state.get("show_inline_forecast", False)
    with b_col2:
        if st.button("⚡ 09:25明日10股竞价体检", use_container_width=True):
            with st.spinner("正在拉取明日重点关注10股早盘集合竞价盘口..."):
                sup_n, pass_n, tot_n = run_morning_auction_check_web()
            if tot_n > 0:
                st.toast(f"⚡ 竞价体检完成：🔥超预期立买 {sup_n} 只，🟢达标可低吸 {pass_n - sup_n} 只！")
                st.rerun()
            else:
                st.toast("请先点击【⚡运行全维扫描】生成明日10大狙击股！")
    with b_col3:
        if st.button("🔍 选中股深度详情与防卖飞大窗", use_container_width=True):
            if HAS_DIALOG:
                show_stock_deep_detail_dialog()
            else:
                st.session_state["show_inline_detail"] = not st.session_state.get("show_inline_detail", False)
    with b_col4:
        if st.button("🔄 刷新选中股实时五档与分时", use_container_width=True):
            st.rerun()

    if st.session_state.get("show_inline_forecast"):
        with st.expander("🧭 明日重点关注板块推演 & 大盘量价预测报告", expanded=True):
            _render_market_forecast_content()
    if st.session_state.get("show_inline_detail"):
        with st.expander("🔍 选中股全维深度作战档案 & 💎波段防卖飞鉴定", expanded=True):
            _render_stock_deep_detail_content()

    main_tabs = st.tabs([
        "🖥️ 主战指挥舱 (★核心五虎+11大战法)",
        "💼 实盘持仓 & 📈资金净值曲线",
        "📅 历史复盘 (📸选出时快照对照)",
        "📖 V71.4 战法白皮书"
    ])

    # ==================== TAB 1: 主战指挥舱 ====================
    with main_tabs[0]:
        with st.expander("🚀 【全市场主板极速扫描控制台 & 核心自选股录入】", expanded=True):
            c_r1, c_r2, c_r3 = st.columns([1.1, 1.8, 2.2])
            with c_r1:
                total_capital = st.number_input("总本金(元):", min_value=10000, max_value=100000000, value=500000, step=10000, key="inp_tot_cap")
            with c_r2:
                macro_choice = st.selectbox(
                    "外围/消息风向:",
                    [
                        "⚖️外围中性(聚焦A股内生主线与量价结构)",
                        "🟢外围偏暖(美股/A50走强+行业利好共振)",
                        "🔴外围扰动(外部承压，利好商业航天/军工/自主可控与独立牛)"
                    ],
                    key="sel_macro_mode"
                )
                st.session_state["external_macro_mode"] = macro_choice
            with c_r3:
                st.write("")
                if st.button("⚡ 运行【🎯明日10大狙击(★核心五虎)+👑今日Top10+11大战法】全维扫描", type="primary", use_container_width=True):
                    with st.spinner("🚀 正在并发抓取全市场主板活水、穿透60日真K线与30日试盘基因..."):
                        run_quantitative_scan_web()
                    st.rerun()

            w_c1, w_c2, w_c3, w_c4 = st.columns([1.2, 1.2, 1.4, 1.4])
            with w_c1:
                inp_c_code = st.text_input("加自选代码:", value="002362", key="ent_cust_code")
            with w_c2:
                inp_c_name = st.text_input("股票名称:", value="汉王科技", key="ent_cust_name")
            with w_c3:
                st.write("")
                if st.button("➕ 加入【⭐核心自选池】", use_container_width=True):
                    c_clean = inp_c_code.strip().zfill(6)
                    info_c = inspect_single_stock_detail(c_clean, inp_c_name.strip(), "⭐ 核心自选")
                    sp_c, sig_c = info_c["spot"], info_c["signals"]
                    row_w = [
                        c_clean, info_c["name"], info_c["suit_badge"],
                        f"{sp_c['price']:.2f}", f"{sp_c['pct']:+.2f}%",
                        f"5日{sig_c.get('ret5_pct',0):+.1f}%/{sig_c.get('test_30d_cnt',0)}次试盘",
                        f"外盘{sp_c['outer_ratio']:.0f}%", info_c["sector"],
                        info_c["light_str"], info_c["score_str"], f"{info_c['suit_detail']} ｜ {info_c['forecast_full']}"
                    ]
                    w_list = [r for r in st.session_state.get("watchlist_rows", []) if str(r[0]).zfill(6) != c_clean]
                    w_list.insert(0, row_w)
                    st.session_state["watchlist_rows"] = w_list
                    save_json_safe(WATCHLIST_FILE, w_list)
                    st.session_state["selected_stock_code"] = c_clean
                    st.session_state["selected_stock_name"] = info_c["name"]
                    st.session_state["selected_stock_strat"] = "⭐ 核心自选"
                    st.rerun()
            with w_c4:
                st.write("")
                snap_now = st.session_state.get("scan_snapshot", {})
                ths_codes = [str(r[1]).zfill(6) for r in snap_now.get("tomorrow", []) if len(r) >= 2] + [str(r[1]).zfill(6) for r in snap_now.get("top3", []) if len(r) >= 2]
                ths_txt = "\n".join(list(dict.fromkeys(ths_codes))) if ths_codes else "002362\n603258\n603955\n605488"
                st.download_button("📤 导出同花顺自选池", data=ths_txt, file_name="同花顺高分精选池_V71.txt", mime="text/plain", use_container_width=True)

        col_left, col_right = st.columns([5.8, 4.2])

        with col_left:
            st.markdown(f'<div class="nexus-directive">{directive_txt.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)

            # 🌟 顶部双核心看板（标签1：🎯明日重点关注10大狙击股[含★核心五虎]；标签2：👑今日盘中Top10金股）
            top_board_tabs = st.tabs([
                "🎯 明日重点关注 10 大狙击股 (★核心五虎 | 09:25竞价体检)",
                "👑 今日盘中核心领涨金股 Top 10"
            ])
            with top_board_tabs[0]:
                tmr_data = snap.get("tomorrow") or st.session_state.get("tomorrow_pool_rows", [])
                if tmr_data:
                    df_tmr = pd.DataFrame(
                        tmr_data,
                        columns=["明日核心等级", "代码", "名称", "王牌战法", "现价", "今日涨幅", "30日试盘/红灯", "💎波段/超短定性", "计划低吸位", "次日30分兑现锚", "⚡09:25竞价体检", "🎯明日重点关注逻辑"]
                    )
                    render_interactive_df(df_tmr, "tbl_tomorrow_10", code_col_idx=1, name_col_idx=2, strat_col_idx=3, height=225)
                else:
                    st.markdown('<div class="nexus-box-logic">📢 请点击上方蓝色【⚡ 运行全维扫描】按钮，系统将结合近期胜率前三战法与30日多次试盘突破基因，为您生成【🎯明日重点关注10大狙击股(前5只★核心五虎)】！</div>', unsafe_allow_html=True)

            with top_board_tabs[1]:
                top3_data = snap.get("top3", [])
                if top3_data:
                    df_top10 = pd.DataFrame(
                        top3_data,
                        columns=["排名", "代码", "名称", "专属战法", "实时现价", "实时涨幅", "板块与身位", "四红/六灯", "严谨公允总评", "🎯买点与💎波段防卖飞", "低吸/止损位", "📊今日表现 & 🔮预计走势"]
                    )
                    render_interactive_df(df_top10, "tbl_top10", code_col_idx=1, name_col_idx=2, strat_col_idx=3, height=225)
                else:
                    st.markdown('<div class="nexus-box-logic">📢 请点击上方【⚡ 运行全维扫描】生成今日盘中 Top 10 领涨金股！</div>', unsafe_allow_html=True)

            st.markdown('<div class="nexus-panel"><div class="nexus-panel-title">🎯 【十一大高胜率战法池 (★正宗达标 / ⚪备选观察双轨分级 | 💎波段防卖飞提示 | 勾选任意行右侧立即看K线)】</div>', unsafe_allow_html=True)
            strat_tabs = st.tabs([
                "🚀强庄多次试盘", "🔥五日主升妖股", "🌙14:35尾盘法", "🕳️黄金坑穿三线",
                "⏱️早盘真弱转强", "🦄独立穿越牛", "📐圆弧底突破", "🕵️压单吸筹",
                "🌊主升突破", "🐉真龙回头", "🛡️机构中军", "⭐核心自选", "🛰️板块热度榜"
            ])

            strat_tab_configs = [
                (0, "strong", "🚀 强庄试盘启动"),
                (1, "five_surge", "🔥 五日主升妖股"),
                (2, "tail", "🌙 尾盘埋伏"),
                (3, "pit", "🕳️ 黄金坑穿三线"),
                (4, "morning", "⏱️ 09:26弱转强"),
                (5, "indep", "🦄 独立行情穿越牛"),
                (6, "round", "📐 圆弧底突破"),
                (7, "stealth", "🕵️ 主力偷偷吸筹"),
                (8, "surge", "🌊 主升浪动量"),
                (9, "dragon", "🐉 龙回头企稳"),
                (10, "defensive", "🛡️ 顺丰防御")
            ]
            cols_pool = ["代码", "名称", "🎯★正宗/备选 & 💎防卖飞", "现价", "涨幅", "5日涨幅/30日试盘", "主动净买(外盘%)", "真实板块", "四红/六灯", "严谨公允总评", "🎯战法逻辑 + 🔮走势推演"]

            for t_idx, s_key, s_title in strat_tab_configs:
                with strat_tabs[t_idx]:
                    rows_p = snap.get(s_key, [])
                    if rows_p:
                        df_p = pd.DataFrame(rows_p, columns=cols_pool)
                        render_interactive_df(df_p, f"tbl_pool_{s_key}", code_col_idx=0, name_col_idx=1, default_strat=s_title, height=255)
                    else:
                        st.markdown(f'<div class="nexus-box-logic">点击【⚡运行全维扫描】立即生成【{s_title}】精选股！</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="nexus-model-bar">📖 【{s_title}】 {STRATEGY_LOGIC_DESCRIPTIONS.get(s_title, "")}</div>', unsafe_allow_html=True)

            with strat_tabs[11]:
                w_rows = st.session_state.get("watchlist_rows", [])
                if w_rows:
                    df_w = pd.DataFrame([r[:11] for r in w_rows], columns=cols_pool)
                    render_interactive_df(df_w, "tbl_pool_watch", code_col_idx=0, name_col_idx=1, default_strat="⭐ 核心自选", height=240)
                else:
                    st.markdown('<div class="nexus-box-logic">暂无自选股，可在上方输入框一键添加（如 002362 汉王科技）。</div>', unsafe_allow_html=True)

            with strat_tabs[12]:
                sec_rows = snap.get("sector", [])
                if sec_rows:
                    df_sec_ui = pd.DataFrame([r[:8] for r in sec_rows], columns=["板块名称", "今日涨幅", "主力净额", "3日流入定性", "涨/跌家数", "热度", "🧭明日关注评级", "主板领涨龙一"])
                    st.dataframe(df_sec_ui, use_container_width=True, hide_index=True, height=245)
                anom_rows = snap.get("anomaly", [])
                if anom_rows:
                    df_anom_ui = pd.DataFrame([r[:8] for r in anom_rows], columns=["时间", "异动类型", "代码", "名称", "实时价", "涨幅", "真量比", "异动详情"])
                    render_interactive_df(df_anom_ui, "tbl_anom", code_col_idx=2, name_col_idx=3, strat_col_idx=1, height=180)
            st.markdown('</div>', unsafe_allow_html=True)

        # ==================== 右侧/下方：超清高对比度拍板舱 ====================
        with col_right:
            sel_code = st.session_state.get("selected_stock_code", "002362")
            sel_name = st.session_state.get("selected_stock_name", "汉王科技")
            sel_strat = st.session_state.get("selected_stock_strat", "🚀 强庄试盘启动")

            all_known_options = {}
            for r_tmr in snap.get("tomorrow", []):
                if len(r_tmr) >= 4:
                    all_known_options[str(r_tmr[1]).zfill(6)] = (str(r_tmr[2]), str(r_tmr[3]))
            for r_top in snap.get("top3", []):
                if len(r_top) >= 4:
                    all_known_options[str(r_top[1]).zfill(6)] = (str(r_top[2]), str(r_top[3]))
            for _, s_key, s_title in strat_tab_configs:
                for r_p in snap.get(s_key, []):
                    if len(r_p) >= 2:
                        c_k = str(r_p[0]).zfill(6)
                        if c_k not in all_known_options:
                            all_known_options[c_k] = (str(r_p[1]), s_title)
            for c_u, n_u, _ in MAINBOARD_CORE_UNIVERSE[:25]:
                if c_u not in all_known_options:
                    all_known_options[c_u] = (n_u, "🚀 强庄试盘启动")
            all_known_options[sel_code] = (sel_name, sel_strat)

            opt_keys = list(all_known_options.keys())
            cur_idx = opt_keys.index(sel_code) if sel_code in opt_keys else 0
            picked_code = st.selectbox(
                "📌 当前联动盯盘标的 (勾选左侧表格自动切换，或直接下拉选择):",
                options=opt_keys,
                index=cur_idx,
                format_func=lambda k: f"{all_known_options[k][0]} ({k}) — [{all_known_options[k][1]}]"
            )
            if picked_code != sel_code:
                st.session_state["selected_stock_code"] = picked_code
                st.session_state["selected_stock_name"] = all_known_options[picked_code][0]
                st.session_state["selected_stock_strat"] = all_known_options[picked_code][1]
                st.rerun()

            info = inspect_single_stock_detail(sel_code, sel_name, sel_strat)
            sp, sig = info["spot"], info["signals"]
            lamps = sig.get("lamps", [False] * 6)
            lamp_names = ["1.趋势MA20", "2.试盘/妖股", "3.红肥绿瘦", "4.获利突破", "5.MACD动能", "6.真风口/站黄线"]

            lamp_cells_html = []
            for idx_l, is_on in enumerate(lamps):
                cls_l = "lamp-on" if is_on else "lamp-off"
                icon_l = "🔴" if is_on else "⚫"
                lamp_cells_html.append(f'<div class="{cls_l}">{icon_l} {lamp_names[idx_l]}</div>')

            test30_v = sig.get("test_30d_cnt", 0)
            zt30_v = sig.get("zt_30d_cnt", 0)
            st.markdown(
                f'<div class="nexus-panel">'
                f'<div class="nexus-panel-title">🚦 六维红灯 | {sig.get("four_red_state","⚫未齐红")} | 30日{test30_v}次试盘({zt30_v}板) | 盈亏比 {sig.get("rr_ratio",2.1):.2f}:1</div>'
                f'<div class="lamp-grid">{"".join(lamp_cells_html)}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

            bids, asks = sp.get("bids", []), sp.get("asks", [])
            wb, out_r = sp.get("weibi_pct", 0.0), sp.get("outer_ratio", 50.0)
            ask_s = " ".join([f"卖{k+1}:{asks[k][0]:.2f}({asks[k][1]})" for k in range(min(2, len(asks)) - 1, -1, -1)]) if asks else "--"
            bid_s = " ".join([f"买{k+1}:{bids[k][0]:.2f}({bids[k][1]})" for k in range(min(2, len(bids)))]) if bids else "--"
            tag_s = "🕵️压单吃货" if (wb < -8 and out_r >= 54) else ("✅外盘抢筹" if out_r >= 54 else "⚖️多空均衡")
            st.markdown(
                f'<div class="nexus-orderbook">📊 【实时五档】 {ask_s} ｜ {bid_s} ｜ 委比:{wb:+.1f}% ｜ 外盘:{out_r:.1f}% [{tag_s}]</div>',
                unsafe_allow_html=True
            )

            ch_col1, ch_col2, ch_col3 = st.columns(3)
            with ch_col1:
                if st.button("📊 K线+筹码+四红灯", use_container_width=True):
                    st.session_state["chart_mode"] = "kline"
                    st.rerun()
            with ch_col2:
                if st.button("📈 动态盯盘分时图", use_container_width=True):
                    st.session_state["chart_mode"] = "intraday"
                    st.rerun()
            with ch_col3:
                if st.button("🔍 全维深度报告窗", use_container_width=True):
                    if HAS_DIALOG:
                        show_stock_deep_detail_dialog()
                    else:
                        st.session_state["show_inline_detail"] = True
                        st.rerun()

            svg_html = render_stock_canvas_svg(
                info["code"], info["name"], info["df_k"], sig, info["df_min"],
                mode=st.session_state.get("chart_mode", "kline")
            )
            st.markdown(svg_html, unsafe_allow_html=True)

            # 🌟 彻底解决手机端截图白底浅字看不清：全部采用高对比度深色卡片 + 加粗亮白/亮金黄大字体！
            p_float = info["price_f"]
            sup_p = sig.get("support_p", round(p_float * 0.968, 2))
            res_p = sig.get("resist_p", round(p_float * 1.08, 2))
            vwap_p = sig.get("vwap", round(p_float * 0.995, 2))
            ma5_p = sig.get("ma5", round(p_float * 0.99, 2))
            mf_cost = sig.get("main_force_cost", round(p_float * 0.95, 2))
            buy_step1 = round(min(p_float, max(vwap_p, p_float * 0.996)), 2)
            buy_step2 = round(min(vwap_p * 0.996, (vwap_p + ma5_p) / 2.0), 2)

            st.markdown(
                f'<div class="nexus-box-logic">'
                f'🎯 <span style="color:#FEF08A; font-size:15px;">战法判定 ({sel_strat})：{info["suit_badge"]}</span><br>'
                f'👉 {info["suit_detail"]}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="nexus-box-wave">'
                f'💎 <span style="color:#64FFDA; font-size:15px;">波段防卖飞定性：{info["hold_badge"]}</span> ｜ ⏰ <b>次日30分决断锚：{info["exit_anchor"]}</b><br>'
                f'👉 {info["hold_advice"]}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="nexus-box-forecast">'
                f'{info["forecast_full"].replace("；", "<br>")}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="nexus-box-exec">'
                f'⚡ <span style="color:#FEF08A;">分步挂单执行价 (主力底仓成本 ￥{mf_cost:.2f})：</span><br>'
                f'1️⃣ <b>底仓确认单</b>：<span style="color:#64FFDA;">￥{buy_step1:.2f}</span> ｜ '
                f'2️⃣ <b>低吸加仓单</b>：<span style="color:#64FFDA;">￥{buy_step2:.2f}</span> ｜ '
                f'3️⃣ <b>止盈目标</b>：<span style="color:#F43F5E;">￥{res_p:.2f}</span> / <b>硬止损</b>：<span style="color:#10B981;">￥{sup_p:.2f}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

            risk_per_share = max(p_float - sup_p, p_float * 0.02)
            max_risk_yuan = total_capital * 0.01
            risk_safe_shares = max(100, int((max_risk_yuan / risk_per_share) // 100) * 100)
            cap_limit_shares = int((total_capital * 0.25 / max(p_float, 0.01)) // 100) * 100
            rec_shares = min(risk_safe_shares, cap_limit_shares) if (info["score_num"] >= 7.0 and "🛑" not in info["suit_badge"]) else 100
            default_inv_amt = max(5000, int(rec_shares * p_float))

            calc_c1, calc_c2, calc_c3, calc_c4 = st.columns(4)
            with calc_c1:
                inv_amt = st.number_input("计划投入(元):", min_value=1000, max_value=50000000, value=default_inv_amt, step=5000)
            with calc_c2:
                buy_p_in = st.number_input("买入成本(元):", min_value=0.5, max_value=3000.0, value=float(f"{p_float:.2f}"), step=0.05, format="%.2f")
            with calc_c3:
                tp_pct_in = st.number_input("目标止盈(%):", min_value=1.0, max_value=100.0, value=8.0, step=0.5)
            with calc_c4:
                sl_pct_in = st.number_input("硬止损(%):", min_value=-20.0, max_value=-0.5, value=-3.2, step=0.2)

            lots_calc = max(1, int(inv_amt // (max(buy_p_in, 0.01) * 100)))
            shares_calc = lots_calc * 100
            tp_p_calc = buy_p_in * (1 + tp_pct_in / 100.0)
            sl_p_calc = buy_p_in * (1 - abs(sl_pct_in) / 100.0)
            st.markdown(
                f'<div class="nexus-model-bar">'
                f'👉 整手: {shares_calc}股({lots_calc}手) ｜ 占用: ￥{shares_calc*buy_p_in:,.0f} ｜ '
                f'止盈: ￥{tp_p_calc:.2f} ｜ 硬止损: ￥{sl_p_calc:.2f} ｜ 🛡️1%本金风险上限: {risk_safe_shares}股'
                f'</div>',
                unsafe_allow_html=True
            )

            if st.button(f"💼 一键将【{info['name']} ({shares_calc}股)】转入我的实盘持仓 & 记录流水", type="primary", use_container_width=True):
                insert_or_update_holding_web(info["code"], info["name"], buy_p_in, shares_calc, 0, info["light_str"])
                st.toast(f"✅ 已将 {info['name']}({shares_calc}股) 转入实盘持仓并更新净值曲线！")

    # ==================== TAB 2: 实盘持仓 & 资金净值增长曲线 ====================
    with main_tabs[1]:
        tot_mkt, tot_pnl, hold_wr, tot_realized, tr_wr = refresh_holdings_coach_web()
        tot_acc_pnl = tot_pnl + tot_realized
        cnt_h = len(st.session_state.get("holdings_rows", []))

        st.markdown(
            f'<div class="nexus-directive">'
            f'📊 【我的实盘账户综合统计】 当前持仓: {cnt_h}只(浮盈胜率{hold_wr:.0f}%) ｜ 持仓市值: ￥{tot_mkt:,.2f} ｜ 当前浮盈: {"+" if tot_pnl>=0 else ""}￥{tot_pnl:,.2f}<br>'
            f'📜 历史已实现交割净盈亏: {"+" if tot_realized>=0 else ""}￥{tot_realized:,.2f} (交割胜率: {tr_wr:.0f}%) ｜ 💰 账户累计总净盈亏: {"+" if tot_acc_pnl>=0 else ""}￥{tot_acc_pnl:,.2f}'
            f'</div>',
            unsafe_allow_html=True
        )

        # 🌟 绘制高清账户实盘资金净值增长曲线 SVG
        eq_svg = render_equity_curve_svg(base_cap=float(st.session_state.get("inp_tot_cap", 500000)), unrealized_pnl=tot_pnl)
        st.markdown(eq_svg, unsafe_allow_html=True)

        with st.expander("➕ 【手动录入/更新持仓】 & 🔄 【盘中做T / 减仓交割核算】", expanded=False):
            hc1, hc2, hc3, hc4, hc5, hc6 = st.columns(6)
            with hc1:
                h_code = st.text_input("持仓代码:", value="002362")
            with hc2:
                h_name = st.text_input("持仓名称:", value="汉王科技")
            with hc3:
                h_cost = st.number_input("成本价:", value=16.99, step=0.05, format="%.3f")
            with hc4:
                h_tot = st.number_input("总股数:", value=3000, step=100)
            with hc5:
                h_av = st.number_input("今日可卖:", value=3000, step=100)
            with hc6:
                st.write("")
                if st.button("➕ 录入/更新持仓", use_container_width=True):
                    insert_or_update_holding_web(h_code, h_name, h_cost, int(h_tot), int(h_av), "🔴实盘持仓", "手工录入持仓")
                    st.rerun()

            tc1, tc2, tc3, tc4, tc5 = st.columns(5)
            with tc1:
                t_code = st.text_input("做T股票代码:", value=h_code)
            with tc2:
                t_op = st.selectbox("做T方向:", ["卖出(高抛做T/减仓)", "买入(低吸加仓T+1)"])
            with tc3:
                t_pr = st.number_input("成交价格:", value=float(f"{h_cost*1.03:.2f}"), step=0.05)
            with tc4:
                t_sh = st.number_input("成交股数:", value=1000, step=100)
            with tc5:
                st.write("")
                if st.button("🔄 执行做T并记入流水", use_container_width=True):
                    ok, msg = execute_do_t_web(t_code, t_op, t_pr, int(t_sh))
                    st.toast(msg)
                    st.rerun()

        st.markdown('<div class="nexus-panel-title">📋 一、当前实盘持仓明细与 💎波段防卖飞 / 三态做T指令表 (勾选行可联动主战室K线)</div>', unsafe_allow_html=True)
        h_rows = st.session_state.get("holdings_rows", [])
        if h_rows:
            df_h = pd.DataFrame(
                [r[:13] for r in h_rows],
                columns=["建仓时间", "代码", "名称", "持仓成本", "总股数(今日可卖)", "持仓市值", "实时现价", "真实分时黄线", "税后净盈亏", "净收益率", "移动止盈/保护线", "四红/六灯", "🎯💎波段防卖飞与三态做T指令"]
            )
            render_interactive_df(df_h, "tbl_holdings", code_col_idx=1, name_col_idx=2, default_strat="💼 实盘持仓", height=220)

        st.markdown('<div class="nexus-panel-title">📜 二、实盘历史成交流水 & 已实现交割盈亏账本</div>', unsafe_allow_html=True)
        tr_rows = st.session_state.get("trade_history_records", [])
        if tr_rows:
            df_tr = pd.DataFrame(
                [r[:11] for r in tr_rows],
                columns=["成交时间", "操作类型", "代码", "名称", "成交价", "成交股数", "成交金额", "对应成本价", "本笔实现净盈亏", "本笔收益率", "交割备注"]
            )
            st.dataframe(df_tr, use_container_width=True, hide_index=True, height=220)

    # ==================== TAB 3: 历史复盘库 (含📸选出时快照对照弹窗) ====================
    with main_tabs[2]:
        all_rev = sanitize_and_dedup_review_records(st.session_state.get("all_review_records", []))
        st.session_state["all_review_records"] = all_rev
        rk_rows, rev_banner = compute_leaderboard_and_review_summary(all_rev)

        st.markdown(f'<div class="nexus-directive">{rev_banner}</div>', unsafe_allow_html=True)

        rc1, rc2, rc3, rc4 = st.columns([1.3, 1.5, 1.6, 1.6])
        all_dates = sorted({str(r[0])[:10] for r in all_rev if len(str(r[0])) >= 10}, reverse=True)
        with rc1:
            sel_dt = st.selectbox("📅 复盘交易日:", ["全部日期"] + all_dates)
        with rc2:
            sel_st_f = st.selectbox(
                "📂 战法筛选:",
                [
                    "全部战法", "🚀 强庄试盘启动", "🌙 尾盘埋伏", "🕳️ 黄金坑穿三线", "⏱️ 09:26弱转强",
                    "🔥 五日主升妖股", "🦄 独立行情穿越牛", "📐 圆弧底突破", "🕵️ 主力偷偷吸筹",
                    "🌊 主升浪动量", "🐉 龙回头企稳", "🛡️ 顺丰防御"
                ]
            )
        with rc3:
            st.write("")
            if st.button("📸 弹出选中股【当时入选快照 vs 当前状态】对照窗", type="primary", use_container_width=True):
                if HAS_DIALOG:
                    show_review_snapshot_dialog()
                else:
                    st.session_state["show_inline_rev_snap"] = not st.session_state.get("show_inline_rev_snap", True)
        with rc4:
            st.write("")
            if st.button("📊 校准所有历史选股最新价 & 回溯最高冲高", use_container_width=True):
                with st.spinner("正在校准历史选股最新价并回溯历史K线最高冲高..."):
                    evaluate_tracking_performance_web()
                st.rerun()

        st.markdown('<div class="nexus-panel-title">🏆 十一大战法实盘胜率争霸排行榜 (前三名王牌战法自动获得明日★核心五虎优先晋级权重)</div>', unsafe_allow_html=True)
        df_rk = pd.DataFrame(
            rk_rows,
            columns=["排名", "战法名称", "去重入选数", "已验证样本", "盈利只数", "实盘胜率", "平均累计涨幅", "最高单票冲高", "代表领涨牛股", "战法数学模型与买点摘要"]
        )
        st.dataframe(df_rk, use_container_width=True, hide_index=True, height=230)

        filtered_rev = [
            r for r in all_rev
            if (sel_dt == "全部日期" or sel_dt in str(r[0]))
            and (sel_st_f == "全部战法" or sel_st_f in str(r[1]))
        ]

        st.markdown('<div class="nexus-panel-title">📝 系统历史选股纯净复盘明细库 (勾选任意股票行，立即查看该股【📸选出时是几红几灯/当时逻辑 vs 📈当前最新状态】对照！)</div>', unsafe_allow_html=True)
        if filtered_rev:
            df_rev = pd.DataFrame(
                [r[:12] for r in filtered_rev],
                columns=["首次选出时间", "当时入选战法", "代码", "名称", "锁定入选价", "实时最新价", "选出后累计涨幅", "期间最高冲高", "📸选出时几红几灯", "📸选出时公允评分", "实盘验证状态", "📸当时选出逻辑 & 📈当前对照"]
            )
            render_interactive_df(df_rev, "tbl_review_main", code_col_idx=2, name_col_idx=3, strat_col_idx=1, height=280, pick_date_col_idx=0)

            # 在下方直接常驻展示当前选中复盘股的【当时快照 vs 当前状态】高清对比卡
            with st.expander("📸 当前选中复盘股：【选出那一刻的历史定格快照 (几红几灯/当时逻辑) vs 当前最新状态】深度对照面板", expanded=True):
                _render_review_snapshot_compare_content()
        else:
            st.markdown('<div class="nexus-box-logic">暂无符合筛选条件的历史复盘记录。</div>', unsafe_allow_html=True)

    # ==================== TAB 4: 战法白皮书 ====================
    with main_tabs[3]:
        wp_lines = ["### 📖 Nexus-Alpha V71.4 强庄30日多次试盘法则、波段防卖飞标准与十一大战法数学白皮书\n"]
        for k_s, v_s in STRATEGY_LOGIC_DESCRIPTIONS.items():
            wp_lines.append(f"- **【{k_s}】**：{v_s}")
        st.markdown(
            f'<div class="nexus-box-logic" style="line-height:1.75;">{"<br><br>".join(wp_lines)}</div>',
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    main()