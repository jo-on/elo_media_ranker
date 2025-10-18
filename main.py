import pandas as pd
from tools import add_item, play, set_match
from variables import CSV


try:
    df = pd.read_csv(CSV, index_col=0)
except FileNotFoundError:
    df = pd.DataFrame({"Name": [], "ELO": [], "General_Score": [], "Year": []})
    df.to_csv(CSV)


def start():
    res = input(f"[1]: Add a new item\n[2]: Play matchups\n[3]: Choose matchup by csv indexes\n[4]: Play ranked matchups\n[q]: Quit\n> ")
    while True:
        if res == 'q':
            break
        elif res == '1':
            add_item(df, CSV)
        elif res == '2':
            play(df, CSV)
        elif res == '3':
            set_match(df, CSV)
        elif res == '4':
            play(df, CSV, True)
        else:
            res = input("Invalid input.\n> ")
        res = input(f"\n[1]: Add a new item\n[2]: Play matchups\n[3]: Choose matchup by csv indexes\n[4]: Play ranked matchups\n[q]: Quit\n> ")


if __name__ == "__main__":
    start()
