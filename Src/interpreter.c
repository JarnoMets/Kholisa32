#include "interpreter.h"
#include "main.h"
#include "memmanager.h"
#include <stdio.h>


error_t interpreter_init() {
	DP = 0;
	SP = 0;

	Rn[5] = 0xAB;

	interpreter_running = 1;

	printf("Running %s\r\n", g_active_game.title);

	return 0;
}


error_t interpreter_update() {

	if (!interpreter_running)
		return 1;

	uint32_t data_reg = *((uint32_t*)(g_active_game.p_data + DP));

	/*
	printf("DP: %d\r\n", DP);
	printf("DATA: %x\r\n", (uint)data_reg);
	*/

	if ((data_reg&MASK_COMMAND) == (STOP&MASK_COMMAND) && ((data_reg&0x00FF0000) > 0)) /* STOP 0x00nnuuuu */
		interpreter_exit((data_reg&0x00FF0000) >> 16);




	/*
	 TBI
	 */





	if ((data_reg&MASK_COMMAND) == DEBUGR) {
			printf("Value of R0x%x: 0x%x\r\n", (uint)(data_reg&0x00FF0000) >> 16, (uint)Rn[(data_reg&0x00FF0000) >> 16]);
			DP ++;
	}

	if ((data_reg&MASK_COMMAND) == (DEBUGM&MASK_COMMAND)) {
			printf("DEBUG: %.*s\r\n", (int)((data_reg&0x00FF0000) >> 16), (char*)(g_active_game.p_data + DP + 1));
			DP += ceil((double)((data_reg&0x00FF0000) >> 16)/4) + 1;
	}

	return 0;
}


error_t interpreter_exit(uint8_t code) {

	printf("Exiting with code %d ... \r\n", code);

	interpreter_running = 0;


	return 0;
}


