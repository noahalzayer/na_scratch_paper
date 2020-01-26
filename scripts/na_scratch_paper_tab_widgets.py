"""
Module containing convenience classes for widgets involved in adding script tabs
"""
import os
import sys
import imp
import time
import inspect
import traceback
from functools import partial

from PySide2 import QtWidgets, QtGui, QtCore


class ScriptWidget(QtWidgets.QWidget):
    """
    Custom Widget for each source script that's loaded in to the tool
    """
    def __init__(self, parent, data):
        """
        Initial call method
        Args:
            parent (QtWidgets.QTabWidget): The parent tab widget
            data (dict): Data being passed in to the widget {(str) name: Tab Label, (str) path: Path to the script,
                                                             (list) excluded: Buttons to Exclude from the UI}
        """
        super(ScriptWidget, self).__init__(parent)

        self.main_lwt = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_lwt)

        # Set up a scroll area (way more complicated than it should be)
        self.scroll = QtWidgets.QScrollArea(self)
        self.scroll.setWidget(QtWidgets.QWidget())
        self.scroll.setWidgetResizable(True)
        self.main_lwt.addWidget(self.scroll)
        self.body_lwt = QtWidgets.QVBoxLayout()
        self.scroll.setWidget(QtWidgets.QWidget())
        self.scroll.widget().setLayout(self.body_lwt)

        self.filter_keys = []
        self.simple = True
        self.data = data

        self.process_script()
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.tab_menu)
        parent.addTab(self, self.data.get('name', 'Default'))

    def process_script(self):
        """
        Attempts to import the script and lay out the tab accordingly
        """
        for child in self.scroll.widget().children()[1:]:
            child.setParent(None)
        # Next bit is strange, I know, but it's the only I know of to get rid of the damn spacer if refreshing without
        # crashing. If there's a clean way to just clear everything that I just don't know, feel free to let me know :)
        for i in range(self.body_lwt.count()):
            self.body_lwt.itemAt(i).changeSize(0, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        if 'script' not in self.data:
            lbl = QtWidgets.QLabel('No scripts in list.\nTo add source scripts, go to File>Edit Script List')
            lbl.setAlignment(QtCore.Qt.AlignCenter)
            self.body_lwt.addWidget(lbl)
            return

        functions = []
        # Everything needs to have a unique name or else things appear to stack. Not a huge imp guru, so might be wrong
        name = '{}_{}'.format(os.path.basename(self.data['script']), time.ctime())
        for char in filter(lambda x: not x.isalnum(), name):
            name = name.replace(char, '_')

        try:
            module = imp.load_source(name, self.data['script'])
            source = inspect.getmembers(module)
            for name, member in source:
                if callable(member):
                    functions.append([name, member])

            instructions = filter(lambda x: x[0] == 'sp_instructions', source)
            if instructions:
                self.build_body_advanced(functions, instructions[0][1])
            else:
                self.build_body_simple(functions)
        except:
            self.build_stack_trace()

        self.filter(self.filter_keys)

    def build_body_simple(self, functions):
        """
        In the case of a file that isn't marked up for advanced layout, this will simply create buttons for each
        function in the script unless the docstring starts with "scratch_exclude"
        Args:
            functions (list): List of functions found in the script file
        """
        for name, function in functions:
            if function.__doc__:
                if function.__doc__.lstrip().startswith('scratch_exclude'):
                    continue

            if name in self.data.get('excluded', []):
                continue

            self.func_button({'label': function.__name__}, function)
        self.body_lwt.addStretch()

    def build_body_advanced(self, functions, instructions):
        """
        Builds a more custom tab according to instructions in the file
        Args:
            functions (list): List of functions found in the script file
            instructions (dict): Instructions for the build such as settings, and widgets
        """
        self.simple = False
        functions = dict(functions)
        settings = instructions.get('settings', {})
        saved = self.data.get('saved', {})

        self.set_palette(self.scroll.widget(), QtGui.QPalette.Background, rgb=settings.get('color'),
                         image=settings.get('image'))

        for group in instructions['contents']:
            if 'simple' in group:
                if 'label' not in group:
                    group['label'] = group['simple']
                self.func_button(group, functions[group['simple']])
                continue

            frame = QtWidgets.QFrame(self)
            frame.data = group
            lwt = QtWidgets.QVBoxLayout()

            frame.setLayout(lwt)
            frame.setFrameShape(QtWidgets.QFrame.WinPanel)
            frame.setFrameShadow(QtWidgets.QFrame.Raised)

            lwt.addWidget(QtWidgets.QLabel(group.get('label', 'Default')))
            frame.children()[-1].setAlignment(QtCore.Qt.AlignHCenter)

            self.set_palette(frame, QtGui.QPalette.Background, rgb=group.get('color'), image=group.get('image'))

            widgets = self.create_input_widgets(frame, group.get('inputWidgets', []), saved)
            previous_layout = None
            for btn in group.get('buttons', []):
                btn_lwt = previous_layout if previous_layout else QtWidgets.QHBoxLayout()
                previous_layout = btn_lwt if btn.get('share') else None

                lwt.addLayout(btn_lwt)
                self.func_button(data=btn, function=functions[btn['function']], layout=btn_lwt, input_widgets=widgets)

            self.body_lwt.addWidget(frame)
            self.body_lwt.addSpacing(10)

        self.body_lwt.addStretch()

    def create_input_widgets(self, parent, inputs, saved):
        """
        Convenience function for creating the widgets from the "inputWidgets" data
        Args:
            parent (QtWidgets.QWidget): Parent Widget
            inputs (list): List of dictionaries containing applicable data for the widgets
        Returns:
            widgets (tuple): Tuple of newly created input widgets
        """
        previous_layout = None
        widgets = []

        # Next two lines are just a helper for docs. Should normally be commented
        # keys = sorted(CLASSES.keys(), key=lambda x: order.index(x))
        # inputs = [{'type': i, 'size': 10, 'label': '{}:'.format(i)} for i in keys]

        for i in inputs:
            if i.get('type') not in CLASSES:
                txt = 'The "{}" type does not have a class. Accepted classes are as follows:'.format(i.get('type'))
                for j in CLASSES:
                    txt += '{}\n'.format(j)
                raise RuntimeError(txt)

            widget = CLASSES[i['type']](parent, i, previous_layout if previous_layout else parent.layout())
            previous_layout = widget.lwt if i.get('share') else None
            widgets.append(widget)

            # print '"{}":'.format(i['type']), widget.allowed_data, widget.__class__.__name__  # Another doc helper

            # Set any saved values
            val = saved.get(parent.findChildren(QtWidgets.QLabel)[0].text(), {}).get(i.get('label'))
            if val is not None:
                widget.set_val(val)

        return tuple(widgets)

    def func_button(self, data, function, layout=None, input_widgets=()):
        """
        Creates a command button.
        Args:
            data (dict): Dictionary of data from the markup
            function (callable): Function to call when the button is pressed
            layout (QtWidgets.QLayout): Optional parent layout for the button. Defaults to self.body_lwt
            input_widgets (tuple): list of input widgets from na_scratch_paper_tab_widgets to read on execution
        """
        inputs = [input_widgets[i] for i in data.get('inputs', [])]
        if not layout:
            layout = self.body_lwt

        btn = QtWidgets.QPushButton(data['label'])
        btn.setToolTip(data.get('toolTip'))
        if 'icon' in data:
            btn.setIcon(QtGui.QIcon(data['icon']))
        if 'color' in data:
            self.set_palette(btn, QtGui.QPalette.Button, rgb=data['color'])

        btn.clicked.connect(partial(self.func_button_clicked, function, inputs))
        btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        btn.customContextMenuRequested.connect(partial(self.button_menu, data['label'], function))
        layout.addWidget(btn)

    def func_button_clicked(self, function, inputs):
        """
        Reads input widgets if supplied to pass in to the function. Otherwise simply runs the function.
        Args:
            function (callable): Function to connect to the click event
            inputs (tuple): list of input widgets from na_scratch_paper_tab_widgets to read on execution
        """
        try:
            if inputs:
                args = [widget.read() for widget in inputs]
                function(*args)
            else:
                function()
        except:
            sys.stderr.write(self.stack_trace())

    def stack_trace(self):
        """
        Looks up and returns a formatted stack trace
        Returns:
            txt (str): The formatted stack trace
        """
        typ, err, tb = sys.exc_info()
        txt = '# {}\n# Traceback (most recent call last):\n'.format(err)
        for fl, num, func, line in traceback.extract_tb(tb):
            txt += '#    File "{}", line {}, in {}\n#      {}\n'.format(fl, num, func, line)
        txt += '# {}\n'.format(err)
        return txt

    def build_stack_trace(self):
        """
        Creates labels and prints out a stack trace in the case of an exception during parsing.
        """
        lbl = QtWidgets.QLabel('Failed to Parse {}\n\nThe following error rose '
                               '(also in the Script Editor):\n'.format(self.data.get('script')))
        lbl.setAlignment(QtCore.Qt.AlignHCenter)
        self.body_lwt.addWidget(lbl)
        txt = self.stack_trace()

        sys.stderr.write(txt)
        self.body_lwt.addWidget(QtWidgets.QLabel(txt))
        self.body_lwt.addStretch()

    def set_palette(self, widget, role, rgb=(), image=''):
        """
        Convenience function for setting a color or image in one line (since it's an overly long process with Qt)
        Args:
            widget (QtWidgets.QWidget): The widget you wish to edit
            role (QtGui.QPalette.ColorRole): Color role to set
            rgb (list): Values to pass in to QColor
            image (str): In the case of an image, the path to an image
        """
        if not rgb and not image:
            return

        widget.setAutoFillBackground(True)
        pal = widget.palette()

        if image:
            brush = pal.brush(role)
            brush.setTextureImage(QtGui.QImage(image))
            pal.setBrush(role, brush)
        else:
            pal.setColor(role, QtGui.QColor(*rgb))

        widget.setPalette(pal)

    def filter(self, keys):
        """
        Filters out buttons or groups depending on filter keys
        Args:
            keys (list): Filter keys. If any key begins with "not," it will filter if it isn't found
        """
        if self.simple:
            children = self.findChildren(QtWidgets.QPushButton)
        else:
            children = filter(lambda x: type(x) is QtWidgets.QFrame or type(x) is QtWidgets.QPushButton,
                              self.scroll.widget().children())

        widgets = zip([wid.text() if type(wid) is QtWidgets.QPushButton else wid.children()[1].text()
                       for wid in children], children)

        passed = list(widgets)
        for key in keys:
            if key.startswith('not '):
                passed = filter(lambda x: key.lstrip('not ').strip() not in x[0].lower(), passed)
            else:
                passed = filter(lambda x: key in x[0].lower(), passed)

        for widget in widgets:
            widget[1].setVisible(widget in passed)

        self.filter_keys = keys

    def add_exclude(self, name):
        """
        Adds a new button to the exclude list for the tab then refreshes to reflect the changes.
        Args:
            name (str): The name of the function you wish to exclude.
        """
        if 'excluded' not in self.data:
            self.data['excluded'] = []
        self.data['excluded'].append(name)
        self.process_script()

    def remove_exclude(self, name=None):
        """
        Removes the named function from the exclude list then refreshes. If no name is given, it removes all.
        Args:
            name (str): The name of the function you wish to remove from the exclude list. If None, removes all.
        """
        if name:
            self.data['excluded'].remove(name)
        else:
            self.data['excluded'] = []
        self.process_script()

    def tab_menu(self, *args):
        """
        Menu for the overall tab widget.
        """
        if 'script' not in self.data:
            return

        menu = QtWidgets.QMenu()
        menu.addAction('Refresh Tab', self.process_script)
        menu.addAction('Copy Script Path to Clipboard', lambda: QtGui.QClipboard().setText(self.data.get('script')))
        menu.addAction('Open Script in Default Editor', lambda: os.system('start {}'.format(self.data.get('script'))))
        if self.data.get('excluded'):
            menu.addSeparator()
            hidden_menu = menu.addMenu('Include Excluded Button(s)')
            for button in self.data.get('excluded', []):
                hidden_menu.addAction(button, partial(self.remove_exclude, button))
            menu.addAction('Include All Excluded Buttons', self.remove_exclude)

        menu.exec_(QtGui.QCursor.pos())

    def button_menu(self, name, func, *args):
        """
        Menu for the buttons in the tab
        Args:
            name (str): The name of the function (for excluding)
            func (callable): The function instance (for looking up the docstring)
        """
        menu = QtWidgets.QMenu()
        menu.addAction('Copy Script Path to Clipboard', lambda: QtGui.QClipboard().setText(self.data.get('script')))
        menu.addAction('Open Script in Default Editor', lambda: os.system('start {}'.format(self.data.get('script'))))
        menu.addSeparator()
        menu.addAction('Exclude Button', lambda: self.add_exclude(name))
        menu.addAction('Print Source Function Docstring', lambda: sys.stdout.write('{}\n'.format(func.__doc__)))

        menu.exec_(QtGui.QCursor.pos())

    def save_vals(self):
        """
        Saves desired values to preferences
        """
        if not self.simple:
            children = filter(lambda x: type(x) is QtWidgets.QFrame, self.findChildren(QtWidgets.QFrame))
            self.data['saved'] = {}
            for child in children:
                input_widgets = child.findChildren(InputBase)
                for widget in input_widgets:
                    if widget.data.get('save'):
                        frame_label = child.data.get('label', '')
                        if frame_label not in self.data['saved']:
                            self.data['saved'][frame_label] = {}

                        child.data['eval'] = False
                        widget.simple_output = True
                        self.data['saved'][frame_label][widget.data.get('label' '')] = widget.read()


class InputBase(QtWidgets.QWidget):
    """
    Baseline widget for setting up standard things like a main layout and reading methods
    """
    def __init__(self, parent, data, layout=None):
        """
        Initial Call Method
        Args:
            parent (QtWidgets.QWidget): Parent Widget
            data (dict): Dictonary containing applicable data for the widget
            layout (QtWidgets.QLayout): Parent layout
        """
        super(InputBase, self).__init__(parent)
        if layout:
            layout.addWidget(self)

        self.lwt = QtWidgets.QHBoxLayout()
        self.setLayout(self.lwt)

        self.setToolTip(data.get('toolTip'))
        if 'label' in data:
            self.lwt.addWidget(QtWidgets.QLabel(data['label']))

        self.allowed_data = ['type', 'label', 'toolTip', 'color', 'share', 'save']
        self.simple_output = False
        self.data = data

    def set_color(self):
        """
        Convenience function for setting a color role in one line (since it's an overly long process with Qt)
        """
        if 'color' not in self.data:
            return

        if not hasattr(self, 'widget_color_info'):
            raise NotImplementedError('The "{}" widget is not eligible for the "color" '
                                      'argument.'.format(self.__class__.__name__))

        for widget, role in self.widget_color_info:
            widget.setAutoFillBackground(True)
            pal = widget.palette()
            pal.setColor(role, QtGui.QColor(*self.data['color']))
            widget.setPalette(pal)

    def data_key_check(self):
        """
        Function for checking keys in the data argument to make sure incorrect keys weren't passed in as a safety check.
        """
        extra_keys = filter(lambda x: x not in self.allowed_data, self.data.keys())
        [self.data.pop(key) for key in extra_keys]
        if extra_keys:
            sys.stderr.write('The following data argument(s) are ineligible for the {} class:\n{}\nEligible keys:\n{}\n'
                             '\n\n'.format(self.__class__.__name__, extra_keys, self.allowed_data))

    def set_val(self, val):
        """
        Generic method for setting values
        Args:
            val (NoneType): The value you wish to pass in (meant to be changed with subclassed methods)
        """
        raise NotImplementedError('The "{}" widget does not have set functionality'.format(self.__class__.__name__))

    def read(self):
        """
        Generic method for reading values
        """
        raise NotImplementedError('The "{}" widget does not have read functionality'.format(self.__class__.__name__))

    def showEvent(self, *args, **kwargs):
        """
        Overridden show event to set colors, check arguments, and load saved values
        """
        super(InputBase, self).showEvent(*args, **kwargs)
        self.data_key_check()
        self.set_color()


class Spacer(InputBase):
    """
    Fixed size QSpacerItem convenience function
    """
    def __init__(self, parent, data, layout):
        """
        Initial Call Method
        Args:
            parent (QtWidgets.QWidget): Parent Widget
            data (dict): Dictonary containing applicable data for the widget
            layout (QtWidgets.QLayout): Parent layout
        """
        super(Spacer, self).__init__(parent, data, layout)
        self.allowed_data.append('size')
        [self.allowed_data.remove(key) for key in ['label', 'color', 'save']]

        if 'size' not in data:
            raise RuntimeError('Size data not provided for Spacer Widget')

        self.lwt.addSpacing(data['size'])


class Stretch(InputBase):
    """
    Stretchy QSpacerItem convenience function
    """
    def __init__(self, parent, data, layout):
        """
        Initial Call Method
        Args:
            parent (QtWidgets.QWidget): Parent Widget
            data (dict): Dictonary containing applicable data for the widget
            layout (QtWidgets.QLayout): Parent layout
        """
        super(Stretch, self).__init__(parent, data, layout)
        [self.allowed_data.remove(key) for key in ['label', 'color', 'save']]
        self.lwt.addStretch()


class Separator(InputBase):
    """
    An empty frame to serve as a separator
    """
    def __init__(self, parent, data, layout):
        """
        Initial Call Method
        Args:
            parent (QtWidgets.QWidget): Parent Widget
            data (dict): Dictonary containing applicable data for the widget
            layout (QtWidgets.QLayout): Parent layout
        """
        super(Separator, self).__init__(parent, data, layout)
        [self.allowed_data.remove(key) for key in ['label', 'color', 'save']]
        self.allowed_data.append('vertical')

        sep = QtWidgets.QFrame(parent)
        sep.setFrameShadow(QtWidgets.QFrame.Sunken)
        sep.setFrameShape(QtWidgets.QFrame.HLine if not data.get('vertical') else QtWidgets.QFrame.VLine)

        sep.setLineWidth(3)
        self.lwt.addWidget(sep)


class LineEdit(InputBase):
    """
    Simply a QLineEdit with built-in label
    """
    def __init__(self, parent, data, layout):
        """
        Initial Call Method
        Args:
            parent (QtWidgets.QWidget): Parent Widget
            data (dict): Dictonary containing applicable data for the widget
            layout (QtWidgets.QLayout): Parent layout
        """
        super(LineEdit, self).__init__(parent, data, layout)
        self.allowed_data.extend(['text', 'placeholderText', 'eval', 'errorIfEmpty'])

        self.le = QtWidgets.QLineEdit()
        self.le.setPlaceholderText(data.get('placeholderText', ''))
        self.lwt.addWidget(self.le)

        self.data = data
        self.set_val(data.get('text', ''))
        self.widget_color_info = [(self.le, QtGui.QPalette.Base)]

    def validate_text(self, txt):
        """
        Validates text data and returns the text if valid, returns an empty string otherwise
        Args:
            txt (str): The text you wish to validate
        Returns:
            txt (str): The validated text
        """
        return txt

    def safe_eval(self, text):
        """
        Checks whether the user has enabled eval (to run eval on the lineEdit and return the result)
        Gives more information than is normal in the case of an error
        Args:
            text (str): The text from the field
        Returns:
            evaluated (object): The return value of the successful eval run
        """
        if not self.data.get('eval'):
            return text

        else:
            try:
                return eval(text)
            except:
                info = sys.exc_info()
                err_txt = 'Error Occured when reading the "{}" Text Field\n'.format(self.data.get('label', ''))
                err_txt += 'Error: {}. {}, line: {}'.format(info[0], info[1], info[2].tb_lineno)
                raise RuntimeError(err_txt)

    def set_val(self, val):
        """
        Generic method for setting values
        Args:
            val (str): The value you wish to pass in
        """
        self.le.setText(self.validate_text(val))

    def read(self):
        """
        Reads self.le and returns the value
        Returns:
            text (str): The text in the lineEdit
        """
        if self.data.get('errorIfEmpty'):
            if not self.le.text():
                raise ValueError('Text Field is Empty')

        return self.safe_eval(str(self.le.text()))


class CmdLineEdit(LineEdit):
    """
    LineEdit with a button to run a command and write out the return value to the lineEdit
    """
    def __init__(self, parent, data, layout):
        """
        Initial Call Method
        Args:
            parent (QtWidgets.QWidget): Parent Widget
            data (dict): Dictonary containing applicable data for the widget
            layout (QtWidgets.QLayout): Parent layout
        """
        super(CmdLineEdit, self).__init__(parent, data, layout)
        self.allowed_data.extend(['buttonCommand', 'buttonLabel', 'buttonToolTip'])

        self.button = QtWidgets.QPushButton(data.get('buttonLabel', ' > '))
        self.button.setToolTip(data.get('buttonToolTip', ''))
        self.button_command = data.get('buttonCommand', self.button_command)

        width = QtGui.QFontMetrics(self.button.font()).width(self.button.text()) * 1.5
        self.button.setFixedWidth(width)

        self.button.clicked.connect(self.button_command_validate)

        self.lwt.insertWidget(1, self.button)
        self.widget_color_info.append((self.button, QtGui.QPalette.Button))

    def button_command_validate(self):
        """
        Command to run "button_command" and set the lineEdit text if a value was returned
        """
        self.set_val(self.button_command())

    def button_command(self):
        """
        Command (meant to be overridden in subclasses) to run when the command button is pressed.
        Returns:
            val (str): The return value from the command to write to the lineEdit
        """
        raise NotImplementedError('buttonCommand data key must be set to a callable function.')


class Browse(CmdLineEdit):
    """
    CmdLineEdit with the command set to get a bring up a browser window and assign the result
    """
    def __init__(self, parent, data, layout):
        """
        Initial Call Method
        Args:
            parent (QtWidgets.QWidget): Parent Widget
            data (dict): Dictonary containing applicable data for the widget
            layout (QtWidgets.QLayout): Parent layout
        """
        data['buttonLabel'] = ' Browse: '
        super(Browse, self).__init__(parent, data, layout)
        self.allowed_data.extend(['caption', 'filter', 'fileMode', 'directory'])
        [self.allowed_data.remove(i) for i in ['eval', 'buttonCommand']]

    def button_command(self):
        """
        Brings up a browser window and returns the value if a selection has been made
        Returns:
            val (str): the file or files from the dialog
        """
        file_dialog = QtWidgets.QFileDialog(caption=self.data.get('caption'), filter=self.data.get('filter'))
        file_modes = {'AnyFile': QtWidgets.QFileDialog.AnyFile,
                      'ExistingFile': QtWidgets.QFileDialog.ExistingFile,
                      'DirectoryOnly': QtWidgets.QFileDialog.DirectoryOnly,
                      'ExistingFiles': QtWidgets.QFileDialog.ExistingFiles,
                      'Directory': QtWidgets.QFileDialog.Directory}

        file_dialog.setFileMode(file_modes[self.data.get('fileMode', 'AnyFile')])
        file_dialog.setDirectory(self.data.get('directory'))

        file_dialog.exec_()
        if not file_dialog.result():
            return

        if file_dialog.fileMode() == QtWidgets.QFileDialog.ExistingFiles:
            return map(str, file_dialog.selectedFiles())
        else:
            return str(file_dialog.selectedFiles()[0])


class Selection(CmdLineEdit):
    """
    CmdLineEdit with the command set to get a single Maya selection and fill in the lineEdit
    """
    def __init__(self, parent, data, layout):
        """
        Initial Call Method
        Args:
            parent (QtWidgets.QWidget): Parent Widget
            data (dict): Dictonary containing applicable data for the widget
            layout (QtWidgets.QLayout): Parent layout
        """
        super(Selection, self).__init__(parent, data, layout)
        self.button.setFixedSize(self.button.width(), self.button.width())
        self.button.setToolTip('Get Selection')
        self.allowed_data.append('checkExisting')
        [self.allowed_data.remove(i) for i in ['eval', 'buttonCommand']]

    def button_command(self):
        """
        Gets the first selection and applies it to the lineEdit
        """
        import pymel.core as pm
        if not pm.selected():
            pm.warning('Nothing Selected')
            return
        return pm.selected()[0].name()

    def exists(self, txt):
        """
        Checks to see if there's a node with the given name in your scene.
        Args:
            txt (str): The name of the node you wish to search for
        Returns:
            exists (bool): Whether or not the node exists in your scene
        """
        if not self.data.get('checkExisting', True):
            return True

        import pymel.core as pm
        return pm.objExists(txt)

    def validate_text(self, txt):
        """
        Validates text data and returns the text if valid, returns an empty string otherwise
        Args:
            txt (str): The text you wish to validate
        Returns:
            txt (str): The validated text
        """
        import pymel.core as pm
        if txt:
            if not self.exists(txt):
                pm.warning('Unable to fill the "{}" field in the "{}" frame.\n"{}" doesn\'t exist in '
                           'your scene'.format(self.data.get('label'), self.parent().children()[1].text(), txt))
                return ''
        return txt


class SelectionMulti(Selection):
    """
    Selection widget that works with multiple selected nodes and fill in the lineEdit
    """
    def __init__(self, parent, data, layout):
        """
        Initial Call Method
        Args:
            parent (QtWidgets.QWidget): Parent Widget
            data (dict): Dictonary containing applicable data for the widget
            layout (QtWidgets.QLayout): Parent layout
        """
        super(SelectionMulti, self).__init__(parent, data, layout)

    def button_command(self):
        """
        Gets all selected items and applies it to the lineEdit
        """
        import pymel.core as pm
        if not pm.selected():
            pm.warning('Nothing Selected')
            return

        txt = ''
        for sel in pm.selected():
            txt += '{}, '.format(sel.name())
        return txt.rstrip(', ')

    def exists(self, txt):
        """
        Checks to see if there are nodes for all the names in the list
        Args:
            txt (str): The names of the nodes you wish to search for
        Returns:
            exists (bool): Whether or not the nodes exist in your scene
        """
        if not self.data.get('checkExisting', True):
            return True

        import pymel.core as pm
        for node in txt.split(','):
            if not pm.objExists(node.strip()):
                return False
        return True

    def read(self):
        """
        Reads self.le and returns the value
        Returns:
            text (list): A parsed list of strings of what's in the field (the function adds quotation marks)
        """
        if self.data.get('errorIfEmpty'):
            if not self.le.text():
                raise RuntimeError('Field is Empty')

        txt = ''
        for i in self.le.text().split(','):
            name = i.strip()
            if not (name.startswith('"') and name.endswith('"')) or (name.startswith('\'') and name.endswith('\'')):
                name = '\'{}\''.format(name)

            txt += '{}, '.format(name)

        return self.safe_eval(txt)


class PyNode(Selection):
    def __init__(self, parent, data, layout):
        """
        Initial Call Method
        Args:
            parent (QtWidgets.QWidget): Parent Widget
            data (dict): Dictonary containing applicable data for the widget
            layout (QtWidgets.QLayout): Parent layout
        """
        super(PyNode, self).__init__(parent, data, layout)
        self.le.setReadOnly(True)
        self.node = None

    def button_command(self):
        """
        Gets all selected items and applies it to the lineEdit
        """
        node = super(PyNode, self).button_command()
        import pymel.core as pm
        if node:
            self.node = pm.selected()[0]
            return self.node.nodeName()

    def read(self):
        """
        Reads self.node and returns the value
        Returns:
            node (PyNode): PyMEL instance of the node
        """
        if self.data.get('errorIfEmpty'):
            if not self.le.text():
                raise RuntimeError('Field is Empty')

        if self.simple_output:
            return str(self.le.text())
        else:
            return self.node


class PyNodeMulti(SelectionMulti):
    def __init__(self, parent, data, layout):
        """
        Initial Call Method
        Args:
            parent (QtWidgets.QWidget): Parent Widget
            data (dict): Dictonary containing applicable data for the widget
            layout (QtWidgets.QLayout): Parent layout
        """
        super(PyNodeMulti, self).__init__(parent, data, layout)
        self.nodes = None

    def button_command(self):
        """
        Gets all selected items and applies it to the lineEdit
        """
        nodes = super(PyNodeMulti, self).button_command()
        import pymel.core as pm
        if nodes:
            self.nodes = pm.selected()
            return nodes

    def read(self):
        """
        Reads self.nodes and returns the value
        Returns:
            nodes (list): List of PyMEL instances of the nodes
        """
        if self.data.get('errorIfEmpty'):
            if not self.le.text():
                raise RuntimeError('Field is Empty')

        if self.simple_output:
            return str(self.le.text())
        else:
            return self.nodes


class IntSpinner(InputBase):
    def __init__(self, parent, data, layout):
        """
        Initial Call Method
        Args:
            parent (QtWidgets.QWidget): Parent Widget
            data (dict): Dictonary containing applicable data for the widget
            layout (QtWidgets.QLayout): Parent layout
        """
        super(IntSpinner, self).__init__(parent, data, layout)
        self.allowed_data.extend(['max', 'min', 'value', 'step'])

        self.spin = self.create_spinner()
        self.spin.setValue(data.get('value', 0))
        self.spin.setMinimum(data.get('min', 0))
        self.spin.setMaximum(data.get('max', 99))
        self.spin.setSingleStep(data.get('step', 1))

        self.lwt.addWidget(self.spin)
        self.widget_color_info = [(self.spin, QtGui.QPalette.Base), (self.spin, QtGui.QPalette.Button)]

    def create_spinner(self):
        """
        Creates and returns a spinBox
        Returns:
            spin (QtWidgets.QSpinBox): The newly created QSpinBox
        """
        return QtWidgets.QSpinBox()

    def set_val(self, val):
        """
        Generic method for setting values
        Args:
            val (int or float): The value you wish to pass in
        """
        self.spin.setValue(val)

    def read(self):
        """
        Reads self.spin and returns the value
         Returns:
            value (int): The spinner value
        """
        return self.spin.value()


class FloatSpinner(IntSpinner):
    def __init__(self, parent, data, layout):
        """
        Initial Call Method
        Args:
            parent (QtWidgets.QWidget): Parent Widget
            data (dict): Dictonary containing applicable data for the widget
            layout (QtWidgets.QLayout): Parent layout
        """
        super(FloatSpinner, self).__init__(parent, data, layout)

    def create_spinner(self):
        """
        Creates and returns a QDoubleSpinBox
        Returns:
            spin (QtWidgets.QDoubleSpinBox):The newly created QDoubleSpinBox
        """
        return QtWidgets.QDoubleSpinBox()


class CheckBox(InputBase):
    def __init__(self, parent, data, layout):
        """
        Initial Call Method
        Args:
            parent (QtWidgets.QWidget): Parent Widget
            data (dict): Dictonary containing applicable data for the widget
            layout (QtWidgets.QLayout): Parent layout
        """
        super(CheckBox, self).__init__(parent, data, layout)
        self.allowed_data.append('value')

        self.check = QtWidgets.QCheckBox()
        self.check.setChecked(data.get('value', False))

        if data.get('label'):
            lbl = self.findChildren(QtWidgets.QLabel)[0]
            lbl.mousePressEvent = self.label_click

        self.lwt.addWidget(self.check)
        self.widget_color_info = [(self.check, QtGui.QPalette.Base)]

    def label_click(self, *args):
        """
        Toggles the checkbox to have the same behavior as checkbox labels
        """
        self.check.setChecked(not self.check.isChecked())

    def set_val(self, val):
        """
        Generic method for setting values
        Args:
            val (bool): The value you wish to pass in
        """
        self.check.setChecked(val)

    def read(self):
        """
                Reads self.check and returns the value
                Returns:
                    value (bool): The check box value
                """
        return self.check.isChecked()


CLASSES = {
    'stretch': Stretch,
    'spacer': Spacer,
    'separator': Separator,
    'lineEdit': LineEdit,
    'cmdLineEdit': CmdLineEdit,
    'browse': Browse,
    'selection': Selection,
    'selectionMulti': SelectionMulti,
    'pyNode': PyNode,
    'pyNodeMulti': PyNodeMulti,
    'intSpinner': IntSpinner,
    'floatSpinner': FloatSpinner,
    'check': CheckBox
}

# Docmumentation helper. Ignore this unless you're a handsome technical artist named Noah
order = [
    'stretch',
    'spacer',
    'separator',
    'lineEdit',
    'cmdLineEdit',
    'browse',
    'selection',
    'selectionMulti',
    'pyNode',
    'pyNodeMulti',
    'intSpinner',
    'floatSpinner',
    'check'
]
