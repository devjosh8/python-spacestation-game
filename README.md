# Python Spacestation Exam 2025

[Link zum Git Repository](https://github.com/devjosh8/python-spacestation-game)

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

* `README.md`: Diese Datei
* `documentation`: Enthält die Dokumentation für dieses Projekt
* `source`: Enthält den Code für das Projekt
* `tests`: Enthält Tests für das Projekt

## Ausführen
Die Hauptdatei ist `main.py` in `source/main.py`. 

# Tests und Codevalidation

* Pylint: `PYTHONPATH=. pylint main.py` im `source`-Ordner ausführen
* Mypy: `mypy --explicit-package-bases --check-untyped-defs .` im `source`-Ordner ausführen

* Unittests: `PYTHONPATH=.. python3 -m unittest` im `tests`-Ordner ausführen

* Coverage: `PYTHONPATH=.. coverage run -m unittest discover` im `tests`-Ordner ausführen
`coverage report` für das finale Ergebnis