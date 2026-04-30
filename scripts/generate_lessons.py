#!/usr/bin/env python3
"""
康波研究院课程转换器 — Markdown → 可视化HTML
功能：
1. 大字体舒适阅读
2. SVG可视化插图
3. 交互式练习题
4. Edge TTS音频朗读
5. 响应式设计
"""
import os, re, sys, json, glob

COURSES_DIR = os.path.expanduser("~/Desktop/OPC/kondratiev-wave/docs/courses")
OUTPUT_DIR = os.path.expanduser("~/Desktop/OPC/kondratiev-wave/docs")

# 课程元数据
COURSE_META = {
    "01": {"title": "康波理论 — 为什么经济有\"四季\"？", "difficulty": "基础", "time": "30分钟", "icon": "🌊", "category": "理论基础"},
    "02": {"title": "周金涛 — \"人生就是一场康波\"", "difficulty": "基础", "time": "35分钟", "icon": "👤", "category": "理论基础"},
    "03": {"title": "第六轮康波 — AI与新能源驱动的未来", "difficulty": "进阶", "time": "40分钟", "icon": "🔮", "category": "理论基础"},
    "04": {"title": "顶级家族的跨周期生存术", "difficulty": "进阶", "time": "35分钟", "icon": "🏰", "category": "理论基础"},
    "05": {"title": "货币战争与全球金融博弈", "difficulty": "进阶", "time": "40分钟", "icon": "⚔️", "category": "宏观分析"},
    "06": {"title": "投资操作手册 — 周期定位实战", "difficulty": "高级", "time": "45分钟", "icon": "📋", "category": "宏观分析"},
    "07": {"title": "价值投资 — 从格雷厄姆到巴菲特", "difficulty": "基础", "time": "35分钟", "icon": "💎", "category": "投资大师"},
    "08": {"title": "索罗斯 — 反身性与量子基金", "difficulty": "进阶", "time": "40分钟", "icon": "🦅", "category": "投资大师"},
    "09": {"title": "达里奥 — 全天候策略与债务周期", "difficulty": "进阶", "time": "40分钟", "icon": "🌦️", "category": "投资大师"},
    "10": {"title": "塔勒布 — 黑天鹅与反脆弱", "difficulty": "进阶", "time": "35分钟", "icon": "🦢", "category": "投资大师"},
    "11": {"title": "凯恩斯 — 动物精神与政府干预", "difficulty": "基础", "time": "30分钟", "icon": "🏛️", "category": "经济学派"},
    "12": {"title": "明斯基 — 金融不稳定假说", "difficulty": "进阶", "time": "35分钟", "icon": "📉", "category": "经济学派"},
    "13": {"title": "奥地利学派 — 货币周期与自由", "difficulty": "进阶", "time": "35分钟", "icon": "🗽", "category": "经济学派"},
    "14": {"title": "现代货币理论 MMT", "difficulty": "高级", "time": "40分钟", "icon": "🖨️", "category": "经济学派"},
    "15": {"title": "马克思 — 资本积累与危机理论", "difficulty": "高级", "time": "40分钟", "icon": "⚙️", "category": "经济学派"},
    "16": {"title": "巴拉塔 — 大贬值与货币重置", "difficulty": "进阶", "time": "35分钟", "icon": "💰", "category": "专题研究"},
    "17": {"title": "人口周期 — 经济的终极密码", "difficulty": "进阶", "time": "35分钟", "icon": "👥", "category": "专题研究"},
    "18": {"title": "地缘政治经济学", "difficulty": "高级", "time": "40分钟", "icon": "🌍", "category": "专题研究"},
    "19": {"title": "技术奇点 — 当AI超越人类", "difficulty": "高级", "time": "40分钟", "icon": "🤖", "category": "专题研究"},
    "20": {"title": "终极整合 — 构建你的投资世界观", "difficulty": "高级", "time": "50分钟", "icon": "🎯", "category": "终极整合"},
    "21": {"title": "有温度的经济学 — 何帆与中国经济的微观脉搏", "difficulty": "基础", "time": "30分钟", "icon": "🌡️", "category": "趋势洞察"},
    "22": {"title": "置身事内 — 理解中国政府与经济", "difficulty": "进阶", "time": "35分钟", "icon": "🏛️", "category": "趋势洞察"},
    "23": {"title": "债务危机 — 达里奥的全天候思维", "difficulty": "进阶", "time": "35分钟", "icon": "💳", "category": "趋势洞察"},
    "24": {"title": "21世纪资本论 — 贫富分化的真相", "difficulty": "进阶", "time": "30分钟", "icon": "📊", "category": "趋势洞察"},
    "25": {"title": "贫穷的本质 — 诺贝尔奖得主的反直觉发现", "difficulty": "基础", "time": "30分钟", "icon": "💡", "category": "生活经济"},
    "26": {"title": "薛兆丰经济学讲义 — 用经济学思维看世界", "difficulty": "基础", "time": "30分钟", "icon": "🧠", "category": "生活经济"},
    "27": {"title": "激荡三十年 — 中国经济的奇迹与教训", "difficulty": "基础", "time": "35分钟", "icon": "🚀", "category": "生活经济"},
    "28": {"title": "房子、教育、医疗 — 三大民生经济学", "difficulty": "进阶", "time": "40分钟", "icon": "🏠", "category": "生活经济"},
    "29": {"title": "数字经济时代 — 你的钱去哪了", "difficulty": "进阶", "time": "35分钟", "icon": "📱", "category": "生活经济"},
    "30": {"title": "未来十年 — 普通人如何守住财富", "difficulty": "高级", "time": "45分钟", "icon": "🎯", "category": "终极整合"},
}

