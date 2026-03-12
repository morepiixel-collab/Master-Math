import ipywidgets as widgets
from IPython.display import display, Markdown, clear_output
from google.colab import files
import random

# ==========================================
# 1. ฐานข้อมูลหลักสูตร (Master Database ป.1-ป.3)
# ==========================================
curriculum_db = {
    "ป.1": {
        "จำนวนนับ 1 ถึง 100 และ 0": [
            "การนับทีละ 1",
            "การนับทีละ 10",
            "การอ่านและการเขียนตัวเลข",
            "การแสดงจำนวนในรูปความสัมพันธ์แบบส่วนย่อย-ส่วนรวม (ภาพกราฟิก)",
            "แบบรูปซ้ำของรูปเรขาคณิต (ภาพกราฟิก)",
            "การบอกอันดับที่ (ภาพกราฟิกรถแข่ง)", 
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
            "การอ่านแผนภูมิรูปภาพอย่างง่าย (ภาพกราฟิก)"
        ]
    },
    "ป.2": {
        "จำนวนนับไม่เกิน 1,000 และ 0": [
            "การนับทีละ 2 ทีละ 5 ทีละ 10 และทีละ 100",
            "การอ่านและการเขียนตัวเลข",
            "จำนวนคู่ จำนวนคี่",
            "หลัก ค่าของเลขโดด และรูปกระจาย",
            "การเปรียบเทียบจำนวน",
            "การเรียงลำดับจำนวน (น้อยไปมาก)",
            "การเรียงลำดับจำนวน (มากไปน้อย)"
        ],
        "เวลาและการวัด": [
            "การบอกเวลาเป็นนาฬิกาและนาที (หน้าปัดนาฬิกา)",
            "การอ่านน้ำหนักจากเครื่องชั่งสปริง (ภาพกราฟิก)"
        ],
        "การบวก ลบ คูณ หาร": [
            "การบวก (แบบตั้งหลัก)",
            "การลบ (แบบตั้งหลัก)",
            "การคูณ การหาร",
            "การบวก ลบ คูณ หารระคน"
        ],
        "แผนภูมิรูปภาพ": [
            "การอ่านแผนภูมิรูปภาพ (ภาพกราฟิก)"
        ]
    },
    "ป.3": {
        "จำนวนนับและเศษส่วน": [
            "การอ่าน การเขียนตัวเลข",
            "หลัก ค่าของเลขโดด และรูปกระจาย",
            "การเปรียบเทียบจำนวน",
            "การเรียงลำดับจำนวน (น้อยไปมาก)",
            "การเรียงลำดับจำนวน (มากไปน้อย)",
            "การอ่านและเขียนเศษส่วน (จากรูปภาพ)",
            "การเปรียบเทียบและการบวกลบเศษส่วน"
        ],
        "เวลา เงิน และการวัด": [
            "การบอกเวลาเป็นนาฬิกาและนาที (หน้าปัดนาฬิกา)",
            "การบอกจำนวนเงินทั้งหมด (ภาพกราฟิกธนบัตรและเหรียญ)",
            "การอ่านน้ำหนักจากเครื่องชั่งสปริง (ภาพกราฟิก)"
        ],
        "การบวก ลบ คูณ หาร": [
            "การบวก (แบบตั้งหลัก)",
            "การลบ (แบบตั้งหลัก)",
            "การคูณ การหารยาวและการหารสั้น",
            "การบวก ลบ คูณ หารระคน"
        ],
        "แผนภูมิรูปภาพ": [
            "การอ่านแผนภูมิรูปภาพ (ภาพกราฟิก)"
        ]
    }
}

