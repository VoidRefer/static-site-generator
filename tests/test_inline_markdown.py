import unittest

from src.textnode import (
    extract_markdown_images, extract_markdown_links,
    TextNode, TextType, split_nodes_delimiter, 
    split_nodes_image, split_nodes_link, text_to_textnodes
    )
from src.markdown import (
    markdown_to_blocks, BlockType, 
    block_to_block_type, markdown_to_html_node
    )


class TestInlineMarkdown(unittest.TestCase):
    def setUp(self):
        self.text_with_image = (
            "This is a text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.text_with_links = (
            "This is a text with a link to [Google](https://google.com), "
            "and another to [Boot.dev](https://www.boot.dev)"
        )
        self.text_mixed = (
            "This is a text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
            "and a link to [imgur](https://imgur.com/)"
        )
        self.text_no_matches = (
            "This is a text with no image and no link"
        )
    

    def test_delim_bold(self):
        node = TextNode("Text with **bolded** word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("Text with _italic_ word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("Text with `code block` word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            self.text_with_image
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            self.text_with_links
        )
        expected = [
            ("Google", "https://google.com"),
            ("Boot.dev", "https://www.boot.dev"),
        ]
        self.assertListEqual(expected, matches)
    
    def test_extract_markdown_images_mix(self):
        matches = extract_markdown_images(
            self.text_mixed
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], 
            matches
            )
        
    def test_extract_markdown_links_mix(self):
        matches = extract_markdown_links(
            self.text_mixed
        )
        self.assertListEqual(
            [("imgur", "https://imgur.com/")], 
            matches
            )

    def test_extract_markdown_no_match(self):
        matches = extract_markdown_images(
            self.text_no_matches
        )
        self.assertListEqual(
            [], 
            matches
            )
        matches = extract_markdown_links(
            self.text_no_matches
        )
        self.assertListEqual(
            [], 
            matches
            )
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_text_to_textnodes(self):
        text = ("This is **text** with an _italic_ word and a `code block` "
                "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
                "and a [link](https://boot.dev)"
                )
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        nodes = text_to_textnodes(text)
        
        self.assertEqual(expected, nodes)

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        block =  "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- unordered list item\n- another list item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. ordered list item\n2. another list item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)    

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )