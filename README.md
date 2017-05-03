
This is a python3 application.

To run it requires Bottle, which can be installed with:
pip install bottle

To develop, it requires unittest, which is part of default Python.


The following utility scripts are here:
python resultingtable.py <file> <table> [<count>]
    This script rolls repeatedly on the table give, and then
    creates another table based on those answers.  The new table
    is in HTML format, and has the number of lines given in
    count, or 20 as default. 

    For example:
    python resultingtable.py rocks.rpggen rock 5


Files starting with ht_ are "human test" files. They are designed to be run and then the results viewed by a person.  Like this:
python ht_roll.py     # tests basic dice rolling
python ht_chars.py    # tests random characters


Might need this on Windows:
set PYTHONIOENCODING=utf-8
