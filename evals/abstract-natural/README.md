# Source-Calibrated Abstract Demonstration

[打开中文对照页](comparison.html)

上一轮候选已经完成了证据筛选，但仍然不像原作者的摘要：它把正文中的
实现细节和实验结果压缩进摘要，导致句子层级相同、段落节奏平直。这一轮
加入了 `references/abstract-rhetoric.md`，并重新阅读五篇官方摘要，学习其
信息层级和组织方式，而不是复制句子。

## 三栏说明

- **作者摘要 · 中文概述**：此前的中文概述，不是原摘要逐字翻译。
- **上一轮候选**：保留上一轮候选；P02 使用已记录的事实修正版。
- **本轮 source-calibrated**：读过官方摘要后重新组织的英文稿及中文译稿。

本轮候选重点恢复：

1. 先给研究问题、能力或资源价值；
2. 方法只写到贡献级别，机制细节只在解释贡献时出现；
3. 结果按原文的抽象层级表达，不逐项复述正文表格；
4. 用迁移能力、资源价值或第二贡献自然收束。

这不是新盲测。候选直接使用了已知论文和原摘要的结构观察，且中文翻译
由同一工作流生成。页面用于检查“是否更像作者式摘要”，不证明人类读者
偏好或写作质量提升。原始候选、事实审计和历史失败实验均未覆盖。

```bash
python3.14 evals/abstract-natural/render.py
python3.14 evals/abstract-natural/render.py --check
python3.14 -m unittest discover -s tests -p 'test_abstract_natural.py'
```

官方摘要页面：

- [EquiBot](https://proceedings.mlr.press/v270/yang25a.html)
- [Sparsh](https://proceedings.mlr.press/v270/higuera25a.html)
- [ManiWAV](https://proceedings.mlr.press/v270/liu25c.html)
- [PoliFormer](https://proceedings.mlr.press/v270/zeng25a.html)
- [OKAMI](https://proceedings.mlr.press/v270/li25a.html)
