import streamlit as st
import streamlit.components.v1 as components
import random
import math
import zipfile
import io
import time
import base64

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
    <p>ระบบสร้างสื่อการสอนคณิตศาสตร์ (ป.1 - ป.6) พร้อมระบบ Branding, Spacing และเฉลยละเอียดยิบ</p>
</div>
""", unsafe_allow_html=True)

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
                if carry > 0 and i > 0: top_marks[i-1] = str(carry)
        elif op == '-':
            a_chars, b_chars = list(str_a), list(str_b)
            a_digits = [int(c) if c.strip() else 0 for c in a_chars]
            b_digits = [int(c) if c.strip() else 0 for c in b_chars]
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
            b_val, carry = b, 0
            a_digits = [int(c) if c.strip() else 0 for c in str_a]
            for i in range(num_len - 1, -1, -1):
                if str_a[i].strip() == "": 
                    if carry > 0: 
                        top_marks[i] = str(carry)
                        carry = 0
                    continue
                prod = a_digits[i] * b_val + carry
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
            extra_steps = f"ทอนเป็นเศษส่วนอย่างต่ำ (นำ {g} มาหารทั้งเศษและส่วน) จะได้ผลลัพธ์เป็นจำนวนเต็ม"
    elif sim_num > sim_den:
        w = sim_num // sim_den
        r = sim_num % sim_den
        final_html = generate_mixed_number_html(w, r, sim_den)
        if g > 1: 
            extra_steps = f"ทอนเป็นเศษส่วนอย่างต่ำ (นำ {g} มาหารทั้งเศษและส่วน) และแปลงให้อยู่ในรูปจำนวนคละ"
        else: 
            extra_steps = f"แปลงเศษเกินให้อยู่ในรูปจำนวนคละ"
    else:
        final_html = f"""<div style="display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; margin: 0 5px; font-family: 'Sarabun', sans-serif;"><span style="font-size: 20px; font-weight: bold; border-bottom: 2px solid red; padding: 0 4px; line-height: 1.1; color: red;">{sim_num}</span><span style="font-size: 20px; font-weight: bold; padding: 0 4px; line-height: 1.1; color: red;">{sim_den}</span></div>"""
        if g > 1: 
            extra_steps = f"ทอนเป็นเศษส่วนอย่างต่ำโดยนำ {g} มาหารทั้งเศษและส่วน"
            
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
            return f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) ลองหาตัวเลขที่สามารถหารทั้ง {a} และ {b} ลงตัวพร้อมกัน<br>2) พบว่าไม่มีตัวเลขใดเลยที่หารทั้งคู่ลงตัว (นอกจากเลข 1)<br><b>ดังนั้น ห.ร.ม. = 1</b></span>"
        else:
            return f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) ลองหาตัวเลขที่สามารถหารทั้ง {a} และ {b} ลงตัวพร้อมกัน<br>2) พบว่าไม่มีตัวเลขใดเลยที่หารทั้งคู่ลงตัว<br>3) การหา ค.ร.น. ในกรณีนี้ ให้นำตัวเลขทั้งสองตัวมาคูณกันได้เลย<br><b>ดังนั้น ค.ร.น. = {a} × {b} = {a*b}</b></span>"
            
    steps_html += f"<tr><td></td><td style='padding: 5px 15px; text-align: center;'>{ca}</td><td style='padding: 5px 15px; text-align: center;'>{cb}</td></tr>"
    table = f"<table style='margin: 10px 0; font-size: 20px; border-collapse: collapse; color: #333;'>{steps_html}</table>"
    
    if mode == "ห.ร.ม.":
        ans = math.prod(factors)
        calc_str = " × ".join(map(str, factors))
        sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (การตั้งหารสั้น):</b><br>1) หาตัวเลขที่สามารถหารทั้ง {a} และ {b} ลงตัวพร้อมกัน แล้วนำมาเป็นตัวหารด้านหน้า<br>2) หารไปเรื่อยๆ จนกว่าจะไม่มีตัวเลขใดหารลงตัวทั้งคู่แล้ว<br>{table}<br>3) <b>การหา ห.ร.ม.</b> ให้นำเฉพาะ <b>ตัวเลขด้านหน้าเครื่องหมายหารสั้น</b> มาคูณกัน<br><b>ดังนั้น ห.ร.ม. = {calc_str} = {ans}</b></span>"
    else:
        ans = math.prod(factors) * ca * cb
        calc_str = " × ".join(map(str, factors + [ca, cb]))
        sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (การตั้งหารสั้น):</b><br>1) หาตัวเลขที่สามารถหารทั้ง {a} และ {b} ลงตัวพร้อมกัน แล้วนำมาเป็นตัวหารด้านหน้า<br>2) หารไปเรื่อยๆ จนกว่าจะไม่มีตัวเลขใดหารลงตัวทั้งคู่แล้ว<br>{table}<br>3) <b>การหา ค.ร.น.</b> ให้นำ <b>ตัวเลขด้านหน้า และ เศษที่เหลือด้านล่างสุดทั้งหมด (เป็นรูปตัว L)</b> มาคูณกัน<br><b>ดังนั้น ค.ร.น. = {calc_str} = {ans}</b></span>"
        
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
    
    # เพิ่มคำอธิบายการหารยาว
    html += f"<div style='margin-top: 15px; color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) นำตัวหาร ({divisor}) ไปหารตัวตั้งทีละหลักจากซ้ายไปขวา<br>2) ท่องสูตรคูณแม่ {divisor} ว่าคูณอะไรแล้วได้ใกล้เคียงหรือเท่ากับตัวตั้งในหลักนั้นที่สุด (แต่ห้ามเกิน)<br>3) ใส่ผลลัพธ์ไว้ด้านบน และนำผลคูณมาลบกันด้านล่าง<br>4) ดึงตัวเลขในหลักถัดไปลงมา แล้วทำซ้ำขั้นตอนเดิมจนหมดทุกหลัก</div>"
    
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
            actual_sub_t = sub_t
            if sub_t == "แบบทดสอบรวมปลายภาค":
                all_mains = [m for m in curriculum_db[grade].keys() if m != "🌟 โหมดพิเศษ (สุ่มทุกเรื่อง)"]
                rand_main = random.choice(all_mains)
                actual_sub_t = random.choice(curriculum_db[grade][rand_main])

            prefix = get_prefix(grade)

            # =========================================================
            # โหมดหลักสูตรปกติ (เขียนอธิบายละเอียด Step-by-Step)
            # =========================================================
            if actual_sub_t == "การคูณ (แบบตั้งหลัก)":
                if grade in ["ป.1", "ป.2"]:
                    a = random.randint(10, 99) 
                elif grade == "ป.3":
                    a = random.randint(100, 999) 
                else:
                    a = random.randint(1000, 9999) 
                b = random.randint(2, 9)
                res = a * b
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} × {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '×', is_key=False)
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) ตั้งหลักตัวเลขให้ตรงกัน<br>2) นำตัวคูณ ({b}) ไปคูณตัวตั้งด้านบนทีละหลัก โดยเริ่มจากหลักหน่วยทางขวาสุด<br>3) หากผลคูณมีค่าตั้งแต่ 10 ขึ้นไป ให้ใส่เลขตัวหลัง (หลักหน่วย) ไว้ด้านล่าง และนำเลขตัวหน้าไป 'ทด' ไว้บนหัวของหลักถัดไปทางซ้ายมือ<br>4) เมื่อคูณหลักถัดไปเสร็จ อย่าลืมบวกตัวทดที่อยู่ด้านบนด้วย</span><br>" + generate_vertical_table_html(a, b, '×', result=res, is_key=True)

            elif actual_sub_t == "การบวก (แบบตั้งหลัก)":
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
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} + {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '+', is_key=False)
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) ตั้งหลักตัวเลขให้ตรงกัน (หลักหน่วยตรงหลักหน่วย, หลักสิบตรงหลักสิบ)<br>2) เริ่มบวกตัวเลขจากหลักหน่วย (ขวาสุด) ไปทางซ้ายทีละหลัก<br>3) หากผลบวกในหลักใดมีค่าตั้งแต่ 10 ขึ้นไป ให้ใส่เลขตัวหลังไว้ด้านล่าง และนำเลขตัวหน้าไป 'ทด' ขึ้นไปไว้บนหัวของหลักถัดไปทางซ้ายมือ<br>4) ในการบวกหลักถัดไป ให้นำตัวทดมาบวกเพิ่มด้วย</span><br>" + generate_vertical_table_html(a, b, '+', result=res, is_key=True)

            elif actual_sub_t == "การลบ (แบบตั้งหลัก)":
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
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} - {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '-', is_key=False)
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) ตั้งหลักตัวเลขให้ตรงกัน (หลักหน่วยตรงหลักหน่วย, หลักสิบตรงหลักสิบ)<br>2) เริ่มลบตัวเลขจากหลักหน่วย (ขวาสุด) ไปทางซ้ายทีละหลัก<br>3) หากตัวเลขด้านบนน้อยกว่าตัวเลขด้านล่าง (ลบไม่พอ) ให้ทำการ 'ขอยืม' ตัวเลขจากหลักถัดไปทางซ้ายมา 1 (ซึ่งจะมีค่าเท่ากับ 10 ในหลักปัจจุบัน)<br>4) นำ 10 ที่ยืมมาบวกกับตัวเลขเดิม แล้วจึงทำการลบตามปกติ</span><br>" + generate_vertical_table_html(a, b, '-', result=res, is_key=True)

            elif "การหารพื้นฐาน" in actual_sub_t:
                a = random.randint(2, 9)
                b = random.randint(2, 12)
                dividend = a * b
                q = f"จงหาผลลัพธ์ของ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {dividend} ÷ {a} = {box_html}</span>"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) การหารคือการหาว่า 'ตัวหาร ({a}) ต้องคูณกับเลขอะไรจึงจะได้ผลลัพธ์เท่ากับตัวตั้ง ({dividend})'<br>2) ให้นักเรียนลองท่องสูตรคูณแม่ <b>{a}</b> ดูครับ:<br>&nbsp;&nbsp;&nbsp;{a} × 1 = {a}<br>&nbsp;&nbsp;&nbsp;...<br>&nbsp;&nbsp;&nbsp;<b>{a} × {b} = {dividend}</b> (เจอคำตอบแล้ว!)<br>ดังนั้น {dividend} ÷ {a} มีค่าเท่ากับ <b>{b}</b><br><b>ตอบ: {b}</b></span>"

            elif "ส่วนย่อย-ส่วนรวม" in actual_sub_t:
                total = random.randint(5, 20)
                p1 = random.randint(1, total - 1)
                p2 = total - p1
                miss = random.choice(['t', 'p1', 'p2'])
                svg_t = f"""<div style="display: block; text-align: center; margin-top: 10px;"><svg width="200" height="160"><line x1="100" y1="40" x2="50" y2="120" stroke="#333" stroke-width="3"/><line x1="100" y1="40" x2="150" y2="120" stroke="#333" stroke-width="3"/><circle cx="100" cy="40" r="30" fill="#e8f8f5" stroke="#16a085" stroke-width="3"/><circle cx="50" cy="120" r="30" fill="#fdf2e9" stroke="#d35400" stroke-width="3"/><circle cx="150" cy="120" r="30" fill="#fdf2e9" stroke="#d35400" stroke-width="3"/><text x="100" y="47" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='t' else "#16a085"}">{{t}}</text><text x="50" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='p1' else "#d35400"}">{{p1}}</text><text x="150" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='p2' else "#d35400"}">{{p2}}</text></svg></div>"""
                q = f"จงหาตัวเลขที่หายไป (?) จากความสัมพันธ์แบบส่วนย่อย-ส่วนรวม : " + svg_t.format(t="?" if miss=='t' else total, p1="?" if miss=='p1' else p1, p2="?" if miss=='p2' else p2)
                if miss == 't':
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>ในการหา 'ส่วนรวม' (วงกลมด้านบน) เราต้องนำ 'ส่วนย่อย' ทั้งสองส่วน (วงกลมด้านล่าง) มาบวกเข้าด้วยกัน<br>จะได้: {p1} + {p2} = <b>{total}</b><br><b>ตอบ: {total}</b></span><br>" + svg_t.format(t=total, p1=p1, p2=p2)
                elif miss == 'p1':
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>ในการหา 'ส่วนย่อย' ที่หายไป เราต้องนำ 'ส่วนรวม' (วงกลมด้านบน) มาลบด้วย 'ส่วนย่อย' อีกข้างที่เราทราบค่าแล้ว<br>จะได้: {total} - {p2} = <b>{p1}</b><br><b>ตอบ: {p1}</b></span><br>" + svg_t.format(t=total, p1=p1, p2=p2)
                else:
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>ในการหา 'ส่วนย่อย' ที่หายไป เราต้องนำ 'ส่วนรวม' (วงกลมด้านบน) มาลบด้วย 'ส่วนย่อย' อีกข้างที่เราทราบค่าแล้ว<br>จะได้: {total} - {p1} = <b>{p2}</b><br><b>ตอบ: {p2}</b></span><br>" + svg_t.format(t=total, p1=p1, p2=p2)

            elif "หลัก ค่าของเลขโดดในแต่ละหลัก และรูปกระจาย" in actual_sub_t or "รูปกระจาย" in actual_sub_t:
                n = random.randint(100, limit - 1 if limit > 10 else 99)
                parts = [f"{int(d)*(10**(len(str(n))-1-i)):,}" for i,d in enumerate(str(n)) if d != '0']
                q = f"จงเขียนจำนวน <b>{n:,}</b> ให้อยู่ในรูปกระจาย"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                การเขียนในรูปกระจาย คือการแยกตัวเลขตาม "ค่าประจำหลัก" ของแต่ละตัว แล้วนำมาเขียนในรูปของการบวกกัน<br>
                1) พิจารณาตัวเลขทีละตัวจากซ้ายไปขวา<br>
                2) นำค่าของตัวเลขในแต่ละหลักมาเขียนคั่นด้วยเครื่องหมาย + (ถ้าหลักไหนเป็น 0 ไม่ต้องเขียน)<br>
                จะได้: <b>{' + '.join(parts)}</b><br>
                <b>ตอบ: {' + '.join(parts)}</b></span>"""
                
            elif "จำนวนคู่ จำนวนคี่" in actual_sub_t:
                n = random.randint(10, limit)
                q = f"จำนวน <b>{n:,}</b> เป็นจำนวนคู่ หรือ จำนวนคี่?"
                ans = "จำนวนคู่" if n % 2 == 0 else "จำนวนคี่"
                reason = "หารด้วย 2 ลงตัวพอดี" if n % 2 == 0 else "หารด้วย 2 ไม่ลงตัว (เหลือเศษ 1)"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                วิธีดูว่าตัวเลขใดเป็นจำนวนคู่หรือจำนวนคี่ เราไม่ต้องสนใจตัวเลขข้างหน้าเลย ให้ดูแค่ <b>"ตัวเลขในหลักหน่วย" (ตัวขวาสุด)</b> เท่านั้นครับ<br>
                1) ตัวเลขในหลักหน่วยของข้อนี้คือเลข <b>{n%10}</b><br>
                2) นำ {n%10} ไปพิจารณาว่าหารด้วย 2 ลงตัวหรือไม่<br>
                &nbsp;&nbsp;&nbsp;พบว่า {reason}<br>
                <b>ตอบ: {n:,} เป็น{ans}</b></span>"""

            elif "เขียนตัวเลข" in actual_sub_t:
                if grade in ["ป.1", "ป.2", "ป.3"]:
                    n = random.randint(11, limit-1)
                else:
                    n = random.randint(100000, 999999)
                    
                if random.choice([True, False]):
                    q = f"จงเขียนตัวเลขฮินดูอารบิก <b>{n:,}</b> ให้เป็น<b>ตัวเลขไทย</b>"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>แปลงตัวเลขฮินดูอารบิกแต่ละตัวให้เป็นตัวเลขไทยตามลำดับ<br><b>ตอบ: {str(n).translate(str.maketrans('0123456789', '๐๑๒๓๔๕๖๗๘๙'))}</b></span>"
                else:
                    q = f"จงเขียนจำนวน <b>{n:,}</b> ให้เป็น<b>ตัวหนังสือ</b>"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>อ่านตัวเลขตามค่าประจำหลักจากซ้ายไปขวา (ถ้ามีหลักหน่วยเป็นเลข 1 เราจะอ่านออกเสียงว่า 'เอ็ด')<br><b>ตอบ: {generate_thai_number_text(str(n))}</b></span>"

            elif "ค่าประมาณ" in actual_sub_t:
                n = random.randint(1111, 99999)
                ptype = random.choice(["เต็มสิบ", "เต็มร้อย", "เต็มพัน"])
                if ptype == "เต็มสิบ":
                    ans = ((n+5)//10)*10
                    chk_d = n % 10
                    chk_p = "หลักหน่วย"
                elif ptype == "เต็มร้อย":
                    ans = (((n+50)//100)*100)
                    chk_d = (n // 10) % 10
                    chk_p = "หลักสิบ"
                else:
                    ans = (((n+500)//1000)*1000)
                    chk_d = (n // 100) % 10
                    chk_p = "หลักร้อย"
                action = "ปัดขึ้น (บวกเพิ่ม 1 ในหลักซ้ายมือและเปลี่ยนตัวมันเองเป็น 0)" if chk_d >= 5 else "ปัดทิ้ง (เปลี่ยนตัวมันเองและหลักทางขวาเป็น 0 ให้หมด)"
                q = f"จงหาค่าประมาณเป็นจำนวน<b>{ptype}</b> ของ {n:,}"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                เมื่อต้องการประมาณเป็นจำนวน{ptype} กฎคือให้เราถอยไปพิจารณาตัวเลขในหลักที่เล็กกว่า 1 ขั้น นั่นคือ <b>{chk_p}</b><br>
                1) ตัวเลขใน {chk_p} ของข้อนี้คือเลข <b>{chk_d}</b><br>
                2) ใช้กฎการปัดเลข: ถ้าเป็นเลข 0-4 ให้ปัดทิ้ง, ถ้าเป็นเลข 5-9 ให้ปัดขึ้น<br>
                3) ในกรณีนี้เป็นเลข {chk_d} ดังนั้นเราต้องทำการ <b>{action}</b><br>
                <b>ตอบ: ค่าประมาณคือ {ans:,}</b></span>"""

            elif "การบอกอันดับที่" in actual_sub_t:
                c_map = {"แดง": "#ff4d4d", "ฟ้า": "#3498db", "เขียว": "#2ecc71", "เหลือง": "#f1c40f"}
                cols = list(c_map.keys())
                random.shuffle(cols)
                idx = random.randint(0, 3)
                name = cols[idx]
                q = f"มีรถ 4 คันวิ่งเรียงกันตามลำดับจากซ้ายไปขวา (คันซ้ายสุดคือคันที่ 1) ได้แก่ รถสี{cols[0]}, สี{cols[1]}, สี{cols[2]}, และ สี{cols[3]}<br>รถสี{name} วิ่งอยู่อันดับที่เท่าไร?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                ให้นับลำดับเรียงจากคันทางซ้ายมือสุดไปหาขวามือทีละคัน<br>
                อันดับที่ 1 คือ รถสี{cols[0]}<br>
                อันดับที่ 2 คือ รถสี{cols[1]}<br>
                อันดับที่ 3 คือ รถสี{cols[2]}<br>
                อันดับที่ 4 คือ รถสี{cols[3]}<br>
                เมื่อนำมาเทียบดูแล้วพบว่า รถสี{name} ตรงกับลำดับที่ <b>{idx + 1}</b><br>
                <b>ตอบ: อยู่อันดับที่ {idx + 1}</b></span>"""

            elif "แบบรูปซ้ำ" in actual_sub_t:
                shapes = ["🔴", "🟦", "⭐"]
                pt = [0, 1, 2]
                seq = [shapes[pt[i%3]] for i in range(7)]
                ans = shapes[pt[7%3]]
                q = f"พิจารณาแบบรูปซ้ำต่อไปนี้ รูปที่หายไปในช่องว่างคือรูปใด? <br><br>{' '.join(seq)} &nbsp;&nbsp;&nbsp; <b>____</b>"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                1) ให้เราสังเกตดูว่ารูปภาพเหล่านี้มีการเรียงซ้ำกันเป็นชุดๆ ละกี่รูป<br>
                2) จะเห็นว่ารูปภาพเรียงซ้ำกันเป็นชุด ชุดละ 3 รูป คือ [ {shapes[0]}, {shapes[1]}, {shapes[2]} ]<br>
                3) เมื่อเรานับลำดับของแบบรูปวนไปเรื่อยๆ จนถึงตำแหน่งที่หายไป จะพบว่ามันวนกลับมาตกที่รูป <b>{ans}</b> พอดี<br>
                <b>ตอบ: รูปที่หายไปคือ {ans}</b></span>"""

            elif "การนับทีละ" in actual_sub_t:
                step = 10 if "10" in actual_sub_t else (1 if "1" in actual_sub_t else random.choice([2, 5, 10, 100]))
                inc = random.choice([True, False])
                max_val = limit - (3 * step)
                if max_val <= 1: max_val = 10
                st_val = random.randint(1, max_val)
                seq = [st_val, st_val+step, st_val+2*step, st_val+3*step] if inc else [st_val+3*step, st_val+2*step, st_val+step, st_val]
                idx = random.randint(0, 3)
                ans_str = f"{seq[idx]:,}"
                seq_str = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;".join([f"{s:,}" if i != idx else "_____" for i, s in enumerate(seq)])
                word_inc = "เพิ่มขึ้น" if inc else "ลดลง"
                q = f"จงพิจารณาแบบรูปและเติมตัวเลขที่หายไปลงในช่องว่าง : <br><br><span style='font-weight: bold; margin-left: 10px;'>{seq_str}</span>"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                1) สังเกตความต่างของตัวเลขสองตัวที่อยู่ติดกัน<br>
                2) จะพบว่าตัวเลขในแบบรูปนี้มีการ <b>{word_inc}ทีละ {step}</b> อย่างสม่ำเสมอ<br>
                3) ดังนั้น การหาตัวเลขที่หายไป ก็ให้เราทำการนำเลขที่อยู่ก่อนหน้ามา{word_inc}ไปอีก {step}<br>
                <b>ตอบ: ตัวเลขที่หายไปคือ {ans_str}</b></span>"""

            elif "เรียงลำดับ" in actual_sub_t:
                nums = random.sample(range(10, limit), 4)
                is_asc = "น้อยไปมาก" in actual_sub_t if "น้อยไปมาก" in actual_sub_t else random.choice([True, False])
                num_str = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;".join([f"{x:,}" for x in nums])
                word_asc = "น้อยไปหามาก" if is_asc else "มากไปหาน้อย"
                ans_str = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;".join([f"{x:,}" for x in sorted(nums, reverse=not is_asc)])
                q = f"จงเรียงลำดับจำนวนต่อไปนี้จาก <b>{word_asc}</b> : <br><br><span style='font-weight: bold; margin-left: 10px;'>{num_str}</span>"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                เปรียบเทียบค่าของตัวเลขทีละจำนวน โดยเริ่มพิจารณาดูจากหลักที่อยู่ซ้ายมือสุดก่อน แล้วค่อยๆ เรียงลำดับจาก <b>{word_asc}</b> ตามที่โจทย์กำหนด จะได้ดังนี้:<br>
                <b>ตอบ: {ans_str}</b></span>"""

            elif "เปรียบเทียบ" in actual_sub_t:
                a = random.randint(10, limit)
                is_eq = "=" in actual_sub_t
                b = a if is_eq and random.choice([True, False]) else random.randint(10, limit)
                while not is_eq and a == b: b = random.randint(10, limit)
                sign = "=" if a == b else ("≠" if is_eq else (">" if a > b else "<"))
                sign_word = "เท่ากับ" if a == b else ("มากกว่า" if a > b else "น้อยกว่า")
                sign_choices = "'=' หรือ '≠'" if is_eq else "'>' หรือ '<'"
                q = f"จงเติมเครื่องหมาย {sign_choices} ลงในช่องว่างให้ถูกต้อง: <span style='display:inline-flex; align-items:center; font-weight:bold; margin-left: 10px;'>{a:,} _____ {b:,}</span>"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                เปรียบเทียบค่าของตัวเลขทีละหลักโดยเริ่มจากทางซ้ายสุดไปทางขวา จะพบว่า {a:,} มีค่า <b>{sign_word}</b> {b:,}<br>
                <b>ตอบ: เติมเครื่องหมาย {sign}</b></span>"""

            elif "ชนิดของมุม" in actual_sub_t:
                angle = random.choice([30, 45, 60, 90, 120, 135, 150, 180])
                q = f"มุมที่มีขนาด <b>{angle} องศา</b> ตามหลักคณิตศาสตร์เรียกว่ามุมชนิดใด?"
                if angle < 90:
                    ans = "มุมแหลม"; reason = "เพราะมีขนาดมากกว่า 0 องศา แต่น้อยกว่า 90 องศา (แคบกว่ามุมฉาก)"
                elif angle == 90:
                    ans = "มุมฉาก"; reason = "เพราะมีขนาดเท่ากับ 90 องศาพอดี"
                elif angle < 180:
                    ans = "มุมป้าน"; reason = "เพราะมีขนาดมากกว่า 90 องศา แต่น้อยกว่า 180 องศา (กว้างกว่ามุมฉาก)"
                else:
                    ans = "มุมตรง"; reason = "เพราะมีขนาดเท่ากับ 180 องศาพอดี (กางออกเป็นเส้นตรง)"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>พิจารณาจากขนาดขององศา มุมนี้คือ <b>{ans}</b><br>{reason}<br><b>ตอบ: {ans}</b></span>"

            elif "ความยาวรอบรูป" in actual_sub_t or ("พื้นที่" in actual_sub_t and "สี่เหลี่ยม" in actual_sub_t):
                s = random.randint(5, 30)
                is_peri = 'รอบรูป' in actual_sub_t
                word = 'ความยาวรอบรูป' if is_peri else 'พื้นที่'
                unit = 'ซม.' if is_peri else 'ตาราง ซม.'
                ans = 4 * s if is_peri else s * s
                q = f"จงหา<b>{word}</b>ของ<b>รูปสี่เหลี่ยมจัตุรัส</b>ที่มีความยาวด้านละ {s} เซนติเมตร"
                if is_peri:
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>สูตรการหาความยาวรอบรูปสี่เหลี่ยมจัตุรัส คือการนำความยาวของทั้ง 4 ด้านมาบวกกัน (หรือนำความยาว 1 ด้านมาคูณด้วย 4)<br>จะได้ = 4 × ด้าน = 4 × {s} = <b>{ans} {unit}</b><br><b>ตอบ: {ans} {unit}</b></span>"
                else:
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>สูตรการหาพื้นที่สี่เหลี่ยมจัตุรัส คือการนำความยาวด้าน มาคูณกับ ความยาวด้าน<br>จะได้ = ด้าน × ด้าน = {s} × {s} = <b>{ans} {unit}</b><br><b>ตอบ: {ans} {unit}</b></span>"

            elif "ไม้โปรแทรกเตอร์" in actual_sub_t:
                angle = random.randint(15, 165)
                q = f"สมมติว่าเมื่อนำไม้โปรแทรกเตอร์ไปทาบที่มุมๆ หนึ่ง แล้วเส้นแขนของมุมชี้ตรงกับสเกลตัวเลข <b>{angle}</b> พอดีเป๊ะ มุมนี้จะมีขนาดกี่องศา?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>การวัดมุมด้วยไม้โปรแทรกเตอร์ เมื่อเราวางจุดกึ่งกลางทาบตรงจุดยอดมุม และแขนข้างหนึ่งทาบตรงเส้น 0 องศาแล้ว แขนอีกข้างชี้ไปที่ตัวเลขใดบนสเกล มุมนั้นก็จะมีขนาดเท่ากับตัวเลขนั้นเลยครับ<br><b>ตอบ: มีขนาด {angle} องศา</b></span>"
                
            elif "อ่านและเขียนเศษส่วน" in actual_sub_t:
                den = random.randint(3, 8)
                num = random.randint(1, den - 1)
                frac_html = generate_fraction_html(num, den)
                q = f"มีช่องสี่เหลี่ยมที่ถูกแบ่งออกเป็นส่วนเท่าๆ กันทั้งหมด {den} ช่อง มีการระบายสีไปทั้งหมด {num} ช่อง จะสามารถเขียนแทนด้วยเศษส่วนได้อย่างไร?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) ให้นำจำนวนช่องทั้งหมดที่แบ่งไว้ ไปเขียนไว้ที่ตัวส่วน (ด้านล่าง) คือเลข <b>{den}</b><br>2) ให้นำจำนวนช่องที่ถูกระบายสี ไปเขียนไว้ที่ตัวเศษ (ด้านบน) คือเลข <b>{num}</b><br>เขียนเป็นเศษส่วนได้คือ:</span> <br><br>{frac_html} <br><br><span style='color:#2c3e50;'>(อ่านว่า เศษ {num} ส่วน {den})</span>"

            elif "เศษเกินเป็นจำนวนคละ" in actual_sub_t:
                den = random.randint(3, 12)
                num = random.randint(den + 1, den * 5)
                while num % den == 0: num = random.randint(den + 1, den * 5)
                frac_html = generate_fraction_html(num, den)
                mixed_raw = generate_mixed_number_html(num // den, num % den, den)
                q = f"จงเขียนเศษเกินต่อไปนี้ ให้อยู่ในรูปของจำนวนคละ : <span style='display:inline-flex; vertical-align: middle; margin-left: 10px;'>{frac_html}</span>"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>การแปลงเศษเกินเป็นจำนวนคละ ให้เรานำตัวเศษ(ด้านบน) ไปตั้งหารด้วยตัวส่วน(ด้านล่าง) ครับ<br>1) นำ {num} ตั้ง ÷ หารด้วย {den}<br>2) ท่องสูตรคูณแม่ {den} จะพบว่าได้ผลลัพธ์จำนวนเต็มคือ <b>{num // den}</b> และเหลือเศษ <b>{num % den}</b><br>3) นำมาเขียนประกอบร่างเป็นจำนวนคละ (ตัวส่วนยังคงเป็นเลขเดิม) จะได้:</span><br><br>{mixed_raw}"

            elif "บวกลบเศษส่วน" in actual_sub_t or ("เศษส่วน" in actual_sub_t and ("บวก" in actual_sub_t or "ลบ" in actual_sub_t)):
                den = random.randint(5, 15)
                num1 = random.randint(1, den-1)
                num2 = random.randint(1, den-1)
                op = "+" if "บวก" in actual_sub_t else "-"
                if op == "-" and num1 < num2: num1, num2 = num2, num1 
                q = f"จงหาผลลัพธ์: <span style='display:inline-flex; align-items:center; margin-left:5px;'>{generate_fraction_html(num1, den)} <span style='margin: 0 8px; font-weight: bold;'>{op}</span> {generate_fraction_html(num2, den)}</span>"
                ans_num = num1 + num2 if op == '+' else num1 - num2
                word_op = "บวก" if op == "+" else "ลบ"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) สังเกตดูที่ตัวส่วน (ด้านล่าง) จะเห็นว่าตัวส่วนมีค่าเท่ากันคือเลข <b>{den}</b> แล้ว<br>2) เมื่อตัวส่วนเท่ากัน เราสามารถนำตัวเศษ (ด้านบน) มา<b>{word_op}กัน</b>ได้เลยทันที โดยที่ตัวส่วนยังคงเป็นเลขเดิม<br>3) นำ {num1} {op} {num2} = <b>{ans_num}</b><br>จะได้คำตอบคือ:</span> <br><br> {generate_fraction_html(ans_num, den)}"

            elif "คูณหารเศษส่วน" in actual_sub_t or ("เศษส่วน" in actual_sub_t and ("คูณ" in actual_sub_t or "หาร" in actual_sub_t)):
                n1, d1 = random.randint(1, 5), random.randint(2, 7)
                n2, d2 = random.randint(1, 5), random.randint(2, 7)
                op = random.choice(["×", "÷"])
                q = f"จงหาผลลัพธ์: <span style='display:inline-flex; align-items:center; margin-left:5px;'>{generate_fraction_html(n1, d1)} <span style='margin: 0 8px; font-weight: bold;'>{op}</span> {generate_fraction_html(n2, d2)}</span>"
                if op == '×':
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>การคูณเศษส่วนนั้นง่ายมากครับ ไม่ต้องสนใจว่าตัวส่วนจะเท่ากันหรือไม่<br>1) ให้นำตัวเศษคูณกับตัวเศษ: {n1} × {n2} = <b>{n1*n2}</b><br>2) ให้นำตัวส่วนคูณกับตัวส่วน: {d1} × {d2} = <b>{d1*d2}</b><br>ประกอบร่างคำตอบจะได้:</span> <br><br> {generate_fraction_html(n1*n2, d1*d2)}"
                else:
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>การหารเศษส่วนมีกฎอยู่ว่า 'เปลี่ยนหารเป็นคูณ กลับเศษเป็นส่วน (เฉพาะตัวหลัง)'<br>1) ตัวหน้าคงเดิม เปลี่ยนเครื่องหมาย ÷ เป็น ×<br>2) กลับตัวหลังให้สลับบนล่าง จากเศษ {n2} ส่วน {d2} เป็นเศษ {d2} ส่วน {n2}<br>3) จากนั้นใช้หลักการคูณคือ เศษคูณเศษ และ ส่วนคูณส่วน<br>&nbsp;&nbsp;&nbsp;ตัวเศษ: {n1} × {d2} = <b>{n1*d2}</b><br>&nbsp;&nbsp;&nbsp;ตัวส่วน: {d1} × {n2} = <b>{d1*n2}</b><br>ประกอบร่างคำตอบจะได้:</span> <br><br> {generate_fraction_html(n1*d2, d1*n2)}"

            elif "ร้อยละเศษส่วน" in actual_sub_t or ("ร้อยละ" in actual_sub_t and "เศษส่วน" in actual_sub_t):
                den = random.choice([2, 4, 5, 10, 20, 25, 50])
                num = random.randint(1, den-1)
                q = f"จงแปลงเศษส่วนต่อไปนี้ ให้อยู่ในรูปร้อยละ (เปอร์เซ็นต์) : <span style='display:inline-flex; vertical-align: middle; margin-left: 10px;'>{generate_fraction_html(num, den)}</span>"
                mul = 100 // den
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>คำว่า 'ร้อยละ' หรือเปอร์เซ็นต์ หมายถึงเศษส่วนที่มีตัวส่วนเป็น 100 เสมอ<br>1) เราต้องหาวิธีแปลงตัวส่วน {den} ให้กลายเป็น 100 โดยการหาตัวเลขมาคูณ<br>2) จะเห็นว่า {den} ต้องคูณกับ <b>{mul}</b> จึงจะได้ 100<br>3) นำ {mul} ไปคูณทั้งตัวเศษและตัวส่วน<br>&nbsp;&nbsp;&nbsp;ตัวเศษใหม่: {num} × {mul} = <b>{num * mul}</b><br>&nbsp;&nbsp;&nbsp;ตัวส่วนใหม่: {den} × {mul} = <b>100</b><br>เมื่อตัวส่วนเป็น 100 แล้ว ตัวเศษด้านบนนั่นแหละครับคือคำตอบของเปอร์เซ็นต์!<br><b>ตอบ: ร้อยละ {int((num/den)*100)} หรือ {int((num/den)*100)}%</b></span>"

            elif "อัตราส่วนที่เท่ากัน" in actual_sub_t:
                a, b, m = random.randint(2, 9), random.randint(2, 9), random.randint(2, 9)
                while a == b: b = random.randint(2, 9)
                is_front = random.choice([True, False])
                q_str = f"{a}:{b} = {a*m}:{box_html}" if is_front else f"{a}:{b} = {box_html}:{b*m}"
                q = f"จงหาจำนวนมาเติมใน {box_html} เพื่อทำให้อัตราส่วนเท่ากัน : <span style='display:inline-flex; align-items:center; color: #3498db; font-weight: bold; margin-left: 10px;'>{q_str}</span>"
                if is_front:
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) ลองสังเกตความสัมพันธ์ของตัวเลขคู่ที่โจทย์ให้มาครบทั้งสองฝั่ง (คือตัวหน้า)<br>2) จาก {a} กลายไปเป็น {a*m} แสดงว่ามันถูกนำไป <b>คูณด้วย {m}</b><br>3) หลักการของอัตราส่วนที่เท่ากันคือ ถ้าตัวหน้าคูณด้วยอะไร ตัวหลังก็ต้องคูณด้วยสิ่งนั้นด้วย!<br>4) นำตัวหลัง ({b}) ไปคูณด้วย {m} เช่นกัน -> {b} × {m} = <b>{b*m}</b><br><b>ตอบ: ตัวเลขในช่องว่างคือ {b*m}</b></span>"
                else:
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) ลองสังเกตความสัมพันธ์ของตัวเลขคู่ที่โจทย์ให้มาครบทั้งสองฝั่ง (คือตัวหลัง)<br>2) จาก {b} กลายไปเป็น {b*m} แสดงว่ามันถูกนำไป <b>คูณด้วย {m}</b><br>3) หลักการของอัตราส่วนที่เท่ากันคือ ถ้าตัวหลังคูณด้วยอะไร ตัวหน้าก็ต้องคูณด้วยสิ่งนั้นด้วย!<br>4) นำตัวหน้า ({a}) ไปคูณด้วย {m} เช่นกัน -> {a} × {m} = <b>{a*m}</b><br><b>ตอบ: ตัวเลขในช่องว่างคือ {a*m}</b></span>"

            elif "โจทย์ปัญหาอัตราส่วน" in actual_sub_t:
                a, b, m = random.randint(2, 7), random.randint(2, 7), random.randint(5, 20)
                while a == b: b = random.randint(2, 7)
                q = f"อัตราส่วนของจำนวนนักเรียนชาย ต่อ จำนวนนักเรียนหญิง ในห้องเรียนแห่งหนึ่ง คือ <b>{a} : {b}</b><br>ถ้าในห้องนี้มีนักเรียนชายทั้งหมด <b>{a*m}</b> คน อยากทราบว่าจะมีนักเรียนหญิงกี่คน?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                1) จากอัตราส่วน ชาย : หญิง = {a} : {b} (หมายความว่าถ้าจัดเป็นกลุ่มๆ กลุ่มชายจะมี {a} ส่วน และกลุ่มหญิงจะมี {b} ส่วน)<br>
                2) โจทย์บอกว่าของจริงมีนักเรียนชายอยู่ {a*m} คน<br>
                3) เราต้องหาว่า 1 ส่วนมีค่าเท่ากับกี่คน โดยนำจำนวนคนจริงไปหารกับจำนวนส่วน:<br>
                &nbsp;&nbsp;&nbsp;{a*m} คน ÷ {a} ส่วน = <b>{m} คนต่อ 1 ส่วน</b><br>
                4) เมื่อรู้ว่า 1 ส่วนคือ {m} คน ให้นำไปคูณกับจำนวนส่วนของนักเรียนหญิง ({b} ส่วน):<br>
                &nbsp;&nbsp;&nbsp;นักเรียนหญิง = {b} × {m} = <b>{b*m} คน</b><br>
                <b>ตอบ: มีนักเรียนหญิงทั้งหมด {b*m} คน</b></span>"""

            elif "หารยาว" in actual_sub_t:
                divisor = random.randint(2, 12); quotient = random.randint(100, 999); dividend = divisor * quotient
                eq_html = f"จงหาผลลัพธ์การหารยาว <span style='display:inline-flex; align-items:center; font-weight: bold; margin-left: 10px; color: #2c3e50;'>{prefix} {dividend:,} ÷ {divisor} = {box_html}</span>"
                q = generate_long_division_step_by_step_html(divisor, dividend, eq_html, is_key=False)
                sol = generate_long_division_step_by_step_html(divisor, dividend, eq_html, is_key=True)

            elif "ทศนิยม" in actual_sub_t and ("บวก" in actual_sub_t or "ลบ" in actual_sub_t):
                a, b = round(random.uniform(10.0, 99.9), 2), round(random.uniform(1.0, 9.9), 2)
                op = random.choice(["+", "-"])
                word_op = "บวก" if op == "+" else "ลบ"
                q = f"จงหาผลลัพธ์ทศนิยม <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:.2f} {op} {b:.2f} = {box_html}</span>"
                sol_table = generate_decimal_vertical_html(a, b, op, is_key=True)
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>กฎเหล็กของการบวกลบทศนิยมคือ <b>ต้องตั้งจุดทศนิยมให้ตรงกันเป๊ะๆ</b> เสมอ! จากนั้นให้ทำการตั้งหลักตัวเลขอื่นๆ ให้ตรงกันตามไปด้วย แล้วทำการ{word_op}เลขจากขวาไปซ้ายตามปกติเหมือนการ{word_op}เลขจำนวนเต็มครับ</span><br>{sol_table}"

            elif "คูณทศนิยม" in actual_sub_t:
                a, b = round(random.uniform(1.0, 12.0), 1), random.randint(2, 9)
                q = f"จงหาผลลัพธ์การคูณทศนิยม <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:.1f} × {b} = {box_html}</span>"
                sol_table = generate_vertical_table_html(int(round(a*10)), b, '×', result=int(round(a*10))*b, is_key=True)
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>เทคนิคการคูณทศนิยมคือ ให้แกล้งลืมจุดทศนิยมไปก่อน แล้วนำตัวเลขมาคูณกันแบบจำนวนเต็มปกติเลยครับ!<br>1) นำ {int(round(a*10))} มาตั้งคูณด้วย {b} ได้ผลลัพธ์ดังนี้:<br>{sol_table}<br>2) จากนั้นมาดูว่าตัวตั้งและตัวคูณรวมกันมีทศนิยมกี่ตำแหน่ง<br>&nbsp;&nbsp;&nbsp;ในข้อนี้ {a:.1f} มีทศนิยม 1 ตำแหน่ง และ {b} ไม่มีทศนิยม (0 ตำแหน่ง) รวมเป็น 1 ตำแหน่ง<br>3) ให้นำผลลัพธ์ที่ได้ มาใส่จุดทศนิยม 1 ตำแหน่ง (นับจากหลังมาหน้า)<br><b>ตอบ: {round(a*b, 1):.1f}</b></span>"

            elif "การแก้สมการ (+/-)" in actual_sub_t or actual_sub_t == "การแก้สมการ (บวก/ลบ)":
                x = random.randint(10, 50); a = random.randint(5, 20); op = random.choice(["+", "-"])
                if op == "+":
                    q = f"จงแก้สมการหาค่า x : <span style='color: #3498db; margin-left: 15px;'><b>x + {a} = {x+a}</b></span>"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                    เป้าหมายในการแก้สมการคือ การทำให้ <b>x</b> เหลืออยู่คนเดียวโดดๆ ทางฝั่งซ้ายของเครื่องหมายเท่ากับ<br>
                    1) สังเกตว่าฝั่งซ้ายมี <b>+{a}</b> เกินมาติดอยู่กับ x เราต้องกำจัดมันทิ้งไป<br>
                    2) โดยใช้สมบัติการเท่ากัน: เราจะนำ <b>{a} มาลบออกทั้งสองข้างของสมการ</b><br>
                    3) เขียนบรรทัดใหม่ได้ว่า: x + {a} <b style='color:red;'>- {a}</b> = {x+a} <b style='color:red;'>- {a}</b><br>
                    4) ทางฝั่งซ้าย +{a} ลบกับ -{a} จะหักล้างกันเหลือ 0 ทำให้เหลือแค่ x ตัวเดียว<br>
                    &nbsp;&nbsp;&nbsp;ทางฝั่งขวา นำ {x+a} ลบด้วย {a} จะได้คำตอบคือ <b>{x}</b><br>
                    <b>ตอบ: x = {x}</b></span>"""
                else:
                    q = f"จงแก้สมการหาค่า x : <span style='color: #3498db; margin-left: 15px;'><b>x - {a} = {x-a}</b></span>"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                    เป้าหมายในการแก้สมการคือ การทำให้ <b>x</b> เหลืออยู่คนเดียวโดดๆ ทางฝั่งซ้ายของเครื่องหมายเท่ากับ<br>
                    1) สังเกตว่าฝั่งซ้ายมี <b>-{a}</b> ติดอยู่กับ x เราต้องกำจัดมันทิ้งไป<br>
                    2) โดยใช้สมบัติการเท่ากัน: เราจะนำ <b>{a} มาบวกเข้าทั้งสองข้างของสมการ</b><br>
                    3) เขียนบรรทัดใหม่ได้ว่า: x - {a} <b style='color:green;'>+ {a}</b> = {x-a} <b style='color:green;'>+ {a}</b><br>
                    4) ทางฝั่งซ้าย -{a} บวกกับ +{a} จะหักล้างกันเหลือ 0 ทำให้เหลือแค่ x ตัวเดียว<br>
                    &nbsp;&nbsp;&nbsp;ทางฝั่งขวา นำ {x-a} บวกด้วย {a} จะได้คำตอบคือ <b>{x}</b><br>
                    <b>ตอบ: x = {x}</b></span>"""

            elif "การแก้สมการ (คูณ/หาร)" in actual_sub_t:
                a = random.randint(2, 12); x = random.randint(5, 20); op = random.choice(["*", "/"])
                if op == "*":
                    q = f"จงแก้สมการหาค่า x : <span style='color: #3498db; margin-left: 15px;'><b>{a}x = {a*x}</b></span>"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                    เป้าหมายคือต้องทำให้ x อยู่คนเดียวโดดๆ<br>
                    1) จากโจทย์ <b>{a}x</b> หมายความว่าเลข <b>{a}</b> กำลัง 'คูณ' อยู่กับ x เราต้องกำจัดเลข {a} ออกไป<br>
                    2) โดยใช้สมบัติการเท่ากัน: เราจะนำ <b>{a} มาหารทั้งสองข้างของสมการ</b><br>
                    3) เขียนบรรทัดใหม่ได้ว่า: ({a}x) <b style='color:red;'>÷ {a}</b> = {a*x} <b style='color:red;'>÷ {a}</b><br>
                    4) ทางฝั่งซ้าย {a} หาร {a} ได้ 1 เหลือแค่ x ตัวเดียว<br>
                    &nbsp;&nbsp;&nbsp;ทางฝั่งขวา นำ {a*x} ตั้งหารด้วย {a} จะได้คำตอบคือ <b>{x}</b><br>
                    <b>ตอบ: x = {x}</b></span>"""
                else:
                    q = f"จงแก้สมการหาค่า x : <span style='color: #3498db; margin-left: 15px;'><b>x / {a} = {x}</b></span>"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                    เป้าหมายคือต้องทำให้ x อยู่คนเดียวโดดๆ<br>
                    1) จากโจทย์ <b>x / {a}</b> หมายความว่า x กำลังถูก 'หาร' ด้วยเลข <b>{a}</b> เราต้องกำจัดเลข {a} ที่เป็นตัวส่วนนี้ออกไป<br>
                    2) โดยใช้สมบัติการเท่ากัน: เราจะนำ <b>{a} มาคูณทั้งสองข้างของสมการ</b><br>
                    3) เขียนบรรทัดใหม่ได้ว่า: (x / {a}) <b style='color:green;'>× {a}</b> = {x} <b style='color:green;'>× {a}</b><br>
                    4) ทางฝั่งซ้าย ตัวหาร {a} จะตัดกับตัวคูณ {a} หมดไป เหลือแค่ x ตัวเดียว<br>
                    &nbsp;&nbsp;&nbsp;ทางฝั่งขวา นำ {x} มาคูณกับ {a} จะได้คำตอบคือ <b>{x*a}</b><br>
                    <b>ตอบ: x = {x*a}</b></span>"""

            elif "การแก้สมการ (สองขั้นตอน)" in actual_sub_t:
                a = random.randint(2, 9); x = random.randint(2, 15); b = random.randint(1, 20)
                q = f"จงแก้สมการแบบ 2 ขั้นตอน : <span style='color: #3498db; margin-left: 15px;'><b>{a}x + {b} = {a*x+b}</b></span>"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (แก้สมการ 2 ขั้นตอน):</b><br>
                    หลักการคือ เราต้องกำจัดตัวเลขที่อยู่ไกล x ที่สุดออกไปก่อน แล้วค่อยกำจัดตัวที่ติดกับ x<br>
                    <b>ขั้นที่ 1: กำจัดตัวบวกลบก่อน</b><br>
                    1) ฝั่งซ้ายมี <b>+{b}</b> อยู่ไกลสุด ให้กำจัดโดยนำ <b>{b} มาลบออกทั้งสองข้าง</b><br>
                    &nbsp;&nbsp;&nbsp;{a}x + {b} <b style='color:red;'>- {b}</b> = {a*x+b} <b style='color:red;'>- {b}</b><br>
                    2) จะได้สมการใหม่ที่สั้นลงคือ: <b>{a}x = {a*x}</b><br><br>
                    <b>ขั้นที่ 2: กำจัดตัวคูณหาร</b><br>
                    3) ฝั่งซ้ายมีเลข <b>{a}</b> คูณติดกับ x อยู่ ให้กำจัดโดยนำ <b>{a} มาหารทั้งสองข้าง</b><br>
                    &nbsp;&nbsp;&nbsp;({a}x) <b style='color:red;'>÷ {a}</b> = {a*x} <b style='color:red;'>÷ {a}</b><br>
                    4) จะได้คำตอบสุดท้ายคือ <b>x = {x}</b><br>
                    <b>ตอบ: x = {x}</b></span>"""

            elif "ห.ร.ม." in actual_sub_t:
                a, b = random.randint(12, 48), random.randint(12, 48)
                while a == b: b = random.randint(12, 48) 
                q = f"จงหา ห.ร.ม. (หารร่วมมาก) ของ <b>{a}</b> และ <b>{b}</b>"
                sol = generate_short_division_html(a, b, mode="ห.ร.ม.")

            elif "ค.ร.น." in actual_sub_t:
                a, b = random.randint(4, 24), random.randint(4, 24)
                while a == b: b = random.randint(4, 24) 
                q = f"จงหา ค.ร.น. (คูณร่วมน้อย) ของ <b>{a}</b> และ <b>{b}</b>"
                sol = generate_short_division_html(a, b, mode="ค.ร.น.")

            else:
                a, b = random.randint(10, 50), random.randint(10, 50)
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a} + {b} = {box_html}</span>"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b> นำ {a} มาบวกกับ {b} ตามหลักคณิตศาสตร์พื้นฐาน จะได้คำตอบเท่ากับ <b>{a + b}</b><br><b>ตอบ: {a + b}</b></span>"

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
        .q-box {{ margin-bottom: {q_margin}; padding: 10px 15px; page-break-inside: avoid; border-bottom: 1px dashed #eee; font-size: 20px; }}
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

def generate_cover_html(grade, main_t, sub_t, num_q, theme_colors, brand_name):
    return f"""<!DOCTYPE html><html lang="th"><head><meta charset="utf-8">
    <style>
        .cover-inner {{ width: 100%; height: 100%; padding: 40px; box-sizing: border-box; text-align: center; position: relative; border: 15px solid {theme_colors['border']}; background: white; }}
        .title-box {{ margin-top: 80px; }}
        .title {{ font-size: 65px; color: #2c3e50; font-weight: bold; margin: 0; line-height: 1.2; }}
        .grade-badge {{ font-size: 45px; background-color: {theme_colors['badge']}; color: white; padding: 15px 50px; border-radius: 50px; display: inline-block; font-weight: bold; margin-top: 30px; }}
        .topic {{ font-size: 42px; color: #34495e; margin-top: 70px; font-weight: bold; }}
        .sub-topic {{ font-size: 32px; color: #7f8c8d; margin-top: 10px; }}
        .icons {{ font-size: 110px; margin: 60px 0; }}
        .details-badge {{ background-color: #2ecc71; color: white; display: inline-block; padding: 15px 40px; border-radius: 15px; font-size: 32px; font-weight: bold; }}
        .footer {{ position: absolute; bottom: 40px; left: 0; width: 100%; text-align: center; font-size: 22px; color: #7f8c8d; }}
    </style></head><body>
    <div class="cover-inner">
        <div class="title-box">
            <h1 class="title">แบบฝึกหัดคณิตศาสตร์</h1>
            <div class="grade-badge">ระดับชั้น {grade}</div>
        </div>
        <div class="topic">เรื่อง: {sub_t}</div>
        <div class="sub-topic">(หมวดหมู่: {main_t})</div>
        <div class="icons">🧮 📏 📐 ✏️</div>
        <div class="details-badge">รวมทั้งหมด {num_q} ข้อ (พร้อมเฉลยละเอียด)</div>
        <div class="footer"><b>ออกแบบและจัดทำโดย:</b> {brand_name}</div>
    </div>
    </body></html>"""

# ==========================================
# 4. Streamlit UI (Sidebar & Result Grouping)
# ==========================================
st.sidebar.markdown("## ⚙️ พารามิเตอร์การสร้าง")

selected_grade = st.sidebar.selectbox("📚 เลือกระดับชั้น:", ["ป.1", "ป.2", "ป.3", "ป.4", "ป.5", "ป.6"])
main_topics_list = list(curriculum_db[selected_grade].keys())
if "🌟 โจทย์แข่งขัน (แนว TMC)" in main_topics_list: 
    main_topics_list.remove("🌟 โจทย์แข่งขัน (แนว TMC)") 
main_topics_list.append("🌟 โหมดพิเศษ (สุ่มทุกเรื่อง)")

selected_main = st.sidebar.selectbox("📂 เลือกหัวข้อหลัก:", main_topics_list)
if selected_main == "🌟 โหมดพิเศษ (สุ่มทุกเรื่อง)":
    selected_sub = "แบบทดสอบรวมปลายภาค"
    st.sidebar.info("💡 โหมดนี้จะสุ่มดึงโจทย์จากทุกเรื่องในชั้นเรียนนี้มายำรวมกัน")
else:
    selected_sub = st.sidebar.selectbox("📝 เลือกหัวข้อย่อย:", curriculum_db[selected_grade][selected_main])


num_input = st.sidebar.number_input("🔢 จำนวนข้อ:", min_value=1, max_value=100, value=10)

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
st.sidebar.markdown("### 🎨 ตั้งค่าแบรนด์ & หน้าปก")
brand_name = st.sidebar.text_input("🏷️ ชื่อแบรนด์ / ผู้สอน:", value="บ้านทีเด็ด")
include_cover = st.sidebar.checkbox("🎨 สร้างหน้าปก", value=True)
color_theme = st.sidebar.selectbox("🎨 ธีมสีหน้าปก:", ["ฟ้าคลาสสิก (Blue)", "ชมพูพาสเทล (Pink)", "เขียวธรรมชาติ (Green)", "ม่วงสร้างสรรค์ (Purple)", "ส้มสดใส (Orange)"])
theme_map = {"ฟ้าคลาสสิก (Blue)": {"border": "#3498db", "badge": "#e74c3c"}, "ชมพูพาสเทล (Pink)": {"border": "#ff9ff3", "badge": "#0abde3"}, "เขียวธรรมชาติ (Green)": {"border": "#2ecc71", "badge": "#e67e22"}, "ม่วงสร้างสรรค์ (Purple)": {"border": "#9b59b6", "badge": "#f1c40f"}, "ส้มสดใส (Orange)": {"border": "#f39c12", "badge": "#2c3e50"}}

if st.sidebar.button("🚀 สั่งสร้างใบงานเดี๋ยวนี้", type="primary", use_container_width=True):
    with st.spinner("กำลังประมวลผลคำอธิบายและวาดภาพเฉลยแบบ Step-by-Step..."):
        grade_arg = selected_grade
            
        qs = generate_questions_logic(grade_arg, selected_main, selected_sub, num_input)
        
        html_w = create_page(selected_grade, selected_sub, qs, is_key=False, q_margin=q_margin, ws_height=ws_height, brand_name=brand_name)
        html_k = create_page(selected_grade, selected_sub, qs, is_key=True, q_margin=q_margin, ws_height=ws_height, brand_name=brand_name)
        html_cover = generate_cover_html(selected_grade, selected_main, selected_sub, num_input, theme_map[color_theme], brand_name) if include_cover else ""
        
        st.session_state['worksheet_html'] = html_w
        st.session_state['answerkey_html'] = html_k
        
        ebook_body = ""
        if include_cover: ebook_body += f'\n<div class="a4-wrapper cover-wrapper">{extract_body(html_cover)}</div>\n'
        ebook_body += f'\n<div class="a4-wrapper">{extract_body(html_w)}</div>\n<div class="a4-wrapper">{extract_body(html_k)}</div>\n'
        
        full_ebook_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap" rel="stylesheet"><style>@page {{ size: A4; margin: 15mm; }} @media screen {{ body {{ font-family: 'Sarabun', sans-serif; background-color: #525659; display: flex; flex-direction: column; align-items: center; padding: 40px 0; margin: 0; }} .a4-wrapper {{ width: 210mm; min-height: 297mm; background: white; margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.3); padding: 15mm; box-sizing: border-box; }} .cover-wrapper {{ padding: 0; }} }} @media print {{ body {{ font-family: 'Sarabun', sans-serif; background: transparent; padding: 0; display: block; margin: 0; }} .a4-wrapper {{ width: 100%; min-height: auto; margin: 0; padding: 0; box-shadow: none; page-break-after: always; }} .cover-wrapper {{ height: 260mm; }} }} .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 10px; padding-bottom: 10px; }} .q-box {{ margin-bottom: {q_margin}; padding: 10px 15px; page-break-inside: avoid; border-bottom: 1px dashed #eee; font-size: 20px; }} .workspace {{ height: {ws_height}; border: 2px dashed #bdc3c7; border-radius: 8px; margin: 15px 0; padding: 10px; color: #95a5a6; font-size: 16px; background-color: #fafbfc; }} .ans-line {{ margin-top: 10px; border-bottom: 1px dotted #999; width: 80%; height: 30px; font-weight: bold; font-size: 20px; display: flex; align-items: flex-end; padding-bottom: 5px; }} .sol-text {{ color: #333; font-size: 18px; display: block; margin-top: 15px; padding: 15px; background-color: #f1f8ff; border-left: 4px solid #3498db; border-radius: 4px; }} .page-footer {{ text-align: right; font-size: 14px; color: #95a5a6; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }} .cover-inner {{ width: 100%; height: 100%; padding: 40px; box-sizing: border-box; text-align: center; position: relative; border: 15px solid {theme_map[color_theme]['border']}; background: white; }} .title-box {{ margin-top: 80px; }} .title {{ font-size: 65px; color: #2c3e50; font-weight: bold; margin: 0; }} .grade-badge {{ font-size: 45px; background-color: {theme_map[color_theme]['badge']}; color: white; padding: 15px 50px; border-radius: 50px; display: inline-block; font-weight: bold; margin-top: 30px; }} .topic {{ font-size: 42px; color: #34495e; margin-top: 70px; font-weight: bold; }} .sub-topic {{ font-size: 32px; color: #7f8c8d; margin-top: 10px; }} .icons {{ font-size: 110px; margin: 60px 0; }} .details-badge {{ background-color: #2ecc71; color: white; display: inline-block; padding: 15px 40px; border-radius: 15px; font-size: 32px; font-weight: bold; }} .footer {{ position: absolute; bottom: 40px; left: 0; width: 100%; text-align: center; font-size: 22px; color: #7f8c8d; }} </style></head><body>{ebook_body}</body></html>"""

        filename_base = f"{selected_grade}_{selected_sub}"
        st.session_state['ebook_html'] = full_ebook_html
        st.session_state['filename_base'] = f"{filename_base}_{int(time.time())}"
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(f"{filename_base}_Full_EBook.html", full_ebook_html.encode('utf-8'))
            zip_file.writestr(f"{filename_base}_Worksheet.html", html_w.encode('utf-8'))
            zip_file.writestr(f"{filename_base}_AnswerKey.html", html_k.encode('utf-8'))
        st.session_state['zip_data'] = zip_buffer.getvalue()

if 'ebook_html' in st.session_state:
    st.success(f"✅ สร้างไฟล์สำเร็จ! (เฉลยถูกอัปเกรดเป็นแบบอธิบายทีละบรรทัด พร้อมบอกที่มาของตัวเลขทุกตัวครับ!)")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📄 โหลดเฉพาะโจทย์", data=st.session_state['worksheet_html'], file_name=f"{st.session_state['filename_base']}_Worksheet.html", mime="text/html", use_container_width=True)
        st.download_button("🔑 โหลดเฉพาะเฉลย", data=st.session_state['answerkey_html'], file_name=f"{st.session_state['filename_base']}_AnswerKey.html", mime="text/html", use_container_width=True)
    with c2:
        st.download_button("📚 โหลดรวมเล่ม E-Book", data=st.session_state['ebook_html'], file_name=f"{st.session_state['filename_base']}_Full_EBook.html", mime="text/html", use_container_width=True)
        st.download_button("🗂️ โหลดแพ็กเกจ (.zip)", data=st.session_state['zip_data'], file_name=f"{st.session_state['filename_base']}.zip", mime="application/zip", use_container_width=True)
    st.markdown("---")
    components.html(st.session_state['ebook_html'], height=800, scrolling=True)
