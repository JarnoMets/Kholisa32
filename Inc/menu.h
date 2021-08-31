#ifndef _MENU_H_
#define _MENU_H_

#include "stm32746g_discovery.h"
#include "stm32746g_discovery_lcd.h"
#include "stm32746g_discovery_sdram.h"
#include "stm32746g_discovery_ts.h"

#include "lcd.h"
#include "memmanager.h"
#include "main.h"

void load_menu();
void menu_update();

#endif
