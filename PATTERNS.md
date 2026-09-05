# PaperSpine 设计模式提炼

> 来源：WUBING2023/PaperSpine（MIT，2026-06-11 吸收）。
> 以下模式可被其他写作类 skill 借鉴，不限于本 skill 内部使用。

## 1. Motivation Gate（动机硬门禁）

写作前强制产出 `motivation_options_after_research.md`（调研后的候选动机表），
停下等用户选择/修改，确认后落盘 `confirmed_motivation.md`（含被拒选项、范围
边界、禁止的过度声明）。动机必须克制：窄贡献就承认窄，不膨胀成多 claim。

适用：任何"先写再说"容易跑偏的生成任务（论文、提案、专利、长报告）。

## 2. Writing Rationale Matrix（写作理由矩阵）

把"为什么这样写"前置为逐单元执行计划表：每行 = 一个最小写作单元，
列 = 功能 / 动机链接 / 学到的样例模式 / 场景规范 / 证据锚点 / 计划改动 / 验收检查。
首行必须论证全文框架。浅行（"提升清晰度"）即失败信号，触发回炉。

适用：替代"先写后审"的事后质检，把审查左移到计划层。

## 3. 双轨文献（Exemplar Learning vs Citation Bank 分离）

- 样例论文（3-6 篇）只用于学结构与修辞 → `exemplar_learning_dossier.md` + `style_profile.md`
- 引用支持库独立构建：候选池 = 3x 目标数，约 80% 近三年，每条绑定 1-2 个
  可直接支撑正文的句子级 claim，经 Crossref 验证后才可入正文，存疑标 `[VERIFY]`。

适用：消除"引用既当样例又当证据"的混用，降低幻觉引用率。

## 4. Original Logic Map → Rewrite Matrix → Logic Transfer Audit

改写不是改句子：先映射原文逻辑（每单元的角色/证据/问题/处置决策），
再用矩阵规划新结构，最后审计逻辑迁移完整性（原文的论证是否都被继承或显式放弃）。

适用：论文大修、重投改版（可与 resubmit-pipeline 配合）。

## 5. Scene-Adaptive Units（场景自适应单元拆分）

拒绝万能 IMRaD：journal/conference/report_review/competition 各有单元词汇表
（竞赛 = 问题重述/假设/建模/求解/检验/灵敏度），由 `references/scenario-*.md` 驱动。

适用：课程报告、数模竞赛、综述等非标准论文场景。

## 6. Teaching Audit（教学式审计报告）

`integrity_audit.py` 的每条发现都带四元组：根因 / 修复动作 / 下游影响 / 教学说明。
审计不只拦截，还教用户为什么错。BLOCKED 是编译硬门禁。

适用：所有 guard 类脚本的报告格式。

## 7. Branch-Owned Artifacts（产物归属分支，坏件回炉）

每个产物有唯一拥有者分支；终审发现某产物弱时路由回该分支重做，
禁止直接在最终论文上打补丁。

适用：多阶段流水线的返工策略（与 auto_phd / paper-writing 的阶段回退一致）。

## 8. Generation-Time Humanize（生成时人化约束）

按 D1 句长分布 / D2 段落结构 / D3 信息密度 / D4 连接词频率 / D5 术语-语境匹配
五个检测维度，分 light/medium/heavy 三档在写作时施加约束，每个改动记录进
`humanize_matrix.md`（教学列说明检测器为何会标记该模式）。
与事后扫描类工具（text-deai-check）互补。

## 9. Deterministic Guards（确定性守卫脚本）

LLM 自评不可信的环节用纯 stdlib Python 脚本兜底：产物齐全性、矩阵深度、
引用覆盖率、DOI 验真、LaTeX 结构、Word 宏残留、翻译逐行覆盖率。
脚本输出 markdown 报告 + 退出码，可被流水线门禁消费。
