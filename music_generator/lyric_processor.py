import re

def count_syllables(word):
    # A simple heuristic for syllable counting
    word = word.lower()
    # remove all non-alpha characters
    word = re.sub(r'[^a-z]', '', word)
    if len(word) <= 3:
        return 1
    # Remove silent 'e' at the end
    if word.endswith('e'):
        word = word[:-1]

    vowels = 'aeiouy'
    syllable_count = 0
    for i in range(len(word)):
        if word[i] in vowels and (i == 0 or word[i-1] not in vowels):
            syllable_count += 1
    return syllable_count if syllable_count > 0 else 1

def process_lyrics(lyrics):
    words = lyrics.split()
    syllable_counts = [count_syllables(word) for word in words]
    return words, syllable_counts

if __name__ == '__main__':
    test_lyrics = "This is a test of the lyric processor."
    words, syllables = process_lyrics(test_lyrics)
    print(f"Lyrics: {test_lyrics}")
    print(f"Words: {words}")
    print(f"Syllables per word: {syllables}")
    print(f"Total syllables: {sum(syllables)}")
