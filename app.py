import streamlit as st
import streamlit.components.v1 as components
import random
import math
import zipfile
import io
import time

try: import pdfkit; HAS_PDFKIT = True
except ImportError: HAS_PDFKIT = False

st.set_page_config(page_title="Math Generator Pro Ultimate", page_icon="🚀", layout="wide")
st.markdown("""<style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1200px; }
    div[data-testid="stSidebar"] div.stButton > button { background-color: #27ae60; color: white; border-radius: 8px; height: 3.5rem; font-size: 18px; font-weight: bold; transition: all 0.3s ease; border: none; box-shadow: 0 4px 6px rgba(39,174,96,0.3); }
    div[data-testid="stSidebar"] div.stButton > button:hover { background-color: #219653; box-shadow: 0 6px 12px rgba(39,174,96,0.4); transform: translateY(-2px); }
    div.stDownloadButton > button { border-radius: 8px; font-weight: bold; border: 1px solid #bdc3c7; transition: all 0.2s ease; }
    div.stDownloadButton > button:hover { border-color: #3498db; color: #3498db; }
    .main-header { background: linear-gradient(135deg, #2980b9, #2c3e50); padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem; box-shadow: 0 10px 20px rgba(0,0,0,0.15); }
    .main-header h1 { margin: 0; font-size: 2.8rem; font-weight: 800; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
    .main-header p { margin: 10px 0 0 0; font-size: 1.2rem; opacity: 0.9; }
</style>""", unsafe_allow_html=True)
st.markdown("""<div class="main-header"><h1>🚀 Math Worksheet Pro <span style="font-size: 20px; background: #f39c12; padding: 5px 15px; border-radius: 20px; vertical-align: middle;">Ultimate Edition</span></h1>
<p>ระบบสร้างสื่อการสอน ป.1-ป.6 + ข้อสอบแข่งขัน TMC (ทุกระดับชั้น) พร้อมภาพอธิบายเฉลย (Visual Models) ขั้นเทพ!</p></div>""", unsafe_allow_html=True)

# --- ฐานข้อมูลแข่งขันแยกตามช่วงชั้น ---
tmc_lower = ["ปริศนาตัวเลขซ่อนแอบ", "สัตว์ปีนบ่อ", "ตรรกะตาชั่งสมดุล", "ปัญหาผลรวม-ผลต่าง", "ตรรกะการจับมือ (ทักทาย)", "โปรโมชั่นแลกของ", "หยิบของในที่มืด", "คิววงกลมมรณะ"]
tmc_mid = ["ผลบวกจำนวนเรียงกัน (Gauss)", "พื้นที่แรเงา (เรขาคณิต)", "การตัดเชือกพับทบ", "แถวคอยแบบซ้อนทับ", "อายุข้ามเวลาขั้นสูง", "แผนภาพความชอบ (Venn)", "จำนวนขาและหัวสัตว์", "วันที่และปฏิทิน"]
tmc_upper = ["ความเร็ววิ่งสวนทาง", "งานและเวลา (Work)", "ระฆังและไฟกะพริบ (ค.ร.น.)", "อัตราส่วนอายุ", "เศษส่วนของที่เหลือ", "เส้นทางที่เป็นไปได้", "จัดของใส่กล่อง (Modulo)", "นาฬิกาเดินเพี้ยน"]

curriculum_db = {
    "ป.1": {
        "จำนวนนับ 1 ถึง 100 และ 0": ["การนับทีละ 1", "การนับทีละ 10", "การอ่านและการเขียนตัวเลข", "การแสดงจำนวนในรูปความสัมพันธ์แบบส่วนย่อย-ส่วนรวม", "แบบรูปซ้ำของรูปเรขาคณิต", "การบอกอันดับที่ (รถแข่ง)", "หลัก ค่าของเลขโดดในแต่ละหลัก และรูปกระจาย", "การเปรียบเทียบจำนวน (> <)",  "การเปรียบเทียบจำนวน (= ≠)", "การเรียงลำดับจำนวน (น้อยไปมาก)", "การเรียงลำดับจำนวน (มากไปน้อย)"],
        "การบวก การลบ": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)"], "แผนภูมิรูปภาพ": ["การอ่านแผนภูมิรูปภาพ"], "🌟 โจทย์แข่งขัน (แนว TMC)": tmc_lower
    },
    "ป.2": {
        "จำนวนนับไม่เกิน 1,000 และ 0": ["การนับทีละ 2 ทีละ 5 ทีละ 10 และทีละ 100", "การอ่านและการเขียนตัวเลข", "จำนวนคู่ จำนวนคี่", "หลัก ค่าของเลขโดด และรูปกระจาย", "การเปรียบเทียบจำนวน (> <)", "การเรียงลำดับจำนวน (น้อยไปมาก)", "การเรียงลำดับจำนวน (มากไปน้อย)"],
        "เวลาและการวัด": ["การบอกเวลาเป็นนาฬิกาและนาที", "การอ่านน้ำหนักจากเครื่องชั่งสปริง"], "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การคูณ (แบบตั้งหลัก)", "การหารพื้นฐาน"], "แผนภูมิรูปภาพ": ["การอ่านแผนภูมิรูปภาพ"], "🌟 โจทย์แข่งขัน (แนว TMC)": tmc_lower
    },
    "ป.3": {
        "จำนวนนับและเศษส่วน": ["การอ่าน การเขียนตัวเลข", "หลัก ค่าของเลขโดด และรูปกระจาย", "การเปรียบเทียบจำนวน (> <)", "การเรียงลำดับจำนวน (น้อยไปมาก)", "การเรียงลำดับจำนวน (มากไปน้อย)", "การอ่านและเขียนเศษส่วน", "การบวกลบเศษส่วน (ตัวส่วนเท่ากัน)"],
        "เวลา เงิน และการวัด": ["การบอกเวลาเป็นนาฬิกาและนาที", "การบอกจำนวนเงินทั้งหมด", "การอ่านน้ำหนักจากเครื่องชั่งสปริง"], "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การคูณ (แบบตั้งหลัก)", "การหารยาว"], "แผนภูมิรูปภาพ": ["การอ่านแผนภูมิรูปภาพ"], "🌟 โจทย์แข่งขัน (แนว TMC)": tmc_mid
    },
    "ป.4": {
        "จำนวนนับที่มากกว่า 100,000": ["การอ่านและการเขียนตัวเลข", "หลัก ค่าประจำหลัก และรูปกระจาย", "การเปรียบเทียบและเรียงลำดับ", "ค่าประมาณเป็นจำนวนเต็มสิบ เต็มร้อย เต็มพัน"],
        "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การคูณ (แบบตั้งหลัก)", "การหารยาว"], "เศษส่วนและทศนิยม": ["แปลงเศษเกินเป็นจำนวนคละ", "การอ่านและการเขียนทศนิยม"],
        "เรขาคณิตและการวัด": ["การบอกชนิดของมุม", "การวัดขนาดของมุม (ไม้โปรแทรกเตอร์)", "การหาความยาวรอบรูปสี่เหลี่ยมมุมฉาก", "การหาพื้นที่รูปสี่เหลี่ยมมุมฉาก"], "สมการ": ["การแก้สมการ (บวก/ลบ)"], "🌟 โจทย์แข่งขัน (แนว TMC)": tmc_mid
    },
    "ป.5": {
        "เศษส่วน": ["การบวกเศษส่วน", "การลบเศษส่วน", "การคูณเศษส่วน", "การหารเศษส่วน"], "ทศนิยม": ["การบวกและการลบทศนิยม", "การคูณทศนิยม"],
        "ร้อยละและเปอร์เซ็นต์": ["การเขียนเศษส่วนในรูปร้อยละ"], "สมการ": ["การแก้สมการ (คูณ/หาร)"], "🌟 โจทย์แข่งขัน (แนว TMC)": tmc_upper
    },
    "ป.6": {
        "ตัวประกอบของจำนวนนับ": ["การหา ห.ร.ม.", "การหา ค.ร.น."], "อัตราส่วนและร้อยละ": ["การหาอัตราส่วนที่เท่ากัน", "โจทย์ปัญหาอัตราส่วน", "โจทย์ปัญหาร้อยละ"],
        "สมการ": ["การแก้สมการ (สองขั้นตอน)"], "🌟 โจทย์แข่งขัน (แนว TMC)": tmc_upper
    }
}

box_html = "<span style='display: inline-block; width: 22px; height: 22px; border: 2px solid #333; border-radius: 3px; vertical-align: middle; margin-left: 5px; position: relative; top: -2px;'></span>"

