import streamlit as st
import streamlit.components.v1 as components
import random
import math
import zipfile
import io
import time

try:
    import pdfkit
    HAS_PDFKIT = True
except ImportError:
    HAS_PDFKIT = False

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
            for _ in range(div_len + 1): empty_rows += f"<td style='width: 35px; height: 45px;'></td>"
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
    if grade in ["ป.1", "ป.2", "ป.3"]: return "<b style='color: #2c3e50; margin-right: 5px;'>ประโยคสัญลักษณ์:</b>"
    return ""

def generate_questions_logic(grade, main_t, sub_t, num_q):
    questions = []; seen = set()
    limit_map = {"ป.1": 100, "ป.2": 1000, "ป.3": 100000, "ป.4": 1000000, "ป.5": 9000000, "ป.6": 9000000}
    limit = limit_map.get(grade, 100)

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
                actual_sub_t = random.choice(curriculum_db[grade][random.choice(all_mains)])
            elif sub_t == "🌟 สุ่มรวมทุกแนว":
                actual_sub_t = random.choice(comp_topics)

            prefix = get_prefix(grade)

            if actual_sub_t == "ปริศนาตัวเลขซ่อนแอบ":
                a, b = random.randint(1, 4), 0
                b = random.randint(a + 2, 9)
                diff, k, sum_val = b - a, (b - a) * 9, a + b
                q = f"ให้ A และ B เป็นเลขโดดที่ต่างกัน โดยที่จำนวนสองหลัก <b>AB</b> เมื่อนำมาบวกกับ <b>{k}</b> จะได้ผลลัพธ์เป็นจำนวนสองหลัก <b>BA</b> (นั่นคือ AB + {k} = BA) และกำหนดให้ <b>A + B = {sum_val}</b> <br>จงหาว่าจำนวนสองหลัก <b>AB</b> คือจำนวนใด?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>จาก BA - AB = {k} เราสามารถหาผลต่างได้จาก B - A = {k} ÷ 9 = <b>{diff}</b><br>โจทย์กำหนด A + B = <b>{sum_val}</b><br>หาเลข 2 ตัวที่บวกกันได้ {sum_val} และลบกันได้ {diff} <br>B = ({sum_val} + {diff}) ÷ 2 = <b>{b}</b> และ A = {sum_val} - {b} = <b>{a}</b><br>ดังนั้น จำนวน AB คือ </span><b>{a}{b}</b>"

            elif actual_sub_t == "การนับหน้าหนังสือ":
                pages = random.randint(40, 150)
                ans = 9 + 180 + ((pages - 99) * 3) if pages > 99 else 9 + ((pages - 9) * 2)
                item = random.choice(ITEMS_LIST)
                q = f"โรงพิมพ์กำลังจัดพิมพ์หนังสือแคตตาล็อกแนะนำ<b>{item}</b> ซึ่งมีความหนาทั้งหมด <b>{pages}</b> หน้า หากต้องการพิมพ์ตัวเลขหน้าทั้งหมดตั้งแต่หน้า 1 ถึง {pages} จะต้องพิมพ์ตัวเลขโดดทั้งหมดกี่ตัว?"
                if pages > 99:
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>1) หน้า 1-9 (เลข 1 หลัก) มี 9 หน้า ใช้ = 9 × 1 = <b>9 ตัว</b><br>2) หน้า 10-99 (เลข 2 หลัก) มี 90 หน้า ใช้ = 90 × 2 = <b>180 ตัว</b><br>3) หน้า 100-{pages} (เลข 3 หลัก) มี {pages-99} หน้า ใช้ = {pages-99} × 3 = <b>{(pages-99)*3} ตัว</b><br>รวม: 9 + 180 + {(pages-99)*3} = </span><b>{ans} ตัว</b>"
                else:
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>1) หน้า 1-9 (เลข 1 หลัก) มี 9 หน้า ใช้ = 9 × 1 = <b>9 ตัว</b><br>2) หน้า 10-{pages} (เลข 2 หลัก) มี {pages-9} หน้า ใช้ = {pages-9} × 2 = <b>{(pages-9)*2} ตัว</b><br>รวม: 9 + {(pages-9)*2} = </span><b>{ans} ตัว</b>"

            elif actual_sub_t == "การปักเสาและปลูกต้นไม้":
                d = random.choice([2, 4, 5, 10, 15]); trees = random.randint(12, 35)
                loc = random.choice(LOCATIONS_LIST)
                q = f"เทศบาลต้องการปลูกต้นไม้ริมถนนทางเข้า<b>{loc}</b> โดยให้ห่างกันต้นละ <b>{d}</b> เมตร และต้องปลูกที่จุดเริ่มต้นและสิ้นสุดของถนนพอดี หากใช้ต้นไม้ <b>{trees}</b> ต้น ถนนเส้นนี้ยาวกี่เมตร?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>เนื่องจากมีการปลูกต้นไม้ที่หัวและท้ายถนน <br>จำนวนช่วงห่าง = จำนวนต้นไม้ - 1 = {trees} - 1 = <b>{trees-1} ช่วง</b><br>แต่ละช่วงยาว {d} เมตร<br>ความยาวถนนทั้งหมด = {trees-1} × {d} = </span><b>{(trees-1)*d} เมตร</b>"

            elif actual_sub_t == "สัตว์ปีนบ่อ":
                u = random.randint(3, 7); d = random.randint(1, u - 1)
                net = u - d; h = random.randint(15, 30); days = math.ceil((h - u) / net) + 1
                animal = random.choice(ANIMALS_LIST)
                q = f"<b>{animal}</b>ตัวหนึ่งตกลงไปในบ่อลึก <b>{h}</b> เมตร กลางวันปีนขึ้นมาได้ <b>{u}</b> เมตร แต่กลางคืนลื่นตกลงไป <b>{d}</b> เมตร จะต้องใช้เวลาอย่างน้อยที่สุดกี่วันจึงจะปีนพ้นปากบ่อ?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>1 วัน (24 ชม.) ปีนได้สุทธิ {u} - {d} = <b>{net} เมตร</b><br><i>*จุดหลอก:</i> วันสุดท้ายเมื่อปีนพ้นบ่อจะไม่ลื่นลงมาอีก!<br>ระยะทางก่อนถึงวันสุดท้าย = {h} - {u} = <b>{h - u} เมตร</b><br>เวลาที่ใช้ช่วงแรก = {h - u} ÷ {net} = {math.ceil((h-u)/net)} วัน<br>บวกวันสุดท้ายอีก 1 วัน = </span><b>{days} วัน</b>"

            elif actual_sub_t == "ตรรกะตาชั่งสมดุล":
                items = [("รถคันใหญ่", "รถคันเล็ก", "ตุ๊กตา"), ("หนังสือหนา", "สมุดบาง", "ยางลบ"), ("แตงโม", "สับปะรด", "มะละกอ")]
                i1, i2, i3 = random.choice(items); mul1 = random.randint(2, 5); mul2 = random.randint(2, 5)
                q = f"จากการเล่นตาชั่งสมดุล พบข้อมูลดังนี้:<br>- <b>{i1} 1 ชิ้น</b> หนักเท่ากับ <b>{i2} {mul1} ชิ้น</b><br>- <b>{i2} 1 ชิ้น</b> หนักเท่ากับ <b>{i3} {mul2} ชิ้น</b><br><br>อยากทราบว่า <b>{i1} จำนวน 2 ชิ้น</b> จะมีน้ำหนักเท่ากับ <b>{i3}</b> กี่ชิ้น?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>แปลงน้ำหนักให้เป็นหน่วย {i3}:<br>{i2} 1 ชิ้น = {i3} {mul2} ชิ้น<br>แทนค่า: {i1} 1 ชิ้น = {i2} {mul1} ชิ้น = {mul1} × {mul2} = <b>{i3} {mul1*mul2} ชิ้น</b><br>โจทย์ถามหา {i1} <b>2 ชิ้น</b> <br>นำ {mul1*mul2} × 2 = </span><b>{mul1*mul2*2} ชิ้น</b>"

            elif actual_sub_t == "อายุข้ามเวลาขั้นสูง":
                n1, n2, n3 = random.sample(NAMES_LIST, 3); age_a = random.randint(6, 10)  
                diff_b = random.randint(2, 5); age_b = age_a + diff_b; diff_c = random.randint(1, age_b - 2) 
                age_c = age_b - diff_c; past_years = random.randint(2, 5) 
                current_sum = age_a + age_b + age_c; past_sum = current_sum - (3 * past_years)
                q = f"ปัจจุบันพี่น้อง 3 คน คือ {n1}, {n2}, {n3} มีอายุรวมกัน <b>{current_sum}</b> ปีพอดี <br>จงหาว่าเมื่อ <b>{past_years}</b> ปีที่แล้ว เด็กทั้งสามคนนี้มีอายุรวมกันกี่ปี? (กำหนดให้ทุกคนเกิดแล้ว)"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>1) ปัจจุบัน ทั้ง 3 คนมีอายุรวมกัน = {current_sum} ปี<br>2) <i>*จุดหลอก:</i> ย้อนเวลาไป {past_years} ปี <b>ทุกคน</b>จะอายุน้อยลงคนละ {past_years} ปี<br>3) เด็ก 3 คน อายุที่ต้องหักออกรวม = 3 × {past_years} = <b>{3*past_years} ปี</b><br>อายุรวมเมื่ออดีต = {current_sum} - {3*past_years} = </span><b>{past_sum} ปี</b>"

            elif actual_sub_t == "การตัดเชือกพับทบ":
                folds = random.randint(2, 4); cuts = random.randint(2, 5); pieces = (2**folds) * cuts + 1
                name = random.choice(NAMES_LIST)
                q = f"<b>{name}</b>นำริบบิ้นมาพับทบครึ่งกัน <b>{folds}</b> ครั้ง (พับทบไปเรื่อยๆ) จากนั้นใช้กรรไกรตัดริบบิ้นให้ขาด <b>{cuts}</b> รอยตัด <br>เมื่อคลี่ออกมา <b>{name}</b>จะได้ริบบิ้นทั้งหมดกี่เส้น?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>1) พับ {folds} ครั้ง จะเกิดความหนา = 2 ยกกำลัง {folds} = <b>{2**folds} ชั้น</b><br>2) ตัด 1 รอย จะได้ริบบิ้นเพิ่ม {2**folds} เส้น<br>3) ตัด {cuts} รอย จะได้เพิ่ม = {2**folds} × {cuts} = <b>{(2**folds)*cuts} เส้น</b><br>รวมกับเส้นตั้งต้น 1 เส้น จะได้ทั้งหมด = {(2**folds)*cuts} + 1 = </span><b>{pieces} เส้น</b>"

            elif actual_sub_t == "แถวคอยแบบซ้อนทับ":
                front_pos = random.randint(10, 20); back_pos = random.randint(10, 20)
                total_people = front_pos + back_pos + random.randint(5, 12); between = total_people - (front_pos + back_pos)
                n1, n2 = random.sample(NAMES_LIST, 2); loc = random.choice(LOCATIONS_LIST)
                q = f"นักเรียนเข้าแถวรอเข้า<b>{loc}</b> มีคนทั้งหมด <b>{total_people}</b> คน<br>ถ้า <b>{n1}</b> ยืนลำดับที่ <b>{front_pos}</b> นับจากหัวแถว และ <b>{n2}</b> ยืนลำดับที่ <b>{back_pos}</b> นับจากท้ายแถว <br>อยากทราบว่ามีคนยืนอยู่ระหว่าง <b>{n1}</b> กับ <b>{n2}</b> กี่คน? (กำหนดให้ <b>{n1}</b> ยืนหน้า <b>{n2}</b>)"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>1) คนตั้งแต่หัวแถวถึง{n1} มี <b>{front_pos} คน</b><br>2) คนตั้งแต่ท้ายแถวถึง{n2} มี <b>{back_pos} คน</b><br>3) จำนวนคนตรงกลาง = คนทั้งหมด - (กลุ่มหน้า + กลุ่มหลัง)<br>= {total_people} - ({front_pos} + {back_pos}) = </span><b>{between} คน</b>"

            elif actual_sub_t == "ปัญหาผลรวม-ผลต่าง":
                diff = random.randint(5, 20); small = random.randint(10, 30)
                large = small + diff; total = large + small
                n1, n2 = random.sample(NAMES_LIST, 2); item = random.choice(ITEMS_LIST)
                q = f"<b>{n1}</b> และ <b>{n2}</b> มี<b>{item}</b>รวมกัน <b>{total}</b> ชิ้น หาก <b>{n1}</b> มีมากกว่า <b>{n2}</b> อยู่ <b>{diff}</b> ชิ้น จงหาว่า <b>{n1}</b> มี<b>{item}</b>กี่ชิ้น?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>1) หักส่วนที่มากกว่าออก: {total} - {diff} = <b>{total-diff} ชิ้น</b><br>2) แบ่ง 2 ส่วนเท่าๆ กัน (คือจำนวนของคนน้อย): {total-diff} ÷ 2 = <b>{small} ชิ้น</b><br>3) จำนวนของคนมาก ({n1}) = {small} + {diff} = </span><b>{large} ชิ้น</b>"

            elif actual_sub_t == "ตรรกะการจับมือ (ทักทาย)":
                n = random.randint(5, 12); ans = n * (n - 1) // 2; loc = random.choice(LOCATIONS_LIST)
                q = f"ในกิจกรรมที่<b>{loc}</b> มีเด็กทั้งหมด <b>{n}</b> คน หากทุกคนต้องเดินไปจับมือทำความรู้จักกันให้ครบทุกคน คนละ 1 ครั้ง จะมีการจับมือเกิดขึ้นทั้งหมดกี่ครั้ง?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>ใช้สูตรจับมือ: (จำนวนคน × จำนวนคนที่ต้องจับ) ÷ 2<br>= ({n} × {n-1}) ÷ 2 = <b>{ans} ครั้ง</b></span>"

            elif actual_sub_t == "โปรโมชั่นแลกของ":
                exch = random.choice([3, 4, 5]); start = exch * random.randint(3, 6)
                snack = random.choice(SNACKS_LIST); tot, emp = start, start
                while emp >= exch: new_b = emp // exch; emp = new_b + (emp % exch); tot += new_b
                q = f"โปรโมชั่น: นำซอง<b>{snack}</b>เปล่า <b>{exch}</b> ซอง แลกฟรี 1 ชิ้น <br>หากนักเรียนซื้อ<b>{snack}</b>ตอนแรก <b>{start}</b> ชิ้น จะได้กินทั้งหมดกี่ชิ้น (รวมของที่นำไปแลกมาใหม่)?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>นำของเปล่าไปแลกและนำเศษมารวมแลกต่อเรื่อยๆ<br>เริ่มต้น: กินไป {start} ชิ้น (เหลือเปล่า {start})<br>นำไปแลกจะได้ทั้งหมด </span><b>{tot} ชิ้น</b> (เหลือเศษซองเปล่า {emp} ซองแลกไม่ได้แล้ว)"

            elif actual_sub_t == "หยิบของในที่มืด":
                c1 = random.randint(5, 12); c2 = random.randint(5, 12); c3 = random.randint(3, 8)
                item = random.choice(ITEMS_LIST)
                q = f"ในกล่องทึบมี<b>{item}</b>สีแดง <b>{c1}</b> ชิ้น, น้ำเงิน <b>{c2}</b> ชิ้น, เขียว <b>{c3}</b> ชิ้น <br>หากหลับตาหยิบ จะต้องหยิบ<b>อย่างน้อยกี่ชิ้น</b> จึงจะมั่นใจ 100% ว่าได้สีเขียวแน่ๆ 1 ชิ้น?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ (ดวงซวยที่สุด):</b><br>สมมติหยิบได้สีอื่นจนหมดก่อน<br>สีแดง {c1} + สีน้ำเงิน {c2} = {c1+c2} ชิ้น<br>ชิ้นต่อไป (บวก 1) จะต้องเป็นสีเขียวแน่นอน<br>ดังนั้น {c1+c2} + 1 = </span><b>{c1+c2+1} ชิ้น</b>"

            elif actual_sub_t == "การคิดย้อนกลับ":
                s_money = random.randint(100, 300); spent = random.randint(20, 80)
                recv = random.randint(50, 150); f_money = s_money - spent + recv
                name = random.choice(NAMES_LIST); item = random.choice(ITEMS_LIST)
                q = f"<b>{name}</b>นำเงินไปซื้อ<b>{item}</b> <b>{spent}</b> บาท จากนั้นแม่ให้เพิ่มอีก <b>{recv}</b> บาท ทำให้ตอนนี้มีเงิน <b>{f_money}</b> บาท <br>จงหาว่าตอนแรก <b>{name}</b>มีเงินกี่บาท?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ (คิดย้อนกลับ):</b><br>คิดย้อนจากท้ายไปหน้า สลับบวกเป็นลบ ลบเป็นบวก<br>มีเงิน {f_money} -> แม่ให้มา (ลบออก) {recv} -> ซื้อของ (บวกคืน) {spent}<br>{f_money} - {recv} + {spent} = </span><b>{s_money} บาท</b>"

            elif actual_sub_t == "แผนภาพความชอบ":
                tot = random.randint(30, 50); both = random.randint(5, 12)
                only_a, only_b = random.randint(8, 15), random.randint(8, 15)
                l_a, l_b = only_a + both, only_b + both; neither = tot - (only_a + only_b + both)
                n1, n2 = random.sample(SNACKS_LIST, 2)
                q = f"นักเรียน <b>{tot}</b> คน มีคนชอบ<b>{n1}</b> <b>{l_a}</b> คน, ชอบ<b>{n2}</b> <b>{l_b}</b> คน, และชอบทั้งสองอย่าง <b>{both}</b> คน <br>มีนักเรียนกี่คนที่ไม่ชอบขนมทั้งสองชนิดนี้เลย?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>คนชอบอย่างน้อย 1 ชนิด = ({l_a} + {l_b}) - {both} = <b>{l_a+l_b-both} คน</b><br>คนที่ไม่ชอบเลย = คนทั้งหมด - คนที่ชอบ<br>= {tot} - {l_a+l_b-both} = </span><b>{neither} คน</b>"

            elif actual_sub_t == "คิววงกลมมรณะ":
                n_half = random.randint(4, 12); total = n_half * 2
                pos1 = random.randint(1, n_half); pos2 = pos1 + n_half
                n1, n2 = random.sample(NAMES_LIST, 2)
                q = f"เด็กยืนล้อมวงกลมเว้นระยะเท่าๆ กัน นับหมายเลข 1, 2, 3... <br>ถ้า <b>{n1}</b> ยืนหมายเลข <b>{pos1}</b> และมองไปฝั่งตรงข้ามพอดีพบ <b>{n2}</b> ยืนหมายเลข <b>{pos2}</b> <br>เด็กกลุ่มนี้มีทั้งหมดกี่คน?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>การอยู่ตรงข้ามกันคือ 'ครึ่งวงกลม'<br>ระยะครึ่งวงกลม = {pos2} - {pos1} = <b>{n_half} คน</b><br>เต็มวงกลม = {n_half} × 2 = </span><b>{total} คน</b>"

            elif actual_sub_t == "ลำดับแบบวนลูป":
                word = random.choice(["MATHEMATICS", "THAILAND", "ELEPHANT", "SUPERMAN"])
                target = random.randint(30, 80); rem = target % len(word)
                ans_char = word[rem - 1] if rem != 0 else word[-1]
                q = f"เขียนคำว่า <b>{word}</b> เรียงต่อกันไปเรื่อยๆ (<b>{word}{word[:3]}...</b>) <br>ตัวอักษรในตำแหน่งที่ <b>{target}</b> คือตัวอักษรใด?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>1 ชุดมี <b>{len(word)} ตัวอักษร</b><br>{target} ÷ {len(word)} = {target//len(word)} เศษ <b>{rem}</b><br>เศษ {rem} คือตัวที่ {rem if rem != 0 else len(word)} ของคำ ซึ่งก็คือ </span><b>{ans_char}</b>"

            elif actual_sub_t == "เส้นทางที่เป็นไปได้":
                p1, p2, p3 = random.randint(2, 4), random.randint(2, 4), random.randint(1, 3)
                q = f"เดินทางจากเมือง A ไป B มีถนน <b>{p1}</b> สาย, จาก B ไป C มีถนน <b>{p2}</b> สาย <br>และมีทางลัดจาก A ไป C โดยตรง <b>{p3}</b> สาย<br>มีเส้นทางจาก A ไป C ทั้งหมดกี่แบบ?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>ผ่าน B: {p1} × {p2} = {p1*p2} ทาง<br>ทางลัด: {p3} ทาง<br>รวม: {p1*p2} + {p3} = </span><b>{(p1*p2)+p3} แบบ</b>"

            elif actual_sub_t == "นาฬิกาเดินเพี้ยน":
                fast_min = random.randint(2, 5); start_h = 8; p_h = random.randint(3, 6)
                end_h = start_h + p_h; total_fast = fast_min * p_h
                q = f"นาฬิกาเดินเร็วไป <b>{fast_min} นาทีในทุก 1 ชั่วโมง</b> <br>ตั้งเวลาให้ตรงเป๊ะตอน <b>{start_h}:00 น.</b> เมื่อเวลาจริงผ่านไปถึง <b>{end_h}:00 น.</b> นาฬิกาจะบอกเวลาใด?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>เวลาผ่านไป {p_h} ชั่วโมง<br>นาฬิกาเร็วขึ้น = {fast_min} × {p_h} = <b>{total_fast} นาที</b><br>ดังนั้น นาฬิกาจะแสดงเวลา </span><b>{end_h}:{total_fast:02d} น.</b>"

            elif actual_sub_t == "จัดของใส่กล่อง":
                box_cap = random.randint(4, 9); num_boxes = random.randint(5, 12)
                rem = random.randint(1, box_cap - 1); tot = (box_cap * num_boxes) + rem
                item, name = random.choice(ITEMS_LIST), random.choice(NAMES_LIST)
                q = f"<b>{name}</b>มี<b>{item}</b> <b>{tot}</b> ชิ้น จัดใส่กล่อง กล่องละ <b>{box_cap}</b> ชิ้น <br>จะได้เต็มกล่องกี่ใบ และเหลือเศษกี่ชิ้น?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>{tot} ÷ {box_cap} = <b>{num_boxes}</b> เศษ <b>{rem}</b><br>ตอบ: จัดเต็มกล่อง </span><b>{num_boxes} ใบ</b> และเหลือเศษ <b>{rem} ชิ้น</b>"

            elif actual_sub_t == "คะแนนยิงเป้า":
                s1, s2, s3 = random.choices([10, 5, 1], k=3)
                name = random.choice(NAMES_LIST)
                q = f"เกมปาลูกดอกมี 3 วง: <b>10, 5, 1</b> คะแนน <br><b>{name}</b> ปา 3 ครั้งเข้าเป้าทั้งหมด ได้คะแนนรวม <b>{s1+s2+s3}</b> คะแนน <br><b>{name}</b> ปาเข้าวงใดบ้าง? (เรียงจากมากไปน้อย)"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>หาตัวเลข 3 ตัวจาก (10, 5, 1) ที่บวกกันได้ {s1+s2+s3}<br>นั่นคือ: {s1} + {s2} + {s3} = {s1+s2+s3}<br>ตอบ: </span><b>{sorted([s1,s2,s3], reverse=True)}</b>"

            # ==============================
            # โหมดหลักสูตรปกติ
            # ==============================
            elif actual_sub_t == "การคูณ (แบบตั้งหลัก)":
                if grade in ["ป.1", "ป.2"]: a = random.randint(10, 99) 
                elif grade == "ป.3": a = random.randint(100, 999) 
                else: a = random.randint(1000, 9999) 
                b = random.randint(2, 9); res = a * b
                sentence = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} × {b:,} = {box_html}</span>"
                q = sentence + generate_vertical_table_html(a, b, '×', is_key=False)
                sol = sentence + generate_vertical_table_html(a, b, '×', result=res, is_key=True)

            elif actual_sub_t == "การบวก (แบบตั้งหลัก)":
                if grade == "ป.1":
                    tens_a = random.randint(1, 9); units_a = random.randint(0, 8)
                    b = random.randint(1, 9 - units_a); a = (tens_a * 10) + units_a
                elif grade in ["ป.4", "ป.5", "ป.6"]:
                    a = random.randint(10000, limit // 2); b = random.randint(10000, limit // 2)
                else:
                    a = random.randint(10, limit - 20); b = random.randint(1, limit - a - 1)
                res = a + b
                sentence = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} + {b:,} = {box_html}</span>"
                q = sentence + generate_vertical_table_html(a, b, '+', is_key=False)
                sol = sentence + generate_vertical_table_html(a, b, '+', result=res, is_key=True)

            elif actual_sub_t == "การลบ (แบบตั้งหลัก)":
                if grade == "ป.1":
                    tens_a = random.randint(1, 9); units_a = random.randint(1, 9)
                    b = random.randint(1, units_a); a = (tens_a * 10) + units_a
                elif grade in ["ป.4", "ป.5", "ป.6"]:
                    a = random.randint(100000, limit - 1); b = random.randint(10000, a - 1)
                else:
                    a = random.randint(10, limit - 1); b = random.randint(1, a - 1)
                res = a - b
                sentence = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} - {b:,} = {box_html}</span>"
                q = sentence + generate_vertical_table_html(a, b, '-', is_key=False)
                sol = sentence + generate_vertical_table_html(a, b, '-', result=res, is_key=True)

            elif "การหารพื้นฐาน" in actual_sub_t:
                a = random.randint(2, 9); b = random.randint(2, 12); dividend = a * b
                q = f"จงหาผลลัพธ์ของ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {dividend} ÷ {a} = {box_html}</span>"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> ท่องสูตรคูณแม่ {a} จะพบว่า {a} × {b} = {dividend}<br>ดังนั้น {dividend} ÷ {a} = </span> <b>{b}</b>"

            elif "ส่วนย่อย-ส่วนรวม" in actual_sub_t:
                total = random.randint(5, 20); p1 = random.randint(1, total - 1); p2 = total - p1; miss = random.choice(['t', 'p1', 'p2'])
                svg_t = f"""<div style="display: block; text-align: center; margin-top: 10px;"><svg width="200" height="160"><line x1="100" y1="40" x2="50" y2="120" stroke="#333" stroke-width="3"/><line x1="100" y1="40" x2="150" y2="120" stroke="#333" stroke-width="3"/><circle cx="100" cy="40" r="30" fill="#e8f8f5" stroke="#16a085" stroke-width="3"/><circle cx="50" cy="120" r="30" fill="#fdf2e9" stroke="#d35400" stroke-width="3"/><circle cx="150" cy="120" r="30" fill="#fdf2e9" stroke="#d35400" stroke-width="3"/><text x="100" y="47" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='t' else "#16a085"}">{{t}}</text><text x="50" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='p1' else "#d35400"}">{{p1}}</text><text x="150" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='p2' else "#d35400"}">{{p2}}</text></svg></div>"""
                q = f"จงหาตัวเลขที่หายไป (?) : " + svg_t.format(t="?" if miss=='t' else total, p1="?" if miss=='p1' else p1, p2="?" if miss=='p2' else p2)
                miss_map = {'t': 'ส่วนรวม (วงกลมบน)', 'p1': 'ส่วนย่อย (วงกลมซ้าย)', 'p2': 'ส่วนย่อย (วงกลมขวา)'}
                if miss == 't': calc_str = f"นำส่วนย่อยมาบวกกัน: {p1} + {p2} = <b>{total}</b>"
                elif miss == 'p1': calc_str = f"นำส่วนรวมลบด้วยส่วนย่อยที่มี: {total} - {p2} = <b>{p1}</b>"
                else: calc_str = f"นำส่วนรวมลบด้วยส่วนย่อยที่มี: {total} - {p1} = <b>{p2}</b>"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> หา{miss_map[miss]}ที่หายไป โดย{calc_str}</span><br>" + svg_t.format(t=total, p1=p1, p2=p2)

            elif "การบอกอันดับที่" in actual_sub_t:
                c_map = {"แดง": "#ff4d4d", "ฟ้า": "#3498db", "เขียว": "#2ecc71", "เหลือง": "#f1c40f", "ชมพู": "#ff9ff3"}
                cols = list(c_map.keys()); random.shuffle(cols); x_pos = [280, 220, 160, 100, 40]
                cars = "".join([f'<g transform="translate({x_pos[i]}, 40)"><path d="M 10 15 L 15 5 L 30 5 L 35 15 Z" fill="#e0e0e0" stroke="#333" stroke-width="1"/><rect x="0" y="15" width="50" height="15" rx="4" fill="{c_map[cols[i]]}" stroke="#333" stroke-width="1.5"/><circle cx="12" cy="30" r="6" fill="#333"/><circle cx="38" cy="30" r="6" fill="#333"/></g>' for i in range(5)])
                svg_d = f"""<div style="display: block; text-align: center; margin-top: 10px;"><svg width="400" height="80"><line x1="20" y1="76" x2="380" y2="76" stroke="#95a5a6" stroke-width="4"/><rect x="350" y="30" width="10" height="46" fill="#fff" stroke="#333"/><text x="355" y="20" font-size="14" font-weight="bold" text-anchor="middle" fill="#e74c3c">เส้นชัย</text>{cars}</svg></div>"""
                idx = random.randint(0, 4); name = cols[idx]
                ans_svg = f'<svg width="60" height="30" style="vertical-align: middle; margin-left: 10px;"><path d="M 10 10 L 15 2 L 30 2 L 35 10 Z" fill="#e0e0e0" stroke="#333"/><rect y="10" width="50" height="12" rx="3" fill="{c_map[name]}" stroke="#333"/><circle cx="12" cy="22" r="5" fill="#333"/><circle cx="38" cy="22" r="5" fill="#333"/></svg>'
                if random.choice([True, False]): 
                    q = f"รถสี{name} วิ่งอยู่อันดับที่เท่าไร? {svg_d}"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> สังเกตจากป้ายเส้นชัยทางขวามือ แล้วนับย้อนมาทางซ้าย</span><br><b>อันดับที่ {idx + 1}</b> {ans_svg}"
                else: 
                    q = f"รถที่วิ่งอยู่ในอันดับที่ {idx + 1} คือรถสีอะไร? {svg_d}"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> เริ่มนับคันแรกจากป้ายเส้นชัยฝั่งขวามือ นับย้อนไป {idx + 1} คัน</span><br><b>สี{name}</b> {ans_svg}"

            elif "แบบรูปซ้ำ" in actual_sub_t:
                shapes = {"วงกลม": '<circle cx="15" cy="15" r="12" fill="#ffb3ba" stroke="#333" stroke-width="2"/>', "สี่เหลี่ยม": '<rect x="3" y="3" width="24" height="24" fill="#bae1ff" stroke="#333" stroke-width="2"/>', "สามเหลี่ยม": '<polygon points="15,3 27,27 3,27" fill="#baffc9" stroke="#333" stroke-width="2"/>', "ดาว": '<polygon points="15,1 19,10 29,10 21,16 24,26 15,20 6,26 9,16 1,10 11,10" fill="#ffffba" stroke="#333" stroke-width="2"/>'}
                pt = random.choice([[0, 1], [0, 1, 2], [0, 0, 1], [0, 1, 1]])
                keys = random.sample(list(shapes.keys()), len(set(pt)))
                seq = [keys[pt[i % len(pt)]] for i in range(12)]; slen = random.randint(5, 8) 
                html = "<div style='margin-top:10px; text-align:center; display: block;'>" + "".join([f'<svg width="30" height="30" style="vertical-align: middle; margin: 0 5px;">{shapes[seq[i]]}</svg>' for i in range(slen)]) + '<span style="display:inline-block; width:30px; height:30px; border-bottom:2px dashed #000; margin: 0 5px;"></span></div>'
                q = f"รูปที่หายไปคือรูปใด? {html}"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> สังเกตจะพบว่ารูปภาพมีการเรียงซ้ำกันเป็นชุด ชุดละ {len(set(pt))} รูป:</span><br><br><svg width='30' height='30' style='vertical-align: middle;'>{shapes[seq[slen]]}</svg>"

            elif "นาฬิกา" in actual_sub_t:
                h = random.randint(1, 12); m = random.randint(0, 59)
                cx, cy = 100, 100; svg_elements = []
                svg_elements.append(f'<circle cx="{cx}" cy="{cy}" r="75" fill="#fdfdfd" stroke="#333" stroke-width="3"/>')
                for i in range(60):
                    angle_deg = i * 6 - 90; angle_rad = math.radians(angle_deg)
                    if i % 5 == 0:
                        tx1 = cx + 65 * math.cos(angle_rad); ty1 = cy + 65 * math.sin(angle_rad)
                        tx2 = cx + 75 * math.cos(angle_rad); ty2 = cy + 75 * math.sin(angle_rad)
                        svg_elements.append(f'<line x1="{tx1}" y1="{ty1}" x2="{tx2}" y2="{ty2}" stroke="#333" stroke-width="3" />')
                        hour = i // 5 if i // 5 != 0 else 12
                        tx_h = cx + 50 * math.cos(angle_rad); ty_h = cy + 50 * math.sin(angle_rad) + 6
                        svg_elements.append(f'<text x="{tx_h}" y="{ty_h}" font-size="18" font-weight="bold" fill="#e74c3c" text-anchor="middle">{hour}</text>')
                        tx_m = cx + 88 * math.cos(angle_rad); ty_m = cy + 88 * math.sin(angle_rad) + 4
                        svg_elements.append(f'<text x="{tx_m}" y="{ty_m}" font-size="12" font-weight="bold" fill="#3498db" text-anchor="middle">{i}</text>')
                    else:
                        tx1 = cx + 70 * math.cos(angle_rad); ty1 = cy + 70 * math.sin(angle_rad)
                        tx2 = cx + 75 * math.cos(angle_rad); ty2 = cy + 75 * math.sin(angle_rad)
                        svg_elements.append(f'<line x1="{tx1}" y1="{ty1}" x2="{tx2}" y2="{ty2}" stroke="#777" stroke-width="1.5" />')
                ah = (h % 12) * 30 + (m / 60) * 30; am = m * 6
                hx_dash = cx + 75 * math.cos(math.radians(ah - 90)); hy_dash = cy + 75 * math.sin(math.radians(ah - 90))
                svg_elements.append(f'<line x1="{cx}" y1="{cy}" x2="{hx_dash}" y2="{hy_dash}" stroke="#e74c3c" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.7"/>')
                hx = cx + 40 * math.cos(math.radians(ah - 90)); hy = cy + 40 * math.sin(math.radians(ah - 90))
                svg_elements.append(f'<line x1="{cx}" y1="{cy}" x2="{hx}" y2="{hy}" stroke="#e74c3c" stroke-width="5" stroke-linecap="round" />')
                mx = cx + 65 * math.cos(math.radians(am - 90)); my = cy + 65 * math.sin(math.radians(am - 90))
                svg_elements.append(f'<line x1="{cx}" y1="{cy}" x2="{mx}" y2="{my}" stroke="#3498db" stroke-width="3" stroke-linecap="round" />')
                svg_elements.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="#333"/>')
                svg = f'<div style="text-align: center; margin: 15px 0;"><svg width="180" height="180" viewBox="0 0 200 200">{"".join(svg_elements)}</svg></div>'
                day = random.choice(["เวลากลางวัน", "เวลากลางคืน"])
                q = f"หากเป็น <b>{day}</b> จะอ่านเวลาได้กี่นาฬิกา กี่นาที? {svg}"
                ans_h = h + 12 if day == "เวลากลางวัน" and 1 <= h <= 5 else (h + 12 if day == "เวลากลางคืน" and 6 <= h <= 11 else (0 if day == "เวลากลางคืน" and h == 12 else h))
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> เข็มสั้นชี้ระหว่าง {h} กับ {h+1 if h<12 else 1} เข็มยาวชี้ที่ {m} นาที</span><br><b>{ans_h:02d}.{m:02d} น.</b>"

            elif "จำนวนเงิน" in actual_sub_t:
                b100 = random.randint(0, 3); b50 = random.randint(0, 2); b20 = random.randint(0, 4)
                c10 = random.randint(0, 5); c5 = random.randint(0, 3); c1 = random.randint(0, 5)
                if b100+b50+b20+c10+c5+c1 == 0: b20 = 1
                total = (b100*100) + (b50*50) + (b20*20) + (c10*10) + (c5*5) + (c1*1)
                money_svg = "<div style='margin-top:10px; line-height: 2.5; display: block; text-align: center;'>"
                for _ in range(b100): money_svg += '<svg width="60" height="30" style="vertical-align: middle; margin: 2px;"><rect width="60" height="30" rx="3" fill="#ff7675" stroke="#c0392b" stroke-width="2"/><text x="30" y="20" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">100</text></svg>'
                for _ in range(b50): money_svg += '<svg width="60" height="30" style="vertical-align: middle; margin: 2px;"><rect width="60" height="30" rx="3" fill="#74b9ff" stroke="#2980b9" stroke-width="2"/><text x="30" y="20" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">50</text></svg>'
                for _ in range(b20): money_svg += '<svg width="60" height="30" style="vertical-align: middle; margin: 2px;"><rect width="60" height="30" rx="3" fill="#55efc4" stroke="#27ae60" stroke-width="2"/><text x="30" y="20" font-size="12" font-weight="bold" fill="#333" text-anchor="middle">20</text></svg>'
                for _ in range(c10): money_svg += '<svg width="30" height="30" style="vertical-align: middle; margin: 2px;"><circle cx="15" cy="15" r="13" fill="#bdc3c7" stroke="#7f8c8d" stroke-width="2"/><circle cx="15" cy="15" r="8" fill="#f1c40f"/><text x="15" y="19" font-size="10" font-weight="bold" fill="#333" text-anchor="middle">10</text></svg>'
                for _ in range(c5): money_svg += '<svg width=\"30\" height=\"30\" style=\"vertical-align: middle; margin: 2px;\"><circle cx=\"15\" cy=\"15\" r=\"11\" fill=\"#ecf0f1\" stroke=\"#95a5a6\" stroke-width=\"2\"/><text x=\"15\" y=\"19\" font-size=\"10\" font-weight=\"bold\" fill=\"#333\" text-anchor=\"middle\">5</text></svg>'
                for _ in range(c1): money_svg += '<svg width=\"30\" height=\"30\" style=\"vertical-align: middle; margin: 2px;\"><circle cx=\"15\" cy=\"15\" r=\"9\" fill=\"#ecf0f1\" stroke=\"#bdc3c7\" stroke-width=\"1.5\"/><text x=\"15\" y=\"19\" font-size=\"10\" font-weight=\"bold\" fill=\"#333\" text-anchor=\"middle\">1</text></svg>'
                money_svg += "</div>"
                q = f"จากภาพ มีเงินทั้งหมดกี่บาท? {money_svg}"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> นำธนบัตรและเหรียญทั้งหมดมารวมกัน</span><br><b>{total:,} บาท</b>"

            elif "เครื่องชั่งสปริง" in actual_sub_t:
                kg = random.randint(0, 4); khid = random.randint(0, 9)
                if kg == 0 and khid == 0: khid = random.randint(1, 9)
                total_khid = kg * 10 + khid; angle_deg = -150 + (total_khid * 6)
                cx, cy = 100, 120; r_dial = 70; svg_elements = []
                svg_elements.append('<rect x="25" y="40" width="150" height="150" rx="20" fill="#f1f2f6" stroke="#333" stroke-width="4"/>')
                svg_elements.append('<path d="M 70 40 L 70 20 L 130 20 L 130 40 Z" fill="#bdc3c7" stroke="#333" stroke-width="3"/>')
                svg_elements.append('<path d="M 40 20 L 30 5 L 170 5 L 160 20 Z" fill="#ecf0f1" stroke="#333" stroke-width="3"/>')
                svg_elements.append(f'<circle cx="{cx}" cy="{cy}" r="{r_dial}" fill="#fff" stroke="#333" stroke-width="3"/>')
                for k in range(51):
                    tick_angle = -150 + k * 6; rad = math.radians(tick_angle - 90)
                    if k % 10 == 0: 
                        x1 = cx + (r_dial - 15) * math.cos(rad); y1 = cy + (r_dial - 15) * math.sin(rad)
                        x2 = cx + r_dial * math.cos(rad); y2 = cy + r_dial * math.sin(rad)
                        svg_elements.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#333" stroke-width="3"/>')
                        tx = cx + (r_dial - 25) * math.cos(rad); ty = cy + (r_dial - 25) * math.sin(rad) + 6
                        svg_elements.append(f'<text x="{tx}" y="{ty}" font-size="18" font-weight="bold" fill="#e74c3c" text-anchor="middle">{k//10}</text>')
                    elif k % 5 == 0: 
                        x1 = cx + (r_dial - 10) * math.cos(rad); y1 = cy + (r_dial - 10) * math.sin(rad)
                        x2 = cx + r_dial * math.cos(rad); y2 = cy + r_dial * math.sin(rad)
                        svg_elements.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#333" stroke-width="2"/>')
                    else: 
                        x1 = cx + (r_dial - 5) * math.cos(rad); y1 = cy + (r_dial - 5) * math.sin(rad)
                        x2 = cx + r_dial * math.cos(rad); y2 = cy + r_dial * math.sin(rad)
                        svg_elements.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#777" stroke-width="1.5"/>')
                needle_rad = math.radians(angle_deg - 90)
                nx_dash = cx + r_dial * math.cos(needle_rad); ny_dash = cy + r_dial * math.sin(needle_rad)
                svg_elements.append(f'<line x1="{cx}" y1="{cy}" x2="{nx_dash}" y2="{ny_dash}" stroke="#e74c3c" stroke-width="1.5" stroke-dasharray="3,3" opacity="0.7"/>')
                nx = cx + (r_dial - 15) * math.cos(needle_rad); ny = cy + (r_dial - 15) * math.sin(needle_rad)
                svg_elements.append(f'<line x1="{cx}" y1="{cy}" x2="{nx}" y2="{ny}" stroke="#e74c3c" stroke-width="4" stroke-linecap="round"/>')
                svg_elements.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="#333"/>')
                svg_content = "".join(svg_elements)
                scale_svg = f'<div style="text-align: center; margin: 15px 0;"><svg width="200" height="220" viewBox="0 0 200 220">{svg_content}</svg></div>'
                q = f"จากหน้าปัดเครื่องชั่งสปริง สินค้ามีน้ำหนักเท่าใด? {scale_svg}"
                ans_text = f"{kg} กิโลกรัม {khid} ขีด" if kg > 0 and khid > 0 else (f"{kg} กิโลกรัม" if khid == 0 else f"{khid} ขีด")
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> อ่านค่าจากเข็มหน้าปัด</span><br><b>{ans_text}</b>"

            elif "แผนภูมิรูปภาพ" in actual_sub_t:
                items = [("🍎 แอปเปิล", "🍎"), ("🍊 ส้ม", "🍊"), ("🍌 กล้วย", "🍌"), ("🍓 องุ่น", "🍓")]
                selected = random.sample(items, 3)
                multiplier = 1 if grade == "ป.1" else (random.choice([2, 5, 10]) if grade == "ป.2" else random.randint(2, 12))
                counts = [random.randint(1, 5), random.randint(1, 5), random.randint(1, 5)]
                table_html = f"""<div style='margin: 15px auto; width: 80%; border: 2px solid #333; border-collapse: collapse;'><div style='background-color: #f1f2f6; border-bottom: 2px solid #333; text-align: center; padding: 5px; font-weight: bold;'>จำนวนผลไม้ที่ร้านค้าขายได้</div>"""
                for i in range(3): table_html += f"<div style='display: flex; border-bottom: 1px solid #ccc;'><div style='width: 30%; border-right: 1px solid #ccc; padding: 5px; font-weight: bold;'>{selected[i][0]}</div><div style='width: 70%; padding: 5px; font-size: 18px;'>{''.join([selected[i][1]] * counts[i])}</div></div>"
                table_html += f"<div style='background-color: #fdfdfd; text-align: center; padding: 5px; font-weight: bold; color: #e74c3c;'>กำหนดให้ 1 รูปภาพ แทนผลไม้ {multiplier} ผล</div></div>"
                q = f"จากแผนภูมิ ขายผลไม้ 3 ชนิดรวมกันกี่ผล? {table_html}"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> รูปภาพทั้งหมด {sum(counts)} รูปภาพ × {multiplier} =</span> <b>{sum(counts) * multiplier} ผล</b>"

            elif "การนับทีละ" in actual_sub_t:
                step = 10 if "10" in actual_sub_t else (1 if "1" in actual_sub_t else random.choice([2, 5, 10, 100]))
                inc = random.choice([True, False]); max_val = limit - (3 * step); max_val = max_val if max_val > 1 else 10
                st_val = random.randint(1, max_val)
                seq = [st_val, st_val+step, st_val+2*step, st_val+3*step] if inc else [st_val+3*step, st_val+2*step, st_val+step, st_val]
                idx = random.randint(0, 3); ans_str = f"{seq[idx]:,}"
                seq_str = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;".join([f"{s:,}" if i != idx else "_____" for i, s in enumerate(seq)])
                q = f"จงเติมตัวเลขที่หายไปในแบบรูป : <span style='font-weight: bold; margin-left: 10px;'>{seq_str}</span>"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> แบบรูปมีการ{'เพิ่ม' if inc else 'ลด'}ทีละ {step}</span><br><b>{ans_str}</b>"

            elif "เรียงลำดับ" in actual_sub_t:
                nums = random.sample(range(10, limit), 4)
                is_asc = "น้อยไปมาก" in actual_sub_t if "น้อยไปมาก" in actual_sub_t else random.choice([True, False])
                num_str = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;".join([f"{x:,}" for x in nums])
                q = f"จงเรียงลำดับต่อไปนี้จาก {'น้อยไปมาก' if is_asc else 'มากไปน้อย'} : <span style='font-weight: bold; margin-left: 10px;'>{num_str}</span>"
                ans_str = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;".join([f"{x:,}" for x in sorted(nums, reverse=not is_asc)])
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>{ans_str}</b>"

            elif "เปรียบเทียบ" in actual_sub_t:
                a = random.randint(10, limit); is_eq = "=" in actual_sub_t
                b = a if is_eq and random.choice([True, False]) else random.randint(10, limit)
                while not is_eq and a == b: b = random.randint(10, limit)
                sign = "=" if a == b else ("≠" if is_eq else (">" if a > b else "<"))
                q = f"จงเติมเครื่องหมาย {'= หรือ ≠' if is_eq else '> หรือ <'} ลงในช่องว่าง: <span style='display:inline-flex; align-items:center; font-weight:bold; margin-left: 10px;'>{a:,} _____ {b:,}</span>"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>{sign}</b>"

            elif "รูปกระจาย" in actual_sub_t:
                n = random.randint(10, limit - 1 if limit > 10 else 99)
                parts = [f"{int(d)*(10**(len(str(n))-1-i)):,}" for i,d in enumerate(str(n)) if d != '0']
                q = f"จงเขียน <b>{n:,}</b> ในรูปกระจาย"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span><b>{' + '.join(parts)}</b>"
                
            elif "จำนวนคู่" in actual_sub_t:
                n = random.randint(10, limit)
                q = f"จำนวน <b>{n:,}</b> เป็นจำนวนคู่ หรือ จำนวนคี่?"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>{'จำนวนคู่' if n % 2 == 0 else 'จำนวนคี่'}</b>"

            elif "เขียนตัวเลข" in actual_sub_t:
                n = random.randint(11, limit-1) if grade in ["ป.1", "ป.2", "ป.3"] else random.randint(100000, 999999)
                if random.choice([True, False]):
                    q = f"จงเขียน <b>{n:,}</b> ให้เป็น<b>ตัวเลขไทย</b>"
                    sol = f"<b>{n:,}</b>".translate(str.maketrans('0123456789', '๐๑๒๓๔๕๖๗๘๙'))
                else:
                    q = f"จงเขียน <b>{n:,}</b> ให้เป็น<b>ตัวหนังสือ</b>"
                    sol = f"<b>{generate_thai_number_text(str(n))}</b>"

            elif "ค่าประมาณ" in actual_sub_t:
                n = random.randint(1111, 99999); ptype = random.choice(["เต็มสิบ", "เต็มร้อย", "เต็มพัน"])
                ans = ((n+5)//10)*10 if ptype=="เต็มสิบ" else (((n+50)//100)*100 if ptype=="เต็มร้อย" else ((n+500)//1000)*1000)
                q = f"จงหาค่าประมาณเป็นจำนวน<b>{ptype}</b> ของ {n:,}"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>{ans:,}</b>"

            elif "หารยาว" in actual_sub_t:
                divisor = random.randint(2, 12); quotient = random.randint(100, 999); dividend = divisor * quotient
                eq_html = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; margin-left: 10px; color: #2c3e50;'>{prefix} {dividend:,} ÷ {divisor} = {box_html}</span>"
                q = generate_long_division_step_by_step_html(divisor, dividend, eq_html, is_key=False)
                sol = generate_long_division_step_by_step_html(divisor, dividend, eq_html, is_key=True)

            elif "เศษเกินเป็นจำนวนคละ" in actual_sub_t:
                den = random.randint(3, 12); num = random.randint(den + 1, den * 5)
                while num % den == 0: num = random.randint(den + 1, den * 5)
                frac_html = generate_fraction_html(num, den); mixed_raw = generate_mixed_number_html(num//den, num%den, den)
                q = f"จงเขียนเศษเกินให้อยู่ในรูปจำนวนคละ : <span style='display:inline-flex; vertical-align: middle; margin-left: 10px;'>{frac_html}</span>"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span><br><br>{mixed_raw}"
                
            elif "อ่านและเขียนเศษส่วน" in actual_sub_t:
                den = random.randint(3, 8); num = random.randint(1, den - 1); frac_html = generate_fraction_html(num, den)
                rects = "".join([f'<rect x="{i*40}" y="0" width="40" height="30" fill="{"#3498db" if i < num else "#ffffff"}" stroke="#333" stroke-width="2"/>' for i in range(den)])
                svg_bar = f'<div style="display: inline-block; vertical-align: middle; margin-left: 15px;"><svg width="{den*40 + 4}" height="34"><g transform="translate(2,2)">{rects}</g></svg></div>'
                q = f"จงอ่านและเขียนเศษส่วนที่ระบายสี : {svg_bar}"
                sol = f"<div style='display: flex; align-items: center; margin-top: 10px;'><b>เขียน: </b> {frac_html} <span style='margin-left: 20px;'><b>อ่าน: </b> เศษ {num} ส่วน {den}</span></div>"

            elif "เศษส่วน" in actual_sub_t and ("บวก" in actual_sub_t or "ลบ" in actual_sub_t) and "ทศนิยม" not in actual_sub_t:
                den = random.randint(5, 15); num1, num2 = random.randint(1, den-1), random.randint(1, den-1)
                op = "+" if "บวก" in actual_sub_t and "ลบ" not in actual_sub_t else ("-" if "ลบ" in actual_sub_t and "บวก" not in actual_sub_t else random.choice(["+", "-"]))
                if op == "-" and num1 < num2: num1, num2 = num2, num1 
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; margin-left:5px;'>{prefix}{generate_fraction_html(num1, den)} <span style='margin: 0 8px; font-weight: bold;'>{op}</span> {generate_fraction_html(num2, den)} <span style='margin: 0 8px; font-weight: bold;'>= </span> {box_html}</span>"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <br><br> {generate_fraction_html(num1+num2 if op=='+' else num1-num2, den)}"

            elif "เศษส่วน" in actual_sub_t and ("คูณ" in actual_sub_t or "หาร" in actual_sub_t) and "เศษเกิน" not in actual_sub_t:
                n1, d1 = random.randint(1, 5), random.randint(2, 7); n2, d2 = random.randint(1, 5), random.randint(2, 7)
                op = "×" if "คูณ" in actual_sub_t else ("÷" if "หาร" in actual_sub_t else random.choice(["×", "÷"]))
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; margin-left:5px;'>{prefix}{generate_fraction_html(n1, d1)} <span style='margin: 0 8px; font-weight: bold;'>{op}</span> {generate_fraction_html(n2, d2)} <span style='margin: 0 8px; font-weight: bold;'>= </span> {box_html}</span>"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <br><br> {generate_fraction_html(n1*n2, d1*d2) if op=='×' else generate_fraction_html(n1*d2, d1*n2)}"

            elif "ทศนิยม" in actual_sub_t and "อ่าน" in actual_sub_t:
                n = round(random.uniform(0.1, 99.999), random.randint(1, 3))
                q = f"จงเขียน <b>{n}</b> เป็นตัวหนังสือ"
                sol = f"<b>{generate_thai_number_text(str(n))}</b>"

            elif "ทศนิยม" in actual_sub_t and ("บวก" in actual_sub_t or "ลบ" in actual_sub_t):
                a, b = round(random.uniform(10.0, 99.9), 2), round(random.uniform(1.0, 9.9), 2); op = random.choice(["+", "-"])
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:.2f} {op} {b:.2f} = {box_html}</span>"
                sol = generate_decimal_vertical_html(a, b, op, is_key=True)

            elif "คูณทศนิยม" in actual_sub_t:
                a, b = round(random.uniform(1.0, 12.0), 1), random.randint(2, 9)
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:.1f} × {b} = {box_html}</span>"
                sol = generate_vertical_table_html(int(round(a*10)), b, '×', result=int(round(a*10))*b, is_key=True) + f"<br><span style='color: #2c3e50;'>ตอบ:</span> <b>{round(a*b, 1):.1f}</b>"

            elif "ร้อยละ" in actual_sub_t and "เศษส่วน" in actual_sub_t:
                den = random.choice([2, 4, 5, 10, 20, 25, 50]); num = random.randint(1, den-1)
                q = f"จงเขียนให้อยู่ในรูปร้อยละ : <span style='display:inline-flex; vertical-align: middle; margin-left: 10px;'>{generate_fraction_html(num, den)}</span>"
                sol = f"<span style='color: #2c3e50;'>ตอบ: <b>ร้อยละ {int((num/den)*100)} หรือ {int((num/den)*100)}%</b></span>"

            elif "อัตราส่วนที่เท่ากัน" in actual_sub_t:
                a, b, m = random.randint(2, 9), random.randint(2, 9), random.randint(2, 9)
                while a == b: b = random.randint(2, 9)
                q = f"หาจำนวนใน {box_html} : <span style='display:inline-flex; align-items:center; color: #3498db; font-weight: bold; margin-left: 10px;'>{a}:{b} = {a*m}:{box_html}</span>" if random.choice([True, False]) else f"หาจำนวนใน {box_html} : <span style='display:inline-flex; align-items:center; color: #3498db; font-weight: bold; margin-left: 10px;'>{a}:{b} = {box_html}:{b*m}</span>"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span><b>{b*m if 'box' in q.split('=')[1].split(':')[1] else a*m}</b>"

            elif "โจทย์ปัญหาอัตราส่วน" in actual_sub_t:
                a, b, m = random.randint(2, 7), random.randint(2, 7), random.randint(5, 20)
                while a == b: b = random.randint(2, 7)
                q = f"อัตราส่วนของนักเรียนชายต่อนักเรียนหญิง คือ <b>{a} : {b}</b><br>ถ้ามีนักเรียนชาย <b>{a*m}</b> คน จะมีนักเรียนหญิงกี่คน?"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span><b>{b*m} คน</b>"

            elif "โจทย์ปัญหาร้อยละ" in actual_sub_t:
                price = random.choice([100, 200, 500, 1000]); percent = random.choice([10, 15, 20, 25])
                q = f"เสื้อราคา {price:,} บาท ลดราคา {percent}% ลดราคากี่บาท?<div style='margin-top: 10px; color: #2c3e50;'>{prefix} ...................................</div>"
                sol = f"<span style='color: #2c3e50;'><b>ประโยคสัญลักษณ์:</b> ({percent}÷100)×{price:,} = {box_html}</span><br><b>ตอบ: {int(price*(percent/100)):,} บาท</b>"

            elif "ห.ร.ม." in actual_sub_t:
                a, b = random.randint(12, 48), random.randint(12, 48)
                while a == b: b = random.randint(12, 48) 
                q, sol = f"จงหา ห.ร.ม. ของ <b>{a}</b> และ <b>{b}</b>", generate_short_division_html(a, b, mode="ห.ร.ม.")

            elif "ค.ร.น." in actual_sub_t:
                a, b = random.randint(4, 24), random.randint(4, 24)
                while a == b: b = random.randint(4, 24) 
                q, sol = f"จงหา ค.ร.น. ของ <b>{a}</b> และ <b>{b}</b>", generate_short_division_html(a, b, mode="ค.ร.น.")

            elif "การแก้สมการ" in actual_sub_t:
                if grade == "ป.4":
                    x, a = random.randint(5, 50), random.randint(1, 20)
                    q = f"แก้สมการ : <span style='color: #3498db; margin-left: 15px;'><b>x + {a} = {x+a}</b></span>"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> x = {x+a} - {a} <br><b>x = {x}</b></span>"
                elif grade == "ป.5":
                    a, x = random.randint(2, 12), random.randint(2, 20)
                    q = f"แก้สมการ : <span style='color: #3498db; margin-left: 15px;'><b>{a}x = {a*x}</b></span>"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> x = {a*x} ÷ {a} <br><b>x = {x}</b></span>"
                elif grade == "ป.6":
                    a, x, b = random.randint(2, 9), random.randint(2, 15), random.randint(1, 20)
                    q = f"แก้สมการ : <span style='color: #3498db; margin-left: 15px;'><b>{a}x + {b} = {a*x+b}</b></span>"
                    sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> {a}x = {a*x+b} - {b} <br>x = {a*x} ÷ {a} <br><b>x = {x}</b></span>"

            elif "ชนิดของมุม" in actual_sub_t:
                angle = random.choice([30, 45, 60, 90, 120, 135, 150, 180])
                q = f"มุมที่มีขนาด <b>{angle} องศา</b> เรียกว่ามุมชนิดใด?"
                ans = "มุมแหลม" if angle < 90 else ("มุมฉาก" if angle == 90 else ("มุมป้าน" if angle < 180 else "มุมตรง"))
                sol = f"<span style='color: #2c3e50;'><b>ตอบ:</b></span> <b>{ans}</b>"

            elif "ความยาวรอบรูป" in actual_sub_t or ("พื้นที่" in actual_sub_t and "สี่เหลี่ยม" in actual_sub_t):
                s = random.randint(5, 30)
                q = f"จงหา{'ความยาวรอบรูป' if 'รอบรูป' in actual_sub_t else 'พื้นที่'}ของ<b>สี่เหลี่ยมจัตุรัส</b>ที่ยาวด้านละ {s} ซม."
                sol = f"<span style='color: #2c3e50;'><b>ตอบ:</b></span> <b>{4*s if 'รอบรูป' in actual_sub_t else s*s} {'ซม.' if 'รอบรูป' in actual_sub_t else 'ตร.ซม.'}</b>"

            elif "ไม้โปรแทรกเตอร์" in actual_sub_t:
                angle = random.randint(15, 165)
                q = f"สมมติไม้โปรแทรกเตอร์ชี้ที่สเกล <b>{angle}</b> องศา มุมนี้มีขนาดเท่าใด?"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ:</b></span> <b>{angle} องศา</b>"

            else:
                a, b = random.randint(10, 50), random.randint(10, 50)
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a} + {b} = {box_html}</span>"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: {a + b}</b></span>"

            if q not in seen:
                seen.add(q); questions.append({"question": q, "solution": sol}); break
            attempts += 1
    return questions

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
            if ("(แบบตั้งหลัก)" in sub_t and "สมการ" not in sub_t) or "หารยาว" in sub_t: html += f'{item["solution"]}'
            else: html += f'{item["question"]}<br><div class="sol-text">{item["solution"]}</div>'
        else:
            html += f'{item["question"]}<div class="workspace">พื้นที่แสดงวิธีทำ / ทดเลข...</div><div class="ans-line">ตอบ: </div>'
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

