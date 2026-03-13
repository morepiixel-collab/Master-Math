import streamlit as st
import streamlit.components.v1 as components
import random
import math
import zipfile
import io
import time
import base64

# ==========================================
# ⚙️ ตรวจสอบไลบรารี pdfkit
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
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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
    <p>ระบบสร้างสื่อการสอนคณิตศาสตร์ (ป.1 - ป.6) ปรับปรุงพื้นที่ทดเลขและ Branding</p>
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

# (ลอจิกการสร้างโจทย์และกราฟิกทั้งหมดอยู่ครบถ้วน)
def generate_vertical_table_html(a, b, op, result=None, is_key=False):
    num_len = max(len(str(a)), len(str(b)), len(str(result)) if result else 0) + 1
    str_a = str(a).rjust(num_len, " "); str_b = str(b).rjust(num_len, " "); strike = [False] * num_len; top_marks = [""] * num_len
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
            b_val, carry = b, 0; a_digits = [int(c) if c.strip() else 0 for c in str_a]
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
        str_r = str(result).rjust(num_len, " "); res_tds = "".join([f'<td style="width: 35px; text-align: center; color: red; font-weight: bold; height: 45px; vertical-align: bottom;">{str_r[i].strip()}</td>' for i in range(num_len)])
    else: res_tds = "".join([f'<td style="width: 35px; height: 45px;"></td>' for _ in range(num_len)])
    return f"""<div style="display: inline-block; font-family: 'Sarabun', sans-serif; font-size: 38px; line-height: 1.1; margin: 10px 20px;"><table style="border-collapse: collapse; margin-left: auto; margin-right: auto;"><tr><td style="width: 20px;"></td>{a_tds}<td style="width: 50px; text-align: center; vertical-align: middle;" rowspan="2">{op}</td></tr><tr><td></td>{b_tds}</tr><tr><td></td>{res_tds}<td></td></tr><tr><td></td><td colspan="{num_len}" style="border-bottom: 6px double #000; height: 10px;"></td><td></td></tr></table></div>"""

def generate_fraction_html(num, den):
    return f"""<div style="display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; margin: 0 8px; font-family: 'Sarabun', sans-serif;"><span style="font-size: 26px; font-weight: bold; border-bottom: 3px solid #000; padding: 0 5px; line-height: 1.1;">{num}</span><span style="font-size: 26px; font-weight: bold; padding: 0 5px; line-height: 1.1;">{den}</span></div>"""

def get_fraction_solution_steps(num, den):
    g = math.gcd(num, den)
    if num == 0: return "", "<span style='font-size: 32px; font-weight: bold; color: red;'>0</span>"
    if num == den: return "", "<span style='font-size: 32px; font-weight: bold; color: red;'>1</span>"
    sn, sd = num // g, den // g; es, fh = "", ""
    if sd == 1:
        fh = f"<span style='font-size: 32px; font-weight: bold; color: red;'>{sn}</span>"
        if g > 1: es = f"ทอนเป็นเศษส่วนอย่างต่ำโดยใช้แม่ {g} หารเศษและส่วน จะได้เป็นจำนวนเต็ม"
    elif sn > sd:
        w, r = sn // sd, sn % sd; fh = f"<div style=\"display: inline-flex; align-items: center; vertical-align: middle; margin: 0 8px; font-family: 'Sarabun', sans-serif;\"><span style=\"font-size: 32px; font-weight: bold; margin-right: 5px; color: red;\">{w}</span><div style=\"display: inline-flex; flex-direction: column; align-items: center;\"><span style=\"font-size: 26px; font-weight: bold; border-bottom: 3px solid red; padding: 0 5px; line-height: 1.1; color: red;\">{r}</span><span style=\"font-size: 26px; font-weight: bold; padding: 0 5px; line-height: 1.1; color: red;\">{sd}</span></div></div>"
        if g > 1: es = f"ทอนเป็นเศษส่วนอย่างต่ำ (ใช้แม่ {g} หาร) และทำให้อยู่ในรูปจำนวนคละ"
        else: es = "แปลงเศษเกินให้อยู่ในรูปจำนวนคละ"
    else:
        fh = f"""<div style="display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; margin: 0 8px; font-family: 'Sarabun', sans-serif;"><span style="font-size: 26px; font-weight: bold; border-bottom: 3px solid red; padding: 0 5px; line-height: 1.1; color: red;">{sn}</span><span style="font-size: 26px; font-weight: bold; padding: 0 5px; line-height: 1.1; color: red;">{sd}</span></div>"""
        if g > 1: es = f"ทอนเป็นเศษส่วนอย่างต่ำโดยใช้แม่ {g} หารทั้งเศษและส่วน"
    return es, fh

def generate_short_division_html(a, b, mode="ห.ร.ม."):
    factors = []; ca, cb = a, b; steps_html = ""
    while True:
        found = False
        for i in range(2, min(ca, cb) + 1):
            if ca % i == 0 and cb % i == 0:
                steps_html += f"<tr><td style='text-align: right; padding-right: 10px; font-weight: bold; color: red;'>{i}</td><td style='border-left: 2px solid #000; border-bottom: 2px solid #000; padding: 5px 15px; text-align: center;'>{ca}</td><td style='border-bottom: 2px solid #000; padding: 5px 15px; text-align: center;'>{cb}</td></tr>"
                factors.append(i); ca //= i; cb //= i; found = True; break
        if not found: break
    if not factors: return f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ไม่มีตัวประกอบร่วมที่หารลงตัวทั้งคู่</span><br><b>{mode} = 1</b>" if mode=="ห.ร.ม." else f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ไม่มีตัวประกอบร่วม</span><br><b>ค.ร.น. = {a} × {b} = {a*b}</b>"
    steps_html += f"<tr><td></td><td style='padding: 5px 15px; text-align: center;'>{ca}</td><td style='padding: 5px 15px; text-align: center;'>{cb}</td></tr>"; table = f"<table style='margin: 10px 0; font-size: 24px; border-collapse: collapse; color: #333;'>{steps_html}</table>"
    if mode == "ห.ร.ม.":
        ans = math.prod(factors); sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ (หารสั้น):</b></span>{table}<span style='color: #2c3e50;'><b>ห.ร.ม.</b> คือนำตัวหารด้านหน้ามาคูณกัน:</span><br>= {' × '.join(map(str, factors))}<br>= <b>{ans}</b>"
    else:
        ans = math.prod(factors) * ca * cb; sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ (หารสั้น):</b></span>{table}<span style='color: #2c3e50;'><b>ค.ร.น.</b> คือนำตัวหารและผลลัพธ์บรรทัดสุดท้ายมาคูณกัน (รูปตัว L):</span><br>= {' × '.join(map(str, factors + [ca, cb]))}<br>= <b>{ans}</b>"
    return sol

