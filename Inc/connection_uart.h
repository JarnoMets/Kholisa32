#ifndef RECEIVEGAME_H_
#define RECEIVEGAME_H_

static int sg_connection;

#include "main.h"

void await_start(void);

void stripcrnl(char *);

void start_connection(void);
void stop_connection(void);

void debug(void);
void receive_game(void);


#endif
