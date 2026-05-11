from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.units import cm, mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, PageBreak, HRFlowable)
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import KeepTogether
import os

# --- Output ---
BASE = os.path.dirname(os.path.abspath(__file__))
output = os.path.join(BASE, "阅读报告_Image_Generation_Models.pdf")

# --- Try to register Chinese font ---
font_registered = False
for font_path, font_name in [
    ("C:/Windows/Fonts/simsun.ttc", "SimSun"),
    ("C:/Windows/Fonts/simhei.ttf", "SimHei"),
    ("C:/Windows/Fonts/msyh.ttc", "MSYH"),
    ("C:/Windows/Fonts/msyhbd.ttc", "MSYHBD"),
]:
    if os.path.exists(font_path):
        try:
            pdfmetrics.registerFont(TTFont(font_name, font_path))
            font_registered = True
        except:
            pass

CN_FONT = "SimSun" if font_registered else "Helvetica"
CN_BOLD = "SimHei" if font_registered else "Helvetica-Bold"
print(f"Using font: {CN_FONT}")

# --- Page Setup ---
W, H = A4  # 210 x 297 mm

doc = SimpleDocTemplate(
    output, pagesize=A4,
    leftMargin=2.5*cm, rightMargin=2.0*cm,
    topMargin=2.0*cm, bottomMargin=2.0*cm,
    title="阅读报告 - Image Generation Models: A Technical History",
    author="钟兴炜"
)

# --- Styles ---
styles = getSampleStyleSheet()

title_style = ParagraphStyle('CNTitle', parent=styles['Title'],
    fontName=CN_BOLD, fontSize=16, leading=22,
    alignment=TA_CENTER, spaceAfter=4*mm)

subtitle_style = ParagraphStyle('CNSub', parent=styles['Normal'],
    fontName=CN_FONT, fontSize=10, leading=14,
    alignment=TA_CENTER, spaceAfter=3*mm, textColor=colors.grey)

h1_style = ParagraphStyle('CNH1', parent=styles['Heading1'],
    fontName=CN_BOLD, fontSize=13, leading=18,
    spaceBefore=8*mm, spaceAfter=3*mm)

h2_style = ParagraphStyle('CNH2', parent=styles['Heading2'],
    fontName=CN_BOLD, fontSize=11, leading=15,
    spaceBefore=5*mm, spaceAfter=2*mm)

em_cn = 10  # approximate Chinese em in pt at size 10 (must be defined before styles that use it)

body_style = ParagraphStyle('CNBody', parent=styles['Normal'],
    fontName=CN_FONT, fontSize=10, leading=16,
    alignment=TA_JUSTIFY, spaceAfter=1.5*mm,
    firstLineIndent=2*em_cn if font_registered else 0)

body_no_indent = ParagraphStyle('CNBodyNI', parent=body_style,
    firstLineIndent=0)

meta_style = ParagraphStyle('CNMeta', parent=styles['Normal'],
    fontName=CN_FONT, fontSize=9, leading=13,
    alignment=TA_LEFT, spaceAfter=1*mm)

bullet_style = ParagraphStyle('CNBullet', parent=body_style,
    firstLineIndent=0, leftIndent=8*mm, bulletIndent=3*mm)

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=colors.black)

def thin_hr():
    return HRFlowable(width="100%", thickness=0.3, color=colors.grey)

# ================================================================
# Build content
# ================================================================
story = []

# --- Title Block ---
story.append(Spacer(1, 1*cm))
story.append(Paragraph("阅读报告", title_style))
story.append(Spacer(1, 3*mm))
story.append(Paragraph(
    "<b>Image Generation Models: A Technical History</b>",
    ParagraphStyle('PaperTitle', parent=title_style, fontSize=13, leading=18)))
story.append(Spacer(1, 2*mm))
story.append(Paragraph("Rouzbeh Shirvani  ·  arXiv: 2603.07455v2  ·  2026 年 3 月", subtitle_style))
story.append(Spacer(1, 5*mm))

# Author info
story.append(Paragraph("钟兴炜  ·  chungxw@whu.edu.cn", meta_style))
story.append(Paragraph("武汉大学", meta_style))
story.append(Spacer(1, 3*mm))
story.append(hr())
story.append(Spacer(1, 4*mm))

# --- Section 1: Overview ---
story.append(Paragraph("一、论文概况", h1_style))
story.append(Spacer(1, 1*mm))

