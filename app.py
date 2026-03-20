import streamlit as st
import streamlit.components.v1 as components
import random
import math
import zipfile
import io
import time

# ==========================================
# ⚙️ ตรวจสอบไลบรารี pdfkit (สำหรับปุ่ม Export PDF โดยตรง)
# ==========================================
try:
    import pdfkit
    HAS_PDFKIT = True
except ImportError:
    HAS_PDFKIT = False

# ==========================================
# ตั้งค่าหน้าเพจ Web App & Professional CSS
# ==========================================
st.set_page_config(page_title="Math Generator Pro Standard", page_icon="🚀", layout="wide")

st.markdown("""
<style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1200px; }
    div[data-testid="stSidebar"] div.stButton > button { background-color: #27ae60; color: white; border-radius: 8px; height: 3.5rem; font-size: 18px; font-weight: bold; transition: all 0.3s ease; border: none; box-shadow: 0 4px 6px rgba(39,174,96,0.3); }
    div[data-testid="stSidebar"] div.stButton > button:hover { background-color: #219653; box-shadow: 0 6px 12px rgba(39,174,96,0.4); transform: translateY(-2px); }
    div.stDownloadButton > button { border-radius: 8px; font-weight: bold; border: 1px solid #bdc3c7; transition: all 0.2s ease; }
    div.stDownloadButton > button:hover { border-color: #3498db; color: #3498db; }
    .main-header { background: linear-gradient(135deg, #2980b9, #2c3e50); padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem; box-shadow: 0 10px 20px rgba(0,0,0,0.15); transition: all 0.3s ease;}
    .main-header.challenge { background: linear-gradient(135deg, #c0392b, #8e44ad); }
    .main-header h1 { margin: 0; font-size: 2.8rem; font-weight: 800; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
    .main-header p { margin: 10px 0 0 0; font-size: 1.2rem; opacity: 0.9; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🚀 Math Worksheet Pro <span style="font-size: 20px; background: #f39c12; color: #fff; padding: 5px 15px; border-radius: 20px; vertical-align: middle;">Standard Edition</span></h1>
    <p>ระบบสร้างสื่อการสอนคณิตศาสตร์ (ป.1 - ป.6) หลักสูตรปกติ พร้อมระบบ Spacing ที่ยืดหยุ่น และเฉลยละเอียดยิบ</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 1. คลังคำศัพท์และฟังก์ชันตัวช่วย
# ==========================================
NAMES = ["อคิณ", "นาวิน", "ภูผา", "สายฟ้า", "เจ้านาย", "ข้าวหอม", "ใบบัว", "มะลิ", "น้ำใส", "ญาญ่า", "ปลื้ม", "พายุ", "ไออุ่น", "กะทิ", "คุณครู", "นักเรียน"]
LOCS = ["โรงเรียน", "สวนสัตว์", "สวนสนุก", "ห้างสรรพสินค้า", "ห้องสมุด", "สวนสาธารณะ", "พิพิธภัณฑ์", "ลานกิจกรรม", "ค่ายลูกเสือ"]
ITEMS = ["ลูกแก้ว", "สติกเกอร์", "การ์ดพลัง", "โมเดลรถ", "ตุ๊กตาหมี", "สมุดระบายสี", "ดินสอสี", "ลูกโป่ง"]
SNACKS = ["ช็อกโกแลต", "คุกกี้", "โดนัท", "เยลลี่", "ขนมปัง", "ไอศกรีม", "น้ำผลไม้", "นมเย็น"]
ANIMALS = ["แมงมุม", "มดแดง", "กบ", "จิ้งจก", "ตั๊กแตน", "เต่า", "หอยทาก"]
PUBLISHERS = ["สำนักพิมพ์", "โรงพิมพ์", "ฝ่ายวิชาการ", "ร้านถ่ายเอกสาร", "ทีมงานจัดทำเอกสาร", "บริษัทสิ่งพิมพ์"]
DOC_TYPES = ["หนังสือนิทาน", "รายงานการประชุม", "แคตตาล็อกสินค้า", "เอกสารประกอบการเรียน", "สมุดภาพ", "นิตยสารรายเดือน", "พจนานุกรม"]
BUILDERS = ["บริษัทรับเหมา", "ผู้ใหญ่บ้าน", "เทศบาลตำบล", "เจ้าของโครงการ", "ผู้อำนวยการโรงเรียน", "กรมทางหลวง", "อบต."]
BUILD_ACTIONS = ["ปักเสาไฟ", "ปลูกต้นไม้", "ตั้งศาลาริมทาง", "ติดป้ายประกาศ", "ตั้งถังขยะ", "ปักธงประดับ", "ติดตั้งกล้องวงจรปิด"]
BUILD_LOCS = ["ริมถนนทางเข้าหมู่บ้าน", "เลียบคลองส่งน้ำ", "ริมทางเดินรอบสวน", "บนสะพานยาว", "สองข้างทางเข้างาน", "รอบรั้วโรงเรียน"]
CONTAINERS = ["กล่อง", "ถุงผ้า", "ตะกร้า", "ลังกระดาษ", "แพ็คพลาสติก"]
FRUIT_EMOJIS = {"แอปเปิล": "🍎", "ส้ม": "🍊", "สตรอว์เบอร์รี": "🍓", "กล้วย": "🍌", "มะม่วง": "🥭", "แตงโม": "🍉", "ลูกพีช": "🍑"}
FRUITS = list(FRUIT_EMOJIS.keys())
MATERIALS = ["แผ่นไม้", "กระดาษสี", "แผ่นพลาสติก", "ผืนผ้าใบ", "แผ่นเหล็ก", "แผ่นกระเบื้อง"]
VEHICLES = ["รถยนต์", "รถจักรยานยนต์", "รถบรรทุก", "รถไฟ", "รถตู้"]
WORK_ACTIONS = ["ทาสีบ้าน", "ปลูกต้นไม้", "สร้างกำแพง", "ประกอบหุ่นยนต์", "เก็บขยะ", "จัดหนังสือ"]
ROOMS = ["ห้องนอน", "ห้องนั่งเล่น", "ห้องเรียน", "ห้องทำงาน", "ห้องประชุม", "ห้องเก็บของ"]
FURNITURE = ["ตู้เสื้อผ้า", "โต๊ะทำงาน", "เตียงนอน", "ชั้นวางหนังสือ", "โซฟา", "ตู้โชว์", "โต๊ะเรียน", "ตู้เก็บเอกสาร"]

PLACE_EMOJIS = {"บ้าน": "🏠", "โรงเรียน": "🏫", "ตลาด": "🛒", "วัด": "🛕", "สวนสาธารณะ": "🌳", "โรงพยาบาล": "🏥", "ห้องสมุด": "📚", "สถานีตำรวจ": "🚓"}

box_html = "<span style='display: inline-block; width: 22px; height: 22px; border: 2px solid #333; border-radius: 3px; vertical-align: middle; margin-left: 5px; position: relative; top: -2px;'></span>"

def f_html(n, d, c="#2c3e50", b=True):
    w = "bold" if b else "normal"
    return f"<span style='display:inline-flex; flex-direction:column; vertical-align:middle; text-align:center; line-height:1.4; margin:0 4px;'><span style='border-bottom:2px solid {c}; padding:0 4px; font-weight:{w}; color:{c};'>{n}</span><span style='padding:0 4px; font-weight:{w}; color:{c};'>{d}</span></span>"

def get_vertical_fraction(num, den, color="#c0392b", is_bold=True):
    weight = "bold" if is_bold else "normal"
    return f"""<span style="display:inline-flex; flex-direction:column; vertical-align:middle; text-align:center; line-height:1.4; margin: 0 6px; font-family:'Sarabun', sans-serif; white-space: nowrap;"><span style="border-bottom: 2px solid {color}; padding: 2px 6px; font-weight:{weight}; color:{color};">{num}</span><span style="padding: 2px 6px; font-weight:{weight}; color:{color};">{den}</span></span>"""

def generate_vertical_table_html(a, b, op, result="", is_key=False):
    a_str = f"{a:,}" if isinstance(a, int) else str(a)
    b_str = f"{b:,}" if isinstance(b, int) else str(b)
    res_str = f"{result:,}" if isinstance(result, int) and result != "" else str(result)
    
    ans_val = res_str if is_key else ""
    border_ans = "border-bottom: 4px double #000;" if is_key else ""
    
    return f"""
    <div style='margin-left: 60px; display: block; font-family: "Sarabun", sans-serif; font-variant-numeric: tabular-nums; font-size: 26px; margin-top: 15px; margin-bottom: 15px;'>
        <table style='border-collapse: collapse; text-align: right;'>
            <tr>
                <td style='padding: 0 10px 0 0; border: none;'>{a_str}</td>
                <td rowspan='2' style='vertical-align: middle; text-align: left; padding: 0 0 0 15px; font-size: 28px; font-weight: bold; border: none; color: #333;'>{op}</td>
            </tr>
            <tr>
                <td style='padding: 5px 10px 5px 0; border: none; border-bottom: 2px solid #000;'>{b_str}</td>
            </tr>
            <tr>
                <td style='padding: 5px 10px 0 0; border: none; {border_ans} height: 35px;'>{ans_val}</td>
                <td style='border: none;'></td>
            </tr>
        </table>
    </div>
    """

def generate_unit_math_html(u_maj, u_min, v1_maj, v1_min, v2_maj, v2_min, op, multiplier):
    if op == "+":
        raw_min = v1_min + v2_min
        raw_maj = v1_maj + v2_maj
        carry = raw_min // multiplier
        fin_min = raw_min % multiplier
        fin_maj = raw_maj + carry
        
        html = f"<div style='margin-left: 40px;'><table style='text-align: center; border-collapse: collapse; font-size: 22px; font-family: Sarabun; margin: 10px 0;'>"
        html += f"<tr style='border-bottom: 2px solid #333; font-weight: bold; color: #2c3e50;'><td style='padding: 5px 25px;'>{u_maj}</td><td style='padding: 5px 25px;'>{u_min}</td><td></td></tr>"
        html += f"<tr><td style='padding: 5px;'>{v1_maj:,}</td><td>{v1_min:,}</td><td></td></tr>"
        html += f"<tr><td style='padding: 5px; border-bottom: 2px solid #333;'>{v2_maj:,}</td><td style='border-bottom: 2px solid #333;'>{v2_min:,}</td><td style='font-weight:bold; font-size:26px; padding-left:15px;'>{op}</td></tr>"
        
        if carry > 0:
            html += f"<tr><td style='padding: 5px;'>{raw_maj:,}</td><td>{raw_min:,}</td><td></td></tr>"
            html += f"<tr style='font-weight: bold; color: #c0392b;'><td style='padding: 5px; border-bottom: 4px double #333;'>{fin_maj:,}</td><td style='border-bottom: 4px double #333;'>{fin_min:,}</td><td style='font-size: 16px; text-align: left; padding-left: 10px;'>(ทด <b style='color:red;'>{carry}</b> {u_maj})</td></tr>"
        else:
            html += f"<tr style='font-weight: bold; color: #c0392b;'><td style='padding: 5px; border-bottom: 4px double #333;'>{fin_maj:,}</td><td style='border-bottom: 4px double #333;'>{fin_min:,}</td><td></td></tr>"
        html += "</table></div>"
        ans_str = f"{fin_maj:,} {u_maj} {fin_min:,} {u_min}" if fin_min > 0 else f"{fin_maj:,} {u_maj}"
        return html, ans_str
        
    else:
        is_borrow = v1_min < v2_min
        if is_borrow:
            c_v1_maj = v1_maj - 1
            c_v1_min = v1_min + multiplier
        else:
            c_v1_maj = v1_maj
            c_v1_min = v1_min
            
        fin_maj = c_v1_maj - v2_maj
        fin_min = c_v1_min - v2_min
        
        html = f"<div style='margin-left: 40px;'><table style='text-align: center; border-collapse: collapse; font-size: 22px; font-family: Sarabun; margin: 10px 0;'>"
        html += f"<tr style='border-bottom: 2px solid #333; font-weight: bold; color: #2c3e50;'><td style='padding: 5px 25px;'>{u_maj}</td><td style='padding: 5px 25px;'>{u_min}</td><td></td></tr>"
        
        if is_borrow:
            html += f"<tr style='color: #e74c3c; font-size: 18px; font-weight: bold;'><td>{c_v1_maj:,}</td><td>{c_v1_min:,}</td><td></td></tr>"
            html += f"<tr><td style='padding: 5px; text-decoration: line-through;'>{v1_maj:,}</td><td style='text-decoration: line-through;'>{v1_min:,}</td><td></td></tr>"
        else:
            html += f"<tr><td style='padding: 5px;'>{v1_maj:,}</td><td>{v1_min:,}</td><td></td></tr>"
            
        html += f"<tr><td style='padding: 5px; border-bottom: 2px solid #333;'>{v2_maj:,}</td><td style='border-bottom: 2px solid #333;'>{v2_min:,}</td><td style='font-weight:bold; font-size:26px; padding-left:15px;'>{op}</td></tr>"
        html += f"<tr style='font-weight: bold; color: #c0392b;'><td style='padding: 5px; border-bottom: 4px double #333;'>{fin_maj:,}</td><td style='border-bottom: 4px double #333;'>{fin_min:,}</td><td></td></tr>"
        html += "</table></div>"
        
        ans_str = f"{fin_maj:,} {u_maj} {fin_min:,} {u_min}" if fin_min > 0 else f"{fin_maj:,} {u_maj}"
        if fin_maj <= 0: ans_str = f"{fin_min:,} {u_min}"
        return html, ans_str

def generate_mixed_number_html(whole, num, den):
    return f"<span style='font-size: 24px; vertical-align: middle;'>{whole}</span> {f_html(num, den)}"

def cm_to_m_cm_mm(cm_float):
    total_mm = int(round(cm_float * 10))
    m = total_mm // 1000
    cm = (total_mm % 1000) // 10
    mm = total_mm % 10
    parts = []
    if m > 0: parts.append(f"{m} เมตร")
    if cm > 0: parts.append(f"{cm} เซนติเมตร")
    if mm > 0: parts.append(f"{mm} มิลลิเมตร")
    if not parts: return "0 เซนติเมตร"
    return " ".join(parts)

# ==========================================
# 🌟 ฟังก์ชันวาดรูปภาพ SVG 🌟
# ==========================================
def draw_beakers_svg(v1_l, v1_ml, v2_l, v2_ml):
    def single_beaker(l, ml, name, color):
        tot = l * 1000 + ml
        d_max = math.ceil(tot/1000)*1000 if tot > 0 else 1000
        if d_max < 1000: d_max = 1000
        h = 100
        w = 60
        fill_h = (tot / d_max) * h
        svg = f'<g>'
        svg += f'<rect x="0" y="{20+h-fill_h}" width="{w}" height="{fill_h}" fill="{color}" opacity="0.7"/>'
        svg += f'<path d="M0,20 L0,{20+h} Q0,{20+h+5} 5,{20+h+5} L{w-5},{20+h+5} Q{w},{20+h+5} {w},{20+h} L{w},20" fill="none" stroke="#34495e" stroke-width="3"/>'
        for i in range(1, 4):
            yy = 20 + h - (i * h / 4)
            svg += f'<line x1="0" y1="{yy}" x2="10" y2="{yy}" stroke="#34495e" stroke-width="2"/>'
        lbl = f"{l} ลิตร {ml} มล." if l > 0 else f"{ml} มล."
        if ml == 0 and l > 0: lbl = f"{l} ลิตร"
        svg += f'<text x="{w/2}" y="{h+45}" font-family="Sarabun" font-size="16" font-weight="bold" fill="#333" text-anchor="middle">{name}</text>'
        svg += f'<text x="{w/2}" y="{h+65}" font-family="Sarabun" font-size="14" fill="#e74c3c" font-weight="bold" text-anchor="middle">{lbl}</text>'
        svg += f'</g>'
        return svg

    svg1 = single_beaker(v1_l, v1_ml, "ถัง A", "#3498db")
    svg2 = single_beaker(v2_l, v2_ml, "ถัง B", "#1abc9c")
    
    full_svg = f'<div style="text-align:center; margin: 20px 0;"><svg width="300" height="200">'
    full_svg += f'<g transform="translate(50, 0)">{svg1}</g>'
    full_svg += f'<g transform="translate(190, 0)">{svg2}</g>'
    full_svg += '</svg></div>'
    return full_svg

def draw_distance_route_svg(p_names, p_emojis, dist_texts):
    width = 500
    height = 120
    svg = f'<div style="text-align:center; margin: 15px 0;"><svg width="{width}" height="{height}">'
    
    svg += f'<line x1="50" y1="60" x2="250" y2="60" stroke="#34495e" stroke-width="4" stroke-dasharray="10,5"/>'
    if len(p_names) == 3:
        svg += f'<line x1="250" y1="60" x2="450" y2="60" stroke="#34495e" stroke-width="4" stroke-dasharray="10,5"/>'
    
    svg += f'<text x="150" y="45" font-family="Sarabun" font-size="16" font-weight="bold" fill="#c0392b" text-anchor="middle">{dist_texts[0]}</text>'
    if len(p_names) == 3:
        svg += f'<text x="350" y="45" font-family="Sarabun" font-size="16" font-weight="bold" fill="#c0392b" text-anchor="middle">{dist_texts[1]}</text>'

    xs = [50, 250, 450]
    for i, name in enumerate(p_names):
        emoji = p_emojis[i]
        svg += f'<circle cx="{xs[i]}" cy="60" r="28" fill="#ecf0f1" stroke="#2c3e50" stroke-width="3"/>'
        svg += f'<text x="{xs[i]}" y="68" font-size="28" text-anchor="middle">{emoji}</text>'
        svg += f'<text x="{xs[i]}" y="110" font-family="Sarabun" font-size="16" font-weight="bold" fill="#2c3e50" text-anchor="middle">{name}</text>'

    svg += '</svg></div>'
    return svg

def draw_ruler_svg(start_cm, end_cm):
    scale = 40  
    max_cm = max(10, math.ceil(end_cm) + 1)
    width = max_cm * scale + 60
    height = 140
    svg = f'<div style="text-align:center; margin: 15px 0;"><svg width="{width}" height="{height}">'
    obj_x = 30 + (start_cm * scale)
    obj_w = (end_cm - start_cm) * scale
    tip_len = min(20, obj_w / 3) 
    
    svg += f'<rect x="{obj_x}" y="20" width="{obj_w - tip_len}" height="24" fill="#f1c40f" stroke="#d35400" stroke-width="2" rx="2"/>'
    svg += f'<polygon points="{obj_x + obj_w - tip_len},20 {obj_x + obj_w - tip_len},44 {obj_x + obj_w},32" fill="#34495e"/>'
    svg += f'<line x1="{obj_x}" y1="44" x2="{obj_x}" y2="70" stroke="#e74c3c" stroke-width="2" stroke-dasharray="4,4"/>'
    svg += f'<line x1="{obj_x + obj_w}" y1="32" x2="{obj_x + obj_w}" y2="70" stroke="#e74c3c" stroke-width="2" stroke-dasharray="4,4"/>'
    svg += f'<rect x="20" y="70" width="{max_cm*scale + 20}" height="50" fill="#ecf0f1" stroke="#bdc3c7" stroke-width="2" rx="5"/>'
    
    for i in range(max_cm * 10 + 1):
        x = 30 + i * (scale / 10)
        if i % 10 == 0:  
            svg += f'<line x1="{x}" y1="70" x2="{x}" y2="90" stroke="#2c3e50" stroke-width="3"/>'
            svg += f'<text x="{x}" y="110" font-family="sans-serif" font-size="16" font-weight="bold" fill="#2c3e50" text-anchor="middle">{i//10}</text>'
        elif i % 5 == 0: 
            svg += f'<line x1="{x}" y1="70" x2="{x}" y2="85" stroke="#2c3e50" stroke-width="2"/>'
        else:  
            svg += f'<line x1="{x}" y1="70" x2="{x}" y2="80" stroke="#7f8c8d" stroke-width="1"/>'
    svg += '</svg></div>'
    return svg

def draw_long_ruler_svg(length_cm, color="#f1c40f", name=""):
    scale = 40
    base_cm = int(length_cm) - 2
    if base_cm < 0: base_cm = 0
    max_cm_display = 6 
    width = max_cm_display * scale + 60
    height = 140
    svg = f'<div style="text-align:center; margin: 15px 0;"><svg width="{width}" height="{height}">'
    svg += f'<rect x="20" y="70" width="{max_cm_display*scale + 20}" height="50" fill="#ecf0f1" stroke="#bdc3c7" stroke-width="2" rx="5"/>'
    
    obj_end_x = 30 + (length_cm - base_cm) * scale
    tip_len = min(20, obj_end_x - 10)
    
    svg += f'<rect x="0" y="20" width="{obj_end_x - tip_len}" height="24" fill="{color}" stroke="#333" stroke-width="2"/>'
    svg += f'<polygon points="{obj_end_x - tip_len},20 {obj_end_x - tip_len},44 {obj_end_x},32" fill="#34495e"/>'
    svg += f'<text x="10" y="15" font-family="Sarabun" font-size="14" font-weight="bold" fill="#e74c3c">← {name} (เริ่มจาก 0)</text>'
    svg += f'<line x1="{obj_end_x}" y1="32" x2="{obj_end_x}" y2="70" stroke="#e74c3c" stroke-width="2" stroke-dasharray="4,4"/>'

    for i in range(max_cm_display * 10 + 1):
        x = 30 + i * (scale / 10)
        if i % 10 == 0:
            svg += f'<line x1="{x}" y1="70" x2="{x}" y2="90" stroke="#2c3e50" stroke-width="3"/>'
            lbl = base_cm + i//10
            svg += f'<text x="{x}" y="110" font-family="sans-serif" font-size="16" font-weight="bold" fill="#2c3e50" text-anchor="middle">{lbl}</text>'
        elif i % 5 == 0:
            svg += f'<line x1="{x}" y1="70" x2="{x}" y2="85" stroke="#2c3e50" stroke-width="2"/>'
        else:
            svg += f'<line x1="{x}" y1="70" x2="{x}" y2="80" stroke="#7f8c8d" stroke-width="1"/>'
    svg += '</svg></div>'
    return svg

def draw_fraction_svg(num, den):
    width = 250
    height = 60
    slice_w = width / den
    svg = f'<div style="text-align:center; margin: 10px 0;"><svg width="{width}" height="{height}" style="border: 2px solid #2c3e50;">'
    for i in range(den):
        fill = "#3498db" if i < num else "#ffffff"
        svg += f'<rect x="{i*slice_w}" y="0" width="{slice_w}" height="{height}" fill="{fill}" stroke="#2c3e50" stroke-width="2"/>'
    svg += '</svg></div>'
    return svg

def draw_clock_svg(h_24, m):
    cx, cy, r = 150, 150, 110
    h_12 = h_24 % 12
    m_angle = math.radians(m * 6 - 90)
    h_angle = math.radians(h_12 * 30 + (m * 0.5) - 90)
    
    hx, hy = cx + 60 * math.cos(h_angle), cy + 60 * math.sin(h_angle)
    mx, my = cx + 90 * math.cos(m_angle), cy + 90 * math.sin(m_angle)
    
    h_ext_x, h_ext_y = cx + r * math.cos(h_angle), cy + r * math.sin(h_angle)
    m_ext_x, m_ext_y = cx + r * math.cos(m_angle), cy + r * math.sin(m_angle)

    svg = f'<div style="text-align:center;"><svg width="300" height="300">'
    svg += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="white" stroke="#333" stroke-width="4"/>'
    
    for i in range(60):
        angle = math.radians(i * 6 - 90)
        is_hour = i % 5 == 0
        tick_len = 10 if is_hour else 5
        x1, y1 = cx + (r - tick_len) * math.cos(angle), cy + (r - tick_len) * math.sin(angle)
        x2, y2 = cx + r * math.cos(angle), cy + r * math.sin(angle)
        sw = 3 if is_hour else 1
        svg += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#333" stroke-width="{sw}"/>'
        if is_hour:
            num = i // 5
            if num == 0: num = 12
            nx, ny = cx + (r - 28) * math.cos(angle), cy + (r - 28) * math.sin(angle)
            svg += f'<text x="{nx}" y="{ny}" font-family="sans-serif" font-size="20" font-weight="bold" fill="#333" text-anchor="middle" dominant-baseline="central">{num}</text>'

    svg += f'<line x1="{hx}" y1="{hy}" x2="{h_ext_x}" y2="{h_ext_y}" stroke="#e74c3c" stroke-width="2" stroke-dasharray="5,5"/>'
    svg += f'<line x1="{mx}" y1="{my}" x2="{m_ext_x}" y2="{m_ext_y}" stroke="#3498db" stroke-width="2" stroke-dasharray="5,5"/>'
    
    svg += f'<line x1="{cx}" y1="{cy}" x2="{hx}" y2="{hy}" stroke="#e74c3c" stroke-width="6" stroke-linecap="round"/>'
    svg += f'<line x1="{cx}" y1="{cy}" x2="{mx}" y2="{my}" stroke="#3498db" stroke-width="4" stroke-linecap="round"/>'
    svg += f'<circle cx="{cx}" cy="{cy}" r="6" fill="#333"/>'
    svg += '</svg></div>'
    return svg

def draw_scale_svg(kg, kheed, max_kg=5):
    cx, cy, r = 150, 150, 120
    total_kheed = kg * 10 + kheed
    angle = math.radians(total_kheed * 7.2 - 90)
    
    nx, ny = cx + 100 * math.cos(angle), cy + 100 * math.sin(angle) 
    
    svg = f'<div style="text-align:center;"><svg width="300" height="300">'
    svg += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fdfefe" stroke="#2c3e50" stroke-width="6"/>'
    svg += f'<circle cx="{cx}" cy="{cy}" r="{r-25}" fill="none" stroke="#bdc3c7" stroke-width="1"/>' 
    svg += f'<text x="{cx}" y="{cy+45}" font-family="sans-serif" font-size="20" font-weight="bold" fill="#7f8c8d" text-anchor="middle">kg</text>'
    
    for i in range(max_kg * 10):
        tick_angle = math.radians(i * 7.2 - 90)
        is_kg = i % 10 == 0
        tick_len = 25 if is_kg else (15 if i % 5 == 0 else 10) 
        x1, y1 = cx + (r - tick_len) * math.cos(tick_angle), cy + (r - tick_len) * math.sin(tick_angle)
        x2, y2 = cx + r * math.cos(tick_angle), cy + r * math.sin(tick_angle)
        sw = 4 if is_kg else (3 if i % 5 == 0 else 2) 
        svg += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#2c3e50" stroke-width="{sw}"/>'
        if is_kg:
            num = i // 10
            nx_t, ny_t = cx + (r - 40) * math.cos(tick_angle), cy + (r - 40) * math.sin(tick_angle)
            svg += f'<text x="{nx_t}" y="{ny_t}" font-family="sans-serif" font-size="26" font-weight="bold" fill="#2c3e50" text-anchor="middle" dominant-baseline="central">{num}</text>'
            
    svg += f'<line x1="{cx}" y1="{cy}" x2="{nx}" y2="{ny}" stroke="#c0392b" stroke-width="4" stroke-linecap="round"/>'
    svg += f'<circle cx="{cx}" cy="{cy}" r="10" fill="#c0392b"/>'
    svg += '</svg></div>'
    return svg

def draw_complex_pictogram_html(item, emoji, pic_val):
    days = random.sample(["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์"], 3)
    counts = [random.randint(2, 6) for _ in range(3)]
    html = f"""
    <div style="border: 2px solid #34495e; border-radius: 10px; width: 80%; margin: 15px auto; background-color: #fff; font-family: 'Sarabun', sans-serif;">
        <div style="text-align: center; background-color: #ecf0f1; padding: 10px; font-weight: bold; border-bottom: 2px solid #34495e; font-size: 20px;">จำนวน{item}ที่ขายได้</div>
        <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 24px;">
    """
    for d, c in zip(days, counts):
        icons = "".join([f"<span style='margin: 0 4px;'>{emoji}</span>"] * c)
        html += f'<tr><td style="padding: 10px; border-bottom: 1px solid #eee; width: 30%; border-right: 2px solid #34495e; text-align: center;"><b>วัน{d}</b></td><td style="padding: 10px; border-bottom: 1px solid #eee; text-align: left; padding-left: 20px;">{icons}</td></tr>'
    html += f"""</table>
        <div style="background-color: #fdf2e9; padding: 10px; text-align: center; font-size: 18px; color: #d35400; font-weight: bold; border-top: 2px solid #34495e;">กำหนดให้ {emoji} 1 รูป แทนจำนวน {pic_val} ผล</div>
    </div>"""
    return html, days, counts

def generate_short_division_html(a, b, mode="ห.ร.ม."):
    factors = []
    ca = a
    cb = b
    steps_html = ""
    while True:
        found = False
        for i in range(2, min(ca, cb) + 1):
            if ca % i == 0 and cb % i == 0:
                steps_html += f"<tr><td style='text-align: right; padding-right: 10px; font-weight: bold; color: #c0392b;'>{i}</td><td style='border-left: 2px solid #000; border-bottom: 2px solid #000; padding: 5px 15px; text-align: center;'>{ca}</td><td style='border-bottom: 2px solid #000; padding: 5px 15px; text-align: center;'>{cb}</td></tr>"
                factors.append(i)
                ca //= i
                cb //= i
                found = True
                break
        if not found: break
    if not factors:
        if mode == "ห.ร.ม.": return f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br><b>ขั้นที่ 1:</b> ลองหาตัวเลขที่สามารถหารทั้ง {a} และ {b} ลงตัวพร้อมกัน<br><b>ขั้นที่ 2:</b> พบว่าไม่มีตัวเลขใดเลยที่หารทั้งคู่ลงตัวได้ (นอกจากเลข 1)<br><b>ดังนั้น ห.ร.ม. = 1</b></span>"
        else: return f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br><b>ขั้นที่ 1:</b> ลองหาตัวเลขที่สามารถหารทั้ง {a} และ {b} ลงตัวพร้อมกัน<br><b>ขั้นที่ 2:</b> พบว่าไม่มีตัวเลขใดเลยที่หารทั้งคู่ลงตัว<br><b>ขั้นที่ 3:</b> การหา ค.ร.น. ในกรณีนี้ ให้นำตัวเลขทั้งสองตัวมาคูณกันได้เลย<br><b>ดังนั้น ค.ร.น. = {a} × {b} = {a*b}</b></span>"
    steps_html += f"<tr><td></td><td style='padding: 5px 15px; text-align: center;'>{ca}</td><td style='padding: 5px 15px; text-align: center;'>{cb}</td></tr>"
    table = f"<table style='margin: 10px 0; font-size: 20px; border-collapse: collapse; color: #333;'>{steps_html}</table>"
    if mode == "ห.ร.ม.":
        ans = math.prod(factors)
        calc_str = " × ".join(map(str, factors))
        sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (การตั้งหารสั้น):</b><br><b>ขั้นที่ 1:</b> หาตัวเลขที่สามารถหารทั้ง {a} และ {b} ลงตัวพร้อมกัน นำมาใส่เป็นตัวหารด้านหน้า<br><b>ขั้นที่ 2:</b> หารไปเรื่อยๆ จนกว่าจะไม่มีตัวเลขใดหารลงตัวทั้งคู่แล้ว<br>{table}<br><b>ขั้นที่ 3:</b> การหา ห.ร.ม. ให้นำเฉพาะ <b>ตัวเลขด้านหน้าเครื่องหมายหารสั้น</b> มาคูณกัน<br><b>ดังนั้น ห.ร.ม. = {calc_str} = {ans}</b></span>"
    else:
        ans = math.prod(factors) * ca * cb
        calc_str = " × ".join(map(str, factors + [ca, cb]))
        sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (การตั้งหารสั้น):</b><br><b>ขั้นที่ 1:</b> หาตัวเลขที่สามารถหารทั้ง {a} และ {b} ลงตัวพร้อมกัน นำมาใส่เป็นตัวหารด้านหน้า<br><b>ขั้นที่ 2:</b> หารไปเรื่อยๆ จนกว่าจะไม่มีตัวเลขใดหารลงตัวทั้งคู่แล้ว<br>{table}<br><b>ขั้นที่ 3:</b> การหา ค.ร.น. ให้นำ <b>ตัวเลขด้านหน้าทั้งหมด และ เศษที่เหลือด้านล่างสุดทั้งหมด (นำมาเป็นรูปตัว L)</b> มาคูณกัน<br><b>ดังนั้น ค.ร.น. = {calc_str} = {ans}</b></span>"
    return sol

def generate_decimal_vertical_html(a, b, op, is_key=False):
    str_a = f"{a:.2f}"
    str_b = f"{b:.2f}"
    ans = a + b if op == '+' else round(a - b, 2)
    str_ans = f"{ans:.2f}"
    max_len = max(len(str_a), len(str_b), len(str_ans)) + 1 
    str_a = str_a.rjust(max_len, " ")
    str_b = str_b.rjust(max_len, " ")
    str_ans = str_ans.rjust(max_len, " ")
    strike = [False] * max_len
    top_marks = [""] * max_len
    
    if is_key:
        if op == '+':
            carry = 0
            for i in range(max_len - 1, -1, -1):
                if str_a[i] == '.': continue
                da = int(str_a[i]) if str_a[i].strip() else 0
                db = int(str_b[i]) if str_b[i].strip() else 0
                s = da + db + carry
                carry = s // 10
                if carry > 0 and i > 0:
                    next_i = i - 1
                    if str_a[next_i] == '.': next_i -= 1
                    if next_i >= 0: top_marks[next_i] = str(carry)
        elif op == '-':
            a_chars = list(str_a)
            b_chars = list(str_b)
            a_digits = [int(c) if c.strip() and c != '.' else 0 for c in a_chars]
            b_digits = [int(c) if c.strip() and c != '.' else 0 for c in b_chars]
            for i in range(max_len - 1, -1, -1):
                if str_a[i] == '.': continue
                if a_digits[i] < b_digits[i]:
                    for j in range(i-1, -1, -1):
                        if str_a[j] == '.': continue
                        if a_digits[j] > 0 and str_a[j].strip() != "":
                            strike[j] = True
                            a_digits[j] -= 1
                            top_marks[j] = str(a_digits[j])
                            for k in range(j+1, i):
                                if str_a[k] == '.': continue
                                strike[k] = True
                                a_digits[k] = 9
                                top_marks[k] = "9"
                            strike[i] = True
                            a_digits[i] += 10
                            top_marks[i] = str(a_digits[i])
                            break
                            
    a_tds = ""
    for i in range(max_len):
        val = str_a[i].strip() if str_a[i].strip() else ""
        if str_a[i] == '.': val = "."
        td_content = val
        if val and val != '.':
            mark = top_marks[i]
            if strike[i] and is_key: 
                td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span style="text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;">{val}</span></div>'
            elif mark and is_key: 
                td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span>{val}</span></div>'
        a_tds += f"<td style='width: 35px; text-align: center; height: 50px; vertical-align: bottom;'>{td_content}</td>"
        
    b_tds = "".join([f"<td style='width: 35px; text-align: center; border-bottom: 2px solid #000; height: 40px; vertical-align: bottom;'>{c.strip() if c.strip() else ('.' if c=='.' else '')}</td>" for c in str_b])
    
    if is_key: 
        ans_tds = "".join([f"<td style='width: 35px; text-align: center; color: red; font-weight: bold; height: 45px; vertical-align: bottom;'>{c.strip() if c.strip() else ('.' if c=='.' else '')}</td>" for c in str_ans])
    else: 
        ans_tds = "".join([f"<td style='width: 35px; height: 45px;'></td>" for _ in str_ans])
        
    return f"""<div style="display: block; margin-left: 60px; margin-top: 15px; margin-bottom: 15px;"><div style="display: inline-block; font-family: 'Sarabun', sans-serif; font-size: 32px; line-height: 1.2;"><table style="border-collapse: collapse;"><tr><td style="width: 20px;"></td>{a_tds}<td style="width: 50px; text-align: left; padding-left: 15px; vertical-align: middle;" rowspan="2">{op}</td></tr><tr><td></td>{b_tds}</tr><tr><td></td>{ans_tds}<td></td></tr><tr><td></td><td colspan="{max_len}" style="border-bottom: 6px double #000; height: 10px;"></td><td></td></tr></table></div></div>"""

def generate_long_division_step_by_step_html(divisor, dividend, equation_html, is_key=False):
    div_str = str(dividend)
    div_len = len(div_str)
    
    if not is_key:
        ans_tds_list = [f'<td style="width: 35px; height: 45px;"></td>' for _ in div_str]
        ans_tds_list.append('<td style="width: 35px;"></td>')
        div_tds_list = []
        for i, c in enumerate(div_str):
            left_border = "border-left: 3px solid #000;" if i == 0 else ""
            div_tds_list.append(f'<td style="width: 35px; text-align: center; border-top: 3px solid #000; {left_border} font-size: 38px; height: 50px; vertical-align: bottom;">{c}</td>')
        div_tds_list.append('<td style="width: 35px;"></td>')
        empty_rows = ""
        for _ in range(div_len + 1): 
            empty_rows += f"<tr><td style='border: none;'></td>"
            for _ in range(div_len + 1):
                empty_rows += f"<td style='width: 35px; height: 45px;'></td>"
            empty_rows += "</tr>"
        return f"{equation_html}<div style=\"display: block; margin-left: 60px; margin-top: 15px; margin-bottom: 15px;\"><div style=\"display: inline-block; font-family: 'Sarabun', sans-serif; line-height: 1.2;\"><table style=\"border-collapse: collapse;\"><tr><td style=\"border: none;\"></td>{''.join(ans_tds_list)}</tr><tr><td style=\"border: none; text-align: right; padding-right: 12px; vertical-align: bottom; font-size: 38px;\">{divisor}</td>{''.join(div_tds_list)}</tr>{empty_rows}</table></div></div>"
    
    steps = []
    current_val_str = ""
    ans_str = ""
    has_started = False
    
    for i, digit in enumerate(div_str):
        current_val_str += digit
        current_val = int(current_val_str)
        q = current_val // divisor
        mul_res = q * divisor
        rem = current_val - mul_res
        if not has_started and q == 0 and i < len(div_str) - 1:
             current_val_str = str(rem) if rem != 0 else ""
             continue
        has_started = True
        ans_str += str(q)
        cur_chars = list(str(current_val))
        m_chars = list(str(mul_res).zfill(len(str(current_val))))
        c_dig = [int(c) for c in cur_chars]
        m_dig = [int(c) for c in m_chars]
        
        top_m = [""] * len(c_dig)
        strik = [False] * len(c_dig)
        for idx_b in range(len(c_dig) - 1, -1, -1):
            if c_dig[idx_b] < m_dig[idx_b]:
                for j in range(idx_b-1, -1, -1):
                    if c_dig[j] > 0:
                        strik[j] = True
                        c_dig[j] -= 1
                        top_m[j] = str(c_dig[j])
                        for k in range(j+1, idx_b): 
                            strik[k] = True
                            c_dig[k] = 9
                            top_m[k] = "9"
                        strik[idx_b] = True
                        c_dig[idx_b] += 10
                        top_m[idx_b] = str(c_dig[idx_b])
                        break
        steps.append({'mul_res': mul_res, 'rem': rem, 'col_index': i, 'top_m': top_m, 'strik': strik})
        current_val_str = str(rem) if rem != 0 else ""
        
    ans_padded = ans_str.rjust(div_len, " ")
    ans_tds_list = [f'<td style="width: 35px; text-align: center; color: red; font-weight: bold; font-size: 38px;">{c.strip()}</td>' for c in ans_padded]
    ans_tds_list.append('<td style="width: 35px;"></td>') 
    div_tds_list = []
    s0 = steps[0] if len(steps) > 0 else None
    s0_start = s0['col_index'] + 1 - len(s0['top_m']) if s0 else 0
    for i, c in enumerate(div_str):
        left_border = "border-left: 3px solid #000;" if i == 0 else ""
        td_content = c
        if is_key and s0 and s0_start <= i <= s0['col_index']:
            t_idx = i - s0_start
            mark = s0['top_m'][t_idx]
            is_strik = s0['strik'][t_idx]
            if is_strik: 
                td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span style="text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;">{c}</span></div>'
            elif mark: 
                td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span>{c}</span></div>'
        div_tds_list.append(f'<td style="width: 35px; height: 50px; vertical-align: bottom; text-align: center; border-top: 3px solid #000; {left_border} font-size: 38px;">{td_content}</td>')
    div_tds_list.append('<td style="width: 35px;"></td>') 
    
    html = f"{equation_html}<div style=\"display: block; margin-left: 60px; margin-top: 15px; margin-bottom: 15px;\"><div style=\"display: inline-block; font-family: 'Sarabun', sans-serif; line-height: 1.2;\"><table style=\"border-collapse: collapse;\"><tr><td style=\"border: none;\"></td>{''.join(ans_tds_list)}</tr><tr><td style=\"border: none; text-align: right; padding-right: 12px; vertical-align: bottom; font-size: 38px;\">{divisor}</td>{''.join(div_tds_list)}</tr>"
    
    for idx, step in enumerate(steps):
        mul_res_str = str(step['mul_res'])
        pad_len = step['col_index'] + 1 - len(mul_res_str)
        mul_tds = ""
        for i in range(div_len + 1):
            if i >= pad_len and i <= step['col_index']:
                digit_idx = i - pad_len
                border_b = "border-bottom: 2px solid #000;" if i <= step['col_index'] else ""
                mul_tds += f'<td style="width: 35px; height: 50px; vertical-align: bottom; text-align: center; font-size: 38px; {border_b}">{mul_res_str[digit_idx]}</td>'
            elif i == step['col_index'] + 1: 
                mul_tds += '<td style="width: 35px; text-align: center; font-size: 38px; color: #333; position: relative; top: -24px;">-</td>'
            else: 
                mul_tds += '<td style="width: 35px;"></td>'
        html += f"<tr><td style='border: none;'></td>{mul_tds}</tr>"
        
        is_last_step = (idx == len(steps) - 1)
        next_step = steps[idx+1] if not is_last_step else None
        ns_start = next_step['col_index'] + 1 - len(next_step['top_m']) if next_step else 0
        rem_str = str(step['rem'])
        next_digit = div_str[step['col_index'] + 1] if not is_last_step else ""
        display_str = rem_str if rem_str != "0" or is_last_step else ""
        
        if not is_last_step and display_str == "": pass
        else: display_str += next_digit
        if display_str == "": display_str = next_digit
        
        pad_len_rem = step['col_index'] + 1 - len(display_str) + (1 if not is_last_step else 0)
        rem_tds = ""
        for i in range(div_len + 1):
            if i >= pad_len_rem and i <= step['col_index'] + (1 if not is_last_step else 0):
                digit_idx = i - pad_len_rem
                char_val = display_str[digit_idx]
                td_content = char_val
                if is_key and next_step and ns_start <= i <= next_step['col_index']:
                    t_idx = i - ns_start
                    mark = next_step['top_m'][t_idx]
                    is_strik = next_step['strik'][t_idx]
                    if is_strik: 
                        td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span style="text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;">{char_val}</span></div>'
                    elif mark: 
                        td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span>{char_val}</span></div>'
                border_b2 = "border-bottom: 6px double #000;" if is_last_step else ""
                rem_tds += f'<td style="width: 35px; height: 50px; vertical-align: bottom; text-align: center; font-size: 38px; {border_b2}">{td_content}</td>'
            else: 
                rem_tds += '<td style="width: 35px;"></td>'
        html += f"<tr><td style='border: none;'></td>{rem_tds}</tr>"
        
    html += "</table></div></div>"
    html += f"<div style='margin-top: 15px; color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) นำตัวหาร ({divisor}) ไปหารตัวตั้ง ({dividend}) ทีละหลักจากซ้ายไปขวา<br>2) ท่องสูตรคูณแม่ {divisor} ว่าคูณอะไรแล้วได้ใกล้เคียงหรือเท่ากับตัวตั้งในหลักนั้นที่สุด (แต่ห้ามเกิน)<br>3) ใส่ผลลัพธ์ไว้ด้านบน และนำผลคูณมาลบกันด้านล่าง<br>4) ดึงตัวเลขในหลักถัดไปลงมา แล้วทำซ้ำขั้นตอนเดิมจนหมดทุกหลัก</div>"
    return html

def generate_thai_number_text(num_str):
    thai_nums = ["ศูนย์", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
    positions = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]
    parts = str(num_str).replace(",", "").split(".")
    int_part = parts[0]
    dec_part = parts[1] if len(parts) > 1 else ""
    
    def read_int(s):
        if s == "0" or s == "": return "ศูนย์"
        res = ""
        length = len(s)
        for i, digit in enumerate(s):
            d = int(digit)
            if d == 0: continue
            pos = length - i - 1
            if pos == 1 and d == 2: res += "ยี่สิบ"
            elif pos == 1 and d == 1: res += "สิบ"
            elif pos == 0 and d == 1 and length > 1: res += "เอ็ด"
            else: res += thai_nums[d] + positions[pos]
        return res
        
    int_text = read_int(int_part)
    dec_text = ("จุด" + "".join([thai_nums[int(d)] for d in dec_part])) if dec_part else ""
    return int_text + dec_text

def get_prefix(grade):
    if grade in ["ป.1", "ป.2", "ป.3"]: 
        return "<b style='color: #2c3e50; margin-right: 5px;'>ประโยคสัญลักษณ์:</b>"
    return ""

# ==========================================
# 2. ฐานข้อมูลหลักสูตร (Master Database)
# ==========================================
curriculum_db = {
    "ป.1": {
        "จำนวนนับ 1 ถึง 100 และ 0": ["การนับทีละ 1", "การนับทีละ 10", "การอ่านและการเขียนตัวเลข", "การแสดงจำนวนในรูปความสัมพันธ์แบบส่วนย่อย-ส่วนรวม", "แบบรูปซ้ำของรูปเรขาคณิต", "การบอกอันดับที่ (รถแข่ง)", "หลัก ค่าของเลขโดดในแต่ละหลัก และรูปกระจาย", "การเปรียบเทียบจำนวน (> <)",  "การเปรียบเทียบจำนวน (= ≠)", "การเรียงลำดับจำนวน (น้อยไปมาก)", "การเรียงลำดับจำนวน (มากไปน้อย)"],
        "การบวก การลบ": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)"],
        "แผนภูมิรูปภาพ": ["การอ่านแผนภูมิรูปภาพ"]
    },
    "ป.2": {
        "จำนวนนับไม่เกิน 1,000 และ 0": ["การนับทีละ 2 ทีละ 5 ทีละ 10 และทีละ 100", "การอ่านและการเขียนตัวเลข", "จำนวนคู่ จำนวนคี่", "หลัก ค่าของเลขโดด และรูปกระจาย", "การเปรียบเทียบจำนวน (> <)", "การเรียงลำดับจำนวน (น้อยไปมาก)", "การเรียงลำดับจำนวน (มากไปน้อย)"],
        "เวลาและการวัด": ["การบอกเวลาเป็นนาฬิกาและนาที", "การอ่านน้ำหนักจากเครื่องชั่งสปริง", "การอ่านความยาวจากไม้บรรทัด"],
        "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การคูณ (แบบตั้งหลัก)", "การหารพื้นฐาน"],
        "แผนภูมิรูปภาพ": ["การอ่านแผนภูมิรูปภาพ"]
    },
    "ป.3": {
        "จำนวนนับและเศษส่วน": ["การอ่าน การเขียนตัวเลข", "หลัก ค่าของเลขโดด และรูปกระจาย", "การเปรียบเทียบจำนวน (> <)", "การเรียงลำดับจำนวน (น้อยไปมาก)", "การเรียงลำดับจำนวน (มากไปน้อย)", "การอ่านและเขียนเศษส่วน", "การบวกลบเศษส่วน (ตัวส่วนเท่ากัน)"],
        "เวลา เงิน และการวัด": [
            "การบอกเวลาเป็นนาฬิกาและนาที", 
            "การบอกจำนวนเงินทั้งหมด", 
            "การอ่านน้ำหนักจากเครื่องชั่งสปริง", 
            "การอ่านความยาวจากไม้บรรทัด", 
            "ระยะทาง (กิโลเมตรและเมตร)", 
            "โจทย์ปัญหาความยาว (คูณและหาร)", 
            "การเปรียบเทียบหน่วยการวัด และการแปลงหน่วย (มิลลิเมตร เซนติเมตร เมตร)",
            "การเปรียบเทียบหน่วยระยะทาง และการแปลงหน่วย (เมตร กิโลเมตร)",
            "การเปรียบเทียบหน่วยน้ำหนัก และการแปลงหน่วย (กรัม กิโลกรัม ตัน)",
            "ปริมาตรและความจุ (มิลลิลิตร ลิตร)"
        ],
        "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การคูณ (แบบตั้งหลัก)", "การหารยาว"],
        "แผนภูมิรูปภาพ": ["การอ่านแผนภูมิรูปภาพ"]
    },
    "ป.4": {
        "จำนวนนับที่มากกว่า 100,000": ["การอ่านและการเขียนตัวเลข", "หลัก ค่าประจำหลัก และรูปกระจาย", "การเปรียบเทียบและเรียงลำดับ", "ค่าประมาณเป็นจำนวนเต็มสิบ เต็มร้อย เต็มพัน"],
        "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การคูณ (แบบตั้งหลัก)", "การหารยาว"],
        "เศษส่วนและทศนิยม": ["แปลงเศษเกินเป็นจำนวนคละ", "การอ่านและการเขียนทศนิยม"],
        "เรขาคณิตและการวัด": ["การบอกชนิดของมุม", "การวัดขนาดของมุม (ไม้โปรแทรกเตอร์)", "การหาความยาวรอบรูปสี่เหลี่ยมมุมฉาก", "การหาพื้นที่รูปสี่เหลี่ยมมุมฉาก"],
        "สมการ": ["การแก้สมการ (บวก/ลบ)"]
    },
    "ป.5": {
        "เศษส่วน": ["การบวกเศษส่วน", "การลบเศษส่วน", "การคูณเศษส่วน", "การหารเศษส่วน"],
        "ทศนิยม": ["การบวกและการลบทศนิยม", "การคูณทศนิยม"],
        "ร้อยละและเปอร์เซ็นต์": ["การเขียนเศษส่วนในรูปร้อยละ"],
        "สมการ": ["การแก้สมการ (คูณ/หาร)"]
    },
    "ป.6": {
        "ตัวประกอบของจำนวนนับ": ["การหา ห.ร.ม.", "การหา ค.ร.น."],
        "อัตราส่วนและร้อยละ": ["การหาอัตราส่วนที่เท่ากัน", "โจทย์ปัญหาอัตราส่วน", "โจทย์ปัญหาร้อยละ"],
        "สมการ": ["การแก้สมการ (สองขั้นตอน)"]
    }
}

# ==========================================
# 3. Logic & Dynamic Difficulty Scaling
# ==========================================
def generate_questions_logic(grade, main_t, sub_t, num_q, is_challenge=False):
    questions = []
    seen = set()
    limit_map = {"ป.1": 100, "ป.2": 1000, "ป.3": 100000, "ป.4": 1000000, "ป.5": 9000000, "ป.6": 9000000}
    
    base_limit = limit_map.get(grade, 100)
    limit = base_limit * (10 if is_challenge else 1)

    for _ in range(num_q):
        q = ""
        sol = ""
        attempts = 0
        
        while attempts < 300:
            actual_sub_t = sub_t
            if sub_t == "แบบทดสอบรวมปลายภาค":
                all_mains = [m for m in curriculum_db[grade].keys()]
                rand_main = random.choice(all_mains)
                actual_sub_t = random.choice(curriculum_db[grade][rand_main])

            prefix = get_prefix(grade)

            if actual_sub_t == "ปริมาตรและความจุ (มิลลิลิตร ลิตร)":
                q_cat = random.choice(["compare", "add_sub"])
                multiplier = 1000
                u_major, u_minor = "ลิตร", "มิลลิลิตร"
                
                if q_cat == "compare":
                    val_major = random.randint(5, 50) if is_challenge else random.randint(1, 15)
                    val_minor = random.randint(50, 950)
                    total_minor_1 = (val_major * multiplier) + val_minor
                    
                    case = random.choice(["greater", "less", "equal"])
                    if case == "equal":
                        total_minor_2 = total_minor_1
                    elif case == "greater":
                        total_minor_2 = total_minor_1 - random.randint(1, multiplier - 1)
                    else:
                        total_minor_2 = total_minor_1 + random.randint(1, multiplier - 1)

                    str_val_1 = f"{val_major} {u_major} {val_minor} {u_minor}"
                    str_val_2 = f"{total_minor_2:,} {u_minor}"

                    if random.choice([True, False]):
                        item_A, item_B = str_val_1, str_val_2
                        val_A, val_B = total_minor_1, total_minor_2
                    else:
                        item_A, item_B = str_val_2, str_val_1
                        val_A, val_B = total_minor_2, total_minor_1

                    if total_minor_1 == total_minor_2:
                        final_ans = "จุเท่ากัน"
                    else:
                        final_ans = "จุมากกว่า" if val_A > val_B else "จุน้อยกว่า"
                        
                    q = f"จงเติมคำว่า <b>จุมากกว่า, จุน้อยกว่า</b> หรือ <b>เท่ากับ</b> ลงในช่องว่างให้ถูกต้อง<br><br><span style='font-size:22px; font-weight:bold; margin-left: 20px;'>{item_A} &nbsp;&nbsp; ____________________ &nbsp;&nbsp; {item_B}</span>"

                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (การเปรียบเทียบความจุ):</b><br>
                    <b>ขั้นที่ 1: สร้างสมการแปลงหน่วยให้เหมือนกัน</b><br>
                    👉 แปลง <b>{str_val_1}</b> ให้เป็น <b>{u_minor}</b> ทั้งหมด<br>
                    👉 เนื่องจาก 1 {u_major} = {multiplier:,} {u_minor}<br>
                    👉 <b>สมการล่าสุด:</b> ({val_major} <b style='color:red;'>× {multiplier:,}</b>) + {val_minor} = {val_major * multiplier:,} + {val_minor} = <b>{total_minor_1:,} {u_minor}</b><br>
                    <b>ขั้นที่ 2: เปรียบเทียบปริมาตร</b><br>"""

                    if val_A == val_B:
                        sol += f"👉 จะเห็นว่า {total_minor_1:,} {u_minor} <b>เท่ากับ</b> {total_minor_2:,} {u_minor} พอดี!<br>"
                    else:
                        comp_sign = "น้อยกว่า" if val_A < val_B else "มากกว่า"
                        sol += f"👉 เปรียบเทียบ {val_A:,} {u_minor} กับ {val_B:,} {u_minor}<br>"
                        sol += f"👉 จะเห็นว่า {val_A:,} <b>{comp_sign}</b> {val_B:,}<br>"

                    sol += f"<b>ตอบ: {final_ans}</b></span>"
                else: # add_sub
                    op = random.choice(["+", "-"])
                    v1_maj = random.randint(3, 10)
                    v1_min = random.randint(100, 900)
                    v2_maj = random.randint(1, v1_maj-1) if op == "-" else random.randint(1, 10)
                    v2_min = random.randint(100, 900)
                    
                    if op == "-":
                        if v1_min >= v2_min:
                            v1_min, v2_min = v2_min, v1_min + 50
                            if v2_min >= 1000: v2_min = 950
                    
                    svg = draw_beakers_svg(v1_maj, v1_min, v2_maj, v2_min)
                    
                    if op == "+":
                        q = f"{svg}จากรูป ถ้านำน้ำจากทั้งสองถังมา<b>รวมกัน</b> จะได้ปริมาตรน้ำทั้งหมดเท่าไร?"
                    else:
                        q = f"{svg}จากรูป ถัง A กับถัง B มีปริมาตรน้ำ<b>ต่างกันอยู่เท่าไร</b>?"
                        
                    table_html, ans_str = generate_unit_math_html(u_major, u_minor, v1_maj, v1_min, v2_maj, v2_min, op, multiplier)
                    
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (การตั้ง{'บวก' if op=='+' else 'ลบ'}แบบข้ามหน่วย):</b><br>
                    {table_html}
                    <b>ตอบ: {ans_str}</b></span>"""

            elif actual_sub_t == "การเปรียบเทียบหน่วยการวัด และการแปลงหน่วย (มิลลิเมตร เซนติเมตร เมตร)":
                q_cat = random.choice(["compare", "add_sub"])
                selected_type = random.choice(["cm_mm", "m_cm"])
                if selected_type == "cm_mm":
                    u_major, u_minor = "เซนติเมตร", "มิลลิเมตร"
                    multiplier = 10
                else: # m_cm
                    u_major, u_minor = "เมตร", "เซนติเมตร"
                    multiplier = 100
                    
                if q_cat == "compare":
                    val_major = random.randint(5, 50) if is_challenge else random.randint(2, 20)
                    val_minor = random.randint(1, multiplier-1)
                    
                    total_minor_1 = (val_major * multiplier) + val_minor
                    case = random.choice(["greater", "less", "equal"])
                    if case == "equal":
                        total_minor_2 = total_minor_1
                    elif case == "greater":
                        total_minor_2 = total_minor_1 - random.randint(1, multiplier - 1)
                    else:
                        total_minor_2 = total_minor_1 + random.randint(1, multiplier - 1)

                    str_val_1 = f"{val_major} {u_major} {val_minor} {u_minor}"
                    str_val_2 = f"{total_minor_2:,} {u_minor}"

                    if random.choice([True, False]):
                        item_A, item_B = str_val_1, str_val_2
                        val_A, val_B = total_minor_1, total_minor_2
                    else:
                        item_A, item_B = str_val_2, str_val_1
                        val_A, val_B = total_minor_2, total_minor_1

                    if total_minor_1 == total_minor_2:
                        final_ans = "ยาวเท่ากัน"
                    else:
                        final_ans = "ยาวกว่า" if val_A > val_B else "สั้นกว่า"
                        
                    q = f"จงเติมคำว่า <b>ยาวกว่า, สั้นกว่า</b> หรือ <b>เท่ากับ</b> ลงในช่องว่างให้ถูกต้อง<br><br><span style='font-size:22px; font-weight:bold; margin-left: 20px;'>{item_A} &nbsp;&nbsp; ____________________ &nbsp;&nbsp; {item_B}</span>"

                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (การเปรียบเทียบความยาว):</b><br>
                    <b>ขั้นที่ 1: สร้างสมการแปลงหน่วยให้เหมือนกัน</b><br>
                    👉 แปลง <b>{str_val_1}</b> ให้เป็น <b>{u_minor}</b> ทั้งหมด<br>
                    👉 เนื่องจาก 1 {u_major} = {multiplier:,} {u_minor}<br>
                    👉 <b>สมการล่าสุด:</b> ({val_major} <b style='color:red;'>× {multiplier:,}</b>) + {val_minor} = {val_major * multiplier:,} + {val_minor} = <b>{total_minor_1:,} {u_minor}</b><br>
                    <b>ขั้นที่ 2: เปรียบเทียบความยาว</b><br>"""

                    if val_A == val_B:
                        sol += f"👉 จะเห็นว่า {total_minor_1:,} {u_minor} <b>เท่ากับ</b> {total_minor_2:,} {u_minor} พอดี!<br>"
                    else:
                        comp_sign = "น้อยกว่า" if val_A < val_B else "มากกว่า"
                        sol += f"👉 เปรียบเทียบ {val_A:,} {u_minor} กับ {val_B:,} {u_minor}<br>"
                        sol += f"👉 จะเห็นว่า {val_A:,} <b>{comp_sign}</b> {val_B:,}<br>"

                    sol += f"<b>ตอบ: {final_ans}</b></span>"
                else: # add_sub
                    op = random.choice(["+", "-"])
                    v1_maj = random.randint(3, 20)
                    v1_min = random.randint(1, multiplier-1)
                    v2_maj = random.randint(1, v1_maj-1) if op == "-" else random.randint(1, 20)
                    v2_min = random.randint(1, multiplier-1)
                    
                    if op == "-":
                        if v1_min >= v2_min:
                            v1_min, v2_min = v2_min, v1_min + (multiplier//2)
                            if v2_min >= multiplier: v2_min = multiplier - 1
                    
                    if op == "+":
                        q = f"สิ่งของชิ้นแรกยาว <b>{v1_maj} {u_major} {v1_min} {u_minor}</b> และชิ้นที่สองยาว <b>{v2_maj} {u_major} {v2_min} {u_minor}</b> <br>ถ้านำมาวางต่อกันจะมีความยาว<b>รวมกัน</b>เท่าไร?"
                    else:
                        q = f"สิ่งของชิ้นแรกยาว <b>{v1_maj} {u_major} {v1_min} {u_minor}</b> และชิ้นที่สองยาว <b>{v2_maj} {u_major} {v2_min} {u_minor}</b> <br>สิ่งของสองชิ้นนี้มีความยาว<b>ต่างกันอยู่เท่าไร</b>?"
                        
                    table_html, ans_str = generate_unit_math_html(u_major, u_minor, v1_maj, v1_min, v2_maj, v2_min, op, multiplier)
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (การตั้ง{'บวก' if op=='+' else 'ลบ'}แบบข้ามหน่วย):</b><br>
                    {table_html}
                    <b>ตอบ: {ans_str}</b></span>"""

            elif actual_sub_t == "การเปรียบเทียบหน่วยระยะทาง และการแปลงหน่วย (เมตร กิโลเมตร)":
                q_cat = random.choice(["compare", "add_sub"])
                u_major, u_minor = "กิโลเมตร", "เมตร"
                multiplier = 1000
                
                if q_cat == "compare":
                    val_major = random.randint(2, 20) if is_challenge else random.randint(1, 9)
                    val_minor = random.randint(50, 950)
                    
                    total_minor_1 = (val_major * multiplier) + val_minor
                    case = random.choice(["greater", "less", "equal"])
                    if case == "equal":
                        total_minor_2 = total_minor_1
                    elif case == "greater":
                        total_minor_2 = total_minor_1 - random.randint(1, multiplier - 1)
                    else:
                        total_minor_2 = total_minor_1 + random.randint(1, multiplier - 1)

                    str_val_1 = f"{val_major} {u_major} {val_minor} {u_minor}"
                    str_val_2 = f"{total_minor_2:,} {u_minor}"

                    if random.choice([True, False]):
                        item_A, item_B = str_val_1, str_val_2
                        val_A, val_B = total_minor_1, total_minor_2
                    else:
                        item_A, item_B = str_val_2, str_val_1
                        val_A, val_B = total_minor_2, total_minor_1

                    if total_minor_1 == total_minor_2:
                        final_ans = "ไกลเท่ากัน"
                    else:
                        final_ans = "ไกลกว่า" if val_A > val_B else "ใกล้กว่า"
                        
                    q = f"จงเติมคำว่า <b>ไกลกว่า, ใกล้กว่า</b> หรือ <b>เท่ากับ</b> ลงในช่องว่างให้ถูกต้อง<br><br><span style='font-size:22px; font-weight:bold; margin-left: 20px;'>{item_A} &nbsp;&nbsp; ____________________ &nbsp;&nbsp; {item_B}</span>"

                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (การเปรียบเทียบระยะทาง):</b><br>
                    <b>ขั้นที่ 1: สร้างสมการแปลงหน่วยให้เหมือนกัน</b><br>
                    👉 แปลง <b>{str_val_1}</b> ให้เป็น <b>{u_minor}</b> ทั้งหมด<br>
                    👉 เนื่องจาก 1 {u_major} = {multiplier:,} {u_minor}<br>
                    👉 <b>สมการล่าสุด:</b> ({val_major} <b style='color:red;'>× {multiplier:,}</b>) + {val_minor} = {val_major * multiplier:,} + {val_minor} = <b>{total_minor_1:,} {u_minor}</b><br>
                    <b>ขั้นที่ 2: เปรียบเทียบระยะทาง</b><br>"""

                    if val_A == val_B:
                        sol += f"👉 จะเห็นว่า {total_minor_1:,} {u_minor} <b>เท่ากับ</b> {total_minor_2:,} {u_minor} พอดี!<br>"
                    else:
                        comp_sign = "น้อยกว่า" if val_A < val_B else "มากกว่า"
                        sol += f"👉 เปรียบเทียบ {val_A:,} {u_minor} กับ {val_B:,} {u_minor}<br>"
                        sol += f"👉 จะเห็นว่า {val_A:,} <b>{comp_sign}</b> {val_B:,}<br>"

                    sol += f"<b>ตอบ: {final_ans}</b></span>"
                else: # add_sub
                    op = random.choice(["+", "-"])
                    v1_maj = random.randint(5, 50)
                    v1_min = random.randint(100, 900)
                    v2_maj = random.randint(1, v1_maj-1) if op == "-" else random.randint(1, 50)
                    v2_min = random.randint(100, 900)
                    
                    if op == "-":
                        if v1_min >= v2_min:
                            v1_min, v2_min = v2_min, v1_min + 500
                            if v2_min >= 1000: v2_min = 950
                            
                    if op == "+":
                        q = f"ระยะทาง <b>{v1_maj} {u_major} {v1_min} {u_minor}</b> กับ <b>{v2_maj} {u_major} {v2_min} {u_minor}</b> <br>ถ้านำระยะทางมา<b>รวมกัน</b> จะได้ระยะทางทั้งหมดเท่าไร?"
                    else:
                        q = f"ระยะทาง <b>{v1_maj} {u_major} {v1_min} {u_minor}</b> กับ <b>{v2_maj} {u_major} {v2_min} {u_minor}</b> <br>ระยะทางทั้งสองนี้<b>ต่างกันอยู่เท่าไร</b>?"
                        
                    table_html, ans_str = generate_unit_math_html(u_major, u_minor, v1_maj, v1_min, v2_maj, v2_min, op, multiplier)
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (การตั้ง{'บวก' if op=='+' else 'ลบ'}แบบข้ามหน่วย):</b><br>
                    {table_html}
                    <b>ตอบ: {ans_str}</b></span>"""

            elif actual_sub_t == "การเปรียบเทียบหน่วยน้ำหนัก และการแปลงหน่วย (กรัม กิโลกรัม ตัน)":
                q_cat = random.choice(["compare", "add_sub"])
                selected_type = random.choice(["kg_g", "ton_kg"])
                if selected_type == "kg_g":
                    u_major, u_minor = "กิโลกรัม", "กรัม"
                else: # ton_kg
                    u_major, u_minor = "ตัน", "กิโลกรัม"
                multiplier = 1000
                
                if q_cat == "compare":
                    val_major = random.randint(5, 50) if is_challenge else random.randint(1, 15)
                    val_minor = random.randint(50, 950)
                    
                    total_minor_1 = (val_major * multiplier) + val_minor
                    case = random.choice(["greater", "less", "equal"])
                    if case == "equal":
                        total_minor_2 = total_minor_1
                    elif case == "greater":
                        total_minor_2 = total_minor_1 - random.randint(1, multiplier - 1)
                    else:
                        total_minor_2 = total_minor_1 + random.randint(1, multiplier - 1)

                    str_val_1 = f"{val_major} {u_major} {val_minor} {u_minor}"
                    str_val_2 = f"{total_minor_2:,} {u_minor}"

                    if random.choice([True, False]):
                        item_A, item_B = str_val_1, str_val_2
                        val_A, val_B = total_minor_1, total_minor_2
                    else:
                        item_A, item_B = str_val_2, str_val_1
                        val_A, val_B = total_minor_2, total_minor_1

                    if total_minor_1 == total_minor_2:
                        final_ans = "หนักเท่ากัน"
                    else:
                        final_ans = "หนักกว่า" if val_A > val_B else "เบากว่า"
                        
                    q = f"จงเติมคำว่า <b>หนักกว่า, เบากว่า</b> หรือ <b>เท่ากับ</b> ลงในช่องว่างให้ถูกต้อง<br><br><span style='font-size:22px; font-weight:bold; margin-left: 20px;'>{item_A} &nbsp;&nbsp; ____________________ &nbsp;&nbsp; {item_B}</span>"

                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (การเปรียบเทียบน้ำหนัก):</b><br>
                    <b>ขั้นที่ 1: สร้างสมการแปลงหน่วยให้เหมือนกัน</b><br>
                    👉 แปลง <b>{str_val_1}</b> ให้เป็น <b>{u_minor}</b> ทั้งหมด<br>
                    👉 เนื่องจาก 1 {u_major} = {multiplier:,} {u_minor}<br>
                    👉 <b>สมการล่าสุด:</b> ({val_major} <b style='color:red;'>× {multiplier:,}</b>) + {val_minor} = {val_major * multiplier:,} + {val_minor} = <b>{total_minor_1:,} {u_minor}</b><br>
                    <b>ขั้นที่ 2: เปรียบเทียบน้ำหนัก</b><br>"""

                    if val_A == val_B:
                        sol += f"👉 จะเห็นว่า {total_minor_1:,} {u_minor} <b>เท่ากับ</b> {total_minor_2:,} {u_minor} พอดี!<br>"
                    else:
                        comp_sign = "น้อยกว่า" if val_A < val_B else "มากกว่า"
                        sol += f"👉 เปรียบเทียบ {val_A:,} {u_minor} กับ {val_B:,} {u_minor}<br>"
                        sol += f"👉 จะเห็นว่า {val_A:,} <b>{comp_sign}</b> {val_B:,}<br>"

                    sol += f"<b>ตอบ: {final_ans}</b></span>"
                else: # add_sub
                    op = random.choice(["+", "-"])
                    v1_maj = random.randint(5, 50)
                    v1_min = random.randint(100, 900)
                    v2_maj = random.randint(1, v1_maj-1) if op == "-" else random.randint(1, 50)
                    v2_min = random.randint(100, 900)
                    
                    if op == "-":
                        if v1_min >= v2_min:
                            v1_min, v2_min = v2_min, v1_min + 500
                            if v2_min >= 1000: v2_min = 950
                            
                    if op == "+":
                        q = f"สิ่งของชิ้นแรกหนัก <b>{v1_maj} {u_major} {v1_min} {u_minor}</b> และชิ้นที่สองหนัก <b>{v2_maj} {u_major} {v2_min} {u_minor}</b> <br>ถ้านำมาชั่ง<b>รวมกัน</b> จะได้น้ำหนักทั้งหมดเท่าไร?"
                    else:
                        q = f"สิ่งของชิ้นแรกหนัก <b>{v1_maj} {u_major} {v1_min} {u_minor}</b> และชิ้นที่สองหนัก <b>{v2_maj} {u_major} {v2_min} {u_minor}</b> <br>สิ่งของสองชิ้นนี้มีน้ำหนัก<b>ต่างกันอยู่เท่าไร</b>?"
                        
                    table_html, ans_str = generate_unit_math_html(u_major, u_minor, v1_maj, v1_min, v2_maj, v2_min, op, multiplier)
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (การตั้ง{'บวก' if op=='+' else 'ลบ'}แบบข้ามหน่วย):</b><br>
                    {table_html}
                    <b>ตอบ: {ans_str}</b></span>"""

            elif actual_sub_t == "โจทย์ปัญหาความยาว (คูณและหาร)":
                q_type = random.choice(["fit_objects", "equal_parts", "multiply_length"])
                
                if q_type == "fit_objects":
                    room = random.choice(ROOMS)
                    furn = random.choice(FURNITURE)
                    
                    if is_challenge:
                        r_m = random.randint(5, 12)
                        r_cm = random.choice([15, 35, 45, 75, 95])
                        f_m = random.randint(0, 1)
                        f_cm = random.choice([45, 65, 85, 125]) if f_m == 0 else random.choice([15, 35, 55])
                    else:
                        r_m = random.randint(3, 8)
                        r_cm = random.choice([0, 20, 50, 80])
                        f_m = random.randint(0, 1)
                        f_cm = random.choice([50, 60, 80, 100]) if f_m == 0 else random.choice([0, 20, 50])
                        
                    if f_m == 0 and f_cm < 40: f_cm = 50 
                    if f_m == 1 and f_cm == 100: f_m, f_cm = 2, 0
                    
                    room_total_cm = r_m * 100 + r_cm
                    furn_total_cm = f_m * 100 + f_cm
                    
                    count = room_total_cm // furn_total_cm
                    rem_cm = room_total_cm % furn_total_cm
                    
                    room_str = f"{r_m} เมตร {r_cm} เซนติเมตร" if r_cm > 0 else f"{r_m} เมตร"
                    furn_str = f"{f_m} เมตร {f_cm} เซนติเมตร" if f_m > 0 and f_cm > 0 else (f"{f_m} เมตร" if f_cm == 0 else f"{f_cm} เซนติเมตร")
                    
                    q = f"<b>{room}</b> มีความกว้าง {room_str} <br>ถ้าต้องการนำ <b>{furn}</b> ที่มีความกว้าง {furn_str} มาวางเรียงติดกัน <br>จะสามารถวาง{furn}ได้มากที่สุดกี่ตัว และเหลือพื้นที่ว่างกี่เซนติเมตร?"
                    
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (โจทย์ปัญหาการหาร):</b><br>
                    <b>ขั้นที่ 1: แปลงหน่วยให้เป็นเซนติเมตรทั้งหมด เพื่อให้คำนวณง่ายขึ้น</b><br>
                    👉 ความกว้างของ{room} = {r_m} เมตร {r_cm} ซม. ➔ ({r_m} × 100) + {r_cm} = <b>{room_total_cm} เซนติเมตร</b><br>
                    👉 ความกว้างของ{furn} = {f_m} เมตร {f_cm} ซม. ➔ ({f_m} × 100) + {f_cm} = <b>{furn_total_cm} เซนติเมตร</b><br>
                    <b>ขั้นที่ 2: นำความกว้างห้องมาตั้ง หารด้วยความกว้างเฟอร์นิเจอร์</b><br>
                    👉 {room_total_cm} ÷ {furn_total_cm} ได้ <b>{count}</b> เศษ <b>{rem_cm}</b><br>
                    <b>ขั้นที่ 3: สรุปคำตอบ</b><br>
                    👉 ผลหารคือจำนวน{furn}ที่สามารถจัดวางได้ = {count} ตัว<br>
                    👉 เศษที่เหลือคือพื้นที่ว่าง = {rem_cm} เซนติเมตร<br>
                    <b>ตอบ: วางได้ {count} ตัว และเหลือพื้นที่ว่าง {rem_cm} เซนติเมตร</b></span>"""

                elif q_type == "equal_parts":
                    material = random.choice(["เชือก", "ริบบิ้น", "ลวด", "ผ้า", "ไม้กระดาน"])
                    N = random.randint(3, 8) if not is_challenge else random.randint(6, 15)
                    ans_m = random.randint(0, 2)
                    ans_cm = random.randint(10, 95)
                    piece_total_cm = ans_m * 100 + ans_cm
                    
                    total_cm = piece_total_cm * N
                    tot_m = total_cm // 100
                    tot_cm = total_cm % 100
                    
                    tot_str = f"{tot_m} เมตร {tot_cm} เซนติเมตร" if tot_cm > 0 else f"{tot_m} เมตร"
                    ans_str = f"{ans_m} เมตร {ans_cm} เซนติเมตร" if ans_m > 0 else f"{ans_cm} เซนติเมตร"
                    
                    q = f"มี{material}ยาว {tot_str} <br>นำมาตัดแบ่งเป็น {N} ส่วนยาวเท่าๆ กัน <br>{material}แต่ละส่วนจะมีความยาวเท่าไร?"
                    
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (โจทย์ปัญหาการหาร):</b><br>
                    <b>ขั้นที่ 1: แปลงหน่วยเป็นเซนติเมตรเพื่อการคำนวณที่ง่ายขึ้น</b><br>
                    👉 ความยาว{material}ทั้งหมด = {tot_m} เมตร {tot_cm} ซม. ➔ ({tot_m} × 100) + {tot_cm} = <b>{total_cm} เซนติเมตร</b><br>
                    <b>ขั้นที่ 2: นำความยาวทั้งหมดมาหารด้วยจำนวนที่ต้องการแบ่ง</b><br>
                    👉 นำ {total_cm} ÷ {N} = <b>{piece_total_cm} เซนติเมตร</b><br>
                    <b>ขั้นที่ 3: แปลงหน่วยกลับเป็นเมตรและเซนติเมตร</b><br>
                    👉 {piece_total_cm} เซนติเมตร คิดเป็น <b>{ans_str}</b><br>
                    <b>ตอบ: {ans_str}</b></span>"""
                    
                elif q_type == "multiply_length":
                    furn = random.choice(FURNITURE)
                    N = random.randint(3, 9) if not is_challenge else random.randint(8, 25)
                    f_m = random.randint(0, 2)
                    f_cm = random.randint(15, 95)
                    furn_total_cm = f_m * 100 + f_cm
                    
                    total_cm = furn_total_cm * N
                    tot_m = total_cm // 100
                    tot_cm = total_cm % 100
                    
                    furn_str = f"{f_m} เมตร {f_cm} เซนติเมตร" if f_m > 0 else f"{f_cm} เซนติเมตร"
                    tot_str = f"{tot_m} เมตร {tot_cm} เซนติเมตร" if tot_cm > 0 else f"{tot_m} เมตร"
                    
                    q = f"<b>{furn}</b> 1 ตัว มีความยาว {furn_str} <br>ถ้านำ{furn}รุ่นเดียวกันจำนวน {N} ตัว มาวางต่อกันเป็นแนวยาว <br>จะมีความยาวรวมทั้งหมดกี่เมตร กี่เซนติเมตร?"
                    
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (โจทย์ปัญหาการคูณ):</b><br>
                    <b>ขั้นที่ 1: ตั้งคูณความยาวของ{furn} 1 ตัว ด้วยจำนวนตัว</b><br>
                    👉 {furn} 1 ตัว ยาว {f_m} เมตร {f_cm} เซนติเมตร นำมาคูณด้วย {N}<br>
                    👉 แยกคูณหน่วยเซนติเมตร และหน่วยเมตร<br>
                    <b>ขั้นที่ 2: คูณหน่วยเซนติเมตร</b><br>
                    👉 {f_cm} × {N} = <b>{f_cm * N} เซนติเมตร</b><br>"""
                    
                    carry_m = (f_cm * N) // 100
                    rem_cm = (f_cm * N) % 100
                    
                    if carry_m > 0:
                        sol += f"👉 เนื่องจากผลลัพธ์เกิน 100 เซนติเมตร ให้แปลงเป็นเมตร จะได้ <b>{carry_m} เมตร กับอีก {rem_cm} เซนติเมตร</b> (นำ {carry_m} เมตรไปทดไว้)<br>"
                        
                    sol += f"""<b>ขั้นที่ 3: คูณหน่วยเมตร</b><br>
                    👉 {f_m} × {N} = <b>{f_m * N} เมตร</b><br>"""
                    
                    if carry_m > 0:
                        sol += f"👉 รวมกับที่ทดมาอีก {carry_m} เมตร จะได้ {f_m * N} + {carry_m} = <b>{tot_m} เมตร</b><br>"
                        
                    sol += f"""<b>ตอบ: {tot_str}</b></span>"""

            elif actual_sub_t == "ระยะทาง (กิโลเมตรและเมตร)":
                p_names = random.sample(list(PLACE_EMOJIS.keys()), 3)
                p_emojis = [PLACE_EMOJIS[n] for n in p_names]
                
                if is_challenge:
                    q_type = random.choice(["diff", "roundtrip"])
                else:
                    q_type = random.choice(["convert_to_km", "convert_to_m", "add"])

                if q_type == "convert_to_km":
                    dist_m = random.randint(1100, 9800)
                    km = dist_m // 1000
                    m = dist_m % 1000
                    svg = draw_distance_route_svg([p_names[0], p_names[1]], [p_emojis[0], p_emojis[1]], [f"{dist_m:,} ม."])
                    q = svg + f"<br>ระยะทางจาก <b>{p_names[0]}</b> ไปถึง <b>{p_names[1]}</b> คือ {dist_m:,} เมตร<br>คิดเป็นระยะทางกี่กิโลเมตร กี่เมตร?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                    <b>ขั้นที่ 1:</b> ทบทวนความรู้: <b>1,000 เมตร = 1 กิโลเมตร</b><br>
                    <b>ขั้นที่ 2:</b> แยกตัวเลข {dist_m:,} เมตร ออกเป็นส่วนหลักพันและส่วนที่เหลือ<br>
                    👉 จะได้ {km * 1000:,} เมตร + {m} เมตร<br>
                    <b>ขั้นที่ 3:</b> แปลง {km * 1000:,} เมตร เป็น {km} กิโลเมตร<br>
                    <b>ตอบ: {km} กิโลเมตร {m} เมตร</b></span>"""
                    
                elif q_type == "convert_to_m":
                    km = random.randint(1, 9)
                    m = random.randint(50, 950)
                    total_m = (km * 1000) + m
                    svg = draw_distance_route_svg([p_names[0], p_names[1]], [p_emojis[0], p_emojis[1]], [f"{km} กม. {m} ม."])
                    q = svg + f"<br>ระยะทางจาก <b>{p_names[0]}</b> ไป <b>{p_names[1]}</b> คือ {km} กิโลเมตร {m} เมตร<br>คิดเป็นระยะทางทั้งหมดกี่เมตร?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                    <b>ขั้นที่ 1:</b> ทบทวนความรู้: <b>1 กิโลเมตร = 1,000 เมตร</b><br>
                    <b>ขั้นที่ 2:</b> แปลง {km} กิโลเมตร ให้เป็นหน่วยเมตร ➔ {km} × 1,000 = {km * 1000:,} เมตร<br>
                    <b>ขั้นที่ 3:</b> นำไปบวกกับระยะทางที่เหลืออีก {m} เมตร<br>
                    👉 {km * 1000:,} + {m} = <b>{total_m:,} เมตร</b><br>
                    <b>ตอบ: {total_m:,} เมตร</b></span>"""
                    
                elif q_type == "add":
                    km1, m1 = random.randint(1, 5), random.randint(100, 800)
                    km2, m2 = random.randint(1, 5), random.randint(100, 800)
                    total_m = m1 + m2
                    carry_km = total_m // 1000
                    rem_m = total_m % 1000
                    total_km = km1 + km2 + carry_km
                    
                    svg = draw_distance_route_svg(p_names, p_emojis, [f"{km1} กม. {m1} ม.", f"{km2} กม. {m2} ม."])
                    q = svg + f"<br>{NAMES[0]}เดินทางจาก <b>{p_names[0]}</b> ผ่าน <b>{p_names[1]}</b> เพื่อไป <b>{p_names[2]}</b> ตามแผนที่<br>รวมระยะทางทั้งหมดกี่กิโลเมตร กี่เมตร?"
                    
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                    นำระยะทางทั้งสองช่วงมาบวกกัน โดยแยกบวกหน่วยเมตรและกิโลเมตร<br>
                    <b>ขั้นที่ 1: บวกหน่วยเมตร</b><br>
                    👉 {m1} + {m2} = <b>{total_m} เมตร</b><br>"""
                    if carry_km > 0:
                        sol += f"👉 เนื่องจากเกิน 1,000 เมตร จึงปัด 1,000 เมตรเป็น 1 กิโลเมตร (เหลือ {rem_m} เมตร)<br>"
                    sol += f"""<b>ขั้นที่ 2: บวกหน่วยกิโลเมตร</b><br>
                    👉 {km1} + {km2} = {km1+km2} กิโลเมตร<br>"""
                    if carry_km > 0:
                        sol += f"👉 รวมกับที่ทดมาอีก 1 กิโลเมตร เป็น <b>{total_km} กิโลเมตร</b><br>"
                    sol += f"""<b>ตอบ: {total_km} กิโลเมตร {rem_m} เมตร</b></span>"""
                    
                elif q_type == "diff": 
                    km1, m1 = random.randint(4, 9), random.randint(100, 950)
                    km2, m2 = random.randint(1, km1-1), random.randint(100, 950)
                    
                    if m1 >= m2:
                        m1, m2 = m2, m1 + 50
                        if m2 >= 1000: m2 = 950
                        
                    dist1 = km1 * 1000 + m1
                    dist2 = km2 * 1000 + m2
                    diff = dist1 - dist2
                    diff_km = diff // 1000
                    diff_m = diff % 1000
                    
                    is_more = random.choice([True, False])
                    if is_more:
                        q_word = "ไกลกว่า"
                        sub_q = f"เส้นทางที่ 1 {q_word}เส้นทางที่ 2"
                    else:
                        q_word = "สั้นกว่า (ใกล้กว่า)"
                        sub_q = f"เส้นทางที่ 2 {q_word}เส้นทางที่ 1"
                    
                    q = f"เส้นทางที่ 1 จาก <b>{p_names[0]}</b> ไป <b>{p_names[1]}</b> ระยะทาง {km1} กิโลเมตร {m1} เมตร<br>เส้นทางที่ 2 จาก <b>{p_names[0]}</b> ไป <b>{p_names[2]}</b> ระยะทาง {km2} กิโลเมตร {m2} เมตร<br>{sub_q} อยู่กี่กิโลเมตร กี่เมตร?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (🔥 โหมดชาเลนจ์):</b><br>
                    นำระยะทางมาลบกันเพื่อหาผลต่าง โดยแยกตั้งหน่วยกิโลเมตรและเมตรให้ตรงกัน<br>
                    <b>ขั้นที่ 1: ลบหน่วยเมตร</b><br>
                    👉 นำ {m1} เมตร ลบด้วย {m2} เมตร ซึ่งตัวตั้งน้อยกว่าตัวลบ จึงลบไม่ได้<br>
                    👉 ต้องไป <b>ยืม</b> จากหน่วยกิโลเมตรมา 1 กม. (ซึ่งเท่ากับ 1,000 เมตร)<br>
                    👉 ทำให้หน่วยเมตรตัวตั้งกลายเป็น {m1} + 1,000 = {1000+m1} เมตร<br>
                    👉 นำ {1000+m1} - {m2} = <b>{diff_m} เมตร</b><br>
                    <b>ขั้นที่ 2: ลบหน่วยกิโลเมตร</b><br>
                    👉 ตัวตั้งถูกยืมไป 1 กม. จะเหลือ {km1-1} กม.<br>
                    👉 นำ {km1-1} - {km2} = <b>{diff_km} กิโลเมตร</b><br>
                    <b>ตอบ: {diff_km} กิโลเมตร {diff_m} เมตร</b></span>"""
                    
                elif q_type == "roundtrip": 
                    km, m = random.randint(2, 6), random.randint(300, 800)
                    dist_m = km * 1000 + m
                    total_m = dist_m * 2
                    tot_km = total_m // 1000
                    tot_m = total_m % 1000
                    
                    svg = draw_distance_route_svg([p_names[0], p_names[1]], [p_emojis[0], p_emojis[1]], [f"{km} กม. {m} ม."])
                    q = svg + f"<br>{NAMES[0]}ต้องเดินทางจาก <b>{p_names[0]}</b> ไป <b>{p_names[1]}</b> และเดินทางกลับตามเส้นทางเดิม<br>อยากทราบว่า{NAMES[0]}ต้องเดินทาง <b>ไป-กลับ</b> รวมระยะทางทั้งหมดกี่กิโลเมตร กี่เมตร?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (🔥 โหมดชาเลนจ์):</b><br>
                    คำว่า <b>"ไป-กลับ"</b> หมายถึงต้องเดินทาง 2 รอบ (ขาไป 1 รอบ ขากลับ 1 รอบ)<br>
                    <b>ขั้นที่ 1: นำระยะทางมาบวกกัน 2 ครั้ง (หรือคูณ 2)</b><br>
                    👉 ขาไป: {km} กม. {m} ม.<br>
                    👉 ขากลับ: {km} กม. {m} ม.<br>
                    <b>ขั้นที่ 2: รวมหน่วยเมตร</b><br>
                    👉 {m} + {m} = {m*2} เมตร<br>"""
                    if m*2 >= 1000:
                        sol += f"👉 แปลงหน่วย: {m*2} เมตร คิดเป็น 1 กิโลเมตร กับ {tot_m} เมตร<br>"
                    sol += f"""<b>ขั้นที่ 3: รวมหน่วยกิโลเมตร</b><br>
                    👉 {km} + {km} = {km*2} กิโลเมตร<br>"""
                    if m*2 >= 1000:
                        sol += f"👉 นำไปบวกกับที่ทดมาอีก 1 กม. จะได้ <b>{tot_km} กิโลเมตร</b><br>"
                    sol += f"""<b>ตอบ: {tot_km} กิโลเมตร {tot_m} เมตร</b></span>"""

            elif actual_sub_t == "การบอกเวลาเป็นนาฬิกาและนาที":
                h_24 = random.randint(0, 23)
                m = random.randint(0, 59)
                period = "เวลากลางวัน" if 6 <= h_24 <= 17 else "เวลากลางคืน"
                
                q = draw_clock_svg(h_24, m) + f"<br>จากรูปนาฬิกาด้านบน (กำหนดเป็น<b>{period}</b>) อ่านเวลาได้ว่าอย่างไร?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                <b>ขั้นที่ 1: ดูเข็มสั้น (สีแดง) เพื่อบอกนาฬิกา</b><br>
                👉 เข็มสั้นชี้ที่เลข {h_24 % 12 if h_24 % 12 != 0 else 12} แต่โจทย์กำหนดเป็น <b>{period}</b> จึงอ่านค่าเป็น <b>{h_24:02d} นาฬิกา</b><br>
                <b>ขั้นที่ 2: ดูเข็มยาว (สีฟ้า) เพื่อบอกนาที</b><br>
                👉 เข็มยาวชี้เลยตัวเลขหลักมาอยู่ที่ขีดที่ {m} (นำช่องละ 5 นาทีมาบวกกัน) จึงอ่านค่าเป็น <b>{m:02d} นาที</b><br>
                <b>ขั้นที่ 3: นำมาอ่านรวมกัน</b><br>
                👉 จะได้ <b>{h_24:02d} นาฬิกา {m:02d} นาที</b><br>
                <b>ตอบ: {h_24:02d}:{m:02d} น. หรือ {h_24} นาฬิกา {m} นาที</b></span>"""

            elif actual_sub_t == "การอ่านน้ำหนักจากเครื่องชั่งสปริง":
                kg = random.randint(0, 4)
                kheed = random.randint(1, 9)
                g = kheed * 100
                
                q = draw_scale_svg(kg, kheed) + "<br>จากรูป เครื่องชั่งสปริงแสดงน้ำหนักเท่าไร? (ตอบเป็นกิโลกรัมและกรัม)"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                <b>ขั้นที่ 1: ดูเข็มชี้ตัวเลขหลัก (กิโลกรัม)</b><br>
                👉 เข็มสีแดงชี้เลยเลข <b>{kg}</b> มาแล้ว แปลว่ามีน้ำหนักหลักคือ <b>{kg} กิโลกรัม</b><br>
                <b>ขั้นที่ 2: นับขีดย่อย (1 ขีด = 100 กรัม)</b><br>
                👉 เข็มชี้เลยเลข {kg} ไป <b>{kheed} ขีดย่อย</b><br>
                👉 แปลงหน่วยขีดเป็นหน่วยกรัม: นำ {kheed} ขีด × 100 = <b>{g} กรัม</b><br>
                <b>ขั้นที่ 3: นำน้ำหนักมารวมกัน</b><br>
                👉 นำกิโลกรัมและกรัมมาต่อกัน ➔ <b>{kg} กิโลกรัม {g} กรัม</b><br>
                <b>ตอบ: {kg} กิโลกรัม {g} กรัม</b></span>"""

            elif actual_sub_t == "การอ่านความยาวจากไม้บรรทัด":
                if grade == "ป.3":
                    if is_challenge:
                        len_a = round(random.uniform(110.0, 350.0), 1)
                        len_b = round(random.uniform(110.0, 350.0), 1)
                        while abs(len_a - len_b) < 1.0: 
                            len_b = round(random.uniform(110.0, 350.0), 1)
                        
                        name_a, color_a = "สิ่งของ A", "#f1c40f"
                        name_b, color_b = "สิ่งของ B", "#3498db"
                        
                        svg_a = draw_long_ruler_svg(len_a, color_a, name_a)
                        svg_b = draw_long_ruler_svg(len_b, color_b, name_b)
                        
                        str_a = cm_to_m_cm_mm(len_a)
                        str_b = cm_to_m_cm_mm(len_b)
                        
                        is_ask_more = random.choice([True, False])
                        if is_ask_more:
                            compare_word = "มากกว่า"
                            if len_a > len_b:
                                target_name, other_name = name_a, name_b
                                diff_len = len_a - len_b
                            else:
                                target_name, other_name = name_b, name_a
                                diff_len = len_b - len_a
                        else:
                            compare_word = "น้อยกว่า"
                            if len_a < len_b:
                                target_name, other_name = name_a, name_b
                                diff_len = len_b - len_a
                            else:
                                target_name, other_name = name_b, name_a
                                diff_len = len_a - len_b
                                
                        diff_str = cm_to_m_cm_mm(diff_len)
                        
                        q = f"สายวัดด้านล่างแสดงตำแหน่งส่วนปลายของสิ่งของ 2 ชิ้น (เริ่มวัดจาก 0 เสมอ)<br>{svg_a}{svg_b}จงหาว่าสิ่งของใดมีความยาว<b>{compare_word}กัน</b> และ{compare_word}กันอยู่เท่าไร? <br>(ตอบในหน่วย เมตร เซนติเมตร มิลลิเมตร)"
                        
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (🔥 โหมดชาเลนจ์ ป.3):</b><br>
                        <b>ขั้นที่ 1: อ่านความยาวของแต่ละสิ่งของ</b><br>
                        👉 {name_a} จุดปลายอยู่ที่ {len_a} ซม. คิดเป็น <b>{str_a}</b><br>
                        👉 {name_b} จุดปลายอยู่ที่ {len_b} ซม. คิดเป็น <b>{str_b}</b><br>
                        <b>ขั้นที่ 2: เปรียบเทียบความยาว</b><br>
                        👉 จะเห็นได้ชัดเจนว่า <b>{target_name}</b> มีความยาว{compare_word}<br>
                        <b>ขั้นที่ 3: หาผลต่าง (ตั้งลบความยาว)</b><br>
                        👉 นำ {max(len_a, len_b):.1f} - {min(len_a, len_b):.1f} = <b>{diff_len:.1f} ซม.</b><br>
                        👉 แปลงผลลัพธ์เป็นหน่วยผสม: {diff_len:.1f} ซม. คิดเป็น <b>{diff_str}</b><br>
                        <b>ตอบ: {target_name} {compare_word}อยู่ {diff_str}</b></span>"""
                        
                    else:
                        len_a = round(random.uniform(110.0, 350.0), 1)
                        svg = draw_long_ruler_svg(len_a, "#f1c40f", "สิ่งของ (เริ่มวัดจาก 0)")
                        str_a = cm_to_m_cm_mm(len_a)
                        
                        q = f"จากรูป สายวัดแสดงตำแหน่งส่วนปลายของสิ่งของ (โดยเริ่มวัดจาก 0 เสมอ)<br>{svg}จงหาว่าสิ่งของนี้ยาวเท่าไร? <br>(ตอบในหน่วย เมตร เซนติเมตร มิลลิเมตร)"
                        
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                        <b>ขั้นที่ 1: อ่านค่าจากสายวัด</b><br>
                        👉 จุดปลายชี้ที่ <b>{len_a}</b> เซนติเมตร (หรือ {int(len_a)} ซม. กับอีก {int(round((len_a-int(len_a))*10))} มม.)<br>
                        <b>ขั้นที่ 2: แปลงหน่วยเป็น เมตร เซนติเมตร มิลลิเมตร</b><br>
                        👉 ความรู้: 100 เซนติเมตร = 1 เมตร<br>
                        👉 ดังนั้น {len_a} ซม. สามารถแบ่งเป็น เมตร และ เซนติเมตร ได้เป็น <b>{str_a}</b><br>
                        <b>ตอบ: {str_a}</b></span>"""
                else:
                    if is_challenge:
                        start_cm = random.randint(1, 4) + (random.randint(0, 9) * 0.1)
                    else:
                        start_cm = 0.0
                    
                    length_cm = random.randint(3, 8) + (random.randint(0, 9) * 0.1)
                    end_cm = start_cm + length_cm
                    
                    ans_cm = int(length_cm)
                    ans_mm = int(round((length_cm - ans_cm) * 10))
                    
                    q = draw_ruler_svg(start_cm, end_cm) + "<br>จากรูป สิ่งของมีความยาวกี่เซนติเมตร กี่มิลลิเมตร?"
                    
                    if start_cm == 0.0:
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                        <b>ขั้นที่ 1:</b> สังเกตว่าสิ่งของเริ่มวัดจากขีด 0 พอดี จึงสามารถอ่านค่าที่จุดปลายได้เลย<br>
                        <b>ขั้นที่ 2:</b> จุดปลายชี้ที่ <b>{int(end_cm)}</b> เซนติเมตร กับอีก <b>{int(round((end_cm - int(end_cm)) * 10))}</b> มิลลิเมตร (ขีดเล็ก)<br>
                        <b>ตอบ: {ans_cm} เซนติเมตร {ans_mm} มิลลิเมตร</b></span>"""
                    else:
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (🔥 โหมดชาเลนจ์):</b><br>
                        <b>ขั้นที่ 1:</b> สิ่งของไม่ได้เริ่มวัดจาก 0 จึงต้องนำ <b>จุดปลาย - จุดเริ่มต้น</b><br>
                        <b>ขั้นที่ 2:</b> จุดปลายชี้ที่ {end_cm:.1f} ซม. และจุดเริ่มต้นอยู่ที่ {start_cm:.1f} ซม.<br>
                        <b>ขั้นที่ 3:</b> คำนวณ {end_cm:.1f} - {start_cm:.1f} = <b>{length_cm:.1f} ซม.</b><br>
                        <b>ขั้นที่ 4:</b> แปลงความยาวที่ได้: {length_cm:.1f} ซม. คือ {ans_cm} เซนติเมตร กับ {ans_mm} มิลลิเมตร<br>
                        <b>ตอบ: {ans_cm} เซนติเมตร {ans_mm} มิลลิเมตร</b></span>"""

            elif actual_sub_t == "การอ่านแผนภูมิรูปภาพ":
                item_keys = list(FRUIT_EMOJIS.keys())
                item = random.choice(item_keys)
                emoji = FRUIT_EMOJIS[item]
                pic_val = random.choice([2, 5, 10]) * (5 if is_challenge else 1)
                
                q_type = random.choice(["single", "total", "diff"])
                pic_html, days, counts = draw_complex_pictogram_html(item, emoji, pic_val)
                
                if q_type == "single":
                    ask_idx = random.randint(0, 2)
                    ans = counts[ask_idx] * pic_val
                    q = pic_html + f"<br>จากแผนภูมิรูปภาพ ใน<b>วัน{days[ask_idx]}</b> ขาย{item}ได้กี่ผล?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                    <b>ขั้นที่ 1:</b> ดูในตารางวัน{days[ask_idx]} มีรูป {emoji} ทั้งหมด {counts[ask_idx]} รูป<br>
                    <b>ขั้นที่ 2:</b> กำหนดให้ 1 รูป = {pic_val} ผล<br>
                    <b>ขั้นที่ 3:</b> นำ {counts[ask_idx]} รูป × {pic_val} = <b>{ans} ผล</b><br>
                    <b>ตอบ: {ans} ผล</b></span>"""
                elif q_type == "total":
                    total_counts = sum(counts)
                    ans = total_counts * pic_val
                    q = pic_html + f"<br>จากแผนภูมิรูปภาพ รวมทั้ง 3 วัน ขาย{item}ได้ทั้งหมดกี่ผล?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                    <b>ขั้นที่ 1:</b> นับจำนวนรูป {emoji} ทั้ง 3 วันรวมกัน จะได้ {total_counts} รูป<br>
                    <b>ขั้นที่ 2:</b> กำหนดให้ 1 รูป = {pic_val} ผล<br>
                    <b>ขั้นที่ 3:</b> นำ {total_counts} รูป × {pic_val} = <b>{ans} ผล</b><br>
                    <b>ตอบ: {ans} ผล</b></span>"""
                else:
                    d1, d2 = random.sample([0, 1, 2], 2)
                    if counts[d1] < counts[d2]: d1, d2 = d2, d1 
                    diff_counts = counts[d1] - counts[d2]
                    ans = diff_counts * pic_val
                    
                    is_more = random.choice([True, False])
                    if is_more:
                        compare_word = "มากกว่า"
                        q = pic_html + f"<br>จากแผนภูมิรูปภาพ วัน{days[d1]} ขาย{item}ได้<b>{compare_word}</b>วัน{days[d2]} กี่ผล?"
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                        <b>ขั้นที่ 1:</b> วัน{days[d1]} มีรูป {emoji} {counts[d1]} รูป ส่วนวัน{days[d2]} มี {counts[d2]} รูป<br>
                        <b>ขั้นที่ 2:</b> หาผลต่างของจำนวนรูป: {counts[d1]} - {counts[d2]} = {diff_counts} รูป<br>
                        <b>ขั้นที่ 3:</b> นำผลต่างของรูป × {pic_val} ผล ➔ {diff_counts} × {pic_val} = <b>{ans} ผล</b><br>
                        <b>ตอบ: {ans} ผล</b></span>"""
                    else:
                        compare_word = "น้อยกว่า"
                        q = pic_html + f"<br>จากแผนภูมิรูปภาพ วัน{days[d2]} ขาย{item}ได้<b>{compare_word}</b>วัน{days[d1]} กี่ผล?"
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                        <b>ขั้นที่ 1:</b> วัน{days[d2]} มีรูป {emoji} {counts[d2]} รูป ส่วนวัน{days[d1]} มี {counts[d1]} รูป<br>
                        <b>ขั้นที่ 2:</b> หาผลต่างของจำนวนรูป: {counts[d1]} - {counts[d2]} = {diff_counts} รูป<br>
                        <b>ขั้นที่ 3:</b> นำผลต่างของรูป × {pic_val} ผล ➔ {diff_counts} × {pic_val} = <b>{ans} ผล</b><br>
                        <b>ตอบ: {ans} ผล</b></span>"""

            else:
                q = f"⚠️ [ระบบผิดพลาด] ไม่พบเงื่อนไขสำหรับหัวข้อ: <b>{actual_sub_t}</b>"
                sol = "Error"

            # ตรวจสอบการซ้ำของโจทย์
            if q not in seen: 
                seen.add(q)
                questions.append({"question": q, "solution": sol})
                break 
            elif attempts >= 499:
                questions.append({"question": q, "solution": sol})
                break
            
    return questions

# ==========================================
# UI Rendering
# ==========================================
def extract_body(html_str):
    try: return html_str.split('<body>')[1].split('</body>')[0]
    except IndexError: return html_str

def create_page(grade, sub_t, questions, is_key=False, q_margin="20px", ws_height="180px", brand_name=""):
    title = "เฉลยแบบฝึกหัด (Answer Key)" if is_key else "แบบฝึกหัดคณิตศาสตร์"
    student_info = """
        <table style="width: 100%; margin-bottom: 10px; font-size: 18px; border-collapse: collapse;">
            <tr>
                <td style="width: 1%; white-space: nowrap; padding-right: 5px;"><b>ชื่อ-สกุล</b></td>
                <td style="border-bottom: 2px dotted #999; width: 60%;"></td>
                <td style="width: 1%; white-space: nowrap; padding-left: 20px; padding-right: 5px;"><b>ชั้น</b></td>
                <td style="border-bottom: 2px dotted #999; width: 15%;"></td>
                <td style="width: 1%; white-space: nowrap; padding-left: 20px; padding-right: 5px;"><b>เลขที่</b></td>
                <td style="border-bottom: 2px dotted #999; width: 15%;"></td>
            </tr>
        </table>
        """ if not is_key else ""
        
    html = f"""<!DOCTYPE html><html lang="th"><head><meta charset="utf-8">
    <style>
        @page {{ size: A4; margin: 15mm; }}
        body {{ font-family: 'Sarabun', sans-serif; padding: 20px; line-height: 1.6; color: #333; }}
        .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 10px; padding-bottom: 10px; }}
        .q-box {{ margin-bottom: {q_margin}; padding: 10px 15px; page-break-inside: avoid; font-size: 20px; line-height: 1.6; }}
        .workspace {{ height: {ws_height}; border: 2px dashed #bdc3c7; border-radius: 8px; margin: 15px 0; padding: 10px; color: #95a5a6; font-size: 16px; background-color: #fafbfc; }}
        .ans-line {{ margin-top: 10px; border-bottom: 1px dotted #999; width: 80%; height: 30px; font-weight: bold; font-size: 20px; display: flex; align-items: flex-end; padding-bottom: 5px; }}
        .sol-text {{ color: #333; font-size: 18px; display: block; margin-top: 15px; padding: 15px; background-color: #f1f8ff; border-left: 4px solid #3498db; border-radius: 4px; line-height: 1.6; }}
        .page-footer {{ text-align: right; font-size: 14px; color: #95a5a6; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }}
    </style></head><body>
    <div class="header"><h2>{title} - {grade}</h2><p><b>หมวดหมู่:</b> {sub_t}</p></div>
    {student_info}"""
    
    for i, item in enumerate(questions, 1):
        html += f'<div class="q-box"><b>ข้อที่ {i}.</b> '
        if is_key:
            if "(แบบตั้งหลัก)" in sub_t or "หารยาว" in sub_t or "การคูณทศนิยม" in sub_t or "การบวกและการลบทศนิยม" in sub_t: 
                html += f'{item["solution"]}'
            else: 
                html += f'{item["question"]}<div class="sol-text">{item["solution"]}</div>'
        else:
            html += f'{item["question"]}<div class="workspace">พื้นที่สำหรับแสดงวิธีทำอย่างละเอียด...</div><div class="ans-line">ตอบ: </div>'
        html += '</div>'
        
    if brand_name: 
        html += f'<div class="page-footer">&copy; 2026 {brand_name} | สงวนลิขสิทธิ์</div>'
        
    return html + "</body></html>"

# ==========================================
# 4. Streamlit UI (Sidebar & Result Grouping)
# ==========================================
st.sidebar.markdown("## ⚙️ พารามิเตอร์การสร้าง")

selected_grade = st.sidebar.selectbox("📚 เลือกระดับชั้น:", ["ป.1", "ป.2", "ป.3", "ป.4", "ป.5", "ป.6"])
main_topics_list = list(curriculum_db[selected_grade].keys())
main_topics_list.append("🌟 โหมดพิเศษ (สุ่มทุกเรื่อง)")

selected_main = st.sidebar.selectbox("📂 เลือกหัวข้อหลัก:", main_topics_list)

if selected_main == "🌟 โหมดพิเศษ (สุ่มทุกเรื่อง)":
    selected_sub = "แบบทดสอบรวมปลายภาค"
    st.sidebar.info("💡 โหมดนี้จะสุ่มดึงโจทย์จากทุกเรื่องในชั้นเรียนนี้มายำรวมกัน")
else:
    selected_sub = st.sidebar.selectbox("📝 เลือกหัวข้อย่อย:", curriculum_db[selected_grade][selected_main])

num_input = st.sidebar.number_input("🔢 จำนวนข้อ:", min_value=1, max_value=100, value=10)

st.sidebar.markdown("---")
is_challenge = st.sidebar.toggle("🔥 โหมดชาเลนจ์ (ท้าทาย)", value=False)

if is_challenge:
    st.markdown("""
    <script>
        const header = window.parent.document.querySelector('.main-header');
        if(header) { header.classList.add('challenge'); header.querySelector('span').innerText = '🔥 โหมดท้าทาย (Challenge)'; header.querySelector('span').style.background = '#e74c3c'; header.querySelector('span').style.color = '#fff'; }
    </script>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <script>
        const header = window.parent.document.querySelector('.main-header');
        if(header) { header.classList.remove('challenge'); header.querySelector('span').innerText = 'Standard Edition'; header.querySelector('span').style.background = '#f39c12'; header.querySelector('span').style.color = '#fff'; }
    </script>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📏 ตั้งค่าหน้ากระดาษ")
spacing_level = st.sidebar.select_slider(
    "↕️ ความสูงของพื้นที่ทดเลข:", 
    options=["แคบ", "ปานกลาง", "กว้าง", "กว้างพิเศษ"], 
    value="ปานกลาง"
)

if spacing_level == "แคบ": q_margin, ws_height = "15px", "100px"
elif spacing_level == "ปานกลาง": q_margin, ws_height = "20px", "180px"
elif spacing_level == "กว้าง": q_margin, ws_height = "30px", "280px"
else: q_margin, ws_height = "40px", "400px"

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 ตั้งค่าแบรนด์")
brand_name = st.sidebar.text_input("🏷️ ชื่อแบรนด์ / ผู้สอน:", value="บ้านทีเด็ด")

if st.sidebar.button("🚀 สั่งสร้างใบงานเดี๋ยวนี้", type="primary", use_container_width=True):
    with st.spinner("กำลังออกแบบรูปภาพและสร้างเฉลยแบบ Step-by-Step..."):
        
        qs = generate_questions_logic(selected_grade, selected_main, selected_sub, num_input, is_challenge)
        
        html_w = create_page(selected_grade, selected_sub, qs, is_key=False, q_margin=q_margin, ws_height=ws_height, brand_name=brand_name)
        html_k = create_page(selected_grade, selected_sub, qs, is_key=True, q_margin=q_margin, ws_height=ws_height, brand_name=brand_name)
        
        st.session_state['worksheet_html'] = html_w
        st.session_state['answerkey_html'] = html_k
        
        ebook_body = f'\n<div class="a4-wrapper">{extract_body(html_w)}</div>\n<div class="a4-wrapper">{extract_body(html_k)}</div>\n'
        
        full_ebook_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap" rel="stylesheet"><style>@page {{ size: A4; margin: 15mm; }} @media screen {{ body {{ font-family: 'Sarabun', sans-serif; background-color: #525659; display: flex; flex-direction: column; align-items: center; padding: 40px 0; margin: 0; }} .a4-wrapper {{ width: 210mm; min-height: 297mm; background: white; margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.3); padding: 15mm; box-sizing: border-box; }} }} @media print {{ body {{ font-family: 'Sarabun', sans-serif; background: transparent; padding: 0; display: block; margin: 0; }} .a4-wrapper {{ width: 100%; min-height: auto; margin: 0; padding: 0; box-shadow: none; page-break-after: always; }} }} .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 10px; padding-bottom: 10px; }} .q-box {{ margin-bottom: {q_margin}; padding: 10px 15px; page-break-inside: avoid; font-size: 20px; line-height: 1.6; }} .workspace {{ height: {ws_height}; border: 2px dashed #bdc3c7; border-radius: 8px; margin: 15px 0; padding: 10px; color: #95a5a6; font-size: 16px; background-color: #fafbfc; }} .ans-line {{ margin-top: 10px; border-bottom: 1px dotted #999; width: 80%; height: 30px; font-weight: bold; font-size: 20px; display: flex; align-items: flex-end; padding-bottom: 5px; }} .sol-text {{ color: #333; font-size: 18px; display: block; margin-top: 15px; padding: 15px; background-color: #f1f8ff; border-left: 4px solid #3498db; border-radius: 4px; line-height: 1.6; }} .page-footer {{ text-align: right; font-size: 14px; color: #95a5a6; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }} </style></head><body>{ebook_body}</body></html>"""

        filename_base = f"Std_{selected_grade}_{selected_sub}"
        st.session_state['ebook_html'] = full_ebook_html
        st.session_state['filename_base'] = f"{filename_base}_{int(time.time())}"
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(f"{filename_base}_Full_EBook.html", full_ebook_html.encode('utf-8'))
            zip_file.writestr(f"{filename_base}_Worksheet.html", html_w.encode('utf-8'))
            zip_file.writestr(f"{filename_base}_AnswerKey.html", html_k.encode('utf-8'))
        st.session_state['zip_data'] = zip_buffer.getvalue()

if 'ebook_html' in st.session_state:
    st.success(f"✅ โค้ดฉบับสมบูรณ์ 100% ไร้ข้อผิดพลาด! ย้อนกลับหน้าตาแอปพลิเคชันเป็น Math Worksheet Pro (ป.1 - ป.6) และเปลี่ยนโจทย์จากเครื่องหมายเป็นคำว่า 'รวมกัน / ต่างกัน' ตามที่คุณครูต้องการครบถ้วนครับ")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📄 โหลดเฉพาะโจทย์", data=st.session_state['worksheet_html'], file_name=f"{st.session_state['filename_base']}_Worksheet.html", mime="text/html", use_container_width=True)
        st.download_button("🔑 โหลดเฉพาะเฉลย", data=st.session_state['answerkey_html'], file_name=f"{st.session_state['filename_base']}_AnswerKey.html", mime="text/html", use_container_width=True)
    with c2:
        st.download_button("📚 โหลดรวมเล่ม E-Book", data=st.session_state['ebook_html'], file_name=f"{st.session_state['filename_base']}_Full_EBook.html", mime="text/html", use_container_width=True)
        st.download_button("🗂️ โหลดแพ็กเกจ (.zip)", data=st.session_state['zip_data'], file_name=f"{st.session_state['filename_base']}.zip", mime="application/zip", use_container_width=True)
    st.markdown("---")
    components.html(st.session_state['ebook_html'], height=800, scrolling=True)
