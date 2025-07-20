import os
import shutil
import sys
from pathlib import Path

from markdown import markdown_to_html_node

def copy_directory(src: str, dst: str):
    if os.path.exists(dst):
        print(f"Removing existing directory: {dst}")
        shutil.rmtree(dst)
    
    def custom_copy(src, dst):
        print(f"Copying {src} to {dst}")
        shutil.copy2(src, dst)
    
    print(f"Copying directory from {src} to {dst}")
    shutil.copytree(src, dst, copy_function=custom_copy)

def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No H1 header found in markdown.")

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as markdown_file:
        markdown_content = markdown_file.read()

    with open(template_path, "r") as template_file:
        template_content = template_file.read()

    html_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)

    full_html = template_content.replace("{{ Title }}", title)
    full_html = template_content.replace("{{ Content }}", html_content)

    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as dest_file:
        dest_file.write(full_html)

def generate_pages_recursive(
        dir_path_content: str, 
        template_path: str, 
        dest_dir_path: str,
        basepath: str
    ):
    content_path = Path(dir_path_content)
    template_path = Path(template_path)
    dest_path = Path(dest_dir_path)

    if not template_path.is_file():
        raise FileNotFoundError(f"Template file not found: {template_path}")
    
    for md_file in content_path.rglob("*.md"):
        try:
            relative_path = md_file.relative_to(content_path)
            dest_file = dest_path / relative_path.with_suffix(".html")

            generate_page(str(md_file), str(template_path), str(dest_file), basepath)
        except Exception as e:
            print(f"Error processing {md_file}: {e}")

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_directory("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()