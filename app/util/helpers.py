import os
import sys


# def get_path(*args):
#     if getattr(sys, 'frozen', False):
#         # Running as a bundled executable
#         if hasattr(sys, '_MEIPASS'):
#             # macOS and Windows
#             base_path = sys._MEIPASS
#         else:
#             # macOS
#             base_path = os.path.dirname(sys.executable)
#     else:
#         # Running as a regular Python script
#         base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
#
#     return os.path.join(base_path, *args)

def get_path(*args):
    if getattr(sys, 'frozen', False):
        # Running as a bundled executable
        if hasattr(sys, '_MEIPASS'):
            # macOS and Windows
            base_path = sys._MEIPASS
        else:
            # macOS
            base_path = os.path.dirname(sys.executable)
    elif 'unittest' in sys.modules:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app'))
    else:
        # Running as a regular Python script
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))

    return os.path.join(base_path, *args)


def get_avatars_list():
    return os.listdir(get_path("assets/avatars"))
