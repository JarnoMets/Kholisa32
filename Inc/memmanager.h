#ifndef _MEMMANAGER_H_
#define _MEMMANAGER_H_

#include "stdint.h"


/* All in 32-bit */
#define GAME_ICON_SIZE				2048


typedef struct game {
		char 		title[64];
		uint8_t * 	p_icon;
		uint32_t 	game_data_len;
		uint32_t * 	p_data;
		uint32_t 	game_sprites_len;
		uint8_t * 	p_sprites;
		uint32_t 	game_sound_len;
		uint8_t * 	p_sound;
		uint32_t 	save_len;
		uint32_t 	save_len_max;
		uint8_t * 	p_save;
} s_game;

typedef struct game_list {
		char 		title[64];
		uint8_t * 	p_icon; /* Icon is a 64x64 pixel ARGB1555 */
		s_game * 	p_game;
		uint32_t 	len; /* Len of total data segment */
} s_game_list;

s_game_list * 	g_games_list;
s_game 			g_active_game;

void 		flash_write(uint32_t address, uint8_t * data, uint32_t size);

void 		init_memmanager(void);

void 		erase_game_list(void);

s_game * 	load_game(char * name);
void 		load_game_list(s_game_list * game_list);
void 		add_game_to_flash(s_game game, uint32_t len);


#endif
