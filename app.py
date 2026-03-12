import streamlit as st
import random
import math
import zipfile
import io
import time

# ==========================================
# ตั้งค่าหน้าเพจ Web App
# ==========================================
st.set_page_config(page_title="เครื่องมือสร้างใบงานคณิตศาสตร์", page_icon="🖨️", layout="centered")
st.title("🖨️ เครื่องมือสร้างใบงานคณิตศาสตร์ ป.1 - ป.6")
st.markdown("ระบบสุ่มโจทย์อัตโนมัติ สำหรับคุณครูประถมศึกษา")

# ==========================================
# 1. ฐานข้อมูลหลักสูตร (Ultimate Master Database ป.1 - ป.6)
# ==========================================
curriculum_db = {
    "ป.1": {
        "จำนวนนับ 1 ถึง 100 และ 0": [
            "การนับทีละ 1", 
            "การนับทีละ 10", 
            "การอ่านและการเขียนตัวเลข",
            "การแสดงจำนวนในรูปความสัมพันธ์แบบส่วนย่อย-ส่วนรวม (ภาพกราฟิก)",
            "แบบรูปซ้ำของรูปเรขาคณิต (ภาพกราฟิก)", 
            "การบอกอันดับที่ (ภาพกราฟิกรถแข่ง)", 
            "หลัก ค่าของเลขโดดในแต่ละหลัก และรูปกระจาย", 
            "การเปรียบเทียบจำนวน (> <)",  
            "การเปรียบเทียบจำนวน (= ≠)", 
            "การเรียงลำดับจำนวน (น้อยไปมาก)", 
            "การเรียงลำดับจำนวน (มากไปน้อย)"
        ],
        "การบวก การลบ": [
            "การบวก (แบบตั้งหลัก)", 
            "การลบ (แบบตั้งหลัก)"
        ],
        "แผนภูมิรูปภาพ": [
            "การอ่านแผนภูมิรูปภาพอย่างง่าย (ภาพกราฟิก)"
        ]
    },
    "ป.2": {
        "จำนวนนับไม่เกิน 1,000 และ 0": [
            "การนับทีละ 2 ทีละ 5 ทีละ 10 และทีละ 100", 
            "การอ่านและการเขียนตัวเลข",
            "จำนวนคู่ จำนวนคี่", 
            "หลัก ค่าของเลขโดด และรูปกระจาย", 
            "การเปรียบเทียบจำนวน",
            "การเรียงลำดับจำนวน (น้อยไปมาก)", 
            "การเรียงลำดับจำนวน (มากไปน้อย)"
        ],
        "เวลาและการวัด": [
            "การบอกเวลาเป็นนาฬิกาและนาที (หน้าปัดนาฬิกา)", 
            "การอ่านน้ำหนักจากเครื่องชั่งสปริง (ภาพกราฟิก)"
        ],
        "การบวก ลบ คูณ หาร": [
            "การบวก (แบบตั้งหลัก)", 
            "การลบ (แบบตั้งหลัก)", 
            "การคูณ การหาร", 
            "การบวก ลบ คูณ หารระคน"
        ],
        "แผนภูมิรูปภาพ": [
            "การอ่านแผนภูมิรูปภาพ (ภาพกราฟิก)"
        ]
    },
    "ป.3": {
        "จำนวนนับและเศษส่วน": [
            "การอ่าน การเขียนตัวเลข", 
            "หลัก ค่าของเลขโดด และรูปกระจาย", 
            "การเปรียบเทียบจำนวน",
            "การเรียงลำดับจำนวน (น้อยไปมาก)", 
            "การเรียงลำดับจำนวน (มากไปน้อย)",
            "การอ่านและเขียนเศษส่วน (จากรูปภาพ)", 
            "การเปรียบเทียบและการบวกลบเศษส่วน"
        ],
        "เวลา เงิน และการวัด": [
            "การบอกเวลาเป็นนาฬิกาและนาที (หน้าปัดนาฬิกา)", 
            "การบอกจำนวนเงินทั้งหมด (ภาพกราฟิกธนบัตรและเหรียญ)", 
            "การอ่านน้ำหนักจากเครื่องชั่งสปริง (ภาพกราฟิก)"
        ],
        "การบวก ลบ คูณ หาร": [
            "การบวก (แบบตั้งหลัก)", 
            "การลบ (แบบตั้งหลัก)", 
            "การคูณ การหารยาวและการหารสั้น", 
            "การบวก ลบ คูณ หารระคน"
        ],
        "แผนภูมิรูปภาพ": [
            "การอ่านแผนภูมิรูปภาพ (ภาพกราฟิก)"
        ]
    },
    "ป.4": {
        "จำนวนนับที่มากกว่า 100,000": [
            "การอ่านและการเขียนตัวเลข", 
            "หลัก ค่าประจำหลัก และรูปกระจาย", 
            "การเปรียบเทียบและเรียงลำดับ", 
            "ค่าประมาณเป็นจำนวนเต็มสิบ เต็มร้อย เต็มพัน"
        ],
        "การบวก ลบ คูณ หาร": [
            "การบวก (แบบตั้งหลัก)", 
            "การลบ (แบบตั้งหลัก)", 
            "การหารยาว"
        ],
        "เศษส่วนและทศนิยม": [
            "แปลงเศษเกินเป็นจำนวนคละ", 
            "การอ่านและการเขียนทศนิยม"
        ],
        "เรขาคณิตและการวัด": [
            "การวัดขนาดของมุม (ภาพกราฟิกไม้โปรแทรกเตอร์)"
        ]
    },
    "ป.5": {
        "เศษส่วน": [
            "การบวกและการลบเศษส่วน", 
            "การคูณและการหารเศษส่วน"
        ],
        "ทศนิยม": [
            "การบวกและการลบทศนิยม", 
            "การคูณทศนิยม"
        ],
        "ร้อยละและเปอร์เซ็นต์": [
            "การเขียนเศษส่วนในรูปร้อยละ"
        ]
    },
    "ป.6": {
        "ตัวประกอบของจำนวนนับ": [
            "การหา ห.ร.ม.", 
            "การหา ค.ร.น."
        ],
        "อัตราส่วนและร้อยละ": [
            "โจทย์ปัญหาร้อยละ"
        ],
        "สมการ": [
            "การแก้สมการเบื้องต้น"
        ]
    }
}

