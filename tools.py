import pandas as pd
import random
from variables import GENERAL_SCORER, GENERAL_SCORE_SCALE


def expected_value(rA, rB):
    return 1 / (1 + 10 ** ((rB - rA) / 400))


def new_elo(rA, result, ev, k=32):
    scores = [0.5, 1, 0]
    return int(rA + k * (scores[int(result)] - ev))


def add_item(df: pd.DataFrame, csv: str, base_rating: int=1000):
    A_n = input("Item name:\n> ")
    A_i = len(df)
    A_s = base_rating

    A_y = input(f"Release year of {A_n}:\n> ")
    while True:
        try:
            A_y = int(A_y)
            if (1878 > A_y) or (A_y > 2025): # TODO: Keep updated
                raise ValueError
            break
        except:
            A_y = input("Invalid input.\n> ")

    A_l = input(f"{GENERAL_SCORER} rating for {A_n} ({A_y}):\n> ")
    while True:
        try:
            A_l = float(A_l)
            if (GENERAL_SCORE_SCALE[0] > A_l) or (A_l > GENERAL_SCORE_SCALE[1]):
                raise ValueError
            break
        except:
            A_l = input("Invalid input.\n> ")

    inds = list(range(len(df)))
    random.shuffle(inds)
    for _ in range(min(len(df), 5)):
        random_index = inds.pop()

        B_n = df.iloc[random_index, 0]
        B_s = df.iloc[random_index, 1]
        B_l = df.iloc[random_index, 2]
        B_y = df.iloc[random_index, 3]

        A_ev = expected_value(A_s, B_s)
        B_ev = expected_value(B_s, A_s)

        resA = input(f"Placement matchup:\n[1]: {A_n} ({A_y}) - [{round(A_ev, 2)}]\n[2]: {B_n} ({B_y}) - [{round(B_ev, 2)}]\n[0]: Tie\n> ")
        while True:
            if resA == '0':
                resB = 0
                break
            elif resA == '1':
                resB = 2
                break
            elif resA == '2':
                resB = 1
                break
            else:
                resA = input("Invalid input.\n> ")

        A_s = new_elo(A_s, int(resA), A_ev)

        df.loc[random_index] = [B_n, (new_elo(B_s, resB, B_ev)), B_l, B_y]

    df.loc[A_i] = [A_n, A_s, A_l, A_y]
    df.to_csv(csv)

    df_sorted = df.sort_values("ELO", ascending=False).reset_index(drop=True)
    print(f"ELO for {A_n}: {A_s}, rank: {df_sorted[(df_sorted["Name"] == A_n) & (df_sorted["Year"] == A_y)].index[0] + 1}/{len(df)}")


def play(df: pd.DataFrame, csv: str, ranked=False):
    if ranked:
        sorted_inds = df.sort_values("ELO", ascending=False).index.to_list()

        pairs = list(zip(sorted_inds[::2], sorted_inds[1::2]))
        random.shuffle(pairs)
        inds = [x for pair in pairs for x in pair]
    else:
        inds = list(range(len(df)))
        random.shuffle(inds)
    
    while (len(inds) >= 2):
        A_i, B_i = inds.pop(), inds.pop()
        A_n, B_n = df.iloc[A_i, 0], df.iloc[B_i, 0]
        A_s, B_s = df.iloc[A_i, 1], df.iloc[B_i, 1]
        A_l, B_l = df.iloc[A_i, 2], df.iloc[B_i, 2]
        A_y, B_y = df.iloc[A_i, 3], df.iloc[B_i, 3]

        A_ev = expected_value(A_s, B_s)
        B_ev = expected_value(B_s, A_s)

        resA = input(f"\nPlacement matchup:\n[1]: {A_n} ({A_y}) - [{round(A_ev, 2)}]\n[2]: {B_n} ({B_y}) - [{round(B_ev, 2)}]\n[0]: Tie\n[q]: Quit\n> ")
        while True:
            if resA == '0':
                resB = 0
                break
            elif resA == '1':
                resB = 2
                break
            elif resA == '2':
                resB = 1
                break
            elif resA == 'q':
                return
            else:
                resA = input("Invalid input.\n> ")

        df.loc[A_i] = [A_n, new_elo(A_s, int(resA), A_ev), A_l, A_y]
        df.loc[B_i] = [B_n, new_elo(B_s, resB, B_ev), B_l, B_y]

        df.to_csv(csv)


def set_match(df: pd.DataFrame, csv: str):
    """ Play a match between two items chosen by their index
    """
    A_i = input("CSV index of first item:\n>")
    while True:
        try:
            A_i = int(A_i)
            if (0 > A_i) or (A_i >= len(df)):
                raise ValueError
            break
        except:
            A_i = input("Invalid input.\n> ")

    B_i = input("CSV index of second item:\n>")
    while True:
        try:
            B_i = int(B_i)
            if (0 > B_i) or (B_i >= len(df)):
                raise ValueError
            break
        except:
            B_i = input("Invalid input.\n> ")

    A_n, B_n = df.iloc[A_i, 0], df.iloc[B_i, 0]
    A_s, B_s = df.iloc[A_i, 1], df.iloc[B_i, 1]
    A_l, B_l = df.iloc[A_i, 2], df.iloc[B_i, 2]
    A_y, B_y = df.iloc[A_i, 3], df.iloc[B_i, 3]

    A_ev = expected_value(A_s, B_s)
    B_ev = expected_value(B_s, A_s)

    resA = input(f"\nPlacement matchup:\n[1]: {A_n} ({A_y}) - [{round(A_ev, 2)}] >\n[2]: {B_n} ({B_y}) - [{round(B_ev, 2)}]\n[0]: Tie\n> ")
    while True:
        if resA == '0':
            resB = 0
            break
        elif resA == '1':
            resB = 2
            break
        elif resA == '2':
            resB = 1
            break
        else:
            resA = input("Invalid input.\n> ")

    df.loc[A_i] = [A_n, new_elo(A_s, int(resA), A_ev), A_l, A_y]
    df.loc[B_i] = [B_n, new_elo(B_s, resB, B_ev), B_l, B_y]

    df.to_csv(csv)
