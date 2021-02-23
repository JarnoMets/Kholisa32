#include <connection_uart.h>
#include "memmanager.h"

extern UART_HandleTypeDef huart1;

void await_start() {
	char p_buf[18];
	do {
		HAL_UART_Receive(&huart1, p_buf, sizeof("Start connection\r\n"), 1000);
	} while(!strcmp(*p_buf, "Start connection\r\n"));
	start_connection();
}

void start_connection() {
	HAL_UART_Transmit(&huart1, "Connection started\r\n", sizeof("Connection started\r\n"), 1000);
	sg_connection = 1;

	char * action = (char *)calloc(64, sizeof(char));

	HAL_UART_Transmit(&huart1, "Action?\r\n", sizeof("Action?\r\n"), 1000);
	HAL_UART_Receive(&huart1, action, 64, 1000);

	if (!strncmp(action, "close")) {
		stop_connection();
	} else
	if (!strncmp(action, "debug")) {
		debug();
	} else
	if (!strncmp(action, "send")) {
		receive_game();
	}
}

void stop_connection() {
	HAL_UART_Transmit(&huart1, "Connection closed\r\n", sizeof("Connection closed\r\n"), 1000);
	sg_connection = 0;
}


void debug() {
	uint8_t modeDebug = 1;
	char * input = (char*)calloc(256, sizeof(char));
	char ** command = (char**)calloc(4, sizeof(char*));
	for (uint8_t i = 0; i < 4; i++)
		command[i] = (char*)calloc(64, sizeof(char*));

	char token = ' ';
	int * words_pos = (int *)calloc(4, sizeof(int));

	HAL_UART_Transmit(&huart1, "Debug mode started\r\n", sizeof("Debug mode started\r\n"), 1000);
	HAL_UART_Transmit(&huart1, "Enter q or exit to quit\r\n", sizeof("Enter q or exit to quit\r\n"), 1000);
	while (modeDebug) {
		HAL_UART_Transmit(&huart1, ">", sizeof(">"), 1000);
		HAL_UART_Receive(&huart1, input, 128, 1000);

			;


	}
	free(input);
	free(command);
	free(words_pos);
}


