import os
import re
from pathlib import Path
from typing import Dict, List, Optional

# Source project path
SOURCE_PATH = r"D:\aloustaz"

# Critical file patterns to search for
CRITICAL_PATTERNS = {
    'theme': [
        'theme.ts', 'theme.js', 'theme.tsx',
        'tailwind.config.js', 'tailwind.config.ts',
        'colors.ts', 'colors.js',
    ],
    'layout': [
        'layout.tsx', 'layout.ts', 'layout.jsx', 'layout.js',
        'Sidebar.tsx', 'Sidebar.ts', 'Sidebar.jsx', 'Sidebar.js',
        'Header.tsx', 'Header.ts', 'Header.jsx', 'Header.js',
        'Navbar.tsx', 'Navbar.ts', 'Navbar.jsx', 'Navbar.js',
        'AppLayout.tsx', 'AppLayout.ts', 'AppLayout.jsx', 'AppLayout.js',
        'DashboardLayout.tsx', 'DashboardLayout.ts',
    ],
    'styles': [
        'globals.css', 'global.css', 'global.scss', 'globals.scss',
        'styles.css', 'index.css',
    ],
    'components': [
        'page.tsx', 'page.ts', 'page.jsx', 'page.js',
        'index.tsx', 'index.ts', 'index.jsx', 'index.js',
    ],
    'config': [
        '_app.tsx', '_app.ts', '_app.jsx', '_app.js',
        '_document.tsx', '_document.ts',
        'providers.tsx', 'providers.ts',
    ],
}

def find_files_recursive(directory: str, patterns: List[str]) -> List[str]:
    """Find files matching patterns recursively."""
    found_files = []
    for root, dirs, files in os.walk(directory):
        # Skip node_modules and hidden directories
        dirs[:] = [d for d in dirs if d not in ['node_modules', '.next', '.git', 'dist', 'build']]
        
        for file in files:
            if file in patterns:
                found_files.append(os.path.join(root, file))
    return found_files

def read_file_content(filepath: str) -> Optional[str]:
    """Read file content with error handling."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(filepath, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            return f"[Error reading file: {e}]"
    except Exception as e:
        return f"[Error reading file: {e}]"

def analyze_project():
    """Main analysis function."""
    print("=" * 80)
    print("SOURCE PROJECT ANALYZER")
    print(f"Analyzing: {SOURCE_PATH}")
    print("=" * 80)
    
    if not os.path.exists(SOURCE_PATH):
        print(f"\n[ERROR] Source path does not exist: {SOURCE_PATH}")
        return
    
    # Get overall directory structure
    print("\n" + "=" * 80)
    print("DIRECTORY STRUCTURE (Top 3 levels)")
    print("=" * 80)
    
    for root, dirs, files in os.walk(SOURCE_PATH):
        level = root.replace(SOURCE_PATH, '').count(os.sep)
        if level < 3:
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files[:10]:  # Limit files shown
                print(f"{subindent}{file}")
            if len(files) > 10:
                print(f"{subindent}... and {len(files) - 10} more files")
            # Skip node_modules and hidden directories
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.next', '.git', 'dist', 'build']]
    
    # Find and read critical files
    print("\n" + "=" * 80)
    print("CRITICAL FILES CONTENT")
    print("=" * 80)
    
    for category, patterns in CRITICAL_PATTERNS.items():
        found = find_files_recursive(SOURCE_PATH, patterns)
        
        if found:
            print(f"\n--- {category.upper()} FILES ---")
            for filepath in found:
                relative_path = os.path.relpath(filepath, SOURCE_PATH)
                print(f"\n[FILE]: {relative_path}")
                print("-" * 60)
                content = read_file_content(filepath)
                if content:
                    print(content[:5000])  # Limit content length
                    if len(content) > 5000:
                        print(f"\n... [TRUNCATED - File has {len(content)} total characters]")
                else:
                    print("[Could not read file content]")

def find_all_tsx_ts_files():
    """Find all TypeScript/JavaScript files for component analysis."""
    print("\n" + "=" * 80)
    print("ALL TSX/TS/JSX/JS FILES")
    print("=" * 80)
    
    extensions = ['.tsx', '.ts', '.jsx', '.js']
    all_files = []
    
    for root, dirs, files in os.walk(SOURCE_PATH):
        dirs[:] = [d for d in dirs if d not in ['node_modules', '.next', '.git', 'dist', 'build']]
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                all_files.append(os.path.join(root, file))
    
    for filepath in all_files[:50]:  # Limit to 50 files
        relative_path = os.path.relpath(filepath, SOURCE_PATH)
        print(f"  {relative_path}")
    
    if len(all_files) > 50:
        print(f"  ... and {len(all_files) - 50} more files")

if __name__ == "__main__":
    analyze_project()
    find_all_tsx_ts_files()
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)