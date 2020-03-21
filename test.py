import numpy as np 
import pandas as pd 
import random as random
import csv
from scipy.sparse.linalg import svds

k = 2


ratings = pd.read_csv("data/mm/listening_data.csv")
#print(ratings.head())

df_ratings = ratings.drop(columns=["longitude", "latitude", "country-id", "city-id", "artist-id"])
print(df_ratings.head())

df_ratings["rating"] = 1
print(df_ratings.head())

rdf = df_ratings.pivot_table(index="user-id",columns="track-id",values="rating").fillna(0) 
print(rdf.head())

"""
r = rdf.values
mean = np.mean(r, axis=1)
demean = r - mean.reshape(-1, 1)

print("input matrix")
print(r)

U, sigma, Vt = svds(demean, k=k)

print(U)
print(Vt)
sigma = np.diag(sigma)


vals = np.matmul(U, Vt) + mean.reshape(-1, 1)

VtS = np.matmul(sigma, Vt)
print(VtS)

#to get a prediction for a pre-existing user: get the values at vals[userID, book_ID]
#to get best predictions for a pre-existing user: find max of unseen values

newP = np.array([5,0,0,0,5])


new_person_value = np.matmul(newP, Vt)
print(new_person_value)

"""








