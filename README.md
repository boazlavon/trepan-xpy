# ⚙️ Canonicalized Execution Traces Debugger for Python Runtime

This repository contains a modified version of the [`trepan-xpy`](https://github.com/Trepan-Debuggers/trepan-xpy) debugger, adapted to emit canonicalized execution traces for use in the [EG-CFG project](https://github.com/boazlavon/eg_cfg) (Execution-Guided Classifier-Free Guidance for Code Generation).

The modifications were made by the **EG-CFG Research Team** at **Tel Aviv University** to support dynamic introspection of partially executed Python programs.

---

## 🎯 Purpose of Modifications

In EG-CFG, runtime behavior is used to guide how programs are generated, line by line.  
This requires accurate and structured feedback from partially executed code.

To support this, we extended the `trepan-xpy` debugger to produce:

- **Canonicalized Execution Traces** — a unified, structured representation of runtime behavior:
  - Variable assignments
  - Function calls and returns
  - Bytecode-level instruction steps
  - Control flow transitions

These traces are consumed by external systems (e.g., LLM-based inference frameworks) but this interpreter itself is **model-agnostic** — it focuses solely on producing standardized runtime information.

---

## 🔁 Relationship to EG-CFG

This repository is used as a **submodule** within [EG-CFG](https://github.com/boazlavon/eg_cfg), where it powers the `traces_dumper/` component.  
EG-CFG uses the canonical trace outputs to guide code generation in external large language models.

> For full integration details, see Section 3 of the EG-CFG paper.

---

## 🛠️ Modification Summary
- Extended trace emitter to output a canonical format
---

## 📜 License

This repository includes code originally licensed under the **GNU General Public License v3 (GPLv3)**.  
All modifications made by the EG-CFG Research Team are also licensed under GPLv3, in accordance with the original terms.

- Original license: [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)
> 🧠 **Note:** Only this submodule — and its modifications — are governed by GPLv3.  
> The main EG-CFG project is licensed separately under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

---

## 👥 Attribution

Modifications © 2025 **EG-CFG Research Team**, Tel Aviv University  
For licensing inquiries, contact [yair.eran@ramot.org](mailto:yair.eran@ramot.org)

