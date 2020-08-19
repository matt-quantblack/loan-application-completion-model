def create_random_list(df):
    # hack to generate a fake list of customers for testing
    from random import random
    r = []
    for i in range(len(df.index)):
        r.append(round(random(), 2))
    df["Prob"] = r
    df = df.sort_values(by="Prob", ascending=False)
    df = df[:35]

    return df