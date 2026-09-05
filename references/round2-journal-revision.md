# Round 2: Journal-Conformity Revision — Detailed Instructions

## Contents
- Phase 0: The Three R's (CASPArS method)
- Phase 1: Build Style Conformity Checklist
- Phase 2: Checklist-Driven Revision

---

## Phase 0: The Three R's — Corpus-Based Style Calibration

Use the available deep-read papers as a small, task-matched corpus. For a conference
paper, select examples of the same paper type and stage rather than transferring
journal conventions unchanged. Corpus observations are soft guidance; official
rules, the author's meaning, evidence strength and technical terminology take priority.

**R1 — Recalibration**: Align word usage with field standards.
- Compare your Round 1 draft against all 3 journal papers for each key term
- Compare how words function in context, not whether their frequencies match.
  Do not replace "show" with "demonstrate" merely because it is more frequent.
- Check: verb+noun pairs, adjective+noun pairs, preposition choices

**R2 — Replacement**: Choose context-appropriate alternatives.
- For overused or non-standard words, use the journal papers' concordance to find field-preferred synonyms
- Example: if our draft says "important" 20× but journal papers use "critical", "essential", "fundamental", "central" contextually, replace accordingly
- Pay special attention to: hedging verbs (suggest vs. indicate vs. demonstrate), connectors (however vs. nevertheless vs. that said), intensifiers (notably vs. particularly vs. especially)

**R3 — Redevelopment**: Holistic revision from corpus insights.
- Read the revised draft alongside a randomly selected journal paper
- If the two texts feel like different journals, identify WHY at sentence and paragraph level
- Fix: sentence rhythm, paragraph density, transition patterns

**Output**: Save Three R's analysis in `restructuring_notes.md`:

| R | Target Word/Pattern | Our Usage | Journal Consensus | Action |
|---|---------------------|-----------|-------------------|--------|
| R1 | "show" vs "demonstrate" | Repeated "show" | Different verbs used for different evidence | Change only where the meaning and evidence support it |
| R2 | "important" | 20× | varied: "critical", "essential" | Diversify |
| R3 | sentence rhythm | avg 28 words/sentence | avg 22 words/sentence | Split longer sentences |

---

## Phase 1: Build the Style Conformity Checklist

From the 3 journal papers' Pass 2 and Pass 3 outputs, build a specific checklist:

```markdown
## Style Conformity Checklist

### Structural
- [ ] Section order matches journal convention [specify]
- [ ] Section allocation fits the paper's argument, evidence and official page budget
- [ ] Abstract format: [structured/unstructured, N words max]
- [ ] Introduction length: [N words target]

### Openings/Closings
- [ ] Abstract opens like journal consensus: [pattern]
- [ ] Introduction opens like journal consensus: [pattern]
- [ ] Discussion opens like journal consensus: [pattern]
- [ ] Each section closes like journal consensus: [pattern]

### Claims
- [ ] Every claim's strength follows its supporting evidence, not corpus averages
- [ ] Hedging states the specific uncertainty or scope boundary

### Terminology
- [ ] Established technical terms are used consistently and correctly
- [ ] New or paper-specific terms are defined clearly, even when absent from the corpus

### Citations
- [ ] Citation density within journal range (N-N cites/page)
- [ ] Citation placement matches journal convention
- [ ] Reference format matches journal's bst/style

### Figures/Tables
- [ ] Captions use journal-consensus style
- [ ] Figure callouts match journal convention
- [ ] Table formatting matches journal convention

### Supplementary
- [ ] Supplementary material policy followed
```

---

## Phase 2: Checklist-Driven Revision

For each section, process in order:
1. Read the current draft section
2. Reference the relevant journal papers' corresponding sections (from Pass 2)
3. Identify deviations from the checklist
4. Rewrite to conform, explicitly addressing each checklist item
5. Mark checklist items as done

Output: `revision_2_journal_style.md` + completed checklist in `restructuring_notes.md`.
