import streamlit as st
import random
import math

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
        "จำนวนนับ 1 ถึง 100 และ 0": ["การนับทีละ 1", "การนับทีละ 10", "การเปรียบเทียบจำนวน (> <)", "การเปรียบเทียบจำนวน (= ≠)", "การเรียงลำดับจำนวน"],
        "การบวก การลบ": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)"],
        "แผนภูมิและกราฟิก": ["การแสดงจำนวนแบบส่วนย่อย-ส่วนรวม", "การบอกอันดับที่ (รถแข่ง)", "แบบรูปซ้ำของรูปเรขาคณิต"]
    },
    "ป.2": {
        "จำนวนนับไม่เกิน 1,000": ["การนับทีละ 2 ทีละ 5 ทีละ 10 และทีละ 100", "จำนวนคู่ จำนวนคี่", "หลัก ค่าของเลขโดด และรูปกระจาย", "การเรียงลำดับจำนวน"],
        "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การคูณพื้นฐาน", "การหารเบื้องต้น"],
        "เวลาและการวัด": ["การบอกเวลาเป็นนาฬิกาและนาที", "การอ่านน้ำหนักจากเครื่องชั่งสปริง"]
    },
    "ป.3": {
        "จำนวนนับและเศษส่วน": ["หลัก ค่าของเลขโดด และรูปกระจาย", "การอ่านและเขียนเศษส่วน", "การบวกลบเศษส่วน (ตัวส่วนเท่ากัน)"],
        "เวลา เงิน และการวัด": ["การบอกจำนวนเงินทั้งหมด (ธนบัตรและเหรียญ)"],
        "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การคูณ (แบบตั้งหลัก)"]
    },
    "ป.4": {
        "จำนวนนับที่มากกว่า 100,000": ["การอ่านและการเขียนตัวเลข", "หลัก ค่าประจำหลัก และรูปกระจาย", "ค่าประมาณเป็นจำนวนเต็มสิบ เต็มร้อย เต็มพัน"],
        "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การหารยาว"],
        "เศษส่วนและทศนิยม": ["แปลงเศษเกินเป็นจำนวนคละ", "การอ่านและการเขียนทศนิยม"],
        "เรขาคณิตและการวัด": ["การวัดขนาดของมุม (ไม้โปรแทรกเตอร์)"]
    },
    "ป.5": {
        "เศษส่วน": ["การบวกและการลบเศษส่วน", "การคูณและการหารเศษส่วน"],
        "ทศนิยม": ["การบวกและการลบทศนิยม", "การคูณทศนิยม"],
        "ร้อยละและเปอร์เซ็นต์": ["การเขียนเศษส่วนในรูปร้อยละ"]
    },
    "ป.6": {
        "ตัวประกอบของจำนวนนับ": ["การหา ห.ร.ม.", "การหา ค.ร.น."],
        "อัตราส่วนและร้อยละ": ["โจทย์ปัญหาร้อยละ"],
        "สมการ": ["การแก้สมการเบื้องต้น"]
    }
}

