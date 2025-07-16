import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag = "p", value="Beware of the leopard")
        node2 = HTMLNode(tag = "p", value="Beware of the leopard")
        self.assertEqual(node, node2)
    
    def test_repr(self):
        node = HTMLNode(
            "p",
            "Beware of the alien",
            None,
            {"class": "primary"}

        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, Beware of the alien, children: None, {'class': 'primary'})"
        )
    
    def test_props_to_html(self):
        node = HTMLNode(
            "div",
            "Greetings, one and all!",
            None,
            {"class": "greeting", "id": "everybody"}
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" id="everybody"',
        )
    
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_notag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_nested_children(self):
        child_node_1 = LeafNode("p", "child 1")
        child_node_2 = LeafNode("l", "child 2")
        parent = ParentNode("section", [child_node_1, child_node_2])
        grandparent = ParentNode("div", [parent])

        expected_html = (
            '<div><section><p>child 1</p><l>child 2</l></section></div>'
        )
        self.assertEqual(
            grandparent.to_html(),
            expected_html,
        )

