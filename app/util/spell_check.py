import config


def spell_check(current_user, word, user_word):
    if user_word == '':
        status = None
    elif user_word == word:
        status = 'correct'
        if word in current_user.misspelled_dict.keys():
            current_user.misspelled_dict[word] -= 1
            current_user.attempts_correct += 1
            check_word_learned(current_user, word)
        else:
            current_user.spelled_ok_lst.append(word)
            current_user.attempts_correct += 1
    else:
        status = 'incorrect'
        if word in current_user.misspelled_dict.keys():
            current_user.misspelled_dict[word] += 1
            current_user.attempts_incorrect += 1
        else:
            current_user.misspelled_dict[word] = config.ATTEMPTS_TO_LEARN_WORD
            current_user.attempts_incorrect += 1
    return status


def check_word_learned(current_user, word):
    """
    Checks if number of attempts is 0 which means the word is considered
    to be learned. Removes learned word from misspelled_dict and puts it
    into vocabulary_lst
    :param current_user: User object
    :param word: str
    :return:
    """
    if current_user.misspelled_dict[word] == 0:
        current_user.misspelled_dict.pop(word)
        current_user.spelled_ok_lst.append(word)
