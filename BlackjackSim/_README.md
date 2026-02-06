## Set-Up

(I)     Clone Repo

    git clone https://github.com/austinleothomas/portfolio
    cd portfolio

(II)    Initiate Virtual Environment (Optional)

    python -m venv venv
    venv\Scripts\Activate

(III)   Install Packages

    pip install -r requirements.txt

(IV)    Run Program

    python blackjack.py

## Note to User
This program relies on tkinter. Ensure your Python version has tkinter natively installed.

## Folder Contents

\Icons                  folder containing artwork for the game
blackjack.py            .py executable to launch game
requirements.txt        packages required for execution (spoiler: it's just pillow)

## Project Overview
Wrote this single-player blackjack game as I was learning Python. It still has a few
bugs but runs well overall. The following features are of note ...

    => allows for a 1 - 8 deck shoes
    => allows for 1 - 3 concurrent hands
    => desk is fully simulated based on shoe size and re-shuffled automatically
    => supports doubling-down
    => allows for variable bet sizing and tracks player bankroll