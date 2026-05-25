#!/usr/bin/env python3
"""
🧠 Agent Memory Architecture — Archive Script

Moves old dated entries from MEMORY.md/USER.md to ~/details/archive/
with full text preservation + searchable index.

Inspired by 2025 Cell paper on norepinephrine-driven glymphatic clearance
during NREM sleep: low-frequency pulsed cleaning, separation of work and rest.
"""

import re, os
from pathlib import Path
from datetime import datetime, timedelta

# === Configuration ===

HERMES_HOME = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
MEMORY_FILE = HERMES_HOME / "memories" / "MEMORY.md"
USER_FILE = HERMES_HOME / "memories" / "USER.md"
ARCHIVE_DIR = Path.home() / "details" / "archive"
ARCHIVE_AFTER_DAYS = 14  # Archive entries older than this
DELIM = "\n§\n"          # Entry delimiter

# === Topic Classification ===
# Customize these keywords to match your domain.

TOPIC_KEYWORDS = {
    "项目": [],
    "客户": [],
    "财务": ["账单", "支出", "预算", "合同"],
    "事件": [],
    "技术": [],
    "法务": [],
    "生活": [],
}

def extract_topics(text: str) -> list:
    topics = []
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            topics.append(topic)
    return topics

def extract_search_terms(text: str) -> str:
    clean = re.sub(r'\d{4}[-年]\d{1,2}[-月]\d{1,2}[日]?', '', text)
    return clean.strip()[:80]

# === Date Detection ===

DATE_PATTERNS = [
    (r'(\d{4})-(\d{2})-(\d{2})', lambda m: (int(m[1]), int(m[2]), int(m[3]))),
    (r'(\d{4})年(\d{1,2})月(\d{1,2})日', lambda m: (int(m[1]), int(m[2]), int(m[3]))),
]

def extract_date(text: str):
    for pat, parser in DATE_PATTERNS:
        m = re.search(pat, text)
        if m:
            try:
                y, mo, d = parser(m.groups())
                return datetime(y, mo, d)
            except:
                pass
    return None

def should_archive(entry: str) -> bool:
    now = datetime.now()
    dt = extract_date(entry)
    return dt is not None and (now - dt) > timedelta(days=ARCHIVE_AFTER_DAYS)

# === Section Protection ===

SECTION_HEADER_RE = re.compile(r'^={2,5}\s*(.+?)\s*={2,5}$')

PROTECTED_PREFIXES = [
    "=",           # section headers
    "管理:",       # behavioral rules
]

PROTECTED_PATTERNS = [
    "-> details/",
    "-> skill:",
    "=>",
]

def is_protected(entry: str) -> bool:
    text = entry.strip()
    if not text:
        return True
    if SECTION_HEADER_RE.match(text):
        return True
    if any(text.startswith(p) for p in PROTECTED_PREFIXES):
        return True
    if any(p in text for p in PROTECTED_PATTERNS):
        return True
    return False

# === Archive File Management ===

def append_entries_to_archive(entries: list, source_label: str) -> Path:
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    archive_file = ARCHIVE_DIR / f"{source_label}.md"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open(archive_file, "a", encoding="utf-8") as f:
        f.write(f"\n\n--- 归档于 {now_str} ---\n\n")
        for entry in entries:
            topics = extract_topics(entry)
            terms = extract_search_terms(entry)
            tags = " / ".join(topics) if topics else "未分类"
            f.write(f"> [{tags}] {terms}\n\n")
            f.write(entry.strip())
            f.write("\n\n§\n\n")
    return archive_file

def update_readme(entries: list, source_label: str, archive_file: Path):
    readme = ARCHIVE_DIR / "README.md"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    rel_path = archive_file.name

    index_lines = []
    for entry in entries:
        topics = extract_topics(entry)
        terms = extract_search_terms(entry)
        tags = " / ".join(topics) if topics else "未分类"
        title = entry.strip().split('\n')[0][:60]
        index_lines.append(
            f"  - `{title}` [{tags}] → `{rel_path}` (搜: {terms})"
        )

    batch = [
        f"\n### {now_str} — 来自 {source_label} ({len(entries)} 条)",
        *index_lines,
    ]

    if readme.exists():
        content = readme.read_text(encoding="utf-8")
    else:
        content = "# 📚 记忆归档索引\n\n" + \
            "每次归档自动生成索引，用 `grep` 或 `ripgrep` 搜索关键词即可定位。\n\n---\n"

    content += "\n".join(batch) + "\n\n---\n"
    readme.write_text(content, encoding="utf-8")

# === Main ===

def process_file(filepath: Path, source_label: str) -> bool:
    if not filepath.exists():
        return False

    content = filepath.read_text(encoding="utf-8")
    entries = content.split(DELIM)

    keep = []
    archive = []

    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        if is_protected(entry):
            keep.append(entry)
            continue
        if should_archive(entry):
            archive.append(entry)
            title = entry.strip().split('\n')[0][:60]
            print(f"  [ARCHIVE] {title}...")
        else:
            keep.append(entry)

    if not archive:
        return False

    filepath.write_text(DELIM.join(keep) + ("\n" if keep else ""), encoding="utf-8")
    archive_file = append_entries_to_archive(archive, source_label)
    update_readme(archive, source_label, archive_file)
    return True

def main():
    print(f"📚 记忆归档 — 查找 {ARCHIVE_AFTER_DAYS} 天前的旧事件")
    print()

    changed = False
    for fname, label in [("MEMORY.md", "memory"), ("USER.md", "user")]:
        fpath = HERMES_HOME / "memories" / fname
        print(f"{fname}:")
        if process_file(fpath, label):
            changed = True
        else:
            print("  无过期条目")

    print()
    if changed:
        print(f"已归档到 {ARCHIVE_DIR}/")
        print(f"索引在 {ARCHIVE_DIR}/README.md — grep 即可找回")
    else:
        print("一切干净。")

if __name__ == "__main__":
    main()
