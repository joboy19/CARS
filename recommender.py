import csv
import random
import string
import numpy as np
import pandas as pd 
import math
import time
from scipy.sparse.linalg import svds


PATH_TO_LISTENING_DATA = "data/mm/listening_data.csv"
PATH_TO_USERS = "data/mm/user_data.csv"
PATH_TO_COUNTRIES = "data/mm/country_mapping.csv"
PATH_TO_STORE = "data/mm/store.h5"
PATH_TO_TRACK = "data/mm/track_mapping.csv"
PATH_TO_ARTIST = "data/mm/artist_mapping.csv"



def user_generate():
    usersids = set()
    with open(PATH_TO_LISTENING_DATA, "r", encoding="utf-8") as filee:
        for x in filee:
            usersids.add(x.strip().split(",")[0])
    
    with open(PATH_TO_USERS, "a", encoding="utf-8", newline="") as filee:
        writer = csv.writer(filee, delimiter=",")
        writer.writerow(["user-id","password","chosen_country","favourite_country","actual_county"])
        for x in list(usersids):
            country = random.randint(0, 179)
            writer.writerow([x, ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)]), country, country, country])


#get all of the ratings, with no context
def get_ratings_all():
    filee = open(PATH_TO_LISTENING_DATA, "r", encoding="utf-8")

    user_dict = {}
    
    #get ratings counts for users
    for x in filee:
        line = x.strip().split(",")
        if line[0] in user_dict:
            if line[6] in user_dict[line[0]]:
                user_dict[line[0]][line[6]]= user_dict[line[0]][line[6]] + 1
            else:
                 user_dict[line[0]][line[6]] = 1
        else:
            user_dict[line[0]] = {}
            user_dict[line[0]][line[6]] = 1

    filee.close()
    list_out = []
    #adjust ratings to 1-5 scale
    for x in user_dict.keys():
        val = int(user_dict[x][max(user_dict[x], key = user_dict[x].get)])/5
        this_one = [(x, k, math.ceil(v/val)) for k, v in user_dict[x].items()]
        list_out = list_out + this_one
    
    print("---SYSTEM---: Total unique ratings:", len(list_out))
    return list_out


def check_context(context, rating_line):
    if country_to_sub_region[rating_line[3]] == context:
        return True
    else:
        return False

#get all of the ratings with current context
def get_ratings_all_context(context):
    filee = open(PATH_TO_LISTENING_DATA, "r", encoding="utf-8")

    user_dict = {}
    
    #get ratings counts for users
    for x in filee:
        line = x.strip().split(",")
        if check_context(context, line):
            if line[0] in user_dict:
                if line[6] in user_dict[line[0]]:
                    user_dict[line[0]][line[6]]= user_dict[line[0]][line[6]] + 1
                else:
                    user_dict[line[0]][line[6]] = 1
            else:
                user_dict[line[0]] = {}
                user_dict[line[0]][line[6]] = 1
        

    print(user_dict)
    filee.close()
    list_out = []
    #adjust ratings to 1-5 scale
    for x in user_dict.keys():
        val = int(user_dict[x][max(user_dict[x], key = user_dict[x].get)])/5
        this_one = [(x, k, math.ceil(v/val)) for k, v in user_dict[x].items()]
        list_out = list_out + this_one
    
    print("---SYSTEM---: Total unique ratings:", len(list_out))
    return list_out
    



def get_ratings_user(user_id):
    filee = open(PATH_TO_LISTENING_DATA, "r", encoding="utf-8")

    user_dict = {}
    total = 0

    for x in filee:
        line = x.strip().split(",")
        if line[0] == user_id:
            if line[6] in user_dict:
                user_dict[line[6]] =  user_dict[line[6]] + 1
            else:
                user_dict[line[6]] = 1
    
    val = int(user_dict[max(user_dict, key = user_dict.get)])/5
    list_out = [(user_id, k, v/val) for k, v in user_dict.items()]
    filee.close()
    return list_out
   

def get_listens_user(user_id):
    filee = open(PATH_TO_LISTENING_DATA, "r", encoding="utf-8")

    user_dict = {}
    total = 0

    for x in filee:
        line = x.strip().split(",")
        if line[0] == user_id:
            if line[6] in user_dict:
                user_dict[line[6]][2] =  user_dict[line[6]][2] + 1
            else:
                try:
                    track = track_dict[line[6]][0]
                    artist = track_dict[line[6]][1]
                    user_dict[line[6]] = [artist, track , 1]
                except:
                    print(line[5], line[6])
    filee.close()

    return user_dict

#done
def get_context_user(user_id):
    filee = open("country_test.csv", "r", encoding="utf-8")
    countries = list(filee)
    filee2 = open(PATH_TO_LISTENING_DATA, "r", encoding="utf-8")

    vals = [0 for x in range(24)]
    count = 0

    for x in filee2:
        line = x.strip().split(",")
        if line[0] == user_id:
            count += 1
            vals[country_to_region[line[3]]] += 1
    
    if count > 0:
        vals = list(map(lambda x: x/count, vals))
    return vals

