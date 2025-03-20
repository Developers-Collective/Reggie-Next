import os

from PyQt5 import QtWidgets, QtGui

import globals_
from res import load_resource_as_str
from ui import GetIcon


class AboutDialog(QtWidgets.QDialog):

    def __init__(self):
        """
        Creates and initializes the dialog
        """
        QtWidgets.QDialog.__init__(self)
        self.setWindowTitle(globals_.trans.string('AboutDlg', 0))
        self.setWindowIcon(GetIcon('reggie'))

        # Open the readme file
        readme = ""
        with open('readme.md', 'r', encoding='utf-8') as f:
            readme = f.read()

        # Logo
        logo = QtGui.QPixmap(os.path.join('reggiedata', 'about.png'))
        logoLabel = QtWidgets.QLabel()
        logoLabel.setPixmap(logo)
        logoLabel.setContentsMargins(16, 4, 32, 4)

        # Description
        description = ''.join(load_resource_as_str('about_text.html', relative_path='text/'))

        # Description label
        descLabel = QtWidgets.QLabel()
        descLabel.setText(description)
        descLabel.setMinimumWidth(512)
        descLabel.setWordWrap(True)

        # Readme.md viewer
        readmeView = QtWidgets.QPlainTextEdit()
        readmeView.setPlainText(readme)
        readmeView.setReadOnly(True)

        # Buttonbox
        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept)

        # Main layout
        L = QtWidgets.QGridLayout()
        L.addWidget(logoLabel, 0, 0, 2, 1)
        L.addWidget(descLabel, 0, 1)
        L.addWidget(readmeView, 1, 1)
        L.addWidget(buttonBox, 2, 0, 1, 2)
        L.setRowStretch(1, 1)
        L.setColumnStretch(1, 1)
        self.setLayout(L)