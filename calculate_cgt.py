import pandas

import argparse


parser = argparse.ArgumentParser(description="Calculate CGT for stocks")

parser.add_argument("Path", metavar="path", type=str, help="Path to input csv")
parser.add_argument("--output", action="store", type=str)

args = parser.parse_args()

df = pandas.read_csv(
    args.Path,
    parse_dates=["date"],
)

df["taxed"] = len(df) * [0]
df["profit"] = len(df) * [0]

for sym in df["symbol"].unique():
    total_profit = 0

    for i_sell, sell in df.loc[
        (df["symbol"] == sym) & (df["sell or buy"] == "sell")
    ].iterrows():

        sell_total = sell["price"] * sell["Number of shares"]
        buy_total = 0

        req = sell["Number of shares"]
        rem = 0

        for i, buy in df.loc[
            (df["symbol"] == sym) & (df["sell or buy"] == "buy")
        ].iterrows():
            rem = buy["Number of shares"] - buy["taxed"]

            if req == 0:
                break
            if rem == 0:
                continue

            if req >= rem:
                buy_total += rem * buy["price"]
                req = req - rem
                rem = 0
            else:
                buy_total += req * buy["price"]
                rem = rem - req
                req = 0
            df.at[i, "taxed"] = buy["Number of shares"] - rem

        assert req == 0

        df.at[i_sell, "profit"] = sell_total - buy_total

        total_profit += sell_total - buy_total

print(f"Total profit = {total_profit}")
print(df)

if args.output is not None:
    df.to_csv(args.output, index=False)
