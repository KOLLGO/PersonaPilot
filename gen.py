import random
#---------Both---------

def genName():
    return "Max Mustermann"

def genAge():
    return random.randint(20, 65)

def genGender():
    return random.choice(["Männlich", "Weiblich"])

def genBirthplace():
    return "Berlin"

def genResidence():
    return "München"

def genMaritalStatus():
    return random.choice(["Ledig", "Verheiratet", "Verlobt", "Vergeben"])

def genHobbies():
    return "Lesen, Reisen, Sport"

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