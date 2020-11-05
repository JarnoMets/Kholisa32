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
	for(n_game = 0; *(uint8_t*)(FLASH_SECTOR_1 + n_game*LIST_GAME_SIZE) && *(uint8_t*)(FLASH_SECTOR_1 + n_game*LIST_GAME_SIZE) < 128; n_game++);
	return n_game;
}

void load_game_list(s_game_list * game_list) {
	uint8_t n_game;
	for(n_game = 0; *(uint8_t*)(FLASH_SECTOR_1 + n_game*LIST_GAME_SIZE) && *(uint8_t*)(FLASH_SECTOR_1 + n_game*LIST_GAME_SIZE) < 128; n_game++) {
		strncpy(game_list[n_game].title, (char*)(FLASH_SECTOR_1 + n_game*LIST_GAME_SIZE), 64);
		game_list[n_game].p_game = (s_game*)(FLASH_SECTOR_1 + n_game*LIST_GAME_SIZE + 16);
		game_list[n_game].icon = (s_game*)(FLASH_SECTOR_1 + n_game*LIST_GAME_SIZE + 17);
	}
}



void add_game_to_flash(s_game game) {
	uint8_t game_pos = game_list_len();
	flash_write(FLASH_SECTOR_1 + game_pos*LIST_GAME_SIZE, game.title, 64);
	uint32_t p_game = (uint32_t)&game;
	uint8_t p_game_8t[4];
	p_game_8t[0] = p_game&0xFF;
	p_game_8t[1] = (p_game<<8)&0xFF;
	p_game_8t[2] = (p_game<<16)&0xFF;
	p_game_8t[3] = (p_game<<24)&0xFF;

	flash_write(FLASH_SECTOR_1 + game_pos*LIST_GAME_SIZE+16, p_game_8t, 4);

	uint32_t p_icon = (uint32_t)game.icon;
	uint8_t p_icon_8t[4];
	p_icon_8t[0] = p_icon&0xFF;
	p_icon_8t[1] = (p_icon<<8)&0xFF;
	p_icon_8t[2] = (p_icon<<16)&0xFF;
	p_icon_8t[3] = (p_icon<<24)&0xFF;

	flash_write(FLASH_SECTOR_1 + game_pos*LIST_GAME_SIZE+17, p_icon_8t, 4);
}

void erase_game_list(void) {
	HAL_FLASH_Unlock();
	flash_write(FLASH_SECTOR_1, NULL, FLASH_SECTOR_2-FLASH_SECTOR_1);
	HAL_FLASH_Lock();
}
