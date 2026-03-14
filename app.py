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
    <p>ระบบสร้างสื่อการสอนคณิตศาสตร์ (ป.1 - ป.6) พร้อมระบบโจทย์แข่งขัน TMC (20 หัวข้อ), คลังคำศัพท์หลากหลาย, และ Spacing ยืดหยุ่นได้</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 1. ฐานข้อมูลหลักสูตร (Master Database)
# ==========================================
comp_topics = [
    "ปริศนาตัวเลขซ่อนแอบ", "การนับหน้าหนังสือ", "การปักเสาและปลูกต้นไม้", 
    "สัตว์ปีนบ่อ", "ตรรกะตาชั่งสมดุล", "อายุข้ามเวลาขั้นสูง", 
    "การตัดเชือกพับทบ", "แถวคอยแบบซ้อนทับ", "ปัญหาผลรวม-ผลต่าง", 
    "ตรรกะการจับมือ (ทักทาย)", "โปรโมชั่นแลกของ", "หยิบของในที่มืด",
    "การคิดย้อนกลับ", "แผนภาพความชอบ", "คิววงกลมมรณะ", 
    "ลำดับแบบวนลูป", "เส้นทางที่เป็นไปได้", "นาฬิกาเดินเพี้ยน", 
    "จัดของใส่กล่อง", "คะแนนยิงเป้า"
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
        "🌟 โจทย์แข่งขัน (แนว TMC)": comp_topics
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
            a_chars, b_chars = list(str_a), list(str_b)
            a_digits = [int(c) if c.strip() else 0 for c in a_chars]; b_digits = [int(c) if c.strip() else 0 for c in b_chars]
            for i in range(num_len - 1, -1, -1):
                if a_digits[i] < b_digits[i]:
                    for j in range(i-1, -1, -1):
                        if a_digits[j] > 0 and str_a[j].strip() != "":
                            strike[j] = True; a_digits[j] -= 1; top_marks[j] = str(a_digits[j])
                            for k in range(j+1, i): strike[k] = True; a_digits[k] = 9; top_marks[k] = "9"
                            strike[i] = True; a_digits[i] += 10; top_marks[i] = str(a_digits[i]); break
        elif op == '×':
            b_val, carry = b, 0
            a_digits = [int(c) if c.strip() else 0 for c in str_a]
            for i in range(num_len - 1, -1, -1):
                if str_a[i].strip() == "": 
                    if carry > 0: top_marks[i] = str(carry); carry = 0
                    continue
                prod = a_digits[i] * b_val + carry; carry = prod // 10
                if carry > 0 and i > 0: top_marks[i-1] = str(carry)
    a_tds = ""
    for i in range(num_len):
        val = str_a[i].strip(); td_content = val
        if val:
            mark = top_marks[i]
            if strike[i] and is_key: td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span style="text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;">{val}</span></div>'
            elif mark and is_key: td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span>{val}</span></div>'
        a_tds += f'<td style="width: 35px; text-align: center; height: 50px; vertical-align: bottom;">{td_content}</td>'
    b_tds = "".join([f'<td style="width: 35px; text-align: center; border-bottom: 2px solid #000; height: 40px; vertical-align: bottom;">{str_b[i].strip()}</td>' for i in range(num_len)])
    if is_key and result is not None:
        str_r = str(result).rjust(num_len, " ")
        res_tds = "".join([f'<td style="width: 35px; text-align: center; color: red; font-weight: bold; height: 45px; vertical-align: bottom;">{str_r[i].strip()}</td>' for i in range(num_len)])
    else: res_tds = "".join([f'<td style="width: 35px; height: 45px;"></td>' for _ in range(num_len)])
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
        if g > 1: extra_steps = f"ทอนเป็นเศษส่วนอย่างต่ำ (ใช้แม่ {g} หารทั้งเศษและส่วน) จะได้ผลลัพธ์เป็นจำนวนเต็ม"
    elif sim_num > sim_den:
        w, r = sim_num // sim_den, sim_num % sim_den
        final_html = generate_mixed_number_html(w, r, sim_den)
        if g > 1: extra_steps = f"ทอนเป็นเศษส่วนอย่างต่ำ (ใช้แม่ {g} หาร) และทำให้อยู่ในรูปจำนวนคละ"
        else: extra_steps = f"แปลงเศษเกินให้อยู่ในรูปจำนวนคละ"
    else:
        final_html = f"""<div style="display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; margin: 0 5px; font-family: 'Sarabun', sans-serif;"><span style="font-size: 20px; font-weight: bold; border-bottom: 2px solid red; padding: 0 4px; line-height: 1.1; color: red;">{sim_num}</span><span style="font-size: 20px; font-weight: bold; padding: 0 4px; line-height: 1.1; color: red;">{sim_den}</span></div>"""
        if g > 1: extra_steps = f"ทอนเป็นเศษส่วนอย่างต่ำโดยใช้แม่ {g} หารทั้งเศษและส่วน"
    return extra_steps, final_html

def generate_short_division_html(a, b, mode="ห.ร.ม."):
    factors = []; ca, cb = a, b; steps_html = ""
    while True:
        found = False
        for i in range(2, min(ca, cb) + 1):
            if ca % i == 0 and cb % i == 0:
                steps_html += f"<tr><td style='text-align: right; padding-right: 10px; font-weight: bold; color: red;'>{i}</td><td style='border-left: 2px solid #000; border-bottom: 2px solid #000; padding: 5px 15px; text-align: center;'>{ca}</td><td style='border-bottom: 2px solid #000; padding: 5px 15px; text-align: center;'>{cb}</td></tr>"
                factors.append(i); ca //= i; cb //= i; found = True; break
        if not found: break
    if not factors: return f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> ไม่มีตัวประกอบร่วมที่หารลงตัวทั้งคู่</span><br><b>{mode} = 1</b>" if mode=="ห.ร.ม." else f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> ไม่มีตัวประกอบร่วม</span><br><b>ค.ร.น. = {a} × {b} = {a*b}</b>"
    steps_html += f"<tr><td></td><td style='padding: 5px 15px; text-align: center;'>{ca}</td><td style='padding: 5px 15px; text-align: center;'>{cb}</td></tr>"
    table = f"<table style='margin: 10px 0; font-size: 20px; border-collapse: collapse; color: #333;'>{steps_html}</table>"
    if mode == "ห.ร.ม.":
        ans = math.prod(factors); calc_str = " × ".join(map(str, factors))
        sol = f"<span style='color: #2c3e50;'><b>วิธีทำ (หารสั้น):</b></span>{table}<span style='color: #2c3e50;'><b>ห.ร.ม.</b> คือนำตัวหารด้านหน้ามาคูณกัน:</span><br>= {calc_str}<br>= <b>{ans}</b>"
    else:
        ans = math.prod(factors) * ca * cb; calc_str = " × ".join(map(str, factors + [ca, cb]))
        sol = f"<span style='color: #2c3e50;'><b>วิธีทำ (หารสั้น):</b></span>{table}<span style='color: #2c3e50;'><b>ค.ร.น.</b> คือนำตัวหารและผลลัพธ์บรรทัดสุดท้ายมาคูณกัน (รูปตัว L):</span><br>= {calc_str}<br>= <b>{ans}</b>"
    return sol

def generate_decimal_vertical_html(a, b, op, is_key=False):
    str_a, str_b = f"{a:.2f}", f"{b:.2f}"
    ans = a + b if op == '+' else round(a - b, 2); str_ans = f"{ans:.2f}"
    max_len = max(len(str_a), len(str_b), len(str_ans)) + 1 
    str_a = str_a.rjust(max_len, " "); str_b = str_b.rjust(max_len, " "); str_ans = str_ans.rjust(max_len, " ")
    strike = [False] * max_len; top_marks = [""] * max_len
    if is_key:
        if op == '+':
            carry = 0
            for i in range(max_len - 1, -1, -1):
                if str_a[i] == '.': continue
                da = int(str_a[i]) if str_a[i].strip() else 0; db = int(str_b[i]) if str_b[i].strip() else 0
                s = da + db + carry; carry = s // 10
                if carry > 0 and i > 0:
                    next_i = i - 1
                    if str_a[next_i] == '.': next_i -= 1
                    if next_i >= 0: top_marks[next_i] = str(carry)
        elif op == '-':
            a_chars, b_chars = list(str_a), list(str_b)
            a_digits = [int(c) if c.strip() and c != '.' else 0 for c in a_chars]; b_digits = [int(c) if c.strip() and c != '.' else 0 for c in b_chars]
            for i in range(max_len - 1, -1, -1):
                if str_a[i] == '.': continue
                if a_digits[i] < b_digits[i]:
                    for j in range(i-1, -1, -1):
                        if str_a[j] == '.': continue
                        if a_digits[j] > 0 and str_a[j].strip() != "":
                            strike[j] = True; a_digits[j] -= 1; top_marks[j] = str(a_digits[j])
                            for k in range(j+1, i):
                                if str_a[k] == '.': continue
                                strike[k] = True; a_digits[k] = 9; top_marks[k] = "9"
                            strike[i] = True; a_digits[i] += 10; top_marks[i] = str(a_digits[i]); break
    a_tds = ""
    for i in range(max_len):
        val = str_a[i].strip() if str_a[i].strip() else ""
        if str_a[i] == '.': val = "."
        td_content = val
        if val and val != '.':
            mark = top_marks[i]
            if strike[i] and is_key: td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span style="text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;">{val}</span></div>'
            elif mark and is_key: td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span>{val}</span></div>'
        a_tds += f"<td style='width: 35px; text-align: center; height: 50px; vertical-align: bottom;'>{td_content}</td>"
    b_tds = "".join([f"<td style='width: 35px; text-align: center; border-bottom: 2px solid #000; height: 40px; vertical-align: bottom;'>{c.strip() if c.strip() else ('.' if c=='.' else '')}</td>" for c in str_b])
    if is_key: ans_tds = "".join([f"<td style='width: 35px; text-align: center; color: red; font-weight: bold; height: 45px; vertical-align: bottom;'>{c.strip() if c.strip() else ('.' if c=='.' else '')}</td>" for c in str_ans])
    else: ans_tds = "".join([f"<td style='width: 35px; height: 45px;'></td>" for _ in str_ans])
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
    
    steps = []; current_val_str = ""; ans_str = ""; has_started = False
    for i, digit in enumerate(div_str):
        current_val_str += digit; current_val = int(current_val_str)
        q = current_val // divisor; mul_res = q * divisor; rem = current_val - mul_res
        if not has_started and q == 0 and i < len(div_str) - 1:
             current_val_str = str(rem) if rem != 0 else ""; continue
        has_started = True; ans_str += str(q)
        cur_chars, m_chars = list(str(current_val)), list(str(mul_res).zfill(len(list(str(current_val)))))
        c_dig, m_dig = [int(c) for c in cur_chars], [int(c) for c in m_chars]
        top_m, strik = [""] * len(c_dig), [False] * len(c_dig)
        for idx_b in range(len(c_dig) - 1, -1, -1):
            if c_dig[idx_b] < m_dig[idx_b]:
                for j in range(idx_b-1, -1, -1):
                    if c_dig[j] > 0:
                        strik[j] = True; c_dig[j] -= 1; top_m[j] = str(c_dig[j])
                        for k in range(j+1, idx_b): strik[k] = True; c_dig[k] = 9; top_m[k] = "9"
                        strik[idx_b] = True; c_dig[idx_b] += 10; top_m[idx_b] = str(c_dig[idx_b]); break
        steps.append({'mul_res': mul_res, 'rem': rem, 'col_index': i, 'top_m': top_m, 'strik': strik})
        current_val_str = str(rem) if rem != 0 else ""
    ans_padded = ans_str.rjust(div_len, " ")
    ans_tds_list = [f'<td style="width: 35px; text-align: center; color: red; font-weight: bold; font-size: 38px;">{c.strip()}</td>' for c in ans_padded]
    ans_tds_list.append('<td style="width: 35px;"></td>') 
    div_tds_list = []
    s0 = steps[0] if len(steps) > 0 else None; s0_start = s0['col_index'] + 1 - len(s0['top_m']) if s0 else 0
    for i, c in enumerate(div_str):
        left_border = "border-left: 3px solid #000;" if i == 0 else ""
        td_content = c
        if is_key and s0 and s0_start <= i <= s0['col_index']:
            t_idx = i - s0_start; mark, is_strik = s0['top_m'][t_idx], s0['strik'][t_idx]
            if is_strik: td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span style="text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;">{c}</span></div>'
            elif mark: td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span>{c}</span></div>'
        div_tds_list.append(f'<td style="width: 35px; height: 50px; vertical-align: bottom; text-align: center; border-top: 3px solid #000; {left_border} font-size: 38px;">{td_content}</td>')
    div_tds_list.append('<td style="width: 35px;"></td>') 
    html = f"{equation_html}<div style=\"display: block; text-align: center; margin-top: 10px;\"><div style=\"display: inline-block; font-family: 'Sarabun', sans-serif; line-height: 1.2; margin: 10px 20px;\"><table style=\"border-collapse: collapse;\"><tr><td style=\"border: none;\"></td>{''.join(ans_tds_list)}</tr><tr><td style=\"border: none; text-align: right; padding-right: 12px; vertical-align: bottom; font-size: 38px;\">{divisor}</td>{''.join(div_tds_list)}</tr>"
    for idx, step in enumerate(steps):
        mul_res_str = str(step['mul_res']); pad_len = step['col_index'] + 1 - len(mul_res_str)
        mul_tds = ""
        for i in range(div_len + 1):
            if i >= pad_len and i <= step['col_index']:
                digit_idx = i - pad_len; border_b = "border-bottom: 2px solid #000;" if i <= step['col_index'] else ""
                mul_tds += f'<td style="width: 35px; height: 50px; vertical-align: bottom; text-align: center; font-size: 38px; {border_b}">{mul_res_str[digit_idx]}</td>'
            elif i == step['col_index'] + 1: mul_tds += '<td style="width: 35px; text-align: center; font-size: 38px; color: #333; position: relative; top: -24px;">-</td>'
            else: mul_tds += '<td style="width: 35px;"></td>'
        html += f"<tr><td style='border: none;'></td>{mul_tds}</tr>"
        is_last_step = (idx == len(steps) - 1)
        next_step = steps[idx+1] if not is_last_step else None; ns_start = next_step['col_index'] + 1 - len(next_step['top_m']) if next_step else 0
        rem_str = str(step['rem']); next_digit = div_str[step['col_index'] + 1] if not is_last_step else ""
        display_str = rem_str if rem_str != "0" or is_last_step else ""
        if not is_last_step and display_str == "": pass
        else: display_str += next_digit
        if display_str == "": display_str = next_digit
        pad_len_rem = step['col_index'] + 1 - len(display_str) + (1 if not is_last_step else 0); rem_tds = ""
        for i in range(div_len + 1):
            if i >= pad_len_rem and i <= step['col_index'] + (1 if not is_last_step else 0):
                digit_idx = i - pad_len_rem; char_val = display_str[digit_idx]; td_content = char_val
                if is_key and next_step and ns_start <= i <= next_step['col_index']:
                    t_idx = i - ns_start; mark, is_strik = next_step['top_m'][t_idx], next_step['strik'][t_idx]
                    if is_strik: td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span style="text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;">{char_val}</span></div>'
                    elif mark: td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span>{char_val}</span></div>'
                border_b2 = "border-bottom: 6px double #000;" if is_last_step else ""
                rem_tds += f'<td style="width: 35px; height: 50px; vertical-align: bottom; text-align: center; font-size: 38px; {border_b2}">{td_content}</td>'
            else: rem_tds += '<td style="width: 35px;"></td>'
        html += f"<tr><td style='border: none;'></td>{rem_tds}</tr>"
    html += "</table></div></div>"
    return html

def generate_thai_number_text(num_str):
    thai_nums = ["ศูนย์", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
    positions = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]
    parts = str(num_str).replace(",", "").split(".")
    int_part = parts[0]; dec_part = parts[1] if len(parts) > 1 else ""
    def read_int(s):
        if s == "0" or s == "": return "ศูนย์"
        res, length = "", len(s)
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
    questions = []; seen = set()
    limit_map = {"ป.1": 100, "ป.2": 1000, "ป.3": 100000, "ป.4": 1000000, "ป.5": 9000000, "ป.6": 9000000}
    limit = limit_map.get(grade, 100)

    # ==============================
    # 📚 คลังคำศัพท์ (Word Pools) เพื่อความหลากหลาย
    # ==============================
    NAMES_LIST = ["อคิณ", "นาวิน", "ภูผา", "สายฟ้า", "เจ้านาย", "ข้าวหอม", "ใบบัว", "มะลิ", "น้ำใส", "ญาญ่า", "ปลื้ม", "พายุ", "ไออุ่น", "กะทิ", "เวลา", "ของขวัญ", "มังกร", "ฉลาม", "ปลาวาฬ", "มาคิน"]
    LOCATIONS_LIST = ["โรงเรียน", "สวนสัตว์", "สวนสนุก", "ห้างสรรพสินค้า", "ห้องสมุด", "สวนสาธารณะ", "ร้านของเล่น", "ร้านเบเกอรี่", "ค่ายลูกเสือ", "พิพิธภัณฑ์"]
    ITEMS_LIST = ["ลูกแก้ว", "สติกเกอร์", "การ์ดโปเกมอน", "โมเดลรถ", "ตุ๊กตาหมี", "สมุดระบายสี", "ดินสอสี", "ลูกโป่ง", "ยางลบ", "ตัวต่อเลโก้", "หนังสือการ์ตูน", "ลูกบอล"]
    SNACKS_LIST = ["ช็อกโกแลต", "คุกกี้", "โดนัท", "เยลลี่", "ขนมปัง", "ไอศกรีม", "น้ำผลไม้", "นมเย็น", "ลูกอม", "เค้ก"]
    ANIMALS_LIST = ["แมงมุม", "มดแดง", "กบ", "จิ้งจก", "ตั๊กแตน", "เต่า"]

    for _ in range(num_q):
        q, sol = "", ""; attempts = 0
        while attempts < 300:
            actual_sub_t = sub_t
            
            if sub_t == "แบบทดสอบรวมปลายภาค":
                all_mains = [m for m in curriculum_db[grade].keys() if m != "🌟 โหมดพิเศษ (สุ่มทุกเรื่อง)"]
                rand_m = random.choice(all_mains)
                actual_sub_t = random.choice(curriculum_db[grade][rand_m])
            elif sub_t == "🌟 สุ่มรวมทุกแนว":
                actual_sub_t = random.choice(comp_topics)

            prefix = get_prefix(grade)

            # ==============================
            # 🌟 โหมดข้อสอบแข่งขัน (TMC) - 20 หัวข้อสุดพรีเมียม
            # ==============================
            if actual_sub_t == "ปริศนาตัวเลขซ่อนแอบ":
                a = random.randint(1, 4)
                b = random.randint(a + 2, 9)
                diff = b - a
                k = diff * 9
                sum_val = a + b
                q = f"ให้ A และ B เป็นเลขโดดที่ต่างกัน (ตั้งแต่ 0 ถึง 9) โดยที่จำนวนสองหลัก <b>AB</b> เมื่อนำมาบวกกับ <b>{k}</b> จะได้ผลลัพธ์เป็นจำนวนสองหลัก <b>BA</b> (นั่นคือ AB + {k} = BA) และกำหนดให้ <b>A + B = {sum_val}</b> <br>จงหาว่าจำนวนสองหลัก <b>AB</b> คือจำนวนใด?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>จากสมการ BA - AB = {k} <br>เราสามารถหาผลต่างของเลขโดดได้จากสูตร: B - A = {k} ÷ 9 = <b>{diff}</b><br>และโจทย์กำหนดให้ A + B = <b>{sum_val}</b><br>หาเลข 2 ตัวที่บวกกันได้ {sum_val} และลบกันได้ {diff} <br>จะได้ B = ({sum_val} + {diff}) ÷ 2 = <b>{b}</b> <br>และ A = {sum_val} - {b} = <b>{a}</b><br>ดังนั้น จำนวนสองหลัก AB คือ </span><b>{a}{b}</b>"

            elif actual_sub_t == "การนับหน้าหนังสือ":
                pages = random.randint(40, 150)
                ans = 9 + 180 + ((pages - 99) * 3) if pages > 99 else 9 + ((pages - 9) * 2)
                item = random.choice(ITEMS_LIST)
                q = f"โรงพิมพ์กำลังจัดพิมพ์หนังสือแคตตาล็อกแนะนำ<b>{item}</b> ซึ่งมีความหนาทั้งหมด <b>{pages}</b> หน้า หากโรงพิมพ์ต้องการพิมพ์ตัวเลขเพื่อบอกเลขหน้าทั้งหมดตั้งแต่หน้า 1 ไปจนถึงหน้า {pages} โรงพิมพ์จะต้องใช้พิมพ์ตัวเลขโดดทั้งหมดกี่ตัว?"
                if pages > 99:
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> แบ่งการนับตัวเลขตามจำนวนหลัก ดังนี้<br>1) หน้า 1 ถึง 9 (เลข 1 หลัก) มี 9 หน้า ใช้ตัวเลขหน้าละ 1 ตัว = 9 × 1 = <b>9 ตัว</b><br>2) หน้า 10 ถึง 99 (เลข 2 หลัก) มี 90 หน้า ใช้ตัวเลขหน้าละ 2 ตัว = 90 × 2 = <b>180 ตัว</b><br>3) หน้า 100 ถึง {pages} (เลข 3 หลัก) มี {pages} - 99 = {pages - 99} หน้า ใช้ตัวเลขหน้าละ 3 ตัว = {pages - 99} × 3 = <b>{(pages - 99) * 3} ตัว</b><br>นำจำนวนตัวเลขทั้งหมดมารวมกัน: 9 + 180 + {(pages - 99) * 3} = </span><b>{ans} ตัว</b>"
                else:
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> แบ่งการนับตัวเลขตามจำนวนหลัก ดังนี้<br>1) หน้า 1 ถึง 9 (เลข 1 หลัก) มี 9 หน้า ใช้ตัวเลขหน้าละ 1 ตัว = 9 × 1 = <b>9 ตัว</b><br>2) หน้า 10 ถึง {pages} (เลข 2 หลัก) มี {pages} - 9 = {pages - 9} หน้า ใช้ตัวเลขหน้าละ 2 ตัว = {pages - 9} × 2 = <b>{(pages - 9) * 2} ตัว</b><br>นำจำนวนตัวเลขทั้งหมดมารวมกัน: 9 + {(pages - 9) * 2} = </span><b>{ans} ตัว</b>"

            elif actual_sub_t == "การปักเสาและปลูกต้นไม้":
                d = random.choice([2, 4, 5, 10, 15])
                trees = random.randint(12, 35)
                length = (trees - 1) * d
                loc = random.choice(LOCATIONS_LIST)
                q = f"เทศบาลต้องการปลูกต้นไม้ริมถนนทางเข้า<b>{loc}</b> โดยให้ต้นไม้แต่ละต้นอยู่ห่างกันต้นละ <b>{d}</b> เมตร และต้องปลูกที่จุดเริ่มต้นและจุดสิ้นสุดของถนนพอดี หากเมื่อปลูกเสร็จแล้วนับจำนวนต้นไม้ได้ทั้งหมด <b>{trees}</b> ต้น จงหาว่าถนนเส้นนี้มีความยาวกี่เมตร?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>เนื่องจากมีการปลูกต้นไม้ทั้งที่หัวและท้ายถนน <br>สูตรคือ: จำนวนช่วงห่าง = จำนวนต้นไม้ - 1<br>จะได้จำนวนช่วงความห่างทั้งหมด = {trees} - 1 = <b>{trees - 1} ช่วง</b><br>และแต่ละช่วงยาว {d} เมตร<br>ดังนั้น ความยาวถนนทั้งหมด = {trees - 1} × {d} = </span><b>{length} เมตร</b>"

            elif actual_sub_t == "สัตว์ปีนบ่อ":
                u = random.randint(3, 7)
                d = random.randint(1, u - 1)
                net = u - d
                h = random.randint(15, 30)
                days = math.ceil((h - u) / net) + 1
                animal = random.choice(ANIMALS_LIST)
                q = f"<b>{animal}</b>ตัวหนึ่งตกลงไปในบ่อดินที่ลึก <b>{h}</b> เมตร ในช่วงเวลากลางวันมีความพยายามปีนขึ้นมาได้ <b>{u}</b> เมตร แต่เมื่อถึงเวลากลางคืนต้องนอนหลับ ทำให้ลื่นไถลตกลงไป <b>{d}</b> เมตร <b>{animal}</b>ตัวนี้จะต้องใช้เวลาอย่างน้อยที่สุดกี่วันจึงจะปีนพ้นปากบ่อ?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>{animal}ปีนได้วันละ {u} เมตร และลื่นลง {d} เมตร สรุป 1 วัน (24 ชม.) ปีนได้สุทธิ {u} - {d} = <b>{net} เมตร</b><br><i>*จุดหลอก:</i> ในวันสุดท้าย เมื่อปีนพ้นปากบ่อแล้ว จะไม่ลื่นตกลงมาอีก!<br>หาระยะทางก่อนถึงวันสุดท้าย = ความลึกบ่อ {h} - ปีนวันสุดท้าย {u} = <b>{h - u} เมตร</b><br>เวลาที่ใช้ปีนช่วงแรก = {h - u} ÷ {net} = {math.ceil((h - u) / net)} วัน<br>บวกกับวันสุดท้ายที่ปีนพ้นบ่ออีก 1 วัน = {math.ceil((h - u) / net)} + 1 = </span><b>{days} วัน</b>"

            elif actual_sub_t == "ตรรกะตาชั่งสมดุล":
                items = [("รถคันใหญ่", "รถคันเล็ก", "ตุ๊กตา"), ("หนังสือหนา", "สมุดบาง", "ยางลบ"), ("แตงโม", "สับปะรด", "มะละกอ")]
                i1, i2, i3 = random.choice(items)
                mul1 = random.randint(2, 5)
                mul2 = random.randint(2, 5)
                q = f"จากการเล่นตาชั่งสมดุลของเด็กๆ พบข้อมูลความสมดุลดังนี้:<br>- <b>{i1} 1 ชิ้น</b> มีน้ำหนักเท่ากับ <b>{i2} {mul1} ชิ้น</b><br>- <b>{i2} 1 ชิ้น</b> มีน้ำหนักเท่ากับ <b>{i3} {mul2} ชิ้น</b><br><br>อยากทราบว่า <b>{i1} จำนวน 2 ชิ้น</b> จะมีน้ำหนักเท่ากับ <b>{i3}</b> รวมกันทั้งหมดกี่ชิ้น?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>เราต้องแปลงน้ำหนักให้เป็นหน่วยของ {i3} ทั้งหมด:<br>จากบรรทัดที่สอง: {i2} 1 ชิ้น = {i3} {mul2} ชิ้น<br>นำไปแทนค่าในบรรทัดแรก: {i1} 1 ชิ้น = {i2} {mul1} ชิ้น = {mul1} × {mul2} = <b>{i3} {mul1 * mul2} ชิ้น</b><br>โจทย์ถามหา {i1} <b>2 ชิ้น</b> <br>ดังนั้น ต้องนำ {mul1 * mul2} × 2 = </span><b>{mul1 * mul2 * 2} ชิ้น</b>"

            elif actual_sub_t == "อายุข้ามเวลาขั้นสูง":
                n1, n2, n3 = random.sample(NAMES_LIST, 3)
                age_a = random.randint(6, 10)  
                diff_b = random.randint(2, 5)   
                age_b = age_a + diff_b
                diff_c = random.randint(1, age_b - 2) 
                age_c = age_b - diff_c
                past_years = random.randint(2, 5) 
                current_sum = age_a + age_b + age_c
                past_sum = current_sum - (3 * past_years)
                
                q = f"ปัจจุบัน ครอบครัวหนึ่งมีพี่น้อง 3 คน คือ {n1}, {n2} และ {n3} ซึ่งเมื่อนำอายุของทั้งสามคนมารวมกันจะได้ <b>{current_sum}</b> ปีพอดี <br>จงหาว่าเมื่อ <b>{past_years}</b> ปีที่แล้ว เด็กทั้งสามคนนี้มีอายุรวมกันเป็นกี่ปี? (กำหนดให้เมื่อ {past_years} ปีที่แล้ว น้องคนเล็กสุดเกิดและมีอายุแล้ว)"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>1) ปัจจุบัน ทั้ง 3 คนมีอายุรวมกัน = {current_sum} ปี<br>2) <i>*จุดหลอก:</i> เมื่อย้อนเวลากลับไป {past_years} ปีที่แล้ว เด็ก<b>ทุกคน</b>จะต้องมีอายุน้อยลงคนละ {past_years} ปี<br>3) เนื่องจากมีเด็ก 3 คน อายุที่ต้องหักออกทั้งหมด = 3 × {past_years} = <b>{3 * past_years} ปี</b><br>ดังนั้น อายุรวมกันเมื่ออดีต = {current_sum} - {3 * past_years} = </span><b>{past_sum} ปี</b>"

            elif actual_sub_t == "การตัดเชือกพับทบ":
                folds = random.randint(2, 4)
                cuts = random.randint(2, 5)
                pieces = (2**folds) * cuts + 1
                name = random.choice(NAMES_LIST)
                q = f"<b>{name}</b>นำริบบิ้นเส้นยาวเส้นหนึ่งมาพับทบครึ่งกันจำนวน <b>{folds}</b> ครั้ง (พับครึ่งแล้วพับครึ่งซ้ำไปเรื่อยๆ) จากนั้นนำกรรไกรมาตัดแบ่งริบบิ้นที่พับไว้ให้ขาดออกจากกันจำนวน <b>{cuts}</b> รอยตัด <br>เมื่อคลี่ริบบิ้นทั้งหมดออกมา <b>{name}</b>จะได้ริบบิ้นทั้งหมดกี่เส้น?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>1) การพับเชือกทบครึ่งแต่ละครั้ง จะทำให้จำนวนทบเชือกเพิ่มขึ้นเป็น 2 เท่า<br>พับ {folds} ครั้ง จะเกิดความหนาของเชือก = 2 ยกกำลัง {folds} = <b>{2**folds} ชั้น</b><br>2) เมื่อเราตัดเชือกที่หนา {2**folds} ชั้น ไป 1 รอยตัด จะเกิดรอยขาด {2**folds} รอย (เทียบเท่าการเพิ่มเส้นเชือก {2**folds} เส้น)<br>3) ตัด {cuts} รอยตัด จะมีเชือกเพิ่มขึ้น = {2**folds} × {cuts} = <b>{(2**folds) * cuts} เส้น</b><br>รวมกับเชือกเส้นตั้งต้นเดิมอีก 1 เส้น จะได้เชือกทั้งหมด = {(2**folds) * cuts} + 1 = </span><b>{pieces} เส้น</b>"

            elif actual_sub_t == "แถวคอยแบบซ้อนทับ":
                front_pos = random.randint(10, 20)
                back_pos = random.randint(10, 20)
                total_people = front_pos + back_pos + random.randint(5, 12)
                between = total_people - (front_pos + back_pos)
                n1, n2 = random.sample(NAMES_LIST, 2)
                loc = random.choice(LOCATIONS_LIST)
                q = f"นักเรียนกลุ่มหนึ่งยืนเข้าแถวตอนเรียงหนึ่งเพื่อรอเข้า<b>{loc}</b> โดยมีนักเรียนทั้งหมดในแถว <b>{total_people}</b> คน<br>ถ้า <b>{n1}</b> ยืนอยู่ในลำดับที่ <b>{front_pos}</b> นับจากหัวแถว <br>และ <b>{n2}</b> ยืนอยู่ในลำดับที่ <b>{back_pos}</b> นับจากท้ายแถว <br>อยากทราบว่ามีนักเรียนคนอื่นๆ ที่ยืนอยู่ระหว่าง <b>{n1}</b> กับ <b>{n2}</b> เป็นจำนวนกี่คน? (กำหนดให้ <b>{n1}</b> ยืนอยู่หน้า <b>{n2}</b>)"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>เราสามารถหาจำนวนคนที่อยู่ตรงกลางได้โดยการหักคนที่อยู่ด้านหน้าและด้านหลังออกไป<br>1) {n1}อยู่ลำดับที่ {front_pos} จากหัวแถว แสดงว่าตั้งแต่หัวแถวจนถึงตัว{n1} มีคนรวม <b>{front_pos} คน</b><br>2) {n2}อยู่ลำดับที่ {back_pos} จากท้ายแถว แสดงว่าตั้งแต่ท้ายแถวจนถึงตัว{n2} มีคนรวม <b>{back_pos} คน</b><br>3) นำคนทั้งแถว ลบด้วยกลุ่มด้านหน้าและกลุ่มด้านหลัง<br>จำนวนคนตรงกลาง = {total_people} - ({front_pos} + {back_pos})<br>= {total_people} - {front_pos + back_pos} = </span><b>{between} คน</b>"

            elif actual_sub_t == "ปัญหาผลรวม-ผลต่าง":
                diff = random.randint(5, 20)
                small = random.randint(10, 30)
                large = small + diff
                total = large + small
                n1, n2 = random.sample(NAMES_LIST, 2)
                item = random.choice(ITEMS_LIST)
                q = f"<b>{n1}</b> และ <b>{n2}</b> สะสม<b>{item}</b>รวมกันได้ <b>{total}</b> ชิ้น หากทราบว่า <b>{n1}</b> มีสะสมมากกว่า <b>{n2}</b> อยู่ <b>{diff}</b> ชิ้น จงหาว่า <b>{n1}</b> มี<b>{item}</b>อยู่กี่ชิ้น?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>1) หักส่วนที่{n1}มีมากกว่า{n2}ออกไปก่อน: {total} - {diff} = <b>{total - diff} ชิ้น</b><br>2) แบ่งจำนวนที่เหลือให้ 2 คนเท่าๆ กัน (จะได้เท่ากับจำนวนของ{n2}): {total - diff} ÷ 2 = <b>{small} ชิ้น</b><br>3) หาจำนวนของ{n1} โดยนำของ{n2}ไปบวกส่วนที่มากกว่า: {small} + {diff} = <b>{large} ชิ้น</b><br>ดังนั้น {n1} มีสะสม </span><b>{large} ชิ้น</b>"

            elif actual_sub_t == "ตรรกะการจับมือ (ทักทาย)":
                n = random.randint(5, 12)
                ans = n * (n - 1) // 2
                loc = random.choice(LOCATIONS_LIST)
                q = f"ในการจัดกิจกรรมที่<b>{loc}</b> มีเพื่อนสนิทมาร่วมกลุ่มทั้งหมด <b>{n}</b> คน หากเด็กทุกคนในกลุ่มต้องเดินไปจับมือทักทายทำความรู้จักกันและกันให้ครบทุกคน คนละ 1 ครั้ง จะมีการจับมือเกิดขึ้นทั้งหมดกี่ครั้ง?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>1) คนที่ 1 ต้องเดินไปจับมือกับคนอื่นอีก {n-1} คน (เกิดการจับมือ {n-1} ครั้ง)<br>2) คนที่ 2 ต้องเดินไปจับมือกับคนอื่น (ไม่นับคนที่ 1 เพราะจับไปแล้ว) อีก {n-2} คน<br>3) ทำแบบนี้ลดหลั่นไปเรื่อยๆ จนถึงคนสุดท้าย จะได้ว่าจำนวนการจับมือทั้งหมดคือ:<br>{n-1} + {n-2} + ... + 1 = <b>{ans} ครั้ง</b><br><br><i>*(หรือใช้สูตรลัด: นำจำนวนคน × จำนวนคนที่ต้องไปจับมือด้วย แล้วหาร 2 เนื่องจากจับสลับกันไปมานับเป็น 1 ครั้ง = ({n} × {n-1}) ÷ 2 = {ans} ครั้ง)</i></span>"

            elif actual_sub_t == "โปรโมชั่นแลกของ":
                exchange_rate = random.choice([3, 4, 5])
                start_bottles = exchange_rate * random.randint(3, 6)
                snack = random.choice(SNACKS_LIST)
                
                total_drank = start_bottles
                empties = start_bottles
                step_count = 1
                sol_steps = f"1) ซื้อมากินครั้งแรก <b>{start_bottles}</b> ชิ้น (เก็บซอง/ขวดเปล่าไว้ {start_bottles} ใบ)<br>"
                while empties >= exchange_rate:
                    step_count += 1
                    new_b = empties // exchange_rate
                    left_b = empties % exchange_rate
                    total_drank += new_b
                    sol_steps += f"{step_count}) นำของเปล่า {new_b * exchange_rate} ใบ ไปแลกได้ใหม่ <b>{new_b}</b> ชิ้น (เหลือเศษที่ยังไม่ได้แลก {left_b} ใบ)<br>"
                    empties = new_b + left_b
                    if empties >= exchange_rate:
                         sol_steps += f"&nbsp;&nbsp;&nbsp;<i>--> ตอนนี้มีของเปล่ารวม {new_b} + {left_b} = {empties} ใบ นำไปแลกต่อได้อีก!</i><br>"
                         
                q = f"โปรโมชั่นพิเศษร้านค้า: นำซองหรือขวดเปล่าของ<b>{snack}</b> จำนวน <b>{exchange_rate}</b> ใบ มาแลก<b>{snack}</b>ชิ้นใหม่ได้ฟรี 1 ชิ้น <br>หากนักเรียนมีเงินซื้อ<b>{snack}</b>มากินในตอนแรกทั้งหมด <b>{start_bottles}</b> ชิ้น นักเรียนจะสามารถกิน<b>{snack}</b>ได้ทั้งหมดกี่ชิ้น (รวมกับของที่นำไปแลกฟรีมาใหม่ด้วยจนกว่าจะแลกไม่ได้อีก)?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>{sol_steps}<br>รวมได้กินทั้งหมด {total_drank} ชิ้น (เหลือของเปล่าแลกไม่ได้อีก {empties} ใบ)<br>ตอบ: </span><b>{total_drank} ชิ้น</b>"

            elif actual_sub_t == "หยิบของในที่มืด":
                c1 = random.randint(5, 12)
                c2 = random.randint(5, 12)
                c3 = random.randint(3, 8)
                item = random.choice(ITEMS_LIST)
                q = f"ในกล่องทึบใบหนึ่งมี<b>{item}</b>สีแดง <b>{c1}</b> ชิ้น, สีน้ำเงิน <b>{c2}</b> ชิ้น และสีเขียว <b>{c3}</b> ชิ้น ปะปนกันอยู่ <br>หากหลับตาหยิบ<b>{item}</b>ทีละชิ้น จะต้องหยิบออกมา<b>อย่างน้อยที่สุดกี่ชิ้น</b> จึงจะมั่นใจได้ 100% ว่าจะได้<b>{item}</b><b>สีเขียว</b>อย่างน้อย 1 ชิ้นแน่นอน?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ (ใช้หลักการดวงซวยที่สุด หรือ Worst-case scenario):</b><br>เพื่อให้มั่นใจ 100% เราต้องคิดในกรณีที่โชคร้ายที่สุด คือเราหยิบได้สีอื่นจนหมดกล่องแล้วค่อยได้สีที่ต้องการ<br>1) สมมติหยิบได้สีแดงหมดเลย = {c1} ชิ้น<br>2) สมมติหยิบได้สีน้ำเงินหมดเลย = {c2} ชิ้น<br>ตอนนี้หยิบไปแล้ว {c1} + {c2} = <b>{c1+c2} ชิ้น</b> (แต่ยังไม่ได้สีเขียวเลยซักชิ้น)<br>3) การหยิบชิ้นต่อไป (ชิ้นที่ {c1+c2+1}) ในกล่องจะเหลือแต่สีเขียวแล้ว จึงหยิบได้สีเขียว 100%<br>ดังนั้น ต้องหยิบอย่างน้อย {c1+c2} + 1 = </span><b>{c1+c2+1} ชิ้น</b>"

            elif actual_sub_t == "การคิดย้อนกลับ":
                start_money = random.randint(100, 300)
                spent = random.randint(20, 80)
                received = random.randint(50, 150)
                final_money = start_money - spent + received
                name = random.choice(NAMES_LIST)
                loc = random.choice(LOCATIONS_LIST)
                item = random.choice(ITEMS_LIST)
                q = f"<b>{name}</b>มีเงินเก็บอยู่ในกระปุกออมสินจำนวนหนึ่ง เมื่อไปถึง<b>{loc}</b> ได้นำเงินไปซื้อ<b>{item}</b>ราคา <b>{spent}</b> บาท จากนั้นคุณแม่ให้เงินค่าขนมเพิ่มมาอีก <b>{received}</b> บาท เมื่อกลับถึงบ้าน<b>{name}</b>นับเงินดูพบว่าตอนนี้มีเงินอยู่ <b>{final_money}</b> บาท <br>จงหาว่าตอนแรกก่อนออกจากบ้าน <b>{name}</b>มีเงินอยู่ในกระปุกออมสินกี่บาท?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ (การคิดย้อนกลับ):</b><br>ให้เริ่มคิดจากเหตุการณ์สุดท้าย ย้อนกลับไปหาเหตุการณ์แรก โดยสลับเครื่องหมาย (บวกเป็นลบ, ลบเป็นบวก)<br>1) ปัจจุบันมีเงิน {final_money} บาท<br>2) แม่ให้เพิ่มมา {received} บาท (ย้อนกลับคือนำไปลบออก): {final_money} - {received} = <b>{final_money - received} บาท</b><br>3) ซื้อของไป {spent} บาท (ย้อนกลับคือนำไปบวกคืน): {final_money - received} + {spent} = <b>{start_money} บาท</b><br>ดังนั้น ตอนแรกมีเงินอยู่ </span><b>{start_money} บาท</b>"

            elif actual_sub_t == "แผนภาพความชอบ":
                total = random.randint(30, 50)
                both = random.randint(5, 12)
                only_a = random.randint(8, 15)
                only_b = random.randint(8, 15)
                like_a = only_a + both
                like_b = only_b + both
                neither = total - (only_a + only_b + both)
                n1, n2 = random.sample(SNACKS_LIST, 2)
                q = f"จากการสอบถามนักเรียนในห้องจำนวน <b>{total}</b> คน เกี่ยวกับขนมที่ชอบ พบว่า:<br>- มีนักเรียนชอบกิน<b>{n1}</b> จำนวน <b>{like_a}</b> คน<br>- มีนักเรียนชอบกิน<b>{n2}</b> จำนวน <b>{like_b}</b> คน<br>- มีนักเรียนที่ชอบกินทั้ง<b>{n1}</b>และ<b>{n2}</b> จำนวน <b>{both}</b> คน<br><br>อยากทราบว่ามีนักเรียนกี่คนในห้องนี้ ที่<b>ไม่ชอบ</b>กินขนมทั้งสองชนิดนี้เลย?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>ใช้หลักการแผนภาพซ้อนทับกัน<br>1) หาคนที่ชอบกินขนมอย่างน้อย 1 ชนิด: (ชอบอย่างแรก + ชอบอย่างหลัง) - ชอบทั้งคู่<br>คนชอบขนม = {like_a} + {like_b} - {both} = <b>{like_a + like_b - both} คน</b><br>2) หาคนที่ไม่ชอบเลย: นำคนทั้งหมดในห้อง ลบด้วยคนที่ชอบขนม<br>คนที่ไม่ชอบเลย = {total} - {like_a + like_b - both} = </span><b>{neither} คน</b>"

            elif actual_sub_t == "คิววงกลมมรณะ":
                n_half = random.randint(4, 12)
                total = n_half * 2
                pos1 = random.randint(1, n_half)
                pos2 = pos1 + n_half
                n1, n2 = random.sample(NAMES_LIST, 2)
                q = f"เด็กกลุ่มหนึ่งยืนล้อมกันเป็นวงกลมโดยเว้นระยะห่างเท่าๆ กัน และมีการนับหมายเลขเรียงตามลำดับ 1, 2, 3... ไปเรื่อยๆ จนครบทุกคน <br>ถ้า <b>{n1}</b> ยืนอยู่ที่ตำแหน่งหมายเลข <b>{pos1}</b> และมองไปฝั่งตรงข้ามพอดีเป๊ะ พบว่า <b>{n2}</b> ยืนอยู่ที่ตำแหน่งหมายเลข <b>{pos2}</b> <br>จงหาว่าเด็กกลุ่มนี้มีทั้งหมดกี่คน?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>การยืนเป็นวงกลมแล้วอยู่ตรงข้ามกัน แสดงว่าระยะห่างระหว่างสองคนนี้ คือ 'ครึ่งวงกลม' พอดี<br>1) หาความต่างของหมายเลข: {pos2} - {pos1} = <b>{n_half}</b> (นี่คือจำนวนคนครึ่งวงกลม)<br>2) หาจำนวนคนทั้งหมด (เต็มวงกลม): นำครึ่งวงกลมมาคูณ 2<br>{n_half} × 2 = </span><b>{total} คน</b>"

            elif actual_sub_t == "ลำดับแบบวนลูป":
                word = random.choice(["MATHEMATICS", "THAILAND", "ELEPHANT", "SUPERMAN"])
                length = len(word)
                target = random.randint(30, 80)
                rem = target % length
                ans_char = word[rem - 1] if rem != 0 else word[-1]
                q = f"หากเราเขียนตัวอักษรภาษาอังกฤษคำว่า <b>{word}</b> เรียงต่อกันไปเรื่อยๆ ดังนี้:<br><b>{word}{word}{word[:3]}...</b><br><br>อยากทราบว่า ตัวอักษรในตำแหน่งที่ <b>{target}</b> คือตัวอักษรใด?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>1) นับจำนวนตัวอักษรใน 1 ชุด: คำว่า {word} มีทั้งหมด <b>{length} ตัวอักษร</b><br>2) หาว่าตำแหน่งที่ {target} อยู่ในชุดที่เท่าไหร่และเหลือเศษกี่ตัว โดยนำไปหารด้วย {length}<br>{target} ÷ {length} = {target // length} ชุด เศษ <b>{rem}</b><br>3) เศษ {rem} หมายถึง ให้ไปดูตัวอักษรตัวที่ {rem if rem != 0 else length} ของคำ<br><i>(ถ้าเศษ 0 จะหมายถึงตัวสุดท้ายของคำ)</i><br>ดังนั้น ตัวอักษรในตำแหน่งที่ {target} คือ </span><b>{ans_char}</b>"

            elif actual_sub_t == "เส้นทางที่เป็นไปได้":
                p1 = random.randint(2, 4)
                p2 = random.randint(2, 4)
                p3 = random.randint(1, 3)
                ans = (p1 * p2) + p3
                q = f"การเดินทางจากเมือง A ไปเมือง B มีถนนเชื่อมต่อกัน <b>{p1}</b> สาย และจากเมือง B ไปเมือง C มีถนนเชื่อมต่อกัน <b>{p2}</b> สาย <br>นอกจากนี้ ยังมีถนนเส้นทางลัดที่เดินทางจากเมือง A ตรงไปยังเมือง C โดยไม่ผ่านเมือง B อีก <b>{p3}</b> สาย<br>ถามว่า มีเส้นทางทั้งหมดกี่แบบในการเดินทางจากเมือง A ไปยังเมือง C ?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>แบ่งการเดินทางเป็น 2 กรณี:<br>กรณีที่ 1: เดินทางผ่านเมือง B<br>ใช้หลักการคูณ: เส้นทาง A->B ({p1} สาย) × เส้นทาง B->C ({p2} สาย) = <b>{p1 * p2} เส้นทาง</b><br>กรณีที่ 2: ใช้ทางลัดไม่ผ่าน B<br>โจทย์กำหนดให้มีทางลัดตรง = <b>{p3} เส้นทาง</b><br>นำทั้งสองกรณีมารวมกัน = {p1 * p2} + {p3} = </span><b>{ans} เส้นทาง</b>"

            elif actual_sub_t == "นาฬิกาเดินเพี้ยน":
                fast_min = random.randint(2, 5)
                start_h = 8
                passed_hours = random.randint(3, 6)
                end_h = start_h + passed_hours
                total_fast = fast_min * passed_hours
                q = f"นาฬิกาเรือนหนึ่งทำงานผิดปกติ โดยจะเดินเร็วไป <b>{fast_min} นาที ในทุกๆ 1 ชั่วโมง</b> <br>ถ้านักเรียนตั้งเวลานาฬิกาเรือนนี้ให้ตรงเป๊ะในเวลา <b>{start_h}:00 น.</b> ตอนเช้า <br>เมื่อเวลาจริงผ่านไปจนถึง <b>{end_h}:00 น.</b> ของวันเดียวกัน นาฬิกาเรือนนี้จะบอกเวลาใด?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>1) หาเวลาที่ผ่านไปทั้งหมด: จาก {start_h}:00 ถึง {end_h}:00 คือ <b>{passed_hours} ชั่วโมง</b><br>2) นาฬิกาเดินเร็ว {fast_min} นาที/ชั่วโมง <br>ดังนั้น จะเดินเร็วไปทั้งหมด = {fast_min} × {passed_hours} = <b>{total_fast} นาที</b><br>3) นำเวลาที่เร็วเกินไป ไปบวกเพิ่มกับเวลาจริง {end_h}:00 น.<br>ดังนั้น นาฬิกาจะบอกเวลา </span><b>{end_h}:{total_fast:02d} น.</b>"

            elif actual_sub_t == "จัดของใส่กล่อง":
                box_cap = random.randint(4, 9)
                num_boxes = random.randint(5, 12)
                rem = random.randint(1, box_cap - 1)
                total_items = (box_cap * num_boxes) + rem
                item = random.choice(ITEMS_LIST)
                name = random.choice(NAMES_LIST)
                q = f"<b>{name}</b>มี<b>{item}</b>จำนวนทั้งหมด <b>{total_items}</b> ชิ้น ต้องการจัดใส่กล่อง กล่องละ <b>{box_cap}</b> ชิ้นเท่าๆ กัน <br>จงหาว่า<b>{name}</b>จะจัด<b>{item}</b>ได้เต็มกล่องกี่ใบ และเหลือ<b>{item}</b>ที่ใส่ไม่เต็มกล่องอีกกี่ชิ้น?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>ใช้การตั้งหารยาวเพื่อหาจำนวนกล่องและเศษที่เหลือ<br>นำ {total_items} ÷ {box_cap} <br>ท่องสูตรคูณแม่ {box_cap} : {box_cap} × {num_boxes} = {box_cap * num_boxes}<br>จะได้ผลลัพธ์คือ {num_boxes} และเหลือเศษ {total_items} - {box_cap * num_boxes} = <b>{rem}</b><br>ดังนั้น จัดได้เต็มกล่อง <b>{num_boxes} ใบ</b> และเหลือเศษ </span><b>{rem} ชิ้น</b>"

            elif actual_sub_t == "คะแนนยิงเป้า":
                score_center = 10
                score_mid = 5
                score_out = 1
                s1, s2, s3 = random.choices([score_center, score_mid, score_out], k=3)
                total_score = s1 + s2 + s3
                name = random.choice(NAMES_LIST)
                q = f"ในงานวัด มีเกมปาลูกดอกลงเป้า โดยเป้ามี 3 วง:<br>- วงตรงกลางได้ <b>10</b> คะแนน<br>- วงถัดมาได้ <b>5</b> คะแนน<br>- วงนอกสุดได้ <b>1</b> คะแนน<br><br>ถ้า <b>{name}</b> ปาลูกดอก 3 ครั้ง และเข้าเป้าทั้ง 3 ครั้ง ได้คะแนนรวม <b>{total_score}</b> คะแนน <br>จงหาว่า <b>{name}</b> ปาลูกดอกเข้าวงใดบ้าง? (เรียงลำดับจากวงที่คะแนนมากไปน้อย)"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>เราต้องหาผลรวมของตัวเลข 3 ตัว ที่มาจากกลุ่ม (10, 5, 1) ที่บวกกันแล้วได้ {total_score}<br>แจกแจงตัวเลข: <b>{s1} + {s2} + {s3} = {total_score}</b><br><i>(ลูกดอกสามารถปาซ้ำวงเดิมได้)</i><br>ดังนั้น {name} ปาเข้าวงที่มีคะแนน: </span><b>{sorted([s1, s2, s3], reverse=True)}</b>"

            # ==============================
            if q not in seen:
                seen.add(q); questions.append({"question": q, "solution": sol}); break
            attempts += 1
    return questions

