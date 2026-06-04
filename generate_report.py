"""
生成汽车理论课程设计报告 DOCX
使用 python-docx + lxml XML方法确保中文字体正确
"""
import os
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
from lxml import etree

doc = Document()

# ============ XML工具函数 ============

def _set_rfonts(rPr, ascii_font, ea_font):
    """在<w:rPr>上设置w:rFonts（西文+东亚字体）"""
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = etree.SubElement(rPr, qn('w:rFonts'))
    rFonts.set(qn('w:ascii'), ascii_font)
    rFonts.set(qn('w:hAnsi'), ascii_font)
    rFonts.set(qn('w:eastAsia'), ea_font)
    rFonts.set(qn('w:cs'), ascii_font)

def _set_sz(rPr, pt):
    """在<w:rPr>上设置字号"""
    val = str(int(pt * 2))
    for tag in [qn('w:sz'), qn('w:szCs')]:
        el = rPr.find(tag)
        if el is None:
            el = etree.SubElement(rPr, tag)
        el.set(qn('w:val'), val)

def _set_b(rPr, bold):
    """在<w:rPr>上设置加粗"""
    b = rPr.find(qn('w:b'))
    if bold:
        if b is None:
            etree.SubElement(rPr, qn('w:b'))
    else:
        if b is not None:
            rPr.remove(b)

def ensure_rPr(parent_el):
    rPr = parent_el.find(qn('w:rPr'))
    if rPr is None:
        rPr = etree.SubElement(parent_el, qn('w:rPr'))
    return rPr

def style_font(style, ascii_font, ea_font, pt, bold=False):
    """设置样式级别的字体"""
    rPr = ensure_rPr(style.element)
    _set_rfonts(rPr, ascii_font, ea_font)
    _set_sz(rPr, pt)
    _set_b(rPr, bold)

def run_font(run, ascii_font, ea_font, pt, bold=False):
    """设置run级别的字体（正确设置w:ascii和w:eastAsia）"""
    rPr = ensure_rPr(run._r)
    _set_rfonts(rPr, ascii_font, ea_font)
    _set_sz(rPr, pt)
    _set_b(rPr, bold)

# ============ 页面设置 A4 ============
for section in doc.sections:
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.18)
    section.right_margin = Cm(3.18)

# ============ 样式定义（XML方法） ============
style_font(doc.styles['Normal'], 'Times New Roman', '宋体', 12)
style_font(doc.styles['Heading 1'], 'Times New Roman', '黑体', 14, bold=True)
style_font(doc.styles['Heading 2'], 'Times New Roman', '宋体', 12, bold=True)
style_font(doc.styles['Heading 3'], 'Times New Roman', '宋体', 12, bold=True)

# ============ 辅助函数 ============

def add_p(text, ascii='Times New Roman', ea='宋体', pt=12, bold=False, align=None):
    """添加段落，自动设置中西文字体"""
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    run = p.add_run(text)
    run_font(run, ascii, ea, pt, bold)
    return p

