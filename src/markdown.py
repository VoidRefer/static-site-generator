import re

from src.textnode import TextNode, TextType

def split_nodes_delimiter(
        old_nodes: list[TextNode], 
        delimiter: str, 
        text_type: TextType
    )  -> list[TextNode]:

    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        
        if len(parts) % 2 == 0:
            raise ValueError(
                "Unmatched delimeter '{delimeter} in text:\n\t{node.text}'"
            )
        
        for idx, part in enumerate(parts):
            if (idx % 2 == 0) and part:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
        
    return new_nodes

def _match_markdown_groups(text: str, split_pattern: re.Pattern):
    lst = []
    for match in split_pattern.finditer(text):
        lst.append((match.group(1), match.group(2)))
    return lst

def extract_markdown_images(text: str) -> list[str]:
    split_pattern = re.compile(r'\!\[(.*?)\]\((.*?)\)')
    return _match_markdown_groups(text, split_pattern)

def extract_markdown_links(text: str) -> list[str]:
    split_pattern = re.compile(r'(?<!!)\[(.*?)\]\((.*?)\)')

    return _match_markdown_groups(text, split_pattern)