#ifndef _LCD_H_
#define _LCD_H_

#include "main.h"
#include "stm32746g_discovery.h"
#include "stm32746g_discovery_lcd.h"
#include "stm32746g_discovery_sdram.h"
#include "stm32746g_discovery_ts.h"
#include "stm32f7xx_hal.h"

void 	LCD_Draw_Init();

void 	LCD_Clear();
error_t LCD_Set_BG_Color(uint32_t);
error_t LCD_Draw_String	(char *,   uint32_t, uint32_t, uint32_t, uint32_t);
error_t LCD_Draw_Number	(uint32_t, uint32_t, uint32_t, uint32_t);
error_t LCD_Draw_Line  	(uint32_t, uint32_t, uint32_t, uint32_t, uint32_t);
error_t LCD_Draw_Rect  	(uint32_t, uint32_t, uint32_t, uint32_t, uint32_t);
error_t LCD_Draw_Circle	(uint32_t, uint32_t, uint32_t, uint32_t);
error_t LCD_Draw_Image	(uint32_t, uint32_t, uint32_t, uint32_t, uint16_t *);
#endif
