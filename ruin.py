import abc
import argparse
import io
import pprint
import urllib.request
import tempfile
from typing import Set
import zipfile

WORDS_URL = "http://gwicks.net/textlists/usa.zip"


class BaseWords(abc.ABC):
    def words(self) -> Set[str]:
        raise NotImplementedError

    @staticmethod
    def clean_raw_words_file(raw_content: str) -> Set[str]:
        return {word.strip() for word in raw_content.split("\n") if word.strip()}


class URLZippedWords(BaseWords):
    def __init__(self, url: str):
        self.url = url

    def words(self) -> Set[str]:
        filename = self.url.rsplit("/", maxsplit=1)[-1].removesuffix(".zip") + ".txt"
        with urllib.request.urlopen(self.url) as _fd:
            raw = _fd.read()
        with tempfile.TemporaryDirectory() as tempdir:
            path = zipfile.ZipFile(io.BytesIO(raw)).extract(filename, path=tempdir)
            with open(path) as _fd:
                return self.clean_raw_words_file(_fd.read())


class SpellingBee:
    def __init__(self, letters: str, middle_letter: str):
        self.letters = letters
        self.middle_letter = middle_letter

    @property
    def letters(self) -> str:
        return self._letters

    @letters.setter
    def letters(self, inp: str):
        self._letters = inp.lower()

    @property
    def middle_letter(self) -> str:
        return self._middle_letter

    @middle_letter.setter
    def middle_letter(self, inp: str):
        assert len(inp) == 1
        self._middle_letter = inp.lower()

    def solve(self, words: Set[str]) -> Set[str]:
        set_letters = set(self.letters)
        set_letters.add(self.middle_letter)
        return {
            word
            for word in words
            if len(word) > 3
            and not set(word) - set_letters
            and self.middle_letter in word
        }


def main():
    puzzle = parse_input()
    words = URLZippedWords(WORDS_URL).words()
    solution = puzzle.solve(words)
    pprint.pprint(sorted(list(solution)))
    print(f"\n{len(solution)} words\n")


def parse_input() -> SpellingBee:
    parser = argparse.ArgumentParser()
    parser.add_argument('letters')
    parser.add_argument('middle_letter')
    args = parser.parse_args()
    return SpellingBee(args.letters, args.middle_letter)


if __name__ == "__main__":
    main()