# ==========================================
# ฟังก์ชันช่วย: สร้างตารางตั้งหลักเลข (ขยายหลักอัตโนมัติถึงหลักล้าน)
# ==========================================
def generate_vertical_table_html(a, b, op, result=None, is_key=False):
    max_val = max(a, b, (result if result else 0))
    num_len = max(len(str(max_val)), 2) 
    
    str_a = f"{a:>{num_len}}"
    str_b = f"{b:>{num_len}}"
    
    def safe_char(c): 
        return c if c.strip() else "" 
    
    show_idx = list(range(num_len))
    
    res_tds = ""
    if is_key and result is not None:
        str_r = f"{result:>{num_len}}"
        res_tds = "".join([f'<td style="width: 35px; text-align: center; color: red; font-weight: bold;">{safe_char(str_r[i])}</td>' for i in show_idx])
    else:
        res_tds = "".join([f'<td style="width: 35px; height: 45px;"></td>' for _ in show_idx])

    html = f"""
    <div style="display: inline-block; font-family: 'Sarabun', sans-serif; font-size: 38px; line-height: 1.2; margin: 20px;">
        <table style="border-collapse: collapse; margin-left: auto; margin-right: auto;">
            <tr>
                <td style="width: 20px;"></td>
                {''.join([f'<td style="width: 35px; text-align: center;">{safe_char(str_a[i])}</td>' for i in show_idx])}
                <td style="width: 50px; text-align: center; vertical-align: middle;" rowspan="2">{op}</td>
            </tr>
            <tr>
                <td></td>
                {''.join([f'<td style="width: 35px; text-align: center; border-bottom: 2px solid #000;">{safe_char(str_b[i])}</td>' for i in show_idx])}
            </tr>
            <tr>
                <td></td>
                {res_tds}
                <td></td>
            </tr>
            <tr>
                <td></td>
                <td colspan="{len(show_idx)}" style="border-bottom: 6px double #000; height: 10px;"></td>
                <td></td>
            </tr>
        </table>
    </div>
    """
    return html

