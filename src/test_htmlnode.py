import unittest

from htmlnode import HTMLNode

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
            'class="greeting" id="everybody"',
        )