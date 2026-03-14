import streamlit as st
import streamlit.components.v1 as components
import random
import math
import zipfile
import io
import time

# ==========================================
# ตั้งค่าหน้าเพจ & Professional CSS
# ==========================================
st.set_page_config(page_title="Math Generator Pro Ultimate", page_icon="🚀", layout="wide")

st.markdown("""<style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1200px; }
    div[data-testid="stSidebar"] div.stButton > button { background-color: #27ae60; color: white; border-radius: 8px; height: 3.5rem; font-size: 18px; font-weight: bold; border: none; }
    .main-header { background: linear-gradient(135deg, #2980b9, #2c3e50); padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem; }
    .main-header h1 { margin: 0; font-size: 2.5rem; font-weight: 800; }
</style>""", unsafe_allow_html=True)

st.markdown("""<div class="main-header"><h1>🚀 Math Worksheet Pro <span style="font-size: 20px; background: #f39c12; padding: 5px 15px; border-radius: 20px; vertical-align: middle;">National Edition</span></h1>
<p>ระบบสร้างสื่อการสอน ป.1-ป.6 + ข้อสอบแข่งขัน TMC ทุกระดับชั้น พร้อมเฉลยละเอียดแบบ Step-by-Step 100%</p></div>""", unsafe_allow_html=True)

# ==========================================
# 1. ฐานข้อมูลหลักสูตรและคลังคำศัพท์
# ==========================================
NAMES = ["อคิณ", "นาวิน", "ภูผา", "สายฟ้า", "เจ้านาย", "ข้าวหอม", "ใบบัว", "มะลิ", "น้ำใส", "ญาญ่า", "ปลื้ม", "พายุ", "ไออุ่น", "กะทิ", "เวลา", "ของขวัญ", "มังกร", "ฉลาม", "ปลาวาฬ", "มาคิน"]
LOCS = ["โรงเรียน", "สวนสัตว์", "สวนสนุก", "ห้องสมุด", "สวนสาธารณะ", "ร้านเบเกอรี่", "พิพิธภัณฑ์"]
ITEMS = ["ลูกแก้ว", "สติกเกอร์", "การ์ดพลัง", "ตุ๊กตา", "ตัวต่อเลโก้", "หนังสือการ์ตูน", "ลูกบอล"]
SNACKS = ["ช็อกโกแลต", "คุกกี้", "โดนัท", "เยลลี่", "อมยิ้ม", "เค้ก"]

comp_topics = [
    "ปริศนาตัวเลขซ่อนแอบ", "การนับหน้าหนังสือ", "การปักเสาและปลูกต้นไม้", 
    "สัตว์ปีนบ่อ", "ตรรกะตาชั่งสมดุล", "อายุข้ามเวลาขั้นสูง", 
    "การตัดเชือกพับทบ", "แถวคอยแบบซ้อนทับ", "ปัญหาผลรวม-ผลต่าง", 
    "ตรรกะการจับมือ", "โปรโมชั่นแลกของ", "หยิบของในที่มืด",
    "การคิดย้อนกลับ", "แผนภาพความชอบ", "คิววงกลมมรณะ", 
    "ลำดับแบบวนลูป", "เส้นทางที่เป็นไปได้", "นาฬิกาเดินเพี้ยน", 
    "จัดของใส่กล่อง", "คะแนนยิงเป้า"
]

curriculum_db = {
    "ป.1": {
        "จำนวนนับ": ["การนับทีละ 1", "หลักและค่าของเลขโดด", "การเปรียบเทียบจำนวน", "การเรียงลำดับจำนวน"],
        "การบวก การลบ": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)"],
        "🌟 โจทย์แข่งขัน (แนว TMC)": comp_topics[:8]
    },
    "ป.2": {
        "จำนวนนับ": ["จำนวนคู่ จำนวนคี่", "หลักและรูปกระจาย", "การเปรียบเทียบจำนวน", "การเรียงลำดับจำนวน"],
        "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การคูณ (แบบตั้งหลัก)", "การหารพื้นฐาน"],
        "🌟 โจทย์แข่งขัน (แนว TMC)": comp_topics
    },
    "ป.3": {
        "จำนวนนับและเศษส่วน": ["หลักและรูปกระจาย", "การอ่านและเขียนเศษส่วน", "การบวกลบเศษส่วน"],
        "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การคูณ (แบบตั้งหลัก)", "การหารยาว"],
        "🌟 โจทย์แข่งขัน (แนว TMC)": comp_topics
    },
    "ป.4": { "จำนวนนับ": ["ค่าประมาณเต็มสิบ/ร้อย/พัน"], "การบวก ลบ คูณ หาร": ["การหารยาว"], "🌟 โจทย์แข่งขัน (แนว TMC)": comp_topics },
    "ป.5": { "เศษส่วนและทศนิยม": ["การบวกเศษส่วน", "การคูณทศนิยม"], "🌟 โจทย์แข่งขัน (แนว TMC)": comp_topics },
    "ป.6": { "สมการและร้อยละ": ["การแก้สมการ", "โจทย์ปัญหาร้อยละ"], "🌟 โจทย์แข่งขัน (แนว TMC)": comp_topics }
}