def generate_decimal_vertical_html(a, b, op, is_key=False):
    str_a, str_b = f"{a:.2f}", f"{b:.2f}"; ans = a + b if op == '+' else round(a - b, 2); str_ans = f"{ans:.2f}"
    max_len = max(len(str_a), len(str_b), len(str_ans)) + 1; str_a = str_a.rjust(max_len, " "); str_b = str_b.rjust(max_len, " "); str_ans = str_ans.rjust(max_len, " ")
    strike = [False] * max_len; top_marks = [""] * max_len
    if is_key:
        if op == '+':
            carry = 0
            for i in range(max_len - 1, -1, -1):
                if str_a[i] == '.': continue
                da = int(str_a[i]) if str_a[i].strip() else 0; db = int(str_b[i]) if str_b[i].strip() else 0
                s = da + db + carry; carry = s // 10
                if carry > 0 and i > 0:
                    ni = i - 1
                    if str_a[ni] == '.': ni -= 1
                    if ni >= 0: top_marks[ni] = str(carry)
        elif op == '-':
            a_chars, b_chars = list(str_a), list(str_b); a_digits = [int(c) if c.strip() and c != '.' else 0 for c in a_chars]; b_digits = [int(c) if c.strip() and c != '.' else 0 for c in b_chars]
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
        val = str_a[i].strip() if str_a[i].strip() else ""; td_content = val if str_a[i] != '.' else "."
        if val and str_a[i] != '.':
            mark = top_marks[i]
            if strike[i] and is_key: td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span style="text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;">{val}</span></div>'
            elif mark and is_key: td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span>{val}</span></div>'
        a_tds += f"<td style='width: 35px; text-align: center; height: 50px; vertical-align: bottom;'>{td_content}</td>"
    b_tds = "".join([f"<td style='width: 35px; text-align: center; border-bottom: 2px solid #000; height: 40px; vertical-align: bottom;'>{c.strip() if c.strip() else ('.' if c=='.' else '')}</td>" for c in str_b])
    if is_key: ans_tds = "".join([f"<td style='width: 35px; text-align: center; color: red; font-weight: bold; height: 45px; vertical-align: bottom;'>{c.strip() if c.strip() else ('.' if c=='.' else '')}</td>" for c in str_ans])
    else: ans_tds = "".join([f"<td style='width: 35px; height: 45px;'></td>" for _ in str_ans])
    return f"""<div style="display: inline-block; font-family: 'Sarabun', sans-serif; font-size: 38px; line-height: 1.2; margin: 10px 20px;"><table style="border-collapse: collapse; margin-left: auto; margin-right: auto;"><tr><td style="width: 20px;"></td>{a_tds}<td style="width: 50px; text-align: center; vertical-align: middle;" rowspan="2">{op}</td></tr><tr><td></td>{b_tds}</tr><tr><td></td>{ans_tds}<td></td></tr><tr><td></td><td colspan="{max_len}" style="border-bottom: 6px double #000; height: 10px;"></td><td></td></tr></table></div>"""

