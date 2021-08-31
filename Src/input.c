#include "input.h"
#include "interpreter.h"

void inputs_init() {
	BSP_TS_Init(480, 272);
	BSP_TS_GetState(TS_State_inputs);
}

void inputs_update() {

	static uint8_t input_cd = 0;
	//if (!(input_cd++))
		BSP_TS_GetState(TS_State_inputs);

	if (TS_State_inputs->touchDetected) {
		TOUCH_B = 1;
		TOUCH_X = *TS_State_inputs->touchX;
		TOUCH_Y = *TS_State_inputs->touchY;
	} else
		TOUCH_B = 0;
}