# ==========================================
# 2. ฟังก์ชันสมองกลสร้างโจทย์และกราฟิก 
# ==========================================
def generate_questions_logic(grade, main_t, sub_t, num_q):
    questions = []
    seen = set()
    limit_map = {"ป.1": 100, "ป.2": 1000, "ป.3": 100000, "ป.4": 1000000, "ป.5": 9000000, "ป.6": 9000000}
    limit = limit_map.get(grade, 100)

    for _ in range(num_q):
        q, sol = "", ""
        attempts = 0
        while attempts < 300:
            
            # ==========================================
            # หมวดการตั้งหลักบวก ลบ คูณ
            # ==========================================
            if sub_t == "การบวก (แบบตั้งหลัก)":
                if grade == "ป.1":
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
                q = generate_vertical_table_html(a, b, '+', is_key=False)
                sol = generate_vertical_table_html(a, b, '+', result=res, is_key=True)

            elif sub_t == "การลบ (แบบตั้งหลัก)":
                if grade == "ป.1":
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
                q = generate_vertical_table_html(a, b, '-', is_key=False)
                sol = generate_vertical_table_html(a, b, '-', result=res, is_key=True)

            elif sub_t == "การคูณ (แบบตั้งหลัก)":
                if grade == "ป.2":
                    a = random.randint(10, 99)
                    b = random.randint(2, 9)
                else:
                    a = random.randint(100, 999)
                    b = random.randint(2, 9)
                res = a * b
                q = generate_vertical_table_html(a, b, '×', is_key=False)
                sol = generate_vertical_table_html(a, b, '×', result=res, is_key=True)

            # ==========================================
            # หมวดภาพกราฟิก SVG 
            # ==========================================
            elif sub_t == "การแสดงจำนวนในรูปความสัมพันธ์แบบส่วนย่อย-ส่วนรวม (ภาพกราฟิก)":
                total = random.randint(5, 20)
                p1 = random.randint(1, total - 1)
                p2 = total - p1
                missing_pos = random.choice(['total', 'p1', 'p2'])
                
                q_text_t = "?" if missing_pos == 'total' else str(total)
                q_text_p1 = "?" if missing_pos == 'p1' else str(p1)
                q_text_p2 = "?" if missing_pos == 'p2' else str(p2)
                
                svg_q = f"""<br><div style="text-align: center; margin-top: 15px; margin-bottom: 5px;"><svg width="200" height="160"><line x1="100" y1="40" x2="50" y2="120" stroke="#333" stroke-width="2"/><line x1="100" y1="40" x2="150" y2="120" stroke="#333" stroke-width="2"/><circle cx="100" cy="40" r="28" fill="#ffffff" stroke="#333" stroke-width="2"/><circle cx="50" cy="120" r="28" fill="#ffffff" stroke="#333" stroke-width="2"/><circle cx="150" cy="120" r="28" fill="#ffffff" stroke="#333" stroke-width="2"/><text x="100" y="47" font-size="22" font-weight="bold" text-anchor="middle" fill="{'#e74c3c' if missing_pos=='total' else '#333'}">{q_text_t}</text><text x="50" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{'#e74c3c' if missing_pos=='p1' else '#333'}">{q_text_p1}</text><text x="150" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{'#e74c3c' if missing_pos=='p2' else '#333'}">{q_text_p2}</text></svg></div>"""
                svg_a = f"""<br><div style="text-align: center; margin-top: 15px; margin-bottom: 5px;"><svg width="200" height="160"><line x1="100" y1="40" x2="50" y2="120" stroke="#333" stroke-width="2"/><line x1="100" y1="40" x2="150" y2="120" stroke="#333" stroke-width="2"/><circle cx="100" cy="40" r="28" fill="#ffffff" stroke="#333" stroke-width="2"/><circle cx="50" cy="120" r="28" fill="#ffffff" stroke="#333" stroke-width="2"/><circle cx="150" cy="120" r="28" fill="#ffffff" stroke="#333" stroke-width="2"/><text x="100" y="47" font-size="22" font-weight="bold" text-anchor="middle" fill="{'#e74c3c' if missing_pos=='total' else '#333'}">{total}</text><text x="50" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{'#e74c3c' if missing_pos=='p1' else '#333'}">{p1}</text><text x="150" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{'#e74c3c' if missing_pos=='p2' else '#333'}">{p2}</text></svg></div>"""

                q = f"จงหาตัวเลขที่หายไป (?) จากความสัมพันธ์แบบส่วนย่อย-ส่วนรวมต่อไปนี้: {svg_q}"
                sol = f"{svg_a}"

            elif sub_t == "การบอกอันดับที่ (ภาพกราฟิกรถแข่ง)":
                color_map = {"แดง": "#ff4d4d", "ฟ้า": "#3498db", "เขียว": "#2ecc71", "เหลือง": "#f1c40f", "ชมพู": "#ff9ff3"}
                colors_th = list(color_map.keys())
                random.shuffle(colors_th)
                cars_svg = ""
                x_positions = [280, 220, 160, 100, 40]
                for i in range(5):
                    c_hex = color_map[colors_th[i]]
                    x = x_positions[i]
                    cars_svg += f"""
                    <g transform="translate({x}, 40)">
                       <path d="M 10 15 L 15 5 L 30 5 L 35 15 Z" fill="#e0e0e0" stroke="#333" stroke-width="1"/>
                       <rect x="0" y="15" width="50" height="15" rx="4" fill="{c_hex}" stroke="#333" stroke-width="1.5"/>
                       <circle cx="12" cy="30" r="6" fill="#333"/>
                       <circle cx="38" cy="30" r="6" fill="#333"/>
                    </g>
                    """
                svg_diagram = f"""<br><div style="text-align: center; margin-top: 15px; margin-bottom: 15px;"><svg width="400" height="80"><line x1="20" y1="76" x2="380" y2="76" stroke="#95a5a6" stroke-width="4"/><rect x="350" y="30" width="10" height="46" fill="#fff" stroke="#333" stroke-width="1"/><rect x="350" y="30" width="10" height="10" fill="#333"/><rect x="350" y="50" width="10" height="10" fill="#333"/><text x="355" y="20" font-size="14" font-weight="bold" text-anchor="middle" fill="#e74c3c">เส้นชัย</text>{cars_svg}</svg></div>"""
                q_type = random.choice(["find_rank", "find_color"])
                idx = random.randint(0, 4)
                c_name = colors_th[idx]
                ans_svg = f"""<svg width="60" height="30" style="vertical-align: middle; margin-left: 10px;"><path d="M 10 10 L 15 2 L 30 2 L 35 10 Z" fill="#e0e0e0" stroke="#333" stroke-width="1"/><rect x="0" y="10" width="50" height="12" rx="3" fill="{color_map[c_name]}" stroke="#333" stroke-width="1"/><circle cx="12" cy="22" r="5" fill="#333"/><circle cx="38" cy="22" r="5" fill="#333"/></svg>"""
                
                if q_type == "find_rank":
                    q = f"จากภาพการแข่งขัน รถสี{c_name} วิ่งอยู่ในอันดับที่เท่าไร? {svg_diagram}"
                    sol = f"อันดับที่ {idx + 1} {ans_svg}"
                else:
                    q = f"จากภาพการแข่งขัน รถที่วิ่งอยู่ในอันดับที่ {idx + 1} คือรถสีอะไร? {svg_diagram}"
                    sol = f"สี{c_name} {ans_svg}"

            elif sub_t == "แบบรูปซ้ำของรูปเรขาคณิต (ภาพกราฟิก)":
                shapes = {
                    "วงกลม": '<circle cx="15" cy="15" r="12" fill="#ffb3ba" stroke="#333" stroke-width="2"/>',
                    "สี่เหลี่ยม": '<rect x="3" y="3" width="24" height="24" fill="#bae1ff" stroke="#333" stroke-width="2"/>',
                    "สามเหลี่ยม": '<polygon points="15,3 27,27 3,27" fill="#baffc9" stroke="#333" stroke-width="2"/>',
                    "ดาว": '<polygon points="15,1 19,10 29,10 21,16 24,26 15,20 6,26 9,16 1,10 11,10" fill="#ffffba" stroke="#333" stroke-width="2"/>',
                    "หัวใจ": '<path d="M 15 8 C 15 8 10 -2 3 5 C -4 12 15 28 15 28 C 15 28 34 12 27 5 C 20 -2 15 8 15 8 z" fill="#ffdfba" stroke="#333" stroke-width="2"/>'
                }
                ptypes = [[0, 1], [0, 1, 2], [0, 0, 1], [0, 1, 1]]
                pt = random.choice(ptypes)
                keys = random.sample(list(shapes.keys()), len(set(pt)))
                seq = [keys[pt[i % len(pt)]] for i in range(12)]
                slen = random.randint(5, 8) 
                
                html = "<br><div style='margin-top:10px; text-align:center;'>"
                for i in range(slen):
                    html += f'<svg width="30" height="30" style="vertical-align: middle; margin: 0 5px;">{shapes[seq[i]]}</svg>'
                html += '<span style="display:inline-block; width:30px; height:30px; border-bottom:2px dashed #000; margin: 0 5px;"></span></div>'
                
                q = f"จงพิจารณาแบบรูปต่อไปนี้ แล้วบอกว่ารูปที่หายไปคือรูปใด? {html}"
                sol = f"<svg width='30' height='30' style='vertical-align: middle;'>{shapes[seq[slen]]}</svg>"

            elif sub_t == "การบอกเวลาเป็นนาฬิกาและนาที (หน้าปัดนาฬิกา)":
                h = random.randint(1, 12)
                m = random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
                am = m * 6
                ah = (h % 12) * 30 + (m / 60) * 30
                ticks = "".join([f'<line x1="60" y1="15" x2="60" y2="20" stroke="#333" stroke-width="2" transform="rotate({i*30} 60 60)" />' for i in range(12)])
                svg = f"""<br><div style="text-align: center; margin-top: 15px; margin-bottom: 5px;"><svg width="120" height="120"><circle cx="60" cy="60" r="50" fill="#fdfdfd" stroke="#333" stroke-width="3"/>{ticks}<line x1="60" y1="60" x2="60" y2="35" stroke="#e74c3c" stroke-width="4" stroke-linecap="round" transform="rotate({ah} 60 60)" /><line x1="60" y1="60" x2="60" y2="20" stroke="#3498db" stroke-width="3" stroke-linecap="round" transform="rotate({am} 60 60)" /><circle cx="60" cy="60" r="4" fill="#333"/></svg></div>"""
                day = random.choice(["เวลากลางวัน", "เวลากลางคืน"])
                q = f"จากรูปหน้าปัดนาฬิกา หากเป็น <b>{day}</b> จะอ่านเวลาได้กี่นาฬิกา กี่นาที? {svg}"
                ans_h = h
                if day == "เวลากลางวัน":
                    if 1 <= h <= 5: ans_h = h + 12
                    elif h == 12: ans_h = 12
                else: 
                    if 6 <= h <= 11: ans_h = h + 12
                    elif h == 12: ans_h = 0
                sol = f"{ans_h:02d}.{m:02d} น."

            elif sub_t == "การอ่านและเขียนเศษส่วน (จากรูปภาพ)":
                den = random.randint(3, 8)
                num = random.randint(1, den - 1)
                rects = "".join([f'<rect x="{i*30+1}" y="1" width="30" height="30" fill="{"#a0c4ff" if i < num else "#ffffff"}" stroke="#333" stroke-width="2"/>' for i in range(den)])
                svg = f'<br><div style="text-align: center; margin-top: 15px; margin-bottom: 5px;"><svg width="{den*30+2}" height="32">{rects}</svg></div>'
                q = f"จากรูปภาพ ส่วนที่ระบายสีเขียนแสดงเป็นเศษส่วนได้อย่างไร? {svg}"
                sol = f"เศษ {num} ส่วน {den}"

            elif sub_t == "การบอกจำนวนเงินทั้งหมด (ภาพกราฟิกธนบัตรและเหรียญ)":
                b100 = random.randint(0, 3)
                b50 = random.randint(0, 2)
                b20 = random.randint(0, 4)
                c10 = random.randint(0, 5)
                c5 = random.randint(0, 3)
                c1 = random.randint(0, 5)
                if b100+b50+b20+c10+c5+c1 == 0: b20 = 1
                total = (b100*100) + (b50*50) + (b20*20) + (c10*10) + (c5*5) + (c1*1)
                
                money_svg = "<br><div style='margin-top:10px; line-height: 2.5;'>"
                for _ in range(b100): money_svg += '<svg width="60" height="30" style="vertical-align: middle; margin: 2px;"><rect width="60" height="30" rx="3" fill="#ff7675" stroke="#c0392b" stroke-width="2"/><text x="30" y="20" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">100</text></svg>'
                for _ in range(b50): money_svg += '<svg width="60" height="30" style="vertical-align: middle; margin: 2px;"><rect width="60" height="30" rx="3" fill="#74b9ff" stroke="#2980b9" stroke-width="2"/><text x="30" y="20" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">50</text></svg>'
                for _ in range(b20): money_svg += '<svg width="60" height="30" style="vertical-align: middle; margin: 2px;"><rect width="60" height="30" rx="3" fill="#55efc4" stroke="#27ae60" stroke-width="2"/><text x="30" y="20" font-size="12" font-weight="bold" fill="#333" text-anchor="middle">20</text></svg>'
                for _ in range(c10): money_svg += '<svg width="30" height="30" style="vertical-align: middle; margin: 2px;"><circle cx="15" cy="15" r="13" fill="#bdc3c7" stroke="#7f8c8d" stroke-width="2"/><circle cx="15" cy="15" r="8" fill="#f1c40f"/><text x="15" y="19" font-size="10" font-weight="bold" fill="#333" text-anchor="middle">10</text></svg>'
                for _ in range(c5): money_svg += '<svg width="26" height="26" style="vertical-align: middle; margin: 2px;"><circle cx="13" cy="13" r="11" fill="#bdc3c7" stroke="#7f8c8d" stroke-width="2"/><text x="13" y="17" font-size="10" font-weight="bold" fill="#333" text-anchor="middle">5</text></svg>'
                for _ in range(c1): money_svg += '<svg width="22" height="22" style="vertical-align: middle; margin: 2px;"><circle cx="11" cy="11" r="9" fill="#bdc3c7" stroke="#7f8c8d" stroke-width="2"/><text x="11" y="14" font-size="8" font-weight="bold" fill="#333" text-anchor="middle">1</text></svg>'
                money_svg += "</div>"
                q = f"จากภาพ มีเงินทั้งหมดกี่บาท? {money_svg}"
                sol = f"{total} บาท"

            elif sub_t == "การอ่านน้ำหนักจากเครื่องชั่งสปริง (ภาพกราฟิก)":
                weight = random.randint(1, 5)
                angle = -150 + (weight * 60)
                scale_svg = f"""
                <br>
                <div style="text-align: center; margin-top: 15px; margin-bottom: 5px;">
                    <svg width="150" height="150">
                        <rect x="25" y="20" width="100" height="110" rx="10" fill="#f1f2f6" stroke="#333" stroke-width="3"/>
                        <circle cx="75" cy="75" r="40" fill="#fff" stroke="#333" stroke-width="2"/>
                        <text x="75" y="47" font-size="10" font-weight="bold" text-anchor="middle">0</text>
                        <text x="105" y="65" font-size="10" font-weight="bold" text-anchor="middle">1</text>
                        <text x="100" y="100" font-size="10" font-weight="bold" text-anchor="middle">2</text>
                        <text x="75" y="112" font-size="10" font-weight="bold" text-anchor="middle">3</text>
                        <text x="50" y="100" font-size="10" font-weight="bold" text-anchor="middle">4</text>
                        <text x="45" y="65" font-size="10" font-weight="bold" text-anchor="middle">5</text>
                        <line x1="75" y1="75" x2="75" y2="45" stroke="#e74c3c" stroke-width="3" stroke-linecap="round" transform="rotate({angle} 75 75)" />
                        <circle cx="75" cy="75" r="4" fill="#333"/>
                        <path d="M 50 20 L 40 5 L 110 5 L 100 20 Z" fill="#bdc3c7" stroke="#333" stroke-width="2"/>
                    </svg>
                </div>
                """
                item_name = random.choice(["ส้ม", "แตงโม", "ข้าวสาร", "เนื้อหมู", "ปลา", "ไก่"])
                q = f"จากหน้าปัดเครื่องชั่งสปริง {item_name}มีน้ำหนักกี่กิโลกรัม? {scale_svg}"
                sol = f"{weight} กิโลกรัม"

            elif sub_t == "การอ่านแผนภูมิรูปภาพอย่างง่าย (ภาพกราฟิก)" or sub_t == "การอ่านแผนภูมิรูปภาพ (ภาพกราฟิก)":
                items = [("🍎 แอปเปิล", "🍎"), ("🍊 ส้ม", "🍊"), ("🍌 กล้วย", "🍌"), ("🍓 องุ่น", "🍓")]
                selected = random.sample(items, 3)
                multiplier = 1 if grade == "ป.1" else random.choice([2, 5])
                counts = [random.randint(1, 5), random.randint(1, 5), random.randint(1, 5)]
                
                table_html = f"""<br>
                <div style='margin-top:10px; width: 80%; border: 2px solid #333; border-collapse: collapse;'>
                    <div style='background-color: #f1f2f6; border-bottom: 2px solid #333; text-align: center; padding: 5px; font-weight: bold;'>
                        จำนวนผลไม้ที่ร้านค้าขายได้
                    </div>
                """
                for i in range(3):
                    emojis = "".join([selected[i][1]] * counts[i])
                    table_html += f"""
                    <div style='display: flex; border-bottom: 1px solid #ccc;'>
                        <div style='width: 30%; border-right: 1px solid #ccc; padding: 5px; font-weight: bold;'>{selected[i][0]}</div>
                        <div style='width: 70%; padding: 5px; font-size: 18px;'>{emojis}</div>
                    </div>
                    """
                table_html += f"""
                    <div style='background-color: #fdfdfd; text-align: center; padding: 5px; font-weight: bold; color: #e74c3c;'>
                        กำหนดให้ 1 รูปภาพ แทนผลไม้ {multiplier} ผล
                    </div>
                </div>"""
                
                q_type = random.choice(["how_many", "difference", "total"])
                if q_type == "how_many":
                    idx = random.randint(0, 2)
                    q = f"จากแผนภูมิ ร้านค้าขาย{selected[idx][0].split(' ')[1]}ได้กี่ผล? {table_html}"
                    sol = str(counts[idx] * multiplier)
                elif q_type == "difference":
                    i1, i2 = random.sample([0, 1, 2], 2)
                    if counts[i1] > counts[i2]:
                        q = f"จากแผนภูมิ ร้านค้าขาย{selected[i1][0].split(' ')[1]}ได้มากกว่า{selected[i2][0].split(' ')[1]}กี่ผล? {table_html}"
                        sol = str((counts[i1] - counts[i2]) * multiplier)
                    elif counts[i2] > counts[i1]:
                        q = f"จากแผนภูมิ ร้านค้าขาย{selected[i2][0].split(' ')[1]}ได้มากกว่า{selected[i1][0].split(' ')[1]}กี่ผล? {table_html}"
                        sol = str((counts[i2] - counts[i1]) * multiplier)
                    else:
                        q = f"จากแผนภูมิ ขายผลไม้ 3 ชนิดรวมกันกี่ผล? {table_html}"
                        sol = str(sum(counts) * multiplier)
                else:
                    q = f"จากแผนภูมิ ขายผลไม้ 3 ชนิดรวมกันกี่ผล? {table_html}"
                    sol = str(sum(counts) * multiplier)

            elif sub_t == "การวัดขนาดของมุม (ภาพกราฟิกไม้โปรแทรกเตอร์)":
                angle = random.randint(2, 16) * 10
                rad = math.radians(180 - angle)
                x_end = 100 + 70 * math.cos(rad)
                y_end = 90 - 70 * math.sin(rad)
                svg = f"""<br><div style="text-align: center;"><svg width="200" height="120"><path d="M 20 90 A 80 80 0 0 1 180 90" fill="#fdfdfd" stroke="#333" stroke-width="2"/><line x1="20" y1="90" x2="180" y2="90" stroke="#333" stroke-width="2"/><circle cx="100" cy="90" r="4" fill="#e74c3c"/><line x1="100" y1="90" x2="190" y2="90" stroke="#3498db" stroke-width="3"/><line x1="100" y1="90" x2="{x_end}" y2="{y_end}" stroke="#e74c3c" stroke-width="3"/></svg></div>"""
                q = f"จากภาพ มุมที่แสดงบนไม้โปรแทรกเตอร์มีขนาดกี่องศา? {svg}"
                sol = f"{angle} องศา"

            # ==========================================
            # หมวดตัวเลข พื้นฐาน และประถมปลาย
            # ==========================================
            elif sub_t == "การนับทีละ 1":
                inc = random.choice([True, False])
                if inc:
                    st_val = random.randint(0, 95)
                    seq = [st_val, st_val+1, st_val+2, st_val+3]
                    w = "นับเพิ่มทีละ 1"
                else:
                    st_val = random.randint(4, 100)
                    seq = [st_val, st_val-1, st_val-2, st_val-3]
                    w = "นับลดทีละ 1"
                idx = random.randint(0, 3) 
                sol = str(seq[idx])
                q = f"จงเติมตัวเลขที่หายไปในแบบรูปที่{w} : {', '.join([str(s) if i != idx else '_____' for i, s in enumerate(seq)])}"

            elif sub_t == "การนับทีละ 10":
                inc = random.choice([True, False])
                if inc:
                    st_val = random.randint(0, 60)
                    seq = [st_val, st_val+10, st_val+20, st_val+30]
                    w = "นับเพิ่มทีละ 10"
                else:
                    st_val = random.randint(40, 100)
                    seq = [st_val, st_val-10, st_val-20, st_val-30]
                    w = "นับลดทีละ 10"
                idx = random.randint(0, 3) 
                sol = str(seq[idx])
                q = f"จงเติมตัวเลขที่หายไปในแบบรูปที่{w} : {', '.join([str(s) if i != idx else '_____' for i, s in enumerate(seq)])}"
                
            elif sub_t == "การนับทีละ 2 ทีละ 5 ทีละ 10 และทีละ 100":
                step = random.choice([2, 5, 10, 100])
                inc = random.choice([True, False])
                if inc:
                    st_val = random.randint(0, 1000 - (3 * step))
                    seq = [st_val, st_val+step, st_val+2*step, st_val+3*step]
                    w = f"นับเพิ่มทีละ {step}"
                else:
                    st_val = random.randint(3 * step, 1000)
                    seq = [st_val, st_val-step, st_val-2*step, st_val-3*step]
                    w = f"นับลดทีละ {step}"
                idx = random.randint(0, 3)
                sol = str(seq[idx])
                q = f"จงเติมตัวเลขที่หายไปในแบบรูปที่{w} : {', '.join([str(s) if i != idx else '_____' for i, s in enumerate(seq)])}"

            elif sub_t == "การเปรียบเทียบจำนวน (> <)" or sub_t == "การเปรียบเทียบจำนวน":
                a = random.randint(10, limit)
                b = random.randint(10, limit)
                while a == b: b = random.randint(10, limit)
                q = f"จงเติมเครื่องหมาย > หรือ < ลงในช่องว่าง: {a:,} _____ {b:,}"
                sol = ">" if a > b else "<"

            elif sub_t == "การเปรียบเทียบจำนวน (= ≠)":
                if random.choice([True, False]):
                    a = random.randint(10, limit)
                    b = a  
                    sol = "="
                else:
                    a = random.randint(10, limit)
                    b = random.randint(10, limit)
                    while a == b: b = random.randint(10, limit)
                    sol = "≠"
                q = f"จงเติมเครื่องหมาย = หรือ ≠ ลงในช่องว่าง: {a:,} _____ {b:,}"

            elif sub_t == "การเรียงลำดับจำนวน (น้อยไปมาก)":
                nums = random.sample(range(10, limit), 4)
                q = f"จงเรียงลำดับจำนวนต่อไปนี้จาก น้อยไปมาก: {', '.join(map(str, nums))}"
                res = sorted(nums)
                sol = ", ".join(map(str, res))

            elif sub_t == "การเรียงลำดับจำนวน (มากไปน้อย)":
                nums = random.sample(range(10, limit), 4)
                q = f"จงเรียงลำดับจำนวนต่อไปนี้จาก มากไปน้อย: {', '.join(map(str, nums))}"
                res = sorted(nums, reverse=True)
                sol = ", ".join(map(str, res))

            elif sub_t == "จำนวนคู่ จำนวนคี่":
                n = random.randint(10, 999)
                q = f"จำนวน {n:,} เป็นจำนวนคู่ หรือ จำนวนคี่?"
                sol = "จำนวนคู่" if n % 2 == 0 else "จำนวนคี่"

            elif sub_t == "การอ่านและการเขียนตัวเลข":
                if grade in ["ป.1", "ป.2", "ป.3"]:
                    n = random.randint(11, limit-1)
                    q = f"จงเขียนตัวเลขฮินดูอารบิก <b>{n}</b> ให้เป็นตัวเลขไทย"
                    sol = str(n).translate(str.maketrans('0123456789', '๐๑๒๓๔๕๖๗๘๙'))
                else:
                    n = random.randint(100000, 9999999)
                    q = f"จงเขียนตัวเลข <b>{n:,}</b> ให้เป็นตัวอักษรภาษาไทย"
                    sol = f"เลข: {n:,}"
                
            elif sub_t == "หลัก ค่าของเลขโดดในแต่ละหลัก และรูปกระจาย" or sub_t == "หลัก ค่าของเลขโดด และรูปกระจาย" or sub_t == "หลัก ค่าประจำหลัก และรูปกระจาย":
                n = random.randint(11, limit-1)
                parts = [str(int(d)*(10**(len(str(n))-1-i))) for i,d in enumerate(str(n)) if d != '0']
                q = f"จงเขียนจำนวน <b>{n:,}</b> ในรูปกระจาย"
                sol = " + ".join(parts)

            elif sub_t == "การเปรียบเทียบและเรียงลำดับ":
                nums = random.sample(range(100000, 999999), 4)
                is_asc = random.choice([True, False])
                q = f"จงเรียงลำดับจำนวนจาก {'น้อยไปมาก' if is_asc else 'มากไปน้อย'}: {', '.join(f'{x:,}' for x in nums)}"
                res = sorted(nums, reverse=not is_asc)
                sol = ", ".join(f"{x:,}" for x in res)

            elif sub_t == "ค่าประมาณเป็นจำนวนเต็มสิบ เต็มร้อย เต็มพัน":
                n = random.randint(1111, 99999)
                ptype = random.choice(["เต็มสิบ", "เต็มร้อย", "เต็มพัน"])
                ans = round(n, -1) if ptype == "เต็มสิบ" else (round(n, -2) if ptype == "เต็มร้อย" else round(n, -3))
                q = f"จงหาค่าประมาณเป็นจำนวน<b>{ptype}</b> ของ {n:,}"
                sol = f"{ans:,}"

            elif sub_t == "การหารยาว":
                divisor = random.randint(2, 12)
                quotient = random.randint(100, 999)
                dividend = divisor * quotient
                q = f"จงหาผลลัพธ์ของการหาร: <b>{dividend:,} ÷ {divisor} = ?</b>"
                sol = f"{quotient:,}"

            elif sub_t == "แปลงเศษเกินเป็นจำนวนคละ":
                den = random.randint(3, 12)
                num = random.randint(den + 1, den * 5)
                q = f"จงเขียนเศษเกินต่อไปนี้ให้อยู่ในรูปจำนวนคละ : <b style='font-size:24px;'><sup>{num}</sup>/<sub>{den}</sub></b>"
                sol = f"{num // den} เศษ {num % den} ส่วน {den}"

            elif sub_t == "การอ่านและการเขียนทศนิยม":
                n = round(random.uniform(0.1, 99.999), random.randint(1, 3))
                q = f"จงอ่านทศนิยมต่อไปนี้ให้ถูกต้อง: <b>{n}</b>"
                sol = f"{n}"

            elif sub_t == "การเปรียบเทียบและการบวกลบเศษส่วน":
                den = random.randint(5, 12)
                n1 = random.randint(1, den-2)
                n2 = 1
                q = f"จงหาผลบวกของ เศษ {n1} ส่วน {den} กับ เศษ {n2} ส่วน {den}"
                sol = f"เศษ {n1+n2} ส่วน {den}"

            elif sub_t == "การบวกและการลบเศษส่วน":
                den = random.randint(5, 15)
                num1 = random.randint(1, den-1)
                num2 = random.randint(1, den-1)
                op = "+" if num1 + num2 < den * 2 else "-"
                if op == "-" and num1 < num2: num1, num2 = num2, num1
                ans_num = num1 + num2 if op == "+" else num1 - num2
                q = f"จงหาผลลัพธ์ของ : <b style='font-size:24px;'><sup>{num1}</sup>/<sub>{den}</sub> {op} <sup>{num2}</sup>/<sub>{den}</sub> = ?</b>"
                sol = f"เศษ {ans_num} ส่วน {den}"

            elif sub_t == "การคูณและการหารเศษส่วน":
                n1, d1 = random.randint(1, 5), random.randint(2, 7)
                n2, d2 = random.randint(1, 5), random.randint(2, 7)
                op = random.choice(["×", "÷"])
                q = f"จงหาผลลัพธ์ของ : <b style='font-size:24px;'><sup>{n1}</sup>/<sub>{d1}</sub> {op} <sup>{n2}</sup>/<sub>{d2}</sub> = ?</b>"
                ans_n = n1 * n2 if op == "×" else n1 * d2
                ans_d = d1 * d2 if op == "×" else d1 * n2
                sol = f"เศษ {ans_n} ส่วน {ans_d}"

            elif sub_t == "การบวกและการลบทศนิยม":
                a = round(random.uniform(10.0, 99.9), 2)
                b = round(random.uniform(1.0, 9.9), 2)
                op = random.choice(["+", "-"])
                q = f"จงหาผลลัพธ์ : <b>{a} {op} {b} = ?</b>"
                sol = f"{round(a+b, 2) if op=='+' else round(a-b, 2)}"

            elif sub_t == "การคูณทศนิยม":
                a = round(random.uniform(1.0, 12.0), 1)
                b = random.randint(2, 9)
                q = f"จงหาผลลัพธ์ : <b>{a} × {b} = ?</b>"
                sol = f"{round(a*b, 1)}"

            elif sub_t == "การเขียนเศษส่วนในรูปร้อยละ":
                den = random.choice([2, 4, 5, 10, 20, 25, 50])
                num = random.randint(1, den-1)
                ans = int((num / den) * 100)
                q = f"จงเขียนเศษส่วนต่อไปนี้ให้อยู่ในรูปร้อยละ : <b style='font-size:24px;'><sup>{num}</sup>/<sub>{den}</sub></b>"
                sol = f"ร้อยละ {ans} หรือ {ans}%"

            elif sub_t == "โจทย์ปัญหาร้อยละ":
                price = random.choice([100, 200, 500, 1000, 1500])
                percent = random.choice([10, 15, 20, 25, 50])
                discount = int(price * (percent / 100))
                q = f"เสื้อราคา {price} บาท ร้านค้าลดราคาให้ {percent}% ร้านค้าลดราคาให้กี่บาท?"
                sol = f"{discount} บาท"

            elif sub_t == "การหา ห.ร.ม.":
                a = random.randint(12, 48)
                b = random.randint(12, 48)
                ans = math.gcd(a, b)
                q = f"จงหา ห.ร.ม. ของ <b>{a}</b> และ <b>{b}</b>"
                sol = str(ans)

            elif sub_t == "การหา ค.ร.น.":
                a = random.randint(4, 24)
                b = random.randint(4, 24)
                ans = (a * b) // math.gcd(a, b)
                q = f"จงหา ค.ร.น. ของ <b>{a}</b> และ <b>{b}</b>"
                sol = str(ans)

            elif sub_t == "การแก้สมการเบื้องต้น":
                x = random.randint(5, 50)
                a = random.randint(1, 20)
                b = x + a
                q = f"จงแก้สมการเพื่อหาค่า x : <br><br><b style='font-size: 24px;'>x + {a} = {b}</b>"
                sol = f"x = {x}"

            elif sub_t == "การคูณ การหาร" or sub_t == "การบวก ลบ คูณ หารระคน" or sub_t == "การคูณ การหารยาวและการหารสั้น":
                a, b = random.randint(2, 12), random.randint(2, 12)
                is_mul = random.choice([True, False])
                if is_mul:
                    q = f"จงหาผลลัพธ์ของ {a} × {b} = ?"
                    sol = str(a * b)
                else:
                    q = f"จงหาผลลัพธ์ของ {a * b} ÷ {a} = ?"
                    sol = str(b)

            else:
                # Fallback สำหรับหัวข้ออื่นๆ ที่อาจพิมพ์ตกหล่น (เผื่อไว้กันระบบ Error)
                a = random.randint(10, limit // 2)
                b = random.randint(10, limit // 2)
                q = f"จงหาผลลัพธ์ของ {a} + {b} = ?"
                sol = str(a + b)

            if q not in seen:
                seen.add(q)
                questions.append({"question": q, "solution": sol})
                break
            attempts += 1
            
    return questions

# ==========================================
# 3. ฟังก์ชันสร้างหน้า HTML
# ==========================================
def create_page(grade, sub_t, questions, is_key=False):
    title = "เฉลยแบบฝึกหัด" if is_key else "แบบฝึกหัดคณิตศาสตร์"
    html = f"""<!DOCTYPE html><html lang="th"><head><meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css2?family=Sarabun&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Sarabun', sans-serif; padding: 40px; line-height: 1.8; }}
        .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 20px; }}
        .q-box {{ margin-bottom: 30px; padding: 15px; page-break-inside: avoid; border-bottom: 1px solid #eee; }}
        .ans-line {{ margin-top: 15px; border-bottom: 1px dotted #999; width: 80%; height: 30px; }}
        .sol-text {{ color: red; font-weight: bold; border-left: 3px solid red; padding-left: 10px; display: inline-block; margin-top: 10px; }}
    </style></head><body>
    <div class="header"><h2>{title} - {grade}</h2><p><b>เรื่อง:</b> {sub_t}</p></div>"""
    
    for i, item in enumerate(questions, 1):
        if "(แบบตั้งหลัก)" in sub_t:
            html += f'<div class="q-box"><b>ข้อที่ {i}.</b><br>{item["solution"] if is_key else item["question"]}</div>'
        else:
            html += f'<div class="q-box"><b>ข้อที่ {i}.</b> {item["question"]}'
            if is_key: 
                html += f'<br><div class="sol-text">คำตอบ: &nbsp;{item["solution"]}</div>'
            else: 
                html += '<div class="ans-line">ตอบ: </div>'
            html += '</div>'
            
    return html + "</body></html>"

# ==========================================
# 4. สร้าง UI ของ Streamlit Web App
# ==========================================
st.sidebar.header("⚙️ การตั้งค่าใบงาน")
selected_grade = st.sidebar.selectbox("1. เลือกระดับชั้น:", list(curriculum_db.keys()))
selected_main = st.sidebar.selectbox("2. เลือกหัวข้อหลัก:", list(curriculum_db[selected_grade].keys()))
selected_sub = st.sidebar.selectbox("3. เลือกหัวข้อย่อย:", curriculum_db[selected_grade][selected_main])
num_input = st.sidebar.number_input("จำนวนข้อ:", min_value=1, max_value=100, value=10)

st.sidebar.info("💡 **เคล็ดลับ:** หากต้องการสุ่มโจทย์ชุดใหม่ ให้กดปุ่ม '🚀 สร้างใบงาน' อีกครั้งก่อนโหลด")

if st.sidebar.button("🚀 สร้างใบงาน", type="primary", use_container_width=True):
    with st.spinner("กำลังประมวลผลลอจิกคณิตศาสตร์และสร้างโจทย์..."):
        qs = generate_questions_logic(selected_grade, selected_main, selected_sub, num_input)
        html_w = create_page(selected_grade, selected_sub, qs, is_key=False)
        html_k = create_page(selected_grade, selected_sub, qs, is_key=True)
        filename_base = f"{selected_grade}_{selected_sub}"
        
        # 🟢 สร้างไฟล์ Zip รวม Worksheet และ AnswerKey ไว้ด้วยกัน
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(f"{filename_base}_Worksheet.html", html_w.encode('utf-8'))
            zip_file.writestr(f"{filename_base}_AnswerKey.html", html_k.encode('utf-8'))
        
        st.session_state['zip_data'] = zip_buffer.getvalue()
        # แทรกรหัสเวลาลงในชื่อไฟล์ ป้องกันระบบโหลดไฟล์เดิมซ้ำ
        st.session_state['filename'] = f"{filename_base}_{int(time.time())}"

# 🟢 แสดงปุ่มดาวน์โหลดเมื่อกดสร้างใบงานเสร็จ
if 'zip_data' in st.session_state:
    st.success("🎉 สร้างใบงานเสร็จสมบูรณ์! คลิกดาวน์โหลดด้านล่างได้เลยครับ")
    st.download_button(
        label="📥 ดาวน์โหลดใบงานและเฉลย (ไฟล์ .zip)",
        data=st.session_state['zip_data'],
        file_name=f"{st.session_state['filename']}.zip",
        mime="application/zip",
        use_container_width=True
    )
else:
    st.info("👈 กรุณาตั้งค่าใบงานที่เมนูด้านซ้าย แล้วกดปุ่ม 'สร้างใบงาน'")
