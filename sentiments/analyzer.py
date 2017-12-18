import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""

        # TODO
        self.positives = set()
        with open("positive-words.txt") as lines:
            for line in lines:
                if line.startswith(';') == False:
                    self.positives.add(line.rstrip("\n"))
        lines.close()

        self.negatives = set()
        with open("negative-words.txt") as lines:
            for line in lines:
                if line.startswith(';') == False:
                    self.negatives.add(line.rstrip("\n"))
        lines.close()

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""

        # TODO
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        n = 0
        for word in tokens:
            if word.lower() in self.positives:
                n += 1
            elif word.lower() in self.negatives:
                n -= 1
            else:
                continue
        return n
        return 0
