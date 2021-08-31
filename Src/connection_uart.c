#include "connection_uart.h"

#include "stm32746g_discovery.h"
#include "stm32746g_discovery_lcd.h"
#include "stm32746g_discovery_sdram.h"
#include "stm32746g_discovery_ts.h"
#include "stm32f7xx_hal.h"

extern UART_HandleTypeDef huart1;

static const uint8_t OPEN = 0x02;
static const uint8_t CLOSE = 0x04;
static const uint8_t ACK = 0x06;
static const uint8_t ERR = 0x15;
static const uint8_t DEBUG = 0x30;
static const uint8_t RECV_GAME = 0x31;


static const int MAX_PACKET_SIZE = 7200;

void await_start() {
	BSP_LCD_SetTextColor(LCD_COLOR_BLACK);
	uint8_t buf = 0;
	do {
		HAL_UART_Receive(&huart1, &buf, 1, 1000);
	} while(buf != OPEN);
	start_connection();
}

void start_connection() {
	HAL_UART_Transmit(&huart1, (uint8_t *)&OPEN, 1, 1000);
	g_connection = 1;

	uint8_t action = 0;

	do {
		HAL_UART_Receive(&huart1, &action, 1, 1000);
	} while(!action);
	HAL_UART_Transmit(&huart1, (uint8_t *)&ACK, 1, 1000);

	if (action == CLOSE) {
		stop_connection();
	} else
	if (action == DEBUG) {
		debug();
	} else
	if (action == RECV_GAME) {
		receive_game();
	}
}

void stop_connection() {
	HAL_UART_Transmit(&huart1, (uint8_t *)&CLOSE, 1, 1000);
	HAL_UART_Abort(&huart1);
	g_connection = 0;
}


void debug() {
	uint8_t modeDebug = 1;
	char * input = (char*)calloc(256, sizeof(char));
	char ** command = (char**)calloc(4, sizeof(char*));
	for (uint8_t i = 0; i < 4; i++)
		command[i] = (char*)calloc(64, sizeof(char*));

	int * words_pos = (int *)calloc(4, sizeof(int));

	HAL_UART_Transmit(&huart1, (uint8_t *)"Debug mode started\r\n", sizeof("Debug mode started\r\n"), 1000);
	HAL_UART_Transmit(&huart1, (uint8_t *)"Enter q or exit to quit\r\n", sizeof("Enter q or exit to quit\r\n"), 1000);
	while (modeDebug) {
		HAL_UART_Transmit(&huart1, (uint8_t *)">", sizeof(">"), 1000);
		HAL_UART_Receive(&huart1, (uint8_t *)input, 128, 1000);


	}
	free(input);
	free(command);
	free(words_pos);
}


