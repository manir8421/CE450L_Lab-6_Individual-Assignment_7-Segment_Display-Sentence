import RPi.GPIO as GPIO
import time

# GPIO pin
SDI = 17
RCLK = 27
SRCLK = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup([SDI, RCLK, SRCLK], GPIO.OUT)

bin_alp = {
    ' ': 0b1111111,  # Space
    'A': 0b0001000, 'B': 0b0000011, 'C': 0b1000110, 'D': 0b0100001,
    'E': 0b0000110, 'F': 0b0001110, 'G': 0b0010000, 'H': 0b0001011,
    'I': 0b1111011, 'J': 0b1110001, 'K': 0b0001111, 'L': 0b1000111,
    'M': 0b1001001, 'N': 0b0101011, 'O': 0b0100011, 'P': 0b0001100,
    'Q': 0b0011000, 'R': 0b0101111, 'S': 0b0010010, 'T': 0b0000111,
    'U': 0b1100011, 'V': 0b1000001, 'W': 0b1001001, 'X': 0b0001001,
    'Y': 0b0010001, 'Z': 0b0100100,
}

def shift(data):
    GPIO.output(RCLK, GPIO.LOW)
    for bit in range(16):
        GPIO.output(SRCLK, GPIO.LOW)
        GPIO.output(SDI, (data >> (15 - bit)) & 0x01)
        GPIO.output(SRCLK, GPIO.HIGH)
    GPIO.output(RCLK, GPIO.HIGH)

def dis_off():
    shift(0b1111111 << 8 | 0b1111111)  # Both displays (off)
    time.sleep(1)                      # Short delay before starting the sequence

def dis_message(sentence):
    sentence = sentence.upper() + '  '  
    prev_char = 0b1111111        # Initialize with space
    
    for char in sentence:
        crnt_char = bin_alp[char] if char in bin_alp else 0b1111111
        combined_code = (prev_char << 8) | crnt_char
        shift(combined_code)
        time.sleep(1.5)                       # Adjust time
        prev_char = crnt_char

try:
    dis_off()
    input_sentence = input("Type the sentence to display: ")
    dis_message(input_sentence)
except KeyboardInterrupt:
    print("Program stopped by user.")
finally:
    GPIO.cleanup()
    print("GPIO cleaned up.")
