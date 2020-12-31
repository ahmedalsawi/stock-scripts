import pandas

df = pandas.read_csv(
    "trans.csv",
    # parse_dates=["date"],
    # index_col='symbol',
)

# print(df)
# syms = df['symbol'].unique

# for sym in df['symbol'].unique():
#     print(f"====== Transactions for {sym}")
#     for i in range(len(df)) :
#         if df.loc[i,'symbol'] == sym:
#             print(df.loc[i])


for sym in df["symbol"].unique():
    print(f"====== Transactions for {sym}")
    sdf = df.loc[df["symbol"] == sym]

    sdf_buy = sdf.loc[sdf["sell or buy"] == "buy"]
    tax_calc = [0] * len(sdf_buy)
    sdf_buy["tax_calc"] = tax_calc
    # print(sdf_buy)

    sdf_sell = sdf.loc[sdf["sell or buy"] == "sell"]
    # print(sdf_sell)

    total_profit = 0

    for i, sell in sdf_sell.iterrows():
        sell_total = sell["price"] * sell["Number of shares"]
        buy_total = 0

        req = sell["Number of shares"]
        rem = 0

        for i, buy in sdf_buy.iterrows():
            rem = buy["Number of shares"] - buy["tax_calc"]

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

            sdf_buy.at[i, "tax_calc"] = buy["Number of shares"] - rem

        assert req == 0

        # print(
        #     f"sell_total = {sell_total}, Buy total = {buy_total} profit={sell_total - buy_total}"
        # )
        total_profit += sell_total - buy_total
print(f"Total profit = {total_profit}")
# print(sdf_buy)