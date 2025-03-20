#!/usr/bin/python
# -*- coding: latin-1 -*-

# Reggie Next - New Super Mario Bros. Wii Level Editor
# Milestone 4
# Copyright (C) 2009-2020 Treeki, Tempus, angelsl, JasonP27, Kamek64,
# MalStar1000, RoadrunnerWMC, AboodXD, John10v10, TheGrop, CLF78,
# Zementblock, Danster64

# This file is part of Reggie Next.

# Reggie Next is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Reggie Next is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Reggie Next.  If not, see <http://www.gnu.org/licenses/>.


# sprites.py
# Contains code to render sprite images from New Super Mario Bros. Wii


################################################################
################################################################

# Imports
import math
import random

from PyQt5 import QtCore, QtGui

import spritelib as SLib
import sprites_common as common
import globals_
from core.sprites.sprite import static_sprite, create_static_sprite, get_registered_sprites, Offset

Qt = QtCore.Qt
ImageCache = SLib.ImageCache


################################################################
################################################################
def LoadBasics():
    """
    Loads basic images used in NSMBW
    """
    # Load some coins, because coins are in almost every Mario level ever
    ImageCache['Coin'] = SLib.GetImg('coin.png')
    ImageCache['SpecialCoin'] = SLib.GetImg('special_coin.png')
    ImageCache['PCoin'] = SLib.GetImg('p_coin.png')
    ImageCache['RedCoin'] = SLib.GetImg('redcoin.png')
    ImageCache['StarCoin'] = SLib.GetImg('starcoin.png')

    # Load block contents
    ContentImage = SLib.GetImg('block_contents.png')
    Blocks = []
    count = ContentImage.width() // 24
    for i in range(count):
        Blocks.append(ContentImage.copy(i * 24, 0, 24, 24))
    ImageCache['BlockContents'] = Blocks

    # Load the blocks
    BlockImage = SLib.GetImg('blocks.png')
    Blocks = []
    count = BlockImage.width() // 24
    for i in range(count):
        Blocks.append(BlockImage.copy(i * 24, 0, 24, 24))
    ImageCache['Blocks'] = Blocks

    # Load the characters
    for num in range(4):
        for direction in 'lr':
            ImageCache['Character%d%s' % (num + 1, direction.upper())] = \
                SLib.GetImg('character_%d_%s.png' % (num + 1, direction))

    # Load vines, because these are used by entrances
    SLib.loadIfNotInImageCache('VineTop', 'vine_top.png')
    SLib.loadIfNotInImageCache('VineMid', 'vine_mid.png')
    SLib.loadIfNotInImageCache('VineBtm', 'vine_btm.png')


######### STATIC SPRITES #########

create_static_sprite('StarCoin', 32, preloaded=True, show_sprite_box=True)
create_static_sprite('StarCoin_Line', 155, base_sprite='StarCoin')
create_static_sprite('StarCoin_Bolt', 389, base_sprite='StarCoin')

create_static_sprite('Coin_Floating', 225, preloaded=True, initial_img='SpecialCoin')
create_static_sprite('PCoin', 237, preloaded=True)
create_static_sprite('Coin_Rotation', 253, preloaded=True, initial_img='SpecialCoin')
create_static_sprite('Coin_RollingHill', 371, preloaded=True, initial_img='SpecialCoin')
create_static_sprite('Coin_Bolt', 390, preloaded=True, initial_img='SpecialCoin')
create_static_sprite('SpinjumpCoin', 417, preloaded=True, initial_img='SpecialCoin', alpha=0.55)

create_static_sprite('Swooper', 100, load_files={'Swooper': 'swooper.png'}, offset=(-8, 8))
create_static_sprite('Bobomb', 101, load_files={'Bobomb': 'bobomb.png'}, offset=(-8, 8))
create_static_sprite('Broozer', 102, load_files={'Broozer': 'broozer.png'}, offset=(-9, -17))
create_static_sprite('Amp', 104, load_files={'Amp': 'amp.png'}, offset=(-8, 8))
create_static_sprite('AmpLine', 108, base_sprite='Amp')
create_static_sprite('UnusedWiimoteDoor', 319, load_files={'UnusedGiantDoor': 'unused_giant_door.png'}, offset=(-8, -8))
create_static_sprite('UnusedSlidingWiimoteDoor', 320, base_sprite='UnusedWiimoteDoor')
create_static_sprite('BoxGeneratr', 318, load_files={'BoxGenerator': 'box_generator.png'}, offset=(0, -64))
create_static_sprite('Bolt', 315, load_files={'Bolt': 'bolt.png'}, offset=(2, 0))
create_static_sprite('GhostHouseStand', 325, load_files={'GhostHouseStand': 'ghost_house_stand.png'}, offset=(8, -16))
create_static_sprite('LinePlatformBolt', 327, load_files={'LinePlatformBolt': 'line_platform_with_bolt.png'},
                     offset=(0, -16))
create_static_sprite('PlayerBlockPlatform', 333, load_files={'PlayerBlockPlatform': 'player_block_platform.png'})
create_static_sprite('FlipFence', 127, load_files={'FlipFence': 'flipfence.png'}, offset=(-4, -8), z=24999)
create_static_sprite('FlipFenceLong', 128, load_files={'FlipFenceLong': 'flipfence_long.png'}, offset=(6, 0), z=24999)
create_static_sprite('RedCoin', 144, preloaded=True)
create_static_sprite('ChainChomp', 146, load_files={'ChainChomp': 'chain_chomp.png'}, offset=(-90, -32))
create_static_sprite('Porcupuffer', 151, load_files={'Porcupuffer': 'porcu_puffer.png'}, offset=(-16, -18))
create_static_sprite('ChestnutGoomba', 170, load_files={'ChestnutGoomba': 'chestnut_goomba.png'}, offset=(-6, -8))
create_static_sprite('PowerupBubble', 171, load_files={'PowerupBubble': 'powerup_bubble.png'}, offset=(-8, -8))
create_static_sprite('GiantFloatingLog', 173, load_files={'GiantFloatingLog': 'giant_floating_log.png'},
                     offset=(-152, -32))
create_static_sprite('RouletteBlock', 176, load_files={'RouletteBlock': 'roulette.png'}, offset=(-4, -8))
create_static_sprite('FireChomp', 177, load_files={'FireChomp': 'fire_chomp.png'}, offset=(-2, -20))
create_static_sprite('CheepChomp', 180, load_files={'CheepChomp': 'cheep_chomp.png'}, offset=(-32, -16))
create_static_sprite('ToadBalloon', 185, load_files={'ToadBalloon': 'toad_balloon.png'}, offset=(-4, -4))
create_static_sprite('PlayerBlock', 187, load_files={'PlayerBlock': 'player_block.png'})
create_static_sprite('MidwayFlag', 188, load_files={'MidwayFlag': 'midway_flag.png'}, offset=(0, -38))
create_static_sprite('LarryKoopa', 189, load_files={'LarryKoopa': 'Larry_Koopa.png'}, offset=(-17, -33))
create_static_sprite('MegaGoomba', 199, load_files={'MegaGoomba': 'mega_goomba.png'}, offset=(-11, -37))
create_static_sprite('Microgoomba', 200, load_files={'Microgoomba': 'microgoomba.png'}, offset=(4, 8))
create_static_sprite('MGCannon', 202, load_files={'MGCannon': 'mg_cannon.png'}, offset=(-12, -42))
create_static_sprite('MGChest', 203, load_files={'MGChest': 'mg_chest.png'}, offset=(-12, -11))
create_static_sprite('FreefallGH', 214, load_files={'FreefallGH': 'freefall_gh_platform.png'}, z=24999)
create_static_sprite('SpikeU', 222, load_files={'SpikeU': 'spike_up.png'})
create_static_sprite('SandPillar', 229, load_files={'SandPillar': 'sand_pillar.png'}, offset=(-33, -150), alpha=0.65)
create_static_sprite('Bramball', 230, load_files={'Bramball': 'bramball.png'}, offset=(-32, -48))
create_static_sprite('BoltPlatformWire', 470, load_files={'BoltPlatformWire': 'bolt_platform_wire.png'},
                     offset=(5, -240))
create_static_sprite('MechaKoopa', 232, load_files={'MechaKoopa': 'mechakoopa.png'}, offset=(-8, -14))
create_static_sprite('Foo', 238, load_files={'Foo': 'foo.png'}, offset=(-8, -16))
create_static_sprite('GiantWiggler', 240, load_files={'GiantWiggler': 'giant_wiggler.png'}, offset=(-24, -64))
create_static_sprite('FallingLedgeBar', 242, load_files={'FallingLedgeBar': 'falling_ledge_bar.png'})
create_static_sprite('EventDeactivBlock', 252, tile=49)
create_static_sprite('SuperGuide', 477, load_files={'SuperGuide': 'superguide_block.png'}, offset=(-4, -4))
create_static_sprite('FlyingWrench', 476, load_files={'Wrench': 'wrench.png'})
create_static_sprite('SpinningThinBars', 457, load_files={'SpinningThinBars': 'spinning_thin_bars.png'},
                     offset=(-115.4, -115.4))
create_static_sprite('HammerPlatform', 455, load_files={'HammerPlatform': 'hammer_platform.png'}, offset=(-24, -8),
                     z=24999)
create_static_sprite('ScaredyRatDespawner', 451, load_files={'ScaredyRatDespawner': 'scaredy_rat_despawner.png'})
create_static_sprite('MetalBar', 448, load_files={'MetalBar': 'metal_bar.png'}, offset=(0, -32))
create_static_sprite('CagePeachReal', 445, load_files={'CagePeachReal': 'cage_peach_real.png'}, offset=(-18, -106))
create_static_sprite('PreSwingVine', 444, load_files={'PreSwingVine': 'swing_vine.png'})
create_static_sprite('ReplayBlock', 443, load_files={'ReplayBlock': 'replay_block.png'}, offset=(-8, -16))
create_static_sprite('CagePeachFake', 439, load_files={'CagePeachFake': 'cage_peach_fake.png'}, offset=(-18, -106))
create_static_sprite('FloatingQBlock', 433, load_files={'FloatingQBlock': 'floating_qblock.png'}, offset=(-6, -6))
create_static_sprite('Toad', 432, load_files={'Toad': 'toad.png'}, offset=(-1, -16))
create_static_sprite('MGPanel', 428, load_files={'MGPanel': 'minigame_flip_panel.png'}, offset=(-2, -6))
create_static_sprite('Kamek', 427, load_files={'Kamek': 'kamek.png'}, offset=(-19, -15))
create_static_sprite('UnusedGhostDoor', 421, load_files={'GhostDoorU': 'ghost_door.png'})
create_static_sprite('Bowser', 419, load_files={'Bowser': 'bowser.png'}, offset=(-35, -70))
create_static_sprite('BanzaiGen', 418, load_files={'BanzaiGen': 'banzai_bill_gen.png'}, offset=(-48, -16))
create_static_sprite('BetaLarryKoopa', 415, load_files={'LarryKoopaBeta': 'Larry_Koopa_Unused.png'},
                     offset=(-13, -22.5))
create_static_sprite('WendyRing', 413, load_files={'WendyRing': 'wendy_ring.png'}, offset=(-4, 4))
create_static_sprite('SpinyCheep', 395, load_files={'SpinyCheep': 'cheep_spiny.png'}, offset=(-1, -2))
create_static_sprite('LemmyBall', 394, load_files={'LemmyBall': 'lemmyball.png'}, offset=(-6, 0))
create_static_sprite('PropellerBlock', 393, load_files={'PropellerBlock': 'propeller_block.png'}, offset=(-1, -6))
create_static_sprite('Barrel', 388, load_files={'Barrel': 'barrel.png'}, offset=(-4, -8))
create_static_sprite('POW', 386, load_files={'POW': 'pow.png'})
create_static_sprite('CloudBlock', 370, load_files={'CloudBlock': 'cloud_block.png'}, offset=(-4, -8))
create_static_sprite('CubeKinokoLine', 367, load_files={'CubeKinokoP': 'cube_kinoko_p.png'})
create_static_sprite('RockyWrench', 352, load_files={'RockyWrench': 'rocky_wrench.png'}, offset=(4, -41))
create_static_sprite('LudwigVonKoopa', 348, load_files={'LudwigVonKoopa': 'Ludwig_Von_Koopa.png'}, offset=(-20, -30))
create_static_sprite('RoyKoopa', 347, load_files={'RoyKoopa': 'Roy_Koopa.png'}, offset=(-27, -24))
create_static_sprite('ChainHolder', 345, load_files={'ChainHolder': 'chain_holder.png'}, offset=(0, -12))
create_static_sprite('MortonKoopa', 344, load_files={'MortonKoopa': 'Morton_Koopa.png'}, offset=(-17, -34))
create_static_sprite('LemmyKoopa', 340, load_files={'LemmyKoopa': 'Lemmy_Koopa.png'}, offset=(-16, -53))
create_static_sprite('IggyKoopa', 337, load_files={'IggyKoopa': 'Iggy_Koopa.png'}, offset=(-17, -46))
create_static_sprite('WendyKoopa', 336, load_files={'WendyKoopa': 'Wendy_Koopa.png'}, offset=(-23, -23))
create_static_sprite('MegaIcicle', 311, load_files={'MegaIcicle': 'mega_icicle.png'}, offset=(-24, -3))
create_static_sprite('IceCube', 294, load_files={'IceCube': 'ice_cube.png'})
create_static_sprite('OldBarrel', 288, load_files={'OldBarrel': 'old_barrel.png'}, offset=(1, -7))
create_static_sprite('FiveEnemyRaft', 275, load_files={'FiveEnemyRaft': '5_enemy_max_raft.png'}, offset=(0, -8))
create_static_sprite('IceBro', 272, load_files={'IceBro': 'icebro.png'}, offset=(-5, -23))
create_static_sprite('WalkingPiranha', 264, load_files={'WalkPiranha': 'walk_piranha.png'}, offset=(-4, -50))
create_static_sprite('Crow', 134, load_files={'Crow': 'crow.png'}, offset=(-3, -2))
create_static_sprite('Wiggler', 130, load_files={'Wiggler': 'wiggler.png'}, offset=(0, -12))
create_static_sprite('SledgeBro', 120, load_files={'SledgeBro': 'sledgebro.png'}, offset=(-8, -28.5))
create_static_sprite('GiantDryBones', 119, load_files={'GiantDryBones': 'giant_drybones.png'}, offset=(-13, -24))
create_static_sprite('DryBones', 118, load_files={'DryBones': 'drybones.png'}, offset=(-7, -16))
create_static_sprite('BlooperBabies', 112, load_files={'BlooperBabies': 'blooper_babies.png'}, offset=(-5, -10))
create_static_sprite('Blooper', 111, load_files={'Blooper': 'blooper.png'}, offset=(-3, -10))
create_static_sprite('GiantSpikeBall', 98, load_files={'GiantSpikeBall': 'giant_spike_ball.png'}, offset=(-24, -24))
create_static_sprite('HammerBro', 95, load_files={'HammerBro': 'hammerbro.png'}, offset=(-4, -21))
create_static_sprite('BoomerangBro', 94, load_files={'BoomerangBro': 'boomerangbro.png'}, offset=(-8, -22))
create_static_sprite('BanzaiBillLauncher', 93, load_files={'BanzaiLauncher': 'banzai_launcher.png'},
                     offset=(-32, -66.7))
create_static_sprite('FireBro', 80, load_files={'FireBro': 'firebro.png'}, offset=(-8, -22))
create_static_sprite('ShipKey', 77, load_files={'ShipKey': 'ship_key.png'}, offset=(0, -8))
create_static_sprite('PipeFiretrapLeft', 72, load_files={'PipeFiretrapLeft': 'firetrap_pipe_left.png'}, offset=(-29, 6))
create_static_sprite('PipePiranhaUp', 65, load_files={'PipePlantUp': 'piranha_pipe_up.png'}, offset=(2, -32))
create_static_sprite('PipePiranhaDown', 66, load_files={'PipePlantDown': 'piranha_pipe_down.png'}, offset=(2, 32))
create_static_sprite('PipePiranhaRight', 67, load_files={'PipePlantRight': 'piranha_pipe_right.png'}, offset=(32, 2))
create_static_sprite('PipePiranhaLeft', 68, load_files={'PipePlantLeft': 'piranha_pipe_left.png'}, offset=(-32, 2))
create_static_sprite('PipeFiretrapUp', 69, load_files={'PipeFiretrapUp': 'firetrap_pipe_up.png'}, offset=(-4, -29))
create_static_sprite('PipeFiretrapDown', 70, load_files={'PipeFiretrapDown': 'firetrap_pipe_down.png'}, offset=(-4, 32))
create_static_sprite('PipeFiretrapRight', 71, load_files={'PipeFiretrapRight': 'firetrap_pipe_right.png'},
                     offset=(32, 6))
create_static_sprite('SpikeBall', 63, load_files={'SpikeBall': 'spike_ball.png'})
create_static_sprite('LineTiltGirder', 59, load_files={'LineGirder': 'line_tilt_girder.png'}, offset=(-8, -10))
create_static_sprite('RisingTiltGirder', 56, load_files={'RisingTiltGirder': 'rising_girder.png'}, offset=(-32, -10))
create_static_sprite('Lakitu', 54, load_files={'Lakitu': 'lakitu.png'}, offset=(-16, -24))
create_static_sprite('TiltingGirder', 51, load_files={'TiltingGirder': 'tilting_girder.png'}, offset=(0, -18))
create_static_sprite('Thwomp', 47, load_files={'Thwomp': 'thwomp.png'}, offset=(-6, -6))
create_static_sprite('GiantThwomp', 48, load_files={'GiantThwomp': 'giant_thwomp.png'}, offset=(-8, -8))
create_static_sprite('PSwitchBlock', 44, load_files={'PSwitchBlock': 'p_switch_block.png'})
create_static_sprite('UpsideDownSpiny', 26, load_files={'SpinyU': 'spiny_u.png'})
create_static_sprite('Goomba', 20, load_files={'Goomba': 'goomba.png'}, offset=(-1, -4))
create_static_sprite('ParaGoomba', 21, load_files={'ParaGoomba': 'para_goomba.png'}, offset=(1, -10))
create_static_sprite('HammerBroPlatform', 308, base_sprite='HammerBro')


@static_sprite(9, preloaded=True, initial_img='Character1R', offset=Offset.SNAP_TO_Y)
class CharacterSpawner:
    def dataChanged(self):
        direction = self.parent.spritedata[2] & 1
        character = self.parent.spritedata[5] & 3

        directionstr = 'L' if direction else 'R'
        self.image = ImageCache[f'Character{character + 1}{directionstr}']

        super().dataChanged()


_toad_ballons = {f'ToadHouseBalloon{cache_str}{num}': f'mg_house_balloon_{file_str}{num}.png'
                 for cache_str, file_str in (('', ''), ('Handle', 'handle_'))
                 for num in range(4)}


create_static_sprite('Unused_ToadHouseBalloon', 411,
                     initial_img='ToadHouseBalloon0', load_files=_toad_ballons, offset=Offset.IMAGE_CENTER)

@static_sprite(412, load_files=_toad_ballons)
class ToadHouseBalloon:
    def dataChanged(self):
        self.livesNum = (self.parent.spritedata[4] >> 4) & 3
        self.hasHandle = not ((self.parent.spritedata[5] >> 4) & 1)

        self.image = ImageCache['ToadHouseBalloon' + ('Handle' if self.hasHandle else '') + str(self.livesNum)]
        self.xOffset = 8 - (self.image.width() / 3)

        super().dataChanged()

        if self.hasHandle:
            self.yOffset = 12
        else:
            self.yOffset = 16 - (self.image.height() / 3)


@static_sprite(24,
               load_files={'BuzzyBeetle': 'buzzy_beetle.png', 'BuzzyBeetleU': 'buzzy_beetle_u.png',
                           'BuzzyBeetleShell': 'buzzy_beetle_shell.png', 'BuzzyBeetleShellU': 'buzzy_beetle_shell_u.png'})
class SpriteImage_BuzzyBeetle:
    def dataChanged(self):
        orient = self.parent.spritedata[5] & 15
        if orient == 1:
            self.image = ImageCache['BuzzyBeetleU']
            self.yOffset = 0
        elif orient == 2:
            self.image = ImageCache['BuzzyBeetleShell']
            self.yOffset = 2
        elif orient == 3:
            self.image = ImageCache['BuzzyBeetleShellU']
            self.yOffset = 2
        else:
            self.image = ImageCache['BuzzyBeetle']
            self.yOffset = 0

        super().dataChanged()


@static_sprite(25, load_files={'Spiny': 'spiny.png', 'SpinyShell': 'spiny_shell.png',
                                       'SpinyShellU': 'spiny_shell_u.png', 'SpinyBall': 'spiny_ball.png'})
class SpriteImage_Spiny:
    def dataChanged(self):
        orient = self.parent.spritedata[5] & 15
        if orient == 1:
            self.image = ImageCache['SpinyBall']
            self.yOffset = -2
        elif orient == 2:
            self.image = ImageCache['SpinyShell']
            self.yOffset = 1
        elif orient == 3:
            self.image = ImageCache['SpinyShellU']
            self.yOffset = 2
        else:
            self.image = ImageCache['Spiny']
            self.yOffset = 0

        super().dataChanged()


@static_sprite(43)
class SpriteImage_QSwitchBlock:  # 43
    @staticmethod
    def loadImages():
        if 'QSwitchBlock' not in ImageCache:
            q = SLib.GetImg('q_switch_block.png', True)
            ImageCache['QSwitchBlock'] = QtGui.QPixmap.fromImage(q)
            ImageCache['QSwitchBlockU'] = QtGui.QPixmap.fromImage(q.mirrored(True, True))

    def dataChanged(self):
        upsideDown = self.parent.spritedata[5] & 1
        if upsideDown:
            self.image = ImageCache['QSwitchBlockU']
        else:
            self.image = ImageCache['QSwitchBlock']

        super().dataChanged()


@static_sprite(45, load_files={'ESwitchBlock': 'e_switch_block.png', 'ESwitchBlockU': 'e_switch_block.png'}, alpha=0.1)
class SpriteImage_ExcSwitchBlock:
    def dataChanged(self):
        upsideDown = self.parent.spritedata[5] & 1
        if upsideDown:
            self.image = ImageCache['ESwitchBlockU']
        else:
            self.image = ImageCache['ESwitchBlock']

        super().dataChanged()



class SpriteImage_WoodenPlatform(SLib.SpriteImage):  # 23, 31, 50, 103, 106, 122
    def __init__(self, parent, scale=1.5):
        super().__init__(parent, scale)
        self.spritebox.shown = False

    @staticmethod
    def loadImages():
        # Load the two batches separately because another sprite only
        # loads the first three.
        if 'WoodenPlatformL' not in ImageCache:
            ImageCache['WoodenPlatformL'] = SLib.GetImg('wood_platform_left.png')
            ImageCache['WoodenPlatformM'] = SLib.GetImg('wood_platform_middle.png')
            ImageCache['WoodenPlatformR'] = SLib.GetImg('wood_platform_right.png')
        if 'StonePlatformL' not in ImageCache:
            ImageCache['StonePlatformL'] = SLib.GetImg('stone_platform_left.png')
            ImageCache['StonePlatformM'] = SLib.GetImg('stone_platform_middle.png')
            ImageCache['StonePlatformR'] = SLib.GetImg('stone_platform_right.png')
            ImageCache['BonePlatformL'] = SLib.GetImg('bone_platform_left.png')
            ImageCache['BonePlatformM'] = SLib.GetImg('bone_platform_middle.png')
            ImageCache['BonePlatformR'] = SLib.GetImg('bone_platform_right.png')

    def paint(self, painter):
        super().paint(painter)

        if self.color == 0:
            color = 'Wooden'
        elif self.color == 1:
            color = 'Stone'
        elif self.color == 2:
            color = 'Bone'

        if self.width > 32:
            painter.drawTiledPixmap(24, 0, int((self.width * 1.5) - 48), int(self.height * 1.5),
                                    ImageCache[color + 'PlatformM'])

        if self.width == 24:
            # replicate glitch effect foRotControlled by sprite 50
            painter.drawPixmap(0, 0, ImageCache[color + 'PlatformR'])
            painter.drawPixmap(8, 0, ImageCache[color + 'PlatformL'])
        else:
            # normal rendering
            painter.drawPixmap(int((self.width - 16) * 1.5), 0, ImageCache[color + 'PlatformR'])
            painter.drawPixmap(0, 0, ImageCache[color + 'PlatformL'])


class SpriteImage_DSStoneBlock(SLib.SpriteImage):  # 27, 28
    def __init__(self, parent, scale=1.5):
        super().__init__(parent, scale)
        self.spritebox.shown = False

    @staticmethod
    def loadImages():
        if 'DSBlockTopLeft' in ImageCache: return
        ImageCache['DSBlockTopLeft'] = SLib.GetImg('dsblock_topleft.png')
        ImageCache['DSBlockTop'] = SLib.GetImg('dsblock_top.png')
        ImageCache['DSBlockTopRight'] = SLib.GetImg('dsblock_topright.png')
        ImageCache['DSBlockLeft'] = SLib.GetImg('dsblock_left.png')
        ImageCache['DSBlockRight'] = SLib.GetImg('dsblock_right.png')
        ImageCache['DSBlockBottomLeft'] = SLib.GetImg('dsblock_bottomleft.png')
        ImageCache['DSBlockBottom'] = SLib.GetImg('dsblock_bottom.png')
        ImageCache['DSBlockBottomRight'] = SLib.GetImg('dsblock_bottomright.png')

    def dataChanged(self):
        super().dataChanged()

        # get size
        width = self.parent.spritedata[5] & 7
        if width == 0: width = 1
        byte5 = self.parent.spritedata[4]
        self.width = (16 + (width << 4))
        self.height = (16 << ((byte5 & 0x30) >> 4)) - 4

    def paint(self, painter):
        super().paint(painter)

        middle_width = int((self.width - 32) * 1.5)
        middle_height = int((self.height * 1.5) - 16)
        bottom_y = int((self.height * 1.5) - 8)
        right_x = int((self.width - 16) * 1.5)

        painter.drawPixmap(0, 0, ImageCache['DSBlockTopLeft'])
        painter.drawTiledPixmap(24, 0, middle_width, 8, ImageCache['DSBlockTop'])
        painter.drawPixmap(right_x, 0, ImageCache['DSBlockTopRight'])

        painter.drawTiledPixmap(0, 8, 24, middle_height, ImageCache['DSBlockLeft'])
        painter.drawTiledPixmap(right_x, 8, 24, middle_height, ImageCache['DSBlockRight'])

        painter.drawPixmap(0, bottom_y, ImageCache['DSBlockBottomLeft'])
        painter.drawTiledPixmap(24, bottom_y, middle_width, 8, ImageCache['DSBlockBottom'])
        painter.drawPixmap(right_x, bottom_y, ImageCache['DSBlockBottomRight'])


class SpriteImage_OldStoneBlock(SLib.SpriteImage):  # 30, 81, 82, 83, 84, 85, 86
    def __init__(self, parent, scale=1.5):
        super().__init__(parent, scale)
        self.spritebox.shown = False

        self.aux.append(SLib.AuxiliaryTrackObject(parent, 16, 16, SLib.AuxiliaryTrackObject.Horizontal))
        self.spikesL = False
        self.spikesR = False
        self.spikesT = False
        self.spikesB = False

        self.hasMovementAux = True

    @staticmethod
    def loadImages():
        if 'OldStoneTL' in ImageCache: return
        ImageCache['OldStoneTL'] = SLib.GetImg('oldstone_tl.png')
        ImageCache['OldStoneT'] = SLib.GetImg('oldstone_t.png')
        ImageCache['OldStoneTR'] = SLib.GetImg('oldstone_tr.png')
        ImageCache['OldStoneL'] = SLib.GetImg('oldstone_l.png')
        ImageCache['OldStoneM'] = SLib.GetImg('oldstone_m.png')
        ImageCache['OldStoneR'] = SLib.GetImg('oldstone_r.png')
        ImageCache['OldStoneBL'] = SLib.GetImg('oldstone_bl.png')
        ImageCache['OldStoneB'] = SLib.GetImg('oldstone_b.png')
        ImageCache['OldStoneBR'] = SLib.GetImg('oldstone_br.png')
        ImageCache['SpikeU'] = SLib.GetImg('spike_up.png')
        ImageCache['SpikeL'] = SLib.GetImg('spike_left.png')
        ImageCache['SpikeR'] = SLib.GetImg('spike_right.png')
        ImageCache['SpikeD'] = SLib.GetImg('spike_down.png')

    def dataChanged(self):
        super().dataChanged()

        size = self.parent.spritedata[5]
        height = (size & 0xF0) >> 4
        width = size & 0xF
        if self.parent.type == 30:
            height = 1 if height == 0 else height
            width = 1 if width == 0 else width
        self.width = width * 16 + 16
        self.height = height * 16 + 16

        if self.spikesL:  # left spikes
            self.xOffset = -16
            self.width += 16
        if self.spikesT:  # top spikes
            self.yOffset = -16
            self.height += 16
        if self.spikesR:  # right spikes
            self.width += 16
        if self.spikesB:  # bottom spikes
            self.height += 16

        # now set up the track
        if self.hasMovementAux:
            direction = self.parent.spritedata[2] & 3
            distance = (self.parent.spritedata[4] & 0xF0) >> 4
            if direction > 3: direction = 0

            if direction <= 1:  # horizontal
                self.aux[0].direction = 1
                self.aux[0].setSize(self.width + (distance * 16), self.height)
            else:  # vertical
                self.aux[0].direction = 2
                self.aux[0].setSize(self.width, self.height + (distance * 16))

            if direction == 0 or direction == 3:  # right, down
                self.aux[0].setPos(0, 0)
            elif direction == 1:  # left
                self.aux[0].setPos(-distance * 24, 0)
            elif direction == 2:  # up
                self.aux[0].setPos(0, -distance * 24)
        else:
            self.aux[0].setSize(0, 0)

    def paint(self, painter):
        super().paint(painter)

        blockX = 0
        blockY = 0
        type = self.parent.type
        width = self.width * 1.5
        height = self.height * 1.5

        if self.spikesL:  # left spikes
            painter.drawTiledPixmap(0, 0, 24, int(height), ImageCache['SpikeL'])
            blockX = 24
            width -= 24
        if self.spikesT:  # top spikes
            painter.drawTiledPixmap(0, 0, int(width), 24, ImageCache['SpikeU'])
            blockY = 24
            height -= 24
        if self.spikesR:  # right spikes
            painter.drawTiledPixmap(int(blockX + width - 24), 0, 24, int(height), ImageCache['SpikeR'])
            width -= 24
        if self.spikesB:  # bottom spikes
            painter.drawTiledPixmap(0, int(blockY + height - 24), int(width), 24, ImageCache['SpikeD'])
            height -= 24

        column2x = blockX + 24
        column3x = int(blockX + width - 24)
        row2y = blockY + 24
        row3y = int(blockY + height - 24)

        painter.drawPixmap(blockX, blockY, ImageCache['OldStoneTL'])
        painter.drawTiledPixmap(column2x, blockY, int(width - 48), 24, ImageCache['OldStoneT'])
        painter.drawPixmap(column3x, blockY, ImageCache['OldStoneTR'])

        painter.drawTiledPixmap(blockX, row2y, 24, int(height - 48), ImageCache['OldStoneL'])
        painter.drawTiledPixmap(column2x, row2y, int(width - 48), int(height - 48), ImageCache['OldStoneM'])
        painter.drawTiledPixmap(column3x, row2y, 24, int(height - 48), ImageCache['OldStoneR'])

        painter.drawPixmap(blockX, row3y, ImageCache['OldStoneBL'])
        painter.drawTiledPixmap(column2x, row3y, int(width - 48), 24, ImageCache['OldStoneB'])
        painter.drawPixmap(column3x, row3y, ImageCache['OldStoneBR'])