# SVG插图模板
SVG_DIAGRAMS = {
    "四季模型": '''<svg viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:600px;margin:20px auto;display:block">
  <defs>
    <linearGradient id="spring" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" style="stop-color:#22c55e;stop-opacity:0.3"/><stop offset="100%" style="stop-color:#22c55e;stop-opacity:0.1"/></linearGradient>
    <linearGradient id="summer" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" style="stop-color:#f59e0b;stop-opacity:0.3"/><stop offset="100%" style="stop-color:#f59e0b;stop-opacity:0.1"/></linearGradient>
    <linearGradient id="autumn" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" style="stop-color:#f97316;stop-opacity:0.3"/><stop offset="100%" style="stop-color:#f97316;stop-opacity:0.1"/></linearGradient>
    <linearGradient id="winter" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" style="stop-color:#3b82f6;stop-opacity:0.3"/><stop offset="100%" style="stop-color:#3b82f6;stop-opacity:0.1"/></linearGradient>
  </defs>
  <path d="M50,150 Q125,140 150,100 T250,80 T350,60 T450,100 T550,150" fill="none" stroke="#e2b64f" stroke-width="3" stroke-dasharray="8,4"/>
  <circle cx="50" cy="150" r="8" fill="#22c55e"/><text x="50" y="175" text-anchor="middle" fill="#a1a1aa" font-size="12">冬末</text>
  <circle cx="150" cy="100" r="8" fill="#22c55e"/><text x="150" y="90" text-anchor="middle" fill="#22c55e" font-size="13" font-weight="600">春 🌱</text>
  <circle cx="250" cy="80" r="8" fill="#f59e0b"/><text x="250" y="70" text-anchor="middle" fill="#f59e0b" font-size="13" font-weight="600">夏 ☀️</text>
  <circle cx="350" cy="60" r="8" fill="#f97316"/><text x="350" y="50" text-anchor="middle" fill="#f97316" font-size="13" font-weight="600">秋 🍂</text>
  <circle cx="450" cy="100" r="8" fill="#3b82f6"/><text x="450" y="90" text-anchor="middle" fill="#3b82f6" font-size="13" font-weight="600">冬 ❄️</text>
  <circle cx="550" cy="150" r="8" fill="#22c55e"/><text x="550" y="175" text-anchor="middle" fill="#a1a1aa" font-size="12">下轮春</text>
  <text x="300" y="195" text-anchor="middle" fill="#71717a" font-size="11">← 50-60年一个完整周期 →</text>
</svg>''',

    "嵌套周期": '''<svg viewBox="0 0 600 250" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:600px;margin:20px auto;display:block">
  <rect x="20" y="10" width="560" height="50" rx="8" fill="#1c1c21" stroke="#27272a"/>
  <text x="40" y="40" fill="#e2b64f" font-size="14" font-weight="700">康波（50-60年）</text>
  <rect x="60" y="70" width="480" height="40" rx="6" fill="#1c1c21" stroke="#27272a"/>
  <text x="80" y="95" fill="#a78bfa" font-size="13" font-weight="600">房地产周期（18-25年）</text>
  <rect x="100" y="120" width="400" height="35" rx="6" fill="#1c1c21" stroke="#27272a"/>
  <text x="120" y="142" fill="#3b82f6" font-size="12" font-weight="600">资本支出周期（7-11年）</text>
  <rect x="140" y="165" width="320" height="30" rx="6" fill="#1c1c21" stroke="#27272a"/>
  <text x="160" y="185" fill="#22c55e" font-size="11" font-weight="600">库存周期（3-5年）</text>
  <text x="300" y="225" text-anchor="middle" fill="#71717a" font-size="11">大周期嵌套小周期，叠加产生共振效应</text>
</svg>''',

    "六轮康波": '''<svg viewBox="0 0 700 180" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:700px;margin:20px auto;display:block">
  <line x1="30" y1="140" x2="670" y2="140" stroke="#27272a" stroke-width="1"/>
  <g transform="translate(50,0)"><rect x="0" y="60" width="90" height="70" rx="6" fill="#1c1c21" stroke="#22c55e" stroke-width="1.5"/><text x="45" y="85" text-anchor="middle" fill="#22c55e" font-size="11" font-weight="600">蒸汽机</text><text x="45" y="105" text-anchor="middle" fill="#a1a1aa" font-size="10">1780-1845</text><text x="45" y="120" text-anchor="middle" fill="#71717a" font-size="9">65年</text></g>
  <g transform="translate(155,0)"><rect x="0" y="50" width="90" height="80" rx="6" fill="#1c1c21" stroke="#3b82f6" stroke-width="1.5"/><text x="45" y="75" text-anchor="middle" fill="#3b82f6" font-size="11" font-weight="600">钢铁铁路</text><text x="45" y="95" text-anchor="middle" fill="#a1a1aa" font-size="10">1845-1900</text><text x="45" y="110" text-anchor="middle" fill="#71717a" font-size="9">55年</text></g>
  <g transform="translate(260,0)"><rect x="0" y="40" width="90" height="90" rx="6" fill="#1c1c21" stroke="#a78bfa" stroke-width="1.5"/><text x="45" y="65" text-anchor="middle" fill="#a78bfa" font-size="11" font-weight="600">电气化</text><text x="45" y="85" text-anchor="middle" fill="#a1a1aa" font-size="10">1900-1950</text><text x="45" y="100" text-anchor="middle" fill="#71717a" font-size="9">50年</text></g>
  <g transform="translate(365,0)"><rect x="0" y="30" width="90" height="100" rx="6" fill="#1c1c21" stroke="#f59e0b" stroke-width="1.5"/><text x="45" y="55" text-anchor="middle" fill="#f59e0b" font-size="11" font-weight="600">石油化工</text><text x="45" y="75" text-anchor="middle" fill="#a1a1aa" font-size="10">1950-1990</text><text x="45" y="90" text-anchor="middle" fill="#71717a" font-size="9">40年</text></g>
  <g transform="translate(470,0)"><rect x="0" y="20" width="90" height="110" rx="6" fill="#1c1c21" stroke="#ef4444" stroke-width="1.5"/><text x="45" y="45" text-anchor="middle" fill="#ef4444" font-size="11" font-weight="600">信息技术</text><text x="45" y="65" text-anchor="middle" fill="#a1a1aa" font-size="10">1990-2025</text><text x="45" y="80" text-anchor="middle" fill="#71717a" font-size="9">35年</text></g>
  <g transform="translate(575,0)"><rect x="0" y="10" width="90" height="120" rx="6" fill="rgba(226,182,79,0.1)" stroke="#e2b64f" stroke-width="2" stroke-dasharray="4,2"/><text x="45" y="35" text-anchor="middle" fill="#e2b64f" font-size="11" font-weight="700">AI+新能源</text><text x="45" y="55" text-anchor="middle" fill="#e2b64f" font-size="10">2025-?</text><text x="45" y="70" text-anchor="middle" fill="#e2b64f" font-size="9">第六轮</text></g>
  <text x="350" y="165" text-anchor="middle" fill="#71717a" font-size="11">每轮康波由一个主导技术群驱动 → 周期在缩短</text>
</svg>''',
}

