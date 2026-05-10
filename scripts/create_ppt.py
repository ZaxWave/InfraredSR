from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from PIL import Image
import os

prs = Presentation()
W = Inches(13.333)
H = Inches(7.5)
prs.slide_width = W
prs.slide_height = H

BLACK = RGBColor(0x00, 0x00, 0x00)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY = RGBColor(0x44, 0x44, 0x44)

BASE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(BASE, '_tmp_ppt')
os.makedirs(TMP, exist_ok=True)

FONT_NAME = 'Times New Roman'  # Academic serif font

def bg(slide):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = WHITE

def add_title(slide, text, top=Inches(0.35)):
    tb = slide.shapes.add_textbox(Inches(0.6), top, Inches(12), Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = BLACK
    p.font.name = FONT_NAME
    return tf

def add_body(slide, text, left, top, width, height, fontSize=16, color=BLACK):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, line_text in enumerate(text.strip().split('\n')):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line_text
        p.font.size = Pt(fontSize)
        p.font.color.rgb = color
        p.font.name = FONT_NAME
        p.space_after = Pt(6)
    return tf

def three_line_table(slide, data, left, top, col_widths, row_h=Inches(0.42), fontSize=14):
    rows = len(data)
    cols = len(data[0])
    tw = sum(col_widths)
    th = row_h * rows
    shape = slide.shapes.add_table(rows, cols, left, top, tw, th)
    tbl = shape.table

    for i, w in enumerate(col_widths):
        tbl.columns[i].width = w

    for r in range(rows):
        tbl.rows[r].height = row_h
        for c in range(cols):
            cell = tbl.cell(r, c)
            cell.text = str(data[r][c])
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            for para in cell.text_frame.paragraphs:
                para.font.size = Pt(fontSize)
                para.font.name = FONT_NAME
                para.font.color.rgb = BLACK
                para.font.bold = (r == 0)
                para.alignment = PP_ALIGN.CENTER
            # Remove default cell borders
            tcPr = cell._tc.get_or_add_tcPr()
            for edge in ('a:lnL', 'a:lnR', 'a:lnT', 'a:lnB',
                         'a:solidFill', 'a:noFill'):
                for child in list(tcPr):
                    if child.tag == qn(edge):
                        tcPr.remove(child)

    # Apply three-line borders: top thick (row 0), bottom-medium (row 0), bottom thick (last row)
    thick = {'w': 19000, 'color': '000000'}    # ~1.5pt
    medium = {'w': 9500, 'color': '000000'}    # ~0.75pt

    def set_border(cell, edge, spec):
        tcPr = cell._tc.get_or_add_tcPr()
        ln = cell._tc.makeelement(qn(f'a:{edge}'), {'w': str(spec['w'])})
        sf = cell._tc.makeelement(qn('a:solidFill'), {})
        sc = cell._tc.makeelement(qn('a:srgbClr'), {'val': spec['color']})
        sf.append(sc); ln.append(sf); tcPr.append(ln)

    for c in range(cols):
        set_border(tbl.cell(0, c), 'lnT', thick)
        set_border(tbl.cell(0, c), 'lnB', medium)
        set_border(tbl.cell(rows - 1, c), 'lnB', thick)

    return tbl

def convert_img(src, dst, size=None):
    try:
        im = Image.open(src)
        if size: im = im.resize(size, Image.LANCZOS)
        if im.mode in ('RGBA', 'P'): im = im.convert('RGB')
        if im.mode != 'RGB': im = im.convert('RGB')
        im.save(dst)
        return dst
    except:
        return None

# ============ SLIDE 1: 封面 ============
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s)
add_title(s, "InfraredSR 项目数据集介绍", top=Inches(2.8))
add_body(s, "红外遥感方向三个数据集：超分辨率重建、航拍车辆检测、跨传感器图像翻译",
         Inches(0.6), Inches(4.2), Inches(12), Inches(1.0), fontSize=18, color=GRAY)

# ============ SLIDE 2: 总览 ============
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s)
add_title(s, "数据集总览")

