#include "memmanager.h"
#include "interpreter.h"

#include "stm32746g_discovery.h"
#include "stm32746g_discovery_lcd.h"
#include "stm32746g_discovery_sdram.h"
#include "stm32746g_discovery_ts.h"
#include "stm32f7xx_hal.h"


void init_memmanager(void) {
	g_games_list = (s_game_list*)calloc(64, sizeof(s_game_list));
}


void flash_write(uint32_t address, const uint8_t * data, uint32_t size) {
	HAL_FLASH_Unlock();
	BSP_QSPI_Write(data, address, size);
	HAL_FLASH_Lock();
}

void flash_write32(uint32_t address, const uint32_t * data, uint32_t size) {
}

uint8_t game_list_len(void) {
	uint8_t n_game;
	for(n_game = 0; *g_games_list[n_game].title; n_game++);
	return n_game;
}

void load_game_list(s_game_list * game_list) {
	for(uint8_t n_game = 0; *(uint8_t*)(SECTOR_LIST + n_game*sizeof(s_game_list)) /* && *(uint8_t*)(SECTOR_LIST + n_game*sizeof(s_game_list)) < 128 */; n_game++) {
		strncpy(game_list[n_game].title, (char*)(SECTOR_LIST + n_game*sizeof(s_game_list)), 64);
		game_list[n_game].p_icon = (uint16_t*)(SECTOR_LIST + n_game*sizeof(s_game_list) + 64);
		game_list[n_game].p_game = (s_game*  )(uint32_t)(SECTOR_LIST + n_game*sizeof(s_game_list) + 68);
		game_list[n_game].len 	 = (uint32_t )(SECTOR_LIST + n_game*sizeof(s_game_list) + 72);
	}
}


void erase_game_list(void) {
	uint8_t tmp0s[SECTOR_LIST_SIZE];
	memset(tmp0s, 0, SECTOR_LIST_SIZE);
	BSP_QSPI_Write(tmp0s, SECTOR_LIST, SECTOR_LIST_SIZE);
}

void flash_erase(void) {
	BSP_QSPI_Erase_Chip();
}

void load_game(const s_game_list * game_list, uint8_t game_index) {
	printf("Game loaded: %s\r\n", game_list[game_index].title);
	interpreter_running = 1;
	g_active_game = game_list[game_index].p_game;
}
