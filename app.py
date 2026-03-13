import streamlit as st
import random
import math
import zipfile
import io
import time
import base64

# ==========================================
# ⚙️ ทดสอบว่ามีไลบรารี pdfkit สำหรับเจน PDF ตรงหรือไม่
# ==========================================
try:
    import pdfkit
    HAS_PDFKIT = True
except ImportError:
    HAS_PDFKIT = False

# ==========================================
# ตั้งค่าหน้าเพจ Web App
# ==========================================
st.set_page_config(page_title="เครื่องมือสร้างใบงานคณิตศาสตร์", page_icon="🖨️", layout="wide")
st.title("🖨️ เครื่องมือสร้างใบงานคณิตศาสตร์ ป.1 - ป.6 (E-Book Edition)")
st.markdown("ระบบสุ่มโจทย์อัตโนมัติ สร้างหน้าปก และรวมเล่ม พร้อมขายบน Teachers Pay Teachers")

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

# ==========================================
# 🟢 รูปแบบกล่องสี่เหลี่ยม (ประโยคสัญลักษณ์)
# ==========================================
box_html = "<span style='display: inline-block; width: 22px; height: 22px; border: 2px solid #333; border-radius: 3px; vertical-align: middle; margin-left: 5px; position: relative; top: -2px;'></span>"

# (ฟังก์ชันช่วยสร้างกราฟิก และ สมองกลสุ่มโจทย์ ทั้งหมดเหมือนเดิมเป๊ะๆ เพื่อรักษาความสมบูรณ์ 100%)
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
    return f"""<div style="display: inline-block; font-family: 'Sarabun', sans-serif; font-size: 38px; line-height: 1.1; margin: 10px 20px;"><table style="border-collapse: collapse; margin-left: auto; margin-right: auto;"><tr><td style="width: 20px;"></td>{a_tds}<td style="width: 50px; text-align: center; vertical-align: middle;" rowspan="2">{op}</td></tr><tr><td></td>{b_tds}</tr><tr><td></td>{res_tds}<td></td></tr><tr><td></td><td colspan="{num_len}" style="border-bottom: 6px double #000; height: 10px;"></td><td></td></tr></table></div>"""

def generate_fraction_html(num, den):
    return f"""<div style="display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; margin: 0 8px; font-family: 'Sarabun', sans-serif;"><span style="font-size: 26px; font-weight: bold; border-bottom: 3px solid #000; padding: 0 5px; line-height: 1.1;">{num}</span><span style="font-size: 26px; font-weight: bold; padding: 0 5px; line-height: 1.1;">{den}</span></div>"""

def generate_mixed_number_html(whole, num, den):
    return f"""<div style="display: inline-flex; align-items: center; vertical-align: middle; margin: 0 8px; font-family: 'Sarabun', sans-serif;"><span style="font-size: 32px; font-weight: bold; margin-right: 5px; color: red;">{whole}</span><div style="display: inline-flex; flex-direction: column; align-items: center;"><span style="font-size: 26px; font-weight: bold; border-bottom: 3px solid red; padding: 0 5px; line-height: 1.1; color: red;">{num}</span><span style="font-size: 26px; font-weight: bold; padding: 0 5px; line-height: 1.1; color: red;">{den}</span></div></div>"""

def get_fraction_solution_steps(num, den):
    g = math.gcd(num, den)
    if num == 0: return "", "<span style='font-size: 32px; font-weight: bold; color: red;'>0</span>"
    if num == den: return "", "<span style='font-size: 32px; font-weight: bold; color: red;'>1</span>"
    sim_num, sim_den = num // g, den // g
    extra_steps, final_html = "", ""
    if sim_den == 1:
        final_html = f"<span style='font-size: 32px; font-weight: bold; color: red;'>{sim_num}</span>"
        if g > 1: extra_steps = f"ทอนเป็นเศษส่วนอย่างต่ำโดยใช้แม่ {g} หารเศษและส่วน จะได้เป็นจำนวนเต็ม"
    elif sim_num > sim_den:
        w, r = sim_num // sim_den, sim_num % sim_den
        final_html = generate_mixed_number_html(w, r, sim_den)
        if g > 1: extra_steps = f"ทอนเป็นเศษส่วนอย่างต่ำ (ใช้แม่ {g} หาร) และทำให้อยู่ในรูปจำนวนคละ"
        else: extra_steps = f"แปลงเศษเกินให้อยู่ในรูปจำนวนคละ"
    else:
        final_html = f"""<div style="display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; margin: 0 8px; font-family: 'Sarabun', sans-serif;"><span style="font-size: 26px; font-weight: bold; border-bottom: 3px solid red; padding: 0 5px; line-height: 1.1; color: red;">{sim_num}</span><span style="font-size: 26px; font-weight: bold; padding: 0 5px; line-height: 1.1; color: red;">{sim_den}</span></div>"""
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
    if not factors: return f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ไม่มีตัวประกอบร่วมที่หารลงตัวทั้งคู่</span><br><b>{mode} = 1</b>" if mode=="ห.ร.ม." else f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ไม่มีตัวประกอบร่วม</span><br><b>ค.ร.น. = {a} × {b} = {a*b}</b>"
    steps_html += f"<tr><td></td><td style='padding: 5px 15px; text-align: center;'>{ca}</td><td style='padding: 5px 15px; text-align: center;'>{cb}</td></tr>"
    table = f"<table style='margin: 10px 0; font-size: 24px; border-collapse: collapse; color: #333;'>{steps_html}</table>"
    if mode == "ห.ร.ม.":
        ans = math.prod(factors); calc_str = " × ".join(map(str, factors))
        sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ (หารสั้น):</b></span>{table}<span style='color: #2c3e50;'><b>ห.ร.ม.</b> คือนำตัวหารด้านหน้ามาคูณกัน:</span><br>= {calc_str}<br>= <b>{ans}</b>"
    else:
        ans = math.prod(factors) * ca * cb; calc_str = " × ".join(map(str, factors + [ca, cb]))
        sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ (หารสั้น):</b></span>{table}<span style='color: #2c3e50;'><b>ค.ร.น.</b> คือนำตัวหารและผลลัพธ์บรรทัดสุดท้ายมาคูณกัน (รูปตัว L):</span><br>= {calc_str}<br>= <b>{ans}</b>"
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
    return f"""<div style="display: inline-block; font-family: 'Sarabun', sans-serif; font-size: 38px; line-height: 1.2; margin: 10px 20px;"><table style="border-collapse: collapse; margin-left: auto; margin-right: auto;"><tr><td style="width: 20px;"></td>{a_tds}<td style="width: 50px; text-align: center; vertical-align: middle;" rowspan="2">{op}</td></tr><tr><td></td>{b_tds}</tr><tr><td></td>{ans_tds}<td></td></tr><tr><td></td><td colspan="{max_len}" style="border-bottom: 6px double #000; height: 10px;"></td><td></td></tr></table></div>"""

def generate_long_division_step_by_step_html(divisor, dividend, is_key=False):
    div_str = str(dividend); div_len = len(div_str)
    equation_html = f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 15px; color: #2c3e50;'>ประโยคสัญลักษณ์: {dividend:,} ÷ {divisor} = {box_html}</div>"
    if not is_key:
        div_tds_list = []
        for i, c in enumerate(div_str):
            left_border = "border-left: 3px solid #000;" if i == 0 else ""
            div_tds_list.append(f'<td style="width: 35px; text-align: center; border-top: 3px solid #000; {left_border} font-size: 38px;">{c}</td>')
        div_tds_list.append('<td style="width: 35px;"></td>')
        return f"{equation_html}<div style=\"display: inline-block; font-family: 'Sarabun', sans-serif; line-height: 1.2; margin: 10px 20px;\"><table style=\"border-collapse: collapse;\"><tr><td style=\"border: none; text-align: right; padding-right: 12px; vertical-align: bottom; font-size: 38px;\">{divisor}</td>{''.join(div_tds_list)}</tr></table></div><br>{'<br>' * 12}"
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
    html = f"{equation_html}<div style=\"display: inline-block; font-family: 'Sarabun', sans-serif; line-height: 1.2; margin: 10px 20px;\"><table style=\"border-collapse: collapse;\"><tr><td style=\"border: none;\"></td>{''.join(ans_tds_list)}</tr><tr><td style=\"border: none; text-align: right; padding-right: 12px; vertical-align: bottom; font-size: 38px;\">{divisor}</td>{''.join(div_tds_list)}</tr>"
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
    html += "</table></div>"
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

