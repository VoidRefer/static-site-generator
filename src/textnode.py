from __future__ import annotations
import re
from enum import Enum

from src.htmlnode import HTMLNode, LeafNode
from src.markdown import extract_markdown_images, extract_markdown_links

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if (self.text != other.text): return False 
        if (self.text_type != other.text_type): return False 
        if (self.url != other.url): return False 

        return True
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

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

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        remaining_text = node.text

        for image_text, image_url in images:
            
            parts = remaining_text.split(f"![{image_text}]({image_url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(TextNode(image_text, TextType.IMAGE, image_url))

            remaining_text = parts[1] if len(parts) > 1 else ""
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        remaining_text = node.text

        for link_text, link_url in links:
            
            parts = remaining_text.split(f"[{link_text}]({link_url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

            remaining_text = parts[1] if len(parts) > 1 else ""
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)

        case TextType.BOLD:
            return LeafNode("b", text_node.text)

        case TextType.ITALIC:
            return LeafNode("i", text_node.text)

        case TextType.CODE:
            return LeafNode("code", text_node.text)
            
        case TextType.LINK:
            if text_node.url is None:
                raise ValueError("TextNode misssing url value")
            return LeafNode("a", text_node.text, {"href": text_node.url})
            
        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("TextNode misssing url value")
            return LeafNode(
                "img", 
                "", 
                {"src": text_node.url, "alt": text_node.text}
            )
    raise Exception("Invalid TextType")

def text_to_textnodes(text: str) -> list[TextNode]:
    node = TextNode(text=text, text_type=TextType.TEXT)
    nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes