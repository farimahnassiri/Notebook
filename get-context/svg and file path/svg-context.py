import xml.etree.ElementTree as ET
import os

def process_svg(svg_file):
    if not os.path.isfile(svg_file):
        print(f"Error: The file '{svg_file}' does not exist.")
        return

    try:
        relative_path = os.path.relpath(svg_file)
        tree = ET.parse(svg_file)
        root = tree.getroot()
        
        output_file = 'SVG_CONTEXT.txt'
        with open(output_file, 'w') as f:
            f.write(f"SVG File: {relative_path}\n\n")
            
            def process_element(element, level=0):
                tag = element.tag.split('}')[-1]
                attrs = element.attrib.copy()
                if tag == 'path' and 'd' in attrs:
                    attrs['d'] = '--some-arbitrary-path'
                attr_str = ' '.join(f'{k}="{v}"' for k, v in attrs.items())
                f.write(' ' * level + f"<{tag} {attr_str}>\n")
                for child in element:
                    process_element(child, level + 1)
                f.write(' ' * level + f"</{tag}>\n")
            
            process_element(root)
        
        print(f"Processing complete. Output written to '{output_file}'")
        return output_file
    except ET.ParseError:
        print(f"Error: Unable to parse '{svg_file}'. Make sure it's a valid SVG file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

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
    print("Current working directory:", os.getcwd())
    print("Files in current directory:", os.listdir())

    svg_file = input("Enter the path to your SVG file: ")
    svg_file = os.path.abspath(svg_file)
    print(f"Attempting to process file: {svg_file}")

    output_file = process_svg(svg_file)
    
    if output_file:
        script_name = os.path.basename(__file__)
        update_gitignore(os.getcwd(), script_name, output_file)

if __name__ == "__main__":
    main()