void receive_game() {
	s_game header;
	uint32_t buffer[MAX_PACKET_SIZE];
	uint32_t n_packets 	= 0;
	uint32_t len 		= 0;
	uint32_t p_currentWriteLoc;

	uint8_t n_games = game_list_len();
	load_game_list(g_games_list);

	/* Calculate position to save game */
	if (n_games)
		p_currentWriteLoc = (uint32_t)((uint32_t)g_games_list[n_games-1].p_game + g_games_list[n_games-1].len);
	else
		p_currentWriteLoc = (uint32_t)SECTOR_GAMES;

	/* Receive total game length */
	HAL_UART_Transmit(&huart1, (uint8_t *)&ACK, 1, 1000);
	HAL_UART_Receive(&huart1, (uint8_t *)&len, sizeof(uint32_t), 1000);
	if (len) {
		HAL_UART_Transmit(&huart1, (uint8_t *)&ACK, 1, 1000);
	} else {
		HAL_UART_Transmit(&huart1, (uint8_t *)&ERR, 1, 1000);
	}

	/* Receive amount of packets */
	HAL_UART_Receive(&huart1, (uint8_t *)&n_packets, sizeof(uint32_t), 1000);

	if (n_packets) {
		HAL_UART_Transmit(&huart1, (uint8_t *)&ACK, 1, 1000);
	} else {
		HAL_UART_Transmit(&huart1, (uint8_t *)&ERR, 1, 1000);
	}



	/* Receive header */
	HAL_UART_Receive(&huart1, (uint8_t *)&header, sizeof(s_game), 1000);

	if (*header.title) {
		n_packets--;
		/* Save header to flash */
		uint32_t tmp_p_icon 	= (uint32_t)header.p_icon		+ p_currentWriteLoc;
		uint32_t tmp_p_data		= (uint32_t)header.p_data 		+ p_currentWriteLoc;
		uint32_t tmp_p_sprites	= (uint32_t)header.p_sprites 	+ p_currentWriteLoc;
		uint32_t tmp_p_sounds	= (uint32_t)header.p_sounds  	+ p_currentWriteLoc;
		uint32_t tmp_p_save		= (uint32_t)header.p_save 		+ p_currentWriteLoc;

		uint8_t tmpBufHeader[20];

		for (uint8_t i = 0; i < 4; i++)
			tmpBufHeader[i]		= (uint8_t)((tmp_p_icon>>i*8)&(0xff));

		for (uint8_t i = 0; i < 4; i++)
			tmpBufHeader[i+4]	= (uint8_t)((tmp_p_data>>i*8)&(0xff));

		for (uint8_t i = 0; i < 4; i++)
			tmpBufHeader[i+8]	= (uint8_t)((tmp_p_sprites>>i*8)&(0xff));

		for (uint8_t i = 0; i < 4; i++)
			tmpBufHeader[i+12]	= (uint8_t)((tmp_p_sounds>>i*8)&(0xff));

		for (uint8_t i = 0; i < 4; i++)
			tmpBufHeader[i+16]	= (uint8_t)((tmp_p_save>>i*8)&(0xff));

		flash_write(p_currentWriteLoc, (uint8_t*)header.title, 64);
		flash_write(p_currentWriteLoc+64, tmpBufHeader, 20);

		HAL_UART_Transmit(&huart1, (uint8_t *)&ACK, 1, 1000);
	} else {
		HAL_UART_Transmit(&huart1, (uint8_t *)&ERR , 1, 1000);
	}

	/* Add to games list */
	uint32_t list_loc = SECTOR_LIST+n_games*sizeof(s_game_list);


	flash_write(list_loc, (uint8_t *)header.title, sizeof(header.title));
	list_loc += sizeof(header.title);


	uint8_t tmpBuf[12];

	for (uint8_t i = 0; i < 4; i++)
		tmpBuf[i] = (uint8_t)(((uint32_t)header.p_icon>>i*8)&(0xff));

	for (uint8_t i = 0; i < 4; i++)
		tmpBuf[i+4] = (uint8_t)((p_currentWriteLoc>>i*8)&(0xff));

	for (uint8_t i = 0; i < 4; i++)
		tmpBuf[i+8] = (uint8_t)((len>>i*8)&(0xff));

	flash_write(list_loc, tmpBuf, 12);
	p_currentWriteLoc += sizeof(header);


	/* Receive data */
	while(n_packets--) {
		uint32_t packet_size;
		/* Receive packet length */
		HAL_UART_Receive(&huart1, (uint8_t *)&packet_size, sizeof(uint32_t), 1000);

		if (packet_size && packet_size <= MAX_PACKET_SIZE)  {
			/* Receive packet */
			HAL_UART_Transmit(&huart1, (uint8_t *)&ACK, 1, 1000);
			if (HAL_UART_Receive(&huart1, (uint8_t *)buffer, packet_size, 1000) == 0) {
				/* Write packet to flash */
				flash_write(p_currentWriteLoc, (uint8_t *)buffer, packet_size);
				p_currentWriteLoc += packet_size;
				HAL_UART_Transmit(&huart1, (uint8_t *)&ACK, 1, 1000);
			} else {
				HAL_UART_Transmit(&huart1, (uint8_t *)&ERR, 1, 1000);
			}
		} else {
			HAL_UART_Transmit(&huart1, (uint8_t *)&ERR, 1, 1000);
		}
	}
	stop_connection();
	load_game_list(g_games_list);
}

void stripcrnl(char * string) {
	for (uint8_t n = 0; string[n]; n++)
		if ('\n' == string[n] || '\r' == string[n])
			string[n] = '\0';
}