class SpriteImage_LiquidOrFog(SLib.SpriteImage):  # 53, 64, 138, 139, 216, 358, 374, 435
    def __init__(self, parent):
        super().__init__(parent)

        self.crest = None
        self.mid = None
        self.rise = None
        self.riseCrestless = None

        self.top = 0

        self.drawCrest = False
        self.risingHeight = 0

        self.locId = 0
        self.findZone()

    def findZone(self):
        self.zoneId = SLib.MapPositionToZoneID(globals_.Area.zones, self.parent.objx, self.parent.objy, True)

    def positionChanged(self):
        self.findZone()
        self.parent.scene().update()
        super().positionChanged()

    def dataChanged(self):
        self.parent.scene().update()
        super().dataChanged()

    def paintZone(self):
        return self.locId == 0 and self.zoneId != -1

    def realViewZone(self, painter, zoneRect):
        """
        Real view zone painter for liquids/fog
        """
        drawRise = self.risingHeight != 0
        drawCrest = self.drawCrest

        crest_rect = QtCore.QRectF()
        rise_rect = QtCore.QRectF()

        # Create the fill_rect (the area where the liquid or fog should be)
        fill_rect = QtCore.QRectF(zoneRect)
        fill_rect.setTop(self.top * 1.5)

        # Translate the fill_rect to be relative to the zone
        fill_rect.translate(-zoneRect.topLeft())

        if fill_rect.isEmpty():
            # the sprite is below the zone; don't draw anything
            return

        if fill_rect.top() <= 0:
            drawCrest = False  # off the top of the zone; no crest

        # Determine where to put the rise image
        if drawRise:
            rise_rect = fill_rect.translated(0, -24 * self.risingHeight)

            # Determine what image to draw for the rise indicator
            rise_img = self.rise
            if not drawCrest or rise_rect.top() <= 0:
                # close enough to the top zone border
                rise_rect.setTop(0)
                rise_img = self.riseCrestless

            # Set the correct height
            rise_rect.setHeight(rise_img.height())

        # If all that fits in the zone is some of the crest, determine how much
        if drawCrest:
            crest_rect = QtCore.QRectF(fill_rect)
            crest_rect.setHeight(self.crest.height())

            # Adjust the fill rect
            fill_rect.setTop(crest_rect.bottom())

        # Draw everything
        if drawCrest:
            painter.drawTiledPixmap(crest_rect, self.crest)

        painter.drawTiledPixmap(fill_rect, self.mid)

        if drawRise:
            painter.drawTiledPixmap(rise_rect, rise_img)

    def realViewLocation(self, painter, location_rect):
        """
        Real view location painter for liquids/fog
        """
        if self.paintZone():
            return

        for zone in globals_.Area.zones:
            if zone.id == self.zoneId:
                break
        else:
            return

        # Only draw in the intersection of the location and the zone. The
        # intersection needs to be translated, because draw offsets are relative
        # to the location.
        draw_rect = location_rect & zone.mapRectToScene(zone.DrawRect)
        draw_rect.translate(QtCore.QPoint(1, 1) - location_rect.topLeft())

        if draw_rect.isEmpty():
            return

        x, y, width, height = draw_rect.getRect()

        drawCrest = False
        crestHeight = 0

        if self.drawCrest:
            crestHeight = self.crest.height()
            drawCrest = y < crestHeight

        if drawCrest:
            if (crestHeight - y) >= height:
                painter.drawTiledPixmap(draw_rect, self.crest, draw_rect.topLeft())
            else:
                draw_rect.setBottom(crestHeight - y)
                painter.drawTiledPixmap(draw_rect, self.crest, draw_rect.topLeft())
                draw_rect.setTop(crestHeight - y)
                draw_rect.setHeight(height - crestHeight + y)
                painter.drawTiledPixmap(draw_rect, self.mid, draw_rect.topLeft())
        else:
            painter.drawTiledPixmap(draw_rect, self.mid, draw_rect.topLeft())


class SpriteImage_UnusedBlockPlatform(SLib.SpriteImage):  # 97, 107, 132, 160
    def __init__(self, parent, scale=1.5):
        super().__init__(parent, scale)
        self.spritebox.shown = False

        self.size = (48, 48)
        self.isDark = False
        self.drawPlatformImage = True

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('UnusedPlatform', 'unused_platform.png')
        SLib.loadIfNotInImageCache('UnusedPlatformDark', 'unused_platform_dark.png')

    def paint(self, painter):
        super().paint(painter)
        if not self.drawPlatformImage: return

        pixmap = ImageCache['UnusedPlatformDark'] if self.isDark else ImageCache['UnusedPlatform']
        pixmap = pixmap.scaled(
            int(self.width * 1.5), int(self.height * 1.5),
            Qt.IgnoreAspectRatio, Qt.SmoothTransformation,
        )
        painter.drawPixmap(0, 0, pixmap)


class SpriteImage_SpikedStake(SLib.SpriteImage):  # 137, 140, 141, 142
    def __init__(self, parent, scale=1.5):
        super().__init__(parent, scale)
        self.spritebox.shown = False

        self.HorzSpikeLength = ((36 * 16) + 41) / 1.5
        self.VertSpikeLength = ((36 * 16) + 39) / 1.5
        # (16 mid sections + an end section), accounting for image/sprite size difference
        self.dir = 'down'

    @staticmethod
    def loadImages():
        if 'StakeM0up' not in ImageCache:
            for dir in ['up', 'down', 'left', 'right']:
                ImageCache['StakeM0' + dir] = SLib.GetImg('stake_%s_m_0.png' % dir)
                ImageCache['StakeM1' + dir] = SLib.GetImg('stake_%s_m_1.png' % dir)
                ImageCache['StakeE0' + dir] = SLib.GetImg('stake_%s_e_0.png' % dir)
                ImageCache['StakeE1' + dir] = SLib.GetImg('stake_%s_e_1.png' % dir)

    def dataChanged(self):
        super().dataChanged()

        rawdistance = self.parent.spritedata[3] >> 4
        distance = (
            (16, 7, 14, 10, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16)
        )[rawdistance]
        distance += 1  # In order to hide one side of the track behind the image.
        speed = (self.parent.spritedata[2] >> 4) & 3

        L = 615
        W = 617  # 16 mid sections + an end section

        if speed == 3:
            self.aux[0].setSize(0, 0)
        else:
            if self.dir == 'up':
                self.aux[0].setPos(36, 24 - (distance * 24))
                self.aux[0].setSize(16, distance * 16)
            elif self.dir == 'down':
                self.aux[0].setPos(36, L - 24)
                self.aux[0].setSize(16, distance * 16)
            elif self.dir == 'left':
                self.aux[0].setPos(24 - (distance * 24), 36)
                self.aux[0].setSize(distance * 16, 16)
            else:
                self.aux[0].setPos(W - 24, 36)
                self.aux[0].setSize(distance * 16, 16)

    def paint(self, painter):
        super().paint(painter)

        color = self.parent.spritedata[3] & 15
        if color == 2 or color == 3 or color == 7:
            mid = ImageCache['StakeM1' + self.dir]
            end = ImageCache['StakeE1' + self.dir]
        else:
            mid = ImageCache['StakeM0' + self.dir]
            end = ImageCache['StakeE0' + self.dir]

        tiles = 16
        tilesize = 36
        endsizeV = 39
        endsizeH = 41
        widthV = 98
        widthH = 99

        if self.dir == 'up':
            painter.drawPixmap(0, 0, end)
            painter.drawTiledPixmap(0, endsizeV, widthV, tilesize * tiles, mid)
        elif self.dir == 'down':
            painter.drawTiledPixmap(0, 0, widthV, tilesize * tiles, mid)
            painter.drawPixmap(0, int((self.height * 1.5) - endsizeV), end)
        elif self.dir == 'left':
            painter.drawPixmap(0, 0, end)
            painter.drawTiledPixmap(endsizeH, 0, tilesize * tiles, widthH, mid)
        elif self.dir == 'right':
            painter.drawTiledPixmap(0, 0, tilesize * tiles, widthH, mid)
            painter.drawPixmap(int((self.width * 1.5) - endsizeH), 0, end)


class SpriteImage_ScrewMushroom(SLib.SpriteImage):  # 172, 382
    def __init__(self, parent, scale=1.5):
        super().__init__(parent, scale)
        self.spritebox.shown = False

        self.hasBolt = False
        self.size = (122, 190)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('Bolt', 'bolt.png')
        if 'ScrewShroomT' not in ImageCache:
            ImageCache['ScrewShroomT'] = SLib.GetImg('screw_shroom_top.png')
            ImageCache['ScrewShroomM'] = SLib.GetImg('screw_shroom_middle.png')
            ImageCache['ScrewShroomB'] = SLib.GetImg('screw_shroom_bottom.png')

    def dataChanged(self):
        super().dataChanged()

        # I wish I knew what this does
        SomeOffset = self.parent.spritedata[3]
        if SomeOffset == 0 or SomeOffset > 8: SomeOffset = 8

        self.height = 206 if self.hasBolt else 190
        self.yOffset = SomeOffset * -16
        if self.hasBolt:
            self.yOffset -= 16

    def paint(self, painter):
        super().paint(painter)

        y = 0
        if self.hasBolt:
            painter.drawPixmap(70, 0, ImageCache['Bolt'])
            print(ImageCache['Bolt'].height())
            y += 24
        painter.drawPixmap(0, y, ImageCache['ScrewShroomT'])
        painter.drawTiledPixmap(76, y + 93, 31, 172, ImageCache['ScrewShroomM'])
        painter.drawPixmap(76, y + 253, ImageCache['ScrewShroomB'])


class SpriteImage_Door(SLib.SpriteImage):  # 182, 259, 276, 277, 278
    def __init__(self, parent, scale=1.5):
        super().__init__(parent, scale)
        self.spritebox.shown = False

        self.doorName = 'Door'
        self.doorDimensions = (0, 0, 32, 48)
        self.entranceOffset = (0, 48)

        self.aux.append(SLib.AuxiliaryRectOutline(parent, 24, 24))
        self.aux[0].setIsBehindSprite(False)

    @staticmethod
    def loadImages():
        if 'DoorU' in ImageCache: return
        doors = {'Door': 'door', 'GhostDoor': 'ghost_door', 'TowerDoor': 'tower_door', 'CastleDoor': 'castle_door'}
        transform90 = QtGui.QTransform()
        transform180 = QtGui.QTransform()
        transform270 = QtGui.QTransform()
        transform90.rotate(90)
        transform180.rotate(180)
        transform270.rotate(270)

        for door, filename in doors.items():
            image = SLib.GetImg('%s.png' % filename, True)
            ImageCache[door + 'U'] = QtGui.QPixmap.fromImage(image)
            ImageCache[door + 'R'] = QtGui.QPixmap.fromImage(image.transformed(transform90))
            ImageCache[door + 'D'] = QtGui.QPixmap.fromImage(image.transformed(transform180))
            ImageCache[door + 'L'] = QtGui.QPixmap.fromImage(image.transformed(transform270))

    def dataChanged(self):
        super().dataChanged()

        rotstatus = self.parent.spritedata[4]
        if rotstatus & 1 == 0:
            direction = 0
        else:
            direction = (rotstatus & 0x30) >> 4

        if direction > 3: direction = 0
        doorName = self.doorName
        doorSize = self.doorDimensions
        if direction == 0:
            self.image = ImageCache[doorName + 'U']
            self.dimensions = doorSize
            paintEntrancePos = True
        elif direction == 1:
            self.image = ImageCache[doorName + 'L']
            self.dimensions = (
                (doorSize[2] / 2) + doorSize[0] - doorSize[3],
                doorSize[1] + (doorSize[3] - (doorSize[2] / 2)),
                doorSize[3],
                doorSize[2],
            )
            paintEntrancePos = False
        elif direction == 2:
            self.image = ImageCache[doorName + 'D']
            self.dimensions = (
                doorSize[0],
                doorSize[1] + doorSize[3],
                doorSize[2],
                doorSize[3],
            )
            paintEntrancePos = False
        elif direction == 3:
            self.image = ImageCache[doorName + 'R']
            self.dimensions = (
                doorSize[0] + (doorSize[2] / 2),
                doorSize[1] + (doorSize[3] - (doorSize[2] / 2)),
                doorSize[3],
                doorSize[2],
            )
            paintEntrancePos = False

        self.aux[0].setSize(
            *(
                (0, 0, 0, 0),
                (24, 24) + self.entranceOffset,
            )[1 if paintEntrancePos else 0]
        )

    def paint(self, painter):
        super().paint(painter)
        painter.setOpacity(self.alpha)
        painter.drawPixmap(0, 0, self.image)
        painter.setOpacity(1)


class SpriteImage_GiantBubble(SLib.SpriteImage):  # 205, 226
    def __init__(self, parent, scale=1.5):
        super().__init__(parent, scale)
        self.spritebox.shown = False
        self.parent.setZValue(24999)
        self.aux.append(SLib.AuxiliaryTrackObject(parent, 16, 16, SLib.AuxiliaryTrackObject.Horizontal))

    @staticmethod
    def loadImages():
        for shape in range(3):
            SLib.loadIfNotInImageCache('GiantBubble%d' % shape, 'giant_bubble_%d.png' % shape)

    def dataChanged(self):
        #super().dataChanged()

        self.shape = self.parent.spritedata[4] >> 4
        #print('Shape', self.shape, [hex(b) for b in self.parent.spritedata.original], self.parent.spritedata[4] >> 4)

        direction = self.parent.spritedata[5] & 0x0F
        distance = (self.parent.spritedata[5] & 0xF0) >> 4

        if self.shape > 3:
            self.shape = 0

        self.size = (
            (122, 137),
            (76, 170),
            (160, 81)
        )[self.shape]

        self.xOffset = -(self.width / 2) + 8
        self.yOffset = -(self.height / 2) + 8

        if distance == 0:
            self.aux[0].setSize(0, 0)
        elif direction == 1:  # horizontal
            self.aux[0].direction = 1
            self.aux[0].setSize((distance * 32) + self.width, 16)
            self.aux[0].setPos((-distance * 24), (self.height * 0.75) - 12)
        else:  # vertical
            self.aux[0].direction = 2
            self.aux[0].setSize(16, (distance * 32) + self.height)
            self.aux[0].setPos((self.width * 0.75) - 12, (-distance * 24))

    def paint(self, painter):
        #super().paint(painter)
        print(super(), painter)

        painter.drawPixmap(0, 0, ImageCache['GiantBubble%d' % self.shape])


class SpriteImage_Block(SLib.SpriteImage):  # 207, 208, 209, 221, 255, 256, 402, 403, 422, 423
    def __init__(self, parent, scale=1.5):
        super().__init__(parent, scale)
        self.spritebox.shown = False

        self.tilenum = 1315
        self.contentsNybble = 5
        self.contentsOverride = None
        self.eightIsMushroom = False
        self.twelveIsMushroom = False
        self.rotates = False

    def dataChanged(self):
        super().dataChanged()

        # SET CONTENTS
        # In the block_contents.png file:
        # 0 = Empty, 1 = Coin, 2 = Mushroom, 3 = Fire Flower, 4 = Propeller, 5 = Penguin Suit,
        # 6 = Mini Shroom, 7 = Star, 8 = Continuous Star, 9 = Yoshi Egg, 10 = 10 Coins,
        # 11 = 1-up, 12 = Vine, 13 = Spring, 14 = Shroom/Coin, 15 = Ice Flower, 16 = Toad, 17 = Hammer

        if self.contentsOverride is not None:
            contents = self.contentsOverride
        else:
            contents = self.parent.spritedata[self.contentsNybble] & 0xF

        if contents == 2:  # 1 and 2 are always fire flowers
            contents = 3

        if contents == 12 and self.twelveIsMushroom:
            contents = 2  # 12 is a mushroom on some types
        if contents == 8 and self.eightIsMushroom:
            contents = 2  # same as above, but for type 8

        self.image = ImageCache['BlockContents'][contents]

        # SET UP ROTATION
        if self.rotates:
            transform = QtGui.QTransform()
            transform.translate(12, 12)

            angle = (self.parent.spritedata[4] & 0xF0) >> 4
            leftTilt = self.parent.spritedata[3] & 1

            angle *= 45 / 16

            if leftTilt == 0:
                transform.rotate(angle)
            else:
                transform.rotate(360 - angle)

            transform.translate(-12, -12)
            self.parent.setTransform(transform)

    def paint(self, painter):
        super().paint(painter)

        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        if self.tilenum < len(SLib.Tiles):
            painter.drawPixmap(0, 0, SLib.GetTile(self.tilenum))
        painter.drawPixmap(0, 0, self.image)


class SpriteImage_Pipe(SLib.SpriteImage):  # 254, 339, 353, 377, 378, 379, 380, 450
    Top = 0
    Bottom = 1

    def __init__(self, parent, scale=1.5):
        super().__init__(parent, scale)
        self.spritebox.shown = False

        self.parent.setZValue(24999)

        self.direction = 'U'
        self.color = 'Green'
        self.length1 = 4
        self.length2 = 4

    @staticmethod
    def loadImages():
        if 'PipeTopGreen' not in ImageCache:
            for color in ('Green', 'Red', 'Yellow', 'Blue'):
                color_l = color.lower()
                ImageCache['PipeTop%s' % color] = SLib.GetImg('pipe_%s_top.png' % color_l)
                ImageCache['PipeMiddleV%s' % color] = SLib.GetImg('pipe_%s_middle.png' % color_l)
                ImageCache['PipeBottom%s' % color] = SLib.GetImg('pipe_%s_bottom.png' % color_l)
                ImageCache['PipeLeft%s' % color] = SLib.GetImg('pipe_%s_left.png' % color_l)
                ImageCache['PipeMiddleH%s' % color] = SLib.GetImg('pipe_%s_center.png' % color_l)
                ImageCache['PipeRight%s' % color] = SLib.GetImg('pipe_%s_right.png' % color_l)

    def dataChanged(self):
        super().dataChanged()
        # sprite types:
        # 339 = Moving Pipe Facing Up
        # 353 = Moving Pipe Facing Down
        # 377 = Pipe Up
        # 378 = Pipe Down
        # 379 = Pipe Right
        # 380 = Pipe Left
        # 450 = Enterable Pipe Up

        size = max(self.length1, self.length2) * 16

        if self.direction in 'LR':  # horizontal
            self.width = size
            self.height = 32
            if self.direction == 'R':  # faces right
                self.xOffset = 0
            else:  # faces left
                self.xOffset = 16 - size
            self.yOffset = 0

        else:  # vertical
            self.width = 32
            self.height = size
            if self.direction == 'D':  # faces down
                self.yOffset = 0
            else:  # faces up
                self.yOffset = 16 - size
            self.xOffset = 0

        if self.direction == 'U':  # facing up
            self.yOffset = 16 - size
        else:  # facing down
            self.yOffset = 0

    def paint(self, painter):
        super().paint(painter)

        color = self.color
        xsize = self.width * 1.5
        ysize = self.height * 1.5

        # Assume moving pipes
        length1 = self.length1 * 24
        length2 = self.length2 * 24
        low = min(length1, length2)
        high = max(length1, length2)

        if self.direction == 'U':
            y1 = ysize - low
            y2 = ysize - high

            if length1 != length2:
                # draw semi-transparent pipe
                painter.save()
                painter.setOpacity(0.5)
                painter.drawPixmap(0, int(y2), ImageCache['PipeTop%s' % color])
                painter.drawTiledPixmap(0, int(y2 + 24), 48, int(high - 24), ImageCache['PipeMiddleV%s' % color])
                painter.restore()

            # draw opaque pipe
            painter.drawPixmap(0, int(y1), ImageCache['PipeTop%s' % color])
            painter.drawTiledPixmap(0, int(y1 + 24), 48, int(low - 24), ImageCache['PipeMiddleV%s' % color])

        elif self.direction == 'D':

            if length1 != length2:
                # draw semi-transparent pipe
                painter.save()
                painter.setOpacity(0.5)
                painter.drawTiledPixmap(0, 0, 48, int(high - 24), ImageCache['PipeMiddleV%s' % color])
                painter.drawPixmap(0, int(high - 24), ImageCache['PipeBottom%s' % color])
                painter.restore()

            # draw opaque pipe
            painter.drawTiledPixmap(0, 0, 48, int(low - 24), ImageCache['PipeMiddleV%s' % color])
            painter.drawPixmap(0, int(low - 24), ImageCache['PipeBottom%s' % color])

        elif self.direction == 'R':

            if length1 != length2:
                # draw semi-transparent pipe
                painter.save()
                painter.setOpacity(0.5)
                painter.drawPixmap(int(high), 0, ImageCache['PipeRight%s' % color])
                painter.drawTiledPixmap(0, 0, int(high - 24), 48, ImageCache['PipeMiddleH%s' % color])
                painter.restore()

            # draw opaque pipe
            painter.drawPixmap(int(low - 24), 0, ImageCache['PipeRight%s' % color])
            painter.drawTiledPixmap(0, 0, int(low - 24), 48, ImageCache['PipeMiddleH%s' % color])

        else:  # left

            if length1 != length2:
                # draw semi-transparent pipe
                painter.save()
                painter.setOpacity(0.5)
                painter.drawTiledPixmap(0, 0, int(high - 24), 48, ImageCache['PipeMiddleH%s' % color])
                painter.drawPixmap(int(high - 24), 0, ImageCache['PipeLeft%s' % color])
                painter.restore()

            # draw opaque pipe
            painter.drawTiledPixmap(24, 0, int(low - 24), 48, ImageCache['PipeMiddleH%s' % color])
            painter.drawPixmap(0, 0, ImageCache['PipeLeft%s' % color])


class SpriteImage_PipeStationary(SpriteImage_Pipe):  # 377, 378, 379, 380, 450
    def __init__(self, parent, scale=1.5):
        super().__init__(parent, scale)
        self.length = 4

    def dataChanged(self):
        self.color = (
            'Green', 'Red', 'Yellow', 'Blue',
        )[(self.parent.spritedata[5] >> 4) & 3]

        self.length1 = self.length
        self.length2 = self.length

        super().dataChanged()


class SpriteImage_RollingHillWithPipe(SLib.SpriteImage):  # 355, 360
    def __init__(self, parent, scale=1.5):
        super().__init__(parent, scale)
        self.aux.append(SLib.AuxiliaryCircleOutline(parent, 800))


class SpriteImage_LongSpikedStake(SLib.SpriteImage):  # 398, 400
    def __init__(self, parent, scale=1.5):
        super().__init__(parent, scale)
        self.parent.setZValue(24999)  # to see sprites behind it easily
        self.spritebox.shown = False

        # 55 mid sections + an end section = 2021
        self.dir = 'left'

    @staticmethod
    def loadImages():
        if 'LongStakeM0left' in ImageCache: return
        for dir in ['left', 'right']:
            ImageCache['LongStakeM0' + dir] = SLib.GetImg('stake_%s_m_0.png' % dir)
            ImageCache['LongStakeM1' + dir] = SLib.GetImg('stake_%s_m_1.png' % dir)
            ImageCache['LongStakeE0' + dir] = SLib.GetImg('stake_%s_e_0.png' % dir)
            ImageCache['LongStakeE1' + dir] = SLib.GetImg('stake_%s_e_1.png' % dir)

    def dataChanged(self):
        super().dataChanged()

        color = self.parent.spritedata[3] & 15
        tiles = 55
        tilesize = 36
        endsize = 41
        width = 99

        pix = QtGui.QPixmap(2021, 99)
        pix.fill(Qt.transparent)
        paint = QtGui.QPainter(pix)

        if color == 2 or color == 3 or color == 6 or color == 7:
            mid = ImageCache['LongStakeM1' + self.dir]
            end = ImageCache['LongStakeE1' + self.dir]
        else:
            mid = ImageCache['LongStakeM0' + self.dir]
            end = ImageCache['LongStakeE0' + self.dir]

        if self.dir == 'left':
            self.aux[0].setPos(-1896, 36)
            paint.drawPixmap(0, 0, end)
            paint.drawTiledPixmap(endsize, 0, tilesize * tiles, width, mid)
        elif self.dir == 'right':
            self.aux[0].setPos(171, 36)
            self.aux[1].setPos(-1829, 0)
            paint.drawTiledPixmap(0, 0, tilesize * tiles, width, mid)
            paint.drawPixmap(1980, 0, end)

        self.aux[1].image = pix
        self.aux[1].alpha = 0.9


class SpriteImage_MassiveSpikedStake(SLib.SpriteImage):  # 401, 404
    def __init__(self, parent, scale=1.5):
        super().__init__(parent, scale)
        self.parent.setZValue(24999)  # to see sprites behind it easily
        self.spritebox.shown = False

        self.SpikeLength = ((72 * 40) + 136) / 1.5
        # (40 mid sections + an end section), accounting for image/sprite size difference
        self.dir = 'down'

    @staticmethod
    def loadImages():
        if 'MassiveStakeM0up' in ImageCache: return
        for dir in ['up', 'down']:
            ImageCache['MassiveStakeM0'] = SLib.GetImg('massive_stake_m_0.png')
            ImageCache['MassiveStakeM1'] = SLib.GetImg('massive_stake_m_1.png')
            ImageCache['MassiveStakeE0' + dir] = SLib.GetImg('massive_stake_%s_e_0.png' % dir)
            ImageCache['MassiveStakeE1' + dir] = SLib.GetImg('massive_stake_%s_e_1.png' % dir)

    def dataChanged(self):
        super().dataChanged()

        color = self.parent.spritedata[3] & 15
        tiles = 40
        tilesize = 72
        endsize = 136
        width = 248

        pix = QtGui.QPixmap(248, 3016)
        pix.fill(Qt.transparent)
        paint = QtGui.QPainter(pix)

        if color == 2 or color == 3 or color == 6 or color == 7:
            mid = ImageCache['MassiveStakeM1']
            end = ImageCache['MassiveStakeE1' + self.dir]
        else:
            mid = ImageCache['MassiveStakeM0']
            end = ImageCache['MassiveStakeE0' + self.dir]

        if self.dir == 'up':
            self.aux[0].setPos(112, -96)
            self.aux[1].setPos(4, -2592)
            paint.drawPixmap(0, 0, end)
            paint.drawTiledPixmap(0, endsize, width, tilesize * tiles, mid)
        elif self.dir == 'down':
            self.aux[0].setPos(112, 184)
            self.aux[1].setPos(4, 137)
            self.aux[2].setPos(0, -2808)
            paint.drawTiledPixmap(0, 0, width, tilesize * tiles, mid)
            paint.drawPixmap(0, 2880, end)

        paint = None
        self.aux[2].image = pix
        self.aux[2].alpha = 0.9


# ---- High-Level Classes ----

class SpriteImage_MeasureJump(SLib.SpriteImage):
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.aux.append(SLib.AuxiliaryImage(parent, 312, 191))
        self.aux[0].image = ImageCache["JumpRun1"]
        self.aux[0].setPos(0, 0)

    @staticmethod
    def loadImages():
        if "JumpRun1" in ImageCache:
            return

        for i in range(1, 4):
            ImageCache["JumpRun%d" % i] = SLib.GetImg("jump_run_%d.png" % i)
            ImageCache["JumpRunSpin%d" % i] = SLib.GetImg("jump_run_spin_%d.png" % i)

    def dataChanged(self):
        super().dataChanged()

        jumptype = self.parent.spritedata[2] & 3
        flags = (self.parent.spritedata[3] & 0xF0) >> 4
        direction = flags >> 3
        spin = (flags & 4) >> 2
        vertical = (flags & 2) >> 1

        if jumptype > 2:
            jumptype = 0

        if spin:
            img = ImageCache["JumpRunSpin%d" % (jumptype + 1)]
        else:
            img = ImageCache["JumpRun%d" % (jumptype + 1)]

        if direction == 1:
            img = img.transformed(QtGui.QTransform().scale(-1, 1))

        self.aux[0].image = img
        width, height = img.width(), img.height()
        self.aux[0].setSize(width, height)

        if direction == 1:
            self.aux[0].setPos(-width, 0)
        else:
            self.aux[0].setPos(0, 0)


class SpriteImage_HorzMovingPlatform(SpriteImage_WoodenPlatform):  # 23
    def __init__(self, parent):
        super().__init__(parent, 1.5)

        self.width = ((self.parent.spritedata[5] & 0xF) + 1) << 4
        self.aux.append(SLib.AuxiliaryTrackObject(parent, self.width, 16, SLib.AuxiliaryTrackObject.Horizontal))

    def dataChanged(self):
        super().dataChanged()

        # get width and distance
        self.width = ((self.parent.spritedata[5] & 0xF) + 1) << 4
        if self.width == 16: self.width = 32

        distance = (self.parent.spritedata[4] & 0xF) << 4

        # update the track
        self.aux[0].setSize(self.width + distance, 16)

        if (self.parent.spritedata[3] & 1) == 0:
            # platform goes right
            self.aux[0].setPos(0, 0)
        else:
            # platform goes left
            self.aux[0].setPos(-distance * 1.5, 0)

        # set color
        self.color = (self.parent.spritedata[3] >> 4) & 1

        self.aux[0].update()


class SpriteImage_DSStoneBlock_Vert(SpriteImage_DSStoneBlock):  # 27
    def __init__(self, parent):
        super().__init__(parent, 1.5)

        self.aux.append(SLib.AuxiliaryTrackObject(parent, 32, 16, SLib.AuxiliaryTrackObject.Vertical))
        self.size = (32, 16)

    def dataChanged(self):
        super().dataChanged()

        # get height and distance
        byte5 = self.parent.spritedata[4]
        distance = (byte5 & 0xF) << 4

        # update the track
        self.aux[0].setSize(self.width, distance + self.height)

        if (self.parent.spritedata[3] & 1) == 0:
            # block goes up
            self.aux[0].setPos(0, -distance * 1.5)
        else:
            # block goes down
            self.aux[0].setPos(0, 0)

        self.aux[0].update()


class SpriteImage_DSStoneBlock_Horz(SpriteImage_DSStoneBlock):  # 28
    def __init__(self, parent):
        super().__init__(parent, 1.5)

        self.aux.append(SLib.AuxiliaryTrackObject(parent, 32, 16, SLib.AuxiliaryTrackObject.Horizontal))
        self.size = (32, 16)

    def dataChanged(self):
        super().dataChanged()

        # get height and distance
        byte5 = self.parent.spritedata[4]
        distance = (byte5 & 0xF) << 4

        # update the track
        self.aux[0].setSize(distance + self.width, self.height)

        if (self.parent.spritedata[3] & 1) == 0:
            # block goes right
            self.aux[0].setPos(0, 0)
        else:
            # block goes left
            self.aux[0].setPos(-distance * 1.5, 0)

        self.aux[0].update()


class SpriteImage_OldStoneBlock_NoSpikes(SpriteImage_OldStoneBlock):  # 30
    pass


class SpriteImage_VertMovingPlatform(SpriteImage_WoodenPlatform):  # 31
    def __init__(self, parent):
        super().__init__(parent, 1.5)

        self.width = ((self.parent.spritedata[5] & 0xF) + 1) << 4
        self.aux.append(SLib.AuxiliaryTrackObject(parent, self.width, 16, SLib.AuxiliaryTrackObject.Vertical))

    def dataChanged(self):
        super().dataChanged()

        # get width and distance
        self.width = ((self.parent.spritedata[5] & 0xF) + 1) << 4
        if self.width == 16: self.width = 32

        distance = (self.parent.spritedata[4] & 0xF) << 4

        # update the track
        self.aux[0].setSize(self.width, distance + 16)

        if (self.parent.spritedata[3] & 1) == 0:
            # platform goes up
            self.aux[0].setPos(0, -distance * 1.5)
        else:
            # platform goes down
            self.aux[0].setPos(0, 0)

        # set color
        self.color = (self.parent.spritedata[3] >> 4) & 1

        self.aux[0].update()


class SpriteImage_QSwitch(common.SpriteImage_Switch):  # 40
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.switchType = 'Q'

    def dataChanged(self):
        self.offset = (0, 0)
        super().dataChanged()


class SpriteImage_PSwitch(common.SpriteImage_Switch):  # 41
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.switchType = 'P'

    def dataChanged(self):
        self.offset = (0, 0)
        super().dataChanged()


class SpriteImage_ExcSwitch(common.SpriteImage_Switch):  # 42
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.switchType = 'E'

    def dataChanged(self):
        self.offset = (0, 0)
        super().dataChanged()

class SpriteImage_Podoboo(SLib.SpriteImage):  # 46
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

        self.aux.append(SLib.AuxiliaryImage(parent, 48, 48))
        self.aux[0].image = ImageCache['Podoboo0']
        self.aux[0].setPos(-6, -6)
        self.aux[0].hover = False

        self.dimensions = (-3, 5, 24, 24)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('Podoboo0', 'podoboo.png')


class SpriteImage_UnusedSeesaw(SLib.SpriteImage):  # 49
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

        self.aux.append(SLib.AuxiliaryRotationAreaOutline(parent, 48))
        self.aux[0].setPos(128, -36)

        self.image = ImageCache['UnusedPlatformDark']
        self.dimensions = (0, -8, 256, 16)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('UnusedPlatformDark', 'unused_platform_dark.png')

    def dataChanged(self):
        w = self.parent.spritedata[5] & 15
        if w == 0:
            self.width = 16 * 16  # 16 blocks wide
        else:
            self.width = w * 32
        self.image = ImageCache['UnusedPlatformDark'].scaled(
            int(self.width * 1.5), int(self.height * 1.5),
            Qt.IgnoreAspectRatio, Qt.SmoothTransformation,
        )
        self.xOffset = (8 * 16) - (self.width / 2)

        swingArc = self.parent.spritedata[5] >> 4
        swingArcs = (
            45,
            4.5,
            9,
            18,
            65,
            80,
        )
        if swingArc <= 5:
            realSwingArc = swingArcs[swingArc]
        elif swingArc in (11, 15):
            realSwingArc = 0
        else:
            realSwingArc = 100  # infinite

        # angle starts at the right position (3 o'clock)
        # negative = clockwise, positive = counter-clockwise
        startAngle = 90 - realSwingArc
        spanAngle = realSwingArc * 2

        self.aux[0].SetAngle(startAngle, spanAngle)
        self.aux[0].setPos((self.width / 1.5) - 36, -36)
        self.aux[0].update()

        super().dataChanged()

    def paint(self, painter):
        super().paint(painter)

        painter.drawPixmap(0, 0, self.image)


