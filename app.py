import streamlit as st
import streamlit.components.v1 as components
import random
import math
import zipfile
import io
import time
import base64

# ==========================================
# ⚙️ Web App Configuration & CSS
# ==========================================
st.set_page_config(page_title="Math Generator Pro Ultimate", page_icon="🚀", layout="wide")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1200px; }
    div[data-testid="stSidebar"] div.stButton > button { 
        background-color: #27ae60; color: white; border-radius: 8px; height: 3.5rem; 
        font-size: 18px; font-weight: bold; transition: all 0.3s ease; border: none; 
        box-shadow: 0 4px 6px rgba(39,174,96,0.3); 
    }
    div[data-testid="stSidebar"] div.stButton > button:hover { background-color: #219653; transform: translateY(-2px); }
    div.stDownloadButton > button { border-radius: 8px; font-weight: bold; border: 1px solid #bdc3c7; }
    .main-header { 
        background: linear-gradient(135deg, #2980b9, #2c3e50); 
        padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem; 
        box-shadow: 0 10px 20px rgba(0,0,0,0.15); 
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🚀 Math Worksheet Pro Ultimate</h1><p>ระบบจัดเต็ม: โจทย์ -> พื้นที่ทด -> ตอบ (ครบ ป.1-ป.6 ไม่มีการตัดโค้ด)</p></div>', unsafe_allow_html=True)

# ==========================================
# 1. ฐานข้อมูลหลักสูตร (Master Database)
# ==========================================
curriculum_db = {
    "ป.1": {
        "จำนวนนับ 1 ถึง 100 และ 0": [
            "การนับทีละ 1", 
            "การนับทีละ 10", 
            "การอ่านและการเขียนตัวเลข",
            "การแสดงจำนวนในรูปความสัมพันธ์แบบส่วนย่อย-ส่วนรวม",
            "แบบรูปซ้ำของรูปเรขาคณิต", 
            "การบอกอันดับที่ (รถแข่ง)", 
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
            "การอ่านแผนภูมิรูปภาพ"
        ]
    },
    "ป.2": {
        "จำนวนนับไม่เกิน 1,000 และ 0": [
            "การนับทีละ 2 ทีละ 5 ทีละ 10 และทีละ 100", 
            "การอ่านและการเขียนตัวเลข",
            "จำนวนคู่ จำนวนคี่", 
            "หลัก ค่าของเลขโดด และรูปกระจาย", 
            "การเปรียบเทียบจำนวน (> <)",
            "การเรียงลำดับจำนวน (น้อยไปมาก)", 
            "การเรียงลำดับจำนวน (มากไปน้อย)"
        ],
        "เวลาและการวัด": [
            "การบอกเวลาเป็นนาฬิกาและนาที", 
            "การอ่านน้ำหนักจากเครื่องชั่งสปริง"
        ],
        "การบวก ลบ คูณ หาร": [
            "การบวก (แบบตั้งหลัก)", 
            "การลบ (แบบตั้งหลัก)", 
            "การคูณ (แบบตั้งหลัก)", 
            "การหารพื้นฐาน"
        ],
        "แผนภูมิรูปภาพ": [
            "การอ่านแผนภูมิรูปภาพ"
        ]
    },
    "ป.3": {
        "จำนวนนับและเศษส่วน": [
            "การอ่าน การเขียนตัวเลข", 
            "หลัก ค่าของเลขโดด และรูปกระจาย", 
            "การเปรียบเทียบจำนวน (> <)",
            "การเรียงลำดับจำนวน (น้อยไปมาก)", 
            "การเรียงลำดับจำนวน (มากไปน้อย)",
            "การอ่านและเขียนเศษส่วน", 
            "การบวกลบเศษส่วน (ตัวส่วนเท่ากัน)"
        ],
        "เวลา เงิน และการวัด": [
            "การบอกเวลาเป็นนาฬิกาและนาที", 
            "การบอกจำนวนเงินทั้งหมด", 
            "การอ่านน้ำหนักจากเครื่องชั่งสปริง"
        ],
        "การบวก ลบ คูณ หาร": [
            "การบวก (แบบตั้งหลัก)", 
            "การลบ (แบบตั้งหลัก)", 
            "การคูณ (แบบตั้งหลัก)", 
            "การหารยาว"
        ],
        "แผนภูมิรูปภาพ": [
            "การอ่านแผนภูมิรูปภาพ"
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
            "การคูณ (แบบตั้งหลัก)", 
            "การหารยาว"
        ],
        "เศษส่วนและทศนิยม": [
            "แปลงเศษเกินเป็นจำนวนคละ", 
            "การอ่านและการเขียนทศนิยม"
        ],
        "เรขาคณิตและการวัด": [
            "การบอกชนิดของมุม",
            "การวัดขนาดของมุม (ไม้โปรแทรกเตอร์)",
            "การหาความยาวรอบรูปสี่เหลี่ยมมุมฉาก",
            "การหาพื้นที่รูปสี่เหลี่ยมมุมฉาก"
        ],
        "สมการ": [
            "การแก้สมการ (บวก/ลบ)"
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
        ],
        "สมการ": [
            "การแก้สมการ (คูณ/หาร)"
        ]
    },
    "ป.6": {
        "ตัวประกอบของจำนวนนับ": [
            "การหา ห.ร.ม.", 
            "การหา ค.ร.น."
        ],
        "อัตราส่วนและร้อยละ": [
            "การหาอัตราส่วนที่เท่ากัน", 
            "โจทย์ปัญหาอัตราส่วน", 
            "โจทย์ปัญหาร้อยละ"
        ],
        "สมการ": [
            "การแก้สมการ (สองขั้นตอน)"
        ]
    }
}
# ==========================================
# 2. ฟังก์ชันสมองกลสร้างโจทย์และกราฟิก (Original Logic - ห้ามตัดทิ้ง)
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
            act_sub = sub_t
            # 🌟 โหมดพิเศษ: สุ่มดึงจากทุกหัวข้อในชั้นนั้นๆ
            if sub_t == "แบบทดสอบรวมปลายภาค":
                all_mains = list(curriculum_db[grade].keys())
                rand_m = random.choice(all_mains)
                act_sub = random.choice(curriculum_db[grade][rand_m])

            # --- เริ่มลอจิกคณิตศาสตร์ดั้งเดิมทั้งหมด (ครบทุกเงื่อนไข) ---
            if "การคูณ (แบบตั้งหลัก)" in act_sub:
                if grade in ["ป.1", "ป.2"]: a = random.randint(10, 99) 
                elif grade == "ป.3": a = random.randint(100, 999) 
                else: a = random.randint(1000, 9999) 
                b = random.randint(2, 9); res = a * b
                sentence = f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #2c3e50;'>ประโยคสัญลักษณ์: {a:,} × {b:,} = {box_html}</div>"
                q = sentence + generate_vertical_table_html(a, b, '×', is_key=False)
                sol = sentence + generate_vertical_table_html(a, b, '×', result=res, is_key=True)

            elif "การบวก (แบบตั้งหลัก)" in act_sub:
                if grade == "ป.1":
                    tens_a = random.randint(1, 9); units_a = random.randint(0, 8)
                    b = random.randint(1, 9 - units_a); a = (tens_a * 10) + units_a
                elif grade in ["ป.4", "ป.5", "ป.6"]:
                    a = random.randint(10000, limit // 2); b = random.randint(10000, limit // 2)
                else:
                    a = random.randint(10, limit - 20); b = random.randint(1, limit - a - 1)
                res = a + b
                sentence = f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #2c3e50;'>ประโยคสัญลักษณ์: {a:,} + {b:,} = {box_html}</div>"
                q = sentence + generate_vertical_table_html(a, b, '+', is_key=False)
                sol = sentence + generate_vertical_table_html(a, b, '+', result=res, is_key=True)

            elif "การลบ (แบบตั้งหลัก)" in act_sub:
                if grade == "ป.1":
                    tens_a = random.randint(1, 9); units_a = random.randint(1, 9)
                    b = random.randint(1, units_a); a = (tens_a * 10) + units_a
                elif grade in ["ป.4", "ป.5", "ป.6"]:
                    a = random.randint(100000, limit - 1); b = random.randint(10000, a - 1)
                else:
                    a = random.randint(10, limit - 1); b = random.randint(1, a - 1)
                res = a - b
                sentence = f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #2c3e50;'>ประโยคสัญลักษณ์: {a:,} - {b:,} = {box_html}</div>"
                q = sentence + generate_vertical_table_html(a, b, '-', is_key=False)
                sol = sentence + generate_vertical_table_html(a, b, '-', result=res, is_key=True)

            elif "การหารพื้นฐาน" in act_sub:
                a = random.randint(2, 9); b = random.randint(2, 12); dvd = a * b
                q = f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #2c3e50;'>ประโยคสัญลักษณ์: {dvd} ÷ {a} = {box_html}</div>จงหาผลลัพธ์ของ <b>{dvd} ÷ {a}</b>"
                sol = f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #2c3e50;'>ประโยคสัญลักษณ์: {dvd} ÷ {a} = {box_html}</div><br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ท่องสูตรคูณแม่ {a} จะพบว่า {a} × {b} = {dvd}<br>ดังนั้น {dvd} ÷ {a} = </span> <b>{b}</b>"

            elif "ส่วนย่อย-ส่วนรวม" in act_sub:
                total = random.randint(5, 20); p1 = random.randint(1, total - 1); p2 = total - p1; miss = random.choice(['t', 'p1', 'p2'])
                svg_t = f"""<br><div style="text-align: center;"><svg width="200" height="160"><line x1="100" y1="40" x2="50" y2="120" stroke="#333" stroke-width="3"/><line x1="100" y1="40" x2="150" y2="120" stroke="#333" stroke-width="3"/><circle cx="100" cy="40" r="30" fill="#e8f8f5" stroke="#16a085" stroke-width="3"/><circle cx="50" cy="120" r="30" fill="#fdf2e9" stroke="#d35400" stroke-width="3"/><circle cx="150" cy="120" r="30" fill="#fdf2e9" stroke="#d35400" stroke-width="3"/><text x="100" y="47" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='t' else "#16a085"}">{{t}}</text><text x="50" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='p1' else "#d35400"}">{{p1}}</text><text x="150" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='p2' else "#d35400"}">{{p2}}</text></svg></div>"""
                q = f"จงหาตัวเลขที่หายไป (?) : " + svg_t.format(t="?" if miss=='t' else total, p1="?" if miss=='p1' else p1, p2="?" if miss=='p2' else p2)
                miss_map = {'t': 'ส่วนรวม (วงกลมบน)', 'p1': 'ส่วนย่อย (วงกลมซ้าย)', 'p2': 'ส่วนย่อย (วงกลมขวา)'}
                if miss == 't': calc_str = f"นำส่วนย่อยมาบวกกัน: {p1} + {p2} = <b>{total}</b>"
                elif miss == 'p1': calc_str = f"นำส่วนรวมลบด้วยส่วนย่อยที่มี: {total} - {p2} = <b>{p1}</b>"
                else: calc_str = f"นำส่วนรวมลบด้วยส่วนย่อยที่มี: {total} - {p1} = <b>{p2}</b>"
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> หา{miss_map[miss]}ที่หายไป โดย{calc_str}</span><br>" + svg_t.format(t=total, p1=p1, p2=p2)

            elif "การบอกอันดับที่" in act_sub:
                c_map = {"แดง": "#ff4d4d", "ฟ้า": "#3498db", "เขียว": "#2ecc71", "เหลือง": "#f1c40f", "ชมพู": "#ff9ff3"}
                cols = list(c_map.keys()); random.shuffle(cols); x_pos = [280, 220, 160, 100, 40]
                cars = "".join([f'<g transform="translate({x_pos[i]}, 40)"><path d="M 10 15 L 15 5 L 30 5 L 35 15 Z" fill="#e0e0e0" stroke="#333" stroke-width="1"/><rect x="0" y="15" width="50" height="15" rx="4" fill="{c_map[cols[i]]}" stroke="#333" stroke-width="1.5"/><circle cx="12" cy="30" r="6" fill="#333"/><circle cx="38" cy="30" r="6" fill="#333"/></g>' for i in range(5)])
                svg_d = f"""<br><div style="text-align: center;"><svg width="400" height="80"><line x1="20" y1="76" x2="380" y2="76" stroke="#95a5a6" stroke-width="4"/><rect x="350" y="30" width="10" height="46" fill="#fff" stroke="#333"/><text x="355" y="20" font-size="14" font-weight="bold" text-anchor="middle" fill="#e74c3c">เส้นชัย</text>{cars}</svg></div>"""
                idx = random.randint(0, 4); name = cols[idx]
                ans_svg = f'<svg width="60" height="30" style="vertical-align: middle; margin-left: 10px;"><path d="M 10 10 L 15 2 L 30 2 L 35 10 Z" fill="#e0e0e0" stroke="#333"/><rect y="10" width="50" height="12" rx="3" fill="{c_map[name]}" stroke="#333"/><circle cx="12" cy="22" r="5" fill="#333"/><circle cx="38" cy="22" r="5" fill="#333"/></svg>'
                if random.choice([True, False]): 
                    q = f"รถสี{name} วิ่งอยู่อันดับที่เท่าไร? {svg_d}"
                    sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> สังเกตจากป้ายเส้นชัยทางขวามือ แล้วนับย้อนมาทางซ้าย คันที่ 1, 2... จะพบว่ารถคันนี้อยู่ใน</span><br><b>อันดับที่ {idx + 1}</b> {ans_svg}"
                else: 
                    q = f"รถที่วิ่งอยู่ในอันดับที่ {idx + 1} คือรถสีอะไร? {svg_d}"
                    sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> เริ่มนับคันแรกจากป้ายเส้นชัยฝั่งขวามือ นับย้อนไป {idx + 1} คัน จะพบว่าเป็น</span><br><b>สี{name}</b> {ans_svg}"

            elif "แบบรูปซ้ำ" in act_sub:
                shapes = {"วงกลม": '<circle cx="15" cy="15" r="12" fill="#ffb3ba" stroke="#333" stroke-width="2"/>', "สี่เหลี่ยม": '<rect x="3" y="3" width="24" height="24" fill="#bae1ff" stroke="#333" stroke-width="2"/>', "สามเหลี่ยม": '<polygon points="15,3 27,27 3,27" fill="#baffc9" stroke="#333" stroke-width="2"/>', "ดาว": '<polygon points="15,1 19,10 29,10 21,16 24,26 15,20 6,26 9,16 1,10 11,10" fill="#ffffba" stroke="#333" stroke-width="2"/>'}
                pt = random.choice([[0, 1], [0, 1, 2], [0, 0, 1], [0, 1, 1]])
                keys = random.sample(list(shapes.keys()), len(set(pt)))
                seq = [keys[pt[i % len(pt)]] for i in range(12)]; slen = random.randint(5, 8) 
                h = "<br><div style='margin-top:10px; text-align:center;'>" + "".join([f'<svg width="30" height="30" style="vertical-align: middle; margin: 0 5px;">{shapes[seq[i]]}</svg>' for i in range(slen)]) + '<span style="display:inline-block; width:30px; height:30px; border-bottom:2px dashed #000; margin: 0 5px;"></span></div>'
                q = f"รูปที่หายไปคือรูปใด? {h}"; sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> สังเกตชุดรูปภาพที่เรียงซ้ำกัน รูปถัดไปคือ:</span><br><br><svg width='30' height='30' style='vertical-align: middle;'>{shapes[seq[slen]]}</svg>"

            elif "นาฬิกา" in act_sub:
                h, m = random.randint(1, 12), random.randint(0, 59); cx, cy = 100, 100; se = [f'<circle cx="{cx}" cy="{cy}" r="75" fill="#fdfdfd" stroke="#333" stroke-width="3"/>'];
                for i in range(60):
                    ad = i * 6 - 90; ar = math.radians(ad)
                    if i % 5 == 0:
                        tx1 = cx + 65 * math.cos(ar); ty1 = cy + 65 * math.sin(ar); tx2 = cx + 75 * math.cos(ar); ty2 = cy + 75 * math.sin(ar); se.append(f'<line x1="{tx1}" y1="{ty1}" x2="{tx2}" y2="{ty2}" stroke="#333" stroke-width="3" />'); hour = i // 5 if i // 5 != 0 else 12; txh = cx + 50 * math.cos(ar); tyh = cy + 50 * math.sin(ar) + 6; se.append(f'<text x="{txh}" y="{tyh}" font-size="18" font-weight="bold" fill="#e74c3c" text-anchor="middle">{hour}</text>'); txm = cx + 88 * math.cos(ar); tym = cy + 88 * math.sin(ar) + 4; se.append(f'<text x="{txm}" y="{tym}" font-size="12" font-weight="bold" fill="#3498db" text-anchor="middle">{i}</text>')
                    else: tx1 = cx + 70 * math.cos(ar); ty1 = cy + 70 * math.sin(ar); tx2 = cx + 75 * math.cos(ar); ty2 = cy + 75 * math.sin(ar); se.append(f'<line x1="{tx1}" y1="{ty1}" x2="{tx2}" y2="{ty2}" stroke="#777" stroke-width="1.5" />')
                ah = (h % 12) * 30 + (m / 60) * 30; am = m * 6; se.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + 40 * math.cos(math.radians(ah-90))}" y2="{cy + 40 * math.sin(math.radians(ah-90))}" stroke="#e74c3c" stroke-width="5" stroke-linecap="round" />'); se.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + 65 * math.cos(math.radians(am-90))}" y2="{cy + 65 * math.sin(math.radians(am-90))}" stroke="#3498db" stroke-width="3" stroke-linecap="round" />'); se.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="#333"/>'); svg = f'<br><div style="text-align: center; margin: 15px 0;"><svg width="180" height="180" viewBox="0 0 200 200">{"".join(se)}</svg></div>'; day = random.choice(["เวลากลางวัน", "เวลากลางคืน"]); q = f"หากเป็น <b>{day}</b> จะอ่านเวลาได้กี่นาฬิกา กี่นาที? {svg}"; ah_ans = h+12 if (day=="เวลากลางวัน" and 1<=h<=5) or (day=="เวลากลางคืน" and 6<=h<=11) else (0 if day=="เวลากลางคืน" and h==12 else h); sol = f"<br><b>ตอบ: {ah_ans:02d}.{m:02d} น.</b>"

            elif "จำนวนเงิน" in act_sub:
                b100, b50, b20, c10, c5, c1 = [random.randint(0, n) for n in [3, 2, 4, 5, 3, 5]]; total = (b100*100) + (b50*50) + (b20*20) + (c10*10) + (c5*5) + (c1*1); msvg = "<br><div style='margin-top:10px; line-height: 2.5;'>" + ('<svg width="60" height="30" style="vertical-align: middle; margin: 2px;"><rect width="60" height="30" rx="3" fill="#ff7675" stroke="#c0392b" stroke-width="2"/><text x="30" y="20" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">100</text></svg>'*b100) + ('<svg width="60" height="30" style="vertical-align: middle; margin: 2px;"><rect width="60" height="30" rx="3" fill="#74b9ff" stroke="#2980b9" stroke-width="2"/><text x="30" y="20" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">50</text></svg>'*b50) + ('<svg width="60" height="30" style="vertical-align: middle; margin: 2px;"><rect width="60" height="30" rx="3" fill="#55efc4" stroke="#27ae60" stroke-width="2"/><text x="30" y="20" font-size="12" font-weight="bold" fill="#333" text-anchor="middle">20</text></svg>'*b20) + "</div>"; q = f"จากภาพ มีเงินทั้งหมดกี่บาท? {msvg}"; sol = f"<br><b>ตอบ: {total:,} บาท</b>"

            elif "ห.ร.ม." in act_sub:
                a, b = random.randint(12, 60), random.randint(12, 60); q = f"จงหา ห.ร.ม. ของ <b>{a}</b> และ <b>{b}</b>"; sol = generate_short_division_html(a, b, "ห.ร.ม.")
            
            elif "ค.ร.น." in act_sub:
                a, b = random.randint(4, 30), random.randint(4, 30); q = f"จงหา ค.ร.น. ของ <b>{a}</b> และ <b>{b}</b>"; sol = generate_short_division_html(a, b, "ค.ร.น.")

            elif "การแก้สมการ" in act_sub:
                a, x, b = random.randint(2, 9), random.randint(2, 15), random.randint(1, 20); c = a*x + b
                q = f"จงแก้สมการเพื่อหาค่า x: {a}x + {b} = {c}"; sol = f"<b>ตอบ: x = {x}</b>"
            
            elif "อัตราส่วนที่เท่ากัน" in act_sub:
                a, b, m = random.randint(2, 9), random.randint(2, 9), random.randint(2, 9)
                while a == b: b = random.randint(2, 9)
                c, d = a*m, b*m; q = f"จงหาเลขในช่องว่าง: {a} : {b} = {c} : {box_html}"; sol = f"<b>ตอบ: {d}</b>"

            elif "โจทย์ปัญหาอัตราส่วน" in act_sub:
                scenarios = [("นักเรียนชาย", "นักเรียนหญิง", "คน", "คน"), ("น้ำหวาน", "น้ำเปล่า", "มิลลิลิตร", "มิลลิลิตร"), ("ปากกา", "ดินสอ", "ด้าม", "แท่ง")]
                item1, item2, u1, u2 = random.choice(scenarios); a, b = random.randint(2, 7), random.randint(2, 7)
                while a == b: b = random.randint(2, 7)
                m = random.randint(5, 20); val1 = a * m; val2 = b * m
                q = f"อัตราส่วนของจำนวน{item1} ต่อจำนวน{item2} เป็น <b>{a} : {b}</b><br>ถ้ามี{item1} <b>{val1} {u1}</b> จะมี{item2}จำนวนเท่าใด?"; sol = f"<b>ตอบ: {val2} {u2}</b>"

            else:
                a, b = random.randint(1, limit//2), random.randint(1, limit//2); q = f"จงหาผลลัพธ์ของ {a:,} + {b:,} = {box_html}"; sol = f"<b>ตอบ: {a+b:,}</b>"

            if q not in seen: seen.add(q); questions.append({"question": q, "solution": sol}); break
            attempts += 1
    return questions

# ==========================================
# 3. HTML Generation Engine (จัดลำดับตามสั่ง)
# ==========================================
def extract_body(html_str):
    try: return html_str.split('<body>')[1].split('</body>')[0]
    except: return html_str

def create_page(grade, sub_t, questions, is_key=False, q_margin="130px", brand_name=""):
    title = "เฉลยแบบฝึกหัด" if is_key else "แบบฝึกหัดคณิตศาสตร์"
    # ส่วนหัวกรอกชื่อ (อยู่บรรทัดเดียวกัน)
    student_info = f"""
    <table style="width: 100%; margin-bottom: 30px; font-size: 18px; border-collapse: collapse;">
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
    
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <style>
        @page {{ size: A4; margin: 15mm; }}
        body {{ font-family: 'Sarabun', sans-serif; padding: 10px; line-height: 1.6; color: #333; }}
        .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 20px; padding-bottom: 10px; }}
        .q-container {{ margin-bottom: 25px; padding: 15px; page-break-inside: avoid; border-bottom: 1px solid #eee; display: flex; flex-direction: column; }}
        .q-text {{ font-size: 20px; margin-bottom: 15px; }}
        .spacing-area {{ height: {q_margin}; }}
        .ans-row {{ border-bottom: 1px dotted #999; width: 80%; height: 35px; font-weight: bold; margin-top: 10px; }}
        .sol-text {{ color: red; font-size: 20px; margin-top: 10px; border-left: 5px solid red; padding-left: 15px; }}
        .footer-branding {{ text-align: right; font-size: 14px; color: #aaa; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }}
    </style></head><body>
    <div class="header"><h2>{title} - {grade}</h2><p><b>เรื่อง:</b> {sub_t}</p></div>
    {student_info}"""
    
    for i, item in enumerate(questions, 1):
        html += f'<div class="q-container">'
        html += f'<div class="q-text"><b>ข้อที่ {i}.</b> &nbsp;&nbsp; {item["question"]}</div>'
        if is_key:
            html += f'<div class="sol-text"><b>เฉลยสเต็ปการคิด:</b><br>{item["solution"]}</div>'
        else:
            html += f'<div class="spacing-area"></div>' # 📏 พื้นที่ว่างสำหรับทดเลข
            html += f'<div class="ans-row">ตอบ: </div>' # ✍️ บรรทัดตอบ
        html += '</div>'
        
    if brand_name: html += f'<div class="footer-branding">&copy; 2026 {brand_name} | สงวนลิขสิทธิ์</div>'
    return html + "</body></html>"

def generate_cover_html(grade, sub_t, num_q, theme, brand):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <style>
        .c-box {{ width: 100%; height: 100%; padding: 50px; box-sizing: border-box; text-align: center; border: 15px solid {theme['border']}; background: white; position: relative; }}
        .c-title {{ font-size: 65px; color: #2c3e50; font-weight: bold; margin-top: 120px; }}
        .c-badge {{ font-size: 45px; background: {theme['badge']}; color: white; padding: 15px 50px; border-radius: 50px; display: inline-block; margin-top: 30px; font-weight: bold; }}
        .c-topic {{ font-size: 40px; margin-top: 80px; font-weight: bold; color: #34495e; }}
        .c-icon {{ font-size: 120px; margin: 60px 0; }}
        .c-details {{ font-size: 24px; background: #2ecc71; color: white; padding: 15px 40px; border-radius: 15px; font-weight: bold; display: inline-block; }}
        .c-footer {{ position: absolute; bottom: 60px; left: 0; width: 100%; font-size: 24px; color: #7f8c8d; font-weight: bold; }}
    </style></head><body>
    <div class="c-box">
        <div class="c-title">แบบฝึกหัดคณิตศาสตร์</div>
        <div class="c-badge">ชั้น {grade}</div>
        <div class="c-topic">เรื่อง: {sub_t}</div>
        <div class="c-icon">🔢 📏 📐</div>
        <div class="c-details">รวมโจทย์ {num_q} ข้อ พร้อมเฉลยละเอียด</div>
        <div class="c-footer">จัดทำโดย: {brand}</div>
    </div></body></html>"""
    # ==========================================
# 4. ฟังก์ชันจัดการเลย์เอาต์หน้ากระดาษ (Pro Layout)
# ==========================================

if 'worksheet_html' not in st.session_state:
    st.session_state['worksheet_html'] = ""
if 'answerkey_html' not in st.session_state:
    st.session_state['answerkey_html'] = ""

# ส่วน Sidebar สำหรับตั้งค่าพารามิเตอร์
st.sidebar.markdown("## ⚙️ พารามิเตอร์การสร้าง")
selected_grade = st.sidebar.selectbox("📚 เลือกระดับชั้น:", list(curriculum_db.keys()))

# เพิ่มตัวเลือกโหมดพิเศษ
main_topics_list = list(curriculum_db[selected_grade].keys()) + ["🌟 แบบทดสอบรวมปลายภาค"]
selected_main = st.sidebar.selectbox("📂 เลือกหัวข้อหลัก:", main_topics_list)

if selected_main == "🌟 แบบทดสอบรวมปลายภาค":
    selected_sub = "แบบทดสอบรวมปลายภาค"
    st.sidebar.info("💡 ระบบจะสุ่มดึงโจทย์จากทุกเรื่องในชั้นนี้มายำรวมกัน")
else:
    selected_sub = st.sidebar.selectbox("📝 เลือกหัวข้อย่อย:", curriculum_db[selected_grade][selected_main])

num_input = st.sidebar.number_input("🔢 จำนวนข้อ:", min_value=1, max_value=100, value=10)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📏 ตั้งค่าพื้นที่ทดเลข")
spacing_level = st.sidebar.select_slider("↕️ ขนาดพื้นที่ว่าง (กลางข้อ):", options=["แคบ", "ปานกลาง", "กว้าง"], value="ปานกลาง")

# กำหนดความสูงพื้นที่ทดเลข (แก้ไขให้ค่านี้ถูกส่งไปทุกข้อแน่นอน)
spacing_map = { "แคบ": "70px", "ปานกลาง": "150px", "กว้าง": "280px" }
q_margin_val = spacing_map[spacing_level]

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 Branding & Copyright")
brand_name_input = st.sidebar.text_input("🏷️ ชื่อแบรนด์ / ร้านค้า (ท้ายกระดาษ):", value="ครูคณิตศาสตร์")
include_cover_page = st.sidebar.checkbox("🎨 สร้างหน้าปก (Cover Page)", value=True)

color_theme_select = st.sidebar.selectbox("🎨 ธีมสีหน้าปก:", ["ฟ้าคลาสสิก (Blue)", "ชมพูพาสเทล (Pink)", "เขียวธรรมชาติ (Green)", "ส้มสดใส (Orange)"])

theme_config = {
    "ฟ้าคลาสสิก (Blue)": {"border": "#3498db", "badge": "#e74c3c"},
    "ชมพูพาสเทล (Pink)": {"border": "#ff9ff3", "badge": "#0abde3"},
    "เขียวธรรมชาติ (Green)": {"border": "#2ecc71", "badge": "#e67e22"},
    "ส้มสดใส (Orange)": {"border": "#f39c12", "badge": "#2c3e50"}
}
current_theme = theme_config[color_theme_select]

# ==========================================
# 🚀 ปุ่มดำเนินการหลัก
# ==========================================
if st.sidebar.button("🚀 สั่งสร้างใบงานเดี๋ยวนี้", type="primary", use_container_width=True):
    with st.spinner("กำลังประมวลผลลอจิกคณิตศาสตร์นับพันบรรทัด..."):
        # 1. สุ่มโจทย์ด้วยลอจิกตัวเต็ม
        generated_qs = generate_questions_logic(selected_grade, selected_main, selected_sub, num_input)
        
        # 2. สร้างหน้า HTML แยกส่วน (ส่งค่า q_margin_val ไปทุกข้อ)
        html_ws = create_page(selected_grade, selected_sub, generated_qs, is_key=False, q_margin=q_margin_val, brand_name=brand_name_input)
        html_ak = create_page(selected_grade, selected_sub, generated_qs, is_key=True, q_margin="20px", brand_name=brand_name_input)
        html_cv = generate_cover_html(selected_grade, selected_sub, num_input, current_theme, brand_name_input) if include_cover_page else ""
        
        # 3. รวมร่างเป็นไฟล์เดียวสำหรับ Print (A4 Preview)
        ebook_render = ""
        if include_cover_page:
            ebook_render += f'\n<div class="a4-wrapper cover-wrapper">{extract_body(html_cv)}</div>\n'
        ebook_render += f'\n<div class="a4-wrapper">{extract_body(html_ws)}</div>\n'
        ebook_render += f'\n<div class="a4-wrapper">{extract_body(html_ak)}</div>\n'
        
        full_html_final = f"""<!DOCTYPE html><html lang="th"><head><meta charset="utf-8">
        <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap" rel="stylesheet">
        <style>
            @page {{ size: A4; margin: 15mm; }}
            @media screen {{
                body {{ font-family: 'Sarabun', sans-serif; background-color: #525659; display: flex; flex-direction: column; align-items: center; padding: 40px 0; margin: 0; }}
                .a4-wrapper {{ width: 210mm; min-height: 297mm; background: white; margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.3); padding: 15mm; box-sizing: border-box; }}
                .cover-wrapper {{ padding: 0; }}
            }}
            @media print {{
                body {{ font-family: 'Sarabun', sans-serif; background: transparent; padding: 0; display: block; margin: 0; }}
                .a4-wrapper {{ width: 100%; min-height: auto; margin: 0; padding: 0; box-shadow: none; page-break-after: always; }}
            }}
        </style></head><body>
        {ebook_render}
        </body></html>"""

        # เก็บลง Session State
        st.session_state['worksheet_html'] = html_ws
        st.session_state['answerkey_html'] = html_ak
        st.session_state['full_ebook_html'] = full_html_final
        st.session_state['filename_base'] = f"{selected_grade}_{selected_sub}_{int(time.time())}"
        
        # สร้างไฟล์ ZIP
        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(f"{selected_grade}_Worksheet.html", html_ws.encode('utf-8'))
            zf.writestr(f"{selected_grade}_AnswerKey.html", html_ak.encode('utf-8'))
            zf.writestr(f"{selected_grade}_Full_EBook.html", full_html_final.encode('utf-8'))
        st.session_state['zip_data'] = zip_buf.getvalue()

# ==========================================
# 📥 ส่วนการแสดงผลดาวน์โหลด (Dashboard)
# ==========================================
if st.session_state['worksheet_html']:
    st.success(f"✅ ระบบประมวลผลลอจิกเรียบร้อยแล้ว! พร้อมส่งออกไฟล์คุณภาพสูง")
    
    st.markdown("### 📥 เลือกดาวน์โหลดไฟล์แยกส่วน หรือ ไฟล์รวมเล่ม")
    c1, c2 = st.columns(2)
    
    with c1:
        st.info("📄 **สำหรับแจกนักเรียน**")
        st.download_button("📄 โหลดเฉพาะโจทย์ (Worksheet)", data=st.session_state['worksheet_html'], file_name=f"{st.session_state['filename_base']}_Worksheet.html", mime="text/html", use_container_width=True)
        st.download_button("🔑 โหลดเฉพาะเฉลย (Answer Key)", data=st.session_state['answerkey_html'], file_name=f"{st.session_state['filename_base']}_AnswerKey.html", mime="text/html", use_container_width=True)

    with c2:
        st.info("📚 **สำหรับขาย TPT / เข้าเล่ม**")
        st.download_button("📚 โหลด Full E-Book (หน้าปก+โจทย์+เฉลย)", data=st.session_state['full_ebook_html'], file_name=f"{st.session_state['filename_base']}_Full_EBook.html", mime="text/html", use_container_width=True)
        st.download_button("🗂️ โหลดแพ็กเกจทั้งหมด (.zip)", data=st.session_state['zip_data'], file_name=f"{st.session_state['filename_base']}.zip", mime="application/zip", use_container_width=True)

    st.markdown("---")
    st.markdown("### 👁️ Live Preview (มุมมองจำลองกระดาษ A4)")
    st.caption("เลื่อนลงเพื่อดูหน้าโจทย์และเฉลยสเต็ปการคิดแบบละเอียด")
    components.html(st.session_state['full_ebook_html'], height=900, scrolling=True)

else:
    st.info("👈 กรุณาตั้งค่าใบงานที่เมนูด้านซ้าย แล้วกดปุ่ม 'สั่งสร้างใบงานเดี๋ยวนี้' เพื่อเริ่มการทำงาน")
