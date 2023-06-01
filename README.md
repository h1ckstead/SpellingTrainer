# Setting up Spelling Trainer 
### Checkout project
`git checkout https://github.com/h1ckstead/SpellingTrainer.git`
### Create virtual environment
`python -m venv /path/to/new/virtual/environment`
### Activate venv
**Mac:** `source venv/bin/activate`
**Windows:** `.\venv\Scripts\activate`
### Install dependencies
`pip install -r requirements.txt`

# Bundling
### on Windows:
`pyinstaller -n "Spelling Trainer" -F --add-data "C:\Path\To\SpellingTrainer\app\assets;assets" --collect-all customtkinter --collect-all random_words --icon "C:\Path\To\SpellingTrainer\app\assets\favicon.ico" main.py`

### on Mac:
`pyinstaller -n "Spelling Trainer" -F --add-data "/Path/To/SpellingTrainer/app/assets:assets"  --add-data "/Path/To/SpellingTrainer/venv/lib/python3.11/site-packages/spellchecker/resources/en.json.gz:spellchecker/resources" --add-data "/Path/To/SpellingTrainer/venv/lib/python3.11/site-packages/random_words/nouns.dat:random_words" --collect-all customtkinter --icon "/Path/To/SpellingTrainer/app/assets/favicon.icns" --onefile --windowed main.py`