def generate_questions_logic(grade, main_t, sub_t, num_q):
    questions = []
    seen = set()
    limit_map = {"ป.1": 100, "ป.2": 1000, "ป.3": 100000, "ป.4": 1000000, "ป.5": 9000000, "ป.6": 9000000}
    limit = limit_map.get(grade, 100)

    for _ in range(num_q):
        q, sol = "", ""
        attempts = 0
        while attempts < 300:
            if sub_t == "การคูณ (แบบตั้งหลัก)":
                if grade in ["ป.1", "ป.2"]: a = random.randint(10, 99) 
                elif grade == "ป.3": a = random.randint(100, 999) 
                else: a = random.randint(1000, 9999) 
                b = random.randint(2, 9)
                res = a * b
                sentence = f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #2c3e50;'>ประโยคสัญลักษณ์: {a:,} × {b:,} = {box_html}</div>"
                q = sentence + generate_vertical_table_html(a, b, '×', is_key=False)
                sol = sentence + generate_vertical_table_html(a, b, '×', result=res, is_key=True)

            elif sub_t == "การบวก (แบบตั้งหลัก)":
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

            elif sub_t == "การลบ (แบบตั้งหลัก)":
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

            elif "การหารพื้นฐาน" in sub_t:
                a = random.randint(2, 9); b = random.randint(2, 12); dividend = a * b
                q = f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #2c3e50;'>ประโยคสัญลักษณ์: {dividend} ÷ {a} = {box_html}</div>จงหาผลลัพธ์ของ <b>{dividend} ÷ {a}</b>"
                sol = f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #2c3e50;'>ประโยคสัญลักษณ์: {dividend} ÷ {a} = {box_html}</div><br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ท่องสูตรคูณแม่ {a} จะพบว่า {a} × {b} = {dividend}<br>ดังนั้น {dividend} ÷ {a} = </span> <b>{b}</b>"

            elif "ส่วนย่อย-ส่วนรวม" in sub_t:
                total = random.randint(5, 20); p1 = random.randint(1, total - 1); p2 = total - p1
                miss = random.choice(['t', 'p1', 'p2'])
                svg_t = f"""<br><div style="text-align: center;"><svg width="200" height="160"><line x1="100" y1="40" x2="50" y2="120" stroke="#333" stroke-width="3"/><line x1="100" y1="40" x2="150" y2="120" stroke="#333" stroke-width="3"/><circle cx="100" cy="40" r="30" fill="#e8f8f5" stroke="#16a085" stroke-width="3"/><circle cx="50" cy="120" r="30" fill="#fdf2e9" stroke="#d35400" stroke-width="3"/><circle cx="150" cy="120" r="30" fill="#fdf2e9" stroke="#d35400" stroke-width="3"/><text x="100" y="47" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='t' else "#16a085"}">{{t}}</text><text x="50" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='p1' else "#d35400"}">{{p1}}</text><text x="150" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='p2' else "#d35400"}">{{p2}}</text></svg></div>"""
                q = f"จงหาตัวเลขที่หายไป (?) : " + svg_t.format(t="?" if miss=='t' else total, p1="?" if miss=='p1' else p1, p2="?" if miss=='p2' else p2)
                miss_map = {'t': 'ส่วนรวม (วงกลมบน)', 'p1': 'ส่วนย่อย (วงกลมซ้าย)', 'p2': 'ส่วนย่อย (วงกลมขวา)'}
                if miss == 't': calc_str = f"นำส่วนย่อยมาบวกกัน: {p1} + {p2} = <b>{total}</b>"
                elif miss == 'p1': calc_str = f"นำส่วนรวมลบด้วยส่วนย่อยที่มี: {total} - {p2} = <b>{p1}</b>"
                else: calc_str = f"นำส่วนรวมลบด้วยส่วนย่อยที่มี: {total} - {p1} = <b>{p2}</b>"
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> หา{miss_map[miss]}ที่หายไป โดย{calc_str}</span><br>" + svg_t.format(t=total, p1=p1, p2=p2)

            elif "การบอกอันดับที่" in sub_t:
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

            elif "แบบรูปซ้ำ" in sub_t:
                shapes = {"วงกลม": '<circle cx="15" cy="15" r="12" fill="#ffb3ba" stroke="#333" stroke-width="2"/>', "สี่เหลี่ยม": '<rect x="3" y="3" width="24" height="24" fill="#bae1ff" stroke="#333" stroke-width="2"/>', "สามเหลี่ยม": '<polygon points="15,3 27,27 3,27" fill="#baffc9" stroke="#333" stroke-width="2"/>', "ดาว": '<polygon points="15,1 19,10 29,10 21,16 24,26 15,20 6,26 9,16 1,10 11,10" fill="#ffffba" stroke="#333" stroke-width="2"/>'}
                pt = random.choice([[0, 1], [0, 1, 2], [0, 0, 1], [0, 1, 1]])
                keys = random.sample(list(shapes.keys()), len(set(pt)))
                seq = [keys[pt[i % len(pt)]] for i in range(12)]; slen = random.randint(5, 8) 
                html = "<br><div style='margin-top:10px; text-align:center;'>" + "".join([f'<svg width="30" height="30" style="vertical-align: middle; margin: 0 5px;">{shapes[seq[i]]}</svg>' for i in range(slen)]) + '<span style="display:inline-block; width:30px; height:30px; border-bottom:2px dashed #000; margin: 0 5px;"></span></div>'
                q = f"รูปที่หายไปคือรูปใด? {html}"
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> สังเกตจะพบว่ารูปภาพมีการเรียงซ้ำกันเป็นชุด ชุดละ {len(set(pt))} รูป เมื่อนับลำดับต่อมาเรื่อยๆ รูปที่หายไปคือ:</span><br><br><svg width='30' height='30' style='vertical-align: middle;'>{shapes[seq[slen]]}</svg>"

            elif "นาฬิกา" in sub_t:
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
                svg = f'<br><div style="text-align: center; margin: 15px 0;"><svg width="180" height="180" viewBox="0 0 200 200">{"".join(svg_elements)}</svg></div>'
                day = random.choice(["เวลากลางวัน", "เวลากลางคืน"])
                q = f"หากเป็น <b>{day}</b> จะอ่านเวลาได้กี่นาฬิกา กี่นาที? {svg}"
                ans_h = h + 12 if day == "เวลากลางวัน" and 1 <= h <= 5 else (h + 12 if day == "เวลากลางคืน" and 6 <= h <= 11 else (0 if day == "เวลากลางคืน" and h == 12 else h))
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> <br>1. เข็มสั้น(สีแดง) มีเส้นประชี้บอกว่ายังอยู่ระหว่างเลข {h} กับ {h+1 if h<12 else 1} แสดงถึงชั่วโมงที่ {h} <br>2. เข็มยาว(สีน้ำเงิน) ชี้ที่ขีดนาทีที่ {m} (ดูตัวเลขด้านนอกประกอบ)<br>ถ้าเป็น{day} จึงอ่านเวลาได้</span> <b>{ans_h:02d}.{m:02d} น.</b>"

            elif "จำนวนเงิน" in sub_t:
                b100 = random.randint(0, 3); b50 = random.randint(0, 2); b20 = random.randint(0, 4)
                c10 = random.randint(0, 5); c5 = random.randint(0, 3); c1 = random.randint(0, 5)
                if b100+b50+b20+c10+c5+c1 == 0: b20 = 1
                total = (b100*100) + (b50*50) + (b20*20) + (c10*10) + (c5*5) + (c1*1)
                money_svg = "<br><div style='margin-top:10px; line-height: 2.5;'>"
                for _ in range(b100): money_svg += '<svg width="60" height="30" style="vertical-align: middle; margin: 2px;"><rect width="60" height="30" rx="3" fill="#ff7675" stroke="#c0392b" stroke-width="2"/><text x="30" y="20" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">100</text></svg>'
                for _ in range(b50): money_svg += '<svg width="60" height="30" style="vertical-align: middle; margin: 2px;"><rect width="60" height="30" rx="3" fill="#74b9ff" stroke="#2980b9" stroke-width="2"/><text x="30" y="20" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">50</text></svg>'
                for _ in range(b20): money_svg += '<svg width="60" height="30" style="vertical-align: middle; margin: 2px;"><rect width="60" height="30" rx="3" fill="#55efc4" stroke="#27ae60" stroke-width="2"/><text x="30" y="20" font-size="12" font-weight="bold" fill="#333" text-anchor="middle">20</text></svg>'
                for _ in range(c10): money_svg += '<svg width="30" height="30" style="vertical-align: middle; margin: 2px;"><circle cx="15" cy="15" r="13" fill="#bdc3c7" stroke="#7f8c8d" stroke-width="2"/><circle cx="15" cy="15" r="8" fill="#f1c40f"/><text x="15" y="19" font-size="10" font-weight="bold" fill="#333" text-anchor="middle">10</text></svg>'
                for _ in range(c5): money_svg += '<svg width=\"30\" height=\"30\" style=\"vertical-align: middle; margin: 2px;\"><circle cx=\"15\" cy=\"15\" r=\"11\" fill=\"#ecf0f1\" stroke=\"#95a5a6\" stroke-width=\"2\"/><text x=\"15\" y=\"19\" font-size=\"10\" font-weight=\"bold\" fill=\"#333\" text-anchor=\"middle\">5</text></svg>'
                for _ in range(c1): money_svg += '<svg width=\"30\" height=\"30\" style=\"vertical-align: middle; margin: 2px;\"><circle cx=\"15\" cy=\"15\" r=\"9\" fill=\"#ecf0f1\" stroke=\"#bdc3c7\" stroke-width=\"1.5\"/><text x=\"15\" y=\"19\" font-size=\"10\" font-weight=\"bold\" fill=\"#333\" text-anchor=\"middle\">1</text></svg>'
                money_svg += "</div>"
                q = f"จากภาพ มีเงินทั้งหมดกี่บาท? {money_svg}"
                sol = "<br><span style='color: #2c3e50;'><b>วิธีทำ:</b><br>"
                if b100 > 0: sol += f"แบงก์ 100 บาท {b100} ใบ = {b100*100} บาท<br>"
                if b50 > 0: sol += f"แบงก์ 50 บาท {b50} ใบ = {b50*50} บาท<br>"
                if b20 > 0: sol += f"แบงก์ 20 บาท {b20} ใบ = {b20*20} บาท<br>"
                if c10 > 0: sol += f"เหรียญ 10 บาท {c10} เหรียญ = {c10*10} บาท<br>"
                if c5 > 0: sol += f"เหรียญ 5 บาท {c5} เหรียญ = {c5*5} บาท<br>"
                if c1 > 0: sol += f"เหรียญ 1 บาท {c1} เหรียญ = {c1*1} บาท<br>"
                sol += f"นำมาบวกกันทั้งหมดจะได้เงินรวม</span> <b>{total:,} บาท</b>"

            elif "เครื่องชั่งสปริง" in sub_t:
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
                scale_svg = f'<br><div style="text-align: center; margin: 15px 0;"><svg width="200" height="220" viewBox="0 0 200 220">{svg_content}</svg></div>'
                q = f"จากหน้าปัดเครื่องชั่งสปริง สินค้ามีน้ำหนักเท่าใด? {scale_svg}"
                if kg == 0: explain = f"เข็มชี้ไปที่ขีดเล็กที่ {khid} (ยังไม่ถึงเลข 1)"
                elif khid == 0: explain = f"เข็มชี้ตรงกับเลข {kg} พอดี"
                else: explain = f"เข็มชี้เลยเลข {kg} มา {khid} ขีดเล็ก"
                ans_text = ""
                if kg > 0 and khid > 0: ans_text = f"{kg} กิโลกรัม {khid} ขีด"
                elif kg > 0 and khid == 0: ans_text = f"{kg} กิโลกรัม"
                else: ans_text = f"{khid} ขีด"
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> {explain} (จำไว้ว่าช่องเล็ก 1 ช่อง = 1 ขีด)<br>ดังนั้น สินค้ามีน้ำหนัก</span> <b>{ans_text}</b>"

            elif "แผนภูมิรูปภาพ" in sub_t:
                items = [("🍎 แอปเปิล", "🍎"), ("🍊 ส้ม", "🍊"), ("🍌 กล้วย", "🍌"), ("🍓 องุ่น", "🍓")]
                selected = random.sample(items, 3); multiplier = 1 if grade == "ป.1" else random.choice([2, 5])
                counts = [random.randint(1, 5), random.randint(1, 5), random.randint(1, 5)]
                table_html = f"""<br><div style='margin-top:10px; width: 80%; border: 2px solid #333; border-collapse: collapse;'><div style='background-color: #f1f2f6; border-bottom: 2px solid #333; text-align: center; padding: 5px; font-weight: bold;'>จำนวนผลไม้ที่ร้านค้าขายได้</div>"""
                for i in range(3): table_html += f"<div style='display: flex; border-bottom: 1px solid #ccc;'><div style='width: 30%; border-right: 1px solid #ccc; padding: 5px; font-weight: bold;'>{selected[i][0]}</div><div style='width: 70%; padding: 5px; font-size: 18px;'>{''.join([selected[i][1]] * counts[i])}</div></div>"
                table_html += f"<div style='background-color: #fdfdfd; text-align: center; padding: 5px; font-weight: bold; color: #e74c3c;'>กำหนดให้ 1 รูปภาพ แทนผลไม้ {multiplier} ผล</div></div>"
                q = f"จากแผนภูมิ ขายผลไม้ 3 ชนิดรวมกันกี่ผล? {table_html}"
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> นับรูปผลไม้ทั้งหมดรวมกันได้ {sum(counts)} รูปภาพ<br>และกำหนดให้ 1 รูปภาพ แทนผลไม้ {multiplier} ผล<br>นำ {sum(counts)} × {multiplier} =</span> <b>{sum(counts) * multiplier} ผล</b>"

            elif "การนับทีละ" in sub_t:
                is_10 = "10" in sub_t; is_1 = "1" in sub_t; step = 10 if is_10 else (1 if is_1 else random.choice([2, 5, 10, 100]))
                inc = random.choice([True, False]); max_val = limit - (3 * step)
                if max_val <= 1: max_val = 10
                st_val = random.randint(1, max_val)
                seq = [st_val, st_val+step, st_val+2*step, st_val+3*step] if inc else [st_val+3*step, st_val+2*step, st_val+step, st_val]
                idx = random.randint(0, 3); ans_str = f"{seq[idx]:,}"
                q = f"จงเติมตัวเลขที่หายไปในแบบรูป : {', '.join([f'{s:,}' if i != idx else '_____' for i, s in enumerate(seq)])}"
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> สังเกตความต่างของตัวเลข พบว่าแบบรูปมีการ{'นับเพิ่มขึ้น' if inc else 'นับลดลง'}ทีละ {step}<br>ดังนั้น ตัวเลขที่หายไปคือ</span> <b>{ans_str}</b>"

            elif "เรียงลำดับ" in sub_t:
                nums = random.sample(range(10, limit), 4)
                is_asc = "น้อยไปมาก" in sub_t if "น้อยไปมาก" in sub_t else random.choice([True, False])
                q = f"จงเรียงลำดับจำนวนต่อไปนี้จาก {'น้อยไปมาก' if is_asc else 'มากไปน้อย'}: {', '.join(f'{x:,}' for x in nums)}"
                res = sorted(nums, reverse=not is_asc)
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> เปรียบเทียบค่าทีละจำนวนและเรียงจาก{'น้อยไปหามาก' if is_asc else 'มากไปหาน้อย'}<br>ตอบ: </span> <b>{', '.join(f'{x:,}' for x in res)}</b>"

            elif "เปรียบเทียบ" in sub_t:
                a = random.randint(10, limit); is_eq = "=" in sub_t
                if is_eq and random.choice([True, False]): b = a
                else:
                    b = random.randint(10, limit)
                    while a == b: b = random.randint(10, limit)
                sign = "=" if a == b else ("≠" if is_eq else (">" if a > b else "<"))
                q = f"จงเติมเครื่องหมาย {'= หรือ ≠' if is_eq else '> หรือ <'} ลงในช่องว่าง: {a:,} _____ {b:,}"
                comp_text = "มีค่าเท่ากับ" if a==b else ("มากกว่า" if a>b else "น้อยกว่า")
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> เปรียบเทียบค่าทีละหลักจากซ้ายไปขวา จะพบว่า {a:,} {comp_text} {b:,}<br>ตอบ: </span> <b>{sign}</b>"

            elif "รูปกระจาย" in sub_t:
                min_val = 10 if limit <= 1000 else 100; max_val = limit - 1 if limit > 10 else 99
                n = random.randint(min_val, max_val)
                parts = [f"{int(d)*(10**(len(str(n))-1-i)):,}" for i,d in enumerate(str(n)) if d != '0']
                q = f"จงเขียน <b>{n:,}</b> ในรูปกระจาย"
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> แยกตัวเลขตามค่าประจำหลักจะได้:<br></span><b>{' + '.join(parts)}</b>"
                
            elif "จำนวนคู่" in sub_t:
                n = random.randint(10, limit)
                q = f"จำนวน <b>{n:,}</b> เป็นจำนวนคู่ หรือ จำนวนคี่?"
                is_even = (n % 2 == 0)
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ดูที่หลักหน่วยคือเลข {n%10} ซึ่ง{'หารด้วย 2 ลงตัว' if is_even else 'หารด้วย 2 ไม่ลงตัว'}<br>ดังนั้นจึงเป็น</span> <b>{'จำนวนคู่' if is_even else 'จำนวนคี่'}</b>"

            elif "เขียนตัวเลข" in sub_t:
                if grade in ["ป.1", "ป.2", "ป.3"]: n = random.randint(11, limit-1)
                else: n = random.randint(100000, limit-1) if limit > 100000 else random.randint(100000, 9999999)
                if random.choice([True, False]):
                    q = f"จงเขียนตัวเลขฮินดูอารบิก <b>{n:,}</b> ให้เป็น<b>ตัวเลขไทย</b>"
                    sol = f"<b>{n:,}</b>".translate(str.maketrans('0123456789', '๐๑๒๓๔๕๖๗๘๙'))
                else:
                    q = f"จงเขียนตัวเลข <b>{n:,}</b> ให้เป็น<b>ตัวหนังสือ</b>"
                    sol = f"<b>{generate_thai_number_text(str(n))}</b>"

            elif "ค่าประมาณ" in sub_t:
                n = random.randint(1111, 99999); ptype = random.choice(["เต็มสิบ", "เต็มร้อย", "เต็มพัน"])
                if ptype == "เต็มสิบ": ans = ((n + 5) // 10) * 10; chk_d = n % 10; chk_p = "หลักหน่วย"
                elif ptype == "เต็มร้อย": ans = ((n + 50) // 100) * 100; chk_d = (n // 10) % 10; chk_p = "หลักสิบ"
                else: ans = ((n + 500) // 1000) * 1000; chk_d = (n // 100) % 10; chk_p = "หลักร้อย"
                action = "ปัดขึ้น" if chk_d >= 5 else "ปัดทิ้ง"
                q = f"จงหาค่าประมาณเป็นจำนวน<b>{ptype}</b> ของ {n:,}"
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ประมาณเป็นจำนวน{ptype} ให้พิจารณาตัวเลขใน {chk_p} ซึ่งก็คือเลข <b>{chk_d}</b><br>ตามกฎแล้วต้องทำการ <b>{action}</b> จะได้เป็น:</span> <b>{ans:,}</b>"

            elif "หารยาว" in sub_t:
                divisor = random.randint(2, 12); quotient = random.randint(100, 999); dividend = divisor * quotient
                q = generate_long_division_step_by_step_html(divisor, dividend, is_key=False)
                sol = generate_long_division_step_by_step_html(divisor, dividend, is_key=True)

            elif "เศษเกินเป็นจำนวนคละ" in sub_t:
                den = random.randint(3, 12); num = random.randint(den + 1, den * 5)
                while num % den == 0: num = random.randint(den + 1, den * 5)
                frac_html = generate_fraction_html(num, den)
                q = f"จงเขียนเศษเกินต่อไปนี้ให้อยู่ในรูปจำนวนคละ : <br>{frac_html}"
                w, r = num // den, num % den; g = math.gcd(r, den)
                mixed_raw = generate_mixed_number_html(w, r, den)
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> นำตัวเศษตั้ง หารด้วยตัวส่วน<br>จะได้ <b>{num} ÷ {den} = {w} เศษ {r}</b><br>เขียนเป็นจำนวนคละโดยให้ <b>{w}</b> เป็นจำนวนเต็ม และ <b>{r}</b> เป็นเศษ: </span><br><br>{mixed_raw}"
                if g > 1:
                    sim_r, sim_den = r // g, den // g; mixed_sim = generate_mixed_number_html(w, sim_r, sim_den)
                    sol += f"<br><br><span style='color: #2c3e50;'><i>*ทอนเป็นเศษส่วนอย่างต่ำได้ (ใช้แม่ {g} หารเศษและส่วน):</i></span><br><br>{mixed_sim}"
                
            elif "อ่านและเขียนเศษส่วน" in sub_t:
                den = random.randint(3, 8); num = random.randint(1, den - 1); frac_html = generate_fraction_html(num, den)
                bar_w = 40; bar_h = 30; total_w = den * bar_w; rects = ""
                for i in range(den):
                    fill_color = "#3498db" if i < num else "#ffffff"
                    rects += f'<rect x="{i*bar_w}" y="0" width="{bar_w}" height="{bar_h}" fill="{fill_color}" stroke="#333" stroke-width="2"/>'
                svg_bar = f'<br><div style="text-align: center; margin: 15px 0;"><svg width="{total_w + 4}" height="{bar_h + 4}"><g transform="translate(2,2)">{rects}</g></svg></div>'
                q = f"จงอ่านและเขียนเศษส่วนที่ระบายสีจากรูปภาพต่อไปนี้ : {svg_bar}"
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> แบ่งรูปออกเป็น <b>{den}</b> ส่วนเท่าๆ กัน และระบายสีไป <b>{num}</b> ส่วน</span><br><div style='display: flex; align-items: center; margin-top: 10px;'><b>เขียนเป็นเศษส่วนได้: </b> {frac_html} <span style='margin-left: 20px;'><b>อ่านว่า: </b> เศษ {num} ส่วน {den}</span></div>"

            elif "บวกลบเศษส่วน" in sub_t or "บวกและการลบเศษส่วน" in sub_t:
                if grade == "ป.5":
                    d1 = random.randint(2, 10); d2 = random.randint(2, 10)
                    while d1 == d2: d2 = random.randint(2, 10) 
                    n1 = random.randint(1, d1 - 1); n2 = random.randint(1, d2 - 1)
                    op = random.choice(["+", "-"])
                    if op == "-" and (n1/d1) < (n2/d2): n1, n2 = n2, n1; d1, d2 = d2, d1
                    lcm_d = (d1 * d2) // math.gcd(d1, d2); m1 = lcm_d // d1; m2 = lcm_d // d2
                    ans_num = (n1 * m1) + (n2 * m2) if op == "+" else (n1 * m1) - (n2 * m2)
                    f1 = generate_fraction_html(n1, d1); f2 = generate_fraction_html(n2, d2)
                    q = f"จงหาผลลัพธ์ <br><div style='display:flex; align-items:center; margin-top:10px;'><b style='font-size: 20px; color: #2c3e50; margin-right: 10px;'>ประโยคสัญลักษณ์: </b> {f1} <span style='font-size:30px; margin: 0 10px;'>{op}</span> {f2} <span style='font-size:30px; margin: 0 10px;'>= </span> {box_html}</div>"
                    f1_ex = generate_fraction_html(f"{n1} × {m1}", f"{d1} × {m1}") if m1 > 1 else f1
                    f2_ex = generate_fraction_html(f"{n2} × {m2}", f"{d2} × {m2}") if m2 > 1 else f2
                    f1_new = generate_fraction_html(n1 * m1, lcm_d); f2_new = generate_fraction_html(n2 * m2, lcm_d); s_ans = generate_fraction_html(ans_num, lcm_d)
                    sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ทำตัวส่วนให้เท่ากัน โดยหา ค.ร.น. ของ {d1} และ {d2} ซึ่งก็คือ <b>{lcm_d}</b></span><br><br>"
                    sol += f"<div style='display:flex; align-items:center; margin-bottom: 10px;'> {f1} <span style='margin:0 10px;'>{op}</span> {f2} <span style='margin:0 10px;'>=</span> {f1_ex} <span style='margin:0 10px;'>{op}</span> {f2_ex} </div>"
                    sol += f"<div style='display:flex; align-items:center; margin-bottom: 15px;'> <span style='margin:0 10px;'></span> <span style='margin:0 10px;'>=</span> {f1_new} <span style='margin:0 10px;'>{op}</span> {f2_new} <span style='margin:0 10px;'>=</span> {s_ans}</div>"
                    extra_txt, final_html = get_fraction_solution_steps(ans_num, lcm_d)
                    if extra_txt: sol += f"<span style='color: #2c3e50;'><i>*{extra_txt}:</i></span><br><br>{final_html}"
                else:
                    den = random.randint(5, 15); num1 = random.randint(1, den-1); num2 = random.randint(1, den-1); op = random.choice(["+", "-"])
                    if op == "-" and num1 < num2: num1, num2 = num2, num1 
                    ans_num = num1 + num2 if op == "+" else num1 - num2
                    f1 = generate_fraction_html(num1, den); f2 = generate_fraction_html(num2, den)
                    q = f"จงหาผลลัพธ์ <br><div style='display:flex; align-items:center; margin-top:10px;'><b style='font-size: 20px; color: #2c3e50; margin-right: 10px;'>ประโยคสัญลักษณ์: </b> {f1} <span style='font-size:30px; margin: 0 10px;'>{op}</span> {f2} <span style='font-size:30px; margin: 0 10px;'>= </span> {box_html}</div>"
                    s1 = generate_fraction_html(f"{num1} {op} {num2}", den); s2 = generate_fraction_html(ans_num, den)
                    sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> เนื่องจากตัวส่วนเท่ากัน ให้นำตัวเศษมา{op}กันได้เลย</span><br><br><div style='display:flex; align-items:center; margin-bottom: 15px;'>{f1} <span style='margin:0 10px;'>{op}</span> {f2} <span style='margin:0 10px;'>=</span> {s1} <span style='margin:0 10px;'>=</span> {s2}</div>"
                    extra_txt, final_html = get_fraction_solution_steps(ans_num, den)
                    if extra_txt: sol += f"<span style='color: #2c3e50;'><i>*{extra_txt}:</i></span><br><br>{final_html}"

            elif "คูณและการหารเศษส่วน" in sub_t:
                n1, d1 = random.randint(1, 5), random.randint(2, 7); n2, d2 = random.randint(1, 5), random.randint(2, 7); op = random.choice(["×", "÷"])
                f1 = generate_fraction_html(n1, d1); f2 = generate_fraction_html(n2, d2)
                q = f"จงหาผลลัพธ์ <br><div style='display:flex; align-items:center; margin-top:10px;'><b style='font-size: 20px; color: #2c3e50; margin-right: 10px;'>ประโยคสัญลักษณ์: </b> {f1} <span style='font-size:30px; margin: 0 10px;'>{op}</span> {f2} <span style='font-size:30px; margin: 0 10px;'>= </span> {box_html}</div>"
                if op == "×":
                    s1 = generate_fraction_html(f"{n1} × {n2}", f"{d1} × {d2}"); ans_n, ans_d = n1*n2, d1*d2; s2 = generate_fraction_html(ans_n, ans_d)
                    sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> การคูณเศษส่วน ให้นำตัวเศษคูณตัวเศษ และตัวส่วนคูณตัวส่วน</span><br><br><div style='display:flex; align-items:center; margin-bottom: 15px;'>{f1} <span style='margin:0 10px;'>×</span> {f2} <span style='margin:0 10px;'>=</span> {s1} <span style='margin:0 10px;'>=</span> {s2}</div>"
                else:
                    f2_flip = generate_fraction_html(d2, n2); s1 = generate_fraction_html(f"{n1} × {d2}", f"{d1} × {n2}"); ans_n, ans_d = n1*d2, d1*n2; s2 = generate_fraction_html(ans_n, ans_d)
                    sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> เปลี่ยนเครื่องหมายหารเป็นคูณ แล้วกลับเศษเป็นส่วนของตัวหารด้านหลัง</span><br><br><div style='display:flex; align-items:center; margin-bottom: 15px;'>{f1} <span style='margin:0 10px;'>÷</span> {f2} <span style='margin:0 10px;'>=</span> {f1} <span style='margin:0 10px;'>×</span> {f2_flip} <span style='margin:0 10px;'>=</span> {s1} <span style='margin:0 10px;'>=</span> {s2}</div>"
                extra_txt, final_html = get_fraction_solution_steps(ans_n, ans_d)
                if extra_txt: sol += f"<span style='color: #2c3e50;'><i>*{extra_txt}:</i></span><br><br>{final_html}"

            elif "ทศนิยม" in sub_t and "อ่าน" in sub_t:
                n = round(random.uniform(0.1, 99.999), random.randint(1, 3))
                q = f"จงเขียน <b>{n}</b> เป็นตัวหนังสือภาษาไทย"
                sol = f"<b>{generate_thai_number_text(str(n))}</b>"

            elif "ทศนิยม" in sub_t and ("บวก" in sub_t or "ลบ" in sub_t):
                a = round(random.uniform(10.0, 99.9), 2); b = round(random.uniform(1.0, 9.9), 2); op = random.choice(["+", "-"])
                q = f"จงหาผลลัพธ์ <br><div style='font-size: 20px; font-weight: bold; margin-top: 5px; color: #2c3e50;'>ประโยคสัญลักษณ์: {a:.2f} {op} {b:.2f} = {box_html}</div>"
                sol_html = generate_decimal_vertical_html(a, b, op, is_key=True)
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ตั้งจุดทศนิยมให้ตรงกันแล้วดำเนินการตามปกติ</span><br>{sol_html}"

            elif "คูณทศนิยม" in sub_t:
                a = round(random.uniform(1.0, 12.0), 1); b = random.randint(2, 9); ans = round(a*b, 1)
                q = f"จงหาผลลัพธ์ <br><div style='font-size: 20px; font-weight: bold; margin-top: 5px; color: #2c3e50;'>ประโยคสัญลักษณ์: {a:.1f} × {b} = {box_html}</div>"
                int_a = int(round(a * 10)); vert_mul_html = generate_vertical_table_html(int_a, b, '×', result=int_a*b, is_key=True)
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b><br>1) ตั้งคูณโดยนำจุดทศนิยมออกก่อน ({int_a} × {b}):</span><br>{vert_mul_html}<br><span style='color: #2c3e50;'>2) ตัวตั้งมีทศนิยม 1 ตำแหน่ง คำตอบจึงต้องใส่ทศนิยม 1 ตำแหน่ง<br>ตอบ:</span> <b>{ans:.1f}</b>"

            elif "ร้อยละ" in sub_t and "เศษส่วน" in sub_t:
                den = random.choice([2, 4, 5, 10, 20, 25, 50]); num = random.randint(1, den-1); ans = int((num / den) * 100)
                frac_html = generate_fraction_html(num, den)
                q = f"จงเขียนเศษส่วนต่อไปนี้ให้อยู่ในรูปร้อยละ : <br>{frac_html}"
                mul = 100 // den
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ทำตัวส่วนให้เป็น 100 โดยการคูณด้วย {mul} ทั้งเศษและส่วน</span><br><br><div style='display:flex; align-items:center;'>{frac_html} <span style='margin:0 10px;'>=</span> {generate_fraction_html(f'{num} × {mul}', f'{den} × {mul}')} <span style='margin:0 10px;'>=</span> {generate_fraction_html(num*mul, 100)}</div><br>ตอบ: <b>ร้อยละ {ans} หรือ {ans}%</b>"

            elif "อัตราส่วนที่เท่ากัน" in sub_t:
                a = random.randint(2, 9); b = random.randint(2, 9)
                while a == b: b = random.randint(2, 9)
                m = random.randint(2, 9); c = a * m; d = b * m
                if random.choice([True, False]):
                    q = f"จงหาจำนวนที่แทนใน {box_html} แล้วทำให้ประโยคเป็นจริง : <br><b style='font-size: 24px; color: #3498db;'>{a} : {b} = {c} : {box_html}</b>"
                    sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> พิจารณาตัวหน้าจาก {a} ไปเป็น {c} พบว่าเกิดจากการคูณด้วย <b>{m}</b> (เพราะ {a} × {m} = {c})<br>ดังนั้น ตัวหลังที่หายไปต้องนำ {b} ไปคูณด้วย {m} ด้วยเช่นกัน<br>จะได้ {b} × {m} = </span><b>{d}</b>"
                else:
                    q = f"จงหาจำนวนที่แทนใน {box_html} แล้วทำให้ประโยคเป็นจริง : <br><b style='font-size: 24px; color: #3498db;'>{a} : {b} = {box_html} : {d}</b>"
                    sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> พิจารณาตัวหลังจาก {b} ไปเป็น {d} พบว่าเกิดจากการคูณด้วย <b>{m}</b> (เพราะ {b} × {m} = {d})<br>ดังนั้น ตัวหน้าที่หายไปต้องนำ {a} ไปคูณด้วย {m} ด้วยเช่นกัน<br>จะได้ {a} × {m} = </span><b>{c}</b>"

            elif "โจทย์ปัญหาอัตราส่วน" in sub_t:
                scenarios = [("นักเรียนชาย", "นักเรียนหญิง", "คน", "คน"), ("น้ำหวาน", "น้ำเปล่า", "มิลลิลิตร", "มิลลิลิตร"), ("ปากกา", "ดินสอ", "ด้าม", "แท่ง"), ("สมุด", "หนังสือ", "เล่ม", "เล่ม"), ("ไก่", "เป็ด", "ตัว", "ตัว")]
                item1, item2, u1, u2 = random.choice(scenarios)
                a = random.randint(2, 7); b = random.randint(2, 7)
                while a == b: b = random.randint(2, 7)
                m = random.randint(5, 20); val1 = a * m; val2 = b * m; q_type = random.choice([1, 2])
                if q_type == 1:
                    q = f"อัตราส่วนของจำนวน{item1} ต่อจำนวน{item2} เป็น <b>{a} : {b}</b><br>ถ้ามี{item1} <b>{val1} {u1}</b> จะมี{item2}จำนวนเท่าใด?"
                    sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> อัตราส่วน {item1} : {item2} = {a} : {b}<br>เนื่องจากมี{item1} {val1} {u1} ซึ่งเกิดจากการนำ {a} ไปคูณด้วย <b>{m}</b> ({a} × {m} = {val1})<br>ดังนั้น ต้องนำอัตราส่วนของ{item2}ไปคูณด้วย {m} ด้วยเช่นกัน<br>จะได้ {b} × {m} = </span><b>{val2} {u2}</b>"
                else:
                    total = val1 + val2
                    q = f"อัตราส่วนของจำนวน{item1} ต่อจำนวน{item2} เป็น <b>{a} : {b}</b><br>ถ้ามีจำนวนของทั้งสองอย่างรวมกัน <b>{total} {u1}</b> จะมี{item1}จำนวนเท่าใด?"
                    sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> อัตราส่วน {item1} : {item2} = {a} : {b}<br>นำอัตราส่วนมาบวกกันจะได้จำนวนส่วนทั้งหมด = {a} + {b} = <b>{a+b} ส่วน</b><br>ของทั้งหมด {total} {u1} แบ่งเป็น {a+b} ส่วน จะได้ส่วนละ {total} ÷ {a+b} = <b>{m} {u1}</b><br>ดังนั้น จำนวน{item1}มี {a} ส่วน จึงเท่ากับ {a} × {m} = </span><b>{val1} {u1}</b>"

            elif "โจทย์ปัญหาร้อยละ" in sub_t:
                price = random.choice([100, 200, 500, 1000, 1500]); percent = random.choice([10, 15, 20, 25, 50]); discount = int(price * (percent / 100))
                q = f"เสื้อราคา {price:,} บาท ร้านค้าลดราคาให้ {percent}% ร้านค้าลดราคาให้กี่บาท?<br><div style='margin-top: 15px; font-size: 18px; color: #2c3e50;'><b>ประโยคสัญลักษณ์:</b> ...........................................................</div>"
                sol = f"<br><span style='color: #2c3e50;'><b>ประโยคสัญลักษณ์:</b> ({percent} ÷ 100) × {price:,} = {box_html}</span><br><br><span style='color: #2c3e50;'><b>วิธีทำ:</b><br>คำว่า ลดราคา {percent}% หมายถึง ({percent} ÷ 100) × ราคาป้าย<br>= ({percent} ÷ 100) × {price:,}<br>ตอบ:</span> <b>{discount:,} บาท</b>"

            elif "ห.ร.ม." in sub_t:
                a = random.randint(12, 48); b = random.randint(12, 48)
                while a == b: b = random.randint(12, 48) 
                q = f"จงหา ห.ร.ม. ของ <b>{a}</b> และ <b>{b}</b>"
                sol = generate_short_division_html(a, b, mode="ห.ร.ม.")

            elif "ค.ร.น." in sub_t:
                a = random.randint(4, 24); b = random.randint(4, 24)
                while a == b: b = random.randint(4, 24) 
                q = f"จงหา ค.ร.น. ของ <b>{a}</b> และ <b>{b}</b>"
                sol = generate_short_division_html(a, b, mode="ค.ร.น.")

            elif "การแก้สมการ" in sub_t:
                if grade == "ป.4":
                    op = random.choice(["+", "-"])
                    if op == "+":
                        x = random.randint(5, 50); a = random.randint(1, 20); b = x + a
                        q = f"จงแก้สมการเพื่อหาค่า x : <br><b style='font-size: 24px; color: #3498db;'>x + {a} = {b}</b>"
                        sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ใช้สมบัติการเท่ากันของการลบ เพื่อกำจัด +{a}</span><br>นำ <b style='color: #27ae60;'>{a}</b> มาลบออกทั้งสองข้างของสมการ<br><b style='color: #3498db;'>x + {a}</b> <b style='color: #27ae60;'>- {a}</b> = <b style='color: #3498db;'>{b}</b> <b style='color: #27ae60;'>- {a}</b><br><b style='color: #3498db;'>x</b> <span style='text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;'><span style='color: #3498db;'>+ {a}</span> <span style='color: #27ae60;'>- {a}</span></span> = <b>{b - a}</b><br><b>x = {x}</b>"
                    else:
                        x = random.randint(20, 60); a = random.randint(5, x-5); b = x - a
                        q = f"จงแก้สมการเพื่อหาค่า x : <br><b style='font-size: 24px; color: #3498db;'>x - {a} = {b}</b>"
                        sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ใช้สมบัติการเท่ากันของการบวก เพื่อกำจัด -{a}</span><br>นำ <b style='color: #27ae60;'>{a}</b> มาบวกเข้าทั้งสองข้างของสมการ<br><b style='color: #3498db;'>x - {a}</b> <b style='color: #27ae60;'>+ {a}</b> = <b style='color: #3498db;'>{b}</b> <b style='color: #27ae60;'>+ {a}</b><br><b style='color: #3498db;'>x</b> <span style='text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;'><span style='color: #3498db;'>- {a}</span> <span style='color: #27ae60;'>+ {a}</span></span> = <b>{b + a}</b><br><b>x = {x}</b>"
                        
                elif grade == "ป.5":
                    op = random.choice(["*", "/"])
                    if op == "*":
                        a = random.randint(2, 12); x = random.randint(2, 20); b = a * x
                        q = f"จงแก้สมการเพื่อหาค่า x : <br><b style='font-size: 24px; color: #3498db;'>{a}x = {b}</b>"
                        sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ใช้สมบัติการเท่ากันของการหาร เพื่อกำจัด {a} ที่คูณอยู่กับ x</span><br>นำ <b style='color: #27ae60;'>{a}</b> มาหารทั้งสองข้างของสมการ<br><div style='display: flex; align-items: center; margin: 10px 0;'><div style='text-align: center; margin-right: 10px;'><span style='border-bottom: 2px solid #000; padding: 0 5px; color: #3498db; font-weight: bold;'>{a}x</span><br><b style='color: #27ae60;'>{a}</b></div> <b>=</b> <div style='text-align: center; margin-left: 10px;'><span style='border-bottom: 2px solid #000; padding: 0 5px; color: #3498db; font-weight: bold;'>{b}</span><br><b style='color: #27ae60;'>{a}</b></div></div><div style='display: flex; align-items: center; margin: 10px 0;'><div style='text-align: center; margin-right: 10px;'><span style='border-bottom: 2px solid #000; padding: 0 5px; color: #3498db; font-weight: bold;'><span style='text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;'>{a}</span>x</span><br><b style='color: #27ae60;'><span style='text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;'>{a}</span></b></div> <b>=</b> <div style='text-align: center; margin-left: 10px;'><b>{x}</b></div></div><b>x = {x}</b>"
                    else:
                        a = random.randint(2, 12); b = random.randint(2, 20); x = a * b
                        q = f"จงแก้สมการเพื่อหาค่า x : <br><div style='display: flex; align-items: center; font-size: 24px; font-weight: bold; margin: 10px 0; color: #3498db;'><div style='text-align: center; margin-right: 10px;'><span style='border-bottom: 2px solid #3498db; padding: 0 5px;'>x</span><br>{a}</div> = {b}</div>"
                        sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ใช้สมบัติการเท่ากันของการคูณ เพื่อกำจัด {a} ที่เป็นตัวส่วน</span><br>นำ <b style='color: #27ae60;'>{a}</b> มาคูณทั้งสองข้างของสมการ<br><div style='display: flex; align-items: center; margin: 10px 0;'><div style='text-align: center; margin-right: 10px; color: #3498db; font-weight: bold;'><span style='border-bottom: 2px solid #3498db; padding: 0 5px;'>x</span><br>{a}</div> <span style='margin: 0 10px;'> <b style='color: #27ae60;'>× {a}</b> </span> <b>=</b> <span style='margin: 0 10px;'><b style='color: #3498db;'>{b}</b> <b style='color: #27ae60;'>× {a}</b></span></div><div style='display: flex; align-items: center; margin: 10px 0;'><div style='text-align: center; margin-right: 10px; color: #3498db; font-weight: bold;'><span style='border-bottom: 2px solid #3498db; padding: 0 5px;'>x</span><br><span style='text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;'>{a}</span></div> <span style='margin: 0 10px;'> <b style='color: #27ae60;'>× <span style='text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;'>{a}</span></b> </span> <b>=</b> <span style='margin: 0 10px;'><b>{x}</b></span></div><b>x = {x}</b>"
                        
                elif grade == "ป.6":
                    op = random.choice(["+", "-"]); a = random.randint(2, 9); x = random.randint(2, 15)
                    if op == "+":
                        b = random.randint(1, 20); c = a * x + b
                        q = f"จงแก้สมการเพื่อหาค่า x : <br><b style='font-size: 24px; color: #3498db;'>{a}x + {b} = {c}</b>"
                        sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ (ขั้นที่ 1):</b> กำจัด +{b} โดยนำ <b style='color: #27ae60;'>{b}</b> มาลบออกทั้งสองข้าง</span><br><b style='color: #3498db;'>{a}x + {b}</b> <b style='color: #27ae60;'>- {b}</b> = <b style='color: #3498db;'>{c}</b> <b style='color: #27ae60;'>- {b}</b><br><b style='color: #3498db;'>{a}x</b> <span style='text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;'><span style='color: #3498db;'>+ {b}</span> <span style='color: #27ae60;'>- {b}</span></span> = <b>{c-b}</b><br><b>{a}x = {c-b}</b><br><br><span style='color: #2c3e50;'><b>วิธีทำ (ขั้นที่ 2):</b> กำจัด {a} ที่คูณอยู่ โดยนำ <b style='color: #27ae60;'>{a}</b> มาหารทั้งสองข้าง</span><br><div style='display: flex; align-items: center; margin: 10px 0;'><div style='text-align: center; margin-right: 10px;'><span style='border-bottom: 2px solid #000; padding: 0 5px; color: #3498db; font-weight: bold;'>{a}x</span><br><b style='color: #27ae60;'>{a}</b></div> <b>=</b> <div style='text-align: center; margin-left: 10px;'><span style='border-bottom: 2px solid #000; padding: 0 5px; color: #3498db; font-weight: bold;'>{c-b}</span><br><b style='color: #27ae60;'>{a}</b></div></div><div style='display: flex; align-items: center; margin: 10px 0;'><div style='text-align: center; margin-right: 10px;'><span style='border-bottom: 2px solid #000; padding: 0 5px; color: #3498db; font-weight: bold;'><span style='text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;'>{a}</span>x</span><br><b style='color: #27ae60;'><span style='text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;'>{a}</span></b></div> <b>=</b> <div style='text-align: center; margin-left: 10px;'><b>{x}</b></div></div><b>x = {x}</b>"
                    else:
                        b = random.randint(1, 20); c = a * x - b
                        q = f"จงแก้สมการเพื่อหาค่า x : <br><b style='font-size: 24px; color: #3498db;'>{a}x - {b} = {c}</b>"
                        sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ (ขั้นที่ 1):</b> กำจัด -{b} โดยนำ <b style='color: #27ae60;'>{b}</b> มาบวกเข้าทั้งสองข้าง</span><br><b style='color: #3498db;'>{a}x - {b}</b> <b style='color: #27ae60;'>+ {b}</b> = <b style='color: #3498db;'>{c}</b> <b style='color: #27ae60;'>+ {b}</b><br><b style='color: #3498db;'>{a}x</b> <span style='text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;'><span style='color: #3498db;'>- {b}</span> <span style='color: #27ae60;'>+ {b}</span></span> = <b>{c+b}</b><br><b>{a}x = {c+b}</b><br><br><span style='color: #2c3e50;'><b>วิธีทำ (ขั้นที่ 2):</b> กำจัด {a} ที่คูณอยู่ โดยนำ <b style='color: #27ae60;'>{a}</b> มาหารทั้งสองข้าง</span><br><div style='display: flex; align-items: center; margin: 10px 0;'><div style='text-align: center; margin-right: 10px;'><span style='border-bottom: 2px solid #000; padding: 0 5px; color: #3498db; font-weight: bold;'>{a}x</span><br><b style='color: #27ae60;'>{a}</b></div> <b>=</b> <div style='text-align: center; margin-left: 10px;'><span style='border-bottom: 2px solid #000; padding: 0 5px; color: #3498db; font-weight: bold;'>{c+b}</span><br><b style='color: #27ae60;'>{a}</b></div></div><div style='display: flex; align-items: center; margin: 10px 0;'><div style='text-align: center; margin-right: 10px;'><span style='border-bottom: 2px solid #000; padding: 0 5px; color: #3498db; font-weight: bold;'><span style='text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;'>{a}</span>x</span><br><b style='color: #27ae60;'><span style='text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;'>{a}</span></b></div> <b>=</b> <div style='text-align: center; margin-left: 10px;'><b>{x}</b></div></div><b>x = {x}</b>"

            elif "ชนิดของมุม" in sub_t:
                angle = random.choice([30, 45, 60, 90, 120, 135, 150, 180, 210, 270, 300])
                rad = math.radians(angle); cx, cy = 100, 100; r_line, r_arc = 70, 25
                line1 = f'<line x1="{cx}" y1="{cy}" x2="{cx+r_line}" y2="{cy}" stroke="#333" stroke-width="3" stroke-linecap="round"/>'
                end_x = cx + r_line * math.cos(rad); end_y = cy - r_line * math.sin(rad)
                line2 = f'<line x1="{cx}" y1="{cy}" x2="{end_x}" y2="{end_y}" stroke="#3498db" stroke-width="3" stroke-linecap="round"/>'
                if angle == 90: arc_svg = f'<polyline points="{cx+15},{cy} {cx+15},{cy-15} {cx},{cy-15}" fill="none" stroke="#e74c3c" stroke-width="2"/>'
                elif angle == 180: arc_svg = f'<path d="M {cx+r_arc} {cy} A {r_arc} {r_arc} 0 0 0 {cx-r_arc} {cy}" fill="none" stroke="#e74c3c" stroke-width="2"/>'
                else:
                    large_arc = 1 if angle > 180 else 0
                    arc_end_x = cx + r_arc * math.cos(rad); arc_end_y = cy - r_arc * math.sin(rad)
                    arc_svg = f'<path d="M {cx+r_arc} {cy} A {r_arc} {r_arc} 0 {large_arc} 0 {arc_end_x} {arc_end_y}" fill="none" stroke="#e74c3c" stroke-width="2"/>'
                text_r = r_arc + 15; text_rad = math.radians(angle / 2)
                text_x = cx + text_r * math.cos(text_rad); text_y = cy - text_r * math.sin(text_rad)
                angle_text = f'<text x="{text_x}" y="{text_y+5}" font-size="14" font-weight="bold" fill="#e74c3c" text-anchor="middle">{angle}°</text>'
                dot = f'<circle cx="{cx}" cy="{cy}" r="4" fill="#333"/>'
                svg = f'<div style="text-align: center; margin: 15px 0;"><svg width="150" height="150" viewBox="20 20 160 160">{line1}{line2}{arc_svg}{angle_text}{dot}</svg></div>'

                q = f"จากรูปภาพ มุมที่มีขนาด <b>{angle} องศา</b> เรียกว่ามุมชนิดใด? {svg}"
                if angle < 90: ans_type = "มุมแหลม"; explain = "เพราะมีขนาดมากกว่า 0 องศา แต่น้อยกว่า 90 องศา (แคบกว่ามุมฉาก)"
                elif angle == 90: ans_type = "มุมฉาก"; explain = "เพราะมีขนาดเท่ากับ 90 องศาพอดี (ตั้งฉาก)"
                elif angle < 180: ans_type = "มุมป้าน"; explain = "เพราะมีขนาดมากกว่า 90 องศา แต่น้อยกว่า 180 องศา (กว้างกว่ามุมฉาก แต่ไม่ถึงเส้นตรง)"
                elif angle == 180: ans_type = "มุมตรง"; explain = "เพราะมีขนาดเท่ากับ 180 องศาพอดี (เป็นเส้นตรง)"
                else: ans_type = "มุมกลับ"; explain = "เพราะมีขนาดมากกว่า 180 องศา แต่น้อยกว่า 360 องศา (มุมโค้งกลับด้านหลัง)"
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> {explain}<br>ตอบ:</span> <b>{ans_type}</b>"

            elif "ความยาวรอบรูป" in sub_t or ("พื้นที่" in sub_t and "สี่เหลี่ยม" in sub_t):
                is_peri = "ความยาวรอบรูป" in sub_t; is_square = random.choice([True, False])
                if is_square:
                    s = random.randint(5, 30) if is_peri else random.randint(5, 25)
                    svg = f"""<br><div style="text-align: center; margin: 10px 0;"><svg width="150" height="150"><rect x="25" y="25" width="100" height="100" fill="#e8f4f8" stroke="#2980b9" stroke-width="3"/><line x1="70" y1="20" x2="80" y2="30" stroke="#c0392b" stroke-width="2"/><line x1="70" y1="120" x2="80" y2="130" stroke="#c0392b" stroke-width="2"/><line x1="20" y1="70" x2="30" y2="80" stroke="#c0392b" stroke-width="2"/><line x1="120" y1="70" x2="130" y2="80" stroke="#c0392b" stroke-width="2"/><text x="75" y="18" font-size="16" font-family="Sarabun" font-weight="bold" fill="#333" text-anchor="middle">{s} ซม.</text></svg></div>"""
                    q = f"จากรูปภาพ จงหา{'ความยาวรอบรูป' if is_peri else 'พื้นที่'}ของ<b>รูปสี่เหลี่ยมจัตุรัส</b> {svg}"
                    if is_peri: ans = 4 * s; sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ความยาวรอบรูปสี่เหลี่ยมจัตุรัส = 4 × ความยาวด้าน<br>= 4 × {s}<br>ตอบ:</span> <b>{ans} เซนติเมตร</b>"
                    else: ans = s * s; sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> พื้นที่สี่เหลี่ยมจัตุรัส = ด้าน × ด้าน<br>= {s} × {s}<br>ตอบ:</span> <b>{ans:,} ตารางเซนติเมตร</b>"
                else:
                    w = random.randint(5, 20); l = random.randint(w + 2, 30)
                    svg = f"""<br><div style="text-align: center; margin: 10px 0;"><svg width="220" height="120"><rect x="20" y="20" width="140" height="80" fill="#e8f8f5" stroke="#16a085" stroke-width="3"/><polyline points="20,35 35,35 35,20" fill="none" stroke="#16a085" stroke-width="1.5"/><polyline points="160,35 145,35 145,20" fill="none" stroke="#16a085" stroke-width="1.5"/><text x="90" y="15" font-size="16" font-family="Sarabun" font-weight="bold" fill="#333" text-anchor="middle">{l} ซม.</text><text x="165" y="65" font-size="16" font-family="Sarabun" font-weight="bold" fill="#333" text-anchor="start">{w} ซม.</text></svg></div>"""
                    q = f"จากรูปภาพ จงหา{'ความยาวรอบรูป' if is_peri else 'พื้นที่'}ของ<b>รูปสี่เหลี่ยมผืนผ้า</b> {svg}"
                    if is_peri: ans = 2 * (w + l); sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ความยาวรอบรูปสี่เหลี่ยมผืนผ้า = 2 × (กว้าง + ยาว)<br>= 2 × ({w} + {l})<br>= 2 × {w+l}<br>ตอบ:</span> <b>{ans} เซนติเมตร</b>"
                    else: ans = w * l; sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> พื้นที่สี่เหลี่ยมผืนผ้า = กว้าง × ยาว<br>= {w} × {l}<br>ตอบ:</span> <b>{ans:,} ตารางเซนติเมตร</b>"

            elif "ไม้โปรแทรกเตอร์" in sub_t:
                angle = random.randint(15, 165); arm_rad = math.radians(angle)
                ax = 150 + 135 * math.cos(arm_rad); ay = 140 - 135 * math.sin(arm_rad); ticks_svg = ""
                for i in range(0, 181):
                    rad = math.radians(i); r_out = 120
                    if i % 10 == 0: r_in, stroke_w = 105, "1.5"
                    elif i % 5 == 0: r_in, stroke_w = 110, "1.2"
                    else: r_in, stroke_w = 115, "0.6"
                    tx1 = 150 + r_out * math.cos(rad); ty1 = 140 - r_out * math.sin(rad)
                    tx2 = 150 + r_in * math.cos(rad); ty2 = 140 - r_in * math.sin(rad)
                    ticks_svg += f'<line x1="{tx1}" y1="{ty1}" x2="{tx2}" y2="{ty2}" stroke="#333" stroke-width="{stroke_w}"/>'
                    if i % 10 == 0:
                        tx_text = 150 + 88 * math.cos(rad); ty_text = 140 - 88 * math.sin(rad)
                        ticks_svg += f'<text x="{tx_text}" y="{ty_text+4}" font-size="10" font-weight="bold" text-anchor="middle" fill="#333">{i}</text>'
                arc_r = 30; arc_x = 150 + arc_r * math.cos(arm_rad); arc_y = 140 - arc_r * math.sin(arm_rad)
                angle_arc = f'<path d="M 180 140 A 30 30 0 0 0 {arc_x} {arc_y}" fill="none" stroke="#e74c3c" stroke-width="2"/>'
                svg = f"""<br><div style="text-align: center;"><svg width="300" height="160"><path d="M 30 140 A 120 120 0 0 1 270 140" fill="#fdfdfd" stroke="#333" stroke-width="2"/><line x1="150" y1="140" x2="270" y2="140" stroke="#3498db" stroke-width="2"/><line x1="150" y1="140" x2="{ax}" y2="{ay}" stroke="#e74c3c" stroke-width="1.5"/>{angle_arc}<line x1="30" y1="140" x2="270" y2="140" stroke="#333" stroke-width="2"/>{ticks_svg}<circle cx="150" cy="140" r="4" fill="#e74c3c"/></svg></div>"""
                q = f"มุมที่แสดงบนไม้โปรแทรกเตอร์มีขนาดกี่องศา? {svg}"
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> สังเกตเส้นสีแดงชี้ตรงกับตัวเลขสเกลด้านในที่เลข {angle} พอดี<br>ตอบ:</span> <b>{angle} องศา</b>"

            else:
                a, b = random.randint(10, 50), random.randint(10, 50)
                q = f"จงหาผลลัพธ์ <br><div style='font-size: 20px; font-weight: bold; margin-top: 5px; color: #2c3e50;'>ประโยคสัญลักษณ์: {a} + {b} = {box_html}</div>"
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ตั้งบวกหลักหน่วยและหลักสิบให้ตรงกัน</span><br><b>ตอบ: {a + b}</b>"

            if q not in seen:
                seen.add(q); questions.append({"question": q, "solution": sol}); break
            attempts += 1
    return questions


# ==========================================
# 3. ฟังก์ชันสร้างหน้า HTML (แบบฝึกหัด/เฉลย) และ E-Book
# ==========================================
def create_page(grade, sub_t, questions, is_key=False):
    title = "เฉลยแบบฝึกหัด" if is_key else "แบบฝึกหัดคณิตศาสตร์"
    student_info = ""
    if not is_key:
        student_info = """
        <div style="text-align: right; margin-bottom: 20px; font-size: 18px;">
            <b>ชื่อ-สกุล</b>..................................................................................................................... <b>ชั้น</b>........................ <b>เลขที่</b>...................
        </div>
        """
        
    html = f"""<!DOCTYPE html><html lang="th"><head><meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css2?family=Sarabun&display=swap" rel="stylesheet">
    <style>
        /* 🖨️ ตั้งค่ากระดาษ A4 สำหรับปริ้นท์ */
        @page {{ size: A4; margin: 15mm; }}
        body {{ font-family: 'Sarabun', sans-serif; padding: 20px; line-height: 1.8; color: #333; }}
        .page-break {{ page-break-before: always; }}
        .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 20px; padding-bottom: 10px; }}
        .q-box {{ margin-bottom: 30px; padding: 15px; page-break-inside: avoid; border-bottom: 1px solid #eee; }}
        .ans-line {{ margin-top: 15px; border-bottom: 1px dotted #999; width: 80%; height: 30px; }}
        .sol-text {{ color: #333; font-size: 20px; display: inline-block; margin-top: 10px; line-height: 1.5; }}
    </style></head><body>
    <div class="header"><h2>{title} - {grade}</h2><p><b>เรื่อง:</b> {sub_t}</p></div>
    {student_info}"""
    
    for i, item in enumerate(questions, 1):
        if ("(แบบตั้งหลัก)" in sub_t and "สมการ" not in sub_t) or "หารยาว" in sub_t:
            html += f'<div class="q-box"><b>ข้อที่ {i}.</b><br>{item["solution"] if is_key else item["question"]}</div>'
        else:
            html += f'<div class="q-box"><b>ข้อที่ {i}.</b> {item["question"]}'
            if is_key: html += f'<br><div class="sol-text">{item["solution"]}</div>'
            else: html += '<div class="ans-line">ตอบ: </div>'
            html += '</div>'
    return html + "</body></html>"

# 🎨 ฟังก์ชันสร้างหน้าปก (Cover Page)
def generate_cover_html(grade, main_t, sub_t, num_q):
    return f"""<!DOCTYPE html><html lang="th"><head><meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap" rel="stylesheet">
    <style>
        @page {{ size: A4; margin: 0mm; }}
        body {{ font-family: 'Sarabun', sans-serif; margin: 0; padding: 0; background-color: #f4f6f7; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
        .cover-container {{ width: 210mm; height: 297mm; background: white; padding: 40px; box-sizing: border-box; text-align: center; position: relative; border: 15px solid #3498db; }}
        .title-box {{ margin-top: 80px; }}
        .title {{ font-size: 65px; color: #2c3e50; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); margin: 0; }}
        .grade-badge {{ font-size: 45px; background-color: #e74c3c; color: white; padding: 15px 50px; border-radius: 50px; display: inline-block; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.2); margin-top: 30px; }}
        .topic {{ font-size: 42px; color: #34495e; margin-top: 70px; font-weight: bold; }}
        .sub-topic {{ font-size: 32px; color: #7f8c8d; margin-top: 10px; }}
        .icons {{ font-size: 110px; margin: 60px 0; }}
        .details-badge {{ background-color: #2ecc71; color: white; display: inline-block; padding: 15px 40px; border-radius: 15px; font-size: 32px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .footer {{ position: absolute; bottom: 40px; left: 0; width: 100%; text-align: center; font-size: 22px; color: #95a5a6; border-top: 2px dashed #bdc3c7; padding-top: 20px; }}
    </style>
    </head><body>
    <div class="cover-container">
        <div class="title-box">
            <h1 class="title">แบบฝึกหัดคณิตศาสตร์</h1>
            <div class="grade-badge">ชั้น{grade}</div>
        </div>
        <div class="topic">เรื่อง: {sub_t}</div>
        <div class="sub-topic">(หมวดหมู่: {main_t})</div>
        <div class="icons">🧮 📏 📐 ✏️</div>
        <div class="details-badge">รวมทั้งหมด {num_q} ข้อ (พร้อมเฉลยละเอียด)</div>
        <div class="footer">ออกแบบเพื่อครูผู้สอนและนักเรียน | สื่อการเรียนรู้อัตโนมัติ (TPT Ready)</div>
    </div>
    </body></html>"""

# 🖨️ ฟังก์ชันดึงเฉพาะส่วน Body เพื่อนำมารวมร่าง (E-Book)
def extract_body(html_str):
    try:
        return html_str.split('<body>')[1].split('</body>')[0]
    except IndexError:
        return html_str

# ==========================================
# 4. สร้าง UI ของ Streamlit Web App
# ==========================================
st.sidebar.header("⚙️ การตั้งค่าใบงาน")
selected_grade = st.sidebar.selectbox("1. เลือกระดับชั้น:", list(curriculum_db.keys()))
selected_main = st.sidebar.selectbox("2. เลือกหัวข้อหลัก:", list(curriculum_db[selected_grade].keys()))
selected_sub = st.sidebar.selectbox("3. เลือกหัวข้อย่อย:", curriculum_db[selected_grade][selected_main])
num_input = st.sidebar.number_input("จำนวนข้อ:", min_value=1, max_value=100, value=10)

st.sidebar.markdown("---")
st.sidebar.markdown("**📚 ตัวเลือกการสร้าง E-Book**")
include_cover = st.sidebar.checkbox("🎨 สร้างหน้าปก (Cover Page)", value=True)

if st.sidebar.button("🚀 สร้างใบงาน", type="primary", use_container_width=True):
    with st.spinner("กำลังประมวลผลลอจิกคณิตศาสตร์และสร้างโจทย์..."):
        qs = generate_questions_logic(selected_grade, selected_main, selected_sub, num_input)
        
        # 1. สร้าง HTML แยกแต่ละส่วน
        html_w = create_page(selected_grade, selected_sub, qs, is_key=False)
        html_k = create_page(selected_grade, selected_sub, qs, is_key=True)
        html_cover = generate_cover_html(selected_grade, selected_main, selected_sub, num_input) if include_cover else ""
        
        # 2. รวมร่างเป็น E-Book เล่มเดียว (A4 Ready)
        ebook_body = ""
        if include_cover:
            ebook_body += extract_body(html_cover) + '\n<div class="page-break"></div>\n'
        ebook_body += extract_body(html_w) + '\n<div class="page-break"></div>\n'
        ebook_body += extract_body(html_k)
        
        full_ebook_html = f"""<!DOCTYPE html><html lang="th"><head><meta charset="utf-8">
        <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap" rel="stylesheet">
        <style>
            @page {{ size: A4; margin: 15mm; }}
            body {{ font-family: 'Sarabun', sans-serif; line-height: 1.8; color: #333; }}
            .page-break {{ page-break-before: always; }}
            .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 20px; padding-bottom: 10px; }}
            .q-box {{ margin-bottom: 30px; padding: 15px; page-break-inside: avoid; border-bottom: 1px solid #eee; }}
            .ans-line {{ margin-top: 15px; border-bottom: 1px dotted #999; width: 80%; height: 30px; }}
            .sol-text {{ color: #333; font-size: 20px; display: inline-block; margin-top: 10px; line-height: 1.5; }}
            /* Cover Styles for unified print */
            .cover-container {{ width: 100%; height: 260mm; background: white; padding: 40px; box-sizing: border-box; text-align: center; position: relative; border: 15px solid #3498db; margin: 0; }}
            .title-box {{ margin-top: 80px; }}
            .title {{ font-size: 65px; color: #2c3e50; font-weight: bold; margin: 0; }}
            .grade-badge {{ font-size: 45px; background-color: #e74c3c; color: white; padding: 15px 50px; border-radius: 50px; display: inline-block; font-weight: bold; margin-top: 30px; }}
            .topic {{ font-size: 42px; color: #34495e; margin-top: 70px; font-weight: bold; }}
            .sub-topic {{ font-size: 32px; color: #7f8c8d; margin-top: 10px; }}
            .icons {{ font-size: 110px; margin: 60px 0; }}
            .details-badge {{ background-color: #2ecc71; color: white; display: inline-block; padding: 15px 40px; border-radius: 15px; font-size: 32px; font-weight: bold; }}
            .footer {{ position: absolute; bottom: 40px; left: 0; width: 100%; text-align: center; font-size: 22px; color: #95a5a6; border-top: 2px dashed #bdc3c7; padding-top: 20px; }}
        </style></head><body>
        {ebook_body}
        </body></html>"""

        filename_base = f"{selected_grade}_{selected_sub}"
        st.session_state['ebook_html'] = full_ebook_html
        st.session_state['filename_base'] = f"{filename_base}_{int(time.time())}"
        
        # สร้าง ZIP สำหรับไฟล์แยก
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            if include_cover:
                zip_file.writestr(f"{filename_base}_0_Cover.html", html_cover.encode('utf-8'))
            zip_file.writestr(f"{filename_base}_1_Worksheet.html", html_w.encode('utf-8'))
            zip_file.writestr(f"{filename_base}_2_AnswerKey.html", html_k.encode('utf-8'))
            zip_file.writestr(f"{filename_base}_Full_EBook.html", full_ebook_html.encode('utf-8'))
        st.session_state['zip_data'] = zip_buffer.getvalue()

if 'ebook_html' in st.session_state:
    st.success("🎉 สร้างเล่ม E-Book และหน้าปกเสร็จสมบูรณ์! พร้อมนำไปขายแล้วครับ")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 🖨️ พิมพ์เป็น E-Book (คลิกเดียวจบ)")
        st.info("💡 **วิธีใช้ง่ายที่สุด:** โหลดไฟล์ด้านล่างนี้ เปิดใน Chrome แล้วกด **Ctrl+P** เลือก Save as PDF ระบบจะจัดหน้า A4 ให้อัตโนมัติ (หน้าปก + โจทย์ + เฉลย)")
        st.download_button(
            label="📄 ดาวน์โหลด Full E-Book (HTML สำหรับ Print)",
            data=st.session_state['ebook_html'],
            file_name=f"{st.session_state['filename_base']}_Full_EBook.html",
            mime="text/html",
            use_container_width=True
        )
        
    with col2:
        st.markdown("### 🗂️ ดาวน์โหลดไฟล์แยกทีละหน้า (Zip)")
        st.info("เหมาะสำหรับนำไปแก้ไขเพิ่มเติม หรือแยกปริ้นท์ทีละส่วน")
        st.download_button(
            label="📥 ดาวน์โหลดไฟล์แยก (ไฟล์ .zip)",
            data=st.session_state['zip_data'],
            file_name=f"{st.session_state['filename_base']}.zip",
            mime="application/zip",
            use_container_width=True
        )

    st.markdown("---")
    st.markdown("### 🚀 สร้างเป็นไฟล์ PDF โดยตรง (Backend Export)")
    if HAS_PDFKIT:
        if st.button("กดเพื่อ Export เป็นไฟล์ PDF ทันที"):
            with st.spinner("กำลังแปลงเป็น PDF... (อาจใช้เวลาสักครู่)"):
                try:
                    options = {
                        'page-size': 'A4',
                        'margin-top': '0mm',
                        'margin-right': '0mm',
                        'margin-bottom': '0mm',
                        'margin-left': '0mm',
                        'encoding': "UTF-8"
                    }
                    pdf_bytes = pdfkit.from_string(st.session_state['ebook_html'], False, options=options)
                    
                    b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                    pdf_display = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{st.session_state["filename_base"]}_EBook.pdf" style="text-decoration: none; padding: 10px 20px; background-color: #e74c3c; color: white; border-radius: 5px; font-weight: bold;">📥 คลิ๊กที่นี่เพื่อเซฟไฟล์ PDF</a>'
                    st.markdown(pdf_display, unsafe_allow_html=True)
                    st.success("✅ แปลง PDF สำเร็จแล้ว! กดปุ่มสีแดงด้านบนเพื่อเซฟไฟล์ได้เลย")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาดจากไลบรารี: {e}")
                    st.warning("⚠️ การแปลง PDF โดยตรงจำเป็นต้องติดตั้งโปรแกรม `wkhtmltopdf` ไว้ในเครื่อง แนะนำให้ใช้วิธี 'โหลดไฟล์ Full E-Book HTML' ด้านบน แล้วกดสั่ง Print เป็น PDF แทนครับ จะได้ผลลัพธ์เหมือนกัน 100%")
    else:
        st.warning("💡 ฟีเจอร์สร้าง PDF โดยตรง ต้องติดตั้งไลบรารี `pdfkit` (รัน `pip install pdfkit`) และโปรแกรม `wkhtmltopdf` ลงในเครื่องคอมพิวเตอร์ก่อนครับ")
        st.info("🔥 **แนะนำ:** ไม่ต้องติดตั้งให้ยุ่งยาก! คุณสามารถโหลดไฟล์ 'Full E-Book HTML' ด้านบน ไปเปิดด้วยเบราว์เซอร์ แล้วกด Print เป็น PDF ได้เลย ระบบจัดหน้า A4 ไว้ให้เป๊ะๆ แล้วครับ!")
else:
    st.info("👈 กรุณาตั้งค่าใบงานที่เมนูด้านซ้าย แล้วกดปุ่ม 'สร้างใบงาน'")