info_data = [
    ["论文标题", "Image Generation Models: A Technical History"],
    ["作者", "Rouzbeh Shirvani (rouzbeh.asghari@gmail.com)"],
    ["发表信息", "arXiv: 2603.07455v2 [cs.CV], 2026 年 3 月 29 日"],
    ["论文类型", "综述 (Survey)"],
    ["页数 / 参考文献", "55 页 / 168 篇参考文献"],
    ["所属领域", "计算机视觉 · 图像生成 · 深度学习"],
]
info_table = Table(info_data, colWidths=[3.8*cm, 12*cm])
info_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (0, -1), CN_BOLD),
    ('FONTNAME', (1, 0), (1, -1), CN_FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('LEADING', (0, 0), (-1, -1), 15),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
    ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
    ('LINEABOVE', (0, 0), (-1, 0), 2, colors.black),
]))
story.append(info_table)
story.append(Spacer(1, 4*mm))

# --- Section 2: Content Summary ---
story.append(Paragraph("二、论文内容概述", h1_style))
story.append(Paragraph(
    "本文是一篇系统性的图像生成模型技术综述，按时间顺序梳理了过去十年图像生成领域"
    "从 VAE、GAN、Normalizing Flows、自回归/Transformer 模型到扩散模型、Flow Matching，"
    "以及视频生成和伪造检测的完整技术演进路径。全文共 10 个章节：",
    body_style))
story.append(Spacer(1, 2*mm))

sections = [
    ("第 1 章", "引言", "阐述图像生成领域碎片化问题，说明综述动机：缺乏一份覆盖各主流模型的统一技术性综述。"),
    ("第 2 章", "变分自编码器 (VAE)", "从 VAE 的 ELBO 推导出发，详述重参数化技巧、KL Collapse 问题及 β-VAE 解决方案，"
     "介绍 PixelVAE、条件 VAE (CVAE)、IWAE、DRAW、NVAE 等变体。指出 VAE 在可解释性和可控性上的优势，以及模糊重建的局限。"),
    ("第 3 章", "生成对抗网络 (GAN)", "从 Goodfellow 原始 GAN 出发，系统梳理 DCGAN、WGAN/WGAN-GP 的训练稳定性改进，"
     "条件 GAN (CGAN/AC-GAN)、StyleGAN v1-v3 的渐进式生成与风格解耦，StackGAN/AttnGAN 的文本到图像生成，"
     "以及 GAN 在超分辨率中的应用 (SRGAN)。总结了 GAN 的模式坍塌和训练不稳定问题。"),
    ("第 4 章", "Normalizing Flows", "介绍可逆映射与变量替换公式，详述 NICE、Real NVP 的仿射耦合层，"
     "Glow 的 1×1 可逆卷积，以及 MAF、IAF 等变体。指出其在精确似然计算和一步采样上的优势，"
     "但在高分辨率复杂图像生成上仍落后于 GAN 和扩散模型。"),
    ("第 5 章", "自回归与 Transformer 模型", "从 PixelRNN/PixelCNN 逐像素生成开始，到 Image Transformer、Image GPT 的自注意力替代卷积，"
     "VQ-VAE/VQ-GAN 的离散潜在空间表示，DALL-E 的文本到图像，MaskGIT 的并行解码，"
     "Muse 的双尺度 VQ tokenizer，以及 Parti (20B 参数) 的缩放实验。指出自回归模型训练稳定、条件生成自然，但逐 token 采样慢。"),
    ("第 6 章", "扩散模型 (Diffusion Models)", "从 Sohl-Dickstein 的热力学启发的扩散过程讲起，到 DDPM 的噪声预测重参数化与 UNet 架构，"
     "DDIM 的加速采样，Improved DDPM 的对数似然优化，条件扩散 (classifier guidance / classifier-free guidance, GLIDE)，"
     "潜在空间扩散 (LDM/Stable Diffusion)，DiT 的 Transformer 骨干替代 UNet，"
     "DALL-E 2 (unCLIP)/Imagen/DALL-E 3/SDXL 等大规模系统的技术细节。覆盖蒸馏加速 (Progressive Distillation, Consistency Models)。"),
    ("第 7 章", "Rectified Flow 与 Flow Matching", "基于连续 Normalizing Flow 的 ODE 框架：Rectified Flow 通过直线插值 + Reflow 实现少数步采样；"
     "Flow Matching 利用条件概率路径回归向量场，在最优传输路径下以更少 NFE 达到更低 FID。"
     "介绍了 Scaling Rectified Flow Transformers (SD3 等系统) 及边界条件改进。"),
    ("第 8 章", "视频生成", "从 GAN 的视频生成 (VGAN/MoCoGAN) 讲起，到 VideoGPT 的 VQ-VAE + 自回归 Transformer，"
     "视频扩散模型 (Video Diffusion Models/Imagen Video/Stable Video Diffusion/Lumiere)，"
     "Make-A-Video 的无文本-视频数据训练，Phenaki 的可变长度生成。核心瓶颈：长时间一致性、运动可控性、计算开销。"),
    ("第 9 章", "伪造图像与社会影响", "讨论 deepfakes 的社会危害（操纵舆论、诈骗、隐私侵犯），检测方法（眨眼检测、面部扭曲伪影、频率域分析），"
     "基准数据集 (FaceForensics++, DFDC)，生成图像水印技术 (Stable Signature)，以及 DIRE (扩散重建误差) 检测方法。"),
    ("第 10 章", "总结", "回顾各模型的演进与相互关系，指出未来方向：更少步数的生成、更好的时序与 3D 一致性、强大的条件控制、"
     "水印技术与负责任部署。"),
]

