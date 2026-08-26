import os
import json
from pathlib import Path
from datetime import datetime

# ============================================
# لیست پوشه‌ها و فایل‌هایی که در خروجی نشان داده نمی‌شوند
# (ابزارهای خودکار و فایل‌های تولیدی خود را اینجا اضافه کنید)
# ============================================
EXCLUDE_DIRS = {
    '.git', '__pycache__', 'node_modules', 'venv', '.idea', '.vscode',
    'docs',           # پوشه‌ای که خروجی‌ها در آن ذخیره می‌شوند
    '.github'         # پوشه‌ی اکشن‌ها (اگر نمی‌خواهید نشان داده شود)
}

EXCLUDE_FILES = {
    '.DS_Store', 'thumbs.db',
    'generate_tree.py',   # خود اسکریپت
    'update_tree.yml',    # فایل تنظیمات اکشن
    'tree_output.txt',
    'PROJECT_STRUCTURE.txt'
}
# ============================================

def get_tree_structure(path, prefix='', is_last=True, output_lines=None):
    if output_lines is None:
        output_lines = []
    
    path = Path(path)
    if path.is_file():
        size = path.stat().st_size
        output_lines.append(f"{prefix}├── {path.name}  ({size} bytes)")
        # (اختیاری) خلاصه‌ای از کدهای فایل‌های خاص
        if path.suffix in ['.py', '.js', '.java', '.cpp', '.h', '.cs', '.go', '.rs']:
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    if lines:
                        preview = ''.join(lines[:3]).strip().replace('\n', ' ')
                        output_lines.append(f"{prefix}│   └── preview: {preview[:80]}...")
            except:
                pass
        return output_lines
    
    # دایرکتوری
    items = list(path.iterdir())
    # فیلتر کردن موارد ناخواسته
    items = [item for item in items 
             if item.name not in EXCLUDE_DIRS and item.name not in EXCLUDE_FILES]
    # مرتب‌سازی: دایرکتوری‌ها اول، سپس فایل‌ها
    dirs = sorted([item for item in items if item.is_dir()], key=lambda x: x.name)
    files = sorted([item for item in items if item.is_file()], key=lambda x: x.name)
    sorted_items = dirs + files
    
    for i, item in enumerate(sorted_items):
        is_last_item = (i == len(sorted_items) - 1)
        if is_last_item:
            output_lines.append(f"{prefix}└── {item.name}")
            new_prefix = prefix + "    "
        else:
            output_lines.append(f"{prefix}├── {item.name}")
            new_prefix = prefix + "│   "
        
        if item.is_dir():
            get_tree_structure(item, new_prefix, is_last_item, output_lines)
        else:
            try:
                size = item.stat().st_size
                output_lines.append(f"{new_prefix}└── size: {size} bytes")
            except:
                pass
    return output_lines

def main():
    root_dir = Path(__file__).parent
    output_dir = root_dir / 'docs' / 'tree'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f'tree_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    latest_file = output_dir / 'latest_tree.txt'
    
    lines = [f"📁 Project Tree - Generated: {datetime.now()}"]
    lines.append("="*50)
    tree_lines = get_tree_structure(root_dir)
    lines.extend(tree_lines)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    with open(latest_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ درخت تولید شد: {output_file}")
    print(f"✅ فایل به‌روز: {latest_file}")

if __name__ == "__main__":
    main()
