# 从结果清单到论证段落

这是人工设计的教学对照，使用仓库已有的[合成回归实验](../knn-regression/materials/summary.json)实际计算值。
它展示写作选择如何落到正文，不是盲测生成结果，也不宣称方法创新。

要回答的问题：在训练范围内增加近邻数量得到的改善，是否延伸到受测外推区域？

数据单位是五个固定训练随机种子；下列 `+/-` 表示跨种子的样本标准差，不是置信区间。

## 准确但像流水账

> We evaluate one- and five-neighbor regression on an in-domain grid and an
> extrapolation grid across five fixed training seeds. In-domain MSE is
> 0.1083 +/- 0.0056 for one neighbor and 0.0851 +/- 0.0128 for five neighbors.
> Extrapolation MSE is 2.6891 +/- 1.4620 for one neighbor and
> 3.7012 +/- 1.3386 for five neighbors. These are means and sample standard
> deviations across training seeds. The results cover both grids.

所有数字都准确，但首尾没有交代这组比较回答了什么问题。读者需要自己从表格推导意义。

## 相同证据，明确论证

> Increasing the neighbor count improves in-domain error but reverses the
> mean-error ranking on the tested extrapolation grid. Across five fixed
> training seeds, five-neighbor regression reduces in-domain MSE from
> 0.1083 +/- 0.0056 to 0.0851 +/- 0.0128, while extrapolation MSE rises
> from 2.6891 +/- 1.4620 to 3.7012 +/- 1.3386 (mean +/- sample SD).
> The in-domain advantage therefore does not extend to this extrapolation
> setting; these descriptive comparisons do not establish significance.

改变的是信息之间的关系：先给出跨条件反转这一发现，接着用两组均值及其波动支撑它，
最后回答范围问题。数值并没有被删掉来制造“简洁”，不利结果和不确定性也仍然保留。

## 迁移了什么

| 写作选择 | 范文中的功能 | 我们材料允许的动作 | 正文中的实现 |
| --- | --- | --- | --- |
| 用一组有区分力的对照检验解释 | [Mirage 摘要](https://proceedings.neurips.cc/paper_files/paper/2023/hash/adc98a266f45005c403b8311ca7e8bd7-Abstract-Conference.html)让互补证据回应同一解释；这里只借鉴这种组织功能 | 把两种测试区域的相反排序放在同一个问题下，而不是各自汇报 | 首句指出反转，两组数值随后支撑 |
| 把比较条件贴在收益旁 | [PagedAttention 摘要](https://arxiv.org/abs/2309.06180)将吞吐收益与延迟条件绑定；这里迁移条件绑定，不迁移其机制 | 分开域内与外推条件，保留跨种子的统计单位 | `in-domain`、`extrapolation`、`five fixed training seeds` |
| 不迁移缺少证据的推导 | DPO 的简化来自其数学重表述，我们没有对应推导 | 不把排序反转归因于某个已证明机制 | 只解释观测范围，不新增因果结论 |

采用哪种开头和需要多少数字取决于当前段落要回答的问题。完整方法、理论、数据集或负结果
应有各自的论证。实际工作采用[论证迁移流程](../../references/argument-transfer.md)，并在现有写作理由矩阵中
定位“借鉴的选择、自己的证据、正文实现”，不用另建一套强制材料。
