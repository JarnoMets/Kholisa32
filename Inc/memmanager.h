#ifndef MEMMANAGER_H_
#define MEMMANAGER_H_

#include "stdint.h"

#define LIST_GAME_SIZE 18

typedef struct game {
		char 		title[64];
		uint32_t 	game_len;
		uint8_t * 	icon;
		uint8_t * 	p_data;
		uint8_t * 	p_sprites;
		uint8_t * 	p_sound;
		uint32_t 	save_len;
		uint32_t 	save_len_max;
		uint8_t * 	p_save;
} s_game;

typedef struct game_list {
		char 		title[64];
		s_game * 	p_game;
		uint8_t * 	icon;
} s_game_list;

s_game_list * g_games_list;
s_game g_active_game;

void flash_write(uint32_t address, uint8_t * data, uint32_t size);

void init_memmanager(void);

void erase_game_list(void);

s_game * load_game(char * name);
void load_game_list(s_game_list * game_list);
void add_game_to_flash(s_game game);
#endif