# ==========================================
# ฟังก์ชันช่วย: สร้างตารางตั้งหลักเลข 
# ==========================================
def generate_vertical_table_html(a, b, op, result=None, is_key=False):
    max_val = max(a, b, (result if result else 0))
    num_len = max(len(str(max_val)), 2) 
    str_a = f"{a:>{num_len}}"
    str_b = f"{b:>{num_len}}"
    def safe_char(c): return c if c.strip() else "" 
    
    show_idx = list(range(num_len))
    if is_key and result is not None:
        str_r = f"{result:>{num_len}}"
        res_tds = "".join([f'<td style="width: 35px; text-align: center; color: red; font-weight: bold;">{safe_char(str_r[i])}</td>' for i in show_idx])
    else:
        res_tds = "".join([f'<td style="width: 35px; height: 45px;"></td>' for _ in show_idx])

    html = f"""
    <div style="display: inline-block; font-family: 'Sarabun', sans-serif; font-size: 38px; line-height: 1.2; margin: 20px;">
        <table style="border-collapse: collapse; margin-left: auto; margin-right: auto;">
            <tr>
                <td style="width: 20px;"></td>
                {''.join([f'<td style="width: 35px; text-align: center;">{safe_char(str_a[i])}</td>' for i in show_idx])}
                <td style="width: 50px; text-align: center; vertical-align: middle;" rowspan="2">{op}</td>
            </tr>
            <tr>
                <td></td>
                {''.join([f'<td style="width: 35px; text-align: center; border-bottom: 2px solid #000;">{safe_char(str_b[i])}</td>' for i in show_idx])}
            </tr>
            <tr><td></td>{res_tds}<td></td></tr>
            <tr><td></td><td colspan="{len(show_idx)}" style="border-bottom: 6px double #000; height: 10px;"></td><td></td></tr>
        </table>
    </div>
    """
    return html

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
            # ==========================================
            # ลอจิกการตั้งหลัก (ป.1 - ป.6)
            # ==========================================
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

            # ==========================================
            # ลอจิกเฉพาะ ป.4 - ป.6 (เขียนเพิ่มครบทุกหัวข้อแล้ว)
            # ==========================================
            elif sub_t == "การอ่านและการเขียนตัวเลข":
                n = random.randint(100000, 9999999)
                q = f"จงเขียนตัวเลข <b>{n:,}</b> ให้เป็นตัวอักษรภาษาไทย"
                sol = f"<i>(ตัวอย่างเฉลย: ตรวจสอบความถูกต้องจากหลักแสน/หลักล้าน)</i> เลข: {n:,}"

            elif sub_t == "หลัก ค่าประจำหลัก และรูปกระจาย":
                n = random.randint(10000, 999999)
                parts = [str(int(d)*(10**(len(str(n))-1-i))) for i,d in enumerate(str(n)) if d != '0']
                q = f"จงเขียน <b>{n:,}</b> ในรูปกระจาย"
                sol = " + ".join(parts)

            elif sub_t == "ค่าประมาณเป็นจำนวนเต็มสิบ เต็มร้อย เต็มพัน":
                n = random.randint(1111, 99999)
                ptype = random.choice(["เต็มสิบ", "เต็มร้อย", "เต็มพัน"])
                ans = round(n, -1) if ptype == "เต็มสิบ" else (round(n, -2) if ptype == "เต็มร้อย" else round(n, -3))
                q = f"จงหาค่าประมาณเป็นจำนวน<b>{ptype}</b> ของ {n:,}"
                sol = f"{ans:,}"

            elif sub_t == "การหารยาว":
                divisor = random.randint(2, 12)
                quotient = random.randint(100, 999)
                dividend = divisor * quotient
                q = f"จงหาผลลัพธ์ของการหาร: <b>{dividend:,} ÷ {divisor} = ?</b>"
                sol = f"{quotient:,}"

            elif sub_t == "แปลงเศษเกินเป็นจำนวนคละ":
                den = random.randint(3, 12); num = random.randint(den + 1, den * 5)
                q = f"จงเขียนเศษเกินต่อไปนี้ให้อยู่ในรูปจำนวนคละ : <b style='font-size:24px;'><sup>{num}</sup>/<sub>{den}</sub></b>"
                sol = f"{num // den} เศษ {num % den} ส่วน {den}"

            elif sub_t == "การอ่านและการเขียนทศนิยม":
                n = round(random.uniform(0.1, 99.999), random.randint(1, 3))
                q = f"จงเขียน <b>{n}</b> เป็นตัวหนังสือภาษาไทย"
                sol = f"{n}"

            elif sub_t == "การบวกและการลบเศษส่วน":
                den = random.randint(5, 15)
                num1 = random.randint(1, den-1); num2 = random.randint(1, den-1)
                op = "+" if num1 + num2 < den * 2 else "-"
                if op == "-" and num1 < num2: num1, num2 = num2, num1
                ans_num = num1 + num2 if op == "+" else num1 - num2
                q = f"จงหาผลลัพธ์ของ : <b style='font-size:24px;'><sup>{num1}</sup>/<sub>{den}</sub> {op} <sup>{num2}</sup>/<sub>{den}</sub> = ?</b>"
                sol = f"เศษ {ans_num} ส่วน {den}"

            elif sub_t == "การคูณและการหารเศษส่วน":
                n1, d1 = random.randint(1, 5), random.randint(2, 7)
                n2, d2 = random.randint(1, 5), random.randint(2, 7)
                op = random.choice(["×", "÷"])
                q = f"จงหาผลลัพธ์ของ : <b style='font-size:24px;'><sup>{n1}</sup>/<sub>{d1}</sub> {op} <sup>{n2}</sup>/<sub>{d2}</sub> = ?</b>"
                ans_n = n1 * n2 if op == "×" else n1 * d2
                ans_d = d1 * d2 if op == "×" else d1 * n2
                sol = f"เศษ {ans_n} ส่วน {ans_d}"

            elif sub_t == "การบวกและการลบทศนิยม":
                a = round(random.uniform(10.0, 99.9), 2)
                b = round(random.uniform(1.0, 9.9), 2)
                op = random.choice(["+", "-"])
                q = f"จงหาผลลัพธ์ : <b>{a} {op} {b} = ?</b>"
                sol = f"{round(a+b, 2) if op=='+' else round(a-b, 2)}"

            elif sub_t == "การคูณทศนิยม":
                a = round(random.uniform(1.0, 12.0), 1)
                b = random.randint(2, 9)
                q = f"จงหาผลลัพธ์ : <b>{a} × {b} = ?</b>"
                sol = f"{round(a*b, 1)}"

            elif sub_t == "การเขียนเศษส่วนในรูปร้อยละ":
                den = random.choice([2, 4, 5, 10, 20, 25, 50])
                num = random.randint(1, den-1)
                ans = int((num / den) * 100)
                q = f"จงเขียนเศษส่วนต่อไปนี้ให้อยู่ในรูปร้อยละ : <b style='font-size:24px;'><sup>{num}</sup>/<sub>{den}</sub></b>"
                sol = f"ร้อยละ {ans} หรือ {ans}%"

            elif sub_t == "โจทย์ปัญหาร้อยละ":
                price = random.choice([100, 200, 500, 1000, 1500])
                percent = random.choice([10, 15, 20, 25, 50])
                discount = int(price * (percent / 100))
                q = f"เสื้อราคา {price} บาท ร้านค้าลดราคาให้ {percent}% ร้านค้าลดราคาให้กี่บาท?"
                sol = f"{discount} บาท"

            elif sub_t == "การหา ห.ร.ม.":
                a = random.randint(12, 48); b = random.randint(12, 48)
                ans = math.gcd(a, b)
                q = f"จงหา ห.ร.ม. ของ <b>{a}</b> และ <b>{b}</b>"
                sol = str(ans)

            elif sub_t == "การหา ค.ร.น.":
                a = random.randint(4, 24); b = random.randint(4, 24)
                ans = (a * b) // math.gcd(a, b)
                q = f"จงหา ค.ร.น. ของ <b>{a}</b> และ <b>{b}</b>"
                sol = str(ans)

            elif sub_t == "การแก้สมการเบื้องต้น":
                x = random.randint(5, 50); a = random.randint(1, 20); b = x + a
                q = f"จงแก้สมการเพื่อหาค่า x : <br><br><b style='font-size: 24px;'>x + {a} = {b}</b>"
                sol = f"x = {x}"

            elif sub_t == "การวัดขนาดของมุม (ไม้โปรแทรกเตอร์)":
                angle = random.randint(2, 16) * 10
                rad = math.radians(180 - angle)
                x_end = 100 + 70 * math.cos(rad); y_end = 90 - 70 * math.sin(rad)
                svg = f"""<br><div style="text-align: center;"><svg width="200" height="120"><path d="M 20 90 A 80 80 0 0 1 180 90" fill="#fdfdfd" stroke="#333" stroke-width="2"/><line x1="20" y1="90" x2="180" y2="90" stroke="#333" stroke-width="2"/><circle cx="100" cy="90" r="4" fill="#e74c3c"/><line x1="100" y1="90" x2="190" y2="90" stroke="#3498db" stroke-width="3"/><line x1="100" y1="90" x2="{x_end}" y2="{y_end}" stroke="#e74c3c" stroke-width="3"/></svg></div>"""
                q = f"มุมที่แสดงบนไม้โปรแทรกเตอร์มีขนาดกี่องศา? {svg}"
                sol = f"{angle} องศา"

            # ==========================================
            # ลอจิกพื้นฐานทั่วไป (อื่นๆ ป.1-ป.3)
            # ==========================================
            elif "การนับทีละ" in sub_t:
                step = int(sub_t.split()[-1]) if any(c.isdigit() for c in sub_t) else 1
                inc = random.choice([True, False])
                st_val = random.randint(10, 100)
                seq = [st_val, st_val+step, st_val+2*step, st_val+3*step] if inc else [st_val+3*step, st_val+2*step, st_val+step, st_val]
                idx = random.randint(0, 3); sol = str(seq[idx])
                q = f"จงเติมตัวเลขที่หายไปในแบบรูป : {', '.join([str(s) if i != idx else '_____' for i, s in enumerate(seq)])}"

            else:
                a, b = random.randint(10, 50), random.randint(10, 50)
                q = f"โจทย์ปัญหา : {a} + {b} = ?"
                sol = str(a + b)

            if q not in seen:
                seen.add(q); questions.append({"question": q, "solution": sol}); break
            attempts += 1
    return questions

