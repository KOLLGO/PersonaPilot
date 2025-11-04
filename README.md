# PersonaPilot

## 1. Grundgedanken

Die Software unterstützt beim Erstellen von Fake-Persona für ethisches Hacking. Die Gesamtheit der Eigenschaften soll eine Person möglichst lückenlos beschreiben, um immer aussagefähig zu sein.

Professionelle Persona sind für den Einsatz in Enterprise-Umgebungen gedacht, ihre Eigenschaften entsprechend fokussiert auf berufliche Eigenschaften für Bewerbungen.

Persönliche Persona sind für Interaktionen unter Privatpersonen vorgesehen. Einige Eigenschaften sind auch nützlich, um eine Social-Media Präsenz der Persona aufzubauen.

Wesentliche Eigenschaften wie Name und Alter sind bei beiden Typen gleich.



Die Software kann als reines Formular verwendet werden, sofern dem User selbst genug Eigenschaften einfallen.

Falls nicht, sind Generatoren implementiert, welche die jeweilige Eigenschaft basierend auf anderen Parametern der Persona sinnvoll ausfüllen.



Auswahl von MBTI für die Persönlichkeitstypen: beschreibt alle wesentlichen Persönlichkeitstypen sehr treffend mit wenigen Parametern, für Weiterverarbeitung mit KI oder zum selbst nachlesen gut geeignet

## 2. Software

### 2.1. Aufbau und Installation

**Aufbau**

- geschrieben und getestet unter Python 3.11.0

- assets: Dateien für Readme, Logo

- data: Datensätze für generatoren

- `fetchData.py`: Datenvorverarbeitung (Einlesen und Bereinigen)

- `gen.py`: Generatoren-Logik

- `main.py`: UI und Ablaufsteuerung



**Installation**

- im Installationsordner

```bash
git clone https://github.com/KOLLGO/PersonaPilot.git
```

```bash
cd PersonaPilot
```

```bash
pip install -r requirements.txt
```

```bash
python main.py
```



### 2.2. UI und Controls

![](https://github.com/KOLLGO/PersonaPilot/blob/main/assets/home.png)

1. Tab Selection
   
   - neue Tabs öffnen
   
   - schließen mit mittlerer Maustaste (`MMB`)

2. Persona Creation
   
   - Persona erstellen: neue Persona
   
   - Persona laden: vorhandene Persona aus CSV-Datei laden (Typ automatisch erkannt)

![](https://github.com/KOLLGO/PersonaPilot/blob/main/assets/types.png)

3. Wahl zwischen den Persona-Typen

![](https://github.com/KOLLGO/PersonaPilot/blob/main/assets/persona.png)

4. Speichert die Persona als CSV, die später wieder vom Programm geöffnet werden kann

5. Kopiert die Persona-Beschreibung, um sie als Kontext für KI, z.B. in LMStudio zu nutzen (beispielsweise als Chatbot)

6. Eingabefeld + Speicher-Button
   
   - Speicher-Button setzt den Eingabewert fest
   
   - um ihn wieder zu editieren: auf Bearbeiten clicken
   
   - alle felder werden bei click auf 4. automatisch gespeichert

7- Ruft den entsprechenden Generator für das Eingabefeld auf



## 3. Probleme und Anmerkungen

- Reverse-Bildersuche Kette nicht implementiert, da das händisch letzendlich nicht  viel aufwendiger wäre und nicht jeder Service eine zugängliche API hat

- Generatoren sind nur teilweise implementiert
  
  - Welche gibt es?
    
    - Name (abhängig von Geschlecht)
    
    - Geschlecht (abhängig von Name)
    
    - Alter (random)
    
    - Geburtsort (random)
    
    - Wohnort (random)
    
    - Familienstand (abhängig von Alter)
    
    - Hobbies (random)
    
    - Beruf (abhängig von Digitalaffinität)
    
    - Username (regelbasiert)
    
    - Wohnsituation (random)
    
    - Bildungsgrad (abhängig von Alter)
  
  - Warum die anderen nicht?
    
    - sehr schwer, mit allen Parametern aber überschaubarem Aufwand zuverlässige Generatoren zu programmieren (Lebenslauf muss Sinn zum alter machen, Hobbies zu den Fähigkeiten passen, usw.)
    
    - für komplexere Generatoren müssten die Daten wesentlich mehr und passende Attribute haben (Beispiel: Hobbies sollten Extroversion, Fähigkeiten, Beruf, Stärken und Schwächen berücksichtigen)
    
    - Annotationsaufwand ist dafür groß, KI dabei nicht immer zuverlässig
  
  - Lösungsvorschläge
    
    - Zufallsgeneratoren mit den vorhandenen Datensätzen
    
    - API eines KI-Services (besonders für Lebenslauf)
    
    - weniger oder keine Parameter verwenden
    
    - Generator-Felder für nicht implementierte entfernen

## 4. Quellen

- Datenquellen
  
  - Vornamen [govdata](https://www.govdata.de/suche/daten/vornamen-27), [dl-de/by-2-0](https://www.govdata.de/dl-de/by-2-0), verändert
  
  - Nachnamen [Datenbörse](https://www.xn--datenbrse-57a.net/item/Die_200_haeufigsten_Nachnamen_in_Deutschland_Excel-Liste), [dl-de/by-2-0](https://www.govdata.de/dl-de/by-2-0), verändert
  
  - alle anderen: Generiert von [Perplexity](https://www.perplexity.ai)

- Quelle MBTI
  
  - Patrick King - read people like a book
