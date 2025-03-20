"""
zone_dialog.py

A refactored Zones dialog for the main editor.
This module defines:
  - ZonesDialog: a dialog with tabs for each zone.
  - ZoneTab: a widget for editing a single zone’s properties.
  - CameraModeZoomSettingsLayout: a custom layout for camera mode and zoom settings.

Dependencies:
  - PyQt5
  - common, globals_, ui, and levelitems
"""

from PyQt5 import QtWidgets, QtCore
from typing import List, Optional

import common
import globals_
from gui.components.combo_box import ReggieComboBox
from ui import GetIcon
from levelitems import ZoneItem  # assumed to have properties like id, objx, objy, width, height, etc.


class ZonesDialog(QtWidgets.QDialog):
    """
    A dialog that lets you choose and manage zone tabs.
    """

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(globals_.trans.string('ZonesDlg', 0))
        self.setWindowIcon(GetIcon('zones'))

        self.tab_widget = QtWidgets.QTabWidget(self)
        self.zone_tabs: List[ZoneTab] = []

        # Assume globals_.Area.zones is a list of ZoneItem objects.
        num_zones = len(globals_.Area.zones)
        for z in globals_.Area.zones:
            if num_zones <= 5:
                zone_tab_name = globals_.trans.string('ZonesDlg', 3, '[num]', z.id + 1)
            else:
                zone_tab_name = str(z.id + 1)
            tab = ZoneTab(z)
            self.zone_tabs.append(tab)
            self.tab_widget.addTab(tab, zone_tab_name)

        self.new_button = QtWidgets.QPushButton(globals_.trans.string('ZonesDlg', 4))
        self.delete_button = QtWidgets.QPushButton(globals_.trans.string('ZonesDlg', 5))

        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        button_box.addButton(self.new_button, QtWidgets.QDialogButtonBox.ActionRole)
        button_box.addButton(self.delete_button, QtWidgets.QDialogButtonBox.ActionRole)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.new_button.clicked.connect(self.new_zone)
        self.delete_button.clicked.connect(self.delete_zone)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.tab_widget)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

    def new_zone(self) -> None:
        """
        Create a new zone.
        If there are already six zones, ask for confirmation.
        """
        if len(self.zone_tabs) >= 6:
            result = QtWidgets.QMessageBox.warning(
                self,
                globals_.trans.string('ZonesDlg', 6),
                globals_.trans.string('ZonesDlg', 7),
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if result == QtWidgets.QMessageBox.No:
                return

        # Create a new zone via the main window.
        new_zone_obj = globals_.mainWindow.CreateZone(256, 256)
        if len(self.zone_tabs) + 1 <= 5:
            zone_tab_name = globals_.trans.string('ZonesDlg', 3, '[num]', new_zone_obj.id + 1)
        else:
            zone_tab_name = str(new_zone_obj.id + 1)

        tab = ZoneTab(new_zone_obj)
        self.zone_tabs.append(tab)
        self.tab_widget.addTab(tab, zone_tab_name)
        self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)

        # Relabel tabs if the number of zones has reached six.
        if self.tab_widget.count() == 6:
            for idx in range(self.tab_widget.count() - 1):
                widget = self.tab_widget.widget(idx)
                if widget:
                    self.tab_widget.setTabText(idx, str(widget.zone_obj.id + 1))

    def delete_zone(self) -> None:
        """
        Delete the currently selected zone tab.
        """
        index = self.tab_widget.currentIndex()
        if self.tab_widget.count() == 0:
            return

        self.tab_widget.removeTab(index)
        self.zone_tabs.pop(index)

        # If the number of tabs drops to five, relabel using long names.
        if self.tab_widget.count() == 5:
            for idx in range(self.tab_widget.count()):
                widget = self.tab_widget.widget(idx)
                if widget:
                    self.tab_widget.setTabText(
                        idx, globals_.trans.string('ZonesDlg', 3, '[num]', widget.zone_obj.id + 1)
                    )


