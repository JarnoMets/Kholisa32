#include "memmanager.h"
#include "main.h"
#include <stdio.h>


void init_memmanager(void) {
	g_games_list = (s_game_list*)calloc(64, sizeof(s_game_list));
}


void flash_write(uint32_t address, uint8_t * data, uint32_t size) {
	HAL_FLASH_Unlock();

	for (uint32_t word_n = 0; word_n <= size/4; word_n++) {
		uint32_t word = 0;
		for (uint8_t n = 0; n < 4; n++)
			word += (uint32_t)*(data+word_n+n) << n*8;
		HAL_FLASH_Program(FLASH_TYPEPROGRAM_WORD,address+word_n,word);
	}
	HAL_FLASH_Lock();
}

uint8_t game_list_len(void) {
	uint8_t n_game;
	for(n_game = 0; *(uint8_t*)(FLASH_SECTOR_1 + n_game*sizeof(s_game_list)) && *(uint8_t*)(FLASH_SECTOR_1 + n_game*sizeof(s_game_list)) < 128; n_game++);
	return n_game;
}

void load_game_list(s_game_list * game_list) {
	uint8_t n_game;
	for(n_game = 0; *(uint8_t*)(FLASH_SECTOR_1 + n_game*sizeof(s_game_list)) && *(uint8_t*)(FLASH_SECTOR_1 + n_game*sizeof(s_game_list)) < 128; n_game++) {
		strncpy(game_list[n_game].title, (char*)(FLASH_SECTOR_1 + n_game*sizeof(s_game_list)), 64);
		game_list[n_game].p_icon = (s_game*)(FLASH_SECTOR_1 + n_game*sizeof(s_game_list) + 16);
		game_list[n_game].p_game = (s_game*)(FLASH_SECTOR_1 + n_game*sizeof(s_game_list) + 17);
		game_list[n_game].len = (s_game*)(FLASH_SECTOR_1 + n_game*sizeof(s_game_list) + 18);
	}
}



void add_game_to_flash(s_game game, uint32_t len) {
	uint8_t game_pos = game_list_len();
	flash_write(FLASH_SECTOR_1 + game_pos*sizeof(s_game_list), game.title, 64);


	uint32_t p_icon = (uint32_t)game.p_icon;
	uint8_t p_icon_8t[4];
	p_icon_8t[0] = p_icon&0xFF;
	p_icon_8t[1] = (p_icon<<8)&0xFF;
	p_icon_8t[2] = (p_icon<<16)&0xFF;
	p_icon_8t[3] = (p_icon<<24)&0xFF;
	flash_write(FLASH_SECTOR_1 + game_pos*sizeof(s_game_list)+17, p_icon_8t, 4);

	uint32_t p_game = (uint32_t)game.p_icon-64;
	uint8_t p_game_8t[4];
	p_game_8t[0] = p_game&0xFF;
	p_game_8t[1] = (p_game<<8)&0xFF;
	p_game_8t[2] = (p_game<<16)&0xFF;
	p_game_8t[3] = (p_game<<24)&0xFF;
	flash_write(FLASH_SECTOR_1 + game_pos*sizeof(s_game_list)+16, p_game_8t, 4);


	uint8_t len_8t[4];
	len_8t[0] = len&0xFF;
	len_8t[1] = (len<<8)&0xFF;
	len_8t[2] = (len<<16)&0xFF;
	len_8t[3] = (len<<24)&0xFF;
}

void erase_game_list(void) {
	HAL_FLASH_Unlock();
	flash_write(FLASH_SECTOR_1, NULL, FLASH_SECTOR_2-FLASH_SECTOR_1);
	HAL_FLASH_Lock();
}