def create_page(grade, sub_t, questions, is_key=False):
    title = "เฉลยแบบฝึกหัด" if is_key else "แบบฝึกหัดคณิตศาสตร์"
    html = f"""<!DOCTYPE html><html lang="th"><head><meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css2?family=Sarabun&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Sarabun', sans-serif; padding: 40px; line-height: 1.8; }}
        .header {{ text-align: center; border-bottom: 2px solid #333; margin-bottom: 20px; }}
        .q-box {{ margin-bottom: 30px; padding: 15px; page-break-inside: avoid; border-bottom: 1px solid #eee; }}
        .ans-line {{ margin-top: 15px; border-bottom: 1px dotted #999; width: 80%; height: 30px; }}
        .sol-text {{ color: red; font-weight: bold; border-left: 3px solid red; padding-left: 10px; display: inline-block; margin-top: 10px; }}
    </style></head><body>
    <div class="header"><h2>{title} - {grade}</h2><p><b>เรื่อง:</b> {sub_t}</p></div>"""
    
    for i, item in enumerate(questions, 1):
        if "(แบบตั้งหลัก)" in sub_t:
            html += f'<div class="q-box"><b>ข้อที่ {i}.</b><br>{item["solution"] if is_key else item["question"]}</div>'
        else:
            html += f'<div class="q-box"><b>ข้อที่ {i}.</b> {item["question"]}'
            if is_key: html += f'<br><div class="sol-text">คำตอบ: &nbsp;{item["solution"]}</div>'
            else: html += '<div class="ans-line">ตอบ: </div>'
            html += '</div>'
    return html + "</body></html>"

