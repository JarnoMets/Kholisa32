#ifndef _MEMMANAGER_H_
#define _MEMMANAGER_H_

#include "main.h"
#include "stdint.h"


/* All in 32-bit */
#define GAME_ICON_SIZE				2048

#define SECTOR_GP			0x91000000
#define SECTOR_GP_SIZE  	256
#define SECTOR_LIST			SECTOR_GP+SECTOR_GP_SIZE
#define SECTOR_LIST_SIZE	8192
#define SECTOR_GAMES		SECTOR_LIST+SECTOR_LIST_SIZE
#define SECTOR_GAMES_SIZE	8388608 /* 32mb */


typedef struct {
	uint32_t width;
	uint32_t height;
	uint16_t img;
} s_img;

typedef struct {
	uint32_t amount;
	s_img * imgs;
} s_img_arr;


typedef struct {
	uint32_t size;
	uint16_t sound;
} s_sound;

typedef struct {
	uint32_t amount;
	s_sound * sounds;
} s_sound_arr;




typedef struct {
		char 				title[64];
		uint16_t *			p_icon; /* Icon is a 64x64 pixel ARGB1555 */
		uint32_t * 			p_data;
		s_img_arr * 		p_sprites;
		s_sound_arr * 		p_sounds;
		uint8_t * 			p_save;
} s_game;

typedef struct {
		char 		title[64];
		uint16_t * 	p_icon;
		s_game * 	p_game;
		uint32_t	len;
} s_game_list;

s_game_list * 	g_games_list;
s_game 		*	g_active_game;


uint8_t 	game_list_len(void);

void 		flash_write(uint32_t address, const uint8_t *, uint32_t);
void 		flash_write32(uint32_t address, const uint32_t *, uint32_t);
void		flash_erase(void);

void 		init_memmanager(void);

void 		erase_game_list(void);

void		load_game(const s_game_list * , uint8_t);
void 		load_game_list(s_game_list * );
void 		add_game_to_flash(s_game, uint32_t);


#endif
