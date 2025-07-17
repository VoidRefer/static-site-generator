import unittest

from src.textnode import (
    TextNode, TextType, 
    )
from src.markdown import (
    split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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