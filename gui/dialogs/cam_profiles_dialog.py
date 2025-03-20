from PyQt5 import QtWidgets, QtCore

import globals_
from gui.dialogs.zone_dialog import CameraModeZoomSettingsLayout
from ui import GetIcon
from ui import createHorzLine


class CustomSortableListWidgetItem(QtWidgets.QListWidgetItem):
    """
    ListWidgetItem subclass that allows sorting by arbitrary key
    """
    sortKey = 0

    def __lt__(self, other):
        if hasattr(self, 'sortKey') and hasattr(other, 'sortKey'):
            return self.sortKey < other.sortKey

        return False


class CameraProfilesDialog(QtWidgets.QDialog):
    """
    Dialog for editing camera profiles
    """

    def __init__(self):
        """
        Creates and initialises the dialog
        """
        super(CameraProfilesDialog, self).__init__()
        self.setWindowTitle('Camera Profiles')
        self.setWindowIcon(GetIcon('camprofile'))
        self.setMinimumHeight(450)

        self.list = QtWidgets.QListWidget()
        self.list.itemSelectionChanged.connect(self.handleSelectionChanged)
        self.list.setSortingEnabled(True)

        self.addButton = QtWidgets.QPushButton('Add')
        self.addButton.clicked.connect(self.handleAdd)
        self.removeButton = QtWidgets.QPushButton('Remove')
        self.removeButton.clicked.connect(self.handleRemove)
        self.removeButton.setEnabled(False)

        listLayout = QtWidgets.QGridLayout()
        listLayout.addWidget(self.addButton, 0, 0)
        listLayout.addWidget(self.removeButton, 0, 1)
        listLayout.addWidget(self.list, 1, 0, 1, 2)

        self.eventid = QtWidgets.QSpinBox()
        self.eventid.setRange(0, 255)
        self.eventid.setToolTip(
            "<b>Triggering Event ID:</b><br>Sets the event ID that will trigger the camera profile. If switching away from a different profile, the previous profile's event ID will be automatically deactivated (so the game doesn't instantly switch back to it).")
        self.eventid.valueChanged.connect(self.handleEventIDChanged)

        self.camsettings = CameraModeZoomSettingsLayout(False)
        self.camsettings.set_values(0, 0)
        self.camsettings.edited.connect(self.handleCamSettingsChanged)

        profileLayout = QtWidgets.QFormLayout()
        profileLayout.addRow('Triggering Event ID:', self.eventid)
        profileLayout.addRow(createHorzLine())
        profileLayout.addRow(self.camsettings)

        self.profileBox = QtWidgets.QGroupBox('Modify Selected Camera Profile Properties')
        self.profileBox.setLayout(profileLayout)
        self.profileBox.setEnabled(False)
        self.profileBox.setToolTip(
            '<b>Modify Selected Camera Profile Properties:</b><br>Camera Profiles can only be used with the "Event-Controlled" camera mode in the "Zones" dialog.<br><br>Transitions between zoom levels are instant, but can be hidden through careful use of zoom sprites (206).')

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        Layout = QtWidgets.QGridLayout()
        Layout.addLayout(listLayout, 0, 0)
        Layout.addWidget(self.profileBox, 0, 1)
        Layout.addWidget(buttonBox, 1, 0, 1, 2)
        self.setLayout(Layout)

        for profile in globals_.Area.camprofiles:
            item = CustomSortableListWidgetItem()
            item.setData(QtCore.Qt.UserRole, profile)
            item.sortKey = profile[0]
            self.updateItemTitle(item)
            self.list.addItem(item)

        self.list.sortItems()

    def handleAdd(self, item=None):
        new_id = 1
        for row in range(self.list.count()):
            item = self.list.item(row)
            values = item.data(QtCore.Qt.UserRole)
            new_id = max(new_id, values[0] + 1)

        item = CustomSortableListWidgetItem()
        item.setData(QtCore.Qt.UserRole, [new_id, 0, 0])
        self.updateItemTitle(item)
        self.list.addItem(item)

    def handleRemove(self):
        self.list.takeItem(self.list.currentRow())

    def handleSelectionChanged(self):
        selItems = self.list.selectedItems()

        self.removeButton.setEnabled(bool(selItems))
        self.profileBox.setEnabled(bool(selItems))

        if selItems:
            selItem = selItems[0]
            values = selItem.data(QtCore.Qt.UserRole)

            self.eventid.setValue(values[0])
            self.camsettings.set_values(values[1], values[2])

    def handleEventIDChanged(self, eventid):
        selItem = self.list.selectedItems()[0]
        values = selItem.data(QtCore.Qt.UserRole)
        values[0] = eventid
        selItem.setData(QtCore.Qt.UserRole, values)
        selItem.sortKey = eventid
        self.updateItemTitle(selItem)

    def handleCamSettingsChanged(self):
        selItem = self.list.selectedItems()[0]
        values = selItem.data(QtCore.Qt.UserRole)
        values[1] = self.camsettings.mode_button_group.checkedId()
        values[2] = self.camsettings.screen_sizes.currentIndex()
        selItem.setData(QtCore.Qt.UserRole, values)

    def updateItemTitle(self, item):
        item.setText('Camera Profile on Event %d' % item.data(QtCore.Qt.UserRole)[0])
