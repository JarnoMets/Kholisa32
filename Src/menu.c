#include "menu.h"

static const int offset_x 	= 40;
static const int offset_y 	= 50;
static const int spacing_x	= 20;
static const int spacing_y	= 44;

static TS_StateTypeDef * TS_State;
static uint8_t menu_active = 0;

void load_menu() {
	/*
	 *	40x50px 64x50px 20x50px 64x50px 20x50px 64x50px 20x50px 64x50px 20x50px 64x50px 40x50px
	 *	40x64px 64x64px 20x64px 64x64px 20x64px 64x64px 20x64px 64x64px 20x64px 64x64px 40x64px
	 *	40x50px 64x44px 20x44px 64x44px 20x44px 64x44px 20x44px 64x44px 20x44px 64x44px 40x44px
	 *	40x64px 64x64px 20x64px 64x64px 20x64px 64x64px 20x64px 64x64px 20x64px 64x64px 40x64px
	 *	40x50px 64x50px 20x50px 64x50px 20x50px 64x50px 20x50px 64x50px 20x50px 64x50px 40x50px
	*/

	LCD_Clear();

	BSP_TS_Init(480,272);

	uint8_t len = game_list_len();
	if (len > 10)
		len = 10;

	/* Draws all the icons on the screen */
	for (uint8_t n = 0; n < len; n++) {
		//LCD_Draw_Image(offset_x+(n%5)*spacing_x, offset_y+(n/5)*spacing_y, 64, 64, g_games_list[n].p_icon);
		LCD_Draw_Rect(offset_x+(n%5)*(spacing_x+64), offset_y+(n/5)*(spacing_y+64), 50, 50, 0xFF00FFFF);
	}
	menu_active = 1;
}

void menu_update() {
	if (!menu_active)
		return;

	BSP_TS_GetState(TS_State);


	uint8_t len = game_list_len();
	if (TS_State->touchDetected)
		for (uint8_t n = 0; n < len; n++) {
			int icon_x_left   = offset_x+(n%5)*(spacing_x+64);
			int icon_x_right  = icon_x_left + 64;
			int icon_y_top    = offset_y+(n/5)*(spacing_y+64);
			int icon_y_bottom = icon_y_top + 64;
			if (*TS_State->touchX >= icon_x_left && *TS_State->touchX <= icon_x_right &&
				*TS_State->touchY >= icon_y_top  && *TS_State->touchY <= icon_y_bottom	)
			{
				load_game(g_games_list, n);
				menu_active = 0;
				BSP_TS_DeInit();
				LCD_Clear();
			}
		}

}
