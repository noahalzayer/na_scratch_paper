"""
This is an example of the easiest Scratch Paper implementation. It will create a tab with 2 buttons.
The third function will be excluded
"""


def simple_func_1():
    print 'This is a simple function'


def simple_func_2():
    print 'This is another simple function'


def simple_func_3():
    """
    scratch_exclude
    ^^ This causes the tool to skip the function when building buttons.
    It's OK to still have the rest of the docstring underneath, it just needs to start with "scratch_exclude."
    """
    print 'This function shouldn\'t show up...'
