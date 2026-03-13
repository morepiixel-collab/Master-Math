import streamlit as st
import streamlit.components.v1 as components
import random
import math
import zipfile
import io
import time
import base64

# ==========================================
# ⚙️ Web App Configuration & CSS Professional UI
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

st.markdown('<div class="main-header"><h1>🚀 Math Worksheet Pro Ultimate</h1><p>จัดลำดับ: โจทย์ -> พื้นที่ทด -> ตอบ (แก้บั๊กข้อ 1 และ Syntax เรียบร้อยแล้ว)</p></div>', unsafe_allow_html=True)

# ==========================================
# 1. ฐานข้อมูลหลักสูตร (Master Database)
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
# ==========================================
# 2. ฟังก์ชันสมองกลสร้างโจทย์และกราฟิก (Full Logic)
# ==========================================

def generate_vertical_table_html(a, b, op, result=None, is_key=False):
    num_len = max(len(str(a)), len(str(b)), len(str(result)) if result else 0) + 1
    str_a = str(a).rjust(num_len, " ")
    str_b = str(b).rjust(num_len, " ")
    strike = [False] * num_len
    top_marks = [""] * num_len
    
    if is_key:
        if op == '+':
            carry = 0
            for i in range(num_len - 1, -1, -1):
                da = int(str_a[i]) if str_a[i].strip() else 0
                db = int(str_b[i]) if str_b[i].strip() else 0
                s = da + db + carry
                carry = s // 10
                if carry > 0 and i > 0:
                    top_marks[i-1] = str(carry)
        elif op == '-':
            a_digits = [int(c) if c.strip() else 0 for c in list(str_a)]
            b_digits = [int(c) if c.strip() else 0 for c in list(str_b)]
            for i in range(num_len - 1, -1, -1):
                if a_digits[i] < b_digits[i]:
                    for j in range(i-1, -1, -1):
                        if a_digits[j] > 0 and str_a[j].strip() != "":
                            strike[j] = True
                            a_digits[j] -= 1
                            top_marks[j] = str(a_digits[j])
                            for k in range(j+1, i):
                                strike[k] = True
                                a_digits[k] = 9
                                top_marks[k] = "9"
                            strike[i] = True
                            a_digits[i] += 10
                            top_marks[i] = str(a_digits[i])
                            break
        elif op == '×':
            a_digits = [int(c) if c.strip() else 0 for c in str_a]
            carry = 0
            for i in range(num_len - 1, -1, -1):
                if str_a[i].strip() == "":
                    if carry > 0:
                        top_marks[i] = str(carry)
                        carry = 0
                    continue
                prod = a_digits[i] * b + carry
                carry = prod // 10
                if carry > 0 and i > 0:
                    top_marks[i-1] = str(carry)

    a_tds = ""
    for i in range(num_len):
        val = str_a[i].strip()
        td_content = val
        if val:
            mark = top_marks[i]
            if strike[i] and is_key:
                td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span style="text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;">{val}</span></div>'
            elif mark and is_key:
                td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span>{val}</span></div>'
        a_tds += f'<td style="width: 35px; text-align: center; height: 50px; vertical-align: bottom;">{td_content}</td>'
        
    b_tds = ""
    for i in range(num_len):
        b_tds += f'<td style="width: 35px; text-align: center; border-bottom: 2px solid #000; height: 40px; vertical-align: bottom;">{str_b[i].strip()}</td>'

    res_tds = ""
    if is_key and result is not None:
        str_r = str(result).rjust(num_len, " ")
        for i in range(num_len):
            res_tds += f'<td style="width: 35px; text-align: center; color: red; font-weight: bold; height: 45px; vertical-align: bottom;">{str_r[i].strip()}</td>'
    else:
        for i in range(num_len):
            res_tds += f'<td style="width: 35px; height: 45px;"></td>'

    return f"""
    <div style="display: inline-block; font-family: 'Sarabun', sans-serif; font-size: 38px; line-height: 1.1; margin: 10px 20px;">
        <table style="border-collapse: collapse; margin-left: auto; margin-right: auto;">
            <tr><td style="width: 20px;"></td>{a_tds}<td style="width: 50px; text-align: center; vertical-align: middle;" rowspan="2">{op}</td></tr>
            <tr><td></td>{b_tds}</tr>
            <tr><td></td>{res_tds}<td></td></tr>
            <tr><td></td><td colspan="{num_len}" style="border-bottom: 6px double #000; height: 10px;"></td><td></td></tr>
        </table>
    </div>
    """

