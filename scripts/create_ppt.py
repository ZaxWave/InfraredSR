from pptx import Presentation
from pptx.util import Inches, Pt, Emu
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
GRAY  = RGBColor(0x55, 0x55, 0x55)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP  = os.path.join(BASE, '_tmp_ppt')
os.makedirs(TMP, exist_ok=True)
OUT  = os.path.join(BASE, 'ppts', 'InfraredSR_Datasets_Overview.pptx')

FONT_NAME = 'Times New Roman'
ML = Inches(0.9)   # left margin
MR = Inches(0.9)   # right margin equivalent
MW = Inches(11.5)  # max usable width

def bg(slide):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = WHITE

def add_title(slide, text, top=Inches(0.3)):
    tb = slide.shapes.add_textbox(ML, top, MW, Inches(0.65))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text; p.font.size = Pt(28); p.font.bold = True
    p.font.color.rgb = BLACK; p.font.name = FONT_NAME

def add_body(slide, text, left, top, width, height, fontSize=15, color=BLACK):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame; tf.word_wrap = True
    for i, line in enumerate(text.strip().split('\n')):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line; p.font.size = Pt(fontSize); p.font.color.rgb = color
        p.font.name = FONT_NAME; p.space_after = Pt(4)

def three_line_table(slide, data, left, top, col_widths, row_h=Inches(0.38), fontSize=12):
    rows, cols = len(data), len(data[0])
    tw = sum(col_widths)
    shape = slide.shapes.add_table(rows, cols, left, top, tw, row_h * rows)
    tbl = shape.table
    for i, w in enumerate(col_widths): tbl.columns[i].width = w
    for r in range(rows):
        tbl.rows[r].height = row_h
        for c in range(cols):
            cell = tbl.cell(r, c)
            cell.text = str(data[r][c])
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            for para in cell.text_frame.paragraphs:
                para.font.size = Pt(fontSize); para.font.name = FONT_NAME
                para.font.color.rgb = BLACK; para.font.bold = (r == 0)
                para.alignment = PP_ALIGN.CENTER
            tcPr = cell._tc.get_or_add_tcPr()
            for e in ('a:lnL','a:lnR','a:lnT','a:lnB','a:solidFill','a:noFill'):
                for ch in list(tcPr):
                    if ch.tag == qn(e): tcPr.remove(ch)

    thick  = {'w': 19000, 'color': '000000'}
    medium = {'w':  9500, 'color': '000000'}
    def sb(cell, edge, spec):
        tcPr = cell._tc.get_or_add_tcPr()
        ln = cell._tc.makeelement(qn(f'a:{edge}'), {'w': str(spec['w'])})
        sf = cell._tc.makeelement(qn('a:solidFill'), {})
        sc = cell._tc.makeelement(qn('a:srgbClr'), {'val': spec['color']})
        sf.append(sc); ln.append(sf); tcPr.append(ln)
    for c in range(cols):
        sb(tbl.cell(0, c), 'lnT', thick)
        sb(tbl.cell(0, c), 'lnB', medium)
        sb(tbl.cell(rows-1, c), 'lnB', thick)
    return tbl

def convert_img(src, dst, size=None):
    """Convert image to compatible format. Returns (path, w_px, h_px) or (None,0,0)."""
    try:
        im = Image.open(src)
        if size: im = im.resize(size, Image.LANCZOS)
        if im.mode in ('RGBA','P'): im = im.convert('RGB')
        if im.mode != 'RGB': im = im.convert('RGB')
        im.save(dst)
        return dst, im.width, im.height
    except:
        return None, 0, 0

def add_image_with_label(slide, src_path, left, top, width, label, label_fontsize=11):
    """Add image and place label below it (calculated from actual image height)."""
    dst = os.path.join(TMP, f'img_{abs(hash(src_path))}.png')
    path, pw, ph = convert_img(src_path, dst)
    if not path:
        return
    # Calculate actual display height from aspect ratio
    display_h = width * ph / pw
    slide.shapes.add_picture(path, left, top, width=width)
    label_y = top + display_h + Inches(0.08)
    add_body(slide, label, left, label_y, width, Inches(0.25), fontSize=label_fontsize, color=GRAY)

def center_table(total_width, max_width=MW):
    """Return left position to center a table of total_width."""
    return ML + (MW - total_width) / 2

