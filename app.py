import streamlit as st
import random
import math
import zipfile
import io
import time

# ==========================================
# ตั้งค่าหน้าเพจ Web App
# ==========================================
st.set_page_config(page_title="เครื่องมือสร้างใบงานคณิตศาสตร์", page_icon="🖨️", layout="centered")
st.title("🖨️ เครื่องมือสร้างใบงานคณิตศาสตร์ ป.1 - ป.6")
st.markdown("ระบบสุ่มโจทย์อัตโนมัติ สำหรับคุณครูประถมศึกษา")

# ==========================================
# 1. ฐานข้อมูลหลักสูตร (Ultimate Master Database ป.1 - ป.6)
# ==========================================
curriculum_db = {
    "ป.1": {
        "จำนวนนับ 1 ถึง 100 และ 0": [
            "การนับทีละ 1", 
            "การนับทีละ 10", 
            "การอ่านและการเขียนตัวเลข",
            "การแสดงจำนวนในรูปความสัมพันธ์แบบส่วนย่อย-ส่วนรวม",
            "แบบรูปซ้ำของรูปเรขาคณิต", 
            "การบอกอันดับที่ (รถแข่ง)", 
            "หลัก ค่าของเลขโดดในแต่ละหลัก และรูปกระจาย", 
            "การเปรียบเทียบจำนวน (> <)",  
            "การเปรียบเทียบจำนวน (= ≠)", 
            "การเรียงลำดับจำนวน (น้อยไปมาก)", 
            "การเรียงลำดับจำนวน (มากไปน้อย)"
        ],
        "การบวก การลบ": [
            "การบวก (แบบตั้งหลัก)", 
            "การลบ (แบบตั้งหลัก)"
        ],
        "แผนภูมิรูปภาพ": [
            "การอ่านแผนภูมิรูปภาพ"
        ]
    },
    "ป.2": {
        "จำนวนนับไม่เกิน 1,000 และ 0": [
            "การนับทีละ 2 ทีละ 5 ทีละ 10 และทีละ 100", 
            "การอ่านและการเขียนตัวเลข",
            "จำนวนคู่ จำนวนคี่", 
            "หลัก ค่าของเลขโดด และรูปกระจาย", 
            "การเปรียบเทียบจำนวน (> <)",
            "การเรียงลำดับจำนวน (น้อยไปมาก)", 
            "การเรียงลำดับจำนวน (มากไปน้อย)"
        ],
        "เวลาและการวัด": [
            "การบอกเวลาเป็นนาฬิกาและนาที", 
            "การอ่านน้ำหนักจากเครื่องชั่งสปริง"
        ],
        "การบวก ลบ คูณ หาร": [
            "การบวก (แบบตั้งหลัก)", 
            "การลบ (แบบตั้งหลัก)", 
            "การคูณ (แบบตั้งหลัก)", 
            "การหารพื้นฐาน"
        ],
        "แผนภูมิรูปภาพ": [
            "การอ่านแผนภูมิรูปภาพ"
        ]
    },
    "ป.3": {
        "จำนวนนับและเศษส่วน": [
            "การอ่าน การเขียนตัวเลข", 
            "หลัก ค่าของเลขโดด และรูปกระจาย", 
            "การเปรียบเทียบจำนวน (> <)",
            "การเรียงลำดับจำนวน (น้อยไปมาก)", 
            "การเรียงลำดับจำนวน (มากไปน้อย)",
            "การอ่านและเขียนเศษส่วน", 
            "การบวกลบเศษส่วน (ตัวส่วนเท่ากัน)"
        ],
        "เวลา เงิน และการวัด": [
            "การบอกเวลาเป็นนาฬิกาและนาที", 
            "การบอกจำนวนเงินทั้งหมด", 
            "การอ่านน้ำหนักจากเครื่องชั่งสปริง"
        ],
        "การบวก ลบ คูณ หาร": [
            "การบวก (แบบตั้งหลัก)", 
            "การลบ (แบบตั้งหลัก)", 
            "การคูณ (แบบตั้งหลัก)", 
            "การหารยาว"
        ],
        "แผนภูมิรูปภาพ": [
            "การอ่านแผนภูมิรูปภาพ"
        ]
    },
    "ป.4": {
        "จำนวนนับที่มากกว่า 100,000": [
            "การอ่านและการเขียนตัวเลข", 
            "หลัก ค่าประจำหลัก และรูปกระจาย", 
            "การเปรียบเทียบและเรียงลำดับ", 
            "ค่าประมาณเป็นจำนวนเต็มสิบ เต็มร้อย เต็มพัน"
        ],
        "การบวก ลบ คูณ หาร": [
            "การบวก (แบบตั้งหลัก)", 
            "การลบ (แบบตั้งหลัก)", 
            "การหารยาว"
        ],
        "เศษส่วนและทศนิยม": [
            "แปลงเศษเกินเป็นจำนวนคละ", 
            "การอ่านและการเขียนทศนิยม"
        ],
        "เรขาคณิตและการวัด": [
            "การวัดขนาดของมุม (ไม้โปรแทรกเตอร์)"
        ]
    },
    "ป.5": {
        "เศษส่วน": [
            "การบวกและการลบเศษส่วน", 
            "การคูณและการหารเศษส่วน"
        ],
        "ทศนิยม": [
            "การบวกและการลบทศนิยม", 
            "การคูณทศนิยม"
        ],
        "ร้อยละและเปอร์เซ็นต์": [
            "การเขียนเศษส่วนในรูปร้อยละ"
        ]
    },
    "ป.6": {
        "ตัวประกอบของจำนวนนับ": [
            "การหา ห.ร.ม.", 
            "การหา ค.ร.น."
        ],
        "อัตราส่วนและร้อยละ": [
            "โจทย์ปัญหาร้อยละ"
        ],
        "สมการ": [
            "การแก้สมการเบื้องต้น"
        ]
    }
}

