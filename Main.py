import pickle
import numpy as np


pickle_in = open("meals", "rb")
meals = pickle.load(pickle_in)

pickle_in = open("log", "rb")
results_log = pickle.load(pickle_in)

veg_opts = []
meat_opts = []
for index in range(0, len(meals)):
    if meals.at[index, "active"]:
        if meals.at[index, "Vegitarian"]:
            veg_opts.append(index)
        else:
            meat_opts.append(index)


mresults = results_log[len(results_log) - 30:len(results_log)]


def past_results(data):
    result = []
    for index in range(0, 30):
        if mresults[index] in veg_opts:
            result.append(mresults[index])
    return result


def probabilities(dataset):
    n = len(dataset)
    probs = []

    for run in range(0, n):
        if dataset[run] in mresults:
            if dataset[run] in mresults[20:30]:
                probs.append(1 / n * 0.3)
            else:
                if dataset[run] in mresults[10:20]:
                    probs.append(1 / n * 0.6)
                else:
                    if dataset[run] in mresults[0:10]:
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


def food_suggestions(days, ratio):
    if ratio == 0.5:
        ratio = 0.505
    vegdays = np.round(ratio * days, 0)
    meatdays = np.round((1 - ratio) * days, 0)
    veg = np.random.choice(veg_opts, size=np.int_(vegdays), p=probabilities(veg_opts), replace=False)
    meat = np.random.choice(meat_opts, size=np.int_(meatdays), p=probabilities(meat_opts), replace=False)
    suggestions = np.concatenate((veg, meat), axis=0)
    np.random.shuffle(suggestions)
    return suggestions

# ratio = 0.7
# days = 12
# print(np.random.choice(veg_opts, size=np.round(0.8 * days, 0), p=probabilities(veg_opts)))
# print(np.round(ratio * days, 0))
# print(np.round((1 - ratio) * days, 0))
# print(type(np.int_(np.round(ratio * days, 0))))
# print(food_suggestions(10, 0.7))
# print(meals)


results = food_suggestions(10, 1)

results_log = np.append(results_log[len(results_log)-50:len(results_log)], results)


pickle_out = open("log", "wb")
pickle.dump(results_log, pickle_out)
pickle_out.close()
