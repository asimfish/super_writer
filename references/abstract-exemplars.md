# Abstract Exemplars: Editorial Notes

Read only a few contribution-matched entries after [abstract decisions](abstract-decisions.md).
These are original Chinese editorial notes on 24 public abstracts, not reproduced
abstracts, official templates, or evidence of acceptance gains. Paper titles and
links identify sources; linked works retain their own rights. Selection is
purposive and classic-heavy, not a representative sample or quality ranking.
Reading scope is the abstract, not full-paper proof/experiment verification.
A famous paper is not a reason to imitate every sentence. These notes have not
been validated as improving generated writing.

Sources were studied on 2026-09-10; synthesis integrated on 2026-09-11.
Rethinking and SQuAD use the linked author versions; PagedAttention uses its
author abstract. The remaining entries use conference/archival pages. For
FlashAttention, suspected missing words in the HTML mean exact wording or
numerical reuse needs a PDF check. No automatic fetching is required here.

## 01. DPO (NeurIPS 2023)

[Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://proceedings.neurips.cc/paper_files/paper/2023/hash/a85b405ed65c6477a4fe8302b5e06ce7-Abstract-Conference.html)

- 主线：偏好对齐流程复杂；奖励与最优策略的映射允许更直接的训练。
- 组织：现有流程负担 → 数学重表述 → 省掉哪些步骤 → 对齐任务验证。
- 证据：用情感控制、摘要、对话结果支持简化后的有效性；没有强行塞入提升百分比。
- 借鉴：关键不是宣称简单，而是交代为何能简单；核心映射不能被实现模块挤掉。
- 边界：不把摘要中的强性能形容词当通用句式；没有等价性推导不能照搬重表述叙事。

## 02. SimCLR (ICML 2020)

[A Simple Framework for Contrastive Learning of Visual Representations](https://proceedings.mlr.press/v119/chen20j.html)

- 主线：对比学习的有效性可以通过关键设计选择得到解释。
- 组织：简化框架 → 系统研究组件 → 三项发现 → 组合收益。
- 证据：区分线性评估和少标签微调，并给出各自指标及参照。
- 借鉴：组件列表在这里是研究发现列表，不是任意实现清单；每项回答什么使方法有效。
- 边界：不能一概禁止列举；但未做组件研究时，三个模块不能写成三个已验证洞察。

## 03. CLIP (ICML 2021)

[Learning Transferable Visual Models From Natural Language Supervision](https://proceedings.mlr.press/v139/radford21a.html)

- 主线：固定类别监督限制通用性，图文匹配训练提供另一种任务接口。
- 组织：监督限制 → 训练机制与规模 → 语言驱动迁移 → 多任务与具体参照。
- 证据：广泛任务覆盖与 ImageNet 零样本参照承担不同证据作用。
- 借鉴：把训练方式和测试时能力接起来，避免只报一个大规模预训练数字。
- 边界：零样本不代表没有训练数据；不能省掉大规模图文预训练条件来制造公平预算印象。

## 04. BERT (NAACL 2019)

[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://aclanthology.org/N19-1423/)

- 主线：深层双向上下文预训练支持少量任务特定改动的迁移。
- 组织：模型与区别 → 下游使用方式 → 跨任务结果。
- 证据：列多个具名指标与改进幅度，支撑适用范围而非只证明单任务峰值。
- 借鉴：几乎不铺垫宏观背景，直接交代区别及其使用后果。
- 边界：包含引用和评价性形容词不是所有会议都适用；获奖也不使每句自动成为最佳表达。

## 05. ResNet (CVPR 2016)

[Deep Residual Learning for Image Recognition](https://openaccess.thecvf.com/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html?_hsmi=2)

- 主线：更深的网络难训练，残差函数重参数化改变优化问题。
- 组织：短问题句 → 核心重表述 → 优化证据 → 深度、复杂度与任务结果。
- 证据：深度增加与复杂度关系，以及分类和检测结果，共同支撑主张。
- 借鉴：机制一句话可复述；不是只有一个新模型名和一串排行榜。
- 边界：不能照搬竞赛成绩堆叠，也不能没有受控证据就使用强因果归因。

## 06. MAE (CVPR 2022)

[Masked Autoencoders Are Scalable Vision Learners](https://openaccess.thecvf.com/content/CVPR2022/html/He_Masked_Autoencoders_Are_Scalable_Vision_Learners_CVPR_2022_paper.html)

- 主线：非对称架构与高遮挡比例共同使图像重建预训练具有可扩展性。
- 组织：主张 → 任务 → 两个设计 → 联合作用 → 效率与迁移证据。
- 证据：效率和准确率对应双重承诺，ImageNet-1K 数据条件约束性能比较。
- 借鉴：不必写人为制造的研究缺口；设计之间的关系比模块名字更重要。
- 边界：列设计必须说明功能关系；不能把数据条件删掉只保留最高准确率。

## 07. Robustness law (NeurIPS 2021)

[A Universal Law of Robustness via Isoperimetry](https://proceedings.neurips.cc/paper_files/paper/2021/hash/f197002b9a0853eca5e046d9ca4663d5-Abstract.html)

- 主线：平滑插值比仅仅插值需要更大的参数规模。
- 组织：经典解释与现象冲突 → 必要性结果 → 维度依赖 → 分布和函数类条件 → 理论意义。
- 证据：参数量的维度依赖和适用假设本身就是证据内容，不需要补造实验。
- 借鉴：必要与充分、适用类和条件是摘要核心信息，不是可随便压缩的免责声明。
- 边界：标题中的 universal 不能脱离正文假设扩展为一切分布、一切模型。

## 08. DAgger (AISTATS 2011)

[A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning](https://proceedings.mlr.press/v15/ross11a.html)

- 主线：动作改变后续观测分布，需在策略诱导分布下理解模仿学习。
- 组织：IID 前提失效 → 现有保证的局限 → 迭代算法与无悔解释 → 有条件保证 → 实验。
- 证据：定理关注策略自身诱导的分布；实验提供实际问题上的补充证据。
- 借鉴：明确保证的对象比多说一句 robust 更有辨识度。
- 边界：附加归约假设不能变成无条件保证；有限任务实验不能代替全部理论前提检查。

## 09. TRPO (ICML 2015)

[Trust Region Policy Optimization](https://proceedings.mlr.press/v37/schulman15.html)

- 主线：有理论根据的策略改进方案经近似转化为可运行算法。
- 组织：理论方案 → 近似后的算法 → 任务验证 → 近似与经验趋势的边界。
- 证据：把单调改进的理论方案与实用算法的经验趋势分开表述。
- 借鉴：一句明确的近似关系比结尾笼统的局限声明更能防止误读。
- 边界：不能把理论方案的保证直接归给所有实际实现；不应机械要求每篇报百分比。

## 10. rliable (NeurIPS 2021)

[Deep Reinforcement Learning at the Edge of the Statistical Precipice](https://proceedings.neurips.cc/paper/2021/hash/f514cec81cb148559cf475e7426eed5e-Abstract.html)

- 主线：少量训练运行下，聚合点估计可能支持不可靠的算法比较。
- 组织：常见评估习惯 → 不确定性后果 → 个案诊断 → 替代统计工具 → 跨基准复核。
- 证据：比较结论变化是核心结果，工具发布是落地支撑，不是新算法性能领先。
- 借鉴：负面诊断可以形成积极贡献：读者应改变怎样判断结果。
- 边界：不能仅因提出指标就声称解决可靠性；其较长铺垫也不必在短字数预算中照搬。

## 11. Mirage (NeurIPS 2023)

[Are Emergent Abilities of Large Language Models a Mirage?](https://proceedings.neurips.cc/paper_files/paper/2023/hash/adc98a266f45005c403b8311ca7e8bd7-Abstract-Conference.html)

- 主线：某些看似突然的能力变化可由指标选择解释，而非模型行为突变。
- 组织：定义现象 → 替代解释 → 数学模型 → 三条互补检验路径 → 有限结论。
- 证据：预测验证、元分析与跨领域构造承担不同证据功能。
- 借鉴：实验不是数量清单，而是对同一解释的交叉检验。
- 边界：不能压成一切涌现都是假的；固定输出、任务和模型族范围及结尾不确定性都重要。

## 12. Rethinking generalization (ICLR 2017)

[Understanding deep learning requires rethinking generalization](https://arxiv.org/abs/1611.03530v2)

- 主线：能拟合随机标签的模型也能在真实数据上泛化，常见解释因此面临挑战。
- 组织：泛化现象 → 传统解释 → 随机标签与噪声反例 → 理论表达能力构造。
- 证据：反例与构造用于检验解释，而不是证明一个新方法优于基线。
- 借鉴：摘要中的意外结果应改变问题理解，而不只是形容结果 surprising。
- 边界：拟合随机标签不等于模型不能泛化；挑战部分解释不等于解决整个泛化理论。

## 13. Edge-of-Reach (NeurIPS 2024)

[The Edge-of-Reach Problem in Offline Model-Based Reinforcement Learning](https://proceedings.neurips.cc/paper_files/paper/2024/hash/7314e20a73542bbfff25030d1185ce88-Abstract-Conference.html)

- 主线：改善动力学模型并不必然修复某些离线模型式 RL 方法，截断 rollout 暴露另一种问题。
- 组织：主流解释 → 理想模型替换反例 → 实际与理论的差异 → 机制命名 → 针对性方法。
- 证据：消除被指责误差后的失败，帮助区分替代解释。
- 借鉴：先让反例提出必须回答的问题，再让方法回答它，方法不是突然出现。
- 边界：不要把受测方法的失败写成所有模型式 RL 都失败；结尾未来预测不应成为固定句式。

## 14. Many Faces (ICCV 2021)

[The Many Faces of Robustness: A Critical Analysis of Out-of-Distribution Generalization](https://openaccess.thecvf.com/content/ICCV2021/html/Hendrycks_The_Many_Faces_of_Robustness_A_Critical_Analysis_of_Out-of-Distribution_ICCV_2021_paper.html)

- 主线：鲁棒性改进依赖偏移类型，单一测试不足以支持通用鲁棒性。
- 组织：新数据 → 检验旧结论 → 正向发现 → 新方法 → 不起作用的偏移 → 范围结论。
- 证据：同时给出成功与失败类型，约束跨偏移的泛化主张。
- 借鉴：限制不是削弱贡献；跨条件差异本身就是主要发现。
- 边界：不能只抽取某个巨大比较数字，删除后面的不一致性结果。

## 15. CheckList (ACL 2020)

[Beyond Accuracy: Behavioral Testing of NLP Models with CheckList](https://aclanthology.org/2020.acl-main.442/)

- 主线：测试集准确率之外，需要系统性检查语言行为。
- 组织：评估缺口 → 行为测试思想 → 能力与测试矩阵 → 模型故障 → 使用者实验。
- 证据：发现可行动错误和使用者测试效果，直接支持工具用途。
- 借鉴：工具论文应证明它让使用者完成了什么，而不只说实现了哪些功能。
- 边界：测试数量不是缺陷发现能力的同义词；用户研究结论不能脱离受测群体推广。

## 16. FlashAttention (NeurIPS 2022)

[FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://proceedings.neurips.cc/paper/2022/hash/67d57c32e20fd0a7a302cb81d36e40d5-Abstract-Conference.html)

- 主线：减少算术复杂度不等于实际加速，内存读写是关键瓶颈之一。
- 组织：长序列成本 → 近似方法与实际速度脱节 → IO 洞察 → 分块机制 → 分析与实测。
- 证据：IO 分析和实际训练/任务结果回答不同层面的效率问题。
- 借鉴：把瓶颈与设计动作建立明确关系；算法名不能替代原因。
- 边界：官方 HTML 存在疑似缺词，精确逐字或数字分析需核对 PDF；不能只照抄网页残句。

## 17. Alpa (OSDI 2022)

[Alpa: Automating Inter- and Intra-Operator Parallelism for Distributed Deep Learning](https://www.usenix.org/conference/osdi22/presentation/zheng-lianmin)

- 主线：自动并行计划需要跨算子和算子内的统一搜索视角。
- 组织：系统功能 → 手工或受限搜索的不足 → 两层抽象 → 编译与运行时 → 手调参照和架构泛化。
- 证据：是否达到手工优化水平及适应异构架构，比代码模块数量更重要。
- 借鉴：以一个层次抽象组织多个组件，复杂系统也能有单一主线。
- 边界：不必为效率摘要虚构加速倍数；自动化能力与每个任务最快是不同主张。

## 18. PagedAttention (SOSP 2023)

[Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180)

- 主线：KV 缓存碎片和重复限制批大小，内存管理影响服务吞吐。
- 组织：吞吐需求 → 动态缓存浪费 → 分页思想 → 系统能力 → 相同延迟下吞吐比较。
- 证据：吞吐与延迟约束绑定，较长序列等工作负载差异限定收益。
- 借鉴：比较条件必须贴着收益写；机制到指标之间的因果路径清楚。
- 边界：吞吐提高不等于延迟降低；不能忽略负载与解码方式，也不能把类比当成新颖性证明。

## 19. Consistency Policy (RSS 2024)

[Consistency Policy: Accelerated Visuomotor Policies via Consistency Distillation](https://www.roboticsproceedings.org/rss20/p071.html)

- 主线：资源受限机器人需要快速推理且保留任务成功能力。
- 组织：硬件约束 → 速度替代方案 → 蒸馏机制 → 仿真与实机 → 速度和成功率 → 训练条件。
- 证据：笔记本 GPU 场景与成功率共同约束速度收益。
- 借鉴：从使用场景出发选择指标，不只报告抽象推理速度。
- 边界：不能把 competitive success 等同于统计等效；仿真和实机结果应分开。

## 20. SAM (ICCV 2023)

[Segment Anything](https://openaccess.thecvf.com/content/ICCV2023/html/Kirillov_Segment_Anything_ICCV_2023_paper.html)

- 主线：可提示分割任务、模型和数据收集循环构成相互支撑的资源项目。
- 组织：项目对象 → 数据形成及规模 → 可提示性 → 迁移验证 → 公开资源。
- 证据：资源规模、获取条件和迁移能力分别支撑不同贡献。
- 借鉴：任务、模型、数据可以组成整体贡献，不必强行写成单个算法。
- 边界：不能学到只有巨大规模和宣传性形容词；规模不能替代质量，公开访问也不等于任意许可。

## 21. SQuAD (EMNLP 2016)

[SQuAD: 100,000+ Questions for Machine Comprehension of Text](https://arxiv.org/abs/1606.05250v3)

- 主线：明确定义答案为原文片段的阅读理解数据，并显示机器与人的差距。
- 组织：数据来源与任务定义 → 推理类型分析 → 基线 → 人类参照 → 可获得性。
- 证据：模型与人类的差距说明挑战空间，不是单纯炫耀数据量。
- 借鉴：数据集摘要首先让读者知道一个样本和一个答案是什么。
- 边界：不能只写样本数；人类成绩不是未经说明的绝对性能上界。

## 22. WILDS (ICML 2021)

[WILDS: A Benchmark of in-the-Wild Distribution Shifts](https://proceedings.mlr.press/v139/koh21a.html)

- 主线：自然发生的分布偏移在常用数据中代表不足。
- 组织：现实风险 → 评估缺口 → 多种真实偏移 → 基线缺口 → 统一评估支持。
- 证据：域内外落差及现有方法仍未消除的差距证明基准的必要性。
- 借鉴：用具体变化轴说明覆盖面，而不是只说 diverse 和 real-world。
- 边界：十个数据集不是覆盖所有现实偏移；标准化工具也不自动保证无泄漏。

## 23. Diffusion Policy (RSS 2023)

[Diffusion Policy: Visuomotor Policy Learning via Action Diffusion](https://roboticsproceedings.org/rss19/p026.html)

- 主线：把视觉运动策略表示为条件去噪过程，适配动作分布特性。
- 组织：表示方式 → 范围与主结果前置 → 生成机制 → 动作空间适配 → 关键实现。
- 证据：任务与基准范围使平均提升有解释对象。
- 借鉴：结果可以在机制之前；只要中心明确，摘要不必遵循固定五段顺序。
- 边界：平均提升不等于每个任务提升，也不能照搬泛化或稳定性形容词。

## 24. DP3 (RSS 2024)

[3D Diffusion Policy: Generalizable Visuomotor Policy Learning via Simple 3D Representations](https://www.roboticsproceedings.org/rss20/p067.html)

- 主线：紧凑的三维表示结合扩散策略，面向少示范与泛化。
- 组织：示范成本 → 三维设计 → 仿真范围与预算 → 实机预算和泛化轴 → 观察性安全结果。
- 证据：仿真与实机分别交代示范量、任务数和表现，避免把不同实验揉成一个数字。
- 借鉴：少样本主张必须随结果带上数据预算，泛化要指出变化轴。
- 边界：很少违反安全要求是实验观察，不是概率安全证书或所有环境保证。
