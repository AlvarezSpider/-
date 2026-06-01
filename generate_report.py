"""
生成汽车理论课程设计报告 DOCX
使用 python-docx + XML 方法
"""
import os
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
from lxml import etree

doc = Document()

# ============ 页面设置 A4 ============
for section in doc.sections:
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.18)
    section.right_margin = Cm(3.18)

# ============ 样式设置 ============
style = doc.styles['Normal']
font = style.font
font.name = '宋体'
font.size = Pt(12)
style.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

# 标题样式
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

def add_code_block(doc, code_text, title=None):
    """添加代码块"""
    if title:
        p = doc.add_paragraph()
        run = p.add_run(title)
        run.bold = True
        run.font.name = '黑体'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
        run.font.size = Pt(11)

    for line in code_text.strip().split('\n'):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = Pt(14)
        run = p.add_run(line)
        run.font.name = 'Consolas'
        run.font.size = Pt(8)
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

def add_formula(doc, formula_text):
    """添加公式（居中）"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(formula_text)
    run.font.italic = True
    run.font.size = Pt(11)
    return p

def add_result_table(doc, headers, rows):
    """添加结果表格"""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    # 表头
    for j, h in enumerate(headers):
        cell = table.rows[0].cells[j]
        cell.text = h
        for p in cell.paragraphs:
            for run in p.runs:
                run.bold = True
                run.font.size = Pt(10)
        # 灰色背景
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="D9E2F3"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    # 数据行
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = table.rows[i + 1].cells[j]
            cell.text = str(val)
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(10)
    doc.add_paragraph()  # 表后空行
    return table


# ============================================================
# 封面
# ============================================================
for _ in range(4):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('汽车理论课程设计')
run.font.name = '黑体'
run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
run.font.size = Pt(26)
run.bold = True

doc.add_paragraph()

info_lines = [
    '专业名称：______________________________',
    '班    级：______________________________',
    '学    号：______________________________',
    '学生姓名：______________________________',
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
# 目录页
# ============================================================
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('目  录')
run.font.name = '黑体'
run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
run.font.size = Pt(18)
run.bold = True

# 插入目录域代码 (TOC field)
p_toc = doc.add_paragraph()
run_toc = p_toc.add_run()
fldChar_begin = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
run_toc._r.append(fldChar_begin)

run_toc2 = p_toc.add_run()
instrText = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> TOC \\o "1-3" \\h \\z </w:instrText>')
run_toc2._r.append(instrText)

run_toc3 = p_toc.add_run()
fldChar_sep = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="separate"/>')
run_toc3._r.append(fldChar_sep)

run_toc4 = p_toc.add_run('[请在Word中右键点击此处，选择"更新域"以生成目录]')
run_toc4.font.size = Pt(10)
run_toc4.font.color.rgb = RGBColor(128, 128, 128)

run_toc5 = p_toc.add_run()
fldChar_end = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
run_toc5._r.append(fldChar_end)

doc.add_page_break()

# ============================================================
# 题目一：动力性能计算
# ============================================================
doc.add_heading('题目一：轻型货车动力性能计算（习题1.3）', level=1)

doc.add_heading('1.1 题目描述', level=2)
doc.add_paragraph(
    '确定一轻型货车的动力性能（货车装用五档变速器）：'
)
doc.add_paragraph('(1) 绘制汽车驱动力与行驶阻力平衡图。')
doc.add_paragraph('(2) 求汽车最高车速、最大爬坡度及克服该坡度时相应的附着率。')
doc.add_paragraph('(3) 绘制汽车行驶加速度倒数曲线，用计算机求汽车用2档起步加速行驶至70km/h的加速时间。')

doc.add_heading('1.2 已知参数', level=2)
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

doc.add_heading('1.3 变速器传动比（五档）', level=2)
add_result_table(doc, ['档位', '1档', '2档', '3档', '4档', '5档'],
                  [['传动比 ig', '5.56', '2.769', '1.644', '1.00', '0.793']])

doc.add_heading('1.4 计算公式', level=2)

doc.add_paragraph('(1) 发动机外特性转矩拟合公式（Tq-n曲线）：')
add_formula(doc, 'Tq = -19.313 + 295.27(n/1000) - 165.44(n/1000)² + 40.874(n/1000)³ - 3.8445(n/1000)⁴')

doc.add_paragraph('(2) 各档车速：')
add_formula(doc, 'ua = 0.377 × r × n / (ig × i0)  [km/h]')

doc.add_paragraph('(3) 各档驱动力：')
add_formula(doc, 'Ft = Tq × ig × i0 × ηt / r  [N]')

doc.add_paragraph('(4) 行驶阻力：')
add_formula(doc, 'Ff + Fw = G × f + CDA × ua² / 21.15  [N]')

doc.add_paragraph('(5) 旋转质量换算系数：')
add_formula(doc, 'δ = 1 + (ΣIw + If × ig² × i0² × ηt) / (m × r²)')

doc.add_paragraph('(6) 加速度：')
add_formula(doc, 'a = (Ft - Ff - Fw) / (δ × m)  [m/s²]')

doc.add_paragraph('(7) 加速时间（图解积分法）：')
add_formula(doc, 't = ∫(1/a) du = (1/3.6) × ∫(1/a) dua  [s]')

doc.add_heading('1.5 计算结果', level=2)

doc.add_paragraph('(1) 驱动力-行驶阻力平衡图如图1所示。')

# 插入图1
if os.path.exists('fig1_driving_resistance_balance.png'):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_img = p_img.add_run()
    run_img.add_picture('fig1_driving_resistance_balance.png', width=Inches(5.5))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_cap = p_cap.add_run('图1  汽车驱动力-行驶阻力平衡图')
    run_cap.font.size = Pt(10)
    run_cap.bold = True

doc.add_paragraph('(2) 最高车速与最大爬坡度：')

r1 = [
    ['最高车速 ua_max', '99.08 km/h'],
    ['发动机最大转矩 Tq_max', '174.97 N·m @ 2044 r/min'],
    ['发动机最大功率 Pe_max', '61.73 kW @ 3864 r/min'],
    ['最大爬坡度 i', '35.02% (19.30°)'],
    ['最大爬坡度对应车速', '10.01 km/h'],
    ['最大爬坡度时附着率 Cφ2', '0.4348'],
]
add_result_table(doc, ['项目', '结果'], r1)

doc.add_paragraph('(3) 加速度倒数曲线与加速时间：')

if os.path.exists('fig2_acceleration_curves.png'):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_img = p_img.add_run()
    run_img.add_picture('fig2_acceleration_curves.png', width=Inches(5.8))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_cap = p_cap.add_run('图2  各档加速度曲线与2档加速度倒数曲线')
    run_cap.font.size = Pt(10)
    run_cap.bold = True

r2 = [
    ['2档加速段时间', '6.34 s'],
    ['换挡时间', '0.80 s'],
    ['3档加速段时间', '9.15 s'],
    ['2档起步加速至70km/h总时间', '16.29 s'],
]
add_result_table(doc, ['项目', '时间'], r2)

doc.add_page_break()

# ============================================================
# 题目二：燃油经济性计算
# ============================================================
doc.add_heading('题目二：轻型货车燃油经济性计算（习题2.7）', level=1)

doc.add_heading('2.1 题目描述', level=2)
doc.add_paragraph(
    '货车的参数与题目一相同。负荷特性曲线的拟合公式为：'
)
add_formula(doc, 'b = B0 + B1·Pe + B2·Pe² + B3·Pe³ + B4·Pe⁴')
doc.add_paragraph('式中，b为燃油消耗率[g/(kW·h)]，Pe为发动机净功率(kW)。')
doc.add_paragraph('(1) 绘制该轻型货车的功率平衡图。')
doc.add_paragraph('(2) 绘制最高挡与次高挡的等速百公里油耗曲线。')
doc.add_paragraph('(3) 计算六工况循环行驶的百公里油耗。')

doc.add_heading('2.2 负荷特性拟合系数', level=2)
load_headers = ['n (r/min)', 'B0', 'B1', 'B2', 'B3', 'B4']
load_rows = [
    ['815', '1326.8', '-416.46', '72.379', '-5.8629', '0.17768'],
    ['1207', '1354.7', '-303.98', '36.657', '-2.0553', '0.043072'],
    ['1614', '1284.4', '-189.75', '14.524', '-0.51184', '0.0068164'],
    ['2012', '1122.9', '-121.59', '7.0035', '-0.18517', '0.0018555'],
    ['2603', '1141.0', '-98.893', '4.4763', '-0.091077', '0.00068906'],
    ['3006', '1051.2', '-73.714', '2.8593', '-0.05138', '0.00035032'],
    ['3403', '1233.9', '-84.478', '2.9788', '-0.047449', '0.00028230'],
    ['3804', '1129.7', '-45.291', '0.71113', '-0.00075215', '-0.000038568'],
]
add_result_table(doc, load_headers, load_rows)

doc.add_heading('2.3 计算公式', level=2)
doc.add_paragraph('(1) 发动机功率：')
add_formula(doc, 'Pe = Tq × n / 9550  [kW]')
doc.add_paragraph('(2) 阻力功率：')
add_formula(doc, 'Pf = (Ff + Fw) × ua / (3600 × ηt)  [kW]')
doc.add_paragraph('(3) 等速百公里油耗：')
add_formula(doc, 'Qs = Pe × b / (1.02 × ua × γ)  [L/100km]')
doc.add_paragraph('式中，γ为燃油重度，93#汽油 γ = ρg = 0.715×9.8 = 7.007 N/L。')
doc.add_paragraph('(4) 瞬时燃油消耗量：')
add_formula(doc, 'Qt = Pe × b / (3600 × ρ)  [mL/s]')

doc.add_heading('2.4 计算结果', level=2)

doc.add_paragraph('(1) 功率平衡图如图3所示。')
if os.path.exists('fig3_power_balance.png'):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.add_run().add_picture('fig3_power_balance.png', width=Inches(5.5))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.add_run('图3  汽车功率平衡图').font.size = Pt(10)

doc.add_paragraph('(2) 等速百公里油耗曲线如图4所示。')
if os.path.exists('fig4_constant_speed_fuel.png'):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.add_run().add_picture('fig4_constant_speed_fuel.png', width=Inches(5.0))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.add_run('图4  最高档与次高档等速百公里油耗曲线').font.size = Pt(10)

doc.add_paragraph('(3) 等速百公里油耗特征值：')
r3 = [
    ['5档（最高档）最低油耗', '11.99 L/100km @ 30 km/h'],
    ['5档 60km/h等速油耗', '13.84 L/100km'],
    ['5档 80km/h等速油耗', '17.96 L/100km'],
    ['4档（次高档）最低油耗', '13.35 L/100km @ 30 km/h'],
    ['4档 60km/h等速油耗', '15.04 L/100km'],
    ['4档 80km/h等速油耗', '19.22 L/100km'],
]
add_result_table(doc, ['项目', '油耗'], r3)

doc.add_paragraph('(4) 六工况循环百公里油耗：')
r4 = [
    ['工况I（等速25km/h，7.2s）', '6.02 mL'],
    ['工况II（25→40km/h加速，16.7s）', '24.26 mL'],
    ['工况III（等速40km/h，22.5s）', '31.07 mL'],
    ['工况IV（40→50km/h加速，14.0s）', '23.24 mL'],
    ['工况V（等速50km/h，18.0s）', '32.25 mL'],
    ['工况VI（50→25km/h减速，19.3s）', '24.87 mL'],
    ['总油耗 / 总行程', '141.70 mL / 1075 m'],
    ['六工况百公里油耗', '13.18 L/100km'],
]
add_result_table(doc, ['工况', '油耗'], r4)

doc.add_page_break()

# ============================================================
# 题目三：制动性能计算
# ============================================================
doc.add_heading('题目三：中型货车制动性能计算（习题4.3）', level=1)

doc.add_heading('3.1 题目描述', level=2)
doc.add_paragraph(
    '一中型货车装有前后制动器分开的双管路制动系，有关参数如下表所示：'
)
r5 = [
    ['空载', '4080', '0.845', '3.950', '2.100', '0.38'],
    ['满载', '9290', '1.170', '3.950', '2.950', '0.38'],
]
add_result_table(doc, ['载荷', '质量(kg)', '质心高hg/m', '轴距L/m', '质心至前轴a/m', '制动力分配系数β'], r5)

doc.add_paragraph('(1) 计算并绘制利用附着系数曲线和制动效率曲线。')
doc.add_paragraph('(2) 求行驶车速Ua=30km/h，在φ=0.80路面上车轮不抱死的制动距离。')
doc.add_paragraph('(3) 求制动系前部/后部管路损坏时的制动距离。')

doc.add_heading('3.2 计算公式', level=2)
doc.add_paragraph('(1) 利用附着系数：')
add_formula(doc, 'φf = β × z × L / (b + z × hg)')
add_formula(doc, 'φr = (1-β) × z × L / (a - z × hg)')
doc.add_paragraph('式中，z为制动强度，b = L - a为质心至后轴距离。')

doc.add_paragraph('(2) 制动效率：')
add_formula(doc, 'Ef = z / φf,  Er = z / φr')

doc.add_paragraph('(3) 同步附着系数：')
add_formula(doc, 'φ0 = (L × β - b) / hg')

doc.add_paragraph('(4) 制动距离：')
add_formula(doc, 's = (τ1 + τ2/2) × ua0 / 3.6 + ua0² / (25.92 × a_bmax)')
doc.add_paragraph('式中，τ1=0.02s（制动系反应时间），τ2=0.02s（减速度上升时间）。')

doc.add_paragraph('(5) 最大制动减速度：')
add_formula(doc, 'a_bmax = E × φ × g  [m/s²]')

doc.add_heading('3.3 计算结果', level=2)

doc.add_paragraph('(1) 利用附着系数曲线和制动效率曲线如图5所示。')
if os.path.exists('fig5_adhesion_efficiency.png'):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.add_run().add_picture('fig5_adhesion_efficiency.png', width=Inches(5.8))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.add_run('图5  利用附着系数曲线与制动效率曲线').font.size = Pt(10)

doc.add_paragraph('(2) 同步附着系数：')
r6 = [
    ['空载', '-0.413'],
    ['满载', '0.428'],
]
add_result_table(doc, ['载荷状态', '同步附着系数 φ0'], r6)

doc.add_paragraph('(3) 制动距离（Ua=30km/h, φ=0.80）：')
r7 = [
    ['满载正常制动', '0.8715', '6.83 m/s²', '5.33 m'],
    ['空载正常制动', '0.6720', '5.27 m/s²', '6.84 m'],
    ['前部管路损坏（仅后轮）', '0.6038', '4.73 m/s²', '7.59 m'],
    ['后部管路损坏（仅前轮）', '0.3318', '2.60 m/s²', '13.60 m'],
]
add_result_table(doc, ['工况', '制动效率 E', '最大减速度', '制动距离 s'], r7)

doc.add_page_break()

# ============================================================
# 附录：编程程序代码
# ============================================================
doc.add_heading('附录：编程程序代码', level=1)

doc.add_heading('A.1 题目一：动力性能计算程序', level=2)
doc.add_paragraph(
    '文件名：part1_dynamic_performance.py'
    '  运行环境：conda run -n modeling python part1_dynamic_performance.py'
)
with open('part1_dynamic_performance.py', 'r', encoding='utf-8') as f:
    code1 = f.read()
add_code_block(doc, code1)

doc.add_page_break()

doc.add_heading('A.2 题目二：燃油经济性计算程序', level=2)
doc.add_paragraph(
    '文件名：part2_fuel_economy.py'
    '  运行环境：conda run -n modeling python part2_fuel_economy.py'
)
with open('part2_fuel_economy.py', 'r', encoding='utf-8') as f:
    code2 = f.read()
add_code_block(doc, code2)

doc.add_page_break()

doc.add_heading('A.3 题目三：制动性能计算程序', level=2)
doc.add_paragraph(
    '文件名：part3_braking_performance.py'
    '  运行环境：conda run -n modeling python part3_braking_performance.py'
)
with open('part3_braking_performance.py', 'r', encoding='utf-8') as f:
    code3 = f.read()
add_code_block(doc, code3)

# ============ 保存 ============
output_path = '课程设计报告.docx'
doc.save(output_path)
print(f'报告已保存：{output_path}')
