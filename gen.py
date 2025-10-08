import random
import pandas as pd
from fetchData import *
#---------Both---------

def genName(gender):
    name =  ""
    if gender == "Männlich":
        name = random.choice(names.loc[names['geschlecht'] == 'm', 'vorname'].tolist())
    else:
        name = random.choice(names.loc[names['geschlecht'] == 'w', 'vorname'].tolist())
    name += " " + random.choice(surnames['name'].tolist())
    return name

def genAge():
    return random.randint(20, 65)

def genGender(name):
    if name.split(" ")[0] in names.loc[names['geschlecht'] == 'm', 'vorname'].tolist():
        return "Männlich"
    elif name.split(" ")[0] in names.loc[names['geschlecht'] == 'w', 'vorname'].tolist():
        return "Weiblich"
    else:
        return random.choice(["Männlich", "Weiblich"])

def genBirthplace():
    return random.choice(cities['stadt'].tolist())

def genResidence():
    return random.choice(cities['stadt'].tolist())

def genMaritalStatus(age):
    age = int(age)
    if age < 25:
        return random.choice(["Ledig", "Vergeben"])
    else:
        return random.choice(["Ledig", "Verheiratet", "Verlobt", "Vergeben"])

def genHobbies():
    freetime = ""
    for i in range(4):
        hobby = random.choice(hobbies['hobby'].tolist())
        while hobby in freetime:
            hobby = random.choice(hobbies['hobby'].tolist())
        freetime += hobby + ", "
    return freetime[:-2]

#---------Professional---------
def professionalPosition():
    return "Softwareentwickler"

def professionalCV():
    return "Lebenslauf-Inhalt"

def professionalSkills():
    return "Programmierkenntnisse, Projektmanagement"

def professionalGoals():
    return "Karriereziele-Inhalt"

def professionalStrengths():
    return "Stärken-Inhalt"

def professionalWeaknesses():
    return "Schwächen-Inhalt"

def professionalSoftskills():
    return "Kommunikation, Teamarbeit"

#---------Personal---------
def personalUsername(name):
    name = name.lower()
    name = name.replace(" ", ".")
    if random.choice([True, False]):
        name = name.replace("a", "4")
    if random.choice([True, False]):
        name = name.replace("e", "3")
    if random.choice([True, False]):
        name = name.replace("i", "1")
    if random.choice([True, False]):
        name = name.replace("o", "0")
    if random.choice([True, False]):
        name += str(random.randint(1, 99))
    if random.choice([True, False]):
        name = name.replace("u", "v")
    return name

def personalLivingSituation():
    return random.choice(["Allein", "Mit Partner", "Mit Familie", "WG"])

def personalOccupation():
    return "Beruf-Inhalt"

def personalEducation(age):
    if age < 21:
        return random.choice(["Hauptschule", "Realschule", "Ausbildung", "Abitur"])
    elif age <= 23:
        return random.choice(["Hauptschule", "Realschule", "Ausbildung", "Abitur", "Bachelor"])
    elif age <= 30:
        return random.choice(["Hauptschule", "Realschule", "Ausbildung", "Abitur", "Bachelor", "Master"])
    else:
        return random.choice(["Hauptschule", "Realschule", "Ausbildung", "Abitur", "Bachelor", "Master", "Promotion"])


def personalGoals():
    return "Persönliche Ziele-Inhalt"

def personalStrengths():
    return "Persönliche Stärken-Inhalt"

def personalWeaknesses():
    return "Persönliche Schwächen-Inhalt"

def personalCharacterTraits():
    return "Charaktereigenschaften-Inhalt"

def personalValues():
    return "Werte-Inhalt"

def personalLifestyle():
    return "Lebensstil-Inhalt"

def personalInterests():
    return "Interessen-Inhalt"

def personalMediaUsage():
    return "Mediennutzungsverhalten-Inhalt"

def personalConsumptionBehavior():
    return "Konsumverhalten-Inhalt"

def personalLifeGoals():
    return "Lebensziele-Inhalt"

def personalBackgroundStory():
    return "Hintergrundgeschichte-Inhalt"