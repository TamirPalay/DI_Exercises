import string
import re

class Text:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

    def word_frequency(self, word):
        words = self.text.split()
        if words.count(word):
            return words.count(word)
        else:
            print(f"The word '{word}' is not found in the text.")
            return None

    def most_common_word(self):
        words = self.text.split()
        word_counts = {}
        for word in words:
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1
        most_common = max(word_counts, key=word_counts.get)
        return most_common, word_counts[most_common]

    def unique_words(self):
        words = self.text.split()
        return list(set(words))

    @classmethod
    def from_file(cls, file_path):
        with open(file_path, 'r') as file:
            text = file.read()
        return cls(text)


class TextModification(Text):
    def __init__(self, text):
        super().__init__(text)

    # A built-in stop words list so you don't need to pass one in
    STOP_WORDS = {
        "a", "an", "the", "and", "or", "but", "is", "are", "was", "were",
        "be", "been", "being", "have", "has", "had", "do", "does", "did",
        "will", "would", "could", "should", "may", "might", "shall", "can",
        "to", "of", "in", "for", "on", "with", "at", "by", "from", "as",
        "into", "through", "about", "it", "its", "this", "that", "i", "he",
        "she", "they", "we", "you", "my", "your", "his", "her", "our", "not"
    }

    def remove_punctuation(self):
        translator = str.maketrans('', '', string.punctuation)
        self.text = self.text.translate(translator)
        return self.text

    def remove_stop_words(self):
        words = self.text.split()
        # .lower() for comparison only — keeps original casing in output
        filtered = [word for word in words if word.lower() not in self.STOP_WORDS]
        self.text = ' '.join(filtered)
        return self.text

    def remove_special_characters(self):
        # Keeps only letters, numbers, and spaces — removes everything else
        self.text = re.sub(r'[^a-zA-Z0-9\s]', '', self.text)
        return self.text


# --- Testing all three methods ---
sample = "Hello! The quick brown fox... jumps over the lazy dog. Is it fast? Yes, it is! #amazing @python"

tm = TextModification(sample)
print("Original:            ", sample)
print("No punctuation:      ", tm.remove_punctuation())
print("No stop words:       ", tm.remove_stop_words())
print("No special chars:    ", tm.remove_special_characters())