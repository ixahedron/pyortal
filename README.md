# Praktikum Python mit Raspberry Pi  
  
### Ausführen
Mit `python3 Menu.py` ausführen. Steuerung mit Pfeiltasten und Maus fürs Setzen von Portalen bzw. auswählen der Menupunkte.

### Multiplayer
Auf einem Rechner muss man `Create a game` klicken, auf dem anderen mit `Connect to a game` sich mit dem ersten verbinden durch Eingabe einer IP-Addresse.

---

### Levels kreieren

Es gibt einen simplen **Map Editor**, den kann man mit `python3 MapEditor.py` ausführen.
Auswahl von Aktionen durch Drücken von Tasten:
- `p` - einfaches Platform, setzbar durch zwei Ecken mit jeweils einem Klick für jede Ecke
- `n` - ein schwarzes Platform (unterstützt keine Portale)
- `c` - Cube
- `b` - Button
- `d` - Door
- `e` - Exit
- `r` - Sprites löshen

`p` ist per Default ausgewählt. Nachdem eine Aktion ausgewählt wurde, kann man die Objekte mit Mausklicken platzieren. Scrollen mit Pfeiltasten ist unterstützt.  
Anschließend soll man den Level mit `s` speichern. Im Textfeld ist ein Name für die resultierende Datei einzugeben. Eine Erweiterung `.py` wird automatisch dazuaddiert. Z.B. falls `level` eingegeben wurde, wird der Level unter `level.py` gespeichert.  
Den gespeicherten Level muss man aber noch manuell ins Spiel einbauen. Dazu:
- In `Level.py` eine neue Klasse analog zu gegebenen definieren mit angepasstem _import statement_
- Die neue Levelklasse in `Singleplayer.py` bzw. `Multiplayer.py` in die Liste von Levels einfügen.

---

### Gruppenteilnehmer

Ilona Prikule  
Atef Azabi  
Victor Saemmer  
_SS16_