def generate_long_division_step_by_step_html(divisor, dividend, is_key=False):
    div_str = str(dividend); div_len = len(div_str)
    equation_html = f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 15px; color: #2c3e50;'>ประโยคสัญลักษณ์: {dividend:,} ÷ {divisor} = {box_html}</div>"
    if not is_key:
        div_tds_list = []
        for i, c in enumerate(div_str):
            lb = "border-left: 3px solid #000;" if i == 0 else ""
            div_tds_list.append(f'<td style="width: 35px; text-align: center; border-top: 3px solid #000; {lb} font-size: 38px;">{c}</td>')
        div_tds_list.append('<td style="width: 35px;"></td>')
        return f"{equation_html}<div style=\"display: inline-block; font-family: 'Sarabun', sans-serif; line-height: 1.2; margin: 10px 20px;\"><table style=\"border-collapse: collapse;\"><tr><td style=\"border: none; text-align: right; padding-right: 12px; vertical-align: bottom; font-size: 38px;\">{divisor}</td>{''.join(div_tds_list)}</tr></table></div><br>{'<br>' * 12}"
    steps = []; cvs = ""; ans_str = ""; started = False
    for i, digit in enumerate(div_str):
        cvs += digit; cv = int(cvs); q = cv // divisor; mr = q * divisor; rem = cv - mr
        if not started and q == 0 and i < len(div_str) - 1:
             cvs = str(rem) if rem != 0 else ""; continue
        started = True; ans_str += str(q); cur_chars, m_chars = list(str(cv)), list(str(mr).zfill(len(list(str(cv))))); cd, md = [int(c) for c in cur_chars], [int(c) for c in m_chars]; tm, st = [""] * len(cd), [False] * len(cd)
        for idx_b in range(len(cd) - 1, -1, -1):
            if cd[idx_b] < md[idx_b]:
                for j in range(idx_b-1, -1, -1):
                    if cd[j] > 0:
                        st[j] = True; cd[j] -= 1; tm[j] = str(cd[j])
                        for k in range(j+1, idx_b): st[k] = True; cd[k] = 9; tm[k] = "9"
                        st[idx_b] = True; cd[idx_b] += 10; tm[idx_b] = str(cd[idx_b]); break
        steps.append({'mul_res': mr, 'rem': rem, 'col_index': i, 'top_m': tm, 'strik': st}); cvs = str(rem) if rem != 0 else ""
    ans_padded = ans_str.rjust(div_len, " "); ans_tds = "".join([f'<td style="width: 35px; text-align: center; color: red; font-weight: bold; font-size: 38px;">{c.strip()}</td>' for c in ans_padded]) + '<td style="width: 35px;"></td>'
    div_tds_list = []; s0 = steps[0] if steps else None; s0s = s0['col_index'] + 1 - len(s0['top_m']) if s0 else 0
    for i, c in enumerate(div_str):
        lb = "border-left: 3px solid #000;" if i == 0 else ""; td_c = c
        if is_key and s0 and s0s <= i <= s0['col_index']:
            ti = i - s0s; mark, is_st = s0['top_m'][ti], s0['strik'][ti]
            if is_st: td_c = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span style="text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;">{c}</span></div>'
            elif mark: td_c = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span>{c}</span></div>'
        div_tds_list.append(f'<td style="width: 35px; height: 50px; vertical-align: bottom; text-align: center; border-top: 3px solid #000; {lb} font-size: 38px;">{td_c}</td>')
    div_tds_list.append('<td style="width: 35px;"></td>'); html = f"{equation_html}<div style=\"display: inline-block; font-family: 'Sarabun', sans-serif; line-height: 1.2; margin: 10px 20px;\"><table style=\"border-collapse: collapse;\"><tr><td style=\"border: none;\"></td>{ans_tds}</tr><tr><td style=\"border: none; text-align: right; padding-right: 12px; vertical-align: bottom; font-size: 38px;\">{divisor}</td>{''.join(div_tds_list)}</tr>"
    for idx, step in enumerate(steps):
        mrs = str(step['mul_res']); pl = step['col_index'] + 1 - len(mrs); mt = ""
        for i in range(div_len + 1):
            if i >= pl and i <= step['col_index']:
                di = i - pl; bb = "border-bottom: 2px solid #000;" if i <= step['col_index'] else ""
                mt += f'<td style="width: 35px; height: 50px; vertical-align: bottom; text-align: center; font-size: 38px; {bb}">{mrs[di]}</td>'
            elif i == step['col_index'] + 1: mt += '<td style="width: 35px; text-align: center; font-size: 38px; color: #333; position: relative; top: -24px;">-</td>'
            else: mt += '<td style="width: 35px;"></td>'
        html += f"<tr><td style='border: none;'></td>{mt}</tr>"; is_last = (idx == len(steps) - 1); next_s = steps[idx+1] if not is_last else None; nss = next_s['col_index'] + 1 - len(next_s['top_m']) if next_s else 0
        rem_s = str(step['rem']); next_d = div_str[step['col_index'] + 1] if not is_last else ""; ds = rem_s if rem_s != "0" or is_last else ""
        if not is_last and ds == "": pass
        else: ds += next_d
        if ds == "": ds = next_d
        plr = step['col_index'] + 1 - len(ds) + (1 if not is_last else 0); rt = ""
        for i in range(div_len + 1):
            if i >= plr and i <= step['col_index'] + (1 if not is_last else 0):
                di = i - plr; char = ds[di]; td_c = char
                if is_key and next_s and nss <= i <= next_s['col_index']:
                    ti = i - nss; mark, is_st = next_s['top_m'][ti], next_s['strik'][ti]
                    if is_st: td_c = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span style="text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;">{char}</span></div>'
                    elif mark: td_c = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span>{char}</span></div>'
                bb2 = "border-bottom: 6px double #000;" if is_last else ""; rt += f'<td style="width: 35px; height: 50px; vertical-align: bottom; text-align: center; font-size: 38px; {bb2}">{td_c}</td>'
            else: rt += '<td style="width: 35px;"></td>'
        html += f"<tr><td style='border: none;'></td>{rt}</tr>"
    return html + "</table></div>"

