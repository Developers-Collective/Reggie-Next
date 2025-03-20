from PyQt5 import QtWidgets

import globals_
from ui import GetIcon


class ScreenCapChoiceDialog(QtWidgets.QDialog):
    """
    Dialog which lets you choose which zone to take a pic of
    """

    def __init__(self):
        """
        Creates and initializes the dialog
        """
        QtWidgets.QDialog.__init__(self)
        self.setWindowTitle(globals_.trans.string('ScrShtDlg', 0))
        self.setWindowIcon(GetIcon('screenshot'))

        self.zoneCombo = QtWidgets.QComboBox()
        self.zoneCombo.addItem(globals_.trans.string('ScrShtDlg', 1))
        self.zoneCombo.addItem(globals_.trans.string('ScrShtDlg', 2))
        for i in range(len(globals_.Area.zones)):
            self.zoneCombo.addItem(globals_.trans.string('ScrShtDlg', 3, '[zone]', i + 1))

        self.hide_background = QtWidgets.QCheckBox()
        self.save_img = QtWidgets.QRadioButton()
        self.save_clip = QtWidgets.QRadioButton()

        self.save_img.setChecked(True)

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QtWidgets.QFormLayout()
        mainLayout.addRow("Target", self.zoneCombo)
        mainLayout.addRow("Hide background", self.hide_background)
        mainLayout.addRow("Save image to file", self.save_img)
        mainLayout.addRow("Copy image", self.save_clip)
        mainLayout.addRow(buttonBox)
        self.setLayout(mainLayout)


class AutoSavedInfoDialog(QtWidgets.QDialog):
    """
    Dialog which lets you know that an auto saved level exists
    """

    def __init__(self, filename):
        """
        Creates and initializes the dialog
        """
        QtWidgets.QDialog.__init__(self)
        self.setWindowTitle(globals_.trans.string('AutoSaveDlg', 0))
        self.setWindowIcon(GetIcon('save'))

        mainlayout = QtWidgets.QVBoxLayout(self)

        hlayout = QtWidgets.QHBoxLayout()

        icon = QtWidgets.QLabel()
        hlayout.addWidget(icon)

        label = QtWidgets.QLabel(globals_.trans.string('AutoSaveDlg', 1, '[path]', filename))
        label.setWordWrap(True)
        hlayout.addWidget(label)
        hlayout.setStretch(1, 1)

        buttonbox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.No | QtWidgets.QDialogButtonBox.Yes)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)

        mainlayout.addLayout(hlayout)
        mainlayout.addWidget(buttonbox)


class AreaChoiceDialog(QtWidgets.QDialog):
    """
    Dialog which lets you choose an area
    """

    def __init__(self, areacount):
        """
        Creates and initializes the dialog
        """
        QtWidgets.QDialog.__init__(self)
        self.setWindowTitle(globals_.trans.string('AreaChoiceDlg', 0))
        self.setWindowIcon(GetIcon('areas'))

        self.areaCombo = QtWidgets.QComboBox()
        for i in range(areacount):
            self.areaCombo.addItem(globals_.trans.string('AreaChoiceDlg', 1, '[num]', i + 1))

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.areaCombo)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
