#ifndef _CONNECTION_UART_H_
#define _CONNECTION_UART_H_

#include "main.h"
#include "memmanager.h"

void await_start(void);

void stripcrnl(char *);

void start_connection(void);
void stop_connection(void);

void debug(void);
void receive_game(void);

uint8_t g_connection;

#endif
