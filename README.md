# InfraredSR — 红外图像超分辨率研究项目

本项目面向红外遥感图像超分辨率及相关任务，包含数据集、论文、汇报材料、阅读报告和辅助脚本。

---

## 目录结构

```
InfraredSR/
├── datasets/      # 实验数据集（5 个）
├── papers/        # 参考文献（14 篇）
├── ppts/          # 汇报 PPT
├── reports/       # 阅读报告
├── scripts/       # 辅助脚本
└── README.md
```

---

## datasets/

共五个数据集，覆盖红外遥感领域的核心任务。

| 子目录 | 任务 | 说明 |
|--------|------|------|
| `Data/` | 红外图像超分辨率 | 7,121 对 HR/LR 灰度红外图像，支持 ×2、×4 两种倍率；已划分 train/val/test |
| `dataset/` | 航拍车辆检测 | VEDAI 数据集，1,246 张配对 RGB+IR 航拍图，3,706 个标注框（8 类），含 5 折交叉验证 |
| `OLI2MSI/` | 跨传感器图像翻译 | Landsat-8 (30m) → Sentinel-2 (10m)，5,325 对 GeoTIFF 图像块，5 个地理场景 |
| `CIDIS-dataset-main/` | 跨光谱图像配准 | 1,000 对热红外+可见光配对图像 (640×448)，train 700 / val 200 / test 100 |
| `dataset_CIDIS_guided_x8x16/` | 可见光引导红外超分 | 基于 CIDIS 构建，热红外 GT/LR×8/LR×16 配可见光引导图，×8 和 ×16 两种倍率 |

详见 `ppts/InfraredSR_Datasets_Overview.pptx`。

---

## papers/

红外/遥感图像超分辨率相关论文，共 14 篇。

| 编号/文件 | 标题 | 年份 |
|-----------|------|------|
| `838/` | ThermalGen: Style-Disentangled Flow-Based Generative Models for RGB-to-Thermal Image Translation | 2025 |
| `841/` | Toward Real-world Infrared Image Super-Resolution: A Unified Autoregressive Framework and Benchmark | 2026 |
| `844/` | DifIISR: A Diffusion Model with Gradient Guidance for Infrared Image Super-Resolution | 2025 |
| `847/` | SwinIBSR: Towards Real-World Infrared Image Super-Resolution | 2024 |
| `849/` | Modeling Thermal Infrared Image Degradation and Real-World Super-Resolution Under Background Thermal | 2024 |
| `851/` | Beyond Synthetic Scenarios: Weakly-Supervised SR for Spatiotemporally Misaligned Remote Sensing | 2026 |
| `853/` | Towards Realistic Data Generation for Real-World Super-Resolution | 2025 |
| `855/` | A Radiometrically and Spatially Consistent Super-Resolution Framework for Sentinel-2 | 2026 |
| `857/` | Unsupervised Diffusion-Based Degradation Modeling for Real-World Super-Resolution | — |
| `2603.07455v2.pdf` | Image Generation Models: A Technical History | 2026 |
| 直接文件 | Infrared Image Super-Resolution: A Systematic Review and Future Trends | — |
| 直接文件 | Thermal Image Super-Resolution Challenge Results — PBVS 2025 (CVPRW) | 2025 |
| 直接文件 | Projection Manifold Regularization (2212.00490v2) | 2022 |
| 直接文件 | Cross-Spectral Image Registration: a Comparative Study and a New Benchmark Dataset | 2024 |

---

## ppts/

汇报与说明材料。

| 文件 | 内容 |
|------|------|
| `InfraredSR_Datasets_Overview.pptx` | 五个数据集的详细介绍（白底黑字、三线表学术风格，8 页） |
| `20260402.pptx` | 阶段性汇报 |
| `20260407.pptx` | 阶段性汇报 |

---

## reports/

阅读报告。

| 文件 | 内容 |
|------|------|
| `report.pdf` | Image Generation Models 论文阅读报告 |
| `report.tex` | 阅读报告 LaTeX 源文件（可用 Overleaf 编译） |

---

## scripts/

辅助工具脚本。

| 文件 | 用途 |
|------|------|
| `create_ppt.py` | 自动生成 `InfraredSR_Datasets_Overview.pptx`，包含数据集总览表、示例图像、统计信息 |
| `generate_report.py` | 生成论文阅读报告 PDF |

运行方式：

```bash
python scripts/create_ppt.py
python scripts/generate_report.py
```
