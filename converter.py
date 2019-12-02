import pandas as pd
import pickle

data = pd.read_csv("~/MEGA/01_Random/Food_List.csv")

pickle_out = open("meals", "wb")
pickle.dump(data, pickle_out)
pickle_out.close()

# results_log = [[]]
# pickle_out = open("log", "wb")
# pickle.dump(results_log, pickle_out)
# pickle_out.close()