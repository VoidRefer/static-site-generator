

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
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

        return " ".join([f'{attribute[0]}="{attribute[1]}"' for attribute in self.props.items()])
    