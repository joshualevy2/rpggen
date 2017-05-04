
from bottle import route, run, template
import sys

sys.path.append('..')
from rpggen import Rpggen, Table

@route('/info')
def info():
    return 'This server returns one malfunction in plain text format'

@route('/malfunction')
def malfunction():
    return Rpggen.finduse('MalfunctionDisplay')

Rpggen.load('malfunctions.rpggen')

run(host='localhost', port=1188)