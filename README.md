
= Installing Rpggen =

This is a python3 application.

To run it requires Bottle, which can be installed with:<br>
```shell
pip install bottle
```

To develop, it requires unittest, which is part of default Python.

= Running Rpggen Programs =

The following utility scripts are here:
```
python resultingtable.py _file_ _table} [_count_]
```

This script rolls repeatedly on the table give, and then
creates another table based on those answers.  The new table
is in HTML format, and has the number of lines given in
count, or 20 as default. 

For example:
```python
python resultingtable.py rocks.rpggen rock 5
```

Files starting with ht_ are "human test" files. They are designed to be run and then the results viewed by a person.  Like this:<br>

```shell
# tests basic dice rolling
python ht_roll.py      
python ht_chars.py    # tests random characters
```

Might need this on Windows:
```
set PYTHONIOENCODING=utf-8
```

= Quick Overview of Rpggen's Object Oriented Architecture =

(This section is for programmers.)

The Rpggen class contains basic support for all RPGs: 
* Dice
* Table
* Template
* etc.

The Traveller class contains support for Traveller style RPGs.

The CepheusEngine file contains support for the Cepheus Engine specific rules for Traveller.
* The CepheusEngine class inherits from the Traveller class.
* The Character
* The Career

The CorporateRepo class is an example Career class.
* It inherits from Career...

The GetFromWeb class is a utility class to grab data from a URL on the web.  It is "stand alone" and does not inherit from any other class.