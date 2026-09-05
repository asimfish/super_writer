# Assumption-Aware Theory / 假设与证明样文

[Manuscript](manuscript.md) | [PDF](manuscript.pdf) | [Word](manuscript.docx)

这篇教学短文展示“假设 → 命题 → 证明 → 反例 → 不支持的解释”。
凸组合的区间性质是基础知识，不是本项目的新定理；有限测试不能代替证明。
正文是 AI 辅助编写、逐步核对证明的 worked example，不是独立模型盲测。

The independently written proof uses nonnegative normalized weights. Tests use
exact rational arithmetic and explicitly exercise negative weights, zero total
weight, and an inaccurate-but-range-preserving aggregate.

```bash
python3 -m unittest discover -s tests -p test_examples.py -v
```

The textbook is referenced only. Its copyrighted text, figures and PDF are not
redistributed. This example's own prose is MIT-licensed.
