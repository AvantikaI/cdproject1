# 🔍 cdproject1 — Language-Specific Static Analyzer

A Python-driven static analysis tool tailored for Java source files.  
Designed to detect code smells, style issues, and potential bugs using AST parsing and custom analysis rules.

## 🛠️ Project Overview

- **Input:** One or more Java `.java` source files or directories.
- **Process:** Parses Java files into ASTs, applies language-specific checks.
- **Output:** Reports issues such as:
  - Code smells (long methods, deep nesting)
  - Unused imports
  - Naming style violations
  - Complexity thresholds exceeded
  - Missing Javadoc comments

## 🚧 Features

- ✅ Lightweight, Python-native solution
- ✅ Modular rule-based analyzer
- ✅ Configurable thresholds & filters
- ✅ Supports both file and folder input
- ✅ Outputs console-friendly reports (+ optional JSON export)

## 🧩 Architecture

1. **Parser Module** — Converts Java source into tree structure.
2. **Rule Engine** — Applies each static-analysis rule.
3. **Reporter Module** — Formats results in text or JSON.

## 🔧 Installation

```bash
git clone https://github.com/AvantikaI/cdproject1.git
cd cdproject1
pip install -r requirements.txt
