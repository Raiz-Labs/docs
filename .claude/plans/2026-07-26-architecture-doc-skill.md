# architecture-doc skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a Claude Code skill, `architecture-doc`, that generates `projects/<slug>/architecture/architecture.md` (arc42 structure, Mermaid C4 diagrams) from a project's PRD, asking only for gaps, and proposes ADR stubs for decisions the PRD leaves open.

**Architecture:** Two files: a stdlib-only Python script that extracts plain text from `.docx` PRDs (no `pandoc`/`python-docx` dependency), and a `SKILL.md` that Claude follows to read the PRD, map it to arc42 sections, fill gaps interactively, emit Mermaid C4 diagrams, and write ADR stubs from the existing `templates/ADR-template.md`.

**Tech Stack:** Python 3 stdlib (`zipfile`, `re`, `html`) for the docx extractor. No new dependencies.

## Global Constraints

- No new dependencies — Python stdlib only for the docx extractor (spec: "Não gera diagramas C4 a partir de código-fonte... Não usa PlantUML/Structurizr").
- Diagrams: Mermaid C4 (`C4Context`, `C4Container`), embedded directly in the markdown.
- Output: one `architecture.md` per project — not 12 separate arc42 files.
- The skill only asks the user about arc42 sections the PRD doesn't already cover.
- ADR stubs are created only after user confirmation, using `templates/ADR-template.md` verbatim as the base, numbered `NNNN-titulo-curto.md` starting at `0001` per project.
- Skill lives at `docs/.claude/skills/architecture-doc/` (project-scoped, versioned with the repo).

---

### Task 1: docx text extractor

**Files:**
- Create: `.claude/skills/architecture-doc/scripts/extract_docx_text.py`

**Interfaces:**
- Produces: `extract_text(docx_path: str) -> str` — importable, and also runnable as a CLI: `python3 extract_docx_text.py <path>` prints extracted text to stdout; `python3 extract_docx_text.py --selftest` runs the embedded self-check and prints `self-test OK` on success, exits non-zero on failure.

- [ ] **Step 1: Write the script with a self-test harness, `extract_text` unimplemented**

```python
#!/usr/bin/env python3
"""Extract plain text from a .docx file's word/document.xml, stdlib only."""
import html
import io
import re
import sys
import zipfile


def extract_text(docx_path: str) -> str:
    raise NotImplementedError


def _demo() -> None:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr(
            "word/document.xml",
            "<w:document><w:body>"
            "<w:p><w:r><w:t>Ol&#225; mundo</w:t></w:r></w:p>"
            "<w:p><w:r><w:t>Segunda linha</w:t></w:r></w:p>"
            "</w:body></w:document>",
        )
    tmp_path = "/tmp/_architecture_doc_selftest.docx"
    with open(tmp_path, "wb") as f:
        f.write(buf.getvalue())

    result = extract_text(tmp_path)
    assert "Olá mundo" in result, f"missing greeting, got: {result!r}"
    assert "Segunda linha" in result, f"missing second line, got: {result!r}"
    assert result.index("Olá mundo") < result.index("Segunda linha"), "line order wrong"
    print("self-test OK")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        _demo()
    elif len(sys.argv) == 2:
        print(extract_text(sys.argv[1]))
    else:
        print("usage: extract_docx_text.py <path.docx> | --selftest", file=sys.stderr)
        sys.exit(1)
```

- [ ] **Step 2: Run the self-test to verify it fails**

Run: `python3 .claude/skills/architecture-doc/scripts/extract_docx_text.py --selftest`
Expected: traceback ending in `NotImplementedError`

- [ ] **Step 3: Implement `extract_text`**

Replace the `raise NotImplementedError` body with:

```python
def extract_text(docx_path: str) -> str:
    with zipfile.ZipFile(docx_path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    text = re.sub(r"<w:p[ >]", "\n", xml)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()
```

- [ ] **Step 4: Run the self-test to verify it passes**

Run: `python3 .claude/skills/architecture-doc/scripts/extract_docx_text.py --selftest`
Expected: prints `self-test OK`, exit code 0

- [ ] **Step 5: Sanity-check against the real PRD already in the repo**

