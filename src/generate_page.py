import os

from block_markdown import (
    markdown_to_html_node,
    extract_title
)
from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode
)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    file = open(from_path)
    text = file.read()
    file.close()

    templatefile = open(template_path)
    template = templatefile.read()
    templatefile.close()

    content = markdown_to_html_node(text).to_html()

    title = extract_title(text)

    generated_page = template.replace("{{ Title }}", title)
    generated_page = generated_page.replace("{{ Content }}", content)
    
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    file = open(dest_path, "w")
    file.write(generated_page)
    file.close()
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"starting recursive generation for {dir_path_content}")
    for filename in os.listdir(dir_path_content):
        new_dir_path_content = f"{dir_path_content}/{filename}"
        new_dest_dir_path = f"{dest_dir_path}/{filename}"
        if os.path.isfile(new_dir_path_content):
            new_dest_dir_path = f"{new_dest_dir_path.rstrip(".md")}.html"
            print(f"generating page for {new_dir_path_content}")
            generate_page(new_dir_path_content, template_path, new_dest_dir_path)
        else :
            generate_pages_recursive(new_dir_path_content, template_path, new_dest_dir_path)