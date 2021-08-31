#include "interpreter.h"
#include "input.h"

static uint32_t PC; 		/* Program counter 	*/
static uint32_t SP; 		/* Stack pointer 	*/
static uint32_t stack[STACK_SIZE];

error_t interpreter_init() {
	PC = 0;
	SP = 0;

	LCD_Draw_Init();
	inputs_init();

	interpreter_running = 0;

	time_t t;
	srand((unsigned) time(&t));

	return 0;
}


error_t interpreter_update() {
	HAL_Delay(1);
	if (!interpreter_running)
		return 1;

	inputs_update();

	uint32_t data_reg = *((uint32_t*)(g_active_game->p_data + PC));

	if ((data_reg&MASK_COMMAND) == (NOP&MASK_COMMAND) && ((data_reg&0x00FF0000) == 0))
		PC++;

	/* STOP: Stops the program with given stop code	*/
	else if ((data_reg&MASK_COMMAND) == (STOP&MASK_COMMAND) && ((data_reg&0x00FF0000) > 0))
		interpreter_exit((data_reg&0x00FF0000) >> 16);

	/* CLR:		*/
	else if ((data_reg&MASK_COMMAND) == (CLEAR&MASK_COMMAND)) {
		LCD_Clear();
		PC++;
	}

	/* RET: */
	else if ((data_reg&MASK_COMMAND) == (RET&MASK_COMMAND))
		PC = stack[--SP]+1;	/* Pulls Program Counter from the stack. Only use in combination with CALL */


	/* SJMP: Changes Program Counter to requested address. Can only handle 16.777.216 32-bit addresses. This should be enough, if not use "JMP". */
	else if ((data_reg&MASK_COMMAND) == (SJMP&MASK_COMMAND))
		PC = (data_reg&~MASK_COMMAND);		  	/* Loads the 24-bit number in the instruction to the Program Counter */


	/* JMP: Changes Program Counter to requested address anywhere in memory. Slightly less efficient than SJMP */
	else if ((data_reg&MASK_COMMAND) == (JMP&MASK_COMMAND))
		PC = *(g_active_game->p_data + PC + 1); 	/* Loads 32-bit number after the instruction to the Program Counter. */


	/* CALL: Changes Program Counter to requested address and also pushes the Program Counter to stack. Only use in combination with RET */
	else if ((data_reg&MASK_COMMAND) == (CALL&MASK_COMMAND)) {
		stack[SP++] = PC;							/* Pushes Program Counter to the Stack */
		PC = *(g_active_game->p_data + PC + 1); 	/* Loads 32-bit number after the instruction to the Program Counter. */
	}


	/* JNE:	Changes Program Counter to requested address if the value of a register isn't the same as the value given */
	else if ((data_reg&MASK_COMMAND) == (JNEV&MASK_COMMAND)) {
		if (Rn[(data_reg&0x00FF0000) >> 16] == *(g_active_game->p_data + PC + 1)) 	/* Compares register to value */
			PC++;
		else
			PC = *(g_active_game->p_data + PC + 2); 									/* Loads 32-bit number after the instruction to the Program Counter. */
	}


	/* JNE:	Changes Program Counter to requested address if the value of two registers isn't the same */
	else if ((data_reg&MASK_COMMAND) == (JNER&MASK_COMMAND)) {
		if (Rn[(data_reg&0x00FF0000) >> 16] == Rn[(data_reg&0x0000FF00) >> 8]) 	/* Compares register to register */
			PC++;
		else
			PC = *(g_active_game->p_data + PC + 1); 								/* Loads 32-bit number after the instruction to the Program Counter. */
	}


	/* JE:	Changes Program Counter to requested address if the value of a register is the same as the value given */
	else if ((data_reg&MASK_COMMAND) == (JEV&MASK_COMMAND)) {
		if (Rn[(data_reg&0x00FF0000) >> 16] == *(g_active_game->p_data + PC + 1)) 	/* Compares register to value */
			PC = *(g_active_game->p_data + PC + 2); 									/* Loads 32-bit number after the instruction to the Program Counter. */
		else
			PC++;
	}


	/* JE:	Changes Program Counter to requested address if the value of two registers is the same */
	else if ((data_reg&MASK_COMMAND) == (JER&MASK_COMMAND)) {
		if (Rn[(data_reg&0x00FF0000) >> 16] == Rn[(data_reg&0x0000FF00) >> 8]) 	/* Compares register to register */
			PC = *(g_active_game->p_data + PC + 1); 								/* Loads 32-bit number after the instruction to the Program Counter. */
		else
			PC++;
	}


	/* MOV: Copies a value to a register */
	else if ((data_reg&MASK_COMMAND) == (MOVV&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] = *(g_active_game->p_data + PC + 1); /* Copies value to register */
		PC += 2;
	}


	/* MOV: Copies the value of a register to another register */
	else if ((data_reg&MASK_COMMAND) == (MOVR&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] = Rn[(data_reg&0x0000FF00) >> 8]; 	/*  Copies value of a register to another register */
		PC++;
	}


	/* RAND: Generates a random number and copies it to a register so Min <= Rn <= Max */
	else if ((data_reg&MASK_COMMAND) == (RANDV&MASK_COMMAND)) {
		int r_num = rand(); 																 /* Generates a random number */
		int delta = *(g_active_game->p_data + PC + 2) - *(g_active_game->p_data + PC + 1);	 /* delta = Max - Min */
		Rn[(data_reg&0x00FF0000) >> 16] = (r_num%delta) + *(g_active_game->p_data + PC + 1);	 /* Fits random number so Min <= Random <= Max */
		PC += 3;
	}


	/* RAND: Generates a random number and copies it to a register so Rmin <= Rn <= Rmax */
	else if ((data_reg&MASK_COMMAND) == (RANDR&MASK_COMMAND)) {
		int r_num = rand(); 															/* Generates a random number */
		int delta = Rn[(data_reg&0x0000FF00) >> 8] - Rn[data_reg&0x000000FF];	 		/* delta = Max - Min */
		Rn[(data_reg&0x00FF0000) >> 16] = (r_num%delta) + Rn[data_reg&0x000000FF];	 	/* Fits random number so Min <= Random <= Max */
		PC++;
	}


	/* ADD: Adds a value to a register */
	else if ((data_reg&MASK_COMMAND) == (ADDV&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] += *(g_active_game->p_data + PC + 1);
		PC += 2;
	}


	/* ADD: Adds a value of a register to another register */
	else if ((data_reg&MASK_COMMAND) == (ADDR&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] += Rn[(data_reg&0x0000FF00) >> 8];
		PC++;
	}


	/* SUB: Subtracts a value from a register */
	else if ((data_reg&MASK_COMMAND) == (SUBV&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] -= *(g_active_game->p_data + PC + 1);
		PC += 2;
	}


	/* SUB: Subtracts a value of a register from another register */
	else if ((data_reg&MASK_COMMAND) == (SUBR&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] -= Rn[(data_reg&0x0000FF00) >> 8];
		PC++;
	}


	/* MUL: Multiplies a value with a register */
	else if ((data_reg&MASK_COMMAND) == (MULV&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] *= *(g_active_game->p_data + PC + 1);
		PC += 2;
	}


	/* MUL: Multiplies a value of a register with another register */
	else if ((data_reg&MASK_COMMAND) == (MULR&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] *= Rn[(data_reg&0x0000FF00) >> 8];
		PC++;
	}


	/* DIV: Divides a value with a register */
	else if ((data_reg&MASK_COMMAND) == (DIVV&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] /= *(g_active_game->p_data + PC + 1);
		PC += 2;
	}


	/* DIV: Divides a value of a register with another register */
	else if ((data_reg&MASK_COMMAND) == (DIVR&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] /= Rn[(data_reg&0x0000FF00) >> 8];
		PC++;
	}


	/* MOD:  */
	else if ((data_reg&MASK_COMMAND) == (MODV&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] %= *(g_active_game->p_data + PC + 1);
		PC += 2;
	}


	/* MOD:  */
	else if ((data_reg&MASK_COMMAND) == (MODR&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] %= Rn[(data_reg&0x0000FF00) >> 8];
		PC++;
	}


	/* LS: Left shift a register by a value, if no value is given this will left shift by one */
	else if ((data_reg&MASK_COMMAND) == (LS&MASK_COMMAND)) {
		if (Rn[(data_reg&0x0000FF00) >> 8] > 0 && Rn[(data_reg&0x0000FF00) >> 8] < 32)
			Rn[(data_reg&0x00FF0000) >> 16] <<= Rn[(data_reg&0x0000FF00) >> 8];
		else
			Rn[(data_reg&0x00FF0000) >> 16] <<= 1;
		PC ++;
	}

	/* RS: Right shift a register by a value, if no value is given this will right shift by one */
	else if ((data_reg&MASK_COMMAND) == (RS&MASK_COMMAND)) {
		if (Rn[(data_reg&0x0000FF00) >> 8] > 0 && Rn[(data_reg&0x0000FF00) >> 8] < 32)
			Rn[(data_reg&0x00FF0000) >> 16] >>= Rn[(data_reg&0x0000FF00) >> 8];
		else
			Rn[(data_reg&0x00FF0000) >> 16] >>= 1;
		PC ++;
	}


	/* LR: */
	else if ((data_reg&MASK_COMMAND) == (LS&MASK_COMMAND)) {
		uint32_t tmp;
		if (Rn[(data_reg&0x0000FF00) >> 8] > 0 && Rn[(data_reg&0x0000FF00) >> 8] < 32) {
			tmp = Rn[(data_reg&0x00FF0000)]>>(32-Rn[(data_reg&0x0000FF00) >> 8]);
			Rn[(data_reg&0x00FF0000) >> 16] <<= Rn[(data_reg&0x0000FF00) >> 8];
			Rn[(data_reg&0x00FF0000) >> 16] += tmp;
		} else {
			tmp = Rn[(data_reg&0x00FF0000)]&1<<31;
			Rn[(data_reg&0x00FF0000) >> 16] <<= 1;
			Rn[(data_reg&0x00FF0000) >> 16] += tmp>>31;
		}
		PC ++;
	}


	/* RR */
	else if ((data_reg&MASK_COMMAND) == (LS&MASK_COMMAND)) {
		uint32_t tmp;
		if (Rn[(data_reg&0x0000FF00) >> 8] > 0 && Rn[(data_reg&0x0000FF00) >> 8] < 32) {
			tmp = Rn[(data_reg&0x00FF0000)]<<(32-Rn[(data_reg&0x0000FF00) >> 8]);
			Rn[(data_reg&0x00FF0000) >> 16] >>= Rn[(data_reg&0x0000FF00) >> 8];
			Rn[(data_reg&0x00FF0000) >> 16] += tmp;
		} else {
			tmp = Rn[(data_reg&0x00FF0000)]&1>>31;
			Rn[(data_reg&0x00FF0000) >> 16] >>= 1;
			Rn[(data_reg&0x00FF0000) >> 16] += tmp<<31;
		}
		PC ++;
	}



	/* INC: Increments a register by one */
	else if ((data_reg&MASK_COMMAND) == (INC&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16]++;
		PC++;
	}


	/* DEC: Decrements a register by one */
	else if ((data_reg&MASK_COMMAND) == (DEC&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16]--;
		PC++;
	}


	/* DJNZ: Decrease register by one and jump to address if register is not 0*/
	else if ((data_reg&MASK_COMMAND) == (DJNZ&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16]--;
		if (Rn[(data_reg&0x00FF0000) >> 16] == 0)
			PC += 2;
		else
			PC = *(g_active_game->p_data + PC + 1);
	}


	/* DJZ: Decrease register by one and jump to address if register is not 0*/
	else if ((data_reg&MASK_COMMAND) == (DJZ&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16]--;
		if (Rn[(data_reg&0x00FF0000) >> 16] != 0)
			PC += 2;
		else
			PC = *(g_active_game->p_data + PC + 1);
	}


	/* PUSH: Pushes a register to the stack	*/
	else if ((data_reg&MASK_COMMAND) == (PUSH&MASK_COMMAND)) {
		stack[SP++] = Rn[(data_reg&0x00FF0000) >> 16];
		PC++;
	}


	/* POP: Pops a 32-bit number from the stack and moves it to a register	*/
	else if ((data_reg&MASK_COMMAND) == (PUSH&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] = stack[--SP];
		PC++;
	}


	/* AND: */
	else if ((data_reg&MASK_COMMAND) == (ANDV&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] &= *(g_active_game->p_data + PC + 1);
		PC+=2;
	}


	/* AND: */
	else if ((data_reg&MASK_COMMAND) == (ANDR&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] &= Rn[(data_reg&0x0000FF00) >> 8];
		PC++;
	}


	/* OR: */
	else if ((data_reg&MASK_COMMAND) == (ORV&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] |= *(g_active_game->p_data + PC + 1);
		PC+=2;
	}


	/* OR: */
	else if ((data_reg&MASK_COMMAND) == (ORR&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] |= Rn[(data_reg&0x0000FF00) >> 8];
		PC++;
	}


	/* XOR: */
	else if ((data_reg&MASK_COMMAND) == (XORV&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] ^= *(g_active_game->p_data + PC + 1);
		PC+=2;
	}


	/* XOR: */
	else if ((data_reg&MASK_COMMAND) == (XORR&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] ^= Rn[(data_reg&0x0000FF00) >> 8];
		PC++;
	}


	/* COMP: */
	else if ((data_reg&MASK_COMMAND) == (COMP&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] = ~Rn[(data_reg&0x00FF0000) >> 16];
		PC++;
	}


	/* JLT: */
	else if ((data_reg&MASK_COMMAND) == (JLTV&MASK_COMMAND)) {
		if (Rn[(data_reg&0x00FF0000) >> 16] < *(g_active_game->p_data + PC + 1))
			PC = *(g_active_game->p_data + PC + 2);
		else
			PC++;
	}


	/* JLT: */
	else if ((data_reg&MASK_COMMAND) == (JLTR&MASK_COMMAND)) {
		if (Rn[(data_reg&0x00FF0000) >> 16] < Rn[(data_reg&0x0000FF00) >> 8])
			PC = *(g_active_game->p_data + PC + 1);
		else
			PC++;
	}

	/* JLE: */
	else if ((data_reg&MASK_COMMAND) == (JLEV&MASK_COMMAND)) {
		if (Rn[(data_reg&0x00FF0000) >> 16] <= *(g_active_game->p_data + PC + 1))
			PC = *(g_active_game->p_data + PC + 2);
		else
			PC++;
	}


	/* JLE: */
	else if ((data_reg&MASK_COMMAND) == (JLER&MASK_COMMAND)) {
		if (Rn[(data_reg&0x00FF0000) >> 16] <= Rn[(data_reg&0x0000FF00) >> 8])
			PC = *(g_active_game->p_data + PC + 1);
		else
			PC++;
	}

	/* JGT: */
	else if ((data_reg&MASK_COMMAND) == (JGTV&MASK_COMMAND)) {
		if (Rn[(data_reg&0x00FF0000) >> 16] > *(g_active_game->p_data + PC + 1))
			PC = *(g_active_game->p_data + PC + 2);
		else
			PC++;
	}


	/* JGT: */
	else if ((data_reg&MASK_COMMAND) == (JGTR&MASK_COMMAND)) {
		if (Rn[(data_reg&0x00FF0000) >> 16] > Rn[(data_reg&0x0000FF00) >> 8])
			PC = *(g_active_game->p_data + PC + 1);
		else
			PC++;
	}

	/* JGE: */
	else if ((data_reg&MASK_COMMAND) == (JGEV&MASK_COMMAND)) {
		if (Rn[(data_reg&0x00FF0000) >> 16] >= *(g_active_game->p_data + PC + 1))
			PC = *(g_active_game->p_data + PC + 2);
		else
			PC++;
	}


	/* JGE: */
	else if ((data_reg&MASK_COMMAND) == (JGER&MASK_COMMAND)) {
		if (Rn[(data_reg&0x00FF0000) >> 16] >= Rn[(data_reg&0x0000FF00) >> 8])
			PC = *(g_active_game->p_data + PC + 1);
		else
			PC++;
	}





	/*DEBUG: Prints the value of a register to the UART */
	else if ((data_reg&MASK_COMMAND) == DEBUGR) {
			printf("Value of R%d: 0x%x\t%ld\r\n", (uint)(data_reg&0x00FF0000) >> 16, (uint)Rn[(data_reg&0x00FF0000) >> 16], (uint)Rn[(data_reg&0x00FF0000) >> 16]);
			PC ++;
	}


	/*DEBUG: Prints a string to the UART */
	else if ((data_reg&MASK_COMMAND) == (DEBUGM&MASK_COMMAND)) {
			printf("DEBUG: %.*s\r\n", (int)((data_reg&0x00FF0000) >> 16), (char*)(g_active_game->p_data + PC + 1));
			PC += (ceil((double)((data_reg&0x00FF0000) >> 16)/4) + 1);
	}


	else if ((data_reg&MASK_COMMAND) == (DISPBGCOLOR&MASK_COMMAND)) {
		LCD_Set_BG_Color(Rn[(data_reg&0x00FF0000) >> 16]);
		PC++;
	}


	else if ((data_reg&MASK_COMMAND) == (DISPSTRING&MASK_COMMAND)) {
		uint32_t data_reg2 = *(g_active_game->p_data + PC + 1);
		char * str = (char*)(g_active_game->p_data + PC + 2);
		LCD_Draw_String(str, Rn[(data_reg&0x0000FF00) >> 8], Rn[data_reg&0x000000FF], Rn[(data_reg2&0xFF000000) >> 24], (data_reg&0x00FF0000) >> 16);
		PC+=ceil((double)((data_reg&0x00FF0000) >> 16)/4) + 2;
	}


	else if ((data_reg&MASK_COMMAND) == (DISPNUMBER&MASK_COMMAND)) {
		uint32_t data_reg2 = *(g_active_game->p_data + PC + 1);
		LCD_Draw_Number(Rn[(data_reg&0x00FF0000) >> 16], Rn[(data_reg&0x0000FF00) >> 8], Rn[data_reg&0x000000FF], Rn[(data_reg2&0xFF000000) >> 24]);
		PC+=2;
	}


	/* DRAWLINE: Draws a line on the screen */
	else if ((data_reg&MASK_COMMAND) == (DRAWLINE&MASK_COMMAND)) {
		uint32_t data_reg2 = *(g_active_game->p_data + PC + 1);
		LCD_Draw_Line(Rn[(data_reg&0x00FF0000) >> 16], Rn[(data_reg&0x0000FF00) >> 8], Rn[data_reg&0x000000FF], Rn[(data_reg2&0xFF000000) >> 24], Rn[(data_reg2&0x00FF0000) >> 16]);
		PC+=2;
	}

	/* DRAWRECT: Draws a rectangle on the screen */
	else if ((data_reg&MASK_COMMAND) == (DRAWRECT&MASK_COMMAND)) {
		uint32_t data_reg2 = *(g_active_game->p_data + PC + 1);
		LCD_Draw_Rect(Rn[(data_reg&0x00FF0000) >> 16], Rn[(data_reg&0x0000FF00) >> 8], Rn[data_reg&0x000000FF], Rn[(data_reg2&0xFF000000) >> 24], Rn[(data_reg2&0x00FF0000) >> 16]);
		PC+=2;
	}

	/* DRAWCIRCLE: Draws a circle on the screen */
	else if ((data_reg&MASK_COMMAND) == (DRAWCIRCLE&MASK_COMMAND)) {
		uint32_t data_reg2 = *(g_active_game->p_data + PC + 1);
		LCD_Draw_Circle(Rn[(data_reg&0x00FF0000) >> 16], Rn[(data_reg&0x0000FF00) >> 8], Rn[data_reg&0x000000FF], Rn[(data_reg2&0xFF000000) >> 24]);
		PC+=2;
	}

	return 0;
}


error_t interpreter_exit(uint8_t code) {

	printf("Exiting with code %d ... \r\n", code);

	PC = 0;
	SP = 0;
	memset(Rn, 0, sizeof(Rn));

	interpreter_running = 0;
	load_menu();

	return 0;
}


