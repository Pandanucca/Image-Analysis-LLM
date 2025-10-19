"""
Advanced tokenization using BPE (Byte Pair Encoding) for better text processing.
This replaces the character-level tokenization with subword tokenization.
"""

import re
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import List, Dict, Tuple


class BPETokenizer:
    """Byte Pair Encoding tokenizer for better text handling."""

    def __init__(self, vocab_size: int = 5000):
        """
        Initialize BPE tokenizer.

        Args:
            vocab_size: Target vocabulary size
        """
        self.vocab_size = vocab_size
        self.vocab = {}
        self.merges = []
        self.byte_encoder = self._bytes_to_unicode()
        self.byte_decoder = {v: k for k, v in self.byte_encoder.items()}

        # Special tokens
        self.pad_token = '<|pad|>'
        self.unk_token = '<|unk|>'
        self.bos_token = '<|bos|>'
        self.eos_token = '<|eos|>'

        self.special_tokens = [
            self.pad_token,
            self.unk_token,
            self.bos_token,
            self.eos_token
        ]

    def _bytes_to_unicode(self):
        """Create mapping from bytes to unicode strings."""
        bs = (
                list(range(ord("!"), ord("~") + 1)) +
                list(range(ord("¡"), ord("¬") + 1)) +
                list(range(ord("®"), ord("ÿ") + 1))
        )
        cs = bs[:]
        n = 0
        for b in range(2 ** 8):
            if b not in bs:
                bs.append(b)
                cs.append(2 ** 8 + n)
                n += 1
        cs = [chr(n) for n in cs]
        return dict(zip(bs, cs))

    def train(self, texts: List[str], verbose: bool = True):
        """
        Train BPE tokenizer on text corpus.

        Args:
            texts: List of training texts
            verbose: Print progress
        """
        if verbose:
            print(f"Training BPE tokenizer on {len(texts)} documents...")

        # Pre-tokenize into words
        word_freqs = Counter()
        for text in texts:
            words = self._pre_tokenize(text)
            word_freqs.update(words)

        # Initialize vocabulary with characters
        vocab = self.special_tokens.copy()
        for word in word_freqs:
            for char in word:
                if char not in vocab:
                    vocab.append(char)

        # Convert words to character sequences
        splits = {
            word: [c for c in word]
            for word in word_freqs.keys()
        }

        # Learn merges
        while len(vocab) < self.vocab_size:
            # Count pairs
            pair_freqs = defaultdict(int)
            for word, freq in word_freqs.items():
                split = splits[word]
                if len(split) == 1:
                    continue
                for i in range(len(split) - 1):
                    pair = (split[i], split[i + 1])
                    pair_freqs[pair] += freq

            if not pair_freqs:
                break

            # Find most frequent pair
            best_pair = max(pair_freqs, key=pair_freqs.get)

            # Merge best pair
            self.merges.append(best_pair)
            new_token = ''.join(best_pair)
            vocab.append(new_token)

            # Update splits
            for word in word_freqs:
                split = splits[word]
                if len(split) == 1:
                    continue

                new_split = []
                i = 0
                while i < len(split):
                    if i < len(split) - 1 and (split[i], split[i + 1]) == best_pair:
                        new_split.append(new_token)
                        i += 2
                    else:
                        new_split.append(split[i])
                        i += 1
                splits[word] = new_split

            if verbose and len(vocab) % 100 == 0:
                print(f"Vocabulary size: {len(vocab)}")

        # Create final vocabulary mapping
        self.vocab = {token: idx for idx, token in enumerate(vocab)}
        self.inv_vocab = {idx: token for token, idx in self.vocab.items()}

        if verbose:
            print(f"Training complete. Final vocabulary size: {len(self.vocab)}")

    def _pre_tokenize(self, text: str) -> List[str]:
        """Split text into words."""
        # Simple word splitting
        pattern = r'\w+|[^\w\s]'
        return re.findall(pattern, text.lower())

    def _tokenize_word(self, word: str) -> List[str]:
        """Tokenize a single word using learned merges."""
        if not self.merges:
            return list(word)

        chars = list(word)

        for merge in self.merges:
            new_chars = []
            i = 0
            while i < len(chars):
                if i < len(chars) - 1 and (chars[i], chars[i + 1]) == merge:
                    new_chars.append(''.join(merge))
                    i += 2
                else:
                    new_chars.append(chars[i])
                    i += 1
            chars = new_chars

            if len(chars) == 1:
                break

        return chars

    def encode(self, text: str) -> List[int]:
        """
        Encode text to token IDs.

        Args:
            text: Input text

        Returns:
            List of token IDs
        """
        words = self._pre_tokenize(text)
        tokens = []

        for word in words:
            word_tokens = self._tokenize_word(word)
            for token in word_tokens:
                if token in self.vocab:
                    tokens.append(self.vocab[token])
                else:
                    tokens.append(self.vocab[self.unk_token])

        return tokens

    def decode(self, token_ids: List[int]) -> str:
        """
        Decode token IDs to text.

        Args:
            token_ids: List of token IDs

        Returns:
            Decoded text
        """
        tokens = []
        for id in token_ids:
            if id in self.inv_vocab:
                token = self.inv_vocab[id]
                if token not in self.special_tokens:
                    tokens.append(token)

        return ''.join(tokens)

    def save(self, path: str):
        """Save tokenizer to file."""
        data = {
            'vocab': self.vocab,
            'merges': self.merges,
            'vocab_size': self.vocab_size
        }
        with open(path, 'w') as f:
            json.dump(data, f)

    def load(self, path: str):
        """Load tokenizer from file."""
        with open(path, 'r') as f:
            data = json.load(f)

        self.vocab = data['vocab']
        self.merges = [tuple(m) for m in data['merges']]
        self.vocab_size = data['vocab_size']
        self.inv_vocab = {int(v): k for k, v in self.vocab.items()}


