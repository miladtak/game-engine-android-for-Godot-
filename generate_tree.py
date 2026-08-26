import os
import json
from pathlib import Path
from datetime import datetime

# پوشه‌هایی که نباید اسکن شوند (مثل .git, node_modules, etc.)
EXCLUDE_DIRS = {'.git', '__pycache__', 'node_modules', 'venv', '.idea', '.vscode'}
EXCLUDE_FILES = {'.DS_Store', 'generate_tree.py', 'tree_output.txt'}

def get_tree_structure(path, prefix='', is_last=True, output_lines=None):
    """ایجاد نمودار درختی با حروف چاپی"""
    if output_lines is None:
        output_lines = []
    
    path = Path(path)
    if path.is_file():
        # اطلاعات فایل را هم اضافه می‌کنیم
        size = path.stat().st_size
        output_lines.append(f"{prefix}├── {path.name}  ({size} bytes)")
        # می‌توانید محتوای کوتاهی از فایل‌های خاص (مثل .py) اضافه کنید
        if path.suffix in ['.py', '.js', '.java', '.cpp', '.h', '.cs']:
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    if lines:
                        # خلاصه ۳ خط اول
                        preview = ''.join(lines[:3]).strip().replace('\n', ' ')
                        output_lines.append(f"{prefix}│   └── preview: {preview[:80]}...")
            except:
                pass
        return output_lines
    
    # اگر دایرکتوری است
    items = list(path.iterdir())
    # فیلتر کردن موارد ناخواسته
    items = [item for item in items if item.name not in EXCLUDE_DIRS and item.name not in EXCLUDE_FILES]
    # مرتب‌سازی: دایرکتوری‌ها اول، سپس فایل‌ها
    dirs = sorted([item for item in items if item.is_dir()], key=lambda x: x.name)
    files = sorted([item for item in items if item.is_file()], key=lambda x: x.name)
    sorted_items = dirs + files
    
    for i, item in enumerate(sorted_items):
        is_last_item = (i == len(sorted_items) - 1)
        # انتخاب علامت مناسب
        if is_last_item:
            output_lines.append(f"{prefix}└── {item.name}")
            new_prefix = prefix + "    "
        else:
            output_lines.append(f"{prefix}├── {item.name}")
            new_prefix = prefix + "│   "
        
        # بازگشت به داخل
        if item.is_dir():
            get_tree_structure(item, new_prefix, is_last_item, output_lines)
        else:
            # اطلاعات بیشتری برای فایل‌ها (مثل حجم و خلاصه)
            try:
                size = item.stat().st_size
                output_lines.append(f"{new_prefix}└── size: {size} bytes")
            except:
                pass
    return output_lines

def main():
    # مسیر ریشه پروژه (جایی که اسکریپت قرار دارد)
    root_dir = Path(__file__).parent
    output_dir = root_dir / 'docs' / 'tree'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f'tree_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    # همچنین یک فایل با نام ثابت برای همیشه به‌روز
    latest_file = output_dir / 'latest_tree.txt'
    
    # تولید درخت
    lines = [f"Project Tree Structure - Generated: {datetime.now()}"]
    lines.append("="*50)
    tree_lines = get_tree_structure(root_dir)
    lines.extend(tree_lines)
    
    # ذخیره در فایل‌ها
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    with open(latest_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ Tree generated: {output_file}")
    print(f"✅ Latest tree updated: {latest_file}")

if __name__ == "__main__":
    main()
