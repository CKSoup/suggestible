import pickle
import numpy as np
import plotly.graph_objects as go
import plotly
import pandas as pd


def main(romeo, ratio):

    meals = pd.read_csv("meals.csv", index_col=0)

    pickle_in = open("log", "rb")
    results_log = pickle.load(pickle_in)

    veg_opts = []
    meat_opts = []
    for index in range(0, len(meals)):
        if meals.at[index, "active"]:
            if meals.at[index, "Vegetarian"]:
                veg_opts.append(index)
            else:
                meat_opts.append(index)

    mresults = results_log[len(results_log) - 30:len(results_log)]

    dishes = meals["Dish"]
    log = []
    for items in range(len(mresults)):
        gen = (i for i, x in enumerate(dishes) if x == mresults[items])
        for i in gen:
            log.append(i)

    def probabilities(dataset):
        n = len(dataset)
        probs = []

        for run in range(0, n):
            if dataset[run] in log:
                if dataset[run] in log[20:30]:
                    probs.append(1 / n * 0.3)
                else:
                    if dataset[run] in log[10:20]:
                        probs.append(1 / n * 0.6)
                    else:
                        if dataset[run] in log[0:10]:
                            probs.append(1 / n * 0.8)
            else:
                probs.append(1)

        def assign_new(x):
            ar = np.asarray(x, dtype=float)
            in_log = ar[np.where(ar != 1)]

            if len(in_log) == 0:
                b = 0
                length = 0
            else:
                b = np.sum(in_log)
                length = len(in_log)

            new_ps = (1 - b) / (n - length)
            ar[np.where(ar == 1)] = new_ps

            return ar

        return assign_new(probs)

    def food_suggestions(ratio):
        if ratio == 0.5:
            ratio = 0.505
        vegdays = np.round(ratio * days, 0)
        meatdays = np.round((1 - ratio) * days, 0)
        veg = np.random.choice(veg_opts, size=np.int_(vegdays), p=probabilities(veg_opts), replace=False)
        meat = np.random.choice(meat_opts, size=np.int_(meatdays), p=probabilities(meat_opts), replace=False)
        suggestions = np.concatenate((veg, meat), axis=0)
        np.random.shuffle(suggestions)
        foods = []
        for index in range(0, len(suggestions)):
            foods.append(meals.at[suggestions[index], "Dish"])
        return foods

    # placeholder_end = "2019-12-12"
    # placeholder_beg = "2019-12-04"

    # def dates(starting, ending):
    #     #end = ending.date()
    #     #start = starting.date()
    #     st = starting
    #     en = ending
    #     #en = end.toString("yyyy-MM-dd")
    #     en = parse(en)
    #     #st = start.toString("yyyy.MM.dd")
    #     st = parse(st)
    #
    #     def daterange(st, en):
    #         for n in range(int((en - st).days) + 1):
    #             yield st + timedelta(n)
    #
    #     fin_dates = []
    #     for dt in daterange(st, en):
    #         fin_dates.append(dt.strftime("%A %d.%m"))
    #
    #     return fin_dates
    #
    # romeo = dates(placeholder_beg, placeholder_end)

    days = len(romeo)
    results = food_suggestions(ratio)

    results_log = np.append(results_log[len(results_log)-50:len(results_log)], results)

    # foods = []
    # for index in range(0, len(results)):
    #     foods.append(meals.at[results[index], "Dish"])

    data0 = pd.DataFrame(columns=["Date", "Dish"])
    data0["Date"] = romeo
    data0["Dish"] = results

    pickle_out = open("log", "wb")
    pickle.dump(results_log, pickle_out)
    pickle_out.close()

    mine = data0
    # Code for plotly table

    layout = go.Layout(margin=dict(l=10, r=10, t=10, b=0),
                       paper_bgcolor="rgb(239,239,239)",
                       plot_bgcolor="rgb(0,0,0)")

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(mine.columns),
                    fill_color="rgb(255, 198, 40)",
                    line_color="black",
                    font=dict(color="black", size=24),
                    height=38),
        cells=dict(values=[mine.Date, mine.Dish],
                    fill_color="rgb(255,255,255)",
                    line_color="black",
                    font=dict(color="black", size=16),
                    height=30)
    )
                         ], layout=layout)


    my_plot = (plotly.offline.plot(
        fig,
        image_width='100%',
        image_height='100%',
        include_plotlyjs=False,
        output_type='div',
        auto_open=False,
    ))

    return my_plot
