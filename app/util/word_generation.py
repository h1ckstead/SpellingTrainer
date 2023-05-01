from random_words import RandomWords
import random


random_words = RandomWords()


def next_word(current_user):
    """
    dict, list
    Randomly decides source of the word and the word itself for practice
    :return: str
    """
    # TODO: Remove debug prints
    if len(current_user.misspelled_dict) > 30:
        choice_source = random.choices(['misspelled_dict', 'commonly_misspelled',
                                        'common_english', 'random'], weights=[4, 3, 2, 1], k=1)
    else:
        choice_source = random.choices(['commonly_misspelled', 'common_english', 'random'], weights=[3, 2, 1], k=1)
    if 'misspelled_dict' in choice_source:
        misspelled_list = list(current_user.misspelled_dict.keys())
        word = misspelled_list[random.randrange(0, len(current_user.misspelled_dict) - 1)]
        print('misspelled_dict')
    elif 'commonly_misspelled' in choice_source:
        word = current_user.words_list[random.randrange(0, len(current_user.words_list) - 1)]
        current_user.words_list.remove(word)
        print('commonly_misspelled')
    elif 'common_english' in choice_source:
        word = current_user.common_english_words_lst[random.randrange(0, len(current_user.common_english_words_lst)-1)]
        current_user.common_english_words_lst.remove(word)
        print('common_english')
    else:
        word = random_words.random_word(min_letter_count=4)
        print('random')
    return word.lower()
