import csv
import random
import string
import numpy as np

regions = ['Middle Africa', 'Western Africa', 'Central America', 'South America', 'South-Eastern Asia', 'Eastern Asia', 'Eastern Africa', 'South Africa', 'Southern Africa', 'Northern Europe', 'Western Asia', 'Southern Asia', 'Southern Europe', 'Eastern Asian', 'Caribbean', 'Eastern Europe', 'Australia and New Zealand', 'South Asia', 'Central Asia', 'Africa', 'Nothern Europe', 'Western Europe', 'Northern Africa', 'Northern America']
country_to_region = {}
countries = open("country_test.csv", "r", encoding="utf-8")
for x in countries:
    line = x.strip().split(",")
    if line[2] != "sub_region":
        country_to_region[line[0]] = regions.index(line[2])

def prep():
    a = []
    with open("listening_data.txt", "r", encoding="utf-8") as filee:
        for x in filee:
            a.append(x.strip().split("\t"))

    with open("listening_data.csv", "a", encoding="utf-8", newline="") as filee:
        writer = csv.writer(filee, delimiter=",")
        writer.writerows(a)

def user_generate():
    usersids = set()
    with open("listening_data.csv", "r", encoding="utf-8") as filee:
        for x in filee:
            usersids.add(x.strip().split(",")[0])
    
    with open("user_data.csv", "a", encoding="utf-8", newline="") as filee:
        writer = csv.writer(filee, delimiter=",")
        writer.writerow(["user-id","password","chosen_country","favourite_country","actual_county"])
        for x in list(usersids):
            country = random.randint(0, 179)
            writer.writerow([x, ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)]), country, country, country])

def get_ratings2():
    fileeU = open("users.csv", "r", encoding="utf-8")

    for x in fileeU:
        lineU = x.strip().split(",")
        user_id = lineU[0]
        filee = open("listening_data.csv", "r", encoding="utf-8")
        user_dict = {}
        for y in filee:
            line = y.strip().split(",")
            if line[0] == user_id:
                if line[6] in user_dict:
                    user_dict[line[6]] = user_dict[line[6]] + 1
                else:
                    user_dict[line[6]] = 1
        print(user_dict)


    filee.close()
    fileeU.close()


#for editing the file
def get_ratings_all():
    filee = open("listening_data.csv", "r", encoding="utf-8")

    user_dict = {}
    
    #get ratings counts for users
    for x in filee:
        line = x.strip().split(",")
        if line[0] in user_dict:
            if line[6] in user_dict[line[0]]:
                user_dict[line[0]][line[6]][0] = user_dict[line[0]][line[6]][0] + 1
            else:
                 user_dict[line[0]][line[6]] = [1] + line[1:-1]
        else:
            user_dict[line[0]] = {}
            user_dict[line[0]][line[6]] = [1] + line[1:-1]

    count = 0
    out_dict = {}
    list3 = []
    list2 = []
    #filter dictionary
    for x in user_dict:
        if len(user_dict[x]) > 10:
            out_dict[x] = user_dict[x]
            list3.append(len(user_dict[x]))

    filee.close()
    filee = open("listening_data.csv", "r", encoding="utf-8")
    out = []
    for x in filee:
        line = x.strip().split(",")
        if line[0] in out_dict.keys():
            out.append(line)
    filee.close()
    out_file = open("listening_data_test.csv", "a", encoding="utf-8", newline="")
    writer = csv.writer(out_file, delimiter=",")
    writer.writerows(out)
    #adjust ratings to 1-5 scale

get_ratings_all()

def get_ratings_user(user_id):
    filee = open("listening_data.csv", "r", encoding="utf-8")

    user_dict = {}

    for x in filee:
        line = x.strip().split(",")
        if line[0] == user_id:
            if line[6] in user_dict:
                user_dict[line[6]][0] = user_dict[line[6]][0] + 1
            else:
                user_dict[line[6]] = [1] + line[1:-1]

    filee.close()




#done
def get_context_user(user_id):
    filee = open("country_test.csv", "r", encoding="utf-8")
    countries = list(filee)
    filee2 = open("listening_data.csv", "r", encoding="utf-8")

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
    filee2 = open("listening_data.csv", "r", encoding="utf-8")

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






        