d = [
    ["数据集", "任务", "模态", "分辨率", "规模"],
    ["Infrared SR", "红外图像超分辨率\n(×2, ×4)", "红外热成像\n(单通道灰度)", "HR 640×512\nLR×2 320×256\nLR×4 160×128", "7,121 对\n训练 4,983\n验证 1,069\n测试 1,069"],
    ["VEDAI", "航拍车辆检测\n(8 类)", "可见光 RGB + 红外\n(双模态配对)", "512×512\n1024×1024", "1,246 张标注图像\n3,706 个目标框\n5 折交叉验证"],
    ["OLI2MSI", "跨传感器图像翻译\n(Landsat-8 → Sentinel-2)", "多光谱卫星遥感\n(GeoTIFF)", "LR: 30m\nHR: 10m", "5,325 对\n训练 5,225\n测试 100"],
]
three_line_table(s, d, Inches(0.6), Inches(1.5),
                 [Inches(2.0), Inches(2.6), Inches(2.6), Inches(2.8), Inches(2.6)],
                 row_h=Inches(1.1), fontSize=16)

# ============ SLIDE 3: Infrared SR ============
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s)
add_title(s, "Infrared SR — 红外图像超分辨率数据集")

info = (
    "• 任务：单帧红外图像超分辨率重建，包含 ×2 和 ×4 两种放大倍率\n"
    "• 格式：JPEG 灰度图像（8-bit 单通道），HR 与 LR 文件名一一对应\n"
    "• 目录结构：{trainsets, valsets, testsets} / {HR, LRx2, LRx4}\n"
    "• 分辨率：HR 640×512，LR×2 320×256，LR×4 160×128"
)
add_body(s, info, Inches(0.5), Inches(1.4), Inches(7.0), Inches(2.0), fontSize=16)

# Sample images
hr_p = os.path.join(BASE, 'datasets/Data/trainsets/HR/0002.jpg')
lr2_p = os.path.join(BASE, 'datasets/Data/trainsets/LRx2/0002.jpg')
lr4_p = os.path.join(BASE, 'datasets/Data/trainsets/LRx4/0002.jpg')

y_img = Inches(3.6)
x = Inches(0.8)
for label, src, w in [("HR 640×512", hr_p, Inches(3.0)), ("LR×2 320×256", lr2_p, Inches(1.5)), ("LR×4 160×128", lr4_p, Inches(0.75))]:
    dst = os.path.join(TMP, f'irsr_{label[:4]}.png')
    if convert_img(src, dst):
        s.shapes.add_picture(dst, x, y_img, width=w)
        add_body(s, label, x, y_img + w * 0.55, w, Inches(0.3), fontSize=12, color=GRAY)
    x += w + Inches(0.6)

# Table on the right
sd = [
    ["集合", "HR", "LR×2", "LR×4"],
    ["训练", "4,983", "4,983", "4,983"],
    ["验证", "1,069", "1,069", "1,069"],
    ["测试", "1,069", "1,069", "1,069"],
]
three_line_table(s, sd, Inches(8.5), Inches(1.4), [Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0)], fontSize=13)

add_body(s, "示例图像 0002.jpg：同一场景在三种分辨率下的对照", Inches(0.5), Inches(6.7), Inches(8), Inches(0.4), fontSize=13, color=GRAY)

# ============ SLIDE 4: VEDAI ============
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s)
add_title(s, "VEDAI — 航拍车辆检测数据集")

info = (
    "• 任务：航拍视角下的多类车辆目标检测，提供配对的可见光与红外图像\n"
    "• 格式：PNG 图像（*_co.png 为可见光，*_ir.png 为红外） + YOLO 格式 TXT 标注\n"
    "• 版本：VEDAI (512×512) 和 VEDAI_1024 (1024×1024)，标注文件 1,246 个\n"
    "• 划分：提供 5 折交叉验证文件（fold01~fold05.txt）\n"
    "• 标注格式：class_id  x_center  y_center  width  height（归一化坐标）"
)
add_body(s, info, Inches(0.5), Inches(1.4), Inches(12), Inches(2.2), fontSize=16)

# Sample images
co_p = os.path.join(BASE, 'datasets/dataset/VEDAI/images/00000000_co.png')
ir_p = os.path.join(BASE, 'datasets/dataset/VEDAI/images/00000000_ir.png')
d1 = os.path.join(TMP, 'vedai_co.png')
d2 = os.path.join(TMP, 'vedai_ir.png')

