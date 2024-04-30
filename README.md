# 🔴 Connect4 🟡

A Connect 4 game in the terminal with beautiful color and dangerous AI !

## 📝 Requirements

To run the project, you must have :

- Python 3.11+

## 💻 Installation

### 📥 Get the source code

Clone this repo with `git` and enter the project directory.

### 📦 Setup Python dependencies

We will use a virtual env to install our Python dependencies, but you can choose
your way!

1. Create a virtual environment with `python3 -m venv venv`.
2. Activate your virtual env with `source venv/bin/activate`.
3. Install dependencies with `pip install -r requirements.txt`.

## 🏁 Play !

### 🎮 Game mode

You can run the game normally with `python3 main.py`, you will have different
menus to configure your game easily.

### 📈 Stats mode

This mode is to test the performance of our evaluation functions and generate
images with pie charts.

Run `python3 main_stats.py --help` to see all the settings available.

The string used to describe a player follows this format :
`eval_X:board_actions_X:depth`

You can add `:m` at the end to use minimax instead of alpha-beta.