def parse_markdown(md_text):
    """Parse markdown into structured sections."""
    lines = md_text.split('\n')
    sections = []
    current_section = {"title": "", "icon": "", "content": []}
    
    for line in lines:
        # Skip metadata header
        if line.startswith('> **学习目标**') or line.startswith('> **预计时长**') or line.startswith('> **难度**'):
            continue
        if line.strip() == '---':
            if current_section["content"]:
                sections.append(current_section)
                current_section = {"title": "", "icon": "", "content": []}
            continue
        
        # Section headers
        if line.startswith('## '):
            if current_section["content"]:
                sections.append(current_section)
            title = line[3:].strip()
            # Extract icon
            icon_match = re.match(r'^([一二三四五六七八九十]+)、(.+)', title)
            if icon_match:
                current_section = {"title": icon_match.group(2), "icon": "📖", "content": []}
            else:
                current_section = {"title": title, "icon": "📖", "content": []}
            continue
        
        if line.startswith('### '):
            current_section["content"].append({"type": "h3", "text": line[4:].strip()})
            continue
        
        # Tables
        if line.startswith('|') and '---' not in line:
            if not any(c.get("type") == "table_start" for c in current_section["content"][-3:]):
                current_section["content"].append({"type": "table_start", "rows": []})
            # Find the last table
            for c in reversed(current_section["content"]):
                if c.get("type") == "table_start":
                    cells = [cell.strip() for cell in line.split('|')[1:-1]]
                    c["rows"].append(cells)
                    break
            continue
        
        # Blockquotes
        if line.startswith('> '):
            current_section["content"].append({"type": "quote", "text": line[2:].strip()})
            continue
        
        # Lists
        if line.startswith('- '):
            current_section["content"].append({"type": "li", "text": line[2:].strip()})
            continue
        
        # Numbered lists
        num_match = re.match(r'^(\d+)\.\s+(.+)', line)
        if num_match:
            current_section["content"].append({"type": "oli", "num": num_match.group(1), "text": num_match.group(2)})
            continue
        
        # Bold text (standalone)
        if line.startswith('**') and line.endswith('**') and len(line) > 4:
            current_section["content"].append({"type": "bold", "text": line[2:-2]})
            continue
        
        # Regular text
        if line.strip():
            current_section["content"].append({"type": "p", "text": line.strip()})
    
    if current_section["content"]:
        sections.append(current_section)
    
    return sections

