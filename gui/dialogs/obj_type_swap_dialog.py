from PyQt5 import QtWidgets

import globals_
from dirty import SetDirty
from ui import GetIcon


class ObjectTypeSwapDialog(QtWidgets.QDialog):
    """
    Lets you pick object types to swap objects to
    """

    def __init__(self):
        """
        Creates and initializes the dialog
        """
        QtWidgets.QDialog.__init__(self)
        self.setWindowTitle(globals_.trans.string("MenuItems", 106))
        self.setWindowIcon(GetIcon('swap'))

        # Create widgets
        self.FromType = QtWidgets.QSpinBox()
        self.FromType.setRange(0, 255)

        self.ToType = QtWidgets.QSpinBox()
        self.ToType.setRange(0, 255)

        self.FromTileset = QtWidgets.QSpinBox()
        self.FromTileset.setRange(1, 4)

        self.ToTileset = QtWidgets.QSpinBox()
        self.ToTileset.setRange(1, 4)

        self.DoExchange = QtWidgets.QCheckBox('Exchange (perform 2-way conversion)')

        # Swap layout
        swapLayout = QtWidgets.QGridLayout()

        swapLayout.addWidget(QtWidgets.QLabel('From Object:'), 0, 0)
        swapLayout.addWidget(self.FromType, 0, 1)

        swapLayout.addWidget(QtWidgets.QLabel('From Tileset:'), 1, 0)
        swapLayout.addWidget(self.FromTileset, 1, 1)

        swapLayout.addWidget(QtWidgets.QLabel('To Object:'), 0, 2)
        swapLayout.addWidget(self.ToType, 0, 3)

        swapLayout.addWidget(QtWidgets.QLabel('To Tileset:'), 1, 2)
        swapLayout.addWidget(self.ToTileset, 1, 3)

        # Buttonbox
        self.buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Apply | QtWidgets.QDialogButtonBox.Close)
        self.buttons.clicked.connect(self.button_clicked)

        # Main layout
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(swapLayout)
        mainLayout.addWidget(self.DoExchange)
        mainLayout.addWidget(self.buttons)
        self.setLayout(mainLayout)

    def button_clicked(self, button):
        """
        Handles one of the buttons being pressed and calls the correct handler.
        """
        role = self.buttons.buttonRole(button)

        if role == QtWidgets.QDialogButtonBox.RejectRole:
            # The close button was pressed
            self.reject()
        elif role == QtWidgets.QDialogButtonBox.ApplyRole:
            # The apply button was pressed
            self.swap_tiles()
        else:
            raise ValueError("ObjectTypeSwapDialog: Unknown role on pressed button. " + repr(role))

    def swap_tiles(self):
        """
        Actually does the swapping
        """
        from_type = self.FromType.value()
        from_tileset = self.FromTileset.value() - 1
        to_type = self.ToType.value()
        to_tileset = self.ToTileset.value() - 1
        do_exchange = self.DoExchange.isChecked()

        # If we don't need to do anything, don't do anything.
        if from_type == to_type and from_tileset == to_tileset:
            return

        for layer in globals_.Area.layers:
            for nsmbobj in layer:
                if nsmbobj.type == from_type and nsmbobj.tileset == from_tileset:
                    nsmbobj.SetType(to_tileset, to_type)
                    SetDirty()
                elif do_exchange and nsmbobj.type == to_type and nsmbobj.tileset == to_tileset:
                    nsmbobj.SetType(from_tileset, from_type)
                    SetDirty()