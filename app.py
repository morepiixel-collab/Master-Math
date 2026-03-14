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
<p>ระบบสร้างสื่อการสอน ป.1-ป.6 + ข้อสอบแข่งขัน TMC ทุกระดับชั้น พร้อมเฉลยละเอียดแบบ Step-by-Step 100%</p></div>""", unsafe_allow_html=True)

# ==========================================
# 1. ฐานข้อมูลหลักสูตรและคลังคำศัพท์
# ==========================================
NAMES = ["อคิณ", "นาวิน", "ภูผา", "สายฟ้า", "เจ้านาย", "ข้าวหอม", "ใบบัว", "มะลิ", "น้ำใส", "ญาญ่า", "ปลื้ม", "พายุ", "ไออุ่น", "กะทิ", "เวลา", "ของขวัญ", "มังกร", "ฉลาม", "ปลาวาฬ", "มาคิน"]
LOCS = ["โรงเรียน", "สวนสัตว์", "สวนสนุก", "ห้างสรรพสินค้า", "ห้องสมุด", "สวนสาธารณะ", "ร้านของเล่น", "ร้านเบเกอรี่", "ค่ายลูกเสือ", "พิพิธภัณฑ์"]
ITEMS = ["ลูกแก้ว", "สติกเกอร์", "การ์ดพลัง", "โมเดลรถ", "ตุ๊กตาหมี", "สมุดระบายสี", "ดินสอสี", "ลูกโป่ง", "ยางลบ", "ตัวต่อเลโก้", "หนังสือการ์ตูน", "ลูกบอล"]
SNACKS = ["ช็อกโกแลต", "คุกกี้", "โดนัท", "เยลลี่", "ขนมปัง", "ไอศกรีม", "น้ำผลไม้", "นมเย็น", "ลูกอม", "เค้ก"]
ANIMALS = ["แมงมุม", "มดแดง", "กบ", "จิ้งจก", "ตั๊กแตน", "เต่า"]

tmc_lower = ["ปริศนาตัวเลขซ่อนแอบ", "สัตว์ปีนบ่อ", "ตรรกะตาชั่งสมดุล", "ปัญหาผลรวม-ผลต่าง", "ตรรกะการจับมือ (ทักทาย)", "โปรโมชั่นแลกของ", "หยิบของในที่มืด", "คิววงกลมมรณะ"]
tmc_mid = ["ผลบวกจำนวนเรียงกัน (Gauss)", "พื้นที่แรเงา (เรขาคณิต)", "การตัดเชือกพับทบ", "แถวคอยแบบซ้อนทับ", "อายุข้ามเวลาขั้นสูง", "แผนภาพความชอบ (Venn)", "การนับหน้าหนังสือ", "วันที่และปฏิทิน"]
tmc_upper = ["ความเร็ววิ่งสวนทาง", "งานและเวลา (Work)", "ระฆังและไฟกะพริบ (ค.ร.น.)", "อัตราส่วนอายุ", "เศษส่วนของที่เหลือ", "เส้นทางที่เป็นไปได้", "จัดของใส่กล่อง (Modulo)", "นาฬิกาเดินเพี้ยน", "คะแนนยิงเป้า"]
comp_topics = tmc_lower + tmc_mid + tmc_upper

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
        "เศษส่วน": ["การบวกเศษส่วน", "การลบเศษส่วน", "การคูณเศษส่วน", "การหารเศษส่วน"], "ทศนิยม": ["การบวกและการลบทศนิยม", "การคูณทศนิยม"], "ร้อยละและเปอร์เซ็นต์": ["การเขียนเศษส่วนในรูปร้อยละ"], "สมการ": ["การแก้สมการ (คูณ/หาร)"], "🌟 โจทย์แข่งขัน (แนว TMC)": tmc_upper
    },
    "ป.6": {
        "ตัวประกอบของจำนวนนับ": ["การหา ห.ร.ม.", "การหา ค.ร.น."], "อัตราส่วนและร้อยละ": ["การหาอัตราส่วนที่เท่ากัน", "โจทย์ปัญหาอัตราส่วน", "โจทย์ปัญหาร้อยละ"], "สมการ": ["การแก้สมการ (สองขั้นตอน)"], "🌟 โจทย์แข่งขัน (แนว TMC)": tmc_upper
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
            for i in range(num_len-1, -1, -1):
                da, db = int(str_a[i]) if str_a[i].strip() else 0, int(str_b[i]) if str_b[i].strip() else 0
                s = da+db+carry; carry = s//10
                if carry > 0 and i > 0: top_marks[i-1] = str(carry)
        elif op == '-':
            a_dig, b_dig = [int(c) if c.strip() else 0 for c in str_a], [int(c) if c.strip() else 0 for c in str_b]
            for i in range(num_len-1, -1, -1):
                if a_dig[i] < b_dig[i]:
                    for j in range(i-1, -1, -1):
                        if a_dig[j] > 0 and str_a[j].strip() != "":
                            strike[j] = True; a_dig[j] -= 1; top_marks[j] = str(a_dig[j])
                            for k in range(j+1, i): strike[k] = True; a_dig[k] = 9; top_marks[k] = "9"
                            strike[i] = True; a_dig[i] += 10; top_marks[i] = str(a_dig[i]); break
        elif op == '×':
            carry = 0; a_dig = [int(c) if c.strip() else 0 for c in str_a]
            for i in range(num_len-1, -1, -1):
                if str_a[i].strip() == "": 
                    if carry > 0: top_marks[i] = str(carry); carry = 0
                    continue
                prod = a_dig[i] * b + carry; carry = prod // 10
                if carry > 0 and i > 0: top_marks[i-1] = str(carry)
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
    steps, cur_val_str, ans_str, started = [], "", "", False
    for i, digit in enumerate(div_str):
        cur_val_str += digit; cur_val = int(cur_val_str)
        q = cur_val // divisor; mul_res = q * divisor; rem = cur_val - mul_res
        if not started and q == 0 and i < len(div_str)-1: cur_val_str = str(rem) if rem != 0 else ""; continue
        started = True; ans_str += str(q)
        c_dig, m_dig = [int(c) for c in str(cur_val)], [int(c) for c in str(mul_res).zfill(len(str(cur_val)))]
        top_m, strik = [""]*len(c_dig), [False]*len(c_dig)
        for idx_b in range(len(c_dig)-1, -1, -1):
            if c_dig[idx_b] < m_dig[idx_b]:
                for j in range(idx_b-1, -1, -1):
                    if c_dig[j] > 0:
                        strik[j] = True; c_dig[j] -= 1; top_m[j] = str(c_dig[j])
                        for k in range(j+1, idx_b): strik[k] = True; c_dig[k] = 9; top_m[k] = "9"
                        strik[idx_b] = True; c_dig[idx_b] += 10; top_m[idx_b] = str(c_dig[idx_b]); break
        steps.append({'mul_res':mul_res, 'rem':rem, 'col_index':i, 'top_m':top_m, 'strik':strik}); cur_val_str = str(rem) if rem != 0 else ""
    ans_tds = "".join([f'<td style="width:35px; text-align:center; color:red; font-weight:bold; font-size:38px;">{c.strip()}</td>' for c in ans_str.rjust(div_len, " ")]) + '<td style="width:35px;"></td>'
    div_tds, s0 = "", steps[0] if steps else None; s0_st = s0['col_index'] + 1 - len(s0['top_m']) if s0 else 0
    for i, c in enumerate(div_str):
        td_c = c
        if s0 and s0_st <= i <= s0['col_index']:
            m, stk = s0['top_m'][i-s0_st], s0['strik'][i-s0_st]
            if stk: td_c = f'<div style="position:relative;"><span style="position:absolute; top:-25px; left:50%; transform:translateX(-50%); font-size:20px; color:red; font-weight:bold;">{m}</span><span style="text-decoration:line-through; text-decoration-color:red;">{c}</span></div>'
            elif m: td_c = f'<div style="position:relative;"><span style="position:absolute; top:-25px; left:50%; transform:translateX(-50%); font-size:20px; color:red; font-weight:bold;">{m}</span><span>{c}</span></div>'
        div_tds += f'<td style="width:35px; height:50px; vertical-align:bottom; text-align:center; border-top:3px solid #000; {"border-left:3px solid #000;" if i==0 else ""} font-size:38px;">{td_c}</td>'
    div_tds += '<td style="width:35px;"></td>'
    html = f"{eq_html}<div style=\"display:block; text-align:center; margin-top:10px;\"><div style=\"display:inline-block; font-family:'Sarabun'; line-height:1.2; margin:10px 20px;\"><table style=\"border-collapse:collapse;\"><tr><td style=\"border:none;\"></td>{ans_tds}</tr><tr><td style=\"border:none; text-align:right; padding-right:12px; vertical-align:bottom; font-size:38px;\">{divisor}</td>{div_tds}</tr>"
    for idx, s in enumerate(steps):
        m_str, p_len = str(s['mul_res']), s['col_index'] + 1 - len(str(s['mul_res']))
        m_tds = "".join([f'<td style="width:35px; height:50px; vertical-align:bottom; text-align:center; font-size:38px; {"border-bottom:2px solid #000;" if i <= s["col_index"] else ""}">{m_str[i-p_len]}</td>' if p_len <= i <= s['col_index'] else ('<td style="width:35px; text-align:center; font-size:38px; color:#333; position:relative; top:-24px;">-</td>' if i == s['col_index']+1 else '<td style="width:35px;"></td>') for i in range(div_len+1)])
        html += f"<tr><td style='border:none;'></td>{m_tds}</tr>"
        is_l = (idx == len(steps)-1); ns = steps[idx+1] if not is_l else None; ns_st = ns['col_index'] + 1 - len(ns['top_m']) if ns else 0
        r_str = str(s['rem']); d_str = (r_str if r_str != "0" or is_l else "") + (div_str[s['col_index']+1] if not is_l else "")
        if not d_str: d_str = div_str[s['col_index']+1] if not is_l else ""
        p_rem = s['col_index'] + 1 - len(d_str) + (1 if not is_l else 0); r_tds = ""
        for i in range(div_len+1):
            if p_rem <= i <= s['col_index'] + (1 if not is_l else 0):
                tc = d_str[i - p_rem]
                if ns and ns_st <= i <= ns['col_index']:
                    m, stk = ns['top_m'][i-ns_st], ns['strik'][i-ns_st]
                    if stk: tc = f'<div style="position:relative;"><span style="position:absolute; top:-25px; left:50%; transform:translateX(-50%); font-size:20px; color:red; font-weight:bold;">{m}</span><span style="text-decoration:line-through; text-decoration-color:red;">{tc}</span></div>'
                    elif m: tc = f'<div style="position:relative;"><span style="position:absolute; top:-25px; left:50%; transform:translateX(-50%); font-size:20px; color:red; font-weight:bold;">{m}</span><span>{tc}</span></div>'
                r_tds += f'<td style="width:35px; height:50px; vertical-align:bottom; text-align:center; font-size:38px; {"border-bottom:6px double #000;" if is_l else ""}">{tc}</td>'
            else: r_tds += '<td style="width:35px;"></td>'
        html += f"<tr><td style='border:none;'></td>{r_tds}</tr>"
    return html + "</table></div></div>"

def generate_fraction_html(num, den, color="#000"): return f"""<div style="display:inline-flex; flex-direction:column; align-items:center; vertical-align:middle; margin:0 5px; font-family:'Sarabun';"><span style="font-size:20px; font-weight:bold; border-bottom:2px solid {color}; padding:0 4px; line-height:1.1; color:{color};">{num}</span><span style="font-size:20px; font-weight:bold; padding:0 4px; line-height:1.1; color:{color};">{den}</span></div>"""
def generate_mixed_number_html(w, num, den): return f"""<div style="display:inline-flex; align-items:center; vertical-align:middle; margin:0 5px; font-family:'Sarabun';"><span style="font-size:24px; font-weight:bold; margin-right:4px; color:red;">{w}</span><div style="display:inline-flex; flex-direction:column; align-items:center;"><span style="font-size:20px; font-weight:bold; border-bottom:2px solid red; padding:0 4px; line-height:1.1; color:red;">{num}</span><span style="font-size:20px; font-weight:bold; padding:0 4px; line-height:1.1; color:red;">{den}</span></div></div>"""

def generate_short_division_html(a, b, mode="ห.ร.ม."):
    factors = []; ca, cb = a, b; steps_html = ""
    while True:
        found = False
        for i in range(2, min(ca, cb) + 1):
            if ca % i == 0 and cb % i == 0:
                steps_html += f"<tr><td style='text-align:right; padding-right:10px; font-weight:bold; color:red;'>{i}</td><td style='border-left:2px solid #000; border-bottom:2px solid #000; padding:5px 15px; text-align:center;'>{ca}</td><td style='border-bottom:2px solid #000; padding:5px 15px; text-align:center;'>{cb}</td></tr>"
                factors.append(i); ca //= i; cb //= i; found = True; break
        if not found: break
    steps_html += f"<tr><td></td><td style='padding:5px 15px; text-align:center;'>{ca}</td><td style='padding:5px 15px; text-align:center;'>{cb}</td></tr>"
    table = f"<table style='margin:10px 0; font-size:20px; border-collapse:collapse; color:#333;'>{steps_html}</table>"
    ans = math.prod(factors) if mode == "ห.ร.ม." else math.prod(factors) * ca * cb
    calc_str = " × ".join(map(str, factors)) if mode == "ห.ร.ม." else " × ".join(map(str, factors + [ca, cb]))
    return f"<span style='color:#2c3e50;'><b>วิธีทำ (ตั้งหารสั้น):</b> หาตัวเลขที่หารทั้ง {a} และ {b} ลงตัวมาหารไปเรื่อยๆ จนกว่าจะหารไม่ได้แล้ว</span>{table}<span style='color:#2c3e50;'><b>{mode}</b> = {calc_str} = <b>{ans}</b></span>"

def get_prefix(grade): return "<b style='color:#2c3e50; margin-right:5px;'>ประโยคสัญลักษณ์:</b>" if grade in ["ป.1","ป.2","ป.3"] else ""

# ==========================================
# 🧠 CORE LOGIC & DETAILED EXPLANATIONS
# ==========================================
def generate_questions_logic(grade, main_t, sub_t, num_q):
    questions, seen = [], set()
    limit = {"ป.1":100, "ป.2":1000, "ป.3":100000, "ป.4":1000000, "ป.5":9000000, "ป.6":9000000}.get(grade, 100)

    for _ in range(num_q):
        q, sol, attempts = "", "", 0
        while attempts < 300:
            act_sub = random.choice(curriculum_db[grade][random.choice([m for m in curriculum_db[grade] if m != "🌟 โหมดพิเศษ (สุ่มทุกเรื่อง)"])]) if sub_t == "แบบทดสอบรวมปลายภาค" else (random.choice(comp_topics) if sub_t == "🌟 สุ่มรวมทุกแนว" else sub_t)
            prefix = get_prefix(grade)

            # ---------------------------------------------
            # โหมดข้อสอบแข่งขัน (พร้อมเฉลยละเอียดแบบสุดยอด)
            # ---------------------------------------------
            if act_sub == "ปริศนาตัวเลขซ่อนแอบ":
                a = random.randint(1, 4); b = random.randint(a+2, 9); diff = b-a; k = diff*9; s_val = a+b
                q = f"กำหนด A และ B เป็นเลขโดดที่ต่างกัน โดย <b>AB + {k} = BA</b> และ <b>A + B = {s_val}</b> <br>จำนวนสองหลัก <b>AB</b> คือจำนวนใด?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) จากประโยค AB + {k} = BA ถ้านำ AB ไปลบออกทั้งสองข้าง จะได้ BA - AB = {k}<br>2) ความลับของตัวเลขสลับหลักคือ: ผลต่างจะเท่ากับ (B - A) × 9 เสมอ!<br>ดังนั้น B - A = {k} ÷ 9 = <b>{diff}</b><br>3) เรามี 2 ข้อมูล: ผลบวก A + B = {s_val} และผลต่าง B - A = {diff}<br>4) หาเลข 2 ตัวที่บวกได้ {s_val} ลบได้ {diff}: นำ ({s_val} + {diff}) ÷ 2 = <b>{b}</b> (คือค่า B)<br>และนำ {s_val} - {b} = <b>{a}</b> (คือค่า A)<br><b>ตอบ: จำนวน AB คือ {a}{b}</b></span>"

            elif act_sub == "การนับหน้าหนังสือ":
                p = random.randint(40, 150); ans = 9 + 180 + ((p-99)*3) if p>99 else 9 + ((p-9)*2)
                q = f"สมุดภาพ<b>{random.choice(ITEMS)}</b> มีความหนา <b>{p}</b> หน้า ต้องพิมพ์ตัวเลขเพื่อบอกเลขหน้า 1 ถึง {p} จะต้องใช้ตัวเลขโดดทั้งหมดกี่ตัว?"
                if p > 99:
                    sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>แบ่งการนับทีละกลุ่มหลัก:<br>1) หน้า 1-9 (เลข 1 หลัก) มี 9 หน้า ใช้หน้าละ 1 ตัว = 9 × 1 = <b>9 ตัว</b><br>2) หน้า 10-99 (เลข 2 หลัก) มี 90 หน้า ใช้หน้าละ 2 ตัว = 90 × 2 = <b>180 ตัว</b><br>3) หน้า 100-{p} (เลข 3 หลัก) มี {p}-99 = {p-99} หน้า ใช้หน้าละ 3 ตัว = {p-99} × 3 = <b>{(p-99)*3} ตัว</b><br>นำทุกกลุ่มมารวมกัน: 9 + 180 + {(p-99)*3} = <b>{ans} ตัว</b><br><b>ตอบ: ใช้ตัวเลขทั้งหมด {ans} ตัว</b></span>"
                else:
                    sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>แบ่งการนับทีละกลุ่มหลัก:<br>1) หน้า 1-9 (เลข 1 หลัก) มี 9 หน้า ใช้หน้าละ 1 ตัว = 9 × 1 = <b>9 ตัว</b><br>2) หน้า 10-{p} (เลข 2 หลัก) มี {p}-9 = {p-9} หน้า ใช้หน้าละ 2 ตัว = {p-9} × 2 = <b>{(p-9)*2} ตัว</b><br>นำทุกกลุ่มมารวมกัน: 9 + {(p-9)*2} = <b>{ans} ตัว</b><br><b>ตอบ: ใช้ตัวเลขทั้งหมด {ans} ตัว</b></span>"

            elif act_sub == "การปักเสาและปลูกต้นไม้":
                d = random.choice([2, 4, 5, 10, 15]); t = random.randint(12, 35); L = (t-1)*d
                q = f"เทศบาลปลูกต้นไม้ริมถนนทางเข้า<b>{random.choice(LOCS)}</b> ห่างกันต้นละ <b>{d}</b> เมตร โดยปลูกที่หัวและท้ายถนนพอดี ถ้านับได้ <b>{t}</b> ต้น ถนนเส้นนี้ยาวกี่เมตร?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) การปลูกต้นไม้ปิดหัวท้าย จะทำให้จำนวน 'ช่องว่าง' น้อยกว่าจำนวนต้นไม้อยู่ 1 เสมอ<br>2) มีต้นไม้ {t} ต้น จะเกิดช่องว่างระหว่างต้นไม้ = {t} - 1 = <b>{t-1} ช่อง</b><br>3) แต่ละช่องมีความยาว {d} เมตร<br>4) นำจำนวนช่องไปคูณความยาวแต่ละช่อง: {t-1} ช่อง × {d} เมตร = <b>{L} เมตร</b><br><b>ตอบ: ถนนยาว {L} เมตร</b></span>"

            elif act_sub == "สัตว์ปีนบ่อ":
                u = random.randint(3,7); d = random.randint(1,u-1); h = random.randint(15,30); net = u-d; days = math.ceil((h-u)/net) + 1
                q = f"<b>{random.choice(ANIMALS)}</b>ตกบ่อลึก <b>{h}</b> เมตร กลางวันปีนขึ้นได้ <b>{u}</b> เมตร แต่กลางคืนลื่นลง <b>{d}</b> เมตร ต้องใช้เวลาอย่างน้อยกี่วันจึงจะปีนพ้นปากบ่อ?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) ใน 1 วัน (ปีนแล้วลื่น) จะปีนได้สุทธิ: {u} - {d} = <b>{net} เมตร</b><br>2) <i>จุดหลอก:</i> ในวันสุดท้ายเมื่อปีนพ้นขอบบ่อแล้ว จะไม่ต้องลื่นตกลงมาอีก! เราจึงต้องแยกคิดวันสุดท้ายออกมาก่อน<br>3) หาระยะทางก่อนถึงวันสุดท้าย: ความลึก {h} - ปีนวันสุดท้าย {u} = <b>{h-u} เมตร</b><br>4) หาเวลาที่ใช้ปีนระยะทางช่วงแรก: {h-u} เมตร ÷ {net} เมตร/วัน = <b>{math.ceil((h-u)/net)} วัน</b><br>5) นำไปบวกกับวันสุดท้ายอีก 1 วัน: {math.ceil((h-u)/net)} + 1 = <b>{days} วัน</b><br><b>ตอบ: ใช้เวลาทั้งหมด {days} วัน</b></span>"

            elif act_sub == "ตรรกะตาชั่งสมดุล":
                i1, i2, i3 = random.choice([("รถคันใหญ่", "รถคันเล็ก", "ลูกบอล"), ("แตงโม", "สับปะรด", "มะละกอ")])
                m1, m2 = random.randint(2,5), random.randint(2,5)
                q = f"ตาชั่งสมดุล:<br>- <b>{i1} 1 ชิ้น</b> หนักเท่ากับ <b>{i2} {m1} ชิ้น</b><br>- <b>{i2} 1 ชิ้น</b> หนักเท่ากับ <b>{i3} {m2} ชิ้น</b><br>อยากทราบว่า <b>{i1} 2 ชิ้น</b> จะหนักเท่ากับ <b>{i3}</b> รวมกี่ชิ้น?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>เราต้องทำการ 'แปลงหน่วย' ของที่ใหญ่สุดให้เป็นของที่เล็กสุดครับ<br>1) จากข้อมูลที่สอง: เรารู้ว่า {i2} 1 ชิ้น เปลี่ยนเป็น {i3} ได้ <b>{m2} ชิ้น</b><br>2) จากข้อมูลแรก: {i1} 1 ชิ้น มีน้ำหนักเท่ากับ {i2} ถึง {m1} ชิ้น<br>นำความรู้มาแทนค่า: ให้นำ {m1} ไปคูณ {m2} จะได้ว่า {i1} 1 ชิ้น = {m1} × {m2} = <b>{m1*m2} ชิ้น ({i3})</b><br>3) โจทย์ไม่ได้ถามแค่ 1 ชิ้น แต่ถามหา {i1} <b>2 ชิ้น</b><br>นำน้ำหนักไปคูณสอง: {m1*m2} × 2 = <b>{m1*m2*2} ชิ้น</b><br><b>ตอบ: {m1*m2*2} ชิ้น</b></span>"

            elif act_sub == "ปัญหาผลรวม-ผลต่าง":
                diff = random.randint(5,20); small = random.randint(10,30); large = small+diff; tot = large+small; n1, n2 = random.sample(NAMES, 2); itm = random.choice(ITEMS)
                q = f"<b>{n1}</b> และ <b>{n2}</b> มี<b>{itm}</b>รวม <b>{tot}</b> ชิ้น หาก <b>{n1}</b> มีมากกว่า <b>{n2}</b> อยู่ <b>{diff}</b> ชิ้น จงหาว่า <b>{n1}</b> มี<b>{itm}</b>กี่ชิ้น?"
                svg = f"<div style='text-align:center; margin:10px 0;'><svg width='250' height='70'><rect x='50' y='10' width='80' height='15' fill='#3498db'/><rect x='50' y='35' width='80' height='15' fill='#e74c3c'/><rect x='130' y='35' width='40' height='15' fill='#f1c40f' stroke-dasharray='2'/><text x='150' y='47' font-size='10' font-weight='bold' text-anchor='middle'>+{diff}</text><text x='40' y='22' font-size='12' text-anchor='end'>{n2}</text><text x='40' y='47' font-size='12' text-anchor='end'>{n1}</text></svg></div>"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b></span>{svg}<span style='color:#2c3e50;'>1) ดูจากรูป ถ้าเราหยิบส่วนที่ {n1} มี 'เกินมา' ({diff} ชิ้น) ทิ้งไปก่อน ของที่เหลือจะแบ่งให้ 2 คนได้เท่ากันพอดี<br>ของที่เหลือ: {tot} - {diff} = <b>{tot-diff} ชิ้น</b><br>2) นำของที่เหลือมาแบ่งครึ่ง (ซึ่งจะได้เท่ากับจำนวนของ {n2}): {tot-diff} ÷ 2 = <b>{small} ชิ้น</b><br>3) โจทย์ถามหาจำนวนของ {n1} ให้นำจำนวนของ {n2} ไปบวกส่วนที่เกินกลับเข้ามา: {small} + {diff} = <b>{large} ชิ้น</b><br><b>ตอบ: {n1} มี {large} ชิ้น</b></span>"

            elif act_sub == "การคิดย้อนกลับ":
                sm = random.randint(100,300); sp = random.randint(20,80); rv = random.randint(50,150); fm = sm-sp+rv; n = random.choice(NAMES)
                q = f"<b>{n}</b>นำเงินไปซื้อ<b>{random.choice(ITEMS)}</b> <b>{sp}</b> บาท จากนั้นแม่ให้เพิ่ม <b>{rv}</b> บาท ทำให้มีเงิน <b>{fm}</b> บาท <br>จงหาว่าตอนแรก <b>{n}</b>มีเงินกี่บาท?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>ใช้วิธีคิดย้อนจากเหตุการณ์สุดท้ายไปหาจุดเริ่มต้น โดยการ 'ทำตรงข้าม' (ได้เงินมาให้นำไปลบ, จ่ายเงินไปให้นำไปบวก)<br>1) ปัจจุบันมีเงิน: <b>{fm} บาท</b><br>2) เหตุการณ์ก่อนหน้า (แม่ให้มา {rv}): ต้องนำไปลบออก -> {fm} - {rv} = <b>{fm-rv} บาท</b><br>3) เหตุการณ์แรกสุด (ซื้อของไป {sp}): ต้องนำไปบวกคืน -> {fm-rv} + {sp} = <b>{sm} บาท</b><br><b>ตอบ: ตอนแรกมีเงิน {sm} บาท</b></span>"

            elif act_sub == "คิววงกลมมรณะ":
                nh = random.randint(4,12); tot = nh*2; p1 = random.randint(1,nh); p2 = p1+nh; n1, n2 = random.sample(NAMES, 2)
                q = f"เด็กยืนเรียงเป็นวงกลมโดยเว้นระยะห่างเท่าๆ กัน และนับหมายเลข 1, 2, 3... <br>ถ้า <b>{n1}</b> ยืนหมายเลข <b>{p1}</b> และมองตรงไปฝั่งตรงข้ามพอดีพบ <b>{n2}</b> ยืนหมายเลข <b>{p2}</b> <br>เด็กกลุ่มนี้มีกี่คน?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>1) การที่คนสองคนยืนอยู่ 'ฝั่งตรงข้าม' ของวงกลม หมายความว่าระยะห่างระหว่างตัวเลขของสองคนนี้ จะเท่ากับ 'ครึ่งวงกลม' พอดี<br>2) หาจำนวนคนในครึ่งวงกลม: นำหมายเลขมาลบกัน {p2} - {p1} = <b>{nh} คน</b><br>3) หาจำนวนคนทั้งวงกลม: นำครึ่งวงกลมมาคูณ 2<br>{nh} × 2 = <b>{tot} คน</b><br><b>ตอบ: มีเด็กทั้งหมด {tot} คน</b></span>"

            elif act_sub == "โปรโมชั่นแลกของ":
                ex = random.choice([3,4,5]); start = ex*random.randint(3,6); tot, emp = start, start
                while emp >= ex: nb = emp//ex; emp = nb+(emp%ex); tot += nb
                q = f"โปรโมชั่น: นำซอง<b>{random.choice(SNACKS)}</b>เปล่า <b>{ex}</b> ซอง แลกฟรี 1 ชิ้น <br>ถ้าซื้อตอนแรก <b>{start}</b> ชิ้น จะได้กินรวมทั้งหมดกี่ชิ้น (รวมของที่นำไปแลกมาใหม่)?"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>เราจะนำซองเปล่าไปแลก แล้วนำเศษซองเปล่าที่เหลือมารวมกับซองใหม่เพื่อแลกต่อเป็นทอดๆ<br>1) ซื้อครั้งแรกได้กิน {start} ชิ้น (มีซองเปล่า {start} ซอง)<br>2) นำซองเปล่า {start} ซอง ไปแลก: {start} ÷ {ex} = แลกได้ <b>{start//ex} ชิ้น</b> (เหลือเศษซอง {start%ex} ซอง)<br><i>(ทำแบบนี้ไปเรื่อยๆ นำจำนวนที่กินได้มาบวกกัน)</i><br>เมื่อบวกจำนวนชิ้นที่กินได้ทั้งหมด จะได้ <b>{tot} ชิ้น</b><br><b>ตอบ: ได้กินทั้งหมด {tot} ชิ้น</b></span>"

            elif act_sub == "ผลบวกจำนวนเรียงกัน (Gauss)":
                n = random.choice([10, 20, 50, 100]); ans = (n*(n+1))//2
                q = f"จงหาผลบวกของ 1 + 2 + 3 + ... + {n}"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>ใช้หลักการจับคู่หัว-ท้ายของเกาส์ (Gauss)<br>1) นำตัวแรกบวกตัวสุดท้าย: 1 + {n} = <b>{n+1}</b><br>2) นำตัวที่สองบวกตัวรองสุดท้าย: 2 + {n-1} = <b>{n+1}</b><br>จะเห็นว่าทุกคู่บวกกันได้ {n+1} เสมอ<br>3) มีเลขทั้งหมด {n} ตัว จัดเป็นคู่ได้ {n} ÷ 2 = <b>{n//2} คู่</b><br>4) นำผลบวกแต่ละคู่คูณจำนวนคู่: {n+1} × {n//2} = <b>{ans:,}</b><br><b>ตอบ: {ans:,}</b></span>"

            # ---------------------------------------------
            # โหมดหลักสูตรปกติ (เขียนอธิบายแบบ Step-by-Step)
            # ---------------------------------------------
            elif actual_sub_t == "การคูณ (แบบตั้งหลัก)":
                a = random.randint(10, 99) if grade in ["ป.1", "ป.2"] else (random.randint(100, 999) if grade == "ป.3" else random.randint(1000, 9999)) 
                b = random.randint(2, 9); res = a * b
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} × {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '×', is_key=False)
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำ:</b> นำ {b} ไปคูณตัวตั้งทีละหลักเริ่มจากหลักหน่วยทางขวามือสุด ถ้าผลคูณได้ตั้งแต่ 10 ขึ้นไป ให้ใส่เลขตัวหลัง (หลักหน่วย) ไว้ด้านล่าง และนำเลขตัวหน้าไปทดในหลักถัดไปทางซ้าย</span><br>" + generate_vertical_table_html(a, b, '×', result=res, is_key=True)

            elif actual_sub_t == "การบวก (แบบตั้งหลัก)":
                a, b = random.randint(10, limit//2), random.randint(10, limit//2)
                res = a + b
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} + {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '+', is_key=False)
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำ:</b> ตั้งหลักให้ตรงกัน แล้วเริ่มบวกจากหลักหน่วย (ขวาสุด) ถ้าผลบวกเกิน 9 ให้ทดเลขหลักสิบขึ้นไปไว้บนหลักถัดไปทางซ้ายมือ</span><br>" + generate_vertical_table_html(a, b, '+', result=res, is_key=True)

            elif actual_sub_t == "การลบ (แบบตั้งหลัก)":
                a = random.randint(1000, limit-1); b = random.randint(100, a-1)
                res = a - b
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {a:,} - {b:,} = {box_html}</span>" + generate_vertical_table_html(a, b, '-', is_key=False)
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำ:</b> ตั้งหลักให้ตรงกัน ลบทีละหลักจากขวาสุด ถ้าเลขด้านบนน้อยกว่าเลขด้านล่าง ไม่สามารถลบได้ ให้ขอยืมเลขในหลักถัดไปทางซ้ายมา 1 (มีค่าเป็น 10 ของหลักปัจจุบัน)</span><br>" + generate_vertical_table_html(a, b, '-', result=res, is_key=True)

            elif "การหารพื้นฐาน" in actual_sub_t:
                a, b = random.randint(2, 9), random.randint(2, 12); dividend = a * b
                q = f"จงหาผลลัพธ์ <span style='display:inline-flex; align-items:center; font-weight: bold; color: #2c3e50; margin-left: 5px;'>{prefix} {dividend} ÷ {a} = {box_html}</span>"
                sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>การหารคือการหาว่า ตัวหาร ({a}) ต้องคูณกับตัวเลขใดจึงจะได้เท่ากับตัวตั้ง ({dividend})<br>ให้ท่องสูตรคูณแม่ {a} :<br>{a} × 1 = {a}<br>...<br><b>{a} × {b} = {dividend}</b> (เจอคำตอบแล้ว!)<br>ดังนั้น {dividend} ÷ {a} = <b>{b}</b></span>"

            elif "การแก้สมการ" in actual_sub_t:
                if grade == "ป.4":
                    x, a = random.randint(5, 50), random.randint(1, 20)
                    q = f"แก้สมการ: <span style='color: #3498db; margin-left: 15px;'><b>x + {a} = {x+a}</b></span>"
                    sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>เป้าหมายคือทำให้ x อยู่คนเดียว เราต้องกำจัด +{a} ออกไป<br>โดยใช้สมบัติการเท่ากัน: นำ <b>{a}</b> มาลบออกทั้งสองข้าง<br>x + {a} <b>- {a}</b> = {x+a} <b>- {a}</b><br><b>x = {x}</b></span>"
                elif grade == "ป.5":
                    a, x = random.randint(2, 12), random.randint(2, 20)
                    q = f"แก้สมการ: <span style='color: #3498db; margin-left: 15px;'><b>{a}x = {a*x}</b></span>"
                    sol = f"<span style='color:#2c3e50;'><b>วิธีทำอย่างละเอียด:</b><br>{a} คูณอยู่กับ x เราต้องกำจัด {a} ออกไป<br>โดยใช้สมบัติการเท่ากัน: นำ <b>{a}</b> มาหารทั้งสองข้าง<br>({a}x) <b>÷ {a}</b> = {a*x} <b>÷ {a}</b><br><b>x = {x}</b></span>"

            # ---------------------------------------------
            # Fallback หากไม่ตรงกับโจทย์ใดด้านบน
            # ---------------------------------------------
            else:
                a, b = random.randint(10, 50), random.randint(10, 50)
                q = f"จงหาผลลัพธ์ {prefix} {a} + {b} = {box_html}"
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
