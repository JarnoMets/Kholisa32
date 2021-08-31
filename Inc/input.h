#ifndef _INPUT_H_
#define _INPUT_H_

#include "stm32746g_discovery.h"
#include "stm32746g_discovery_lcd.h"
#include "stm32746g_discovery_sdram.h"
#include "stm32746g_discovery_ts.h"

#include "lcd.h"
#include "memmanager.h"
#include "main.h"

#define BUTTON_LEFT	 	Rn[0]
#define BUTTON_UP 		Rn[1]
#define BUTTON_RIGHT 	Rn[2]
#define BUTTON_DOWN	 	Rn[3]

#define BUTTON_A 		Rn[4]
#define BUTTON_B 		Rn[5]
#define BUTTON_X 		Rn[6]
#define BUTTON_Y 		Rn[7]

#define TOUCH_B			Rn[8]
#define TOUCH_X			Rn[9]
#define TOUCH_Y			Rn[10]

TS_StateTypeDef * TS_State_inputs;

void inputs_init();
void inputs_update();


#endif