# ==================== SLIDE 1: 封面 ====================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
add_title(s, "InfraredSR 项目数据集介绍", top=Inches(2.6))
add_body(s, "红外遥感方向五个数据集\n超分辨率重建 · 航拍车辆检测 · 跨传感器图像翻译 · 跨光谱配准 · 可见光引导超分",
         ML, Inches(4.0), MW, Inches(1.2), fontSize=18, color=GRAY)

# ==================== SLIDE 2: 总览 ====================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
add_title(s, "数据集总览")

d = [
    ["数据集", "任务", "模态", "分辨率 / 尺度", "规模"],
    ["Infrared SR", "红外图像超分辨率 (×2, ×4)", "红外热成像\n(单通道灰度)", "HR 640×512\nLR×2 320×256 / LR×4 160×128", "7,121 对\n训练 4,983 / 验证 1,069 / 测试 1,069"],
    ["VEDAI", "航拍车辆检测 (8 类)", "可见光 RGB + 红外\n(双模态配对)", "512×512 / 1024×1024", "1,246 张\n3,706 目标框 / 5 折交叉验证"],
    ["OLI2MSI", "跨传感器图像翻译\n(Landsat-8 → Sentinel-2)", "多光谱卫星遥感\n(GeoTIFF)", "LR 30m → HR 10m", "5,325 对\n训练 5,225 / 测试 100"],
    ["CIDIS", "跨光谱图像配准\n(热红外 ↔ 可见光)", "热红外 + 可见光\n(配对)", "640×448", "1,000 对\n训练 700 / 验证 200 / 测试 100"],
    ["CIDIS_guided", "可见光引导红外超分\n(×8, ×16)", "热红外 + 可见光引导\n(配对)", "GT 640×448\nLR×8 80×56 / LR×16 40×28", "训练 700 / 验证 200\n测试 40 (×8 + ×16)"],
]
cw = [Inches(1.6), Inches(2.4), Inches(2.2), Inches(2.6), Inches(2.7)]
three_line_table(s, d, center_table(sum(cw)), Inches(1.3), cw, row_h=Inches(0.82), fontSize=12)

# ==================== SLIDE 3: Infrared SR ====================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
add_title(s, "Infrared SR — 红外图像超分辨率数据集")

info = (
    "• 任务：单帧红外图像超分辨率重建 (×2, ×4)\n"
    "• 格式：JPEG 灰度图像 (8-bit)，HR 与 LR 文件名一一对应\n"
    "• 分辨率：HR 640×512，LR×2 320×256，LR×4 160×128\n"
    "• 目录：{trainsets, valsets, testsets} / {HR, LRx2, LRx4}"
)
add_body(s, info, ML, Inches(1.3), Inches(7.5), Inches(1.6), fontSize=15)

hr_p  = os.path.join(BASE, 'datasets/Data/trainsets/HR/0002.jpg')
lr2_p = os.path.join(BASE, 'datasets/Data/trainsets/LRx2/0002.jpg')
lr4_p = os.path.join(BASE, 'datasets/Data/trainsets/LRx4/0002.jpg')

y_img = Inches(3.2)
x = ML
add_image_with_label(s, hr_p,  x, y_img, Inches(3.0), "HR 640×512")
x += Inches(3.5)
add_image_with_label(s, lr2_p, x, y_img, Inches(1.5), "LR×2 320×256")
x += Inches(2.0)
add_image_with_label(s, lr4_p, x, y_img, Inches(0.75), "LR×4 160×128")

sd = [["集合", "HR", "LR×2", "LR×4"],
      ["训练", "4,983", "4,983", "4,983"],
      ["验证", "1,069", "1,069", "1,069"],
      ["测试", "1,069", "1,069", "1,069"]]
cw3 = [Inches(1.2), Inches(1.3), Inches(1.3), Inches(1.3)]
three_line_table(s, sd, center_table(sum(cw3)), Inches(6.2), cw3, fontSize=13)

# ==================== SLIDE 4: VEDAI ====================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
add_title(s, "VEDAI — 航拍车辆检测数据集")

info = (
    "• 任务：航拍视角多类车辆目标检测，提供配对可见光与红外图像\n"
    "• 格式：PNG 图像 (*_co.png 可见光, *_ir.png 红外) + YOLO 标注\n"
    "• 版本：VEDAI (512×512) 和 VEDAI_1024 (1024×1024)\n"
    "• 划分：5 折交叉验证 (fold01~fold05.txt)，1,246 张标注图"
)
add_body(s, info, ML, Inches(1.3), Inches(7.0), Inches(1.8), fontSize=15)

