import json
class AnagramChecker():
    def __init__(self):
        with open("sowpods.txt", 'r') as file:
            self.words = set(word.strip().upper() for word in file)
    
    def is_valid_word(self,word):
        return word in self.words
    def is_anagram(self,word1,word2):
        if word1 == word2:
            print("The words are the same, not anagrams.")
            return False
        return sorted(word1) == sorted(word2)
    
    def get_anagrams(self,word):
        anagrams = []
        for candidate in self.words-{word}:
            if not self.is_anagram(word,candidate):
                continue
            anagrams.append(candidate)
        return anagrams
