#include "interpreter.h"
#include "main.h"
#include "memmanager.h"
#include <stdio.h>
#include <math.h>

error_t interpreter_init() {
	PC = 0;
	SP = 0;

	Rn[5] = 0xAB;

	interpreter_running = 1;

	printf("Running %s\r\n", g_active_game.title);

	time_t t;
	srand((unsigned) time(&t));

	return 0;
}


error_t interpreter_update() {

	if (!interpreter_running)
		return 1;

	uint32_t data_reg = *((uint32_t*)(g_active_game.p_data + PC));

	/*
	printf("DP: %d\r\n", DP);
	printf("DATA: %x\r\n", (uint)data_reg);
	*/

	/* STOP: Stops the program with given stop code	*/
	if ((data_reg&MASK_COMMAND) == (STOP&MASK_COMMAND) && ((data_reg&0x00FF0000) > 0))
		interpreter_exit((data_reg&0x00FF0000) >> 16);

	/* CLR:		*/
	if ((data_reg&MASK_COMMAND) == (CLEAR&MASK_COMMAND))
		/* Add function to clear the screen */
		;


	if ((data_reg&MASK_COMMAND) == (RET&MASK_COMMAND))
		PC = stack[--SP];	/* Pulls Program Counter from the stack. Only use in combination with CALL */


	/* SJMP: Changes Program Counter to requested address. Can only handle 16.777.216 32-bit addresses. This should be enough, if not use "JMP". */
	if ((data_reg&MASK_COMMAND) == (SJMP&MASK_COMMAND))
		PC = (data_reg&~MASK_COMMAND);		  	/* Loads the 24-bit number in the instruction to the Program Counter */


	/* JMP: Changes Program Counter to requested address anywhere in memory. Slightly less efficient than SJMP */
	if ((data_reg&MASK_COMMAND) == (JMP&MASK_COMMAND))
		PC = *(g_active_game.p_data + PC + 1); 	/* Loads 32-bit number after the instruction to the Program Counter. */


	/* CALL: Changes Program Counter to requested address and also pushes the Program Counter to stack. Only use in combination with RET */
	if ((data_reg&MASK_COMMAND) == (CALL&MASK_COMMAND)) {
		stack[SP++] = PC;						/* Pushes Program Counter to the Stack */
		PC = *(g_active_game.p_data + PC + 1); 	/* Loads 32-bit number after the instruction to the Program Counter. */
	}


	/* JNE:	Changes Program Counter to requested address if the value of a register isn't the same as the value given */
	if ((data_reg&MASK_COMMAND) == (JNEV&MASK_COMMAND)) {
		if (Rn[(data_reg&0x00FF0000) >> 16] == *(g_active_game.p_data + PC + 1)) 	/* Compares register to value */
			PC++;
		else
			PC = *(g_active_game.p_data + PC + 2); 									/* Loads 32-bit number after the instruction to the Program Counter. */
	}


	/* JNE:	Changes Program Counter to requested address if the value of two registers isn't the same */
	if ((data_reg&MASK_COMMAND) == (JNER&MASK_COMMAND)) {
		if (Rn[(data_reg&0x00FF0000) >> 16] == Rn[(data_reg&0x0000FF00) >> 8]) 	/* Compares register to register */
			PC++;
		else
			PC = *(g_active_game.p_data + PC + 1); 								/* Loads 32-bit number after the instruction to the Program Counter. */
	}


	/* JE:	Changes Program Counter to requested address if the value of a register is the same as the value given */
	if ((data_reg&MASK_COMMAND) == (JEV&MASK_COMMAND)) {
		if (Rn[(data_reg&0x00FF0000) >> 16] == *(g_active_game.p_data + PC + 1)) 	/* Compares register to value */
			PC = *(g_active_game.p_data + PC + 2); 									/* Loads 32-bit number after the instruction to the Program Counter. */
		else
			PC++;
	}


	/* JE:	Changes Program Counter to requested address if the value of two registers is the same */
	if ((data_reg&MASK_COMMAND) == (JER&MASK_COMMAND)) {
		if (Rn[(data_reg&0x00FF0000) >> 16] == Rn[(data_reg&0x0000FF00) >> 8]) 	/* Compares register to register */
			PC = *(g_active_game.p_data + PC + 1); 								/* Loads 32-bit number after the instruction to the Program Counter. */
		else
			PC++;
	}


	/* MOV: Copies a value to a register */
	if ((data_reg&MASK_COMMAND) == (MOVV&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] = *(g_active_game.p_data + PC + 1); /* Copies value to register */
		PC++;
	}


	/* MOV: Copies the value of a register to another register */
	if ((data_reg&MASK_COMMAND) == (MOVR&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] = Rn[(data_reg&0x0000FF00) >> 8]; 	/*  Copies value of a register to another register */
		PC++;
	}


	/* RAND: Generates a random number and copies it to a register so Min <= Rn <= Max */
	if ((data_reg&MASK_COMMAND) == (RANDV&MASK_COMMAND)) {
		int r_num = rand(); 																 /* Generates a random number */
		int delta = *(g_active_game.p_data + PC + 2) - *(g_active_game.p_data + PC + 1);	 /* delta = Max - Min */
		Rn[(data_reg&0x00FF0000) >> 16] = (r_num%delta) + *(g_active_game.p_data + PC + 1);	 /* Fits random number so Min <= Random <= Max */
		PC += 3;
	}


	/* RAND: Generates a random number and copies it to a register so Rmin <= Rn <= Rmax */
	if ((data_reg&MASK_COMMAND) == (RANDR&MASK_COMMAND)) {
		int r_num = rand(); 															/* Generates a random number */
		int delta = Rn[(data_reg&0x0000FF00) >> 8] - Rn[data_reg&0x000000FF];	 		/* delta = Max - Min */
		Rn[(data_reg&0x00FF0000) >> 16] = (r_num%delta) + Rn[data_reg&0x000000FF];	 	/* Fits random number so Min <= Random <= Max */
		PC++;
	}


	/* ADD: Adds a value to a register */
	if ((data_reg&MASK_COMMAND) == (ADDV&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] += *(g_active_game.p_data + PC + 1);
		PC += 2;
	}


	/* ADD: Adds a value of a register to another register */
	if ((data_reg&MASK_COMMAND) == (ADDR&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] += Rn[(data_reg&0x0000FF00) >> 8];
		PC++;
	}


	/* SUB: Subtracts a value from a register */
	if ((data_reg&MASK_COMMAND) == (SUBV&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] -= *(g_active_game.p_data + PC + 1);
		PC += 2;
	}


	/* SUB: Subtracts a value of a register from another register */
	if ((data_reg&MASK_COMMAND) == (SUBR&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] -= Rn[(data_reg&0x0000FF00) >> 8];
		PC++;
	}


	/* MUL: Multiplies a value with a register */
	if ((data_reg&MASK_COMMAND) == (MULV&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] *= *(g_active_game.p_data + PC + 1);
		PC += 2;
	}


	/* MUL: Multiplies a value of a register with another register */
	if ((data_reg&MASK_COMMAND) == (MULR&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] *= Rn[(data_reg&0x0000FF00) >> 8];
		PC++;
	}


	/* DIV: Divides a value with a register */
	if ((data_reg&MASK_COMMAND) == (DIVV&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] /= *(g_active_game.p_data + PC + 1);
		PC += 2;
	}


	/* DIV: Divides a value of a register with another register */
	if ((data_reg&MASK_COMMAND) == (DIVR&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] /= Rn[(data_reg&0x0000FF00) >> 8];
		PC++;
	}


	/* MOD:  */
	if ((data_reg&MASK_COMMAND) == (MODV&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] %= *(g_active_game.p_data + PC + 1);
		PC += 2;
	}


	/* MOD:  */
	if ((data_reg&MASK_COMMAND) == (MODR&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16] %= Rn[(data_reg&0x0000FF00) >> 8];
		PC++;
	}


	/* LS: Left shift a register by a value, if no value is given this will left shift by one */
	if ((data_reg&MASK_COMMAND) == (LS&MASK_COMMAND)) {
		if (Rn[(data_reg&0x0000FF00) >> 8] > 0 && Rn[(data_reg&0x0000FF00) >> 8] < 32)
			Rn[(data_reg&0x00FF0000) >> 16] <<= Rn[(data_reg&0x0000FF00) >> 8];
		else
			Rn[(data_reg&0x00FF0000) >> 16] <<= 1;
		PC ++;
	}

	/* RS: Right shift a register by a value, if no value is given this will right shift by one */
	if ((data_reg&MASK_COMMAND) == (RS&MASK_COMMAND)) {
		if (Rn[(data_reg&0x0000FF00) >> 8] > 0 && Rn[(data_reg&0x0000FF00) >> 8] < 32)
			Rn[(data_reg&0x00FF0000) >> 16] >>= Rn[(data_reg&0x0000FF00) >> 8];
		else
			Rn[(data_reg&0x00FF0000) >> 16] >>= 1;
		PC ++;
	}


	/* LR and RR TBI */


	/* INC: Increments a register by one */
	if ((data_reg&MASK_COMMAND) == (INC&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16]++;
		PC++;
	}


	/* DEC: Decrements a register by one */
	if ((data_reg&MASK_COMMAND) == (DEC&MASK_COMMAND)) {
		Rn[(data_reg&0x00FF0000) >> 16]--;
		PC++;
	}


	/* DJNZ and DJZ TBI */


	/*
	 TBI
	 */




	/*DEBUG: Prints the value of a register to the UART */
	if ((data_reg&MASK_COMMAND) == DEBUGR) {
			printf("Value of R0x%x: 0x%x\r\n", (uint)(data_reg&0x00FF0000) >> 16, (uint)Rn[(data_reg&0x00FF0000) >> 16]);
			PC ++;
	}


	/*DEBUG: Prints a string to the UART */
	if ((data_reg&MASK_COMMAND) == (DEBUGM&MASK_COMMAND)) {
			printf("DEBUG: %.*s\r\n", (int)((data_reg&0x00FF0000) >> 16), (char*)(g_active_game.p_data + PC + 1));
			PC += ceil((double)((data_reg&0x00FF0000) >> 16)/4) + 1;
	}

	return 0;
}


error_t interpreter_exit(uint8_t code) {

	printf("Exiting with code %d ... \r\n", code);

	interpreter_running = 0;


	return 0;
}