def md_inline(text):
    """Convert inline markdown to HTML."""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Code
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text

def section_to_html(section, lesson_num):
    """Convert a parsed section to HTML."""
    html = f'<div class="section">\n'
    html += f'  <h2><span class="icon">{section["icon"]}</span> {md_inline(section["title"])}</h2>\n'
    
    in_table = False
    in_exercise = False
    exercise_items = []
    
    for item in section["content"]:
        t = item["type"]
        
        if t == "table_start":
            if in_table:
                html += '  </tbody></table>\n'
            rows = item["rows"]
            if len(rows) >= 2:
                html += '  <table class="data-table"><thead><tr>'
                for cell in rows[0]:
                    html += f'<th>{md_inline(cell)}</th>'
                html += '</tr></thead><tbody>\n'
                for row in rows[1:]:
                    html += '  <tr>'
                    for cell in row:
                        html += f'<td>{md_inline(cell)}</td>'
                    html += '</tr>\n'
                html += '  </tbody></table>\n'
            in_table = False
            continue
        
        if t == "h3":
            title = item["text"]
            # Check if this is an exercise section
            if "练习" in title or "思考题" in title:
                in_exercise = True
                html += f'  <div class="exercise"><div class="exercise-label">✏️ 练习</div><h3>{md_inline(title)}</h3>\n'
            elif "答案" in title or "参考" in title:
                if in_exercise:
                    html += '  </div>\n'
                    in_exercise = False
                html += f'  <div class="callout green"><div class="callout-title">📝 参考答案</div>\n'
            elif "下节预告" in title or "预告" in title:
                html += f'  <div class="callout blue"><div class="callout-title">🔮 下节预告</div>\n'
            else:
                html += f'  <h3>{md_inline(title)}</h3>\n'
            continue
        
        if t == "quote":
            html += f'  <div class="callout gold"><div class="callout-title">💡 核心洞察</div><p>{md_inline(item["text"])}</p></div>\n'
            continue
        
        if t == "li":
            html += f'  <p>• {md_inline(item["text"])}</p>\n'
            continue
        
        if t == "oli":
            html += f'  <p><strong>{item["num"]}.</strong> {md_inline(item["text"])}</p>\n'
            continue
        
        if t == "bold":
            html += f'  <p><strong>{md_inline(item["text"])}</strong></p>\n'
            continue
        
        if t == "p":
            text = item["text"]
            # Check if it's a question (for exercises)
            if in_exercise and ("?" in text or "？" in text):
                html += f'  <p class="exercise-question">{md_inline(text)}</p>\n'
                html += '  <textarea placeholder="写下你的思考..." rows="3"></textarea>\n'
            else:
                html += f'  <p>{md_inline(text)}</p>\n'
            continue
    
    if in_exercise:
        html += '  </div>\n'
    
    html += '</div>\n'
    return html