# ==========================================
# 🟢 ฟังก์ชันช่วย 1: สร้างตารางตั้งหลักเลข
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
                if carry > 0 and i > 0: top_marks[i-1] = str(carry)
        elif op == '-':
            a_chars, b_chars = list(str_a), list(str_b)
            a_digits = [int(c) if c.strip() else 0 for c in a_chars]
            b_digits = [int(c) if c.strip() else 0 for c in b_chars]
            for i in range(num_len - 1, -1, -1):
                if a_digits[i] < b_digits[i]:
                    for j in range(i-1, -1, -1):
                        if a_digits[j] > 0 and str_a[j].strip() != "":
                            strike[j] = True; a_digits[j] -= 1; top_marks[j] = str(a_digits[j])
                            for k in range(j+1, i):
                                strike[k] = True; a_digits[k] = 9; top_marks[k] = "9"
                            strike[i] = True; a_digits[i] += 10; top_marks[i] = str(a_digits[i])
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

    res_tds = ""
    if is_key and result is not None:
        str_r = str(result).rjust(num_len, " ")
        res_tds = "".join([f'<td style="width: 35px; text-align: center; color: red; font-weight: bold; height: 45px; vertical-align: bottom;">{str_r[i].strip()}</td>' for i in range(num_len)])
    else:
        res_tds = "".join([f'<td style="width: 35px; height: 45px;"></td>' for _ in range(num_len)])

    return f"""
    <div style="display: inline-block; font-family: 'Sarabun', sans-serif; font-size: 38px; line-height: 1.1; margin: 20px;">
        <table style="border-collapse: collapse; margin-left: auto; margin-right: auto;">
            <tr><td style="width: 20px;"></td>{a_tds}<td style="width: 50px; text-align: center; vertical-align: middle;" rowspan="2">{op}</td></tr>
            <tr><td></td>{b_tds}</tr>
            <tr><td></td>{res_tds}<td></td></tr>
            <tr><td></td><td colspan="{num_len}" style="border-bottom: 6px double #000; height: 10px;"></td><td></td></tr>
        </table>
    </div>
    """

# ==========================================
# 🟢 ฟังก์ชันช่วย 2: วาดเศษส่วนและจำนวนคละ
# ==========================================
def generate_fraction_html(num, den):
    return f"""
    <div style="display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; margin: 0 8px; font-family: 'Sarabun', sans-serif;">
        <span style="font-size: 26px; font-weight: bold; border-bottom: 3px solid #000; padding: 0 5px; line-height: 1.1;">{num}</span>
        <span style="font-size: 26px; font-weight: bold; padding: 0 5px; line-height: 1.1;">{den}</span>
    </div>
    """

def generate_mixed_number_html(whole, num, den):
    return f"""
    <div style="display: inline-flex; align-items: center; vertical-align: middle; margin: 0 8px; font-family: 'Sarabun', sans-serif;">
        <span style="font-size: 32px; font-weight: bold; margin-right: 5px; color: red;">{whole}</span>
        <div style="display: inline-flex; flex-direction: column; align-items: center;">
            <span style="font-size: 26px; font-weight: bold; border-bottom: 3px solid red; padding: 0 5px; line-height: 1.1; color: red;">{num}</span>
            <span style="font-size: 26px; font-weight: bold; padding: 0 5px; line-height: 1.1; color: red;">{den}</span>
        </div>
    </div>
    """

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

# ==========================================
# 🟢 ฟังก์ชันช่วย 3, 4, 5 (หารสั้น, ทศนิยม, หารยาว)
# ==========================================
def generate_short_division_html(a, b, mode="ห.ร.ม."):
    factors = []
    ca, cb = a, b
    steps_html = ""
    while True:
        found = False
        for i in range(2, min(ca, cb) + 1):
            if ca % i == 0 and cb % i == 0:
                steps_html += f"<tr><td style='text-align: right; padding-right: 10px; font-weight: bold; color: red;'>{i}</td><td style='border-left: 2px solid #000; border-bottom: 2px solid #000; padding: 5px 15px; text-align: center;'>{ca}</td><td style='border-bottom: 2px solid #000; padding: 5px 15px; text-align: center;'>{cb}</td></tr>"
                factors.append(i); ca //= i; cb //= i; found = True; break
        if not found: break
    
    if not factors:
        return f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ไม่มีตัวประกอบร่วมที่หารลงตัวทั้งคู่</span><br><b>{mode} = 1</b>" if mode=="ห.ร.ม." else f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ไม่มีตัวประกอบร่วม</span><br><b>ค.ร.น. = {a} × {b} = {a*b}</b>"

    steps_html += f"<tr><td></td><td style='padding: 5px 15px; text-align: center;'>{ca}</td><td style='padding: 5px 15px; text-align: center;'>{cb}</td></tr>"
    table = f"<table style='margin: 10px 0; font-size: 24px; border-collapse: collapse; color: #333;'>{steps_html}</table>"
    
    if mode == "ห.ร.ม.":
        ans = math.prod(factors)
        calc_str = " × ".join(map(str, factors))
        sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ (หารสั้น):</b></span>{table}<span style='color: #2c3e50;'><b>ห.ร.ม.</b> คือนำตัวหารด้านหน้ามาคูณกัน:</span><br>= {calc_str}<br>= <b>{ans}</b>"
    else:
        ans = math.prod(factors) * ca * cb
        calc_str = " × ".join(map(str, factors + [ca, cb]))
        sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ (หารสั้น):</b></span>{table}<span style='color: #2c3e50;'><b>ค.ร.น.</b> คือนำตัวหารและผลลัพธ์บรรทัดสุดท้ายมาคูณกัน (รูปตัว L):</span><br>= {calc_str}<br>= <b>{ans}</b>"
    return sol

def generate_decimal_vertical_html(a, b, op):
    str_a, str_b = f"{a:.2f}", f"{b:.2f}"
    ans = a + b if op == '+' else round(a - b, 2)
    str_ans = f"{ans:.2f}"
    max_len = max(len(str_a), len(str_b), len(str_ans))
    str_a, str_b, str_ans = str_a.rjust(max_len, " "), str_b.rjust(max_len, " "), str_ans.rjust(max_len, " ")
    a_tds = "".join([f"<td style='width: 25px; text-align: center;'>{c}</td>" for c in str_a])
    b_tds = "".join([f"<td style='width: 25px; text-align: center; border-bottom: 2px solid #000;'>{c}</td>" for c in str_b])
    ans_tds = "".join([f"<td style='width: 25px; text-align: center; color: red; font-weight: bold;'>{c}</td>" for c in str_ans])
    return f"""
    <div style="display: inline-block; font-family: 'Sarabun', sans-serif; font-size: 28px; line-height: 1.2; margin: 10px 20px;">
        <table style="border-collapse: collapse;">
            <tr><td style="width: 20px;"></td>{a_tds}<td style="padding-left: 15px;">{op}</td></tr>
            <tr><td></td>{b_tds}<td></td></tr>
            <tr><td></td>{ans_tds}<td></td></tr>
            <tr><td></td><td colspan="{max_len}" style="border-bottom: 4px double #000;"></td><td></td></tr>
        </table>
    </div>
    """

