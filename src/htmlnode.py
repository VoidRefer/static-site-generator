from __future__ import annotations

from typing import Any

class HTMLNode():
    def __init__(
            self, 
            tag:str | None = None, 
            value: str | None = None, 
            children: list[HTMLNode] = None, 
            props=None
        ):
        self.tag = tag
        self.value = value
        self.children= children
        self.props = props

    def __eq__(self, other):
        if (self.tag != other.tag): return False 
        if (self.value != other.value): return False 
        if (self.children != other.children): return False 
        if (self.props != other.props): return False 

        return True
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        
        return "".join([f' {attribute[0]}="{attribute[1]}"' for attribute in self.props.items()])
    

class LeafNode(HTMLNode):
    def __init__(
            self, 
            tag: str | None, 
            value: str | None, 
            props: dict[str, str] | None = None,
        ):
        super().__init__(tag, value, None, props)
    
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
    def to_html(self) -> str:
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(
            self, 
            tag: str, 
            children: list[HTMLNode], 
            props: dict[str, str] | None = None,
        ):
        super().__init__(tag, None, children, props)
    
    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("All parents nodes must have a tag")
        
        if not self.children:
            return ValueError("Missing children attribute")

        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"