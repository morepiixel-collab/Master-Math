import streamlit as st
import streamlit.components.v1 as components
import random
import math
import zipfile
import io
import time
import base64

# ==========================================
# ⚙️ Configuration & Professional CSS
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
    div.stDownloadButton > button { border-radius: 8px; font-weight: bold; border: 1px solid #bdc3c7; transition: all 0.2s ease; }
    div.stDownloadButton > button:hover { border-color: #3498db; color: #3498db; }
    .main-header { background: linear-gradient(135deg, #2980b9, #2c3e50); padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem; box-shadow: 0 10px 20px rgba(0,0,0,0.15); }
    .main-header h1 { margin: 0; font-size: 2.8rem; font-weight: 800; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
    .main-header p { margin: 10px 0 0 0; font-size: 1.2rem; opacity: 0.9; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🚀 Math Worksheet Pro <span style="font-size: 20px; background: #f39c12; padding: 5px 15px; border-radius: 20px; vertical-align: middle;">Ultimate Edition</span></h1>
    <p>ระบบสร้างสื่อการสอนคณิตศาสตร์ (ป.1 - ป.6) ลำดับ: โจทย์ -> พื้นที่ทด -> ตอบ (สมบูรณ์ 100%)</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 1. ฐานข้อมูลหลักสูตร (Master Database) - ห้ามตัดเด็ดขาด
# ==========================================
curriculum_db = {
    "ป.1": {
        "จำนวนนับ 1 ถึง 100 และ 0": ["การนับทีละ 1", "การนับทีละ 10", "การอ่านและการเขียนตัวเลข", "การแสดงจำนวนในรูปความสัมพันธ์แบบส่วนย่อย-ส่วนรวม", "แบบรูปซ้ำของรูปเรขาคณิต", "การบอกอันดับที่ (รถแข่ง)", "หลัก ค่าของเลขโดดในแต่ละหลัก และรูปกระจาย", "การเปรียบเทียบจำนวน (> <)",  "การเปรียบเทียบจำนวน (= ≠)", "การเรียงลำดับจำนวน (น้อยไปมาก)", "การเรียงลำดับจำนวน (มากไปน้อย)"],
        "การบวก การลบ": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)"],
        "แผนภูมิรูปภาพ": ["การอ่านแผนภูมิรูปภาพ"]
    },
    "ป.2": {
        "จำนวนนับไม่เกิน 1,000 และ 0": ["การนับทีละ 2 ทีละ 5 ทีละ 10 และทีละ 100", "การอ่านและการเขียนตัวเลข", "จำนวนคู่ จำนวนคี่", "หลัก ค่าของเลขโดด และรูปกระจาย", "การเปรียบเทียบจำนวน (> <)", "การเรียงลำดับจำนวน (น้อยไปมาก)", "การเรียงลำดับจำนวน (มากไปน้อย)"],
        "เวลาและการวัด": ["การบอกเวลาเป็นนาฬิกาและนาที", "การอ่านน้ำหนักจากเครื่องชั่งสปริง"],
        "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การคูณ (แบบตั้งหลัก)", "การหารพื้นฐาน"],
        "แผนภูมิรูปภาพ": ["การอ่านแผนภูมิรูปภาพ"]
    },
    "ป.3": {
        "จำนวนนับและเศษส่วน": ["การอ่าน การเขียนตัวเลข", "หลัก ค่าของเลขโดด และรูปกระจาย", "การเปรียบเทียบจำนวน (> <)", "การเรียงลำดับจำนวน (น้อยไปมาก)", "การเรียงลำดับจำนวน (มากไปน้อย)", "การอ่านและเขียนเศษส่วน", "การบวกลบเศษส่วน (ตัวส่วนเท่ากัน)"],
        "เวลา เงิน และการวัด": ["การบอกเวลาเป็นนาฬิกาและนาที", "การบอกจำนวนเงินทั้งหมด", "การอ่านน้ำหนักจากเครื่องชั่งสปริง"],
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
        "เศษส่วน": ["การบวกและการลบเศษส่วน", "การคูณและการหารเศษส่วน"],
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

box_html = "<span style='display: inline-block; width: 22px; height: 22px; border: 2px solid #333; border-radius: 3px; vertical-align: middle; margin-left: 5px; position: relative; top: -2px;'></span>"

# 🟢 ฟังก์ชันกราฟิกดั้งเดิม (ห้ามตัดทิ้ง)
def generate_vertical_table_html(a, b, op, result=None, is_key=False):
    num_len = max(len(str(a)), len(str(b)), len(str(result)) if result else 0) + 1
    str_a = str(a).rjust(num_len, " "); str_b = str(b).rjust(num_len, " ")
    strike = [False] * num_len; top_marks = [""] * num_len
    if is_key:
        if op == '+':
            carry = 0
            for i in range(num_len - 1, -1, -1):
                da = int(str_a[i]) if str_a[i].strip() else 0; db = int(str_b[i]) if str_b[i].strip() else 0
                s = da + db + carry; carry = s // 10
                if carry > 0 and i > 0: top_marks[i-1] = str(carry)
        elif op == '-':
            a_chars, b_chars = list(str_a), list(str_b); a_digits = [int(c) if c.strip() else 0 for c in a_chars]; b_digits = [int(c) if c.strip() else 0 for c in b_chars]
            for i in range(num_len - 1, -1, -1):
                if a_digits[i] < b_digits[i]:
                    for j in range(i-1, -1, -1):
                        if a_digits[j] > 0 and str_a[j].strip() != "":
                            strike[j] = True; a_digits[j] -= 1; top_marks[j] = str(a_digits[j])
                            for k in range(j+1, i): strike[k] = True; a_digits[k] = 9; top_marks[k] = "9"
                            strike[i] = True; a_digits[i] += 10; top_marks[i] = str(a_digits[i]); break
        elif op == '×':
            b_val, carry = b, 0; a_digits = [int(c) if c.strip() else 0 for c in str_a]
            for i in range(num_len - 1, -1, -1):
                if str_a[i].strip() == "": 
                    if carry > 0: top_marks[i] = str(carry); carry = 0
                    continue
                prod = a_digits[i] * b_val + carry; carry = prod // 10
                if carry > 0 and i > 0: top_marks[i-1] = str(carry)
    a_tds = "".join([f'<td style="width: 35px; text-align: center; height: 50px; vertical-align: bottom;">{str_a[i].strip()}</td>' for i in range(num_len)])
    b_tds = "".join([f'<td style="width: 35px; text-align: center; border-bottom: 2px solid #000; height: 40px; vertical-align: bottom;">{str_b[i].strip()}</td>' for i in range(num_len)])
    res_tds = "".join([f'<td style="width: 35px; text-align: center; color: red; font-weight: bold; height: 45px; vertical-align: bottom;">{str(result).rjust(num_len, " ")[i].strip()}</td>' if is_key else f'<td style="width: 35px; height: 45px;"></td>' for i in range(num_len)])
    return f"""<div style="display: inline-block; font-family: 'Sarabun', sans-serif; font-size: 38px; line-height: 1.1; margin: 10px 20px;"><table style="border-collapse: collapse; margin-left: auto; margin-right: auto;"><tr><td style="width: 20px;"></td>{a_tds}<td style="width: 50px; text-align: center; vertical-align: middle;" rowspan="2">{op}</td></tr><tr><td></td>{b_tds}</tr><tr><td></td>{res_tds}<td></td></tr><tr><td></td><td colspan="{num_len}" style="border-bottom: 6px double #000; height: 10px;"></td><td></td></tr></table></div>"""

def generate_fraction_html(num, den):
    return f"""<div style="display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; margin: 0 8px; font-family: 'Sarabun', sans-serif;"><span style="font-size: 26px; font-weight: bold; border-bottom: 3px solid #000; padding: 0 5px; line-height: 1.1;">{num}</span><span style="font-size: 26px; font-weight: bold; padding: 0 5px; line-height: 1.1;">{den}</span></div>"""

def generate_short_division_html(a, b, mode="ห.ร.ม."):
    factors = []; ca, cb = a, b; steps_html = ""
    while True:
        found = False
        for i in range(2, min(ca, cb) + 1):
            if ca % i == 0 and cb % i == 0:
                steps_html += f"<tr><td style='text-align: right; padding-right: 10px; font-weight: bold; color: red;'>{i}</td><td style='border-left: 2px solid #000; border-bottom: 2px solid #000; padding: 5px 15px; text-align: center;'>{ca}</td><td style='border-bottom: 2px solid #000; padding: 5px 15px; text-align: center;'>{cb}</td></tr>"
                factors.append(i); ca //= i; cb //= i; found = True; break
        if not found: break
    if not factors: return f"<br><b>{mode} = 1</b>"
    steps_html += f"<tr><td></td><td style='padding: 5px 15px; text-align: center;'>{ca}</td><td style='padding: 5px 15px; text-align: center;'>{cb}</td></tr>"
    ans = math.prod(factors) if mode=="ห.ร.ม." else math.prod(factors) * ca * cb
    return f"<table style='margin: 10px 0; font-size: 24px; border-collapse: collapse; color: #333;'>{steps_html}</table><b>{mode} = {ans}</b>"

def generate_long_division_step_by_step_html(divisor, dividend, is_key=False):
    div_str = str(dividend); qn = dividend // divisor
    eq_html = f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #2c3e50;'>ประโยคสัญลักษณ์: {dividend:,} ÷ {divisor} = {box_html}</div>"
    if not is_key:
        d_tds = "".join([f'<td style="width: 35px; text-align: center; border-top: 3px solid #000; {"border-left: 3px solid #000;" if i==0 else ""} font-size: 38px;">{c}</td>' for i, c in enumerate(div_str)])
        return f"{eq_html}<div style=\"display: inline-block; font-family: 'Sarabun', sans-serif; line-height: 1.2;\"><table style=\"border-collapse: collapse;\"><tr><td style=\"border: none; text-align: right; padding-right: 12px; vertical-align: bottom; font-size: 38px;\">{divisor}</td>{d_tds}</tr></table></div>"
    return f"{eq_html}<br><b style='color: red; font-size: 24px;'>คำตอบคือ {qn:,}</b>"
    # (ต่อจากส่วนที่ 1)
def generate_questions_logic(grade, main_t, sub_t, num_q):
    questions = []; seen = set(); limit_map = {"ป.1": 100, "ป.2": 1000, "ป.3": 100000, "ป.4": 1000000, "ป.5": 9000000, "ป.6": 9000000}; limit = limit_map.get(grade, 100)
    for _ in range(num_q):
        q, sol, attempts = "", "", 0
        while attempts < 300:
            act_sub = sub_t
            if sub_t == "แบบทดสอบรวมปลายภาค":
                all_m = list(curriculum_db[grade].keys()); rm = random.choice(all_m); act_sub = random.choice(curriculum_db[grade][rm])
            
            if "ห.ร.ม." in act_sub:
                a, b = random.randint(12, 60), random.randint(12, 60); q = f"จงหา ห.ร.ม. ของ <b>{a}</b> และ <b>{b}</b>"; sol = generate_short_division_html(a, b, "ห.ร.ม.")
            elif "ค.ร.น." in act_sub:
                a, b = random.randint(4, 30), random.randint(4, 30); q = f"จงหา ค.ร.น. ของ <b>{a}</b> และ <b>{b}</b>"; sol = generate_short_division_html(a, b, "ค.ร.น.")
            elif "ตั้งหลัก" in act_sub:
                a, b = random.randint(100, 999), random.randint(10, 99); op = '+' if 'บวก' in act_sub else ('-' if 'ลบ' in act_sub else '×'); res = a+b if op=='+' else (a-b if op=='-' else a*b)
                q = generate_vertical_table_html(a, b, op, is_key=False); sol = generate_vertical_table_html(a, b, op, result=res, is_key=True)
            elif "หารยาว" in act_sub:
                ds, dvd = random.randint(2, 9), random.randint(100, 900); q = generate_long_division_step_by_step_html(ds, dvd, False); sol = generate_long_division_step_by_step_html(ds, dvd, True)
            elif "อัตราส่วนที่เท่ากัน" in act_sub:
                a, b, m = random.randint(2, 9), random.randint(2, 9), random.randint(2, 9); while a==b: b=random.randint(2,9)
                c, d = a*m, b*m; q = f"จงหาเลขในช่องว่าง: {a} : {b} = {c} : {box_html}"; sol = f"<b>ตอบ: {d}</b>"
            elif "โจทย์ปัญหาอัตราส่วน" in act_sub:
                scenarios = [("นักเรียนชาย", "นักเรียนหญิง", "คน"), ("น้ำหวาน", "น้ำเปล่า", "มล."), ("ปากกา", "ดินสอ", "ด้าม")]
                it1, it2, unit = random.choice(scenarios); a, b = random.randint(2, 7), random.randint(2, 7); while a==b: b=random.randint(2,7)
                m = random.randint(5, 20); v1 = a*m; v2 = b*m; q = f"อัตราส่วน {it1} ต่อ {it2} คือ {a}:{b} ถ้ามี {it1} {v1} {unit} จะมี {it2} กี่ {unit}?"; sol = f"<b>ตอบ: {v2} {unit}</b>"
            elif "การแก้สมการ" in act_sub:
                a, x, b = random.randint(2, 9), random.randint(2, 15), random.randint(1, 20); c = a*x + b; q = f"แก้สมการ: {a}x + {b} = {c}"; sol = f"<b>ตอบ: x = {x}</b>"
            else:
                a, b = random.randint(1, limit//2), random.randint(1, limit//2); q = f"จงหาผลลัพธ์ของ {a:,} + {b:,} = {box_html}"; sol = f"<b>ตอบ: {a+b:,}</b>"
            if q not in seen: seen.add(q); questions.append({"question": q, "solution": sol}); break
            attempts += 1
    return questions

def extract_body(html_str):
    try: return html_str.split('<body>')[1].split('</body>')[0]
    except: return html_str

def create_page(grade, sub_t, questions, is_key=False, q_margin="120px", brand_name=""):
    title = "เฉลยแบบฝึกหัด" if is_key else "แบบฝึกหัดคณิตศาสตร์"
    student_info = f"""<table style="width: 100%; margin-bottom: 30px; font-size: 18px; border-collapse: collapse;"><tr><td style="width: 1%; white-space: nowrap; padding-right: 5px;"><b>ชื่อ-สกุล</b></td><td style="border-bottom: 2px dotted #999; width: 60%;"></td><td style="width: 1%; white-space: nowrap; padding-left: 20px; padding-right: 5px;"><b>ชั้น</b></td><td style="border-bottom: 2px dotted #999; width: 15%;"></td><td style="width: 1%; white-space: nowrap; padding-left: 20px; padding-right: 5px;"><b>เลขที่</b></td><td style="border-bottom: 2px dotted #999; width: 15%;"></td></tr></table>""" if not is_key else ""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
        @page {{ size: A4; margin: 15mm; }}
        body {{ font-family: 'Sarabun', sans-serif; padding: 10px; line-height: 1.6; color: #333; }}
        .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 20px; padding-bottom: 10px; }}
        .q-container {{ margin-bottom: 25px; padding: 15px; page-break-inside: avoid; border-bottom: 1px solid #eee; display: flex; flex-direction: column; }}
        .q-text {{ font-size: 20px; margin-bottom: 15px; }}
        .spacing-area {{ height: {q_margin}; }}
        .ans-row {{ border-bottom: 1px dotted #999; width: 80%; height: 35px; font-weight: bold; margin-top: 10px; }}
        .sol-text {{ color: red; font-size: 20px; margin-top: 10px; }}
    </style></head><body><div class="header"><h2>{title} - {grade}</h2><p><b>เรื่อง:</b> {sub_t}</p></div>{student_info}"""
    for i, item in enumerate(questions, 1):
        html += f'<div class="q-container"><div class="q-text"><b>ข้อที่ {i}.</b> &nbsp;&nbsp; {item["question"]}</div>'
        if is_key: html += f'<div class="sol-text"><b>เฉลย:</b> {item["solution"]}</div>'
        else: html += f'<div class="spacing-area"></div><div class="ans-row">ตอบ: </div>'
        html += '</div>'
    if brand_name: html += f'<div style="text-align:right; font-size:14px; color:#aaa;">&copy; 2026 {brand_name}</div>'
    return html + "</body></html>"

def generate_cover_html(grade, sub_t, num_q, theme, brand):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
        .c-box {{ width: 100%; height: 100%; padding: 50px; box-sizing: border-box; text-align: center; border: 15px solid {theme['border']}; background: white; }}
        .c-title {{ font-size: 65px; color: #2c3e50; font-weight: bold; margin-top: 120px; }}
        .c-badge {{ font-size: 45px; background: {theme['badge']}; color: white; padding: 15px 50px; border-radius: 50px; display: inline-block; margin-top: 30px; font-weight: bold; }}
        .c-topic {{ font-size: 40px; margin-top: 80px; font-weight: bold; color: #34495e; }}
        .c-footer {{ position: absolute; bottom: 60px; left: 0; width: 100%; font-size: 24px; color: #7f8c8d; font-weight: bold; }}
    </style></head><body><div class="c-box"><div class="c-title">แบบฝึกหัดคณิตศาสตร์</div><div class="c-badge">ชั้น {grade}</div><div class="c-topic">เรื่อง: {sub_t}</div><div style="font-size:100px; margin:50px;">🔢 📐</div><div class="c-footer">จัดทำโดย: {brand}</div></div></body></html>"""

st.sidebar.markdown("## ⚙️ ตั้งค่า")
g = st.sidebar.selectbox("📚 ระดับชั้น:", list(curriculum_db.keys()))
ms = list(curriculum_db[g].keys()) + ["🌟 แบบทดสอบรวมปลายภาค"]
mt = st.sidebar.selectbox("📂 หัวข้อหลัก:", ms)
st_sel = "แบบทดสอบรวมปลายภาค" if mt == "🌟 แบบทดสอบรวมปลายภาค" else st.sidebar.selectbox("📝 หัวข้อย่อย:", curriculum_db[g][mt])
nq = st.sidebar.number_input("🔢 จำนวนข้อ:", 1, 100, 10)
sp = st.sidebar.select_slider("↕️ พื้นที่ทดเลข:", ["แคบ", "ปานกลาง", "กว้าง"], "ปานกลาง")
mv = {"แคบ": "70px", "ปานกลาง": "140px", "กว้าง": "280px"}[sp]
br = st.sidebar.text_input("🏷️ แบรนด์:", "ครู Pro")
tm = st.sidebar.selectbox("🎨 สี:", ["Blue", "Pink", "Green"])
ths = {"Blue": {"border": "#3498db", "badge": "#e74c3c"}, "Pink": {"border": "#ff9ff3", "badge": "#0abde3"}, "Green": {"border": "#2ecc71", "badge": "#e67e22"}}

if st.sidebar.button("🚀 สร้างใบงาน Pro", type="primary", use_container_width=True):
    qs = generate_questions_logic(g, mt, st_sel, nq)
    w_h = create_page(g, st_sel, qs, False, mv, br)
    k_h = create_page(g, st_sel, qs, True, "10px", br)
    c_h = generate_cover_html(g, st_sel, nq, ths[tm], br)
    eb = f'<div class="a4-wrapper c-wrapper">{extract_body(c_h)}</div><div class="a4-wrapper">{extract_body(w_h)}</div><div class="a4-wrapper">{extract_body(k_h)}</div>'
    final = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
        @page {{ size: A4; margin: 15mm; }}
        @media screen {{ body {{ background: #525659; display: flex; flex-direction: column; align-items: center; padding: 40px 0; }}
        .a4-wrapper {{ width: 210mm; min-height: 297mm; background: white; margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.3); padding: 15mm; box-sizing: border-box; }} .c-wrapper {{ padding: 0; }} }}
        @media print {{ body {{ background: white; }} .a4-wrapper {{ width: 100%; margin: 0; padding: 0; box-shadow: none; page-break-after: always; }} }}
    </style></head><body>{eb}</body></html>"""
    st.session_state['f_h'] = final
    st.session_state['w_h'] = w_h
    st.session_state['k_h'] = k_h

if 'f_h' in st.session_state:
    st.success("✅ สร้างใบงานเสร็จสมบูรณ์!")
    c1, c2 = st.columns(2)
    with c1: st.download_button("📄 โหลดโจทย์", data=st.session_state['w_h'], file_name="Worksheet.html", mime="text/html", use_container_width=True)
    with c2: st.download_button("📚 โหลด E-Book", data=st.session_state['f_h'], file_name="EBook.html", mime="text/html", use_container_width=True)
    st.markdown("### 👁️ Live Preview")
    components.html(st.session_state['f_h'], height=800, scrolling=True)
