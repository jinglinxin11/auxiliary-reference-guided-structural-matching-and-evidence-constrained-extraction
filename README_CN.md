# 结构匹配与证据约束提取

本仓库仅包含结构匹配算法、必要输入、诊断和对应图集。
完整参数及文件定义见 [README.md](README.md) 和
[图集说明](paper_figures/README.md)。

从仓库根目录运行：

```text
python paper_figures/run_all.py --target-scale-bar-um 200 --reference-scale-bar-um 500
```

入口自动创建隔离临时环境并执行全部 16 次配准，需安装 Arial。
旧六 ROI UV/NIR 绘图已移至单独历史归档，不属于本仓库，也不是当前补充材料图 14。
源码提交和输入路径均采用版本标识与仓库相对路径，不依赖个人目录。
