# About
Python project that utilizes oop principles to create a singleton app that analyzes the sentiment of a given text.
App uses tkinter to create a GUI.
App uses threading to run the model building in the background.
Program is windows centric.
The program can use between 3 models per user discretion trained on the imdb datasets.
Namely:
- RNN
- LSTM
- CNN

# To compile
- Navigate to the project directory
- Run `pip install -r requirements.txt`
- Run `!python main.py`

# Note
Project may not run on lower end hardware. In that case utizing the ai on colab is recommended.
Ui cannot be used on colab so ai functions would have to be directly called from a modified main.py file.

# Group members
- 1. Abdulah Chouhan