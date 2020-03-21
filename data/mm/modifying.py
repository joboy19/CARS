import csv
import random
import string
import numpy as np

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
    print(out_dict[random.choice(list(out_dict.keys()))])
    
    filee.close()
    #adjust ratings to 1-5 scale

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

def get_context_user(user_id):
    filee = open("listening_data.csv", "r", encoding="utf-8")

    vals = [0 for x in range()]


def countries():
    filee = open("country_mapping.txt", "r", encoding="utf-8")

    out = []
    count = 0

    for x in filee:
        line = x.strip().split("\t")
        this_line = [line[0], line[1]]
        fileee = open("countryContinent.csv", "r")
        for y in fileee:
            line2 = y.strip().split(",")
            if line[1].lower() in line2[0].lower():
                this_line.append(line2[2])
                count += 1
        out.append(this_line)
        
        
    print(out)
    
    filee = open("country_test.csv", "a", encoding="utf-8", newline="")
    writer = csv.writer(filee, delimiter=",")
    writer.writerows(out)

    

countries()
        