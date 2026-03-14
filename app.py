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
st.set_page_config(page_title="Math Generator Pro Ultimate", page_icon="🚀", layout="wide")

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
    <h1>🚀 Math Worksheet Pro <span style="font-size: 20px; background: #f39c12; padding: 5px 15px; border-radius: 20px; vertical-align: middle;">Ultimate Edition</span></h1>
    <p>ระบบสร้างสื่อการสอน ป.1-ป.6 + ข้อสอบแข่งขัน TMC (ทุกระดับชั้น) พร้อมภาพอธิบายเฉลย (Visual Models) ขั้นเทพ!</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 1. ฐานข้อมูลหลักสูตร (Master Database)
# ==========================================
tmc_lower = ["ปริศนาตัวเลขซ่อนแอบ", "สัตว์ปีนบ่อ", "ตรรกะตาชั่งสมดุล", "ปัญหาผลรวม-ผลต่าง", "ตรรกะการจับมือ (ทักทาย)", "โปรโมชั่นแลกของ", "หยิบของในที่มืด", "คิววงกลมมรณะ", "จำนวนขาและหัวสัตว์"]
tmc_mid = ["ผลบวกจำนวนเรียงกัน (Gauss)", "พื้นที่แรเงา (เรขาคณิต)", "การตัดเชือกพับทบ", "แถวคอยแบบซ้อนทับ", "อายุข้ามเวลาขั้นสูง", "แผนภาพความชอบ (Venn)", "การนับหน้าหนังสือ", "วันที่และปฏิทิน"]
tmc_upper = ["ความเร็ววิ่งสวนทาง", "งานและเวลา (Work)", "ระฆังและไฟกะพริบ (ค.ร.น.)", "อัตราส่วนอายุ", "เศษส่วนของที่เหลือ", "เส้นทางที่เป็นไปได้", "จัดของใส่กล่อง (Modulo)", "นาฬิกาเดินเพี้ยน", "คะแนนยิงเป้า"]

curriculum_db = {
    "ป.1": {
        "จำนวนนับ 1 ถึง 100 และ 0": ["การนับทีละ 1", "การนับทีละ 10", "การอ่านและการเขียนตัวเลข", "การแสดงจำนวนในรูปความสัมพันธ์แบบส่วนย่อย-ส่วนรวม", "แบบรูปซ้ำของรูปเรขาคณิต", "การบอกอันดับที่ (รถแข่ง)", "หลัก ค่าของเลขโดดในแต่ละหลัก และรูปกระจาย", "การเปรียบเทียบจำนวน (> <)",  "การเปรียบเทียบจำนวน (= ≠)", "การเรียงลำดับจำนวน (น้อยไปมาก)", "การเรียงลำดับจำนวน (มากไปน้อย)"],
        "การบวก การลบ": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)"],
        "แผนภูมิรูปภาพ": ["การอ่านแผนภูมิรูปภาพ"],
        "🌟 โจทย์แข่งขัน (แนว TMC)": tmc_lower
    },
    "ป.2": {
        "จำนวนนับไม่เกิน 1,000 และ 0": ["การนับทีละ 2 ทีละ 5 ทีละ 10 และทีละ 100", "การอ่านและการเขียนตัวเลข", "จำนวนคู่ จำนวนคี่", "หลัก ค่าของเลขโดด และรูปกระจาย", "การเปรียบเทียบจำนวน (> <)", "การเรียงลำดับจำนวน (น้อยไปมาก)", "การเรียงลำดับจำนวน (มากไปน้อย)"],
        "เวลาและการวัด": ["การบอกเวลาเป็นนาฬิกาและนาที", "การอ่านน้ำหนักจากเครื่องชั่งสปริง"],
        "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การคูณ (แบบตั้งหลัก)", "การหารพื้นฐาน"],
        "แผนภูมิรูปภาพ": ["การอ่านแผนภูมิรูปภาพ"],
        "🌟 โจทย์แข่งขัน (แนว TMC)": tmc_lower
    },
    "ป.3": {
        "จำนวนนับและเศษส่วน": ["การอ่าน การเขียนตัวเลข", "หลัก ค่าของเลขโดด และรูปกระจาย", "การเปรียบเทียบจำนวน (> <)", "การเรียงลำดับจำนวน (น้อยไปมาก)", "การเรียงลำดับจำนวน (มากไปน้อย)", "การอ่านและเขียนเศษส่วน", "การบวกลบเศษส่วน (ตัวส่วนเท่ากัน)"],
        "เวลา เงิน และการวัด": ["การบอกเวลาเป็นนาฬิกาและนาที", "การบอกจำนวนเงินทั้งหมด", "การอ่านน้ำหนักจากเครื่องชั่งสปริง"],
        "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การคูณ (แบบตั้งหลัก)", "การหารยาว"],
        "แผนภูมิรูปภาพ": ["การอ่านแผนภูมิรูปภาพ"],
        "🌟 โจทย์แข่งขัน (แนว TMC)": tmc_mid
    },
    "ป.4": {
        "จำนวนนับที่มากกว่า 100,000": ["การอ่านและการเขียนตัวเลข", "หลัก ค่าประจำหลัก และรูปกระจาย", "การเปรียบเทียบและเรียงลำดับ", "ค่าประมาณเป็นจำนวนเต็มสิบ เต็มร้อย เต็มพัน"],
        "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การคูณ (แบบตั้งหลัก)", "การหารยาว"],
        "เศษส่วนและทศนิยม": ["แปลงเศษเกินเป็นจำนวนคละ", "การอ่านและการเขียนทศนิยม"],
        "เรขาคณิตและการวัด": ["การบอกชนิดของมุม", "การวัดขนาดของมุม (ไม้โปรแทรกเตอร์)", "การหาความยาวรอบรูปสี่เหลี่ยมมุมฉาก", "การหาพื้นที่รูปสี่เหลี่ยมมุมฉาก"],
        "สมการ": ["การแก้สมการ (บวก/ลบ)"],
        "🌟 โจทย์แข่งขัน (แนว TMC)": tmc_mid
    },
    "ป.5": {
        "เศษส่วน": ["การบวกเศษส่วน", "การลบเศษส่วน", "การคูณเศษส่วน", "การหารเศษส่วน"],
        "ทศนิยม": ["การบวกและการลบทศนิยม", "การคูณทศนิยม"],
        "ร้อยละและเปอร์เซ็นต์": ["การเขียนเศษส่วนในรูปร้อยละ"],
        "สมการ": ["การแก้สมการ (คูณ/หาร)"],
        "🌟 โจทย์แข่งขัน (แนว TMC)": tmc_upper
    },
    "ป.6": {
        "ตัวประกอบของจำนวนนับ": ["การหา ห.ร.ม.", "การหา ค.ร.น."],
        "อัตราส่วนและร้อยละ": ["การหาอัตราส่วนที่เท่ากัน", "โจทย์ปัญหาอัตราส่วน", "โจทย์ปัญหาร้อยละ"],
        "สมการ": ["การแก้สมการ (สองขั้นตอน)"],
        "🌟 โจทย์แข่งขัน (แนว TMC)": tmc_upper
    }
}