def generate_fraction_html(num, den):
    return f"""<div style="display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; margin: 0 8px; font-family: 'Sarabun', sans-serif;"><span style="font-size: 26px; font-weight: bold; border-bottom: 3px solid #000; padding: 0 5px; line-height: 1.1;">{num}</span><span style="font-size: 26px; font-weight: bold; padding: 0 5px; line-height: 1.1;">{den}</span></div>"""

def generate_short_division_html(a, b, mode="ห.ร.ม."):
    factors = []
    ca = a
    cb = b
    steps_html = ""
    while True:
        found = False
        for i in range(2, min(ca, cb) + 1):
            if ca % i == 0 and cb % i == 0:
                steps_html += f"<tr><td style='text-align: right; padding-right: 10px; font-weight: bold; color: red;'>{i}</td><td style='border-left: 2px solid #000; border-bottom: 2px solid #000; padding: 5px 15px; text-align: center;'>{ca}</td><td style='border-bottom: 2px solid #000; padding: 5px 15px; text-align: center;'>{cb}</td></tr>"
                factors.append(i)
                ca = ca // i
                cb = cb // i
                found = True
                break
        if not found:
            break
    
    if not factors:
        return f"<br><b>{mode} = 1</b>"
    
    steps_html += f"<tr><td></td><td style='padding: 5px 15px; text-align: center;'>{ca}</td><td style='padding: 5px 15px; text-align: center;'>{cb}</td></tr>"
    
    if mode == "ห.ร.ม.":
        ans = math.prod(factors)
    else:
        ans = math.prod(factors) * ca * cb
        
    return f"<table style='margin: 10px 0; font-size: 24px; border-collapse: collapse; color: #333;'>{steps_html}</table><b>{mode} = {ans}</b>"

def generate_long_division_step_by_step_html(divisor, dividend, is_key=False):
    div_str = str(dividend)
    qn = dividend // divisor
    eq_html = f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #2c3e50;'>ประโยคสัญลักษณ์: {dividend:,} ÷ {divisor} = {box_html}</div>"
    if not is_key:
        d_tds = ""
        for i, c in enumerate(div_str):
            border_l = "border-left: 3px solid #000;" if i == 0 else ""
            d_tds += f'<td style="width: 35px; text-align: center; border-top: 3px solid #000; {border_l} font-size: 38px;">{c}</td>'
        return f"{eq_html}<div style=\"display: inline-block; font-family: 'Sarabun', sans-serif; line-height: 1.2;\"><table style=\"border-collapse: collapse;\"><tr><td style=\"border: none; text-align: right; padding-right: 12px; vertical-align: bottom; font-size: 38px;\">{divisor}</td>{d_tds}</tr></table></div>"
    return f"{eq_html}<br><b style='color: red; font-size: 24px;'>คำตอบคือ {qn:,}</b>"