class SpriteImage_FallingPlatform(SpriteImage_WoodenPlatform):  # 50
    def __init__(self, parent):
        super().__init__(parent, 1.5)

    def dataChanged(self):
        super().dataChanged()

        # get width
        raw_width = self.parent.spritedata[5] & 0xF
        slow = (self.parent.spritedata[5] >> 4) & 1

        self.width = (raw_width + 1) << 4
        if raw_width == 0:
            # override this for the "glitchy" effect caused by length=0
            self.width = 24
            self.xOffset = -4
        else:
            if slow:
                self.xOffset = 0
            else:
                self.xOffset = -16 * (raw_width >> 1)

        # set color
        color = (self.parent.spritedata[3] >> 4) & 3
        if color == 1:
            self.color = 1
        elif color == 3:
            self.color = 2
            self.height = 20
        else:
            self.color = 0


class SpriteImage_UnusedRotPlatforms(SLib.SpriteImage):  # 52
    def __init__(self, parent):
        super().__init__(parent, 1.5)

        for _ in range(4):
            img = SLib.AuxiliaryImage(parent, 144, 24)
            img.image = ImageCache["UnusedRotPlatform"]
            self.aux.append(img)

        self.aux[0].setPos(-60, -144)  # top
        self.aux[1].setPos(-60, 144)  # bottom
        self.aux[2].setPos(-204, 0)  # left
        self.aux[3].setPos(84, 0)  # right

    @staticmethod
    def loadImages():
        if 'UnusedRotPlatform' in ImageCache:
            return

        SLib.loadIfNotInImageCache('UnusedPlatformDark', 'unused_platform_dark.png')

        platform = ImageCache['UnusedPlatformDark'].scaled(
            144, 24,
            Qt.IgnoreAspectRatio, Qt.SmoothTransformation,
        )
        img = QtGui.QPixmap(144, 24)
        img.fill(Qt.transparent)
        paint = QtGui.QPainter(img)
        paint.setOpacity(0.8)
        paint.drawPixmap(0, 0, platform)
        ImageCache['UnusedRotPlatform'] = img


class SpriteImage_Quicksand(SpriteImage_LiquidOrFog):  # 53
    def __init__(self, parent):
        super().__init__(parent)

        self.crest = ImageCache['LiquidSandCrest']
        self.mid = ImageCache['LiquidSand']

        self.top = self.parent.objy + 8

    @staticmethod
    def loadImages():
        if 'LiquidSand' in ImageCache: return
        ImageCache['LiquidSand'] = SLib.GetImg('liquid_sand.png')
        ImageCache['LiquidSandCrest'] = SLib.GetImg('liquid_sand_crest.png')

    def dataChanged(self):
        self.locId = self.parent.spritedata[5] & 0x7F
        self.drawCrest = self.parent.spritedata[4] & 8 == 0

        if self.drawCrest:
            self.top = self.parent.objy + 8
        else:
            self.top = self.parent.objy

        super().dataChanged()

    def positionChanged(self):
        if self.drawCrest:
            self.top = self.parent.objy + 8
        else:
            self.top = self.parent.objy

        super().positionChanged()


class SpriteImage_UnusedRisingSeesaw(SLib.SpriteImage_Static):  # 55
    def __init__(self, parent):
        super().__init__(
            parent,
            1.5,
            ImageCache['UnusedPlatformDark'].scaled(
                377, 24,
                Qt.IgnoreAspectRatio, Qt.SmoothTransformation,
            ),
        )

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('UnusedPlatformDark', 'unused_platform_dark.png')


class SpriteImage_KoopaTroopa(SLib.SpriteImage_StaticMultiple):  # 57
    @staticmethod
    def loadImages():
        if 'KoopaG' in ImageCache: return
        ImageCache['KoopaG'] = SLib.GetImg('koopa_green.png')
        ImageCache['KoopaR'] = SLib.GetImg('koopa_red.png')
        ImageCache['KoopaShellG'] = SLib.GetImg('koopa_green_shell.png')
        ImageCache['KoopaShellR'] = SLib.GetImg('koopa_red_shell.png')

    def dataChanged(self):
        # get properties
        props = self.parent.spritedata[5]
        shell = (props >> 4) & 1
        red = props & 1

        if not shell:
            self.offset = (-7, -15)
            self.image = ImageCache['KoopaG'] if not red else ImageCache['KoopaR']
        else:
            del self.offset
            self.image = ImageCache['KoopaShellG'] if not red else ImageCache['KoopaShellR']

        super().dataChanged()


class SpriteImage_KoopaParatroopa(SLib.SpriteImage_StaticMultiple):  # 58
    def __init__(self, parent):
        super().__init__(parent, 1.5, None, (-7, -12))
        self.aux.append(SLib.AuxiliaryTrackObject(parent, 0, 0, 0))

    @staticmethod
    def loadImages():
        if 'ParakoopaG' not in ImageCache:
            ImageCache['ParakoopaG'] = SLib.GetImg('parakoopa_green.png')
            ImageCache['ParakoopaR'] = SLib.GetImg('parakoopa_red.png')
        if 'KoopaShellG' not in ImageCache:
            ImageCache['KoopaShellG'] = SLib.GetImg('koopa_green_shell.png')
            ImageCache['KoopaShellR'] = SLib.GetImg('koopa_red_shell.png')

    def dataChanged(self):

        # get properties
        color = self.parent.spritedata[5] & 1
        mode = (self.parent.spritedata[5] >> 4) & 3

        # 0: jumping
        # 3: shell
        if color == 0:
            if mode == 3:
                del self.offset
                self.image = ImageCache['KoopaShellG']
            else:
                self.offset = (-7, -12)
                self.image = ImageCache['ParakoopaG']
        else:
            if mode == 3:
                del self.offset
                self.image = ImageCache['KoopaShellR']
            else:
                self.offset = (-7, -12)
                self.image = ImageCache['ParakoopaR']

        if mode == 1 or mode == 2:

            track = self.aux[0]
            turnImmediately = self.parent.spritedata[4] & 1 == 1

            if mode == 1:
                track.direction = SLib.AuxiliaryTrackObject.Horizontal
                track.setSize(9 * 16, 16)
                if turnImmediately:
                    track.setPos(self.width / 2, self.height / 2)
                else:
                    track.setPos(-4 * 24 + self.width / 2, self.height / 2)
            else:
                track.direction = SLib.AuxiliaryTrackObject.Vertical
                track.setSize(16, 9 * 16)
                if turnImmediately:
                    track.setPos(self.width / 2, self.height / 2)
                else:
                    track.setPos(self.width / 2, -4 * 24 + self.height / 2)

        else:
            # hide the track
            self.aux[0].setSize(0, 0)

        super().dataChanged()


class SpriteImage_SpikeTop(SLib.SpriteImage_StaticMultiple):  # 60
    def __init__(self, parent):
        super().__init__(
            parent,
            1.5,
            ImageCache['SpikeTop00'],
            (0, -4),
        )

    @staticmethod
    def loadImages():
        if 'SpikeTop00' in ImageCache: return
        SpikeTop = SLib.GetImg('spiketop.png', True)

        Transform = QtGui.QTransform()
        ImageCache['SpikeTop00'] = QtGui.QPixmap.fromImage(SpikeTop.mirrored(True, False))
        Transform.rotate(90)
        ImageCache['SpikeTop10'] = ImageCache['SpikeTop00'].transformed(Transform)
        Transform.rotate(90)
        ImageCache['SpikeTop20'] = ImageCache['SpikeTop00'].transformed(Transform)
        Transform.rotate(90)
        ImageCache['SpikeTop30'] = ImageCache['SpikeTop00'].transformed(Transform)

        Transform = QtGui.QTransform()
        ImageCache['SpikeTop01'] = QtGui.QPixmap.fromImage(SpikeTop)
        Transform.rotate(90)
        ImageCache['SpikeTop11'] = ImageCache['SpikeTop01'].transformed(Transform)
        Transform.rotate(90)
        ImageCache['SpikeTop21'] = ImageCache['SpikeTop01'].transformed(Transform)
        Transform.rotate(90)
        ImageCache['SpikeTop31'] = ImageCache['SpikeTop01'].transformed(Transform)

    def dataChanged(self):
        orientation = (self.parent.spritedata[5] >> 4) & 3
        direction = self.parent.spritedata[5] & 1

        self.image = ImageCache['SpikeTop%d%d' % (orientation, direction)]

        self.offset = (
            (0, -4),
            (0, 0),
            (0, 0),
            (-4, 0),
        )[orientation]

        super().dataChanged()


class SpriteImage_BigBoo(SLib.SpriteImage):  # 61
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

        self.aux.append(SLib.AuxiliaryImage(parent, 243, 248))
        self.aux[0].image = ImageCache['BigBoo']
        self.aux[0].setPos(-48, -48)
        self.aux[0].hover = False

        self.dimensions = (-38, -80, 98, 102)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('BigBoo', 'bigboo.png')


class SpriteImage_SpinningFirebar(SLib.SpriteImage):  # 62
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False
        self.aux.append(SLib.AuxiliaryCircleOutline(parent, 12, Qt.AlignCenter))

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('FirebarBase', 'firebar_base_0.png')
        SLib.loadIfNotInImageCache('FirebarBaseWide', 'firebar_base_1.png')

    def dataChanged(self):
        super().dataChanged()

        size = self.parent.spritedata[5] & 0xF
        wideBase = (self.parent.spritedata[3] >> 4) & 1

        width = ((size * 2) + 1) * 12
        self.aux[0].setSize(width)

        currentAuxX = self.aux[0].x()
        currentAuxY = self.aux[0].y()
        if wideBase: self.aux[0].setPos(currentAuxX + 12, currentAuxY)

        self.image = ImageCache['FirebarBase'] if not wideBase else ImageCache['FirebarBaseWide']
        self.xOffset = 0 if not wideBase else -8
        self.width = 16 if not wideBase else 32

    def paint(self, painter):
        super().paint(painter)
        painter.drawPixmap(0, 0, self.image)


class SpriteImage_OutdoorsFog(SpriteImage_LiquidOrFog):  # 64
    def __init__(self, parent):
        super().__init__(parent)
        self.mid = ImageCache['OutdoorsFog']
        self.top = self.parent.objy

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('OutdoorsFog', 'fog_outdoors.png')

    def dataChanged(self):
        self.locId = self.parent.spritedata[5] & 0x7F
        super().dataChanged()

    def positionChanged(self):
        self.top = self.parent.objy
        super().positionChanged()


class SpriteImage_GroundPiranha(SLib.SpriteImage_StaticMultiple):  # 73
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.xOffset = -20

    @staticmethod
    def loadImages():
        if 'GroundPiranha' in ImageCache: return
        GP = SLib.GetImg('ground_piranha.png', True)
        ImageCache['GroundPiranha'] = QtGui.QPixmap.fromImage(GP)
        ImageCache['GroundPiranhaU'] = QtGui.QPixmap.fromImage(GP.mirrored(False, True))

    def dataChanged(self):

        upsideDown = self.parent.spritedata[5] & 1
        if not upsideDown:
            self.yOffset = 6
            self.image = ImageCache['GroundPiranha']
        else:
            self.yOffset = 0
            self.image = ImageCache['GroundPiranhaU']

        super().dataChanged()


class SpriteImage_BigGroundPiranha(SLib.SpriteImage_StaticMultiple):  # 74
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.xOffset = -65

    @staticmethod
    def loadImages():
        if 'BigGroundPiranha' in ImageCache: return
        BGP = SLib.GetImg('big_ground_piranha.png', True)
        ImageCache['BigGroundPiranha'] = QtGui.QPixmap.fromImage(BGP)
        ImageCache['BigGroundPiranhaU'] = QtGui.QPixmap.fromImage(BGP.mirrored(False, True))

    def dataChanged(self):

        upsideDown = self.parent.spritedata[5] & 1
        if not upsideDown:
            self.yOffset = -32
            self.image = ImageCache['BigGroundPiranha']
        else:
            self.yOffset = 0
            self.image = ImageCache['BigGroundPiranhaU']

        super().dataChanged()


class SpriteImage_GroundFiretrap(SLib.SpriteImage_StaticMultiple):  # 75
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.xOffset = 5

    @staticmethod
    def loadImages():
        if 'GroundFiretrap' in ImageCache: return
        GF = SLib.GetImg('ground_firetrap.png', True)
        ImageCache['GroundFiretrap'] = QtGui.QPixmap.fromImage(GF)
        ImageCache['GroundFiretrapU'] = QtGui.QPixmap.fromImage(GF.mirrored(False, True))

    def dataChanged(self):

        upsideDown = self.parent.spritedata[5] & 1
        if not upsideDown:
            self.yOffset = -10
            self.image = ImageCache['GroundFiretrap']
        else:
            self.yOffset = 0
            self.image = ImageCache['GroundFiretrapU']

        super().dataChanged()


class SpriteImage_BigGroundFiretrap(SLib.SpriteImage_StaticMultiple):  # 76
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.xOffset = -14

    @staticmethod
    def loadImages():
        if 'BigGroundFiretrap' in ImageCache: return
        BGF = SLib.GetImg('big_ground_firetrap.png', True)
        ImageCache['BigGroundFiretrap'] = QtGui.QPixmap.fromImage(BGF)
        ImageCache['BigGroundFiretrapU'] = QtGui.QPixmap.fromImage(BGF.mirrored(False, True))

    def dataChanged(self):

        upsideDown = self.parent.spritedata[5] & 1
        if not upsideDown:
            self.yOffset = -68
            self.image = ImageCache['BigGroundFiretrap']
        else:
            self.yOffset = 0
            self.image = ImageCache['BigGroundFiretrapU']

        super().dataChanged()


class SpriteImage_CloudTrampoline(SLib.SpriteImage_StaticMultiple):  # 78
    def __init__(self, parent):
        super().__init__(
            parent,
            1.5,
            ImageCache['CloudTrSmall'],
            (-2, -2),
        )

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('CloudTrBig', 'cloud_trampoline_big.png')
        SLib.loadIfNotInImageCache('CloudTrSmall', 'cloud_trampoline_small.png')

    def dataChanged(self):

        size = (self.parent.spritedata[4] >> 4) & 1
        if size == 0:
            self.image = ImageCache['CloudTrSmall']
        else:
            self.image = ImageCache['CloudTrBig']

        super().dataChanged()


class SpriteImage_OldStoneBlock_SpikesLeft(SpriteImage_OldStoneBlock):  # 81
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spikesL = True


class SpriteImage_OldStoneBlock_SpikesRight(SpriteImage_OldStoneBlock):  # 82
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spikesR = True


class SpriteImage_OldStoneBlock_SpikesLeftRight(SpriteImage_OldStoneBlock):  # 83
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spikesL = True
        self.spikesR = True


class SpriteImage_OldStoneBlock_SpikesTop(SpriteImage_OldStoneBlock):  # 84
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spikesT = True


class SpriteImage_OldStoneBlock_SpikesBottom(SpriteImage_OldStoneBlock):  # 85
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spikesB = True


class SpriteImage_OldStoneBlock_SpikesTopBottom(SpriteImage_OldStoneBlock):  # 86
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spikesT = True
        self.spikesB = True


class SpriteImage_TrampolineWall(SLib.SpriteImage_StaticMultiple):  # 87
    def __init__(self, parent):
        super().__init__(parent, 1.5)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('UnusedPlatformDark', 'unused_platform_dark.png')

    def dataChanged(self):
        height = (self.parent.spritedata[5] & 15) + 1

        self.image = ImageCache['UnusedPlatformDark'].scaled(
            24, height * 24,
            Qt.IgnoreAspectRatio, Qt.SmoothTransformation,
        )
        self.height = height * 16

        super().dataChanged()


class SpriteImage_BulletBillLauncher(SLib.SpriteImage):  # 92
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('BBLauncherT', 'bullet_launcher_top.png')
        SLib.loadIfNotInImageCache('BBLauncherM', 'bullet_launcher_middle.png')

    def dataChanged(self):
        super().dataChanged()
        height = (self.parent.spritedata[5] & 0xF0) >> 4

        self.height = (height + 2) * 16
        self.yOffset = (height + 1) * -16

    def paint(self, painter):
        super().paint(painter)

        painter.drawPixmap(0, 0, ImageCache['BBLauncherT'])
        painter.drawTiledPixmap(0, 48, 24, int(self.height * 1.5 - 48), ImageCache['BBLauncherM'])


class SpriteImage_RotationControllerSwaying(SLib.SpriteImage):  # 96
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.parent.setZValue(100000)
        self.aux.append(SLib.AuxiliaryRotationAreaOutline(parent, 48))

    def dataChanged(self):
        super().dataChanged()
        # get the swing arc: 4 == 90 degrees (45 left from the origin, 45 right)
        swingArc = self.parent.spritedata[2] >> 4
        realSwingArc = swingArc * 11.25

        # angle starts at the right position (3 o'clock)
        # negative = clockwise, positive = counter-clockwise
        startAngle = 90 - realSwingArc
        spanAngle = realSwingArc * 2

        self.aux[0].SetAngle(startAngle, spanAngle)
        self.aux[0].update()


class SpriteImage_RotationControlledSolidBetaPlatform(SpriteImage_UnusedBlockPlatform):  # 97
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.isDark = True

    def dataChanged(self):
        size = self.parent.spritedata[4]
        width = size >> 4
        height = size & 0xF

        if width == 0 or height == 0:
            self.spritebox.shown = True
            self.drawPlatformImage = False
            del self.size
        else:
            self.spritebox.shown = False
            self.drawPlatformImage = True
            self.size = (width * 16, height * 16)

        super().dataChanged()


class SpriteImage_PipeEnemyGenerator(SLib.SpriteImage):  # 99
    def __init__(self, parent):
        super().__init__(parent, 1.5)

    def dataChanged(self):
        super().dataChanged()

        self.spritebox.size = (16, 16)
        direction = (self.parent.spritedata[5] & 0xF) & 3
        if direction in (0, 1):  # vertical pipe
            self.spritebox.size = (32, 16)
        elif direction in (2, 3):  # horizontal pipe
            self.spritebox.size = (16, 32)

        self.yOffset = 0
        if direction in (2, 3):
            self.yOffset = -16


class SpriteImage_PlatformGenerator(SpriteImage_WoodenPlatform):  # 103
    # TODO: Add arrows
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.yOffset = 16

    def dataChanged(self):
        super().dataChanged()

        # get width
        self.width = self.parent.spritedata[5] & 0xF0

        # length 0 results in the same width as length 4
        if self.width == 0: self.width = 64

        # override the x offset for the "glitchy" effect caused by length 0
        if self.width in {16, 24}:
            self.width = 24
            self.xOffset = -8
        else:
            self.xOffset = 0

        self.color = 0


class SpriteImage_Pokey(SLib.SpriteImage):  # 105
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

        self.dimensions = (-4, 0, 24, 32)

    @staticmethod
    def loadImages():
        if 'PokeyTop' in ImageCache: return
        ImageCache['PokeyTop'] = SLib.GetImg('pokey_top.png')
        ImageCache['PokeyMiddle'] = SLib.GetImg('pokey_middle.png')
        ImageCache['PokeyBottom'] = SLib.GetImg('pokey_bottom.png')

    def dataChanged(self):
        super().dataChanged()

        # get the height
        height = self.parent.spritedata[5] & 7
        self.height = (height * 16) + 16 + 25
        self.yOffset = 16 - self.height

    def paint(self, painter):
        super().paint(painter)

        painter.drawPixmap(0, 0, ImageCache['PokeyTop'])
        painter.drawTiledPixmap(0, 37, 36, int(self.height * 1.5 - 61), ImageCache['PokeyMiddle'])
        painter.drawPixmap(0, int(self.height * 1.5 - 24), ImageCache['PokeyBottom'])


class SpriteImage_LinePlatform(SpriteImage_WoodenPlatform):  # 106
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.yOffset = 8

    def dataChanged(self):
        super().dataChanged()

        # get width
        self.width = (self.parent.spritedata[5] & 0xF) << 4

        # length=0 becomes length=4
        if self.width == 0: self.width = 64

        # override this for the "glitchy" effect caused by length=0
        if self.width == 16: self.width = 24

        # reposition platform
        self.xOffset = 32 - (self.width / 2)

        color = (self.parent.spritedata[4] & 0xF0) >> 4
        if color > 1: color = 0
        self.color = color


class SpriteImage_RotationControlledPassBetaPlatform(SpriteImage_UnusedBlockPlatform):  # 107
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.isDark = True
        self.width = 16

    def dataChanged(self):
        size = self.parent.spritedata[4]
        height = (size & 0xF) + 1

        self.yOffset = -(height - 1) * 8
        self.height = height * 16

        super().dataChanged()


class SpriteImage_ChainBall(SLib.SpriteImage_StaticMultiple):  # 109
    def __init__(self, parent):
        super().__init__(parent, 1.5)

    @staticmethod
    def loadImages():
        if 'ChainBallU' in ImageCache: return
        ImageCache['ChainBallU'] = SLib.GetImg('chainball_up.png')
        ImageCache['ChainBallR'] = SLib.GetImg('chainball_right.png')
        ImageCache['ChainBallD'] = SLib.GetImg('chainball_down.png')
        ImageCache['ChainBallL'] = SLib.GetImg('chainball_left.png')

    def dataChanged(self):
        direction = self.parent.spritedata[5] & 3
        if direction > 3: direction = 0

        if direction & 1 == 0:  # horizontal
            self.size = (96, 38)
        else:  # vertical
            self.size = (37, 96)

        if direction == 0:  # right
            self.image = ImageCache['ChainBallR']
            self.offset = (3, -8.5)
        elif direction == 1:  # up
            self.image = ImageCache['ChainBallU']
            self.offset = (-8.5, -81.5)
        elif direction == 2:  # left
            self.image = ImageCache['ChainBallL']
            self.offset = (-83, -11)
        elif direction == 3:  # down
            self.image = ImageCache['ChainBallD']
            self.offset = (-11, 3.5)

        super().dataChanged()


class SpriteImage_Sunlight(SLib.SpriteImage):  # 110
    def __init__(self, parent):
        super().__init__(parent, 1.5)

        i = ImageCache['Sunlight']
        self.aux.append(SLib.AuxiliaryImage_FollowsRect(parent, i.width(), i.height()))
        self.aux[0].realimage = i
        self.aux[0].alignment = Qt.AlignTop | Qt.AlignRight
        self.aux[0].hover = False

        # Moving the sunlight when a repaint occured is overkill and causes an
        # infinite loop. Alternative idea: Only move the sunlight when
        # - scrolling or
        # - zooming
        # This causes small visual bugs while moving the sprite, but moving this
        # sprite makes little sense, so I guess it's fine.

        slot = self.moveSunlight

        # scrolling
        view = self.parent.scene().views()[0]
        view.XScrollBar.valueChanged.connect(slot)
        view.YScrollBar.valueChanged.connect(slot)

        # zooming
        self.parent.scene().getMainWindow().ZoomWidget.slider.valueChanged.connect(slot)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('Sunlight', 'sunlight.png')

    def paint(self, painter):
        self.moveSunlight()
        SLib.SpriteImage.paint(self, painter)

    def moveSunlight(self):
        try:
            if not SLib.RealViewEnabled:
                self.aux[0].realimage = None
                return

            zone = self.parent.nearestZone(True)
            if zone is None:
                self.aux[0].realimage = None
                return

            zoneRect = QtCore.QRectF(zone.objx * 1.5, zone.objy * 1.5, zone.width * 1.5, zone.height * 1.5)
            view = self.parent.scene().views()[0]
            viewRect = view.mapToScene(view.viewport().rect()).boundingRect()
            bothRect = zoneRect & viewRect

            if bothRect.getRect() == (0, 0, 0, 0):
                # The zone is out of view -> hide the image
                self.aux[0].realimage = None
                return

            self.aux[0].realimage = ImageCache['Sunlight']
            self.aux[0].move(*bothRect.getRect())
        except RuntimeError:
            # happens if the parent was deleted
            pass


class SpriteImage_Flagpole(SLib.SpriteImage):  # 113
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

        self.image = ImageCache['Flagpole']

        self.aux.append(SLib.AuxiliaryImage(parent, 144, 149))
        self.offset = (-30, -144)
        self.size = (self.image.width() / 1.5, self.image.height() / 1.5)

    @staticmethod
    def loadImages():
        if 'Flagpole' in ImageCache: return
        ImageCache['Flagpole'] = SLib.GetImg('flagpole.png')
        ImageCache['FlagpoleSecret'] = SLib.GetImg('flagpole_secret.png')
        ImageCache['Castle'] = SLib.GetImg('castle.png')
        ImageCache['CastleSecret'] = SLib.GetImg('castle_secret.png')
        ImageCache['SnowCastle'] = SLib.GetImg('snow_castle.png')
        ImageCache['SnowCastleSecret'] = SLib.GetImg('snow_castle_secret.png')

    def dataChanged(self):

        # get the info (mimic the way the game does it)
        exit_type = self.parent.spritedata[2] >> 4
        snow_type = self.parent.spritedata[5] & 0xF
        value = exit_type + snow_type * 2

        if value == 0:
            show_snow = show_secret = False
        elif value == 1:
            show_snow = False
            show_secret = True
        elif value == 2:
            show_snow = True
            show_secret = False
        else:
            show_snow = show_secret = True

        if show_secret:
            suffix = "Secret"
        else:
            suffix = ""

        self.image = ImageCache['Flagpole' + suffix]

        if show_snow:
            self.aux[0].image = ImageCache['SnowCastle' + suffix]
            self.aux[0].setPos(356, 91)
        else:
            self.aux[0].image = ImageCache['Castle' + suffix]
            self.aux[0].setPos(356, 97)

        super().dataChanged()

    def paint(self, painter):
        super().paint(painter)
        painter.drawPixmap(0, 0, self.image)


class SpriteImage_FlameCannon(SLib.SpriteImage_StaticMultiple):  # 114
    def __init__(self, parent):
        super().__init__(parent, 1.5)

        self.height = 64

    @staticmethod
    def loadImages():
        if 'FlameCannonR' in ImageCache: return
        transform90 = QtGui.QTransform()
        transform270 = QtGui.QTransform()
        transform90.rotate(90)
        transform270.rotate(270)

        image = SLib.GetImg('continuous_flame_cannon.png', True)
        ImageCache['FlameCannonR'] = QtGui.QPixmap.fromImage(image)
        ImageCache['FlameCannonD'] = QtGui.QPixmap.fromImage(image.transformed(transform90))
        ImageCache['FlameCannonL'] = QtGui.QPixmap.fromImage(image.mirrored(True, False))
        ImageCache['FlameCannonU'] = QtGui.QPixmap.fromImage(image.transformed(transform270).mirrored(True, False))

    def dataChanged(self):
        direction = self.parent.spritedata[5] & 15
        if direction > 3: direction = 0

        if direction == 0:  # right
            del self.offset
        elif direction == 1:  # left
            self.offset = (-48, 0)
        elif direction == 2:  # up
            self.offset = (0, -48)
        elif direction == 3:  # down
            del self.offset

        directionstr = 'RLUD'[direction]
        self.image = ImageCache['FlameCannon%s' % directionstr]

        super().dataChanged()


class SpriteImage_Cheep(SLib.SpriteImage):  # 115
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

        self.aux.append(SLib.AuxiliaryTrackObject(self.parent, 24, 24, SLib.AuxiliaryTrackObject.Horizontal))

    @staticmethod
    def loadImages():
        if 'CheepGreen' in ImageCache: return
        ImageCache['CheepRedLeft'] = SLib.GetImg('cheep_red.png')
        ImageCache['CheepRedRight'] = QtGui.QPixmap.fromImage(SLib.GetImg('cheep_red.png', True).mirrored(True, False))
        ImageCache['CheepRedAtYou'] = SLib.GetImg('cheep_red_atyou.png')
        ImageCache['CheepGreen'] = SLib.GetImg('cheep_green.png')
        ImageCache['CheepYellow'] = SLib.GetImg('cheep_yellow.png')

    def dataChanged(self):

        type = self.parent.spritedata[5] & 0xF
        if type in (1, 7):
            self.image = ImageCache['CheepGreen']
        elif type == 8:
            self.image = ImageCache['CheepYellow']
        elif type == 5:
            self.image = ImageCache['CheepRedAtYou']
        else:
            self.image = ImageCache['CheepRedLeft']
        self.size = (self.image.width() / 1.5, self.image.height() / 1.5)

        if type == 3:
            distance = ((self.parent.spritedata[3] & 0xF) + 1) * 16
            self.aux[0].setSize((distance * 2) + 16, 16)
            self.aux[0].setPos(-distance * 1.5, 0)
        else:
            self.aux[0].setSize(0, 24)

        super().dataChanged()

    def paint(self, painter):
        super().paint(painter)
        painter.drawPixmap(0, 0, self.image)


class SpriteImage_CoinCheep(SLib.SpriteImage):  # 116
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

    @staticmethod
    def loadImages():
        if 'CheepRedLeft' in ImageCache: return
        ImageCache['CheepRedLeft'] = SLib.GetImg('cheep_red.png')
        ImageCache['CheepRedRight'] = QtGui.QPixmap.fromImage(SLib.GetImg('cheep_red.png', True).mirrored(True, False))
        ImageCache['CheepRedAtYou'] = SLib.GetImg('cheep_red_atyou.png')
        ImageCache['CheepGreen'] = SLib.GetImg('cheep_green.png')
        ImageCache['CheepYellow'] = SLib.GetImg('cheep_yellow.png')

    def dataChanged(self):

        waitFlag = self.parent.spritedata[5] & 1
        if waitFlag:
            self.spritebox.shown = False
            self.image = ImageCache['CheepRedAtYou']
        else:
            type = self.parent.spritedata[2] >> 4
            if type & 3 == 3:
                self.spritebox.shown = True
                self.image = None
            elif type < 7:
                self.spritebox.shown = False
                self.image = self.image = ImageCache['CheepRedRight']
            else:
                self.spritebox.shown = False
                self.image = self.image = ImageCache['CheepRedLeft']

        if self.image is not None:
            self.size = (self.image.width() / 1.5, self.image.height() / 1.5)
        super().dataChanged()

    def paint(self, painter):
        super().paint(painter)
        if self.image is None: return
        painter.drawPixmap(0, 0, self.image)


class SpriteImage_PulseFlameCannon(SLib.SpriteImage_StaticMultiple):  # 117
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.height = 112

    @staticmethod
    def loadImages():
        if 'PulseFlameCannonR' in ImageCache: return
        transform90 = QtGui.QTransform()
        transform270 = QtGui.QTransform()
        transform90.rotate(90)
        transform270.rotate(270)

        onImage = SLib.GetImg('synchro_flame_jet.png', True)
        ImageCache['PulseFlameCannonR'] = QtGui.QPixmap.fromImage(onImage)
        ImageCache['PulseFlameCannonD'] = QtGui.QPixmap.fromImage(onImage.transformed(transform90))
        ImageCache['PulseFlameCannonL'] = QtGui.QPixmap.fromImage(onImage.mirrored(True, False))
        ImageCache['PulseFlameCannonU'] = QtGui.QPixmap.fromImage(
            onImage.transformed(transform270).mirrored(True, False))

    def dataChanged(self):

        direction = self.parent.spritedata[5] & 15
        if direction > 3: direction = 0

        if direction == 0:
            del self.offset
        elif direction == 1:
            self.offset = (-96, 0)
        elif direction == 2:
            self.offset = (0, -96)
        elif direction == 3:
            del self.offset

        directionstr = 'RLUD'[direction]
        self.image = ImageCache['PulseFlameCannon%s' % directionstr]

        super().dataChanged()


class SpriteImage_OneWayPlatform(SpriteImage_WoodenPlatform):  # 122
    def dataChanged(self):
        super().dataChanged()
        width = self.parent.spritedata[5] & 0xF
        if width < 2: width = 1
        self.width = width * 32 + 32

        self.xOffset = self.width * -0.5

        self.color = ((self.parent.spritedata[4] & 0xF0) >> 4) & 1


class SpriteImage_UnusedCastlePlatform(SLib.SpriteImage_StaticMultiple):  # 123
    def __init__(self, parent):
        super().__init__(parent, 1.5)

        self.image = ImageCache['UnusedCastlePlatform']
        self.size = (255, 255)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('UnusedCastlePlatform', 'unused_castle_platform.png')

    def dataChanged(self):
        rawSize = self.parent.spritedata[4] >> 4

        if rawSize != 0:
            widthInBlocks = rawSize * 4
        else:
            widthInBlocks = 8

        topRadiusInBlocks = widthInBlocks / 10
        heightInBlocks = widthInBlocks + topRadiusInBlocks

        self.image = ImageCache['UnusedCastlePlatform'].scaled(widthInBlocks * 24, int(heightInBlocks * 24))

        self.offset = (
            -(self.image.width() / 1.5) / 2,
            -topRadiusInBlocks * 16,
        )

        super().dataChanged()