def generate_questions_logic(grade, main_t, sub_t, num_q):
    questions = []; seen = set(); limit_map = {"ป.1": 100, "ป.2": 1000, "ป.3": 100000, "ป.4": 1000000, "ป.5": 9000000, "ป.6": 9000000}; limit = limit_map.get(grade, 100)
    for _ in range(num_q):
        q, sol = "", ""; attempts = 0
        while attempts < 300:
            act_sub = sub_t
            if sub_t == "แบบทดสอบรวมปลายภาค":
                all_m = [m for m in curriculum_db[grade].keys()]; rm = random.choice(all_m); act_sub = random.choice(curriculum_db[grade][rm])

            if act_sub == "การคูณ (แบบตั้งหลัก)":
                a = random.randint(10, 99) if grade in ["ป.1", "ป.2"] else (random.randint(100, 999) if grade == "ป.3" else random.randint(1000, 9999)); b = random.randint(2, 9); res = a * b; sentence = f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #2c3e50;'>ประโยคสัญลักษณ์: {a:,} × {b:,} = {box_html}</div>"
                q = sentence + generate_vertical_table_html(a, b, '×', is_key=False); sol = sentence + generate_vertical_table_html(a, b, '×', result=res, is_key=True)
            elif act_sub == "การบวก (แบบตั้งหลัก)":
                if grade == "ป.1": ta = random.randint(1, 9); ua = random.randint(0, 8); b = random.randint(1, 9 - ua); a = (ta * 10) + ua
                elif grade in ["ป.4", "ป.5", "ป.6"]: a = random.randint(10000, limit // 2); b = random.randint(10000, limit // 2)
                else: a = random.randint(10, limit - 20); b = random.randint(1, limit - a - 1)
                res = a + b; sentence = f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #2c3e50;'>ประโยคสัญลักษณ์: {a:,} + {b:,} = {box_html}</div>"; q = sentence + generate_vertical_table_html(a, b, '+', is_key=False); sol = sentence + generate_vertical_table_html(a, b, '+', result=res, is_key=True)
            elif act_sub == "การลบ (แบบตั้งหลัก)":
                if grade == "ป.1": ta = random.randint(1, 9); ua = random.randint(1, 9); b = random.randint(1, ua); a = (ta * 10) + ua
                elif grade in ["ป.4", "ป.5", "ป.6"]: a = random.randint(100000, limit - 1); b = random.randint(10000, a - 1)
                else: a = random.randint(10, limit - 1); b = random.randint(1, a - 1)
                res = a - b; sentence = f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #2c3e50;'>ประโยคสัญลักษณ์: {a:,} - {b:,} = {box_html}</div>"; q = sentence + generate_vertical_table_html(a, b, '-', is_key=False); sol = sentence + generate_vertical_table_html(a, b, '-', result=res, is_key=True)
            elif "การหารพื้นฐาน" in act_sub:
                a, b = random.randint(2, 9), random.randint(2, 12); dvd = a * b; q = f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #2c3e50;'>ประโยคสัญลักษณ์: {dvd} ÷ {a} = {box_html}</div>จงหาผลลัพธ์ของ <b>{dvd} ÷ {a}</b>"; sol = f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #2c3e50;'>ประโยคสัญลักษณ์: {dvd} ÷ {a} = {box_html}</div><br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ท่องสูตรคูณแม่ {a} จะพบว่า {a} × {b} = {dvd}<br>ดังนั้น {dvd} ÷ {a} = </span> <b>{b}</b>"
            elif "ส่วนย่อย-ส่วนรวม" in act_sub:
                total = random.randint(5, 20); p1 = random.randint(1, total - 1); p2 = total - p1; miss = random.choice(['t', 'p1', 'p2']); svg_t = f"""<br><div style="text-align: center;"><svg width="200" height="160"><line x1="100" y1="40" x2="50" y2="120" stroke="#333" stroke-width="3"/><line x1="100" y1="40" x2="150" y2="120" stroke="#333" stroke-width="3"/><circle cx="100" cy="40" r="30" fill="#e8f8f5" stroke="#16a085" stroke-width="3"/><circle cx="50" cy="120" r="30" fill="#fdf2e9" stroke="#d35400" stroke-width="3"/><circle cx="150" cy="120" r="30" fill="#fdf2e9" stroke="#d35400" stroke-width="3"/><text x="100" y="47" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='t' else "#16a085"}">{{t}}</text><text x="50" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='p1' else "#d35400"}">{{p1}}</text><text x="150" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='p2' else "#d35400"}">{{p2}}</text></svg></div>"""; q = f"จงหาตัวเลขที่หายไป (?) : " + svg_t.format(t="?" if miss=='t' else total, p1="?" if miss=='p1' else p1, p2="?" if miss=='p2' else p2); mm = {'t': 'ส่วนรวม (วงกลมบน)', 'p1': 'ส่วนย่อย (วงกลมซ้าย)', 'p2': 'ส่วนย่อย (วงกลมขวา)'}; cs = f"นำส่วนย่อยมาบวกกัน: {p1} + {p2} = <b>{total}</b>" if miss == 't' else (f"นำส่วนรวมลบด้วยส่วนย่อยที่มี: {total} - {p2} = <b>{p1}</b>" if miss == 'p1' else f"นำส่วนรวมลบด้วยส่วนย่อยที่มี: {total} - {p1} = <b>{p2}</b>"); sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> หา{mm[miss]}ที่หายไป โดย{cs}</span><br>" + svg_t.format(t=total, p1=p1, p2=p2)
            elif "การบอกอันดับที่" in act_sub:
                cmap = {"แดง": "#ff4d4d", "ฟ้า": "#3498db", "เขียว": "#2ecc71", "เหลือง": "#f1c40f", "ชมพู": "#ff9ff3"}; cols = list(cmap.keys()); random.shuffle(cols); xpos = [280, 220, 160, 100, 40]; cars = "".join([f'<g transform="translate({xpos[i]}, 40)"><path d="M 10 15 L 15 5 L 30 5 L 35 15 Z" fill="#e0e0e0" stroke="#333" stroke-width="1"/><rect x="0" y="15" width="50" height="15" rx="4" fill="{cmap[cols[i]]}" stroke="#333" stroke-width="1.5"/><circle cx="12" cy="30" r="6" fill="#333"/><circle cx="38" cy="30" r="6" fill="#333"/></g>' for i in range(5)]); svgd = f"""<br><div style="text-align: center;"><svg width="400" height="80"><line x1="20" y1="76" x2="380" y2="76" stroke="#95a5a6" stroke-width="4"/><rect x="350" y="30" width="10" height="46" fill="#fff" stroke="#333"/><text x="355" y="20" font-size="14" font-weight="bold" text-anchor="middle" fill="#e74c3c">เส้นชัย</text>{cars}</svg></div>"""; idx = random.randint(0, 4); name = cols[idx]; asvg = f'<svg width="60" height="30" style="vertical-align: middle; margin-left: 10px;"><path d="M 10 10 L 15 2 L 30 2 L 35 10 Z" fill="#e0e0e0" stroke="#333"/><rect y="10" width="50" height="12" rx="3" fill="{cmap[name]}" stroke="#333"/><circle cx="12" cy="22" r="5" fill="#333"/><circle cx="38" cy="22" r="5" fill="#333"/></svg>'; q = f"รถสี{name} วิ่งอยู่อันดับที่เท่าไร? {svgd}" if random.choice([True, False]) else f"รถที่วิ่งอยู่ในอันดับที่ {idx + 1} คือรถสีอะไร? {svgd}"; sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> นับจากเส้นชัยทางขวา จะพบว่ารถสี{name} อยู่</span> <b>อันดับที่ {idx+1}</b> {asvg}"
            elif "แบบรูปซ้ำ" in act_sub:
                sh = {"วงกลม": '<circle cx="15" cy="15" r="12" fill="#ffb3ba" stroke="#333" stroke-width="2"/>', "สี่เหลี่ยม": '<rect x="3" y="3" width="24" height="24" fill="#bae1ff" stroke="#333" stroke-width="2"/>', "สามเหลี่ยม": '<polygon points="15,3 27,27 3,27" fill="#baffc9" stroke="#333" stroke-width="2"/>', "ดาว": '<polygon points="15,1 19,10 29,10 21,16 24,26 15,20 6,26 9,16 1,10 11,10" fill="#ffffba" stroke="#333" stroke-width="2"/>'}; pt = random.choice([[0, 1], [0, 1, 2], [0, 0, 1], [0, 1, 1]]); keys = random.sample(list(sh.keys()), len(set(pt))); seq = [keys[pt[i % len(pt)]] for i in range(12)]; slen = random.randint(5, 8); h = "<br><div style='margin-top:10px; text-align:center;'>" + "".join([f'<svg width="30" height="30" style="vertical-align: middle; margin: 0 5px;">{sh[seq[i]]}</svg>' for i in range(slen)]) + '<span style="display:inline-block; width:30px; height:30px; border-bottom:2px dashed #000; margin: 0 5px;"></span></div>'; q = f"รูปที่หายไปคือรูปใด? {h}"; sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> สังเกตชุดรูปภาพที่เรียงซ้ำกัน รูปถัดไปคือ:</span><br><br><svg width='30' height='30' style='vertical-align: middle;'>{sh[seq[slen]]}</svg>"
            elif "นาฬิกา" in act_sub:
                h, m = random.randint(1, 12), random.randint(0, 59); cx, cy = 100, 100; se = [f'<circle cx="{cx}" cy="{cy}" r="75" fill="#fdfdfd" stroke="#333" stroke-width="3"/>'];
                for i in range(60):
                    ad = i * 6 - 90; ar = math.radians(ad)
                    if i % 5 == 0:
                        tx1 = cx + 65 * math.cos(ar); ty1 = cy + 65 * math.sin(ar); tx2 = cx + 75 * math.cos(ar); ty2 = cy + 75 * math.sin(ar); se.append(f'<line x1="{tx1}" y1="{ty1}" x2="{tx2}" y2="{ty2}" stroke="#333" stroke-width="3" />'); hour = i // 5 if i // 5 != 0 else 12; txh = cx + 50 * math.cos(ar); tyh = cy + 50 * math.sin(ar) + 6; se.append(f'<text x="{txh}" y="{tyh}" font-size="18" font-weight="bold" fill="#e74c3c" text-anchor="middle">{hour}</text>'); txm = cx + 88 * math.cos(ar); tym = cy + 88 * math.sin(ar) + 4; se.append(f'<text x="{txm}" y="{tym}" font-size="12" font-weight="bold" fill="#3498db" text-anchor="middle">{i}</text>')
                    else: tx1 = cx + 70 * math.cos(ar); ty1 = cy + 70 * math.sin(ar); tx2 = cx + 75 * math.cos(ar); ty2 = cy + 75 * math.sin(ar); se.append(f'<line x1="{tx1}" y1="{ty1}" x2="{tx2}" y2="{ty2}" stroke="#777" stroke-width="1.5" />')
                ah = (h % 12) * 30 + (m / 60) * 30; am = m * 6; se.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + 40 * math.cos(math.radians(ah-90))}" y2="{cy + 40 * math.sin(math.radians(ah-90))}" stroke="#e74c3c" stroke-width="5" stroke-linecap="round" />'); se.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + 65 * math.cos(math.radians(am-90))}" y2="{cy + 65 * math.sin(math.radians(am-90))}" stroke="#3498db" stroke-width="3" stroke-linecap="round" />'); se.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="#333"/>'); svg = f'<br><div style="text-align: center; margin: 15px 0;"><svg width="180" height="180" viewBox="0 0 200 200">{"".join(se)}</svg></div>'; day = random.choice(["เวลากลางวัน", "เวลากลางคืน"]); q = f"หากเป็น <b>{day}</b> จะอ่านเวลาได้กี่นาฬิกา กี่นาที? {svg}"; ah = h+12 if (day=="เวลากลางวัน" and 1<=h<=5) or (day=="เวลากลางคืน" and 6<=h<=11) else (0 if day=="เวลากลางคืน" and h==12 else h); sol = f"<br><b>ตอบ: {ah:02d}.{m:02d} น.</b>"
            elif "จำนวนเงิน" in act_sub:
                b100, b50, b20, c10, c5, c1 = [random.randint(0, n) for n in [3, 2, 4, 5, 3, 5]]; total = (b100*100) + (b50*50) + (b20*20) + (c10*10) + (c5*5) + (c1*1); msvg = "<br><div style='margin-top:10px; line-height: 2.5;'>" + ('<svg width="60" height="30" style="vertical-align: middle; margin: 2px;"><rect width="60" height="30" rx="3" fill="#ff7675" stroke="#c0392b" stroke-width="2"/><text x="30" y="20" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">100</text></svg>'*b100) + ('<svg width="60" height="30" style="vertical-align: middle; margin: 2px;"><rect width="60" height="30" rx="3" fill="#74b9ff" stroke="#2980b9" stroke-width="2"/><text x="30" y="20" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">50</text></svg>'*b50) + ('<svg width="60" height="30" style="vertical-align: middle; margin: 2px;"><rect width="60" height="30" rx="3" fill="#55efc4" stroke="#27ae60" stroke-width="2"/><text x="30" y="20" font-size="12" font-weight="bold" fill="#333" text-anchor="middle">20</text></svg>'*b20) + "</div>"; q = f"จากภาพ มีเงินทั้งหมดกี่บาท? {msvg}"; sol = f"<br><b>ตอบ: {total:,} บาท</b>"
            elif "เครื่องชั่งสปริง" in act_sub:
                kg, kh = random.randint(0, 4), random.randint(1, 9); ad = -150 + (kg*10+kh)*6; cx, cy, rd = 100, 120, 70; se = ['<rect x="25" y="40" width="150" height="150" rx="20" fill="#f1f2f6" stroke="#333" stroke-width="4"/>','<circle cx="100" cy="120" r="70" fill="#fff" stroke="#333" stroke-width="3"/>'];
                for k in range(51):
                    ta = -150 + k*6; r = math.radians(ta-90); x2 = cx + rd*math.cos(r); y2 = cy + rd*math.sin(r)
                    if k%10==0: se.append(f'<line x1="{cx+(rd-15)*math.cos(r)}" y1="{cy+(rd-15)*math.sin(r)}" x2="{x2}" y2="{y2}" stroke="#333" stroke-width="3"/><text x="{cx+(rd-25)*math.cos(r)}" y="{cy+(rd-25)*math.sin(r)+6}" font-size="18" font-weight="bold" fill="#e74c3c" text-anchor="middle">{k//10}</text>')
                    else: se.append(f'<line x1="{cx+(rd-5)*math.cos(r)}" y1="{cy+(rd-5)*math.sin(r)}" x2="{x2}" y2="{y2}" stroke="#777" stroke-width="1.5"/>')
                nr = math.radians(ad-90); se.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+(rd-15)*math.cos(nr)}" y2="{cy+(rd-15)*math.sin(nr)}" stroke="#e74c3c" stroke-width="4" stroke-linecap="round"/>'); se.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="#333"/>'); ssvg = f'<br><div style="text-align: center; margin: 15px 0;"><svg width="200" height="220" viewBox="0 0 200 220">{"".join(se)}</svg></div>'; q = f"สินค้ามีน้ำหนักเท่าใด? {ssvg}"; sol = f"<b>ตอบ: {kg} กิโลกรัม {kh} ขีด</b>"
            elif "การนับทีละ" in act_sub:
                step = 10 if "10" in act_sub else (1 if "1" in act_sub else random.choice([2, 5, 10, 100])); inc = random.choice([True, False]); stv = random.randint(1, limit - (3*step)); seq = [stv, stv+step, stv+2*step, stv+3*step] if inc else [stv+3*step, stv+2*step, stv+step, stv]; idx = random.randint(0, 3); q = f"เติมเลขที่หายไป: {', '.join([f'{s:,}' if i != idx else '_____' for i, s in enumerate(seq)])}"; sol = f"<b>ตอบ: {seq[idx]:,}, {'เพิ่ม' if inc else 'ลด'}ทีละ {step}</b>"
            elif "เรียงลำดับ" in act_sub:
                ns = random.sample(range(10, limit), 4); asc = "น้อยไปมาก" in act_sub; q = f"เรียงจาก{'น้อยไปมาก' if asc else 'มากไปน้อย'}: {', '.join(f'{x:,}' for x in ns)}"; sol = f"<b>ตอบ: {', '.join(f'{x:,}' for x in sorted(ns, reverse=not asc))}</b>"
            elif "เปรียบเทียบ" in act_sub:
                a, b = random.randint(10, limit), random.randint(10, limit); eq = "=" in act_sub; s = "=" if a==b else ("≠" if eq else (">" if a>b else "<")); q = f"เติม {'> < =' if not eq else '= ≠'}: {a:,} _____ {b:,}"; sol = f"<b>ตอบ: {s}</b>"
            elif "รูปกระจาย" in act_sub:
                n = random.randint(100, limit); ps = [f"{int(d)*(10**(len(str(n))-1-i)):,}" for i,d in enumerate(str(n)) if d!='0']; q = f"เขียน <b>{n:,}</b> ในรูปกระจาย"; sol = f"<b>ตอบ: {' + '.join(ps)}</b>"
            elif "เขียนตัวเลข" in act_sub:
                n = random.randint(11, limit-1); q = f"เขียน <b>{n:,}</b> เป็น{'ตัวหนังสือ' if attempts%2==0 else 'เลขไทย'}"; sol = f"<b>ตอบ: {generate_thai_number_text(str(n)) if attempts%2==0 else str(n).translate(str.maketrans('0123456789','๐๑๒๓๔๕๖๗๘๙'))}</b>"
            elif "ค่าประมาณ" in act_sub:
                n = random.randint(1111, 99999); p = random.choice(["เต็มสิบ", "เต็มร้อย", "เต็มพัน"]); v = 10 if p=="เต็มสิบ" else (100 if p=="เต็มร้อย" else 1000); ans = ((n + v//2) // v) * v; q = f"ค่าประมาณ<b>{p}</b> ของ {n:,}"; sol = f"<b>ตอบ: {ans:,}</b>"
            elif "หารยาว" in act_sub:
                ds, qn = random.randint(2, 12), random.randint(100, 999); dvd = ds * qn; q = generate_long_division_step_by_step_html(ds, dvd, False); sol = generate_long_division_step_by_step_html(ds, dvd, True)
            elif "เศษเกินเป็นจำนวนคละ" in act_sub:
                d = random.randint(3, 12); n = random.randint(d+1, d*5); q = f"เขียนเศษเกินให้อยู่ในรูปจำนวนคละ: <br>{generate_fraction_html(n, d)}"; w, r = n // d, n % d; sol = f"<b>ตอบ: {w} เศษ {r} ส่วน {d}</b>"
            elif "บวกลบเศษส่วน" in act_sub or "บวกและการลบเศษส่วน" in act_sub:
                if grade == "ป.5":
                    d1, d2 = random.randint(2, 10), random.randint(2, 10);
                    while d1==d2: d2 = random.randint(2,10)
                    n1, n2 = random.randint(1, d1-1), random.randint(1, d2-1); op = random.choice(["+", "-"])
                    if op=="-" and n1/d1 < n2/d2: n1,d1,n2,d2 = n2,d2,n1,d1
                    lcm = (d1*d2)//math.gcd(d1,d2); m1, m2 = lcm//d1, lcm//d2; ans_n = (n1*m1) + (n2*m2) if op=="+" else (n1*m1) - (n2*m2); f1, f2 = generate_fraction_html(n1, d1), generate_fraction_html(n2, d2); q = f"หาผลลัพธ์: {f1} {op} {f2} = {box_html}"; sol = f"<b>ตอบ: {generate_fraction_html(ans_n, lcm)}</b>"
                else:
                    den = random.randint(5, 15); n1, n2 = random.randint(1, den-1), random.randint(1, den-1); op = random.choice(["+", "-"])
                    if op=="-" and n1 < n2: n1, n2 = n2, n1
                    ans_n = n1+n2 if op=="+" else n1-n2; q = f"หาผลลัพธ์: {generate_fraction_html(n1, den)} {op} {generate_fraction_html(n2, den)} = {box_html}"; sol = f"<b>ตอบ: {generate_fraction_html(ans_n, den)}</b>"
            elif "คูณและการหารเศษส่วน" in act_sub:
                n1, d1, n2, d2 = random.randint(1, 5), random.randint(2, 7), random.randint(1, 5), random.randint(2, 7); op = random.choice(["×", "÷"]); q = f"หาผลลัพธ์: {generate_fraction_html(n1, d1)} {op} {generate_fraction_html(n2, d2)} = {box_html}"; ans_n, ans_d = (n1*n2, d1*d2) if op=="×" else (n1*d2, d1*n2); sol = f"<b>ตอบ: {generate_fraction_html(ans_n, ans_d)}</b>"
            elif "ทศนิยม" in act_sub and "บวก" in act_sub:
                a, b = round(random.uniform(10.0, 99.9), 2), round(random.uniform(1.0, 9.9), 2); q = f"หาผลลัพธ์: {a:.2f} + {b:.2f} = {box_html}"; sol = generate_decimal_vertical_html(a, b, '+', True)
            elif "คูณทศนิยม" in act_sub:
                a, b = round(random.uniform(1.0, 12.0), 1), random.randint(2, 9); q = f"หาผลลัพธ์: {a:.1f} × {b} = {box_html}"; sol = f"<b>ตอบ: {round(a*b, 1):.1f}</b>"
            elif "ร้อยละ" in act_sub:
                d = random.choice([2, 4, 5, 10, 20, 25, 50]); n = random.randint(1, d-1); q = f"เขียน {generate_fraction_html(n, d)} ในรูปร้อยละ"; sol = f"<b>ตอบ: ร้อยละ {int((n/d)*100)}</b>"
            elif "ห.ร.ม." in act_sub:
                a, b = random.randint(12, 48), random.randint(12, 48); q = f"หา ห.ร.ม. ของ {a} และ {b}"; sol = generate_short_division_html(a, b, "ห.ร.ม.")
            elif "ค.ร.น." in act_sub:
                a, b = random.randint(4, 24), random.randint(4, 24); q = f"หา ค.ร.น. ของ {a} และ {b}"; sol = generate_short_division_html(a, b, "ค.ร.น.")
            elif "อัตราส่วนที่เท่ากัน" in act_sub:
                a, b, m = random.randint(2, 9), random.randint(2, 9), random.randint(2, 9);
                while a==b: b=random.randint(2,9)
                c, d = a*m, b*m; q = f"หาเลขในช่องว่าง: {a} : {b} = {c} : {box_html}"; sol = f"<b>ตอบ: {d}</b>"
            elif "การแก้สมการ" in act_sub:
                a, x, b = random.randint(2, 9), random.randint(2, 15), random.randint(1, 20); c = a*x + b; q = f"แก้สมการเพื่อหาค่า x: {a}x + {b} = {c}"; sol = f"<b>ตอบ: x = {x}</b>"
            else:
                a, b = random.randint(10, 50), random.randint(10, 50); q = f"หาผลบวก: {a} + {b} = {box_html}"; sol = f"<b>ตอบ: {a+b}</b>"

            if q not in seen: seen.add(q); questions.append({"question": q, "solution": sol}); break
            attempts += 1
    return questions

# ==========================================
# 3. ฟังก์ชันช่วยสำหรับการเจนเพจ และ E-Book
# ==========================================
def extract_body(html_str):
    try: return html_str.split('<body>')[1].split('</body>')[0]
    except IndexError: return html_str

def create_page(grade, sub_t, questions, is_key=False, q_margin="60px", brand_name=""):
    title = "เฉลยแบบฝึกหัด" if is_key else "แบบฝึกหัดคณิตศาสตร์"
    student_info = ""
    if not is_key:
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
        """
    html = f"""<!DOCTYPE html><html lang="th"><head><meta charset="utf-8">
    <style>
        @page {{ size: A4; margin: 15mm; }}
        body {{ font-family: 'Sarabun', sans-serif; padding: 10px; line-height: 1.8; color: #333; }}
        .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 20px; padding-bottom: 10px; }}
        .q-box {{ margin-bottom: 20px; padding: 15px; page-break-inside: avoid; border-bottom: 1px solid #eee; display: flex; flex-direction: column; }}
        .spacing-box {{ height: {q_margin}; }} /* 💡 พื้นที่ทดเลขเปิดโล่งกลางข้อ */
        .ans-line {{ border-bottom: 1px dotted #999; width: 80%; height: 30px; margin-top: 10px; }}
        .sol-text {{ color: #333; font-size: 20px; display: inline-block; margin-top: 10px; line-height: 1.5; }}
        .page-footer {{ text-align: right; font-size: 14px; color: #95a5a6; margin-top: 30px; border-top: 1px solid #eee; padding-top: 10px; }}
    </style></head><body>
    <div class="header"><h2>{title} - {grade}</h2><p><b>เรื่อง:</b> {sub_t}</p></div>
    {student_info}"""
    for i, item in enumerate(questions, 1):
        html += f'<div class="q-box"><b>ข้อที่ {i}.</b> {item["question"]}'
        if is_key:
            html += f'<div class="sol-text">{item["solution"]}</div>'
        else:
            html += f'<div class="spacing-box"></div>' # 📏 พื้นที่ทดเลข (อยู่กลางข้อ)
            html += '<div class="ans-line">ตอบ: </div>' # ✍️ บรรทัดตอบ (อยู่ล่างข้อ)
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
        <div class="footer"><b>จัดทำโดย:</b> {brand_name}</div>
    </div>
    </body></html>"""

# ==========================================
# 4. Streamlit UI
# ==========================================
st.sidebar.markdown("## ⚙️ พารามิเตอร์การสร้าง")
selected_grade = st.sidebar.selectbox("📚 เลือกระดับชั้น:", list(curriculum_db.keys()))
main_topics_list = list(curriculum_db[selected_grade].keys()) + ["🌟 โหมดพิเศษ (สุ่มทุกเรื่อง)"]
selected_main = st.sidebar.selectbox("📂 เลือกหัวข้อหลัก:", main_topics_list)

if selected_main == "🌟 โหมดพิเศษ (สุ่มทุกเรื่อง)":
    selected_sub = "แบบทดสอบรวมปลายภาค"
    st.sidebar.info("💡 โหมดนี้จะสุ่มดึงโจทย์จากทุกเรื่องในชั้นเรียนนี้มายำรวมกัน")
else:
    selected_sub = st.sidebar.selectbox("📝 เลือกหัวข้อย่อย:", curriculum_db[selected_grade][selected_main])

num_input = st.sidebar.number_input("🔢 จำนวนข้อ:", min_value=1, max_value=100, value=10)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📏 ตั้งค่าหน้ากระดาษ")
spacing_level = st.sidebar.select_slider("↕️ ระยะห่างพื้นที่ทดเลข:", options=["แคบ", "ปานกลาง", "กว้าง"], value="ปานกลาง")
q_margin = {"แคบ": "50px", "ปานกลาง": "100px", "กว้าง": "200px"}[spacing_level]

st.sidebar.markdown("---")
brand_name = st.sidebar.text_input("🏷️ ชื่อแบรนด์ / ผู้สอน:", value="ครูคณิตศาสตร์")
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
    with st.spinner("กำลังประมวลผลลอจิกคณิตศาสตร์..."):
        qs = generate_questions_logic(selected_grade, selected_main, selected_sub, num_input)
        html_w = create_page(selected_grade, selected_sub, qs, False, q_margin, brand_name)
        html_k = create_page(selected_grade, selected_sub, qs, True, "20px", brand_name)
        html_cover = generate_cover_html(selected_grade, selected_main, selected_sub, num_input, theme_map[color_theme], brand_name) if include_cover else ""
        
        st.session_state['worksheet_html'] = html_w
        st.session_state['answerkey_html'] = html_k
        
        eb = ""
        if include_cover: eb += f'\n<div class="a4-wrapper cover-wrapper">{extract_body(html_cover)}</div>\n'
        eb += f'\n<div class="a4-wrapper">{extract_body(html_w)}</div>\n<div class="a4-wrapper">{extract_body(html_k)}</div>\n'
        
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
            .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 20px; padding-bottom: 10px; }}
            .q-box {{ margin-bottom: 15px; padding: 15px; page-break-inside: avoid; border-bottom: 1px solid #eee; display: flex; flex-direction: column; }}
            .spacing-box {{ height: {q_margin}; }}
            .ans-line {{ border-bottom: 1px dotted #999; width: 80%; height: 30px; margin-top: 10px; }}
            .sol-text {{ color: #333; font-size: 20px; display: inline-block; margin-top: 10px; line-height: 1.5; }}
            .page-footer {{ text-align: right; font-size: 14px; color: #95a5a6; margin-top: 30px; border-top: 1px solid #eee; padding-top: 10px; }}
            .cover-inner {{ width: 100%; height: 100%; padding: 40px; box-sizing: border-box; text-align: center; position: relative; border: 15px solid {theme_map[color_theme]['border']}; background: white; }}
            .title-box {{ margin-top: 80px; }} .title {{ font-size: 65px; color: #2c3e50; font-weight: bold; margin: 0; }}
            .grade-badge {{ font-size: 45px; background-color: {theme_map[color_theme]['badge']}; color: white; padding: 15px 50px; border-radius: 50px; display: inline-block; font-weight: bold; margin-top: 30px; }}
            .topic {{ font-size: 42px; color: #34495e; margin-top: 70px; font-weight: bold; }}
            .sub-topic {{ font-size: 32px; color: #7f8c8d; margin-top: 10px; }} .icons {{ font-size: 110px; margin: 60px 0; }}
            .details-badge {{ background-color: #2ecc71; color: white; display: inline-block; padding: 15px 40px; border-radius: 15px; font-size: 32px; font-weight: bold; }}
            .footer {{ position: absolute; bottom: 40px; left: 0; width: 100%; text-align: center; font-size: 22px; color: #7f8c8d; }}
        </style></head><body>{eb}</body></html>"""
        
        st.session_state['ebook_html'] = full_ebook_html
        st.session_state['filename_base'] = f"{selected_grade}_{selected_sub}_{int(time.time())}"
        zb = io.BytesIO()
        with zipfile.ZipFile(zb, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(f"{st.session_state['filename_base']}_EBook.html", full_ebook_html.encode('utf-8'))
            zf.writestr(f"{st.session_state['filename_base']}_Worksheet.html", html_w.encode('utf-8'))
            zf.writestr(f"{st.session_state['filename_base']}_AnswerKey.html", html_k.encode('utf-8'))
        st.session_state['zip_data'] = zb.getvalue()

if 'ebook_html' in st.session_state:
    st.success(f"✅ สร้างไฟล์สำเร็จ!")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📄 โหลดเฉพาะโจทย์", data=st.session_state['worksheet_html'], file_name=f"{st.session_state['filename_base']}_Worksheet.html", mime="text/html", use_container_width=True)
        st.download_button("🔑 โหลดเฉพาะเฉลย", data=st.session_state['answerkey_html'], file_name=f"{st.session_state['filename_base']}_AnswerKey.html", mime="text/html", use_container_width=True)
    with c2:
        st.download_button("📚 โหลดรวมเล่ม E-Book", data=st.session_state['ebook_html'], file_name=f"{st.session_state['filename_base']}_EBook.html", mime="text/html", use_container_width=True)
        st.download_button("🗂️ โหลดแพ็กเกจ (.zip)", data=st.session_state['zip_data'], file_name=f"{st.session_state['filename_base']}.zip", mime="application/zip", use_container_width=True)
    st.markdown("---")
    st.markdown("### 👁️ Live Preview")
    components.html(st.session_state['ebook_html'], height=800, scrolling=True)
else:
    st.info("👈 กรุณาเลือกตั้งค่าใบงานที่แถบเมนูด้านซ้าย แล้วกดปุ่ม สีเขียว 'สั่งสร้างใบงานเดี๋ยวนี้'")