box_html = "<span style='display: inline-block; width: 22px; height: 22px; border: 2px solid #333; border-radius: 3px; vertical-align: middle; margin-left: 5px; position: relative; top: -2px;'></span>"

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
            a_dig = [int(c) if c.strip() else 0 for c in str_a]
            b_dig = [int(c) if c.strip() else 0 for c in str_b]
            for i in range(num_len - 1, -1, -1):
                if a_dig[i] < b_dig[i]:
                    for j in range(i-1, -1, -1):
                        if a_dig[j] > 0 and str_a[j].strip() != "":
                            strike[j] = True
                            a_dig[j] -= 1
                            top_marks[j] = str(a_dig[j])
                            for k in range(j+1, i): 
                                strike[k] = True
                                a_dig[k] = 9
                                top_marks[k] = "9"
                            strike[i] = True
                            a_dig[i] += 10
                            top_marks[i] = str(a_dig[i])
                            break
                            
        elif op == '×':
            b_val = b
            carry = 0
            a_dig = [int(c) if c.strip() else 0 for c in str_a]
            for i in range(num_len - 1, -1, -1):
                if str_a[i].strip() == "": 
                    if carry > 0: 
                        top_marks[i] = str(carry)
                        carry = 0
                    continue
                prod = a_dig[i] * b_val + carry
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
        
    b_tds = "".join([f'<td style="width: 35px; text-align: center; border-bottom: 2px solid #000; height: 40px; vertical-align: bottom;">{str_b[i].strip()}</td>' for i in range(num_len)])
    
    if is_key and result is not None:
        str_r = str(result).rjust(num_len, " ")
        res_tds = "".join([f'<td style="width: 35px; text-align: center; color: red; font-weight: bold; height: 45px; vertical-align: bottom;">{str_r[i].strip()}</td>' for i in range(num_len)])
    else: 
        res_tds = "".join([f'<td style="width: 35px; height: 45px;"></td>' for _ in range(num_len)])
        
    return f"""<div style="display: block; text-align: center; margin-top: 10px;"><div style="display: inline-block; font-family: 'Sarabun', sans-serif; font-size: 38px; line-height: 1.1; margin: 10px 20px;"><table style="border-collapse: collapse; margin-left: auto; margin-right: auto;"><tr><td style="width: 20px;"></td>{a_tds}<td style="width: 50px; text-align: center; vertical-align: middle;" rowspan="2">{op}</td></tr><tr><td></td>{b_tds}</tr><tr><td></td>{res_tds}<td></td></tr><tr><td></td><td colspan="{num_len}" style="border-bottom: 6px double #000; height: 10px;"></td><td></td></tr></table></div></div>"""

