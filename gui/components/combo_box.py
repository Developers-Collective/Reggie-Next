from PyQt5 import QtWidgets

DEFAULT_MAX_HEIGHT_HINT = 300
DEFAULT_HEIGHT_HINT = 300


class ReggieComboBox(QtWidgets.QComboBox):
    def __init__(self, preferred_height: int = DEFAULT_HEIGHT_HINT, max_height: int = DEFAULT_MAX_HEIGHT_HINT) -> None:
        super().__init__()
        self._preferred_height = preferred_height
        self._max_height = max_height

    def showPopup(self):
        super().showPopup()
        # After the popup is shown, we can access the popup widget:
        popup = self.view().parentWidget()

        if not popup:
            return

        # Hide the popup until resized and relocated properly
        # If we do not do that, you can see for a brief moment
        # a flicker, so the resizing/relocating of the box. To
        # prevent showing that, we hide the popup until everything
        # is finished.

        popup.hide()
        super().hidePopup()

        # Force a max height
        popup.setMaximumHeight(self._max_height)

        # Force the popup geometry to appear under the combo box
        # (By default, Qt tries to position it, but since we override showPopup(),
        # we need to do it ourselves.)
        combo_rect = self.rect()
        global_bottom_left = self.mapToGlobal(combo_rect.bottomLeft())

        # Evaluate how big the popup *wants* to be
        size_hint = popup.sizeHint()
        desired_width = max(self.width(), size_hint.width())
        desired_height = self._preferred_height

        # Place the popup so that its top-left corner is at the combo box's bottom-left
        popup.setGeometry(
            global_bottom_left.x(),
            global_bottom_left.y(),
            desired_width,
            desired_height
        )

        popup.show()