Run: `python3 .claude/skills/architecture-doc/scripts/extract_docx_text.py projects/porteira-aberta-ai/prds/PRD_PorteiraAbertaAI_v1.docx | head -20`
Expected: readable Portuguese text starting with "Porteira Aberta AI" / "PRD — Documento de Requisitos de Produto" (same content already seen manually in this session)

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/architecture-doc/scripts/extract_docx_text.py
git commit -m "Add stdlib docx text extractor for architecture-doc skill"
```

---

### Task 2: SKILL.md

**Files:**
- Create: `.claude/skills/architecture-doc/SKILL.md`

**Interfaces:**
- Consumes: `.claude/skills/architecture-doc/scripts/extract_docx_text.py` (Task 1) for `.docx` PRDs.
- Consumes: `templates/ADR-template.md` (already in repo) as the base for ADR stubs.
- Produces: `projects/<slug>/architecture/architecture.md` and, on confirmation, `projects/<slug>/architecture/adr/NNNN-titulo-curto.md` files.

- [ ] **Step 1: Write the skill file**

```markdown
---
name: architecture-doc
description: Use when creating or updating a project's architecture.md in this docs repo. Generates an arc42-structured document with Mermaid C4 diagrams from the project's PRD, asking only for what the PRD doesn't cover, and proposes ADR stubs for decisions the PRD leaves open. Triggers on "criar arquitetura", "gerar architecture.md", "arc42", "C4 model" for a project under projects/.
argument-hint: "<project-slug>"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

<objective>
Generate `projects/<slug>/architecture/architecture.md` for the project named in `$ARGUMENTS`, following the arc42 template (12 sections) with Mermaid C4 diagrams, sourced primarily from the project's PRD(s) in `projects/<slug>/prds/`. Ask the user only for what the PRD doesn't cover. Propose ADR stubs (from `templates/ADR-template.md`) for decisions the PRD leaves open.
</objective>

<preconditions>
- `$ARGUMENTS` must name an existing `projects/<slug>/` directory. If it doesn't exist, stop and tell the user to create the project first — this skill does not create projects.
- If `projects/<slug>/architecture/architecture.md` already exists, ask the user: overwrite, merge (keep existing section content where the PRD has nothing new to add), or cancel.
</preconditions>

<steps>

1. **Locate and read the PRD.**
   - List `projects/<slug>/prds/`. If empty, skip to step 3 with no PRD text — every arc42 section will need a question.
   - If more than one file, use the one with the most recent mtime (`ls -t`) and tell the user which file was picked and why.
   - `.md` files: read directly.
   - `.docx` files: run `python3 .claude/skills/architecture-doc/scripts/extract_docx_text.py <path>` and use its stdout as the PRD text.

2. **Map PRD content to the 12 arc42 sections** (see `<arc42-sections>`). For each section, decide: covered by the PRD, or a gap.

3. **Fill gaps interactively.** One focused question per gap, one at a time. Use `AskUserQuestion` when the answer has enumerable options; ask directly otherwise. Never ask about something the PRD already answers.

4. **Generate Mermaid C4 diagrams**: at minimum a Context diagram (arc42 §3) and a Container diagram (arc42 §5), built from the stack/entities identified in the PRD or gathered in step 3. Use `C4Context` / `C4Container` syntax — see `<mermaid-c4-example>`.

5. **Detect open decisions and propose ADR stubs.** Scan the PRD text for markers of an unresolved technical decision: phrases like "decisão pendente", "a definir", "TBD", or a sentence ending in "?" near words like "arquitetura", "stack", "banco", "perfil". For each match found, show the surrounding sentence to the user and ask for confirmation before creating anything. On confirmation:
   - Find the next ADR number in `projects/<slug>/architecture/adr/` — 4-digit zero-padded, starting at `0001`.
   - Copy `templates/ADR-template.md` to `projects/<slug>/architecture/adr/NNNN-<titulo-curto>.md`, fill in the title and set status to `proposto`, and put the PRD's own wording about the open question into the "Contexto" section.

6. **Write `projects/<slug>/architecture/architecture.md`** using `<architecture-template>`, filled with the content from steps 2-4.

7. **Summarize**: list what was written, and list any ADR stubs created that still need a decision.

</steps>

<arc42-sections>
1. Introdução e Metas — objetivo do sistema, requisitos essenciais, stakeholders.
2. Restrições de Arquitetura — restrições técnicas, organizacionais, regulatórias.
3. Escopo e Contexto do Sistema — fronteira do sistema, quem/o que interage com ele (vira o diagrama de Contexto C4).
4. Estratégia de Solução — decisões tecnológicas de alto nível e por quê.
5. Visão de Building Blocks — decomposição em módulos/serviços (vira o diagrama de Container C4).
6. Visão de Runtime — fluxos principais (ex: uma jornada de usuário ponta a ponta).
7. Visão de Deployment — onde e como o sistema roda em produção.
8. Conceitos Transversais — segurança, autenticação, tratamento de erros, i18n, etc.
9. Decisões de Arquitetura — lista as ADRs (com link pra `architecture/adr/`).
10. Requisitos de Qualidade — atributos de qualidade priorizados, com métricas quando existirem.
11. Riscos e Dívida Técnica — riscos conhecidos e mitigação.
12. Glossário — termos do domínio.
</arc42-sections>