co_p = os.path.join(BASE, 'datasets/dataset/VEDAI/images/00000000_co.png')
ir_p = os.path.join(BASE, 'datasets/dataset/VEDAI/images/00000000_ir.png')

y2 = Inches(3.3)
add_image_with_label(s, co_p, Inches(1.2), y2, Inches(2.5), "可见光 RGB (00000000_co.png)")
add_image_with_label(s, ir_p, Inches(4.2), y2, Inches(2.5), "红外 IR (00000000_ir.png)")

cd = [["类别", "轿车", "卡车", "皮卡", "拖拉机", "房车", "船", "其他"],
      ["数量", "955", "397", "307", "204", "190", "171", "1,377"]]
cw4 = [Inches(1.2), Inches(0.85), Inches(0.85), Inches(0.85), Inches(0.85), Inches(0.85), Inches(0.85), Inches(0.85)]
three_line_table(s, cd, center_table(sum(cw4)), Inches(5.8), cw4, fontSize=13)

# ==================== SLIDE 5: OLI2MSI ====================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
add_title(s, "OLI2MSI — Landsat-8 → Sentinel-2 跨传感器图像翻译")

info = (
    "• 任务：Landsat-8 OLI (30m) 翻译为 Sentinel-2 MSI (10m)，带域迁移的超分重建\n"
    "• 格式：GeoTIFF (.TIF) 多波段遥感图像\n"
    "• LR 输入：Landsat-8 OLI, 30m, 单文件约 265 KB\n"
    "• HR 真值：Sentinel-2 MSI, 10m, 单文件约 1.1 MB\n"
    "• 5 个地理场景 (ID: 126038~126042)，2019-09-23 同日采集，网格切分\n"
    "• 命名：L8_{场景ID}_{日期}_S2B_{日期}_T{瓦片号}_N{块号}.TIF"
)
add_body(s, info, ML, Inches(1.2), Inches(7.0), Inches(3.0), fontSize=15)

od = [["集合", "图像对", "场景数", "说明"],
      ["训练", "5,225", "5", "5 个场景按网格均匀分块"],
      ["测试", "100", "5", "同一场景中取不重叠块"],
      ["合计", "5,325", "5", "Landsat-8 → Sentinel-2 一一配对"]]
cw5 = [Inches(1.2), Inches(1.2), Inches(1.0), Inches(3.5)]
three_line_table(s, od, center_table(sum(cw5)), Inches(4.5), cw5, fontSize=13)

# ==================== SLIDE 6: CIDIS ====================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
add_title(s, "CIDIS — 跨光谱图像配准数据集")

info = (
    "• 任务：热红外与可见光图像的跨光谱特征匹配与配准\n"
    "• 来源：Rivadeneira et al., 2024, Cross-Spectral Image Registration\n"
    "• 格式：热红外 + 可见光配对图像，均为 640×448\n"
    "• 共 1,000 对：训练 700 / 验证 200 / 测试 100\n"
    "• 目录：{thermal, visible} / {train, val, test}"
)
add_body(s, info, ML, Inches(1.3), Inches(7.5), Inches(2.2), fontSize=15)

cidis_th = os.path.join(BASE, 'datasets/CIDIS-dataset-main/dataset/thermal/train')
cidis_vi = os.path.join(BASE, 'datasets/CIDIS-dataset-main/dataset/visible/train')
th_files = sorted(os.listdir(cidis_th)) if os.path.isdir(cidis_th) else []
vi_files = sorted(os.listdir(cidis_vi)) if os.path.isdir(cidis_vi) else []

y3 = Inches(3.6)
if th_files:
    add_image_with_label(s, os.path.join(cidis_th, th_files[0]), Inches(1.5), y3, Inches(2.5), "热红外示例")
if vi_files:
    add_image_with_label(s, os.path.join(cidis_vi, vi_files[0]), Inches(4.5), y3, Inches(2.5), "可见光示例")

cd_cidis = [["集合", "热红外", "可见光", "总计"],
            ["训练", "700", "700", "700 对"],
            ["验证", "200", "200", "200 对"],
            ["测试", "100", "100", "100 对"]]
cw6 = [Inches(1.2)] * 4
three_line_table(s, cd_cidis, center_table(sum(cw6)), Inches(6.2), cw6, fontSize=13)

# ==================== SLIDE 7: CIDIS_guided ====================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
add_title(s, "CIDIS_guided_x8x16 — 可见光引导红外超分辨率数据集")

