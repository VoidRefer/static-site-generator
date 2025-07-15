from textnode import TextNode, TextType

def main():
    test = TextNode("This is some anchor text", TextType.LINKS, "https://www.boot.dev")
    print(test)

if __name__ == "__main__":
    main()