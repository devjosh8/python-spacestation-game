# Dokumentation

# Inhaltsverzeichnis
1. [Grundlegender Aufbau, Funktion und Ansatz](#introduction)
2. [Programmarchitektur](#2)
3. [Programmablauf](#1)
4. [Testergebnisse und Analyse](#0)


# Grundlegender Aufbau, Funktionen und Ansatz <a name="introduction"></a>

## Vorüberlegungen und erste Ideeen

Das Ziel des Spiels soll es sein, alle Räume einer Raumstation zu scannen und dabei den Scan eines Raums, der als "gefährlich"  markiert ist, zu vermeiden. Dabei sollen bereits gescannte Räume anzeigen, wie viele der nebenliegenden Räume "gefährlich"  sind.

Die Spielprinzipien sind folgende:

* Es gibt ein Spielfeld mit Bereichen, wobei jeder Bereich _sicher_ oder _gefährlich_ sein kann
* In einem Spielzug kann ein Bereich gescannt werden. Wenn der Bereich _sicher_ ist, erscheint in diesem Bereich eine Zahl die angibt, wie viele umliegende Bereiche _gefährlich_ sind
* Wenn alle _sicheren_ Bereiche gescannt wurden und man keinen _gefährlichen_ Bereiche gescannt hat, hat man das Spiel gewonnen

### Die Raumstation als verbundene Räume

<div style="float: left; margin-right: 15px; max-width: 300px;">
  <img src="images/raum_problem.png" alt="Bildbeschreibung" />
</div>


*Abbildung 1: Demonstration von Problemen*

Um die Spielregeln zu erfüllen und den Spielspaß zu garantieren, ist es nötig, sich vorher ein paar Grundideeen zu überlegen. Grundsätzlich wäre es möglich, ein Raster als Spielfeld zu verwenden, allerdings ist eine Raumstation eher eine Ansammlung von Räumen, die miteinander verbunden sind. Somit soll das Programm Räume generieren, welche miteinander verbunden sind. Es gibt aber Probleme, wenn Räume nur über einen Weg verbunden sind. 

Wenn der Spieler in _Abbildung 1_ die Information über Raum 1 hat, dass dieser gefährlich ist aber keine Information über Raum 2 hat, so ist der Scan von Raum 2 rein zufällig und kann, wenn man Pech hat, das Spiel beenden. Solche Situation führen zur Verringerung des Spielspaßes und müssen deshalb vermieden werden.

Deshalb muss garantiert werden, dass es keine Sackgassen gibt, die nach mehreren nur einzeln verbundenen Räumen entstehen. Die meisten Räume der Raumstation sollten entweder 2 oder mehr Verbindungen haben.

### Test-driven Development

Im Test-driven Development werden nicht die Tests nach dem eigentlich Programmcode geschrieben, sondern mithilfe der Tests wird zuerst die Funktion des Programmcodes festgelegt und beschrieben, nach welchen dieser dann verfasst wird.

In diesem Python-Projekt soll dieser Ansatz verfolgt und wie es möglich ist umgesetzt werden.

### Räume generieren

Eine der wichtigsten Funktionen ist somit das Generieren von Räumen der Raumstation. Räume werden also in einem Algorithmus generiert, der eine bestimmte Anzahl von Räumen und Verbindungen generiert und dann abbricht. Es müssen zufällig bereits bestehende Räume ausgewählt werden, die nicht bereits an jeder Seite einen Nachbarraum haben. Dann wird dieser zufällig ausgewählte Raum in eine zufällige Richtung erweitert, wenn der neue Raum Nachbar-Räume hat, wird der neue Raum mit diesen Nachbarn verbunden.

### Userinterface
Wohl eines der wichtigsten Dinge für optimale User-Experience ist das Userinterface. Es sollte einfach erkennbar sein, welche Räume man gescannt hat und welche man scannen kann. Ein Userinterface sollte stets einfach zu nutzen sein, aber trotzdem alle wichtigen Informationen auf einen Blick anzeigen. Wichtig für das Spiel ist:
* Eine Karte der Räume
* Gescannte Räume zeigen Anzahl der gefährlichen Nachbarräume an
* Scannen eines neuen Raumes

Eine Karte, die einen Raum darstellt könnte ungefähr so aussehen, wobei jede Raute (#) einen nicht gescannten Raum zeigt und gescannte Räume die Anzahl an nebenliegenden gefährlichen Räumen anzeigen. Die Verbindungen zwischen den Zeichen stellen die Verbindungen der Räume da.

```
  1 - #       # - #
    \ |     / | \
      2 - 1 - # - #
      |       | X |
      #       # - 1
```
*Abbildung 2 Vorüberlegung für die Darstellung von Räumen*

Es muss irgendwie für den User möglich sein, dem Spiel mitzuteilen, welcher Raum als nächstes gescannt werden soll. Es wäre hier nicht praktikabel jedem Raum einfach eine Nummer zu geben den User nach der Nummer des Raumes zu fragen, den er aufdecken möchte, weil es hier Probleme mit einer kompakten Darstellung gäbe. Wie will man denn wie in Abbildung 2 gezeigt, jetzt noch wohlmöhlich 2-stellige Zahlen an die Räume notieren, ohne dass das Userinterface unschön wird?

Eine einfachere Methode für den User, mit unter schwerer im Code, ist die Möglichkeit für den User mithilfe der Pfeiltasten oder den Tasten WASD den Raum der gescannt werden soll auszuwählen. Der User sollte hier Feedback durch eine farbige Markierung des aktuell ausgewählten Raumes **<span style="color:green;">#</span>** bekommen.

## Grundlegende Funktionen
In diesem Kapitel werden die grundlegenden Funktionen des Projektes erläutert und inwiefern die oben genannten Vorüberlegungen tatsächlich im Code umgesetzt wurden.

### Spielstart - Räume generieren
Zum Spielstart ist das Spielfeld leer. Das Spielfeld wird in jedem Spiel neu generiert, sodass Abwechslung beim Spielen garantiert ist. Die Generierung eines Spielfeldes ist eine große Herausforderung, da es viele verschiedene Konstellationen zwischen Räumen gibt. Es muss ein grundlegendes Schema festgelegt werden, nachdem die Generierung passiert:
```
  1. einen Raum in der Mitte der Karte erzeugen
  2. eine zufällige Richtung aussuchen
  3. in diese Richtung einen Raum erzeugen und beide Räume verbinden

  4. einen zufälligen Raum auf der Karte auswählen
  5. eine zufällige Richtung aussuchen
    6a: wenn ein Raum in diese Richtung exisitert, beide Räume verbinden
    6b: ansonsten einen Raum in diese Richtung erzeugen und Verbindung herstellen
  7: gehe so lange zu 4 bis genügend Räume existieren

  8: Solange alle Räume die nur eine Verbindung haben entfernen, bis nur noch Räume mit mehr als einer Verbindungen übrig bleiben
```
Anschließend müssen Räume als _sicher_ oder _gefährlich_ klassifiziert werden:
```
  1. gehe alle Räume durch
    2. setze Räume zufällig auf "gefährlich" mit einer bestimmten Wahrscheinlichkeit
  3. gehe nochmal alle Räume durch
    4. setze für jeden Raum die Anzahl an gefährlichen Nachbarräumen, sodass diese später nicht berechnet werden muss
```

# Programmarchitektur

## Projektaufbau

```
.
├── mypy.ini
├── README.md
├── requirements.txt
├── documentation
│   └── documentation.pdf
├── source
│   ├── main.py
│   └── example.py
└── tests
    ├── test_main.py
    └── test_example.py
```

Der Projektaufbau folgt den Bestimmungen in den Anforderungen an das Projekt.

# Programmablauf
# Testergebnisse und Analyse