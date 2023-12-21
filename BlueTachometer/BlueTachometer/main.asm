; register description
; R16 - general purpose register
; R17 - uart data register
; R18 - uart flag register
; R20 - data bit counter
; R23 - 2nd byte of 32-bit timer [ R25 | R24 | R23 | TCNT0 ]
; R24 - 3rd byte of 32-bit timer [ R25 | R24 | R23 | TCNT0 ]
; R25 - 4th byte of 32-bit timer [ R25 | R24 | R23 | TCNT0 ]

; port description
; PB3 - TX pin
; PB4 - digital input for HALL sensor VOUT

; constant definitions
.equ uart_data_bits = 8

; reset and interrupt vectors
.CSEG ; Program code segment
.ORG 0 ; Reset- and vector address
rjmp RESET ; RESET ; External Pin, Power-on Reset, Brown-out Reset, Watchdog Reset
reti ; INT0 ; External Interrupt Request 0
reti ; PCINT0 ; Pin Change Interrupt Request 0
rjmp TIM0_OVF ; Timer/Counter Overflow
reti ; EE_RDY ; EEPROM Ready
reti ; ANA_COMP ; Analog Comparator
rjmp TIM0_COMPA ; Timer/Counter Compare Match A
reti ; TIM0_COMPB ; Timer/Counter Compare Match B
reti ; WDT ; Watchdog Time-out
reti ; ADC ; ADC Conversion Complete

; interrupt service routines
TIM0_OVF:
in R16, SREG ; save status register
inc R23 ; 2nd byte
brne TIM0_OVF_END
inc R24 ; 3rd byte
brne TIM0_OVF_END
inc R25 ; 4th byte
TIM0_OVF_END:
out SREG, R16 ; restore status register
reti

TIM0_COMPA:
ldi R18, 1 ; set flag register
reti ; Interrupt Return

; RESET START
RESET:
; init UART TX and HALL sensor input pins
sbi DDRB, DDB3 ; configure PB3 pin as output
ldi R16, (1<<PORTB3) ; set PB3 pin high (active low)
out PORTB, R16 ; PORTB - Port B Data Register
; init stack pointer
ldi R16, LOW(RAMEND) ; set stack pointer to the top
out SPL, R16 ; SPL - Stack Pointer Low Register
; init timer/counter compare value
ldi R16, 125 ; 9600 baud (104.167 us)
out OCR0A, R16 ; OCR0A - Output Compare Register A
; init interrupts
ldi R16, (1<<OCIE0A) | (1<<TOIE0) ; OCIEA0A - Compare Match A Interrupt Enable | TOIE0 - Overflow Interrupt Enable
out TIMSK0, R16 ; TIMSK0 - Timer/Counter Interrupt Mask Register
sei ; Global Interrupt Enable
; RESET END

; MAIN START
MAIN_0:
; configure timer/counter
clr R16
out TCCR0A, R16 ; Normal mode, TCCR0A - Timer/Counter Control Register A
out TCNT0, R16 ; reset 32-bit timer, TCNT0 - Timer/Counter Register
clr R23 ; reset 32-bit timer
clr R24 ; reset 32-bit timer
clr R25 ; reset 32-bit timer
; wait for input to go HIGH
MAIN_1:
sbis PINB, PINB4 ; Skip if Bit in I/O Register Set ; 1/2
rjmp MAIN_1 ; 2
; wait for input to go LOW
MAIN_2:
sbic PINB, PINB4 ; Skip if Bit in I/O Register Cleared
rjmp MAIN_2 ; 2
; start timer
ldi R16, (1<<CS00) ; no prescaler = 1.2 MHz = 833 ns
out TCCR0B, R16 ; TCCR0B - Timer/Counter Control Register B
; wait for input to go HIGH again
MAIN_3:
sbis PINB, PINB4; Skip if Bit in I/O Register Set
rjmp MAIN_3 ; 2
; wait for input to go LOW again
MAIN_4:
sbic PINB, PINB4; Skip if Bit in I/O Register Cleared
rjmp MAIN_4 ; 2
; stop timer
clr R16 ; No clock source (Timer/Counter stopped)
out TCCR0B, R16 ; TCCR0B - Timer/Counter Control Register B
; send time via UART
MAIN_5:
in R17, TCNT0 ; move recorded 1st byte to uart data register
rcall UART_START ; send 1st byte
mov R17, R23 ; move recorded 2nd byte to uart data register
rcall UART_START ; send 2nd byte
mov R17, R24 ; move recorded 3rd byte to uart data register
rcall UART_START ; send 3rd byte
mov R17, R25 ; move recorded 4th byte to uart data register
rcall UART_START ; send 4th byte
; repeat
rjmp MAIN_0
; MAIN END

; UART SUBROUTINE START
UART_START:
ldi R16, 1<<WGM01 ; CTC mode
out TCCR0A, R16 ; Timer/Counter Control Register A
clr R16 ; reset timer
out TCNT0, R16 ; Timer/Counter Register
clr R20 ; reset data bit counter
clr R18 ; clear uart flag register
ldi R16, 1<<CS00 ; start timer with no prescaling	1
out TCCR0B, R16 ; TCCR0B - Timer/Counter Control Register B	1
cbi PORTB, PORTB3 ; start uart communication, send START bit

UART_DATA:
; wait for uart flag to be set
sbrs R18, 0 ; Skip if Bit in Register Set	1/2
rjmp UART_DATA ;	2
; send data bit
sbrc R17, 0 ; Skip if Bit in Register Cleared	1/2
sbi PORTB, PORTB3 ; pull TX pin high	2
sbrs R17, 0 ; Skip if Bit in Register Set	1/2
cbi PORTB, PORTB3 ; pull TX pin low	2
; prepare next data bit
lsr R17 ; Logical Shift Right	1
inc R20 ; increment data counter	1
ldi R18, 0 ; reset flag register	1
; send stop bit or no yet?
cpi R20, uart_data_bits ; Compare Register with Immediate	1
brne UART_DATA ; Branch if not Equal	1/2

UART_STOP:
; wait for uart flag to be set
sbrs R18, 0 ; Skip if Bit in Register Set	1/2
rjmp UART_STOP ;	2
; send stop bit
sbi PORTB, PORTB3 ; stop uart communication		2
ldi R18, 0 ; reset flag register	1

UART_END:
; wait for uart flag to be set
sbrs R18, 0 ; Skip if Bit in Register Set	1/2
rjmp UART_END ;	2
ldi R16, 0<<CS00 ; stop timer	1
out TCCR0B, R16 ; TCCR0B - Timer/Counter Control Register B	1
ret ; 4
; UART SUBROUTINE END