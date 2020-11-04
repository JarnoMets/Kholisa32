#ifndef MEMMANAGER_H_
#define MEMMANAGER_H_

#include "stdint.h"

typedef struct game {
		uint32_t len;
		char title[64];
		uint8_t * p_data;
		uint8_t * p_sprites;
		uint8_t * p_sound;
} s_game;

typedef struct game_list {
		char title[64];
		s_game * p_game;
} s_game_list;

s_game_list games_list;

#endif
