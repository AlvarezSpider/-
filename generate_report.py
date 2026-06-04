"""
生成汽车理论课程设计报告 DOCX
封面和题目使用原始PDF页面图片，解题过程和代码为正文
"""
import os
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

doc = Document()

# ============ 页面设置 A4 ============
for section in doc.sections:
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)

# ============ 样式 ============
style = doc.styles['Normal']
font = style.font
font.name = '宋体'
font.size = Pt(12)
style.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

for i in range(1, 4):
    h_style = doc.styles[f'Heading {i}']
    h_font = h_style.font
    h_font.name = '黑体'
    h_font.color.rgb = RGBColor(0, 0, 0)
    h_style.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    if i == 1:
        h_font.size = Pt(16)
    elif i == 2:
        h_font.size = Pt(14)
    else:
        h_font.size = Pt(13)


def insert_full_page_image(doc, image_path, width=Inches(5.8)):
    """插入图片并居中"""
    if not os.path.exists(image_path):
        doc.add_paragraph(f'[图片缺失: {image_path}]')
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(image_path, width=width)


def add_code_block(doc, code_text):
    """添加代码块"""
    for line in code_text.strip().split('\n'):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = Pt(14)
        run = p.add_run(line)
        run.font.name = 'Consolas'
        run.font.size = Pt(7.5)
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')