#done
def get_context_track(track_id):
    filee = open("country_test.csv", "r", encoding="utf-8")
    countries = list(filee)
    filee2 = open(PATH_TO_LISTENING_DATA, "r", encoding="utf-8")

    vals = [0 for x in range(24)]
    count = 0

    for x in filee2:
        line = x.strip().split(",")
        if line[6] == track_id:
            count += 1
            vals[country_to_region[line[3]]] += 1
    
    vals = list(map(lambda x: x/count, vals))
    return vals

def list_regions():
    filee = open("country_test.csv", "r", encoding="utf-8")
    out = set()
    for x in filee:
        line = x.strip().split(",")
        try:
            out.add(line[2])
        except:
            print(line)
    
    print(out)




regions = ['Middle Africa', 'Western Africa', 'Central America', 'South America', 'South-Eastern Asia', 'Eastern Asia', 'Eastern Africa', 'South Africa', 'Southern Africa', 'Northern Europe', 'Western Asia', 'Southern Asia', 'Southern Europe', 'Eastern Asian', 'Caribbean', 'Eastern Europe', 'Australia and New Zealand', 'South Asia', 'Central Asia', 'Africa', 'Nothern Europe', 'Western Europe', 'Northern Africa', 'Northern America']
country_to_region = {}
countries = {}
countries_file = open(PATH_TO_COUNTRIES, "r", encoding="utf-8")
for x in countries_file:
    line = x.strip().split(",")
    if line[2] != "sub_region":
        country_to_region[line[0]] = regions.index(line[2])
        countries[line[0]] = line[1]
countries_file.close()

tracks = open(PATH_TO_TRACK, "r", encoding="utf-8")
reader = csv.reader(tracks)
track_dict = {}
for x in reader:
    track_dict[x[0]] = [x[1]]
tracks.close()

artists = open(PATH_TO_ARTIST, "r", encoding="utf-8")
reader = csv.reader(artists)
artist_dict = {}
for x in reader:
    artist_dict[x[0]] = x[1]
artists.close()


for y in open(PATH_TO_LISTENING_DATA, "r", encoding="utf-8"):
    line = y.strip().split(",")
    try:
        track_dict[line[6]] = [track_dict[line[6]][0], artist_dict[line[5]]]
    except:
        pass

def get_countries():
    out = []
    for x in countries:
        out.append((x, countries[x]))
    return out


print("---SYSTEM---: STARTING")

k = 20

users = open(PATH_TO_USERS, "r", encoding="utf-8")
user_list = []
for x in users:
    user_list.append(x.strip().split(",")[0])
users.close()



print("---SYSTEM---: SVD calculated, with no context.")

def calc_svd(context_val=-1):
    print("---SYSTEM---: Calculating SVD")

    print("---SYSTEM---: Collecting ratings and calculating. Context Value:", context_val)
    if context_val != -1:
        ratings_list = get_ratings_all_context(context_val)
        print("---SYSTEM---: Ratings collected and calculated, with context.")
    else:
        ratings_list = get_ratings_all()
        print("---SYSTEM---: Ratings collected and calculated, without context.")

    df_ratings = pd.DataFrame(ratings_list, columns=["user-id", "track-id", "rating"])
    print("---SYSTEM---: Sanity Check:")
    print(df_ratings.head())

    df_ratings.astype({"rating":"int8"})

    rdf = df_ratings.pivot_table(index="user-id",columns="track-id",values="rating").fillna(0) 
    #print(rdf.head())

    rdf.to_hdf(PATH_TO_STORE, "data")

    #df = pd.read_hdf(PATH_TO_STORE)

    r = rdf.values
    mean = np.mean(r, axis=1)
    demean = r - mean.reshape(-1, 1)


    U, sigma, Vt = svds(demean, k=k)

    sigma = np.diag(sigma)
    Us = np.matmul(U, sigma)

    vals = np.matmul(Us, Vt) + mean.reshape(-1, 1)

    print("---SYSTEM---: SVD calculated.")

calc_svd()

def RMSE(pred, real):
    diff = abs(real - pred)
    return sum(diff)/len(diff)


def get_recommendation(user_id, recoms):
    user_index = list(rdf.axes[0]).index(user_id)
    user_row_pred = vals[user_index]
    user_row_real = np.array(rdf.iloc[user_index,:])
    #print(user_row_pred)
    #print(user_row_real)
    RMSE_ = RMSE(user_row_pred, user_row_real)

    user_pred = dict(zip(rdf.axes[1], user_row_pred))
    user_pred = np.array([(u, v) for u, v in sorted(user_pred.items(), key=lambda x: x[1], reverse=True)])
    #print(user_pred)

    out = []
    count = -1
    for x in user_pred:
        if not user_row_real[list(rdf.axes[1]).index(x[0])] > 0:
            out.append([x[0], track_dict[x[0]][0], track_dict[x[0]][1]])
            count += 1
            if count == recoms:
                break
         
    return out



        