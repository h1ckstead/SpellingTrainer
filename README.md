Setting up Spelling Trainer 
Checkout project
git checkout https://github.com/h1ckstead/SpellingTrainer.git
create virtual environment
python -m venv /path/to/new/virtual/environment
activate venv
Mac: source venv/bin/activate
Windows: .\venv\Scripts\activate

To bundle on Windows:
pyinstaller -n "Spelling Trainer" -F --add-data "C:\Users\Constantinas\PycharmProjects\SpellingTrainer\app\assets;assets" --collect-all customtkinter --collect-all random_words --icon "C:\Users\Constantinas\PycharmProjects\SpellingTrainer\app\assets\favicon.ico" --log-level DEBUG main.py

On Mac:
pyinstaller -n "Spelling Trainer" -F --add-data "/Users/victorialazareva/PycharmProjects/SpellingTrainer/app/assets:assets" --collect-all customtkinter --icon "/Users/victorialazareva/PycharmProjects/SpellingTrainer/app/assets/favicon.icns" --onefile --windowed main.py


