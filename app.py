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
        "จำนวนนับ 1 ถึง 100 และ 0": [
            "การนับทีละ 1", "การนับทีละ 10", "การอ่านและการเขียนตัวเลข",
            "การแสดงจำนวนในรูปความสัมพันธ์แบบส่วนย่อย-ส่วนรวม (ภาพกราฟิก)",
            "แบบรูปซ้ำของรูปเรขาคณิต (ภาพกราฟิก)", "การบอกอันดับที่ (ภาพกราฟิกรถแข่ง)", 
            "หลัก ค่าของเลขโดดในแต่ละหลัก และรูปกระจาย", "การเปรียบเทียบจำนวน (> <)",  
            "การเปรียบเทียบจำนวน (= ≠)", "การเรียงลำดับจำนวน (น้อยไปมาก)", "การเรียงลำดับจำนวน (มากไปน้อย)"
        ],
        "การบวก การลบ": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)"],
        "แผนภูมิรูปภาพ": ["การอ่านแผนภูมิรูปภาพอย่างง่าย (ภาพกราฟิก)"]
    },
    "ป.2": {
        "จำนวนนับไม่เกิน 1,000 และ 0": [
            "การนับทีละ 2 ทีละ 5 ทีละ 10 และทีละ 100", "การอ่านและการเขียนตัวเลข",
            "จำนวนคู่ จำนวนคี่", "หลัก ค่าของเลขโดด และรูปกระจาย", "การเปรียบเทียบจำนวน",
            "การเรียงลำดับจำนวน (น้อยไปมาก)", "การเรียงลำดับจำนวน (มากไปน้อย)"
        ],
        "เวลาและการวัด": ["การบอกเวลาเป็นนาฬิกาและนาที (หน้าปัดนาฬิกา)", "การอ่านน้ำหนักจากเครื่องชั่งสปริง (ภาพกราฟิก)"],
        "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การคูณ การหาร", "การบวก ลบ คูณ หารระคน"],
        "แผนภูมิรูปภาพ": ["การอ่านแผนภูมิรูปภาพ (ภาพกราฟิก)"]
    },
    "ป.3": {
        "จำนวนนับและเศษส่วน": [
            "การอ่าน การเขียนตัวเลข", "หลัก ค่าของเลขโดด และรูปกระจาย", "การเปรียบเทียบจำนวน",
            "การเรียงลำดับจำนวน (น้อยไปมาก)", "การเรียงลำดับจำนวน (มากไปน้อย)",
            "การอ่านและเขียนเศษส่วน (จากรูปภาพ)", "การเปรียบเทียบและการบวกลบเศษส่วน"
        ],
        "เวลา เงิน และการวัด": ["การบอกเวลาเป็นนาฬิกาและนาที (หน้าปัดนาฬิกา)", "การบอกจำนวนเงินทั้งหมด (ภาพกราฟิกธนบัตรและเหรียญ)", "การอ่านน้ำหนักจากเครื่องชั่งสปริง (ภาพกราฟิก)"],
        "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การคูณ การหารยาวและการหารสั้น", "การบวก ลบ คูณ หารระคน"],
        "แผนภูมิรูปภาพ": ["การอ่านแผนภูมิรูปภาพ (ภาพกราฟิก)"]
    },
    "ป.4": {
        "จำนวนนับที่มากกว่า 100,000": ["การอ่านและการเขียนตัวเลข", "หลัก ค่าประจำหลัก และรูปกระจาย", "การเปรียบเทียบและเรียงลำดับ", "ค่าประมาณเป็นจำนวนเต็มสิบ เต็มร้อย เต็มพัน"],
        "การบวก ลบ คูณ หาร": ["การบวก (แบบตั้งหลัก)", "การลบ (แบบตั้งหลัก)", "การหารยาว"],
        "เศษส่วนและทศนิยม": ["แปลงเศษเกินเป็นจำนวนคละ", "การอ่านและการเขียนทศนิยม"],
        "เรขาคณิตและการวัด": ["การวัดขนาดของมุม (ภาพกราฟิกไม้โปรแทรกเตอร์)"]
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
# ฟังก์ชันช่วย: สร้างตารางตั้งหลักเลข (ขยายหลักอัตโนมัติถึงหลักล้าน)
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
            # === การบวก ลบ ตั้งหลัก ===
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

            # === กราฟิก SVG ป.1-ป.3 ===
            elif sub_t == "การแสดงจำนวนในรูปความสัมพันธ์แบบส่วนย่อย-ส่วนรวม (ภาพกราฟิก)":
                total = random.randint(5, 20); p1 = random.randint(1, total - 1); p2 = total - p1
                miss = random.choice(['t', 'p1', 'p2'])
                svg_t = f"""<br><div style="text-align: center;"><svg width="200" height="160"><line x1="100" y1="40" x2="50" y2="120" stroke="#333" stroke-width="2"/><line x1="100" y1="40" x2="150" y2="120" stroke="#333" stroke-width="2"/><circle cx="100" cy="40" r="28" fill="#ffffff" stroke="#333" stroke-width="2"/><circle cx="50" cy="120" r="28" fill="#ffffff" stroke="#333" stroke-width="2"/><circle cx="150" cy="120" r="28" fill="#ffffff" stroke="#333" stroke-width="2"/><text x="100" y="47" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='t' else "#333"}">{{t}}</text><text x="50" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='p1' else "#333"}">{{p1}}</text><text x="150" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{"#e74c3c" if miss=='p2' else "#333"}">{{p2}}</text></svg></div>"""
                q = f"จงหาตัวเลขที่หายไป (?) : " + svg_t.format(t="?" if miss=='t' else total, p1="?" if miss=='p1' else p1, p2="?" if miss=='p2' else p2)
                sol = svg_t.format(t=total, p1=p1, p2=p2)

            elif sub_t == "การบอกอันดับที่ (ภาพกราฟิกรถแข่ง)":
                c_map = {"แดง": "#ff4d4d", "ฟ้า": "#3498db", "เขียว": "#2ecc71", "เหลือง": "#f1c40f", "ชมพู": "#ff9ff3"}
                cols = list(c_map.keys()); random.shuffle(cols); x_pos = [280, 220, 160, 100, 40]
                cars = "".join([f'<g transform="translate({x_pos[i]}, 40)"><path d="M 10 15 L 15 5 L 30 5 L 35 15 Z" fill="#e0e0e0" stroke="#333" stroke-width="1"/><rect x="0" y="15" width="50" height="15" rx="4" fill="{c_map[cols[i]]}" stroke="#333" stroke-width="1.5"/><circle cx="12" cy="30" r="6" fill="#333"/><circle cx="38" cy="30" r="6" fill="#333"/></g>' for i in range(5)])
                svg_d = f"""<br><div style="text-align: center;"><svg width="400" height="80"><line x1="20" y1="76" x2="380" y2="76" stroke="#95a5a6" stroke-width="4"/><rect x="350" y="30" width="10" height="46" fill="#fff" stroke="#333"/><text x="355" y="20" font-size="14" font-weight="bold" text-anchor="middle" fill="#e74c3c">เส้นชัย</text>{cars}</svg></div>"""
                idx = random.randint(0, 4); name = cols[idx]
                ans_svg = f'<svg width="60" height="30" style="vertical-align: middle;"><path d="M 10 10 L 15 2 L 30 2 L 35 10 Z" fill="#e0e0e0" stroke="#333"/><rect y="10" width="50" height="12" rx="3" fill="{c_map[name]}" stroke="#333"/><circle cx="12" cy="22" r="5" fill="#333"/><circle cx="38" cy="22" r="5" fill="#333"/></svg>'
                if random.choice([True, False]): q, sol = f"รถสี{name} วิ่งอยู่อันดับที่เท่าไร? {svg_d}", f"อันดับที่ {idx + 1} {ans_svg}"
                else: q, sol = f"รถที่วิ่งอยู่ในอันดับที่ {idx + 1} คือรถสีอะไร? {svg_d}", f"สี{name} {ans_svg}"

            # === กราฟิก SVG ป.4-ป.6 ===
            elif sub_t == "การวัดขนาดของมุม (ภาพกราฟิกไม้โปรแทรกเตอร์)":
                angle = random.randint(2, 16) * 10
                rad = math.radians(180 - angle)
                x_end = 100 + 70 * math.cos(rad); y_end = 90 - 70 * math.sin(rad)
                svg = f"""<br><div style="text-align: center;"><svg width="200" height="120"><path d="M 20 90 A 80 80 0 0 1 180 90" fill="#fdfdfd" stroke="#333" stroke-width="2"/><line x1="20" y1="90" x2="180" y2="90" stroke="#333" stroke-width="2"/><circle cx="100" cy="90" r="4" fill="#e74c3c"/><line x1="100" y1="90" x2="190" y2="90" stroke="#3498db" stroke-width="3"/><line x1="100" y1="90" x2="{x_end}" y2="{y_end}" stroke="#e74c3c" stroke-width="3"/></svg></div>"""
                q, sol = f"มุมที่แสดงบนไม้โปรแทรกเตอร์มีขนาดกี่องศา? {svg}", f"{angle} องศา"

            elif sub_t == "การแก้สมการเบื้องต้น":
                x = random.randint(5, 50); a = random.randint(1, 20); b = x + a
                q, sol = f"จงแก้สมการหาค่า x : <br><br><span style='font-size: 24px;'>x + {a} = {b}</span>", f"x = {x}"

            elif sub_t == "การหา ห.ร.ม.":
                a = random.randint(12, 48); b = random.randint(12, 48)
                ans = math.gcd(a, b)
                q, sol = f"จงหา ห.ร.ม. ของ {a} และ {b}", str(ans)

            elif sub_t == "การหา ค.ร.น.":
                a = random.randint(4, 24); b = random.randint(4, 24)
                ans = (a * b) // math.gcd(a, b)
                q, sol = f"จงหา ค.ร.น. ของ {a} และ {b}", str(ans)

            # === หมวดพื้นฐาน ป.1-ป.3 (ที่เหลือ) ===
            elif sub_t == "การนับทีละ 1":
                inc = random.choice([True, False]); st = random.randint(0, 95)
                seq = [st, st+1, st+2, st+3] if inc else [st+4, st+3, st+2, st+1]
                idx = random.randint(0, 3); sol = str(seq[idx])
                q = f"จงเติมตัวเลขที่หายไปในแบบรูปที่{'นับเพิ่ม' if inc else 'นับลด'}ทีละ 1 : {', '.join([str(s) if i != idx else '_____' for i, s in enumerate(seq)])}"

            else:
                a = random.randint(1, 10); q, sol = f"โจทย์ทั่วไปสำหรับหัวข้อนี้: {a}", str(a)

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
    with st.spinner("กำลังประมวลผลลอจิกและวาดกราฟิก..."):
        qs = generate_questions_logic(selected_grade, selected_main, selected_sub, num_input)
        html_w = create_page(selected_grade, selected_sub, qs, is_key=False)
        html_k = create_page(selected_grade, selected_sub, qs, is_key=True)
        
        st.session_state['worksheet'] = html_w
        st.session_state['answerkey'] = html_k
        st.session_state['filename'] = f"{selected_grade}_{selected_sub}"

# แสดงผลหน้าจอกลาง
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
