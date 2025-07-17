import re

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