class SpriteImage_FenceKoopaHorz(SLib.SpriteImage_StaticMultiple):  # 125
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.offset = (-3, -12)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('FenceKoopaHG', 'fencekoopa_horz.png')
        SLib.loadIfNotInImageCache('FenceKoopaHR', 'fencekoopa_horz_red.png')

    def dataChanged(self):

        color = self.parent.spritedata[5] & 1
        if color == 1:
            self.image = ImageCache['FenceKoopaHR']
        else:
            self.image = ImageCache['FenceKoopaHG']

        super().dataChanged()


class SpriteImage_FenceKoopaVert(SLib.SpriteImage_StaticMultiple):  # 126
    def __init__(self, parent):
        super().__init__(parent, 1.5)

        self.offset = (-2, -12)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('FenceKoopaVG', 'fencekoopa_vert.png')
        SLib.loadIfNotInImageCache('FenceKoopaVR', 'fencekoopa_vert_red.png')

    def dataChanged(self):

        color = self.parent.spritedata[5] & 1
        if color == 1:
            self.image = ImageCache['FenceKoopaVR']
        else:
            self.image = ImageCache['FenceKoopaVG']

        super().dataChanged()


class SpriteImage_4Spinner(SLib.SpriteImage_Static):  # 129
    def __init__(self, parent):
        super().__init__(
            parent,
            1.5,
            ImageCache['4Spinner'],
            (-62, -48),
        )

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('4Spinner', '4spinner.png')

    def dataChanged(self):
        super().dataChanged()
        self.alpha = 0.6 if (self.parent.spritedata[2] >> 4) & 1 else 1


class SpriteImage_Boo(SLib.SpriteImage):  # 131
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

        self.aux.append(SLib.AuxiliaryImage(parent, 50, 51))
        self.aux[0].image = ImageCache['Boo1']
        self.aux[0].setPos(-6, -6)

        self.dimensions = (-1, -4, 22, 22)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('Boo1', 'boo1.png')


class SpriteImage_UnusedBlockPlatform1(SpriteImage_UnusedBlockPlatform):  # 132
    def dataChanged(self):
        self.width = ((self.parent.spritedata[5] & 0xF) + 1) * 16
        self.height = ((self.parent.spritedata[5] >> 4) + 1) * 16
        super().dataChanged()


class SpriteImage_StalagmitePlatform(SLib.SpriteImage):  # 133
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

        self.aux.append(SLib.AuxiliaryImage(parent, 48, 156))
        self.aux[0].image = ImageCache['StalagmitePlatformBottom']
        self.aux[0].setPos(24, 60)

        self.image = ImageCache['StalagmitePlatformTop']
        self.dimensions = (0, -8, 64, 40)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('StalagmitePlatformTop', 'stalagmite_platform_top.png')
        SLib.loadIfNotInImageCache('StalagmitePlatformBottom', 'stalagmite_platform_bottom.png')

    def paint(self, painter):
        super().paint(painter)
        painter.drawPixmap(0, 0, self.image)


class SpriteImage_HangingPlatform(SLib.SpriteImage_Static):  # 135
    def __init__(self, parent):
        super().__init__(parent, 1.5)

        self.aux.append(SLib.AuxiliaryImage(parent, 11, 378))
        self.aux[0].image = ImageCache['HangingPlatformTop']
        self.aux[0].setPos(138, -378)

        self.image = ImageCache['HangingPlatformBottom']
        self.size = (192, 32)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('HangingPlatformTop', 'hanging_platform_top.png')
        SLib.loadIfNotInImageCache('HangingPlatformBottom', 'hanging_platform_bottom.png')


