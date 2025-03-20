from PyQt5 import QtWidgets, QtGui

import globals_
import spritelib as SLib

from dirty import SetDirty
from raw_data import RawData
from ui import GetIcon


class DiagnosticToolDialog(QtWidgets.QDialog):
    """
    Dialog which checks for errors within the level
    """

    def __init__(self):
        """
        Creates and initializes the dialog
        """
        QtWidgets.QDialog.__init__(self)
        self.setWindowTitle(globals_.trans.string('Diag', 0))
        self.setWindowIcon(GetIcon('diagnostics'))

        # CheckFunctions: (icon, description, function, iscritical)
        self.CheckFunctions = (('objects', globals_.trans.string('Diag', 2), self.ObjsInTileset, True),
                               ('sprites', globals_.trans.string('Diag', 3), self.CrashSprites, False),
                               ('sprites', globals_.trans.string('Diag', 4), self.CrashSpriteSettings, True),
                               ('sprites', globals_.trans.string('Diag', 5), self.TooManySprites, False),
                               ('entrances', globals_.trans.string('Diag', 6), self.DuplicateEntranceIDs, True),
                               ('entrances', globals_.trans.string('Diag', 7), self.NoStartEntrance, True),
                               ('entrances', globals_.trans.string('Diag', 8), self.EntranceTooCloseToZoneEdge, False),
                               ('entrances', globals_.trans.string('Diag', 9), self.EntranceOutsideOfZone, False),
                               ('zones', globals_.trans.string('Diag', 10), self.TooManyZones, True),
                               ('zones', globals_.trans.string('Diag', 11), self.NoZones, True),
                               ('zones', globals_.trans.string('Diag', 12), self.ZonesTooClose, True),
                               ('zones', globals_.trans.string('Diag', 13), self.ZonesTooCloseToAreaEdges, True),
                               ('zones', globals_.trans.string('Diag', 14), self.BiasNotEnabled, False),
                               ('zones', globals_.trans.string('Diag', 15), self.ZonesTooBig, True),
                               )

        box = QtWidgets.QGroupBox(globals_.trans.string('Diag', 17))
        self.errorLayout = QtWidgets.QVBoxLayout()
        result, numErrors = self.populateLists()
        box.setLayout(self.errorLayout)

        self.updateHeader(result)
        hW = QtWidgets.QWidget()
        hW.setLayout(self.header)

        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(hW)
        self.mainLayout.addWidget(box)
        self.mainLayout.addWidget(self.buttonBox)
        self.setLayout(self.mainLayout)

    def updateHeader(self, testresult, secondTime=False):
        """
        Creates the header
        """
        self.header = QtWidgets.QGridLayout()
        self.header.addWidget(QtWidgets.QLabel(globals_.trans.string('Diag', 18)), 0, 0, 1, 3)

        pointsize = 14  # change this if you don't like it
        if testresult is None:  # good
            L = QtWidgets.QLabel()
            L.setPixmap(GetIcon('check', True).pixmap(64, 64))
            self.header.addWidget(L, 1, 0)

            px = QtGui.QPixmap(64, pointsize)
            px.fill(QtGui.QColor(0, 0, 0, 0))
            p = QtGui.QPainter(px)
            f = p.font()
            f.setPointSize(pointsize)
            p.setFont(f)
            p.setPen(QtGui.QColor(0, 200, 0))
            p.drawText(0, pointsize, globals_.trans.string('Diag', 19))
            del p
            L = QtWidgets.QLabel()
            L.setPixmap(px)
            self.header.addWidget(L, 1, 1)

            self.header.addWidget(QtWidgets.QLabel(globals_.trans.string('Diag', 20)), 1, 2)
        elif not testresult:  # warnings
            L = QtWidgets.QLabel()
            L.setPixmap(GetIcon('warning', True).pixmap(64, 64))
            self.header.addWidget(L, 1, 0)

            px = QtGui.QPixmap(128, int(pointsize * 3 / 2))
            px.fill(QtGui.QColor(0, 0, 0, 0))
            p = QtGui.QPainter(px)
            f = p.font()
            f.setPointSize(pointsize)
            p.setFont(f)
            p.setPen(QtGui.QColor(210, 210, 0))
            p.drawText(0, pointsize, globals_.trans.string('Diag', 21))
            del p
            L = QtWidgets.QLabel()
            L.setPixmap(px)
            self.header.addWidget(L, 1, 1)

            self.header.addWidget(QtWidgets.QLabel(globals_.trans.string('Diag', 22)), 1, 2)
        else:  # bad
            L = QtWidgets.QLabel()
            L.setPixmap(GetIcon('delete', True).pixmap(64, 64))
            self.header.addWidget(L, 1, 0)

            px = QtGui.QPixmap(72, pointsize)
            px.fill(QtGui.QColor(0, 0, 0, 0))
            p = QtGui.QPainter(px)
            f = p.font()
            f.setPointSize(pointsize)
            p.setFont(f)
            p.setPen(QtGui.QColor(255, 0, 0))
            p.drawText(0, pointsize, globals_.trans.string('Diag', 23))
            del p
            L = QtWidgets.QLabel()
            L.setPixmap(px)
            self.header.addWidget(L, 1, 1)

            self.header.addWidget(QtWidgets.QLabel(globals_.trans.string('Diag', 24)), 1, 2)

        if secondTime:
            w = QtWidgets.QWidget()
            w.setLayout(self.header)
            self.mainLayout.takeAt(0).widget().hide()
            self.mainLayout.insertWidget(0, w)

    def populateLists(self):
        """
        Runs the check functions and adds items to the list if needed
        """
        self.buttonHandlers = []

        self.errorList = QtWidgets.QListWidget()
        self.errorList.setSelectionMode(self.errorList.MultiSelection)

        foundAnything = False
        foundCritical = False
        for ico, desc, fxn, isCritical in self.CheckFunctions:
            if fxn('c'):

                foundAnything = True
                if isCritical: foundCritical = True

                item = QtWidgets.QListWidgetItem()
                item.setText(desc)
                if isCritical:
                    item.setForeground(QtGui.QColor(255, 0, 0))
                else:
                    item.setForeground(QtGui.QColor(172, 172, 0))
                item.setIcon(GetIcon(ico))
                item.fix = fxn

                self.errorList.addItem(item)

        self.fixBtn = QtWidgets.QPushButton(globals_.trans.string('Diag', 25))
        self.fixBtn.setToolTip(globals_.trans.string('Diag', 26))
        self.fixBtn.clicked.connect(self.FixSelected)
        if not foundAnything: self.fixBtn.setEnabled(False)

        self.errorLayout.addWidget(self.errorList)
        self.errorLayout.addWidget(self.fixBtn)

        if foundCritical:
            return True, len(self.buttonHandlers)
        elif foundAnything:
            return False, len(self.buttonHandlers)
        return None, len(self.buttonHandlers)

    def FixSelected(self):
        """
        Fixes the selected items
        """

        # Ask the user to make sure
        btn = QtWidgets.QMessageBox.warning(None, globals_.trans.string('Diag', 27), globals_.trans.string('Diag', 28),
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if btn != QtWidgets.QMessageBox.Yes: return

        # Show the 'Fixing...' box while fixing
        pleasewait = QtWidgets.QProgressDialog()
        pleasewait.setLabelText(globals_.trans.string('Diag', 29))  # Fixing...
        pleasewait.setMinimum(0)
        pleasewait.setMaximum(100)
        pleasewait.setAutoClose(True)
        pleasewait.open()
        pleasewait.show()
        pleasewait.setValue(0)

        # Fix them
        for index, item in enumerate(self.errorList.selectedIndexes()[:]):
            listItem = self.errorList.itemFromIndex(item)
            try:
                listItem.fix()
                SetDirty()
            except Exception:
                pass  # fail silently
            self.errorList.takeItem(item.row())

            total = len(self.errorList.selectedIndexes())
            if total != 0: pleasewait.setValue(int(index / total * 100))

        # Remove the 'Fixing...' box
        pleasewait.setValue(100)
        del pleasewait

        # Gray out the Fix button if there are no more problems
        if self.errorList.count() == 0: self.fixBtn.setEnabled(False)

    def ObjsInTileset(self, mode='f'):
        """
        Checks for any objects which cannot be found in the tilesets
        """
        deletions = []
        for layer in globals_.Area.layers:
            for obj in layer:

                if globals_.ObjectDefinitions[obj.tileset] is None:
                    deletions.append(obj)
                elif globals_.ObjectDefinitions[obj.tileset][obj.type] is None:
                    deletions.append(obj)

        has_problem = bool(deletions)
        if mode == 'c':
            return has_problem

        if not has_problem: return

        for obj in deletions:
            obj.delete()
            obj.setSelected(False)
            globals_.mainWindow.scene.removeItem(obj)

        globals_.mainWindow.levelOverview.update()

    def CrashSprites(self, mode='f'):
        """
        Checks if there are any sprites which are known to be crashy and cause problems often
        """
        problems = (121,  # en reverse
                    475)  # will crash if you use a looped path

        founds = []
        for sprite in globals_.Area.sprites:
            if sprite.type in problems: founds.append(sprite)

        if mode == 'c':
            return bool(founds)
        else:
            for sprite in founds:
                sprite.delete()
                sprite.setSelected(False)
                globals_.mainWindow.scene.removeItem(sprite)
                globals_.mainWindow.levelOverview.update()

    def CrashSpriteSettings(self, mode='f'):
        """
        Checks for sprite settings which are known to cause major glitches and crashes
        """
        checkfor = []
        problem = False
        for sprite in globals_.Area.sprites:
            # ask somebody about 153 for clarification, the add it to the fixers
            if sprite.type == 166 and (sprite.spritedata[2] & 0xF0) >> 4 == 4: problem = True
            #           also double-check nyb10, then add it to the fixers
            if sprite.type == 171 and sprite.spritedata[4] & 0xF != 1: problem = True
            if sprite.type == 203 and sprite.spritedata[4] & 0xF == 1:
                if [454, 432] not in checkfor: checkfor.append([454, 432])
            if sprite.type == 247 and sprite.spritedata[5] & 0xF == 1: problem = True
            if sprite.type == 323:
                if sprite.spritedata[4] & 0xF == 4: problem = True
                if sprite.spritedata[2] & 0xF < (sprite.spritedata[3] & 0xF0) >> 4: problem = True
            if sprite.type == 449 and (sprite.spritedata[5] & 0xF0) >> 4 == 1: problem = True
            if sprite.type == 479 and sprite.spritedata[4] & 0xF == 1: problem = True
            if sprite.type == 481:
                if sprite.spritedata[5] & 0xF > 2: problem = True
                if [419] not in checkfor: checkfor.append([419])

        # check for sprites which are depended on by other sprites
        new = list(checkfor)
        for item in checkfor:
            for sprite in globals_.Area.sprites:
                if sprite.type in item:
                    try:
                        new.remove(item)
                    except Exception:
                        pass  # probably already removed it
        checkfor = new
        if checkfor: problem = True

        if mode == 'c':
            return problem
        elif problem:
            addsprites = []
            for sprite in globals_.Area.sprites:
                # :(
                if sprite.type == 166 and (
                    sprite.spritedata[2] & 0xF0) >> 4 == 4: sprite.spritedata = sprite.spritedata[
                                                                                0:2] + ' ' + sprite.spritedata[3:]
                if sprite.type == 171 and sprite.spritedata[4] & 0xF != 1: sprite.spritedata = sprite.spritedata[
                                                                                               0:4] + chr(
                    1) + sprite.spritedata[5:]
                if sprite.type == 203 and sprite.spritedata[4] & 0xF == 1:
                    if [454, 432] in checkfor:
                        addsprites.append((454, sprite.objx - 128, sprite.objy - 128))
                if sprite.type == 247 and sprite.spritedata[5] & 0xF == 1: sprite.spritedata = sprite.spritedata[
                                                                                               0:5] + chr(
                    0) + sprite.spritedata[6:]
                if sprite.type == 323:
                    if sprite.spritedata[4] & 0xF == 4: sprite.spritedata = sprite.spritedata[0:4] + chr(
                        1) + sprite.spritedata[5:]
                    if sprite.spritedata[2] & 0xF < (sprite.spritedata[3] & 0xF0) >> 4:
                        sprite.spritedata = sprite.spritedata[0:2] + chr(
                            (sprite.spritedata[3] & 0xF0) >> 4) + sprite.spritedata[3:]
                if sprite.type == 449 and (
                    sprite.spritedata[5] & 0xF0) >> 4 == 1: sprite.spritedata = sprite.spritedata[0:5] + chr(
                    0) + sprite.spritedata[6:]
                if sprite.type == 479 and sprite.spritedata[4] & 0xF == 1:
                    if (sprite.spritedata[4] & 0xF0) >> 4 == 1:
                        sprite.spritedata = sprite.spritedata[0:4] + chr(0x10) + sprite.spritedata[5:]
                    else:
                        sprite.spritedata = sprite.spritedata[0:4] + chr(0) + sprite.spritedata[5:]
                if sprite.type == 481:
                    if sprite.spritedata[5] & 0xF > 2: sprite.spritedata = sprite.spritdata[0:5] + chr(
                        2) + sprite.spritedata[6:]
                    addsprites.append((419, sprite.objx - 128, sprite.objy - 128))

            for id_, x, y in addsprites:
                globals_.mainWindow.CreateSprite(x, y, id_, RawData.from_sprite_id(id_))

            globals_.mainWindow.scene.update()

    def TooManySprites(self, mode='f'):
        """
        Determines if the # of sprites in the current area is > max_
        """
        max_ = 1000

        problem = len(globals_.Area.sprites) > max_

        if mode == 'c':
            return problem

        if not problem:
            return None

        for spr in globals_.Area.sprites[max_:]:
            spr.delete()
            spr.setSelected(False)
            globals_.mainWindow.scene.removeItem(spr)

        globals_.Area.sprites = globals_.Area.sprites[:max_]
        globals_.mainWindow.scene.update()
        globals_.mainWindow.levelOverview.update()

    def DuplicateEntranceIDs(self, mode='f'):
        """
        mode 'c': Checks for the prescence of multiple entrances with the same ID
        mode 'f': Fixes the entrance id of the duplicate entrances
        """
        ids = []
        for ent in globals_.Area.entrances:
            if ent.entid in ids:
                if mode == 'c':
                    return False

                # find the lowest available ID
                getids = [False for _ in range(256)]
                for check in globals_.Area.entrances:
                    getids[check.entid] = True

                minimumID = getids.index(False)

                ent.entid = minimumID
                ent.UpdateTooltip()
                ent.UpdateListItem()

            ids.append(ent.entid)

        return False

    def NoStartEntrance(self, mode='f'):
        """
        Determines if there is a start entrance or not
        """
        if globals_.Area.areanum != 1:
            return False

        start = None
        for ent in globals_.Area.entrances:
            if ent.entid == globals_.Area.startEntrance:
                start = ent
            else:
                problem = False
        problem = start is None

        if mode == 'c':
            return problem
        elif problem:
            # make an entrance at 1024, 512 with an ID of globals_.Area.startEntrance
            globals_.mainWindow.CreateEntrance(1024, 512, globals_.Area.startEntrance)

    def EntranceTooCloseToZoneEdge(self, mode='f'):
        """
        Checks if the main entrance is too close to the left zone edge
        """
        offset = 24 * 8  # 8 blocks away from the left zone edge
        if not globals_.Area.zones: return False

        # if the ent isn't even in the zone, return
        if self.EntranceOutsideOfZone('c'): return False

        start = None
        for ent in globals_.Area.entrances:
            if ent.entid == globals_.Area.startEntrance: start = ent
        if start is None: return False

        firstzone_idx = SLib.MapPositionToZoneID(globals_.Area.zones, start.objx, start.objy)

        if firstzone_idx == -1: return False

        firstzone = globals_.Area.zones[firstzone_idx]

        problem = start.objx < firstzone.objx + offset
        if mode == 'c':
            return problem
        elif problem:
            start.setPos((firstzone.objx + offset) * 1.5, start.objy * 1.5)

    def EntranceOutsideOfZone(self, mode='f'):
        """
        Checks if any entrances are not inside of a zone
        """
        left_offset = 24 * 8  # 8 blocks away from the left zone edge
        if not globals_.Area.zones: return False

        for ent in globals_.Area.entrances:
            x = ent.objx
            y = ent.objy
            zone_idx = SLib.MapPositionToZoneID(globals_.Area.zones, x, y)

            if zone_idx == -1: return False
            zone = globals_.Area.zones[zone_idx]

            if x < zone.objx:
                problem = True
            elif x > zone.objx + zone.width:
                problem = True
            elif y < zone.objy - 64:
                problem = True
            elif y > zone.objy + zone.height + 192:
                problem = True
            else:
                problem = False

            if problem and mode == 'c':
                return True
            elif problem:
                if x < zone.objx:
                    newx = zone.objx + left_offset
                elif x > zone.objx + zone.width:
                    newx = zone.objx + zone.width - 16
                else:
                    newx = ent.objx
                if y < (zone.objy - 64):
                    newy = zone.objy - 64  # entrances can be placed a few blocks above the top zone border
                elif y > zone.objy + zone.height:
                    newy = zone.objy + zone.height - 32
                else:
                    newy = ent.objy
                ent.objx = newx
                ent.objy = newy
                ent.setPos(int(newx * 1.5), int(newy * 1.5))
                globals_.mainWindow.scene.update()

        return False

    def TooManyZones(self, mode='f'):
        """
        Checks if there are too many zones in this area
        """
        problem = len(globals_.Area.zones) > 6

        if mode == 'c':
            return problem
        elif problem:
            globals_.Area.zones = globals_.Area.zones[:6]

            globals_.mainWindow.scene.update()
            globals_.mainWindow.levelOverview.update()

    def NoZones(self, mode='f'):
        """
        Checks if there are no zones in this area
        """
        problem = not globals_.Area.zones
        if mode == 'c':
            return problem

        if not problem:
            return

        # make a default zone
        globals_.mainWindow.CreateZone(16, 16)

    def ZonesTooClose(self, mode='f'):
        """
        Checks for any zones which are too close together or are overlapping
        """
        padding = 4  # minimum blocks between zones

        for check in reversed(
                globals_.Area.zones):  # reversed because generally zone 0 is most important, 1 is less, 2 is lesser, etc.
            crect = check.ZoneRect
            for against in globals_.Area.zones:
                if check is against: continue
                arect = against.ZoneRect.adjusted(-16 * padding, -16 * padding, 16 * padding, 16 * padding)

                if crect.intersects(arect):
                    if mode == 'c':
                        return True
                    else:
                        # AAAAAAAAAAA
                        center = crect.center()

                        if arect.contains(crect) or crect.contains(arect):
                            # one inside the other
                            axes = [None, 'both']
                        elif abs(center.x() - arect.center().x()) > abs(center.y() - arect.center().y()):
                            # horizontally positioned
                            if arect.center().x() > center.x():
                                # shrink the right
                                axes = [None, 'w']
                            else:
                                # shrink the left
                                axes = ['x', 'w']
                        else:
                            # vertically positioned
                            if arect.center().y() < center.y():
                                # shrink the top
                                axes = ['y', 'h']
                            else:
                                # shrink the bottom
                                axes = [None, 'h']

                        # the simplest method :D
                        checkzone = check.ZoneRect
                        oldCoords = checkzone.getCoords()
                        while checkzone.intersects(arect):
                            if axes[0] is None:
                                pass
                            elif axes[0] == 'x':
                                check.objx += 1
                            else:
                                check.objy += 1

                            if axes[1] == 'both':
                                check.objx += 1
                                check.objy += 1
                            elif axes[1] == 'w':
                                check.width -= 1
                            else:
                                check.height -= 1
                            if check.width < 204: check.width = 204
                            if check.height < 112: check.height = 112

                            check.UpdateRects()
                            check.setPos(int(check.objx * 1.5), int(check.objy * 1.5))
                            globals_.mainWindow.scene.update()
                            checkzone = check.ZoneRect

                            if oldCoords == checkzone.getCoords(): break
                            oldCoords = checkzone.getCoords()

                        globals_.mainWindow.scene.update()

        return False

    def ZonesTooCloseToAreaEdges(self, mode='f'):
        """
        Checks for any zones which are too close to the area edges, and moves them
        """
        areaw = 16384
        areah = 8192

        for z in globals_.Area.zones:
            if (z.objx < 16) or (z.objy < 16) or (z.objx + z.width > areaw - 16) or (z.objy + z.height > areah - 16):
                if mode == 'c':
                    return False
                else:
                    if z.objx < 16: z.objx = 16
                    if z.objy < 16: z.objy = 16
                    if z.objx + z.width > areaw - 16: z.width = areaw - z.objx - 16
                    if z.objy + z.height > areah - 16: z.height = areah - z.objy - 16
                    z.UpdateRects()
                    globals_.mainWindow.scene.update()

        return False

    def BiasNotEnabled(self, mode='f'):
        """
        Checks for any zones which do not have bias enabled
        """
        fix = {'0 0': (0, 1),
               '0 7': (0, 6),
               '0 11': (0, 4),
               '3 2': (0, 3),
               '3 7': (3, 3),  # This doesn't always appear
               '6 0': (6, 2),  # to work due to inconsistencies
               '6 7': (6, 6),  # in the editor, but I'm pretty
               '6 11': (6, 4),  # sure it's written correctly.
               '1 0': (1, 1),
               '1 7': (1, 10),
               '1 11': (1, 4),
               '4 2': (1, 3),
               '4 7': (4, 3)}

        for z in globals_.Area.zones:
            check = str(z.cammode) + ' ' + str(z.camzoom)
            if check in fix:
                if mode == 'c':
                    return False
                else:
                    z.cammode = fix[check][0]
                    z.camzoom = fix[check][1]

        return False

    def ZonesTooBig(self, mode='f'):
        """
        Checks for any zones which may be too large
        """
        maxarea = 16384  # blocks (approximated value)

        for z in globals_.Area.zones:
            if int((z.width / 32) * (z.height / 32)) > maxarea * 8:
                if mode == 'c':
                    return False
                else:  # shrink it by whichever dimension is larger
                    if z.width > z.height:
                        z.width = int(256 * maxarea / z.height)
                    else:
                        z.height = int(256 * maxarea / z.width)
                    z.UpdateRects()
                    globals_.mainWindow.scene.update()

        return False

    def ZonesTooSmall(self, mode='f'):
        """
        Checks for any zones which may be too small for their zoom level
        """
        MinimumSize = (484, 272)
        ##                        (484, 272), # -1
        ##                        (484, 272), # 0
        ##                        (484, 272), # 1
        ##                        (540, 304), # 2
        ##                        (596, 336), # 3
        ##                        (796, 448)) # 4
        ##        ZoomLevels = (3,
        ##                      3,
        ##                      6,
        ##                      6,
        ##                      5,
        ##                      None,
        ##                      4,
        ##                      4,
        ##                      0,
        ##                      1,
        ##                      None,
        ##                      5)

        fixes = []
        for z in globals_.Area.zones:
            if z.width < MinimumSize[0]:
                fixes.append(z)
            elif z.height < MinimumSize[1]:
                fixes.append(z)

        if mode == 'c':
            return bool(fixes)

        for z in fixes:
            if z.width < MinimumSize[0]: z.width = MinimumSize[0]
            if z.height < MinimumSize[1]: z.height = MinimumSize[1]
            z.prepareGeometryChange()
            z.UpdateRects()

        globals_.mainWindow.scene.update()
        globals_.mainWindow.levelOverview.update()
