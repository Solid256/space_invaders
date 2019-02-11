import xml.etree.ElementTree as ETree
import pygame


class SpriteInfo:
    def __init__(self):
        self.n = ""
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0


class Sprites:
    def __init__(self):
        # Load the sprites from the xml file.
        self.e_tree = ETree.parse("images/sprites.xml")
        self.root = self.e_tree.getroot()

        sprite_infos_xml = self.root.findall('sprite')

        for sprite_info_xml in sprite_infos_xml:
            # The new sprite info object being created.
            sprite_info = SpriteInfo()

            # Load the sprite info attributes
            for sprite_attr in sprite_info_xml.attrib:
                if sprite_attr == 'n':
                    sprite_info.n = sprite_info_xml.get(sprite_attr)
                elif sprite_attr == 'x':
                    sprite_info.x = int(sprite_info_xml.get(sprite_attr))
                elif sprite_attr == 'y':
                    sprite_info.y = int(sprite_info_xml.get(sprite_attr))
                elif sprite_attr == 'w':
                    sprite_info.w = int(sprite_info_xml.get(sprite_attr))
                elif sprite_attr == 'h':
                    sprite_info.h = int(sprite_info_xml.get(sprite_attr))

            self.sprite_infos[sprite_info.n] = sprite_info

        # Load the sprite sheet image.
        self.sprite_sheet = pygame.image.load('images/sprites.png')

    # Member variables:

    # The sprite infos dictionary.
    sprite_infos = {}

    # The xml parser
    e_tree = 0

    # The root of the xml tree.
    root = 0
