import pandas as pd


def clean(dfs):  # data cleaning
    for df in dfs:
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        df.columns = df.columns.str.strip().str.lower()


# load data
character_traits = pd.read_csv("data/character_traits.csv")
cities = pd.read_csv("data/cities.csv")
consumerism = pd.read_csv("data/consumerism.csv")
hobbies = pd.read_csv("data/hobbies.csv")
jobs = pd.read_csv("data/jobs.csv")
lifegoals = pd.read_csv("data/lifegoals.csv")
lifestyles = pd.read_csv("data/lifestyles.csv")
media = pd.read_csv("data/media.csv")
names = pd.read_csv("data/names.csv", sep=";")
pers_attributes = pd.read_csv("data/pers_attributes.csv")
prof_attributes = pd.read_csv("data/prof_attributes.csv")
prof_goals = pd.read_csv("data/prof_goals.csv")
softskills = pd.read_csv("data/softskills.csv")
surnames = pd.read_csv("data/surnames.csv")
values = pd.read_csv("data/values.csv")
vars = [
    character_traits,
    cities,
    consumerism,
    hobbies,
    jobs,
    lifegoals,
    lifestyles,
    media,
    names,
    pers_attributes,
    prof_attributes,
    prof_goals,
    softskills,
    surnames,
    values,
]
clean(vars)  # call cleaning
