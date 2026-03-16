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
    .main-header { background: linear-gradient(135deg, #2980b9, #2c3e50); padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem; box-shadow: 0 10px 20px rgba(0,0,0,0.15); }
    .main-header h1 { margin: 0; font-size: 2.8rem; font-weight: 800; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
    .main-header p { margin: 10px 0 0 0; font-size: 1.2rem; opacity: 0.9; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🚀 Math Worksheet Pro <span style="font-size: 20px; background: #f39c12; padding: 5px 15px; border-radius: 20px; vertical-align: middle;">Standard Edition</span></h1>
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
PUBLISHERS = ["สำพิมพ์", "โรงพิมพ์", "ฝ่ายวิชาการ", "ร้านถ่ายเอกสาร", "ทีมงานจัดทำเอกสาร", "บริษัทสิ่งพิมพ์"]
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

box_html = "<span style='display: inline-block; width: 22px; height: 22px; border: 2px solid #333; border-radius: 3px; vertical-align: middle; margin-left: 5px; position: relative; top: -2px;'></span>"

def f_html(n, d, c="#2c3e50", b=True):
    w = "bold" if b else "normal"
    return f"<span style='display:inline-flex; flex-direction:column; vertical-align:middle; text-align:center; line-height:1.4; margin:0 4px;'><span style='border-bottom:2px solid {c}; padding:0 4px; font-weight:{w}; color:{c};'>{n}</span><span style='padding:0 4px; font-weight:{w}; color:{c};'>{d}</span></span>"

def get_vertical_fraction(num, den, color="#c0392b", is_bold=True):
    weight = "bold" if is_bold else "normal"
    return f"""<span style="display:inline-flex; flex-direction:column; vertical-align:middle; text-align:center; line-height:1.4; margin: 0 6px; font-family:'Sarabun', sans-serif; white-space: nowrap;"><span style="border-bottom: 2px solid {color}; padding: 2px 6px; font-weight:{weight}; color:{color};">{num}</span><span style="padding: 2px 6px; font-weight:{weight}; color:{color};">{den}</span></span>"""

def get_vertical_math(top_chars, bottom_chars, result_chars, operator="+"):
    max_len = max(len(top_chars), len(bottom_chars), len(result_chars))
    top_padded = [""] * (max_len - len(top_chars)) + top_chars
    bot_padded = [""] * (max_len - len(bottom_chars)) + bottom_chars
    res_padded = [""] * (max_len - len(result_chars)) + result_chars
    
    html = "<table style='border-collapse: collapse; font-size: 26px; font-weight: bold; text-align: center; margin: 15px 0 15px 40px;'>"
    html += "<tr>"
    for char in top_padded: html += f"<td style='padding: 5px 12px; width: 35px;'>{char}</td>"
    html += f"<td rowspan='2' style='padding-left: 20px; vertical-align: middle; font-size: 28px; color: #2c3e50;'>{operator}</td></tr><tr>"
    for char in bot_padded: html += f"<td style='padding: 5px 12px; width: 35px; border-bottom: 2px solid #333;'>{char}</td>"
    html += "</tr><tr>"
    for char in res_padded: html += f"<td style='padding: 5px 12px; width: 35px; border-bottom: 4px double #333;'>{char}</td>"
    html += "<td></td></tr></table>"
    return html

def generate_vertical_table_html(a, b, op, result="", is_key=False):
    ans_html = f"<br><span style='text-decoration: underline double;'>{result}</span>" if is_key else "<br>___"
    return f"<div style='margin-left: 30px; font-family: monospace; font-size: 24px; text-align: right; width: 100px;'>{a}<br>{op} {b}<hr style='margin: 5px 0;'>{result if is_key else ''}</div>"

def generate_mixed_number_html(whole, num, den):
    return f"<span style='font-size: 24px; vertical-align: middle;'>{whole}</span> {f_html(num, den)}"

def lcm_multiple(*args):
    res = args[0]
    for i in args[1:]: res = abs(res * i) // math.gcd(res, i)
    return res

# ==========================================
# 🌟 ฟังก์ชันวาดรูปภาพ SVG 🌟
# ==========================================
def draw_ruler_svg(start_cm, end_cm):
    scale = 40  # 1 cm = 40 pixels
    max_cm = max(10, math.ceil(end_cm) + 1)
    width = max_cm * scale + 60
    height = 140

    svg = f'<div style="text-align:center; margin: 15px 0;"><svg width="{width}" height="{height}">'
    
    # วาดดินสอ
    obj_x = 30 + (start_cm * scale)
    obj_w = (end_cm - start_cm) * scale
    tip_len = min(20, obj_w / 3) 
    
    svg += f'<rect x="{obj_x}" y="20" width="{obj_w - tip_len}" height="24" fill="#f1c40f" stroke="#d35400" stroke-width="2" rx="2"/>'
    svg += f'<polygon points="{obj_x + obj_w - tip_len},20 {obj_x + obj_w - tip_len},44 {obj_x + obj_w},32" fill="#34495e"/>'
    
    # เส้นไกด์ไลน์ประ
    svg += f'<line x1="{obj_x}" y1="44" x2="{obj_x}" y2="70" stroke="#e74c3c" stroke-width="2" stroke-dasharray="4,4"/>'
    svg += f'<line x1="{obj_x + obj_w}" y1="32" x2="{obj_x + obj_w}" y2="70" stroke="#e74c3c" stroke-width="2" stroke-dasharray="4,4"/>'

    # วาดไม้บรรทัด
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

def draw_cars_svg(colors):
    svg = '<div style="text-align:center; margin: 15px 0;"><svg width="400" height="80">'
    for i, c in enumerate(colors):
        cx = 50 + i * 100
        svg += f'<rect x="{cx-35}" y="20" width="70" height="30" fill="{c}" rx="8" stroke="#333" stroke-width="2"/>'
        svg += f'<rect x="{cx-20}" y="10" width="40" height="15" fill="#ecf0f1" stroke="#333" stroke-width="2"/>'
        svg += f'<circle cx="{cx-20}" cy="50" r="10" fill="#333"/>'
        svg += f'<circle cx="{cx+20}" cy="50" r="10" fill="#333"/>'
    svg += '</svg></div>'
    return svg

def draw_square_svg(side):
    svg = '<div style="text-align:center; margin: 15px 0;"><svg width="160" height="160">'
    svg += '<rect x="30" y="30" width="100" height="100" fill="#e8f8f5" stroke="#16a085" stroke-width="3"/>'
    svg += f'<text x="80" y="20" font-family="Sarabun" font-size="16" font-weight="bold" fill="#333" text-anchor="middle">{side} ซม.</text>'
    svg += f'<text x="140" y="80" font-family="Sarabun" font-size="16" font-weight="bold" fill="#333" text-anchor="start" dominant-baseline="central">{side} ซม.</text>'
    svg += '</svg></div>'
    return svg

def draw_angle_svg(angle):
    cx, cy, r = 100, 120, 80
    rad = math.radians(angle)
    x2, y2 = cx + r * math.cos(math.pi - rad), cy - r * math.sin(math.pi - rad)
    svg = '<div style="text-align:center; margin: 15px 0;"><svg width="220" height="150">'
    svg += f'<line x1="{cx}" y1="{cy}" x2="{cx+r+20}" y2="{cy}" stroke="#2c3e50" stroke-width="4" stroke-linecap="round"/>'
    svg += f'<line x1="{cx}" y1="{cy}" x2="{x2}" y2="{y2}" stroke="#2c3e50" stroke-width="4" stroke-linecap="round"/>'
    svg += f'<path d="M {cx+30} {cy} A 30 30 0 0 0 {cx + 30*math.cos(math.pi-rad)} {cy - 30*math.sin(math.pi-rad)}" fill="none" stroke="#e74c3c" stroke-width="3"/>'
    svg += f'<text x="{cx+45}" y="{cy-15}" font-family="Sarabun" font-size="16" font-weight="bold" fill="#e74c3c">{angle}&deg;</text>'
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
        <div style="text-align: center; background-color: #ecf0f1; padding: 10px; font-weight: bold; border-bottom: 2px solid #34495e; font-size: 20px;">
            จำนวน{item}ที่ขายได้
        </div>
        <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 24px;">
    """
    for d, c in zip(days, counts):
        icons = "".join([f"<span style='margin: 0 4px;'>{emoji}</span>"] * c)
        html += f'<tr><td style="padding: 10px; border-bottom: 1px solid #eee; width: 30%; border-right: 2px solid #34495e; text-align: center;"><b>วัน{d}</b></td><td style="padding: 10px; border-bottom: 1px solid #eee; text-align: left; padding-left: 20px;">{icons}</td></tr>'
        
    html += f"""
        </table>
        <div style="background-color: #fdf2e9; padding: 10px; text-align: center; font-size: 18px; color: #d35400; font-weight: bold; border-top: 2px solid #34495e;">
            กำหนดให้ {emoji} 1 รูป แทนจำนวน {pic_val} ผล
        </div>
    </div>
    """
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
        if mode == "ห.ร.ม.":
            return f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br><b>ขั้นที่ 1:</b> ลองหาตัวเลขที่สามารถหารทั้ง {a} และ {b} ลงตัวพร้อมกัน<br><b>ขั้นที่ 2:</b> พบว่าไม่มีตัวเลขใดเลยที่หารทั้งคู่ลงตัวได้ (นอกจากเลข 1)<br><b>ดังนั้น ห.ร.ม. = 1</b></span>"
        else:
            return f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br><b>ขั้นที่ 1:</b> ลองหาตัวเลขที่สามารถหารทั้ง {a} และ {b} ลงตัวพร้อมกัน<br><b>ขั้นที่ 2:</b> พบว่าไม่มีตัวเลขใดเลยที่หารทั้งคู่ลงตัว<br><b>ขั้นที่ 3:</b> การหา ค.ร.น. ในกรณีนี้ ให้นำตัวเลขทั้งสองตัวมาคูณกันได้เลย<br><b>ดังนั้น ค.ร.น. = {a} × {b} = {a*b}</b></span>"
            
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
        
    return f"""<div style="display: block; text-align: center; margin-top: 10px;"><div style="display: inline-block; font-family: 'Sarabun', sans-serif; font-size: 38px; line-height: 1.2; margin: 10px 20px;"><table style="border-collapse: collapse; margin-left: auto; margin-right: auto;"><tr><td style="width: 20px;"></td>{a_tds}<td style="width: 50px; text-align: center; vertical-align: middle;" rowspan="2">{op}</td></tr><tr><td></td>{b_tds}</tr><tr><td></td>{ans_tds}<td></td></tr><tr><td></td><td colspan="{max_len}" style="border-bottom: 6px double #000; height: 10px;"></td><td></td></tr></table></div></div>"""

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
            
        return f"{equation_html}<div style=\"display: block; text-align: center; margin-top: 10px;\"><div style=\"display: inline-block; font-family: 'Sarabun', sans-serif; line-height: 1.2; margin: 10px 20px;\"><table style=\"border-collapse: collapse;\"><tr><td style=\"border: none;\"></td>{''.join(ans_tds_list)}</tr><tr><td style=\"border: none; text-align: right; padding-right: 12px; vertical-align: bottom; font-size: 38px;\">{divisor}</td>{''.join(div_tds_list)}</tr>{empty_rows}</table></div></div>"
    
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
                        
        steps.append({
            'mul_res': mul_res, 
            'rem': rem, 
            'col_index': i, 
            'top_m': top_m, 
            'strik': strik
        })
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
    
    html = f"{equation_html}<div style=\"display: block; text-align: center; margin-top: 10px;\"><div style=\"display: inline-block; font-family: 'Sarabun', sans-serif; line-height: 1.2; margin: 10px 20px;\"><table style=\"border-collapse: collapse;\"><tr><td style=\"border: none;\"></td>{''.join(ans_tds_list)}</tr><tr><td style=\"border: none; text-align: right; padding-right: 12px; vertical-align: bottom; font-size: 38px;\">{divisor}</td>{''.join(div_tds_list)}</tr>"
    
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
# 2. ฐานข้อมูลหลักสูตร (Master Database) เฉพาะหลักสูตรปกติ ป.1-ป.6
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
        "เวลา เงิน และการวัด": ["การบอกเวลาเป็นนาฬิกาและนาที", "การบอกจำนวนเงินทั้งหมด", "การอ่านน้ำหนักจากเครื่องชั่งสปริง", "การอ่านความยาวจากไม้บรรทัด"],
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
    
    # 🔥 ปรับ Limit x10 เมื่อเปิดโหมดชาเลนจ์
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

            # =========================================================
            # ภาพกราฟิก (นาฬิกา, เครื่องชั่ง, แผนภูมิ, การวัดความยาว)
            # =========================================================
            if actual_sub_t == "การบอกเวลาเป็นนาฬิกาและนาที":
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
                # 🔥 ระบบชาเลนจ์สำหรับการวัด
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
                pic_val = random.choice([2, 5, 10]) * (5 if is_challenge else 1) # ทวีคูณถ้าเป็น challenge
                
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
                    q = pic_html + f"<br>จากแผนภูมิรูปภาพ วัน{days[d1]} ขาย{item}ได้มากกว่าวัน{days[d2]} กี่ผล?"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                    <b>ขั้นที่ 1:</b> วัน{days[d1]} มีรูป {emoji} {counts[d1]} รูป ส่วนวัน{days[d2]} มี {counts[d2]} รูป<br>
                    <b>ขั้นที่ 2:</b> หาผลต่างของจำนวนรูป: {counts[d1]} - {counts[d2]} = {diff_counts} รูป<br>
                    <b>ขั้นที่ 3:</b> นำผลต่างของรูป × {pic_val} ผล ➔ {diff_counts} × {pic_val} = <b>{ans} ผล</b><br>
                    <b>ตอบ: {ans} ผล</b></span>"""

            # =========================================================
            # โหมดหลักสูตรปกติอื่นๆ
            # =========================================================
            elif actual_sub_t == "การบอกจำนวนเงินทั้งหมด":
                b1000 = random.randint(0, 2); b500 = random.randint(0, 2); b100 = random.randint(1, 5); b50 = random.randint(0, 2)
                b20 = random.randint(1, 5); c10 = random.randint(0, 5); c5 = random.randint(0, 5)
                money_list = []
                if b1000 > 0: money_list.append(f"ธนบัตร 1,000 บาท {b1000} ฉบับ")
                if b500 > 0: money_list.append(f"ธนบัตร 500 บาท {b500} ฉบับ")
                if b100 > 0: money_list.append(f"ธนบัตร 100 บาท {b100} ฉบับ")
                if b50 > 0: money_list.append(f"ธนบัตร 50 บาท {b50} ฉบับ")
                if b20 > 0: money_list.append(f"ธนบัตร 20 บาท {b20} ฉบับ")
                if c10 > 0: money_list.append(f"เหรียญ 10 บาท {c10} เหรียญ")
                if c5 > 0: money_list.append(f"เหรียญ 5 บาท {c5} เหรียญ")
                
                tot = (b1000*1000) + (b500*500) + (b100*100) + (b50*50) + (b20*20) + (c10*10) + (c5*5)
                
                calc_text = ""
                if b1000 > 0: calc_text += f"👉 1,000 × {b1000} = {b1000*1000:,} บาท<br>"
                if b500 > 0: calc_text += f"👉 500 × {b500} = {b500*500:,} บาท<br>"
                if b100 > 0: calc_text += f"👉 100 × {b100} = {b100*100:,} บาท<br>"
                if b50 > 0: calc_text += f"👉 50 × {b50} = {b50*50:,} บาท<br>"
                if b20 > 0: calc_text += f"👉 20 × {b20} = {b20*20:,} บาท<br>"
                if c10 > 0: calc_text += f"👉 10 × {c10} = {c10*10:,} บาท<br>"
                if c5 > 0: calc_text += f"👉 5 × {c5} = {c5*5:,} บาท<br>"
                
                q = f"จงหาจำนวนเงินทั้งหมดจาก: <b>{', '.join(money_list)}</b>"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                <b>ขั้นที่ 1: คำนวณมูลค่าของเงินแต่ละชนิด</b><br>
                {calc_text}
                <b>ขั้นที่ 2: นำเงินทั้งหมดมาบวกกัน</b><br>
                👉 ผลรวม = <b>{tot:,} บาท</b><br>
                <b>ตอบ: {tot:,} บาท</b></span>"""

            elif actual_sub_t == "การคูณ (แบบตั้งหลัก)":
                if grade in ["ป.1", "ป.2"]: a = random.randint(10, limit-1) 
                elif grade == "ป.3": a = random.randint(100, min(limit-1, 999)) 
                else: a = random.randint(1000, min(limit-1, 9999)) 
                b = random.randint(2, 9) if not is_challenge else random.randint(11, 99)
                res = a * b
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} × {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '×', is_key=False)
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br><b>ขั้นที่ 1:</b> ตั้งหลักตัวเลขให้ตรงกัน<br><b>ขั้นที่ 2:</b> นำตัวคูณ ({b}) ไปคูณตัวตั้งด้านบนทีละหลัก โดยเริ่มจากหลักหน่วยทางขวาสุด<br><b>ขั้นที่ 3:</b> หากผลคูณมีค่าตั้งแต่ 10 ขึ้นไป ให้ใส่เลขตัวหลัง (หลักหน่วย) ไว้ด้านล่าง และนำเลขตัวหน้าไป 'ทด' ไว้บนหัวของหลักถัดไปทางซ้ายมือ<br><b>ขั้นที่ 4:</b> เมื่อคูณหลักถัดไปเสร็จ อย่าลืมบวกตัวทดที่อยู่ด้านบนด้วย</span><br>" + generate_vertical_table_html(a, b, '×', result=res, is_key=True)

            elif actual_sub_t == "การบวก (แบบตั้งหลัก)":
                if grade == "ป.1" and not is_challenge:
                    tens_a = random.randint(1, 9)
                    units_a = random.randint(0, 8)
                    b = random.randint(1, 9 - units_a)
                    a = (tens_a * 10) + units_a
                elif grade in ["ป.4", "ป.5", "ป.6"]:
                    a = random.randint(10000, limit // 2)
                    b = random.randint(10000, limit // 2)
                else:
                    a = random.randint(10, limit - 20)
                    b = random.randint(1, limit - a - 1)
                res = a + b
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} + {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '+', is_key=False)
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br><b>ขั้นที่ 1:</b> ตั้งหลักตัวเลขให้ตรงกัน (หลักหน่วยตรงหลักหน่วย, หลักสิบตรงหลักสิบ)<br><b>ขั้นที่ 2:</b> เริ่มบวกตัวเลขจากหลักหน่วย (ขวาสุด) ไปทางซ้ายทีละหลัก<br><b>ขั้นที่ 3:</b> หากผลบวกในหลักใดมีค่าตั้งแต่ 10 ขึ้นไป ให้ใส่เลขตัวหลังไว้ด้านล่าง และนำเลขตัวหน้าไป 'ทด' ขึ้นไปไว้บนหัวของหลักถัดไปทางซ้ายมือ<br><b>ขั้นที่ 4:</b> ในการบวกหลักถัดไป ให้นำตัวทดมาบวกเพิ่มด้วย</span><br>" + generate_vertical_table_html(a, b, '+', result=res, is_key=True)

            elif actual_sub_t == "การลบ (แบบตั้งหลัก)":
                if grade == "ป.1" and not is_challenge:
                    tens_a = random.randint(1, 9)
                    units_a = random.randint(1, 9)
                    b = random.randint(1, units_a)
                    a = (tens_a * 10) + units_a
                elif grade in ["ป.4", "ป.5", "ป.6"]:
                    a = random.randint(100000, limit - 1)
                    b = random.randint(10000, a - 1)
                else:
                    a = random.randint(10, limit - 1)
                    b = random.randint(1, a - 1)
                res = a - b
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} - {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '-', is_key=False)
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br><b>ขั้นที่ 1:</b> ตั้งหลักตัวเลขให้ตรงกัน (หลักหน่วยตรงหลักหน่วย, หลักสิบตรงหลักสิบ)<br><b>ขั้นที่ 2:</b> เริ่มลบตัวเลขจากหลักหน่วย (ขวาสุด) ไปทางซ้ายทีละหลัก<br><b>ขั้นที่ 3:</b> หากตัวเลขด้านบนน้อยกว่าตัวเลขด้านล่าง (ลบไม่พอ) ให้ทำการ 'ขอยืม' ตัวเลขจากหลักถัดไปทางซ้ายมา 1 (ซึ่งจะมีค่าเท่ากับ 10 ในหลักปัจจุบัน)<br><b>ขั้นที่ 4:</b> นำ 10 ที่ยืมมาบวกกับตัวเลขเดิม แล้วจึงทำการลบตามปกติ</span><br>" + generate_vertical_table_html(a, b, '-', result=res, is_key=True)

            elif actual_sub_t == "การหารพื้นฐาน":
                a = random.randint(2, 9) if not is_challenge else random.randint(5, 15)
                b = random.randint(2, 12) if not is_challenge else random.randint(10, 25)
                dividend = a * b
                q = f"จงหาผลลัพธ์ของ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {dividend} ÷ {a} = {box_html}</span>"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br><b>ขั้นที่ 1:</b> การหารคือการหาว่า 'ตัวหาร ({a}) ต้องคูณกับเลขอะไรจึงจะได้ผลลัพธ์เท่ากับตัวตั้ง ({dividend})'<br><b>ขั้นที่ 2:</b> ให้นักเรียนลองท่องสูตรคูณแม่ <b>{a}</b> ดูครับ:<br>&nbsp;&nbsp;&nbsp;👉 {a} × 1 = {a}<br>&nbsp;&nbsp;&nbsp;👉 ...<br>&nbsp;&nbsp;&nbsp;👉 <b>{a} × {b} = {dividend}</b> (เจอคำตอบแล้ว!)<br>ดังนั้น {dividend} ÷ {a} มีค่าเท่ากับ <b>{b}</b><br><b>ตอบ: {b}</b></span>"

            elif actual_sub_t == "การแสดงจำนวนในรูปความสัมพันธ์แบบส่วนย่อย-ส่วนรวม":
                total = random.randint(5, limit); p1 = random.randint(1, total - 1); p2 = total - p1
                miss = random.choice(['t', 'p1', 'p2'])
                svg_t = f"""<div style="display: block; text-align: center; margin-top: 10px;"><svg width="200" height="160"><line x1="100" y1="40" x2="50" y2="120" stroke="#333" stroke-width="3"/><line x1="100" y1="40" x2="150" y2="120" stroke="#333" stroke-width="3"/><circle cx="100" cy="40" r="30" fill="#e8f8f5" stroke="#16a085" stroke-width="3"/><circle cx="50" cy="120" r="30" fill="#fdf2e9" stroke="#d35400" stroke-width="3"/><circle cx="150" cy="120" r="30" fill="#fdf2e9" stroke="#d35400" stroke-width="3"/><text x="100" y="47" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='t' else "#16a085"}">{{t}}</text><text x="50" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='p1' else "#d35400"}">{{p1}}</text><text x="150" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='p2' else "#d35400"}">{{p2}}</text></svg></div>"""
                q = f"จงหาตัวเลขที่หายไป (?) จากความสัมพันธ์แบบส่วนย่อย-ส่วนรวม : " + svg_t.format(t="?" if miss=='t' else total, p1="?" if miss=='p1' else p1, p2="?" if miss=='p2' else p2)
                if miss == 't':
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>ในการหา 'ส่วนรวม' (วงกลมด้านบน) เราต้องนำ 'ส่วนย่อย' ทั้งสองส่วน (วงกลมด้านล่าง) มาบวกเข้าด้วยกัน<br>จะได้: {p1} + {p2} = <b>{total}</b><br><b>ตอบ: {total}</b></span><br>" + svg_t.format(t=total, p1=p1, p2=p2)
                else:
                    known = p2 if miss == 'p1' else p1
                    ans = p1 if miss == 'p1' else p2
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>ในการหา 'ส่วนย่อย' ที่หายไป เราต้องนำ 'ส่วนรวม' (วงกลมด้านบน) มาลบด้วย 'ส่วนย่อย' อีกข้างที่เราทราบค่าแล้ว<br>จะได้: {total} - {known} = <b>{ans}</b><br><b>ตอบ: {ans}</b></span><br>" + svg_t.format(t=total, p1=p1, p2=p2)

            elif actual_sub_t in ["หลัก ค่าของเลขโดดในแต่ละหลัก และรูปกระจาย", "หลัก ค่าของเลขโดด และรูปกระจาย", "หลัก ค่าประจำหลัก และรูปกระจาย"]:
                n = random.randint(100, limit - 1 if limit > 10 else 99)
                parts = [f"{int(d)*(10**(len(str(n))-1-i)):,}" for i,d in enumerate(str(n)) if d != '0']
                q = f"จงเขียนจำนวน <b>{n:,}</b> ให้อยู่ในรูปกระจาย"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                การเขียนในรูปกระจาย คือการแยกตัวเลขตาม "ค่าประจำหลัก" ของแต่ละตัว แล้วนำมาเขียนในรูปของการบวกกัน<br>
                <b>ขั้นที่ 1:</b> พิจารณาตัวเลขทีละตัวจากซ้ายไปขวา<br>
                <b>ขั้นที่ 2:</b> นำค่าของตัวเลขในแต่ละหลักมาเขียนคั่นด้วยเครื่องหมาย + (ถ้าหลักไหนเป็น 0 ไม่ต้องเขียน)<br>
                👉 จะได้: <b>{' + '.join(parts)}</b><br>
                <b>ตอบ: {' + '.join(parts)}</b></span>"""
                
            elif actual_sub_t == "จำนวนคู่ จำนวนคี่":
                n = random.randint(10, limit)
                q = f"จำนวน <b>{n:,}</b> เป็นจำนวนคู่ หรือ จำนวนคี่?"
                ans = "จำนวนคู่" if n % 2 == 0 else "จำนวนคี่"
                reason = "หารด้วย 2 ลงตัวพอดี" if n % 2 == 0 else "หารด้วย 2 ไม่ลงตัว (เหลือเศษ 1)"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                วิธีดูว่าตัวเลขใดเป็นจำนวนคู่หรือจำนวนคี่ เราไม่ต้องสนใจตัวเลขข้างหน้าเลย ให้ดูแค่ <b>"ตัวเลขในหลักหน่วย" (ตัวขวาสุด)</b> เท่านั้นครับ<br>
                <b>ขั้นที่ 1:</b> ตัวเลขในหลักหน่วยของข้อนี้คือเลข <b>{n%10}</b><br>
                <b>ขั้นที่ 2:</b> นำ {n%10} ไปพิจารณาว่าหารด้วย 2 ลงตัวหรือไม่<br>
                👉 พบว่า {reason}<br>
                <b>ตอบ: {n:,} เป็น{ans}</b></span>"""

            elif actual_sub_t in ["การอ่านและการเขียนตัวเลข", "การอ่าน การเขียนตัวเลข"]:
                n = random.randint(11, limit-1) if grade in ["ป.1", "ป.2", "ป.3"] else random.randint(100000, limit-1)
                if random.choice([True, False]):
                    q = f"จงเขียนตัวเลขฮินดูอารบิก <b>{n:,}</b> ให้เป็น<b>ตัวเลขไทย</b>"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>แปลงตัวเลขฮินดูอารบิกแต่ละตัวให้เป็นตัวเลขไทยตามลำดับ<br><b>ตอบ: {str(n).translate(str.maketrans('0123456789', '๐๑๒๓๔๕๖๗๘๙'))}</b></span>"
                else:
                    q = f"จงเขียนจำนวน <b>{n:,}</b> ให้เป็น<b>ตัวหนังสือ</b>"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>อ่านตัวเลขตามค่าประจำหลักจากซ้ายไปขวา (ถ้ามีหลักหน่วยเป็นเลข 1 เราจะอ่านออกเสียงว่า 'เอ็ด')<br><b>ตอบ: {generate_thai_number_text(str(n))}</b></span>"

            elif actual_sub_t == "ค่าประมาณเป็นจำนวนเต็มสิบ เต็มร้อย เต็มพัน":
                n = random.randint(1111, limit-1)
                ptype = random.choice(["เต็มสิบ", "เต็มร้อย", "เต็มพัน"])
                if ptype == "เต็มสิบ": ans = ((n+5)//10)*10; chk_d = n % 10; chk_p = "หลักหน่วย"
                elif ptype == "เต็มร้อย": ans = (((n+50)//100)*100); chk_d = (n // 10) % 10; chk_p = "หลักสิบ"
                else: ans = (((n+500)//1000)*1000); chk_d = (n // 100) % 10; chk_p = "หลักร้อย"
                action = "ปัดขึ้น (บวกเพิ่ม 1 ในหลักซ้ายมือและเปลี่ยนตัวมันเองเป็น 0)" if chk_d >= 5 else "ปัดทิ้ง (เปลี่ยนตัวมันเองและหลักทางขวาเป็น 0 ให้หมด)"
                q = f"จงหาค่าประมาณเป็นจำนวน<b>{ptype}</b> ของ {n:,}"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                เมื่อต้องการประมาณเป็นจำนวน{ptype} กฎคือให้เราถอยไปพิจารณาตัวเลขในหลักที่เล็กกว่า 1 ขั้น นั่นคือ <b>{chk_p}</b><br>
                <b>ขั้นที่ 1:</b> ตัวเลขใน {chk_p} ของข้อนี้คือเลข <b>{chk_d}</b><br>
                <b>ขั้นที่ 2:</b> ใช้กฎการปัดเลข: ถ้าเป็นเลข 0-4 ให้ปัดทิ้ง, ถ้าเป็นเลข 5-9 ให้ปัดขึ้น<br>
                <b>ขั้นที่ 3:</b> ในกรณีนี้เป็นเลข {chk_d} ดังนั้นเราต้องทำการ <b>{action}</b><br>
                <b>ตอบ: ค่าประมาณคือ {ans:,}</b></span>"""

            elif actual_sub_t == "แบบรูปซ้ำของรูปเรขาคณิต":
                shapes = ["🔴", "🟦", "⭐"]
                pt = [0, 1, 2]
                seq = [shapes[pt[i%3]] for i in range(7)]
                ans = shapes[pt[7%3]]
                q = f"พิจารณาแบบรูปซ้ำต่อไปนี้ รูปที่หายไปในช่องว่างคือรูปใด? <br><br>{' '.join(seq)} &nbsp;&nbsp;&nbsp; <b>____</b>"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                <b>ขั้นที่ 1:</b> ให้เราสังเกตดูว่ารูปภาพเหล่านี้มีการเรียงซ้ำกันเป็นชุดๆ ละกี่รูป<br>
                <b>ขั้นที่ 2:</b> จะเห็นว่ารูปภาพเรียงซ้ำกันเป็นชุด ชุดละ 3 รูป คือ [ {shapes[0]}, {shapes[1]}, {shapes[2]} ]<br>
                <b>ขั้นที่ 3:</b> เมื่อเรานับลำดับของแบบรูปวนไปเรื่อยๆ จนถึงตำแหน่งที่หายไป จะพบว่ามันวนกลับมาตกที่รูป <b>{ans}</b> พอดี<br>
                <b>ตอบ: รูปที่หายไปคือ {ans}</b></span>"""

            elif actual_sub_t in ["การนับทีละ 1", "การนับทีละ 10", "การนับทีละ 2 ทีละ 5 ทีละ 10 และทีละ 100"]:
                step = 10 if actual_sub_t == "การนับทีละ 10" else (1 if actual_sub_t == "การนับทีละ 1" else random.choice([2, 5, 10, 100]))
                inc = random.choice([True, False])
                max_val = limit - (3 * step); max_val = max(max_val, 10)
                st_val = random.randint(1, max_val)
                seq = [st_val, st_val+step, st_val+2*step, st_val+3*step] if inc else [st_val+3*step, st_val+2*step, st_val+step, st_val]
                idx = random.randint(0, 3)
                ans_str = f"{seq[idx]:,}"
                seq_str = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;".join([f"{s:,}" if i != idx else "_____" for i, s in enumerate(seq)])
                word_inc = "เพิ่มขึ้น" if inc else "ลดลง"
                q = f"จงพิจารณาแบบรูปและเติมตัวเลขที่หายไปลงในช่องว่าง : <br><br><span style='font-weight: bold; margin-left: 10px;'>{seq_str}</span>"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                <b>ขั้นที่ 1:</b> สังเกตความต่างของตัวเลขสองตัวที่อยู่ติดกัน<br>
                <b>ขั้นที่ 2:</b> จะพบว่าตัวเลขในแบบรูปนี้มีการ <b>{word_inc}ทีละ {step}</b> อย่างสม่ำเสมอ<br>
                <b>ขั้นที่ 3:</b> ดังนั้น การหาตัวเลขที่หายไป ก็ให้เราทำการนำเลขที่อยู่ก่อนหน้ามา{word_inc}ไปอีก {step}<br>
                <b>ตอบ: ตัวเลขที่หายไปคือ {ans_str}</b></span>"""

            elif actual_sub_t in ["การเรียงลำดับจำนวน (น้อยไปมาก)", "การเรียงลำดับจำนวน (มากไปน้อย)", "การเปรียบเทียบและเรียงลำดับ"]:
                nums = random.sample(range(10, limit), 4)
                is_asc = "น้อยไปมาก" in actual_sub_t if "น้อยไปมาก" in actual_sub_t else random.choice([True, False])
                num_str = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;".join([f"{x:,}" for x in nums])
                word_asc = "น้อยไปหามาก" if is_asc else "มากไปหาน้อย"
                ans_str = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;".join([f"{x:,}" for x in sorted(nums, reverse=not is_asc)])
                q = f"จงเรียงลำดับจำนวนต่อไปนี้จาก <b>{word_asc}</b> : <br><br><span style='font-weight: bold; margin-left: 10px;'>{num_str}</span>"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                เปรียบเทียบค่าของตัวเลขทีละจำนวน โดยเริ่มพิจารณาดูจากหลักที่อยู่ซ้ายมือสุดก่อน แล้วค่อยๆ เรียงลำดับจาก <b>{word_asc}</b> ตามที่โจทย์กำหนด จะได้ดังนี้:<br>
                <b>ตอบ: {ans_str}</b></span>"""

            elif actual_sub_t in ["การเปรียบเทียบจำนวน (> <)", "การเปรียบเทียบจำนวน (= ≠)"]:
                a = random.randint(10, limit); is_eq = "=" in actual_sub_t
                b = a if is_eq and random.choice([True, False]) else random.randint(10, limit)
                while not is_eq and a == b: b = random.randint(10, limit)
                sign = "=" if a == b else ("≠" if is_eq else (">" if a > b else "<"))
                sign_word = "เท่ากับ" if a == b else ("มากกว่า" if a > b else "น้อยกว่า")
                sign_choices = "'=' หรือ '≠'" if is_eq else "'>' หรือ '<'"
                q = f"จงเติมเครื่องหมาย {sign_choices} ลงในช่องว่างให้ถูกต้อง: <span style='display:inline-flex; align-items:center; font-weight:bold; margin-left: 10px;'>{a:,} _____ {b:,}</span>"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                เปรียบเทียบค่าของตัวเลขทีละหลักโดยเริ่มจากทางซ้ายสุดไปทางขวา จะพบว่า {a:,} มีค่า <b>{sign_word}</b> {b:,}<br>
                <b>ตอบ: เติมเครื่องหมาย {sign}</b></span>"""

            elif actual_sub_t == "การอ่านและเขียนเศษส่วน":
                den = random.randint(3, 8); num = random.randint(1, den - 1); frac_html = f_html(num, den); svg_graphic = draw_fraction_svg(num, den)
                q = svg_graphic + f"<br>มีรูปสี่เหลี่ยมที่ถูกแบ่งออกเป็นส่วนเท่าๆ กันทั้งหมด {den} ช่อง มีการระบายสีไปทั้งหมด {num} ช่อง จะสามารถเขียนแทนด้วยเศษส่วนได้อย่างไร?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                <b>ขั้นที่ 1: หาตัวส่วน (จำนวนช่องทั้งหมด)</b><br>👉 นับจำนวนช่องสี่เหลี่ยมทั้งหมดที่ถูกแบ่งไว้เท่าๆ กัน จะได้ <b>{den} ช่อง</b><br>👉 นำตัวเลขนี้ไปเขียนไว้เป็น "ตัวส่วน" (เลขด้านล่าง)<br>
                <b>ขั้นที่ 2: หาตัวเศษ (จำนวนช่องที่ระบายสี)</b><br>👉 นับจำนวนช่องสีฟ้าที่ถูกระบายสี จะได้ <b>{num} ช่อง</b><br>👉 นำตัวเลขนี้ไปเขียนไว้เป็น "ตัวเศษ" (เลขด้านบน)<br>
                <b>ขั้นที่ 3: ประกอบร่างเศษส่วน</b><br>👉 เขียนให้อยู่ในรูปเศษส่วน จะได้: <br><br>{frac_html}<br><br>👉 อ่านว่า "เศษ {num} ส่วน {den}"<br>
                <b>ตอบ: <span style='display:inline-flex; align-items:center;'>{frac_html}</span></b></span>"""

            elif actual_sub_t == "แปลงเศษเกินเป็นจำนวนคละ":
                den = random.randint(3, 12); num = random.randint(den + 1, den * 5)
                while num % den == 0: num = random.randint(den + 1, den * 5)
                f_h = f_html(num, den); mix = generate_mixed_number_html(num // den, num % den, den)
                q = f"จงเขียนเศษเกินต่อไปนี้ ให้อยู่ในรูปของจำนวนคละ : <span style='display:inline-flex; vertical-align: middle; margin-left: 10px;'>{f_h}</span>"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                การแปลงเศษเกินให้เป็นจำนวนคละ ทำได้โดยการนำตัวเศษ(เลขด้านบน) ไปตั้งหารด้วยตัวส่วน(เลขด้านล่าง)<br>
                <b>ขั้นที่ 1: ตั้งหาร</b><br>👉 นำตัวเศษ <b>{num}</b> ตั้ง หารด้วย <b>{den}</b> ({num} ÷ {den})<br>
                <b>ขั้นที่ 2: หาผลหารและเศษ</b><br>👉 ท่องสูตรคูณแม่ {den} ว่า {den} คูณอะไรได้ใกล้เคียง {num} มากที่สุดโดยไม่เกิน<br>👉 จะได้ {den} × {num // den} = {den * (num // den)}<br>👉 ดังนั้นจะได้ผลลัพธ์จำนวนเต็มคือ <b>{num // den}</b><br>👉 นำ {num} ลบ {den * (num // den)} จะเหลือเศษ <b>{num % den}</b><br>
                <b>ขั้นที่ 3: ประกอบร่างเป็นจำนวนคละ</b><br>👉 นำ "จำนวนเต็ม" มาเขียนไว้ด้านหน้าสุด<br>👉 นำ "เศษ" มาเขียนเป็นตัวเศษด้านบน (ส่วนตัวส่วนยังคงเป็นเลข {den} เหมือนเดิม)<br>👉 จะได้ผลลัพธ์คือ:<br><br>{mix}<br>
                <b>ตอบ: <span style='display:inline-flex; align-items:center;'>{mix}</span></b></span>"""

            elif actual_sub_t in ["การบวกลบเศษส่วน (ตัวส่วนเท่ากัน)", "การบวกเศษส่วน", "การลบเศษส่วน"]:
                den = random.randint(5, 15); num1 = random.randint(1, den-1); num2 = random.randint(1, den-1)
                op = "+" if "บวก" in actual_sub_t else "-"
                if actual_sub_t == "การบวกลบเศษส่วน (ตัวส่วนเท่ากัน)": op = random.choice(["+", "-"])
                if op == "-" and num1 < num2: num1, num2 = num2, num1 
                
                if grade == "ป.5" and actual_sub_t in ["การบวกเศษส่วน", "การลบเศษส่วน"]:
                    d1 = random.randint(2, 10); d2 = random.randint(2, 10)
                    while d1 == d2: d2 = random.randint(2, 10) 
                    n1 = random.randint(1, d1 - 1); n2 = random.randint(1, d2 - 1)
                    if op == "-" and (n1/d1) < (n2/d2): n1, n2 = n2, n1; d1, d2 = d2, d1
                    lcm_d = (d1 * d2) // math.gcd(d1, d2); m1 = lcm_d // d1; m2 = lcm_d // d2
                    ans_num = (n1 * m1) + (n2 * m2) if op == "+" else (n1 * m1) - (n2 * m2); word_op = "บวก" if op == "+" else "ลบ"
                    
                    f1 = f_html(n1, d1); f2 = f_html(n2, d2)
                    q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; margin-left:5px;'>{prefix}{f1} <span style='margin: 0 8px; font-weight: bold;'>{op}</span> {f2}</span>"
                    f1_mul = f_html(f"{n1} × {m1}", f"{d1} × {m1}", is_bold=False); f2_mul = f_html(f"{n2} × {m2}", f"{d2} × {m2}", is_bold=False)
                    f1_new = f_html(n1 * m1, lcm_d); f2_new = f_html(n2 * m2, lcm_d); s_ans = f_html(ans_num, lcm_d)
                    
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                    <b>ขั้นที่ 1: ตรวจสอบและหา ค.ร.น. ของตัวส่วน</b><br>👉 สังเกตว่าตัวส่วน {d1} และ {d2} ยังไม่เท่ากัน จึงไม่สามารถ{word_op}กันได้ทันที<br>👉 ต้องหา ค.ร.น. ของ {d1} และ {d2} ซึ่งคำนวณได้เท่ากับ <b>{lcm_d}</b><br>
                    <b>ขั้นที่ 2: แปลงเศษส่วนให้มีตัวส่วนเท่ากับ {lcm_d}</b><br>👉 ตัวแรก: นำ {m1} มาคูณทั้งเศษและส่วน ➔ <span style='display:inline-flex; align-items:center;'>{f1_mul}</span> = <span style='display:inline-flex; align-items:center;'>{f1_new}</span><br>👉 ตัวที่สอง: นำ {m2} มาคูณทั้งเศษและส่วน ➔ <span style='display:inline-flex; align-items:center;'>{f2_mul}</span> = <span style='display:inline-flex; align-items:center;'>{f2_new}</span><br>
                    <b>ขั้นที่ 3: ดำเนินการ{word_op}ตัวเศษ</b><br>👉 เมื่อตัวส่วนเป็น {lcm_d} เท่ากันแล้ว ให้นำตัวเศษมา{word_op}กัน: {n1*m1} {op} {n2*m2} = <b>{ans_num}</b><br>👉 ประกอบร่างเป็นเศษส่วนผลลัพธ์ จะได้: <br><br>{s_ans}<br>
                    <b>ตอบ: <span style='display:inline-flex; align-items:center;'>{s_ans}</span></b></span>"""
                else:
                    ans_num = num1 + num2 if op == '+' else num1 - num2; word_op = "บวก" if op == "+" else "ลบ"
                    f1 = f_html(num1, den); f2 = f_html(num2, den); s_ans = f_html(ans_num, den)
                    q = f"จงหาผลลัพธ์: <span style='display:inline-flex; align-items:center; margin-left:5px;'>{f1} <span style='margin: 0 8px; font-weight: bold;'>{op}</span> {f2}</span>"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                    <b>ขั้นที่ 1: ตรวจสอบตัวส่วน</b><br>👉 สังเกตที่ตัวส่วน (เลขด้านล่าง) จะพบว่าทั้งสองจำนวนมีตัวส่วนเป็น <b>{den}</b> เท่ากันแล้ว<br>
                    <b>ขั้นที่ 2: ดำเนินการคำนวณ</b><br>👉 เมื่อตัวส่วนเท่ากัน เราสามารถนำตัวเศษ (เลขด้านบน) มา<b>{word_op}</b>กันได้ทันที โดยที่ตัวส่วนยังคงเดิม<br>👉 นำ {num1} {op} {num2} = <b>{ans_num}</b><br>
                    <b>ขั้นที่ 3: สรุปผลลัพธ์</b><br>👉 จะได้คำตอบคือ: <br><br>{s_ans}<br>
                    <b>ตอบ: <span style='display:inline-flex; align-items:center;'>{s_ans}</span></b></span>"""

            elif actual_sub_t in ["การคูณเศษส่วน", "การหารเศษส่วน"]:
                n1, d1 = random.randint(1, 5), random.randint(2, 7); n2, d2 = random.randint(1, 5), random.randint(2, 7)
                op = "×" if actual_sub_t == "การคูณเศษส่วน" else "÷"
                f1 = f_html(n1, d1); f2 = f_html(n2, d2)
                q = f"จงหาผลลัพธ์: <span style='display:inline-flex; align-items:center; margin-left:5px;'>{f1} <span style='margin: 0 8px; font-weight: bold;'>{op}</span> {f2}</span>"
                if op == '×':
                    ans_f = f_html(n1*n2, d1*d2)
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                    <b>ขั้นที่ 1: เข้าใจหลักการคูณเศษส่วน</b><br>👉 การคูณเศษส่วนไม่ต้องทำตัวส่วนให้เท่ากัน สามารถจับคู่คูณได้เลย คือ "เศษคูณเศษ" และ "ส่วนคูณส่วน"<br>
                    <b>ขั้นที่ 2: นำตัวเศษ (เลขด้านบน) มาคูณกัน</b><br>👉 {n1} × {n2} = <b>{n1*n2}</b><br>
                    <b>ขั้นที่ 3: นำตัวส่วน (เลขด้านล่าง) มาคูณกัน</b><br>👉 {d1} × {d2} = <b>{d1*d2}</b><br>
                    <b>ขั้นที่ 4: ประกอบร่างเป็นเศษส่วนผลลัพธ์</b><br>👉 นำผลคูณที่ได้มาเขียนเป็นเศษส่วน จะได้: <br><br>{ans_f}<br>
                    <b>ตอบ: <span style='display:inline-flex; align-items:center;'>{ans_f}</span></b></span>"""
                else:
                    ans_f = f_html(n1*d2, d1*n2); f2_rev = f_html(d2, n2)
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                    <b>ขั้นที่ 1: ใช้กฎของการหารเศษส่วน</b><br>👉 กฎคือ "ตัวหน้าคงเดิม เปลี่ยนเครื่องหมายหารเป็นคูณ และสลับบนล่างเฉพาะเศษส่วนตัวหลัง"<br>👉 เปลี่ยนจาก <span style='display:inline-flex; align-items:center;'>{f2}</span> เป็น <span style='display:inline-flex; align-items:center;'>{f2_rev}</span><br>
                    <b>ขั้นที่ 2: ดำเนินการคูณเศษส่วนตามปกติ</b><br>👉 นำตัวเศษคูณตัวเศษ: {n1} × {d2} = <b>{n1*d2}</b><br>👉 นำตัวส่วนคูณตัวส่วน: {d1} × {n2} = <b>{d1*n2}</b><br>
                    <b>ขั้นที่ 3: ประกอบร่างผลลัพธ์</b><br>👉 นำมาเขียนเป็นเศษส่วน จะได้: <br><br>{ans_f}<br>
                    <b>ตอบ: <span style='display:inline-flex; align-items:center;'>{ans_f}</span></b></span>"""

            elif actual_sub_t == "การเขียนเศษส่วนในรูปร้อยละ":
                den = random.choice([2, 4, 5, 10, 20, 25, 50]); num = random.randint(1, den-1); f_h = f_html(num, den)
                q = f"จงแปลงเศษส่วนต่อไปนี้ ให้อยู่ในรูปร้อยละ (เปอร์เซ็นต์) : <span style='display:inline-flex; vertical-align: middle; margin-left: 10px;'>{f_h}</span>"
                mul = 100 // den; frac_100 = f_html(num*mul, 100)
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                <b>ขั้นที่ 1: ทำความเข้าใจความหมายของร้อยละ</b><br>👉 คำว่า 'ร้อยละ' หรือ 'เปอร์เซ็นต์ (%)' หมายถึง เศษส่วนที่มี <b>ตัวส่วน (เลขด้านล่าง) เป็น 100 เสมอ</b><br>
                <b>ขั้นที่ 2: หาตัวเลขมาคูณตัวส่วนให้เป็น 100</b><br>👉 จากโจทย์ ตัวส่วนคือ {den} เราต้องคิดว่า {den} คูณอะไรถึงจะได้ 100<br>👉 นำ 100 ÷ {den} = <b>{mul}</b> แสดงว่าต้องนำ {mul} มาคูณ<br>
                <b>ขั้นที่ 3: ขยายเศษส่วน</b><br>👉 นำ {mul} ไปคูณทั้งตัวเศษและตัวส่วนเพื่อรักษาค่าให้เท่าเดิม<br>👉 ตัวเศษ: {num} × {mul} = <b>{num * mul}</b><br>👉 ตัวส่วน: {den} × {mul} = <b>100</b><br>👉 จะได้เศษส่วนใหม่คือ <span style='display:inline-flex; align-items:center;'>{frac_100}</span><br>
                <b>ขั้นที่ 4: สรุปคำตอบ</b><br>👉 เมื่อตัวส่วนเป็น 100 แล้ว ตัวเศษด้านบนคือคำตอบของเปอร์เซ็นต์ได้เลย!<br>
                <b>ตอบ: ร้อยละ {num * mul} หรือ {num * mul}%</b></span>"""

            elif actual_sub_t == "การหารยาว":
                divisor = random.randint(2, 12); quotient = random.randint(100, 999); dividend = divisor * quotient
                eq_html = f"จงหาผลลัพธ์การหารยาว <span style='display:inline-flex; align-items:center; font-weight: bold; margin-left: 10px; color: #2c3e50;'>{prefix} {dividend:,} ÷ {divisor} = {box_html}</span>"
                q = generate_long_division_step_by_step_html(divisor, dividend, eq_html, is_key=False)
                sol = generate_long_division_step_by_step_html(divisor, dividend, eq_html, is_key=True)

            elif actual_sub_t == "การบวกและการลบทศนิยม":
                a, b = round(random.uniform(10.0, 99.9), 2), round(random.uniform(1.0, 9.9), 2)
                op = random.choice(["+", "-"]); word_op = "บวก" if op == "+" else "ลบ"
                q = f"จงหาผลลัพธ์ทศนิยม <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:.2f} {op} {b:.2f} = {box_html}</span>"
                sol_table = generate_decimal_vertical_html(a, b, op, is_key=True)
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                <b>ขั้นที่ 1:</b> กฎเหล็กของการบวกลบทศนิยมคือ <b>ต้องตั้งจุดทศนิยมให้ตรงกันเป๊ะๆ</b> เสมอ!<br>
                <b>ขั้นที่ 2:</b> ทำการตั้งหลักตัวเลขอื่นๆ ให้ตรงกันตามจุดทศนิยม<br>
                <b>ขั้นที่ 3:</b> ทำการ{word_op}เลขจากขวาไปซ้ายตามปกติเหมือนการ{word_op}เลขจำนวนเต็มครับ</span><br>{sol_table}"""

            elif actual_sub_t == "การคูณทศนิยม":
                a, b = round(random.uniform(1.0, 12.0), 1), random.randint(2, 9)
                q = f"จงหาผลลัพธ์การคูณทศนิยม <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:.1f} × {b} = {box_html}</span>"
                sol_table = generate_vertical_table_html(int(round(a*10)), b, '×', result=int(round(a*10))*b, is_key=True)
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                เทคนิคการคูณทศนิยมคือ ให้แกล้งลืมจุดทศนิยมไปก่อน แล้วนำตัวเลขมาคูณกันแบบจำนวนเต็มปกติเลยครับ!<br>
                <b>ขั้นที่ 1:</b> นำ {int(round(a*10))} มาตั้งคูณด้วย {b} ได้ผลลัพธ์ดังนี้:<br>{sol_table}<br>
                <b>ขั้นที่ 2:</b> จากนั้นมาพิจารณาดูว่าตัวตั้งและตัวคูณรวมกันมีทศนิยมกี่ตำแหน่ง<br>
                👉 ในข้อนี้ {a:.1f} มีทศนิยม 1 ตำแหน่ง และ {b} ไม่มีทศนิยม (0 ตำแหน่ง) รวมเป็น 1 ตำแหน่ง<br>
                <b>ขั้นที่ 3:</b> ให้นำผลลัพธ์ที่ได้ มาใส่จุดทศนิยม 1 ตำแหน่ง (นับจากหลังมาหน้า)<br>
                <b>ตอบ: {round(a*b, 1):.1f}</b></span>"""

            elif actual_sub_t == "การอ่านและการเขียนทศนิยม":
                n = round(random.uniform(0.1, 99.999), random.randint(1, 3))
                q = f"จงเขียน <b>{n}</b> เป็นตัวหนังสือภาษาไทย"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                การอ่านทศนิยม แบ่งออกเป็น 2 ส่วน คือส่วนหน้าจุด และส่วนหลังจุด<br>
                <b>ขั้นที่ 1:</b> ตัวเลขหน้าจุดให้อ่านแบบจำนวนเต็มปกติ<br>
                <b>ขั้นที่ 2:</b> ตัวเลขหลังจุดให้อ่านเรียงตัวทีละตัว (ห้ามอ่านเป็นสิบหรือร้อย)<br>
                <b>ตอบ: {generate_thai_number_text(str(n))}</b></span>"""

            elif actual_sub_t == "การแก้สมการ (บวก/ลบ)":
                x = random.randint(10, 50); a = random.randint(5, 20); op = random.choice(["+", "-"])
                if op == "+":
                    q = f"จงแก้สมการหาค่า x : <span style='color: #3498db; margin-left: 15px;'><b>x + {a} = {x+a}</b></span>"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                    เป้าหมายในการแก้สมการคือ การทำให้ <b>x</b> เหลืออยู่คนเดียวโดดๆ ทางฝั่งซ้ายของเครื่องหมายเท่ากับ<br>
                    <b>ขั้นที่ 1:</b> สังเกตว่าฝั่งซ้ายมี <b>+{a}</b> เกินมาติดอยู่กับ x เราต้องกำจัดมันทิ้งไป<br>
                    <b>ขั้นที่ 2:</b> โดยใช้สมบัติการเท่ากัน: เราจะนำ <b>{a} มาลบออกทั้งสองข้างของสมการ</b><br>
                    <b>ขั้นที่ 3:</b> เขียนบรรทัดใหม่ได้ว่า: x + {a} <b style='color:red;'>- {a}</b> = {x+a} <b style='color:red;'>- {a}</b><br>
                    <b>ขั้นที่ 4:</b> ทางฝั่งซ้าย +{a} ลบกับ -{a} จะหักล้างกันเหลือ 0 ทำให้เหลือแค่ x ตัวเดียว<br>
                    👉 ทางฝั่งขวา นำ {x+a} ลบด้วย {a} จะได้คำตอบคือ <b>{x}</b><br>
                    <b>ตอบ: x = {x}</b></span>"""
                else:
                    q = f"จงแก้สมการหาค่า x : <span style='color: #3498db; margin-left: 15px;'><b>x - {a} = {x-a}</b></span>"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                    เป้าหมายในการแก้สมการคือ การทำให้ <b>x</b> เหลืออยู่คนเดียวโดดๆ ทางฝั่งซ้ายของเครื่องหมายเท่ากับ<br>
                    <b>ขั้นที่ 1:</b> สังเกตว่าฝั่งซ้ายมี <b>-{a}</b> ติดอยู่กับ x เราต้องกำจัดมันทิ้งไป<br>
                    <b>ขั้นที่ 2:</b> โดยใช้สมบัติการเท่ากัน: เราจะนำ <b>{a} มาบวกเข้าทั้งสองข้างของสมการ</b><br>
                    <b>ขั้นที่ 3:</b> เขียนบรรทัดใหม่ได้ว่า: x - {a} <b style='color:green;'>+ {a}</b> = {x-a} <b style='color:green;'>+ {a}</b><br>
                    <b>ขั้นที่ 4:</b> ทางฝั่งซ้าย -{a} บวกกับ +{a} จะหักล้างกันเหลือ 0 ทำให้เหลือแค่ x ตัวเดียว<br>
                    👉 ทางฝั่งขวา นำ {x-a} บวกด้วย {a} จะได้คำตอบคือ <b>{x}</b><br>
                    <b>ตอบ: x = {x}</b></span>"""

            elif actual_sub_t == "การแก้สมการ (คูณ/หาร)":
                a = random.randint(2, 12); x = random.randint(5, 20); op = random.choice(["*", "/"])
                if op == "*":
                    q = f"จงแก้สมการหาค่า x : <span style='color: #3498db; margin-left: 15px;'><b>{a}x = {a*x}</b></span>"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                    เป้าหมายคือต้องทำให้ x อยู่คนเดียวโดดๆ ทางฝั่งซ้าย<br>
                    <b>ขั้นที่ 1:</b> จากโจทย์ <b>{a}x</b> หมายความว่าเลข <b>{a}</b> กำลัง 'คูณ' อยู่กับ x เราต้องกำจัดเลข {a} ออกไป<br>
                    <b>ขั้นที่ 2:</b> โดยใช้สมบัติการเท่ากัน: เราจะนำ <b>{a} มาหารทั้งสองข้างของสมการ</b><br>
                    <b>ขั้นที่ 3:</b> เขียนบรรทัดใหม่ได้ว่า: ({a}x) <b style='color:red;'>÷ {a}</b> = {a*x} <b style='color:red;'>÷ {a}</b><br>
                    <b>ขั้นที่ 4:</b> ทางฝั่งซ้าย {a} หาร {a} ได้ 1 เหลือแค่ x ตัวเดียว<br>
                    👉 ทางฝั่งขวา นำ {a*x} ตั้งหารด้วย {a} จะได้คำตอบคือ <b>{x}</b><br>
                    <b>ตอบ: x = {x}</b></span>"""
                else:
                    frac_x_a = f_html("x", str(a), color="#3498db")
                    q = f"จงแก้สมการหาค่า x : <span style='color: #3498db; margin-left: 15px; display:inline-flex; align-items:center;'>{frac_x_a} = {x}</span>"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step):</b><br>
                    เป้าหมายคือต้องทำให้ x อยู่คนเดียวโดดๆ ทางฝั่งซ้าย<br>
                    <b>ขั้นที่ 1:</b> จากโจทย์ <span style='display:inline-flex; align-items:center;'>{f_html('x', str(a), '#2c3e50', is_bold=False)}</span> หมายความว่า x กำลังถูก "หาร" ด้วยเลข <b>{a}</b> เราจึงต้องกำจัดเลข {a} ที่เป็นตัวส่วนนี้ออกไป<br>
                    <b>ขั้นที่ 2:</b> โดยใช้สมบัติการเท่ากัน: เราจะนำ <b>{a} มาคูณเข้าทั้งสองข้างของสมการ</b><br>
                    <b>ขั้นที่ 3:</b> เขียนบรรทัดใหม่ได้ว่า: <span style='display:inline-flex; align-items:center;'>{f_html('x', str(a), '#2c3e50', is_bold=False)}</span> <b style='color:green;'>× {a}</b> = {x} <b style='color:green;'>× {a}</b><br>
                    <b>ขั้นที่ 4:</b> ทางฝั่งซ้าย ตัวส่วน (ตัวหาร) {a} จะตัดกับตัวคูณ {a} หมดไป เหลือเพียงแค่ <b>x</b> ตัวเดียว<br>
                    👉 ทางฝั่งขวา นำ {x} มาคูณกับ {a} จะได้ <b>{x*a}</b><br>
                    <b>ตอบ: x = {x*a}</b></span>"""

            elif actual_sub_t == "การแก้สมการ (สองขั้นตอน)":
                a = random.randint(2, 9); x = random.randint(2, 15); b = random.randint(1, 20)
                q = f"จงแก้สมการแบบ 2 ขั้นตอน : <span style='color: #3498db; margin-left: 15px;'><b>{a}x + {b} = {a*x+b}</b></span>"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (Step-by-step แก้สมการ 2 ขั้นตอน):</b><br>
                    หลักการคือ เราต้องกำจัดตัวเลขที่อยู่ "ไกล" จาก x ที่สุดออกไปก่อน แล้วค่อยกำจัดตัวที่ติดกับ x ภายหลัง<br>
                    <b>ขั้นที่ 1: กำจัดตัวบวกลบก่อน (อยู่ไกลกว่า)</b><br>
                    👉 ฝั่งซ้ายมี <b>+{b}</b> อยู่ไกลสุด ให้กำจัดโดยนำ <b>{b} มาลบออกทั้งสองข้าง</b><br>
                    👉 จะได้: {a}x + {b} <b style='color:red;'>- {b}</b> = {a*x+b} <b style='color:red;'>- {b}</b><br>
                    👉 จะได้สมการใหม่ที่สั้นลงคือ: <b>{a}x = {a*x}</b><br><br>
                    <b>ขั้นที่ 2: กำจัดตัวคูณหาร (อยู่ติดกัน)</b><br>
                    👉 ฝั่งซ้ายมีเลข <b>{a}</b> คูณติดกับ x อยู่ ให้กำจัดโดยนำ <b>{a} มาหารทั้งสองข้าง</b><br>
                    👉 จะได้: ({a}x) <b style='color:red;'>÷ {a}</b> = {a*x} <b style='color:red;'>÷ {a}</b><br>
                    👉 จะได้คำตอบสุดท้ายคือ <b>x = {x}</b><br>
                    <b>ตอบ: x = {x}</b></span>"""

            elif actual_sub_t == "การหา ห.ร.ม.":
                a, b = random.randint(12, 48), random.randint(12, 48)
                while a == b: b = random.randint(12, 48) 
                q = f"จงหา ห.ร.ม. (หารร่วมมาก) ของ <b>{a}</b> และ <b>{b}</b>"
                sol = generate_short_division_html(a, b, mode="ห.ร.ม.")

            elif actual_sub_t == "การหา ค.ร.น.":
                a, b = random.randint(4, 24), random.randint(4, 24)
                while a == b: b = random.randint(4, 24) 
                q = f"จงหา ค.ร.น. (คูณร่วมน้อย) ของ <b>{a}</b> และ <b>{b}</b>"
                sol = generate_short_division_html(a, b, mode="ค.ร.น.")

            if q not in seen: 
                seen.add(q)
                questions.append({"question": q, "solution": sol})
                break
            attempts += 1
            
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
        .q-box {{ margin-bottom: {q_margin}; padding: 10px 15px; page-break-inside: avoid; font-size: 20px; }}
        .workspace {{ height: {ws_height}; border: 2px dashed #bdc3c7; border-radius: 8px; margin: 15px 0; padding: 10px; color: #95a5a6; font-size: 16px; background-color: #fafbfc; }}
        .ans-line {{ margin-top: 10px; border-bottom: 1px dotted #999; width: 80%; height: 30px; font-weight: bold; font-size: 20px; display: flex; align-items: flex-end; padding-bottom: 5px; }}
        .sol-text {{ color: #333; font-size: 18px; display: block; margin-top: 15px; padding: 15px; background-color: #f1f8ff; border-left: 4px solid #3498db; border-radius: 4px; }}
        .page-footer {{ text-align: right; font-size: 14px; color: #95a5a6; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }}
    </style></head><body>
    <div class="header"><h2>{title} - {grade}</h2><p><b>หมวดหมู่:</b> {sub_t}</p></div>
    {student_info}"""
    
    for i, item in enumerate(questions, 1):
        html += f'<div class="q-box"><b>ข้อที่ {i}.</b> '
        if is_key:
            if "(แบบตั้งหลัก)" in sub_t or "หารยาว" in sub_t: 
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

# 🔥 โหมดชาเลนจ์
st.sidebar.markdown("---")
is_challenge = st.sidebar.toggle("🔥 โหมดชาเลนจ์ (ท้าทาย)", value=False)
if is_challenge:
    st.sidebar.warning("เปิดโหมดชาเลนจ์แล้ว! ตัวเลขจะยากขึ้นและโจทย์รูปภาพจะท้าทายกว่าเดิม")

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
        
        # ส่งพารามิเตอร์ is_challenge เข้าไปใน Logic ด้วย
        qs = generate_questions_logic(selected_grade, selected_main, selected_sub, num_input, is_challenge)
        
        html_w = create_page(selected_grade, selected_sub, qs, is_key=False, q_margin=q_margin, ws_height=ws_height, brand_name=brand_name)
        html_k = create_page(selected_grade, selected_sub, qs, is_key=True, q_margin=q_margin, ws_height=ws_height, brand_name=brand_name)
        
        st.session_state['worksheet_html'] = html_w
        st.session_state['answerkey_html'] = html_k
        
        # ถอดหน้าปกออก
        ebook_body = f'\n<div class="a4-wrapper">{extract_body(html_w)}</div>\n<div class="a4-wrapper">{extract_body(html_k)}</div>\n'
        
        full_ebook_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap" rel="stylesheet"><style>@page {{ size: A4; margin: 15mm; }} @media screen {{ body {{ font-family: 'Sarabun', sans-serif; background-color: #525659; display: flex; flex-direction: column; align-items: center; padding: 40px 0; margin: 0; }} .a4-wrapper {{ width: 210mm; min-height: 297mm; background: white; margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.3); padding: 15mm; box-sizing: border-box; }} }} @media print {{ body {{ font-family: 'Sarabun', sans-serif; background: transparent; padding: 0; display: block; margin: 0; }} .a4-wrapper {{ width: 100%; min-height: auto; margin: 0; padding: 0; box-shadow: none; page-break-after: always; }} }} .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 10px; padding-bottom: 10px; }} .q-box {{ margin-bottom: {q_margin}; padding: 10px 15px; page-break-inside: avoid; font-size: 20px; }} .workspace {{ height: {ws_height}; border: 2px dashed #bdc3c7; border-radius: 8px; margin: 15px 0; padding: 10px; color: #95a5a6; font-size: 16px; background-color: #fafbfc; }} .ans-line {{ margin-top: 10px; border-bottom: 1px dotted #999; width: 80%; height: 30px; font-weight: bold; font-size: 20px; display: flex; align-items: flex-end; padding-bottom: 5px; }} .sol-text {{ color: #333; font-size: 18px; display: block; margin-top: 15px; padding: 15px; background-color: #f1f8ff; border-left: 4px solid #3498db; border-radius: 4px; }} .page-footer {{ text-align: right; font-size: 14px; color: #95a5a6; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }} </style></head><body>{ebook_body}</body></html>"""

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
    st.success(f"✅ คืนชีพโค้ดเดิมทั้งหมด 100% พร้อมโหมดไม้บรรทัดและ Challenge เรียบร้อยแล้วครับ!")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📄 โหลดเฉพาะโจทย์", data=st.session_state['worksheet_html'], file_name=f"{st.session_state['filename_base']}_Worksheet.html", mime="text/html", use_container_width=True)
        st.download_button("🔑 โหลดเฉพาะเฉลย", data=st.session_state['answerkey_html'], file_name=f"{st.session_state['filename_base']}_AnswerKey.html", mime="text/html", use_container_width=True)
    with c2:
        st.download_button("📚 โหลดรวมเล่ม E-Book", data=st.session_state['ebook_html'], file_name=f"{st.session_state['filename_base']}_Full_EBook.html", mime="text/html", use_container_width=True)
        st.download_button("🗂️ โหลดแพ็กเกจ (.zip)", data=st.session_state['zip_data'], file_name=f"{st.session_state['filename_base']}.zip", mime="application/zip", use_container_width=True)
    st.markdown("---")
    components.html(st.session_state['ebook_html'], height=800, scrolling=True)