st.sidebar.markdown("## ⚙️ พารามิเตอร์การสร้าง")
worksheet_mode = st.sidebar.radio("🎯 เลือกหมวดหมู่โจทย์:", ["📚 หลักสูตรปกติ (ป.1 - ป.6)", "🏆 ข้อสอบแข่งขันระดับชาติ (TMC)"])
st.sidebar.markdown("---")

if worksheet_mode == "📚 หลักสูตรปกติ (ป.1 - ป.6)":
    selected_grade = st.sidebar.selectbox("📚 เลือกระดับชั้น:", ["ป.1", "ป.2", "ป.3", "ป.4", "ป.5", "ป.6"])
    main_topics_list = list(curriculum_db[selected_grade].keys())
    if "🌟 โจทย์แข่งขัน (แนว TMC)" in main_topics_list: main_topics_list.remove("🌟 โจทย์แข่งขัน (แนว TMC)") 
    main_topics_list.append("🌟 โหมดพิเศษ (สุ่มทุกเรื่อง)")
    selected_main = st.sidebar.selectbox("📂 เลือกหัวข้อหลัก:", main_topics_list)
    if selected_main == "🌟 โหมดพิเศษ (สุ่มทุกเรื่อง)":
        selected_sub = "แบบทดสอบรวมปลายภาค"
        st.sidebar.info("💡 โหมดนี้จะสุ่มดึงโจทย์จากทุกเรื่องในชั้นเรียนนี้มายำรวมกัน")
    else:
        selected_sub = st.sidebar.selectbox("📝 เลือกหัวข้อย่อย:", curriculum_db[selected_grade][selected_main])
