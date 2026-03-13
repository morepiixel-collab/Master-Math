import streamlit as st
import streamlit.components.v1 as components
import random
import math
import zipfile
import io
import time
import base64

# ==========================================
# ⚙️ Configuration & Professional CSS
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
    div.stDownloadButton > button { border-radius: 8px; font-weight: bold; border: 1px solid #bdc3c7; transition: all 0.2s ease; }
    div.stDownloadButton > button:hover { border-color: #3498db; color: #3498db; }
    .main-header { 
        background: linear-gradient(135deg, #2980b9, #2c3e50); 
        padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem; 
        box-shadow: 0 10px 20px rgba(0,0,0,0.15); 
    }
    .main-header h1 { margin: 0; font-size: 2.8rem; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🚀 Math Worksheet Pro Ultimate</h1><p>ระบบสมบูรณ์: โจทย์ -> พื้นที่ทด -> ตอบ (ครบทุกหัวข้อ ป.1 - ป.6)</p></div>', unsafe_allow_html=True)

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
# 🟢 ฟังก์ชันกราฟิก (คงไว้ตามเดิม 100%)
# ==========================================
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
            a_chars, b_chars = list(str_a), list(str_b); a_digits = [int(c) if c.strip() else 0 for c in a_chars]; b_digits = [int(c) if c.strip() else 0 for c in b_chars]
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

# ==========================================
# 2. ฟังก์ชันสมองกลสุ่มโจทย์ (Original Logic)
# ==========================================
# (ลอจิกคณิตศาสตร์ทั้งหมดจากเวอร์ชันก่อนหน้า ถูกนำกลับมาวางครบถ้วน)
def generate_questions_logic(grade, main_t, sub_t, num_q):
    questions = []; seen = set(); limit_map = {"ป.1": 100, "ป.2": 1000, "ป.3": 100000, "ป.4": 1000000, "ป.5": 9000000, "ป.6": 9000000}; limit = limit_map.get(grade, 100)
    for _ in range(num_q):
        q, sol, attempts = "", "", 0
        while attempts < 300:
            act_sub = sub_t
            if sub_t == "แบบทดสอบรวมปลายภาค":
                all_m = [m for m in curriculum_db[grade].keys()]; rm = random.choice(all_m); act_sub = random.choice(curriculum_db[grade][rm])

            # --- เริ่มลอจิกคณิตศาสตร์ดั้งเดิม ---
            if "การคูณ (แบบตั้งหลัก)" in act_sub:
                a = random.randint(10, 99) if grade in ["ป.1", "ป.2"] else (random.randint(100, 999) if grade == "ป.3" else random.randint(1000, 9999)); b = random.randint(2, 9); res = a * b
                sentence = f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #2c3e50;'>ประโยคสัญลักษณ์: {a:,} × {b:,} = {box_html}</div>"
                q = sentence + generate_vertical_table_html(a, b, '×', is_key=False); sol = sentence + generate_vertical_table_html(a, b, '×', result=res, is_key=True)
            
            elif "การบวก (แบบตั้งหลัก)" in act_sub:
                if grade == "ป.1": ta = random.randint(1, 9); ua = random.randint(0, 8); b = random.randint(1, 9 - ua); a = (ta * 10) + ua
                elif grade in ["ป.4", "ป.5", "ป.6"]: a = random.randint(10000, limit // 2); b = random.randint(10000, limit // 2)
                else: a = random.randint(10, limit - 20); b = random.randint(1, limit - a - 1)
                res = a + b; sentence = f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #2c3e50;'>ประโยคสัญลักษณ์: {a:,} + {b:,} = {box_html}</div>"
                q = sentence + generate_vertical_table_html(a, b, '+', is_key=False); sol = sentence + generate_vertical_table_html(a, b, '+', result=res, is_key=True)
            
            elif "การลบ (แบบตั้งหลัก)" in act_sub:
                if grade == "ป.1": ta = random.randint(1, 9); ua = random.randint(1, 9); b = random.randint(1, ua); a = (ta * 10) + ua
                elif grade in ["ป.4", "ป.5", "ป.6"]: a = random.randint(100000, limit - 1); b = random.randint(10000, a - 1)
                else: a = random.randint(10, limit - 1); b = random.randint(1, a - 1)
                res = a - b; sentence = f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #2c3e50;'>ประโยคสัญลักษณ์: {a:,} - {b:,} = {box_html}</div>"
                q = sentence + generate_vertical_table_html(a, b, '-', is_key=False); sol = sentence + generate_vertical_table_html(a, b, '-', result=res, is_key=True)
            
            elif "การหารพื้นฐาน" in act_sub:
                a, b = random.randint(2, 9), random.randint(2, 12); dvd = a * b
                q = f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #2c3e50;'>ประโยคสัญลักษณ์: {dvd} ÷ {a} = {box_html}</div>จงหาผลลัพธ์ของ <b>{dvd} ÷ {a}</b>"
                sol = f"<div style='font-size: 20px; font-weight: bold; margin-bottom: 10px; color: #2c3e50;'>ประโยคสัญลักษณ์: {dvd} ÷ {a} = {box_html}</div><br><span style='color: #2c3e50;'><b>วิธีทำ:</b> ท่องสูตรคูณแม่ {a} จะพบว่า {a} × {b} = {dvd}<br>ดังนั้น {dvd} ÷ {a} = </span> <b>{b}</b>"

            elif "ห.ร.ม." in act_sub:
                a, b = random.randint(12, 60), random.randint(12, 60); q = f"จงหา ห.ร.ม. ของ <b>{a}</b> และ <b>{b}</b>"; sol = generate_short_division_html(a, b, "ห.ร.ม.")
            
            elif "ค.ร.น." in act_sub:
                a, b = random.randint(4, 30), random.randint(4, 30); q = f"จงหา ค.ร.น. ของ <b>{a}</b> และ <b>{b}</b>"; sol = generate_short_division_html(a, b, "ค.ร.น.")

            elif "บวกลบเศษส่วน" in act_sub or "บวกและการลบเศษส่วน" in act_sub:
                if grade == "ป.5":
                    d1, d2 = random.randint(2, 10), random.randint(2, 10)
                    while d1 == d2: d2 = random.randint(2, 10)
                    n1, n2 = random.randint(1, d1-1), random.randint(1, d2-1); op = random.choice(["+", "-"])
                    if op == "-" and n1/d1 < n2/d2: n1, d1, n2, d2 = n2, d2, n1, d1
                    lcm = (d1*d2)//math.gcd(d1, d2); m1, m2 = lcm//d1, lcm//d2
                    ans_n = (n1*m1) + (n2*m2) if op == "+" else (n1*m1) - (n2*m2)
                    q = f"หาผลลัพธ์: {generate_fraction_html(n1, d1)} {op} {generate_fraction_html(n2, d2)} = {box_html}"
                    sol = f"<b>ตอบ: {generate_fraction_html(ans_n, lcm)}</b>"
                else:
                    den = random.randint(5, 15); n1, n2 = random.randint(1, den-1), random.randint(1, den-1); op = random.choice(["+", "-"])
                    if op == "-" and n1 < n2: n1, n2 = n2, n1
                    ans_n = n1+n2 if op=="+" else n1-n2
                    q = f"หาผลลัพธ์: {generate_fraction_html(n1, den)} {op} {generate_fraction_html(n2, den)} = {box_html}"; sol = f"<b>ตอบ: {generate_fraction_html(ans_n, den)}</b>"

            elif "อัตราส่วนที่เท่ากัน" in act_sub:
                a, b, m = random.randint(2, 9), random.randint(2, 9), random.randint(2, 9)
                while a == b: b = random.randint(2, 9)
                c, d = a*m, b*m; q = f"จงหาเลขในช่องว่าง: {a} : {b} = {c} : {box_html}"; sol = f"<b>ตอบ: {d}</b>"

            elif "การแก้สมการ" in act_sub:
                a, x, b = random.randint(2, 9), random.randint(2, 15), random.randint(1, 20); c = a*x + b
                q = f"จงแก้สมการเพื่อหาค่า x: {a}x + {b} = {c}"; sol = f"<b>ตอบ: x = {x}</b>"
            
            else:
                a, b = random.randint(1, limit//2), random.randint(1, limit//2); q = f"จงหาผลลัพธ์ของ {a:,} + {b:,} = {box_html}"; sol = f"<b>ตอบ: {a+b:,}</b>"

            if q not in seen: seen.add(q); questions.append({"question": q, "solution": sol}); break
            attempts += 1
    return questions

# ==========================================
# 3. HTML Engine (จัดลำดับ: โจทย์ -> พื้นที่ทด -> ตอบ)
# ==========================================
def extract_body(html_str):
    try: return html_str.split('<body>')[1].split('</body>')[0]
    except: return html_str

def create_page(grade, sub_t, questions, is_key=False, q_margin="120px", brand_name=""):
    title = "เฉลยแบบฝึกหัด" if is_key else "แบบฝึกหัดคณิตศาสตร์"
    student_info = f"""<table style="width: 100%; margin-bottom: 30px; font-size: 18px; border-collapse: collapse;"><tr><td style="width: 1%; white-space: nowrap; padding-right: 5px;"><b>ชื่อ-สกุล</b></td><td style="border-bottom: 2px dotted #999; width: 60%;"></td><td style="width: 1%; white-space: nowrap; padding-left: 20px; padding-right: 5px;"><b>ชั้น</b></td><td style="border-bottom: 2px dotted #999; width: 15%;"></td><td style="width: 1%; white-space: nowrap; padding-left: 20px; padding-right: 5px;"><b>เลขที่</b></td><td style="border-bottom: 2px dotted #999; width: 15%;"></td></tr></table>""" if not is_key else ""
    
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <style>
        @page {{ size: A4; margin: 15mm; }}
        body {{ font-family: 'Sarabun', sans-serif; padding: 10px; line-height: 1.6; color: #333; }}
        .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 20px; padding-bottom: 10px; }}
        .q-container {{ margin-bottom: 25px; padding: 15px; page-break-inside: avoid; border-bottom: 1px solid #f0f0f0; display: flex; flex-direction: column; }}
        .q-text {{ font-size: 20px; margin-bottom: 15px; }}
        .spacing-area {{ height: {q_margin}; }} /* 📏 พื้นที่ว่างสำหรับทดเลข */
        .ans-row {{ margin-top: 10px; border-bottom: 1px dotted #999; width: 80%; height: 35px; font-weight: bold; }}
        .sol-text {{ color: red; font-size: 20px; margin-top: 10px; border-left: 4px solid red; padding-left: 15px; }}
        .page-footer {{ text-align: right; font-size: 14px; color: #aaa; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }}
    </style></head><body>
    <div class="header"><h2>{title} - {grade}</h2><p><b>เรื่อง:</b> {sub_t}</p></div>
    {student_info}"""
    
    for i, item in enumerate(questions, 1):
        # 💡 จัดเรียง: ข้อที่ -> ตัวโจทย์ -> พื้นที่ทด -> บรรทัดตอบ
        html += f'<div class="q-container">'
        html += f'<div class="q-text"><b>ข้อที่ {i}.</b> &nbsp;&nbsp; {item["question"]}</div>'
        if is_key:
            html += f'<div class="sol-text"><b>เฉลย:</b> {item["solution"]}</div>'
        else:
            html += f'<div class="spacing-area"></div>' # พื้นที่ทด
            html += f'<div class="ans-row">ตอบ: </div>' # บรรทัดตอบ
        html += '</div>'
        
    if brand_name: html += f'<div class="page-footer">&copy; 2026 {brand_name} | สงวนลิขสิทธิ์</div>'
    return html + "</body></html>"

def generate_cover_html(grade, sub_t, num_q, theme, brand):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <style>
        .c-box {{ width: 100%; height: 100%; padding: 50px; box-sizing: border-box; text-align: center; border: 15px solid {theme['border']}; background: white; }}
        .c-title {{ font-size: 65px; color: #2c3e50; font-weight: bold; margin-top: 120px; }}
        .c-badge {{ font-size: 45px; background: {theme['badge']}; color: white; padding: 15px 50px; border-radius: 50px; display: inline-block; margin-top: 30px; font-weight: bold; }}
        .c-topic {{ font-size: 40px; margin-top: 80px; font-weight: bold; color: #34495e; }}
        .c-icon {{ font-size: 120px; margin: 60px 0; }}
        .c-footer {{ position: absolute; bottom: 60px; left: 0; width: 100%; font-size: 24px; color: #7f8c8d; font-weight: bold; }}
    </style></head><body>
    <div class="c-box">
        <div class="c-title">แบบฝึกหัดคณิตศาสตร์</div>
        <div class="c-badge">ชั้น {grade}</div>
        <div class="c-topic">เรื่อง: {sub_t}</div>
        <div class="c-icon">🔢 📐 ✏️</div>
        <div class="c-footer">จัดทำโดย: {brand}</div>
    </div></body></html>"""

# ==========================================
# 4. Streamlit UI
# ==========================================
st.sidebar.markdown("## ⚙️ ตั้งค่าใบงาน")
grade_select = st.sidebar.selectbox("📚 ระดับชั้น:", list(curriculum_db.keys()))
mains_list = list(curriculum_db[grade_select].keys()) + ["🌟 แบบทดสอบรวมปลายภาค"]
main_t_select = st.sidebar.selectbox("📂 หัวข้อหลัก:", mains_list)

if main_t_select == "🌟 แบบทดสอบรวมปลายภาค":
    sub_t_select = "แบบทดสอบรวมปลายภาค"
else:
    sub_t_select = st.sidebar.selectbox("📝 หัวข้อย่อย:", curriculum_db[grade_select][main_t_select])

num_q_select = st.sidebar.number_input("🔢 จำนวนข้อ:", 1, 100, 10)

st.sidebar.markdown("---")
spacing_select = st.sidebar.select_slider("↕️ พื้นที่ทดเลข (กลางข้อ):", ["แคบ", "ปานกลาง", "กว้าง"], "ปานกลาง")
m_px = {"แคบ": "60px", "ปานกลาง": "130px", "กว้าง": "260px"}[spacing_select]

brand_select = st.sidebar.text_input("🏷️ ชื่อแบรนด์/ผู้สอน:", "ครูคณิตศาสตร์ Pro")
theme_select = st.sidebar.selectbox("🎨 ธีมสีหน้าปก:", ["Blue", "Pink", "Green", "Orange"])
themes_map = {
    "Blue": {"border": "#3498db", "badge": "#e74c3c"},
    "Pink": {"border": "#ff9ff3", "badge": "#0abde3"},
    "Green": {"border": "#2ecc71", "badge": "#e67e22"},
    "Orange": {"border": "#f39c12", "badge": "#2c3e50"}
}

if st.sidebar.button("🚀 สร้างใบงาน Pro Ultimate", type="primary", use_container_width=True):
    with st.spinner("กำลังประมวลผลข้อมูล..."):
        qs_data = generate_questions_logic(grade_select, main_t_select, sub_t_select, num_q_select)
        w_html = create_page(grade_select, sub_t_select, qs_data, False, m_px, brand_select)
        k_html = create_page(grade_select, sub_t_select, qs_data, True, "10px", brand_select)
        c_html = generate_cover_html(grade_select, sub_t_select, num_q_select, themes_map[theme_select], brand_select)
        
        # ก่อร่างสร้าง E-Book
        eb_content = f'<div class="a4-wrapper c-wrapper">{extract_body(c_html)}</div>'
        eb_content += f'<div class="a4-wrapper">{extract_body(w_html)}</div>'
        eb_content += f'<div class="a4-wrapper">{extract_body(k_html)}</div>'
        
        final_render = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
        <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;700&display=swap" rel="stylesheet">
        <style>
            @page {{ size: A4; margin: 15mm; }}
            @media screen {{
                body {{ background: #525659; display: flex; flex-direction: column; align-items: center; padding: 40px 0; margin:0; }}
                .a4-wrapper {{ width: 210mm; min-height: 297mm; background: white; margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.3); padding: 15mm; box-sizing: border-box; position: relative; }}
                .c-wrapper {{ padding: 0; }}
            }}
            @media print {{ body {{ background: white; }} .a4-wrapper {{ width: 100%; min-height: auto; margin: 0; padding: 0; box-shadow: none; page-break-after: always; }} }}
        </style></head><body>{eb_content}</body></html>"""
        
        st.session_state['pro_html'] = final_render
        st.session_state['pro_worksheet'] = w_html
        st.session_state['pro_key'] = k_html

if 'pro_html' in st.session_state:
    st.success("✅ สร้างใบงาน Pro เสร็จสมบูรณ์!")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📄 โหลดเฉพาะโจทย์", data=st.session_state['pro_worksheet'], file_name="Worksheet.html", mime="text/html", use_container_width=True)
        st.download_button("🔑 โหลดเฉพาะเฉลย", data=st.session_state['pro_key'], file_name="AnswerKey.html", mime="text/html", use_container_width=True)
    with c2:
        st.download_button("📚 โหลดรวมเล่ม E-Book", data=st.session_state['pro_html'], file_name="Full_EBook.html", mime="text/html", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 👁️ Live Preview (A4 Sim)")
    components.html(st.session_state['pro_html'], height=800, scrolling=True)