def add_formula_p(formula_text):
    """添加公式段落（居中、斜体）"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(formula_text)
    run.italic = True
    run_font(run, 'Times New Roman', '宋体', 11)
    return p

def add_code_block(code_text, title=None):
    """添加代码块"""
    if title:
        add_p(title, ea='黑体', pt=11, bold=True)

    for line in code_text.strip().split('\n'):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = Pt(14)
        run = p.add_run(line)
        run_font(run, 'Consolas', '宋体', 8)

def add_result_table(headers, rows):
    """添加结果表格"""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    for j, h in enumerate(headers):
        cell = table.rows[0].cells[j]
        cell.text = h
        for p in cell.paragraphs:
            for run in p.runs:
                run.bold = True
                run_font(run, 'Times New Roman', '宋体', 10)
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="D9E2F3"/>')
        cell._tc.get_or_add_tcPr().append(shading)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = table.rows[i + 1].cells[j]
            cell.text = str(val)
            for p in cell.paragraphs:
                for run in p.runs:
                    run_font(run, 'Times New Roman', '宋体', 10)
    doc.add_paragraph()
    return table


# ============================================================
# 封面
# ============================================================
for _ in range(4):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('汽车理论课程设计')
run_font(r, 'Times New Roman', '黑体', 26, bold=True)

doc.add_paragraph()

for line in ['专业名称：车辆工程', '班    级：2023370501',
             '学    号：2023901021', '学生姓名：李思成']:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(line)
    run_font(r, 'Times New Roman', '宋体', 14)

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('2026 年 6 月 1 日')
run_font(r, 'Times New Roman', '宋体', 14)

doc.add_page_break()

# ============================================================
# 目录
# ============================================================
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('目  录')
run_font(r, 'Times New Roman', '黑体', 18, bold=True)

# TOC field
p_toc = doc.add_paragraph()
for xml_str, text_val in [
    ('begin', None), ('instrText', ' TOC \\o "1-3" \\h \\z '),
    ('separate', None), ('text', '[请在Word中右键点击此处，选择"更新域"以生成目录]'),
    ('end', None),
]:
    if xml_str == 'text':
        r = p_toc.add_run(text_val)
        run_font(r, 'Times New Roman', '宋体', 10)
        r.font.color.rgb = RGBColor(128, 128, 128)
    else:
        r = p_toc.add_run()
        el = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="{xml_str}"/>') if xml_str != 'instrText' \
            else parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve">{text_val}</w:instrText>')
        r._r.append(el)

doc.add_page_break()

# ============================================================
# 题目一：动力性能计算
# ============================================================
doc.add_heading('题目一：轻型货车动力性能计算（习题1.3）', level=1)

doc.add_heading('1.1 题目描述', level=2)
add_p('确定一轻型货车的动力性能（货车装用五档变速器）：')
add_p('(1) 绘制汽车驱动力与行驶阻力平衡图。')
add_p('(2) 求汽车最高车速、最大爬坡度及克服该坡度时相应的附着率。')
add_p('(3) 绘制汽车行驶加速度倒数曲线，用计算机求汽车用2档起步加速行驶至70km/h的加速时间。')

doc.add_heading('1.2 已知参数', level=2)
add_result_table(['参数', '数值'], [
    ['装载质量', '2000 kg'], ['整车整备质量', '1800 kg'],
    ['总质量', '3880 kg'], ['车轮半径', '0.367 m'],
    ['传动系机械效率 ηt', '0.85'], ['滚动阻力系数 f', '0.013'],
    ['空气阻力系数×迎风面积 CDA', '2.77 m²'], ['主减速器传动比 i0', '5.83'],
    ['飞轮转动惯量 If', '0.218 kg·m²'], ['二前轮转动惯量 Iw1', '1.798 kg·m²'],
    ['四后轮转动惯量 Iw2', '3.598 kg·m²'], ['轴距 L', '3.2 m'],
    ['质心至前轴距离（满载）a', '1.947 m'], ['质心高（满载）hg', '0.9 m'],
])

doc.add_heading('1.3 变速器传动比（五档）', level=2)
add_result_table(['档位', '1档', '2档', '3档', '4档', '5档'],
                  [['传动比 ig', '5.56', '2.769', '1.644', '1.00', '0.793']])

doc.add_heading('1.4 计算公式', level=2)
add_p('(1) 发动机外特性转矩拟合公式（Tq-n曲线）：')
add_formula_p('Tq = -19.313 + 295.27(n/1000) - 165.44(n/1000)² + 40.874(n/1000)³ - 3.8445(n/1000)⁴')
add_p('(2) 各档车速：')
add_formula_p('ua = 0.377 × r × n / (ig × i0)  [km/h]')
add_p('(3) 各档驱动力：')
add_formula_p('Ft = Tq × ig × i0 × ηt / r  [N]')
add_p('(4) 行驶阻力：')
add_formula_p('Ff + Fw = G × f + CDA × ua² / 21.15  [N]')
add_p('(5) 旋转质量换算系数：')
add_formula_p('δ = 1 + (ΣIw + If × ig² × i0² × ηt) / (m × r²)')
add_p('(6) 加速度：')
add_formula_p('a = (Ft - Ff - Fw) / (δ × m)  [m/s²]')
add_p('(7) 加速时间（图解积分法）：')
add_formula_p('t = ∫(1/a) du = (1/3.6) × ∫(1/a) dua  [s]')

doc.add_heading('1.5 计算结果', level=2)
add_p('(1) 驱动力-行驶阻力平衡图如图1所示。')

if os.path.exists('fig1_driving_resistance_balance.png'):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture('fig1_driving_resistance_balance.png', width=Inches(5.5))
    add_p('图1  汽车驱动力-行驶阻力平衡图', pt=10, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

add_p('(2) 最高车速与最大爬坡度：')
add_result_table(['项目', '结果'], [
    ['最高车速 ua_max', '99.08 km/h'],
    ['发动机最大转矩 Tq_max', '174.97 N·m @ 2044 r/min'],
    ['发动机最大功率 Pe_max', '61.73 kW @ 3864 r/min'],
    ['最大爬坡度 i', '35.02% (19.30°)'],
    ['最大爬坡度对应车速', '10.01 km/h'],
    ['最大爬坡度时附着率 Cφ2', '0.4348'],
])

add_p('(3) 加速度倒数曲线与加速时间：')
if os.path.exists('fig2_acceleration_curves.png'):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture('fig2_acceleration_curves.png', width=Inches(5.8))
    add_p('图2  各档加速度曲线与2档加速度倒数曲线', pt=10, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

add_result_table(['项目', '时间'], [
    ['2档加速段时间', '6.34 s'], ['换挡时间', '0.80 s'],
    ['3档加速段时间', '9.15 s'], ['2档起步加速至70km/h总时间', '16.29 s'],
])
doc.add_page_break()

# ============================================================
# 题目二：燃油经济性计算
# ============================================================
doc.add_heading('题目二：轻型货车燃油经济性计算（习题2.7）', level=1)

doc.add_heading('2.1 题目描述', level=2)
add_p('货车的参数与题目一相同。负荷特性曲线的拟合公式为：')
add_formula_p('b = B0 + B1·Pe + B2·Pe² + B3·Pe³ + B4·Pe⁴')
add_p('式中，b为燃油消耗率[g/(kW·h)]，Pe为发动机净功率(kW)。')
add_p('(1) 绘制该轻型货车的功率平衡图。')
add_p('(2) 绘制最高挡与次高挡的等速百公里油耗曲线。')
add_p('(3) 计算六工况循环行驶的百公里油耗。')

doc.add_heading('2.2 负荷特性拟合系数', level=2)
add_result_table(['n (r/min)', 'B0', 'B1', 'B2', 'B3', 'B4'], [
    ['815', '1326.8', '-416.46', '72.379', '-5.8629', '0.17768'],
    ['1207', '1354.7', '-303.98', '36.657', '-2.0553', '0.043072'],
    ['1614', '1284.4', '-189.75', '14.524', '-0.51184', '0.0068164'],
    ['2012', '1122.9', '-121.59', '7.0035', '-0.18517', '0.0018555'],
    ['2603', '1141.0', '-98.893', '4.4763', '-0.091077', '0.00068906'],
    ['3006', '1051.2', '-73.714', '2.8593', '-0.05138', '0.00035032'],
    ['3403', '1233.9', '-84.478', '2.9788', '-0.047449', '0.00028230'],
    ['3804', '1129.7', '-45.291', '0.71113', '-0.00075215', '-0.000038568'],
])

doc.add_heading('2.3 计算公式', level=2)
add_p('(1) 发动机功率：')
add_formula_p('Pe = Tq × n / 9550  [kW]')
add_p('(2) 阻力功率：')
add_formula_p('Pf = (Ff + Fw) × ua / (3600 × ηt)  [kW]')
add_p('(3) 等速百公里油耗：')
add_formula_p('Qs = Pe × b / (1.02 × ua × γ)  [L/100km]')
add_p('式中，γ为燃油重度，93#汽油 γ = ρg = 0.715×9.8 = 7.007 N/L。')
add_p('(4) 瞬时燃油消耗量：')
add_formula_p('Qt = Pe × b / (3600 × ρ)  [mL/s]')

doc.add_heading('2.4 计算结果', level=2)

add_p('(1) 功率平衡图如图3所示。')
if os.path.exists('fig3_power_balance.png'):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture('fig3_power_balance.png', width=Inches(5.5))
    add_p('图3  汽车功率平衡图', pt=10, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

add_p('(2) 等速百公里油耗曲线如图4所示。')
if os.path.exists('fig4_constant_speed_fuel.png'):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture('fig4_constant_speed_fuel.png', width=Inches(5.0))
    add_p('图4  最高档与次高档等速百公里油耗曲线', pt=10, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

add_p('(3) 等速百公里油耗特征值：')
add_result_table(['项目', '油耗'], [
    ['5档（最高档）最低油耗', '11.99 L/100km @ 30 km/h'],
    ['5档 60km/h等速油耗', '13.84 L/100km'],
    ['5档 80km/h等速油耗', '17.96 L/100km'],
    ['4档（次高档）最低油耗', '13.35 L/100km @ 30 km/h'],
    ['4档 60km/h等速油耗', '15.04 L/100km'],
    ['4档 80km/h等速油耗', '19.22 L/100km'],
])

add_p('(4) 六工况循环百公里油耗：')
add_result_table(['工况', '油耗'], [
    ['工况I（等速25km/h，7.2s）', '6.02 mL'],
    ['工况II（25→40km/h加速，16.7s）', '24.26 mL'],
    ['工况III（等速40km/h，22.5s）', '31.07 mL'],
    ['工况IV（40→50km/h加速，14.0s）', '23.24 mL'],
    ['工况V（等速50km/h，18.0s）', '32.25 mL'],
    ['工况VI（50→25km/h减速，19.3s）', '24.87 mL'],
    ['总油耗 / 总行程', '141.70 mL / 1075 m'],
    ['六工况百公里油耗', '13.18 L/100km'],
])
doc.add_page_break()

# ============================================================
# 题目三：制动性能计算
# ============================================================
doc.add_heading('题目三：中型货车制动性能计算（习题4.3）', level=1)

doc.add_heading('3.1 题目描述', level=2)
add_p('一中型货车装有前后制动器分开的双管路制动系，有关参数如下表所示：')
add_result_table(['载荷', '质量(kg)', '质心高hg/m', '轴距L/m', '质心至前轴a/m', '分配系数β'], [
    ['空载', '4080', '0.845', '3.950', '2.100', '0.38'],
    ['满载', '9290', '1.170', '3.950', '2.950', '0.38'],
])
add_p('(1) 计算并绘制利用附着系数曲线和制动效率曲线。')
add_p('(2) 求行驶车速Ua=30km/h，在φ=0.80路面上车轮不抱死的制动距离。')
add_p('(3) 求制动系前部/后部管路损坏时的制动距离。')

doc.add_heading('3.2 计算公式', level=2)
add_p('(1) 利用附着系数：')
add_formula_p('φf = β × z × L / (b + z × hg)')
add_formula_p('φr = (1-β) × z × L / (a - z × hg)')
add_p('式中，z为制动强度，b = L - a为质心至后轴距离。')
add_p('(2) 制动效率：')
add_formula_p('Ef = z / φf,  Er = z / φr')
add_p('(3) 同步附着系数：')
add_formula_p('φ0 = (L × β - b) / hg')
add_p('(4) 制动距离：')
add_formula_p('s = (τ1 + τ2/2) × ua0 / 3.6 + ua0² / (25.92 × a_bmax)')
add_p('式中，τ1=0.02s（制动系反应时间），τ2=0.02s（减速度上升时间）。')
add_p('(5) 最大制动减速度：')
add_formula_p('a_bmax = E × φ × g  [m/s²]')

doc.add_heading('3.3 计算结果', level=2)

add_p('(1) 利用附着系数曲线和制动效率曲线如图5所示。')
if os.path.exists('fig5_adhesion_efficiency.png'):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture('fig5_adhesion_efficiency.png', width=Inches(5.8))
    add_p('图5  利用附着系数曲线与制动效率曲线', pt=10, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)

add_p('(2) 同步附着系数：')
add_result_table(['载荷状态', '同步附着系数 φ0'], [['空载', '-0.413'], ['满载', '0.428']])

add_p('(3) 制动距离（Ua=30km/h, φ=0.80）：')
add_result_table(['工况', '制动效率 E', '最大减速度', '制动距离 s'], [
    ['满载正常制动', '0.8715', '6.83 m/s²', '5.33 m'],
    ['空载正常制动', '0.6720', '5.27 m/s²', '6.84 m'],
    ['前部管路损坏（仅后轮）', '0.6038', '4.73 m/s²', '7.59 m'],
    ['后部管路损坏（仅前轮）', '0.3318', '2.60 m/s²', '13.60 m'],
])
doc.add_page_break()

# ============================================================
# 附录：编程程序代码
# ============================================================
doc.add_heading('附录：编程程序代码', level=1)

for label, filename in [
    ('A.1 题目一：动力性能计算程序', 'part1_dynamic_performance.py'),
    ('A.2 题目二：燃油经济性计算程序', 'part2_fuel_economy.py'),
    ('A.3 题目三：制动性能计算程序', 'part3_braking_performance.py'),
]:
    doc.add_heading(label, level=2)
    add_p(f'文件名：{filename}    运行环境：conda run -n modeling python {filename}')
    with open(filename, 'r', encoding='utf-8') as f:
        add_code_block(f.read())
    if label != 'A.3 题目三：制动性能计算程序':
        doc.add_page_break()

# ============ 保存 ============
output_path = '课程设计报告.docx'
doc.save(output_path)
print(f'报告已保存：{output_path}')