<mermaid-c4-example>
\`\`\`mermaid
C4Context
    Person(user, "Nome do papel", "Como usa o sistema")
    System(app, "Nome do Sistema", "O que o sistema faz")
    System_Ext(ext, "Serviço externo", "Ex: API de terceiro")
    Rel(user, app, "Usa")
    Rel(app, ext, "Chama")
\`\`\`
</mermaid-c4-example>

<architecture-template>
\`\`\`markdown
# Arquitetura — <Nome do Projeto>

- **Status**: rascunho
- **Data**: <data de hoje>
- **PRD de origem**: `projects/<slug>/prds/<arquivo>`

## 1. Introdução e Metas

## 2. Restrições de Arquitetura

## 3. Escopo e Contexto do Sistema

\`\`\`mermaid
C4Context
\`\`\`

## 4. Estratégia de Solução

## 5. Visão de Building Blocks

\`\`\`mermaid
C4Container
\`\`\`

## 6. Visão de Runtime

## 7. Visão de Deployment

## 8. Conceitos Transversais

## 9. Decisões de Arquitetura

Ver `architecture/adr/`.

| ADR | Título | Status |
|---|---|---|

## 10. Requisitos de Qualidade

## 11. Riscos e Dívida Técnica

## 12. Glossário
\`\`\`
</architecture-template>
```

- [ ] **Step 2: Validate frontmatter and required sections are present**

Run:
```bash
head -1 .claude/skills/architecture-doc/SKILL.md
grep -c '^name: architecture-doc$' .claude/skills/architecture-doc/SKILL.md
grep -c '^argument-hint:' .claude/skills/architecture-doc/SKILL.md
grep -c '<arc42-sections>' .claude/skills/architecture-doc/SKILL.md
grep -c '<architecture-template>' .claude/skills/architecture-doc/SKILL.md
```
Expected: first command prints `---`; each `grep -c` prints `1`.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/architecture-doc/SKILL.md
git commit -m "Add architecture-doc skill definition"
```

---

### Task 3: End-to-end verification against the real project

**Files:** none created — this is a manual/agentic dry run of Tasks 1-2 combined.

**Interfaces:**
- Consumes: `/architecture-doc porteira-aberta-ai` (the skill from Task 2, which calls the script from Task 1).

- [ ] **Step 1: Invoke the skill**

In a Claude Code session at the repo root, run: `/architecture-doc porteira-aberta-ai`

- [ ] **Step 2: Answer the gap-filling questions as they appear**

Expected: questions only appear for arc42 sections the PRD (`projects/porteira-aberta-ai/prds/PRD_PorteiraAbertaAI_v1.docx`) doesn't already cover — most sections (stack, DB schema, RBAC, MVP scope) should NOT trigger a question since the PRD already has them (sections 8, 9 of the PRD).

- [ ] **Step 3: Confirm the ADR stub prompt for the known open decision**

Expected: the skill flags the PRD's own "Decisão de produto pendente: a arquitetura multi-perfil deve ser construída no Sprint 1..." line (PRD §13) and asks for confirmation to create an ADR stub. Confirm it.

- [ ] **Step 4: Verify the generated files**

Run:
```bash
test -f projects/porteira-aberta-ai/architecture/architecture.md && echo "architecture.md OK"
ls projects/porteira-aberta-ai/architecture/adr/
grep -c '^## 9' projects/porteira-aberta-ai/architecture/architecture.md
grep -c 'C4Context' projects/porteira-aberta-ai/architecture/architecture.md
grep -c 'C4Container' projects/porteira-aberta-ai/architecture/architecture.md
```
Expected: `architecture.md OK`; one `NNNN-*.md` file listed in `adr/`; each `grep -c` prints `1` or more.

- [ ] **Step 5: Read through `architecture.md` and the new ADR stub for accuracy**

Confirm the content reflects the actual PRD (stack: React/Vite, Node/Express, Claude Vision API, Supabase; DB tables from PRD §8.3; RBAC roles from §8.4) — not generic placeholder text.

- [ ] **Step 6: Commit the generated docs**

```bash
git add projects/porteira-aberta-ai/architecture/
git commit -m "Generate architecture.md for Porteira Aberta AI via architecture-doc skill"
git push
```

---

## Self-Review Notes

- **Spec coverage**: docx extraction (Task 1) ✅, arc42 mapping + gap questions (Task 2 steps 1-3) ✅, Mermaid C4 (Task 2 step 4, Task 3 step 4) ✅, ADR stub proposal on confirmation (Task 2 step 5, Task 3 step 3) ✅, single `architecture.md` output (Task 2 step 6) ✅, existing-file overwrite/merge/cancel precondition ✅, no-PRD fallback (step 1 of skill) ✅, multi-PRD mtime tie-break ✅.
- **Placeholder scan**: none — script and skill file are both given in full; verification steps use real repo content (the Porteira Aberta AI PRD already committed) rather than synthetic fixtures, except the self-test in Task 1 which needs a minimal in-memory docx and is fully spelled out.
- **Type consistency**: `extract_text(docx_path: str) -> str` is defined once (Task 1) and referenced identically in Task 2's skill text and Task 3's verification.