void receive_game() {
	s_game tmp_game;
	uint32_t p_gameBase;

	if (game_list_len())
		p_gameBase = g_games_list[game_list_len()-1].p_game + g_games_list[game_list_len()-1].len;
	else
		p_gameBase = FLASH_SECTOR_2;


	/* Title receive start */
	HAL_UART_Transmit(&huart1, "Title\r\n", sizeof("Title\r\n"), 1000); 							/* Ask for title 															*/
	char str_title_len[2];																			/* Reserve place for length of title 										*/
	HAL_UART_Receive(&huart1, str_title_len, 2, 1000); 												/* Receive title length														*/
	HAL_UART_Transmit(&huart1, "\x06\r\n", sizeof("\x06\r\n"), 1000); 								/* ACK 																		*/
	HAL_UART_Receive(&huart1, tmp_game.title, atoi(str_title_len), 1000); 							/* Receive title 															*/
	HAL_UART_Transmit(&huart1, "\x06\r\n", sizeof("\x06\r\n"), 1000); 								/* ACK 																		*/
	/* Title receive stop */



	/* Icon receive start */
	HAL_UART_Transmit(&huart1, "Icon\r\n", sizeof("Icon\r\n"), 1000); 								/* Ask for icon 															*/
	uint8_t * tmp_icon = (uint8_t *)calloc(64*64*2, sizeof(uint8_t)); 								/* Make temporary place for the icon 										*/
	HAL_UART_Receive(&huart1, tmp_icon, 2, 1000); 													/* Receive icon 															*/
	tmp_game.p_icon = p_gameBase + sizeof(s_game); 													/* Calc position of the icon in flash 										*/
	flash_write(tmp_game.p_icon, tmp_icon, 64*64*2); 												/* Write the icon received to flash											*/
	free(tmp_icon); 																				/* Free up the temporary icon 												*/
	HAL_UART_Transmit(&huart1, "\x06\r\n", sizeof("\x06\r\n"), 1000); 								/* ACK 																		*/
	/* Icon receive stop */



	/* Game data receive start */
	HAL_UART_Transmit(&huart1, "Game data\r\n", sizeof("Game data\r\n"), 1000); 					/* Ask for game data 														*/
	char str_game_len[32];																			/* Reserve place for length of game 										*/
	HAL_UART_Receive(&huart1, str_game_len, 32, 1000);												/* Receive length of game 													*/
	HAL_UART_Transmit(&huart1, "\x06\r\n", sizeof("\x06\r\n"), 1000); 								/* ACK 																		*/
	tmp_game.game_data_len = atoi(str_game_len);													/* Convert game length into uint32 											*/
	uint8_t * tmp_game_data = (uint8_t *)calloc(tmp_game.game_data_len, sizeof(uint8_t));			/* Make temporary place for game data 										*/
	HAL_UART_Receive(&huart1, tmp_game_data, tmp_game.game_data_len, 1000);							/* Receive game data														*/
	tmp_game.p_data = tmp_game.p_icon + 64*64/2;													/* Calc position for game data in flash 									*/
	flash_write(tmp_game.p_data, tmp_game_data, tmp_game.game_data_len);													/* Write the game data received to flash									*/
	free(tmp_game_data);																			/* Free up the temporary game data 											*/
	HAL_UART_Transmit(&huart1, "\x06\r\n", sizeof("\x06\r\n"), 1000); 								/* ACK 																		*/
	/*Game data receive stop */



	/* Sprites receive start */
	HAL_UART_Transmit(&huart1, "Sprites\r\n", sizeof("Sprites\r\n"), 1000); 						/* Ask for sprites															*/
	char str_sprites_len[32];																		/* Reserve place for length of sprites										*/
	HAL_UART_Receive(&huart1, str_sprites_len, 32, 1000);											/* Receive length of sprites												*/
	HAL_UART_Transmit(&huart1, "\x06\r\n", sizeof("\x06\r\n"), 1000); 								/* ACK 																		*/
	tmp_game.game_sprites_len = atoi(str_sprites_len);												/* Convert sprites length in uint32 										*/
	uint8_t * tmp_sprites = (uint8_t *)calloc(tmp_game.game_sprites_len, sizeof(uint8_t));			/* Make temporary place for sprites											*/
	HAL_UART_Receive(&huart1, tmp_sprites, tmp_game.game_sprites_len, 1000);						/* Receive sprites															*/
	tmp_game.p_sprites = tmp_game.p_data + tmp_game.game_data_len;									/* Calc position for sprites flash 											*/
	flash_write(tmp_game.p_sprites, tmp_sprites, tmp_game.game_data_len);													/* Write the sprites received to flash										*/
	free(tmp_sprites);																				/* Free up the temporary sprites 											*/
	HAL_UART_Transmit(&huart1, "\x06\r\n", sizeof("\x06\r\n"), 1000); 								/* ACK																		*/
	/* Sprites receive stop */

	/* Sound receive start */
	HAL_UART_Transmit(&huart1, "Sound\r\n", sizeof("Sound\r\n"), 1000); 							/* Ask for sound															*/
	char str_sound_len[32];																			/* Reserve place for length of sound										*/
	HAL_UART_Receive(&huart1, str_sound_len, 32, 1000);												/* Receive length of sound 													*/
	HAL_UART_Transmit(&huart1, "\x06\r\n", sizeof("\x06\r\n"), 1000); 								/* ACK 																		*/
	tmp_game.game_sound_len = atoi(str_sound_len);													/* Convert sound length into uint32 										*/
	uint8_t * tmp_sound = (uint8_t *)calloc(tmp_game.game_sound_len, sizeof(uint8_t));				/* Make temporary place for sound											*/
	HAL_UART_Receive(&huart1, tmp_sound, tmp_game.game_sound_len, 1000);							/* Receive sound															*/
	tmp_game.p_sound = tmp_game.p_sprites + tmp_game.game_sprites_len;								/* Calc position for sound in flash	 										*/
	flash_write(tmp_game.p_sound, tmp_sound, tmp_game.game_sound_len);								/* Write the sound received to flash										*/
	free(tmp_sound);																				/* Free up the temporary sound 												*/
	HAL_UART_Transmit(&huart1, "\x06\r\n", sizeof("\x06\r\n"), 1000); 								/* ACK																		*/
	/* Sound receive stop */



	/* Save information start */
	tmp_game.p_save = tmp_game.p_sound + tmp_game.game_sound_len;									/* Calc position for save in flash											*/
	tmp_game.save_len = 0;																			/* New game received doesn't have any saved data, so length of save = 0		*/
	HAL_UART_Transmit(&huart1, "Save max\r\n", sizeof("Sound\r\n"), 1000);							/* Ask for maximum save length												*/
	char str_save_len[32];																			/* Reserve place for string about maximum save length 						*/
	HAL_UART_Receive(&huart1, str_save_len, 32, 1000);												/* Receive maximum save length												*/
	HAL_UART_Transmit(&huart1, "\x06\r\n", sizeof("\x06\r\n"), 1000);								/* ACK																		*/
	tmp_game.save_len_max = atoi(str_save_len);														/* Convert maximum save length into int32									*/
	/* Save information stop */

	uint32_t tmp_game_len = tmp_game.p_save + tmp_game.save_len_max - (uint8_t *)tmp_game.title;				/* Calculate the length of the total game									*/

	add_game_to_flash(tmp_game, tmp_game_len);														/* Add the game struct to flash and add the game to the game list in flash	*/

	stop_connection();
}

void stripcrnl(char * string) {
	for (uint8_t n = 0; string[n]; n++)
		if ('\n' == string[n] || '\r' == string[n])
			string[n] = NULL;
}