def generate_vertical_table_html(a, b, op, result=None, is_key=False):
    num_len = max(len(str(a)), len(str(b)), len(str(result)) if result else 0) + 1
    str_a, str_b = str(a).rjust(num_len, " "), str(b).rjust(num_len, " ")
    strike, top_marks = [False] * num_len, [""] * num_len
    if is_key:
        if op == '+':
            carry = 0
            for i in range(num_len - 1, -1, -1):
                da, db = int(str_a[i]) if str_a[i].strip() else 0, int(str_b[i]) if str_b[i].strip() else 0
                s = da + db + carry; carry = s // 10
                if carry > 0 and i > 0: top_marks[i-1] = str(carry)
        elif op == '-':
            a_dig, b_dig = [int(c) if c.strip() else 0 for c in str_a], [int(c) if c.strip() else 0 for c in str_b]
            for i in range(num_len - 1, -1, -1):
                if a_dig[i] < b_dig[i]:
                    for j in range(i-1, -1, -1):
                        if a_dig[j] > 0 and str_a[j].strip() != "":
                            strike[j] = True; a_dig[j] -= 1; top_marks[j] = str(a_dig[j])
                            for k in range(j+1, i): strike[k] = True; a_dig[k] = 9; top_marks[k] = "9"
                            strike[i] = True; a_dig[i] += 10; top_marks[i] = str(a_dig[i]); break
        elif op == '×':
            b_val, carry, a_dig = b, 0, [int(c) if c.strip() else 0 for c in str_a]
            for i in range(num_len - 1, -1, -1):
                if str_a[i].strip() == "": 
                    if carry > 0: top_marks[i] = str(carry); carry = 0
                    continue
                prod = a_dig[i] * b_val + carry; carry = prod // 10
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
    res_tds = "".join([f'<td style="width: 35px; text-align: center; color: red; font-weight: bold; height: 45px; vertical-align: bottom;">{str(result).rjust(num_len, " ")[i].strip()}</td>' for i in range(num_len)]) if is_key and result is not None else "".join([f'<td style="width: 35px; height: 45px;"></td>' for _ in range(num_len)])
    return f"""<div style="display: block; text-align: center; margin-top: 10px;"><div style="display: inline-block; font-family: 'Sarabun', sans-serif; font-size: 38px; line-height: 1.1; margin: 10px 20px;"><table style="border-collapse: collapse; margin-left: auto; margin-right: auto;"><tr><td style="width: 20px;"></td>{a_tds}<td style="width: 50px; text-align: center; vertical-align: middle;" rowspan="2">{op}</td></tr><tr><td></td>{b_tds}</tr><tr><td></td>{res_tds}<td></td></tr><tr><td></td><td colspan="{num_len}" style="border-bottom: 6px double #000; height: 10px;"></td><td></td></tr></table></div></div>"""

def generate_fraction_html(num, den, color="#000"): return f"""<div style="display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; margin: 0 5px; font-family: 'Sarabun', sans-serif;"><span style="font-size: 20px; font-weight: bold; border-bottom: 2px solid {color}; padding: 0 4px; line-height: 1.1; color: {color};">{num}</span><span style="font-size: 20px; font-weight: bold; padding: 0 4px; line-height: 1.1; color: {color};">{den}</span></div>"""
def generate_mixed_number_html(whole, num, den): return f"""<div style="display: inline-flex; align-items: center; vertical-align: middle; margin: 0 5px; font-family: 'Sarabun', sans-serif;"><span style="font-size: 24px; font-weight: bold; margin-right: 4px; color: red;">{whole}</span><div style="display: inline-flex; flex-direction: column; align-items: center;"><span style="font-size: 20px; font-weight: bold; border-bottom: 2px solid red; padding: 0 4px; line-height: 1.1; color: red;">{num}</span><span style="font-size: 20px; font-weight: bold; padding: 0 4px; line-height: 1.1; color: red;">{den}</span></div></div>"""

def get_fraction_solution_steps(num, den):
    g = math.gcd(num, den)
    if num == 0: return "เป็น 0 เสมอ", "<span style='font-size: 24px; font-weight: bold; color: red;'>0</span>"
    if num == den: return "มีค่าเท่ากับ 1 เสมอ", "<span style='font-size: 24px; font-weight: bold; color: red;'>1</span>"
    sim_num, sim_den = num // g, den // g
    extra_steps, final_html = "", ""
    if sim_den == 1:
        final_html = f"<span style='font-size: 24px; font-weight: bold; color: red;'>{sim_num}</span>"
        if g > 1: extra_steps = f"ทอนเป็นเศษส่วนอย่างต่ำ (ใช้แม่ {g} หาร)"
    elif sim_num > sim_den:
        w, r = sim_num // sim_den, sim_num % sim_den
        final_html = generate_mixed_number_html(w, r, sim_den)
        if g > 1: extra_steps = f"ทอนอย่างต่ำ (แม่ {g}) และทำเป็นจำนวนคละ"
        else: extra_steps = f"แปลงเศษเกินเป็นจำนวนคละ"
    else:
        final_html = generate_fraction_html(sim_num, sim_den, "red")
        if g > 1: extra_steps = f"ทอนเป็นเศษส่วนอย่างต่ำ (ใช้แม่ {g} หาร)"
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
    if not factors: return f"<span style='color: #2c3e50;'>ไม่มีตัวประกอบร่วมที่หารลงตัว</span><br><b>{mode} = {1 if mode=='ห.ร.ม.' else a*b}</b>"
    steps_html += f"<tr><td></td><td style='padding: 5px 15px; text-align: center;'>{ca}</td><td style='padding: 5px 15px; text-align: center;'>{cb}</td></tr>"
    table = f"<table style='margin: 10px 0; font-size: 20px; border-collapse: collapse; color: #333;'>{steps_html}</table>"
    ans = math.prod(factors) if mode == "ห.ร.ม." else math.prod(factors) * ca * cb
    calc_str = " × ".join(map(str, factors)) if mode == "ห.ร.ม." else " × ".join(map(str, factors + [ca, cb]))
    return f"<span style='color: #2c3e50;'><b>วิธีทำ (หารสั้น):</b></span>{table}<span style='color: #2c3e50;'><b>{mode}</b> = {calc_str} = <b>{ans}</b></span>"

def generate_decimal_vertical_html(a, b, op, is_key=False):
    str_a, str_b = f"{a:.2f}", f"{b:.2f}"
    ans = a + b if op == '+' else round(a - b, 2); str_ans = f"{ans:.2f}"
    max_len = max(len(str_a), len(str_b), len(str_ans)) + 1 
    str_a, str_b, str_ans = str_a.rjust(max_len, " "), str_b.rjust(max_len, " "), str_ans.rjust(max_len, " ")
    strike, top_marks = [False] * max_len, [""] * max_len
    if is_key:
        if op == '+':
            carry = 0
            for i in range(max_len - 1, -1, -1):
                if str_a[i] == '.': continue
                s = (int(str_a[i]) if str_a[i].strip() else 0) + (int(str_b[i]) if str_b[i].strip() else 0) + carry
                carry = s // 10
                if carry > 0 and i > 0:
                    ni = i - 1 if str_a[i-1] != '.' else i - 2
                    if ni >= 0: top_marks[ni] = str(carry)
        elif op == '-':
            a_dig = [int(c) if c.strip() and c != '.' else 0 for c in str_a]
            b_dig = [int(c) if c.strip() and c != '.' else 0 for c in str_b]
            for i in range(max_len - 1, -1, -1):
                if str_a[i] == '.': continue
                if a_dig[i] < b_dig[i]:
                    for j in range(i-1, -1, -1):
                        if str_a[j] == '.': continue
                        if a_dig[j] > 0 and str_a[j].strip() != "":
                            strike[j] = True; a_dig[j] -= 1; top_marks[j] = str(a_dig[j])
                            for k in range(j+1, i):
                                if str_a[k] == '.': continue
                                strike[k] = True; a_dig[k] = 9; top_marks[k] = "9"
                            strike[i] = True; a_dig[i] += 10; top_marks[i] = str(a_dig[i]); break
    a_tds = ""
    for i in range(max_len):
        val = "." if str_a[i] == '.' else (str_a[i].strip() if str_a[i].strip() else "")
        td_content = val
        if val and val != '.':
            mark = top_marks[i]
            if strike[i] and is_key: td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span style="text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;">{val}</span></div>'
            elif mark and is_key: td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span>{val}</span></div>'
        a_tds += f"<td style='width: 35px; text-align: center; height: 50px; vertical-align: bottom;'>{td_content}</td>"
    b_tds = "".join([f"<td style='width: 35px; text-align: center; border-bottom: 2px solid #000; height: 40px; vertical-align: bottom;'>{c.strip() if c.strip() else ('.' if c=='.' else '')}</td>" for c in str_b])
    ans_tds = "".join([f"<td style='width: 35px; text-align: center; color: red; font-weight: bold; height: 45px; vertical-align: bottom;'>{c.strip() if c.strip() else ('.' if c=='.' else '')}</td>" for c in str_ans]) if is_key else "".join([f"<td style='width: 35px; height: 45px;'></td>" for _ in str_ans])
    return f"""<div style="display: block; text-align: center; margin-top: 10px;"><div style="display: inline-block; font-family: 'Sarabun', sans-serif; font-size: 38px; line-height: 1.2; margin: 10px 20px;"><table style="border-collapse: collapse; margin-left: auto; margin-right: auto;"><tr><td style="width: 20px;"></td>{a_tds}<td style="width: 50px; text-align: center; vertical-align: middle;" rowspan="2">{op}</td></tr><tr><td></td>{b_tds}</tr><tr><td></td>{ans_tds}<td></td></tr><tr><td></td><td colspan="{max_len}" style="border-bottom: 6px double #000; height: 10px;"></td><td></td></tr></table></div></div>"""