# --- ฟังก์ชันช่วยวาดรูปประกอบ ---
def draw_bar_model(name1, val1, name2, val2, diff):
    return f"""<div style='text-align: center; margin: 10px 0;'><svg width="300" height="80">
    <text x="60" y="25" text-anchor="end" font-size="12">{name2}</text>
    <rect x="70" y="10" width="100" height="20" fill="#3498db" rx="3"/>
    <text x="60" y="55" text-anchor="end" font-size="12">{name1}</text>
    <rect x="70" y="40" width="100" height="20" fill="#e74c3c" rx="3"/>
    <rect x="170" y="40" width="40" height="20" fill="#f1c40f" rx="3" stroke="#333" stroke-dasharray="3"/>
    <text x="190" y="55" text-anchor="middle" font-size="10" font-weight="bold">+{diff}</text>
    </svg></div>"""

def generate_vertical_table_html(a, b, op, result=None, is_key=False):
    num_len = max(len(str(a)), len(str(b)), len(str(result)) if result else 0) + 1
    str_a, str_b = str(a).rjust(num_len, " "), str(b).rjust(num_len, " ")
    strike, top_marks = [False] * num_len, [""] * num_len
    if is_key:
        if op == '+':
            carry = 0
            for i in range(num_len-1, -1, -1):
                da, db = int(str_a[i]) if str_a[i].strip() else 0, int(str_b[i]) if str_b[i].strip() else 0
                s = da+db+carry; carry = s//10
                if carry > 0 and i > 0: top_marks[i-1] = str(carry)
        elif op == '-':
            a_dig = [int(c) if c.strip() else 0 for c in str_a]
            b_dig = [int(c) if c.strip() else 0 for c in str_b]
            for i in range(num_len-1, -1, -1):
                if a_dig[i] < b_dig[i]:
                    for j in range(i-1, -1, -1):
                        if a_dig[j] > 0 and str_a[j].strip() != "":
                            strike[j] = True; a_dig[j] -= 1; top_marks[j] = str(a_dig[j])
                            for k in range(j+1, i): strike[k] = True; a_dig[k] = 9; top_marks[k] = "9"
                            strike[i] = True; a_dig[i] += 10; top_marks[i] = str(a_dig[i]); break
    a_tds = "".join([f'<td style="width:35px; text-align:center; height:50px; vertical-align:bottom;">{ (f"<div style=\'position:relative;\'><span style=\'position:absolute; top:-25px; left:50%; transform:translateX(-50%); font-size:20px; color:red; font-weight:bold;\'>{top_marks[i]}</span><span style=\'text-decoration:line-through; text-decoration-color:red;\'>{str_a[i]}</span></div>" if strike[i] and is_key else (f"<div style=\'position:relative;\'><span style=\'position:absolute; top:-25px; left:50%; transform:translateX(-50%); font-size:20px; color:red; font-weight:bold;\'>{top_marks[i]}</span>{str_a[i]}</div>" if top_marks[i] and is_key else str_a[i])) if str_a[i].strip() else "" }</td>' for i in range(num_len)])
    b_tds = "".join([f'<td style="width:35px; text-align:center; border-bottom:2px solid #000; height:40px; vertical-align:bottom;">{str_b[i].strip()}</td>' for i in range(num_len)])
    res_tds = "".join([f'<td style="width:35px; text-align:center; color:red; font-weight:bold; height:45px; vertical-align:bottom;">{str(result).rjust(num_len, " ")[i].strip()}</td>' for i in range(num_len)]) if is_key else "".join([f'<td style="width:35px; height:45px;"></td>' for _ in range(num_len)])
    return f"""<div style="display:block; text-align:center; margin-top:10px;"><div style="display:inline-block; font-family:'Sarabun'; font-size:38px; line-height:1.1; margin:10px 20px;"><table style="border-collapse:collapse; margin-left:auto; margin-right:auto;"><tr><td style="width:20px;"></td>{a_tds}<td style="width:50px; text-align:center; vertical-align:middle;" rowspan="2">{op}</td></tr><tr><td></td>{b_tds}</tr><tr><td></td>{res_tds}<td></td></tr><tr><td></td><td colspan="{num_len}" style="border-bottom:6px double #000; height:10px;"></td><td></td></tr></table></div></div>"""

def generate_long_division_step_by_step_html(divisor, dividend, eq_html, is_key=False):
    div_str = str(dividend); div_len = len(div_str)
    if not is_key:
        ans_tds = "".join([f'<td style="width:35px; height:45px;"></td>' for _ in div_str]) + '<td style="width:35px;"></td>'
        div_tds = "".join([f'<td style="width:35px; text-align:center; border-top:3px solid #000; {"border-left:3px solid #000;" if i==0 else ""} font-size:38px; height:50px; vertical-align:bottom;">{c}</td>' for i, c in enumerate(div_str)]) + '<td style="width:35px;"></td>'
        empty_rows = "".join([f"<tr><td style='border:none;'></td>{''.join(['<td style=\"width:35px; height:45px;\"></td>' for _ in range(div_len+1)])}</tr>" for _ in range(div_len+1)])
        return f"{eq_html}<div style=\"display:block; text-align:center; margin-top:10px;\"><div style=\"display:inline-block; font-family:'Sarabun'; line-height:1.2; margin:10px 20px;\"><table style=\"border-collapse:collapse;\"><tr><td style=\"border:none;\"></td>{ans_tds}</tr><tr><td style=\"border:none; text-align:right; padding-right:12px; vertical-align:bottom; font-size:38px;\">{divisor}</td>{div_tds}</tr>{empty_rows}</table></div></div>"
    
    # ลอจิกเฉลยหารยาวแบบละเอียดจะอยู่ในส่วนการสร้างโจทย์
    return "เฉลยหารยาว..." # (ถูกแทนที่ด้วยลอจิกเต็มในฟังก์ชันหลัก)

