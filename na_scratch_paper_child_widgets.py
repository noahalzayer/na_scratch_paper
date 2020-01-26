# -*- coding: utf-8 -*-
"""
Module containing extra windows for na_scratch_paper
"""
import os
import sys
from functools import partial

from PySide2 import QtWidgets, QtCore, QtGui

import na_scratch_paper_tab_widgets as tab_widgets


class AdvQuickRef(QtWidgets.QWidget):
    """
    Window for quick reference on marking up modules for advanced tabs
    """
    def __init__(self, parent):
        """
        Initial call method
        Args:
            parent (na_scratch_paper.ScratchPaperWidget): The parent widget
        """
        super(AdvQuickRef, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle('Script Markup Quick-Reference')

        self.setLayout(QtWidgets.QVBoxLayout())

        scroll = QtWidgets.QScrollArea(self)
        scroll.setWidget(QtWidgets.QWidget())
        scroll.setWidgetResizable(True)
        self.layout().addWidget(scroll)
        body_lwt = QtWidgets.QVBoxLayout()
        scroll.setWidget(QtWidgets.QWidget())
        scroll.widget().setLayout(body_lwt)

        txt = '<html><head/><body><p><span style=" font-size:14pt; font-weight:600; text-decoration: underline; color' \
              ':#e4e4e4;">Simple Tabs:</span></p><p><span style=" color:#e4e4e4;">For any scripts that are added that' \
              ' don\'t have any markup, the tool will simply add buttons for all &quot;callables&quot; (functions, cl' \
              'asses, etc) that are declared within the script in the base namespace. </span></p><p><br/></p><p><span' \
              ' style=" color:#e4e4e4;">If you wish to exclude any functions within the script, simply add </span><sp' \
              'an style=" font-weight:600; font-style:italic; color:#e4e4e4;">scratch_exclude</span><span style=" col' \
              'or:#e4e4e4;"> at the beginning of the docstring (an unassigned string at the beginning of the function' \
              ', google if you wanna know more) and it should skip that function when building the tab.</span></p></b' \
              'ody></html>'
        body_lwt.addWidget(self.wrapping_label(txt))
        body_lwt.addSpacing(60)
        tab_widgets.Separator(scroll.widget(), {}, body_lwt)
        body_lwt.addSpacing(60)

        txt = '<html><head/><body><p><span style=" font-size:14pt; font-weight:600; text-decoration: underline; color' \
              ':#e4e4e4;">Advanced Tabs:</span></p><p><span style=" color:#e4e4e4;">For more power-users or people wh' \
              'o want more control over how things are built or want to be able to supply arguments to their function' \
              's, the script can be marked up using a dict variable named </span><span style=" font-weight:600; font-' \
              'style:italic; color:#e4e4e4;">sp_instructions.</span></p><p><br/></p><p><span style=" font-size:10pt; ' \
              'font-weight:600; color:#e4e4e4;">sp_instructions Structure:</span></p><p><span style=" color:#e4e4e4;"' \
              '>It\'s recommended that you top the module with this:</span></p></body></html>'
        body_lwt.addWidget(self.wrapping_label(txt))
        
        txt = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><h' \
              'ead><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</styl' \
              'e></head><body style=" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:norm' \
              'al;"><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent' \
              ':0; text-indent:0px;"><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#e4e4e4;">sp_inst' \
              'ructions = {</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'contents' \
              '\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: []</span><span sty' \
              'le=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">,</span></p><p style=" margin-top:0px;' \
              ' margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span sty' \
              'le=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">                   \'settings\': </spa' \
              'n><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">{}} # Any overall settings ' \
              'should go here if you want</span></p></body></html>'
        browser = QtWidgets.QTextBrowser()
        browser.setWordWrapMode(QtGui.QTextOption.NoWrap)
        browser.setText(txt)
        body_lwt.addWidget(browser)
        body_lwt.addSpacing(60)

        txt = '<html><head/><body><p><span style=" color:#e4e4e4;">Then precede function definitions with something s' \
              'imilar to this:</span></p></body></html>'
        body_lwt.addWidget(self.wrapping_label(txt))
        
        txt = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><h' \
              'ead><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</styl' \
              'e></head><body style=" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:norm' \
              'al;"><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent' \
              ':0; text-indent:0px;"><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#e4e4e4;">sp_inst' \
              'ructions</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">[</span><span ' \
              'style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'contents\'</span><span style=" fo' \
              'nt-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">].append({</span><span style=" font-family:\'' \
              'Consolas\'; font-size:9.8pt; color:#a5c261;">\'label\'</span><span style=" font-family:\'Consolas\'; f' \
              'ont-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; colo' \
              'r:#a5c261;">\'Do Something To a Node\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; ' \
              'color:#cc7832;">,</span></p><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-righ' \
              't:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'Consolas\'; font-size:9.8pt; ' \
              'color:#a5c261;">                                    \'inputWidgets\'</span><span style=" font-family:' \
              '\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: [{</span><span style=" font-family:\'Consolas\'; font' \
              '-size:9.8pt; color:#a5c261;">\'type\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; c' \
              'olor:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'pyN' \
              'ode\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </span><span st' \
              'yle=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'label\'</span><span style=" font-fa' \
              'mily:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; f' \
              'ont-size:9.8pt; color:#a5c261;">\'Node: \'</span><span style=" font-family:\'Consolas\'; font-size:9.8' \
              'pt; color:#a9b7c6;">}]</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;"' \
              '>,<br />                                    </span><span style=" font-family:\'Consolas\'; font-size:9' \
              '.8pt; color:#a5c261;">\'buttons\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color' \
              ':#a9b7c6;">: [{</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'label' \
              '\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style' \
              '=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'Run from Field\'</span><span style=" f' \
              'ont-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" font-family:\'Consola' \
              's\'; font-size:9.8pt; color:#a5c261;">\'function\'</span><span style=" font-family:\'Consolas\'; font-' \
              'size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a' \
              '5c261;">\'do_something\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;' \
              '">, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'inputs\'</span><' \
              'span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: [</span><span style=" font-f' \
              'amily:\'Consolas\'; font-size:9.8pt; color:#6897bb;">0</span><span style=" font-family:\'Consolas\'; f' \
              'ont-size:9.8pt; color:#a9b7c6;">]</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color' \
              ':#cc7832;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'share\'' \
              '</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style="' \
              ' font-family:\'Consolas\'; font-size:9.8pt; color:#8888c6;">True</span><span style=" font-family:\'Con' \
              'solas\'; font-size:9.8pt; color:#a9b7c6;">}</span><span style=" font-family:\'Consolas\'; font-size:9.' \
              '8pt; color:#cc7832;">,<br />                                                </span><span style=" font-' \
              'family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">{</span><span style=" font-family:\'Consolas\'; ' \
              'font-size:9.8pt; color:#a5c261;">\'label\'</span><span style=" font-family:\'Consolas\'; font-size:9.8' \
              'pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">' \
              '\'Run from Current Selection\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#c' \
              'c7832;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'function\'' \
              '</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style="' \
              ' font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'do_something\'</span><span style=" font-' \
              'family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">}]})</span></p></body></html>'
        browser = QtWidgets.QTextBrowser()
        browser.setWordWrapMode(QtGui.QTextOption.NoWrap)
        browser.setText(txt)
        body_lwt.addWidget(browser)

        body_lwt.addSpacing(60)

        txt = '<html><head/><body><p><span style=" font-size:10pt; font-weight:600; color:#e4e4e4;">Widget Templates:' \
              '</span></p></body></html>'
        body_lwt.addWidget(self.wrapping_label(txt))
        
        txt = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><h' \
              'ead><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</styl' \
              'e></head><body style=" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:norm' \
              'al;"><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent' \
              ':0; text-indent:0px;"><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#808080;">#######' \
              '############################################<br /># Things to Add in to sp_instructions[\'contents\'] ' \
              '#<br />###################################################<br /># Simple Button<br /></span><span styl' \
              'e=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">{</span><span style=" font-family:\'Con' \
              'solas\'; font-size:9.8pt; color:#a5c261;">\'simple\'</span><span style=" font-family:\'Consolas\'; fon' \
              't-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:' \
              '#a5c261;">\'do_something_simple\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color' \
              ':#cc7832;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'label\'' \
              '</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style="' \
              ' font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'Button Label\'</span><span style=" font-' \
              'family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" font-family:\'Consolas\';' \
              ' font-size:9.8pt; color:#a5c261;">\'tooltip\'</span><span style=" font-family:\'Consolas\'; font-size:' \
              '9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261' \
              ';">\'Button tool tip\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">' \
              '}<br /><br /></span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#808080;"># Frame<b' \
              'r /></span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">{</span><span styl' \
              'e=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'label\'</span><span style=" font-fami' \
              'ly:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; fon' \
              't-size:9.8pt; color:#a5c261;">\'Frame Label\'</span><span style=" font-family:\'Consolas\'; font-size:' \
              '9.8pt; color:#cc7832;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261' \
              ';">\'color\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: [</span>' \
              '<span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#6897bb;">100</span><span style=" font-' \
              'family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" font-family:\'Consolas\';' \
              ' font-size:9.8pt; color:#6897bb;">20</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; co' \
              'lor:#cc7832;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#6897bb;">20</sp' \
              'an><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">]</span><span style=" font' \
              '-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" font-family:\'Consolas\'' \
              '; font-size:9.8pt; color:#a5c261;">\'image\'</span><span style=" font-family:\'Consolas\'; font-size:9' \
              '.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;' \
              '">\'path/to/image.png\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;"' \
              '>, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'toolTip\'</span><' \
              'span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-fa' \
              'mily:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'This is a Frame\'</span><span style=" font-famil' \
              'y:\'Consolas\'; font-size:9.8pt; color:#cc7832;">,<br /> </span><span style=" font-family:\'Consolas\'' \
              '; font-size:9.8pt; color:#a5c261;">\'inputWidgets\'</span><span style=" font-family:\'Consolas\'; font' \
              '-size:9.8pt; color:#a9b7c6;">: []</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color' \
              ':#cc7832;">,  </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#808080;"># Indici' \
              'es of the widgets you want to read should be in \'inputs\' below (1st and 3rd widget = [0, 2])<br /> <' \
              '/span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'buttons\'</span><span' \
              ' style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: [{</span><span style=" font-fami' \
              'ly:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'label\'</span><span style=" font-family:\'Consolas' \
              '\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt;' \
              ' color:#a5c261;">\'Button\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc78' \
              '32;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'function\'</s' \
              'pan><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" fo' \
              'nt-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'do_something\'</span><span style=" font-fam' \
              'ily:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" font-family:\'Consolas\'; fo' \
              'nt-size:9.8pt; color:#a5c261;">\'inputs\'</span><span style=" font-family:\'Consolas\'; font-size:9.8p' \
              't; color:#a9b7c6;">: []</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;"' \
              '>, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'share\'</span><sp' \
              'an style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-fami' \
              'ly:\'Consolas\'; font-size:9.8pt; color:#8888c6;">False</span><span style=" font-family:\'Consolas\'; ' \
              'font-size:9.8pt; color:#cc7832;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; col' \
              'or:#a5c261;">\'toolTip\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;' \
              '">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'This is a Button' \
              '.\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">,<br />            ' \
              '  </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'icon\'</span><span' \
              ' style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family' \
              ':\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'path/to/icon.png\'</span><span style=" font-family:' \
              '\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" font-family:\'Consolas\'; font-s' \
              'ize:9.8pt; color:#a5c261;">\'color\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; co' \
              'lor:#a9b7c6;">: [</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#6897bb;">40</s' \
              'pan><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" fo' \
              'nt-family:\'Consolas\'; font-size:9.8pt; color:#6897bb;">40</span><span style=" font-family:\'Consolas' \
              '\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt;' \
              ' color:#6897bb;">40</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">]}]' \
              '}  </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#808080;"># Other buttons can' \
              ' be added to the list if desired<br /><br />################<br /># inputWidgets #<br />##############' \
              '##<br /># Stretch<br /></span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;"' \
              '>{</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'type\'</span><span' \
              ' style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family' \
              ':\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'stretch\'</span><span style=" font-family:\'Consolas' \
              '\'; font-size:9.8pt; color:#a9b7c6;">}<br /><br /></span><span style=" font-family:\'Consolas\'; font-' \
              'size:9.8pt; color:#808080;"># Spacer<br /></span><span style=" font-family:\'Consolas\'; font-size:9.8' \
              'pt; color:#a9b7c6;">{</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">' \
              '\'type\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span' \
              ' style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'spacer\'</span><span style=" fon' \
              't-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" font-family:\'Consolas' \
              '\'; font-size:9.8pt; color:#a5c261;">\'size\'</span><span style=" font-family:\'Consolas\'; font-size:' \
              '9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#6897bb' \
              ';">50</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">}<br /><br /></sp' \
              'an><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#808080;"># Separator<br /></span><s' \
              'pan style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">{</span><span style=" font-fami' \
              'ly:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'type\'</span><span style=" font-family:\'Consolas' \
              '\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt;' \
              ' color:#a5c261;">\'separator\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#c' \
              'c7832;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'vertical\'' \
              '</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style="' \
              ' font-family:\'Consolas\'; font-size:9.8pt; color:#8888c6;">False</span><span style=" font-family:\'Co' \
              'nsolas\'; font-size:9.8pt; color:#a9b7c6;">}<br /><br /></span><span style=" font-family:\'Consolas\';' \
              ' font-size:9.8pt; color:#808080;"># LineEdit<br /></span><span style=" font-family:\'Consolas\'; font-' \
              'size:9.8pt; color:#a9b7c6;">{</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5' \
              'c261;">\'type\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </spa' \
              'n><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'lineEdit\'</span><span st' \
              'yle=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" font-family:\'' \
              'Consolas\'; font-size:9.8pt; color:#a5c261;">\'label\'</span><span style=" font-family:\'Consolas\'; f' \
              'ont-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; colo' \
              'r:#a5c261;">\'Line Edit:\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc783' \
              '2;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'toolTip\'</spa' \
              'n><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font' \
              '-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'This is a Line Edit Input Widget.\'</span><sp' \
              'an style=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" font-fami' \
              'ly:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'text\'</span><span style=" font-family:\'Consolas' \
              '\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt;' \
              ' color:#a5c261;">\'\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">,' \
              ' </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'placeholderText\'</' \
              'span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" f' \
              'ont-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'Placeholder\'</span><span style=" font-fam' \
              'ily:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">}<br /><br /></span><span style=" font-family:\'Con' \
              'solas\'; font-size:9.8pt; color:#808080;"># Selection<br /></span><span style=" font-family:\'Consolas' \
              '\'; font-size:9.8pt; color:#a9b7c6;">{</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; ' \
              'color:#a5c261;">\'type\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;' \
              '">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'selection\'</spa' \
              'n><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" font' \
              '-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'label\'</span><span style=" font-family:\'Con' \
              'solas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9' \
              '.8pt; color:#a5c261;">\'Selection:\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; co' \
              'lor:#cc7832;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'tool' \
              'Tip\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span st' \
              'yle=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'This is a Selection Input Widget.\'' \
              '</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </span><span style="' \
              ' font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'text\'</span><span style=" font-family:' \
              '\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-s' \
              'ize:9.8pt; color:#a5c261;">\'\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#' \
              'cc7832;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'placehold' \
              'erText\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span' \
              ' style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'Placeholder\'</span><span style=' \
              '" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">}<br /><br /></span><span style=" font-fa' \
              'mily:\'Consolas\'; font-size:9.8pt; color:#808080;"># SelectionMulti<br /></span><span style=" font-fa' \
              'mily:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">{</span><span style=" font-family:\'Consolas\'; fo' \
              'nt-size:9.8pt; color:#a5c261;">\'type\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt;' \
              ' color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'s' \
              'electionMulti\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </spa' \
              'n><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'label\'</span><span style' \
              '=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Con' \
              'solas\'; font-size:9.8pt; color:#a5c261;">\'Selection Multi:\'</span><span style=" font-family:\'Conso' \
              'las\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8' \
              'pt; color:#a5c261;">\'toolTip\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#' \
              'a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'This is a' \
              ' Selection Multi Input Widget.\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:' \
              '#cc7832;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'text\'</' \
              'span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" f' \
              'ont-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'\'</span><span style=" font-family:\'Conso' \
              'las\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8' \
              'pt; color:#a5c261;">\'placeholderText\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt;' \
              ' color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'P' \
              'laceholder\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">}<br /><br' \
              ' /></span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#808080;"># PyNode<br /></spa' \
              'n><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">{</span><span style=" font-' \
              'family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'type\'</span><span style=" font-family:\'Conso' \
              'las\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8' \
              'pt; color:#a5c261;">\'pyNode\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#c' \
              'c7832;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'label\'</s' \
              'pan><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" fo' \
              'nt-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'PyNode:\'</span><span style=" font-family:' \
              '\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" font-family:\'Consolas\'; font-s' \
              'ize:9.8pt; color:#a5c261;">\'toolTip\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; ' \
              'color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'Th' \
              'is is a PyNode Input Widget.\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#c' \
              'c7832;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'text\'</sp' \
              'an><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" fon' \
              't-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'\'</span><span style=" font-family:\'Consola' \
              's\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt' \
              '; color:#a5c261;">\'placeholderText\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; c' \
              'olor:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'Pla' \
              'ceholder\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">}<br /><br /' \
              '></span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#808080;"># PyNodeMulti<br /></' \
              'span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">{</span><span style=" fo' \
              'nt-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'type\'</span><span style=" font-family:\'Co' \
              'nsolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:' \
              '9.8pt; color:#a5c261;">\'pyNodeMulti\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; ' \
              'color:#cc7832;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'la' \
              'bel\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span st' \
              'yle=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'PyNode Multi:\'</span><span style="' \
              ' font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" font-family:\'Conso' \
              'las\'; font-size:9.8pt; color:#a5c261;">\'toolTip\'</span><span style=" font-family:\'Consolas\'; font' \
              '-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#' \
              'a5c261;">\'This is a PyNode Multi Input Widget.\'</span><span style=" font-family:\'Consolas\'; font-s' \
              'ize:9.8pt; color:#cc7832;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5' \
              'c261;">\'text\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </spa' \
              'n><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'\'</span><span style=" fo' \
              'nt-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" font-family:\'Consolas' \
              '\'; font-size:9.8pt; color:#a5c261;">\'placeholderText\'</span><span style=" font-family:\'Consolas\';' \
              ' font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; co' \
              'lor:#a5c261;">\'Placeholder\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9' \
              'b7c6;">}<br /><br /></span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#808080;"># ' \
              'IntSpinner<br /></span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">{</spa' \
              'n><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'type\'</span><span style=' \
              '" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Cons' \
              'olas\'; font-size:9.8pt; color:#a5c261;">\'intSpinner\'</span><span style=" font-family:\'Consolas\'; ' \
              'font-size:9.8pt; color:#cc7832;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; col' \
              'or:#a5c261;">\'label\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">' \
              ': </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'Int Spinner:\'</sp' \
              'an><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" fon' \
              't-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'toolTip\'</span><span style=" font-family:\'' \
              'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-siz' \
              'e:9.8pt; color:#a5c261;">\'This is a Int Spinner Input Widget.\'</span><span style=" font-family:\'Con' \
              'solas\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" font-family:\'Consolas\'; font-size:9' \
              '.8pt; color:#a5c261;">\'value\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#' \
              'a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#6897bb;">0</span><sp' \
              'an style=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" font-fami' \
              'ly:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'min\'</span><span style=" font-family:\'Consolas\'' \
              '; font-size:9.8pt; color:#a9b7c6;">: -</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; ' \
              'color:#6897bb;">100</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, <' \
              '/span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'max\'</span><span sty' \
              'le=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'C' \
              'onsolas\'; font-size:9.8pt; color:#6897bb;">100</span><span style=" font-family:\'Consolas\'; font-siz' \
              'e:9.8pt; color:#a9b7c6;">}<br /><br /></span><span style=" font-family:\'Consolas\'; font-size:9.8pt; ' \
              'color:#808080;"># FloatSpinner<br /></span><span style=" font-family:\'Consolas\'; font-size:9.8pt; co' \
              'lor:#a9b7c6;">{</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'typ' \
              'e\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span styl' \
              'e=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'floatSpinner\'</span><span style=" fo' \
              'nt-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" font-family:\'Consolas' \
              '\'; font-size:9.8pt; color:#a5c261;">\'label\'</span><span style=" font-family:\'Consolas\'; font-size' \
              ':9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c26' \
              '1;">\'Float Spinner:\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">' \
              ', </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'toolTip\'</span><s' \
              'pan style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-fam' \
              'ily:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'This is a Float Spinner Input Widget.\'</span><sp' \
              'an style=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" font-fami' \
              'ly:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'value\'</span><span style=" font-family:\'Consolas' \
              '\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt;' \
              ' color:#6897bb;">0</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </' \
              'span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'min\'</span><span styl' \
              'e=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: -</span><span style=" font-family:\'C' \
              'onsolas\'; font-size:9.8pt; color:#6897bb;">100</span><span style=" font-family:\'Consolas\'; font-siz' \
              'e:9.8pt; color:#cc7832;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c2' \
              '61;">\'max\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><' \
              'span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#6897bb;">100</span><span style=" font-f' \
              'amily:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">}<br /><br /></span><span style=" font-family:\'C' \
              'onsolas\'; font-size:9.8pt; color:#808080;"># Check,<br /></span><span style=" font-family:\'Consolas' \
              '\'; font-size:9.8pt; color:#a9b7c6;">{</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; ' \
              'color:#a5c261;">\'type\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;' \
              '">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'check\'</span><s' \
              'pan style=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" font-fam' \
              'ily:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'label\'</span><span style=" font-family:\'Consola' \
              's\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size:9.8pt' \
              '; color:#a5c261;">\'Check Box:\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:' \
              '#cc7832;">, </span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'toolTip' \
              '\'</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style' \
              '=" font-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'This is a Check Box Input Widget.\'</s' \
              'pan><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#cc7832;">, </span><span style=" fo' \
              'nt-family:\'Consolas\'; font-size:9.8pt; color:#a5c261;">\'value\'</span><span style=" font-family:\'C' \
              'onsolas\'; font-size:9.8pt; color:#a9b7c6;">: </span><span style=" font-family:\'Consolas\'; font-size' \
              ':9.8pt; color:#8888c6;">False</span><span style=" font-family:\'Consolas\'; font-size:9.8pt; color:#a9' \
              'b7c6;">}<br /></span></p></body></html>'

        browser = QtWidgets.QTextBrowser()
        browser.setWordWrapMode(QtGui.QTextOption.NoWrap)
        browser.setText(txt)
        browser.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        browser.setMinimumHeight(500)
        body_lwt.addWidget(browser)

    def wrapping_label(self, txt):
        """
        Creates a label with rich text format that's properly aligned and set to wrap.
        Args:
            txt (str): The text you want to pass in.
        """
        lbl = QtWidgets.QLabel(txt)
        lbl.setTextFormat(QtCore.Qt.RichText)
        lbl.setAlignment(QtCore.Qt.AlignTop)
        lbl.setWordWrap(True)
        return lbl


class EditScriptListDialog(QtWidgets.QDialog):
    """
    Custom dialog for adjusting the scripts being sourced in the scratch paper window
    """
    def __init__(self, parent, data):
        """
        Initial call method
        Args:
            parent (na_scratch_paper.ScratchPaperWidget): The parent widget
            data (dict): Data being passed in to the widget {(str) name: Tab Label, (str) path: Path to the script,
                                                             (list) excluded: Buttons to Exclude from the UI}
        """
        super(EditScriptListDialog, self).__init__(parent)
        self.setWindowTitle('Edit Script List')
        self.data = data

        self.create_base()
        self.populate_table()


    def create_base(self):
        """
        Creates the Main UI elements.
        """
        conditional_enable_btns = []
        main_lwt = QtWidgets.QVBoxLayout()
        main_lwt.setContentsMargins(20, 20, 20, 20)
        self.setLayout(main_lwt)

        # Add and Remove buttons
        add_remove_lwt = QtWidgets.QHBoxLayout()
        main_lwt.addLayout(add_remove_lwt)
        btn = QtWidgets.QPushButton('Add')
        btn.clicked.connect(self.add)
        add_remove_lwt.addWidget(btn)
        btn = QtWidgets.QPushButton('Remove')
        btn.clicked.connect(self.remove)
        conditional_enable_btns.append(btn)
        add_remove_lwt.addWidget(btn)

        # Table
        line = QtWidgets.QFrame()
        main_lwt.addWidget(line)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.table = QtWidgets.QTableWidget()
        table_lwt = QtWidgets.QHBoxLayout()
        main_lwt.addLayout(table_lwt)
        table_lwt.addWidget(self.table)
        self.table.setColumnCount(2)
        self.table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table.setHorizontalHeaderLabels(['Name', 'Script Path'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.table_menu)

        # Table item nudging buttons
        line = QtWidgets.QFrame()
        table_lwt.addWidget(line)
        line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)

        table_btn_lwt = QtWidgets.QVBoxLayout()
        table_btn_lwt.setSpacing(20)
        table_lwt.addLayout(table_btn_lwt)
        labels = u'🠉🠉'.encode('utf-8'), u'🠉'.encode('utf-8'), u'🠟'.encode('utf-8'), u'🠟🠟'.encode('utf-8')
        clues = 'top', 'up', 'down', 'bottom'

        for i, label in enumerate(labels):
            btn = QtWidgets.QPushButton(label)
            btn.setToolTip('{} {}'.format('Nudge' if i % 3 else 'Send to', clues[i]))
            btn.clicked.connect(partial(self.move_table_items, clues[i]))

            table_btn_lwt.addWidget(btn)
            conditional_enable_btns.append(btn)

        # Bottom Buttons
        line = QtWidgets.QFrame()
        main_lwt.addWidget(line)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        bottom_btn_lwt = QtWidgets.QHBoxLayout()
        main_lwt.addLayout(bottom_btn_lwt)
        btn = QtWidgets.QPushButton('Save')
        btn.setDefault(True)
        btn.clicked.connect(self.save)
        bottom_btn_lwt.addWidget(btn)
        btn = QtWidgets.QPushButton('Cancel')
        btn.clicked.connect(self.reject)
        bottom_btn_lwt.addWidget(btn)

        # Sizing and Spacing based on elements in window
        btn_width = QtGui.QFontMetrics(conditional_enable_btns[-1].font()).width(conditional_enable_btns[-1].text())*1.5
        for i in range(len(labels)):
            conditional_enable_btns[-(i+1)].setFixedWidth(btn_width)

        table_btn_lwt.addStretch()
        add_remove_lwt.addSpacing(btn_width + table_btn_lwt.spacing())
        self.resize((self.table.columnWidth(0) + self.table.columnWidth(1)) * 2, self.height())

        # Button Enabling Logic
        [btn.setEnabled(False) for btn in conditional_enable_btns]
        func = lambda: [btn.setEnabled(len(self.table.selectedItems())) for btn in conditional_enable_btns]
        self.table.itemSelectionChanged.connect(func)


    def populate_table(self):
        """
        Populates the table widget according to existing scripts in the list according to the value in self.data
        """
        self.table.clearContents()
        for data in self.data:
            self.append_row(data)


    def append_row(self, data):
        """
        Adds a row and items to the table based on the data.
        Args:
            data (dict): Data being passed in to the widget {(str) name: Tab Label, (str) path: Path to the script,
                                                             (list) excluded: Buttons to Exlcude from the UI}
        """
        row = self.table.rowCount()
        self.table.setRowCount(row + 1)
        self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(data['name']))
        self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(data['script']))
        self.table.item(row, 1).excluded = data.get('excluded', [])


    def move_table_items(self, clue):
        """
        Moves or nudges table items according to the given clue.
        Args:
            clue (str): clue as to where to move the selected items. Accepted are 'up', 'down', 'top,' or 'bottom'
        """
        selected_rows = list(set(item.row() for item in self.table.selectedItems()))
        if clue in ['down', 'bottom']:
            selected_rows.reverse()

        # Figure out what's moving
        out_rows = list(selected_rows)
        for i, row in enumerate(out_rows):
            dst = {'up': row + -1, 'down': row + 1, 'top': 0, 'bottom': self.table.rowCount() - 1}
            out_row = dst[clue]
            if 0 <= out_row <= self.table.rowCount() - 1:
                for j in range(self.table.rowCount()):
                    if out_row in out_rows:
                        if out_row is not row:
                            out_row = out_row + 1 if clue in ['up', 'top'] else out_row - 1
                    else:
                        break
            else:
                out_row = int(row)
            out_rows[i] = out_row

        # Move the items and grab the items that have been priced out of the neighborhood #gentrification
        displaced = []
        for i, row in enumerate(out_rows):
            if row is not selected_rows[i]:
                displaced.append([row, self.table.takeItem(row, 0), self.table.takeItem(row, 1)])
                self.table.setItem(row, 0, self.table.takeItem(selected_rows[i], 0))
                self.table.setItem(row, 1, self.table.takeItem(selected_rows[i], 1))

        # Find new homes for the displaced objects
        for i, [row, item1, item2] in enumerate(displaced):
            for j in range(self.table.rowCount()):
                if not self.table.item(row, 0):
                    break
                row = row + 1 if clue in ['up', 'top'] else row - 1

            self.table.setItem(row, 0, item1)
            self.table.setItem(row, 1, item2)
            displaced[i][0] = row

        # Select moved items in their new homes
        [item.setSelected(False) for item in self.table.selectedItems()]
        self.table.setSelectionMode(QtWidgets.QTableWidget.MultiSelection)
        for row in out_rows:
            self.table.selectRow(row)
        self.table.setSelectionMode(QtWidgets.QTableWidget.ExtendedSelection)


    def read_table(self):
        """
        Reads the contents of the table and returns the values
        Returns:
            data (list): Data from each row's items {(str) name: Tab Label, (str) path: Path to the script,
                                                     (list) excluded: Buttons to Exclude from the UI}
        """
        data = []
        for row in range(self.table.rowCount()):
            name = str(self.table.item(row, 0).text())
            script = str(self.table.item(row, 1).text())
            excluded = self.table.item(row, 1).excluded

            if not name:
                sys.stdout.write('Name for row {} not set. The tool will make '
                                 'the tab label "Default."\n'.format(row + 1))

            if not os.path.exists(script):
                sys.stderr.write('Path for row {} doesn\'t exist on your system. Cancelling Save.'.format(row + 1))
                return

            if ' ' in script:
                sys.stderr.write('Path for row {} has spaces. This can mess with this script and python in general, '
                                 'and thus can\'t be added.'.format(row + 1))
                return

            data.append({'name': name, 'script': script, 'excluded': excluded})
        return data


    def add(self):
        """
        Adds a script to the list.
        """
        file_dialog = QtWidgets.QFileDialog(caption='New Script', filter='*.py')
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)

        file_dialog.exec_()
        if not file_dialog.result():
            return

        text, ok = QtWidgets.QInputDialog().getText(self, '(Optional) Tab Name',
                                                    '  What tab label would you like for this script? (optional)  ')

        name = str(text) if ok else ''
        script = str(file_dialog.selectedFiles()[0])
        self.append_row({'name': name, 'script': script})


    def remove(self):
        """
        Removes the selected rows from the list.
        """
        for row in reversed(list(set([item.row() for item in self.table.selectedItems()]))):
            self.table.removeRow(row)


    def edit_paths(self):
        """
        Opens up file browsers for selected items to edit paths
        """
        for row in list(set([item.row() for item in self.table.selectedItems()])):
            path = os.path.dirname(self.table.item(row, 1).text())
            dialog = QtWidgets.QFileDialog(caption='Edit Row {} Path'.format(row + 1), filter='*.py', directory=path)
            dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
            dialog.exec_()
            
            if not dialog.result():
                break
            
            self.table.item(row, 1).setText(dialog.selectedFiles()[0])


    def table_menu(self, *args):
        """
        Sets up a right-click menu for editing the table.
        """
        if self.table.selectedItems():
            menu = QtWidgets.QMenu()
            clues = 'top', 'up', 'down', 'bottom'
            for i, clue in enumerate(clues):
                menu.addAction('{} {}'.format('Nudge' if i % 3 else 'Send to', clues[i].capitalize()),
                               partial(self.move_table_items, clue))
            menu.addSeparator()
            menu.addAction('Edit Path(s)', self.edit_paths)
            menu.addAction('Remove', self.remove)

            menu.exec_(QtGui.QCursor.pos())


    def save(self):
        """
        Runs read_table, then if it was successful, saves to prefs and closes the window.
        """
        data = self.read_table()
        if data is None:
            return

        self.data = data
        self.accept()