def generate_long_division_step_by_step_html(divisor, dividend, equation_html, is_key=False):
    div_str = str(dividend); div_len = len(div_str)
    if not is_key:
        ans_tds_list = [f'<td style="width: 35px; height: 45px;"></td>' for _ in div_str] + ['<td style="width: 35px;"></td>']
        div_tds_list = [f'<td style="width: 35px; text-align: center; border-top: 3px solid #000; {"border-left: 3px solid #000;" if i==0 else ""} font-size: 38px; height: 50px; vertical-align: bottom;">{c}</td>' for i, c in enumerate(div_str)] + ['<td style="width: 35px;"></td>']
        empty_rows = "".join([f"<tr><td style='border: none;'></td>{''.join([chr(60)+f'td style=\"width: 35px; height: 45px;\"'+chr(62)+chr(60)+'/td'+chr(62) for _ in range(div_len+1)])}</tr>" for _ in range(div_len+1)])
        return f"{equation_html}<div style=\"display: block; text-align: center; margin-top: 10px;\"><div style=\"display: inline-block; font-family: 'Sarabun', sans-serif; line-height: 1.2; margin: 10px 20px;\"><table style=\"border-collapse: collapse;\"><tr><td style=\"border: none;\"></td>{''.join(ans_tds_list)}</tr><tr><td style=\"border: none; text-align: right; padding-right: 12px; vertical-align: bottom; font-size: 38px;\">{divisor}</td>{''.join(div_tds_list)}</tr>{empty_rows}</table></div></div>"
    
    steps, current_val_str, ans_str, has_started = [], "", "", False
    for i, digit in enumerate(div_str):
        current_val_str += digit; current_val = int(current_val_str)
        q = current_val // divisor; mul_res = q * divisor; rem = current_val - mul_res
        if not has_started and q == 0 and i < len(div_str) - 1: current_val_str = str(rem) if rem != 0 else ""; continue
        has_started = True; ans_str += str(q)
        c_dig, m_dig = [int(c) for c in str(current_val)], [int(c) for c in str(mul_res).zfill(len(str(current_val)))]
        top_m, strik = [""] * len(c_dig), [False] * len(c_dig)
        for idx_b in range(len(c_dig) - 1, -1, -1):
            if c_dig[idx_b] < m_dig[idx_b]:
                for j in range(idx_b-1, -1, -1):
                    if c_dig[j] > 0:
                        strik[j] = True; c_dig[j] -= 1; top_m[j] = str(c_dig[j])
                        for k in range(j+1, idx_b): strik[k] = True; c_dig[k] = 9; top_m[k] = "9"
                        strik[idx_b] = True; c_dig[idx_b] += 10; top_m[idx_b] = str(c_dig[idx_b]); break
        steps.append({'mul_res': mul_res, 'rem': rem, 'col_index': i, 'top_m': top_m, 'strik': strik}); current_val_str = str(rem) if rem != 0 else ""
    
    ans_tds_list = [f'<td style="width: 35px; text-align: center; color: red; font-weight: bold; font-size: 38px;">{c.strip()}</td>' for c in ans_str.rjust(div_len, " ")] + ['<td style="width: 35px;"></td>']
    div_tds_list, s0 = [], steps[0] if len(steps) > 0 else None
    s0_start = s0['col_index'] + 1 - len(s0['top_m']) if s0 else 0
    for i, c in enumerate(div_str):
        td_content = c
        if is_key and s0 and s0_start <= i <= s0['col_index']:
            mark, is_strik = s0['top_m'][i-s0_start], s0['strik'][i-s0_start]
            if is_strik: td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span style="text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;">{c}</span></div>'
            elif mark: td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span>{c}</span></div>'
        div_tds_list.append(f'<td style="width: 35px; height: 50px; vertical-align: bottom; text-align: center; border-top: 3px solid #000; {"border-left: 3px solid #000;" if i==0 else ""} font-size: 38px;">{td_content}</td>')
    div_tds_list.append('<td style="width: 35px;"></td>') 
    
    html = f"{equation_html}<div style=\"display: block; text-align: center; margin-top: 10px;\"><div style=\"display: inline-block; font-family: 'Sarabun', sans-serif; line-height: 1.2; margin: 10px 20px;\"><table style=\"border-collapse: collapse;\"><tr><td style=\"border: none;\"></td>{''.join(ans_tds_list)}</tr><tr><td style=\"border: none; text-align: right; padding-right: 12px; vertical-align: bottom; font-size: 38px;\">{divisor}</td>{''.join(div_tds_list)}</tr>"
    for idx, step in enumerate(steps):
        mul_res_str = str(step['mul_res']); pad_len = step['col_index'] + 1 - len(mul_res_str)
        mul_tds = "".join([f'<td style="width: 35px; height: 50px; vertical-align: bottom; text-align: center; font-size: 38px; {"border-bottom: 2px solid #000;" if i <= step["col_index"] else ""}">{mul_res_str[i-pad_len]}</td>' if pad_len <= i <= step['col_index'] else ('<td style="width: 35px; text-align: center; font-size: 38px; color: #333; position: relative; top: -24px;">-</td>' if i == step['col_index'] + 1 else '<td style="width: 35px;"></td>') for i in range(div_len + 1)])
        html += f"<tr><td style='border: none;'></td>{mul_tds}</tr>"
        is_last = (idx == len(steps) - 1); next_step = steps[idx+1] if not is_last else None
        ns_start = next_step['col_index'] + 1 - len(next_step['top_m']) if next_step else 0
        rem_str = str(step['rem']); display_str = (rem_str if rem_str != "0" or is_last else "") + (div_str[step['col_index'] + 1] if not is_last else "")
        if display_str == "": display_str = div_str[step['col_index'] + 1] if not is_last else ""
        pad_len_rem = step['col_index'] + 1 - len(display_str) + (1 if not is_last else 0); rem_tds = ""
        for i in range(div_len + 1):
            if pad_len_rem <= i <= step['col_index'] + (1 if not is_last else 0):
                td_content = display_str[i - pad_len_rem]
                if is_key and next_step and ns_start <= i <= next_step['col_index']:
                    mark, is_strik = next_step['top_m'][i-ns_start], next_step['strik'][i-ns_start]
                    if is_strik: td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span style="text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;">{td_content}</span></div>'
                    elif mark: td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span>{td_content}</span></div>'
                rem_tds += f'<td style="width: 35px; height: 50px; vertical-align: bottom; text-align: center; font-size: 38px; {"border-bottom: 6px double #000;" if is_last else ""}">{td_content}</td>'
            else: rem_tds += '<td style="width: 35px;"></td>'
        html += f"<tr><td style='border: none;'></td>{rem_tds}</tr>"
    return html + "</table></div></div>"

def generate_thai_number_text(num_str):
    thai_nums = ["ศูนย์", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
    positions = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]
    int_part, dec_part = (str(num_str).replace(",", "").split(".") + [""])[0:2]
    def read_int(s):
        if s == "0" or not s: return "ศูนย์"
        res, l = "", len(s)
        for i, d in enumerate(s):
            v, p = int(d), l - i - 1
            if v == 0: continue
            if p == 1 and v == 2: res += "ยี่สิบ"
            elif p == 1 and v == 1: res += "สิบ"
            elif p == 0 and v == 1 and l > 1: res += "เอ็ด"
            else: res += thai_nums[v] + positions[p]
        return res
    return read_int(int_part) + (("จุด" + "".join([thai_nums[int(d)] for d in dec_part])) if dec_part else "")

def get_prefix(grade): return "<b style='color: #2c3e50; margin-right: 5px;'>ประโยคสัญลักษณ์:</b>" if grade in ["ป.1", "ป.2", "ป.3"] else ""

