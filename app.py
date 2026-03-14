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
    div[data-testid="stSidebar"] div.stButton > button { background-color: #27ae60; color: white; border-radius: 8px; height: 3.5rem; font-size: 18px; font-weight: bold; border: none; }
    div.stDownloadButton > button { border-radius: 8px; font-weight: bold; border: 1px solid #bdc3c7; }
    .main-header { background: linear-gradient(135deg, #2980b9, #2c3e50); padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem; }
    .main-header h1 { margin: 0; font-size: 2.5rem; font-weight: 800; }
</style>""", unsafe_allow_html=True)
st.markdown("""<div class="main-header"><h1>🚀 Math Worksheet Pro <span style="font-size: 20px; background: #f39c12; padding: 5px 15px; border-radius: 20px; vertical-align: middle;">National Edition</span></h1>
<p>ระบบสร้างสื่อการสอน ป.1-ป.6 + ข้อสอบแข่งขัน TMC (พร้อมเฉลยละเอียดแบบ Step-by-Step ทุกหัวข้อ 100%)</p></div>""", unsafe_allow_html=True)

NAMES = ["อคิณ", "นาวิน", "ภูผา", "สายฟ้า", "เจ้านาย", "ข้าวหอม", "ใบบัว", "มะลิ", "น้ำใส", "ญาญ่า", "ปลื้ม", "พายุ", "ไออุ่น", "กะทิ", "เวลา", "ของขวัญ", "มังกร", "ฉลาม", "ปลาวาฬ", "มาคิน"]
LOCS = ["โรงเรียน", "สวนสัตว์", "สวนสนุก", "ห้างสรรพสินค้า", "ห้องสมุด", "สวนสาธารณะ", "ร้านของเล่น", "ร้านเบเกอรี่", "ค่ายลูกเสือ", "พิพิธภัณฑ์"]
ITEMS = ["ลูกแก้ว", "สติกเกอร์", "การ์ดพลัง", "โมเดลรถ", "ตุ๊กตาหมี", "สมุดระบายสี", "ดินสอสี", "ลูกโป่ง", "ยางลบ", "ตัวต่อเลโก้", "หนังสือการ์ตูน", "ลูกบอล"]
SNACKS = ["ช็อกโกแลต", "คุกกี้", "โดนัท", "เยลลี่", "ขนมปัง", "ไอศกรีม", "น้ำผลไม้", "นมเย็น", "ลูกอม", "เค้ก"]
ANIMALS = ["แมงมุม", "มดแดง", "กบ", "จิ้งจก", "ตั๊กแตน", "เต่า"]

tmc_lower = ["ปริศนาตัวเลขซ่อนแอบ", "สัตว์ปีนบ่อ", "ตรรกะตาชั่งสมดุล", "ปัญหาผลรวม-ผลต่าง", "ตรรกะการจับมือ (ทักทาย)", "โปรโมชั่นแลกของ", "หยิบของในที่มืด", "คิววงกลมมรณะ"]
tmc_mid = ["ผลบวกจำนวนเรียงกัน (Gauss)", "พื้นที่แรเงา (เรขาคณิต)", "การตัดเชือกพับทบ", "แถวคอยแบบซ้อนทับ", "อายุข้ามเวลาขั้นสูง", "แผนภาพความชอบ (Venn)", "การนับหน้าหนังสือ", "วันที่และปฏิทิน"]
tmc_upper = ["ความเร็ววิ่งสวนทาง", "งานและเวลา (Work)", "ระฆังและไฟกะพริบ (ค.ร.น.)", "อัตราส่วนอายุ", "เศษส่วนของที่เหลือ", "เส้นทางที่เป็นไปได้", "จัดของใส่กล่อง (Modulo)", "นาฬิกาเดินเพี้ยน", "คะแนนยิงเป้า"]

curriculum_db = {
    "ป.1": {
        "จำนวนนับ 1 ถึง 100 และ 0": ["การนับทีละ 1", "การนับทีละ 10", "การอ่านและการเขียนตัวเลข", "ส่วนย่อย-ส่วนรวม", "แบบรูปซ้ำ", "การบอกอันดับที่", "รูปกระจาย", "การเปรียบเทียบจำนวน", "การเรียงลำดับจำนวน"],
        "การบวก การลบ": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)"], "แผนภูมิรูปภาพ": ["การอ่านแผนภูมิรูปภาพ"], "🌟 โจทย์แข่งขัน (แนว TMC)": tmc_lower
    },
    "ป.2": {
        "จำนวนนับไม่เกิน 1,000 และ 0": ["การนับทีละ 2, 5, 10, 100", "การอ่านและการเขียนตัวเลข", "จำนวนคู่ จำนวนคี่", "รูปกระจาย", "การเปรียบเทียบจำนวน", "การเรียงลำดับจำนวน"],
        "เวลาและการวัด": ["นาฬิกา", "เครื่องชั่งสปริง"], "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การคูณ (แบบตั้งหลัก)", "การหารพื้นฐาน"], "แผนภูมิรูปภาพ": ["การอ่านแผนภูมิรูปภาพ"], "🌟 โจทย์แข่งขัน (แนว TMC)": tmc_lower
    },
    "ป.3": {
        "จำนวนนับและเศษส่วน": ["การอ่าน การเขียนตัวเลข", "รูปกระจาย", "การเปรียบเทียบจำนวน", "การเรียงลำดับจำนวน", "อ่านและเขียนเศษส่วน", "บวกลบเศษส่วน"],
        "เวลา เงิน และการวัด": ["นาฬิกา", "จำนวนเงิน", "เครื่องชั่งสปริง"], "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การคูณ (แบบตั้งหลัก)", "หารยาว"], "แผนภูมิรูปภาพ": ["การอ่านแผนภูมิรูปภาพ"], "🌟 โจทย์แข่งขัน (แนว TMC)": tmc_mid
    },
    "ป.4": {
        "จำนวนนับ": ["การอ่าน การเขียนตัวเลข", "รูปกระจาย", "การเปรียบเทียบจำนวน", "ค่าประมาณ"], "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การคูณ (แบบตั้งหลัก)", "หารยาว"],
        "เศษส่วนและทศนิยม": ["เศษเกินเป็นจำนวนคละ", "อ่านทศนิยม"], "เรขาคณิตและการวัด": ["ชนิดของมุม", "ไม้โปรแทรกเตอร์", "ความยาวรอบรูปและพื้นที่"], "สมการ": ["การแก้สมการ (+/-)"], "🌟 โจทย์แข่งขัน (แนว TMC)": tmc_mid
    },
    "ป.5": {
        "เศษส่วน": ["บวกลบเศษส่วน", "คูณหารเศษส่วน"], "ทศนิยม": ["บวกลบทศนิยม", "คูณทศนิยม"], "ร้อยละและเปอร์เซ็นต์": ["ร้อยละเศษส่วน"], "สมการ": ["การแก้สมการ (คูณ/หาร)"], "🌟 โจทย์แข่งขัน (แนว TMC)": tmc_upper
    },
    "ป.6": {
        "ตัวประกอบ": ["ห.ร.ม.", "ค.ร.น."], "อัตราส่วนและร้อยละ": ["อัตราส่วนที่เท่ากัน", "โจทย์ปัญหาอัตราส่วน", "โจทย์ปัญหาร้อยละ"], "สมการ": ["การแก้สมการ (2 ขั้นตอน)"], "🌟 โจทย์แข่งขัน (แนว TMC)": tmc_upper
    }
}

box_html = "<span style='display: inline-block; width: 22px; height: 22px; border: 2px solid #333; border-radius: 3px; vertical-align: middle; margin-left: 5px; position: relative; top: -2px;'></span>"
def get_prefix(grade): return "<b style='color:#2c3e50; margin-right:5px;'>ประโยคสัญลักษณ์:</b>" if grade in ["ป.1","ป.2","ป.3"] else ""
def generate_fraction_html(n, d, c="#000"): return f"<div style='display:inline-flex; flex-direction:column; align-items:center; vertical-align:middle; margin:0 5px; font-family:Sarabun;'><span style='font-size:20px; font-weight:bold; border-bottom:2px solid {c}; padding:0 4px; line-height:1.1; color:{c};'>{n}</span><span style='font-size:20px; font-weight:bold; padding:0 4px; line-height:1.1; color:{c};'>{d}</span></div>"
def generate_mixed_html(w, n, d): return f"<div style='display:inline-flex; align-items:center; vertical-align:middle; margin:0 5px; font-family:Sarabun;'><span style='font-size:24px; font-weight:bold; margin-right:4px; color:red;'>{w}</span><div style='display:inline-flex; flex-direction:column; align-items:center;'><span style='font-size:20px; font-weight:bold; border-bottom:2px solid red; padding:0 4px; line-height:1.1; color:red;'>{n}</span><span style='font-size:20px; font-weight:bold; padding:0 4px; line-height:1.1; color:red;'>{d}</span></div></div>"

def generate_vertical_table_html(a, b, op, result=None, is_key=False):
    nl = max(len(str(a)), len(str(b)), len(str(result)) if result else 0) + 1
    sa, sb = str(a).rjust(nl, " "), str(b).rjust(nl, " "); stk, tm = [False]*nl, [""]*nl
    if is_key:
        if op == '+':
            c = 0
            for i in range(nl-1, -1, -1):
                s = (int(sa[i]) if sa[i].strip() else 0) + (int(sb[i]) if sb[i].strip() else 0) + c
                c = s//10
                if c > 0 and i > 0: tm[i-1] = str(c)
        elif op == '-':
            ad, bd = [int(x) if x.strip() else 0 for x in sa], [int(x) if x.strip() else 0 for x in sb]
            for i in range(nl-1, -1, -1):
                if ad[i] < bd[i]:
                    for j in range(i-1, -1, -1):
                        if ad[j] > 0 and sa[j].strip():
                            stk[j] = True; ad[j] -= 1; tm[j] = str(ad[j])
                            for k in range(j+1, i): stk[k] = True; ad[k] = 9; tm[k] = "9"
                            stk[i] = True; ad[i] += 10; tm[i] = str(ad[i]); break
        elif op == '×':
            c, ad = 0, [int(x) if x.strip() else 0 for x in sa]
            for i in range(nl-1, -1, -1):
                if not sa[i].strip():
                    if c > 0: tm[i] = str(c); c = 0
                    continue
                p = ad[i] * b + c; c = p // 10
                if c > 0 and i > 0: tm[i-1] = str(c)
    at = "".join([f'<td style="width:35px; text-align:center; height:50px; vertical-align:bottom;">{(f"<div style=\'position:relative;\'><span style=\'position:absolute; top:-25px; left:50%; transform:translateX(-50%); font-size:20px; color:red; font-weight:bold;\'>{tm[i]}</span><span style=\'text-decoration:line-through; text-decoration-color:red;\'>{sa[i]}</span></div>" if stk[i] and is_key else (f"<div style=\'position:relative;\'><span style=\'position:absolute; top:-25px; left:50%; transform:translateX(-50%); font-size:20px; color:red; font-weight:bold;\'>{tm[i]}</span>{sa[i]}</div>" if tm[i] and is_key else sa[i])) if sa[i].strip() else ""}</td>' for i in range(nl)])
    bt = "".join([f'<td style="width:35px; text-align:center; border-bottom:2px solid #000; height:40px; vertical-align:bottom;">{sb[i].strip()}</td>' for i in range(nl)])
    rt = "".join([f'<td style="width:35px; text-align:center; color:red; font-weight:bold; height:45px; vertical-align:bottom;">{str(result).rjust(nl, " ")[i].strip()}</td>' for i in range(nl)]) if is_key else "".join([f'<td style="width:35px; height:45px;"></td>' for _ in range(nl)])
    return f"<div style='display:block; text-align:center; margin-top:10px;'><div style='display:inline-block; font-size:38px;'><table style='border-collapse:collapse;'><tr><td style='width:20px;'></td>{at}<td style='width:50px; text-align:center; vertical-align:middle;' rowspan='2'>{op}</td></tr><tr><td></td>{bt}</tr><tr><td></td>{rt}<td></td></tr><tr><td></td><td colspan='{nl}' style='border-bottom:6px double #000; height:10px;'></td><td></td></tr></table></div></div>"

def generate_decimal_vertical_html(a, b, op, is_key=False):
    sa, sb = f"{a:.2f}", f"{b:.2f}"; ans = a + b if op == '+' else round(a - b, 2); sr = f"{ans:.2f}"
    nl = max(len(sa), len(sb), len(sr)) + 1; sa, sb, sr = sa.rjust(nl, " "), sb.rjust(nl, " "), sr.rjust(nl, " ")
    stk, tm = [False]*nl, [""]*nl
    if is_key:
        if op == '+':
            c = 0
            for i in range(nl-1, -1, -1):
                if sa[i] == '.': continue
                s = (int(sa[i]) if sa[i].strip() else 0) + (int(sb[i]) if sb[i].strip() else 0) + c; c = s//10
                if c > 0 and i > 0: tm[i-1 if sa[i-1] != '.' else i-2] = str(c)
        elif op == '-':
            ad, bd = [int(x) if x.strip() and x != '.' else 0 for x in sa], [int(x) if x.strip() and x != '.' else 0 for x in sb]
            for i in range(nl-1, -1, -1):
                if sa[i] == '.': continue
                if ad[i] < bd[i]:
                    for j in range(i-1, -1, -1):
                        if sa[j] == '.': continue
                        if ad[j] > 0 and sa[j].strip():
                            stk[j] = True; ad[j] -= 1; tm[j] = str(ad[j])
                            for k in range(j+1, i):
                                if sa[k] == '.': continue
                                stk[k] = True; ad[k] = 9; tm[k] = "9"
                            stk[i] = True; ad[i] += 10; tm[i] = str(ad[i]); break
    at = "".join([f'<td style="width:35px; text-align:center; height:50px; vertical-align:bottom;">{(f"<div style=\'position:relative;\'><span style=\'position:absolute; top:-25px; left:50%; transform:translateX(-50%); font-size:20px; color:red; font-weight:bold;\'>{tm[i]}</span><span style=\'text-decoration:line-through; text-decoration-color:red;\'>{sa[i]}</span></div>" if stk[i] and is_key else (f"<div style=\'position:relative;\'><span style=\'position:absolute; top:-25px; left:50%; transform:translateX(-50%); font-size:20px; color:red; font-weight:bold;\'>{tm[i]}</span>{sa[i]}</div>" if tm[i] and is_key else sa[i])) if sa[i].strip() else ""}</td>' for i in range(nl)])
    bt = "".join([f'<td style="width:35px; text-align:center; border-bottom:2px solid #000; height:40px; vertical-align:bottom;">{sb[i].strip() if sb[i].strip() else ("." if sb[i]=="." else "")}</td>' for i in range(nl)])
    rt = "".join([f'<td style="width:35px; text-align:center; color:red; font-weight:bold; height:45px; vertical-align:bottom;">{sr[i].strip() if sr[i].strip() else ("." if sr[i]=="." else "")}</td>' for i in range(nl)]) if is_key else "".join([f'<td style="width:35px; height:45px;"></td>' for _ in range(nl)])
    return f"<div style='display:block; text-align:center; margin-top:10px;'><div style='display:inline-block; font-size:38px;'><table style='border-collapse:collapse;'><tr><td style='width:20px;'></td>{at}<td style='width:50px; text-align:center; vertical-align:middle;' rowspan='2'>{op}</td></tr><tr><td></td>{bt}</tr><tr><td></td>{rt}<td></td></tr><tr><td></td><td colspan='{nl}' style='border-bottom:6px double #000; height:10px;'></td><td></td></tr></table></div></div>"

def generate_short_division_html(a, b, mode):
    f, ca, cb, stp = [], a, b, ""
    while True:
        fd = False
        for i in range(2, min(ca, cb) + 1):
            if ca % i == 0 and cb % i == 0:
                stp += f"<tr><td style='text-align:right; padding-right:10px; font-weight:bold; color:red;'>{i}</td><td style='border-left:2px solid #000; border-bottom:2px solid #000; padding:5px 15px;'>{ca}</td><td style='border-bottom:2px solid #000; padding:5px 15px;'>{cb}</td></tr>"
                f.append(i); ca //= i; cb //= i; fd = True; break
        if not fd: break
    stp += f"<tr><td></td><td style='padding:5px 15px;'>{ca}</td><td style='padding:5px 15px;'>{cb}</td></tr>"
    ans = math.prod(f) if mode == "ห.ร.ม." else math.prod(f)*ca*cb
    cstr = " × ".join(map(str, f)) if mode == "ห.ร.ม." else " × ".join(map(str, f+[ca, cb]))
    if not f: return f"<span style='color:#2c3e50;'><b>วิธีทำ:</b> ไม่มีตัวประกอบร่วมที่หารลงตัว<br><b>{mode} = {1 if mode=='ห.ร.ม.' else a*b}</b></span>"
    return f"<span style='color:#2c3e50;'><b>วิธีทำ (ตั้งหารสั้น):</b> หาเลขที่หารทั้งสองจำนวนลงตัวมาหารเรื่อยๆ</span><br><table style='margin:10px 0; font-size:20px; border-collapse:collapse;'>{stp}</table><span style='color:#2c3e50;'><b>{mode}</b> = {cstr} = <b>{ans}</b></span>"

def generate_thai_num(num_str):
    tn = ["ศูนย์", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
    pos = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]
    s = str(num_str).split(".")[0]; r = ""; l = len(s)
    if s == "0": return "ศูนย์"
    for i, d in enumerate(s):
        v, p = int(d), l-i-1
        if v == 0: continue
        if p == 1 and v == 2: r += "ยี่สิบ"
        elif p == 1 and v == 1: r += "สิบ"
        elif p == 0 and v == 1 and l > 1: r += "เอ็ด"
        else: r += tn[v] + pos[p]
    return r

# ==========================================
# 🧠 CORE LOGIC & DETAILED EXPLANATIONS
# ==========================================
def generate_questions_logic(grade, main_t, sub_t, num_q):
    questions, seen = [], set()
    lim = {"ป.1":100, "ป.2":1000, "ป.3":100000, "ป.4":1000000, "ป.5":9000000, "ป.6":9000000}.get(grade, 100)

    for _ in range(num_q):
        q, sol, att = "", "", 0
        while att < 300:
            act_sub = random.choice(curriculum_db[grade][random.choice([m for m in curriculum_db[grade] if m != "🌟 โหมดพิเศษ (สุ่มทุกเรื่อง)"])]) if sub_t == "แบบทดสอบรวมปลายภาค" else (random.choice(comp_topics) if sub_t == "🌟 สุ่มรวมทุกแนว" else sub_t)
            pre = get_prefix(grade)

            # --- โหมดแข่งขัน TMC (เฉลยละเอียดยิบ) ---
            if act_sub == "ปริศนาตัวเลขซ่อนแอบ":
                a = random.randint(1, 4); b = random.randint(a+2, 9); diff = b-a; k = diff*9; s_val = a+b
                q = f"ให้ A และ B เป็นเลขโดดที่ต่างกัน โดย <b>AB + {k} = BA</b> และ <b>A + B = {s_val}</b> <br>จงหาว่าจำนวนสองหลัก <b>AB</b> คือจำนวนใด?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) จาก AB + {k} = BA ใช้สมบัติการลบ นำ AB ลบออกทั้งสองข้าง จะได้ BA - AB = {k}<br>2) เลขสลับหลักลบกัน ผลต่างจะเท่ากับ (B - A) × 9 เสมอ<br>ดังนั้นหาผลต่างได้โดย: B - A = {k} ÷ 9 = <b>{diff}</b><br>3) เรารู้ว่า A + B = <b>{s_val}</b> (จากโจทย์)<br>4) หาเลข 2 ตัวที่บวกได้ {s_val} ลบได้ {diff}: นำ ({s_val} + {diff}) ÷ 2 = <b>{b} (คือ B)</b><br>หา A โดยนำ {s_val} - {b} = <b>{a} (คือ A)</b><br><b>ตอบ: จำนวน AB คือ {a}{b}</b></span>"

            elif act_sub == "การนับหน้าหนังสือ":
                p = random.randint(40, 150); ans = 9 + 180 + ((p-99)*3) if p>99 else 9 + ((p-9)*2)
                q = f"สมุดภาพ<b>{random.choice(ITEMS)}</b> มี <b>{p}</b> หน้า ต้องพิมพ์ตัวเลขหน้า 1 ถึง {p} ต้องใช้เลขโดดรวมกี่ตัว?"
                if p > 99: sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>แบ่งนับตามกลุ่มหลัก:<br>1) หน้า 1-9 (เลข 1 หลัก) มี 9 หน้า ใช้หน้าละ 1 ตัว = 9 × 1 = <b>9 ตัว</b><br>2) หน้า 10-99 (เลข 2 หลัก) มี 90 หน้า ใช้หน้าละ 2 ตัว = 90 × 2 = <b>180 ตัว</b><br>3) หน้า 100-{p} (เลข 3 หลัก) มี {p}-99 = {p-99} หน้า ใช้หน้าละ 3 ตัว = {p-99} × 3 = <b>{(p-99)*3} ตัว</b><br>นำทุกกลุ่มมารวมกัน: 9 + 180 + {(p-99)*3} = <b>{ans} ตัว</b></span>"
                else: sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>แบ่งนับตามกลุ่มหลัก:<br>1) หน้า 1-9 (เลข 1 หลัก) มี 9 หน้า ใช้หน้าละ 1 ตัว = 9 × 1 = <b>9 ตัว</b><br>2) หน้า 10-{p} (เลข 2 หลัก) มี {p}-9 = {p-9} หน้า ใช้หน้าละ 2 ตัว = {p-9} × 2 = <b>{(p-9)*2} ตัว</b><br>นำทุกกลุ่มมารวมกัน: 9 + {(p-9)*2} = <b>{ans} ตัว</b></span>"

            elif act_sub == "การปักเสาและปลูกต้นไม้":
                d = random.choice([2, 4, 5, 10, 15]); t = random.randint(12, 35); L = (t-1)*d
                q = f"ปลูกต้นไม้ริมถนนทางเข้า<b>{random.choice(LOCS)}</b> ห่างกันต้นละ <b>{d}</b> เมตร ปลูกหัวและท้ายพอดี ถ้านับได้ <b>{t}</b> ต้น ถนนเส้นนี้ยาวกี่เมตร?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) การปลูกต้นไม้ปิดหัวท้าย จำนวน 'ช่องว่าง' จะน้อยกว่าจำนวนต้นไม้อยู่ 1 เสมอ<br>2) มีต้นไม้ {t} ต้น จะมีช่องว่าง = {t} - 1 = <b>{t-1} ช่อง</b><br>3) แต่ละช่องห่าง {d} เมตร นำไปคูณกัน<br>ความยาวถนน = {t-1} × {d} = <b>{L} เมตร</b></span>"

            elif act_sub == "สัตว์ปีนบ่อ":
                u = random.randint(3,7); d = random.randint(1,u-1); h = random.randint(15,30); net = u-d; days = math.ceil((h-u)/net) + 1
                q = f"<b>{random.choice(ANIMALS)}</b>ตกบ่อลึก <b>{h}</b> เมตร กลางวันปีนขึ้นได้ <b>{u}</b> เมตร แต่กลางคืนลื่นลง <b>{d}</b> เมตร ต้องใช้เวลาอย่างน้อยกี่วันจึงจะปีนพ้นปากบ่อ?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) ใน 1 วัน (24 ชม.) ปีนได้สุทธิ: {u} - {d} = <b>{net} เมตร</b><br>2) <i>จุดหลอก:</i> วันสุดท้ายเมื่อพ้นบ่อจะไม่ลื่นลงมาอีก! ต้องแยกคิดระยะวันสุดท้าย<br>3) ระยะทางก่อนถึงวันสุดท้าย: {h} - {u} = <b>{h-u} เมตร</b><br>4) เวลาช่วงแรก: {h-u} ÷ {net} = <b>{math.ceil((h-u)/net)} วัน</b><br>5) รวมกับวันสุดท้ายอีก 1 วัน: {math.ceil((h-u)/net)} + 1 = <b>{days} วัน</b></span>"

            elif act_sub == "ตรรกะตาชั่งสมดุล":
                i1, i2, i3 = random.choice([("รถคันใหญ่", "รถคันเล็ก", "ลูกบอล"), ("แตงโม", "สับปะรด", "มะละกอ")])
                m1, m2 = random.randint(2,5), random.randint(2,5)
                q = f"ตาชั่งสมดุล:<br>- <b>{i1} 1 ชิ้น</b> หนักเท่ากับ <b>{i2} {m1} ชิ้น</b><br>- <b>{i2} 1 ชิ้น</b> หนักเท่ากับ <b>{i3} {m2} ชิ้น</b><br>อยากทราบว่า <b>{i1} 2 ชิ้น</b> จะหนักเท่ากับ <b>{i3}</b> กี่ชิ้น?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>เป้าหมายคือแปลงของใหญ่ให้เป็นของเล็กทีละทอด<br>1) เรารู้ว่า {i2} 1 ชิ้น แลกเป็น {i3} ได้ <b>{m2} ชิ้น</b><br>2) นำไปแทนค่าในบรรทัดแรก: {i1} 1 ชิ้น = {m1} กลุ่มของ {i2}<br>แปลงเป็น {i3} ได้ = {m1} × {m2} = <b>{m1*m2} ชิ้น</b><br>3) โจทย์ถามหา {i1} <b>2 ชิ้น</b> นำไปคูณ 2<br>{m1*m2} × 2 = <b>{m1*m2*2} ชิ้น</b></span>"

            elif act_sub == "อายุข้ามเวลาขั้นสูง":
                n1, n2, n3 = random.sample(NAMES, 3); a = random.randint(6,10); b = a + random.randint(2,5); c = b - random.randint(1, b-2)
                p = random.randint(2,5); curr = a+b+c; past = curr - (3*p)
                q = f"ปัจจุบัน {n1}, {n2}, {n3} อายุรวมกัน <b>{curr}</b> ปี <br>เมื่อ <b>{p}</b> ปีที่แล้ว ทั้งสามคนอายุรวมกันกี่ปี? (กำหนดให้ทุกคนเกิดแล้ว)"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) ปัจจุบัน ทั้ง 3 คนมีอายุรวมกัน = <b>{curr} ปี</b><br>2) <i>จุดหลอก:</i> เมื่อย้อนเวลาไป {p} ปี <b>ทุกคน (ทั้ง 3 คน)</b> จะอายุน้อยลงคนละ {p} ปี<br>3) อายุที่ต้องหักออกรวมกัน = 3 คน × {p} ปี = <b>{3*p} ปี</b><br>4) นำอายุรวมปัจจุบันลบด้วยอายุที่หักออก: {curr} - {3*p} = <b>{past} ปี</b></span>"

            elif act_sub == "การตัดเชือกพับทบ":
                f = random.randint(2,4); c = random.randint(2,5); ans = (2**f)*c + 1; n = random.choice(NAMES)
                q = f"<b>{n}</b>พับทบครึ่งริบบิ้น <b>{f}</b> ครั้ง (พับแล้วพับซ้ำ) แล้วใช้กรรไกรตัดริบบิ้นให้ขาด <b>{c}</b> รอยตัด <br>เมื่อคลี่ออกมาจะได้ริบบิ้นกี่เส้น?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) การพับทบครึ่งแต่ละครั้ง ทำให้ความหนาเพิ่มเป็น 2 เท่า<br>พับ {f} ครั้ง เกิดความหนา = 2 คูณกัน {f} ครั้ง = <b>{2**f} ชั้น</b><br>2) เมื่อใช้กรรไกรตัด 1 รอย จะได้ริบบิ้นเพิ่มมาเท่ากับจำนวนชั้น คือ {2**f} เส้น<br>3) ตัด {c} รอยตัด จะได้ริบบิ้นเพิ่ม = {2**f} × {c} = <b>{(2**f)*c} เส้น</b><br>4) นำไปบวกกับเส้นริบบิ้นตั้งต้นเดิมที่มีอยู่ 1 เส้น: {(2**f)*c} + 1 = <b>{ans} เส้น</b></span>"

            elif act_sub == "แถวคอยแบบซ้อนทับ":
                f, b = random.randint(10,20), random.randint(10,20); tot = f+b+random.randint(5,12); mid = tot-(f+b); n1, n2 = random.sample(NAMES, 2)
                q = f"นักเรียนเข้าแถวรอเข้า<b>{random.choice(LOCS)}</b> มีคนทั้งหมด <b>{tot}</b> คน<br>ถ้า <b>{n1}</b> ยืนลำดับที่ <b>{f}</b> นับจากหัวแถว และ <b>{n2}</b> ยืนลำดับที่ <b>{b}</b> นับจากท้ายแถว <br>มีคนยืนอยู่ระหว่าง <b>{n1}</b> กับ <b>{n2}</b> กี่คน? (กำหนดให้ {n1} ยืนอยู่หน้า {n2})"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>เราจะหาจำนวนคนตรงกลางได้ โดยเอาคนทั้งหมด ลบกลุ่มด้านหน้าและกลุ่มด้านหลังออกไป<br>1) ตั้งแต่หัวแถวจนถึง {n1} มีคนรวม <b>{f} คน</b> (นี่คือกลุ่มหน้า)<br>2) ตั้งแต่ท้ายแถวจนถึง {n2} มีคนรวม <b>{b} คน</b> (นี่คือกลุ่มหลัง)<br>3) นำคนทั้งแถว ลบด้วยกลุ่มหน้าและกลุ่มหลัง:<br>คนตรงกลาง = {tot} - ({f} + {b}) = <b>{mid} คน</b></span>"

            elif act_sub == "ปัญหาผลรวม-ผลต่าง":
                d = random.randint(5,20); s = random.randint(10,30); l = s+d; tot = l+s; n1, n2 = random.sample(NAMES, 2); itm = random.choice(ITEMS)
                q = f"<b>{n1}</b> และ <b>{n2}</b> มี<b>{itm}</b>รวมกัน <b>{tot}</b> ชิ้น หาก <b>{n1}</b> มีมากกว่า <b>{n2}</b> อยู่ <b>{d}</b> ชิ้น จงหาว่า <b>{n1}</b> มี<b>{itm}</b>กี่ชิ้น?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) ถ้าเราหยิบของที่ {n1} มี 'เกินมา' ({d} ชิ้น) ออกไปก่อน ของที่เหลือจะแบ่งให้ 2 คนได้เท่ากันพอดี<br>ของที่เหลือ: {tot} - {d} = <b>{tot-d} ชิ้น</b><br>2) นำของที่เหลือมาแบ่งครึ่ง (จะได้จำนวนของคนน้อย คือ {n2}):<br>{tot-d} ÷ 2 = <b>{s} ชิ้น</b><br>3) โจทย์ถามหาจำนวนของ {n1} (คนมาก) ให้นำจำนวนของ {n2} ไปบวกส่วนที่เกินกลับเข้ามา:<br>{s} + {d} = <b>{l} ชิ้น</b></span>"

            elif act_sub == "ตรรกะการจับมือ (ทักทาย)":
                n = random.randint(5,12); ans = sum(range(1, n))
                q = f"ในกิจกรรมที่<b>{random.choice(LOCS)}</b> มีเด็ก <b>{n}</b> คน หากทุกคนต้องเดินจับมือกันให้ครบทุกคน คนละ 1 ครั้ง จะเกิดการจับมือทั้งหมดกี่ครั้ง?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>นับการจับมือทีละคนเพื่อไม่ให้ซ้ำซ้อน<br>คนที่ 1: จับมือกับเพื่อนคนอื่นที่เหลือ <b>{n-1} คน</b><br>คนที่ 2: จับมือกับเพื่อนที่เหลือ (ไม่นับคนที่ 1 แล้ว) <b>{n-2} คน</b><br>คนที่ 3: จับกับเพื่อนที่เหลือ <b>{n-3} คน</b><br>ลดหลั่นไปเรื่อยๆ นำจำนวนมาบวกกัน: {' + '.join([str(x) for x in range(n-1, 0, -1)])} = <b>{ans} ครั้ง</b></span>"

            elif act_sub == "โปรโมชั่นแลกของ":
                ex = random.choice([3,4,5]); start = ex*random.randint(3,6); tot, emp = start, start; s = random.choice(SNACKS)
                q = f"โปรโมชั่น: นำซอง<b>{s}</b>เปล่า <b>{ex}</b> ซอง แลกฟรี 1 ชิ้น <br>ถ้าซื้อตอนแรก <b>{start}</b> ชิ้น จะได้กินรวมทั้งหมดกี่ชิ้น (รวมของที่นำไปแลกมาใหม่)?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>นำของเปล่าไปแลก แล้วนำเศษที่เหลือมารวมกับของใหม่เพื่อแลกต่อ<br>1) ตอนแรกซื้อกินไป <b>{start} ชิ้น</b> (เกิดซองเปล่า {start} ซอง)<br>2) นำซองเปล่า {start} ซอง ไปแลก: {start} ÷ {ex} = แลกได้อีก <b>{start//ex} ชิ้น</b> (เหลือเศษซอง {start%ex} ซอง)<br>ทำไปเรื่อยๆ และนำจำนวนชิ้นที่กินได้ทั้งหมดมาบวกกันจะได้ <b>{tot} ชิ้น</b></span>"

            elif act_sub == "หยิบของในที่มืด":
                c1, c2, c3 = random.randint(5,12), random.randint(5,12), random.randint(3,8); itm = random.choice(ITEMS)
                q = f"กล่องทึบมี<b>{itm}</b>สีแดง <b>{c1}</b> ชิ้น, สีน้ำเงิน <b>{c2}</b> ชิ้น และสีเขียว <b>{c3}</b> ชิ้น <br>หลับตาหยิบ ต้องหยิบ<b>อย่างน้อยกี่ชิ้น</b> จึงจะมั่นใจ 100% ว่าได้สีเขียวแน่ๆ 1 ชิ้น?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด (หลักการดวงซวยที่สุด):</b><br>เพื่อให้มั่นใจ 100% ต้องคิดกรณีที่โชคร้ายที่สุด คือหยิบได้สีอื่นจนหมดกล่องแล้วค่อยได้สีที่ต้องการ<br>1) สมมติหยิบได้สีแดงหมดเลย = <b>{c1} ชิ้น</b><br>2) สมมติหยิบได้สีน้ำเงินหมดเลย = <b>{c2} ชิ้น</b><br>ตอนนี้หยิบไปแล้ว {c1} + {c2} = <b>{c1+c2} ชิ้น</b> (แต่ยังไม่ได้สีเขียวเลย)<br>3) ชิ้นต่อไปที่จะหยิบ (บวกเพิ่มอีก 1) ในกล่องจะเหลือแต่สีเขียว จึงได้สีเขียวแน่นอน<br>ดังนั้นต้องหยิบอย่างน้อย {c1+c2} + 1 = <b>{c1+c2+1} ชิ้น</b></span>"

            elif act_sub == "การคิดย้อนกลับ":
                sm = random.randint(100,300); sp = random.randint(20,80); rv = random.randint(50,150); fm = sm-sp+rv; n = random.choice(NAMES)
                q = f"<b>{n}</b>นำเงินไปซื้อ<b>{random.choice(ITEMS)}</b> <b>{sp}</b> บาท จากนั้นแม่ให้ค่าขนมเพิ่ม <b>{rv}</b> บาท ทำให้ตอนนี้มีเงิน <b>{fm}</b> บาท <br>จงหาว่าตอนแรก <b>{n}</b>มีเงินกี่บาท?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด (คิดย้อนกลับ):</b><br>เริ่มจากเหตุการณ์สุดท้าย ย้อนกลับไปหาจุดเริ่มต้น โดยการ 'ทำตรงข้าม' (ได้มาให้นำไปลบ, จ่ายไปให้นำไปบวก)<br>1) ปัจจุบันมีเงิน <b>{fm} บาท</b><br>2) ย้อนเหตุการณ์แม่ให้เงิน {rv} บาท: ต้องนำไปลบออก -> {fm} - {rv} = <b>{fm-rv} บาท</b><br>3) ย้อนเหตุการณ์ซื้อของ {sp} บาท: ต้องนำไปบวกคืน -> {fm-rv} + {sp} = <b>{sm} บาท</b><br>ดังนั้น ตอนแรกมีเงิน <b>{sm} บาท</b></span>"

            elif act_sub == "แผนภาพความชอบ (Venn)":
                tot = random.randint(30,50); both = random.randint(5,12); oa, ob = random.randint(8,15), random.randint(8,15)
                la, lb = oa+both, ob+both; nei = tot-(oa+ob+both); n1, n2 = random.sample(SNACKS, 2)
                q = f"นักเรียน <b>{tot}</b> คน มีคนชอบ<b>{n1}</b> <b>{la}</b> คน, ชอบ<b>{n2}</b> <b>{lb}</b> คน, และชอบทั้งคู่ <b>{both}</b> คน <br>มีนักเรียนกี่คนที่ไม่ชอบขนมทั้งสองชนิดนี้เลย?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>ตัวเลข {la} กับ {lb} มีคนที่ชอบทั้งสองอย่างนับซ้ำอยู่ เราจึงบวกกันตรงๆ ไม่ได้<br>1) หาคนชอบ {n1} อย่างเดียว: {la} - {both} = <b>{oa} คน</b><br>2) หาคนชอบ {n2} อย่างเดียว: {lb} - {both} = <b>{ob} คน</b><br>3) หาคนที่ชอบขนมอย่างน้อย 1 ชนิด: ชอบอย่างแรก + ชอบอย่างที่สอง + ชอบทั้งคู่<br>= {oa} + {ob} + {both} = <b>{oa+ob+both} คน</b><br>4) หาคนที่ไม่ชอบเลย: นำคนทั้งหมด ลบด้วยคนที่ชอบขนม<br>= {tot} - {oa+ob+both} = <b>{nei} คน</b></span>"

            elif act_sub == "ผลบวกจำนวนเรียงกัน (Gauss)":
                n = random.choice([10, 20, 50, 100]); ans = (n*(n+1))//2
                q = f"จงหาผลบวกของ 1 + 2 + 3 + ... + {n}"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด (สูตรเกาส์จับคู่):</b><br>1) จับคู่ตัวหน้าสุดกับหลังสุด: 1 + {n} = <b>{n+1}</b><br>2) คู่ที่สอง: 2 + {n-1} = <b>{n+1}</b> (ทุกคู่บวกกันจะได้ {n+1} เสมอ)<br>3) มีเลขทั้งหมด {n} ตัว นำมาจัดคู่ได้: {n} ÷ 2 = <b>{n//2} คู่</b><br>4) นำผลบวก 1 คู่ ไปคูณกับจำนวนคู่ทั้งหมด: {n+1} × {n//2} = <b>{ans:,}</b></span>"

            elif act_sub == "คิววงกลมมรณะ":
                nh = random.randint(4,12); tot = nh*2; p1 = random.randint(1,nh); p2 = p1+nh; n1, n2 = random.sample(NAMES, 2)
                q = f"เด็กยืนล้อมวงกลมเว้นระยะเท่าๆ กัน นับหมายเลข 1, 2, 3... <br>ถ้า <b>{n1}</b> ยืนหมายเลข <b>{p1}</b> มองไปฝั่งตรงข้ามพบ <b>{n2}</b> ยืนหมายเลข <b>{p2}</b> <br>กลุ่มนี้มีเด็กกี่คน?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) การที่คนสองคนยืนอยู่ 'ฝั่งตรงข้าม' ของวงกลม แปลว่าระยะห่างระหว่างตัวเลขคือ 'ครึ่งวงกลม' พอดี<br>2) หาจำนวนคนในครึ่งวงกลม: นำหมายเลขมาลบกัน {p2} - {p1} = <b>{nh} คน</b><br>3) หาจำนวนคนทั้งหมด (เต็มวงกลม): นำครึ่งวงกลมมาคูณ 2<br>{nh} × 2 = <b>{tot} คน</b></span>"

            elif act_sub == "เส้นทางที่เป็นไปได้":
                p1, p2, p3 = random.randint(2,4), random.randint(2,4), random.randint(1,3)
                q = f"เดินทางจากเมือง A ไป B มีถนน <b>{p1}</b> สาย, จาก B ไป C มี <b>{p2}</b> สาย, และมีทางลัดจาก A ไป C โดยตรงอีก <b>{p3}</b> สาย<br>มีเส้นทางเดินทางจาก A ไป C ทั้งหมดกี่แบบ?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>แบ่งการเดินทางเป็น 2 กรณี<br>1) กรณีผ่านเมือง B: ใช้หลักการคูณ คือนำเส้นทาง A->B คูณกับ B->C<br>= {p1} × {p2} = <b>{p1*p2} แบบ</b><br>2) กรณีใช้ทางลัดตรง: มี <b>{p3} แบบ</b><br>นำทั้งสองกรณีมารวมกัน: {p1*p2} + {p3} = <b>{(p1*p2)+p3} แบบ</b></span>"

            elif act_sub == "พื้นที่แรเงา (เรขาคณิต)":
                w, h = random.randint(10,20), random.randint(10,20); i_s = random.randint(3, min(w, h)-2)
                q = f"กระดาษรูปสี่เหลี่ยมผืนผ้ากว้าง {w} ซม. ยาว {h} ซม. ถูกเจาะรูตรงกลางเป็นรูปสี่เหลี่ยมจัตุรัสที่มีความยาวด้านละ {i_s} ซม. <br>พื้นที่กระดาษส่วนที่เหลือมีขนาดกี่ตารางเซนติเมตร?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>การหาพื้นที่ส่วนที่เหลือ คือการนำ พื้นที่รูปใหญ่ ลบด้วย พื้นที่รูปที่เจาะทิ้ง<br>1) พื้นที่รูปใหญ่ (ผืนผ้า) = กว้าง × ยาว = {w} × {h} = <b>{w*h} ตร.ซม.</b><br>2) พื้นที่รูปที่เจาะทิ้ง (จัตุรัส) = ด้าน × ด้าน = {i_s} × {i_s} = <b>{i_s**2} ตร.ซม.</b><br>3) พื้นที่ส่วนที่เหลือ = {w*h} - {i_s**2} = <b>{(w*h)-(i_s**2)} ตร.ซม.</b></span>"

            elif act_sub == "ความเร็ววิ่งสวนทาง":
                d = random.choice([100, 200, 300]); v1, v2 = random.randint(10,25), random.randint(10,25); t = d/(v1+v2)
                q = f"รถสองคันอยู่ห่างกัน <b>{d} กม.</b> วิ่งเข้าหากัน รถคันแรกวิ่ง <b>{v1} กม./ชม.</b> คันที่สองวิ่ง <b>{v2} กม./ชม.</b> <br>กี่ชั่วโมงรถทั้งสองจึงจะพบกัน?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>เมื่อรถวิ่งเข้าหากัน ระยะทางจะถูกทำให้สั้นลงด้วยความเร็วของรถทั้งสองคันรวมกัน<br>1) หาความเร็วรวม: {v1} + {v2} = <b>{v1+v2} กม./ชม.</b><br>2) หาเวลา: นำระยะทางทั้งหมด หารด้วย ความเร็วรวม<br>เวลา = {d} ÷ {v1+v2} = <b>{t:.1f} ชั่วโมง</b></span>"

            elif act_sub == "งานและเวลา (Work)":
                w1, w2 = 3, 6; ans = (w1*w2)/(w1+w2)
                q = f"ทาสีรั้วบ้าน นาย ก ทำคนเดียวเสร็จใน {w1} วัน, นาย ข ทำคนเดียวเสร็จใน {w2} วัน ถ้าทั้งสองคนช่วยกันทาสีจะเสร็จในกี่วัน?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>ใช้สูตรลัดการทำงานช่วยกัน: (เวลาของ ก × เวลาของ ข) ÷ (เวลาของ ก + เวลาของ ข)<br>= ({w1} × {w2}) ÷ ({w1} + {w2})<br>= 18 ÷ 9 = <b>{ans:.0f} วัน</b></span>"

            elif act_sub == "จัดของใส่กล่อง (Modulo)":
                bc = random.randint(4, 9); nb = random.randint(5, 12); r = random.randint(1, bc-1); tot = (bc*nb)+r
                n = random.choice(NAMES); itm = random.choice(ITEMS)
                q = f"<b>{n}</b>มี<b>{itm}</b>ทั้งหมด <b>{tot}</b> ชิ้น ต้องการจัดใส่กล่อง กล่องละ <b>{bc}</b> ชิ้น <br>จะได้เต็มกล่องกี่ใบ และเหลือเศษกี่ชิ้น?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>ตั้งหารยาว นำของทั้งหมด ({tot}) หารด้วย จำนวนของใน 1 กล่อง ({bc})<br>ท่องสูตรคูณแม่ {bc}: พบว่า {bc} × {nb} = {bc*nb}<br>นำ {tot} ลบด้วย {bc*nb} จะเหลือเศษ <b>{r}</b><br><b>ตอบ: ได้กล่องเต็ม {nb} ใบ และเหลือเศษ {r} ชิ้น</b></span>"

            # ---------------------------------------------
            # โหมดหลักสูตรปกติ (คำอธิบายละเอียดยิบ)
            # ---------------------------------------------
            elif act_sub == "การบวก (แบบตั้งหลัก)":
                a, b = random.randint(10, limit//2), random.randint(10, limit//2); res = a + b
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} + {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '+', is_key=False)
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>ตั้งหลักตัวเลขให้ตรงกัน (หลักหน่วยตรงหลักหน่วย หลักสิบตรงหลักสิบ) แล้วเริ่มบวกจากหลักหน่วย(ขวาสุด) ไปทางซ้ายทีละหลัก หากผลบวกได้ตั้งแต่ 10 ขึ้นไป ให้ทดเลขหลักสิบขึ้นไปไว้บนหัวของหลักถัดไปทางซ้ายมือ</span><br>" + generate_vertical_table_html(a, b, '+', result=res, is_key=True)

            elif act_sub == "การลบ (แบบตั้งหลัก)":
                a = random.randint(1000, limit-1); b = random.randint(100, a-1); res = a - b
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} - {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '-', is_key=False)
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>ตั้งหลักตัวเลขให้ตรงกัน เริ่มลบจากหลักหน่วย(ขวาสุด) ไปทางซ้าย หากตัวเลขด้านบนน้อยกว่าตัวเลขด้านล่าง (ลบไม่พอ) ให้ขอยืมตัวเลขจากหลักถัดไปทางซ้ายมา 1 (ซึ่งจะมีค่าเท่ากับ 10 ในหลักปัจจุบัน) แล้วจึงลบตามปกติ</span><br>" + generate_vertical_table_html(a, b, '-', result=res, is_key=True)

            elif act_sub == "การคูณ (แบบตั้งหลัก)":
                a = random.randint(10, 99) if grade in ["ป.1", "ป.2"] else (random.randint(100, 999) if grade == "ป.3" else random.randint(1000, 9999)) 
                b = random.randint(2, 9); res = a * b
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} × {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '×', is_key=False)
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>นำตัวคูณ ({b}) ไปคูณตัวตั้งด้านบนทีละหลัก เริ่มจากหลักหน่วยทางขวาสุด หากผลคูณได้เกิน 9 ให้ใส่หลักหน่วยไว้ด้านล่าง และนำหลักสิบไป 'ทด' ไว้บนหัวของหลักถัดไปทางซ้ายมือ และเมื่อคูณหลักถัดไปเสร็จอย่าลืมบวกตัวทดด้วย</span><br>" + generate_vertical_table_html(a, b, '×', result=res, is_key=True)

            elif "การหารพื้นฐาน" in act_sub:
                a, b = random.randint(2, 9), random.randint(2, 12); dividend = a * b
                q = f"จงหาผลลัพธ์ของ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {dividend} ÷ {a} = {box_html}</span>"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>การหารคือการหาว่า 'ตัวหาร ({a}) ต้องคูณกับเลขอะไรจึงจะได้เท่ากับตัวตั้ง ({dividend})'<br>ให้นักเรียนท่องสูตรคูณแม่ <b>{a}</b>:<br>{a} × 1 = {a}<br>...<br><b>{a} × {b} = {dividend}</b> (เจอคำตอบแล้ว!)<br>ดังนั้น {dividend} ÷ {a} = <b>{b}</b></span>"

            elif "จำนวนเงิน" in act_sub:
                b100, b50, c10 = random.randint(1,3), random.randint(0,2), random.randint(1,5); tot = b100*100 + b50*50 + c10*10
                q = f"มีธนบัตรใบละ 100 บาท จำนวน <b>{b100}</b> ใบ, ธนบัตรใบละ 50 บาท จำนวน <b>{b50}</b> ใบ, และเหรียญ 10 บาท จำนวน <b>{c10}</b> เหรียญ รวมเป็นเงินทั้งหมดกี่บาท?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>แจกแจงมูลค่าเงินแต่ละชนิดแล้วนำมารวมกัน:<br>1) แบงก์ 100 บาท {b100} ใบ = 100 × {b100} = <b>{b100*100} บาท</b><br>2) แบงก์ 50 บาท {b50} ใบ = 50 × {b50} = <b>{b50*50} บาท</b><br>3) เหรียญ 10 บาท {c10} เหรียญ = 10 × {c10} = <b>{c10*10} บาท</b><br>นำมูลค่าทั้งหมดมาบวกกัน: {b100*100} + {b50*50} + {c10*10} = <b>{tot} บาท</b></span>"

            elif "โจทย์ปัญหาร้อยละ" in act_sub:
                price = random.choice([100, 200, 400, 500, 1000]); percent = random.choice([10, 20, 25, 50])
                q = f"ป้ายติดราคาสินค้าไว้ <b>{price:,} บาท</b> ร้านค้าประกาศลดราคา <b>{percent}%</b> นักเรียนจะได้ลดราคากี่บาท?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>คำว่า 'ลดราคา {percent}%' หมายถึง <b>{percent} ส่วน 100 ของราคาป้าย</b><br>ประโยคสัญลักษณ์: <b>({percent} ÷ 100) × {price:,}</b><br>นำ {price:,} คูณ {percent} แล้วหาร 100 (หรือตัดศูนย์ทิ้ง)<br>จะได้ ({percent} × {price}) ÷ 100 = <b>{int(price*(percent/100)):,} บาท</b></span>"

            elif "การแก้สมการ (+/-)" in act_sub or act_sub == "การแก้สมการ (บวก/ลบ)":
                x, a = random.randint(10, 50), random.randint(5, 20); op = random.choice(["+", "-"])
                if op == "+":
                    q = f"จงแก้สมการหาค่า x : <span style='color: #3498db; margin-left: 15px;'><b>x + {a} = {x+a}</b></span>"
                    sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>เป้าหมายคือทำให้ <b>x</b> เหลืออยู่คนเดียวทางฝั่งซ้าย<br>1) ฝั่งซ้ายมี <b>+{a}</b> เกินมา กำจัดโดยใช้สมบัติการเท่ากัน นำ <b>{a} มาลบออกทั้งสองข้าง</b><br>2) จะได้: x + {a} <b style='color:red;'>- {a}</b> = {x+a} <b style='color:red;'>- {a}</b><br>3) ฝั่งซ้ายจะเหลือแค่ x ส่วนฝั่งขวา {x+a} ลบ {a} ได้ <b>{x}</b><br><b>ตอบ: x = {x}</b></span>"
                else:
                    q = f"จงแก้สมการหาค่า x : <span style='color: #3498db; margin-left: 15px;'><b>x - {a} = {x-a}</b></span>"
                    sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>เป้าหมายคือทำให้ <b>x</b> เหลืออยู่คนเดียวทางฝั่งซ้าย<br>1) ฝั่งซ้ายติด <b>-{a}</b> อยู่ กำจัดโดยใช้สมบัติการเท่ากัน นำ <b>{a} มาบวกเข้าทั้งสองข้าง</b><br>2) จะได้: x - {a} <b style='color:green;'>+ {a}</b> = {x-a} <b style='color:green;'>+ {a}</b><br>3) ฝั่งซ้ายจะเหลือแค่ x ส่วนฝั่งขวา {x-a} บวก {a} ได้ <b>{x}</b><br><b>ตอบ: x = {x}</b></span>"

            elif "การแก้สมการ (คูณ/หาร)" in act_sub:
                a, x = random.randint(2, 12), random.randint(5, 20); op = random.choice(["*", "/"])
                if op == "*":
                    q = f"จงแก้สมการหาค่า x : <span style='color: #3498db; margin-left: 15px;'><b>{a}x = {a*x}</b></span>"
                    sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) {a}x หมายถึง {a} คูณอยู่กับ x เราต้องกำจัด {a} ออกไป<br>2) ใช้สมบัติการเท่ากัน โดยนำ <b>{a} มาหารทั้งสองข้าง</b><br>3) จะได้: ({a}x) <b style='color:red;'>÷ {a}</b> = {a*x} <b style='color:red;'>÷ {a}</b><br>4) ฝั่งซ้าย {a} หาร {a} ได้ 1 เหลือแค่ x ส่วนฝั่งขวา {a*x} หาร {a} ได้ <b>{x}</b><br><b>ตอบ: x = {x}</b></span>"
                else:
                    q = f"จงแก้สมการหาค่า x : <span style='color: #3498db; margin-left: 15px;'><b>x / {a} = {x}</b></span>"
                    sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) x / {a} หมายถึง x ถูกหารด้วย {a} เราต้องกำจัด {a} ออกไป<br>2) ใช้สมบัติการเท่ากัน โดยนำ <b>{a} มาคูณทั้งสองข้าง</b><br>3) จะได้: (x / {a}) <b style='color:green;'>× {a}</b> = {x} <b style='color:green;'>× {a}</b><br>4) ฝั่งซ้ายตัวหารตัดตัวคูณเหลือแค่ x ส่วนฝั่งขวา {x} คูณ {a} ได้ <b>{x*a}</b><br><b>ตอบ: x = {x*a}</b></span>"

            elif "การแก้สมการ (สองขั้นตอน)" in act_sub:
                a, x, b = random.randint(2, 9), random.randint(2, 15), random.randint(1, 20)
                q = f"จงแก้สมการ 2 ขั้นตอน : <span style='color: #3498db; margin-left: 15px;'><b>{a}x + {b} = {a*x+b}</b></span>"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>ขั้นที่ 1: กำจัดตัวบวกลบที่อยู่ไกล x ก่อน<br>นำ <b>{b} มาลบออกทั้งสองข้าง</b> -> {a}x + {b} <b style='color:red;'>- {b}</b> = {a*x+b} <b style='color:red;'>- {b}</b><br>จะได้สมการใหม่คือ: <b>{a}x = {a*x}</b><br><br>ขั้นที่ 2: กำจัดตัวคูณที่ติดอยู่กับ x<br>นำ <b>{a} มาหารทั้งสองข้าง</b> -> ({a}x) <b style='color:red;'>÷ {a}</b> = {a*x} <b style='color:red;'>÷ {a}</b><br><b>ตอบ: x = {x}</b></span>"

            elif "ห.ร.ม." in act_sub:
                a, b = random.randint(12, 48), random.randint(12, 48)
                while a == b: b = random.randint(12, 48) 
                q = f"จงหา ห.ร.ม. (หารร่วมมาก) ของ <b>{a}</b> และ <b>{b}</b>"
                sol = generate_short_division_html(a, b, mode="ห.ร.ม.")

            elif "ค.ร.น." in act_sub:
                a, b = random.randint(4, 24), random.randint(4, 24)
                while a == b: b = random.randint(4, 24) 
                q = f"จงหา ค.ร.น. (คูณร่วมน้อย) ของ <b>{a}</b> และ <b>{b}</b>"
                sol = generate_short_division_html(a, b, mode="ค.ร.น.")

            elif "อ่านและเขียนเศษส่วน" in act_sub:
                den = random.randint(3, 8); num = random.randint(1, den - 1); frac_html = generate_fraction_html(num, den)
                rects = "".join([f'<rect x="{i*40}" y="0" width="40" height="30" fill="{"#3498db" if i < num else "#ffffff"}" stroke="#333" stroke-width="2"/>' for i in range(den)])
                svg_bar = f'<div style="display: inline-block; vertical-align: middle; margin-left: 15px;"><svg width="{den*40 + 4}" height="34"><g transform="translate(2,2)">{rects}</g></svg></div>'
                q = f"จงเขียนเศษส่วนจากรูปภาพที่ระบายสี : {svg_bar}"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) นับช่องสี่เหลี่ยมทั้งหมดได้ <b>{den} ช่อง</b> (คือตัวส่วนด้านล่าง)<br>2) นับช่องที่ระบายสีฟ้าได้ <b>{num} ช่อง</b> (คือตัวเศษด้านบน)<br>เขียนเป็นเศษส่วนได้: </span>{frac_html} <span style='color:#2c3e50;'>(อ่านว่า เศษ {num} ส่วน {den})</span>"

            # (หัวข้อพื้นฐานที่เหลือใช้ Fallback อธิบายแบบรัดกุม)
            else:
                a, b = random.randint(10, 50), random.randint(10, 50)
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a} + {b} = {box_html}</span>"
                sol = f"<span style='color: #2c3e50;'><b>วิธีทำอย่างละเอียด:</b> นำ {a} มาบวกกับ {b} จะได้คำตอบเท่ากับ <b>{a + b}</b></span>"

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
    student_info = """<table style="width: 100%; margin-bottom: 10px; font-size: 18px; border-collapse: collapse;"><tr><td style="width: 1%; white-space: nowrap; padding-right: 5px;"><b>ชื่อ-สกุล</b></td><td style="border-bottom: 2px dotted #999; width: 60%;"></td><td style="width: 1%; white-space: nowrap; padding-left: 20px; padding-right: 5px;"><b>ชั้น</b></td><td style="border-bottom: 2px dotted #999; width: 15%;"></td><td style="width: 1%; white-space: nowrap; padding-left: 20px; padding-right: 5px;"><b>เลขที่</b></td><td style="border-bottom: 2px dotted #999; width: 15%;"></td></tr></table>""" if not is_key else ""
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
            if "(แบบตั้งหลัก)" in sub_t or "หารยาว" in sub_t: html += f'{item["solution"]}'
            else: html += f'{item["question"]}<div class="sol-text">{item["solution"]}</div>'
        else:
            html += f'{item["question"]}<div class="workspace">พื้นที่สำหรับแสดงวิธีทำอย่างละเอียด...</div><div class="ans-line">ตอบ: </div>'
        html += '</div>'
    if brand_name: html += f'<div class="page-footer">&copy; 2026 {brand_name} | สงวนลิขสิทธิ์</div>'
    return html + "</body></html>"

def generate_cover_html(grade, main_t, sub_t, num_q, theme_colors, brand_name):
    return f"""<!DOCTYPE html><html lang="th"><head><meta charset="utf-8">
    <style>.cover-inner {{ width: 100%; height: 100%; padding: 40px; box-sizing: border-box; text-align: center; position: relative; border: 15px solid {theme_colors['border']}; background: white; }} .title-box {{ margin-top: 80px; }} .title {{ font-size: 65px; color: #2c3e50; font-weight: bold; margin: 0; line-height: 1.2; }} .grade-badge {{ font-size: 45px; background-color: {theme_colors['badge']}; color: white; padding: 15px 50px; border-radius: 50px; display: inline-block; font-weight: bold; margin-top: 30px; }} .topic {{ font-size: 42px; color: #34495e; margin-top: 70px; font-weight: bold; }} .sub-topic {{ font-size: 32px; color: #7f8c8d; margin-top: 10px; }} .icons {{ font-size: 110px; margin: 60px 0; }} .details-badge {{ background-color: #2ecc71; color: white; display: inline-block; padding: 15px 40px; border-radius: 15px; font-size: 32px; font-weight: bold; }} .footer {{ position: absolute; bottom: 40px; left: 0; width: 100%; text-align: center; font-size: 22px; color: #7f8c8d; }}</style></head><body>
    <div class="cover-inner"><div class="title-box"><h1 class="title">แบบฝึกหัดคณิตศาสตร์</h1><div class="grade-badge">ระดับชั้น {grade}</div></div><div class="topic">เรื่อง: {sub_t}</div><div class="sub-topic">(หมวดหมู่: {main_t})</div><div class="icons">🧮 📏 📐 ✏️</div><div class="details-badge">รวมทั้งหมด {num_q} ข้อ (พร้อมเฉลยละเอียด)</div><div class="footer"><b>ออกแบบและจัดทำโดย:</b> {brand_name}</div></div></body></html>"""

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
    with st.spinner("กำลังประมวลผลคำอธิบายและวาดภาพเฉลยแบบ Step-by-Step..."):
        grade_arg = "ป.1" if "ป.1" in selected_grade else ("ป.3" if "ป.3" in selected_grade else "ป.5")
        if worksheet_mode == "📚 หลักสูตรปกติ (ป.1 - ป.6)": grade_arg = selected_grade
            
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