class SimpleSubwordTokenizer:
    """
    Simplified subword tokenizer without BPE training.
    Good for quick deployment without training.
    """

    def __init__(self, text: str = None):
        """Initialize with optional training text."""
        self.word_tokens = {}
        self.token_to_id = {}
        self.id_to_token = {}
        self.vocab_size = 0

        # Special tokens
        self.pad_token = '<PAD>'
        self.unk_token = '<UNK>'
        self.bos_token = '<BOS>'
        self.eos_token = '<EOS>'

        if text:
            self.build_vocab(text)

    def build_vocab(self, text: str):
        """Build vocabulary from text."""
        # Tokenize into words
        words = re.findall(r'\w+|[^\w\s]', text.lower())
        word_freq = Counter(words)

        # Add special tokens
        vocab = [self.pad_token, self.unk_token, self.bos_token, self.eos_token]

        # Add common words
        common_words = [word for word, freq in word_freq.most_common(3000)]
        vocab.extend(common_words)

        # Add individual characters for OOV handling
        chars = set(text.lower())
        for char in sorted(chars):
            if char not in vocab and char.strip():
                vocab.append(char)

        # Create mappings
        self.token_to_id = {token: idx for idx, token in enumerate(vocab)}
        self.id_to_token = {idx: token for token, idx in self.token_to_id.items()}
        self.vocab_size = len(vocab)

    def encode(self, text: str) -> List[int]:
        """Encode text to IDs."""
        words = re.findall(r'\w+|[^\w\s]', text.lower())
        ids = []

        for word in words:
            if word in self.token_to_id:
                ids.append(self.token_to_id[word])
            else:
                # Fallback to character-level
                for char in word:
                    if char in self.token_to_id:
                        ids.append(self.token_to_id[char])
                    else:
                        ids.append(self.token_to_id[self.unk_token])

        return ids

    def decode(self, ids: List[int]) -> str:
        """Decode IDs to text."""
        tokens = []
        for id in ids:
            if id in self.id_to_token:
                token = self.id_to_token[id]
                if token not in [self.pad_token, self.unk_token, self.bos_token, self.eos_token]:
                    tokens.append(token)

        # Simple reconstruction
        result = ' '.join(tokens)
        # Remove spaces before punctuation
        result = re.sub(r'\s+([.,!?;:])', r'\1', result)
        return result


if __name__ == "__main__":
    # Test tokenizer
    with open("../input.txt", "r", encoding="utf-8") as f:
        text = f.read()

    print("Testing SimpleSubwordTokenizer...")
    tokenizer = SimpleSubwordTokenizer(text)

    test_text = "What are your bathroom remodeling services?"
    print(f"\nOriginal: {test_text}")

    encoded = tokenizer.encode(test_text)
    print(f"Encoded: {encoded}")

    decoded = tokenizer.decode(encoded)
    print(f"Decoded: {decoded}")

    print(f"\nVocabulary size: {tokenizer.vocab_size}")
    print(f"Compression ratio: {len(test_text) / len(encoded):.2f}x")