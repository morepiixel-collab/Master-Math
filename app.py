import streamlit as st
import streamlit.components.v1 as components
import random
import math
import zipfile
import io
import time

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
    <p>ระบบสร้างสื่อการสอนคณิตศาสตร์ พร้อมข้อสอบแข่งขัน TMC + ภาพอธิบายเฉลย (Visual Models) ขั้นเทพ!</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 1. ฐานข้อมูลหลักสูตร (Master Database)
# ==========================================

# จัดกลุ่มหัวข้อแข่งขันตามระดับชั้น (ตรวจสอบแล้วว่าไม่เกินเนื้อหาเด็ก)
comp_topics_p1_p2 = [
    "ตรรกะตาชั่งสมดุล", "การนับหน้าหนังสือ", "ปัญหาผลรวม-ผลต่าง", 
    "โปรโมชั่นแลกของ", "หยิบของในที่มืด", "การคิดย้อนกลับ", "แถวคอยแบบซ้อนทับ"
]

comp_topics_p3_p4 = [
    "ปริศนาตัวเลขซ่อนแอบ", "การปักเสาและปลูกต้นไม้", "สัตว์ปีนบ่อ", 
    "ตรรกะการจับมือ (ทักทาย)", "แผนภาพความชอบ", "คิววงกลมมรณะ", "อายุข้ามเวลาขั้นสูง"
]

comp_topics_p5_p6 = [
    "ลำดับแบบวนลูป", "เส้นทางที่เป็นไปได้", "นาฬิกาเดินเพี้ยน", 
    "จัดของใส่กล่อง", "คะแนนยิงเป้า", "การตัดเชือกพับทบ"
]

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
        "แผนภูมิรูปภาพ": ["การอ่านแผนภูมิรูปภาพ"],
        "🌟 โจทย์แข่งขัน (แนว TMC)": comp_topics_p1_p2
    },
    "ป.3": {
        "จำนวนนับและเศษส่วน": ["การอ่าน การเขียนตัวเลข", "หลัก ค่าของเลขโดด และรูปกระจาย", "การเปรียบเทียบจำนวน (> <)", "การเรียงลำดับจำนวน (น้อยไปมาก)", "การเรียงลำดับจำนวน (มากไปน้อย)", "การอ่านและเขียนเศษส่วน", "การบวกลบเศษส่วน (ตัวส่วนเท่ากัน)"],
        "เวลา เงิน และการวัด": ["การบอกเวลาเป็นนาฬิกาและนาที", "การบอกจำนวนเงินทั้งหมด", "การอ่านน้ำหนักจากเครื่องชั่งสปริง"],
        "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การคูณ (แบบตั้งหลัก)", "การหารยาว"],
        "แผนภูมิรูปภาพ": ["การอ่านแผนภูมิรูปภาพ"],
        "🌟 โจทย์แข่งขัน (แนว TMC)": comp_topics_p1_p2 + comp_topics_p3_p4
    },
    "ป.4": {
        "จำนวนนับที่มากกว่า 100,000": ["การอ่านและการเขียนตัวเลข", "หลัก ค่าประจำหลัก และรูปกระจาย", "การเปรียบเทียบและเรียงลำดับ", "ค่าประมาณเป็นจำนวนเต็มสิบ เต็มร้อย เต็มพัน"],
        "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การคูณ (แบบตั้งหลัก)", "การหารยาว"],
        "เศษส่วนและทศนิยม": ["แปลงเศษเกินเป็นจำนวนคละ", "การอ่านและการเขียนทศนิยม"],
        "เรขาคณิตและการวัด": ["การบอกชนิดของมุม", "การวัดขนาดของมุม (ไม้โปรแทรกเตอร์)", "การหาความยาวรอบรูปสี่เหลี่ยมมุมฉาก", "การหาพื้นที่รูปสี่เหลี่ยมมุมฉาก"],
        "สมการ": ["การแก้สมการ (บวก/ลบ)"],
        "🌟 โจทย์แข่งขัน (แนว TMC)": comp_topics_p1_p2 + comp_topics_p3_p4
    },
    "ป.5": {
        "เศษส่วน": ["การบวกเศษส่วน", "การลบเศษส่วน", "การคูณเศษส่วน", "การหารเศษส่วน"],
        "ทศนิยม": ["การบวกและการลบทศนิยม", "การคูณทศนิยม"],
        "ร้อยละและเปอร์เซ็นต์": ["การเขียนเศษส่วนในรูปร้อยละ"],
        "สมการ": ["การแก้สมการ (คูณ/หาร)"],
        "🌟 โจทย์แข่งขัน (แนว TMC)": comp_topics_p1_p2 + comp_topics_p3_p4 + comp_topics_p5_p6
    },
    "ป.6": {
        "ตัวประกอบของจำนวนนับ": ["การหา ห.ร.ม.", "การหา ค.ร.น."],
        "อัตราส่วนและร้อยละ": ["การหาอัตราส่วนที่เท่ากัน", "โจทย์ปัญหาอัตราส่วน", "โจทย์ปัญหาร้อยละ"],
        "สมการ": ["การแก้สมการ (สองขั้นตอน)"],
        "🌟 โจทย์แข่งขัน (แนว TMC)": comp_topics_p1_p2 + comp_topics_p3_p4 + comp_topics_p5_p6
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
                    if carry > 0: top_marks[i] = str(carry); carry = 0
                    continue
                prod = a_digits[i] * b_val + carry
                carry = prod // 10
                if carry > 0 and i > 0: top_marks[i-1] = str(carry)
                
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
    if num == 0: return "เศษส่วนที่มีตัวเศษเป็น 0 จะมีค่าเท่ากับ 0 เสมอ", "<span style='font-size: 24px; font-weight: bold; color: red;'>0</span>"
    if num == den: return "เศษส่วนที่มีตัวเศษและตัวส่วนเท่ากัน (หารกันลงตัวพอดี) จะมีค่าเท่ากับ 1 เสมอ", "<span style='font-size: 24px; font-weight: bold; color: red;'>1</span>"
    
    sim_num, sim_den = num // g, den // g
    extra_steps, final_html = "", ""
    
    if sim_den == 1:
        final_html = f"<span style='font-size: 24px; font-weight: bold; color: red;'>{sim_num}</span>"
        if g > 1: extra_steps = f"ทอนเป็นเศษส่วนอย่างต่ำ (นำ {g} มาหารทั้งเศษและส่วน) จะได้ผลลัพธ์เป็นจำนวนเต็ม"
    elif sim_num > sim_den:
        w, r = sim_num // sim_den, sim_num % sim_den
        final_html = generate_mixed_number_html(w, r, sim_den)
        if g > 1: extra_steps = f"ทอนเป็นเศษส่วนอย่างต่ำ (นำ {g} มาหารทั้งเศษและส่วน) และแปลงเศษเกินให้อยู่ในรูปจำนวนคละ"
        else: extra_steps = f"แปลงเศษเกินให้อยู่ในรูปจำนวนคละ"
    else:
        final_html = f"""<div style="display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; margin: 0 5px; font-family: 'Sarabun', sans-serif;"><span style="font-size: 20px; font-weight: bold; border-bottom: 2px solid red; padding: 0 4px; line-height: 1.1; color: red;">{sim_num}</span><span style="font-size: 20px; font-weight: bold; padding: 0 4px; line-height: 1.1; color: red;">{sim_den}</span></div>"""
        if g > 1: extra_steps = f"ทอนเป็นเศษส่วนอย่างต่ำโดยนำ {g} มาหารทั้งเศษและส่วน"
        
    return extra_steps, final_html

def generate_short_division_html(a, b, mode="ห.ร.ม."):
    factors = []
    ca, cb = a, b
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
        if not found: break
        
    if not factors: 
        if mode == "ห.ร.ม.":
            return f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) ลองหาตัวเลขที่สามารถหารทั้ง {a} และ {b} ลงตัวพร้อมกัน<br>2) พบว่าไม่มีตัวเลขใดเลยที่หารทั้งคู่ลงตัว (นอกจาก 1)<br><b>ดังนั้น ห.ร.ม. = 1</b></span>"
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
    str_a, str_b = f"{a:.2f}", f"{b:.2f}"
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
            a_chars, b_chars = list(str_a), list(str_b)
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
    div_str = str(dividend); div_len = len(div_str)
    
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