y2 = Inches(3.8)
if convert_img(co_p, d1, (320, 320)):
    s.shapes.add_picture(d1, Inches(1.0), y2, width=Inches(2.5))
    add_body(s, "可见光 RGB（00000000_co.png）", Inches(1.0), y2 + Inches(2.6), Inches(2.5), Inches(0.3), fontSize=12, color=GRAY)
if convert_img(ir_p, d2, (320, 320)):
    s.shapes.add_picture(d2, Inches(4.0), y2, width=Inches(2.5))
    add_body(s, "红外 IR（00000000_ir.png）", Inches(4.0), y2 + Inches(2.6), Inches(2.5), Inches(0.3), fontSize=12, color=GRAY)

# Class table on the right
cd = [
    ["类别", "轿车", "卡车", "皮卡", "拖拉机", "房车", "船", "摩托车", "其他"],
    ["数量", "955", "397", "307", "204", "190", "171", "105", "1,377"],
]
three_line_table(s, cd, Inches(7.2), Inches(3.8), [Inches(0.9), Inches(0.65), Inches(0.65), Inches(0.65), Inches(0.7), Inches(0.65), Inches(0.55), Inches(0.8), Inches(0.7)], fontSize=12)

# ============ SLIDE 5: OLI2MSI ============
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s)
add_title(s, "OLI2MSI — Landsat-8 → Sentinel-2 跨传感器图像翻译数据集")

info = (
    "• 任务：将 Landsat-8 OLI (30m) 图像翻译为 Sentinel-2 MSI (10m) 高质量图像\n"
    "    本质为带域迁移的超分辨率重建\n"
    "• 格式：GeoTIFF (.TIF) 多波段遥感图像\n"
    "• LR 输入：Landsat-8 OLI，30m 空间分辨率，单文件约 265 KB\n"
    "• HR 真值：Sentinel-2 MSI，10m 空间分辨率，单文件约 1.1 MB\n"
    "• 命名规则：L8_{场景ID}_{日期}_S2B_{日期}_T{瓦片号}_N{块号}.TIF\n"
    "    例：L8_126038_20190923_S2B_20190923_T49RBQ_N0008.TIF\n"
    "• 5 个地理场景，2019-09-23 同日采集，按网格切分为小图像块\n"
    "    场景 ID：126038, 126039, 126040, 126041, 126042"
)
add_body(s, info, Inches(0.5), Inches(1.4), Inches(8.2), Inches(4.8), fontSize=16)

od = [
    ["集合", "图像对数量", "场景数", "说  明"],
    ["训练集", "5,225", "5", "5 个场景按网格均匀分块"],
    ["测试集", "100", "5", "同一场景中取不重叠块"],
    ["合计", "5,325", "5", "Landsat-8 → Sentinel-2 一一配对"],
]
three_line_table(s, od, Inches(9.0), Inches(1.4), [Inches(1.2), Inches(1.4), Inches(1.0), Inches(3.2)], fontSize=14)

# ============ SLIDE 6: 总结 ============
s = prs.slides.add_slide(prs.slide_layouts[6])
bg(s)
add_title(s, "总结与对比")

sm = [
    ["", "Infrared SR", "VEDAI", "OLI2MSI"],
    ["任务", "单图超分辨率", "多类车辆目标检测", "跨传感器图像翻译"],
    ["模态", "红外热成像 (灰度)", "可见光 + 红外 (双模态)", "Landsat-8 + Sentinel-2 多光谱"],
    ["分辨率", "HR 640×512\nLR×4 160×128", "512×512 / 1024×1024", "LR 30m → HR 10m"],
    ["格式", "JPEG", "PNG + TXT (YOLO)", "GeoTIFF"],
    ["规模", "7,121 对图像", "1,246 张图 + 3,706 框", "5,325 对图像块"],
    ["划分", "预划分 train/val/test", "5 折交叉验证", "预划分 train/test"],
]
three_line_table(s, sm, Inches(0.5), Inches(1.5), [Inches(1.5), Inches(3.0), Inches(3.5), Inches(4.0)],
                 row_h=Inches(0.65), fontSize=14)

add_body(s, "三个数据集覆盖了红外遥感领域从像素级重建、目标检测到跨传感器增强的完整任务链。",
         Inches(0.5), Inches(6.5), Inches(12), Inches(0.4), fontSize=15, color=GRAY)

# Save
output = os.path.join(BASE, "InfraredSR_Datasets_Overview.pptx")
prs.save(output)
print(f"Done: {output}")