def generate_lesson_html(md_path, lesson_num):
    """Generate complete HTML for a lesson."""
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    meta = COURSE_META.get(f"{lesson_num:02d}", {})
    title = meta.get("title", f"第{lesson_num}课")
    difficulty = meta.get("difficulty", "进阶")
    time_est = meta.get("time", "30分钟")
    icon = meta.get("icon", "📖")
    category = meta.get("category", "")
    
    sections = parse_markdown(md_text)
    
    # Count exercises
    exercise_count = sum(1 for s in sections for c in s["content"] if "练习" in str(c))
    
    # Generate section HTML
    sections_html = ""
    for s in sections:
        sections_html += section_to_html(s, lesson_num)
    
    # Insert relevant SVG diagrams
    svg_insert = ""
    if lesson_num == 1:
        svg_insert = SVG_DIAGRAMS.get("四季模型", "")
        svg_insert += SVG_DIAGRAMS.get("六轮康波", "")
    elif lesson_num == 2:
        svg_insert = SVG_DIAGRAMS.get("嵌套周期", "")
    
    # Navigation
    prev_lesson = f"lesson{lesson_num-1}.html" if lesson_num > 1 else None
    next_lesson = f"lesson{lesson_num+1}.html" if lesson_num < 20 else None
    
    prev_btn = f'<a href="{prev_lesson}" class="prev">← 第{lesson_num-1}课</a>' if prev_lesson else '<span></span>'
    next_btn = f'<a href="{next_lesson}" class="next">第{lesson_num+1}课 →</a>' if next_lesson else '<span></span>'
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>第{lesson_num}课：{title} — 康波研究院</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#09090b;--bg2:#0f0f13;--card:#1c1c21;--card2:#222228;--card3:#2a2a32;--border:#27272a;--border2:#3f3f46;--text:#fafafa;--text2:#a1a1aa;--text3:#71717a;--gold:#e2b64f;--gold2:#f5d98a;--green:#22c55e;--blue:#3b82f6;--purple:#a78bfa;--orange:#f59e0b;--red:#ef4444;--serif:'Noto Serif SC',serif;--sans:'Inter',sans-serif;--radius:16px}}
body{{font-family:var(--sans);background:var(--bg);color:var(--text);line-height:2;font-size:18px}}
a{{color:var(--gold);text-decoration:none}}

/* NAV */
.nav{{position:fixed;top:0;left:0;right:0;z-index:100;background:rgba(9,9,11,0.92);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);height:56px;display:flex;align-items:center}}
.nav-inner{{max-width:900px;margin:0 auto;padding:0 24px;width:100%;display:flex;align-items:center;justify-content:space-between}}
.nav-left{{display:flex;align-items:center;gap:16px}}
.nav-back{{font-size:0.9rem;color:var(--text3);transition:color .2s}}.nav-back:hover{{color:var(--gold)}}
.nav-title{{font-size:0.9rem;color:var(--text2);font-weight:500}}
.nav-right{{display:flex;align-items:center;gap:12px}}
.nav-lesson{{font-size:0.8rem;color:var(--text3);background:var(--card2);padding:4px 14px;border-radius:6px}}