def generate_long_division_step_by_step_html(divisor, dividend, is_key=False):
    div_str = str(dividend)
    div_len = len(div_str)
    equation_html = f"<div style='font-size: 24px; font-weight: bold; margin-bottom: 15px;'>{dividend:,} ÷ {divisor} = ?</div>"
    
    if not is_key:
        div_tds_list = []
        for i, c in enumerate(div_str):
            left_border = "border-left: 3px solid #000;" if i == 0 else ""
            div_tds_list.append(f'<td style="width: 35px; text-align: center; border-top: 3px solid #000; {left_border} font-size: 38px;">{c}</td>')
        div_tds_list.append('<td style="width: 35px;"></td>')
        return f"{equation_html}<div style=\"display: inline-block; font-family: 'Sarabun', sans-serif; line-height: 1.2; margin: 10px 20px;\"><table style=\"border-collapse: collapse;\"><tr><td style=\"border: none; text-align: right; padding-right: 12px; vertical-align: bottom; font-size: 38px;\">{divisor}</td>{''.join(div_tds_list)}</tr></table></div><br>{'<br>' * 12}"

    steps = []; current_val_str = ""; ans_str = ""; has_started = False
    
    for i, digit in enumerate(div_str):
        current_val_str += digit
        current_val = int(current_val_str)
        q = current_val // divisor
        mul_res = q * divisor
        rem = current_val - mul_res
        
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
                        strik[idx_b] = True; c_dig[idx_b] += 10; top_m[idx_b] = str(c_dig[idx_b])
                        break
                        
        steps.append({'mul_res': mul_res, 'rem': rem, 'col_index': i, 'top_m': top_m, 'strik': strik})
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
            mark, is_strik = s0['top_m'][t_idx], s0['strik'][t_idx]
            if is_strik: td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span style="text-decoration: line-through; text-decoration-color: red; text-decoration-thickness: 2px;">{c}</span></div>'
            elif mark: td_content = f'<div style="position: relative;"><span style="position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 20px; color: red; font-weight: bold;">{mark}</span><span>{c}</span></div>'
        div_tds_list.append(f'<td style="width: 35px; height: 50px; vertical-align: bottom; text-align: center; border-top: 3px solid #000; {left_border} font-size: 38px;">{td_content}</td>')
    div_tds_list.append('<td style="width: 35px;"></td>') 

    html = f"{equation_html}<div style=\"display: inline-block; font-family: 'Sarabun', sans-serif; line-height: 1.2; margin: 10px 20px;\"><table style=\"border-collapse: collapse;\"><tr><td style=\"border: none;\"></td>{''.join(ans_tds_list)}</tr><tr><td style=\"border: none; text-align: right; padding-right: 12px; vertical-align: bottom; font-size: 38px;\">{divisor}</td>{''.join(div_tds_list)}</tr>"

    for idx, step in enumerate(steps):
        mul_res_str = str(step['mul_res'])
        pad_len = step['col_index'] + 1 - len(mul_res_str)
        mul_tds = ""
        for i in range(div_len + 1):
            if i >= pad_len and i <= step['col_index']:
                digit_idx = i - pad_len
                border_b = "border-bottom: 2px solid #000;" if i <= step['col_index'] else ""
                mul_tds += f'<td style="width: 35px; height: 50px; vertical-align: bottom; text-align: center; font-size: 38px; {border_b}">{mul_res_str[digit_idx]}</td>'
            elif i == step['col_index'] + 1: mul_tds += '<td style="width: 35px; text-align: center; font-size: 38px; color: #333; position: relative; top: -24px;">-</td>'
            else: mul_tds += '<td style="width: 35px;"></td>'
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
                    mark, is_strik = next_step['top_m'][t_idx], next_step['strik'][t_idx]
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
    int_part = parts[0]
    dec_part = parts[1] if len(parts) > 1 else ""
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

