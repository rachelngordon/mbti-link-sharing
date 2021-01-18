import pandas as pd
import matplotlib.pyplot as plt

# read in the data and create a list of all Myers Briggs Personality Types
data=pd.read_csv("mbti_1.csv")
mbti_types=['INTJ','INTP','ENTJ','ENTP','INFJ','INFP','ENFJ','ENFP',
            'ISTJ','ISFJ','ESTJ','ESFJ','ISTP','ISFP','ESTP','ESFP']

# finds a given type in the data and returns all of the posts made by that type
def find_type(type_name):
    type_posts=data[data.type.isin([type_name])]
    return type_posts['posts']

# counts how many times a particular personality type is found in the data
def find_num_type(type_name):
    num_type=len(find_type(type_name))
    return num_type

# creates a new dictionary in which each personality type is a key and its value is a string of
# posts made by that type
types_data={}
for type_name in mbti_types:
    x=find_type(type_name)
    x=x.to_string(index=False)
    x=x.strip('\n')
    types_data[type_name]=x

import re

# uses a regular expression to find all of the URLs within a given string and return the number of
# URLS found
def findURL(string):
    regex="http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    x=re.findall(regex,string)
    return len(x)

# counts the number of links posted by each type in a given list of personality types and returns 
# the results as a dictionary
def find_links(list_types):
    num_links={}
    for type_name in list_types:
        num_links[type_name]=findURL(types_data[type_name])
    return num_links

# counts the number of posts made by each type in a given list and returns results as a dictionary
def find_posts(list_types):
    num_posts={}
    for type_name in list_types:
        num_posts[type_name]=find_num_type(type_name)
    return num_posts

# calculates the ratios of links to number of posts for each type in a given list and returns the
# results as a dictionary
def calc_ratios(list_types):
    links=find_links(list_types)
    posts=find_posts(list_types)
    ratios={}
    for type_name in list_types:
        ratios[type_name]=round(links[type_name]/posts[type_name], 2)
    return ratios

print(calc_ratios(mbti_types))

# plots the ratio of links posted for each Myers Briggs Personality Type in a bar chart
types_ratios=pd.DataFrame.from_dict(calc_ratios(mbti_types), orient="index")
fig=plt.figure()
plot=types_ratios.plot(kind="bar")
plot.get_legend().remove()
plot.set_title("Ratio of URLs Posted to Total Posts for MBTI Types")
plot.set_xlabel("MBTI Type")
plot.set_ylabel("Ratio")
plt.savefig('mbti_URLanalysis.png', dpi=400)

# dictionary of regular expressions for finding all types with a given personality trait
regex_dict={"I":"I[A-Z][A-Z][A-Z]", "E":"E[A-Z][A-Z][A-Z]", "S":"[A-Z]S[A-Z][A-Z]", 
            "N":"[A-Z]N[A-Z][A-Z]", "T":"[A-Z][A-Z]T[A-Z]", "F":"[A-Z][A-Z]F[A-Z]", 
            "J":"[A-Z][A-Z][A-Z]J", "P":"[A-Z][A-Z][A-Z]P"}

# finds a list of types with a given personality trait
def find_quality(regex):
    list_types=re.findall(regex, str(mbti_types))
    return list_types

# calculates the ratio of links to posts for a given personality trait
trait_ratios={}
for quality in regex_dict:
    list_types=find_quality(regex_dict[quality])
    sum_links=pd.Series(find_links(list_types)).sum()
    sum_posts=pd.Series(find_posts(list_types)).sum()
    links_ratio=round(sum_links/sum_posts, 2)
    trait_ratios[quality]=links_ratio
    print("Ratio of Links Posted for Personality Trait ", quality, " = ", links_ratio)

# plots the ratio of links posted for each personality trait in a bar chart
trait_ratios=pd.DataFrame.from_dict(trait_ratios, orient="index")
fig=plt.figure()
plot=trait_ratios.plot(kind="bar", color="red")
plot.get_legend().remove()
plot.set_title("Ratio of URLs Posted to Total Posts for MBTI Traits")
plot.set_xlabel("MBTI Trait")
plot.set_ylabel("Ratio")
plt.savefig('MBTItraits_URLanalysis.png', dpi=400)