for chap, title, desc in sections:
    story.append(Paragraph(f"<b>{chap} — {title}</b>", h2_style))
    story.append(Paragraph(desc, body_style))

story.append(Spacer(1, 4*mm))

# --- Section 3: Key Contributions ---
story.append(Paragraph("三、主要贡献", h1_style))

contributions = [
    "<b>首次提供跨模型族的统一技术综述：</b>不同于仅聚焦单一模型族的综述，本文覆盖 VAE/GAN/Flow/"
    "Autoregressive/Diffusion/Flow Matching 等所有主流生成模型，对每种模型均提供从数学公式到训练算法的完整技术 walkthrough。",

    "<b>技术细节与训练流程并重：</b>对每种模型给出：(i) 底层目标函数与数学推导，(ii) 架构设计选择，"
    "(iii) 算法级训练步骤（以伪代码 Box 形式呈现），(iv) 常见失败模式与优化技巧。这对于工程实现具有直接参考价值。",

    "<b>覆盖最新进展：</b>包含 2024-2026 年最新工作，如 Rectified Flow/Flow Matching 的现代生成系统、"
    "Stable Video Diffusion、Lumiere、Gen-4 等，追踪了从扩散模型到 Flow-based 范式的范式转移。",

    "<b>兼顾社会责任维度：</b>专设章节讨论 deepfake 检测、频率域伪影、水印技术（Stable Signature）等防御手段，"
    "技术综述与社会影响并重，这在同类综述中较为少见。",

    "<b>清晰的技术演进叙事：</b>按时间顺序组织，帮助读者理解各模型为何出现、解决了什么问题、遗留了什么局限，"
    "形成完整的认知框架。",
]

for c in contributions:
    story.append(Paragraph(f"• {c}", bullet_style))
    story.append(Spacer(1, 1*mm))

story.append(Spacer(1, 4*mm))

# --- Section 4: Methods Comparison ---
story.append(Paragraph("四、各模型核心对比", h1_style))
story.append(Spacer(1, 1*mm))

comp_data = [
    ["模型族", "训练方式", "生成质量", "采样速度", "主要局限"],
    ["VAE", "ELBO 最大化", "中等（模糊）", "一步（快）", "后验坍塌、模糊重建"],
    ["GAN", "对抗博弈", "高（清晰）", "一步（快）", "模式坍塌、训练不稳定"],
    ["Normalizing Flow", "精确对数似然", "中等", "一步（快）", "维度受限、高分辨率困难"],
    ["自回归/Transformer", "最大似然", "高", "逐 token（慢）", "O(n²)注意力、顺序依赖"],
    ["扩散模型 (DDPM)", "噪声预测 MSE", "很高", "数百~千步（慢）", "采样步骤多，去噪耗时长"],
    ["Rectified Flow / FM", "向量场回归 MSE", "很高", "少量步（快）", "边界条件敏感"],
]
comp_table = Table(comp_data, colWidths=[3.2*cm, 2.8*cm, 2.2*cm, 2.5*cm, 5.3*cm])
comp_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), CN_FONT),
    ('FONTNAME', (0, 0), (-1, 0), CN_BOLD),
    ('FONTSIZE', (0, 0), (-1, -1), 8.5),
    ('LEADING', (0, 0), (-1, -1), 12),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('ALIGN', (4, 0), (4, -1), 'LEFT'),
    ('LEFTPADDING', (0, 0), (-1, -1), 4),
    ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ('TOPPADDING', (0, 0), (-1, -1), 2),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ('LINEABOVE', (0, 0), (-1, 0), 2, colors.black),
    ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
    ('LINEBELOW', (0, -1), (-1, -1), 2, colors.black),
    ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.9, 0.9, 0.9)),
]))
story.append(comp_table)
story.append(Spacer(1, 5*mm))

