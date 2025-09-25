import pandas as pd
from tools import add_item, play, set_match
from variables import CSV


try:
    df = pd.read_csv(CSV, index_col=0)
except FileNotFoundError:
    df = pd.DataFrame({"Name": [], "ELO": [], "General_Score": [], "Year": []})
    df.to_csv(CSV)


def start():
    res = input(f"[1]: Add a new item\n[2]: Decide between existing items\n[3]: Choose own matchup by indexes\n[0]: Quit\n> ")
    while True:
        if res == '0':
            return
        elif res == '1':
            add_item(df, CSV)
        elif res == '2':
            play(df, CSV)
        elif res == '3':
            set_match(df, CSV)
        else:
            res = input("Invalid input.\n> ")
        res = input(f"[1]: Add a new item\n[2]: Decide between existing items\n[3]: Choose own matchup by indexes\n[0]: Quit\n> ")


if __name__ == "__main__":
    start()
