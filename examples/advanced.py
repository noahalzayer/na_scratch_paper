"""
This is an example of the advanced functionality in the system in a slightly esoteric overly colored way.
If running outside of Maya, you should comment out the 'Maya Only section towards the bottom-half of the script'
"""
import os
import time

from PySide2 import QtWidgets, QtGui

IMG_DIR = os.path.join(os.path.dirname(__file__), 'images')

# This is the first line that establishes the instructions
sp_instructions = {'contents': [],
                   'settings': {'color': [40, 40, 60], 'toolTip': 'This is a tip for the entire tab'}}


# This function is the simplest possible in an advanced tab. Only one key required to point to the buton function.
sp_instructions['contents'].append({'simple': 'super_simple'})
def super_simple():
    print 'This is the simplest function'


# This is an example of a simple button that has some instructions for label, color, icon, and tooltip. Still takes no inputs
sp_instructions['contents'].append({'simple': 'pretty_simple', 'label': 'Pretty Simple (simple function with instructions)',
                                    'toolTip': 'Prints a message', 'icon': os.path.join(IMG_DIR, 'chat.png'), 'color': [20, 80, 80]})
def pretty_simple():
    print 'This function is simple, but not as simple as super_simple'


# This is an example of a function with a lineEdit widget. Also shows some simple functionality for the frame look
# It also has a nerdy joke that will probably confuse a lot of people, but considering the audience, you might get it B)
sp_instructions['contents'].append({'label': 'Print 3 Times', 'color': [100, 20, 20],
                                    'inputWidgets': [{'type': 'lineEdit', 'label': 'Message:',
                                                      'toolTip': '3 shall be the number thou shalt print, '
                                                                 'and the number of the printing shall be 3.'}],
                                    'buttons': [{'label': 'Print 5 Times!', 'function': 'print_3_times', 'inputs': [0],
                                                 'toolTip': '3 Sir!', 'icon': os.path.join(IMG_DIR, 'arthur.png')}]})
def print_3_times(txt):
    for i in range(3):
        print txt


# These functions have the instructions after to show both that order doesn't matter, and that you can pass in function
# objects rather than the naems of the functions if you choose, so the instructions for these mix the paradigms.
def get_time():
    return str(time.time())


def time_menu():
    menu = QtWidgets.QMenu()
    actions = [menu.addAction('Now Minus 10 Seconds')]
    actions.append((menu.addAction('Now')))
    actions.append((menu.addAction('Now Plus 10 Seconds')))

    val = menu.exec_(QtGui.QCursor().pos())
    if val:
        return eval(get_time()) + (-10, 0, 10)[actions.index(val)]


def seconds_between(time1, time2=None):
    now = time2 is None
    if now:
        time2 = time.time()

    print '{} seconds passed between Time 1 and {}'.format(time2 - time1, 'now' if now else 'Time 2')


# These instructions set up cmdLineEdit widgets, show a couple ways of showing labels for lineEdits and widgets that
# subclass, and also show an example of setting background images. The buttons also show off sharing.
sp_instructions['contents'].append({'label': 'How Much Time Has Passed?', 'image': os.path.join(IMG_DIR, 'clock.png'),
                                    'inputWidgets': [{'type': 'cmdLineEdit', 'eval': True, 'errorIfEmpty': True,
                                                      'buttonCommand': 'time_menu', 'buttonLabel': 'Menu',
                                                      'placeholderText': 'Time 1', 'save': True},

                                                     {'type': 'cmdLineEdit', 'eval': True, 'share': False,
                                                      'errorIfEmpty': True, 'buttonCommand': get_time,
                                                      'buttonLabel': ' > ', 'label': 'Time 2: ', 'save': True},
                                                     {'type': 'spacer', 'size': 30}],

                                    'buttons': [{'label': 'Time1 > 2', 'function': 'seconds_between', 'inputs': [0, 1],
                                                 'share': True},
                                                {'label': 'Time1 > Now', 'function': seconds_between, 'inputs': [0]}]})


# This section shows the browse widget, which is a cmdLineEdit widget that has a file browser to fill the field
sp_instructions['contents'].append({'label': 'List Items in Directory',
                                    'inputWidgets': [{'type': 'browse', 'color': [40, 20, 10],
                                                      'errorIfEmpty': True, 'caption': 'Select Folder',
                                                      'fileMode': 'Directory'}],
                                    'buttons': [{'label': 'List', 'function': 'list_dir', 'inputs': [0]}]})
def list_dir(path):
    print 'The directory "{}" contains the following:'.format(path)
    for i in os.listdir(path):
        print i


# Ths next section shows off a lot of the non-input widgets: spacers, stretch, and separators
sp_instructions['contents'].append({'label': 'Do math stuff', 'color': [20, 20, 30],
                                    'inputWidgets': [{'type': 'spacer', 'share': True, 'size': 20},
                                                     {'type': 'intSpinner', 'label': 'Integer: ', 'save': True,
                                                      'value': 10, 'step': 2, 'max': 10000, 'share': True},
                                                     {'type': 'stretch', 'share': True},
                                                     {'type': 'floatSpinner', 'label': 'Float: ', 'save': True,
                                                      'value': 5, 'step': 0.1, 'max': 20, 'share': True},
                                                     {'type': 'spacer', 'size': 20},
                                                     {'type': 'separator'},
                                                     {'type': 'spacer', 'size': 20, 'share': True},
                                                     {'type': 'check', 'share': True, 'save': True, 'label': 'Round: '},
                                                     {'type': 'stretch'}],
                                    'buttons': [{'label': 'Plus', 'function': 'plus', 'inputs': [1, 3, 7], 'share': True},
                                                {'label': 'Multiply', 'function': 'mult', 'inputs': [1, 3, 7], 'share': True},
                                                {'label': 'Power Of', 'function': 'power', 'inputs': [1, 3, 7]}]})
def plus(val1, val2, round_result):
    print round(val1 + val2) if round_result else val1 + val2


def mult(val1, val2, round_result):
    print round(val1 * val2) if round_result else val1 * val2


def power(val1, val2, round_result):
    print round(val1 ** val2) if round_result else val1 ** val2


###########
'Maya Only'
###########
# This function shows the Maya-specific selection widgets. They will show a maya string-based function being run
sp_instructions['contents'].append({'label': 'Parent Selection (selection, selectionMulti Widgets)',
                                    'inputWidgets': [{'type': 'selectionMulti', 'errorIfEmpty': True, 'placeholderText': 'Children'},
                                                     {'type': 'selection', 'errorIfEmpty': True, 'placeholderText': 'Parent'}],
                                    'buttons': [{'label': 'Parent', 'function': 'parent_nodes_strings', 'inputs': range(2)}]})
def parent_nodes_strings(nodes, parent):
    import pymel.core as pm
    pm.parent(nodes, parent)


# This function shows off the pyNode widgets to run a similar function to the previous one, but using the object-
# oriented functionality that exists with PyMEL nodes (and hence why separate widgets were made for those)
sp_instructions['contents'].append({'label': 'Parent Selection (pyNode, pyNodeMulti Widgets)',
                                    'inputWidgets': [{'type': 'pyNodeMulti', 'errorIfEmpty': True, 'placeholderText': 'Children'},
                                                     {'type': 'pyNode', 'errorIfEmpty': True, 'placeholderText': 'Parent'}],
                                    'buttons': [{'label': 'Parent', 'function': 'parent_nodes_strings', 'inputs': range(2)}]})
def parent_nodes_pyNodes(nodes, parent):
    for node in nodes:
        node.setParent(parent)