# ฟังก์ชันจัดการ PDF/E-Book
def extract_body(html_str):
    try: return html_str.split('<body>')[1].split('</body>')[0]
    except IndexError: return html_str

def create_page(grade, sub_t, questions, is_key=False, q_margin="20px", ws_height="180px", brand_name=""):
    title = "เฉลยแบบฝึกหัด" if is_key else "แบบฝึกหัดคณิตศาสตร์"
    student_info = ""
    if not is_key:
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
        """
    html = f"""<!DOCTYPE html><html lang="th"><head><meta charset="utf-8">
    <style>
        @page {{ size: A4; margin: 15mm; }}
        body {{ font-family: 'Sarabun', sans-serif; padding: 20px; line-height: 1.6; color: #333; }}
        .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 10px; padding-bottom: 10px; }}
        .q-box {{ margin-bottom: {q_margin}; padding: 5px 15px; page-break-inside: avoid; border-bottom: 1px dashed #eee; font-size: 20px; }}
        .workspace {{ height: {ws_height}; border: 2px dashed #bdc3c7; border-radius: 8px; margin: 10px 0; padding: 10px; color: #95a5a6; font-size: 16px; display: flex; align-items: flex-start; }}
        .ans-line {{ margin-top: 5px; border-bottom: 1px dotted #999; width: 80%; height: 30px; font-weight: bold; font-size: 20px; display: flex; align-items: flex-end; padding-bottom: 5px; }}
        .sol-text {{ color: #333; font-size: 20px; display: inline-block; margin-top: 5px; line-height: 1.5; }}
        .page-footer {{ text-align: right; font-size: 14px; color: #95a5a6; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }}
    </style></head><body>
    <div class="header"><h2>{title} - {grade}</h2><p><b>เรื่อง:</b> {sub_t}</p></div>
    {student_info}"""
    
    for i, item in enumerate(questions, 1):
        html += f'<div class="q-box"><b>ข้อที่ {i}.</b> '
        if is_key:
            if ("(แบบตั้งหลัก)" in sub_t and "สมการ" not in sub_t) or "หารยาว" in sub_t:
                html += f'{item["solution"]}'
            else:
                html += f'{item["question"]}<br><div class="sol-text">{item["solution"]}</div>'
        else:
            html += f'{item["question"]}'
            html += '<div class="workspace">พื้นที่แสดงวิธีทำ / ทดเลข...</div><div class="ans-line">ตอบ: </div>'
        html += '</div>'
        
    if brand_name: html += f'<div class="page-footer">&copy; 2026 {brand_name} | สงวนลิขสิทธิ์</div>'
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
            <div class="grade-badge">ชั้น{grade}</div>
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

else: # โหมดข้อสอบแข่งขัน TMC
    selected_grade = st.sidebar.selectbox("🏆 เลือกระดับชั้นแข่งขัน:", ["ป.2"]) 
    selected_main = "ข้อสอบแข่งขันระดับชาติ"
    selected_sub = st.sidebar.selectbox("📝 เลือกแนวข้อสอบ (รวม 20 แนวระดับท็อป!):", curriculum_db["ป.2"]["🌟 โจทย์แข่งขัน (แนว TMC)"] + ["🌟 สุ่มรวมทุกแนว"])
    if selected_sub == "🌟 สุ่มรวมทุกแนว":
        st.sidebar.info("💡 โหมดนี้จะสุ่มข้อสอบแข่งขันทั้ง 20 แนวมาคละกัน พร้อมสุ่มชื่อตัวละคร สถานที่ และสิ่งของ ไม่ให้ซ้ำกันเลย!")

num_input = st.sidebar.number_input("🔢 จำนวนข้อ:", min_value=1, max_value=100, value=10)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📏 ตั้งค่าหน้ากระดาษ (อัปเดตใหม่)")
spacing_level = st.sidebar.select_slider(
    "↕️ ความสูงของพื้นที่ทดเลข (อัปเดตใหม่):", 
    options=["แคบ", "ปานกลาง", "กว้าง", "กว้างพิเศษ"], 
    value="ปานกลาง"
)

if spacing_level == "แคบ":
    q_margin, ws_height = "15px", "100px"
elif spacing_level == "ปานกลาง":
    q_margin, ws_height = "20px", "180px"
elif spacing_level == "กว้าง":
    q_margin, ws_height = "30px", "280px"
else: # กว้างพิเศษ
    q_margin, ws_height = "40px", "400px"

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 ตั้งค่าแบรนด์ & หน้าปก")
brand_name = st.sidebar.text_input("🏷️ ชื่อแบรนด์ / ผู้สอน (Copyright):", value="บ้านทีเด็ด")
include_cover = st.sidebar.checkbox("🎨 สร้างหน้าปก (Cover Page)", value=True)
color_theme = st.sidebar.selectbox("🎨 ธีมสีหน้าปก:", ["ฟ้าคลาสสิก (Blue)", "ชมพูพาสเทล (Pink)", "เขียวธรรมชาติ (Green)", "ม่วงสร้างสรรค์ (Purple)", "ส้มสดใส (Orange)"])
theme_map = {
    "ฟ้าคลาสสิก (Blue)": {"border": "#3498db", "badge": "#e74c3c"},
    "ชมพูพาสเทล (Pink)": {"border": "#ff9ff3", "badge": "#0abde3"},
    "เขียวธรรมชาติ (Green)": {"border": "#2ecc71", "badge": "#e67e22"},
    "ม่วงสร้างสรรค์ (Purple)": {"border": "#9b59b6", "badge": "#f1c40f"},
    "ส้มสดใส (Orange)": {"border": "#f39c12", "badge": "#2c3e50"}
}

if st.sidebar.button("🚀 สั่งสร้างใบงานเดี๋ยวนี้", type="primary", use_container_width=True):
    with st.spinner("กำลังประมวลผลลอจิกคณิตศาสตร์และวาดกราฟิก..."):
        qs = generate_questions_logic(selected_grade, selected_main, selected_sub, num_input)
        
        html_w = create_page(selected_grade, selected_sub, qs, is_key=False, q_margin=q_margin, ws_height=ws_height, brand_name=brand_name)
        html_k = create_page(selected_grade, selected_sub, qs, is_key=True, q_margin=q_margin, ws_height=ws_height, brand_name=brand_name)
        html_cover = generate_cover_html(selected_grade, selected_main, selected_sub, num_input, theme_map[color_theme], brand_name) if include_cover else ""
        
        st.session_state['worksheet_html'] = html_w
        st.session_state['answerkey_html'] = html_k
        
        ebook_body = ""
        if include_cover: ebook_body += f'\n<div class="a4-wrapper cover-wrapper">{extract_body(html_cover)}</div>\n'
        ebook_body += f'\n<div class="a4-wrapper">{extract_body(html_w)}</div>\n<div class="a4-wrapper">{extract_body(html_k)}</div>\n'
        
        full_ebook_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
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
                .cover-wrapper {{ height: 260mm; }} 
            }}
            .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 10px; padding-bottom: 10px; }}
            .q-box {{ margin-bottom: {q_margin}; padding: 5px 15px; page-break-inside: avoid; border-bottom: 1px dashed #eee; font-size: 20px; }}
            .workspace {{ height: {ws_height}; border: 2px dashed #bdc3c7; border-radius: 8px; margin: 10px 0; padding: 10px; color: #95a5a6; font-size: 16px; display: flex; align-items: flex-start; }}
            .ans-line {{ margin-top: 5px; border-bottom: 1px dotted #999; width: 80%; height: 30px; font-weight: bold; font-size: 20px; display: flex; align-items: flex-end; padding-bottom: 5px; }}
            .sol-text {{ color: #333; font-size: 20px; display: inline-block; margin-top: 5px; line-height: 1.5; }}
            .page-footer {{ text-align: right; font-size: 14px; color: #95a5a6; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }}
            .cover-inner {{ width: 100%; height: 100%; padding: 40px; box-sizing: border-box; text-align: center; position: relative; border: 15px solid {theme_map[color_theme]['border']}; background: white; }}
            .title-box {{ margin-top: 80px; }} .title {{ font-size: 65px; color: #2c3e50; font-weight: bold; margin: 0; }}
            .grade-badge {{ font-size: 45px; background-color: {theme_map[color_theme]['badge']}; color: white; padding: 15px 50px; border-radius: 50px; display: inline-block; font-weight: bold; margin-top: 30px; }}
            .topic {{ font-size: 42px; color: #34495e; margin-top: 70px; font-weight: bold; }}
            .sub-topic {{ font-size: 32px; color: #7f8c8d; margin-top: 10px; }} .icons {{ font-size: 110px; margin: 60px 0; }}
            .details-badge {{ background-color: #2ecc71; color: white; display: inline-block; padding: 15px 40px; border-radius: 15px; font-size: 32px; font-weight: bold; }}
            .footer {{ position: absolute; bottom: 40px; left: 0; width: 100%; text-align: center; font-size: 22px; color: #7f8c8d; }}
        </style></head><body>{ebook_body}</body></html>"""

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
    st.success(f"✅ สร้างไฟล์สำเร็จ! (กล่องทดเลขจะปรับขนาดตามการตั้งค่าแล้ว)")
    st.markdown("### 📥 เลือกรูปแบบดาวน์โหลด")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📄 โหลดเฉพาะโจทย์ (Worksheet)", data=st.session_state['worksheet_html'], file_name=f"{st.session_state['filename_base']}_Worksheet.html", mime="text/html", use_container_width=True)
        st.download_button("🔑 โหลดเฉพาะเฉลย (Answer Key)", data=st.session_state['answerkey_html'], file_name=f"{st.session_state['filename_base']}_AnswerKey.html", mime="text/html", use_container_width=True)
    with c2:
        st.download_button("📚 โหลดรวมเล่ม (Full E-Book)", data=st.session_state['ebook_html'], file_name=f"{st.session_state['filename_base']}_Full_EBook.html", mime="text/html", use_container_width=True)
        st.download_button("🗂️ โหลดแพ็กเกจทั้งหมด (.zip)", data=st.session_state['zip_data'], file_name=f"{st.session_state['filename_base']}.zip", mime="application/zip", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 👁️ ดูตัวอย่างใบงาน (Live Preview)")
    components.html(st.session_state['ebook_html'], height=800, scrolling=True)
else:
    st.info("👈 กรุณาเลือกโหมด 'ข้อสอบแข่งขันระดับชาติ' ทางซ้ายมือ เพื่อดูโจทย์ชุดใหม่ล่าสุด!")
