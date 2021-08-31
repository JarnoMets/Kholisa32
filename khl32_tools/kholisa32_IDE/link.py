# This Python file uses the following encoding: utf-8
from PySide2 import QtWidgets

import sys
from img_converter import Img_converter
from PIL import Image
from typing import List, Set, Dict, Tuple, Optional

"""
Game:
    char                        title[64];
    uint8_t *                   p_icon;
    uint32_t *                  p_data;
    uint8_t **                  p_sprites;
    uint8_t **                  p_sounds;
    uint8_t *                   p_save;
    64*64 uint16_t              ICON
    n uint32_t instructions     DATA
    uint8_t *                   SPRITES ->  uint32_t        n sprites
                                            uint32_t*       p_sprite1
                                            uint32_t*       p_sprite2
                                                .               .
                                                .               .
                                                .               .
                                            uint32_t        sprite1 x
                                            uint32_t        sprite1 y
                                            uint16_t *      sprite1
                                            uint32_t        sprite2 x
                                            uint32_t        sprite2 y
                                            uint16_t *      sprite2
                                                .               .
                                                .               .
                                                .               .

    SOUND
    SAVE
"""



class Linker:
    def __init__():
        pass


    def link(strin: str) -> bytearray:
        game = bytearray()

        title = Linker.get_title(strin)
        offset_icon = 84

        icon = Linker.get_icon(strin)
        offset_game = offset_icon + (len(icon)+3)//4*4

        game_data = Linker.get_game(strin)
        offset_sprites  = offset_game + (len(game_data)+3)//4*4

        imgs = Linker.get_images(strin, offset_sprites)
        offset_sound    = offset_sprites + (len(imgs)+3)//4*4

        sounds = Linker.get_sounds(strin, offset_sound)
        offset_save     = offset_sound + (len(sounds)+3)//4*4

        b_offset_icon       = offset_icon.to_bytes(4, 'little')
        b_offset_game       = offset_game.to_bytes(4, 'little')
        b_offset_sprites    = offset_sprites.to_bytes(4, 'little')
        b_offset_sound      = offset_sound.to_bytes(4, 'little')
        b_offset_save       = offset_save.to_bytes(4, 'little')

        game.extend(title)

        """ Make sure game is saved in 32-bit multiples """

        if len(b_offset_icon)%4:
            game.extend(bytearray(4-len(b_offset_icon)%4))
        game.extend(b_offset_icon)

        if len(b_offset_game)%4:
            game.extend(bytearray(4-len(b_offset_game)%4))
        game.extend(b_offset_game)

        if len(b_offset_sprites)%4:
            game.extend(bytearray(4-len(b_offset_sprites)%4))
        game.extend(b_offset_sprites)

        if len(b_offset_sound)%4:
            game.extend(bytearray(4-len(b_offset_sound)%4))
        game.extend(b_offset_sound)

        if len(b_offset_save)%4:
            game.extend(bytearray(4-len(b_offset_save)%4))
        game.extend(b_offset_save)



        if len(icon)%4:
            game.extend(bytearray(4-len(icon)%4))
        game.extend(icon)

        if len(game)%4:
            game.extend(bytearray(4-len(game_data)%4))
        game.extend(game_data)

        if len(imgs)%4:
            game.extend(bytearray(4-len(imgs)%4))
        game.extend(imgs)

        if len(sounds)%4:
            game.extend(bytearray(4-len(sounds)%4))
        game.extend(sounds)

        return game

    def get_title(strin: str) -> bytearray:
        for index, line in enumerate(strin.split("\n")):
            if ".name" in line:
                start = line.find("'")
                stop = line[start+1:].find("'")+start
                title = bytearray(line[start+1:stop+1], "ascii")
                if len(title)<64:
                    title.extend(bytearray(64-len(title)))

                return title[:64]

    def get_icon(strin: str) -> bytearray:
        icon = bytearray()
        for index, line in enumerate(strin.split("\n")):
            if ".icon" in line:
                string = line[5:].replace("=", "")
                string = string.replace(" ", "")
                string = string.replace('"', "")
                icon_img = Image.open(string)
                icon.extend(Img_converter.convert_icon(icon_img))
                return icon

        return bytearray(64*64*2)

    def get_images(strin: str, offset_sprites: int) -> bytearray:
        imgs = bytearray()
        t_imgs = bytearray()
        t_offsets = []
        n_imgs = 0

        img_width = 0
        img_height = 0

        img_loc = -1
        start = -1
        stop = -1

        for index, line in enumerate(strin.split("\n")):
            if ".img" in line:
                img_loc = index
                break;

        if img_loc >= 0:
            for index, line in enumerate(strin.split("\n")[index:]):
                if "{" in line:
                    start = index + img_loc
                if "}" in line:
                    stop = index + img_loc
                    break

        if start >= 0 and stop >= 0 and start < stop:
            for index, line in enumerate(strin.split("\n")[start+1:stop]):
                img_line = line.replace(" ", "")
                img_line = img_line.replace('"', "")
                if img_line and img_line[0].isalpha():
                    f_img = Image.open(img_line)

                    img_width, img_height = f_img.size

                    img_RGBA8888 = Img_converter.convert_img_to_RGBA8888(f_img)
                    img_arr = Img_converter.convert_type(img_RGBA8888)
                    t_imgs.extend(img_width.to_bytes(4, 'little'))
                    t_imgs.extend(img_height.to_bytes(4, 'little'))
                    t_imgs.extend(img_arr)

                    try:
                        t_offsets.append(t_offsets[-1]+(len(img_arr)+3)//4)
                    except IndexError:
                        t_offsets.append(offset_sprites)

                    n_imgs += 1

        imgs.extend(n_imgs.to_bytes(4, 'little'))
        for offset in t_offsets:
            imgs.extend(t_offsets.to_bytes(4, 'little'))
        imgs.extend(t_imgs)
        return imgs


    def get_sounds(strin: str, offset_sound: int) -> bytearray:
        sounds = bytearray()
        t_sounds = bytearray()
        t_offsets = []
        n_sounds = 0

        sound_loc = -1
        start = -1
        stop = -1

        for index, line in enumerate(strin.split("\n")):
            if ".sound" in line:
                sound_loc = index
                break;

        if sound_loc >= 0:
            for index, line in enumerate(strin.split("\n")[index:]):
                if "{" in line:
                    start = index + sound_loc
                if "}" in line:
                    stop = index + sound_loc
                    break

        if start >= 0 and stop >= 0 and start < stop:
            for index, line in enumerate(strin.split("\n")[start+1:stop]):
                sound_line = line.replace(" ", "")
                sound_line = img_line.replace('"', "")
                if sound_line and sound_line[0].isalpha():
                    f_sound = open(sound_line, "rb")
                    sound_arr = f_sound.read()
                    t_sounds.extend(len(sound_arr).to_bytes(4, 'little'))
                    t_sounds.extend(sound_arr)

                    try:
                        t_offsets.append(t_offsets[-1]+(len(sound_arr)+3)//4)
                    except IndexError:
                        t_offsets.append(offset_sound)

                    n_sounds += 1
                    f_sound.close()


        sounds.extend(n_sounds.to_bytes(4, 'little'))
        for offset in t_offsets:
            sounds.extend(offset.to_bytes(4, 'little'))
        sounds.extend(t_sounds)

        return sounds


    def get_game(strin: str) -> bytearray:
        game = bytearray()

        for index, line in enumerate(strin.split("\n")):
            if line[:2] == "0x":
                dword = int(line[2:], 16)
                game.extend(dword.to_bytes(4, "little"))

        return game
