import pickle
import numpy as np

pickle_in = open("meals", "rb")
meals = pickle.load(pickle_in)


# for index in range(0,len(meals)-1):
#     if meals.at[index, "Vegitarian"] == "veg":
#         meals.at[index, "Vegitarian"] = True
#     else:
#         meals.at[index, "Vegitarian"] = False

#meals["active"] = True
meals.at[53, "Vegitarian"] = True

# print(meals.head())
#
#meals.at[1:3, "active"] = False
#
# sam = (meals.loc[np.where(meals["active"] == True)])
# print(sam)
#
# print(len(meals))

pickle_out = open("meals", "wb")
pickle.dump(meals, pickle_out)
pickle_out.close()
