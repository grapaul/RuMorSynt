from typing import Tuple


class TrieNode(object):
    """
    Prefix trie with symbol nodes, presenting words backwards.
    """
    def __init__(self, char: str):
        self.char = char
        self.children = dict()
        # Is it the last character of the word
        self.word_finished = False
        # How many times this character appeared in the addition process
        self.counter = 1


def add(root: TrieNode, word: str):
    """
    Add symbol sequences of the word to the main trie.
    """
    node = root
    for char in word[::-1]:
        if char in node.children:
            child = node.children[char]
            child.counter += 1
            node = child
        else:
            new_node = TrieNode(char)
            node.children[char] = new_node
            node = new_node
    node.word_finished = True


def find_suffix(root: TrieNode, suffix: str) -> Tuple[bool, TrieNode]:
    """
    Returns bool search result and the lowest node of the suffix sequence in the trie.
    """
    node = root
    if not root.children:
        return False, node
    for char in suffix[::-1]:
        if char in node.children:
            node = node.children[char]
        else:
            return False, node
    return True, node
