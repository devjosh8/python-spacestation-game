# Dokumentation

# Inhaltsverzeichnis
1. [Grundlegender Aufbau, Funktion und Ansatz](#introduction)
2. [Programmarchitektur](#2)
3. [Programmablauf](#1)
4. [Testergebnisse und Analyse](#0)


# Grundlegender Aufbau, Funktionen und Ansatz <a name="introduction"></a>

## Grundlegende Spielprinzipien

Das Ziel des Spiels soll es sein, alle Räume einer Raumstation zu scannen und dabei den Scan eines Raums, der als "gefährlich"  markiert ist, zu vermeiden. Dabei sollen bereits gescannte Räume anzeigen, wie viele der nebenliegenden Räume "gefährlich"  sind.

Die Spielprinzipien sind folgende:

* Es gibt ein Spielfeld mit Bereichen, wobei jeder Bereich _sicher_ oder _gefährlich_ sein kann
* In einem Spielzug kann ein Bereich gescannt werden. Wenn der Bereich _sicher_ ist, erscheint in diesem Bereich eine Zahl die angibt, wie viele umliegende Bereiche _gefährlich_ sind
* Wenn alle _sicheren_ Bereiche gescannt wurden und man keinen _gefährlichen_ Bereiche gescannt hat, hat man das Spiel gewonnen

### Erste Ideeen und Brainstorming

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

## Räume generieren

Eine der wichtigsten Funktionen ist somit das Generieren von Räumen der Raumstation. Räume werden also in einem Algorithmus generiert, der eine bestimmte Anzahl von Räumen und Verbindungen generiert und dann abbricht. Es müssen zufällig bereits bestehende Räume ausgewählt werden, die nicht bereits an jeder Seite einen Nachbarraum haben. Dann wird dieser zufällig ausgewählte Raum in eine zufällige Richtung erweitert, wenn der neue Raum Nachbar-Räume hat, wird der neue Raum mit diesen Nachbarn verbunden.

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

# Programmablauf
# Testergebnisse und Analyse