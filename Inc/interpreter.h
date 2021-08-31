#ifndef _INTERPRETER_H_
#define _INTERPRETER_H_

#include "main.h"
#include "stdint.h"
#include "lcd.h"
#include "main.h"
#include "memmanager.h"
#include <stdio.h>
#include <math.h>
#include <time.h>


#define STACK_SIZE 1024
#define error_t int

#define MASK_COMMAND 	0xFF000000


#define	NOP 			0x00000000
#define STOP 			0x00000000
#define CLEAR   		0x01000000
#define RET				0x02000000
#define SJMP 			0x03000000
#define JMP 			0x04000000
#define CALL 			0x05000000
#define JNEV			0x06000000
#define JNER 			0x07000000
#define JEV 			0x08000000
#define JER 			0x09000000
#define MOVV			0x0A000000
#define MOVR 			0x0B000000
#define RANDV			0x0C000000
#define RANDR 			0x0D000000
#define ADDV    		0x0E000000
#define ADDR 			0x0F000000
#define SUBV			0x10000000
#define SUBR 			0x11000000
#define MULV 			0x12000000
#define MULR 			0x13000000
#define DIVV 			0x14000000
#define DIVR 			0x15000000
#define MODV 			0x16000000
#define MODR 			0x17000000
#define LS 				0x18000000
#define RS 				0x19000000
#define LR 				0x1A000000
#define RR 				0x1B000000
#define INC 			0x1C000000
#define DEC 			0x1D000000
#define DJNZ 			0x1E000000
#define DJZ 			0x1F000000
#define PUSH    		0x20000000
#define POP				0x21000000
#define ANDV			0x22000000
#define ANDR			0x23000000
#define ORV				0x24000000
#define ORR				0x25000000
#define XORV			0x26000000
#define XORR			0x27000000
#define COMP			0x28000000

#define JLTV			0x30000000
#define JLTR			0x31000000
#define JLEV			0x32000000
#define JLER			0x33000000
#define JGTV			0x34000000
#define JGTR			0x35000000
#define JGEV			0x36000000
#define JGER			0x37000000


#define DISP 			0xA0000000
#define PLAY 			0xA1000000
#define DEBUGR 			0xA2000000
#define DEBUGM 			0xA3000000
#define DISPBGCOLOR 	0xA4000000
#define DISPSTRING		0xA5000000
#define DISPNUMBER		0xA6000000

#define DRAWLINE 		0xB0000000
#define DRAWRECT 		0xB1000000
#define DRAWCIRCLE 		0xB2000000

uint32_t Rn[256];	/* Registers 		*/

uint8_t interpreter_running;



error_t interpreter_init();

error_t interpreter_update();

error_t interpreter_exit(uint8_t code);




#endif
