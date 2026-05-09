from trie import Trie


class Homework(Trie):
    def count_words_with_suffix(self, pattern) -> int:
        if not isinstance(pattern, str):
            raise TypeError("pattern must be a string")
 
        count = 0

        def dfs(node, current_word):
            nonlocal count

            if node.value is not None and current_word.endswith(pattern):
                count += 1

            for char, child in node.children.items():
                dfs(child, current_word + char)

        dfs(self.root, "")
        return count
    def has_prefix(self, prefix) -> bool:
        if not isinstance(prefix, str):
            raise TypeError("prefix must be a string")

        node = self.root

        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]

        return True


if __name__ == "__main__":
    trie = Homework()
    words = [
        "apple", "application", "banana", "cat",
        "Apple", "App", "dog", "catalog", "log",
        "testing", "king", "Ring", "ring"
    ]

    for i, word in enumerate(words):
        trie.put(word, i)

    # 1. Suffixes
    assert trie.count_words_with_suffix("e") == 2      # apple, Apple
    assert trie.count_words_with_suffix("ion") == 1    # application
    assert trie.count_words_with_suffix("a") == 1      # banana
    assert trie.count_words_with_suffix("at") == 1     # cat
    assert trie.count_words_with_suffix("log") == 2    # catalog, log
    assert trie.count_words_with_suffix("ing") == 4    # testing, king,Ring, ring
    assert trie.count_words_with_suffix("xyz") == 0

    # 2. Register check
    assert trie.count_words_with_suffix("Apple") == 1
    assert trie.count_words_with_suffix("apple") == 1
    assert trie.count_words_with_suffix("Ring") == 1
    assert trie.count_words_with_suffix("ring") == 1

    assert trie.has_prefix("App") is True
    assert trie.has_prefix("app") is True
    assert trie.has_prefix("APP") is False

    # 3. Prefixes
    assert trie.has_prefix("app") is True
    assert trie.has_prefix("bat") is False
    assert trie.has_prefix("ban") is True
    assert trie.has_prefix("ca") is True
    assert trie.has_prefix("dog") is True
    assert trie.has_prefix("dogs") is False

    # 4. Invalid data
    try:
        trie.count_words_with_suffix(123)
        assert False, "count_words_with_suffix should raise TypeError"
    except TypeError:
        pass

    try:
        trie.has_prefix(None)
        assert False, "has_prefix should raise TypeError"
    except TypeError:
        pass

    # 5. Verification on a large dataset
    big_trie = Homework()

    for i in range(10000):
        big_trie.put(f"word{i}", i)

    assert big_trie.has_prefix("word") is True
    assert big_trie.has_prefix("unknown") is False
    assert big_trie.count_words_with_suffix("999") == 10
    assert big_trie.count_words_with_suffix("not_found") == 0

    print("All tests passed!")