def generate_questions_logic(grade, main_t, sub_t, num_q):
    questions = []
    seen = set()
    limit_map = {"ป.1": 100, "ป.2": 1000, "ป.3": 100000, "ป.4": 1000000, "ป.5": 9000000, "ป.6": 9000000}
    limit = limit_map.get(grade, 100)
    for _ in range(num_q):
        q = ""
        sol = ""
        attempts = 0
        while attempts < 300:
            act_sub = sub_t
            if sub_t == "แบบทดสอบรวมปลายภาค":
                all_m = list(curriculum_db[grade].keys())
                rm = random.choice(all_m)
                act_sub = random.choice(curriculum_db[grade][rm])
            
            if "ห.ร.ม." in act_sub:
                a = random.randint(12, 60)
                b = random.randint(12, 60)
                q = f"จงหา ห.ร.ม. ของ <b>{a}</b> และ <b>{b}</b>"
                sol = generate_short_division_html(a, b, "ห.ร.ม.")
            elif "ค.ร.น." in act_sub:
                a = random.randint(4, 30)
                b = random.randint(4, 30)
                q = f"จงหา ค.ร.น. ของ <b>{a}</b> และ <b>{b}</b>"
                sol = generate_short_division_html(a, b, "ค.ร.น.")
            elif "ตั้งหลัก" in act_sub:
                a = random.randint(100, 999)
                b = random.randint(10, 99)
                if 'บวก' in act_sub:
                    op = '+'
                    res = a + b
                elif 'ลบ' in act_sub:
                    op = '-'
                    if a < b:
                        a, b = b, a
                    res = a - b
                else:
                    op = '×'
                    res = a * b
                q = generate_vertical_table_html(a, b, op, is_key=False)
                sol = generate_vertical_table_html(a, b, op, result=res, is_key=True)
            elif "หารยาว" in act_sub:
                ds = random.randint(2, 9)
                qn_val = random.randint(100, 900)
                dvd = ds * qn_val
                q = generate_long_division_step_by_step_html(ds, dvd, False)
                sol = generate_long_division_step_by_step_html(ds, dvd, True)
            elif "อัตราส่วนที่เท่ากัน" in act_sub:
                a = random.randint(2, 9)
                b = random.randint(2, 9)
                while a == b:
                    b = random.randint(2, 9)
                m = random.randint(2, 9)
                c = a * m
                d = b * m
                q = f"จงหาเลขในช่องว่าง: {a} : {b} = {c} : {box_html}"
                sol = f"<b>ตอบ: {d}</b>"
            elif "แก้สมการ" in act_sub:
                a = random.randint(2, 9)
                x = random.randint(2, 15)
                b = random.randint(1, 20)
                c = a * x + b
                q = f"แก้สมการเพื่อหาค่า x: {a}x + {b} = {c}"
                sol = f"<b>ตอบ: x = {x}</b>"
            else:
                a = random.randint(1, limit // 2)
                b = random.randint(1, limit // 2)
                q = f"จงหาผลลัพธ์ของ {a:,} + {b:,} = {box_html}"
                sol = f"<b>ตอบ: {a+b:,}</b>"
                
            if q not in seen:
                seen.add(q)
                questions.append({"question": q, "solution": sol})
                break
            attempts += 1
    return questions
    # ==========================================
# 3. HTML Generation Engine (จัดลำดับตามสั่ง)
# ==========================================
def extract_body(html_str):
    try:
        return html_str.split('<body>')[1].split('</body>')[0]
    except:
        return html_str

def create_page(grade, sub_t, questions, is_key=False, q_margin="130px", brand_name=""):
    title = "เฉลยแบบฝึกหัด" if is_key else "แบบฝึกหัดคณิตศาสตร์"
    
    # ส่วนข้อมูลส่วนตัว (จัดให้อยู่บรรทัดเดียวกัน)
    student_info = f"""
    <table style="width: 100%; margin-bottom: 30px; font-size: 18px; border-collapse: collapse; border: none;">
        <tr style="border: none;">
            <td style="width: 1%; white-space: nowrap; padding-right: 5px; border: none;"><b>ชื่อ-สกุล</b></td>
            <td style="border-bottom: 2px dotted #999; width: 60%; border-top: none; border-left: none; border-right: none;"></td>
            <td style="width: 1%; white-space: nowrap; padding-left: 20px; padding-right: 5px; border: none;"><b>ชั้น</b></td>
            <td style="border-bottom: 2px dotted #999; width: 15%; border-top: none; border-left: none; border-right: none;"></td>
            <td style="width: 1%; white-space: nowrap; padding-left: 20px; padding-right: 5px; border: none;"><b>เลขที่</b></td>
            <td style="border-bottom: 2px dotted #999; width: 15%; border-top: none; border-left: none; border-right: none;"></td>
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
        .spacing-area {{ height: {q_margin}; width: 100%; }}
        .ans-row {{ border-bottom: 1px dotted #999; width: 80%; height: 35px; font-weight: bold; margin-top: 10px; }}
        .sol-text {{ color: red; font-size: 20px; margin-top: 10px; border-left: 5px solid red; padding-left: 15px; }}
        .footer-branding {{ text-align: right; font-size: 14px; color: #aaa; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }}
    </style></head><body>
    <div class="header"><h2>{title} - {grade}</h2><p><b>เรื่อง:</b> {sub_t}</p></div>
    {student_info}"""
    
    for i, item in enumerate(questions, 1):
        # 💡 ลำดับ: ข้อที่ -> ตัวโจทย์ -> พื้นที่ว่าง -> บรรทัดตอบ
        html += f'<div class="q-container">'
        html += f'<div class="q-text"><b>ข้อที่ {i}.</b> &nbsp;&nbsp; {item["question"]}</div>'
        if is_key:
            html += f'<div class="sol-text"><b>เฉลย:</b><br>{item["solution"]}</div>'
        else:
            # พื้นที่ทดเลข (Spacing) จะปรากฏในทุกข้อ รวมถึงข้อ 1
            html += f'<div class="spacing-area"></div>' 
            html += f'<div class="ans-row">ตอบ: </div>'
        html += '</div>'
        
    if brand_name: 
        html += f'<div class="footer-branding">&copy; 2026 {brand_name} | สงวนลิขสิทธิ์</div>'
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
        <div class="c-icon">🔢 📐 ✏️</div>
        <div class="c-details">รวมโจทย์ {num_q} ข้อ พร้อมเฉลยละเอียด</div>
        <div class="c-footer">จัดทำโดย: {brand}</div>
    </div></body></html>"""

# ==========================================
# 4. Streamlit UI Logic
# ==========================================
st.sidebar.markdown("## ⚙️ ตั้งค่าใบงาน")
grade_val = st.sidebar.selectbox("📚 ระดับชั้น:", list(curriculum_db.keys()))
mains = list(curriculum_db[grade_val].keys()) + ["🌟 แบบทดสอบรวมปลายภาค"]
main_t_val = st.sidebar.selectbox("📂 หัวข้อหลัก:", mains)

if main_t_val == "🌟 แบบทดสอบรวมปลาย髮":
    sub_t_val = "แบบทดสอบรวมปลายภาค"
    st.sidebar.info("💡 ระบบจะสุ่มดึงโจทย์จากทุกเรื่องในชั้นนี้มายำรวมกัน")
else:
    sub_t_val = st.sidebar.selectbox("📝 หัวข้อย่อย:", curriculum_db[grade_val][main_t_val])

num_q_val = st.sidebar.number_input("🔢 จำนวนข้อ:", 1, 100, 10)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📏 พื้นที่ว่างสำหรับทดเลข")
spacing_val = st.sidebar.select_slider("↕️ ขนาดช่องว่าง (กลางข้อ):", options=["แคบ", "ปานกลาง", "กว้าง"], value="ปานกลาง")
px_map = {"แคบ": "70px", "ปานกลาง": "140px", "กว้าง": "280px"}
m_px = px_map[spacing_val]

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 Branding & Theme")
brand_val = st.sidebar.text_input("🏷️ ชื่อผู้สอน/ร้านค้า:", value="ครูคณิตศาสตร์")
include_cov = st.sidebar.checkbox("🎨 สร้างหน้าปก (Cover)", value=True)
theme_val = st.sidebar.selectbox("🎨 ธีมสีหน้าปก:", ["Blue", "Pink", "Green", "Orange"])
themes_db = {
    "Blue": {"border": "#3498db", "badge": "#e74c3c"},
    "Pink": {"border": "#ff9ff3", "badge": "#0abde3"},
    "Green": {"border": "#2ecc71", "badge": "#e67e22"},
    "Orange": {"border": "#f39c12", "badge": "#2c3e50"}
}

if st.sidebar.button("🚀 สั่งสร้างใบงานเดี๋ยวนี้", type="primary", use_container_width=True):
    with st.spinner("กำลังประมวลผลลอจิกคณิตศาสตร์..."):
        # 1. สุ่มโจทย์
        qs = generate_questions_logic(grade_val, main_t_val, sub_t_val, num_q_val)
        # 2. สร้าง HTML
        ws_h = create_page(grade_val, sub_t_val, qs, False, m_px, brand_val)
        ak_h = create_page(grade_val, sub_t_val, qs, True, "10px", brand_val)
        cv_h = generate_cover_html(grade_val, sub_t_val, num_q_val, themes_db[theme_val], brand_val) if include_cov else ""
        
        # 3. รวมร่าง
        eb = ""
        if include_cov: eb += f'<div class="a4-wrapper c-wrapper">{extract_body(cv_h)}</div>'
        eb += f'<div class="a4-wrapper">{extract_body(ws_h)}</div><div class="a4-wrapper">{extract_body(ak_h)}</div>'
        
        final_html_code = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
        <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap" rel="stylesheet">
        <style>
            @page {{ size: A4; margin: 15mm; }}
            @media screen {{
                body {{ background: #525659; display: flex; flex-direction: column; align-items: center; padding: 40px 0; margin:0; }}
                .a4-wrapper {{ width: 210mm; min-height: 297mm; background: white; margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.3); padding: 15mm; box-sizing: border-box; position: relative; }}
                .c-wrapper {{ padding: 0; }}
            }}
            @media print {{ body {{ background: white; }} .a4-wrapper {{ width: 100%; margin: 0; padding: 0; box-shadow: none; page-break-after: always; }} }}
        </style></head><body>{eb}</body></html>"""
        
        st.session_state['full_out'] = final_html_code
        st.session_state['ws_only'] = ws_h
        st.session_state['ak_only'] = ak_h
        st.session_state['fname'] = f"{grade_val}_{sub_t_val}_{int(time.time())}"

if 'full_out' in st.session_state:
    st.success("✅ สร้างใบงาน Pro เสร็จสมบูรณ์!")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📄 โหลดโจทย์ (Worksheet)", data=st.session_state['ws_only'], file_name="Worksheet.html", mime="text/html", use_container_width=True)
    with c2:
        st.download_button("📚 โหลดรวมเล่ม (Full E-Book)", data=st.session_state['full_out'], file_name="Full_EBook.html", mime="text/html", use_container_width=True)
    st.markdown("---")
    st.markdown("### 👁️ Live Preview")
    components.html(st.session_state['full_out'], height=800, scrolling=True)
