def commonly_misspelled_lst():
    with open('assets/commonly_misspelled_words.txt') as document:
        commonly_misspelled_words = document.read().splitlines()
    return commonly_misspelled_words


def common_english_words_lst():
    with open('assets/old_common_english_words.txt') as document:
        common_english_words = document.read().splitlines()
    return common_english_words
