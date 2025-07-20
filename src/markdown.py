from __future__ import annotations

import re
from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node, text_to_textnodes

class BlockType(Enum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
    return [block.strip() for block in markdown.split("\n\n") if block]

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)

    children = []

    for block in blocks:
        match block_to_block_type(block):
            case BlockType.HEADING:
                children.append(heading_to_html_node(block))
                
            case BlockType.PARAGRAPH:
                children.append(paragraph_to_html_node(block))

            case BlockType.CODE:
                children.append(code_to_html_node(block))

            case BlockType.QUOTE:
                children.append(quote_to_html_node(block))


            case BlockType.UNORDERED_LIST:
                children.append(ulist_to_html_node(block))

            case BlockType.ORDERED_LIST:
                children.append(olist_to_html_node(block))

            case _:
                raise ValueError("invalid block type")
            
    return ParentNode("div", children, None)

def text_to_childen(text: str):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def heading_to_html_node(block: str):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break

    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level+1 :]
    children = text_to_childen(text)
    return ParentNode(f"h{level}", children)

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_childen(paragraph)
    return ParentNode("p", children)

def code_to_html_node(block: str):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def quote_to_html_node(block: str):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            print("Line:" + line)
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_childen(content)
    return ParentNode("blockquote", children)

def ulist_to_html_node(block: str):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_childen(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def olist_to_html_node(block: str):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_childen(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)
