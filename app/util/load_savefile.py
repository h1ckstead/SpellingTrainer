import pickle


def load_save():
    try:
        with open('savefile', 'rb') as file:
            data = pickle.load(file)
        return data
    except FileNotFoundError:
        return None