else:
    selected_grade = st.sidebar.selectbox("🏆 เลือกระดับชั้นแข่งขัน:", ["ป.2"]) 
    selected_main = "ข้อสอบแข่งขันระดับชาติ"
    selected_sub = st.sidebar.selectbox("📝 เลือกแนวข้อสอบ (20 แนวจัดเต็ม!):", curriculum_db["ป.2"]["🌟 โจทย์แข่งขัน (แนว TMC)"] + ["🌟 สุ่มรวมทุกแนว"])
    if selected_sub == "🌟 สุ่มรวมทุกแนว":
        st.sidebar.info("💡 สุ่มโจทย์ทั้ง 20 แนว พร้อมสุ่มตัวละคร/สถานที่แบบไม่ซ้ำ!")

num_input = st.sidebar.number_input("🔢 จำนวนข้อ:", min_value=1, max_value=100, value=10)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📏 ตั้งค่าหน้ากระดาษ (อัปเดตใหม่)")
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
theme_map = {
    "ฟ้าคลาสสิก (Blue)": {"border": "#3498db", "badge": "#e74c3c"},
    "ชมพูพาสเทล (Pink)": {"border": "#ff9ff3", "badge": "#0abde3"},
    "เขียวธรรมชาติ (Green)": {"border": "#2ecc71", "badge": "#e67e22"},
    "ม่วงสร้างสรรค์ (Purple)": {"border": "#9b59b6", "badge": "#f1c40f"},
    "ส้มสดใส (Orange)": {"border": "#f39c12", "badge": "#2c3e50"}
}

