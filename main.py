import csv
import os
import re

input_datei = "/Users/lehieuly/Downloads/Basics 23bca16ba4f4802fa965fa714fee7625.md" # Input Dateienpfad
output_csv = "/Users/lehieuly/Documents/anki_export.csv" # Output CSV-Dateipfad
media_folder = ""

cards = [] # In der Liste werden die Karten gespeichert

with open(input_datei, 'r', encoding='utf-8') as file: # Öffnet die Markdown Datei und speichert den Inhalt in der Variable lines
    lines = file.readlines()

frage = None # Variable für aktuelle Frage. Wichtig für erste if-Abfrage
antwort_zeilen = [] # Antworten werden hier gespeichert

for line in lines: # Iteration durch alle Zeilen im Markdown-Dokument
    line = line.strip() # Entfernt führende und nachfolgende Leerzeichen
    if line.startswith("- "):
        if frage and antwort_zeilen: # Wenn Frage und Antwort vorhanden sind, füge sie der Liste hinzu
            antwort = " ".join(antwort_zeilen).strip()
            cards.append((frage,antwort))
            antwort_zeilen = []
        frage = line[2:].strip() # Speichert die Frage, indem das "- " entfernt wird

    elif line.startswith("![]") or line.startswith("!["): # Überprüft, ob die Zeile ein Bild enthält
        match = re.search(r"!\[.*?\]\((.*?)\)", line) # Regex zum Extrahieren des Bildpfads
        if match: # Wenn ein Bildpfad gefunden wurde
            pfad = match.group(1) # Extrahiert den Pfad des Bildes
            dateiname = os.path.basename(pfad) # Extrahiert den Dateinamen des Bildes
            antwort_zeilen.append(f'<img src="{dateiname}">') # Fügt das Bild in die Antwort ein
    
    elif line: # Wenn die Zeile nicht leer ist und keine Frage oder Bild ist
        antwort_zeilen.append(line.strip()) # Fügt die Zeile zur Antwort hinzu

if frage and antwort_zeilen: # Wenn am Ende der Datei noch eine Frage und Antwort vorhanden sind, füge sie hinzu
        antwort = " ".join(antwort_zeilen).strip()
        cards.append((frage,antwort))
 
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile: # Öffnet die CSV-Datei zum Schreiben
    writer = csv.writer(csvfile, delimiter=';') # Erstellt einen CSV-Schreiber mit Semikolon als Trennzeichen
    writer.writerow(['Frage', 'Antwort']) # Schreibt die Header-Zeile in die CSV-Datei
    for frage, antwort in cards: # Iteriert durch alle Karten und schreibt sie in die CSV-Datei
        writer.writerow([frage, antwort])
        x += 1 

print(f"{x} Anki-Karten wurden in {output_csv} exportiert.")

        