def generate_questions_logic(grade, main_t, sub_t, num_q):
    questions, seen = [], set()
    limit = {"ป.1": 100, "ป.2": 1000, "ป.3": 100000, "ป.4": 1000000, "ป.5": 9000000, "ป.6": 9000000}.get(grade, 100)

    NAMES = ["อคิณ", "นาวิน", "ภูผา", "สายฟ้า", "เจ้านาย", "ข้าวหอม", "ใบบัว", "มะลิ", "น้ำใส", "ญาญ่า", "ปลื้ม", "พายุ", "ไออุ่น", "กะทิ", "เวลา", "ของขวัญ", "มังกร", "ฉลาม", "ปลาวาฬ", "มาคิน"]
    LOCS = ["โรงเรียน", "สวนสัตว์", "สวนสนุก", "ห้างสรรพสินค้า", "ห้องสมุด", "สวนสาธารณะ", "ร้านของเล่น", "ร้านเบเกอรี่", "ค่ายลูกเสือ", "พิพิธภัณฑ์"]
    ITEMS = ["ลูกแก้ว", "สติกเกอร์", "การ์ดโปเกมอน", "โมเดลรถ", "ตุ๊กตาหมี", "สมุดระบายสี", "ดินสอสี", "ลูกโป่ง", "ยางลบ", "ตัวต่อเลโก้", "หนังสือการ์ตูน", "ลูกบอล"]
    SNACKS = ["ช็อกโกแลต", "คุกกี้", "โดนัท", "เยลลี่", "ขนมปัง", "ไอศกรีม", "น้ำผลไม้", "นมเย็น", "ลูกอม", "เค้ก"]
    ANIMALS = ["แมงมุม", "มดแดง", "กบ", "จิ้งจก", "ตั๊กแตน", "เต่า"]

    for _ in range(num_q):
        q, sol, attempts = "", "", 0
        while attempts < 300:
            act_sub = random.choice(curriculum_db[grade][random.choice([m for m in curriculum_db[grade] if m != "🌟 โหมดพิเศษ (สุ่มทุกเรื่อง)"])]) if sub_t == "แบบทดสอบรวมปลายภาค" else (random.choice(comp_topics) if sub_t == "🌟 สุ่มรวมทุกแนว" else sub_t)
            prefix = get_prefix(grade)

            # ==================================
            # 🌟 20 สุดยอดแนวข้อสอบแข่งขัน (TMC)
            # ==================================
            if act_sub == "ปริศนาตัวเลขซ่อนแอบ":
                a = random.randint(1, 4); b = random.randint(a+2, 9); diff = b-a; k = diff*9; s_val = a+b
                q = f"กำหนด A และ B เป็นเลขโดดที่ต่างกัน โดย <b>AB + {k} = BA</b> และ <b>A + B = {s_val}</b> <br>จำนวนสองหลัก <b>AB</b> คือจำนวนใด?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b><br>จาก BA - AB = {k} จะได้ผลต่าง B - A = {k} ÷ 9 = <b>{diff}</b><br>และ A + B = <b>{s_val}</b><br>หาเลข 2 ตัวที่บวกกันได้ {s_val} ลบกันได้ {diff} -> B = ({s_val}+{diff})÷2 = <b>{b}</b>, A = {s_val}-{b} = <b>{a}</b><br>ตอบ: </span><b>{a}{b}</b>"
            elif act_sub == "การนับหน้าหนังสือ":
                p = random.randint(40, 150); itm = random.choice(ITEMS)
                ans = 9 + 180 + ((p-99)*3) if p>99 else 9 + ((p-9)*2)
                q = f"สมุดภาพ<b>{itm}</b> มีความหนา <b>{p}</b> หน้า ต้องพิมพ์ตัวเลขเพื่อบอกเลขหน้า 1 ถึง {p} จะต้องใช้ตัวเลขโดดทั้งหมดกี่ตัว?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> แบ่งนับตามหลัก<br>1-9 (1 หลัก) = 9 × 1 = <b>9 ตัว</b><br>10-99 (2 หลัก) = 90 × 2 = <b>180 ตัว</b><br>" + (f"100-{p} (3 หลัก) = {p-99} × 3 = <b>{(p-99)*3} ตัว</b><br>รวม: 9 + 180 + {(p-99)*3} = </span><b>{ans} ตัว</b>" if p>99 else f"รวม: 9 + {(p-9)*2} = </span><b>{ans} ตัว</b>")
            elif act_sub == "การปักเสาและปลูกต้นไม้":
                d = random.choice([2, 4, 5, 10, 15]); t = random.randint(12, 35); L = (t-1)*d
                q = f"ปลูกต้นไม้ทางเข้า<b>{random.choice(LOCS)}</b> ห่างกันต้นละ <b>{d}</b> ม. โดยปลูกที่หัวและท้ายถนนพอดี ถ้านับได้ <b>{t}</b> ต้น ถนนยาวกี่เมตร?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> ปลูกหัวท้าย -> จำนวนช่วง = ต้นไม้ - 1 = {t}-1 = <b>{t-1} ช่วง</b><br>ความยาวถนน = {t-1} × {d} = </span><b>{L} เมตร</b>"
            elif act_sub == "สัตว์ปีนบ่อ":
                u = random.randint(3,7); d = random.randint(1,u-1); h = random.randint(15,30); net = u-d; days = math.ceil((h-u)/net) + 1
                q = f"<b>{random.choice(ANIMALS)}</b>ตกบ่อลึก <b>{h}</b> ม. กลางวันปีนได้ <b>{u}</b> ม. กลางคืนลื่นลง <b>{d}</b> ม. ต้องใช้เวลาอย่างน้อยกี่วันจึงจะพ้นปากบ่อ?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> 1 วันปีนสุทธิ {u}-{d} = <b>{net} ม.</b><br><i>(วันสุดท้ายเมื่อพ้นบ่อจะไม่ลื่นลง)</i><br>ระยะก่อนวันสุดท้าย = {h}-{u} = <b>{h-u} ม.</b><br>เวลาช่วงแรก = {h-u} ÷ {net} = {math.ceil((h-u)/net)} วัน<br>รวมวันสุดท้าย = {math.ceil((h-u)/net)} + 1 = </span><b>{days} วัน</b>"
            elif act_sub == "ตรรกะตาชั่งสมดุล":
                i1, i2, i3 = random.choice([("รถคันใหญ่", "รถคันเล็ก", "ตุ๊กตา"), ("แตงโม", "สับปะรด", "มะละกอ")]); m1, m2 = random.randint(2,5), random.randint(2,5)
                q = f"ตาชั่งสมดุล:<br>- <b>{i1} 1 ชิ้น</b> หนักเท่ากับ <b>{i2} {m1} ชิ้น</b><br>- <b>{i2} 1 ชิ้น</b> หนักเท่ากับ <b>{i3} {m2} ชิ้น</b><br><b>{i1} 2 ชิ้น</b> จะหนักเท่ากับ <b>{i3}</b> กี่ชิ้น?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b></span><br><svg width='200' height='60'><line x1='100' y1='50' x2='100' y2='20' stroke='#333' stroke-width='3'/><line x1='40' y1='20' x2='160' y2='20' stroke='#333' stroke-width='3'/><text x='40' y='45' text-anchor='middle' fill='#3498db' font-weight='bold' font-size='12'>{i1}(1)</text><text x='160' y='45' text-anchor='middle' fill='#e74c3c' font-weight='bold' font-size='12'>{i2}({m1})</text></svg><br><span style='color: #2c3e50;'>{i1} 1 ชิ้น = {m1} × {m2} = <b>{m1*m2} {i3}</b><br>{i1} 2 ชิ้น = {m1*m2} × 2 = </span><b>{m1*m2*2} ชิ้น</b>"
            elif act_sub == "อายุข้ามเวลาขั้นสูง":
                n1, n2, n3 = random.sample(NAMES, 3); a = random.randint(6,10); b = a + random.randint(2,5); c = b - random.randint(1, b-2)
                p = random.randint(2,5); curr = a+b+c; past = curr - (3*p)
                q = f"ปัจจุบัน {n1}, {n2}, {n3} อายุรวมกัน <b>{curr}</b> ปี <br>เมื่อ <b>{p}</b> ปีที่แล้ว ทั้งสามคนอายุรวมกันกี่ปี? (ทุกคนเกิดแล้ว)"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> ย้อนเวลาไป {p} ปี <b>ทุกคน</b>จะอายุน้อยลงคนละ {p} ปี<br>อายุที่หักออกรวม = 3 × {p} = <b>{3*p} ปี</b><br>อดีตรวมกัน = {curr} - {3*p} = </span><b>{past} ปี</b>"
            elif act_sub == "การตัดเชือกพับทบ":
                f = random.randint(2,4); c = random.randint(2,5); ans = (2**f)*c + 1
                q = f"<b>{random.choice(NAMES)}</b>พับทบครึ่งริบบิ้น <b>{f}</b> ครั้ง แล้วตัด <b>{c}</b> รอยตัด <br>เมื่อคลี่ออกมาจะได้ริบบิ้นกี่เส้น?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> พับ {f} ครั้ง เกิดความหนา = 2^{f} = <b>{2**f} ชั้น</b><br>ตัด 1 รอย ได้เพิ่ม {2**f} เส้น -> ตัด {c} รอย ได้เพิ่ม = {2**f} × {c} = <b>{(2**f)*c} เส้น</b><br>บวกเส้นตั้งต้น 1 เส้น = {(2**f)*c} + 1 = </span><b>{ans} เส้น</b>"
            elif act_sub == "แถวคอยแบบซ้อนทับ":
                f, b = random.randint(10,20), random.randint(10,20); tot = f+b+random.randint(5,12); mid = tot-(f+b); n1, n2 = random.sample(NAMES, 2)
                q = f"แถวรอเข้า<b>{random.choice(LOCS)}</b> มี <b>{tot}</b> คน<br><b>{n1}</b> ยืนลำดับ <b>{f}</b> จากหัวแถว และ <b>{n2}</b> ยืนลำดับ <b>{b}</b> จากท้ายแถว <br>มีคนอยู่ระหว่าง <b>{n1}</b> กับ <b>{n2}</b> กี่คน? ({n1} ยืนหน้า {n2})"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> คนตรงกลาง = ทั้งหมด - (กลุ่มหน้า + กลุ่มหลัง)<br>= {tot} - ({f} + {b}) = </span><b>{mid} คน</b>"
            elif act_sub == "ปัญหาผลรวม-ผลต่าง":
                d = random.randint(5,20); s = random.randint(10,30); L = s+d; tot = L+s; n1, n2 = random.sample(NAMES, 2); itm = random.choice(ITEMS)
                q = f"<b>{n1}</b> และ <b>{n2}</b> มี<b>{itm}</b>รวม <b>{tot}</b> ชิ้น หาก <b>{n1}</b> มีมากกว่า <b>{n2}</b> อยู่ <b>{d}</b> ชิ้น <b>{n1}</b> มีกี่ชิ้น?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b></span><br><svg width='250' height='70'><rect x='50' y='10' width='80' height='15' fill='#3498db'/><rect x='50' y='35' width='80' height='15' fill='#e74c3c'/><rect x='130' y='35' width='40' height='15' fill='#f1c40f' stroke-dasharray='2'/><text x='150' y='47' font-size='10' font-weight='bold' text-anchor='middle'>+{d}</text><text x='40' y='22' font-size='12' text-anchor='end'>{n2}</text><text x='40' y='47' font-size='12' text-anchor='end'>{n1}</text></svg><br><span style='color: #2c3e50;'>หักส่วนเกิน: {tot} - {d} = <b>{tot-d}</b><br>แบ่งครึ่ง (ของ{n2}): {tot-d} ÷ 2 = <b>{s}</b><br>ของ{n1}: {s} + {d} = </span><b>{L} ชิ้น</b>"
            elif act_sub == "ตรรกะการจับมือ (ทักทาย)":
                n = random.randint(5,12); ans = n*(n-1)//2
                q = f"ที่<b>{random.choice(LOCS)}</b> มีเด็ก <b>{n}</b> คน หากทุกคนต้องเดินจับมือกันให้ครบทุกคน คนละ 1 ครั้ง จะเกิดการจับมือคี่ครั้ง?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> (จำนวนคน × จำนวนคนที่ต้องจับ) ÷ 2<br>= ({n} × {n-1}) ÷ 2 = </span><b>{ans} ครั้ง</b>"
            elif act_sub == "โปรโมชั่นแลกของ":
                ex = random.choice([3,4,5]); start = ex*random.randint(3,6); tot, emp = start, start
                while emp >= ex: nb = emp//ex; emp = nb+(emp%ex); tot += nb
                q = f"ซอง<b>{random.choice(SNACKS)}</b>เปล่า <b>{ex}</b> ซอง แลกฟรี 1 ชิ้น <br>ถ้าซื้อตอนแรก <b>{start}</b> ชิ้น จะได้กินรวมกี่ชิ้น?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> แลกไปเรื่อยๆ จนซองไม่พอ<br>ตอนแรกได้ {start} ชิ้น -> นำไปแลกได้รวม </span><b>{tot} ชิ้น</b>"
            elif act_sub == "หยิบของในที่มืด":
                c1, c2, c3 = random.randint(5,12), random.randint(5,12), random.randint(3,8)
                q = f"กล่องทึบมี<b>{random.choice(ITEMS)}</b> แดง <b>{c1}</b>, น้ำเงิน <b>{c2}</b>, เขียว <b>{c3}</b> ชิ้น <br>หลับตาหยิบ ต้องหยิบ<b>อย่างน้อยกี่ชิ้น</b> จึงจะการันตีว่าได้สีเขียว 1 ชิ้นชัวร์ๆ?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ (ดวงซวยสุด):</b> สมมติหยิบสีอื่นหมดก่อน<br>แดง {c1} + น้ำเงิน {c2} = {c1+c2} ชิ้น<br>ชิ้นต่อไป (บวก 1) เป็นเขียวแน่นอน = {c1+c2} + 1 = </span><b>{c1+c2+1} ชิ้น</b>"
            elif act_sub == "การคิดย้อนกลับ":
                sm = random.randint(100,300); sp = random.randint(20,80); rv = random.randint(50,150); fm = sm-sp+rv
                q = f"<b>{random.choice(NAMES)}</b>ซื้อของ <b>{sp}</b> บาท แม่ให้เพิ่ม <b>{rv}</b> บาท ทำให้มีเงิน <b>{fm}</b> บาท <br>ตอนแรกมีเงินกี่บาท?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> คิดย้อนกลับสลับเครื่องหมาย<br>{fm} (ปัจจุบัน) - {rv} (แม่ให้) + {sp} (ซื้อของ) = </span><b>{sm} บาท</b>"
            elif act_sub == "แผนภาพความชอบ":
                tot = random.randint(30,50); both = random.randint(5,12); oa, ob = random.randint(8,15), random.randint(8,15)
                la, lb = oa+both, ob+both; nei = tot-(oa+ob+both); n1, n2 = random.sample(SNACKS, 2)
                q = f"นักเรียน <b>{tot}</b> คน ชอบ<b>{n1}</b> <b>{la}</b> คน, ชอบ<b>{n2}</b> <b>{lb}</b> คน, ชอบทั้งคู่ <b>{both}</b> คน <br>มีกี่คนที่ไม่ชอบทั้งสองชนิด?"
                svg = f"<svg width='200' height='100'><circle cx='70' cy='50' r='40' fill='#3498db' opacity='0.5'/><circle cx='130' cy='50' r='40' fill='#e74c3c' opacity='0.5'/><text x='100' y='55' text-anchor='middle' font-weight='bold'>{both}</text><text x='50' y='55' text-anchor='middle' font-weight='bold'>{oa}</text><text x='150' y='55' text-anchor='middle' font-weight='bold'>{ob}</text></svg>"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b></span><br>{svg}<br><span style='color: #2c3e50;'>ในวงกลมรวมกัน = {oa}+{both}+{ob} = <b>{oa+both+ob} คน</b><br>ไม่ชอบเลย = {tot} - {oa+both+ob} = </span><b>{nei} คน</b>"
            elif act_sub == "คิววงกลมมรณะ":
                nh = random.randint(4,12); tot = nh*2; p1 = random.randint(1,nh); p2 = p1+nh; n1, n2 = random.sample(NAMES, 2)
                q = f"เด็กยืนเป็นวงกลม <b>{n1}</b> ยืนหมายเลข <b>{p1}</b> มองไปฝั่งตรงข้ามพบ <b>{n2}</b> ยืนหมายเลข <b>{p2}</b> <br>กลุ่มนี้มีกี่คน?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> ตรงข้ามกันคือครึ่งวงกลม<br>ครึ่งวงกลม = {p2} - {p1} = <b>{nh} คน</b><br>เต็มวงกลม = {nh} × 2 = </span><b>{tot} คน</b>"
            elif act_sub == "ลำดับแบบวนลูป":
                w = random.choice(["MATHEMATICS", "THAILAND", "ELEPHANT", "SUPERMAN"]); t = random.randint(30,80); r = t % len(w)
                ans = w[r-1] if r != 0 else w[-1]
                q = f"เขียน <b>{w}</b> เรียงกันไปเรื่อยๆ ตัวอักษรที่ <b>{t}</b> คืออะไร?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> 1 ชุดมี <b>{len(w)} ตัว</b><br>{t} ÷ {len(w)} = เศษ <b>{r}</b><br>เศษ {r} คือตัวที่ {r if r!=0 else len(w)} = </span><b>{ans}</b>"
            elif act_sub == "เส้นทางที่เป็นไปได้":
                p1, p2, p3 = random.randint(2,4), random.randint(2,4), random.randint(1,3)
                q = f"จาก A ไป B มีถนน <b>{p1}</b> สาย, B ไป C มี <b>{p2}</b> สาย, และทางลัด A ไป C มี <b>{p3}</b> สาย<br>มีเส้นทาง A ไป C รวมกี่แบบ?"
                svg = f"<svg width='200' height='50'><circle cx='20' cy='25' r='10' fill='#3498db'/><circle cx='100' cy='25' r='10' fill='#f1c40f'/><circle cx='180' cy='25' r='10' fill='#2ecc71'/><line x1='30' y1='25' x2='90' y2='25' stroke='#000'/><text x='60' y='20' font-size='10' text-anchor='middle'>{p1}</text><line x1='110' y1='25' x2='170' y2='25' stroke='#000'/><text x='140' y='20' font-size='10' text-anchor='middle'>{p2}</text><path d='M 20 15 Q 100 -15 180 15' fill='none' stroke='red' stroke-dasharray='3'/><text x='100' y='10' font-size='10' text-anchor='middle' fill='red'>{p3}</text></svg>"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b></span><br>{svg}<br><span style='color: #2c3e50;'>ผ่าน B: {p1} × {p2} = {p1*p2} ทาง<br>รวมทางลัด: {p1*p2} + {p3} = </span><b>{(p1*p2)+p3} แบบ</b>"
            elif act_sub == "นาฬิกาเดินเพี้ยน":
                fm = random.randint(2,5); sh = 8; ph = random.randint(3,6); eh = sh+ph; tf = fm*ph
                q = f"นาฬิกาเดินเร็ว <b>{fm} นาที/ชม.</b> <br>ตั้งตรงเป๊ะตอน <b>{sh}:00 น.</b> เวลาจริง <b>{eh}:00 น.</b> นาฬิกาบอกเวลาใด?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> ผ่านไป {ph} ชม.<br>เวลาที่เร็วขึ้น = {fm} × {ph} = <b>{tf} นาที</b><br>ตอบ: </span><b>{eh}:{tf:02d} น.</b>"
            elif act_sub == "จัดของใส่กล่อง":
                bc = random.randint(4,9); nb = random.randint(5,12); r = random.randint(1,bc-1); tot = (bc*nb)+r
                q = f"มี<b>{random.choice(ITEMS)}</b> <b>{tot}</b> ชิ้น จัดใส่กล่องละ <b>{bc}</b> ชิ้น <br>ได้กี่กล่อง เหลือเศษกี่ชิ้น?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> {tot} ÷ {bc} = </span><b>{nb} กล่อง เศษ {r} ชิ้น</b>"
            elif act_sub == "คะแนนยิงเป้า":
                s1, s2, s3 = random.choices([10, 5, 1], k=3)
                q = f"ปาเป้า 3 ครั้ง (มีเป้า 10, 5, 1 คะแนน) ได้คะแนน <b>{s1+s2+s3}</b> คะแนน <br>เข้าเป้าใดบ้าง?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> หาเลข 3 ตัวที่บวกกันได้ {s1+s2+s3} <br>ตอบ: </span><b>{sorted([s1,s2,s3], reverse=True)}</b>"
            
            # --- อัปเกรดความยากช่วงชั้น ป.3-ป.6 ---
            elif act_sub == "ผลบวกจำนวนเรียงกัน (Gauss)":
                n = random.choice([10, 20, 50, 100]); ans = (n*(n+1))//2
                q = f"จงหาผลบวกของ 1 + 2 + 3 + ... + {n}"
                svg = f"<svg width='250' height='60'><text x='10' y='50'>1</text><text x='40' y='50'>2</text><text x='125' y='50'>...</text><text x='190' y='50'>{n-1}</text><text x='220' y='50'>{n}</text><path d='M 15 40 Q 120 0 230 40' fill='none' stroke='#e74c3c' stroke-width='2'/><path d='M 45 40 Q 120 15 200 40' fill='none' stroke='#3498db' stroke-width='2'/><text x='125' y='15' text-anchor='middle' font-size='10' font-weight='bold' fill='#e74c3c'>{n+1}</text></svg>"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ (สูตรเกาส์จับคู่):</b></span><br>{svg}<br><span style='color: #2c3e50;'>จับคู่หัวท้ายได้ {n+1} จำนวน {n//2} คู่<br>= {n+1} × {n//2} = </span><b>{ans:,}</b>"
            elif act_sub == "พื้นที่แรเงา (เรขาคณิต)":
                out_w, out_h = random.randint(10,20), random.randint(10,20); in_s = random.randint(3, min(out_w, out_h)-2)
                q = f"สี่เหลี่ยมรูปใหญ่มีขนาด {out_w}×{out_h} ซม. ถูกเจาะช่องสี่เหลี่ยมจัตุรัสตรงกลางขนาด {in_s}×{in_s} ซม. <br>พื้นที่ส่วนที่เหลือคือกี่ ตร.ซม.?"
                svg = f"<svg width='150' height='100'><rect x='10' y='10' width='130' height='80' fill='#bdc3c7' stroke='#333'/><rect x='50' y='30' width='50' height='40' fill='#fff' stroke='#333'/></svg>"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b></span><br>{svg}<br><span style='color: #2c3e50;'>พื้นที่ใหญ่ = {out_w}×{out_h} = {out_w*out_h}<br>พื้นที่เล็ก = {in_s}×{in_s} = {in_s**2}<br>เหลือ = {out_w*out_h} - {in_s**2} = </span><b>{(out_w*out_h)-(in_s**2)} ตร.ซม.</b>"
            elif act_sub == "ความเร็ววิ่งสวนทาง":
                d = random.choice([100, 200, 300]); v1, v2 = random.randint(10,25), random.randint(10,25); t = d/(v1+v2)
                q = f"รถ A และ B อยู่ห่างกัน <b>{d} กม.</b> วิ่งเข้าหากัน รถ A วิ่ง <b>{v1} กม./ชม.</b> รถ B วิ่ง <b>{v2} กม./ชม.</b> <br>กี่ชั่วโมงรถถึงจะพบกัน?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> ความเร็วรวมที่เข้าหากัน = {v1}+{v2} = {v1+v2} กม./ชม.<br>เวลา = ระยะทาง ÷ ความเร็วรวม = {d} ÷ {v1+v2} = </span><b>{t:.1f} ชั่วโมง</b>"
            elif act_sub == "เศษส่วนของที่เหลือ":
                tot = random.choice([120, 240, 360]); n1, n2 = random.choice([(NAMES[0], ITEMS[0]), (NAMES[1], ITEMS[1])])
                q = f"{n1} มีเงิน {tot} บ. ซื้อขนมไป 1/2 ของเงินที่มี และซื้อ{n2} 1/3 <b>ของเงินที่เหลือ</b> <br>{n1} เหลือเงินกี่บาท?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> 1) ซื้อขนม 1/2 = {tot//2} บ. (เหลือ {tot//2} บ.)<br>2) ซื้อ{n2} 1/3 ของที่เหลือ = 1/3 × {tot//2} = {tot//6} บ.<br>เหลือเงิน = {tot//2} - {tot//6} = </span><b>{(tot//2)-(tot//6)} บาท</b>"
            elif act_sub == "งานและเวลา (Work)":
                w1, w2 = 3, 6; ans = (w1*w2)/(w1+w2)
                q = f"ทาสีบ้าน A ทำเสร็จใน {w1} วัน, B ทำเสร็จใน {w2} วัน ถ้าช่วยกันจะเสร็จในกี่วัน?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> สูตรช่วยกัน = (A×B)/(A+B) = ({w1}×{w2})/({w1}+{w2}) = 18/9 = </span><b>{ans:.0f} วัน</b>"
            elif act_sub == "ระฆังและไฟกะพริบ (ค.ร.น.)":
                l1, l2, l3 = 2, 3, 4; lcm = 12
                q = f"ไฟ 3 ดวงกะพริบทุกๆ {l1}, {l2}, {l3} วินาที ถ้ากะพริบพร้อมกันตอน 10:00 น. จะพร้อมกันอีกครั้งกี่วินาที?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> หา ค.ร.น. ของ {l1}, {l2}, {l3} = </span><b>{lcm} วินาที</b>"
            elif act_sub == "อัตราส่วนอายุ":
                a_now, b_now = 10, 30; f = 10; r1, r2 = (a_now+f)//10, (b_now+f)//10
                q = f"ปัจจุบัน ก อายุ {a_now} ข อายุ {b_now} อีก {f} ปี อัตราส่วนอายุ ก : ข คือเท่าใด?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> อีก {f} ปี ก = {a_now+f}, ข = {b_now+f} <br>ทอนอย่างต่ำ {a_now+f}:{b_now+f} = </span><b>{r1}:{r2}</b>"
            elif act_sub == "วันที่และปฏิทิน":
                d_th = ["จ.", "อ.", "พ.", "พฤ.", "ศ.", "ส.", "อา."]; s_d = random.randint(1,5); s_idx = random.randint(0,6)
                add = random.choice([14, 21, 28]); t_d = s_d + add; t_idx = (s_idx + (add%7)) % 7
                q = f"วันที่ {s_d} คือวัน{d_th[s_idx]} วันที่ {t_d} ของเดือนนี้คือวันอะไร?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> ห่างกัน {add} วัน หาร 7 เศษ {add%7} <br>ตรงกับวัน </span><b>{d_th[t_idx]}</b>"

            # ==============================
            # โหมดหลักสูตรปกติ (คงไว้ครบ 100%)
            # ==============================
            elif actual_sub_t == "การคูณ (แบบตั้งหลัก)":
                a = random.randint(10, 99) if grade in ["ป.1", "ป.2"] else (random.randint(100, 999) if grade == "ป.3" else random.randint(1000, 9999)) 
                b = random.randint(2, 9); res = a * b
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} × {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '×', is_key=False)
                sol = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} × {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '×', result=res, is_key=True)

            elif actual_sub_t == "การบวก (แบบตั้งหลัก)":
                a = random.randint(10, limit//2); b = random.randint(10, limit//2)
                res = a + b
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} + {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '+', is_key=False)
                sol = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} + {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '+', result=res, is_key=True)

            elif actual_sub_t == "การลบ (แบบตั้งหลัก)":
                a = random.randint(1000, limit-1); b = random.randint(100, a-1)
                res = a - b
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} - {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '-', is_key=False)
                sol = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} - {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '-', result=res, is_key=True)

            elif "การหารพื้นฐาน" in actual_sub_t:
                a, b = random.randint(2, 9), random.randint(2, 12); dividend = a * b
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {dividend} ÷ {a} = {box_html}</span>"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> ท่องสูตรคูณแม่ {a} จะพบว่า {a} × {b} = {dividend}<br>ตอบ: </span> <b>{b}</b>"

            elif "ส่วนย่อย-ส่วนรวม" in actual_sub_t:
                tot = random.randint(5, 20); p1 = random.randint(1, tot-1); p2 = tot-p1; miss = random.choice(['t', 'p1', 'p2'])
                svg_t = f"""<div style="display: block; text-align: center; margin-top: 10px;"><svg width="200" height="160"><line x1="100" y1="40" x2="50" y2="120" stroke="#333" stroke-width="3"/><line x1="100" y1="40" x2="150" y2="120" stroke="#333" stroke-width="3"/><circle cx="100" cy="40" r="30" fill="#e8f8f5" stroke="#16a085" stroke-width="3"/><circle cx="50" cy="120" r="30" fill="#fdf2e9" stroke="#d35400" stroke-width="3"/><circle cx="150" cy="120" r="30" fill="#fdf2e9" stroke="#d35400" stroke-width="3"/><text x="100" y="47" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='t' else "#16a085"}">{{t}}</text><text x="50" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='p1' else "#d35400"}">{{p1}}</text><text x="150" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='p2' else "#d35400"}">{{p2}}</text></svg></div>"""
                q = f"จงหาตัวเลขที่หายไป (?) : " + svg_t.format(t="?" if miss=='t' else tot, p1="?" if miss=='p1' else p1, p2="?" if miss=='p2' else p2)
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span><br>" + svg_t.format(t=tot, p1=p1, p2=p2)

            elif "การบอกอันดับที่" in actual_sub_t:
                c_map = {"แดง": "#ff4d4d", "ฟ้า": "#3498db", "เขียว": "#2ecc71", "เหลือง": "#f1c40f"}
                cols = list(c_map.keys()); random.shuffle(cols); idx = random.randint(0, 3); name = cols[idx]
                q = f"รถสี{name} วิ่งอยู่อันดับที่เท่าไร? (เรียงซ้ายไปขวา)"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>อันดับที่ {idx + 1}</b>"

            elif "แบบรูปซ้ำ" in actual_sub_t:
                shapes = ["🔴", "🟦", "⭐"]; pt = [0, 1, 2]; seq = [shapes[pt[i%3]] for i in range(7)]
                q = f"รูปที่หายไปคือรูปใด? {' '.join(seq)} ____"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>{shapes[pt[7%3]]}</b>"

            elif "นาฬิกา" in actual_sub_t:
                h, m = random.randint(1, 12), random.randint(0, 59)
                q = f"หากเข็มสั้นชี้เลข {h} เข็มยาวชี้ขีดที่ {m} จะอ่านเวลาได้เท่าใด? (กลางวัน)"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>{h+12 if 1<=h<=5 else h:02d}.{m:02d} น.</b>"

            elif "จำนวนเงิน" in actual_sub_t:
                b100, b50, c10 = random.randint(1,3), random.randint(0,2), random.randint(1,5)
                tot = b100*100 + b50*50 + c10*10
                q = f"มีแบงก์ร้อย {b100} ใบ แบงก์ห้าสิบ {b50} ใบ เหรียญสิบ {c10} เหรียญ รวมเป็นเงิน?"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>{tot} บาท</b>"

            elif "เครื่องชั่งสปริง" in actual_sub_t:
                kg, khid = random.randint(1,4), random.randint(1,9)
                q = f"เข็มชี้เลยเลข {kg} มา {khid} ขีดเล็ก สินค้าหนักเท่าใด?"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>{kg} กิโลกรัม {khid} ขีด</b>"

            elif "แผนภูมิรูปภาพ" in actual_sub_t:
                m = random.choice([2, 5, 10]); c = random.randint(3, 8)
                q = f"กำหนดให้ 1 รูปภาพแทนผลไม้ {m} ผล ถ้านับได้ {c} รูปภาพ จะมีผลไม้กี่ผล?"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>{c*m} ผล</b>"

            elif "การนับทีละ" in actual_sub_t:
                step = random.choice([2, 5, 10]); start = random.randint(10, 50)
                q = f"จงเติมตัวเลข: {start} &nbsp;&nbsp; {start+step} &nbsp;&nbsp; ____ &nbsp;&nbsp; {start+step*3}"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>{start+step*2}</b>"

            elif "เรียงลำดับ" in actual_sub_t:
                nums = random.sample(range(10, limit), 4)
                q = f"จงเรียงจากน้อยไปมาก : {', '.join([str(x) for x in nums])}"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>{', '.join([str(x) for x in sorted(nums)])}</b>"

            elif "เปรียบเทียบ" in actual_sub_t:
                a, b = random.randint(10, limit), random.randint(10, limit)
                q = f"เติม > หรือ < : {a:,} _____ {b:,}"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>{'>' if a>b else '<'}</b>"

            elif "รูปกระจาย" in actual_sub_t:
                n = random.randint(100, 999)
                q = f"เขียน <b>{n}</b> ในรูปกระจาย"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>{n//100*100} + {(n//10)%10*10} + {n%10}</b>"
                
            elif "จำนวนคู่" in actual_sub_t:
                n = random.randint(10, 99)
                q = f"<b>{n}</b> เป็นจำนวนคู่หรือคี่?"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>{'คู่' if n%2==0 else 'คี่'}</b>"

            elif "เขียนตัวเลข" in actual_sub_t:
                n = random.randint(100, 999)
                q = f"เขียน <b>{n}</b> เป็นตัวเลขไทย"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>{str(n).translate(str.maketrans('0123456789','๐๑๒๓๔๕๖๗๘๙'))}</b>"

            elif "ค่าประมาณ" in actual_sub_t:
                n = random.randint(111, 999)
                q = f"ค่าประมาณเต็มสิบของ {n} คือ?"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>{((n+5)//10)*10}</b>"

            elif "หารยาว" in actual_sub_t:
                divisor = random.randint(2, 9); quotient = random.randint(100, 999); dividend = divisor * quotient
                eq_html = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; margin-left: 10px; color: #2c3e50;'>{prefix} {dividend:,} ÷ {divisor} = {box_html}</span>"
                q = generate_long_division_step_by_step_html(divisor, dividend, eq_html, is_key=False)
                sol = generate_long_division_step_by_step_html(divisor, dividend, eq_html, is_key=True)

            elif "เศษเกินเป็นจำนวนคละ" in actual_sub_t:
                den = random.randint(3, 12); num = random.randint(den+1, den*5)
                while num%den==0: num = random.randint(den+1, den*5)
                q = f"เขียนเป็นจำนวนคละ : {generate_fraction_html(num, den)}"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span><br><br>{generate_mixed_number_html(num//den, num%den, den)}"
                
            elif "อ่านและเขียนเศษส่วน" in actual_sub_t:
                den = random.randint(3, 8); num = random.randint(1, den-1)
                q = f"ระบายสี {num} ช่อง จาก {den} ช่อง เขียนเป็นเศษส่วนได้เท่าใด?"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> {generate_fraction_html(num, den)}"

            elif "เศษส่วน" in actual_sub_t and ("บวก" in actual_sub_t or "ลบ" in actual_sub_t) and "ทศนิยม" not in actual_sub_t:
                den = random.randint(5, 15); num1, num2 = random.randint(1, den-1), random.randint(1, den-1)
                op = "+" if "บวก" in actual_sub_t else "-"
                if op == "-" and num1 < num2: num1, num2 = num2, num1 
                q = f"จงหาผลลัพธ์: {generate_fraction_html(num1, den)} {op} {generate_fraction_html(num2, den)}"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> {generate_fraction_html(num1+num2 if op=='+' else num1-num2, den)}"

            elif "ทศนิยม" in actual_sub_t and ("บวก" in actual_sub_t or "ลบ" in actual_sub_t):
                a, b = round(random.uniform(10.0, 99.9), 2), round(random.uniform(1.0, 9.9), 2); op = random.choice(["+", "-"])
                q = f"จงหาผลลัพธ์ {a:.2f} {op} {b:.2f} = ?"
                sol = generate_decimal_vertical_html(a, b, op, is_key=True)

            elif "คูณทศนิยม" in actual_sub_t:
                a, b = round(random.uniform(1.0, 12.0), 1), random.randint(2, 9)
                q = f"จงหาผลลัพธ์ {a:.1f} × {b} = ?"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>{round(a*b, 1):.1f}</b>"

            elif "ร้อยละ" in actual_sub_t and "เศษส่วน" in actual_sub_t:
                den = random.choice([2, 4, 5, 10, 20]); num = random.randint(1, den-1)
                q = f"เศษส่วน {num}/{den} คิดเป็นร้อยละเท่าใด?"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>{int((num/den)*100)}%</b>"

            elif "อัตราส่วนที่เท่ากัน" in actual_sub_t:
                a, b, m = random.randint(2, 9), random.randint(2, 9), random.randint(2, 9)
                q = f"หาจำนวนในช่องว่าง {a} : {b} = {a*m} : ___"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>{b*m}</b>"

            elif "โจทย์ปัญหาร้อยละ" in actual_sub_t:
                price = random.choice([100, 200, 500]); percent = random.choice([10, 20, 25])
                q = f"เสื้อราคา {price} บาท ลด {percent}% ลดกี่บาท?"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>{int(price*percent/100)} บาท</b>"

            elif "ห.ร.ม." in actual_sub_t:
                a, b = random.randint(12, 48), random.randint(12, 48)
                while a == b: b = random.randint(12, 48) 
                q, sol = f"จงหา ห.ร.ม. ของ <b>{a}</b> และ <b>{b}</b>", generate_short_division_html(a, b, mode="ห.ร.ม.")

            elif "การแก้สมการ" in actual_sub_t:
                x, a = random.randint(5, 50), random.randint(1, 20)
                q = f"แก้สมการ: x + {a} = {x+a}"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>x = {x}</b>"

            elif "ชนิดของมุม" in actual_sub_t:
                angle = random.choice([30, 90, 120])
                q = f"มุม <b>{angle} องศา</b> คือมุมชนิดใด?"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: </b></span> <b>{'มุมแหลม' if angle<90 else 'มุมฉาก' if angle==90 else 'มุมป้าน'}</b>"

            else:
                a, b = random.randint(10, 50), random.randint(10, 50)
                q = f"จงหาผลลัพธ์ {prefix} {a} + {b} = {box_html}"
                sol = f"<span style='color: #2c3e50;'><b>ตอบ: {a + b}</b></span>"

            if q not in seen: seen.add(q); questions.append({"question": q, "solution": sol}); break
            attempts += 1
    return questions

def extract_body(html_str):
    try: return html_str.split('<body>')[1].split('</body>')[0]
    except IndexError: return html_str

def create_page(grade, sub_t, questions, is_key=False, q_margin="20px", ws_height="180px", brand_name=""):
    title = "เฉลยแบบฝึกหัด" if is_key else "แบบฝึกหัดคณิตศาสตร์"
    student_info = """<table style="width: 100%; margin-bottom: 10px; font-size: 18px; border-collapse: collapse;"><tr><td style="width: 1%; white-space: nowrap; padding-right: 5px;"><b>ชื่อ-สกุล</b></td><td style="border-bottom: 2px dotted #999; width: 60%;"></td><td style="width: 1%; white-space: nowrap; padding-left: 20px; padding-right: 5px;"><b>ชั้น</b></td><td style="border-bottom: 2px dotted #999; width: 15%;"></td><td style="width: 1%; white-space: nowrap; padding-left: 20px; padding-right: 5px;"><b>เลขที่</b></td><td style="border-bottom: 2px dotted #999; width: 15%;"></td></tr></table>""" if not is_key else ""
    html = f"""<!DOCTYPE html><html lang="th"><head><meta charset="utf-8"><style>@page {{ size: A4; margin: 15mm; }} body {{ font-family: 'Sarabun', sans-serif; padding: 20px; line-height: 1.6; color: #333; }} .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 10px; padding-bottom: 10px; }} .q-box {{ margin-bottom: {q_margin}; padding: 5px 15px; page-break-inside: avoid; border-bottom: 1px dashed #eee; font-size: 20px; }} .workspace {{ height: {ws_height}; border: 2px dashed #bdc3c7; border-radius: 8px; margin: 10px 0; padding: 10px; color: #95a5a6; font-size: 16px; display: flex; align-items: flex-start; }} .ans-line {{ margin-top: 5px; border-bottom: 1px dotted #999; width: 80%; height: 30px; font-weight: bold; font-size: 20px; display: flex; align-items: flex-end; padding-bottom: 5px; }} .sol-text {{ color: #333; font-size: 20px; display: inline-block; margin-top: 5px; line-height: 1.5; }} .page-footer {{ text-align: right; font-size: 14px; color: #95a5a6; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }} </style></head><body><div class="header"><h2>{title} - {grade}</h2><p><b>เรื่อง:</b> {sub_t}</p></div>{student_info}"""
    for i, item in enumerate(questions, 1):
        html += f'<div class="q-box"><b>ข้อที่ {i}.</b> '
        if is_key:
            if "(แบบตั้งหลัก)" in sub_t or "หารยาว" in sub_t: html += f'{item["solution"]}'
            else: html += f'{item["question"]}<br><div class="sol-text">{item["solution"]}</div>'
        else: html += f'{item["question"]}<div class="workspace">พื้นที่แสดงวิธีทำ...</div><div class="ans-line">ตอบ: </div>'
        html += '</div>'
    if brand_name: html += f'<div class="page-footer">&copy; 2026 {brand_name} | สงวนลิขสิทธิ์</div>'
    return html + "</body></html>"

def generate_cover_html(grade, main_t, sub_t, num_q, theme_colors, brand_name):
    return f"""<!DOCTYPE html><html lang="th"><head><meta charset="utf-8"><style>.cover-inner {{ width: 100%; height: 100%; padding: 40px; box-sizing: border-box; text-align: center; position: relative; border: 15px solid {theme_colors['border']}; background: white; }} .title-box {{ margin-top: 80px; }} .title {{ font-size: 65px; color: #2c3e50; font-weight: bold; margin: 0; line-height: 1.2; }} .grade-badge {{ font-size: 45px; background-color: {theme_colors['badge']}; color: white; padding: 15px 50px; border-radius: 50px; display: inline-block; font-weight: bold; margin-top: 30px; }} .topic {{ font-size: 42px; color: #34495e; margin-top: 70px; font-weight: bold; }} .sub-topic {{ font-size: 32px; color: #7f8c8d; margin-top: 10px; }} .icons {{ font-size: 110px; margin: 60px 0; }} .details-badge {{ background-color: #2ecc71; color: white; display: inline-block; padding: 15px 40px; border-radius: 15px; font-size: 32px; font-weight: bold; }} .footer {{ position: absolute; bottom: 40px; left: 0; width: 100%; text-align: center; font-size: 22px; color: #7f8c8d; }}</style></head><body><div class="cover-inner"><div class="title-box"><h1 class="title">แบบฝึกหัดคณิตศาสตร์</h1><div class="grade-badge">ชั้น{grade}</div></div><div class="topic">เรื่อง: {sub_t}</div><div class="sub-topic">(หมวดหมู่: {main_t})</div><div class="icons">🧮 📏 📐 ✏️</div><div class="details-badge">รวมทั้งหมด {num_q} ข้อ (พร้อมเฉลยละเอียด)</div><div class="footer"><b>ออกแบบและจัดทำโดย:</b> {brand_name}</div></div></body></html>"""

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
    else: selected_sub = st.sidebar.selectbox("📝 เลือกหัวข้อย่อย:", curriculum_db[selected_grade][selected_main])
else: 
    selected_grade = st.sidebar.selectbox("🏆 เลือกระดับชั้นแข่งขัน:", ["ป.1-ป.2 (พื้นฐาน)", "ป.3-ป.4 (ประยุกต์)", "ป.5-ป.6 (วิเคราะห์)"]) 
    selected_main = "ข้อสอบแข่งขันระดับชาติ"
    sub_options = tmc_lower if "ป.1" in selected_grade else (tmc_mid if "ป.3" in selected_grade else tmc_upper)
    selected_sub = st.sidebar.selectbox("📝 เลือกแนวข้อสอบ (พร้อมภาพอธิบายเฉลย):", sub_options + ["🌟 สุ่มรวมทุกแนว"])

num_input = st.sidebar.number_input("🔢 จำนวนข้อ:", min_value=1, max_value=100, value=10)
st.sidebar.markdown("---")
st.sidebar.markdown("### 📏 ตั้งค่าหน้ากระดาษ (อัปเดตใหม่)")
spacing_level = st.sidebar.select_slider("↕️ ความสูงของพื้นที่ทดเลข:", options=["แคบ", "ปานกลาง", "กว้าง", "กว้างพิเศษ"], value="ปานกลาง")

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
    with st.spinner("กำลังประมวลผลวาดภาพเฉลยขั้นเทพ..."):
        grade_arg = "ป.1" if "ป.1" in selected_grade else ("ป.3" if "ป.3" in selected_grade else "ป.5")
        qs = generate_questions_logic(grade_arg, selected_main, selected_sub, num_input)
        html_w = create_page(selected_grade, selected_sub, qs, is_key=False, q_margin=q_margin, ws_height=ws_height, brand_name=brand_name)
        html_k = create_page(selected_grade, selected_sub, qs, is_key=True, q_margin=q_margin, ws_height=ws_height, brand_name=brand_name)
        html_cover = generate_cover_html(selected_grade, selected_main, selected_sub, num_input, theme_map[color_theme], brand_name) if include_cover else ""
        
        st.session_state['worksheet_html'] = html_w
        st.session_state['answerkey_html'] = html_k
        
        ebook_body = ""
        if include_cover: ebook_body += f'\n<div class="a4-wrapper cover-wrapper">{extract_body(html_cover)}</div>\n'
        ebook_body += f'\n<div class="a4-wrapper">{extract_body(html_w)}</div>\n<div class="a4-wrapper">{extract_body(html_k)}</div>\n'
        
        full_ebook_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap" rel="stylesheet"><style>@page {{ size: A4; margin: 15mm; }} @media screen {{ body {{ font-family: 'Sarabun', sans-serif; background-color: #525659; display: flex; flex-direction: column; align-items: center; padding: 40px 0; margin: 0; }} .a4-wrapper {{ width: 210mm; min-height: 297mm; background: white; margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.3); padding: 15mm; box-sizing: border-box; }} .cover-wrapper {{ padding: 0; }} }} @media print {{ body {{ font-family: 'Sarabun', sans-serif; background: transparent; padding: 0; display: block; margin: 0; }} .a4-wrapper {{ width: 100%; min-height: auto; margin: 0; padding: 0; box-shadow: none; page-break-after: always; }} .cover-wrapper {{ height: 260mm; }} }} .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 10px; padding-bottom: 10px; }} .q-box {{ margin-bottom: {q_margin}; padding: 5px 15px; page-break-inside: avoid; border-bottom: 1px dashed #eee; font-size: 20px; }} .workspace {{ height: {ws_height}; border: 2px dashed #bdc3c7; border-radius: 8px; margin: 10px 0; padding: 10px; color: #95a5a6; font-size: 16px; display: flex; align-items: flex-start; }} .ans-line {{ margin-top: 5px; border-bottom: 1px dotted #999; width: 80%; height: 30px; font-weight: bold; font-size: 20px; display: flex; align-items: flex-end; padding-bottom: 5px; }} .sol-text {{ color: #333; font-size: 20px; display: inline-block; margin-top: 5px; line-height: 1.5; }} .page-footer {{ text-align: right; font-size: 14px; color: #95a5a6; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }} .cover-inner {{ width: 100%; height: 100%; padding: 40px; box-sizing: border-box; text-align: center; position: relative; border: 15px solid {theme_map[color_theme]['border']}; background: white; }} .title-box {{ margin-top: 80px; }} .title {{ font-size: 65px; color: #2c3e50; font-weight: bold; margin: 0; }} .grade-badge {{ font-size: 45px; background-color: {theme_map[color_theme]['badge']}; color: white; padding: 15px 50px; border-radius: 50px; display: inline-block; font-weight: bold; margin-top: 30px; }} .topic {{ font-size: 42px; color: #34495e; margin-top: 70px; font-weight: bold; }} .sub-topic {{ font-size: 32px; color: #7f8c8d; margin-top: 10px; }} .icons {{ font-size: 110px; margin: 60px 0; }} .details-badge {{ background-color: #2ecc71; color: white; display: inline-block; padding: 15px 40px; border-radius: 15px; font-size: 32px; font-weight: bold; }} .footer {{ position: absolute; bottom: 40px; left: 0; width: 100%; text-align: center; font-size: 22px; color: #7f8c8d; }} </style></head><body>{ebook_body}</body></html>"""

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
    st.success(f"✅ สร้างไฟล์สำเร็จ! ภาพเฉลยระดับ Masterpiece พร้อมใช้งาน!")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📄 โหลดเฉพาะโจทย์", data=st.session_state['worksheet_html'], file_name=f"{st.session_state['filename_base']}_Worksheet.html", mime="text/html", use_container_width=True)
        st.download_button("🔑 โหลดเฉพาะเฉลย", data=st.session_state['answerkey_html'], file_name=f"{st.session_state['filename_base']}_AnswerKey.html", mime="text/html", use_container_width=True)
    with c2:
        st.download_button("📚 โหลดรวมเล่ม E-Book", data=st.session_state['ebook_html'], file_name=f"{st.session_state['filename_base']}_Full_EBook.html", mime="text/html", use_container_width=True)
        st.download_button("🗂️ โหลดแพ็กเกจ (.zip)", data=st.session_state['zip_data'], file_name=f"{st.session_state['filename_base']}.zip", mime="application/zip", use_container_width=True)
    st.markdown("---")
    components.html(st.session_state['ebook_html'], height=800, scrolling=True)