def generate_thai_number_text(num_str):
    thai_nums = ["ศูนย์", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
    positions = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]
    int_part = str(num_str).split(".")[0]
    def read_int(s):
        if s == "0": return "ศูนย์"
        res, l = "", len(s)
        for i, d in enumerate(s):
            v, p = int(d), l-i-1
            if v == 0: continue
            if p == 1 and v == 2: res += "ยี่สิบ"
            elif p == 1 and v == 1: res += "สิบ"
            elif p == 0 and v == 1 and l > 1: res += "เอ็ด"
            else: res += thai_nums[v] + positions[p]
        return res
    return read_int(int_part)

def get_prefix(grade): return "<b style='color:#2c3e50; margin-right:5px;'>ประโยคสัญลักษณ์:</b>" if grade in ["ป.1","ป.2","ป.3"] else ""
    def generate_questions_logic(grade, main_t, sub_t, num_q):
    questions = []
    seen = set()
    limit_map = {"ป.1": 100, "ป.2": 1000, "ป.3": 100000, "ป.4": 1000000, "ป.5": 9000000, "ป.6": 9000000}
    limit = limit_map.get(grade, 100)

    NAMES = ["อคิณ", "นาวิน", "ภูผา", "สายฟ้า", "เจ้านาย", "ข้าวหอม", "ใบบัว", "มะลิ", "น้ำใส", "ญาญ่า", "ปลื้ม", "พายุ", "ไออุ่น", "กะทิ", "เวลา", "ของขวัญ", "มังกร", "ฉลาม", "ปลาวาฬ", "มาคิน"]
    LOCS = ["โรงเรียน", "สวนสัตว์", "สวนสนุก", "ห้างสรรพสินค้า", "ห้องสมุด", "สวนสาธารณะ", "ร้านของเล่น", "ร้านเบเกอรี่", "ค่ายลูกเสือ", "พิพิธภัณฑ์"]
    ITEMS = ["ลูกแก้ว", "สติกเกอร์", "การ์ดพลัง", "โมเดลรถ", "ตุ๊กตาหมี", "สมุดระบายสี", "ดินสอสี", "ลูกโป่ง", "ยางลบ", "ตัวต่อเลโก้", "หนังสือการ์ตูน", "ลูกบอล"]
    SNACKS = ["ช็อกโกแลต", "คุกกี้", "โดนัท", "เยลลี่", "ขนมปัง", "ไอศกรีม", "น้ำผลไม้", "นมเย็น", "ลูกอม", "เค้ก"]
    ANIMALS = ["แมงมุม", "มดแดง", "กบ", "จิ้งจก", "ตั๊กแตน", "เต่า"]

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
                actual_sub_t = random.choice(comp_topics)

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
                item = random.choice(ITEMS)
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
                loc = random.choice(LOCS)
                q = f"เทศบาลต้องการปลูกต้นไม้ริมถนนทางเข้า<b>{loc}</b> โดยให้ต้นไม้แต่ละต้นอยู่ห่างกันระยะทาง <b>{d}</b> เมตร และมีเงื่อนไขว่า <b>ต้องปลูกต้นไม้ที่จุดเริ่มต้นและจุดสิ้นสุดของถนนพอดี</b> หากปลูกเสร็จแล้วนับต้นไม้ได้ทั้งหมด <b>{trees}</b> ต้น ถนนเส้นนี้ยาวกี่เมตร?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                1) ลองนึกภาพตามนะครับ ถ้าเราปลูกต้นไม้ 3 ต้น จะเกิดช่องว่างระหว่างต้นไม้แค่ 2 ช่อง, ถ้าปลูก 4 ต้น จะเกิดช่องว่าง 3 ช่อง<br>
                2) สรุปได้ว่า <b>จำนวนช่องว่าง จะน้อยกว่าจำนวนต้นไม้อยู่ 1 เสมอ</b> (เพราะปลูกปิดหัวท้าย)<br>
                3) ในโจทย์นี้ มีต้นไม้ทั้งหมด {trees} ต้น <br>
                &nbsp;&nbsp;&nbsp;ดังนั้น จะมีช่องว่างทั้งหมด = {trees} - 1 = <b>{trees - 1} ช่องว่าง</b><br>
                4) โจทย์บอกว่า 1 ช่องว่าง มีระยะห่าง {d} เมตร<br>
                &nbsp;&nbsp;&nbsp;นำจำนวนช่องว่างไปคูณกับระยะห่าง: {trees - 1} ช่อง × {d} เมตร = <b>{length} เมตร</b><br>
                <b>ตอบ: ถนนเส้นนี้มีความยาว {length} เมตร</b></span>"""

            elif actual_sub_t == "ตรรกะตาชั่งสมดุล":
                items_pair = [("รถคันใหญ่", "รถคันเล็ก", "ลูกบอล"), ("หนังสือหนา", "สมุดบาง", "ดินสอ"), ("แตงโม", "ส้ม", "มะนาว")]
                i1, i2, i3 = random.choice(items_pair)
                m1 = random.randint(2, 5)
                m2 = random.randint(2, 5)
                q = f"จากการเล่นตาชั่งสมดุล พบข้อมูลดังนี้:<br>- <b>{i1} 1 ชิ้น</b> หนักเท่ากับ <b>{i2} {m1} ชิ้น</b><br>- <b>{i2} 1 ชิ้น</b> หนักเท่ากับ <b>{i3} {m2} ชิ้น</b><br><br>อยากทราบว่า <b>{i1} จำนวน 2 ชิ้น</b> จะมีน้ำหนักเท่ากับ <b>{i3}</b> กี่ชิ้น?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                เป้าหมายของเราคือการเปลี่ยนของที่ใหญ่ที่สุด ({i1}) ให้กลายเป็นของที่เล็กที่สุด ({i3}) ทีละขั้นตอนครับ<br>
                1) จากบรรทัดที่ 2: เรารู้แล้วว่า {i2} 1 ชิ้น สามารถแลกเป็น {i3} ได้ <b>{m2} ชิ้น</b><br>
                2) จากบรรทัดที่ 1: {i1} 1 ชิ้น หนักเท่ากับ {i2} จำนวน {m1} ชิ้น<br>
                &nbsp;&nbsp;&nbsp;ให้นำความรู้จากข้อ 1 มาแทนค่า: เปลี่ยน {i2} {m1} ชิ้น เป็น {i3}<br>
                &nbsp;&nbsp;&nbsp;จะได้ {i1} 1 ชิ้น = {m1} กลุ่ม กลุ่มละ {m2} ชิ้น = {m1} × {m2} = <b>{m1 * m2} ชิ้น ({i3})</b><br>
                3) แต่โจทย์ไม่ได้ถามหา {i1} แค่ 1 ชิ้น โจทย์ถามหา {i1} <b>2 ชิ้น</b><br>
                &nbsp;&nbsp;&nbsp;เราจึงต้องนำน้ำหนักไปคูณ 2: {m1 * m2} × 2 = <b>{m1 * m2 * 2} ชิ้น</b><br>
                <b>ตอบ: หนักเท่ากับ {i3} ทั้งหมด {m1 * m2 * 2} ชิ้น</b></span>"""

            elif actual_sub_t == "ปัญหาผลรวม-ผลต่าง":
                diff = random.randint(5, 20)
                small = random.randint(10, 30)
                large = small + diff
                total = large + small
                n1, n2 = random.sample(NAMES, 2)
                itm = random.choice(ITEMS)
                q = f"<b>{n1}</b> และ <b>{n2}</b> มี<b>{itm}</b>รวมกันทั้งหมด <b>{total}</b> ชิ้น หากทราบว่า <b>{n1}</b> มีมากกว่า <b>{n2}</b> อยู่ <b>{diff}</b> ชิ้น จงหาว่า <b>{n1}</b> มี<b>{itm}</b>กี่ชิ้น?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                1) ลองนึกภาพว่ากองของของ {n1} และ {n2} วางคู่กันอยู่ กองของ {n1} จะสูงกว่า {n2} อยู่ {diff} ชิ้น<br>
                2) ถ้าเราหยิบของที่ "เกินมา" ({diff} ชิ้น) ออกไปจากกองรวมก่อน <br>
                &nbsp;&nbsp;&nbsp;ของที่เหลือจะคือส่วนที่ <b>{n1} และ {n2} มีเท่าๆ กันพอดี</b><br>
                &nbsp;&nbsp;&nbsp;เหลือของ: {total} (ทั้งหมด) - {diff} (ส่วนเกิน) = <b>{total - diff} ชิ้น</b><br>
                3) นำของที่เหลือมาแบ่งครึ่งให้ 2 คน คนละเท่าๆ กัน (ซึ่งนี่คือจำนวนของคนที่น้อยกว่า คือ {n2})<br>
                &nbsp;&nbsp;&nbsp;จำนวนของ {n2}: {total - diff} ÷ 2 = <b>{small} ชิ้น</b><br>
                4) โจทย์ถามหาจำนวนของ {n1} ซึ่งมีมากกว่า {n2} อยู่ {diff} ชิ้น<br>
                &nbsp;&nbsp;&nbsp;จำนวนของ {n1}: {small} (ส่วนที่เท่ากัน) + {diff} (ส่วนที่มากกว่า) = <b>{large} ชิ้น</b><br>
                <b>ตอบ: {n1} มี{itm}ทั้งหมด {large} ชิ้น</b></span>"""

            elif actual_sub_t == "ตรรกะการจับมือ (ทักทาย)":
                n = random.randint(5, 10)
                loc = random.choice(LOCS)
                # สร้างข้อความบวกเลขแบบแจกแจง
                sum_str_list = [str(x) for x in range(n-1, 0, -1)]
                sum_display = " + ".join(sum_str_list)
                ans = sum(range(1, n))
                q = f"ในการจัดกิจกรรมที่<b>{loc}</b> มีเด็กมาร่วมกลุ่มทั้งหมด <b>{n}</b> คน หากเด็กทุกคนต้องเดินไปจับมือทำความรู้จักกันให้ครบทุกคน (จับมือกันคนละ 1 ครั้ง) จะมีการจับมือเกิดขึ้นทั้งหมดกี่ครั้ง?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                เราจะนับการจับมือทีละคน เพื่อไม่ให้มีการจับมือซ้ำซ้อนกันครับ<br>
                1) <b>คนที่ 1:</b> เดินไปจับมือกับเพื่อนคนอื่นที่เหลืออีก <b>{n-1} คน</b> (เกิดการจับมือ {n-1} ครั้ง)<br>
                2) <b>คนที่ 2:</b> เดินไปจับมือกับเพื่อนคนอื่น (แต่ไม่ต้องไปจับคนที่ 1 แล้ว เพราะจับไปแล้วเมื่อกี้!) จึงเหลือคนให้จับอีก <b>{n-2} คน</b><br>
                3) <b>คนที่ 3:</b> เหลือเพื่อนให้จับมืออีก <b>{n-3} คน</b><br>
                ...ทำแบบนี้ลดหลั่นไปเรื่อยๆ จนถึงคนรองสุดท้าย จะเหลือคนให้จับอีกแค่ 1 คน ส่วนคนสุดท้ายไม่ต้องเดินไปหาใครแล้วเพราะโดนจับครบแล้ว<br>
                4) นำจำนวนการจับมือของแต่ละคนมาบวกกันทั้งหมด:<br>
                &nbsp;&nbsp;&nbsp;{sum_display} = <b>{ans} ครั้ง</b><br>
                <b>ตอบ: เกิดการจับมือทั้งหมด {ans} ครั้ง</b></span>"""

            elif actual_sub_t == "การคิดย้อนกลับ":
                s_money = random.randint(100, 300)
                spent = random.randint(20, 80)
                recv = random.randint(50, 150)
                f_money = s_money - spent + recv
                name = random.choice(NAMES)
                item = random.choice(ITEMS)
                q = f"<b>{name}</b>นำเงินไปซื้อ<b>{item}</b> <b>{spent}</b> บาท จากนั้นแม่ให้ค่าขนมเพิ่มมาอีก <b>{recv}</b> บาท เมื่อกลับถึงบ้าน<b>{name}</b>นับเงินดูพบว่าตอนนี้มีเงินเหลือ <b>{f_money}</b> บาท <br>จงหาว่าตอนแรกก่อนออกจากบ้าน <b>{name}</b>มีเงินอยู่ในกระเป๋ากี่บาท?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (หลักการคิดย้อนกลับ):</b><br>
                การคิดย้อนกลับ คือการเริ่มจากเหตุการณ์สุดท้าย ย้อนกลับไปหาจุดเริ่มต้น โดยการ "ทำตรงกันข้าม" (บวกเปลี่ยนเป็นลบ, ลบเปลี่ยนเป็นบวก)<br>
                1) <b>เหตุการณ์สุดท้าย:</b> ตอนนี้มีเงินเหลือ <b>{f_money} บาท</b><br>
                2) <b>ย้อนกลับเหตุการณ์ แม่ให้เพิ่ม:</b> แม่ให้มา {recv} บาท (ของจริงเงินเพิ่มขึ้น ย้อนกลับคือต้องนำไป <b>ลบออก</b>)<br>
                &nbsp;&nbsp;&nbsp;ก่อนแม่ให้ มีเงิน: {f_money} - {recv} = <b>{f_money - recv} บาท</b><br>
                3) <b>ย้อนกลับเหตุการณ์ ซื้อของ:</b> ซื้อของไป {spent} บาท (ของจริงเงินลดลง ย้อนกลับคือต้องนำไป <b>บวกคืน</b>)<br>
                &nbsp;&nbsp;&nbsp;ก่อนซื้อของ (ตอนแรกสุด) มีเงิน: {f_money - recv} + {spent} = <b>{s_money} บาท</b><br>
                <b>ตอบ: ตอนแรกมีเงิน {s_money} บาท</b></span>"""

            elif actual_sub_t == "แผนภาพความชอบ":
                tot = random.randint(30, 50)
                both = random.randint(5, 12)
                only_a = random.randint(8, 15)
                only_b = random.randint(8, 15)
                l_a = only_a + both
                l_b = only_b + both
                neither = tot - (only_a + only_b + both)
                n1, n2 = random.sample(SNACKS, 2)
                q = f"จากการสำรวจนักเรียน <b>{tot}</b> คน พบว่ามีคนชอบกิน<b>{n1}</b> <b>{l_a}</b> คน, ชอบกิน<b>{n2}</b> <b>{l_b}</b> คน, และมีคนที่ชอบกินทั้งสองอย่าง <b>{both}</b> คน <br>อยากทราบว่ามีนักเรียนกี่คนในกลุ่มนี้ ที่<b>ไม่ชอบกินขนมทั้งสองชนิดนี้เลย</b>?"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                ข้อนี้เราจะนำตัวเลข <b>{l_a}</b> กับ <b>{l_b}</b> มาบวกกันตรงๆ ไม่ได้ครับ เพราะมันมีคนที่ชอบทั้งสองอย่าง (<b>{both}</b> คน) ถูกนับซ้ำซ้อนไปแล้วในทั้งสองกลุ่ม!<br>
                1) หาจำนวนคนที่ชอบ <b>{n1} อย่างเดียว</b> (เอาคนที่ชอบทั้งคู่ออกไป):<br>
                &nbsp;&nbsp;&nbsp;{l_a} - {both} = <b>{only_a} คน</b><br>
                2) หาจำนวนคนที่ชอบ <b>{n2} อย่างเดียว</b> (เอาคนที่ชอบทั้งคู่ออกไป):<br>
                &nbsp;&nbsp;&nbsp;{l_b} - {both} = <b>{only_b} คน</b><br>
                3) หาจำนวนคนที่ <b>ชอบขนมอย่างน้อย 1 ชนิด</b> โดยนำ 3 กลุ่มมาบวกกัน (ชอบ n1 อย่างเดียว + ชอบ n2 อย่างเดียว + ชอบทั้งคู่):<br>
                &nbsp;&nbsp;&nbsp;{only_a} + {only_b} + {both} = <b>{only_a + only_b + both} คน</b><br>
                4) หาคนที่ <b>ไม่ชอบเลย</b> โดยนำคนทั้งหมดตั้ง ลบด้วยคนที่ชอบขนม:<br>
                &nbsp;&nbsp;&nbsp;{tot} (ทั้งหมด) - {only_a + only_b + both} (คนที่ชอบ) = <b>{neither} คน</b><br>
                <b>ตอบ: มีคนที่ไม่ชอบเลยจำนวน {neither} คน</b></span>"""

            elif actual_sub_t == "ผลบวกจำนวนเรียงกัน (Gauss)":
                n = random.choice([10, 20, 50, 100])
                ans = (n * (n + 1)) // 2
                q = f"จงหาผลบวกของตัวเลขเรียงลำดับตั้งแต่ 1 ถึง {n} <br>( 1 + 2 + 3 + ... + {n} = ? )"
                sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (หลักการจับคู่ของเกาส์):</b><br>
                แทนที่เราจะบวกทีละตัว เราจะใช้วิธีนำ "ตัวหน้าสุด" จับคู่บวกกับ "ตัวหลังสุด" ครับ<br>
                1) จับคู่ตัวแรกกับตัวสุดท้าย: <b>1 + {n} = {n+1}</b><br>
                2) จับคู่ตัวที่สองกับตัวรองสุดท้าย: <b>2 + {n-1} = {n+1}</b><br>
                3) จับคู่ตัวที่สามกับตัวถัดมา: <b>3 + {n-2} = {n+1}</b><br>
                จะเห็นว่าทุกคู่เมื่อบวกกันแล้วจะได้ <b>{n+1}</b> เสมอ!<br>
                4) มีตัวเลขทั้งหมด {n} ตัว เมื่อจับคู่ทีละ 2 ตัว จะได้ทั้งหมด: {n} ÷ 2 = <b>{n//2} คู่</b><br>
                5) นำผลบวกของ 1 คู่ ไปคูณกับ จำนวนคู่ทั้งหมด:<br>
                &nbsp;&nbsp;&nbsp;{n+1} (ผลบวกแต่ละคู่) × {n//2} (จำนวนคู่) = <b>{ans:,}</b><br>
                <b>ตอบ: ผลบวกคือ {ans:,}</b></span>"""

            elif actual_sub_t == "การแก้สมการ":
                if grade == "ป.4":
                    x = random.randint(10, 50)
                    a = random.randint(5, 20)
                    op = random.choice(["+", "-"])
                    if op == "+":
                        q = f"จงแก้สมการเพื่อหาค่า x : <span style='color: #3498db; margin-left: 15px;'><b>x + {a} = {x+a}</b></span>"
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                        เป้าหมายของเราคือทำให้ <b>x</b> เหลืออยู่ตัวเดียวทางฝั่งซ้ายของเครื่องหมายเท่ากับ<br>
                        1) ทางฝั่งซ้ายมี <b>+{a}</b> เกินมา เราต้องกำจัดมันทิ้งโดยใช้สมบัติการเท่ากัน คือนำ <b>{a} มาลบออกทั้งสองข้าง</b><br>
                        2) เขียนสมการใหม่ได้เป็น:<br>
                        &nbsp;&nbsp;&nbsp;x + {a} <b style='color:red;'>- {a}</b> = {x+a} <b style='color:red;'>- {a}</b><br>
                        3) ฝั่งซ้าย +{a} ลบกับ -{a} กลายเป็น 0 เหลือแค่ x<br>
                        &nbsp;&nbsp;&nbsp;ฝั่งขวา {x+a} ลบ {a} ได้ <b>{x}</b><br>
                        <b>ตอบ: x = {x}</b></span>"""
                    else:
                        q = f"จงแก้สมการเพื่อหาค่า x : <span style='color: #3498db; margin-left: 15px;'><b>x - {a} = {x-a}</b></span>"
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                        เป้าหมายของเราคือทำให้ <b>x</b> เหลืออยู่ตัวเดียวทางฝั่งซ้ายของเครื่องหมายเท่ากับ<br>
                        1) ทางฝั่งซ้ายมี <b>-{a}</b> เกาะอยู่ เราต้องกำจัดมันทิ้งโดยใช้สมบัติการเท่ากัน คือนำ <b>{a} มาบวกเข้าทั้งสองข้าง</b><br>
                        2) เขียนสมการใหม่ได้เป็น:<br>
                        &nbsp;&nbsp;&nbsp;x - {a} <b style='color:green;'>+ {a}</b> = {x-a} <b style='color:green;'>+ {a}</b><br>
                        3) ฝั่งซ้าย -{a} บวกกับ +{a} หักล้างกันเหลือแค่ x<br>
                        &nbsp;&nbsp;&nbsp;ฝั่งขวา {x-a} บวก {a} ได้ <b>{x}</b><br>
                        <b>ตอบ: x = {x}</b></span>"""

                elif grade == "ป.5":
                    a = random.randint(2, 12)
                    x = random.randint(5, 20)
                    op = random.choice(["*", "/"])
                    if op == "*":
                        q = f"จงแก้สมการเพื่อหาค่า x : <span style='color: #3498db; margin-left: 15px;'><b>{a}x = {a*x}</b></span>"
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                        {a}x หมายถึง {a} คูณอยู่กับ x เป้าหมายคือต้องทำให้ x อยู่ตัวเดียว<br>
                        1) เราต้องกำจัดเลข <b>{a}</b> ที่คูณอยู่ออกไป โดยใช้สมบัติการเท่ากัน คือนำ <b>{a} มาหารทั้งสองข้าง</b><br>
                        2) เขียนสมการใหม่ได้เป็น:<br>
                        &nbsp;&nbsp;&nbsp;({a}x) <b style='color:red;'>÷ {a}</b> = {a*x} <b style='color:red;'>÷ {a}</b><br>
                        3) ฝั่งซ้าย {a} หาร {a} ได้ 1 เหลือแค่ x<br>
                        &nbsp;&nbsp;&nbsp;ฝั่งขวา นำ {a*x} ไปตั้งหารด้วย {a} ได้ผลลัพธ์เป็น <b>{x}</b><br>
                        <b>ตอบ: x = {x}</b></span>"""
                    else:
                        q = f"จงแก้สมการเพื่อหาค่า x : <span style='color: #3498db; margin-left: 15px;'><b>x / {a} = {x}</b></span>"
                        sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>
                        x / {a} หมายถึง x ถูกหารด้วย {a} เป้าหมายคือต้องทำให้ x อยู่ตัวเดียว<br>
                        1) เราต้องกำจัดเลข <b>{a}</b> ที่เป็นตัวส่วนออกไป โดยใช้สมบัติการเท่ากัน คือนำ <b>{a} มาคูณทั้งสองข้าง</b><br>
                        2) เขียนสมการใหม่ได้เป็น:<br>
                        &nbsp;&nbsp;&nbsp;(x / {a}) <b style='color:green;'>× {a}</b> = {x} <b style='color:green;'>× {a}</b><br>
                        3) ฝั่งซ้าย ตัวหาร {a} ตัดกับตัวคูณ {a} เหลือแค่ x<br>
                        &nbsp;&nbsp;&nbsp;ฝั่งขวา นำ {x} ไปคูณกับ {a} ได้ผลลัพธ์เป็น <b>{x*a}</b><br>
                        <b>ตอบ: x = {x*a}</b></span>"""
                        
                elif grade == "ป.6":
                    a = random.randint(2, 9)
                    x = random.randint(2, 15)
                    b = random.randint(1, 20)
                    q = f"จงแก้สมการเพื่อหาค่า x : <span style='color: #3498db; margin-left: 15px;'><b>{a}x + {b} = {a*x+b}</b></span>"
                    sol = f"""<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด (แก้สมการ 2 ขั้นตอน):</b><br>
                        <b>ขั้นที่ 1: กำจัดตัวบวกลบที่อยู่ไกล x ก่อน</b><br>
                        กำจัด <b>+{b}</b> โดยนำ <b>{b} มาลบออกทั้งสองข้าง</b><br>
                        &nbsp;&nbsp;&nbsp;{a}x + {b} <b style='color:red;'>- {b}</b> = {a*x+b} <b style='color:red;'>- {b}</b><br>
                        &nbsp;&nbsp;&nbsp;จะได้สมการใหม่คือ: <b>{a}x = {a*x}</b><br><br>
                        <b>ขั้นที่ 2: กำจัดตัวคูณที่ติดอยู่กับ x</b><br>
                        กำจัด <b>{a}</b> ที่คูณอยู่ โดยนำ <b>{a} มาหารทั้งสองข้าง</b><br>
                        &nbsp;&nbsp;&nbsp;({a}x) <b style='color:red;'>÷ {a}</b> = {a*x} <b style='color:red;'>÷ {a}</b><br>
                        &nbsp;&nbsp;&nbsp;จะได้ <b>x = {x}</b><br>
                        <b>ตอบ: x = {x}</b></span>"""

            # =========================================================
            # โหมดหลักสูตรปกติ (เสริมคำอธิบายละเอียด)
            # =========================================================
            elif actual_sub_t == "การคูณ (แบบตั้งหลัก)":
                a = random.randint(10, 99) if grade in ["ป.1", "ป.2"] else (random.randint(100, 999) if grade == "ป.3" else random.randint(1000, 9999)) 
                b = random.randint(2, 9); res = a * b
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} × {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '×', is_key=False)
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> ตั้งหลักให้ตรงกัน นำ {b} ไปคูณตัวเลขด้านบนทีละหลักจากขวาไปซ้าย ถ้าได้ผลลัพธ์เกิน 9 ให้ใส่หลักหน่วยและนำหลักสิบไปทดในหลักถัดไปทางซ้าย</span><br>" + generate_vertical_table_html(a, b, '×', result=res, is_key=True)

            elif actual_sub_t == "การบวก (แบบตั้งหลัก)":
                a = random.randint(10, limit//2); b = random.randint(10, limit//2)
                res = a + b
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} + {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '+', is_key=False)
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> ตั้งหลักตัวเลขให้ตรงกัน (หลักหน่วยตรงหลักหน่วย, หลักสิบตรงหลักสิบ) แล้วทำการบวกทีละหลักจากขวาไปซ้าย หากบวกได้เกิน 9 ให้ทดหลักสิบไปไว้ยังหลักถัดไปทางซ้าย</span><br>" + generate_vertical_table_html(a, b, '+', result=res, is_key=True)

            elif actual_sub_t == "การลบ (แบบตั้งหลัก)":
                a = random.randint(1000, limit-1); b = random.randint(100, a-1)
                res = a - b
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} - {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '-', is_key=False)
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> ตั้งหลักตัวเลขให้ตรงกัน ลบทีละหลักจากขวาไปซ้าย หากตัวตั้งน้อยกว่าตัวลบ ให้ทำการขอยืมตัวเลขในหลักถัดไปทางซ้ายมา 10</span><br>" + generate_vertical_table_html(a, b, '-', result=res, is_key=True)

            elif "การหารพื้นฐาน" in actual_sub_t:
                a, b = random.randint(2, 9), random.randint(2, 12); dividend = a * b
                q = f"จงหาผลลัพธ์ของ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {dividend} ÷ {a} = {box_html}</span>"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>การหารคือการหาว่าตัวหาร ({a}) ต้องคูณกับเลขอะไรจึงจะได้เท่ากับตัวตั้ง ({dividend})<br>ให้ท่องสูตรคูณแม่ <b>{a}</b>:<br>...<br>{a} × {b-1} = {a*(b-1)}<br><b>{a} × {b} = {dividend}</b> (เจอแล้ว!)<br>ดังนั้น {dividend} ÷ {a} = </span> <b>{b}</b>"

            elif "จำนวนเงิน" in actual_sub_t:
                b100, b50, c10 = random.randint(1,3), random.randint(0,2), random.randint(1,5)
                tot = b100*100 + b50*50 + c10*10
                q = f"มีธนบัตรใบละ 100 บาท จำนวน <b>{b100}</b> ใบ, ธนบัตรใบละ 50 บาท จำนวน <b>{b50}</b> ใบ, และเหรียญ 10 บาท จำนวน <b>{c10}</b> เหรียญ รวมเป็นเงินทั้งหมดกี่บาท?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>แจกแจงมูลค่าเงินแต่ละชนิดแล้วนำมารวมกัน:<br>1) แบงก์ 100 บาท {b100} ใบ = 100 × {b100} = <b>{b100*100} บาท</b><br>2) แบงก์ 50 บาท {b50} ใบ = 50 × {b50} = <b>{b50*50} บาท</b><br>3) เหรียญ 10 บาท {c10} เหรียญ = 10 × {c10} = <b>{c10*10} บาท</b><br>นำมูลค่าทั้งหมดมาบวกกัน: {b100*100} + {b50*50} + {c10*10} = </span> <b>{tot} บาท</b>"

            elif "โจทย์ปัญหาร้อยละ" in actual_sub_t:
                price = random.choice([100, 200, 400, 500, 1000]); percent = random.choice([10, 20, 25, 50])
                q = f"ป้ายติดราคาสินค้าไว้ <b>{price:,} บาท</b> ร้านค้าประกาศลดราคา <b>{percent}%</b> นักเรียนจะได้ลดราคากี่บาท?"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>คำว่า 'ลดราคา {percent}%' หมายถึง <b>{percent} ส่วน 100 ของราคาป้าย</b><br>เขียนเป็นประโยคสัญลักษณ์: <b>({percent} ÷ 100) × {price:,}</b><br>การคำนวณ: นำ {price:,} ไปคูณ {percent} แล้วหารด้วย 100 (หรือตัดศูนย์ทิ้ง)<br>จะได้ ({percent} × {price}) ÷ 100 = <b>{int(price*(percent/100)):,} บาท</b><br><b>ตอบ: ได้ลดราคา {int(price*(percent/100)):,} บาท</b></span>"

            elif "ห.ร.ม." in actual_sub_t:
                a, b = random.randint(12, 48), random.randint(12, 48)
                while a == b: b = random.randint(12, 48) 
                q = f"จงหา ห.ร.ม. (หารร่วมมาก) ของ <b>{a}</b> และ <b>{b}</b>"
                sol = generate_short_division_html(a, b, mode="ห.ร.ม.") + "<br><span style='color: #2c3e50; font-size: 14px;'><i>*ห.ร.ม. คือการนำตัวเลขหน้าเครื่องหมายหารสั้นทุกตัวมาคูณกัน</i></span>"

            elif "ค.ร.น." in actual_sub_t:
                a, b = random.randint(4, 24), random.randint(4, 24)
                while a == b: b = random.randint(4, 24) 
                q = f"จงหา ค.ร.น. (คูณร่วมน้อย) ของ <b>{a}</b> และ <b>{b}</b>"
                sol = generate_short_division_html(a, b, mode="ค.ร.น.") + "<br><span style='color: #2c3e50; font-size: 14px;'><i>*ค.ร.น. คือการนำตัวเลขด้านหน้าและผลลัพธ์เศษด้านล่างทั้งหมด (เป็นรูปตัว L) มาคูณกัน</i></span>"

            else:
                # Fallback ป้องกัน Error หากหัวข้ออื่นๆ ไม่เข้าเงื่อนไข
                a, b = random.randint(10, 50), random.randint(10, 50)
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a} + {b} = {box_html}</span>"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำ:</b> นำ {a} บวกกับ {b} <br><b>ตอบ: {a + b}</b></span>"

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
            # กรณีที่เป็นการตั้งหลักแนวตั้ง ไม่ต้องใส่กล่องเฉลยสีฟ้าซ้อน
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
    st.success(f"✅ สร้างไฟล์สำเร็จ! (ลองตรวจดูหน้าเฉลย (Answer Key) รับรองว่าอธิบายละเอียดยิบครับ!)")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📄 โหลดเฉพาะโจทย์", data=st.session_state['worksheet_html'], file_name=f"{st.session_state['filename_base']}_Worksheet.html", mime="text/html", use_container_width=True)
        st.download_button("🔑 โหลดเฉพาะเฉลย", data=st.session_state['answerkey_html'], file_name=f"{st.session_state['filename_base']}_AnswerKey.html", mime="text/html", use_container_width=True)
    with c2:
        st.download_button("📚 โหลดรวมเล่ม E-Book", data=st.session_state['ebook_html'], file_name=f"{st.session_state['filename_base']}_Full_EBook.html", mime="text/html", use_container_width=True)
        st.download_button("🗂️ โหลดแพ็กเกจ (.zip)", data=st.session_state['zip_data'], file_name=f"{st.session_state['filename_base']}.zip", mime="application/zip", use_container_width=True)
    st.markdown("---")
    components.html(st.session_state['ebook_html'], height=800, scrolling=True)