def generate_fraction_html(num, den, color="#000"):
    return f"""<div style="display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; margin: 0 5px; font-family: 'Sarabun', sans-serif;"><span style="font-size: 20px; font-weight: bold; border-bottom: 2px solid {color}; padding: 0 4px; line-height: 1.1; color: {color};">{num}</span><span style="font-size: 20px; font-weight: bold; padding: 0 4px; line-height: 1.1; color: {color};">{den}</span></div>"""

def generate_mixed_number_html(whole, num, den):
    return f"""<div style="display: inline-flex; align-items: center; vertical-align: middle; margin: 0 5px; font-family: 'Sarabun', sans-serif;"><span style="font-size: 24px; font-weight: bold; margin-right: 4px; color: red;">{whole}</span><div style="display: inline-flex; flex-direction: column; align-items: center;"><span style="font-size: 20px; font-weight: bold; border-bottom: 2px solid red; padding: 0 4px; line-height: 1.1; color: red;">{num}</span><span style="font-size: 20px; font-weight: bold; padding: 0 4px; line-height: 1.1; color: red;">{den}</span></div></div>"""

def get_fraction_solution_steps(num, den):
    g = math.gcd(num, den)
    if num == 0: 
        return "เศษส่วนที่มีตัวเศษเป็น 0 จะมีค่าเท่ากับ 0 เสมอ", "<span style='font-size: 24px; font-weight: bold; color: red;'>0</span>"
    if num == den: 
        return "เศษส่วนที่มีตัวเศษและตัวส่วนเท่ากัน (หารกันลงตัวพอดี) จะมีค่าเท่ากับ 1 เสมอ", "<span style='font-size: 24px; font-weight: bold; color: red;'>1</span>"
        
    sim_num = num // g
    sim_den = den // g
    extra_steps = ""
    final_html = ""
    
    if sim_den == 1:
        final_html = f"<span style='font-size: 24px; font-weight: bold; color: red;'>{sim_num}</span>"
        if g > 1: 
            extra_steps = f"ทอนเป็นเศษส่วนอย่างต่ำ (ใช้แม่ {g} หารทั้งเศษและส่วน) จะได้ผลลัพธ์เป็นจำนวนเต็ม"
    elif sim_num > sim_den:
        w = sim_num // sim_den
        r = sim_num % sim_den
        final_html = generate_mixed_number_html(w, r, sim_den)
        if g > 1: 
            extra_steps = f"ทอนเป็นเศษส่วนอย่างต่ำ (ใช้แม่ {g} หาร) และทำให้อยู่ในรูปจำนวนคละ"
        else: 
            extra_steps = f"แปลงเศษเกินให้อยู่ในรูปจำนวนคละ"
    else:
        final_html = f"""<div style="display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; margin: 0 5px; font-family: 'Sarabun', sans-serif;"><span style="font-size: 20px; font-weight: bold; border-bottom: 2px solid red; padding: 0 4px; line-height: 1.1; color: red;">{sim_num}</span><span style="font-size: 20px; font-weight: bold; padding: 0 4px; line-height: 1.1; color: red;">{sim_den}</span></div>"""
        if g > 1: 
            extra_steps = f"ทอนเป็นเศษส่วนอย่างต่ำโดยใช้แม่ {g} หารทั้งเศษและส่วน"
            
    return extra_steps, final_html

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
                ca //= i
                cb //= i
                found = True
                break
        if not found: 
            break
            
    if not factors: 
        if mode == "ห.ร.ม.":
            return f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> ไม่มีตัวประกอบร่วมที่หารลงตัวทั้งคู่</span><br><b>ห.ร.ม. = 1</b>"
        else:
            return f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> ไม่มีตัวประกอบร่วมที่หารลงตัวทั้งคู่</span><br><b>ค.ร.น. = {a} × {b} = {a*b}</b>"
            
    steps_html += f"<tr><td></td><td style='padding: 5px 15px; text-align: center;'>{ca}</td><td style='padding: 5px 15px; text-align: center;'>{cb}</td></tr>"
    table = f"<table style='margin: 10px 0; font-size: 20px; border-collapse: collapse; color: #333;'>{steps_html}</table>"
    
    if mode == "ห.ร.ม.":
        ans = math.prod(factors)
        calc_str = " × ".join(map(str, factors))
        sol = f"<span style='color: #2c3e50;'><b>วิธีทำ (หารสั้น):</b></span>{table}<span style='color: #2c3e50;'><b>ห.ร.ม.</b> คือนำตัวหารด้านหน้ามาคูณกัน:</span><br>= {calc_str}<br>= <b>{ans}</b>"
    else:
        ans = math.prod(factors) * ca * cb
        calc_str = " × ".join(map(str, factors + [ca, cb]))
        sol = f"<span style='color: #2c3e50;'><b>วิธีทำ (หารสั้น):</b></span>{table}<span style='color: #2c3e50;'><b>ค.ร.น.</b> คือนำตัวหารและผลลัพธ์บรรทัดสุดท้ายมาคูณกัน (รูปตัว L):</span><br>= {calc_str}<br>= <b>{ans}</b>"
        
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
        div_tds_list.append(f'