if st.sidebar.button("🚀 สั่งสร้างใบงานเดี๋ยวนี้", type="primary", use_container_width=True):
    with st.spinner("กำลังประมวลผล..."):
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
    st.success(f"✅ สร้างไฟล์สำเร็จ! (ลองปรับความสูงกล่องทดเลขให้กว้างพิเศษดูได้ครับ)")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📄 โหลดเฉพาะโจทย์", data=st.session_state['worksheet_html'], file_name=f"{st.session_state['filename_base']}_Worksheet.html", mime="text/html", use_container_width=True)
        st.download_button("🔑 โหลดเฉพาะเฉลย", data=st.session_state['answerkey_html'], file_name=f"{st.session_state['filename_base']}_AnswerKey.html", mime="text/html", use_container_width=True)
    with c2:
        st.download_button("📚 โหลดรวมเล่ม E-Book", data=st.session_state['ebook_html'], file_name=f"{st.session_state['filename_base']}_Full_EBook.html", mime="text/html", use_container_width=True)
        st.download_button("🗂️ โหลดแพ็กเกจทั้งหมด (.zip)", data=st.session_state['zip_data'], file_name=f"{st.session_state['filename_base']}.zip", mime="application/zip", use_container_width=True)
    st.markdown("---")
    components.html(st.session_state['ebook_html'], height=800, scrolling=True)