# ==========================================
# 2. ฟังก์ชันสมองกลสร้างโจทย์และกราฟิก 
# ==========================================
def generate_questions_logic(grade, main_t, sub_t, num_q):
    questions = []
    seen = set()
    limit_map = {"ป.1": 100, "ป.2": 1000, "ป.3": 100000, "ป.4": 1000000, "ป.5": 9000000, "ป.6": 9000000}
    limit = limit_map.get(grade, 100)

    for _ in range(num_q):
        q, sol = "", ""
        attempts = 0
        while attempts < 300:
            
            # --- หมวดตั้งหลัก ---
            if sub_t == "การบวก (แบบตั้งหลัก)":
                if grade == "ป.1":
                    tens_a = random.randint(1, 9); units_a = random.randint(0, 8)
                    b = random.randint(1, 9 - units_a); a = (tens_a * 10) + units_a
                elif grade in ["ป.4", "ป.5", "ป.6"]:
                    a = random.randint(10000, limit // 2); b = random.randint(10000, limit // 2)
                else:
                    a = random.randint(10, limit - 20); b = random.randint(1, limit - a - 1)
                res = a + b
                q = generate_vertical_table_html(a, b, '+', is_key=False)
                sol = generate_vertical_table_html(a, b, '+', result=res, is_key=True)

            elif sub_t == "การลบ (แบบตั้งหลัก)":
                if grade == "ป.1":
                    tens_a = random.randint(1, 9); units_a = random.randint(1, 9)
                    b = random.randint(1, units_a); a = (tens_a * 10) + units_a
                elif grade in ["ป.4", "ป.5", "ป.6"]:
                    a = random.randint(100000, limit - 1); b = random.randint(10000, a - 1)
                else:
                    a = random.randint(10, limit - 1); b = random.randint(1, a - 1)
                res = a - b
                q = generate_vertical_table_html(a, b, '-', is_key=False)
                sol = generate_vertical_table_html(a, b, '-', result=res, is_key=True)

            elif sub_t == "การคูณ (แบบตั้งหลัก)":
                a = random.randint(100, 999); b = random.randint(2, 9)
                res = a * b
                q = generate_vertical_table_html(a, b, '×', is_key=False)
                sol = generate_vertical_table_html(a, b, '×', result=res, is_key=True)

            # --- หมวดกราฟิก ป.1-ป.3 (เพิ่มคำอธิบายวิธีคิด) ---
            elif "ส่วนย่อย-ส่วนรวม" in sub_t:
                total = random.randint(5, 20); p1 = random.randint(1, total - 1); p2 = total - p1
                miss = random.choice(['t', 'p1', 'p2'])
                svg_t = f"""<br><div style="text-align: center;"><svg width="200" height="160"><line x1="100" y1="40" x2="50" y2="120" stroke="#333" stroke-width="2"/><line x1="100" y1="40" x2="150" y2="120" stroke="#333" stroke-width="2"/><circle cx="100" cy="40" r="28" fill="#ffffff" stroke="#333" stroke-width="2"/><circle cx="50" cy="120" r="28" fill="#ffffff" stroke="#333" stroke-width="2"/><circle cx="150" cy="120" r="28" fill="#ffffff" stroke="#333" stroke-width="2"/><text x="100" y="47" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='t' else "#333"}">{{t}}</text><text x="50" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='p1' else "#333"}">{{p1}}</text><text x="150" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='p2' else "#333"}">{{p2}}</text></svg></div>"""
                q = f"จงหาตัวเลขที่หายไป (?) : " + svg_t.format(t="?" if miss=='t' else total, p1="?" if miss=='p1' else p1, p2="?" if miss=='p2' else p2)
                
                # อธิบายวิธีคิด
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
                
                # อธิบายวิธีคิด
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
                seq = [keys[pt[i % len(pt)]] for i in range(12)]
                slen = random.randint(5, 8) 
                html = "<br><div style='margin-top:10px; text-align:center;'>" + "".join([f'<svg width="30" height="30" style="vertical-align: middle; margin: 0 5px;">{shapes[seq[i]]}</svg>' for i in range(slen)]) + '<span style="display:inline-block; width:30px; height:30px; border-bottom:2px dashed #000; margin: 0 5px;"></span></div>'
                q = f"รูปที่หายไปคือรูปใด? {html}"
                
                # อธิบายวิธีคิด
                pattern_len = len(set(pt))
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> สังเกตจะพบว่ารูปภาพมีการเรียงซ้ำกันเป็นชุด ชุดละ {pattern_len} รูป เมื่อนับลำดับต่อมาเรื่อยๆ รูปที่หายไปคือ:</span><br><br><svg width='30' height='30' style='vertical-align: middle;'>{shapes[seq[slen]]}</svg>"

            elif "นาฬิกา" in sub_t:
                h = random.randint(1, 12); m = random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
                am = m * 6; ah = (h % 12) * 30 + (m / 60) * 30
                ticks = "".join([f'<line x1="60" y1="15" x2="60" y2="20" stroke="#333" stroke-width="2" transform="rotate({i*30} 60 60)" />' for i in range(12)])
                svg = f"""<br><div style="text-align: center; margin-top: 15px; margin-bottom: 5px;"><svg width="120" height="120"><circle cx="60" cy="60" r="50" fill="#fdfdfd" stroke="#333" stroke-width="3"/>{ticks}<line x1="60" y1="60" x2="60" y2="35" stroke="#e74c3c" stroke-width="4" stroke-linecap="round" transform="rotate({ah} 60 60)" /><line x1="60" y1="60" x2="60" y2="20" stroke="#3498db" stroke-width="3" stroke-linecap="round" transform="rotate({am} 60 60)" /><circle cx="60" cy="60" r="4" fill="#333"/></svg></div>"""
                day = random.choice(["เวลากลางวัน", "เวลากลางคืน"])
                q = f"หากเป็น <b>{day}</b> จะอ่านเวลาได้กี่นาฬิกา กี่นาที? {svg}"
                ans_h = h + 12 if day == "เวลากลางวัน" and 1 <= h <= 5 else (h + 12 if day == "เวลากลางคืน" and 6 <= h <= 11 else (0 if day == "เวลากลางคืน" and h == 12 else h))
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> เข็มสั้นชี้ระหว่างเลข {h} กับ {h+1 if h<12 else 1} (บอกชั่วโมง) และเข็มยาวชี้ที่เลข {m//5} (บอกนาทีคือ {m} นาที)<br>เวลา{day} จึงอ่านได้</span> <b>{ans_h:02d}.{m:02d} น.</b>"

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
                money_svg += "</div>"
                q = f"จากภาพ มีเงินทั้งหมดกี่บาท? {money_svg}"
                sol = "<br><span style='color: #2c3e50;'><b>วิธีทำ:</b><br>"
                if b100 > 0: sol += f"แบงก์ 100 บาท {b100} ใบ = {b100*100} บาท<br>"
                if b50 > 0: sol += f"แบงก์ 50 บาท {b50} ใบ = {b50*50} บาท<br>"
                if b20 > 0: sol += f"แบงก์ 20 บาท {b20} ใบ = {b20*20} บาท<br>"
                if c10 > 0: sol += f"เหรียญ 10 บาท {c10} เหรียญ = {c10*10} บาท<br>"
                sol += f"นำมาบวกกันทั้งหมดจะได้เงินรวม</span> <b>{total:,} บาท</b>"

            elif "เครื่องชั่งสปริง" in sub_t:
                weight = random.randint(1, 5); angle = -150 + (weight * 60)
                scale_svg = f"""<br><div style="text-align: center; margin-top: 15px; margin-bottom: 5px;"><svg width="150" height="150"><rect x="25" y="20" width="100" height="110" rx="10" fill="#f1f2f6" stroke="#333" stroke-width="3"/><circle cx="75" cy="75" r="40" fill="#fff" stroke="#333" stroke-width="2"/><text x="75" y="47" font-size="10" font-weight="bold" text-anchor="middle">0</text><text x="105" y="65" font-size="10" font-weight="bold" text-anchor="middle">1</text><text x="100" y="100" font-size="10" font-weight="bold" text-anchor="middle">2</text><text x="75" y="112" font-size="10" font-weight="bold" text-anchor="middle">3</text><text x="50" y="100" font-size="10" font-weight="bold" text-anchor="middle">4</text><text x="45" y="65" font-size="10" font-weight="bold" text-anchor="middle">5</text><line x1="75" y1="75" x2="75" y2="45" stroke="#e74c3c" stroke-width="3" stroke-linecap="round" transform="rotate({angle} 75 75)" /><circle cx="75" cy="75" r="4" fill="#333"/><path d="M 50 20 L 40 5 L 110 5 L 100 20 Z" fill="#bdc3c7" stroke="#333" stroke-width="2"/></svg></div>"""
                q = f"จากหน้าปัดเครื่องชั่งสปริง สินค้ามีน้ำหนักกี่กิโลกรัม? {scale_svg}"
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ดูที่ปลายเข็มสีแดงบนหน้าปัดชี้ตรงกับเลข {weight} พอดี<br>ดังนั้น สินค้ามีน้ำหนัก</span> <b>{weight} กิโลกรัม</b>"

            elif "แผนภูมิรูปภาพ" in sub_t:
                items = [("🍎 แอปเปิล", "🍎"), ("🍊 ส้ม", "🍊"), ("🍌 กล้วย", "🍌"), ("🍓 องุ่น", "🍓")]
                selected = random.sample(items, 3)
                multiplier = 1 if grade == "ป.1" else random.choice([2, 5])
                counts = [random.randint(1, 5), random.randint(1, 5), random.randint(1, 5)]
                table_html = f"""<br><div style='margin-top:10px; width: 80%; border: 2px solid #333; border-collapse: collapse;'><div style='background-color: #f1f2f6; border-bottom: 2px solid #333; text-align: center; padding: 5px; font-weight: bold;'>จำนวนผลไม้ที่ร้านค้าขายได้</div>"""
                for i in range(3): table_html += f"<div style='display: flex; border-bottom: 1px solid #ccc;'><div style='width: 30%; border-right: 1px solid #ccc; padding: 5px; font-weight: bold;'>{selected[i][0]}</div><div style='width: 70%; padding: 5px; font-size: 18px;'>{''.join([selected[i][1]] * counts[i])}</div></div>"
                table_html += f"<div style='background-color: #fdfdfd; text-align: center; padding: 5px; font-weight: bold; color: #e74c3c;'>กำหนดให้ 1 รูปภาพ แทนผลไม้ {multiplier} ผล</div></div>"
                q = f"จากแผนภูมิ ขายผลไม้ 3 ชนิดรวมกันกี่ผล? {table_html}"
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> นับรูปผลไม้ทั้งหมดรวมกันได้ {sum(counts)} รูปภาพ<br>และกำหนดให้ 1 รูปภาพ แทนผลไม้ {multiplier} ผล<br>นำ {sum(counts)} × {multiplier} =</span> <b>{sum(counts) * multiplier} ผล</b>"

            # --- หมวดการนับ เรียงลำดับ เปรียบเทียบ ---
            elif "การนับทีละ" in sub_t:
                is_10 = "10" in sub_t; is_1 = "1" in sub_t; is_2 = "2" in sub_t
                step = 10 if is_10 else (1 if is_1 else random.choice([2, 5, 10, 100]))
                inc = random.choice([True, False])
                st_val = random.randint(10, 500)
                seq = [st_val, st_val+step, st_val+2*step, st_val+3*step] if inc else [st_val+3*step, st_val+2*step, st_val+step, st_val]
                idx = random.randint(0, 3)
                ans_str = f"{seq[idx]:,}"
                q = f"จงเติมตัวเลขที่หายไปในแบบรูป : {', '.join([f'{s:,}' if i != idx else '_____' for i, s in enumerate(seq)])}"
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> สังเกตความต่างของตัวเลข พบว่าแบบรูปมีการ{'นับเพิ่มขึ้น' if inc else 'นับลดลง'}ทีละ {step}<br>ดังนั้น ตัวเลขที่หายไปคือ</span> <b>{ans_str}</b>"

            elif "เปรียบเทียบจำนวน" in sub_t:
                is_eq = "=" in sub_t
                a = random.randint(10, limit); b = random.randint(10, limit)
                if is_eq and random.choice([True, False]): b = a
                else:
                    while a == b: b = random.randint(10, limit)
                
                sign = ""
                if is_eq: sign = "=" if a == b else "≠"
                else: sign = ">" if a > b else "<"
                
                q = f"จงเติมเครื่องหมาย {'= หรือ ≠' if is_eq else '> หรือ <'} ลงในช่องว่าง: {a:,} _____ {b:,}"
                comp_text = "มีค่าเท่ากับ" if a==b else ("มากกว่า" if a>b else "น้อยกว่า")
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> เปรียบเทียบค่าทีละหลักจากซ้ายไปขวา จะพบว่า {a:,} {comp_text} {b:,}<br>ตอบ: </span> <b>{sign}</b>"

            elif "เรียงลำดับจำนวน" in sub_t:
                nums = random.sample(range(10, limit), 4)
                is_asc = "น้อยไปมาก" in sub_t if "น้อยไปมาก" in sub_t else random.choice([True, False])
                q = f"จงเรียงลำดับจำนวนต่อไปนี้จาก {'น้อยไปมาก' if is_asc else 'มากไปน้อย'}: {', '.join(f'{x:,}' for x in nums)}"
                res = sorted(nums, reverse=not is_asc)
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> เปรียบเทียบค่าทีละจำนวนและเรียงจาก{'น้อยไปหามาก' if is_asc else 'มากไปหาน้อย'}<br>ตอบ: </span> <b>{', '.join(f'{x:,}' for x in res)}</b>"

            elif "รูปกระจาย" in sub_t:
                n = random.randint(100, limit-1)
                parts = [f"{int(d)*(10**(len(str(n))-1-i)):,}" for i,d in enumerate(str(n)) if d != '0']
                q = f"จงเขียน <b>{n:,}</b> ในรูปกระจาย"
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> แยกตัวเลขตามค่าประจำหลักจะได้:<br></span><b>{' + '.join(parts)}</b>"
                
            elif "จำนวนคู่" in sub_t:
                n = random.randint(10, limit)
                q = f"จำนวน <b>{n:,}</b> เป็นจำนวนคู่ หรือ จำนวนคี่?"
                is_even = (n % 2 == 0)
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ดูที่หลักหน่วยคือเลข {n%10} ซึ่ง{'หารด้วย 2 ลงตัว' if is_even else 'หารด้วย 2 ไม่ลงตัว'}<br>ดังนั้นจึงเป็น</span> <b>{'จำนวนคู่' if is_even else 'จำนวนคี่'}</b>"

            elif "เขียนตัวเลข" in sub_t:
                if grade in ["ป.1", "ป.2", "ป.3"]:
                    n = random.randint(11, limit-1)
                    q = f"จงเขียนตัวเลขฮินดูอารบิก <b>{n:,}</b> ให้เป็นตัวเลขไทย"
                    sol = f"<b>{n:,}</b>".translate(str.maketrans('0123456789', '๐๑๒๓๔๕๖๗๘๙'))
                else:
                    n = random.randint(100000, 9999999)
                    q = f"จงเขียนตัวเลข <b>{n:,}</b> ให้เป็นตัวหนังสือภาษาไทย"
                    sol = f"<b>{generate_thai_number_text(str(n))}</b>"

            # --- หมวดประถมปลาย (ทศนิยม เศษส่วน สมการ เรขาคณิต) ---
            elif "ค่าประมาณ" in sub_t:
                n = random.randint(1111, 99999); ptype = random.choice(["เต็มสิบ", "เต็มร้อย", "เต็มพัน"])
                if ptype == "เต็มสิบ":
                    ans = ((n + 5) // 10) * 10
                    chk_d = n % 10; chk_p = "หลักหน่วย"
                elif ptype == "เต็มร้อย":
                    ans = ((n + 50) // 100) * 100
                    chk_d = (n // 10) % 10; chk_p = "หลักสิบ"
                else:
                    ans = ((n + 500) // 1000) * 1000
                    chk_d = (n // 100) % 10; chk_p = "หลักร้อย"
                
                action = "ปัดขึ้น" if chk_d >= 5 else "ปัดทิ้ง"
                q = f"จงหาค่าประมาณเป็นจำนวน<b>{ptype}</b> ของ {n:,}"
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ประมาณเป็นจำนวน{ptype} ให้พิจารณาตัวเลขใน {chk_p} ซึ่งก็คือเลข <b>{chk_d}</b><br>ตามกฎแล้วต้องทำการ <b>{action}</b> จะได้เป็น:</span> <b>{ans:,}</b>"

            elif "หารยาว" in sub_t:
                divisor = random.randint(2, 12); quotient = random.randint(100, 999); dividend = divisor * quotient
                q = generate_long_division_step_by_step_html(divisor, dividend, is_key=False)
                sol = generate_long_division_step_by_step_html(divisor, dividend, is_key=True)

            elif "เศษเกินเป็นจำนวนคละ" in sub_t:
                den = random.randint(3, 12)
                num = random.randint(den + 1, den * 5)
                while num % den == 0: num = random.randint(den + 1, den * 5)
                frac_html = generate_fraction_html(num, den)
                q = f"จงเขียนเศษเกินต่อไปนี้ให้อยู่ในรูปจำนวนคละ : <br>{frac_html}"
                
                w, r = num // den, num % den
                g = math.gcd(r, den)
                
                mixed_raw = generate_mixed_number_html(w, r, den)
                
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> นำตัวเศษตั้ง หารด้วยตัวส่วน<br>จะได้ <b>{num} ÷ {den} = {w} เศษ {r}</b><br>"
                sol += f"เขียนเป็นจำนวนคละโดยให้ <b>{w}</b> เป็นจำนวนเต็ม และ <b>{r}</b> เป็นเศษ: </span><br><br>{mixed_raw}"

                if g > 1:
                    sim_r, sim_den = r // g, den // g
                    mixed_sim = generate_mixed_number_html(w, sim_r, sim_den)
                    sol += f"<br><br><span style='color: #2c3e50;'><i>*ทอนเป็นเศษส่วนอย่างต่ำได้ (ใช้แม่ {g} หารเศษและส่วน):</i></span><br><br>{mixed_sim}"
                
            elif "อ่านและเขียนเศษส่วน" in sub_t:
                den = random.randint(3, 12); num = random.randint(1, den - 1)
                frac_html = generate_fraction_html(num, den)
                q = f"จงอ่านเศษส่วนต่อไปนี้ : <br>{frac_html}"
                sol = f"<b>เศษ {num} ส่วน {den}</b>"

            elif "บวกลบเศษส่วน" in sub_t or "บวกและการลบเศษส่วน" in sub_t:
                den = random.randint(5, 15); num1 = random.randint(1, den-1); num2 = random.randint(1, den-1)
                op = random.choice(["+", "-"])
                if op == "-" and num1 < num2: num1, num2 = num2, num1 
                ans_num = num1 + num2 if op == "+" else num1 - num2
                
                f1 = generate_fraction_html(num1, den)
                f2 = generate_fraction_html(num2, den)
                q = f"จงหาผลลัพธ์ของ : <div style='display:flex; align-items:center; margin-top:10px;'>{f1} <span style='font-size:30px; margin: 0 10px;'>{op}</span> {f2} <span style='font-size:30px; margin: 0 10px;'>= ?</span></div>"
                
                s1 = generate_fraction_html(f"{num1} {op} {num2}", den)
                s2 = generate_fraction_html(ans_num, den)
                
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> เนื่องจากตัวส่วนเท่ากัน ให้นำตัวเศษมา{op}กันได้เลย</span><br><br><div style='display:flex; align-items:center; margin-bottom: 15px;'>{f1} <span style='margin:0 10px;'>{op}</span> {f2} <span style='margin:0 10px;'>=</span> {s1} <span style='margin:0 10px;'>=</span> {s2}</div>"
                
                extra_txt, final_html = get_fraction_solution_steps(ans_num, den)
                if extra_txt:
                    sol += f"<span style='color: #2c3e50;'><i>*{extra_txt}:</i></span><br><br>{final_html}"

            elif "คูณและการหารเศษส่วน" in sub_t:
                n1, d1 = random.randint(1, 5), random.randint(2, 7)
                n2, d2 = random.randint(1, 5), random.randint(2, 7)
                op = random.choice(["×", "÷"])
                f1 = generate_fraction_html(n1, d1)
                f2 = generate_fraction_html(n2, d2)
                q = f"จงหาผลลัพธ์ของ : <div style='display:flex; align-items:center; margin-top:10px;'>{f1} <span style='font-size:30px; margin: 0 10px;'>{op}</span> {f2} <span style='font-size:30px; margin: 0 10px;'>= ?</span></div>"
                
                if op == "×":
                    s1 = generate_fraction_html(f"{n1} × {n2}", f"{d1} × {d2}")
                    ans_n, ans_d = n1*n2, d1*d2
                    s2 = generate_fraction_html(ans_n, ans_d)
                    sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> การคูณเศษส่วน ให้นำตัวเศษคูณตัวเศษ และตัวส่วนคูณตัวส่วน</span><br><br><div style='display:flex; align-items:center; margin-bottom: 15px;'>{f1} <span style='margin:0 10px;'>×</span> {f2} <span style='margin:0 10px;'>=</span> {s1} <span style='margin:0 10px;'>=</span> {s2}</div>"
                else:
                    f2_flip = generate_fraction_html(d2, n2)
                    s1 = generate_fraction_html(f"{n1} × {d2}", f"{d1} × {n2}")
                    ans_n, ans_d = n1*d2, d1*n2
                    s2 = generate_fraction_html(ans_n, ans_d)
                    sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> เปลี่ยนเครื่องหมายหารเป็นคูณ แล้วกลับเศษเป็นส่วนของตัวหารด้านหลัง</span><br><br><div style='display:flex; align-items:center; margin-bottom: 15px;'>{f1} <span style='margin:0 10px;'>÷</span> {f2} <span style='margin:0 10px;'>=</span> {f1} <span style='margin:0 10px;'>×</span> {f2_flip} <span style='margin:0 10px;'>=</span> {s1} <span style='margin:0 10px;'>=</span> {s2}</div>"

                extra_txt, final_html = get_fraction_solution_steps(ans_n, ans_d)
                if extra_txt:
                    sol += f"<span style='color: #2c3e50;'><i>*{extra_txt}:</i></span><br><br>{final_html}"

            elif "ทศนิยม" in sub_t and "อ่าน" in sub_t:
                n = round(random.uniform(0.1, 99.999), random.randint(1, 3))
                q = f"จงเขียน <b>{n}</b> เป็นตัวหนังสือภาษาไทย"
                sol = f"<b>{generate_thai_number_text(str(n))}</b>"

            elif "ทศนิยม" in sub_t and ("บวก" in sub_t or "ลบ" in sub_t):
                a = round(random.uniform(10.0, 99.9), 2); b = round(random.uniform(1.0, 9.9), 2)
                op = random.choice(["+", "-"])
                q = f"จงหาผลลัพธ์ : <b>{a:.2f} {op} {b:.2f} = ?</b>"
                sol_html = generate_decimal_vertical_html(a, b, op)
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ตั้งจุดทศนิยมให้ตรงกันแล้วดำเนินการตามปกติ</span><br>{sol_html}"

            elif "คูณทศนิยม" in sub_t:
                a = round(random.uniform(1.0, 12.0), 1); b = random.randint(2, 9)
                ans = round(a*b, 1)
                q = f"จงหาผลลัพธ์ : <b>{a:.1f} × {b} = ?</b>"
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b><br>1) นำทศนิยมออกก่อน จะได้ {int(a*10)} × {b} = {int(a*10)*b}<br>2) เนื่องจากตัวตั้งมีทศนิยม 1 ตำแหน่ง คำตอบจึงต้องใส่ทศนิยม 1 ตำแหน่ง<br>ตอบ:</span> <b>{ans:.1f}</b>"

            elif "ร้อยละ" in sub_t and "เศษส่วน" in sub_t:
                den = random.choice([2, 4, 5, 10, 20, 25, 50]); num = random.randint(1, den-1)
                ans = int((num / den) * 100)
                frac_html = generate_fraction_html(num, den)
                q = f"จงเขียนเศษส่วนต่อไปนี้ให้อยู่ในรูปร้อยละ : <br>{frac_html}"
                mul = 100 // den
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ทำตัวส่วนให้เป็น 100 โดยการคูณด้วย {mul} ทั้งเศษและส่วน</span><br><br><div style='display:flex; align-items:center;'>{frac_html} <span style='margin:0 10px;'>=</span> {generate_fraction_html(f'{num} × {mul}', f'{den} × {mul}')} <span style='margin:0 10px;'>=</span> {generate_fraction_html(num*mul, 100)}</div><br>ตอบ: <b>ร้อยละ {ans} หรือ {ans}%</b>"

            elif "โจทย์ปัญหาร้อยละ" in sub_t:
                price = random.choice([100, 200, 500, 1000, 1500])
                percent = random.choice([10, 15, 20, 25, 50])
                discount = int(price * (percent / 100))
                q = f"เสื้อราคา {price:,} บาท ร้านค้าลดราคาให้ {percent}% ร้านค้าลดราคาให้กี่บาท?"
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b><br>คำว่า ลดราคา {percent}% หมายถึง ({percent} ÷ 100) × ราคาป้าย<br>= ({percent} ÷ 100) × {price:,}<br>ตอบ:</span> <b>{discount:,} บาท</b>"

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

            elif "สมการ" in sub_t:
                x = random.randint(5, 50); a = random.randint(1, 20); b = x + a
                q = f"จงแก้สมการเพื่อหาค่า x : <br><b style='font-size: 24px;'>x + {a} = {b}</b>"
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ย้ายข้างตัวเลขเพื่อหาค่าตัวแปร (จากบวกย้ายไปลบ)<br>x = {b} - {a}<br>ตอบ:</span> <b>x = {x}</b>"

            elif "ไม้โปรแทรกเตอร์" in sub_t:
                angle = random.randint(15, 165)
                arm_rad = math.radians(angle)
                ax = 150 + 120 * math.cos(arm_rad); ay = 140 - 120 * math.sin(arm_rad)
                ticks_svg = ""
                for i in range(0, 181):
                    rad = math.radians(i)
                    r_out = 120
                    if i % 10 == 0: r_in, stroke_w = 105, "1.5"
                    elif i % 5 == 0: r_in, stroke_w = 110, "1.2"
                    else: r_in, stroke_w = 115, "0.6"
                    tx1 = 150 + r_out * math.cos(rad); ty1 = 140 - r_out * math.sin(rad)
                    tx2 = 150 + r_in * math.cos(rad); ty2 = 140 - r_in * math.sin(rad)
                    ticks_svg += f'<line x1="{tx1}" y1="{ty1}" x2="{tx2}" y2="{ty2}" stroke="#333" stroke-width="{stroke_w}"/>'
                    if i % 10 == 0:
                        tx_text = 150 + 88 * math.cos(rad); ty_text = 140 - 88 * math.sin(rad)
                        ticks_svg += f'<text x="{tx_text}" y="{ty_text+4}" font-size="10" font-weight="bold" text-anchor="middle" fill="#333">{i}</text>'
                
                arc_r = 30
                arc_x = 150 + arc_r * math.cos(arm_rad); arc_y = 140 - arc_r * math.sin(arm_rad)
                angle_arc = f'<path d="M 180 140 A 30 30 0 0 0 {arc_x} {arc_y}" fill="none" stroke="#e74c3c" stroke-width="2"/>'
                svg = f"""<br><div style="text-align: center;"><svg width="300" height="160"><path d="M 30 140 A 120 120 0 0 1 270 140" fill="#fdfdfd" stroke="#333" stroke-width="2"/><line x1="150" y1="140" x2="270" y2="140" stroke="#3498db" stroke-width="2"/><line x1="150" y1="140" x2="{ax}" y2="{ay}" stroke="#e74c3c" stroke-width="1.5"/>{angle_arc}<line x1="30" y1="140" x2="270" y2="140" stroke="#333" stroke-width="2"/>{ticks_svg}<circle cx="150" cy="140" r="4" fill="#e74c3c"/></svg></div>"""
                q = f"มุมที่แสดงบนไม้โปรแทรกเตอร์มีขนาดกี่องศา? {svg}"
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> สังเกตเส้นสีแดงชี้ตรงกับตัวเลขสเกลด้านในที่เลข {angle} พอดี<br>ตอบ:</span> <b>{angle} องศา</b>"
                
            elif "คูณ" in sub_t or "หาร" in sub_t:
                a, b = random.randint(2, 12), random.randint(2, 12)
                if "คูณ" in sub_t:
                    q = f"จงหาผลลัพธ์ของ {a} × {b} = ?"
                    sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ท่องสูตรคูณแม่ {a} จะได้ว่า {a} × {b} =</span> <b>{a * b}</b>"
                else:
                    q = f"จงหาผลลัพธ์ของ {a * b} ÷ {a} = ?"
                    sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> เนื่องจาก {a} × {b} = {a * b}<br>ดังนั้น {a * b} ÷ {a} =</span> <b>{b}</b>"
            else:
                a, b = random.randint(10, 50), random.randint(10, 50)
                q = f"จงหาผลลัพธ์ : {a} + {b} = ?"
                sol = f"<br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ตั้งบวกหลักหน่วยและหลักสิบให้ตรงกัน</span><br><b>ตอบ: {a + b}</b>"

            if q not in seen:
                seen.add(q); questions.append({"question": q, "solution": sol}); break
            attempts += 1
    return questions

# ==========================================
# 3. ฟังก์ชันสร้างหน้า HTML
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
        body {{ font-family: 'Sarabun', sans-serif; padding: 40px; line-height: 1.8; }}
        .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 20px; padding-bottom: 10px; }}
        .q-box {{ margin-bottom: 30px; padding: 15px; page-break-inside: avoid; border-bottom: 1px solid #eee; }}
        .ans-line {{ margin-top: 15px; border-bottom: 1px dotted #999; width: 80%; height: 30px; }}
        .sol-text {{ color: red; font-size: 20px; display: inline-block; margin-top: 10px; line-height: 1.5; }}
    </style></head><body>
    <div class="header"><h2>{title} - {grade}</h2><p><b>เรื่อง:</b> {sub_t}</p></div>
    {student_info}"""
    
    for i, item in enumerate(questions, 1):
        if "(แบบตั้งหลัก)" in sub_t or "หารยาว" in sub_t:
            html += f'<div class="q-box"><b>ข้อที่ {i}.</b><br>{item["solution"] if is_key else item["question"]}</div>'
        else:
            html += f'<div class="q-box"><b>ข้อที่ {i}.</b> {item["question"]}'
            if is_key: html += f'<br><div class="sol-text">{item["solution"]}</div>'
            else: html += '<div class="ans-line">ตอบ: </div>'
            html += '</div>'
    return html + "</body></html>"

# ==========================================
# 4. สร้าง UI ของ Streamlit Web App
# ==========================================
st.sidebar.header("⚙️ การตั้งค่าใบงาน")
selected_grade = st.sidebar.selectbox("1. เลือกระดับชั้น:", list(curriculum_db.keys()))
selected_main = st.sidebar.selectbox("2. เลือกหัวข้อหลัก:", list(curriculum_db[selected_grade].keys()))
selected_sub = st.sidebar.selectbox("3. เลือกหัวข้อย่อย:", curriculum_db[selected_grade][selected_main])
num_input = st.sidebar.number_input("จำนวนข้อ:", min_value=1, max_value=100, value=10)

st.sidebar.info("💡 **เคล็ดลับ:** หากต้องการสุ่มโจทย์ชุดใหม่ ให้กดปุ่ม '🚀 สร้างใบงาน' อีกครั้งก่อนโหลด")

if st.sidebar.button("🚀 สร้างใบงาน", type="primary", use_container_width=True):
    with st.spinner("กำลังประมวลผลลอจิกคณิตศาสตร์และสร้างโจทย์..."):
        qs = generate_questions_logic(selected_grade, selected_main, selected_sub, num_input)
        html_w = create_page(selected_grade, selected_sub, qs, is_key=False)
        html_k = create_page(selected_grade, selected_sub, qs, is_key=True)
        filename_base = f"{selected_grade}_{selected_sub}"
        
        st.session_state['worksheet_html'] = html_w
        st.session_state['answerkey_html'] = html_k
        st.session_state['filename_base'] = f"{filename_base}_{int(time.time())}"
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(f"{filename_base}_Worksheet.html", html_w.encode('utf-8'))
            zip_file.writestr(f"{filename_base}_AnswerKey.html", html_k.encode('utf-8'))
        st.session_state['zip_data'] = zip_buffer.getvalue()

if 'worksheet_html' in st.session_state:
    st.success("🎉 สร้างใบงานเสร็จสมบูรณ์! เลือกดาวน์โหลดด้านล่างได้เลยครับ")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📄 ดาวน์โหลดแบบฝึกหัด",
            data=st.session_state['worksheet_html'],
            file_name=f"{st.session_state['filename_base']}_Worksheet.html",
            mime="text/html",
            use_container_width=True
        )
        
    with col2:
        st.download_button(
            label="🔑 ดาวน์โหลดเฉลย",
            data=st.session_state['answerkey_html'],
            file_name=f"{st.session_state['filename_base']}_AnswerKey.html",
            mime="text/html",
            use_container_width=True
        )
        
    st.markdown("---")
    st.download_button(
        label="📥 ดาวน์โหลดทั้งคู่พร้อมกัน (ไฟล์ .zip)",
        data=st.session_state['zip_data'],
        file_name=f"{st.session_state['filename_base']}.zip",
        mime="application/zip",
        use_container_width=True
    )
else:
    st.info("👈 กรุณาตั้งค่าใบงานที่เมนูด้านซ้าย แล้วกดปุ่ม 'สร้างใบงาน'")
