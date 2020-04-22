#ifndef UART_H
#define UART_H

#include <avr/io.h>
#include <stdlib.h>

void uart_init(uint16_t baud);
void uart_putchar(unsigned char data);
unsigned char uart_getchar();

#endif