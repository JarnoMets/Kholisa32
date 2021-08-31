#include "lcd.h"

void LCD_Draw_Init()
{
	/* Init BSP LCD driver */
	BSP_LCD_Init();
	/* Set buffer address */
	BSP_LCD_LayerDefaultInit(1, LCD_FB_START_ADDRESS);
	BSP_LCD_LayerDefaultInit(0, LCD_FB_START_ADDRESS+(480*272*4));
	/* Enable the LCD */
	BSP_LCD_DisplayOn();
	/* Select the LCD Background Layer  */
	BSP_LCD_SelectLayer(0);
	/* Clear the Background Layer */
	BSP_LCD_Clear(LCD_COLOR_WHITE);
	BSP_LCD_SelectLayer(1);
	/* Clear the foreground Layer(with transparency) */
	BSP_LCD_Clear(0);
}

void LCD_Clear() {
	BSP_LCD_Clear(LCD_COLOR_WHITE);
}


error_t LCD_Set_BG_Color(uint32_t color) {
	BSP_LCD_SetBackColor(color);

	return 0;
}


error_t LCD_Draw_String(char * string, uint32_t x,uint32_t y, uint32_t color, uint32_t len) {
	char * tmpStr = calloc(len+1, sizeof(char));
	strncpy(tmpStr, string, len);
	strcat(tmpStr, "\0");
	BSP_LCD_SetTextColor(color);
	BSP_LCD_DisplayStringAt(x, y, tmpStr, LEFT_MODE);

	return 0;
}

error_t LCD_Draw_Number(uint32_t num, uint32_t x,uint32_t y, uint32_t color) {
	BSP_LCD_SetTextColor(color);
	char tmpStr[32];
	snprintf(tmpStr, 32, "%d", num);
	BSP_LCD_DisplayStringAt(x, y, tmpStr, LEFT_MODE);

	return 0;
}

error_t LCD_Draw_Line(uint32_t x1, uint32_t y1, uint32_t x2, uint32_t y2, uint32_t color) {
	BSP_LCD_SetTextColor(color);
	BSP_LCD_DrawLine(x1, y1, x2, y2);

	return 0;
}

error_t LCD_Draw_Rect(uint32_t x1, uint32_t y1, uint32_t w, uint32_t h, uint32_t color) {
	BSP_LCD_SetTextColor(color);
	BSP_LCD_FillRect(x1, y1, w, h);

	return 0;
}

error_t LCD_Draw_Circle(uint32_t x, uint32_t y, uint32_t r, uint32_t color) {
	BSP_LCD_SetTextColor(color);
	BSP_LCD_FillCircle(x, y, r);

	return 0;
}

error_t LCD_Draw_Image(uint32_t x, uint32_t y, uint32_t width, uint32_t height, uint16_t * img) {
	WDA_LCD_DrawBitmap(img, x, y, width, height, 0x00000003U /* ARGB1555*/);

	return 0;
}

