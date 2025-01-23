import os
from pathlib import Path
from typing import Dict, Tuple

EXCLUDE_DIRS = {'venv', '.git', '__pycache__', 'build', 'dist'}

def count_lines(directory: str) -> Tuple[int, Dict[str, int]]:
    """Count lines of Python code in the project"""
    total_lines = 0
    file_counts = {}
    
    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if file.endswith('.py'):
                try:
                    path = os.path.join(root, file)
                    if os.path.exists(path):  # Verify file exists
                        with open(path, 'r', encoding='utf-8') as f:
                            lines = len(f.readlines())
                            rel_path = os.path.relpath(path, directory)
                            file_counts[rel_path] = lines
                            total_lines += lines
                except Exception as e:
                    print(f"Warning: Could not read {file}: {str(e)}")
    
    return total_lines, file_counts

def format_output(file_counts: Dict[str, int], project_root: str) -> str:
    """Format the LOC count output"""
    sections = {
        'src/agent': [],
        'src/utils': [],
        'src/services': [],
        'src/models': [],
        'src/config': [],
        'root': []
    }
    
    # Group files by section
    for file_path, count in file_counts.items():
        matched = False
        for section in sections.keys():
            if section != 'root' and file_path.startswith(section):
                sections[section].append((file_path, count))
                matched = True
                break
        if not matched:
            sections['root'].append((file_path, count))
    
    # Format output
    output = ["# Bible Study Assistant - Code Statistics\n"]
    total = sum(file_counts.values())
    
    for section, files in sections.items():
        if files:
            section_total = sum(count for _, count in files)
            output.append(f"\n## {section.replace('src/', '').title()} Components ({section_total} lines)")
            for file_path, count in sorted(files):
                output.append(f"- {file_path}: {count} lines")
    
    output.append(f"\n## Total Project Size: {total} lines of Python code")
    return '\n'.join(output)

if __name__ == '__main__':
    try:
        project_root = Path(__file__).parent
        print(f"\nCounting Python files in: {project_root}")
        print("(excluding venv, git, and cache directories)")
        print("-" * 50)
        
        total, file_counts = count_lines(str(project_root))
        print(format_output(file_counts, str(project_root)))
    except Exception as e:
        print(f"Error counting lines: {str(e)}")