info = (
    "• 任务：以可见光为引导，对热红外图像进行 ×8 和 ×16 超分辨率重建\n"
    "• 基于 CIDIS 构建，合成退化生成 LR；GT 640×448, LR×8 80×56, LR×16 40×28\n"
    "• 可见光引导图 640×448 (提供高频纹理引导)\n"
    "• 训练 700 对 / 验证 200 对 / 测试 40 对 (×8 和 ×16 各 40 张)"
)
add_body(s, info, ML, Inches(1.2), Inches(7.5), Inches(1.8), fontSize=15)

th_gt_dir  = os.path.join(BASE, 'datasets/dataset_CIDIS_guided_x8x16/thermal/train/GT')
th_lr8_dir = os.path.join(BASE, 'datasets/dataset_CIDIS_guided_x8x16/thermal/train/LR_x8')
th_lr16_dir= os.path.join(BASE, 'datasets/dataset_CIDIS_guided_x8x16/thermal/train/LR_x16')
vis_dir    = os.path.join(BASE, 'datasets/dataset_CIDIS_guided_x8x16/visible/train')

gt_files  = sorted(os.listdir(th_gt_dir)) if os.path.isdir(th_gt_dir) else []
lr8_files = sorted(os.listdir(th_lr8_dir)) if os.path.isdir(th_lr8_dir) else []
lr16_files= sorted(os.listdir(th_lr16_dir)) if os.path.isdir(th_lr16_dir) else []
vis_files = sorted(os.listdir(vis_dir)) if os.path.isdir(vis_dir) else []

y4 = Inches(3.3)
if gt_files:
    add_image_with_label(s, os.path.join(th_gt_dir, gt_files[0]), Inches(0.9), y4, Inches(2.2), "GT 640×448", 10)
if vis_files:
    add_image_with_label(s, os.path.join(vis_dir, vis_files[0]), Inches(3.4), y4, Inches(2.2), "可见光引导 640×448", 10)
if lr8_files:
    add_image_with_label(s, os.path.join(th_lr8_dir, lr8_files[0]), Inches(5.9), Inches(3.3), Inches(0.7), "LR×8\n80×56", 10)
if lr16_files:
    add_image_with_label(s, os.path.join(th_lr16_dir, lr16_files[0]), Inches(7.0), Inches(3.3), Inches(0.35), "LR×16\n40×28", 10)

cd_cg = [["集合", "热红外 (GT/LR×8/LR×16)", "可见光引导", "分辨率"],
         ["训练", "700×3 = 2,100", "700", "640×448 → 80×56 / 40×28"],
         ["验证", "200×3 = 600", "200", ""],
         ["测试", "40×2 = 80", "40", "×8 / ×16 各 40 张"]]
cw7 = [Inches(1.2), Inches(2.8), Inches(1.8), Inches(2.5)]
three_line_table(s, cd_cg, center_table(sum(cw7)), Inches(5.5), cw7, fontSize=12)

# ==================== SLIDE 8: 总结 ====================
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s)
add_title(s, "总结与对比")

sm = [
    ["", "Infrared SR", "VEDAI", "OLI2MSI", "CIDIS", "CIDIS_guided"],
    ["任务", "单图超分辨率", "车辆目标检测", "跨传感器翻译", "跨光谱配准", "引导式超分"],
    ["模态", "红外热成像", "RGB + IR", "L8 + S2 多光谱", "热红外 + 可见光", "热红外 + 可见光"],
    ["分辨率", "HR 640×512\nLR×4 160×128", "512 / 1024", "LR 30m → HR 10m", "640×448", "GT 640×448\nLR×16 40×28"],
    ["格式", "JPEG", "PNG + TXT", "GeoTIFF", "图像文件", "图像文件"],
    ["规模", "7,121 对", "1,246 张 / 3,706 框", "5,325 对", "1,000 对", "940 对"],
    ["划分", "train/val/test", "5 折交叉验证", "train/test", "train/val/test", "train/val/test"],
]
cw8 = [Inches(1.2), Inches(1.9), Inches(2.0), Inches(2.0), Inches(2.0), Inches(2.2)]
three_line_table(s, sm, center_table(sum(cw8)), Inches(1.4), cw8, row_h=Inches(0.58), fontSize=11)

add_body(s, "五个数据集覆盖红外遥感领域从像素级重建、目标检测、跨传感器增强、跨光谱配准到引导式超分的完整任务链。",
         ML, Inches(6.5), MW, Inches(0.4), fontSize=15, color=GRAY)

# ==================== Save ====================
prs.save(OUT)
print(f"Done: {OUT}")