class ZoneTab(QtWidgets.QWidget):
    """
    A tab widget for editing a single zone's properties.
    """

    def __init__(self, z: ZoneItem, parent: Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)
        self.zone_obj = z
        self.auto_changing_size = False

        # Create UI sections.
        self.create_dimensions(z)
        self.create_rendering(z)
        self.create_audio(z)
        self.create_camera(z)
        self.create_bounds(z)

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(self.dimensions_group)
        left_layout.addWidget(self.rendering_group)
        left_layout.addWidget(self.audio_group)

        right_layout = QtWidgets.QVBoxLayout()
        right_layout.addWidget(self.camera_group)
        right_layout.addWidget(self.bounds_group)

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

    def create_dimensions(self, z: ZoneItem) -> None:
        """Creates the dimensions section."""
        self.dimensions_group = QtWidgets.QGroupBox(globals_.trans.string('ZonesDlg', 8))

        self.zone_xpos = QtWidgets.QSpinBox()
        self.zone_xpos.setRange(16, 65535)
        self.zone_xpos.setToolTip(globals_.trans.string('ZonesDlg', 10))
        self.zone_xpos.setValue(z.objx)

        self.zone_ypos = QtWidgets.QSpinBox()
        self.zone_ypos.setRange(16, 65535)
        self.zone_ypos.setToolTip(globals_.trans.string('ZonesDlg', 12))
        self.zone_ypos.setValue(z.objy)

        self.snap_button_8 = QtWidgets.QPushButton(globals_.trans.string('ZonesDlg', 76))
        self.snap_button_8.clicked.connect(lambda: self.handle_snap_to_grid(grid_size=8))

        self.snap_button_16 = QtWidgets.QPushButton(globals_.trans.string('ZonesDlg', 77))
        self.snap_button_16.clicked.connect(lambda: self.handle_snap_to_grid(grid_size=16))

        self.zone_width = QtWidgets.QSpinBox()
        self.zone_width.setRange(204, 65535)
        self.zone_width.setToolTip(globals_.trans.string('ZonesDlg', 14))
        self.zone_width.setValue(z.width)
        self.zone_width.valueChanged.connect(self.preset_deselected)

        self.zone_height = QtWidgets.QSpinBox()
        self.zone_height.setRange(112, 65535)
        self.zone_height.setToolTip(globals_.trans.string('ZonesDlg', 16))
        self.zone_height.setValue(z.height)
        self.zone_height.valueChanged.connect(self.preset_deselected)

        self.zone_presets_values = (
            '204x112', '308x168', '408x224', '468x256', '496x272',
            '556x304', '584x320', '700x384', '816x448'
        )
        self.zone_presets = QtWidgets.QComboBox()
        self.zone_presets.addItems(self.zone_presets_values)
        self.zone_presets.setToolTip(globals_.trans.string('ZonesDlg', 18))
        self.zone_presets.currentIndexChanged.connect(self.preset_selected)
        self.preset_deselected()  # initialize preset state

        position_layout = QtWidgets.QFormLayout()
        position_layout.addRow(globals_.trans.string('ZonesDlg', 9), self.zone_xpos)
        position_layout.addRow(globals_.trans.string('ZonesDlg', 11), self.zone_ypos)

        size_layout = QtWidgets.QFormLayout()
        size_layout.addRow(globals_.trans.string('ZonesDlg', 13), self.zone_width)
        size_layout.addRow(globals_.trans.string('ZonesDlg', 15), self.zone_height)
        size_layout.addRow(globals_.trans.string('ZonesDlg', 17), self.zone_presets)

        snap_layout = QtWidgets.QHBoxLayout()
        snap_layout.addWidget(self.snap_button_8)
        snap_layout.addWidget(self.snap_button_16)

        inner_layout = QtWidgets.QHBoxLayout()
        inner_layout.addLayout(position_layout)
        inner_layout.addLayout(size_layout)

        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.addLayout(inner_layout)
        vertical_layout.addLayout(snap_layout)

        self.dimensions_group.setLayout(vertical_layout)

    def handle_snap_to_grid(self, grid_size: int) -> None:
        """
        Snaps the zone's dimensions to the nearest multiple of grid_size.
        """
        left = self.zone_xpos.value()
        top = self.zone_ypos.value()
        width = self.zone_width.value()
        height = self.zone_height.value()
        right = left + width
        bottom = top + height

        # Snap each coordinate using a helper.
        left = self._snap_value(left, grid_size)
        top = self._snap_value(top, grid_size)
        right = self._snap_value(right, grid_size)
        bottom = self._snap_value(bottom, grid_size)

        if right <= left:
            right = left + grid_size
        if bottom <= top:
            bottom = top + grid_size

        new_width = right - left
        new_height = bottom - top

        # Enforce minimum constraints.
        left = max(left, 16)
        top = max(top, 16)
        new_width = max(new_width, 304 if grid_size == 8 else 304)
        new_height = max(new_height, 200 if grid_size == 8 else 208)

        # Enforce maximum constraints.
        left = min(left, 65535 - grid_size)
        top = min(top, 65535 - grid_size)
        new_width = min(new_width, 65535 - left)
        new_height = min(new_height, 65535 - top)

        self.zone_xpos.setValue(left)
        self.zone_ypos.setValue(top)
        self.zone_width.setValue(new_width)
        self.zone_height.setValue(new_height)

    @staticmethod
    def _snap_value(value: int, grid_size: int) -> int:
        remainder = value % grid_size
        return value - remainder if remainder < grid_size / 2 else value + (grid_size - remainder)

    def preset_selected(self, index: int) -> None:
        """Handles a zone preset being selected."""
        if self.auto_changing_size:
            return
        if self.zone_presets.currentText() == globals_.trans.string('ZonesDlg', 60):
            return
        try:
            w, h = self.zone_presets.currentText().split('x')
        except ValueError:
            return
        self.auto_changing_size = True
        self.zone_width.setValue(int(w))
        self.zone_height.setValue(int(h))
        self.auto_changing_size = False
        if self.zone_presets.itemText(0) == globals_.trans.string('ZonesDlg', 60):
            self.zone_presets.removeItem(0)

    def preset_deselected(self) -> None:
        """Handles custom size input by the user."""
        if self.auto_changing_size:
            return
        self.auto_changing_size = True
        w = self.zone_width.value()
        h = self.zone_height.value()
        check = f"{w}x{h}"
        custom_size_name = globals_.trans.string('ZonesDlg', 60)
        try:
            idx = self.zone_presets_values.index(check)
        except ValueError:
            idx = -1
        if idx == -1:
            if self.zone_presets.itemText(0) != custom_size_name:
                self.zone_presets.insertItem(0, custom_size_name)
            idx = 0
        elif self.zone_presets.itemText(0) == custom_size_name:
            self.zone_presets.removeItem(0)
        self.zone_presets.setCurrentIndex(idx)
        self.auto_changing_size = False

    def create_rendering(self, z: ZoneItem) -> None:
        """Creates the rendering settings section."""
        self.rendering_group = QtWidgets.QGroupBox('Rendering')
        combobox_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed
        )

        zone_theme_values = globals_.ZoneThemeValues
        terrain_theme_values = globals_.trans.stringList('ZonesDlg', 2)

        self.zone_modeldark = QtWidgets.QComboBox()
        self.zone_modeldark.addItems(zone_theme_values)
        self.zone_modeldark.setToolTip(globals_.trans.string('ZonesDlg', 21))
        self.zone_modeldark.setSizePolicy(combobox_policy)
        z.modeldark = common.clamp(z.modeldark, 0, len(zone_theme_values))
        self.zone_modeldark.setCurrentIndex(z.modeldark)

        self.zone_terraindark = QtWidgets.QComboBox()
        self.zone_terraindark.addItems(terrain_theme_values)
        self.zone_terraindark.setToolTip(globals_.trans.string('ZonesDlg', 23))
        self.zone_terraindark.setSizePolicy(combobox_policy)
        z.terraindark = common.clamp(z.terraindark, 0, len(terrain_theme_values))
        self.zone_terraindark.setCurrentIndex(z.terraindark)

        self.zone_vspotlight = QtWidgets.QCheckBox(globals_.trans.string('ZonesDlg', 26))
        self.zone_vspotlight.setToolTip(globals_.trans.string('ZonesDlg', 27))
        self.zone_vfulldark = QtWidgets.QCheckBox(globals_.trans.string('ZonesDlg', 28))
        self.zone_vfulldark.setToolTip(globals_.trans.string('ZonesDlg', 29))

        self.zone_visibility = QtWidgets.QComboBox()
        self.zv = z.visibility
        self.zone_vspotlight.setChecked(bool(self.zv & 0x10))
        self.zone_vfulldark.setChecked(bool(self.zv & 0x20))

        self.change_visibility_list()
        self.zone_vspotlight.clicked.connect(self.change_visibility_list)
        self.zone_vfulldark.clicked.connect(self.change_visibility_list)

        rendering_layout = QtWidgets.QFormLayout()
        rendering_layout.addRow(globals_.trans.string('ZonesDlg', 20), self.zone_modeldark)
        rendering_layout.addRow(globals_.trans.string('ZonesDlg', 22), self.zone_terraindark)

        visibility_layout = QtWidgets.QHBoxLayout()
        visibility_layout.addWidget(self.zone_vspotlight)
        visibility_layout.addWidget(self.zone_vfulldark)

        inner_layout = QtWidgets.QVBoxLayout()
        inner_layout.addLayout(rendering_layout)
        inner_layout.addLayout(visibility_layout)
        inner_layout.addWidget(self.zone_visibility)
        self.rendering_group.setLayout(inner_layout)

    def change_visibility_list(self) -> None:
        """
        Updates the visibility list based on spotlight and fulldark settings.
        """
        if self.zone_vfulldark.isChecked():
            add_idx = 82 if self.zone_vspotlight.isChecked() else 45
        else:
            add_idx = 43 if self.zone_vspotlight.isChecked() else 41

        add_list = globals_.trans.stringList('ZonesDlg', add_idx)
        self.zone_visibility.clear()
        self.zone_visibility.addItems(add_list)
        self.zone_visibility.setToolTip(globals_.trans.string('ZonesDlg', add_idx + 1))
        choice = min(self.zv & 0xF, len(add_list) - 1)
        self.zone_visibility.setCurrentIndex(choice)

    def create_camera(self, z: ZoneItem) -> None:
        """Creates the camera settings section."""
        self.camera_group = QtWidgets.QGroupBox(globals_.trans.string('ZonesDlg', 19))
        combobox_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed
        )

        self.zone_cammodezoom = CameraModeZoomSettingsLayout(show_mode_5=True)
        self.zone_cammodezoom.set_values(z.cammode, z.camzoom)

        dirs = globals_.trans.stringList('ZonesDlg', 38)
        self.zone_direction = QtWidgets.QComboBox()
        self.zone_direction.addItems(dirs)
        self.zone_direction.setToolTip(globals_.trans.string('ZonesDlg', 40))
        self.zone_direction.setSizePolicy(combobox_policy)
        z.camtrack = common.clamp(z.camtrack, 0, len(dirs) - 1)
        self.zone_direction.setCurrentIndex(z.camtrack)

        self.zone_yrestrict = QtWidgets.QCheckBox()
        self.zone_yrestrict.setToolTip(globals_.trans.string('ZonesDlg', 78))
        self.zone_yrestrict.setChecked(z.mpcamzoomadjust != 15)
        self.zone_yrestrict.stateChanged.connect(self.change_mp_zoom_adjust)

        self.zone_mpzoomadjust = QtWidgets.QSpinBox()
        self.zone_mpzoomadjust.setRange(0, 14)
        self.zone_mpzoomadjust.setToolTip(globals_.trans.string('ZonesDlg', 79))
        self.change_mp_zoom_adjust()
        if z.mpcamzoomadjust < 15:
            self.zone_mpzoomadjust.setValue(z.mpcamzoomadjust)

        camera_layout = QtWidgets.QFormLayout()
        camera_layout.addRow(self.zone_cammodezoom)
        camera_layout.addRow(globals_.trans.string('ZonesDlg', 39), self.zone_direction)
        camera_layout.addRow(globals_.trans.string('ZonesDlg', 80), self.zone_yrestrict)
        camera_layout.addRow(globals_.trans.string('ZonesDlg', 81), self.zone_mpzoomadjust)
        self.camera_group.setLayout(camera_layout)

    def change_mp_zoom_adjust(self) -> None:
        self.zone_mpzoomadjust.setEnabled(self.zone_yrestrict.isChecked())
        self.zone_mpzoomadjust.setValue(0)

    def create_bounds(self, z: ZoneItem) -> None:
        """Creates the bounds settings section."""
        self.bounds_group = QtWidgets.QGroupBox(globals_.trans.string('ZonesDlg', 47))

        self.zone_yboundup = QtWidgets.QSpinBox()
        self.zone_yboundup.setRange(-32768, 32767)
        self.zone_yboundup.setToolTip(globals_.trans.string('ZonesDlg', 49))
        self.zone_yboundup.setSpecialValueText('32')
        self.zone_yboundup.setValue(z.yupperbound)

        self.zone_ybounddown = QtWidgets.QSpinBox()
        self.zone_ybounddown.setRange(-32768, 32767)
        self.zone_ybounddown.setToolTip(globals_.trans.string('ZonesDlg', 51))
        self.zone_ybounddown.setValue(z.ylowerbound)

        self.zone_yboundup2 = QtWidgets.QSpinBox()
        self.zone_yboundup2.setRange(-32768, 32767)
        self.zone_yboundup2.setToolTip(globals_.trans.string('ZonesDlg', 71))
        self.zone_yboundup2.setValue(z.yupperbound2)

        self.zone_ybounddown2 = QtWidgets.QSpinBox()
        self.zone_ybounddown2.setRange(-32768, 32767)
        self.zone_ybounddown2.setToolTip(globals_.trans.string('ZonesDlg', 73))
        self.zone_ybounddown2.setValue(z.ylowerbound2)

        self.zone_yboundup3 = QtWidgets.QSpinBox()
        self.zone_yboundup3.setRange(-32768, 32767)
        self.zone_yboundup3.setToolTip(
            "<b>Multiplayer Upper Bounds Adjust:</b><br>Added to the upper bounds during multiplayer mode."
        )
        self.zone_yboundup3.setSpecialValueText('32')
        self.zone_yboundup3.setValue(z.yupperbound3)

        self.zone_ybounddown3 = QtWidgets.QSpinBox()
        self.zone_ybounddown3.setRange(-32768, 32767)
        self.zone_ybounddown3.setToolTip(
            "<b>Multiplayer Lower Bounds Adjust:</b><br>Added to the lower bounds during multiplayer mode."
        )
        self.zone_ybounddown3.setValue(z.ylowerbound3)

        layout_a = QtWidgets.QFormLayout()
        layout_a.addRow(globals_.trans.string('ZonesDlg', 48), self.zone_yboundup)
        layout_a.addRow(globals_.trans.string('ZonesDlg', 50), self.zone_ybounddown)

        layout_b = QtWidgets.QFormLayout()
        layout_b.addRow(globals_.trans.string('ZonesDlg', 70), self.zone_yboundup2)
        layout_b.addRow(globals_.trans.string('ZonesDlg', 72), self.zone_ybounddown2)

        horizontal_layout = QtWidgets.QHBoxLayout()
        horizontal_layout.addLayout(layout_a)
        horizontal_layout.addLayout(layout_b)

        layout_c = QtWidgets.QFormLayout()
        layout_c.addRow(horizontal_layout)
        layout_c.addRow('Multiplayer Upper Bounds Adjust:', self.zone_yboundup3)
        layout_c.addRow('Multiplayer Lower Bounds Adjust:', self.zone_ybounddown3)

        self.bounds_group.setLayout(layout_c)

    def create_audio(self, z: ZoneItem) -> None:
        self.audio_group = QtWidgets.QGroupBox(globals_.trans.string('ZonesDlg', 52))
        self.auto_edit_music = False

        # Hopefully fixes this annoying error where the
        # combo box exceeds the window.
        self.zone_music = ReggieComboBox()
        self.zone_music.setToolTip(globals_.trans.string('ZonesDlg', 54))

        # Fill the combo box
        for songid, text in globals_.MusicInfo:
            self.zone_music.addItem(text, songid)

        index = self.zone_music.findData(z.music)
        if index < 0:
            index = 0
        self.zone_music.setCurrentIndex(index)
        self.zone_music.currentIndexChanged.connect(self.handle_music_list_select)

        self.zone_musicid = QtWidgets.QSpinBox()
        self.zone_musicid.setToolTip(globals_.trans.string('ZonesDlg', 69))
        self.zone_musicid.setMaximum(255)
        self.zone_musicid.setValue(z.music)
        self.zone_musicid.valueChanged.connect(self.handle_music_id_change)

        self.zone_sfx = QtWidgets.QComboBox()
        self.zone_sfx.setToolTip(globals_.trans.string('ZonesDlg', 56))
        sfx_items = globals_.trans.stringList('ZonesDlg', 57)
        self.zone_sfx.addItems(sfx_items)
        self.zone_sfx.setCurrentIndex(z.sfxmod // 16)

        self.zone_boss = QtWidgets.QCheckBox()
        self.zone_boss.setToolTip(globals_.trans.string('ZonesDlg', 59))
        self.zone_boss.setChecked(bool(z.sfxmod % 16))

        layout = QtWidgets.QFormLayout()
        layout.addRow(globals_.trans.string('ZonesDlg', 53), self.zone_music)
        layout.addRow(globals_.trans.string('ZonesDlg', 68), self.zone_musicid)
        layout.addRow(globals_.trans.string('ZonesDlg', 55), self.zone_sfx)
        layout.addRow(globals_.trans.string('ZonesDlg', 58), self.zone_boss)

        self.audio_group.setLayout(layout)

    def handle_music_list_select(self) -> None:
        """
        Synchronizes music list selection with the music ID spinbox.
        """
        if self.auto_edit_music:
            return
        song_id = self.zone_music.itemData(self.zone_music.currentIndex())
        try:
            song_id = int(str(song_id))
        except Exception:
            song_id = 0
        self.auto_edit_music = True
        self.zone_musicid.setValue(song_id)
        self.auto_edit_music = False

    def handle_music_id_change(self) -> None:
        """
        Synchronizes music ID spinbox with the music list selection.
        """
        if self.auto_edit_music:
            return
        song_id = self.zone_musicid.value()
        self.auto_edit_music = True
        index = self.zone_music.findData(song_id)
        self.zone_music.setCurrentIndex(index)
        self.auto_edit_music = False


class CameraModeZoomSettingsLayout(QtWidgets.QFormLayout):
    """
    A custom layout for camera mode/zoom settings.
    Emits 'edited' when a setting is changed.
    """
    edited = QtCore.pyqtSignal()

    def __init__(self, show_mode_5: bool) -> None:
        super().__init__()
        self.updating = True
        self.zm: int = -1

        combobox_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed
        )
        self.mode_button_group = QtWidgets.QButtonGroup()
        mode_buttons = []

        modes = [
            (0, 'Normal', 'The standard camera mode, appropriate for most situations.'),
            (3, 'Static Zoom', 'Camera will not zoom out during multiplayer.'),
            (4, 'Static Zoom, Y Tracking Only', 'Camera does not zoom out and is centered horizontally.'),
            (5, 'Static Zoom, Event-Controlled', 'Camera does not zoom out and uses event-controlled settings.'),
            (6, 'X Tracking Only', 'Camera moves only horizontally.'),
            (7, 'X Expanding Only', 'Camera zooms out in multiplayer only if players are far apart horizontally.'),
            (1, 'Y Tracking Only', 'Camera moves only vertically and is centered horizontally.'),
            (2, 'Y Expanding Only', 'Camera zooms out in multiplayer if players are far apart vertically.')
        ]

        for i, name, tooltip in modes:
            rb = QtWidgets.QRadioButton(name)
            rb.setToolTip(f"<b>{name}:</b><br>{tooltip}")
            self.mode_button_group.addButton(rb, i)
            mode_buttons.append(rb)
            if i == 5 and not show_mode_5:
                rb.setVisible(False)
            rb.clicked.connect(self.change_cam_mode_list)
            rb.clicked.connect(self.handle_mode_changed)

        self.screen_sizes = QtWidgets.QComboBox()
        self.screen_sizes.setToolTip(
            "<b>Screen Heights:</b><br>Selects screen heights (in blocks) for multiplayer zoom-out. "
            "In single-player, only the smallest height is used. Options marked with * or ** may be glitchy."
        )
        self.screen_sizes.setSizePolicy(combobox_policy)
        self.screen_sizes.currentIndexChanged.connect(self.handle_screen_sizes_changed)

        modes_layout = QtWidgets.QGridLayout()
        for idx, btn in enumerate(mode_buttons):
            modes_layout.addWidget(btn, idx % 4, idx // 4)

        self.addRow(modes_layout)
        self.addRow('Screen Heights:', self.screen_sizes)
        self.updating = False

    def change_cam_mode_list(self) -> None:
        """
        Updates the screen sizes based on the selected camera mode.
        """
        mode = self.mode_button_group.checkedId()
        if self.zm != -1:
            old_choice = [1, 1, 2, 3, 3, 3, 1, 1][self.zm]
            new_choice = [1, 1, 2, 3, 3, 3, 1, 1][mode]
            if old_choice == new_choice:
                return
        else:
            new_choice = [1, 1, 2, 3, 3, 3, 1, 1][mode]

        if new_choice == 1:
            sizes = [
                ([14, 19], ''),
                ([14, 19, 24], ''),
                ([14, 19, 28], ''),
                ([20, 24], ''),
                ([19, 24, 28], ''),
                ([17, 24], ''),
                ([17, 24, 28], ''),
                ([17, 20], ''),
                ([7, 11, 28], '**'),
                ([17, 20.5, 24], ''),
                ([17, 20, 28], '')
            ]
        elif new_choice == 2:
            sizes = [
                ([14, 19], ''),
                ([14, 19, 24], ''),
                ([14, 19, 28], ''),
                ([19, 19, 24], ''),
                ([19, 24, 28], ''),
                ([19, 24, 28], ''),
                ([17, 24, 28], ''),
                ([17, 20.5, 24], '')
            ]
        else:
            sizes = [
                ([14], ''),
                ([19], ''),
                ([24], ''),
                ([28], ''),
                ([17], ''),
                ([20], ''),
                ([16], ''),
                ([28], ''),
                ([7], '*'),
                ([10.5], '*')
            ]
        items = [", ".join(str(o) for o in opts) + asterisk for opts, asterisk in sizes]
        self.screen_sizes.clear()
        self.screen_sizes.addItems(items)
        self.screen_sizes.setCurrentIndex(0)
        self.zm = mode

    def set_values(self, cammode: int, camzoom: int) -> None:
        """Sets the camera mode and zoom values."""
        self.updating = True
        if cammode < 0:
            cammode = 0
        if cammode >= 8:
            cammode = 7
        self.mode_button_group.button(cammode).setChecked(True)
        self.change_cam_mode_list()
        if camzoom < 0:
            camzoom = 0
        if camzoom >= self.screen_sizes.count():
            camzoom = self.screen_sizes.count() - 1
        self.screen_sizes.setCurrentIndex(camzoom)
        self.updating = False

    def handle_mode_changed(self) -> None:
        if self.updating:
            return
        self.change_cam_mode_list()
        self.edited.emit()

    def handle_screen_sizes_changed(self) -> None:
        if self.updating:
            return
        self.edited.emit()
