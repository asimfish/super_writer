# Reproducible Toy Regression / 可复算实证样文

[Read the manuscript](manuscript.md) | [PDF](manuscript.pdf) | [Word](manuscript.docx) |
[Evidence and revision](writing-decisions.md) | [Raw materials](materials/)

不是编造实验数字的展示：数据生成过程是合成的，表格数字由公开脚本实际计算。
样文展示如何写清楚方法、复现协议、正反结果和主张边界，不宣称方法创新或顶会录用。
正文由 AI 辅助编写并据材料核对，属于 worked example，不是独立盲测结果。

Reproduce from the repository root (Python 3.10+, standard library only):

```bash
python3 examples/knn-regression/experiment.py
python3 -m unittest discover -s tests -p test_examples.py -v
```

The first command prints the measured summary without writing files. To regenerate
the checked-in CSV and JSON explicitly:

```bash
python3 examples/knn-regression/experiment.py --output-dir examples/knn-regression/materials
```

Independent exercise input, without the worked answers:

```text
使用 $super-writer，根据 experiment.py、materials/ 和 draft.md，
改写摘要与 Results，并列出不能写的主张。只使用提供的材料；
不补做实验，不运行完整投稿流程，不把教学例子当成原创研究。
```

The referenced textbook is cited, not redistributed. All prose, code and locally
generated data in this example are released under the repository's MIT license.
