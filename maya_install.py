import os
import distutils
import pymel.core as pm
from PySide2 import QtWidgets

def onMayaDroppedPythonFile(*args):
    pass

script_dir = pm.internalVar(usd=True)
icon_dir = pm.internalVar(ubd=True)
dl_dir = os.path.dirname(__file__)

distutils.dir_util.copy_tree(os.path.join(dl_dir, 'scripts'), os.path.dirname(script_dir))
distutils.dir_util.copy_tree(os.path.join(dl_dir, 'icons'), os.path.dirname(icon_dir))

shelves = pm.tabLayout(pm.getMelGlobal('string', '$gShelfTopLevel'), query=True, childArray=True)
current = shelves.index(pm.tabLayout(pm.getMelGlobal('string', '$gShelfTopLevel'), query=True, selectTab=True))
itm, accepted = QtWidgets.QInputDialog().getItem(None, 'Shelf Button', 'Which Shelf Do You Wish to Add the Button To?',
                                                 shelves, editable=False, current=current)

if accepted:
    pm.shelfButton(style="iconOnly", parent=itm, image='na_scratch_paper', label='Scratch Paper',
                   command='import na_scratch_paper\nreload(na_scratch_paper)\nna_scratch_paper.run_maya()')