# ==========================================
# 3. สร้าง UI ของ Streamlit Web App
# ==========================================
st.sidebar.header("⚙️ การตั้งค่าใบงาน")
selected_grade = st.sidebar.selectbox("1. เลือกระดับชั้น:", list(curriculum_db.keys()))
selected_main = st.sidebar.selectbox("2. เลือกหัวข้อหลัก:", list(curriculum_db[selected_grade].keys()))
selected_sub = st.sidebar.selectbox("3. เลือกหัวข้อย่อย:", curriculum_db[selected_grade][selected_main])
num_input = st.sidebar.number_input("จำนวนข้อ:", min_value=1, max_value=100, value=10)

if st.sidebar.button("🚀 สร้างใบงาน", type="primary", use_container_width=True):
    with st.spinner("กำลังประมวลผลลอจิกและสร้างโจทย์..."):
        qs = generate_questions_logic(selected_grade, selected_main, selected_sub, num_input)
        html_w = create_page(selected_grade, selected_sub, qs, is_key=False)
        html_k = create_page(selected_grade, selected_sub, qs, is_key=True)
        
        st.session_state['worksheet'] = html_w
        st.session_state['answerkey'] = html_k
        st.session_state['filename'] = f"{selected_grade}_{selected_sub}"

if 'worksheet' in st.session_state:
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📄 ดาวน์โหลดใบงาน",
            data=st.session_state['worksheet'],
            file_name=f"{st.session_state['filename']}_Worksheet.html",
            mime="text/html",
            use_container_width=True
        )
    with col2:
        st.download_button(
            label="🔑 ดาวน์โหลดเฉลย",
            data=st.session_state['answerkey'],
            file_name=f"{st.session_state['filename']}_AnswerKey.html",
            mime="text/html",
            use_container_width=True
        )
else:
    st.info("👈 กรุณาตั้งค่าใบงานที่เมนูด้านซ้าย แล้วกดปุ่ม 'สร้างใบงาน'")