# ==========================================
# ฟังก์ชันช่วย: สร้างตารางตั้งหลักเลข (อัปเดตเครื่องหมายเยื้องขวา)
# ==========================================
def generate_vertical_table_html(a, b, op, result=None, is_key=False):
    """วาดตารางตั้งหลักเลข ขยับเครื่องหมายให้อยู่ด้านขวาแบบรูปสกรีนช็อต"""
    str_a = f"{a:>3}" # จัดชิดขวาเพื่อรองรับกรณีตัวเลขหลักไม่เท่ากัน
    str_b = f"{b:>3}"
    
    # เลือกว่าจะแสดง 2 หรือ 3 หลักตามตัวเลขที่มากที่สุด
    show_idx = [1, 2] if max(a, b, (result if result else 0)) < 100 else [0, 1, 2]
    
    res_tds = ""
    if is_key and result is not None:
        str_r = f"{result:>3}"
        res_tds = "".join([f'<td style="width: 35px; text-align: center; color: red;">{str_r[i].strip()}</td>' for i in show_idx])
    else:
        res_tds = "".join([f'<td style="width: 35px; height: 45px;"></td>' for _ in show_idx])

    html = f"""
    <div style="display: inline-block; font-family: 'Sarabun', sans-serif; font-size: 40px; line-height: 1.2; margin: 20px;">
        <table style="border-collapse: collapse; margin-left: auto; margin-right: auto;">
            <tr>
                <td style="width: 20px;"></td>
                {''.join([f'<td style="width: 35px; text-align: center;">{str_a[i].strip()}</td>' for i in show_idx])}
                <td style="width: 50px; text-align: center; vertical-align: middle;" rowspan="2">{op}</td>
            </tr>
            <tr>
                <td></td>
                {''.join([f'<td style="width: 35px; text-align: center; border-bottom: 2px solid #000;">{str_b[i].strip()}</td>' for i in show_idx])}
            </tr>
            <tr>
                <td></td>
                {res_tds}
                <td></td>
            </tr>
            <tr>
                <td></td>
                <td colspan="{len(show_idx)}" style="border-bottom: 6px double #000; height: 10px;"></td>
                <td></td>
            </tr>
        </table>
    </div>
    """
    return html