/* PROGRESS BAR */
.progress-bar{{position:fixed;top:56px;left:0;right:0;height:3px;background:var(--border);z-index:99}}
.progress-fill{{height:100%;background:linear-gradient(90deg,var(--gold),var(--gold2));transition:width .3s;width:0%}}

/* MAIN */
.main{{max-width:800px;margin:0 auto;padding:80px 28px 60px}}

/* LESSON HEADER */
.lesson-header{{margin-bottom:56px;text-align:center}}
.lesson-cat{{display:inline-block;font-size:0.75rem;color:var(--gold);background:rgba(226,182,79,0.1);padding:4px 14px;border-radius:20px;margin-bottom:16px;letter-spacing:0.1em}}
.lesson-header h1{{font-family:var(--serif);font-size:clamp(2rem,5vw,2.8rem);font-weight:900;line-height:1.3;margin-bottom:16px;background:linear-gradient(135deg,var(--text),var(--gold2));-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.lesson-meta{{display:flex;gap:20px;justify-content:center;flex-wrap:wrap}}
.lesson-meta span{{font-size:0.85rem;color:var(--text3);display:flex;align-items:center;gap:6px}}

/* SECTIONS */
.section{{margin-bottom:48px}}
.section h2{{font-size:1.4rem;font-weight:700;margin-bottom:20px;color:var(--text);display:flex;align-items:center;gap:10px}}
.section h2 .icon{{font-size:1.2rem}}
.section h3{{font-size:1.15rem;font-weight:600;margin:28px 0 12px;color:var(--gold2)}}
.section p{{color:var(--text2);font-size:1.05rem;margin-bottom:14px;line-height:2}}

/* CALLOUT */
.callout{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:28px;margin:24px 0}}
.callout.gold{{border-left:4px solid var(--gold)}}
.callout.green{{border-left:4px solid var(--green)}}
.callout.blue{{border-left:4px solid var(--blue)}}
.callout-title{{font-size:0.85rem;font-weight:600;color:var(--gold);margin-bottom:10px;text-transform:uppercase;letter-spacing:0.08em}}
.callout p{{color:var(--text2);font-size:1rem;line-height:1.9}}

/* TABLE */
.data-table{{width:100%;border-collapse:collapse;margin:20px 0;font-size:0.95rem}}
.data-table th{{text-align:left;padding:12px 14px;background:var(--card2);color:var(--text3);font-weight:600;font-size:0.85rem;text-transform:uppercase;letter-spacing:0.05em;border-bottom:2px solid var(--border)}}
.data-table td{{padding:12px 14px;border-bottom:1px solid var(--border);color:var(--text2)}}
.data-table tr:hover td{{background:var(--card)}}

/* EXERCISE */
.exercise{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:32px;margin:28px 0}}
.exercise-label{{display:inline-flex;align-items:center;gap:6px;font-size:0.8rem;font-weight:600;color:var(--blue);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:14px}}
.exercise h3{{font-size:1.1rem;margin-bottom:10px;color:var(--text)}}
.exercise p{{color:var(--text2);font-size:1rem;margin-bottom:14px}}
.exercise-question{{color:var(--text);font-weight:500;font-size:1.05rem}}
.exercise textarea{{width:100%;min-height:90px;background:var(--card2);border:1px solid var(--border);border-radius:12px;padding:16px;color:var(--text);font-family:var(--sans);font-size:1rem;resize:vertical;transition:border-color .2s;line-height:1.8}}
.exercise textarea:focus{{outline:none;border-color:var(--gold)}}
.exercise textarea::placeholder{{color:var(--text3)}}