def generate_questions_logic(grade, main_t, sub_t, num_q):
    questions = []
    seen = set()
    limit_map = {"ป.1": 100, "ป.2": 1000, "ป.3": 100000, "ป.4": 1000000, "ป.5": 9000000, "ป.6": 9000000}
    limit = limit_map.get(grade, 100)

    NAMES_LIST = ["อคิณ", "นาวิน", "ภูผา", "สายฟ้า", "เจ้านาย", "ข้าวหอม", "ใบบัว", "มะลิ", "น้ำใส", "ญาญ่า", "ปลื้ม", "พายุ", "ไออุ่น", "กะทิ", "เวลา", "ของขวัญ", "มังกร", "ฉลาม", "ปลาวาฬ", "มาคิน"]
    LOCATIONS_LIST = ["โรงเรียน", "สวนสัตว์", "สวนสนุก", "ห้างสรรพสินค้า", "ห้องสมุด", "สวนสาธารณะ", "ร้านของเล่น", "ร้านเบเกอรี่", "ค่ายลูกเสือ", "พิพิธภัณฑ์"]
    ITEMS_LIST = ["ลูกแก้ว", "สติกเกอร์", "การ์ดโปเกมอน", "โมเดลรถ", "ตุ๊กตาหมี", "สมุดระบายสี", "ดินสอสี", "ลูกโป่ง", "ยางลบ", "ตัวต่อเลโก้", "หนังสือการ์ตูน", "ลูกบอล"]
    SNACKS_LIST = ["ช็อกโกแลต", "คุกกี้", "โดนัท", "เยลลี่", "ขนมปัง", "ไอศกรีม", "น้ำผลไม้", "นมเย็น", "ลูกอม", "เค้ก"]
    ANIMALS_LIST = ["แมงมุม", "มดแดง", "กบ", "จิ้งจก", "ตั๊กแตน", "เต่า"]

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
            elif sub_t == "🌟 สุ่มรวมทุกแนว":
                # เลือกลิสต์โจทย์แข่งขันตามช่วงชั้นที่สุ่มมา
                if grade in ["ป.1", "ป.2"]:
                    actual_sub_t = random.choice(comp_topics_p1_p2)
                elif grade in ["ป.3", "ป.4"]:
                    actual_sub_t = random.choice(comp_topics_p1_p2 + comp_topics_p3_p4)
                else:
                    actual_sub_t = random.choice(comp_topics_p1_p2 + comp_topics_p3_p4 + comp_topics_p5_p6)

            prefix = get_prefix(grade)

            # =========================================================
            # 🌟 โหมดข้อสอบแข่งขัน (TMC) - อธิบายละเอียดยิบแบบ Step-by-Step
            # =========================================================
            if actual_sub_t == "ปริศนาตัวเลขซ่อนแอบ":
                a = random.randint(1, 4)
                b = random.randint(a + 2, 9)
                diff = b - a
                k = diff * 9
                sum_val = a + b
                q = f"ให้ A และ B เป็นเลขโดดที่ต่างกัน โดยที่จำนวนสองหลัก <b>AB</b> เมื่อนำมาบวกกับ <b>{k}</b> จะได้ผลลัพธ์เป็นจำนวนสลับหลักคือ <b>BA</b> (นั่นคือ AB + {k} = BA) และโจทย์กำหนดให้ <b>A + B = {sum_val}</b> <br>จงหาว่าจำนวนสองหลัก <b>AB</b> คือจำนวนใด?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                1) จากประโยค "AB + {k} = BA" ถ้านำ AB ไปลบออกทั้งสองข้าง จะได้ <b>BA - AB = {k}</b><br>
                2) ความลับของตัวเลขสลับหลักคือ: ผลต่างของ BA และ AB จะมีค่าเท่ากับ <b>(B - A) × 9 เสมอ!</b><br>
                ดังนั้น เราหาผลต่างของเลขโดดได้โดย: B - A = {k} ÷ 9 = <b>{diff}</b><br>
                3) ตอนนี้เรารู้ข้อมูล 2 อย่างคือ:<br>
                &nbsp;&nbsp;&nbsp;ผลบวก: A + B = <b>{sum_val}</b> (จากที่โจทย์กำหนด)<br>
                &nbsp;&nbsp;&nbsp;ผลต่าง: B - A = <b>{diff}</b><br>
                4) ลองหาเลขโดด 2 ตัวที่บวกกันได้ {sum_val} และลบกันได้ {diff}:<br>
                &nbsp;&nbsp;&nbsp;นำผลบวกและผลต่างมารวมกัน: {sum_val} + {diff} = {sum_val + diff}<br>
                &nbsp;&nbsp;&nbsp;แบ่งครึ่งเพื่อหาค่า B: {sum_val + diff} ÷ 2 = <b>{b}</b><br>
                &nbsp;&nbsp;&nbsp;เมื่อ B คือ {b} ดังนั้น A คือ {sum_val} - {b} = <b>{a}</b><br>
                ตรวจคำตอบ: {a}{b} + {k} = {b}{a} (ถูกต้อง!)<br>
                <b>ตอบ: จำนวน AB คือ {a}{b}</b></span>"""

            elif actual_sub_t == "การนับหน้าหนังสือ":
                pages = random.randint(40, 150)
                item = random.choice(ITEMS_LIST)
                q = f"โรงพิมพ์กำลังจัดพิมพ์หนังสือแคตตาล็อกแนะนำ<b>{item}</b> ซึ่งมีความหนาทั้งหมด <b>{pages}</b> หน้า หากต้องการพิมพ์ตัวเลขหน้าทั้งหมดตั้งแต่หน้า 1 ถึงหน้า {pages} จะต้องพิมพ์ตัวเลขโดด (0-9) รวมทั้งหมดกี่ตัว?"
                if pages > 99:
                    ans = 9 + 180 + ((pages - 99) * 3)
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                    เราจะแบ่งการนับตัวเลขหน้าออกเป็นกลุ่มตามจำนวนหลัก ดังนี้ครับ:<br>
                    1) <b>กลุ่มเลข 1 หลัก (หน้า 1 ถึง 9):</b> มีทั้งหมด 9 หน้า<br>
                    &nbsp;&nbsp;&nbsp;ใช้ตัวเลขหน้าละ 1 ตัว = 9 × 1 = <b>9 ตัว</b><br>
                    2) <b>กลุ่มเลข 2 หลัก (หน้า 10 ถึง 99):</b> มีทั้งหมด 90 หน้า (คิดจาก 99 - 9 หน้าแรก)<br>
                    &nbsp;&nbsp;&nbsp;ใช้ตัวเลขหน้าละ 2 ตัว = 90 × 2 = <b>180 ตัว</b><br>
                    3) <b>กลุ่มเลข 3 หลัก (หน้า 100 ถึง {pages}):</b> มีทั้งหมด {pages} - 99 = {pages - 99} หน้า<br>
                    &nbsp;&nbsp;&nbsp;ใช้ตัวเลขหน้าละ 3 ตัว = {pages - 99} × 3 = <b>{(pages - 99) * 3} ตัว</b><br>
                    นำจำนวนตัวเลขที่ใช้ของทุกกลุ่มมาบวกกัน:<br>
                    9 + 180 + {(pages - 99) * 3} = <b>{ans} ตัว</b><br>
                    <b>ตอบ: ต้องใช้ตัวเลขโดดทั้งหมด {ans} ตัว</b></span>"""
                else:
                    ans = 9 + ((pages - 9) * 2)
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                    เราจะแบ่งการนับตัวเลขหน้าออกเป็นกลุ่มตามจำนวนหลัก ดังนี้ครับ:<br>
                    1) <b>กลุ่มเลข 1 หลัก (หน้า 1 ถึง 9):</b> มีทั้งหมด 9 หน้า<br>
                    &nbsp;&nbsp;&nbsp;ใช้ตัวเลขหน้าละ 1 ตัว = 9 × 1 = <b>9 ตัว</b><br>
                    2) <b>กลุ่มเลข 2 หลัก (หน้า 10 ถึง {pages}):</b> มีทั้งหมด {pages} - 9 (หน้าแรก) = {pages - 9} หน้า<br>
                    &nbsp;&nbsp;&nbsp;ใช้ตัวเลขหน้าละ 2 ตัว = {pages - 9} × 2 = <b>{(pages - 9) * 2} ตัว</b><br>
                    นำจำนวนตัวเลขที่ใช้ของทุกกลุ่มมาบวกกัน:<br>
                    9 + {(pages - 9) * 2} = <b>{ans} ตัว</b><br>
                    <b>ตอบ: ต้องใช้ตัวเลขโดดทั้งหมด {ans} ตัว</b></span>"""

            elif actual_sub_t == "การปักเสาและปลูกต้นไม้":
                d = random.choice([2, 4, 5, 10, 15])
                trees = random.randint(12, 35)
                length = (trees - 1) * d
                loc = random.choice(LOCATIONS_LIST)
                q = f"เทศบาลต้องการปลูกต้นไม้ริมถนนทางเข้า<b>{loc}</b> โดยให้ต้นไม้แต่ละต้นอยู่ห่างกันระยะทาง <b>{d}</b> เมตร และมีเงื่อนไขว่า <b>ต้องปลูกต้นไม้ที่จุดเริ่มต้นและจุดสิ้นสุดของถนนพอดี</b> หากปลูกเสร็จแล้วนับต้นไม้ได้ทั้งหมด <b>{trees}</b> ต้น ถนนเส้นนี้ยาวกี่เมตร?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                1) ลองนึกภาพตามนะครับ ถ้าเราปลูกต้นไม้ 3 ต้น จะเกิดช่องว่างระหว่างต้นไม้แค่ 2 ช่อง, ถ้าปลูก 4 ต้น จะเกิดช่องว่าง 3 ช่อง<br>
                2) สรุปได้ว่า <b>จำนวนช่องว่าง จะน้อยกว่าจำนวนต้นไม้อยู่ 1 เสมอ</b> (เพราะปลูกปิดหัวท้าย)<br>
                3) ในโจทย์นี้ มีต้นไม้ทั้งหมด {trees} ต้น <br>
                &nbsp;&nbsp;&nbsp;ดังนั้น จะมีช่องว่างทั้งหมด = {trees} - 1 = <b>{trees - 1} ช่องว่าง</b><br>
                4) โจทย์บอกว่า 1 ช่องว่าง มีระยะห่าง {d} เมตร<br>
                &nbsp;&nbsp;&nbsp;นำจำนวนช่องว่างไปคูณกับระยะห่าง: {trees - 1} ช่อง × {d} เมตร = <b>{length} เมตร</b><br>
                <b>ตอบ: ถนนเส้นนี้มีความยาว {length} เมตร</b></span>"""

            elif actual_sub_t == "สัตว์ปีนบ่อ":
                u = random.randint(3, 7)
                d = random.randint(1, u - 1)
                net = u - d
                h = random.randint(15, 30)
                days = math.ceil((h - u) / net) + 1
                animal = random.choice(ANIMALS_LIST)
                q = f"<b>{animal}</b>ตัวหนึ่งตกลงไปในบ่อดินที่ลึก <b>{h}</b> เมตร ในช่วงเวลากลางวันมีความพยายามปีนขึ้นมาได้ <b>{u}</b> เมตร แต่เมื่อถึงเวลากลางคืนต้องนอนหลับ ทำให้ลื่นไถลตกลงไป <b>{d}</b> เมตร <b>{animal}</b>ตัวนี้จะต้องใช้เวลาอย่างน้อยที่สุดกี่วันจึงจะปีนพ้นปากบ่อ?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                1) ใน 1 วัน (24 ชม. ทั้งขึ้นและลง) จะปีนได้ระยะทางสุทธิคือ: {u} (ขึ้น) - {d} (ลง) = <b>{net} เมตร</b><br>
                2) <i>จุดหลอกที่ต้องระวัง:</i> ในวันสุดท้ายเมื่อปีนพ้นขอบบ่อไปแล้ว จะไม่ต้องลื่นตกลงมาอีก! เราจึงต้องแยกคิดวันสุดท้ายออกมาก่อน<br>
                3) หาระยะทางก่อนจะถึงการปีนในวันสุดท้าย:<br>
                &nbsp;&nbsp;&nbsp;ความลึกทั้งหมด {h} - ระยะปีนวันสุดท้าย {u} = <b>{h - u} เมตร</b><br>
                4) หาเวลาที่ใช้ปีนระยะทางช่วงแรก:<br>
                &nbsp;&nbsp;&nbsp;{h - u} เมตร ÷ {net} เมตร/วัน = <b>{math.ceil((h - u) / net)} วัน</b><br>
                5) นำเวลาช่วงแรกไปบวกกับวันสุดท้ายอีก 1 วัน:<br>
                &nbsp;&nbsp;&nbsp;{math.ceil((h - u) / net)} + 1 = <b>{days} วัน</b><br>
                <b>ตอบ: ต้องใช้เวลาทั้งหมด {days} วัน</b></span>"""

            elif actual_sub_t == "ตรรกะตาชั่งสมดุล":
                items_pair = [("รถคันใหญ่", "รถคันเล็ก", "ลูกบอล"), ("หนังสือหนา", "สมุดบาง", "ดินสอ"), ("แตงโม", "ส้ม", "มะนาว")]
                i1, i2, i3 = random.choice(items_pair)
                m1 = random.randint(2, 5)
                m2 = random.randint(2, 5)
                q = f"จากการเล่นตาชั่งสมดุล พบข้อมูลดังนี้:<br>- <b>{i1} 1 ชิ้น</b> หนักเท่ากับ <b>{i2} {m1} ชิ้น</b><br>- <b>{i2} 1 ชิ้น</b> หนักเท่ากับ <b>{i3} {m2} ชิ้น</b><br><br>อยากทราบว่า <b>{i1} จำนวน 2 ชิ้น</b> จะมีน้ำหนักเท่ากับ <b>{i3}</b> กี่ชิ้น?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                เป้าหมายของเราคือการเปลี่ยนของที่ใหญ่ที่สุด ({i1}) ให้กลายเป็นของที่เล็กที่สุด ({i3}) ทีละขั้นตอนครับ<br>
                1) จากข้อมูลบรรทัดที่ 2: เรารู้แล้วว่า {i2} 1 ชิ้น สามารถแลกเปลี่ยนเป็น {i3} ได้ <b>{m2} ชิ้น</b><br>
                2) จากข้อมูลบรรทัดที่ 1: {i1} 1 ชิ้น มีน้ำหนักเท่ากับ {i2} จำนวน {m1} ชิ้น<br>
                &nbsp;&nbsp;&nbsp;ให้นำความรู้จากข้อ 1 มาแทนค่า: เปลี่ยน {i2} {m1} ชิ้น ให้กลายเป็น {i3}<br>
                &nbsp;&nbsp;&nbsp;จะได้ว่า {i1} 1 ชิ้น = มีอยู่ {m1} กลุ่ม กลุ่มละ {m2} ชิ้น<br>
                &nbsp;&nbsp;&nbsp;ดังนั้น {i1} 1 ชิ้น = {m1} × {m2} = <b>{m1 * m2} ชิ้น (ในหน่วย {i3})</b><br>
                3) แต่โจทย์ไม่ได้ถามหา {i1} แค่ 1 ชิ้น โจทย์ถามหา {i1} <b>2 ชิ้น</b><br>
                &nbsp;&nbsp;&nbsp;เราจึงต้องนำน้ำหนักไปคูณ 2: {m1 * m2} × 2 = <b>{m1 * m2 * 2} ชิ้น</b><br>
                <b>ตอบ: หนักเท่ากับ {i3} ทั้งหมด {m1 * m2 * 2} ชิ้น</b></span>"""

            elif actual_sub_t == "ปัญหาผลรวม-ผลต่าง":
                diff = random.randint(5, 20)
                small = random.randint(10, 30)
                large = small + diff
                total = large + small
                n1, n2 = random.sample(NAMES_LIST, 2)
                itm = random.choice(ITEMS_LIST)
                q = f"<b>{n1}</b> และ <b>{n2}</b> มี<b>{itm}</b>รวมกันทั้งหมด <b>{total}</b> ชิ้น หากทราบว่า <b>{n1}</b> มีมากกว่า <b>{n2}</b> อยู่ <b>{diff}</b> ชิ้น จงหาว่า <b>{n1}</b> มี<b>{itm}</b>กี่ชิ้น?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                1) ลองนึกภาพว่าเรานำของของ {n1} และ {n2} มาวางกองคู่กัน กองของ {n1} จะสูงกว่า {n2} อยู่ {diff} ชิ้น<br>
                2) ถ้าเราหยิบของที่ "เกินมา" ({diff} ชิ้น) ออกไปจากกองรวมก่อน <br>
                &nbsp;&nbsp;&nbsp;ของที่เหลือจะคือส่วนที่ <b>{n1} และ {n2} มีเท่าๆ กันพอดี</b><br>
                &nbsp;&nbsp;&nbsp;เหลือของ: {total} (ทั้งหมด) - {diff} (ส่วนที่เกิน) = <b>{total - diff} ชิ้น</b><br>
                3) นำของที่เหลือมาแบ่งครึ่งให้ 2 คน คนละเท่าๆ กัน (ซึ่งนี่คือจำนวนของคนที่น้อยกว่า คือ {n2})<br>
                &nbsp;&nbsp;&nbsp;จำนวนของ {n2}: {total - diff} ÷ 2 = <b>{small} ชิ้น</b><br>
                4) โจทย์ถามหาจำนวนของ {n1} ซึ่งเป็นคนที่มีมากกว่า<br>
                &nbsp;&nbsp;&nbsp;จำนวนของ {n1}: {small} (ส่วนที่เท่ากัน) + {diff} (ส่วนที่มากกว่า) = <b>{large} ชิ้น</b><br>
                <b>ตอบ: {n1} มี{itm}ทั้งหมด {large} ชิ้น</b></span>"""

            elif actual_sub_t == "ตรรกะการจับมือ (ทักทาย)":
                n = random.randint(5, 10)
                loc = random.choice(LOCATIONS_LIST)
                # สร้างข้อความบวกเลขแบบแจกแจงให้ดูยาวๆ
                sum_str_list = [str(x) for x in range(n-1, 0, -1)]
                sum_display = " + ".join(sum_str_list)
                ans = sum(range(1, n))
                q = f"ในการจัดกิจกรรมที่<b>{loc}</b> มีเด็กมาร่วมกลุ่มทั้งหมด <b>{n}</b> คน หากเด็กทุกคนต้องเดินไปจับมือทำความรู้จักกันให้ครบทุกคน (จับมือกันคนละ 1 ครั้งโดยไม่ซ้ำคนเดิม) จะมีการจับมือเกิดขึ้นทั้งหมดกี่ครั้ง?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                เราจะนับการจับมือทีละคน เพื่อให้เห็นภาพและไม่ให้มีการนับซ้ำซ้อนกันครับ<br>
                1) <b>คนที่ 1:</b> ต้องเดินไปจับมือกับเพื่อนคนอื่นที่เหลืออีก <b>{n-1} คน</b> (เกิดการจับมือขึ้น {n-1} ครั้ง)<br>
                2) <b>คนที่ 2:</b> ต้องเดินไปจับมือกับเพื่อนคนอื่น (แต่ไม่ต้องไปจับคนที่ 1 แล้ว เพราะจับกันไปแล้วเมื่อกี้!) จึงเหลือเพื่อนให้จับอีก <b>{n-2} คน</b><br>
                3) <b>คนที่ 3:</b> เหลือเพื่อนให้จับมืออีก <b>{n-3} คน</b><br>
                ...ทำแบบนี้ลดหลั่นไปเรื่อยๆ จนถึงคนรองสุดท้าย จะเหลือคนให้จับอีกแค่ 1 คน ส่วนคนสุดท้ายไม่ต้องเดินไปหาใครแล้วเพราะโดนจับครบหมดแล้ว<br>
                4) นำจำนวนการจับมือของแต่ละคนมาบวกกันทั้งหมดจะได้:<br>
                &nbsp;&nbsp;&nbsp;{sum_display} = <b>{ans} ครั้ง</b><br>
                <b>ตอบ: เกิดการจับมือขึ้นทั้งหมด {ans} ครั้ง</b></span>"""

            elif actual_sub_t == "การคิดย้อนกลับ":
                s_money = random.randint(100, 300)
                spent = random.randint(20, 80)
                recv = random.randint(50, 150)
                f_money = s_money - spent + recv
                name = random.choice(NAMES_LIST)
                item = random.choice(ITEMS_LIST)
                q = f"<b>{name}</b>นำเงินไปซื้อ<b>{item}</b> <b>{spent}</b> บาท จากนั้นคุณแม่ให้ค่าขนมเพิ่มมาอีก <b>{recv}</b> บาท เมื่อกลับถึงบ้าน<b>{name}</b>ลองนับเงินดูพบว่าตอนนี้มีเงินเหลือ <b>{f_money}</b> บาท <br>จงหาว่าตอนแรกก่อนออกจากบ้าน <b>{name}</b>มีเงินอยู่ในกระเป๋ากี่บาท?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (หลักการคิดย้อนกลับ):</b><br>
                การคิดย้อนกลับ คือการเริ่มจากเหตุการณ์สุดท้าย ย้อนกลับไปหาจุดเริ่มต้น โดยการ "ทำกระบวนการตรงกันข้าม" (บวกให้เปลี่ยนเป็นลบ, ลบให้เปลี่ยนเป็นบวก)<br>
                1) <b>เหตุการณ์สุดท้าย (ปัจจุบัน):</b> ตอนนี้มีเงินเหลือ <b>{f_money} บาท</b><br>
                2) <b>ย้อนกลับเหตุการณ์ 'แม่ให้เพิ่ม':</b> แม่ให้มา {recv} บาท (ของจริงเงินเพิ่ม ย้อนกลับคือต้องนำไป <b>ลบออก</b>)<br>
                &nbsp;&nbsp;&nbsp;ก่อนแม่ให้ จะมีเงิน: {f_money} - {recv} = <b>{f_money - recv} บาท</b><br>
                3) <b>ย้อนกลับเหตุการณ์ 'ซื้อของ':</b> ซื้อของไป {spent} บาท (ของจริงเงินลดลง ย้อนกลับคือต้องนำไป <b>บวกคืน</b>)<br>
                &nbsp;&nbsp;&nbsp;ก่อนซื้อของ (ตอนแรกสุด) จะมีเงิน: {f_money - recv} + {spent} = <b>{s_money} บาท</b><br>
                <b>ตอบ: ตอนแรกมีเงินอยู่ในกระเป๋า {s_money} บาท</b></span>"""

            elif actual_sub_t == "แผนภาพความชอบ":
                tot = random.randint(30, 50)
                both = random.randint(5, 12)
                only_a = random.randint(8, 15)
                only_b = random.randint(8, 15)
                l_a = only_a + both
                l_b = only_b + both
                neither = tot - (only_a + only_b + both)
                n1, n2 = random.sample(SNACKS_LIST, 2)
                q = f"จากการสำรวจนักเรียน <b>{tot}</b> คน พบว่ามีคนชอบกิน<b>{n1}</b> จำนวน <b>{l_a}</b> คน, มีคนชอบกิน<b>{n2}</b> จำนวน <b>{l_b}</b> คน, และมีคนที่ชอบกินทั้งสองอย่าง จำนวน <b>{both}</b> คน <br>อยากทราบว่ามีนักเรียนกี่คนในกลุ่มนี้ ที่<b>ไม่ชอบกินขนมทั้งสองชนิดนี้เลย</b>?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                ข้อนี้เราจะนำตัวเลข <b>{l_a}</b> กับ <b>{l_b}</b> มาบวกกันตรงๆ ไม่ได้ครับ เพราะมันมีคนที่ชอบทั้งสองอย่าง (<b>{both}</b> คน) ถูกนับซ้ำซ้อนไปแล้วในทั้งสองกลุ่ม!<br>
                1) หาจำนวนคนที่ชอบ <b>{n1} อย่างเดียว</b> (โดยเอาคนที่ชอบทั้งคู่ออกไป):<br>
                &nbsp;&nbsp;&nbsp;{l_a} - {both} = <b>{only_a} คน</b><br>
                2) หาจำนวนคนที่ชอบ <b>{n2} อย่างเดียว</b> (โดยเอาคนที่ชอบทั้งคู่ออกไป):<br>
                &nbsp;&nbsp;&nbsp;{l_b} - {both} = <b>{only_b} คน</b><br>
                3) หาจำนวนคนที่ <b>ชอบขนมอย่างน้อย 1 ชนิด</b> โดยนำ 3 กลุ่มที่ไม่ซ้ำกันมาบวกกัน (ชอบอย่างแรก + ชอบอย่างหลัง + ชอบทั้งคู่):<br>
                &nbsp;&nbsp;&nbsp;{only_a} + {only_b} + {both} = <b>{only_a + only_b + both} คน</b><br>
                4) หาคนที่ <b>ไม่ชอบเลย</b> โดยนำคนทั้งหมดตั้ง ลบด้วยคนที่ชอบขนม:<br>
                &nbsp;&nbsp;&nbsp;{tot} (ทั้งหมด) - {only_a + only_b + both} (คนที่ชอบ) = <b>{neither} คน</b><br>
                <b>ตอบ: มีคนที่ไม่ชอบเลยจำนวน {neither} คน</b></span>"""

            elif actual_sub_t == "ผลบวกจำนวนเรียงกัน (Gauss)":
                n = random.choice([10, 20, 50, 100])
                ans = (n * (n + 1)) // 2
                q = f"จงหาผลบวกของตัวเลขเรียงลำดับตั้งแต่ 1 ถึง {n} <br>( 1 + 2 + 3 + ... + {n} = ? )"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (หลักการจับคู่ของเกาส์):</b><br>
                แทนที่เราจะบวกเรียงไปทีละตัว เราจะใช้วิธีนำ "ตัวหน้าสุด" จับคู่บวกกับ "ตัวหลังสุด" ครับ<br>
                1) จับคู่ตัวแรกกับตัวสุดท้าย: <b>1 + {n} = {n+1}</b><br>
                2) จับคู่ตัวที่สองกับตัวรองสุดท้าย: <b>2 + {n-1} = {n+1}</b><br>
                3) จับคู่ตัวที่สามกับตัวถัดมา: <b>3 + {n-2} = {n+1}</b><br>
                จะเห็นว่าทุกคู่เมื่อจับมาบวกกันแล้วจะได้ผลลัพธ์เป็น <b>{n+1}</b> เสมอ!<br>
                4) มีตัวเลขทั้งหมด {n} ตัว เมื่อเรานำมาจับคู่ทีละ 2 ตัว จะได้ทั้งหมด: {n} ÷ 2 = <b>{n//2} คู่</b><br>
                5) นำผลบวกของ 1 คู่ ไปคูณกับ จำนวนคู่ทั้งหมด:<br>
                &nbsp;&nbsp;&nbsp;{n+1} (ผลบวกแต่ละคู่) × {n//2} (จำนวนคู่) = <b>{ans:,}</b><br>
                <b>ตอบ: ผลบวกคือ {ans:,}</b></span>"""

            elif actual_sub_t == "คิววงกลมมรณะ":
                n_half = random.randint(4, 12)
                total = n_half * 2
                pos1 = random.randint(1, n_half)
                pos2 = pos1 + n_half
                n1, n2 = random.sample(NAMES_LIST, 2)
                q = f"เด็กกลุ่มหนึ่งยืนล้อมกันเป็นวงกลมโดยเว้นระยะห่างเท่าๆ กัน และมีการนับหมายเลขเรียงตามลำดับ 1, 2, 3... ไปเรื่อยๆ จนครบทุกคน <br>ถ้า <b>{n1}</b> ยืนอยู่ที่ตำแหน่งหมายเลข <b>{pos1}</b> และมองไปฝั่งตรงข้ามพอดีเป๊ะ พบว่า <b>{n2}</b> ยืนอยู่ที่ตำแหน่งหมายเลข <b>{pos2}</b> <br>จงหาว่าเด็กกลุ่มนี้มีทั้งหมดกี่คน?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                1) ลองจินตนาการถึงหน้าปัดนาฬิกาครับ การที่คนสองคนยืนอยู่ "ฝั่งตรงข้ามกันพอดี" (เช่น เลข 12 ตรงข้ามกับเลข 6) หมายความว่าระยะห่างระหว่างสองคนนี้ คือ "ครึ่งวงกลม" พอดี<br>
                2) หาจำนวนคนในครึ่งวงกลม โดยนำหมายเลขของทั้งสองคนมาลบกัน:<br>
                &nbsp;&nbsp;&nbsp;{pos2} - {pos1} = <b>{n_half} คน</b><br>
                3) เมื่อเรารู้ว่าครึ่งวงกลมมี {n_half} คน การหาจำนวนคนทั้งหมดในวงกลมเต็มวง ก็เพียงแค่นำจำนวนคนในครึ่งวงกลมมาคูณ 2<br>
                &nbsp;&nbsp;&nbsp;{n_half} × 2 = <b>{total} คน</b><br>
                <b>ตอบ: เด็กกลุ่มนี้มีทั้งหมด {total} คน</b></span>"""

            elif actual_sub_t == "โปรโมชั่นแลกของ":
                exch = random.choice([3, 4, 5])
                start_bottles = exch * random.randint(3, 6)
                snack = random.choice(SNACKS_LIST)
                
                total_drank = start_bottles
                empties = start_bottles
                step_count = 1
                sol_steps = f"1) ตอนแรกซื้อกินไป <b>{start_bottles} ชิ้น</b> (ทำให้เราเก็บซองเปล่าไว้ได้ {start_bottles} ซอง)<br>"
                
                while empties >= exch:
                    step_count += 1
                    new_b = empties // exch
                    left_b = empties % exch
                    total_drank += new_b
                    sol_steps += f"{step_count}) นำซองเปล่า {new_b * exch} ซอง ไปแลกของใหม่มาได้อีก <b>{new_b} ชิ้น</b> (เราจะเหลือเศษซองที่ยังไม่ได้แลกอีก {left_b} ซอง)<br>"
                    empties = new_b + left_b
                    if empties >= exch:
                         sol_steps += f"&nbsp;&nbsp;&nbsp;<i>-> เมื่อเรากินของที่แลกมาใหม่หมด ตอนนี้เราจะมีซองเปล่ารวม {new_b} + {left_b} = {empties} ซอง นำไปแลกต่อได้อีก!</i><br>"
                         
                q = f"โปรโมชั่นพิเศษร้านค้า: นำซอง<b>{snack}</b>เปล่าจำนวน <b>{exch}</b> ซอง มาแลก<b>{snack}</b>ชิ้นใหม่ได้ฟรี 1 ชิ้น <br>หากนักเรียนมีเงินซื้อ<b>{snack}</b>มากินในตอนแรกทั้งหมด <b>{start_bottles}</b> ชิ้น นักเรียนจะสามารถกิน<b>{snack}</b>ได้รวมทั้งหมดกี่ชิ้น (ให้นับรวมกับของที่นำซองไปแลกฟรีมาใหม่ด้วย จนกว่าซองจะแลกไม่ได้อีก)?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                เราจะนำของเปล่าไปแลก แล้วนำเศษของเปล่าที่เหลือมารวมกับของที่แลกมาใหม่เพื่อนำไปแลกต่อเป็นทอดๆ ครับ<br>
                {sol_steps}<br>
                เมื่อบวกจำนวนชิ้นที่เราได้กินในทุกๆ รอบเข้าด้วยกัน จะได้:<br>
                รวมกินไปทั้งหมด = <b>{total_drank} ชิ้น</b> (และเราจะเหลือเศษซองเปล่า {empties} ซอง ซึ่งไม่พอแลกแล้ว)<br>
                <b>ตอบ: ได้กินรวมทั้งหมด {total_drank} ชิ้น</b></span>"""

            elif actual_sub_t == "หยิบของในที่มืด":
                c1 = random.randint(5, 12)
                c2 = random.randint(5, 12)
                c3 = random.randint(3, 8)
                item = random.choice(ITEMS_LIST)
                q = f"ในกล่องทึบใบหนึ่งมี<b>{item}</b>สีแดง <b>{c1}</b> ชิ้น, สีน้ำเงิน <b>{c2}</b> ชิ้น และสีเขียว <b>{c3}</b> ชิ้น ปะปนกันอยู่ <br>หากหลับตาหยิบ<b>{item}</b>ออกมาทีละชิ้น จะต้องหยิบออกมา<b>อย่างน้อยที่สุดกี่ชิ้น</b> จึงจะมั่นใจได้ 100% ว่าจะได้<b>{item}</b><b>สีเขียว</b>อย่างน้อย 1 ชิ้นแน่นอน?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (ใช้หลักการดวงซวยที่สุด หรือ Worst-case scenario):</b><br>
                เพื่อให้เรามั่นใจแบบ 100% เต็มว่าจะได้สีเขียวแน่ๆ เราต้องคิดคำนวณในกรณีที่เรา 'โชคร้ายที่สุด' ครับ<br>
                ความโชคร้ายที่สุดคือ: เราหยิบได้สีอื่นที่ไม่ใช่สีเขียวออกมาจนหมดกล่องเลย แล้วถึงจะได้สีเขียวในตอนท้ายสุด!<br>
                1) สมมติว่าเราโชคร้าย หยิบได้สีแดงออกมาหมดเลย = <b>{c1} ชิ้น</b><br>
                2) ยังโชคร้ายต่อ หยิบได้สีน้ำเงินออกมาหมดเลยอีก = <b>{c2} ชิ้น</b><br>
                ตอนนี้เราหยิบของออกไปแล้วรวม {c1} + {c2} = <b>{c1+c2} ชิ้น</b> (แต่ในมือเรายังไม่ได้สีเขียวเลยสักชิ้นเดียว!)<br>
                3) แต่ไม่ต้องห่วงครับ เพราะตอนนี้ของสีแดงและสีน้ำเงินหมดกล่องแล้ว การหยิบชิ้นต่อไป (บวกเพิ่มอีก 1) ในกล่องจะเหลือแต่สีเขียวล้วนๆ จึงการันตีว่าได้สีเขียว 100%<br>
                ดังนั้น จำนวนที่เราต้องหยิบอย่างน้อยคือ: {c1+c2} + 1 = <b>{c1+c2+1} ชิ้น</b><br>
                <b>ตอบ: ต้องหยิบอย่างน้อยที่สุด {c1+c2+1} ชิ้น</b></span>"""

            elif actual_sub_t == "ลำดับแบบวนลูป":
                word = random.choice(["MATHEMATICS", "THAILAND", "ELEPHANT", "SUPERMAN"])
                length = len(word)
                target = random.randint(30, 80)
                rem = target % length
                ans_char = word[rem - 1] if rem != 0 else word[-1]
                q = f"หากเราเขียนตัวอักษรภาษาอังกฤษคำว่า <b>{word}</b> เรียงต่อกันไปเรื่อยๆ ดังนี้:<br><b>{word}{word}{word[:3]}...</b><br><br>อยากทราบว่า ตัวอักษรในตำแหน่งที่ <b>{target}</b> คือตัวอักษรใด?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                นี่คือโจทย์แบบรูปที่วนซ้ำเป็นชุดๆ (Looping Pattern) ครับ<br>
                1) เริ่มจากนับจำนวนตัวอักษรใน 1 ชุด: คำว่า {word} มีตัวอักษรทั้งหมด <b>{length} ตัว</b><br>
                2) หาว่าตำแหน่งที่ {target} ที่โจทย์ถามนั้น กินความยาวไปกี่ชุด และเหลือเศษกี่ตัว โดยนำไปตั้งหาร:<br>
                &nbsp;&nbsp;&nbsp;{target} ÷ {length} = {target // length} ชุด และเหลือเศษ <b>{rem}</b><br>
                3) ความหมายของเศษ {rem} คือ: ให้เราไปดูตัวอักษร <b>ตัวที่ {rem if rem != 0 else length}</b> ของคำว่า {word}<br>
                &nbsp;&nbsp;&nbsp;<i>(จำไว้ว่า: ถ้าหารลงตัว หรือเหลือเศษ 0 จะหมายถึง 'ตัวอักษรตัวสุดท้าย' ของชุดนั้นๆ พอดีครับ)</i><br>
                เมื่อนับดูตัวที่ {rem if rem != 0 else length} ของคำว่า {word} จะพบว่าเป็นตัว <b>{ans_char}</b><br>
                <b>ตอบ: ตัวอักษรในตำแหน่งที่ {target} คือ {ans_char}</b></span>"""

            elif actual_sub_t == "เส้นทางที่เป็นไปได้":
                p1 = random.randint(2, 4)
                p2 = random.randint(2, 4)
                p3 = random.randint(1, 3)
                ans = (p1 * p2) + p3
                q = f"การเดินทางจากเมือง A ไปเมือง B มีถนนเชื่อมต่อกัน <b>{p1}</b> สาย และจากเมือง B ไปเมือง C มีถนนเชื่อมต่อกัน <b>{p2}</b> สาย <br>นอกจากนี้ ยังมีถนนเส้นทางลัดที่เดินทางจากเมือง A ตรงไปยังเมือง C โดยไม่ผ่านเมือง B อีก <b>{p3}</b> สาย<br>ถามว่า มีเส้นทางทั้งหมดกี่แบบในการเดินทางจากเมือง A ไปยังเมือง C ?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                เราต้องแบ่งการเดินทางออกเป็น 2 กรณีที่ไม่เกี่ยวข้องกัน แล้วนำผลลัพธ์มาบวกกันในตอนท้ายครับ<br>
                <b>กรณีที่ 1: เดินทางตามเส้นทางปกติ (ต้องผ่านเมือง B)</b><br>
                &nbsp;&nbsp;&nbsp;จาก A ไป B มี {p1} ทาง และ ทุกๆ 1 ทางสามารถแยกไป C ได้อีก {p2} ทาง<br>
                &nbsp;&nbsp;&nbsp;ใช้หลักการคูณ: เส้นทาง A->B ({p1} สาย) × เส้นทาง B->C ({p2} สาย) = <b>{p1 * p2} รูปแบบเส้นทาง</b><br>
                <b>กรณีที่ 2: เดินทางโดยใช้ทางลัด (ไม่ผ่านเมือง B)</b><br>
                &nbsp;&nbsp;&nbsp;โจทย์กำหนดให้มีทางลัดตรงจาก A ไป C เลย = <b>{p3} รูปแบบเส้นทาง</b><br>
                นำเส้นทางที่เป็นไปได้ของทั้งสองกรณีมารวมกัน:<br>
                {p1 * p2} (ผ่าน B) + {p3} (ทางลัด) = <b>{ans} รูปแบบเส้นทาง</b><br>
                <b>ตอบ: มีเส้นทางที่เป็นไปได้ทั้งหมด {ans} แบบ</b></span>"""

            elif actual_sub_t == "พื้นที่แรเงา (เรขาคณิต)":
                out_w = random.randint(10, 20)
                out_h = random.randint(10, 20)
                in_s = random.randint(3, min(out_w, out_h) - 2)
                q = f"กระดาษรูปสี่เหลี่ยมผืนผ้ากว้าง {out_w} ซม. ยาว {out_h} ซม. ถูกใช้กรรไกรเจาะรูตรงกลางเป็นรูปสี่เหลี่ยมจัตุรัสที่มีความยาวด้านละ {in_s} ซม. แล้วทิ้งไป <br>จงหาว่าพื้นที่กระดาษส่วนที่เหลือ (ไม่ได้ถูกเจาะ) มีขนาดกี่ตารางเซนติเมตร?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                หลักการของการหาพื้นที่ส่วนที่เหลือ คือการนำ <b>"พื้นที่ของรูปแผ่นใหญ่ทั้งหมด"</b> ลบออกด้วย <b>"พื้นที่ของส่วนที่ถูกเจาะทิ้งไป"</b><br>
                1) <b>หาพื้นที่ของกระดาษแผ่นใหญ่ (สี่เหลี่ยมผืนผ้า):</b><br>
                &nbsp;&nbsp;&nbsp;สูตรพื้นที่ผืนผ้า = กว้าง × ยาว<br>
                &nbsp;&nbsp;&nbsp;= {out_w} × {out_h} = <b>{out_w * out_h} ตารางเซนติเมตร</b><br>
                2) <b>หาพื้นที่ของรูที่เจาะทิ้ง (สี่เหลี่ยมจัตุรัส):</b><br>
                &nbsp;&nbsp;&nbsp;สูตรพื้นที่จัตุรัส = ด้าน × ด้าน<br>
                &nbsp;&nbsp;&nbsp;= {in_s} × {in_s} = <b>{in_s**2} ตารางเซนติเมตร</b><br>
                3) <b>หาพื้นที่ส่วนที่เหลือ:</b><br>
                &nbsp;&nbsp;&nbsp;พื้นที่รูปใหญ่ - พื้นที่รูปที่เจาะทิ้ง<br>
                &nbsp;&nbsp;&nbsp;= {out_w * out_h} - {in_s**2} = <b>{(out_w * out_h) - (in_s**2)} ตารางเซนติเมตร</b><br>
                <b>ตอบ: พื้นที่ส่วนที่เหลือมีขนาด {(out_w * out_h) - (in_s**2)} ตารางเซนติเมตร</b></span>"""

            elif actual_sub_t == "ความเร็ววิ่งสวนทาง":
                d = random.choice([100, 200, 300])
                v1 = random.randint(10, 25)
                v2 = random.randint(10, 25)
                t = d / (v1 + v2)
                q = f"รถยนต์สองคันอยู่ห่างกันระยะทาง <b>{d} กิโลเมตร</b> และกำลังวิ่งเข้าหากัน (วิ่งสวนทางกัน) <br>ถ้ารถคันแรกวิ่งด้วยความเร็ว <b>{v1} กิโลเมตร/ชั่วโมง</b> และรถคันที่สองวิ่งด้วยความเร็ว <b>{v2} กิโลเมตร/ชั่วโมง</b> <br>จงหาว่าต้องใช้เวลาอีกกี่ชั่วโมง รถทั้งสองคันจึงจะวิ่งมาเจอกันพอดี?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                เมื่อวัตถุสองสิ่งเคลื่อนที่ <b>วิ่งเข้าหากัน</b> ระยะทางระหว่างกันจะถูกทำให้สั้นลงอย่างรวดเร็วด้วยความเร็วของทั้งสองฝ่ายรวมกันครับ<br>
                1) <b>หาความเร็วรวมที่ช่วยกันลดระยะทาง:</b><br>
                &nbsp;&nbsp;&nbsp;นำความเร็วของรถคันแรกบวกความเร็วรถคันที่สอง<br>
                &nbsp;&nbsp;&nbsp;= {v1} + {v2} = <b>{v1 + v2} กิโลเมตร/ชั่วโมง</b><br>
                2) <b>หาเวลาที่ใช้ในการพบกัน:</b><br>
                &nbsp;&nbsp;&nbsp;เวลา = ระยะทางทั้งหมด ÷ ความเร็วรวม<br>
                &nbsp;&nbsp;&nbsp;= {d} ÷ {v1 + v2} = <b>{t:.1f} ชั่วโมง</b><br>
                <b>ตอบ: รถทั้งสองจะพบกันในอีก {t:.1f} ชั่วโมง</b></span>"""

            elif actual_sub_t == "งานและเวลา (Work)":
                w1, w2 = 3, 6
                ans = (w1 * w2) / (w1 + w2)
                q = f"ในการทาสีรั้วบ้าน หากให้นาย ก. ทำงานคนเดียว เขาจะทำเสร็จภายในเวลา {w1} วัน แต่ถ้าให้นาย ข. ทำงานคนเดียว เขาจะทำเสร็จในเวลา {w2} วัน <br>จงหาว่าถ้านาย ก. และนาย ข. ช่วยกันทาสีรั้วบ้านนี้พร้อมกัน พวกเขาจะทำงานเสร็จภายในเวลากี่วัน?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                การทำงานร่วมกัน ไม่สามารถนำเวลามาบวกหรือลบกันตรงๆ ได้ แต่เราสามารถใช้สูตรลัดเรื่องงานและเวลาได้ดังนี้:<br>
                <b>สูตรทำงานพร้อมกัน = (เวลาของคนแรก × เวลาของคนที่สอง) ÷ (เวลาของคนแรก + เวลาของคนที่สอง)</b><br>
                1) แทนค่าลงในสูตร:<br>
                &nbsp;&nbsp;&nbsp;= ({w1} × {w2}) ÷ ({w1} + {w2})<br>
                2) คำนวณผลคูณและผลบวกในวงเล็บ:<br>
                &nbsp;&nbsp;&nbsp;= (18) ÷ (9)<br>
                3) นำมาหารกัน:<br>
                &nbsp;&nbsp;&nbsp;18 ÷ 9 = <b>{ans:.0f} วัน</b><br>
                <b>ตอบ: ถ้าช่วยกันทำจะเสร็จภายใน {ans:.0f} วัน</b></span>"""

            elif actual_sub_t == "จัดของใส่กล่อง (Modulo)":
                box_cap = random.randint(4, 9)
                num_boxes = random.randint(5, 12)
                rem = random.randint(1, box_cap - 1)
                total_items = (box_cap * num_boxes) + rem
                item = random.choice(ITEMS_LIST)
                name = random.choice(NAMES_LIST)
                q = f"<b>{name}</b>มี<b>{item}</b>จำนวนทั้งหมด <b>{total_items}</b> ชิ้น ต้องการจัดใส่กล่อง โดยให้แต่ละกล่องมี<b>{item}</b>กล่องละ <b>{box_cap}</b> ชิ้นเท่าๆ กัน <br>จงหาว่า<b>{name}</b>จะจัด<b>{item}</b>ใส่ได้เต็มกล่องกี่ใบ? และจะเหลือ<b>{item}</b>ที่ใส่ไม่เต็มกล่องอีกกี่ชิ้น?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                ข้อนี้คือการหารยาวเพื่อหา "จำนวนเต็ม" และ "เศษที่เหลือ" ครับ<br>
                1) นำจำนวนของทั้งหมด ({total_items}) ตั้ง แล้วหารด้วยจำนวนของที่จุได้ใน 1 กล่อง ({box_cap})<br>
                2) ท่องสูตรคูณแม่ {box_cap} เพื่อหาว่าคูณอะไรแล้วได้ใกล้เคียง {total_items} ที่สุด (แต่ห้ามเกิน)<br>
                &nbsp;&nbsp;&nbsp;จะพบว่า: <b>{box_cap} × {num_boxes} = {box_cap * num_boxes}</b><br>
                3) แสดงว่าเราสามารถจัดใส่กล่องได้เต็มจำนวน <b>{num_boxes} กล่อง</b><br>
                4) หาของเศษที่เหลือที่จัดใส่กล่องไม่ลงตัว โดยนำของทั้งหมดมาลบด้วยของที่จัดลงกล่องไปแล้ว:<br>
                &nbsp;&nbsp;&nbsp;{total_items} - {box_cap * num_boxes} = <b>{rem} ชิ้น</b><br>
                <b>ตอบ: จัดได้เต็มกล่อง {num_boxes} ใบ และเหลือเศษอีก {rem} ชิ้น</b></span>"""

            elif actual_sub_t == "นาฬิกาเดินเพี้ยน":
                fast_min = random.randint(2, 5)
                start_h = 8
                passed_hours = random.randint(3, 6)
                end_h = start_h + passed_hours
                total_fast = fast_min * passed_hours
                q = f"นาฬิกาเรือนหนึ่งทำงานผิดปกติ โดยจะเดินเร็วไป <b>{fast_min} นาที ในทุกๆ 1 ชั่วโมง</b> <br>ถ้านักเรียนตั้งเวลานาฬิกาเรือนนี้ให้ตรงเป๊ะในเวลา <b>{start_h}:00 น.</b> ตอนเช้า <br>เมื่อเวลาจริงผ่านไปจนถึง <b>{end_h}:00 น.</b> ของวันเดียวกัน นาฬิกาเรือนนี้จะแสดงเวลาใด?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                1) อันดับแรก เราต้องหาว่ามีเวลาผ่านไปทั้งหมดกี่ชั่วโมง นับตั้งแต่ตอนที่ตั้งเวลาตรงเป๊ะ:<br>
                &nbsp;&nbsp;&nbsp;จาก {start_h}:00 ถึง {end_h}:00 คือเวลาผ่านไป <b>{passed_hours} ชั่วโมง</b><br>
                2) โจทย์บอกว่า นาฬิกาจะเดินเร็วขึ้น {fast_min} นาที ในทุกๆ 1 ชั่วโมงที่ผ่านไป<br>
                &nbsp;&nbsp;&nbsp;เราจึงนำเวลาที่ผ่านไปทั้งหมด มาคูณกับ นาทีที่เดินเร็ว<br>
                &nbsp;&nbsp;&nbsp;จะได้เวลาที่นาฬิกาเดินเร็วเกินไปทั้งหมด = {fast_min} × {passed_hours} = <b>{total_fast} นาที</b><br>
                3) นำเวลาที่เร็วเกินไป ไปบวกเพิ่มเข้ากับเวลาจริง ({end_h}:00 น.)<br>
                &nbsp;&nbsp;&nbsp;นาฬิกาจะแสดงเวลา <b>{end_h}:{total_fast:02d} น.</b><br>
                <b>ตอบ: นาฬิกาจะแสดงเวลา {end_h}:{total_fast:02d} น.</b></span>"""

            elif actual_sub_t == "คะแนนยิงเป้า":
                s1, s2, s3 = random.choices([10, 5, 1], k=3)
                total_score = s1 + s2 + s3
                name = random.choice(NAMES_LIST)
                q = f"ในงานวัด มีเกมปาลูกดอกลงเป้า โดยเป้ามี 3 วงคะแนนคือ:<br>- วงตรงกลางได้ <b>10</b> คะแนน<br>- วงถัดมาได้ <b>5</b> คะแนน<br>- วงนอกสุดได้ <b>1</b> คะแนน<br><br>ถ้า <b>{name}</b> ปาลูกดอก 3 ครั้ง และลูกดอกเข้าเป้าทั้ง 3 ครั้ง โดยรวมคะแนนทั้งหมดได้ <b>{total_score}</b> คะแนน <br>จงหาว่า <b>{name}</b> ปาลูกดอกเข้าวงใดบ้าง? (เรียงลำดับจากคะแนนมากไปน้อย)"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                เราต้องหาวิธีนำตัวเลขจากกลุ่ม (10, 5, และ 1) จำนวน 3 ตัวมาบวกกัน ให้ได้ผลลัพธ์เท่ากับ <b>{total_score}</b> พอดี<br>
                <i>(จำไว้ว่า: ลูกดอกสามารถปาซ้ำเข้าวงเดิมได้ ดังนั้นตัวเลขจึงซ้ำกันได้)</i><br>
                1) ลองพิจารณาตัวเลขที่มากที่สุดก่อนคือ 10 ว่าใส่ได้กี่ครั้งโดยไม่เกิน {total_score}<br>
                2) กระจายตัวเลขออกมาจะได้ว่า: <b>{s1} + {s2} + {s3} = {total_score}</b> พอดีเป๊ะ!<br>
                3) นำคะแนนแต่ละวงที่ปาเข้า มาเรียงลำดับจากมากไปน้อย จะได้ <b>{sorted([s1, s2, s3], reverse=True)}</b><br>
                <b>ตอบ: {name} ปาเข้าเป้าคะแนน {sorted([s1, s2, s3], reverse=True)}</b></span>"""

            # =========================================================
            # โหมดหลักสูตรปกติ (เขียนอธิบายละเอียด Step-by-Step เช่นกัน)
            # =========================================================
            elif actual_sub_t == "การคูณ (แบบตั้งหลัก)":
                a = random.randint(10, 99) if grade in ["ป.1", "ป.2"] else (random.randint(100, 999) if grade == "ป.3" else random.randint(1000, 9999)) 
                b = random.randint(2, 9); res = a * b
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} × {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '×', is_key=False)
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) ตั้งหลักตัวเลขให้ตรงกัน<br>2) นำตัวคูณ ({b}) ไปคูณตัวตั้งด้านบนทีละหลัก โดยเริ่มจากหลักหน่วยทางขวาสุด<br>3) หากผลคูณมีค่าตั้งแต่ 10 ขึ้นไป ให้ใส่เลขตัวหลัง (หลักหน่วย) ไว้ด้านล่าง และนำเลขตัวหน้าไป 'ทด' ไว้บนหัวของหลักถัดไปทางซ้ายมือ<br>4) เมื่อคูณหลักถัดไปเสร็จ อย่าลืมบวกตัวทดที่อยู่ด้านบนด้วย</span><br>" + generate_vertical_table_html(a, b, '×', result=res, is_key=True)

            elif actual_sub_t == "การบวก (แบบตั้งหลัก)":
                a = random.randint(10, limit // 2); b = random.randint(10, limit // 2)
                res = a + b
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} + {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '+', is_key=False)
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) ตั้งหลักตัวเลขให้ตรงกัน (หลักหน่วยตรงหลักหน่วย, หลักสิบตรงหลักสิบ)<br>2) เริ่มบวกตัวเลขจากหลักหน่วย (ขวาสุด) ไปทางซ้ายทีละหลัก<br>3) หากผลบวกในหลักใดมีค่าตั้งแต่ 10 ขึ้นไป ให้ใส่เลขตัวหลังไว้ด้านล่าง และนำเลขตัวหน้าไป 'ทด' ขึ้นไปไว้บนหัวของหลักถัดไปทางซ้ายมือ<br>4) ในการบวกหลักถัดไป ให้นำตัวทดมาบวกเพิ่มด้วย</span><br>" + generate_vertical_table_html(a, b, '+', result=res, is_key=True)

            elif actual_sub_t == "การลบ (แบบตั้งหลัก)":
                a = random.randint(1000, limit - 1); b = random.randint(100, a - 1)
                res = a - b
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} - {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '-', is_key=False)
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) ตั้งหลักตัวเลขให้ตรงกัน (หลักหน่วยตรงหลักหน่วย, หลักสิบตรงหลักสิบ)<br>2) เริ่มลบตัวเลขจากหลักหน่วย (ขวาสุด) ไปทางซ้ายทีละหลัก<br>3) หากตัวเลขด้านบนน้อยกว่าตัวเลขด้านล่าง (ลบไม่พอ) ให้ทำการ 'ขอยืม' ตัวเลขจากหลักถัดไปทางซ้ายมา 1 (ซึ่งจะมีค่าเท่ากับ 10 ในหลักปัจจุบัน)<br>4) นำ 10 ที่ยืมมาบวกกับตัวเลขเดิม แล้วจึงทำการลบตามปกติ</span><br>" + generate_vertical_table_html(a, b, '-', result=res, is_key=True)

            elif "การหารพื้นฐาน" in actual_sub_t:
                a = random.randint(2, 9); b = random.randint(2, 12); dividend = a * b
                q = f"จงหาผลลัพธ์ของ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {dividend} ÷ {a} = {box_html}</span>"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) การหารคือการหาว่า 'ตัวหาร ({a}) ต้องคูณกับเลขอะไรจึงจะได้ผลลัพธ์เท่ากับตัวตั้ง ({dividend})'<br>2) ให้นักเรียนลองท่องสูตรคูณแม่ <b>{a}</b> ดูครับ:<br>&nbsp;&nbsp;&nbsp;{a} × 1 = {a}<br>&nbsp;&nbsp;&nbsp;...<br>&nbsp;&nbsp;&nbsp;<b>{a} × {b} = {dividend}</b> (เจอคำตอบแล้ว!)<br>ดังนั้น {dividend} ÷ {a} มีค่าเท่ากับ <b>{b}</b><br><b>ตอบ: {b}</b></span>"

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
                    4) ทางฝั่งซ้าย {a} หาร {a} มีค่าเท่ากับ 1 จึงเหลือแค่ x ตัวเดียว<br>
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

            # --- ถ้าสุ่มมาโดนหัวข้อที่ไม่ได้ตั้งเงื่อนไขพิเศษไว้ ให้ใช้ Fallback อธิบายละเอียด ---
            else:
                a, b = random.randint(10, 50), random.randint(10, 50)
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a} + {b} = {box_html}</span>"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>ให้นำตัวตั้ง <b>{a}</b> ไปบวกเพิ่มกับตัวบวก <b>{b}</b> โดยตั้งหลักให้ตรงกัน แล้วทำการบวกทีละหลักจากขวาไปซ้าย จะได้คำตอบเท่ากับ <b>{a + b}</b><br><b>ตอบ: {a + b}</b></span>"

            if q not in seen: 
                seen.add(q)
                questions.append({"question": q, "solution": sol})
                break
            attempts += 1
            
    return questions

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
worksheet_mode = st.sidebar.radio("🎯 เลือกหมวดหมู่โจทย์:", ["📚 หลักสูตรปกติ (ป.1 - ป.6)", "🏆 ข้อสอบแข่งขันระดับชาติ (TMC)"])
st.sidebar.markdown("---")

if worksheet_mode == "📚 หลักสูตรปกติ (ป.1 - ป.6)":
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
else: 
    selected_grade = st.sidebar.selectbox("🏆 เลือกระดับชั้นแข่งขัน:", ["ป.1-ป.2 (พื้นฐาน)", "ป.3-ป.4 (ประยุกต์)", "ป.5-ป.6 (วิเคราะห์)"]) 
    selected_main = "ข้อสอบแข่งขันระดับชาติ"
    sub_options = tmc_lower if "ป.1" in selected_grade else (tmc_mid if "ป.3" in selected_grade else tmc_upper)
    selected_sub = st.sidebar.selectbox("📝 เลือกแนวข้อสอบ (พร้อมภาพอธิบายเฉลย):", sub_options + ["🌟 สุ่มรวมทุกแนว"])

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
        grade_arg = "ป.1" if "ป.1" in selected_grade else ("ป.3" if "ป.3" in selected_grade else "ป.5")
        if worksheet_mode == "📚 หลักสูตรปกติ (ป.1 - ป.6)":
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

        filename_base = f"Competition_{selected_grade}_{selected_sub}" if worksheet_mode != "📚 หลักสูตรปกติ (ป.1 - ป.6)" else f"{selected_grade}_{selected_sub}"
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
