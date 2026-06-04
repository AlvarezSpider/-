# 汽车理论课程设计

基于《汽车理论》课程的三道典型计算题目，使用 Python 编程完成全部计算与绘图。

## 题目

| # | 习题 | 内容 |
|---|------|------|
| 一 | 1.3 | 轻型货车动力性能计算（五档变速器） |
| 二 | 2.7 | 轻型货车燃油经济性计算 |
| 三 | 4.3 | 中型货车制动性能计算 |

## 主要结果

| 指标 | 结果 |
|------|------|
| 最高车速 | 99.08 km/h |
| 最大爬坡度 | 35.02% |
| 2档起步至70km/h加速 | 16.29 s |
| 5档60km/h等速油耗 | 13.84 L/100km |
| 六工况循环百公里油耗 | 13.18 L/100km |
| 满载制动距离 (30km/h, φ=0.8) | 5.33 m |

## 运行

```bash
conda run -n modeling python part1_dynamic_performance.py
conda run -n modeling python part2_fuel_economy.py
conda run -n modeling python part3_braking_performance.py
```

## 文件说明

```
├── part1_dynamic_performance.py   # 题目一：动力性能计算
├── part2_fuel_economy.py          # 题目二：燃油经济性计算
├── part3_braking_performance.py   # 题目三：制动性能计算
├── generate_report.py             # DOCX报告生成脚本
├── fig*.png                       # 计算图表 (5张)
├── 课程设计报告.docx              # 完整课程设计报告
└── 2026汽车理论课程设计题目2.pdf   # 原题
```

## 报告生成

```bash
conda run -n modeling python generate_report.py
```

生成 `课程设计报告.docx`，含目录、解题过程、图表和完整代码附录。
