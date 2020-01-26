# -*- coding: utf-8 -*-
"""
Module containing the main window/callables for na_scratch_paper

This should (theoretically) work in any program with PySide2, though it was designed for Maya.
"""
# TODO - Add a window for writing up the markups in a more GUI centric way instead of script editor markup

import os
import json

from PySide2 import QtWidgets, QtCore
import shiboken2

import na_scratch_paper_child_widgets as child_widgets
import na_scratch_paper_tab_widgets as tab_widgets
reload(tab_widgets)


class ScratchPaperWidget(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(ScratchPaperWidget, self).__init__(*args, **kwargs)

        self.prefs = {}
        self.skip_save = False

        self.load_prefs()
        self.create_base()
        self.apply_prefs()


    def create_base(self):
        """
        Creates the Main UI elements.
        """
        self.setObjectName('na_scratch_paper')
        self.setWindowTitle('Scratch Paper')

        # Menu
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction('Edit Script List', self.edit_script_list)
        file_menu.addAction('Refresh Tabs', self.populate_tabs)
        file_menu.addSeparator()
        file_menu.addAction('Save Preferences', self.save_prefs)
        file_menu.addAction('Reset Preferences', self.reset_prefs)

        help_menu = menu_bar.addMenu('Help')
        help_menu.addAction('Script Markup Quick-Reference', lambda: child_widgets.AdvQuickRef(self).show())
        help_menu.addAction('Scratch Paper Documentation')

        self.refresh_btn = QtWidgets.QPushButton(u'⟳'.encode('utf-8'), self)
        self.refresh_btn.move(0, 10)
        self.refresh_btn.setToolTip('Refreshes the tabs (if the source scripts have been updated)')

        font = self.refresh_btn.font()
        font.setPixelSize(font.pixelSize()*1.5)
        self.refresh_btn.setFixedSize(font.pixelSize()*1.5, font.pixelSize()*1.5)

        self.refresh_btn.setFont(font)
        self.refresh_btn.clicked.connect(self.populate_tabs)

        # Body
        self.setCentralWidget(QtWidgets.QWidget())
        body_lwt = QtWidgets.QVBoxLayout()
        body_lwt.setContentsMargins(10, 20, 10, 10)
        self.centralWidget().setLayout(body_lwt)

        line = QtWidgets.QFrame()
        body_lwt.addWidget(line)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.search_le = QtWidgets.QLineEdit(self.centralWidget())
        self.search_le.textChanged.connect(self.filter)
        body_lwt.addWidget(self.search_le)
        self.search_le.setPlaceholderText('Search')
        self.search_le.setAlignment(QtCore.Qt.AlignCenter)

        self.tab_widget = QtWidgets.QTabWidget(self.centralWidget())
        body_lwt.addWidget(self.tab_widget)


    def populate_tabs(self, initial=False):
        """
        Populates tabs based on sourced script(s)
        """
        if not initial:
            for i in range(self.tab_widget.count()):
                self.tab_widget.widget(i).save_vals()

        ind = self.tab_widget.currentIndex()
        self.tab_widget.clear()

        if self.prefs.get('tab_data'):
            for data in self.prefs['tab_data']:
                tab_widgets.ScriptWidget(self.tab_widget, data=data)
        else:
            tab_widgets.ScriptWidget(self.tab_widget, data={})

        self.tab_widget.setCurrentIndex(ind)
        if self.search_le.text():
            self.filter(self.search_le.text())


    def edit_script_list(self):
        """
        Opens the EditScriptListDialog
        :return:
        """
        dialog = child_widgets.EditScriptListDialog(self, self.prefs.get('tab_data', {}))
        dialog.exec_()

        if dialog.result():
            self.prefs['tab_data'] = dialog.data
            self.populate_tabs()


    def filter(self, text):
        """
        Filters buttons and group boxes in the tabs according to what's in the search field separated by commas
        Args:
            text (str): Text from the line edit from which to extract search keys
        """
        keys = [key.strip().lower() for key in text.split(',')]
        for i in range(self.tab_widget.count()):
            self.tab_widget.widget(i).filter(keys)


    def apply_prefs(self):
        """
        Applies preferences to the window
        """
        geometry = self.prefs.get('geometry', [100, 100, 800, 1000])
        self.setGeometry(QtCore.QRect(geometry[0], geometry[1], geometry[2], geometry[3]))

        self.populate_tabs(initial=True)
        self.tab_widget.setCurrentIndex(self.prefs.get('tab_index', 0))


    def save_prefs(self, skip_gather=False):
        """
        Saves window preferences out to a user preferences directory.
        Args:
            skip_gather (bool): If True, skips gathering of information (useful for resetting prefs)
        """
        if not skip_gather:
            geometry = self.geometry()
            self.prefs['geometry'] = geometry.x(), geometry.y(), geometry.width(), geometry.height()
            self.prefs['tab_index'] = self.tab_widget.currentIndex()
            for i in range(len(self.prefs.get('tab_data', []))):
                self.tab_widget.widget(i).save_vals()
                self.prefs['tab_data'][i]['excluded'] = self.tab_widget.widget(i).data['excluded']

        txt = json.dumps(self.prefs, sort_keys=True, indent=4, separators=(',', ': '))
        if not os.path.exists(os.path.expanduser('~/na_tool_prefs')):
           os.mkdir(os.path.expanduser('~/na_tool_prefs'))

        f = open(os.path.join(os.path.expanduser('~/na_tool_prefs'), 'scratch_paper_prefs.json'), 'w')
        f.write(txt)
        f.close()


    def load_prefs(self):
        """
        Reads the prefereces file and updates the prefs variable
        """
        path = os.path.join(os.path.join(os.path.expanduser('~/na_tool_prefs'), 'scratch_paper_prefs.json'))
        if os.path.exists(path):
            f = file(path)
            txt = f.read()
            f.close()
            self.prefs = json.loads(txt)


    def reset_prefs(self):
        """
        Clears preferences and restarts the window
        """
        dialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, 'Resetting Preferences',
                                       'You are about to reset preferences. This operation is not undoable.\n'
                                       'Do you wish to continue?',
                                       buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        dialog.exec_()
        if not dialog.buttonRole(dialog.clickedButton()) is QtWidgets.QMessageBox.YesRole:
            return

        self.prefs = {}
        self.save_prefs(skip_gather=True)
        self.skip_save = True
        run()


    def resizeEvent(self, event):
        """
        Overridden resizeEvent to make the refresh button stick to the right side of the window
        """
        geo = self.refresh_btn.geometry()
        geo.setX(event.size().width() - self.refresh_btn.width() -
                 self.centralWidget().layout().contentsMargins().right())
        self.refresh_btn.setGeometry(geo)


    def closeEvent(self, *args, **kwargs):
        """
        Overridden closeEvent to save preferences
        """
        if not self.skip_save:
            self.save_prefs()


def run():
    import maya.OpenMayaUI
    import pymel.core as pm

    if pm.window('na_scratch_paper', q=True, exists=True):
        pm.deleteUI('na_scratch_paper')

    ScratchPaperWidget(shiboken2.wrapInstance(long(maya.OpenMayaUI.MQtUtil.mainWindow()), QtWidgets.QWidget)).show()