# --- Section 5: Highlights ---
story.append(Paragraph("五、值得关注的亮点", h1_style))

highlights = [
    "<b>数学推导完整：</b>VAE 从 ELBO 到重参数化，GAN 从 min-max 到 WGAN 的 Wasserstein 距离，"
    "扩散模型从马尔可夫链到 DDIM 的确定性采样——每个公式都有上下文解释，适合作为教学参考资料。",

    "<b>算法步骤清晰：</b>文中包含 12 个 Box，以伪代码形式给出 CVAE、Normalizing Flow、DDPM、"
    "DALL-E 2、Rectified Flow、Flow Matching、Stable Video Diffusion 等模型的完整训练/推理流程。",

    "<b>核心模型间的联系被揭示：</b>例如 VQ-VAE 是扩散模型进入潜在空间的关键使能技术；"
    "DDPM 的重参数化技巧（预测噪声而非均值）是其工程可行性的关键；"
    "Classifier-free guidance 从标签条件到文本条件的推广直接催生了 GLIDE 和 Stable Diffusion。",

    "<b>范式转移信号：</b>论文敏锐地捕捉到从扩散模型到 Flow Matching 的转变趋势——"
    "Rectified Flow 和 Flow Matching 提供了更干净的连续时间动态、更少的采样步数和更好的训练稳定性，"
    "正在成为下一代生成系统的基础。",

    "<b>安全性讨论务实：</b>不止于泛泛而谈，详细介绍了 DIRE（扩散重建误差检测）、"
    "频谱伪影分析（上卷积引入的棋盘格频率特征）、Stable Signature 水印（48-bit 签名，"
    "误检率 1/10⁹）等具体技术方案。",
]
for h in highlights:
    story.append(Paragraph(f"• {h}", bullet_style))
    story.append(Spacer(1, 1*mm))

story.append(Spacer(1, 4*mm))

# --- Section 6: Evaluation ---
story.append(Paragraph("六、读后评价", h1_style))

eval_points = [
    "<b>优点：</b>(1) 技术深度与广度平衡得当，公式推导严谨但不过度晦涩，适合作为入门到进阶的桥梁读物；"
    "(2) 各章节的 Conclusion 和末章 Final Conclusion 提供了精炼的技术总结，可直接引用；"
    "(3) 数学符号统一、Box 式训练流程可操作性强，便于复现；"
    "(4) 引用全面（168 篇），涵盖了各方向的关键论文。",

    "<b>不足：</b>(1) 几乎没有实验结果对比——综述未提供各模型在标准 benchmark 上的 FID/IS 等量化对比表，"
    "缺少定量比较是明显短板；(2) 对 GAN 之后模型之间的内在理论联系讨论不够深入（如 score-based SDE 统一框架），"
    "更多是按时间线的并列叙述；(3) 实验架构多为文字描述，缺少架构图对理解有影响；(4) 对最新闭源商业模型 "
    "（如 DALL-E 3、Sora 等）的技术细节披露有限。",

    "<b>对个人研究的启发：</b>本文为红外图像超分辨率研究提供了清晰的模型选型参考——扩散/Flow Matching 模型"
    "在图像重建质量和多样性方面优于 GAN 和 VAE，Flow Matching 正成为更高效的选择；"
    "潜在空间操作和条件控制机制可直接借鉴用于红外-SR 的退化建模和重建。",
]
for e in eval_points:
    story.append(Paragraph(f"• {e}", bullet_style))
    story.append(Spacer(1, 1*mm))

story.append(Spacer(1, 5*mm))
story.append(hr())
story.append(Spacer(1, 2*mm))
story.append(Paragraph(
    "报告完成日期：2026 年 5 月 11 日  ·  钟兴炜  ·  chungxw@whu.edu.cn",
    ParagraphStyle('Footer', parent=meta_style, alignment=TA_CENTER)))

# ================================================================
# Build PDF
# ================================================================
doc.build(story)
print(f"PDF saved to: {output}")