class SpriteImage_RotBulletLauncher(SLib.SpriteImage):  # 136
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

        self.dimensions = (-4, 0, 24, 16)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('RotLauncherCannon', 'bullet_cannon_rot_0.png')
        SLib.loadIfNotInImageCache('RotLauncherPivot', 'bullet_cannon_rot_1.png')

    def dataChanged(self):
        super().dataChanged()
        pieces = self.parent.spritedata[3] & 15
        if pieces > 7: pieces = 7
        self.yOffset = -pieces * 16
        self.height = (pieces + 1) * 16

    def paint(self, painter):
        super().paint(painter)

        pieces = (self.parent.spritedata[3] & 15) + 1
        if pieces > 8: pieces = 8
        pivot1_4 = self.parent.spritedata[4] & 15
        pivot5_8 = self.parent.spritedata[4] >> 4
        startleft1_4 = self.parent.spritedata[5] & 15
        startleft5_8 = self.parent.spritedata[5] >> 4

        pivots = [pivot1_4, pivot5_8]
        startleft = [startleft1_4, startleft5_8]

        ysize = self.height * 1.5

        for piece in range(pieces):
            bitpos = 1 << (piece & 3)
            if pivots[piece // 4] & bitpos:
                painter.drawPixmap(5, int(ysize - (piece - 1) * 24), ImageCache['RotLauncherPivot'])
            else:
                xo = 6
                image = ImageCache['RotLauncherCannon']
                if startleft[piece // 4] & bitpos:
                    transform = QtGui.QTransform()
                    transform.rotate(180)
                    image = QtGui.QPixmap(image.transformed(transform))
                    xo = 0
                painter.drawPixmap(xo, int(ysize - (piece + 1) * 24), image)


class SpriteImage_SpikedStakeDown(SpriteImage_SpikedStake):  # 137
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.dir = 'down'
        self.aux.append(SLib.AuxiliaryTrackObject(parent, 16, 64, SLib.AuxiliaryTrackObject.Vertical))

        self.dimensions = (0, 16 - self.VertSpikeLength, 66, self.VertSpikeLength)


class SpriteImage_Water(SpriteImage_LiquidOrFog):  # 138
    def __init__(self, parent):
        super().__init__(parent)

        self.crest = ImageCache['LiquidWaterCrest']
        self.mid = ImageCache['LiquidWater']
        self.rise = ImageCache['LiquidWaterRiseCrest']
        self.riseCrestless = ImageCache['LiquidWaterRise']

        self.top = self.parent.objy

    @staticmethod
    def loadImages():
        if 'LiquidWater' in ImageCache: return
        ImageCache['LiquidWater'] = SLib.GetImg('liquid_water.png')
        ImageCache['LiquidWaterCrest'] = SLib.GetImg('liquid_water_crest.png')
        ImageCache['LiquidWaterRise'] = SLib.GetImg('liquid_water_rise.png')
        ImageCache['LiquidWaterRiseCrest'] = SLib.GetImg('liquid_water_rise_crest.png')

    def dataChanged(self):
        self.locId = self.parent.spritedata[5] & 0x7F
        self.drawCrest = self.parent.spritedata[4] & 8 == 0

        self.risingHeight = (self.parent.spritedata[3] & 0xF) << 4
        self.risingHeight |= self.parent.spritedata[4] >> 4
        if self.parent.spritedata[2] & 15 > 7:  # falling
            self.risingHeight = -self.risingHeight

        if not self.drawCrest and self.locId == 0:
            self.top = self.parent.objy + 20
            self.mid.alpha = 0.1
        else:
            self.top = self.parent.objy
            self.mid.alpha = 1

        super().dataChanged()

    def positionChanged(self):
        self.top = self.parent.objy
        super().positionChanged()


class SpriteImage_Lava(SpriteImage_LiquidOrFog):  # 139
    def __init__(self, parent):
        super().__init__(parent)

        self.crest = ImageCache['LiquidLavaCrest']
        self.mid = ImageCache['LiquidLava']
        self.rise = ImageCache['LiquidLavaRiseCrest']
        self.riseCrestless = ImageCache['LiquidLavaRise']

        self.top = self.parent.objy

    @staticmethod
    def loadImages():
        if 'LiquidLava' in ImageCache: return
        ImageCache['LiquidLava'] = SLib.GetImg('liquid_lava.png')
        ImageCache['LiquidLavaCrest'] = SLib.GetImg('liquid_lava_crest.png')
        ImageCache['LiquidLavaRise'] = SLib.GetImg('liquid_lava_rise.png')
        ImageCache['LiquidLavaRiseCrest'] = SLib.GetImg('liquid_lava_rise_crest.png')

    def dataChanged(self):
        self.locId = self.parent.spritedata[5] & 0x7F
        self.drawCrest = self.parent.spritedata[4] & 8 == 0

        self.risingHeight = (self.parent.spritedata[3] & 0xF) << 4
        self.risingHeight |= self.parent.spritedata[4] >> 4
        if self.parent.spritedata[2] & 15 > 7:  # falling
            self.risingHeight = -self.risingHeight

        super().dataChanged()

    def positionChanged(self):
        self.top = self.parent.objy
        super().positionChanged()


class SpriteImage_SpikedStakeUp(SpriteImage_SpikedStake):  # 140
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.dir = 'up'
        self.aux.append(SLib.AuxiliaryTrackObject(parent, 16, 64, SLib.AuxiliaryTrackObject.Vertical))

        self.dimensions = (0, 0, 66, self.VertSpikeLength)


class SpriteImage_SpikedStakeRight(SpriteImage_SpikedStake):  # 141
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.dir = 'right'
        self.aux.append(SLib.AuxiliaryTrackObject(parent, 64, 16, SLib.AuxiliaryTrackObject.Horizontal))

        self.dimensions = (16 - self.HorzSpikeLength, 0, self.HorzSpikeLength, 66)


class SpriteImage_SpikedStakeLeft(SpriteImage_SpikedStake):  # 142
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.dir = 'left'
        self.aux.append(SLib.AuxiliaryTrackObject(parent, 64, 16, SLib.AuxiliaryTrackObject.Horizontal))

        self.dimensions = (0, 0, self.HorzSpikeLength, 66)


class SpriteImage_Arrow(SLib.SpriteImage_StaticMultiple):  # 143
    def __init__(self, parent):
        super().__init__(parent, 1.5)

    @staticmethod
    def loadImages():
        if 'Arrow0' in ImageCache: return
        for i in range(8):
            ImageCache['Arrow%d' % i] = SLib.GetImg('arrow_%d.png' % i)

    def dataChanged(self):
        ArrowOffsets = [(3, 0), (5, 4), (1, 3), (5, -1), (3, 0), (-1, -1), (0, 3), (-1, 4)]

        direction = self.parent.spritedata[5] & 7
        self.image = ImageCache['Arrow%d' % direction]

        self.width = self.image.width() / 1.5
        self.height = self.image.height() / 1.5
        self.offset = ArrowOffsets[direction]

        super().dataChanged()


class SpriteImage_FloatingBarrel(SLib.SpriteImage_Static):  # 145
    def __init__(self, parent):
        super().__init__(
            parent,
            1.5,
            offset=(-16, -9)
        )

        img = ImageCache['FloatingBarrel']
        self.width = (img.width() / self.scale) + 1
        self.height = (img.height() / self.scale) + 2

        self.aux.append(SLib.AuxiliaryImage(parent, img.width(), img.height()))
        self.aux[0].image = img

        path = QtGui.QPainterPath()
        path.lineTo(QtCore.QPointF(self.width * 1.5, 0))

        self.aux.append(SLib.AuxiliaryPainterPath(parent, path, img.width(),
                                                  SLib.OutlinePen.width(), 0, 36))

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('FloatingBarrel', 'barrel_floating.png')

    def dataChanged(self):
        # Don't let SLib.SpriteImage_Static reset size
        SLib.SpriteImage.dataChanged(self)


class SpriteImage_Coin(SLib.SpriteImage_StaticMultiple):  # 147
    @staticmethod
    def loadImages():
        if 'CoinF' in ImageCache: return

        pix = QtGui.QPixmap(24, 24)
        pix.fill(Qt.transparent)
        paint = QtGui.QPainter(pix)
        paint.setOpacity(0.9)
        paint.drawPixmap(0, 0, SLib.GetImg('iceblock00.png'))
        paint.setOpacity(0.6)
        paint.drawPixmap(0, 0, ImageCache['Coin'])
        del paint
        ImageCache['CoinF'] = pix

        ImageCache['CoinBubble'] = SLib.GetImg('coin_bubble.png')

    def dataChanged(self):
        type = self.parent.spritedata[5] & 0xF

        if type == 0:
            self.image = ImageCache['Coin']
            self.offset = (0, 0)
        elif type == 0xF:
            self.image = ImageCache['CoinF']
            self.offset = (0, 0)
        elif type in (1, 2, 4):
            self.image = ImageCache['CoinBubble']
            self.offset = (-4, -4)
        else:
            self.image = ImageCache['SpecialCoin']
            self.offset = (0, 0)

        super().dataChanged()


class SpriteImage_Spring(SLib.SpriteImage_Static):  # 148
    def __init__(self, parent):
        super().__init__(
            parent,
            1.5,
            ImageCache['Spring'],
        )

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('Spring', 'spring.png')

    def dataChanged(self):
        offset = (self.parent.spritedata[5] >> 4) & 1
        self.xOffset = 8 if offset else 0

        super().dataChanged()


class SpriteImage_RotationControllerSpinning(SLib.SpriteImage):  # 149
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.parent.setZValue(100000)


class SpriteImage_QSwitchUnused(common.SpriteImage_Switch):  # 153
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.switchType = 'Q'

    def dataChanged(self):
        self.offset = (0, 0)
        super().dataChanged()


class SpriteImage_RedCoinRing(SLib.SpriteImage):  # 156
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

        self.aux.append(SLib.AuxiliaryImage(parent, 76, 95))
        self.aux[0].image = ImageCache['RedCoinRing']
        self.aux[0].setPos(-10, -15)
        self.aux[0].hover = False

        self.dimensions = (-10, -8, 37, 48)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('RedCoinRing', 'redcoinring.png')

    def dataChanged(self):
        shifted = self.parent.spritedata[5] & 1
        self.xOffset = -2 if shifted else -10

        super().dataChanged()


class SpriteImage_BigBrick(SLib.SpriteImage_StaticMultiple):  # 157
    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('BigBrick', 'big_brick.png')
        SLib.loadIfNotInImageCache('ShipKey', 'ship_key.png')
        SLib.loadIfNotInImageCache('5Coin', '5_coin.png')

        if 'YoshiFire' not in ImageCache:
            pix = QtGui.QPixmap(48, 24)
            pix.fill(Qt.transparent)
            paint = QtGui.QPainter(pix)
            paint.drawPixmap(0, 0, ImageCache['BlockContents'][9])
            paint.drawPixmap(24, 0, ImageCache['BlockContents'][3])
            del paint
            ImageCache['YoshiFire'] = pix

        for power in range(16):
            if power in (0, 8, 12, 13):
                ImageCache['BigBrick%d' % power] = ImageCache['BigBrick']
                continue

            x = y = 24
            overlay = ImageCache['BlockContents'][power]
            if power == 9:
                overlay = ImageCache['YoshiFire']
                x = 12
            elif power == 10:
                overlay = ImageCache['5Coin']
            elif power == 14:
                overlay = ImageCache['ShipKey']
                x, y = 22, 18

            new = QtGui.QPixmap(ImageCache['BigBrick'])
            paint = QtGui.QPainter(new)
            paint.drawPixmap(x, y, overlay)
            del paint
            ImageCache['BigBrick%d' % power] = new

    def dataChanged(self):

        power = self.parent.spritedata[5] & 0xF
        self.image = ImageCache['BigBrick%d' % power]
        super().dataChanged()


class SpriteImage_FireSnake(SLib.SpriteImage_StaticMultiple):  # 158
    def __init__(self, parent):
        super().__init__(parent, 1.5)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('FireSnakeWait', 'fire_snake_0.png')
        SLib.loadIfNotInImageCache('FireSnake', 'fire_snake_1.png')

    def dataChanged(self):

        move = self.parent.spritedata[5] & 15
        if move == 1:
            del self.size
            self.yOffset = 0
            self.image = ImageCache['FireSnakeWait']
        else:
            self.size = (20, 32)
            self.yOffset = -16
            self.image = ImageCache['FireSnake']

        super().dataChanged()


class SpriteImage_UnusedBlockPlatform2(SpriteImage_UnusedBlockPlatform):  # 160
    def dataChanged(self):
        self.width = ((self.parent.spritedata[4] & 0xF) + 1) * 16
        self.height = ((self.parent.spritedata[4] >> 4) + 1) * 16
        super().dataChanged()


class SpriteImage_PipeBubbles(SLib.SpriteImage_StaticMultiple):  # 161
    @staticmethod
    def loadImages():
        if 'PipeBubblesU' in ImageCache: return
        transform90 = QtGui.QTransform()
        transform180 = QtGui.QTransform()
        transform270 = QtGui.QTransform()
        transform90.rotate(90)
        transform180.rotate(180)
        transform270.rotate(270)

        image = SLib.GetImg('pipe_bubbles.png', True)
        ImageCache['PipeBubbles' + 'U'] = QtGui.QPixmap.fromImage(image)
        ImageCache['PipeBubbles' + 'R'] = QtGui.QPixmap.fromImage(image.transformed(transform90))
        ImageCache['PipeBubbles' + 'D'] = QtGui.QPixmap.fromImage(image.transformed(transform180))
        ImageCache['PipeBubbles' + 'L'] = QtGui.QPixmap.fromImage(image.transformed(transform270))

    def dataChanged(self):

        direction = self.parent.spritedata[5] & 15
        if direction == 0 or direction > 3:
            self.dimensions = (0, -52, 32, 53)
            direction = 'U'
        elif direction == 1:
            self.dimensions = (0, 16, 32, 53)
            direction = 'D'
        elif direction == 2:
            self.dimensions = (16, -16, 53, 32)
            direction = 'R'
        elif direction == 3:
            self.dimensions = (-52, -16, 53, 32)
            direction = 'L'

        self.image = ImageCache['PipeBubbles%s' % direction]

        super().dataChanged()


class SpriteImage_BlockTrain(SLib.SpriteImage):  # 166
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('BlockTrain', 'block_train.png')

    def dataChanged(self):
        super().dataChanged()
        length = self.parent.spritedata[5] & 15
        self.width = (length + 3) * 16

    def paint(self, painter):
        super().paint(painter)

        endpiece = ImageCache['BlockTrain']
        painter.drawPixmap(0, 0, endpiece)
        painter.drawTiledPixmap(24, 0, int((self.width * 1.5) - 48), 24, ImageCache['BlockTrain'])
        painter.drawPixmap(int((self.width * 1.5) - 24), 0, endpiece)


class SpriteImage_ScrewMushroomWithBolt(SpriteImage_ScrewMushroom):  # 172
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.hasBolt = True


class SpriteImage_OneWayGate(SLib.SpriteImage_StaticMultiple):  # 174
    @staticmethod
    def loadImages():
        if '1WayGate00' in ImageCache: return

        # This loop generates all 1-way gate images from a single image
        gate = SLib.GetImg('1_way_gate.png', True)
        for flip in (0, 1):
            for direction in range(4):
                if flip:
                    newgate = QtGui.QPixmap.fromImage(gate.mirrored(True, False))
                else:
                    newgate = QtGui.QPixmap.fromImage(gate)

                width = 24
                height = 60  # constants, from the PNG
                xsize = width if direction in (0, 1) else height
                ysize = width if direction in (2, 3) else height
                if direction == 0:
                    rotValue = 0
                    xpos = 0
                    ypos = 0
                elif direction == 1:
                    rotValue = 180
                    xpos = -width
                    ypos = -height
                elif direction == 2:
                    rotValue = 270
                    xpos = -width
                    ypos = 0
                elif direction == 3:
                    rotValue = 90
                    xpos = 0
                    ypos = -height

                dest = QtGui.QPixmap(xsize, ysize)
                dest.fill(Qt.transparent)
                p = QtGui.QPainter(dest)
                p.rotate(rotValue)
                p.drawPixmap(xpos, ypos, newgate)
                del p

                ImageCache['1WayGate%d%d' % (flip, direction)] = dest

    def dataChanged(self):

        flag = (self.parent.spritedata[5] >> 4) & 1
        direction = self.parent.spritedata[5] & 3
        self.image = ImageCache['1WayGate%d%d' % (flag, direction)]

        if direction > 3: direction = 3
        self.offset = (
            (0, -24),
            (0, 0),
            (-24, 0),
            (0, 0),
        )[direction]

        super().dataChanged()


class SpriteImage_FlyingQBlock(SLib.SpriteImage):  # 175
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

        self.dimensions = (-12, -16, 42, 32)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('FlyingQBlock', 'flying_qblock.png')

    def paint(self, painter):
        super().paint(painter)

        theme = self.parent.spritedata[4] >> 4
        content = self.parent.spritedata[5] & 0xF

        if theme > 3:
            theme = 0

        if content == 2:
            content = 17
        elif content in (8, 9, 10, 12, 13, 14):
            content = 0

        painter.drawPixmap(0, 0, ImageCache['FlyingQBlock'])
        painter.drawPixmap(18, 23, ImageCache['Blocks'][theme])
        painter.drawPixmap(18, 23, ImageCache['BlockContents'][content])


class SpriteImage_ScalePlatform(SLib.SpriteImage):  # 178
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.offset = (0, -8)
        self.spritebox.shown = False

    @staticmethod
    def loadImages():
        if 'WoodenPlatformL' not in ImageCache:
            ImageCache['WoodenPlatformL'] = SLib.GetImg('wood_platform_left.png')
            ImageCache['WoodenPlatformM'] = SLib.GetImg('wood_platform_middle.png')
            ImageCache['WoodenPlatformR'] = SLib.GetImg('wood_platform_right.png')
        if 'ScaleRopeH' not in ImageCache:
            ImageCache['ScaleRopeH'] = SLib.GetImg('scale_rope_horz.png')
            ImageCache['ScaleRopeV'] = SLib.GetImg('scale_rope_vert.png')
            ImageCache['ScalePulley'] = SLib.GetImg('scale_pulley.png')

    def dataChanged(self):
        super().dataChanged()

        info1 = self.parent.spritedata[4]
        info2 = self.parent.spritedata[5]
        self.parent.platformWidth = (info1 & 0xF0) >> 4
        if self.parent.platformWidth > 12: self.parent.platformWidth = -1

        self.parent.ropeLengthLeft = info1 & 0xF
        self.parent.ropeLengthRight = (info2 & 0xF0) >> 4
        self.parent.ropeWidth = info2 & 0xF

        ropeWidth = self.parent.ropeWidth * 16
        platformWidth = (self.parent.platformWidth + 3) * 16
        self.width = ropeWidth + platformWidth

        maxRopeHeight = max(self.parent.ropeLengthLeft, self.parent.ropeLengthRight)
        self.height = maxRopeHeight * 16 + 19
        if maxRopeHeight == 0: self.height += 8

        self.xOffset = -(self.parent.platformWidth + 3) * 8

    def paint(self, painter):
        super().paint(painter)

        # this is FUN!! (not)
        ropeLeft = int(self.parent.ropeLengthLeft * 24 + 4)
        if self.parent.ropeLengthLeft == 0: ropeLeft += 12

        ropeRight = int(self.parent.ropeLengthRight * 24 + 4)
        if self.parent.ropeLengthRight == 0: ropeRight += 12

        ropeWidth = int(self.parent.ropeWidth * 24 + 8)
        platformWidth = int((self.parent.platformWidth + 3) * 24)

        ropeX = int(platformWidth / 2 - 4)

        painter.drawTiledPixmap(ropeX + 8, 0, ropeWidth - 16, 8, ImageCache['ScaleRopeH'])

        ropeVertImage = ImageCache['ScaleRopeV']
        painter.drawTiledPixmap(ropeX, 8, 8, ropeLeft - 8, ropeVertImage)
        painter.drawTiledPixmap(ropeX + ropeWidth - 8, 8, 8, ropeRight - 8, ropeVertImage)

        pulleyImage = ImageCache['ScalePulley']
        painter.drawPixmap(ropeX, 0, pulleyImage)
        painter.drawPixmap(ropeX + ropeWidth - 20, 0, pulleyImage)

        platforms = [(0, ropeLeft), (ropeX + ropeWidth - int(platformWidth / 2) - 4, ropeRight)]
        for x, y in platforms:
            painter.drawPixmap(x, y, ImageCache['WoodenPlatformL'])
            painter.drawTiledPixmap(x + 24, y, (platformWidth - 48), 24, ImageCache['WoodenPlatformM'])
            painter.drawPixmap(x + platformWidth - 24, y, ImageCache['WoodenPlatformR'])


class SpriteImage_SpecialExit(SLib.SpriteImage):  # 179
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.aux.append(SLib.AuxiliaryRectOutline(parent, 0, 0))

    def dataChanged(self):
        super().dataChanged()

        w = (self.parent.spritedata[4] & 15) + 1
        h = (self.parent.spritedata[5] >> 4) + 1
        if w == 1 and h == 1:  # no point drawing a 1x1 outline behind the self.parent
            self.aux[0].setSize(0, 0)
            return
        self.aux[0].setSize(w * 24, h * 24)


class SpriteImage_EventDoor(SpriteImage_Door):  # 182
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.alpha = 0.5


class SpriteImage_TileEvent(common.SpriteImage_TileEvent):  # 191
    def __init__(self, parent):
        super().__init__(parent)
        self.notAllowedTypes = (2, 5, 7)

    def getTileFromType(self, type_):
        if type_ == 0:
            return SLib.GetTile(55)

        if type_ == 1:
            return SLib.GetTile(48)

        if type_ == 3:
            return SLib.GetTile(52)

        if type_ == 4:
            return SLib.GetTile(51)

        if type_ == 6:
            return SLib.GetTile(45)

        if type_ == 12:
            return SLib.GetTile(256 * 3 + 67)

        if type_ == 14:
            return SLib.GetTile(256)

        return None


class SpriteImage_LarryKoopaCastleBoss(SLib.SpriteImage):  # 192
    def __init__(self, parent):
        super().__init__(parent)
        self.parent.setZValue(24999)

        self.aux.append(SLib.AuxiliaryImage(parent, 528, 240))
        self.aux[0].image = ImageCache['LarryKoopaCastleBoss']
        self.aux[0].setPos(48, 192)
        self.aux.append(SLib.AuxiliaryRectOutline(parent, 24, 24, 0, 288))

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('LarryKoopaCastleBoss', 'larry_castle_boss.png')


class SpriteImage_Urchin(SLib.SpriteImage_Static):  # 193
    def __init__(self, parent):
        super().__init__(
            parent,
            1.5,
            ImageCache['Urchin'],
            (-12, -14),
        )

        self.aux.append(SLib.AuxiliaryTrackObject(
            parent, 16, 16, SLib.AuxiliaryTrackObject.Vertical
        ))
        self.aux[0].setPos(self.width * 0.75 - 12, self.height * 0.75 - 12)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('Urchin', 'urchin.png')

    def dataChanged(self):
        super().dataChanged()

        distance = ((self.parent.spritedata[5] & 0xF0) << 1) | 8
        horizontal = (self.parent.spritedata[5] & 1) == 1

        if horizontal:
            self.aux[0].direction = SLib.AuxiliaryTrackObject.Horizontal
            self.aux[0].setSize(distance + 8, 16)
            self.aux[0].setPos((self.width - distance) * 0.75 - 8, self.height * 0.75 - 12)
        else:
            self.aux[0].direction = SLib.AuxiliaryTrackObject.Vertical
            self.aux[0].setSize(16, distance + 8)
            self.aux[0].setPos(self.width * 0.75 - 12, (self.height - distance) * 0.75 - 8)


class SpriteImage_MegaUrchin(SLib.SpriteImage_Static):  # 194
    def __init__(self, parent):
        super().__init__(
            parent,
            1.5,
            ImageCache['MegaUrchin'],
            (-48, -46),
        )

        self.aux.append(SLib.AuxiliaryTrackObject(
            parent, 16, 16, SLib.AuxiliaryTrackObject.Vertical
        ))
        self.aux[0].setPos(self.width * 0.75 - 12, self.height * 0.75 - 12)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('MegaUrchin', 'mega_urchin.png')

    def dataChanged(self):
        super().dataChanged()

        distance = ((self.parent.spritedata[5] & 0xF0) << 1) | 8
        horizontal = (self.parent.spritedata[5] & 1) == 1

        if horizontal:
            self.aux[0].direction = SLib.AuxiliaryTrackObject.Horizontal
            self.aux[0].setSize(distance + 8, 16)
            self.aux[0].setPos((self.width - distance) * 0.75 - 8, self.height * 0.75 - 12)
        else:
            self.aux[0].direction = SLib.AuxiliaryTrackObject.Vertical
            self.aux[0].setSize(16, distance + 8)
            self.aux[0].setPos(self.width * 0.75 - 12, (self.height - distance) * 0.75 - 8)


class SpriteImage_HuckitCrab(SLib.SpriteImage_StaticMultiple):  # 195
    @staticmethod
    def loadImages():
        if 'HuckitCrabR' in ImageCache: return
        Huckitcrab = SLib.GetImg('huckit_crab.png', True)
        ImageCache['HuckitCrabL'] = QtGui.QPixmap.fromImage(Huckitcrab)
        ImageCache['HuckitCrabR'] = QtGui.QPixmap.fromImage(Huckitcrab.mirrored(True, False))

    def dataChanged(self):
        info = self.parent.spritedata[5]

        if info == 1:
            self.image = ImageCache['HuckitCrabR']
            self.xOffset = 0
        else:
            if info == 13:
                self.image = ImageCache['HuckitCrabR']
                self.xOffset = 0
            else:
                self.image = ImageCache['HuckitCrabL']
                self.xOffset = -16

        super().dataChanged()


class SpriteImage_Fishbones(SLib.SpriteImage_StaticMultiple):  # 196
    def __init__(self, parent):
        super().__init__(
            parent,
            1.5,
            ImageCache['FishbonesL'],
            (0, -2)
        )
        self.aux.append(SLib.AuxiliaryTrackObject(
            parent, 16, 16, SLib.AuxiliaryTrackObject.Horizontal
        ))

    def dataChanged(self):

        direction = self.parent.spritedata[5] >> 4
        distance = self.parent.spritedata[5] & 0xF

        # distance values > 1 result in a distance of 9
        if distance == 0:
            distance = 5
        elif distance == 1:
            distance = 7
        else:
            distance = 9

        self.aux[0].setSize(distance * 16, 16)
        self.aux[0].setPos(distance * -12 + 12, 2)

        if direction == 1:
            self.image = ImageCache['FishbonesR']
        else:
            self.image = ImageCache['FishbonesL']

        super().dataChanged()

    @staticmethod
    def loadImages():
        if 'FishbonesL' in ImageCache: return
        Fishbones = SLib.GetImg('fishbones.png', True)
        ImageCache['FishbonesL'] = QtGui.QPixmap.fromImage(Fishbones)
        ImageCache['FishbonesR'] = QtGui.QPixmap.fromImage(Fishbones.mirrored(True, False))


class SpriteImage_Clam(SLib.SpriteImage_StaticMultiple):  # 197
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.offset = (-29, -54)

    @staticmethod
    def loadImages():
        if 'ClamEmpty' in ImageCache: return

        if 'PSwitch' not in ImageCache:
            p = SLib.GetImg('p_switch.png', True)
            ImageCache['PSwitch'] = QtGui.QPixmap.fromImage(p)
            ImageCache['PSwitchU'] = QtGui.QPixmap.fromImage(p.mirrored(True, True))

        SLib.loadIfNotInImageCache('ClamEmpty', 'clam.png')

        overlays = (
            (26, 22, 'Star', ImageCache['StarCoin']),
            (40, 42, '1Up', ImageCache['BlockContents'][11]),
            (40, 42, 'PSwitch', ImageCache['PSwitch']),
            (40, 42, 'PSwitchU', ImageCache['PSwitchU']),
        )
        for x, y, clamName, overlayImage in overlays:
            newPix = QtGui.QPixmap(ImageCache['ClamEmpty'])
            painter = QtGui.QPainter(newPix)
            painter.setOpacity(0.6)
            painter.drawPixmap(x, y, overlayImage)
            del painter
            ImageCache['Clam' + clamName] = newPix

        # 2 coins special case
        newPix = QtGui.QPixmap(ImageCache['ClamEmpty'])
        painter = QtGui.QPainter(newPix)
        painter.setOpacity(0.6)
        painter.drawPixmap(28, 42, ImageCache['Coin'])
        painter.drawPixmap(52, 42, ImageCache['Coin'])
        del painter
        ImageCache['Clam2Coin'] = newPix

    def dataChanged(self):

        holds = self.parent.spritedata[5] & 0xF
        switchdir = self.parent.spritedata[4] & 0xF

        holdsStr = 'Empty'
        if holds == 1:
            holdsStr = 'Star'
        elif holds == 2:
            holdsStr = '2Coin'
        elif holds == 3:
            holdsStr = '1Up'
        elif holds == 4:
            if switchdir == 1:
                holdsStr = 'PSwitchU'
            else:
                holdsStr = 'PSwitch'

        self.image = ImageCache['Clam' + holdsStr]

        super().dataChanged()


class SpriteImage_GiantGoomba(SLib.SpriteImage_Static):  # 198
    def __init__(self, parent):
        super().__init__(
            parent,
            1.5,
            ImageCache['GiantGoomba'],
            (-6, -19),
        )

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('GiantGoomba', 'giant_goomba.png')


class SpriteImage_Icicle(SLib.SpriteImage_StaticMultiple):  # 201
    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('IcicleSmallS', 'icicle_small_static.png')
        SLib.loadIfNotInImageCache('IcicleLargeS', 'icicle_large_static.png')

    def dataChanged(self):

        size = self.parent.spritedata[5] & 1
        if size == 0:
            self.image = ImageCache['IcicleSmallS']
        else:
            self.image = ImageCache['IcicleLargeS']

        super().dataChanged()


class SpriteImage_GiantBubbleNormal(SpriteImage_GiantBubble):  # 205
    pass


class SpriteImage_Zoom(SLib.SpriteImage):  # 206
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.aux.append(SLib.AuxiliaryRectOutline(parent, 0, 0))

    def dataChanged(self):
        super().dataChanged()

        w = self.parent.spritedata[5]
        h = self.parent.spritedata[4]
        if w == 0 and h == 0:  # no point drawing a 1x1 outline behind the self.parent
            self.aux[0].setSize(0, 0, 0, 0)
            return
        self.aux[0].setSize(w * 24, h * 24, 0, 24 - (h * 24))


class SpriteImage_QBlock(SpriteImage_Block):  # 207
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.tilenum = 49


class SpriteImage_QBlockUnused(SpriteImage_Block):  # 208
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.tilenum = 49
        self.eightIsMushroom = True
        self.twelveIsMushroom = True


class SpriteImage_BrickBlock(SpriteImage_Block):  # 209
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.tilenum = 48


class SpriteImage_BowserJr1stController(SLib.SpriteImage):  # 211
    def __init__(self, parent):
        super().__init__(parent)
        self.parent.setZValue(24999)

        self.aux.append(SLib.AuxiliaryImage(parent, 672, 80))
        self.aux[0].image = ImageCache['BowserJr1stController']
        self.aux[0].setPos(-504, -55)

        self.aux.append(SLib.AuxiliaryRectOutline(parent, 24, 24, -504, -312))

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('BowserJr1stController', 'boss_controller_bowserjr_1.png')


class SpriteImage_RollingHill(SLib.SpriteImage):  # 212
    RollingHillSizes = [0, 18 * 16, 32 * 16, 50 * 16, 64 * 16, 10 * 16, 14 * 16, 20 * 16, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self, parent):
        super().__init__(parent, 1.5)

        size = (self.parent.spritedata[3] >> 4) & 0xF
        realSize = self.RollingHillSizes[size]

        self.aux.append(SLib.AuxiliaryCircleOutline(parent, realSize))

    def dataChanged(self):
        super().dataChanged()

        size = (self.parent.spritedata[3] >> 4) & 0xF
        if size != 0:
            realSize = self.RollingHillSizes[size]
        else:
            adjust = self.parent.spritedata[4]
            realSize = 32 * (adjust + 1)

        self.aux[0].setSize(realSize)
        self.aux[0].update()


class SpriteImage_Poison(SpriteImage_LiquidOrFog):  # 216
    def __init__(self, parent):
        super().__init__(parent)

        self.crest = ImageCache['LiquidPoisonCrest']
        self.mid = ImageCache['LiquidPoison']
        self.rise = ImageCache['LiquidPoisonRiseCrest']
        self.riseCrestless = ImageCache['LiquidPoisonRise']

        self.top = self.parent.objy

    @staticmethod
    def loadImages():
        if 'LiquidPoison' in ImageCache: return
        ImageCache['LiquidPoison'] = SLib.GetImg('liquid_poison.png')
        ImageCache['LiquidPoisonCrest'] = SLib.GetImg('liquid_poison_crest.png')
        ImageCache['LiquidPoisonRise'] = SLib.GetImg('liquid_poison_rise.png')
        ImageCache['LiquidPoisonRiseCrest'] = SLib.GetImg('liquid_poison_rise_crest.png')

    def dataChanged(self):
        self.locId = self.parent.spritedata[5] & 0x7F
        self.drawCrest = self.parent.spritedata[4] & 8 == 0

        self.risingHeight = (self.parent.spritedata[3] & 0xF) << 4
        self.risingHeight |= self.parent.spritedata[4] >> 4
        if self.parent.spritedata[2] & 15 > 7:  # falling
            self.risingHeight = -self.risingHeight

        super().dataChanged()

    def positionChanged(self):
        self.top = self.parent.objy
        super().positionChanged()


class SpriteImage_LineBlock(common.SpriteImage_LineBlock):  # 219

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('LineBlock', 'lineblock.png')

    def dataChanged(self):
        self.setLineBlockImage(ImageCache['LineBlock'])

        super().dataChanged()


class SpriteImage_InvisibleBlock(SpriteImage_Block):  # 221
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.eightIsMushroom = True
        self.tilenum = 0x200 * 4


class SpriteImage_SpringBlock(SLib.SpriteImage_StaticMultiple):  # 223
    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('SpringBlock1', 'spring_block.png')
        SLib.loadIfNotInImageCache('SpringBlock2', 'spring_block_alt.png')

    def dataChanged(self):
        type = self.parent.spritedata[5] & 1
        self.image = ImageCache['SpringBlock2'] if type else ImageCache['SpringBlock1']

        super().dataChanged()


class SpriteImage_JumboRay(SLib.SpriteImage_StaticMultiple):  # 224
    @staticmethod
    def loadImages():
        if 'JumboRayL' in ImageCache: return
        Ray = SLib.GetImg('jumbo_ray.png', True)
        ImageCache['JumboRayL'] = QtGui.QPixmap.fromImage(Ray)
        ImageCache['JumboRayR'] = QtGui.QPixmap.fromImage(Ray.mirrored(True, False))

    def dataChanged(self):

        flyleft = self.parent.spritedata[4] & 15
        if flyleft:
            self.xOffset = 0
            self.image = ImageCache['JumboRayL']
        else:
            self.xOffset = -152
            self.image = ImageCache['JumboRayR']

        super().dataChanged()


class SpriteImage_GiantBubbleUnused(SpriteImage_GiantBubble):  # 226
    pass


class SpriteImage_PipeCannon(SLib.SpriteImage):  # 227
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

        # self.aux[0] is the pipe image
        self.aux.append(SLib.AuxiliaryImage(parent, 24, 24))
        self.aux[0].hover = False

        # self.aux[1] is the trajectory indicator
        self.aux.append(SLib.AuxiliaryPainterPath(parent, QtGui.QPainterPath(), 24, 24))
        self.aux[1].fillFlag = False

        self.aux[0].setZValue(self.aux[1].zValue() + 1)

        self.size = (32, 64)

    @staticmethod
    def loadImages():
        if 'PipeCannon0' in ImageCache: return
        for i in range(7):
            ImageCache['PipeCannon%d' % i] = SLib.GetImg('pipe_cannon_%d.png' % i)

    def dataChanged(self):
        super().dataChanged()

        fireDirection = (self.parent.spritedata[5] & 0xF) % 7

        self.aux[0].image = ImageCache['PipeCannon%d' % (fireDirection)]

        if fireDirection == 0:
            # 30 deg to the right
            self.aux[0].setSize(84, 101, 0, -5)
            path = QtGui.QPainterPath(QtCore.QPoint(0, 184))
            path.cubicTo(QtCore.QPoint(152, -24), QtCore.QPoint(168, -24), QtCore.QPoint(264, 48))
            path.lineTo(QtCore.QPoint(480, 216))
            self.aux[1].setSize(480, 216, 24, -120)
        elif fireDirection == 1:
            # 30 deg to the left
            self.aux[0].setSize(85, 101, -36, -5)
            path = QtGui.QPainterPath(QtCore.QPoint(480 - 0, 184))
            path.cubicTo(QtCore.QPoint(480 - 152, -24), QtCore.QPoint(480 - 168, -24), QtCore.QPoint(480 - 264, 48))
            path.lineTo(QtCore.QPoint(480 - 480, 216))
            self.aux[1].setSize(480, 216, -480 + 24, -120)
        elif fireDirection == 2:
            # 15 deg to the right
            self.aux[0].setSize(60, 102, 0, -6)
            path = QtGui.QPainterPath(QtCore.QPoint(0, 188))
            path.cubicTo(QtCore.QPoint(36, -36), QtCore.QPoint(60, -36), QtCore.QPoint(96, 84))
            path.lineTo(QtCore.QPoint(144, 252))
            self.aux[1].setSize(144, 252, 30, -156)
        elif fireDirection == 3:
            # 15 deg to the left
            self.aux[0].setSize(61, 102, -12, -6)
            path = QtGui.QPainterPath(QtCore.QPoint(144 - 0, 188))
            path.cubicTo(QtCore.QPoint(144 - 36, -36), QtCore.QPoint(144 - 60, -36), QtCore.QPoint(144 - 96, 84))
            path.lineTo(QtCore.QPoint(144 - 144, 252))
            self.aux[1].setSize(144, 252, -144 + 18, -156)
        elif fireDirection == 4:
            # Straight up
            self.aux[0].setSize(135, 132, -43, -35)
            path = QtGui.QPainterPath(QtCore.QPoint(26, 0))
            path.lineTo(QtCore.QPoint(26, 656))
            self.aux[1].setSize(48, 656, 0, -632)
        elif fireDirection == 5:
            # 45 deg to the right
            self.aux[0].setSize(90, 98, 0, -1)
            path = QtGui.QPainterPath(QtCore.QPoint(0, 320))
            path.lineTo(QtCore.QPoint(264, 64))
            path.cubicTo(QtCore.QPoint(348, -14), QtCore.QPoint(420, -14), QtCore.QPoint(528, 54))
            path.lineTo(QtCore.QPoint(1036, 348))
            self.aux[1].setSize(1036, 348, 24, -252)
        elif fireDirection == 6:
            # 45 deg to the left
            self.aux[0].setSize(91, 98, -42, -1)
            path = QtGui.QPainterPath(QtCore.QPoint(1036 - 0, 320))
            path.lineTo(QtCore.QPoint(1036 - 264, 64))
            path.cubicTo(QtCore.QPoint(1036 - 348, -14), QtCore.QPoint(1036 - 420, -14), QtCore.QPoint(1036 - 528, 54))
            path.lineTo(QtCore.QPoint(1036 - 1036, 348))
            self.aux[1].setSize(1036, 348, -1036 + 24, -252)
        self.aux[1].setPath(path)


class SpriteImage_ExtendShroom(SLib.SpriteImage):  # 228
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False
        self.parent.setZValue(24999)

    @staticmethod
    def loadImages():
        if 'ExtendShroomB' in ImageCache: return
        ImageCache['ExtendShroomB'] = SLib.GetImg('extend_shroom_big.png')
        ImageCache['ExtendShroomS'] = SLib.GetImg('extend_shroom_small.png')
        ImageCache['ExtendShroomC'] = SLib.GetImg('extend_shroom_cont.png')
        ImageCache['ExtendShroomStem'] = SLib.GetImg('extend_shroom_stem.png')

    def dataChanged(self):

        props = self.parent.spritedata[5]
        size = self.parent.spritedata[4] & 1
        self.start = (props & 0x10) >> 4
        stemlength = props & 0xF

        if size == 0:  # big
            self.image = ImageCache['ExtendShroomB']
            self.width = 160
        else:  # small
            self.image = ImageCache['ExtendShroomS']
            self.width = 96

        if self.start == 0:  # contracted
            self.indicator, self.image = self.image, ImageCache['ExtendShroomC']

        self.xOffset = 8 - (self.width / 2)
        self.height = (stemlength * 16) + 48

        super().dataChanged()

    def paint(self, painter):
        super().paint(painter)

        if self.start == 0:  # contracted, so paint indicator
            painter.save()
            painter.setOpacity(0.5)
            painter.drawPixmap(0, 0, self.indicator)
            painter.restore()

            painter.drawPixmap(int(self.width * 1.5 / 2 - 24), 0, self.image)
        else:
            painter.drawPixmap(0, 0, self.image)

        painter.drawTiledPixmap(
            int((self.width * 1.5) / 2 - 14),
            48,
            28,
            int((self.height * 1.5) - 48),
            ImageCache['ExtendShroomStem'],
        )


class SpriteImage_WiggleShroom(SLib.SpriteImage):  # 231
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False
        self.parent.setZValue(24999)
        self.aux.append(SLib.AuxiliaryTrackObject(parent, 16, 16, SLib.AuxiliaryTrackObject.Vertical))

    @staticmethod
    def loadImages():
        if 'WiggleShroomL' in ImageCache: return
        ImageCache['WiggleShroomL'] = SLib.GetImg('wiggle_shroom_left.png')
        ImageCache['WiggleShroomM'] = SLib.GetImg('wiggle_shroom_middle.png')
        ImageCache['WiggleShroomR'] = SLib.GetImg('wiggle_shroom_right.png')
        ImageCache['WiggleShroomS'] = SLib.GetImg('wiggle_shroom_stem.png')

    def dataChanged(self):
        super().dataChanged()
        width = (self.parent.spritedata[4] & 0xF0) >> 4
        long = (self.parent.spritedata[3] >> 2) & 1
        extends = (self.parent.spritedata[3] >> 5) & 1
        distance = self.parent.spritedata[3] & 3  # this is also the stem length

        self.xOffset = -(width * 8) - 20
        self.width = (width * 16) + 56
        self.wiggleleft = ImageCache['WiggleShroomL']
        self.wigglemiddle = ImageCache['WiggleShroomM']
        self.wiggleright = ImageCache['WiggleShroomR']
        self.wigglestem = ImageCache['WiggleShroomS']

        if extends:
            self.aux[0].setPos((self.width * 0.75) - 12, (-distance * 24))
            self.aux[0].setSize(16, (distance * 32))
            if long:
                self.height = 96
            else:
                self.height = 64
        else:
            self.aux[0].setSize(0, 0)
            self.height = (distance * 16) + 64

    def paint(self, painter):
        super().paint(painter)

        xsize = self.width * 1.5
        painter.drawPixmap(0, 0, self.wiggleleft)
        painter.drawTiledPixmap(18, 0, int(xsize - 36), 24, self.wigglemiddle)
        painter.drawPixmap(int(xsize - 18), 0, self.wiggleright)
        painter.drawTiledPixmap(int((xsize / 2) - 12), 24, 24, int((self.height * 1.5) - 24), self.wigglestem)


class SpriteImage_Bulber(SLib.SpriteImage):  # 233
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

        self.aux.append(SLib.AuxiliaryImage(parent, 243, 248))
        self.aux[0].image = ImageCache['Bulber']
        self.aux[0].setPos(-8, 0)

        self.dimensions = (2, -4, 59, 50)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('Bulber', 'bulber.png')


class SpriteImage_RotControlledPipe(SpriteImage_Pipe):  # 254
    def dataChanged(self):
        self.length1 = self.length2 = (self.parent.spritedata[4] >> 4) + 2
        dir = self.parent.spritedata[4] & 3
        self.direction = 'URDL'[dir]
        super().dataChanged()


class SpriteImage_RotatingQBlock(SpriteImage_Block):  # 255
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.tilenum = 49
        self.contentsNybble = 4
        self.twelveIsMushroom = True
        self.rotates = True


class SpriteImage_RotatingBrickBlock(SpriteImage_Block):  # 256
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.tilenum = 48
        self.contentsNybble = 4
        self.twelveIsMushroom = True
        self.rotates = True


class SpriteImage_MoveWhenOnMetalLavaBlock(SLib.SpriteImage_StaticMultiple):  # 257
    @staticmethod
    def loadImages():
        if 'MetalLavaBlock0' in ImageCache: return
        ImageCache['MetalLavaBlock0'] = SLib.GetImg('lava_iron_block_0.png')
        ImageCache['MetalLavaBlock1'] = SLib.GetImg('lava_iron_block_1.png')
        ImageCache['MetalLavaBlock2'] = SLib.GetImg('lava_iron_block_2.png')

    def dataChanged(self):
        size = (self.parent.spritedata[5] & 0xF) % 3
        self.image = ImageCache['MetalLavaBlock%d' % size]

        super().dataChanged()


class SpriteImage_RegularDoor(SpriteImage_Door):  # 259
    pass


class SpriteImage_MovementController_TwoWayLine(SLib.SpriteImage):  # 260
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.aux.append(SLib.AuxiliaryTrackObject(parent, 16, 16, SLib.AuxiliaryTrackObject.Horizontal))

    def dataChanged(self):
        super().dataChanged()

        direction = self.parent.spritedata[3] & 3
        distance = (self.parent.spritedata[5] >> 4) + 1

        if direction <= 1:  # horizontal
            self.aux[0].direction = 1
            self.aux[0].setSize(distance * 16, 16)
        else:  # vertical
            self.aux[0].direction = 2
            self.aux[0].setSize(16, distance * 16)

        if direction == 0 or direction == 3:  # right, down
            self.aux[0].setPos(0, 0)
        elif direction == 1:  # left
            self.aux[0].setPos((-distance * 24) + 24, 0)
        elif direction == 2:  # up
            self.aux[0].setPos(0, (-distance * 24) + 24)


class SpriteImage_OldStoneBlock_MovementControlled(SpriteImage_OldStoneBlock):  # 261
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.hasMovementAux = False


class SpriteImage_PoltergeistItem(SLib.SpriteImage):  # 262
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

        self.aux.append(SLib.AuxiliaryImage(parent, 60, 60))
        self.aux[0].image = ImageCache['PolterQBlock']
        self.aux[0].setPos(-18, -18)
        self.aux[0].hover = False

    @staticmethod
    def loadImages():
        if 'PolterQBlock' in ImageCache: return

        SLib.loadIfNotInImageCache('GhostHouseStand', 'ghost_house_stand.png')

        polterstand = SLib.GetImg('polter_stand.png')
        polterblock = SLib.GetImg('polter_qblock.png')

        standpainter = QtGui.QPainter(polterstand)
        blockpainter = QtGui.QPainter(polterblock)

        standpainter.drawPixmap(18, 18, ImageCache['GhostHouseStand'])
        blockpainter.drawPixmap(18, 18, ImageCache['Blocks'][0])

        del standpainter
        del blockpainter

        ImageCache['PolterStand'] = polterstand
        ImageCache['PolterQBlock'] = polterblock

    def dataChanged(self):

        style = self.parent.spritedata[5] & 15
        if style == 0:
            self.offset = (0, 0)
            self.height = 16
            self.aux[0].setSize(60, 60)
            self.aux[0].image = ImageCache['PolterQBlock']
        else:
            self.offset = (8, -16)
            self.height = 32
            self.aux[0].setSize(60, 84)
            self.aux[0].image = ImageCache['PolterStand']

        self.aux[0].setPos(-18, -18)

        super().dataChanged()


class SpriteImage_WaterPiranha(SLib.SpriteImage_Static):  # 263
    def __init__(self, parent):
        super().__init__(
            parent,
            1.5,
            ImageCache['WaterPiranhaBody'],
            (-5, -28),
        )

        self.aux.append(SLib.AuxiliaryImage(parent, 38, 30))
        self.aux[0].image = ImageCache['WaterPiranhaBall']
        self.aux[0].setPos(0, -165)
        self.aux[0].hover = True

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('WaterPiranhaBody', 'water_piranha_body.png')
        SLib.loadIfNotInImageCache('WaterPiranhaBall', 'water_piranha_ball.png')


class SpriteImage_FallingIcicle(SLib.SpriteImage_StaticMultiple):  # 265
    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('IcicleSmall', 'icicle_small.png')
        SLib.loadIfNotInImageCache('IcicleLarge', 'icicle_large.png')

    def dataChanged(self):
        super().dataChanged()

        size = self.parent.spritedata[5] & 1
        if size == 0:
            self.image = ImageCache['IcicleSmall']
            self.height = 19
        else:
            self.image = ImageCache['IcicleLarge']
            self.height = 36


class SpriteImage_RotatingFence(SLib.SpriteImage_Static):  # 266
    def __init__(self, parent):
        w, h = ImageCache['RotatingFence'].width(), ImageCache['RotatingFence'].height()
        super().__init__(
            parent,
            1.5,
            ImageCache['RotatingFence'],
            (
                -((w / 2) - 12) / 1.5,
                -((h / 2) - 12) / 1.5,
            ),
        )

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('RotatingFence', 'rotating_chainlink.png')


class SpriteImage_TiltGrate(SLib.SpriteImage_StaticMultiple):  # 267
    @staticmethod
    def loadImages():
        if 'TiltGrateU' in ImageCache: return
        ImageCache['TiltGrateU'] = SLib.GetImg('tilt_grate_up.png')
        ImageCache['TiltGrateD'] = SLib.GetImg('tilt_grate_down.png')
        ImageCache['TiltGrateL'] = SLib.GetImg('tilt_grate_left.png')
        ImageCache['TiltGrateR'] = SLib.GetImg('tilt_grate_right.png')

    def dataChanged(self):
        direction = self.parent.spritedata[5] & 3
        if direction > 3: direction = 3

        if direction < 2:
            self.size = (69, 166)
        else:
            self.size = (166, 69)

        if direction == 0:
            self.offset = (-36, -115)
            self.image = ImageCache['TiltGrateU']
        elif direction == 1:
            self.offset = (-36, 12)
            self.image = ImageCache['TiltGrateD']
        elif direction == 2:
            self.offset = (-144, 0)
            self.image = ImageCache['TiltGrateL']
        elif direction == 3:
            self.offset = (-20, 0)
            self.image = ImageCache['TiltGrateR']

        super().dataChanged()


class SpriteImage_LavaGeyser(SLib.SpriteImage_StaticMultiple):  # 268
    def __init__(self, parent):
        super().__init__(parent, 1.5)

        self.parent.setZValue(24999)
        self.dimensions = (-37, -186, 69, 200)

    @staticmethod
    def loadImages():
        if 'LavaGeyser0' in ImageCache: return
        for i in range(7):
            ImageCache['LavaGeyser%d' % i] = SLib.GetImg('lava_geyser_%d.png' % i)

    def dataChanged(self):

        height = self.parent.spritedata[4] >> 4
        startsOn = self.parent.spritedata[5] & 1

        if height > 6: height = 0
        self.offset = (
            (-30, -170),
            (-28, -155),
            (-30, -155),
            (-43, -138),
            (-32, -105),
            (-26, -89),
            (-32, -34),
        )[height]

        self.alpha = 0.75 if startsOn else 0.5

        self.image = ImageCache['LavaGeyser%d' % height]

        super().dataChanged()


class SpriteImage_Parabomb(SLib.SpriteImage_Static):  # 269
    def __init__(self, parent):
        super().__init__(
            parent,
            1.5,
            ImageCache['Parabomb'],
            (-2, -16),
        )

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('Parabomb', 'parabomb.png')


class SpriteImage_ScaredyRat(SLib.SpriteImage):  # 271
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('ScaredyRat', 'scaredy_rat.png')

    def dataChanged(self):
        super().dataChanged()

        number = (self.parent.spritedata[5] >> 4) & 3
        direction = self.parent.spritedata[5] & 0xF

        self.width = (number + 1) * (ImageCache['ScaredyRat'].width() / 1.5)

        if direction == 0:  # Facing right
            self.xOffset = -self.width + 16
        else:
            self.xOffset = 0

    def paint(self, painter):
        super().paint(painter)

        direction = self.parent.spritedata[5] & 0xF

        rat = ImageCache['ScaredyRat']
        if direction == 1:
            rat = QtGui.QImage(rat)
            rat = QtGui.QPixmap.fromImage(rat.mirrored(True, False))

        painter.drawTiledPixmap(0, 0, int(self.width * 1.5), 24, rat)


class SpriteImage_CastleGear(SLib.SpriteImage):  # 274
    def __init__(self, parent):
        super().__init__(parent)
        self.aux.append(SLib.AuxiliaryImage(parent, 456, 456))
        self.parent.setZValue(24999)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('CastleGearL', 'castle_gear_large.png')
        SLib.loadIfNotInImageCache('CastleGearS', 'castle_gear_small.png')

    def dataChanged(self):
        big = (self.parent.spritedata[4] & 0xF) & 1

        if big:
            self.aux[0].image = ImageCache['CastleGearL']
            self.aux[0].setPos(-216, -216)
        else:
            self.aux[0].image = ImageCache['CastleGearS']
            self.aux[0].setPos(-144, -144)

        super().dataChanged()


class SpriteImage_GhostDoor(SpriteImage_Door):  # 276
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.doorName = 'GhostDoor'
        self.doorDimensions = (0, 0, 32, 48)


class SpriteImage_TowerDoor(SpriteImage_Door):  # 277
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.doorName = 'TowerDoor'
        self.doorDimensions = (-2, -13, 53, 61)
        self.entranceOffset = (15, 68)


class SpriteImage_CastleDoor(SpriteImage_Door):  # 278
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.doorName = 'CastleDoor'
        self.doorDimensions = (-2, -13, 53, 61)
        self.entranceOffset = (15, 68)


class SpriteImage_GiantIceBlock(SLib.SpriteImage_StaticMultiple):  # 280
    @staticmethod
    def loadImages():
        if 'BigIceBlockEmpty' in ImageCache: return
        ImageCache['BigIceBlockEmpty'] = SLib.GetImg('big_ice_block_empty.png')
        ImageCache['BigIceBlockBobomb'] = SLib.GetImg('big_ice_block_bobomb.png')
        ImageCache['BigIceBlockSpikeBall'] = SLib.GetImg('big_ice_block_spikeball.png')

    def dataChanged(self):

        item = self.parent.spritedata[5] & 3
        if item > 2: item = 0

        if item == 0:
            self.image = ImageCache['BigIceBlockEmpty']
        elif item == 1:
            self.image = ImageCache['BigIceBlockBobomb']
        elif item == 2:
            self.image = ImageCache['BigIceBlockSpikeBall']

        super().dataChanged()


class SpriteImage_WoodCircle(SLib.SpriteImage_StaticMultiple):  # 286
    @staticmethod
    def loadImages():
        if 'WoodCircle0' in ImageCache: return
        ImageCache['WoodCircle0'] = SLib.GetImg('wood_circle_0.png')
        ImageCache['WoodCircle1'] = SLib.GetImg('wood_circle_1.png')
        ImageCache['WoodCircle2'] = SLib.GetImg('wood_circle_2.png')

    def dataChanged(self):
        super().dataChanged()
        size = (self.parent.spritedata[5] & 0xF) % 3

        self.image = ImageCache['WoodCircle%d' % size]

        if size > 2: size = 0
        self.dimensions = (
            (-24, -24, 64, 64),
            (-40, -40, 96, 96),
            (-56, -56, 128, 128),
        )[size]


class SpriteImage_PathIceBlock(SLib.SpriteImage_StaticMultiple):  # 287
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False
        self.alpha = 0.8

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('PathIceBlock', 'unused_path_ice_block.png')

    def dataChanged(self):
        width = (self.parent.spritedata[5] & 0xF) + 1
        height = (self.parent.spritedata[5] >> 4) + 1

        self.image = ImageCache['PathIceBlock'].scaled(width * 24, height * 24)

        super().dataChanged()


class SpriteImage_Box(SLib.SpriteImage_StaticMultiple):  # 289
    @staticmethod
    def loadImages():
        if 'Box00' in ImageCache: return
        for style, stylestr in ((0, 'wood'), (1, 'metal')):
            for size, sizestr in zip(range(4), ('small', 'wide', 'tall', 'big')):
                ImageCache['Box%d%d' % (style, size)] = SLib.GetImg('box_%s_%s.png' % (stylestr, sizestr))

    def dataChanged(self):

        style = self.parent.spritedata[4] & 1
        size = (self.parent.spritedata[5] >> 4) & 3

        self.image = ImageCache['Box%d%d' % (style, size)]

        super().dataChanged()


class SpriteImage_Parabeetle(SLib.SpriteImage_StaticMultiple):  # 291
    @staticmethod
    def loadImages():
        if 'Parabeetle0' in ImageCache: return
        ImageCache['Parabeetle0'] = SLib.GetImg('parabeetle_right.png')
        ImageCache['Parabeetle1'] = SLib.GetImg('parabeetle_left.png')
        ImageCache['Parabeetle2'] = SLib.GetImg('parabeetle_moreright.png')
        ImageCache['Parabeetle3'] = SLib.GetImg('parabeetle_atyou.png')

    def dataChanged(self):

        direction = self.parent.spritedata[5] & 3
        self.image = ImageCache['Parabeetle%d' % direction]

        if direction == 0 or direction > 3:  # right
            self.xOffset = -12
        elif direction == 1:  # left
            self.xOffset = -10
        elif direction == 2:  # more right
            self.xOffset = -12
        elif direction == 3:  # at you
            self.xOffset = -26

        super().dataChanged()


class SpriteImage_HeavyParabeetle(SLib.SpriteImage_StaticMultiple):  # 292
    @staticmethod
    def loadImages():
        if 'HeavyParabeetle0' in ImageCache: return
        ImageCache['HeavyParabeetle0'] = SLib.GetImg('heavy_parabeetle_right.png')
        ImageCache['HeavyParabeetle1'] = SLib.GetImg('heavy_parabeetle_left.png')
        ImageCache['HeavyParabeetle2'] = SLib.GetImg('heavy_parabeetle_moreright.png')
        ImageCache['HeavyParabeetle3'] = SLib.GetImg('heavy_parabeetle_atyou.png')

    def dataChanged(self):

        direction = self.parent.spritedata[5] & 3
        self.image = ImageCache['HeavyParabeetle%d' % direction]

        if direction == 0 or direction > 3:  # right
            self.xOffset = -38
        elif direction == 1:  # left
            self.xOffset = -38
        elif direction == 2:  # more right
            self.xOffset = -38
        elif direction == 3:  # at you
            self.xOffset = -52

        super().dataChanged()


class SpriteImage_NutPlatform(SLib.SpriteImage_StaticMultiple):  # 295
    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('NutPlatform', 'nut_platform.png')

    def dataChanged(self):
        offsetUp = self.parent.spritedata[5] >> 4
        offsetRight = self.parent.spritedata[5] & 7

        if offsetUp == 0:
            self.yOffset = -8
        else:
            self.yOffset = 0

        self.xOffset = (
            -16,
            -8,
            0,
            8,
            16,
            24,
            32,
            40,
        )[offsetRight]

        self.image = ImageCache['NutPlatform']

        super().dataChanged()


class SpriteImage_MegaBuzzy(SLib.SpriteImage_StaticMultiple):  # 296
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.offset = (-43, -74)

    @staticmethod
    def loadImages():
        if 'MegaBuzzyR' in ImageCache: return
        ImageCache['MegaBuzzyR'] = SLib.GetImg('megabuzzy_right.png')
        ImageCache['MegaBuzzyL'] = SLib.GetImg('megabuzzy_left.png')
        SLib.loadIfNotInImageCache('MegaBuzzyF', 'megabuzzy_front.png')

    def dataChanged(self):

        direction = self.parent.spritedata[5] & 3
        if direction == 0 or direction > 2:
            self.image = ImageCache['MegaBuzzyR']
        elif direction == 1:
            self.image = ImageCache['MegaBuzzyL']
        elif direction == 2:
            self.image = ImageCache['MegaBuzzyF']

        super().dataChanged()


class SpriteImage_DragonCoaster(SLib.SpriteImage):  # 297
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False
        self.height = 22

    @staticmethod
    def loadImages():
        if 'DragonHead' in ImageCache: return
        ImageCache['DragonHead'] = SLib.GetImg('dragon_coaster_head.png')
        ImageCache['DragonBody'] = SLib.GetImg('dragon_coaster_body.png')
        ImageCache['DragonTail'] = SLib.GetImg('dragon_coaster_tail.png')

    def dataChanged(self):
        super().dataChanged()

        raw_size = self.parent.spritedata[5] & 7

        if raw_size == 0:
            self.width = 32
            self.xOffset = 0
        else:
            self.width = (raw_size * 32) + 32
            self.xOffset = 32 - self.width

    def paint(self, painter):
        super().paint(painter)

        raw_size = self.parent.spritedata[5] & 15

        if raw_size == 0 or raw_size == 8:
            # just the head
            painter.drawPixmap(0, 0, ImageCache['DragonHead'])
        elif raw_size == 1:
            # head and tail only
            painter.drawPixmap(48, 0, ImageCache['DragonHead'])
            painter.drawPixmap(0, 0, ImageCache['DragonTail'])
        else:
            painter.drawPixmap(int((self.width * 1.5) - 48), 0, ImageCache['DragonHead'])
            if raw_size > 1:
                painter.drawTiledPixmap(48, 0, int((self.width * 1.5) - 96), 24, ImageCache['DragonBody'])
            painter.drawPixmap(0, 0, ImageCache['DragonTail'])


class SpriteImage_LongCannon(SLib.SpriteImage_StaticMultiple):  # 298
    def __init__(self, parent):
        super().__init__(parent, 1.5)

    @staticmethod
    def loadImages():
        # TODO: make LongCannonER and BLongCannonER
        if 'LongCannonFL' in ImageCache: return
        ImageCache['LongCannonFL'] = SLib.GetImg('cannon_front_left.png')
        ImageCache['LongCannonFR'] = SLib.GetImg('cannon_front_right.png')
        ImageCache['LongCannonM'] = SLib.GetImg('cannon_middle.png')
        ImageCache['LongCannonEL'] = SLib.GetImg('cannon_end_left.png')

        ImageCache['BLongCannonFL'] = SLib.GetImg('cannonbig_front_left.png')
        ImageCache['BLongCannonFR'] = SLib.GetImg('cannonbig_front_right.png')
        ImageCache['BLongCannonM'] = SLib.GetImg('cannonbig_middle.png')
        ImageCache['BLongCannonEL'] = SLib.GetImg('cannonbig_end_left.png')

        ImageCache['LongCannonFU'] = SLib.GetImg('cannon_front_up.png')
        ImageCache['BLongCannonFU'] = SLib.GetImg('cannonbig_front_up.png')

        ImageCache['LongCannonER'] = ImageCache['LongCannonEL']
        ImageCache['BLongCannonER'] = ImageCache['BLongCannonEL']
        #ImageCache['LongCannonER'] = SLib.GetImg('cannon_end_right.png')
        #ImageCache['BLongCannonER'] = SLib.GetImg('cannonbig_end_right.png')

    def dataChanged(self):
        super().dataChanged()

        raw_length = self.parent.spritedata[4] & 0xF
        self.dir = self.parent.spritedata[5] & 1
        self.big = self.parent.spritedata[5] & 0x10 != 0

        self.bugged = (self.parent.spritedata[5] & 2 == 2) and self.dir == 0

        if self.bugged:
            self.dir = 1

        if self.big:
            self.height = 32
            self.tilesize = 48
            self.width = 16 * (raw_length + 3)
            if self.dir == 0:
                self.numMiddle = raw_length - 2
                self.xOffset = 16 - self.width
            else:
                self.xOffset = 0
                self.numMiddle = raw_length - 1

            if self.bugged:
                self.xOffset = -8
                self.width += 8
        else:
            self.height = 16
            self.tilesize = 24
            self.numMiddle = raw_length
            self.width = 16 * (raw_length + 2)
            if self.dir == 0:
                self.xOffset = 12 - self.width
            else:
                self.xOffset = 4

            if self.bugged:
                self.xOffset = 0
                self.height += 8
                self.width -= 4

    def paint(self, painter):
        super().paint(painter)

        big_s = 'B' if self.big else ''

        middle = ImageCache[big_s + 'LongCannonM']
        solid = SLib.GetTile(1)
        if self.dir == 0:  # right
            front = ImageCache[big_s + 'LongCannonFR']
            end = ImageCache[big_s + 'LongCannonEL']
        else:
            front = ImageCache[big_s + 'LongCannonFL']
            end = ImageCache[big_s + 'LongCannonER']

        # the front
        if self.bugged and self.big:
            front = ImageCache['BLongCannonFU']
            painter.drawPixmap(0, 0, front)
        elif self.bugged:
            front = ImageCache['LongCannonFU']
            painter.drawPixmap(0, 12, front)
        elif self.big and self.dir == 0:
            painter.drawPixmap(24 + 24 * self.numMiddle + self.tilesize, 0, front)
        elif self.dir == 0:
            painter.drawPixmap(24 * self.numMiddle + self.tilesize, 0, front)
        else:
            painter.drawPixmap(0, 0, front)

        # the middle
        if self.bugged and self.big:
            painter.drawTiledPixmap(self.tilesize, 0, self.numMiddle * 24 + 8, self.tilesize, middle)
        elif self.bugged:
            painter.drawTiledPixmap(self.tilesize, 12, self.numMiddle * 24 - 8, self.tilesize, middle)
        elif self.dir == 0 and self.big:
            painter.drawTiledPixmap(self.tilesize + 24, 0, self.numMiddle * 24, self.tilesize, middle)
        else:
            painter.drawTiledPixmap(self.tilesize, 0, self.numMiddle * 24, self.tilesize, middle)

        # the end
        if self.bugged and self.big:
            painter.drawPixmap(24 * self.numMiddle + self.tilesize + 8, 0, end)
        elif self.bugged:
            painter.drawPixmap(24 * self.numMiddle + self.tilesize - 8, 12, end)
        elif self.dir == 0 and self.big:
            painter.drawTiledPixmap(0, 0, 24, 48, solid)
            painter.drawPixmap(24, 0, end)
        elif self.dir == 0:
            painter.drawPixmap(0, 0, end)
        else:
            painter.drawPixmap(24 * self.numMiddle + self.tilesize, 0, end)


class SpriteImage_CannonMulti(SLib.SpriteImage_StaticMultiple):  # 299
    def __init__(self, parent):
        super().__init__(parent, 1.5)

    @staticmethod
    def loadImages():
        if 'CannonMultiU0' in ImageCache: return
        CannonUR = SLib.GetImg('cannon_multi_0.png', True)
        CannonUL = SLib.GetImg('cannon_multi_1.png', True)
        ImageCache['CannonMultiU0'] = QtGui.QPixmap.fromImage(CannonUR)
        ImageCache['CannonMultiU1'] = QtGui.QPixmap.fromImage(CannonUL)
        ImageCache['CannonMultiD0'] = QtGui.QPixmap.fromImage(CannonUR.mirrored(False, True))
        ImageCache['CannonMultiD1'] = QtGui.QPixmap.fromImage(CannonUL.mirrored(False, True))

    def dataChanged(self):
        left = self.parent.spritedata[5] & 1
        upsideDown = (self.parent.spritedata[5] >> 4) & 1

        if upsideDown:
            self.image = ImageCache['CannonMultiD%d' % left]
            self.offset = (-8, -1)
        else:
            self.image = ImageCache['CannonMultiU%d' % left]
            self.offset = (-8, -11)

        super().dataChanged()


class SpriteImage_RotCannon(SLib.SpriteImage_StaticMultiple):  # 300
    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('RotCannon', 'rot_cannon.png')
        SLib.loadIfNotInImageCache('RotCannonU', 'rot_cannon_u.png')

    def dataChanged(self):

        upsideDown = (self.parent.spritedata[5] >> 4) & 1
        if not upsideDown:
            self.image = ImageCache['RotCannon']
            self.offset = (-12, -29)
        else:
            self.image = ImageCache['RotCannonU']
            self.offset = (-12, 0)

        super().dataChanged()


class SpriteImage_RotCannonPipe(SLib.SpriteImage_StaticMultiple):  # 301
    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('RotCannonPipe', 'rot_cannon_pipe.png')
        SLib.loadIfNotInImageCache('RotCannonPipeU', 'rot_cannon_pipe_u.png')

    def dataChanged(self):

        upsideDown = (self.parent.spritedata[5] >> 4) & 1
        if not upsideDown:
            self.image = ImageCache['RotCannonPipe']
            self.offset = (-40, -74)
        else:
            self.image = ImageCache['RotCannonPipeU']
            self.offset = (-40, 0)

        super().dataChanged()


class SpriteImage_MontyMole(SLib.SpriteImage_StaticMultiple):  # 303
    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('Mole', 'monty_mole.png')
        SLib.loadIfNotInImageCache('MoleCave', 'monty_mole_hole.png')

    def dataChanged(self):

        notInCave = self.parent.spritedata[5] & 1
        if not notInCave:  # wow, that looks weird
            self.image = ImageCache['MoleCave']
            del self.offset
        else:
            self.image = ImageCache['Mole']
            self.offset = (3.5, -4)

        super().dataChanged()


class SpriteImage_RotFlameCannon(SLib.SpriteImage_StaticMultiple):  # 304
    @staticmethod
    def loadImages():
        if 'RotFlameCannon0' in ImageCache: return
        for i in range(5):
            ImageCache['RotFlameCannon%d' % i] = SLib.GetImg('rotating_flame_cannon_%d.png' % i)
            originalImg = SLib.GetImg('rotating_flame_cannon_%d.png' % i, True)
            ImageCache['RotFlameCannonFlipped%d' % i] = QtGui.QPixmap.fromImage(originalImg.mirrored(False, True))

    def dataChanged(self):

        orientation = self.parent.spritedata[5] >> 4
        length = self.parent.spritedata[5] & 15
        orientation = '' if orientation == 0 else 'Flipped'

        if length > 4: length = 0
        if not orientation:
            self.yOffset = -2
        else:
            self.yOffset = 0

        self.image = ImageCache['RotFlameCannon%s%d' % (orientation, length)]

        super().dataChanged()


class SpriteImage_LightCircle(SLib.SpriteImage):  # 305
    def __init__(self, parent):
        super().__init__(parent, 1.5)

        self.aux.append(SLib.AuxiliaryImage(parent, 128, 128))
        self.aux[0].image = ImageCache['LightCircle']
        self.aux[0].setPos(-60, -60)
        self.aux[0].hover = False
        self.aux[0].setIsBehindSprite(False)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('LightCircle', 'light_circle.png')


class SpriteImage_RotSpotlight(SLib.SpriteImage_StaticMultiple):  # 306
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.offset = (-22, -64)

    @staticmethod
    def loadImages():
        if 'RotSpotlight0' in ImageCache: return
        for i in range(16):
            ImageCache['RotSpotlight%d' % i] = SLib.GetImg('rotational_spotlight_%d.png' % i)

    def dataChanged(self):

        angle = self.parent.spritedata[3] & 15
        self.image = ImageCache['RotSpotlight%d' % angle]

        super().dataChanged()


class SpriteImage_SynchroFlameJet(SLib.SpriteImage_StaticMultiple):  # 309
    @staticmethod
    def loadImages():
        if 'SynchroFlameJetOnR' in ImageCache: return
        transform90 = QtGui.QTransform()
        transform270 = QtGui.QTransform()
        transform90.rotate(90)
        transform270.rotate(270)

        onImage = SLib.GetImg('synchro_flame_jet.png', True)
        offImage = SLib.GetImg('synchro_flame_jet_off.png', True)
        ImageCache['SynchroFlameJetOnR'] = QtGui.QPixmap.fromImage(onImage)
        ImageCache['SynchroFlameJetOnD'] = QtGui.QPixmap.fromImage(onImage.transformed(transform90))
        ImageCache['SynchroFlameJetOnL'] = QtGui.QPixmap.fromImage(onImage.mirrored(True, False))
        ImageCache['SynchroFlameJetOnU'] = QtGui.QPixmap.fromImage(
            onImage.transformed(transform270).mirrored(True, False))
        ImageCache['SynchroFlameJetOffR'] = QtGui.QPixmap.fromImage(offImage)
        ImageCache['SynchroFlameJetOffD'] = QtGui.QPixmap.fromImage(offImage.transformed(transform90))
        ImageCache['SynchroFlameJetOffL'] = QtGui.QPixmap.fromImage(offImage.mirrored(True, False))
        ImageCache['SynchroFlameJetOffU'] = QtGui.QPixmap.fromImage(
            offImage.transformed(transform270).mirrored(True, False))

    def dataChanged(self):
        mode = self.parent.spritedata[4] & 1
        direction = self.parent.spritedata[5] & 3

        mode = 'Off' if mode else 'On'
        self.offset = (
            (0, 0),
            (-96, 0),
            (0, -96),
            (0, 0),
        )[direction]
        directionstr = 'RLUD'[direction]

        self.image = ImageCache['SynchroFlameJet%s%s' % (mode, directionstr)]

        super().dataChanged()


class SpriteImage_ArrowSign(SLib.SpriteImage_StaticMultiple):  # 310
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.offset = (-8, -16)

    @staticmethod
    def loadImages():
        if 'ArrowSign0' in ImageCache: return
        for i in range(8):
            ImageCache['ArrowSign%d' % i] = SLib.GetImg('arrow_sign_%d.png' % i)

    def dataChanged(self):

        direction = self.parent.spritedata[5] & 0xF
        self.image = ImageCache['ArrowSign%d' % direction]

        super().dataChanged()


class SpriteImage_BubbleGen(SLib.SpriteImage):  # 314

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('BubbleGenEffect', 'bubble_gen.png')

    def dataChanged(self):
        super().dataChanged()
        self.parent.scene().update()

    def positionChanged(self):
        super().positionChanged()
        self.parent.scene().update()

    def realViewZone(self, painter, zoneRect):

        # Constants (change these if you want)
        bubbleFrequency = .01
        bubbleEccentricityX = 16
        bubbleEccentricityY = 48

        size = self.parent.spritedata[5] & 0xF
        if size > 3: return

        Image = ImageCache['BubbleGenEffect']

        if size == 0:
            pct = 50.0
        elif size == 1:
            pct = 60.0
        elif size == 2:
            pct = 80.0
        else:
            pct = 70.0
        Image = Image.scaledToWidth(int(Image.width() * pct / 100))

        distanceFromTop = (self.parent.objy * 1.5) - zoneRect.topLeft().y()
        random.seed(distanceFromTop + self.parent.objx)  # looks ridiculous without this

        numOfBubbles = int(distanceFromTop * bubbleFrequency)
        for num in range(numOfBubbles):
            xmod = (random.random() * 2 * bubbleEccentricityX) - bubbleEccentricityX
            ymod = (random.random() * 2 * bubbleEccentricityY) - bubbleEccentricityY
            x = ((self.parent.objx * 1.5) - zoneRect.topLeft().x()) + xmod + 12 - (Image.width() / 2.0)
            y = ((num * 1.0 / numOfBubbles) * distanceFromTop) + ymod
            if not (0 < y < self.parent.objy * 1.5): continue
            painter.drawPixmap(int(x), int(y), Image)


class SpriteImage_BoltBox(SLib.SpriteImage):  # 316
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

    @staticmethod
    def loadImages():
        if 'BoltBoxTL' in ImageCache: return
        ImageCache['BoltBoxTL'] = SLib.GetImg('boltbox_tl.png')
        ImageCache['BoltBoxT'] = SLib.GetImg('boltbox_t.png')
        ImageCache['BoltBoxTR'] = SLib.GetImg('boltbox_tr.png')
        ImageCache['BoltBoxL'] = SLib.GetImg('boltbox_l.png')
        ImageCache['BoltBoxM'] = SLib.GetImg('boltbox_m.png')
        ImageCache['BoltBoxR'] = SLib.GetImg('boltbox_r.png')
        ImageCache['BoltBoxBL'] = SLib.GetImg('boltbox_bl.png')
        ImageCache['BoltBoxB'] = SLib.GetImg('boltbox_b.png')
        ImageCache['BoltBoxBR'] = SLib.GetImg('boltbox_br.png')

    def dataChanged(self):
        super().dataChanged()

        size = self.parent.spritedata[5]
        self.width = (size & 0xF) * 16 + 32
        self.height = ((size & 0xF0) >> 4) * 16 + 32

    def paint(self, painter):
        super().paint(painter)

        xsize = int(self.width * 1.5)
        ysize = int(self.height * 1.5)

        painter.drawPixmap(0, 0, ImageCache['BoltBoxTL'])
        painter.drawTiledPixmap(24, 0, xsize - 48, 24, ImageCache['BoltBoxT'])
        painter.drawPixmap(xsize - 24, 0, ImageCache['BoltBoxTR'])

        painter.drawTiledPixmap(0, 24, 24, ysize - 48, ImageCache['BoltBoxL'])
        painter.drawTiledPixmap(24, 24, xsize - 48, ysize - 48, ImageCache['BoltBoxM'])
        painter.drawTiledPixmap(xsize - 24, 24, 24, ysize - 48, ImageCache['BoltBoxR'])

        painter.drawPixmap(0, ysize - 24, ImageCache['BoltBoxBL'])
        painter.drawTiledPixmap(24, ysize - 24, xsize - 48, 24, ImageCache['BoltBoxB'])
        painter.drawPixmap(xsize - 24, ysize - 24, ImageCache['BoltBoxBR'])


class SpriteImage_ArrowBlock(SLib.SpriteImage_StaticMultiple):  # 321
    @staticmethod
    def loadImages():
        if 'ArrowBlock0' in ImageCache: return
        ImageCache['ArrowBlock0'] = SLib.GetImg('arrow_block_up.png')
        ImageCache['ArrowBlock1'] = SLib.GetImg('arrow_block_down.png')
        ImageCache['ArrowBlock2'] = SLib.GetImg('arrow_block_left.png')
        ImageCache['ArrowBlock3'] = SLib.GetImg('arrow_block_right.png')

    def dataChanged(self):
        direction = self.parent.spritedata[5] & 3
        self.image = ImageCache['ArrowBlock%d' % direction]

        super().dataChanged()


class SpriteImage_BooCircle(SLib.SpriteImage):  # 323
    def __init__(self, parent):
        super().__init__(parent, 1.5)

        self.BooAuxImage = QtGui.QPixmap(1024, 1024)
        self.BooAuxImage.fill(Qt.transparent)
        self.aux.append(SLib.AuxiliaryImage(parent, 1024, 1024))
        self.aux[0].image = self.BooAuxImage
        offsetX = ImageCache['Boo1'].width() / 4
        offsetY = ImageCache['Boo1'].height() / 4
        self.aux[0].setPos(-512 + offsetX, -512 + offsetY)
        self.aux[0].hover = False

    @staticmethod
    def loadImages():
        if 'Boo2' in ImageCache: return
        ImageCache['Boo1'] = SLib.GetImg('boo1.png')
        ImageCache['Boo2'] = SLib.GetImg('boo2.png')
        ImageCache['Boo3'] = SLib.GetImg('boo3.png')
        ImageCache['Boo4'] = SLib.GetImg('boo4.png')

    def dataChanged(self):
        # Constants (change these to fine-tune the boo positions)
        radiusMultiplier = 24  # pixels between boos per distance value
        radiusConstant = 24  # add to all radius values
        opacity = 0.5

        # Read the data
        outrad = self.parent.spritedata[2] & 15
        inrad = self.parent.spritedata[3] >> 4
        ghostnum = 1 + (self.parent.spritedata[3] & 15)
        differentRads = not (inrad == outrad)

        # Give up if the data is invalid
        if inrad > outrad:
            null = QtGui.QPixmap(2, 2)
            null.fill(Qt.transparent)
            self.aux[0].image = null
            return

        # Create a pixmap
        pix = QtGui.QPixmap(1024, 1024)
        pix.fill(Qt.transparent)
        paint = QtGui.QPainter(pix)
        paint.setOpacity(opacity)

        # Paint each boo
        for i in range(ghostnum):
            # Find the angle at which to place the ghost from the center
            MissingGhostWeight = 0.75 - (1 / ghostnum)  # approximate
            angle = math.radians(-360 * i / (ghostnum + MissingGhostWeight)) + 89.6

            # Since the origin of the boo img is in the top left, account for that
            offsetX = ImageCache['Boo1'].width() / 2
            offsetY = (ImageCache['Boo1'].height() / 2) + 16  # the circle is not centered

            # Pick a pixmap
            boo = ImageCache['Boo%d' % (1 if i == 0 else ((i - 1) % 3) + 2)]  # 1  2 3 4  2 3 4  2 3 4 ...

            # Find the abs pos, and paint the ghost at its inner position
            x = math.sin(angle) * ((inrad * radiusMultiplier) + radiusConstant) - offsetX
            y = -(math.cos(angle) * ((inrad * radiusMultiplier) + radiusConstant)) - offsetY
            paint.drawPixmap(int(x + 512), int(y + 512), boo)

            # Paint it at its outer position if it has one
            if differentRads:
                x = math.sin(angle) * ((outrad * radiusMultiplier) + radiusConstant) - offsetX
                y = -(math.cos(angle) * ((outrad * radiusMultiplier) + radiusConstant)) - offsetY
                paint.drawPixmap(int(x + 512), int(y + 512), boo)

        # Finish it
        paint = None
        self.aux[0].image = pix


class SpriteImage_KingBill(SLib.SpriteImage):  # 326
    def __init__(self, parent):
        super().__init__(parent, 1.5)

        self.aux.append(SLib.AuxiliaryPainterPath(parent, QtGui.QPainterPath(), 24, 24))
        self.aux[0].setSize(24 * 17, 24 * 17)

        self.paths = []
        for direction in range(4):

            # This has to be within the loop because the
            # following commands transpose them
            PointsRects = (  # These form a LEFT-FACING bullet
                QtCore.QPointF(192, -180 + 180),
                QtCore.QRectF(0, -180 + 180, 384, 384),
                QtCore.QPointF(192 + 72, 204 + 180),
                QtCore.QPointF(192 + 72 + 6, 204 - 24 + 180),
                QtCore.QPointF(192 + 72 + 42, 204 - 24 + 180),
                QtCore.QPointF(192 + 72 + 48, 204 + 180),
                QtCore.QPointF(192 + 72 + 96, 204 + 180),
                QtCore.QPointF(192 + 72 + 96 + 6, 204 - 6 + 180),
                QtCore.QPointF(192 + 72 + 96 + 6, -180 + 6 + 180),
                QtCore.QPointF(192 + 72 + 96, -180 + 180),
                QtCore.QPointF(192 + 72 + 48, -180 + 180),
                QtCore.QPointF(192 + 72 + 42, -180 + 24 + 180),
                QtCore.QPointF(192 + 72 + 6, -180 + 24 + 180),
                QtCore.QPointF(192 + 72, -180 + 180),
            )

            for thing in PointsRects:  # translate each point to flip the image
                if direction == 0:  # faces left
                    arc = 'LR'
                elif direction == 1:  # faces right
                    arc = 'LR'
                    if isinstance(thing, QtCore.QPointF):
                        thing.setX(408 - thing.x())
                    else:
                        thing.setRect(408 - thing.x(), thing.y(), -thing.width(), thing.height())
                elif direction == 2:  # faces down
                    arc = 'UD'
                    if isinstance(thing, QtCore.QPointF):
                        x = thing.y()
                        y = 408 - thing.x()
                        thing.setX(x)
                        thing.setY(y)
                    else:
                        x = thing.y()
                        y = 408 - thing.x()
                        thing.setRect(x, y, thing.height(), -thing.width())
                else:  # faces up
                    arc = 'UD'
                    if isinstance(thing, QtCore.QPointF):
                        x = thing.y()
                        y = thing.x()
                        thing.setX(x)
                        thing.setY(y)
                    else:
                        x = thing.y()
                        y = thing.x()
                        thing.setRect(x, y, thing.height(), thing.width())

            PainterPath = QtGui.QPainterPath()
            PainterPath.moveTo(PointsRects[0])
            if arc == 'LR':
                PainterPath.arcTo(PointsRects[1], 90, 180)
            else:
                PainterPath.arcTo(PointsRects[1], 180, -180)
            for point in PointsRects[2:]:
                PainterPath.lineTo(point)
            PainterPath.closeSubpath()
            self.paths.append(PainterPath)

    def dataChanged(self):

        direction = self.parent.spritedata[5] & 3

        self.aux[0].setPath(self.paths[direction])

        newx, newy = (
            (0, (-8 * 24) + 12),
            ((-24 * 16), (-8 * 24) + 12),
            ((-24 * 10), (-24 * 16)),
            ((-24 * 5), 0),
        )[direction]
        self.aux[0].setPos(newx, newy)

        super().dataChanged()


class SpriteImage_BubbleCannon(SLib.SpriteImage_StaticMultiple):  # 328
    @staticmethod
    def loadImages():
        if 'BubbleCannon0' in ImageCache: return
        ImageCache['BubbleCannon0'] = SLib.GetImg('bubble_cannon_small.png')
        ImageCache['BubbleCannon1'] = SLib.GetImg('bubble_cannon_big.png')

    def dataChanged(self):
        size = self.parent.spritedata[5] & 1
        self.image = ImageCache['BubbleCannon%d' % size]
        self.offset = (
            (-17, -15),
            (-36, -31),
        )[size]

        super().dataChanged()


class SpriteImage_RopeLadder(SLib.SpriteImage_StaticMultiple):  # 330
    @staticmethod
    def loadImages():
        if 'RopeLadder0' in ImageCache: return
        ImageCache['RopeLadder0'] = SLib.GetImg('ropeladder_0.png')
        ImageCache['RopeLadder1'] = SLib.GetImg('ropeladder_1.png')
        ImageCache['RopeLadder2'] = SLib.GetImg('ropeladder_2.png')

    def dataChanged(self):

        size = self.parent.spritedata[5]
        if size > 2: size = 0

        self.image = ImageCache['RopeLadder%d' % size]
        self.offset = (-3, -2)

        super().dataChanged()


class SpriteImage_DishPlatform(SLib.SpriteImage_StaticMultiple):  # 331
    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('DishPlatform0', 'dish_platform_short.png')
        SLib.loadIfNotInImageCache('DishPlatform1', 'dish_platform_long.png')

    def dataChanged(self):

        size = self.parent.spritedata[4] & 15
        if size == 0:
            self.xOffset = -144
            self.width = 304
        else:
            self.xOffset = -208
            self.width = 433

        self.image = ImageCache['DishPlatform%d' % size]

        super().dataChanged()


class SpriteImage_CheepGiant(SLib.SpriteImage):  # 334
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

        self.aux.append(SLib.AuxiliaryTrackObject(self.parent, 24, 24, SLib.AuxiliaryTrackObject.Horizontal))

    @staticmethod
    def loadImages():
        if 'CheepGiantRedLeft' in ImageCache: return
        ImageCache['CheepGiantRedLeft'] = SLib.GetImg('cheep_giant_red.png')
        ImageCache['CheepGiantRedAtYou'] = SLib.GetImg('cheep_giant_red_atyou.png')
        ImageCache['CheepGiantGreen'] = SLib.GetImg('cheep_giant_green.png')
        ImageCache['CheepGiantYellow'] = SLib.GetImg('cheep_giant_yellow.png')

    def dataChanged(self):

        type = self.parent.spritedata[5] & 0xF
        if type in (1, 7):
            self.image = ImageCache['CheepGiantGreen']
        elif type == 8:
            self.image = ImageCache['CheepGiantYellow']
        elif type == 5:
            self.image = ImageCache['CheepGiantRedAtYou']
        else:
            self.image = ImageCache['CheepGiantRedLeft']
        self.size = (self.image.width() / 1.5, self.image.height() / 1.5)
        self.xOffset = 0 if type != 5 else -8

        if type == 3:
            distance = ((self.parent.spritedata[3] & 0xF) + 1) * 16
            self.aux[0].setSize((distance * 2) + 16, 16)
            self.aux[0].setPos(-distance * 1.5, 8)
        else:
            self.aux[0].setSize(0, 24)

        super().dataChanged()

    def paint(self, painter):
        super().paint(painter)
        painter.drawPixmap(0, 0, self.image)


# Copied and edited from Miyamoto, credit to mrbengtsson for original code
class SpriteImage_MovingBulletBillLauncher(SLib.SpriteImage):  # 338
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('BBLauncherT', 'bullet_launcher_top.png')
        SLib.loadIfNotInImageCache('BBLauncherM', 'bullet_launcher_middle.png')

    def dataChanged(self):
        self.image = None
        self.xOffset = 0
        self.width = 16

        self.cannonHeight = (self.parent.spritedata[5] & 0xF0) >> 4
        self.cannonHeightTwo = self.parent.spritedata[5] & 0xF

        if self.cannonHeight >= self.cannonHeightTwo:
            self.height = (self.cannonHeight + 2) * 16

        else:
            self.height = (self.cannonHeightTwo + 2) * 16

        if self.cannonHeight >= self.cannonHeightTwo:
            self.yOffset = -(self.cannonHeight + 1) * 16

        else:
            self.yOffset = -(self.cannonHeightTwo + 1) * 16

        super().dataChanged()

    def paint(self, painter):
        if self.cannonHeightTwo > self.cannonHeight:
            painter.setOpacity(0.5)
            painter.drawPixmap(0, 0, 24, 48, ImageCache['BBLauncherT'])
            painter.drawTiledPixmap(0, 48, 24, 24 * self.cannonHeightTwo, ImageCache['BBLauncherM'])
            painter.setOpacity(1)

            painter.drawPixmap(0, 24 * (self.cannonHeightTwo - self.cannonHeight), 24, 48, ImageCache['BBLauncherT'])
            painter.drawTiledPixmap(0, 24 * (self.cannonHeightTwo - self.cannonHeight + 2), 24, 48 * self.cannonHeight,
                                    ImageCache['BBLauncherM'])

        else:
            painter.drawPixmap(0, 0, 24, 48, ImageCache['BBLauncherT'])
            painter.drawTiledPixmap(0, 48, 24, 24 * self.cannonHeight, ImageCache['BBLauncherM'])


class SpriteImage_Pipe_MovingUp(SpriteImage_Pipe):  # 339
    def dataChanged(self):
        self.length1 = (self.parent.spritedata[5] >> 4) + 2
        self.length2 = (self.parent.spritedata[5] & 0xF) + 2
        self.color = (
            'Green', 'Red', 'Yellow', 'Blue',
        )[self.parent.spritedata[3] & 3]

        super().dataChanged()


class SpriteImage_BigShell(SLib.SpriteImage_StaticMultiple):  # 341
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.offset = (-97, -145)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('BigShell', 'bigshell_green.png')
        SLib.loadIfNotInImageCache('BigShellGrass', 'bigshell_green_grass.png')

    def dataChanged(self):
        style = self.parent.spritedata[5] & 1

        if style == 0:
            self.image = ImageCache['BigShellGrass']
        else:
            self.image = ImageCache['BigShell']

        super().dataChanged()


class SpriteImage_Muncher(SLib.SpriteImage_StaticMultiple):  # 342
    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('Muncher', 'muncher.png')
        SLib.loadIfNotInImageCache('MuncherF', 'muncher_frozen.png')

    def dataChanged(self):

        frozen = self.parent.spritedata[5] & 1
        if frozen == 1:
            self.image = ImageCache['MuncherF']
            self.offset = (0, 0)
        else:
            self.image = ImageCache['Muncher']
            self.offset = (0, -1)

        super().dataChanged()


class SpriteImage_Fuzzy(SLib.SpriteImage_StaticMultiple):  # 343
    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('Fuzzy', 'fuzzy.png')
        SLib.loadIfNotInImageCache('FuzzyGiant', 'fuzzy_giant.png')

    def dataChanged(self):
        giant = self.parent.spritedata[4] & 1

        self.image = ImageCache['FuzzyGiant'] if giant else ImageCache['Fuzzy']
        self.offset = (-18, -18) if giant else (-7, -7)

        super().dataChanged()


class SpriteImage_HangingChainPlatform(SLib.SpriteImage_StaticMultiple):  # 346
    @staticmethod
    def loadImages():
        if 'HangingChainPlatform0' in ImageCache: return
        ImageCache['HangingChainPlatform0'] = SLib.GetImg('hanging_chain_platform_small.png')
        ImageCache['HangingChainPlatform1'] = SLib.GetImg('hanging_chain_platform_medium.png')
        ImageCache['HangingChainPlatform2'] = SLib.GetImg('hanging_chain_platform_large.png')

    def dataChanged(self):
        size = (self.parent.spritedata[4] & 3) % 3
        self.offset = (
            (-26, -12),
            (-42, -12),
            (-58, -12),
        )[size]
        self.image = ImageCache['HangingChainPlatform%d' % size]

        super().dataChanged()


class SpriteImage_MortonKoopaCastleBoss(SLib.SpriteImage):  # 349
    def __init__(self, parent):
        super().__init__(parent)
        self.parent.setZValue(24999)

        self.aux.append(SLib.AuxiliaryImage(parent, 552, 408))
        self.aux[0].image = ImageCache['MortonKoopaCastleBoss']
        self.aux[0].setPos(48, 0)
        self.aux.append(SLib.AuxiliaryRectOutline(parent, 24, 24, 0, 288))

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('MortonKoopaCastleBoss', 'morton_castle_boss.png')


class SpriteImage_Pipe_MovingDown(SpriteImage_Pipe):  # 353
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.direction = 'D'

    def dataChanged(self):
        self.length1 = (self.parent.spritedata[5] >> 4) + 2
        self.length2 = (self.parent.spritedata[5] & 0xF) + 2
        self.color = (
            'Green', 'Red', 'Yellow', 'Blue',
        )[self.parent.spritedata[3] & 3]

        super().dataChanged()


class SpriteImage_RollingHillWith1Pipe(SpriteImage_RollingHillWithPipe):  # 355
    pass


class SpriteImage_BrownBlock(SLib.SpriteImage):  # 356
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

        self.aux.append(SLib.AuxiliaryTrackObject(parent, 16, 16, SLib.AuxiliaryTrackObject.Horizontal))

    @staticmethod
    def loadImages():
        for vert in 'TMB':
            for horz in 'LMR':
                SLib.loadIfNotInImageCache(
                    'BrownBlock' + vert + horz,
                    'brown_block_%s%s.png' % (vert, horz)
                )

    def dataChanged(self):
        super().dataChanged()

        size = self.parent.spritedata[5]
        height = size >> 4
        width = size & 0xF
        height = 1 if height == 0 else height
        width = 1 if width == 0 else width
        self.width = width * 16 + 16
        self.height = height * 16 + 16

        # now set up the track
        direction = self.parent.spritedata[2] & 3
        distance = (self.parent.spritedata[4] & 0xF0) >> 4

        if direction <= 1:  # horizontal
            self.aux[0].direction = 1
            self.aux[0].setSize(self.width + (distance * 16), self.height)
        else:  # vertical
            self.aux[0].direction = 2
            self.aux[0].setSize(self.width, self.height + (distance * 16))

        if (direction in (0, 3)) or (direction not in (1, 2)):  # right, down
            self.aux[0].setPos(0, 0)
        elif direction == 1:  # left
            self.aux[0].setPos(-distance * 24, 0)
        elif direction == 2:  # up
            self.aux[0].setPos(0, -distance * 24)

    def paint(self, painter):
        super().paint(painter)

        width = int(self.width * 1.5)
        height = int(self.height * 1.5)

        column2x = 24
        column3x = width - 24
        row2y = 24
        row3y = height - 24

        painter.drawPixmap(0, 0, ImageCache['BrownBlockTL'])
        painter.drawTiledPixmap(column2x, 0, width - 48, 24, ImageCache['BrownBlockTM'])
        painter.drawPixmap(column3x, 0, ImageCache['BrownBlockTR'])

        painter.drawTiledPixmap(0, row2y, 24, height - 48, ImageCache['BrownBlockML'])
        painter.drawTiledPixmap(column2x, row2y, width - 48, height - 48, ImageCache['BrownBlockMM'])
        painter.drawTiledPixmap(column3x, row2y, 24, height - 48, ImageCache['BrownBlockMR'])

        painter.drawPixmap(0, row3y, ImageCache['BrownBlockBL'])
        painter.drawTiledPixmap(column2x, row3y, width - 48, 24, ImageCache['BrownBlockBM'])
        painter.drawPixmap(column3x, row3y, ImageCache['BrownBlockBR'])


class SpriteImage_Fruit(SLib.SpriteImage_StaticMultiple):  # 357
    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('Fruit', 'fruit.png')
        SLib.loadIfNotInImageCache('FruitCookie', 'fruit_cookie.png')

    def dataChanged(self):

        style = self.parent.spritedata[5] & 1
        if style == 0:
            self.image = ImageCache['Fruit']
        else:
            self.image = ImageCache['FruitCookie']

        super().dataChanged()


class SpriteImage_LavaParticles(SpriteImage_LiquidOrFog):  # 358
    @staticmethod
    def loadImages():
        if 'LavaParticlesA' in ImageCache: return
        ImageCache['LavaParticlesA'] = SLib.GetImg('lava_particles_a.png')
        ImageCache['LavaParticlesB'] = SLib.GetImg('lava_particles_b.png')
        ImageCache['LavaParticlesC'] = SLib.GetImg('lava_particles_c.png')

    def dataChanged(self):
        type = (self.parent.spritedata[5] & 0xF) % 3
        self.mid = (
            ImageCache['LavaParticlesA'],
            ImageCache['LavaParticlesB'],
            ImageCache['LavaParticlesC'],
        )[type]

        super().dataChanged()


class SpriteImage_WallLantern(SLib.SpriteImage):  # 359
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

        self.aux.append(SLib.AuxiliaryImage(parent, 128, 128))
        self.aux[0].image = ImageCache['WallLanternAux']
        self.aux[0].setPos(-48, -48)
        self.aux[0].hover = False

        self.image = ImageCache['WallLantern']
        self.yOffset = 8

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('WallLantern', 'wall_lantern.png')
        SLib.loadIfNotInImageCache('WallLanternAux', 'wall_lantern_aux.png')

    def paint(self, painter):
        super().paint(painter)
        painter.drawPixmap(0, 0, self.image)


class SpriteImage_RollingHillWith8Pipes(SpriteImage_RollingHillWithPipe):  # 360
    pass


class SpriteImage_CrystalBlock(SLib.SpriteImage_StaticMultiple):  # 361
    @staticmethod
    def loadImages():
        if 'CrystalBlock0' in ImageCache: return
        for size in range(3):
            ImageCache['CrystalBlock%d' % size] = SLib.GetImg('crystal_block_%d.png' % size)

    def dataChanged(self):
        size = self.parent.spritedata[4] & 3

        if size == 3:
            size = 2

        self.image = ImageCache['CrystalBlock%d' % size]

        super().dataChanged()


class SpriteImage_ColoredBox(SLib.SpriteImage):  # 362
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

    @staticmethod
    def loadImages():
        if 'CBox0TL' in ImageCache: return
        for color in range(4):
            for direction in ('TL', 'T', 'TR', 'L', 'M', 'R', 'BL', 'B', 'BR'):
                ImageCache['CBox%d%s' % (color, direction)] = SLib.GetImg('cbox_%s_%d.png' % (direction, color))

    def dataChanged(self):
        super().dataChanged()
        self.color = (self.parent.spritedata[3] >> 4) & 3

        size = self.parent.spritedata[4]
        width = size >> 4
        height = size & 0xF

        self.width = (width + 3) * 16
        self.height = (height + 3) * 16

    def paint(self, painter):
        super().paint(painter)

        prefix = 'CBox%d' % self.color
        xsize = int(self.width * 1.5)
        ysize = int(self.height * 1.5)

        painter.drawPixmap(0, 0, ImageCache[prefix + 'TL'])
        painter.drawPixmap(xsize - 25, 0, ImageCache[prefix + 'TR'])
        painter.drawPixmap(0, ysize - 25, ImageCache[prefix + 'BL'])
        painter.drawPixmap(xsize - 25, ysize - 25, ImageCache[prefix + 'BR'])

        painter.drawTiledPixmap(25, 0, xsize - 50, 25, ImageCache[prefix + 'T'])
        painter.drawTiledPixmap(25, ysize - 25, xsize - 50, 25, ImageCache[prefix + 'B'])
        painter.drawTiledPixmap(0, 25, 25, ysize - 50, ImageCache[prefix + 'L'])
        painter.drawTiledPixmap(xsize - 25, 25, 25, ysize - 50, ImageCache[prefix + 'R'])

        painter.drawTiledPixmap(25, 25, xsize - 50, ysize - 50, ImageCache[prefix + 'M'])


class SpriteImage_RoyKoopaCastleBoss(SLib.SpriteImage):  # 364
    def __init__(self, parent):
        super().__init__(parent)
        self.parent.setZValue(24999)

        self.aux.append(SLib.AuxiliaryImage(parent, 528, 384))
        self.aux[0].image = ImageCache['RoyKoopaCastleBoss']
        self.aux[0].setPos(72, -96)
        self.aux.append(SLib.AuxiliaryRectOutline(parent, 24, 24, 24, 312))

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('RoyKoopaCastleBoss', 'roy_castle_boss.png')


class SpriteImage_LudwigVonKoopaCastleBoss(SLib.SpriteImage):  # 365
    def __init__(self, parent):
        super().__init__(parent)
        self.parent.setZValue(24999)

        self.aux.append(SLib.AuxiliaryImage(parent, 720, 840))
        self.aux[0].image = ImageCache['LudwigVonKoopaCastleBoss']
        self.aux[0].setPos(-24, -360)
        self.aux.append(SLib.AuxiliaryRectOutline(parent, 24, 24, 24, 288))
        self.aux.append(SLib.AuxiliaryRectOutline(parent, 528, 24, 72, 264))
        self.aux[2].fillFlag = False

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('LudwigVonKoopaCastleBoss', 'ludwig_castle_boss.png')


class SpriteImage_CubeKinokoRot(SLib.SpriteImage_StaticMultiple):  # 366
    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('CubeKinokoG', 'cube_kinoko_g.png')
        SLib.loadIfNotInImageCache('CubeKinokoR', 'cube_kinoko_r.png')

    def dataChanged(self):

        style = self.parent.spritedata[4] & 1
        if style == 0:
            self.image = ImageCache['CubeKinokoR']
        else:
            self.image = ImageCache['CubeKinokoG']

        super().dataChanged()


class SpriteImage_FlashRaft(SLib.SpriteImage_StaticMultiple):  # 368
    def __init__(self, parent):
        super().__init__(
            parent,
            1.5,
            ImageCache['FlashlightRaft'],
            (-16, -20),
        )

        self.aux.append(SLib.AuxiliaryImage(parent, 72, 114))
        self.aux[0].image = ImageCache['FlashlightLamp']
        self.aux[0].setPos(0, -114)

        self.aux.append(SLib.AuxiliaryRectOutline(parent, 24, 24, 144, 30))
        self.aux[1].setIsBehindSprite(False)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('FlashlightRaft', 'flashraft.png')
        SLib.loadIfNotInImageCache('FlashlightLamp', 'flashraft_light.png')

    def dataChanged(self):
        pathcontrolled = self.parent.spritedata[5] & 1
        midway = (self.parent.spritedata[5] >> 4) & 1

        self.aux[1].setSize(24, 24, 144, 30) if pathcontrolled else self.aux[1].setSize(0, 0)

        if midway:
            self.alpha = 0.5
            self.aux[0].alpha = 0.5
        else:
            self.alpha = 1
            self.aux[0].alpha = 1

        super().dataChanged()


class SpriteImage_SlidingPenguin(SLib.SpriteImage_StaticMultiple):  # 369
    @staticmethod
    def loadImages():
        if 'PenguinL' in ImageCache: return
        penguin = SLib.GetImg('sliding_penguin.png', True)
        ImageCache['PenguinL'] = QtGui.QPixmap.fromImage(penguin)
        ImageCache['PenguinR'] = QtGui.QPixmap.fromImage(penguin.mirrored(True, False))

    def dataChanged(self):

        direction = self.parent.spritedata[5] & 1
        if direction == 0:
            self.image = ImageCache['PenguinL']
        else:
            self.image = ImageCache['PenguinR']

        super().dataChanged()


class SpriteImage_IggyKoopaCastleBoss(SLib.SpriteImage):  # 372
    def __init__(self, parent):
        super().__init__(parent)
        self.aux.append(SLib.AuxiliaryImage(parent, 240, 288))
        self.parent.setZValue(24999)
        self.aux[0].image = ImageCache['IggyKoopaCastleBoss']
        self.aux[0].setSize(240, 288, 360, 48)

        self.aux.append(SLib.AuxiliaryRectOutline(parent, 24, 24, 24, 312))

        self.aux.append(SLib.AuxiliaryRectOutline(parent, 528, 264, 72, 24))
        self.aux[2].fillFlag = False

        w = SLib.OutlinePen.widthF()
        self.aux.append(SLib.AuxiliaryRectOutline(parent, 336 + w, 24 + w, 168 - w / 2, 144 - w / 2))
        self.aux[3].fillFlag = False

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('IggyKoopaCastleBoss', 'iggy_castle_boss.png')


class SpriteImage_RaftWater(SpriteImage_LiquidOrFog):  # 373
    def __init__(self, parent):
        super().__init__(parent)

        self.crest = ImageCache['RaftWaterCrest']
        self.mid = ImageCache['RaftWater']

        self.top = self.parent.objy
        self.drawCrest = True

    @staticmethod
    def loadImages():
        if 'RaftWaterCrest' in ImageCache: return
        ImageCache['RaftWater'] = SLib.GetImg('liquid_water.png')
        ImageCache['RaftWaterCrest'] = SLib.GetImg('liquid_water_crest.png')

    def positionChanged(self):
        self.top = self.parent.objy
        super().positionChanged()


class SpriteImage_SnowWind(SpriteImage_LiquidOrFog):  # 374
    def __init__(self, parent):
        super().__init__(parent)
        self.mid = ImageCache['SnowEffect']

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('SnowEffect', 'snow.png')

    def paintZone(self):
        # For now, we only paint snow
        return self.parent.spritedata[5] == 0 and self.zoneId != -1


class SpriteImage_WendyKoopaCastleBoss(SLib.SpriteImage):  # 375
    def __init__(self, parent):
        super().__init__(parent)
        self.parent.setZValue(24999)

        self.aux.append(SLib.AuxiliaryImage(parent, 648, 528))
        self.aux[0].image = ImageCache['WendyKoopaCastleBoss']
        self.aux[0].setPos(0, -120)
        self.aux.append(SLib.AuxiliaryRectOutline(parent, 24, 24, 0, 288))

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('WendyKoopaCastleBoss', 'wendy_castle_boss.png')


class SpriteImage_MovingFence(SLib.SpriteImage):  # 376
    def __init__(self, parent, scale=1.5):
        super().__init__(parent, scale)
        self.spritebox.shown = False
        self.aux.append(SLib.AuxiliaryTrackObject(parent, 16, 16, SLib.AuxiliaryTrackObject.Horizontal))

    @staticmethod
    def loadImages():
        if 'MovingFence0' in ImageCache: return
        for shape in range(4):
            ImageCache['MovingFence%d' % shape] = SLib.GetImg('moving_fence_%d.png' % shape)

    def dataChanged(self):
        super().dataChanged()

        self.shape = (self.parent.spritedata[4] >> 4) & 3
        direction = self.parent.spritedata[5] & 1
        distance = (self.parent.spritedata[5] & 0xF0) >> 4

        self.size = (
            (64, 64),
            (64, 128),
            (64, 224),
            (192, 64)
        )[self.shape]

        self.xOffset = -self.size[0] / 2
        self.yOffset = -self.size[1] / 2

        if distance == 0:
            self.aux[0].setSize(0, 0)
        elif direction == 1:  # horizontal
            self.aux[0].direction = 1
            self.aux[0].setSize((distance * 32) + self.width, 16)
            self.aux[0].setPos(-distance * 24, (self.height * 0.75) - 12)
        else:  # vertical
            self.aux[0].direction = 2
            self.aux[0].setSize(16, (distance * 32) + self.height)
            self.aux[0].setPos((self.width * 0.75) - 12, -distance * 24)

    def paint(self, painter):
        super().paint(painter)

        painter.drawPixmap(0, 0, ImageCache['MovingFence%d' % self.shape])


class SpriteImage_Pipe_Up(SpriteImage_PipeStationary):  # 377
    def dataChanged(self):
        self.length = (self.parent.spritedata[5] & 0xF) + 2
        super().dataChanged()


class SpriteImage_Pipe_Down(SpriteImage_PipeStationary):  # 378
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.direction = 'D'

    def dataChanged(self):
        self.length = (self.parent.spritedata[5] & 0xF) + 2
        super().dataChanged()


class SpriteImage_Pipe_Right(SpriteImage_PipeStationary):  # 379
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.direction = 'R'

    def dataChanged(self):
        self.length = (self.parent.spritedata[5] & 0xF) + 2
        super().dataChanged()


class SpriteImage_Pipe_Left(SpriteImage_PipeStationary):  # 380
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.direction = 'L'

    def dataChanged(self):
        self.length = (self.parent.spritedata[5] & 0xF) + 2
        super().dataChanged()


class SpriteImage_LemmyKoopaCastleBoss(SLib.SpriteImage):  # 381
    def __init__(self, parent):
        super().__init__(parent)
        self.parent.setZValue(24999)

        self.aux.append(SLib.AuxiliaryImage(parent, 552, 216))
        self.aux[0].image = ImageCache['LemmyKoopaCastleBoss']
        self.aux[0].setPos(48, 168)
        self.aux.append(SLib.AuxiliaryRectOutline(parent, 24, 24, 0, 312))

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('LemmyKoopaCastleBoss', 'lemmy_castle_boss.png')


class SpriteImage_ScrewMushroomNoBolt(SpriteImage_ScrewMushroom):  # 382
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.hasBolt = False


class SpriteImage_KamekController(SLib.SpriteImage):  # 383
    def __init__(self, parent):
        super().__init__(parent)
        self.aux.append(SLib.AuxiliaryImage(parent, 1272, 360))
        self.parent.setZValue(24999)
        self.aux[0].image = ImageCache['KamekController']
        self.aux[0].setPos(-144, 48)
        self.aux.append(SLib.AuxiliaryRectOutline(parent, 1154, 360, 0, 48))
        self.aux[1].fillFlag = False

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('KamekController', 'boss_controller_kamek.png')


class SpriteImage_PipeCooliganGenerator(SLib.SpriteImage):  # 384
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.size = (16, 32)
        self.spritebox.yOffset = -16


class SpriteImage_IceBlock(SLib.SpriteImage_StaticMultiple):  # 385
    @staticmethod
    def loadImages():
        if 'IceBlock00' in ImageCache: return
        for i in range(4):
            for j in range(4):
                ImageCache['IceBlock%d%d' % (i, j)] = SLib.GetImg('iceblock%d%d.png' % (i, j))

    def dataChanged(self):

        size = self.parent.spritedata[5]
        height = (size & 0x30) >> 4
        width = size & 3

        self.image = ImageCache['IceBlock%d%d' % (width, height)]
        self.xOffset = width * -4
        self.yOffset = height * -8

        super().dataChanged()


class SpriteImage_Bush(SLib.SpriteImage_StaticMultiple):  # 387
    def __init__(self, parent):
        # this sprite image should actually show behind layer 1...
        super().__init__(parent, 1.5)
        self.parent.setZValue(24999)

    @staticmethod
    def loadImages():
        if 'Bush00' in ImageCache: return
        for typenum, typestr in enumerate(('green', 'yellowish')):
            for sizenum, sizestr in enumerate(('small', 'med', 'large', 'xlarge')):
                ImageCache['Bush%d%d' % (typenum, sizenum)] = SLib.GetImg('bush_%s_%s.png' % (typestr, sizestr))

    def dataChanged(self):

        props = self.parent.spritedata[5]
        style = (props >> 4) & 1
        size = props & 3

        self.offset = (
            (-22, -26),
            (-28, -46),
            (-41, -62),
            (-52, -80),
        )[size]

        self.image = ImageCache['Bush%d%d' % (style, size)]

        super().dataChanged()


class SpriteImage_GlowBlock(SLib.SpriteImage):  # 391
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

        self.aux.append(SLib.AuxiliaryImage(parent, 48, 48))
        self.aux[0].image = ImageCache['GlowBlock']
        self.aux[0].setPos(-12, -12)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('GlowBlock', 'glow_block.png')


class SpriteImage_MoveWhenOn(SLib.SpriteImage):  # 396
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

    @staticmethod
    def loadImages():
        if 'MoveWhenOnL' in ImageCache: return
        ImageCache['MoveWhenOnL'] = SLib.GetImg('mwo_left.png')
        ImageCache['MoveWhenOnM'] = SLib.GetImg('mwo_middle.png')
        ImageCache['MoveWhenOnR'] = SLib.GetImg('mwo_right.png')
        ImageCache['MoveWhenOnC'] = SLib.GetImg('mwo_circle.png')

        transform90 = QtGui.QTransform()
        transform180 = QtGui.QTransform()
        transform270 = QtGui.QTransform()
        transform90.rotate(90)
        transform180.rotate(180)
        transform270.rotate(270)

        image = SLib.GetImg('sm_arrow.png', True)
        ImageCache['SmArrowR'] = QtGui.QPixmap.fromImage(image)
        ImageCache['SmArrowD'] = QtGui.QPixmap.fromImage(image.transformed(transform90))
        ImageCache['SmArrowL'] = QtGui.QPixmap.fromImage(image.transformed(transform180))
        ImageCache['SmArrowU'] = QtGui.QPixmap.fromImage(image.transformed(transform270))

    def dataChanged(self):
        super().dataChanged()

        # get width
        self.raw_size = self.parent.spritedata[5] & 0xF
        if self.raw_size == 0:
            self.xOffset = -16
            self.width = 32
        else:
            self.xOffset = 0
            self.width = self.raw_size * 16

        # set direction
        self.direction = (self.parent.spritedata[3] >> 4) % 5

    def paint(self, painter):
        super().paint(painter)

        direction = ("R", "L", "U", "D", None)[self.direction]

        if self.raw_size == 0:
            # hack for the glitchy version
            painter.drawPixmap(0, 2, ImageCache['MoveWhenOnR'])
            painter.drawPixmap(24, 2, ImageCache['MoveWhenOnL'])
        elif self.raw_size == 1:
            painter.drawPixmap(0, 2, ImageCache['MoveWhenOnM'])
        else:
            painter.drawPixmap(0, 2, ImageCache['MoveWhenOnL'])
            if self.raw_size > 2:
                painter.drawTiledPixmap(24, 2, (self.raw_size - 2) * 24, 24, ImageCache['MoveWhenOnM'])
            painter.drawPixmap(int((self.width * 1.5) - 24), 2, ImageCache['MoveWhenOnR'])

        center = int((self.width / 2) * 1.5)
        painter.drawPixmap(center - 14, 0, ImageCache['MoveWhenOnC'])
        if direction is not None:
            painter.drawPixmap(center - 12, 1, ImageCache['SmArrow%s' % direction])


class SpriteImage_GhostHouseBox(SLib.SpriteImage):  # 397
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

    @staticmethod
    def loadImages():
        if 'GHBoxTL' in ImageCache: return
        for direction in ('TL', 'T', 'TR', 'L', 'M', 'R', 'BL', 'B', 'BR'):
            ImageCache['GHBox%s' % direction] = SLib.GetImg('ghbox_%s.png' % direction)

    def dataChanged(self):
        super().dataChanged()

        height = self.parent.spritedata[4] >> 4
        width = self.parent.spritedata[5] & 15

        self.width = (width + 2) * 16
        self.height = (height + 2) * 16

    def paint(self, painter):
        super().paint(painter)

        prefix = 'GHBox'
        xsize = int(self.width * 1.5)
        ysize = int(self.height * 1.5)

        # Corners
        painter.drawPixmap(0, 0, ImageCache[prefix + 'TL'])
        painter.drawPixmap(xsize - 24, 0, ImageCache[prefix + 'TR'])
        painter.drawPixmap(0, ysize - 24, ImageCache[prefix + 'BL'])
        painter.drawPixmap(xsize - 24, ysize - 24, ImageCache[prefix + 'BR'])

        # Edges
        painter.drawTiledPixmap(24, 0, xsize - 48, 24, ImageCache[prefix + 'T'])
        painter.drawTiledPixmap(24, ysize - 24, xsize - 48, 24, ImageCache[prefix + 'B'])
        painter.drawTiledPixmap(0, 24, 24, ysize - 48, ImageCache[prefix + 'L'])
        painter.drawTiledPixmap(xsize - 24, 24, 24, ysize - 48, ImageCache[prefix + 'R'])

        # Middle
        painter.drawTiledPixmap(24, 24, xsize - 48, ysize - 48, ImageCache[prefix + 'M'])


class SpriteImage_LongSpikedStakeRight(SpriteImage_LongSpikedStake):  # 398
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.dir = 'right'
        self.aux.append(SLib.AuxiliaryTrackObject(parent, 1296, 16, SLib.AuxiliaryTrackObject.Horizontal))
        self.aux.append(SLib.AuxiliaryImage(parent, 2021, 99))

        self.dimensions = (-112, 0, 128, 66)  # 6 mid sections + end section


class SpriteImage_LongSpikedStakeLeft(SpriteImage_LongSpikedStake):  # 400
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.dir = 'left'
        self.aux.append(SLib.AuxiliaryTrackObject(parent, 1296, 16, SLib.AuxiliaryTrackObject.Horizontal))
        self.aux.append(SLib.AuxiliaryImage(parent, 2021, 99))

        self.dimensions = (0, 0, 128, 66)


class SpriteImage_MassiveSpikedStakeDown(SpriteImage_MassiveSpikedStake):  # 401
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.dir = 'down'
        self.aux.append(SLib.AuxiliaryTrackObject(parent, 16, 80, SLib.AuxiliaryTrackObject.Vertical))
        self.aux.append(SLib.AuxiliaryRectOutline(parent, 240, 2664, 4, 2944))
        self.aux.append(SLib.AuxiliaryImage(parent, 248, 3016))

        self.dimensions = (-67, -123, 165, 139)


class SpriteImage_LineQBlock(SpriteImage_Block):  # 402
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.tilenum = 49
        self.twelveIsMushroom = True


class SpriteImage_LineBrickBlock(SpriteImage_Block):  # 403
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.tilenum = 48


class SpriteImage_MassiveSpikedStakeUp(SpriteImage_MassiveSpikedStake):  # 404
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.dir = 'up'
        self.aux.append(SLib.AuxiliaryTrackObject(parent, 16, 80, SLib.AuxiliaryTrackObject.Vertical))
        self.aux.append(SLib.AuxiliaryRectOutline(parent, 240, 2664, 4, -2592))
        self.aux.append(SLib.AuxiliaryImage(parent, 248, 3016))

        self.dimensions = (-67, 0, 165, 139)


class SpriteImage_BowserJr2ndController(SLib.SpriteImage):  # 405
    def __init__(self, parent):
        super().__init__(parent)
        self.parent.setZValue(24999)

        self.aux.append(SLib.AuxiliaryImage(parent, 672, 384))
        self.aux[0].image = ImageCache['BowserJr2ndController']
        self.aux[0].setPos(-504, -336)

        self.aux.append(SLib.AuxiliaryRectOutline(parent, 24, 24, -504, -312))

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('BowserJr2ndController', 'boss_controller_bowserjr_2.png')


class SpriteImage_BowserJr3rdController(SLib.SpriteImage):  # 406
    def __init__(self, parent):
        super().__init__(parent)
        self.parent.setZValue(24999)

        self.aux.append(SLib.AuxiliaryImage(parent, 672, 372))
        self.aux[0].image = ImageCache['BowserJr3rdController']
        self.aux[0].setPos(-324, -192)

        self.aux.append(SLib.AuxiliaryRectOutline(parent, 24, 24, -324, -192))

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('BowserJr3rdController', 'boss_controller_bowserjr_3.png')


class SpriteImage_BossControllerCastleBoss(SLib.SpriteImage):  # 407
    def __init__(self, parent):
        super().__init__(parent)

        self.aux.append(SLib.AuxiliaryImage(parent, 48, 96))
        self.aux.append(SLib.AuxiliaryImage(parent, 48, 96))
        self.aux.append(SLib.AuxiliaryImage(parent, 48, 96))
        self.aux.append(SLib.AuxiliaryImage(parent, 48, 96))
        self.aux[0].image = ImageCache['ShutterDoor']
        self.aux[1].image = ImageCache['ShutterDoor']
        self.aux[1].alpha = 0.375
        self.aux[2].image = ImageCache['ShutterDoor']
        self.aux[3].image = ImageCache['ShutterDoor']
        self.aux[3].alpha = 0.375

    def dataChanged(self):
        boss = (self.parent.spritedata[5] & 0xF) % 7

        self.aux[0].setPos(*(
            (0, -216),
            (0, -216),
            (0, -216),
            (0, -216),
            (0, -216),
            (0, -240),
            (0, -216)
        )[boss])
        self.aux[1].setPos(self.aux[0].x(), self.aux[0].y() + 96)
        self.aux[2].setPos(*(
            (576, -120),
            (576, -120),
            (600, -120),
            (576, -120),
            (576, -120),
            (600, -120),
            (576, -487)
        )[boss])
        self.aux[3].setPos(self.aux[2].x(), self.aux[2].y() - 96)

        super().dataChanged()

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('ShutterDoor', 'shutter_door.png')


class SpriteImage_Gabon(SLib.SpriteImage_StaticMultiple):  # 414
    @staticmethod
    def loadImages():
        if 'GabonLeft' in ImageCache: return
        gabon = SLib.GetImg('gabon.png', True)
        ImageCache['GabonLeft'] = QtGui.QPixmap.fromImage(gabon)
        ImageCache['GabonRight'] = QtGui.QPixmap.fromImage(gabon.mirrored(True, False))
        SLib.loadIfNotInImageCache('GabonSpike', 'gabon_spike.png')

    def dataChanged(self):
        throwdir = self.parent.spritedata[5] & 1
        facing = self.parent.spritedata[4] & 1

        if throwdir == 0:
            self.image = ImageCache['GabonSpike']
            self.offset = (-7, -31)  #-11, -47
        else:
            self.image = (
                ImageCache['GabonLeft'],
                ImageCache['GabonRight'],
            )[facing]
            self.offset = (-8, -33)  #-12, -50

        super().dataChanged()


class SpriteImage_InvisibleOneUp(SLib.SpriteImage_Static):  # 416
    def __init__(self, parent):
        super().__init__(
            parent,
            1.5,
            ImageCache['InvisibleOneUp'],
            (3, 5),
        )
        self.alpha = 0.65

    @staticmethod
    def loadImages():
        if 'InvisibleOneUp' in ImageCache: return
        ImageCache['InvisibleOneUp'] = ImageCache['BlockContents'][11].scaled(16, 16)


class SpriteImage_GiantGlowBlock(SLib.SpriteImage):  # 420
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

        self.aux.append(SLib.AuxiliaryImage(parent, 100, 100))
        self.size = (32, 32)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('GiantGlowBlockOn', 'giant_glow_block.png')
        SLib.loadIfNotInImageCache('GiantGlowBlockOff', 'giant_glow_block_off.png')

    def dataChanged(self):
        super().dataChanged()

        type = self.parent.spritedata[4] >> 4
        if type == 0:
            self.aux[0].image = ImageCache['GiantGlowBlockOn']
            self.aux[0].setSize(100, 100, -25, -30)
        else:
            self.aux[0].image = ImageCache['GiantGlowBlockOff']
            self.aux[0].setSize(48, 48)


class SpriteImage_ToadQBlock(SpriteImage_Block):  # 422
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.tilenum = 49
        self.contentsOverride = 16


class SpriteImage_ToadBrickBlock(SpriteImage_Block):  # 423
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.tilenum = 48
        self.contentsOverride = 16


class SpriteImage_PalmTree(SLib.SpriteImage_StaticMultiple):  # 424
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.parent.setZValue(24999)
        self.xOffset = -24.5

    @staticmethod
    def loadImages():
        if 'PalmTree0' in ImageCache: return
        for i in range(8):
            ImageCache['PalmTree%d' % i] = SLib.GetImg('palmtree_%d.png' % i)

    def dataChanged(self):

        size = self.parent.spritedata[5] & 7
        self.image = ImageCache['PalmTree%d' % size]
        self.yOffset = 16 - (self.image.height() / 1.5)

        super().dataChanged()


class SpriteImage_Jellybeam(SLib.SpriteImage_Static):  # 425
    def __init__(self, parent):
        super().__init__(
            parent,
            1.5,
            ImageCache['Jellybeam'],
            (-6, 0),
        )

        self.aux.append(SLib.AuxiliaryTrackObject(parent, 16, 16, SLib.AuxiliaryTrackObject.Vertical))

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('Jellybeam', 'jellybeam.png')

    def dataChanged(self):
        distance = self.parent.spritedata[5] & 3
        self.aux[0].setSize(16, (distance * 32) + 108)
        self.aux[0].setPos(self.width * 0.75 - 14, self.height * 0.75 - 16)

        super().dataChanged()


class SpriteImage_BowserController(SLib.SpriteImage):  # 431
    def __init__(self, parent):
        super().__init__(parent)

        self.aux.append(SLib.AuxiliaryImage(parent, 48, 288))
        self.aux[0].image = ImageCache['BowserShutterDoor']
        self.aux[0].setPos(1248, -288)

        self.aux.append(SLib.AuxiliaryRectOutline(parent, 768, 408, 1248, -336))
        self.aux[1].fillFlag = False

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('BowserShutterDoor', 'bowser_shutter_door.png')


class SpriteImage_WarpCannon(SLib.SpriteImage_StaticMultiple):  # 434
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.offset = (5, -25)

    @staticmethod
    def loadImages():
        if 'Warp0' in ImageCache: return
        ImageCache['Warp0'] = SLib.GetImg('warp_w5.png')
        ImageCache['Warp1'] = SLib.GetImg('warp_w6.png')
        ImageCache['Warp2'] = SLib.GetImg('warp_w8.png')

    def dataChanged(self):

        dest = self.parent.spritedata[5] & 3
        if dest == 3: dest = 0
        self.image = ImageCache['Warp%d' % dest]

        super().dataChanged()


class SpriteImage_GhostFog(SpriteImage_LiquidOrFog):  # 435
    def __init__(self, parent):
        super().__init__(parent)
        self.mid = ImageCache['GhostFog']
        self.top = self.parent.objy

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('GhostFog', 'fog_ghost.png')

    def dataChanged(self):
        self.locId = self.parent.spritedata[5] & 0x7F
        super().dataChanged()

    def positionChanged(self):
        # This sprite's cutoff works a bit differently. The effect is always
        # fixed to the top of the zone, but only the part below the sprite image
        # is rendered.
        # BUG: This is not recreated.
        self.top = self.parent.objy
        super().positionChanged()


class SpriteImage_PurplePole(SLib.SpriteImage):  # 437
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

    @staticmethod
    def loadImages():
        if 'VertPole' in ImageCache: return
        ImageCache['VertPoleTop'] = SLib.GetImg('purple_pole_top.png')
        ImageCache['VertPole'] = SLib.GetImg('purple_pole_middle.png')
        ImageCache['VertPoleBottom'] = SLib.GetImg('purple_pole_bottom.png')

    def dataChanged(self):
        super().dataChanged()

        length = self.parent.spritedata[5]
        self.height = (length + 3) * 16

    def paint(self, painter):
        super().paint(painter)

        painter.drawPixmap(0, 0, ImageCache['VertPoleTop'])
        painter.drawTiledPixmap(0, 24, 24, int(self.height * 1.5 - 48), ImageCache['VertPole'])
        painter.drawPixmap(0, int(self.height * 1.5 - 24), ImageCache['VertPoleBottom'])


class SpriteImage_CageBlocks(SLib.SpriteImage_StaticMultiple):  # 438
    @staticmethod
    def loadImages():
        if 'CageBlock0' in ImageCache: return

        for i in range(5):
            ImageCache['CageBlock%d' % i] = SLib.GetImg('cage_block_%d.png' % i)

    def dataChanged(self):

        type = (self.parent.spritedata[4] & 15) % 5

        self.offset = (
            (-112, -112),
            (-112, -112),
            (-97, -81),
            (-80, -96),
            (-112, -112),
        )[type]

        self.image = ImageCache['CageBlock%d' % type]

        super().dataChanged()


class SpriteImage_HorizontalRope(SLib.SpriteImage):  # 440
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('HorzRope', 'horizontal_rope_middle.png')
        SLib.loadIfNotInImageCache('HorzRopeEnd', 'horizontal_rope_end.png')

    def dataChanged(self):
        super().dataChanged()

        length = self.parent.spritedata[5]
        self.width = (length + 3) * 16

    def paint(self, painter):
        super().paint(painter)

        endpiece = ImageCache['HorzRopeEnd']
        painter.drawPixmap(0, 0, endpiece)
        painter.drawTiledPixmap(24, 0, int(self.width * 1.5 - 48), 24, ImageCache['HorzRope'])
        painter.drawPixmap(int(self.width * 1.5 - 24), 0, endpiece)


class SpriteImage_MushroomPlatform(SLib.SpriteImage):  # 441
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

    @staticmethod
    def loadImages():
        if 'RedShroomL' in ImageCache: return
        ImageCache['RedShroomL'] = SLib.GetImg('red_mushroom_left.png')
        ImageCache['RedShroomM'] = SLib.GetImg('red_mushroom_middle.png')
        ImageCache['RedShroomR'] = SLib.GetImg('red_mushroom_right.png')
        ImageCache['GreenShroomL'] = SLib.GetImg('green_mushroom_left.png')
        ImageCache['GreenShroomM'] = SLib.GetImg('green_mushroom_middle.png')
        ImageCache['GreenShroomR'] = SLib.GetImg('green_mushroom_right.png')
        ImageCache['BlueShroomL'] = SLib.GetImg('blue_mushroom_left.png')
        ImageCache['BlueShroomM'] = SLib.GetImg('blue_mushroom_middle.png')
        ImageCache['BlueShroomR'] = SLib.GetImg('blue_mushroom_right.png')
        ImageCache['OrangeShroomL'] = SLib.GetImg('orange_mushroom_left.png')
        ImageCache['OrangeShroomM'] = SLib.GetImg('orange_mushroom_middle.png')
        ImageCache['OrangeShroomR'] = SLib.GetImg('orange_mushroom_right.png')

    def dataChanged(self):
        super().dataChanged()

        # get size/color
        self.color = self.parent.spritedata[4] & 1
        self.shroomsize = (self.parent.spritedata[5] >> 4) & 1
        self.height = 16 * (self.shroomsize + 1)

        # get width
        width = self.parent.spritedata[5] & 0xF
        if self.shroomsize == 0:
            self.width = (width << 4) + 32
            self.offset = (
                0 - (((width + 1) // 2) << 4),
                0,
            )
        else:
            self.width = (width << 5) + 64
            self.offset = (
                16 - (self.width / 2),
                -16,
            )

    def paint(self, painter):
        super().paint(painter)

        tilesize = 24 + (self.shroomsize * 24)
        if self.shroomsize == 0:
            if self.color == 0:
                color = 'Orange'
            else:
                color = 'Blue'
        else:
            if self.color == 0:
                color = 'Red'
            else:
                color = 'Green'

        painter.drawPixmap(0, 0, ImageCache[color + 'ShroomL'])
        painter.drawTiledPixmap(tilesize, 0, int((self.width * 1.5) - (tilesize * 2)), tilesize,
                                ImageCache[color + 'ShroomM'])
        painter.drawPixmap(int(self.width * 1.5) - tilesize, 0, ImageCache[color + 'ShroomR'])


class SpriteImage_UnderwaterLamp(SLib.SpriteImage):  # 447
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

        self.aux.append(SLib.AuxiliaryImage(parent, 105, 105))
        self.aux[0].image = ImageCache['UnderwaterLamp']
        self.aux[0].setPos(-34, -34)

        self.dimensions = (-4, -4, 24, 26)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('UnderwaterLamp', 'underwater_lamp.png')


class SpriteImage_Pipe_EnterableUp(SpriteImage_PipeStationary):  # 450
    def dataChanged(self):
        self.length = (self.parent.spritedata[5] & 0xF) + 2
        super().dataChanged()


class SpriteImage_BowserDoor(SLib.SpriteImage_Static):  # 452
    def __init__(self, parent):
        super().__init__(
            parent,
            1.5,
            ImageCache['BowserDoor'],
            (-53, -130),
        )
        self.aux.append(SLib.AuxiliaryRectOutline(parent, 24, 24))
        self.aux[0].setIsBehindSprite(False)
        self.aux[0].setPos(91, 243)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('BowserDoor', 'bowser_door.png')


class SpriteImage_Seaweed(SLib.SpriteImage_StaticMultiple):  # 453
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.parent.setZValue(24998)

    @staticmethod
    def loadImages():
        if 'Seaweed0' in ImageCache: return
        for i in range(4):
            ImageCache['Seaweed%d' % i] = SLib.GetImg('seaweed_%d.png' % i)

    def dataChanged(self):
        SeaweedSizes = [0, 1, 2, 2, 3, 3]
        SeaweedXOffsets = [-15, -25, -29, -38]

        style = (self.parent.spritedata[5] & 0xF) % 6
        size = SeaweedSizes[style]

        self.image = ImageCache['Seaweed%d' % size]
        self.offset = (
            SeaweedXOffsets[size],
            16 - (self.image.height() / 1.5),
        )

        super().dataChanged()


class SpriteImage_BossBridge(SLib.SpriteImage_StaticMultiple):  # 456
    @staticmethod
    def loadImages():
        if 'BossBridgeL' in ImageCache: return
        ImageCache['BossBridgeL'] = SLib.GetImg('boss_bridge_left.png')
        ImageCache['BossBridgeM'] = SLib.GetImg('boss_bridge_middle.png')
        ImageCache['BossBridgeR'] = SLib.GetImg('boss_bridge_right.png')

    def dataChanged(self):
        style = (self.parent.spritedata[5] & 3) % 3
        self.image = (
            ImageCache['BossBridgeM'],
            ImageCache['BossBridgeR'],
            ImageCache['BossBridgeL'],
        )[style]

        super().dataChanged()


class SpriteImage_LongMetalBar(SLib.SpriteImage):  # 458
    def __init__(self, parent):
        super().__init__(parent)
        i = ImageCache['LongMetalBar']
        self.aux.append(SLib.AuxiliaryImage(parent, i.width(), i.height()))
        self.aux[0].image = i
        self.aux[0].setSize(i.width(), i.height(), -252, -24)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('LongMetalBar', 'long_metal_bar.png')


class SpriteImage_SilverGearBlock(SLib.SpriteImage_StaticMultiple):  # 460
    @staticmethod
    def loadImages():
        if 'SilverGearBlockDown3' in ImageCache: return
        for gear in range(4):
            image = SLib.GetImg('silver_gear_block_%d.png' % gear, True)
            ImageCache['SilverGearBlockUp%d' % gear] = QtGui.QPixmap.fromImage(image)
            ImageCache['SilverGearBlockDown%d' % gear] = QtGui.QPixmap.fromImage(image.mirrored(True, True))

    def dataChanged(self):
        style = self.parent.spritedata[5] & 3
        flipped = (self.parent.spritedata[5] >> 4) & 1

        if flipped:
            self.image = ImageCache['SilverGearBlockDown%d' % style]
        else:
            self.image = ImageCache['SilverGearBlockUp%d' % style]

        super().dataChanged()


class SpriteImage_EnormousBlock(SLib.SpriteImage):  # 462
    def __init__(self, parent):
        super().__init__(parent, 1.5)

        self.aux.append(SLib.AuxiliaryRectOutline(parent, 24, 24))
        self.aux.append(
            SLib.AuxiliaryPainterPath(parent, QtGui.QPainterPath(), 24, 24)
        )
        self.aux.append(
            SLib.AuxiliaryTrackObject(parent, 16, 16, SLib.AuxiliaryTrackObject.Horizontal)
        )

        self.spikes = []
        for height in (28, 16, 41, 47, 31):
            spikes = []
            for direction in range(2):
                # This has to be within the loop because the
                # following commands transpose them
                if direction == 0:
                    points = ((0, 0), (24, 12))
                else:
                    # faces right
                    points = ((24, 0), (0, 12))

                painterPath = QtGui.QPainterPath()
                painterPath.moveTo(direction * 24, 0)
                for i in range(height):
                    for point in points:
                        painterPath.lineTo(QtCore.QPointF(point[0], point[1] + i * 24))
                painterPath.lineTo(QtCore.QPointF(direction * 24, height * 24))
                painterPath.closeSubpath()
                spikes.append(painterPath)
            self.spikes.append(spikes)

    def dataChanged(self):
        # get sprite data
        size = (self.parent.spritedata[5] >> 1) & 7
        direction = self.parent.spritedata[2] & 1
        distance = (self.parent.spritedata[4] >> 4) + 1
        side = self.parent.spritedata[5] & 1

        # update the platform
        realsize = ((18, 28), (18, 16), (18, 41), (18, 47), (24, 31))[size]
        self.aux[0].setSize(realsize[0] * 24 - 24, realsize[1] * 24)
        if side == 0:
            self.aux[0].setPos(0, 0)
        else:
            self.aux[0].setPos(24, 0)

        # update the spikes
        self.aux[1].setSize(48, realsize[1] * 24 + 24)
        if side == 0:
            self.aux[1].setPos(realsize[0] * 24 - 24, 0)
        else:
            self.aux[1].setPos(0, 0)
        self.aux[1].setPath(self.spikes[size][side])

        # update the track
        self.aux[2].setSize(distance * 16, 16)
        halfheight = realsize[1] * 12 - 12
        halfwidth = realsize[0] * 12
        if direction == 0:
            self.aux[2].setPos(halfwidth, halfheight)
        else:
            self.aux[2].setPos(halfwidth - distance * 24, halfheight)


class SpriteImage_Glare(SLib.SpriteImage):  # 463
    def __init__(self, parent):
        super().__init__(parent)
        self.aux.append(SLib.AuxiliaryImage(parent, 1000, 1000))
        self.aux[0].image = ImageCache['SunGlare']
        self.aux[0].setSize(9 * 24, 9 * 24, -4 * 24 - 5, -4 * 24 - 20)

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('SunGlare', 'glare.png')


class SpriteImage_SwingingVine(SLib.SpriteImage_StaticMultiple):  # 464
    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('SwingVine', 'swing_vine.png')
        SLib.loadIfNotInImageCache('SwingChain', 'swing_chain.png')

    def dataChanged(self):
        style = self.parent.spritedata[5] & 1
        self.image = ImageCache['SwingVine'] if not style else ImageCache['SwingChain']

        super().dataChanged()


class SpriteImage_LavaIronBlock(SLib.SpriteImage_Static):  # 466
    def __init__(self, parent):
        super().__init__(
            parent,
            1.5,
            ImageCache['LavaIronBlock'],
            (-1, -1),
        )

        self.aux.append(SLib.AuxiliaryTrackObject(parent, 16, 16, SLib.AuxiliaryTrackObject.Horizontal))

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('LavaIronBlock', 'lava_iron_block.png')

    def dataChanged(self):
        direction = self.parent.spritedata[2] & 3
        distance = (self.parent.spritedata[4] & 0xF0) >> 4

        if direction <= 1:  # horizontal
            self.aux[0].direction = 1
            self.aux[0].setSize((distance * 16) + 16, 16)
        else:  # vertical
            self.aux[0].direction = 2
            self.aux[0].setSize(16, (distance * 16) + 16)

        if direction == 0:  # right
            self.aux[0].setPos(self.width + 48, self.height / 2)
        elif direction == 1:  # left
            self.aux[0].setPos((-distance * 24) + 2, self.height / 2)
        elif direction == 2:  # up
            self.aux[0].setPos((self.width * 0.75) - 12, (-distance * 24))
        else:  # down
            self.aux[0].setPos((self.width * 0.75) - 12, self.height)

        super().dataChanged()


class SpriteImage_MovingGemBlock(SLib.SpriteImage_Static):  # 467
    def __init__(self, parent):
        super().__init__(
            parent,
            1.5,
            ImageCache['MovingGemBlock'],
        )

        self.aux.append(SLib.AuxiliaryTrackObject(parent, 16, 16, SLib.AuxiliaryTrackObject.Vertical))

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('MovingGemBlock', 'moving_gem_block.png')

    def dataChanged(self):
        direction = self.parent.spritedata[2] & 1
        distance = (self.parent.spritedata[4] & 0xF0) >> 4

        self.aux[0].setSize(16, (distance * 16) + 16)
        if direction == 0:  # up
            self.aux[0].setPos(self.width / 2, -distance * 24)
        else:  # down
            self.aux[0].setPos(self.width / 2, self.height - 8)

        super().dataChanged()


class SpriteImage_BoltPlatform(SLib.SpriteImage):  # 469
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.spritebox.shown = False

    @staticmethod
    def loadImages():
        if 'BoltPlatformL' in ImageCache: return
        ImageCache['BoltPlatformL'] = SLib.GetImg('bolt_platform_left.png')
        ImageCache['BoltPlatformM'] = SLib.GetImg('bolt_platform_middle.png')
        ImageCache['BoltPlatformR'] = SLib.GetImg('bolt_platform_right.png')

    def dataChanged(self):
        super().dataChanged()

        length = self.parent.spritedata[5] & 0xF
        self.width = (length + 2) * 16

    def paint(self, painter):
        super().paint(painter)

        painter.drawPixmap(0, 0, ImageCache['BoltPlatformL'])

        #print(ImageCache['BoltPlatformL'].width(), ImageCache['BoltPlatformL'].height(),
        #      ImageCache['BoltPlatformM'].width(), ImageCache['BoltPlatformM'].height(),
        #      ImageCache['BoltPlatformR'].width(), ImageCache['BoltPlatformR'].height(),)

        painter.drawTiledPixmap(24, 3, int(self.width * 1.5) - 48, 24, ImageCache['BoltPlatformM'])
        painter.drawPixmap(int(self.width * 1.5) - 24, 0, ImageCache['BoltPlatformR'])


class SpriteImage_PotPlatform(SLib.SpriteImage_Static):  # 471
    def __init__(self, parent):
        super().__init__(
            parent,
            1.5,
            ImageCache['PotPlatform'],
            (-12, -2),
        )

    @staticmethod
    def loadImages():
        if 'PotPlatform' in ImageCache: return
        top = SLib.GetImg('pot_platform_top.png')
        mid = SLib.GetImg('pot_platform_middle.png')
        full = QtGui.QPixmap(77, 722)

        full.fill(Qt.transparent)
        painter = QtGui.QPainter(full)
        painter.drawPixmap(0, 0, top)
        painter.drawTiledPixmap(12, 143, 52, 579, mid)
        del painter

        ImageCache['PotPlatform'] = full


class SpriteImage_IceFloeGenerator(SLib.SpriteImage):  # 472
    def __init__(self, parent):
        super().__init__(parent)
        self.aux.append(SLib.AuxiliaryRectOutline(parent, 96, 120, 0, -96))


class SpriteImage_FloatingIceFloeGenerator(SLib.SpriteImage):  # 473
    def __init__(self, parent):
        super().__init__(parent)
        self.aux.append(SLib.AuxiliaryRectOutline(parent, 96, 96, 0, 24))


class SpriteImage_IceFloe(SLib.SpriteImage_StaticMultiple):  # 475
    def __init__(self, parent):
        super().__init__(parent, 1.5)
        self.alpha = 0.65

    @staticmethod
    def loadImages():
        if 'IceFloe0' in ImageCache: return

        for size in range(13):
            ImageCache['IceFloe%d' % size] = SLib.GetImg('ice_floe_%d.png' % size)

    def dataChanged(self):

        size = self.parent.spritedata[5] & 15

        if size > 12:
            size = 0

        self.offset = (
            (-1, -32),  # 0: 3x3
            (-2, -48),  # 1: 4x4
            (-2, -64),  # 2: 5x5
            (-2, -32),  # 3: 4x3
            (-2, -48),  # 4: 5x4
            (-3, -80),  # 5: 7x6
            (-3, -160),  # 6: 16x11
            (-3, -112),  # 7: 11x8
            (-1, -48),  # 8: 2x4
            (-2, -48),  # 9: 3x4
            (-2.5, -96),  # 10: 6x7
            (-1, -64),  # 11: 2x5
            (-1, -64),  # 12: 3x5
        )[size]

        self.image = ImageCache['IceFloe%d' % size]

        super().dataChanged()


class SpriteImage_BowserSwitchSm(SLib.SpriteImage_StaticMultiple):  # 478
    @staticmethod
    def loadImages():
        if 'ESwitch' in ImageCache: return
        e = SLib.GetImg('e_switch.png', True)
        ImageCache['ESwitch'] = QtGui.QPixmap.fromImage(e)
        ImageCache['ESwitchU'] = QtGui.QPixmap.fromImage(e.mirrored(True, True))

    def dataChanged(self):

        upsideDown = self.parent.spritedata[5] & 1
        if not upsideDown:
            self.image = ImageCache['ESwitch']
        else:
            self.image = ImageCache['ESwitchU']

        super().dataChanged()


class SpriteImage_BowserSwitchLg(SLib.SpriteImage_StaticMultiple):  # 479
    @staticmethod
    def loadImages():
        if 'ELSwitch' in ImageCache: return
        elg = SLib.GetImg('e_switch_lg.png', True)
        ImageCache['ELSwitch'] = QtGui.QPixmap.fromImage(elg)
        ImageCache['ELSwitchU'] = QtGui.QPixmap.fromImage(elg.mirrored(True, True))

    def dataChanged(self):

        upsideDown = self.parent.spritedata[5] & 1
        if not upsideDown:
            self.image = ImageCache['ELSwitch']
            self.offset = (-15, -24)
        else:
            self.image = ImageCache['ELSwitchU']
            self.offset = (-15, 0)

        super().dataChanged()


class SpriteImage_MortonSpikedStake(SLib.SpriteImage):  # 480
    def __init__(self, parent):
        super().__init__(parent)
        self.spritebox.shown = False
        self.dimensions = (0, -368, 64, 410)
        self.aux.append(SLib.AuxiliaryTrackObject(parent, 36, 591, SLib.AuxiliaryTrackObject.Vertical))

    @staticmethod
    def loadImages():
        SLib.loadIfNotInImageCache('MortonStakeM', 'stake_down_m_0.png')
        SLib.loadIfNotInImageCache('MortonStakeE', 'stake_down_e_0.png')

    def dataChanged(self):
        super().dataChanged()

        self.aux[0].setPos(36, 591)
        self.aux[0].setSize(16, 160)

    def paint(self, painter):
        super().paint(painter)

        painter.drawTiledPixmap(0, 0, 98, 576, ImageCache['MortonStakeM'])
        painter.drawPixmap(0, 576, ImageCache['MortonStakeE'])


class SpriteImage_FinalBossRubble(SLib.SpriteImage_StaticMultiple):  # 481
    def __init__(self, parent):
        super().__init__(parent)

    @staticmethod
    def loadImages():
        if 'FinalBossRubble0' in ImageCache: return
        for size in range(2):
            ImageCache['FinalBossRubble%d' % size] = SLib.GetImg('final_boss_rubble_%d.png' % size)

    def dataChanged(self):
        size = self.parent.spritedata[5] & 1

        self.image = ImageCache['FinalBossRubble%d' % size]

        super().dataChanged()


class SpriteImage_FinalBossEffects(SLib.SpriteImage):  # 482
    def __init__(self, parent):
        super().__init__(parent)
        self.aux.append(SLib.AuxiliaryImage(parent, 3612, 672))
        self.aux[0].image = ImageCache['FinalBossEffects0']
        self.aux[0].setPos(-228, -555)
        self.parent.setZValue(24999)

    @staticmethod
    def loadImages():
        if 'FinalBossEffects0' in ImageCache: return

        for i in range(3):
            ImageCache["FinalBossEffects%d" % i] = SLib.GetImg("final_boss_effects_%d.png" % i)

    def dataChanged(self):
        style = self.parent.spritedata[5] & 15

        # Styles greater than 2 load nothing
        if style > 2:
            self.aux[0].image = None

        else:
            self.aux[0].image = ImageCache['FinalBossEffects%d' % style]

            if style == 0:
                self.aux[0].setPos(-228, -555)
            elif style == 1:
                self.aux[0].setPos(-228, -408)
            else:
                self.aux[0].setPos(-24, -192)

        super().dataChanged()


################################################################
################################################################
################################################################
################################################################


ImageClasses = {
                   0: SpriteImage_MeasureJump,
                   23: SpriteImage_HorzMovingPlatform,
                   27: SpriteImage_DSStoneBlock_Vert,
                   28: SpriteImage_DSStoneBlock_Horz,
                   30: SpriteImage_OldStoneBlock_NoSpikes,
                   31: SpriteImage_VertMovingPlatform,
                   40: SpriteImage_QSwitch,
                   41: SpriteImage_PSwitch,
                   42: SpriteImage_ExcSwitch,
                   46: SpriteImage_Podoboo,
                   49: SpriteImage_UnusedSeesaw,
                   50: SpriteImage_FallingPlatform,
                   52: SpriteImage_UnusedRotPlatforms,
                   53: SpriteImage_Quicksand,
                   55: SpriteImage_UnusedRisingSeesaw,
                   57: SpriteImage_KoopaTroopa,
                   58: SpriteImage_KoopaParatroopa,
                   60: SpriteImage_SpikeTop,
                   61: SpriteImage_BigBoo,
                   62: SpriteImage_SpinningFirebar,
                   64: SpriteImage_OutdoorsFog,
                   73: SpriteImage_GroundPiranha,
                   74: SpriteImage_BigGroundPiranha,
                   75: SpriteImage_GroundFiretrap,
                   76: SpriteImage_BigGroundFiretrap,
                   78: SpriteImage_CloudTrampoline,
                   81: SpriteImage_OldStoneBlock_SpikesLeft,
                   82: SpriteImage_OldStoneBlock_SpikesRight,
                   83: SpriteImage_OldStoneBlock_SpikesLeftRight,
                   84: SpriteImage_OldStoneBlock_SpikesTop,
                   85: SpriteImage_OldStoneBlock_SpikesBottom,
                   86: SpriteImage_OldStoneBlock_SpikesTopBottom,
                   87: SpriteImage_TrampolineWall,
                   92: SpriteImage_BulletBillLauncher,
                   96: SpriteImage_RotationControllerSwaying,
                   97: SpriteImage_RotationControlledSolidBetaPlatform,
                   99: SpriteImage_PipeEnemyGenerator,
                   103: SpriteImage_PlatformGenerator,
                   105: SpriteImage_Pokey,
                   106: SpriteImage_LinePlatform,
                   107: SpriteImage_RotationControlledPassBetaPlatform,
                   109: SpriteImage_ChainBall,
                   110: SpriteImage_Sunlight,
                   113: SpriteImage_Flagpole,
                   114: SpriteImage_FlameCannon,
                   115: SpriteImage_Cheep,
                   116: SpriteImage_CoinCheep,
                   117: SpriteImage_PulseFlameCannon,
                   122: SpriteImage_OneWayPlatform,
                   123: SpriteImage_UnusedCastlePlatform,
                   125: SpriteImage_FenceKoopaHorz,
                   126: SpriteImage_FenceKoopaVert,
                   129: SpriteImage_4Spinner,
                   131: SpriteImage_Boo,
                   132: SpriteImage_UnusedBlockPlatform1,
                   133: SpriteImage_StalagmitePlatform,
                   135: SpriteImage_HangingPlatform,
                   136: SpriteImage_RotBulletLauncher,
                   137: SpriteImage_SpikedStakeDown,
                   138: SpriteImage_Water,
                   139: SpriteImage_Lava,
                   140: SpriteImage_SpikedStakeUp,
                   141: SpriteImage_SpikedStakeRight,
                   142: SpriteImage_SpikedStakeLeft,
                   143: SpriteImage_Arrow,
                   145: SpriteImage_FloatingBarrel,
                   147: SpriteImage_Coin,
                   148: SpriteImage_Spring,
                   149: SpriteImage_RotationControllerSpinning,
                   156: SpriteImage_RedCoinRing,
                   157: SpriteImage_BigBrick,
                   158: SpriteImage_FireSnake,
                   160: SpriteImage_UnusedBlockPlatform2,
                   161: SpriteImage_PipeBubbles,
                   166: SpriteImage_BlockTrain,
                   172: SpriteImage_ScrewMushroomWithBolt,
                   174: SpriteImage_OneWayGate,
                   175: SpriteImage_FlyingQBlock,
                   178: SpriteImage_ScalePlatform,
                   179: SpriteImage_SpecialExit,
                   182: SpriteImage_EventDoor,
                   191: SpriteImage_TileEvent,
                   192: SpriteImage_LarryKoopaCastleBoss,
                   193: SpriteImage_Urchin,
                   194: SpriteImage_MegaUrchin,
                   195: SpriteImage_HuckitCrab,
                   196: SpriteImage_Fishbones,
                   197: SpriteImage_Clam,
                   198: SpriteImage_GiantGoomba,
                   201: SpriteImage_Icicle,
                   205: SpriteImage_GiantBubbleNormal,
                   206: SpriteImage_Zoom,
                   207: SpriteImage_QBlock,
                   208: SpriteImage_QBlockUnused,
                   209: SpriteImage_BrickBlock,
                   211: SpriteImage_BowserJr1stController,
                   212: SpriteImage_RollingHill,
                   216: SpriteImage_Poison,
                   219: SpriteImage_LineBlock,
                   221: SpriteImage_InvisibleBlock,
                   223: SpriteImage_SpringBlock,
                   224: SpriteImage_JumboRay,
                   226: SpriteImage_GiantBubbleUnused,
                   227: SpriteImage_PipeCannon,
                   228: SpriteImage_ExtendShroom,
                   231: SpriteImage_WiggleShroom,
                   233: SpriteImage_Bulber,
                   254: SpriteImage_RotControlledPipe,
                   255: SpriteImage_RotatingQBlock,
                   257: SpriteImage_MoveWhenOnMetalLavaBlock,
                   256: SpriteImage_RotatingBrickBlock,
                   259: SpriteImage_RegularDoor,
                   260: SpriteImage_MovementController_TwoWayLine,
                   261: SpriteImage_OldStoneBlock_MovementControlled,
                   262: SpriteImage_PoltergeistItem,
                   263: SpriteImage_WaterPiranha,
                   265: SpriteImage_FallingIcicle,
                   266: SpriteImage_RotatingFence,
                   267: SpriteImage_TiltGrate,
                   268: SpriteImage_LavaGeyser,
                   269: SpriteImage_Parabomb,
                   271: SpriteImage_ScaredyRat,
                   274: SpriteImage_CastleGear,
                   276: SpriteImage_GhostDoor,
                   277: SpriteImage_TowerDoor,
                   278: SpriteImage_CastleDoor,
                   280: SpriteImage_GiantIceBlock,
                   286: SpriteImage_WoodCircle,
                   287: SpriteImage_PathIceBlock,
                   289: SpriteImage_Box,
                   291: SpriteImage_Parabeetle,
                   292: SpriteImage_HeavyParabeetle,
                   295: SpriteImage_NutPlatform,
                   296: SpriteImage_MegaBuzzy,
                   297: SpriteImage_DragonCoaster,
                   298: SpriteImage_LongCannon,
                   299: SpriteImage_CannonMulti,
                   300: SpriteImage_RotCannon,
                   301: SpriteImage_RotCannonPipe,
                   303: SpriteImage_MontyMole,
                   304: SpriteImage_RotFlameCannon,
                   305: SpriteImage_LightCircle,
                   306: SpriteImage_RotSpotlight,
                   309: SpriteImage_SynchroFlameJet,
                   310: SpriteImage_ArrowSign,
                   314: SpriteImage_BubbleGen,
                   316: SpriteImage_BoltBox,
                   321: SpriteImage_ArrowBlock,
                   323: SpriteImage_BooCircle,
                   326: SpriteImage_KingBill,
                   328: SpriteImage_BubbleCannon,
                   330: SpriteImage_RopeLadder,
                   331: SpriteImage_DishPlatform,
                   334: SpriteImage_CheepGiant,
                   338: SpriteImage_MovingBulletBillLauncher,
                   339: SpriteImage_Pipe_MovingUp,
                   341: SpriteImage_BigShell,
                   342: SpriteImage_Muncher,
                   343: SpriteImage_Fuzzy,
                   346: SpriteImage_HangingChainPlatform,
                   349: SpriteImage_MortonKoopaCastleBoss,
                   353: SpriteImage_Pipe_MovingDown,
                   354: SpriteImage_BrownBlock,
                   355: SpriteImage_RollingHillWith1Pipe,
                   356: SpriteImage_BrownBlock,
                   357: SpriteImage_Fruit,
                   358: SpriteImage_LavaParticles,
                   359: SpriteImage_WallLantern,
                   360: SpriteImage_RollingHillWith8Pipes,
                   361: SpriteImage_CrystalBlock,
                   362: SpriteImage_ColoredBox,
                   364: SpriteImage_RoyKoopaCastleBoss,
                   365: SpriteImage_LudwigVonKoopaCastleBoss,
                   366: SpriteImage_CubeKinokoRot,
                   368: SpriteImage_FlashRaft,
                   369: SpriteImage_SlidingPenguin,
                   372: SpriteImage_IggyKoopaCastleBoss,
                   373: SpriteImage_RaftWater,
                   374: SpriteImage_SnowWind,
                   375: SpriteImage_WendyKoopaCastleBoss,
                   376: SpriteImage_MovingFence,
                   377: SpriteImage_Pipe_Up,
                   378: SpriteImage_Pipe_Down,
                   379: SpriteImage_Pipe_Right,
                   380: SpriteImage_Pipe_Left,
                   381: SpriteImage_LemmyKoopaCastleBoss,
                   382: SpriteImage_ScrewMushroomNoBolt,
                   383: SpriteImage_KamekController,
                   384: SpriteImage_PipeCooliganGenerator,
                   385: SpriteImage_IceBlock,
                   387: SpriteImage_Bush,
                   391: SpriteImage_GlowBlock,
                   396: SpriteImage_MoveWhenOn,
                   397: SpriteImage_GhostHouseBox,
                   398: SpriteImage_LongSpikedStakeRight,
                   400: SpriteImage_LongSpikedStakeLeft,
                   401: SpriteImage_MassiveSpikedStakeDown,
                   402: SpriteImage_LineQBlock,
                   403: SpriteImage_LineBrickBlock,
                   404: SpriteImage_MassiveSpikedStakeUp,
                   405: SpriteImage_BowserJr2ndController,
                   406: SpriteImage_BowserJr3rdController,
                   407: SpriteImage_BossControllerCastleBoss,
                   414: SpriteImage_Gabon,
                   416: SpriteImage_InvisibleOneUp,
                   420: SpriteImage_GiantGlowBlock,
                   422: SpriteImage_ToadQBlock,
                   423: SpriteImage_ToadBrickBlock,
                   424: SpriteImage_PalmTree,
                   425: SpriteImage_Jellybeam,
                   431: SpriteImage_BowserController,
                   434: SpriteImage_WarpCannon,
                   435: SpriteImage_GhostFog,
                   437: SpriteImage_PurplePole,
                   438: SpriteImage_CageBlocks,
                   440: SpriteImage_HorizontalRope,
                   441: SpriteImage_MushroomPlatform,
                   447: SpriteImage_UnderwaterLamp,
                   450: SpriteImage_Pipe_EnterableUp,
                   452: SpriteImage_BowserDoor,
                   453: SpriteImage_Seaweed,
                   456: SpriteImage_BossBridge,
                   458: SpriteImage_LongMetalBar,
                   460: SpriteImage_SilverGearBlock,
                   462: SpriteImage_EnormousBlock,
                   463: SpriteImage_Glare,
                   464: SpriteImage_SwingingVine,
                   466: SpriteImage_LavaIronBlock,
                   467: SpriteImage_MovingGemBlock,
                   469: SpriteImage_BoltPlatform,
                   471: SpriteImage_PotPlatform,
                   472: SpriteImage_IceFloeGenerator,
                   473: SpriteImage_FloatingIceFloeGenerator,
                   475: SpriteImage_IceFloe,
                   478: SpriteImage_BowserSwitchSm,
                   479: SpriteImage_BowserSwitchLg,
                   480: SpriteImage_MortonSpikedStake,
                   481: SpriteImage_FinalBossRubble,
                   482: SpriteImage_FinalBossEffects,
               } | get_registered_sprites()