/* BOTTOM NAV */
.bottom-nav{{display:flex;justify-content:space-between;align-items:center;padding:36px 0;margin-top:48px;border-top:1px solid var(--border)}}
.bottom-nav a{{display:flex;align-items:center;gap:8px;padding:14px 24px;border-radius:12px;font-size:1rem;font-weight:500;transition:all .2s}}
.bottom-nav .prev{{color:var(--text3);border:1px solid var(--border)}}
.bottom-nav .prev:hover{{border-color:var(--gold);color:var(--gold)}}
.bottom-nav .next{{background:var(--gold);color:#000}}
.bottom-nav .next:hover{{background:var(--gold2)}}

/* AUDIO PLAYER */
.audio-player{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px;margin:24px 0;display:flex;align-items:center;gap:16px}}
.audio-player .play-btn{{width:48px;height:48px;border-radius:50%;background:var(--gold);border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:1.2rem;transition:background .2s;flex-shrink:0}}
.audio-player .play-btn:hover{{background:var(--gold2)}}
.audio-player .audio-info{{flex:1}}
.audio-player .audio-title{{font-size:0.9rem;font-weight:600;color:var(--text);margin-bottom:4px}}
.audio-player .audio-sub{{font-size:0.8rem;color:var(--text3)}}

/* RESPONSIVE */
@media(max-width:640px){{
  .main{{padding:72px 16px 40px}}
  .lesson-header h1{{font-size:1.8rem}}
  .section h2{{font-size:1.2rem}}
  .data-table{{font-size:0.85rem}}
  .data-table th,.data-table td{{padding:8px 10px}}
}}
</style>
</head>
<body>

<nav class="nav">
  <div class="nav-inner">
    <div class="nav-left">
      <a href="index.html" class="nav-back">← 返回首页</a>
      <span class="nav-title">第{lesson_num}课</span>
    </div>
    <div class="nav-right">
      <span class="nav-lesson">{lesson_num} / 20</span>
    </div>
  </div>
</nav>
<div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>

<div class="main">

<!-- HEADER -->
<div class="lesson-header">
  <div class="lesson-cat">{category}</div>
  <h1>{icon} {title}</h1>
  <div class="lesson-meta">
    <span>📖 阅读约{time_est}</span>
    <span>✏️ {exercise_count}道练习题</span>
    <span>🎯 {difficulty}</span>
  </div>
</div>

<!-- AUDIO OVERVIEW -->
<div class="audio-player">
  <button class="play-btn" onclick="toggleAudio()" id="playBtn">▶️</button>
  <div class="audio-info">
    <div class="audio-title">🎧 课程音频概述</div>
    <div class="audio-sub">点击播放课程核心内容摘要</div>
  </div>
  <audio id="courseAudio" preload="none">
    <source src="audio/lesson{lesson_num}.mp3" type="audio/mpeg">
  </audio>
</div>

{svg_insert}

{sections_html}

<!-- BOTTOM NAV -->
<div class="bottom-nav">
  {prev_btn}
  {next_btn}
</div>

</div>

<script>
// Reading progress
window.addEventListener('scroll',()=>{{
  const h=document.documentElement;
  const pct=(h.scrollTop)/(h.scrollHeight-h.clientHeight)*100;
  document.getElementById('progressFill').style.width=pct+'%';
}});

// Audio player
function toggleAudio(){{
  const audio=document.getElementById('courseAudio');
  const btn=document.getElementById('playBtn');
  if(audio.paused){{audio.play();btn.textContent='⏸️'}}else{{audio.pause();btn.textContent='▶️'}}
}}
</script>

</body>
</html>'''
    
    return html


def main():
    # Find all course markdown files
    md_files = sorted(glob.glob(os.path.join(COURSES_DIR, "[0-9]*.md")))
    
    for md_path in md_files:
        basename = os.path.basename(md_path)
        match = re.match(r'^(\d+)-', basename)
        if not match:
            continue
        
        lesson_num = int(match.group(1))
        if lesson_num == 0:
            continue
        
        print(f"Converting lesson {lesson_num}: {basename}...")
        
        html = generate_lesson_html(md_path, lesson_num)
        
        output_path = os.path.join(OUTPUT_DIR, f"lesson{lesson_num}.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"  → {output_path}")
    
    print(f"\nDone! Generated {len(md_files)} lesson pages.")


if __name__ == "__main__":
    main()
