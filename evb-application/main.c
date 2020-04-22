#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <stdlib.h>
#include "uart.h"

const char key_desription[8][16] = {
	"K1: ............",
	"K2: ............",
	"K3: ............",
	"K4: ............",
	"K5: ............",
	"K6: ............",
	"K7: ............",
	"K8: ............"
};

bool volume_changed = 0;
uint8_t new_volume_level = 0;

bool key_pressed = 0;
uint8_t key_id   = 0;

int main(void) {
	uart_init(9600);
    
    // ZAD 5: 
    /// TODO: interrupts

	while(true) {
        // ZAD 1: 
        if (volume_changed == 1) {
            uart_putchar('S');
            delay_ms(10);
            uart_putchar(new_volume_level);
            /// TODO: interrupts
            volume_changed = 0;
        }

        // ZAD 2: 
        uart_putchar('A');
        uint8_t current_volume_level = uart_getchar();
        /// TODO: Handle received message and light up diodes

        // ZAD 3: 
        uart_putchar('T');
        uint8_t cpu_usage       = uart_getchar();
        uint8_t cpu_temperature = uart_getchar();
        uint8_t ram_usage       = uart_getchar();
        /// TODO: Handle received message and show data on screen 1st row eg. "C:100 T:47 R:50"

        // ZAD 4: 
        if (key_pressed == 1) {
            uart_putchar('K');
            _delay_ms(10);
            uart_putchar(key_id);

            /// TODO: interrupts
            key_pressed = 0;
        }

        // ZAD 6: 
        uart_putchar('V');
        uint8_t red   = uart_getchar();
        uint8_t green = uart_getchar();
        uint8_t blue  = uart_getchar();
        /// TODO: Handle received message and show data on rgb diode"



		_delay_ms(100);
	}

	return 0;
}
