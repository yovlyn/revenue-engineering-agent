import os

# امتدادات الملفات البرمجية التي تريد تضمينها
VALID_EXTENSIONS = ('.py', '.json', '.md', '.yml', '.yaml', '.txt')
OUTPUT_FILE = 'project_combined.txt'

def merge_code():
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk('.'):
            # استثناء المجلدات غير المرغوب فيها مثل git أو venv أو pycache
            if '.git' in root or '__pycache__' in root or 'venv' in root:
                continue
            
            for file in files:
                if file.endswith(VALID_EXTENSIONS) and file != OUTPUT_FILE and file != 'merge_code.py':
                    file_path = os.path.join(root, file)
                    outfile.write(f"\n\n=== FILE: {file_path} ===\n\n")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(infile.read())
                    except Exception as e:
                        outfile.write(f"[Error reading file: {e}]")
                        
    print(f"تم دمج جميع الملفات بنجاح في: {OUTPUT_FILE}")

if __name__ == '__main__':
    merge_code()