def add_formula(doc, formula_text):
    """居中公式"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(formula_text)
    run.font.italic = True
    run.font.size = Pt(11)
    return p


def add_result_table(doc, headers, rows):
    """结果表格"""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    for j, h in enumerate(headers):
        cell = table.rows[0].cells[j]
        cell.text = h
        for p in cell.paragraphs:
            for run in p.runs:
                run.bold = True
                run.font.size = Pt(10)
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="D9E2F3"/>')
        cell._tc.get_or_add_tcPr().append(shading)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = table.rows[i + 1].cells[j]
            cell.text = str(val)
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(10)
    doc.add_paragraph()
    return table


# ============================================================
# 封面（使用原PDF第1页图片 + 个人信息）
# ============================================================
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('汽车理论课程设计')
run.font.name = '黑体'
run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
run.font.size = Pt(26)
run.bold = True
doc.add_paragraph()

info_lines = [
    '专业名称：车辆工程',
    '班    级：2023370501',
    '学    号：2023901021',
    '学生姓名：李思成',
]
for line in info_lines:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(line)
    run.font.size = Pt(14)
doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('2026 年 6 月 1 日')
run.font.size = Pt(14)

doc.add_page_break()

# ============================================================
# 目录
# ============================================================
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('目  录')
run.font.name = '黑体'
run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
run.font.size = Pt(18)
run.bold = True

p_toc = doc.add_paragraph()
run_toc = p_toc.add_run()
run_toc._r.append(parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>'))
run_toc2 = p_toc.add_run()
run_toc2._r.append(parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> TOC \\o "1-3" \\h \\z </w:instrText>'))
run_toc3 = p_toc.add_run()
run_toc3._r.append(parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="separate"/>'))
run_toc4 = p_toc.add_run('[请在Word中右键此处，选择"更新域"以生成目录]')
run_toc4.font.size = Pt(10)
run_toc4.font.color.rgb = RGBColor(128, 128, 128)
run_toc5 = p_toc.add_run()
run_toc5._r.append(parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>'))

doc.add_page_break()

# ============================================================
# 题目一：动力性能计算
# ============================================================
doc.add_heading('题目一：轻型货车动力性能计算（习题1.3）', level=1)

doc.add_heading('1.1 题目原文', level=2)
insert_full_page_image(doc, 'problem1_page1.png', Inches(5.5))
insert_full_page_image(doc, 'problem1_page2.png', Inches(5.5))

doc.add_heading('1.2 已知参数整理', level=2)
params = [
    ['装载质量', '2000 kg'],
    ['整车整备质量', '1800 kg'],
    ['总质量', '3880 kg'],
    ['车轮半径', '0.367 m'],
    ['传动系机械效率 ηt', '0.85'],
    ['滚动阻力系数 f', '0.013'],
    ['空气阻力系数×迎风面积 CDA', '2.77 m²'],
    ['主减速器传动比 i0', '5.83'],
    ['飞轮转动惯量 If', '0.218 kg·m²'],
    ['二前轮转动惯量 Iw1', '1.798 kg·m²'],
    ['四后轮转动惯量 Iw2', '3.598 kg·m²'],
    ['轴距 L', '3.2 m'],
    ['质心至前轴距离（满载）a', '1.947 m'],
    ['质心高（满载）hg', '0.9 m'],
]
add_result_table(doc, ['参数', '数值'], params)

add_result_table(doc, ['档位', '1档', '2档', '3档', '4档', '5档'],
                  [['传动比 ig', '5.56', '2.769', '1.644', '1.00', '0.793']])

doc.add_heading('1.3 主要计算公式', level=2)
doc.add_paragraph('(1) 发动机外特性转矩（Tq-n曲线）：')
add_formula(doc, 'Tq = -19.313 + 295.27(n/1000) - 165.44(n/1000)² + 40.874(n/1000)³ - 3.8445(n/1000)⁴')
doc.add_paragraph('(2) 各档车速与驱动力：')
add_formula(doc, 'ua = 0.377·r·n / (ig·i0)    Ft = Tq·ig·i0·ηt / r')
doc.add_paragraph('(3) 行驶阻力（滚动阻力+空气阻力）：')
add_formula(doc, 'Ff + Fw = G·f + CDA·ua² / 21.15')
doc.add_paragraph('(4) 旋转质量换算系数与加速度：')
add_formula(doc, 'δ = 1 + (ΣIw + If·ig²·i0²·ηt) / (m·r²)')
add_formula(doc, 'a = (Ft - Ff - Fw) / (δ·m)')
doc.add_paragraph('(5) 加速时间（图解积分法）：')
add_formula(doc, 't = (1/3.6)·∫(1/a) dua')

doc.add_heading('1.4 计算结果', level=2)

insert_full_page_image(doc, 'fig1_driving_resistance_balance.png', Inches(5.2))
p_cap = doc.add_paragraph()
p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_cap.add_run('图1  汽车驱动力-行驶阻力平衡图').font.size = Pt(10)

add_result_table(doc, ['项目', '结果'], [
    ['最高车速 ua_max', '99.08 km/h'],
    ['发动机最大转矩 Tq_max', '174.97 N·m @ 2044 r/min'],
    ['发动机最大功率 Pe_max', '61.73 kW @ 3864 r/min'],
    ['最大爬坡度 i', '35.02% (19.30°)'],
    ['最大爬坡度对应车速', '10.01 km/h (1档)'],
    ['最大爬坡度时附着率 Cφ2', '0.4348'],
])

insert_full_page_image(doc, 'fig2_acceleration_curves.png', Inches(5.6))
p_cap = doc.add_paragraph()
p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_cap.add_run('图2  各档加速度曲线与2档加速度倒数曲线').font.size = Pt(10)

add_result_table(doc, ['加速阶段', '时间'], [
    ['2档加速段', '6.34 s'],
    ['换挡', '0.80 s'],
    ['3档加速段', '9.15 s'],
    ['2档起步→70km/h 总计', '16.29 s'],
])

doc.add_page_break()

# ============================================================
# 题目二：燃油经济性计算
# ============================================================
doc.add_heading('题目二：轻型货车燃油经济性计算（习题2.7）', level=1)

doc.add_heading('2.1 题目原文', level=2)
insert_full_page_image(doc, 'problem2_page1.png', Inches(5.5))
insert_full_page_image(doc, 'problem2_page2.png', Inches(5.5))

doc.add_heading('2.2 负荷特性拟合系数', level=2)
add_result_table(doc, ['n (r/min)', 'B0', 'B1', 'B2', 'B3', 'B4'], [
    ['815', '1326.8', '-416.46', '72.379', '-5.8629', '0.17768'],
    ['1207', '1354.7', '-303.98', '36.657', '-2.0553', '0.043072'],
    ['1614', '1284.4', '-189.75', '14.524', '-0.51184', '0.0068164'],
    ['2012', '1122.9', '-121.59', '7.0035', '-0.18517', '0.0018555'],
    ['2603', '1141.0', '-98.893', '4.4763', '-0.091077', '0.00068906'],
    ['3006', '1051.2', '-73.714', '2.8593', '-0.05138', '0.00035032'],
    ['3403', '1233.9', '-84.478', '2.9788', '-0.047449', '0.00028230'],
    ['3804', '1129.7', '-45.291', '0.71113', '-0.00075215', '-0.000038568'],
])

doc.add_heading('2.3 主要计算公式', level=2)
doc.add_paragraph('(1) 发动机功率与阻力功率：')
add_formula(doc, 'Pe = Tq·n / 9550    Pf = (Ff + Fw)·ua / (3600·ηt)')
doc.add_paragraph('(2) 燃油消耗率b值由相邻转速曲线插值：')
add_formula(doc, 'b = B0 + B1·Pe + B2·Pe² + B3·Pe³ + B4·Pe⁴')
doc.add_paragraph('(3) 等速百公里油耗（γ = ρg = 7.007 N/L）：')
add_formula(doc, 'Qs = Pe·b / (1.02·ua·γ)  [L/100km]')
doc.add_paragraph('(4) 瞬时燃油消耗量：')
add_formula(doc, 'Qt = Pe·b / (3600·ρ)  [mL/s]')

doc.add_heading('2.4 计算结果', level=2)

insert_full_page_image(doc, 'fig3_power_balance.png', Inches(5.2))
p_cap = doc.add_paragraph()
p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_cap.add_run('图3  汽车功率平衡图').font.size = Pt(10)

insert_full_page_image(doc, 'fig4_constant_speed_fuel.png', Inches(4.8))
p_cap = doc.add_paragraph()
p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_cap.add_run('图4  最高档与次高档等速百公里油耗曲线').font.size = Pt(10)

doc.add_paragraph('等速百公里油耗特征值：')
add_result_table(doc, ['档位/车速', '油耗 (L/100km)'], [
    ['5档（最高档）30 km/h', '11.99'],
    ['5档（最高档）60 km/h', '13.84'],
    ['5档（最高档）80 km/h', '17.96'],
    ['4档（次高档）30 km/h', '13.35'],
    ['4档（次高档）60 km/h', '15.04'],
    ['4档（次高档）80 km/h', '19.22'],
])

doc.add_paragraph('六工况循环百公里油耗：')
add_result_table(doc, ['工况', '车速 (km/h)', '时间 (s)', '油耗 (mL)'], [
    ['I (等速)', '25', '7.2', '6.02'],
    ['II (加速)', '25→40', '16.7', '24.26'],
    ['III (等速)', '40', '22.5', '31.07'],
    ['IV (加速)', '40→50', '14.0', '23.24'],
    ['V (等速)', '50', '18.0', '32.25'],
    ['VI (减速)', '50→25', '19.3', '24.87'],
])
add_result_table(doc, ['项目', '结果'], [
    ['总油耗', '141.70 mL'],
    ['总行程', '1075 m'],
    ['百公里油耗', '13.18 L/100km'],
])

doc.add_page_break()

# ============================================================
# 题目三：制动性能计算
# ============================================================
doc.add_heading('题目三：中型货车制动性能计算（习题4.3）', level=1)

doc.add_heading('3.1 题目原文', level=2)
insert_full_page_image(doc, 'problem3_page.png', Inches(5.5))

doc.add_heading('3.2 已知参数', level=2)
add_result_table(doc, ['载荷', '质量(kg)', '质心高hg/m', '轴距L/m', '质心至前轴a/m', '制动力分配β'], [
    ['空载', '4080', '0.845', '3.950', '2.100', '0.38'],
    ['满载', '9290', '1.170', '3.950', '2.950', '0.38'],
])

doc.add_heading('3.3 主要计算公式', level=2)
doc.add_paragraph('(1) 利用附着系数（b = L - a）：')
add_formula(doc, 'φf = β·z·L / (b + z·hg)    φr = (1-β)·z·L / (a - z·hg)')
doc.add_paragraph('(2) 制动效率：')
add_formula(doc, 'Ef = z / φf    Er = z / φr')
doc.add_paragraph('(3) 同步附着系数：')
add_formula(doc, 'φ0 = (L·β - b) / hg')
doc.add_paragraph('(4) 制动距离（τ1=0.02s, τ2=0.02s）：')
add_formula(doc, 's = (τ1 + τ2/2)·ua0/3.6 + ua0²/(25.92·E·φ·g)')
doc.add_paragraph('(5) 管路损坏时分别取 β=0（前部坏）或 β=1（后部坏）。')

doc.add_heading('3.4 计算结果', level=2)

insert_full_page_image(doc, 'fig5_adhesion_efficiency.png', Inches(5.6))
p_cap = doc.add_paragraph()
p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_cap.add_run('图5  利用附着系数曲线与制动效率曲线').font.size = Pt(10)

doc.add_paragraph('同步附着系数：')
add_result_table(doc, ['载荷', 'b = L-a (m)', '同步附着系数 φ0'], [
    ['空载', '1.850', '-0.413'],
    ['满载', '1.000', '0.428'],
])

doc.add_paragraph('制动距离汇总（Ua = 30 km/h，φ = 0.80，满载）：')
add_result_table(doc, ['工况', '制动效率 E', 'a_bmax (m/s²)', '制动距离 s (m)'], [
    ['正常制动', '0.8715', '6.83', '5.33'],
    ['前部管路损坏（仅后轮）', '0.6038', '4.73', '7.59'],
    ['后部管路损坏（仅前轮）', '0.3318', '2.60', '13.60'],
])

doc.add_page_break()

# ============================================================
# 附录：程序代码
# ============================================================
doc.add_heading('附录：编程程序代码', level=1)

for name, file in [
    ('A.1 题目一：动力性能计算', 'part1_dynamic_performance.py'),
    ('A.2 题目二：燃油经济性计算', 'part2_fuel_economy.py'),
    ('A.3 题目三：制动性能计算', 'part3_braking_performance.py'),
]:
    doc.add_heading(name, level=2)
    doc.add_paragraph(f'运行：conda run -n modeling python {file}')
    with open(file, 'r', encoding='utf-8') as f:
        add_code_block(doc, f.read())
    if file != 'part3_braking_performance.py':
        doc.add_page_break()

# ============ 保存 ============
doc.save('课程设计报告.docx')
print('报告已保存：课程设计报告.docx')
print('封面和题目使用原版PDF图片，解题过程及代码为正文')
