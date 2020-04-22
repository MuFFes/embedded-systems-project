#include "uart.h"

void uart_init(uint16_t baud) {
	// Set baudrate
	uint16_t ubbr=F_CPU/16/baud-1;
	UBRRH = (uint8_t)(ubbr>>8);
	UBRRL = (uint8_t)ubbr;

	// Enable both - recieving and transmitting
	UCSRB = (1<<RXEN)|(1<<TXEN); 
	// Set data bit count to 8
	UCSRC = (1<<URSEL)|(1<<UCSZ0)|(1<<UCSZ1);
}

void uart_putchar(unsigned char data) {
	while(!(UCSRA&(1<<UDRE))); // Wait for buffor to be empty
	UDR = data; // Pass value to buffor 
	while(!(UCSRA&(1<<TXC))); // Wait for value to be sent
}

unsigned char uart_getchar() {
	while (!(UCSRA & _BV(RXC)));	// Wait for data to be received
	return (uint8_t) UDR0;
}