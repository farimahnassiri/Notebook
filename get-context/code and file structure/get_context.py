import os

def get_file_structure(root_dir):
    file_structure = []
    files_content = []
    
    for subdir, _, files in os.walk(root_dir):
        if 'node_modules' in subdir or 'public' in subdir or 'package' in subdir:
            continue
        
        for file in files:
            if file == '.DS_Store':
                continue
            
            file_path = os.path.join(subdir, file)
            relative_path = os.path.relpath(file_path, root_dir)
            
            if file.lower().endswith(('.ico', '.svg', '.jpeg', '.png', '.jpg')):
                file_structure.append(relative_path)
            elif 'src/app' in relative_path:  # Only include files in src/app
                # Add text-based files to file structure and contents
                file_structure.append(relative_path)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()
                    files_content.append((relative_path, file_content))
    
    return file_structure, files_content

def write_context_file(file_structure, files_content, output_file):
    total_files = len(file_structure)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("===================================================================\n")
        f.write("                   FILES & FOLDER STRUCTURE\n")
        f.write("===================================================================\n\n")
        
        tree = {}
        
        for path in file_structure:
            parts = path.split(os.sep)
            current_level = tree
            for part in parts:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
        
        def write_tree(level, indent=""):
            for name, subtree in level.items():
                if subtree:
                    f.write(f"{indent}+ {name}/\n")
                    write_tree(subtree, indent + "  ")
                else:
                    f.write(f"{indent}  - {name}\n")
        
        write_tree(tree)
        
        f.write("\n")
        f.write(f"===== TOTAL FILES: {total_files} =====\n\n")
        
        for path, content in files_content:
            f.write("===================================================================\n")
            f.write(f"FILE PATH: {path}\n")
            f.write("===================================================================\n\n")
            f.write(content)
            f.write("\n// END OF FILE\n\n")

def update_gitignore(root_dir, script_name, output_file):
    gitignore_path = os.path.join(root_dir, '.gitignore')
    entries_to_add = [
        f'\n# Ignore {script_name} and its output',
        script_name,
        output_file
    ]
    
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r+', encoding='utf-8') as f:
            content = f.read()
            if not any(entry in content for entry in entries_to_add[1:]):
                f.seek(0, 2)  # Move to the end of the file
                f.write('\n'.join(entries_to_add))
    else:
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(entries_to_add))
    
    print(f"Updated .gitignore to ignore {script_name} and {output_file}")

def main():
    root_dir = '.'
    script_name = 'get_context.py'
    output_file = 'GET_CONTEXT.txt'
    
    file_structure, files_content = get_file_structure(root_dir)
    write_context_file(file_structure, files_content, output_file)
    update_gitignore(root_dir, script_name, output_file)
    print(f"Context file '{output_file}' created successfully!")

if __name__ == "__main__":
    main()