# ==========================================
# 2. ฟังก์ชันสมองกลสร้างโจทย์และกราฟิก (Master Logic)
# ==========================================
def generate_questions_logic(grade, main_t, sub_t, num_q):
    questions = []
    seen = set()
    limit_map = {"ป.1": 100, "ป.2": 1000, "ป.3": 100000}
    limit = limit_map.get(grade, 100)

    for _ in range(num_q):
        q, sol = "", ""
        attempts = 0
        while attempts < 300:
            
            # ==========================================
            # หมวด: การบวก และ การลบ (แบบตั้งหลักตามสกรีนช็อต)
            # ==========================================
            if sub_t == "การบวก (แบบตั้งหลัก)":
                if grade == "ป.1":
                    # 🟢 สำหรับ ป.1: สองหลัก + หนึ่งหลัก (ไม่มีการทด)
                    tens_a = random.randint(1, 9) 
                    units_a = random.randint(0, 8) 
                    b = random.randint(1, 9 - units_a) 
                    a = (tens_a * 10) + units_a
                else:
                    # สำหรับ ป.2 - ป.3: สุ่มปกติ
                    a = random.randint(10, limit - 20)
                    b = random.randint(1, limit - a - 1)
                
                res = a + b
                q = generate_vertical_table_html(a, b, '+', is_key=False)
                sol = generate_vertical_table_html(a, b, '+', result=res, is_key=True)

            elif sub_t == "การลบ (แบบตั้งหลัก)":
                if grade == "ป.1":
                    # 🟢 สำหรับ ป.1: สองหลัก - หนึ่งหลัก (ไม่มีการยืม)
                    tens_a = random.randint(1, 9) 
                    units_a = random.randint(1, 9) 
                    b = random.randint(1, units_a) 
                    a = (tens_a * 10) + units_a
                else:
                    # สำหรับ ป.2 - ป.3: สุ่มปกติ
                    a = random.randint(10, limit - 1)
                    b = random.randint(1, a - 1)
                
                res = a - b
                q = generate_vertical_table_html(a, b, '-', is_key=False)
                sol = generate_vertical_table_html(a, b, '-', result=res, is_key=True)

            # ==========================================
            # หมวด: กราฟิกภาพ (SVG) คงเดิม 100%
            # ==========================================
            elif sub_t == "การแสดงจำนวนในรูปความสัมพันธ์แบบส่วนย่อย-ส่วนรวม (ภาพกราฟิก)":
                total = random.randint(5, 20)
                p1 = random.randint(1, total - 1)
                p2 = total - p1
                missing_pos = random.choice(['total', 'p1', 'p2'])
                
                q_text_t = "?" if missing_pos == 'total' else str(total)
                q_text_p1 = "?" if missing_pos == 'p1' else str(p1)
                q_text_p2 = "?" if missing_pos == 'p2' else str(p2)
                
                svg_q = f"""<br><div style="text-align: center; margin-top: 15px; margin-bottom: 5px;"><svg width="200" height="160"><line x1="100" y1="40" x2="50" y2="120" stroke="#333" stroke-width="2"/><line x1="100" y1="40" x2="150" y2="120" stroke="#333" stroke-width="2"/><circle cx="100" cy="40" r="28" fill="#ffffff" stroke="#333" stroke-width="2"/><circle cx="50" cy="120" r="28" fill="#ffffff" stroke="#333" stroke-width="2"/><circle cx="150" cy="120" r="28" fill="#ffffff" stroke="#333" stroke-width="2"/><text x="100" y="47" font-size="22" font-weight="bold" text-anchor="middle" fill="{'#e74c3c' if missing_pos=='total' else '#333'}">{q_text_t}</text><text x="50" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{'#e74c3c' if missing_pos=='p1' else '#333'}">{q_text_p1}</text><text x="150" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{'#e74c3c' if missing_pos=='p2' else '#333'}">{q_text_p2}</text></svg></div>"""
                svg_a = f"""<br><div style="text-align: center; margin-top: 15px; margin-bottom: 5px;"><svg width="200" height="160"><line x1="100" y1="40" x2="50" y2="120" stroke="#333" stroke-width="2"/><line x1="100" y1="40" x2="150" y2="120" stroke="#333" stroke-width="2"/><circle cx="100" cy="40" r="28" fill="#ffffff" stroke="#333" stroke-width="2"/><circle cx="50" cy="120" r="28" fill="#ffffff" stroke="#333" stroke-width="2"/><circle cx="150" cy="120" r="28" fill="#ffffff" stroke="#333" stroke-width="2"/><text x="100" y="47" font-size="22" font-weight="bold" text-anchor="middle" fill="{'#e74c3c' if missing_pos=='total' else '#333'}">{total}</text><text x="50" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{'#e74c3c' if missing_pos=='p1' else '#333'}">{p1}</text><text x="150" y="127" font-size="22" font-weight="bold" text-anchor="middle" fill="{'#e74c3c' if missing_pos=='p2' else '#333'}">{p2}</text></svg></div>"""

                q = f"จงหาตัวเลขที่หายไป (?) จากความสัมพันธ์แบบส่วนย่อย-ส่วนรวมต่อไปนี้: {svg_q}"
                sol = f"{svg_a}"

            elif sub_t == "การบอกอันดับที่ (ภาพกราฟิกรถแข่ง)":
                color_map = {"แดง": "#ff4d4d", "ฟ้า": "#3498db", "เขียว": "#2ecc71", "เหลือง": "#f1c40f", "ชมพู": "#ff9ff3"}
                colors_th = list(color_map.keys())
                random.shuffle(colors_th)
                cars_svg = ""
                x_positions = [280, 220, 160, 100, 40]
                for i in range(5):
                    c_hex = color_map[colors_th[i]]
                    x = x_positions[i]
                    cars_svg += f"""
                    <g transform="translate({x}, 40)">
                       <path d="M 10 15 L 15 5 L 30 5 L 35 15 Z" fill="#e0e0e0" stroke="#333" stroke-width="1"/>
                       <rect x="0" y="15" width="50" height="15" rx="4" fill="{c_hex}" stroke="#333" stroke-width="1.5"/>
                       <circle cx="12" cy="30" r="6" fill="#333"/>
                       <circle cx="38" cy="30" r="6" fill="#333"/>
                    </g>
                    """
                svg_diagram = f"""<br><div style="text-align: center; margin-top: 15px; margin-bottom: 15px;"><svg width="400" height="80"><line x1="20" y1="76" x2="380" y2="76" stroke="#95a5a6" stroke-width="4"/><rect x="350" y="30" width="10" height="46" fill="#fff" stroke="#333" stroke-width="1"/><rect x="350" y="30" width="10" height="10" fill="#333"/><rect x="350" y="50" width="10" height="10" fill="#333"/><text x="355" y="20" font-size="14" font-weight="bold" text-anchor="middle" fill="#e74c3c">เส้นชัย</text>{cars_svg}</svg></div>"""
                q_type = random.choice(["find_rank", "find_color"])
                idx = random.randint(0, 4)
                c_name = colors_th[idx]
                ans_svg = f"""<svg width="60" height="30" style="vertical-align: middle; margin-left: 10px;"><path d="M 10 10 L 15 2 L 30 2 L 35 10 Z" fill="#e0e0e0" stroke="#333" stroke-width="1"/><rect x="0" y="10" width="50" height="12" rx="3" fill="{color_map[c_name]}" stroke="#333" stroke-width="1"/><circle cx="12" cy="22" r="5" fill="#333"/><circle cx="38" cy="22" r="5" fill="#333"/></svg>"""
                
                if q_type == "find_rank":
                    q = f"จากภาพการแข่งขัน รถสี{c_name} วิ่งอยู่ในอันดับที่เท่าไร? {svg_diagram}"
                    sol = f"อันดับที่ {idx + 1} {ans_svg}"
                else:
                    q = f"จากภาพการแข่งขัน รถที่วิ่งอยู่ในอันดับที่ {idx + 1} คือรถสีอะไร? {svg_diagram}"
                    sol = f"สี{c_name} {ans_svg}"

            elif sub_t == "แบบรูปซ้ำของรูปเรขาคณิต (ภาพกราฟิก)":
                shapes = {
                    "วงกลม": '<circle cx="15" cy="15" r="12" fill="#ffb3ba" stroke="#333" stroke-width="2"/>',
                    "สี่เหลี่ยม": '<rect x="3" y="3" width="24" height="24" fill="#bae1ff" stroke="#333" stroke-width="2"/>',
                    "สามเหลี่ยม": '<polygon points="15,3 27,27 3,27" fill="#baffc9" stroke="#333" stroke-width="2"/>',
                    "ดาว": '<polygon points="15,1 19,10 29,10 21,16 24,26 15,20 6,26 9,16 1,10 11,10" fill="#ffffba" stroke="#333" stroke-width="2"/>',
                    "หัวใจ": '<path d="M 15 8 C 15 8 10 -2 3 5 C -4 12 15 28 15 28 C 15 28 34 12 27 5 C 20 -2 15 8 15 8 z" fill="#ffdfba" stroke="#333" stroke-width="2"/>'
                }
                ptypes = [[0, 1], [0, 1, 2], [0, 0, 1], [0, 1, 1]]
                pt = random.choice(ptypes)
                keys = random.sample(list(shapes.keys()), len(set(pt)))
                seq = [keys[pt[i % len(pt)]] for i in range(12)]
                slen = random.randint(5, 8) 
                
                html = "<br><div style='margin-top:10px; text-align:center;'>"
                for i in range(slen):
                    html += f'<svg width="30" height="30" style="vertical-align: middle; margin: 0 5px;">{shapes[seq[i]]}</svg>'
                html += '<span style="display:inline-block; width:30px; height:30px; border-bottom:2px dashed #000; margin: 0 5px;"></span></div>'
                
                q = f"จงพิจารณาแบบรูปต่อไปนี้ แล้วบอกว่ารูปที่หายไปคือรูปใด? {html}"
                sol = f"<svg width='30' height='30' style='vertical-align: middle;'>{shapes[seq[slen]]}</svg>"

            elif sub_t == "การบอกเวลาเป็นนาฬิกาและนาที (หน้าปัดนาฬิกา)":
                h = random.randint(1, 12)
                m = random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
                am = m * 6
                ah = (h % 12) * 30 + (m / 60) * 30
                ticks = "".join([f'<line x1="60" y1="15" x2="60" y2="20" stroke="#333" stroke-width="2" transform="rotate({i*30} 60 60)" />' for i in range(12)])
                svg = f"""<br><div style="text-align: center; margin-top: 15px; margin-bottom: 5px;"><svg width="120" height="120"><circle cx="60" cy="60" r="50" fill="#fdfdfd" stroke="#333" stroke-width="3"/>{ticks}<line x1="60" y1="60" x2="60" y2="35" stroke="#e74c3c" stroke-width="4" stroke-linecap="round" transform="rotate({ah} 60 60)" /><line x1="60" y1="60" x2="60" y2="20" stroke="#3498db" stroke-width="3" stroke-linecap="round" transform="rotate({am} 60 60)" /><circle cx="60" cy="60" r="4" fill="#333"/></svg></div>"""
                day = random.choice(["เวลากลางวัน", "เวลากลางคืน"])
                q = f"จากรูปหน้าปัดนาฬิกา หากเป็น <b>{day}</b> จะอ่านเวลาได้กี่นาฬิกา กี่นาที? {svg}"
                ans_h = h
                if day == "เวลากลางวัน":
                    if 1 <= h <= 5: ans_h = h + 12
                    elif h == 12: ans_h = 12
                else: 
                    if 6 <= h <= 11: ans_h = h + 12
                    elif h == 12: ans_h = 0
                sol = f"{ans_h:02d}.{m:02d} น."

            elif sub_t == "การอ่านและเขียนเศษส่วน (จากรูปภาพ)":
                den = random.randint(3, 8)
                num = random.randint(1, den - 1)
                rects = "".join([f'<rect x="{i*30+1}" y="1" width="30" height="30" fill="{"#a0c4ff" if i < num else "#ffffff"}" stroke="#333" stroke-width="2"/>' for i in range(den)])
                svg = f'<br><div style="text-align: center; margin-top: 15px; margin-bottom: 5px;"><svg width="{den*30+2}" height="32">{rects}</svg></div>'
                q = f"จากรูปภาพ ส่วนที่ระบายสีเขียนแสดงเป็นเศษส่วนได้อย่างไร? {svg}"
                sol = f"เศษ {num} ส่วน {den}"

            elif sub_t == "การบอกจำนวนเงินทั้งหมด (ภาพกราฟิกธนบัตรและเหรียญ)":
                b100 = random.randint(0, 3)
                b50 = random.randint(0, 2)
                b20 = random.randint(0, 4)
                c10 = random.randint(0, 5)
                c5 = random.randint(0, 3)
                c1 = random.randint(0, 5)
                if b100+b50+b20+c10+c5+c1 == 0: b20 = 1
                total = (b100*100) + (b50*50) + (b20*20) + (c10*10) + (c5*5) + (c1*1)
                
                money_svg = "<br><div style='margin-top:10px; line-height: 2.5;'>"
                for _ in range(b100): money_svg += '<svg width="60" height="30" style="vertical-align: middle; margin: 2px;"><rect width="60" height="30" rx="3" fill="#ff7675" stroke="#c0392b" stroke-width="2"/><text x="30" y="20" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">100</text></svg>'
                for _ in range(b50): money_svg += '<svg width="60" height="30" style="vertical-align: middle; margin: 2px;"><rect width="60" height="30" rx="3" fill="#74b9ff" stroke="#2980b9" stroke-width="2"/><text x="30" y="20" font-size="12" font-weight="bold" fill="#fff" text-anchor="middle">50</text></svg>'
                for _ in range(b20): money_svg += '<svg width="60" height="30" style="vertical-align: middle; margin: 2px;"><rect width="60" height="30" rx="3" fill="#55efc4" stroke="#27ae60" stroke-width="2"/><text x="30" y="20" font-size="12" font-weight="bold" fill="#333" text-anchor="middle">20</text></svg>'
                for _ in range(c10): money_svg += '<svg width="30" height="30" style="vertical-align: middle; margin: 2px;"><circle cx=\"15\" cy=\"15\" r=\"13\" fill=\"#bdc3c7\" stroke=\"#7f8c8d\" stroke-width=\"2\"/><circle cx=\"15\" cy=\"15\" r=\"8\" fill=\"#f1c40f\"/><text x="15" y="19" font-size="10" font-weight="bold" fill="#333" text-anchor="middle">10</text></svg>'
                for _ in range(c5): money_svg += '<svg width="26" height="26" style="vertical-align: middle; margin: 2px;"><circle cx=\"13\" cy=\"13\" r=\"11\" fill=\"#bdc3c7\" stroke=\"#7f8c8d\" stroke-width=\"2\"/><text x="13" y="17" font-size="10" font-weight="bold" fill="#333" text-anchor="middle">5</text></svg>'
                for _ in range(c1): money_svg += '<svg width="22" height="22" style="vertical-align: middle; margin: 2px;"><circle cx=\"11\" cy=\"11\" r=\"9\" fill=\"#bdc3c7\" stroke=\"#7f8c8d\" stroke-width=\"2\"/><text x="11" y="14" font-size="8" font-weight="bold" fill="#333" text-anchor="middle">1</text></svg>'
                money_svg += "</div>"
                q = f"จากภาพ มีเงินทั้งหมดกี่บาท? {money_svg}"
                sol = f"{total} บาท"

            elif sub_t == "การอ่านน้ำหนักจากเครื่องชั่งสปริง (ภาพกราฟิก)":
                weight = random.randint(1, 5)
                angle = -150 + (weight * 60)
                scale_svg = f"""
                <br>
                <div style="text-align: center; margin-top: 15px; margin-bottom: 5px;">
                    <svg width="150" height="150">
                        <rect x="25" y="20" width="100" height="110" rx="10" fill="#f1f2f6" stroke="#333" stroke-width="3"/>
                        <circle cx="75" cy="75" r="40" fill="#fff" stroke="#333" stroke-width="2"/>
                        <text x="75" y="47" font-size="10" font-weight="bold" text-anchor="middle">0</text>
                        <text x="105" y="65" font-size="10" font-weight="bold" text-anchor="middle">1</text>
                        <text x="100" y="100" font-size="10" font-weight="bold" text-anchor="middle">2</text>
                        <text x="75" y="112" font-size="10" font-weight="bold" text-anchor="middle">3</text>
                        <text x="50" y="100" font-size="10" font-weight="bold" text-anchor="middle">4</text>
                        <text x="45" y="65" font-size="10" font-weight="bold" text-anchor="middle">5</text>
                        <line x1="75" y1="75" x2="75" y2="45" stroke="#e74c3c" stroke-width="3" stroke-linecap="round" transform="rotate({angle} 75 75)" />
                        <circle cx="75" cy="75" r="4" fill="#333"/>
                        <path d="M 50 20 L 40 5 L 110 5 L 100 20 Z" fill="#bdc3c7" stroke="#333" stroke-width="2"/>
                    </svg>
                </div>
                """
                item_name = random.choice(["ส้ม", "แตงโม", "ข้าวสาร", "เนื้อหมู", "ปลา", "ไก่"])
                q = f"จากหน้าปัดเครื่องชั่งสปริง {item_name}มีน้ำหนักกี่กิโลกรัม? {scale_svg}"
                sol = f"{weight} กิโลกรัม"

            elif "การอ่านแผนภูมิรูปภาพ" in sub_t:
                items = [("🍎 แอปเปิล", "🍎"), ("🍊 ส้ม", "🍊"), ("🍌 กล้วย", "🍌"), ("🍓 องุ่น", "🍓")]
                selected = random.sample(items, 3)
                multiplier = 1 if grade == "ป.1" else random.choice([2, 5])
                counts = [random.randint(1, 5), random.randint(1, 5), random.randint(1, 5)]
                
                table_html = f"""<br>
                <div style='margin-top:10px; width: 80%; border: 2px solid #333; border-collapse: collapse;'>
                    <div style='background-color: #f1f2f6; border-bottom: 2px solid #333; text-align: center; padding: 5px; font-weight: bold;'>
                        จำนวนผลไม้ที่ร้านค้าขายได้
                    </div>
                """
                for i in range(3):
                    emojis = "".join([selected[i][1]] * counts[i])
                    table_html += f"""
                    <div style='display: flex; border-bottom: 1px solid #ccc;'>
                        <div style='width: 30%; border-right: 1px solid #ccc; padding: 5px; font-weight: bold;'>{selected[i][0]}</div>
                        <div style='width: 70%; padding: 5px; font-size: 18px;'>{emojis}</div>
                    </div>
                    """
                table_html += f"""
                    <div style='background-color: #fdfdfd; text-align: center; padding: 5px; font-weight: bold; color: #e74c3c;'>
                        กำหนดให้ 1 รูปภาพ แทนผลไม้ {multiplier} ผล
                    </div>
                </div>"""
                
                q_type = random.choice(["how_many", "difference", "total"])
                if q_type == "how_many":
                    idx = random.randint(0, 2)
                    q = f"จากแผนภูมิ ร้านค้าขาย{selected[idx][0].split(' ')[1]}ได้กี่ผล? {table_html}"
                    sol = str(counts[idx] * multiplier)
                elif q_type == "difference":
                    i1, i2 = random.sample([0, 1, 2], 2)
                    if counts[i1] > counts[i2]:
                        q = f"จากแผนภูมิ ร้านค้าขาย{selected[i1][0].split(' ')[1]}ได้มากกว่า{selected[i2][0].split(' ')[1]}กี่ผล? {table_html}"
                        sol = str((counts[i1] - counts[i2]) * multiplier)
                    elif counts[i2] > counts[i1]:
                        q = f"จากแผนภูมิ ร้านค้าขาย{selected[i2][0].split(' ')[1]}ได้มากกว่า{selected[i1][0].split(' ')[1]}กี่ผล? {table_html}"
                        sol = str((counts[i2] - counts[i1]) * multiplier)
                    else:
                        q = f"จากแผนภูมิ ขายผลไม้ 3 ชนิดรวมกันกี่ผล? {table_html}"
                        sol = str(sum(counts) * multiplier)
                else:
                    q = f"จากแผนภูมิ ขายผลไม้ 3 ชนิดรวมกันกี่ผล? {table_html}"
                    sol = str(sum(counts) * multiplier)

            # ==========================================
            # หมวด: เนื้อหาปกติ (Logic แบบ Child-Centric)
            # ==========================================
            elif sub_t == "การนับทีละ 1":
                inc = random.choice([True, False])
                if inc:
                    st = random.randint(0, 95)
                    seq = [st, st+1, st+2, st+3]
                    w = "นับเพิ่มทีละ 1"
                else:
                    st = random.randint(4, 100)
                    seq = [st, st-1, st-2, st-3]
                    w = "นับลดทีละ 1"
                idx = random.randint(0, 3) 
                sol = str(seq[idx])
                q = f"จงเติมตัวเลขที่หายไปในแบบรูปที่{w} : {', '.join([str(s) if i != idx else '_____' for i, s in enumerate(seq)])}"

            elif sub_t == "การนับทีละ 10":
                inc = random.choice([True, False])
                if inc:
                    st = random.randint(0, 60)
                    seq = [st, st+10, st+20, st+30]
                    w = "นับเพิ่มทีละ 10"
                else:
                    st = random.randint(40, 100)
                    seq = [st, st-10, st-20, st-30]
                    w = "นับลดทีละ 10"
                idx = random.randint(0, 3) 
                sol = str(seq[idx])
                q = f"จงเติมตัวเลขที่หายไปในแบบรูปที่{w} : {', '.join([str(s) if i != idx else '_____' for i, s in enumerate(seq)])}"
                
            elif sub_t == "การนับทีละ 2 ทีละ 5 ทีละ 10 และทีละ 100":
                step = random.choice([2, 5, 10, 100])
                inc = random.choice([True, False])
                if inc:
                    st = random.randint(0, 1000 - (3 * step))
                    seq = [st, st+step, st+2*step, st+3*step]
                    w = f"นับเพิ่มทีละ {step}"
                else:
                    st = random.randint(3 * step, 1000)
                    seq = [st, st-step, st-2*step, st-3*step]
                    w = f"นับลดทีละ {step}"
                idx = random.randint(0, 3)
                sol = str(seq[idx])
                q = f"จงเติมตัวเลขที่หายไปในแบบรูปที่{w} : {', '.join([str(s) if i != idx else '_____' for i, s in enumerate(seq)])}"

            elif sub_t == "การเปรียบเทียบจำนวน (> <)" or sub_t == "การเปรียบเทียบจำนวน":
                a = random.randint(10, limit)
                b = random.randint(10, limit)
                while a == b: b = random.randint(10, limit)
                q = f"จงเติมเครื่องหมาย > หรือ < ลงในช่องว่าง: {a} _____ {b}"
                sol = ">" if a > b else "<"

            elif sub_t == "การเปรียบเทียบจำนวน (= ≠)":
                if random.choice([True, False]):
                    a = random.randint(10, limit)
                    b = a  
                    sol = "="
                else:
                    a = random.randint(10, limit)
                    b = random.randint(10, limit)
                    while a == b: b = random.randint(10, limit)
                    sol = "≠"
                q = f"จงเติมเครื่องหมาย = หรือ ≠ ลงในช่องว่าง: {a} _____ {b}"

            elif sub_t == "การเรียงลำดับจำนวน (น้อยไปมาก)":
                nums = random.sample(range(10, limit), 4)
                q = f"จงเรียงลำดับจำนวนต่อไปนี้จาก น้อยไปมาก: {', '.join(map(str, nums))}"
                res = sorted(nums)
                sol = ", ".join(map(str, res))

            elif sub_t == "การเรียงลำดับจำนวน (มากไปน้อย)":
                nums = random.sample(range(10, limit), 4)
                q = f"จงเรียงลำดับจำนวนต่อไปนี้จาก มากไปน้อย: {', '.join(map(str, nums))}"
                res = sorted(nums, reverse=True)
                sol = ", ".join(map(str, res))

            elif sub_t == "จำนวนคู่ จำนวนคี่":
                n = random.randint(10, 999)
                q = f"จำนวน {n} เป็นจำนวนคู่ หรือ จำนวนคี่?"
                sol = "จำนวนคู่" if n % 2 == 0 else "จำนวนคี่"

            elif sub_t in ["การอ่านและการเขียนตัวเลขฮินดูอารบิก ตัวเลขไทยแสดงจำนวน", "การอ่าน การเขียนตัวเลขฮินดูอารบิก ตัวเลขไทย", "การอ่านและการเขียนตัวเลข"]:
                n = random.randint(11, limit-1)
                q = f"จงเขียนตัวเลขฮินดูอารบิก {n} ให้เป็นตัวเลขไทย"
                sol = str(n).translate(str.maketrans('0123456789', '๐๑๒๓๔๕๖๗๘๙'))
                
            elif sub_t in ["หลัก ค่าของเลขโดดในแต่ละหลัก และรูปกระจาย", "หลัก ค่าของเลขโดด และรูปกระจาย", "หลัก ค่าของเลขโดดในแต่ละหลักและการเขียนตัวเลขแสดงจำนวนในรูปกระจาย"]:
                n = random.randint(11, limit-1)
                parts = [str(int(d)*(10**(len(str(n))-1-i))) if d != '0' else '0' for i,d in enumerate(str(n))]
                q = f"จงเขียนจำนวน {n} ในรูปกระจาย"
                sol = " + ".join(parts)

            elif sub_t == "การเปรียบเทียบและการบวกลบเศษส่วน":
                den = random.randint(5, 12)
                n1 = random.randint(1, den-2)
                n2 = 1
                q = f"จงหาผลบวกของ เศษ {n1} ส่วน {den} กับ เศษ {n2} ส่วน {den}"
                sol = f"เศษ {n1+n2} ส่วน {den}"

            elif "โจทย์ปัญหา" in sub_t:
                a = random.randint(20, limit//2)
                b = random.randint(5, 20)
                item = random.choice(["ลูกอม", "ดินสอ", "ตุ๊กตา", "สมุด"])
                if random.choice([True, False]):
                    q = f"แม่ซื้อ{item}มา {a} ชิ้น พ่อซื้อมาให้อีก {b} ชิ้น รวมมี{item}ทั้งหมดกี่ชิ้น?"
                    sol = str(a + b)
                else:
                    q = f"มี{item}อยู่ {a} ชิ้น แบ่งให้เพื่อนไป {b} ชิ้น จะเหลือ{item}กี่ชิ้น?"
                    sol = str(a - b)

            elif "คูณ" in sub_t or "หาร" in sub_t:
                a, b = random.randint(2, 12), random.randint(2, 12)
                q = f"จงหาผลลัพธ์ของ {a} × {b} = ?"
                sol = str(a * b)

            else:
                a, b = random.randint(10, limit//2), random.randint(10, limit//2)
                q = f"จงหาผลลัพธ์ของ {a} + {b} = ?"
                sol = str(a + b)

            if q not in seen:
                seen.add(q)
                questions.append({"question": q, "solution": sol})
                break
            attempts += 1
            
    return questions

# ==========================================
# 3. ระบบ UI และส่งออกไฟล์แบบดาวน์โหลดคู่
# ==========================================
grade_dd = widgets.Dropdown(options=list(curriculum_db.keys()), description='1. ระดับชั้น:')
main_topic_dd = widgets.Dropdown(options=list(curriculum_db[grade_dd.value].keys()), description='2. หัวข้อหลัก:', layout={'width': 'max-content'})
sub_topic_dd = widgets.Dropdown(options=curriculum_db[grade_dd.value][main_topic_dd.value], description='3. หัวข้อย่อย:', layout={'width': 'max-content'})
num_input = widgets.BoundedIntText(value=10, min=1, max=100, description='จำนวนข้อ:')
output = widgets.Output()

def update_main(*args): 
    main_topic_dd.options = list(curriculum_db[grade_dd.value].keys())
grade_dd.observe(update_main, 'value')

def update_sub(*args): 
    if main_topic_dd.value in curriculum_db[grade_dd.value]:
        sub_topic_dd.options = curriculum_db[grade_dd.value][main_topic_dd.value]
main_topic_dd.observe(update_sub, 'value')

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
            # หมวดตั้งหลัก ให้แสดงตารางโจทย์/เฉลย เลย
            html += f'<div class="q-box"><b>ข้อที่ {i}.</b><br>{item["solution"] if is_key else item["question"]}</div>'
        else:
            # หมวดอื่นๆ ให้แสดงโจทย์ และแสดงเส้นตอบ หรือ คำตอบเฉลย
            html += f'<div class="q-box"><b>ข้อที่ {i}.</b> {item["question"]}'
            if is_key: 
                html += f'<br><div class="sol-text">คำตอบ: &nbsp;{item["solution"]}</div>'
            else: 
                html += '<div class="ans-line">ตอบ: </div>'
            html += '</div>'
            
    return html + "</body></html>"

def run_export(obj):
    output.clear_output()

    # สุ่มโจทย์ใหม่
    questions = generate_questions_logic(grade_dd.value, main_topic_dd.value, sub_topic_dd.value, num_input.value)
    
    # 1. เขียนไฟล์ Worksheet
    content_w = create_page(grade_dd.value, sub_topic_dd.value, questions, is_key=False)
    fname_w = f"{grade_dd.value}_Worksheet.html"
    with open(fname_w, 'w', encoding='utf-8') as f: 
        f.write(content_w)
        
    # 2. เขียนไฟล์ Answer Key
    content_k = create_page(grade_dd.value, sub_topic_dd.value, questions, is_key=True)
    fname_k = f"{grade_dd.value}_AnswerKey.html"
    with open(fname_k, 'w', encoding='utf-8') as f: 
        f.write(content_k)
    
    # 3. ดาวน์โหลดพร้อมกัน
    files.download(fname_w)
    files.download(fname_k)
    
btn_download = widgets.Button(description="📥 ดาวน์โหลดแบบฝึกหัด + เฉลย", button_style='primary', layout={'width': 'max-content'})
btn_download.on_click(run_export)

display(widgets.VBox([grade_dd, main_topic_dd, sub_topic_dd, num_input, btn_download, output]))