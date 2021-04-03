import time
import re

from GPIOSimulator_v1 import *
GPIO = GPIOSimulator()

MORSE_CODE = {'01': 'a', '1000': 'b', '101.': 'c', '100': 'd', '0': 'e', '0010': 'f', '110': 'g',
              '0000': 'h', '00': 'i', '0111': 'j', '101': 'k', '0100': 'l', '11': 'm', '10': 'n',
              '111': 'o', '0110': 'p', '1101': 'q', '010': 'r', '000': 's', '1': 't', '001': 'u',
              '0001': 'v', '011': 'w', '1001': 'x', '1011': 'y', '1100': 'z', '01111': '1',
              '00111': '2', '00011': '3', '00001': '4', '00000': '5', '10000': '6', '11000': '7',
              '11100': '8', '11110': '9', '11111': '0'}


class MorseDecoder:
    """ Morse code class """
    current_symbol = ""
    current_word = ""
    current_message = ""

    def reset(self):
        self.current_symbol = ""
        self.current_word = ""
        self.current_message = ""


    def read_one_signal(self): #Leser av button signalet fra simulatoren, for hver avlesning leser vi av 9 ganger og bruker medianen som input
        signal = []
        for i in range(9):
            signal.append(int(GPIO.input(PIN_BTN)))
        signal.sort()
        return str(signal[4])


    def decoding_loop(self):
        time.sleep(1)
        print("Start clicking in the morse code")
        signal_input = ""
        while True:
            signal_input += self.read_one_signal()
            time.sleep(.2) #Setter opp tidsintervallet til å være 0.2sec
            if signal_input == "0000000": #Sjekker etter signalet på at ordet er over
                self.handle_word_end()
                signal_input = ""
            elif signal_input[-1] == self.read_one_signal(): #Dersom to signaler på rad er de samme fortsetter loopen
                continue
            else:
                if re.match("0000*", signal_input): #Godtar alle signal av bare 0 (større eller lik 3 og mindre enn 7) som ende på et symbol
                    self.process_signal("2")
                elif signal_input == "111" or signal_input == "1111": #Godtar "111" og "1111" som dash
                    self.process_signal("1")
                elif signal_input == "1" or signal_input == "11": #Godtar "1" og "11" som dot
                    self.process_signal("0")
                signal_input = ""


    def process_signal(self, signal): #Tar for seg hvilket signal som gjør hva og skrur av og på riktige LED
        if len(self.current_symbol) > 0 and self.current_symbol[-1] == "0":
            GPIO.output(PIN_BLUE_LED, GPIO.LOW)
        elif len(self.current_symbol) > 0 and self.current_symbol[-1] == "1":
            GPIO.output(PIN_RED_LED_0, GPIO.LOW)
            GPIO.output(PIN_RED_LED_1, GPIO.LOW)
            GPIO.output(PIN_RED_LED_2, GPIO.LOW)
        if signal == "0" or signal == "1":
            if signal == "0":
                GPIO.output(PIN_BLUE_LED, GPIO.HIGH)
            else:
                GPIO.output(PIN_RED_LED_0, GPIO.HIGH)
                GPIO.output(PIN_RED_LED_1, GPIO.HIGH)
                GPIO.output(PIN_RED_LED_2, GPIO.HIGH)
            self.update_current_symbol(signal)
        elif signal == "2":
            self.handle_symbol_end()
        else :
            self.handle_word_end()

    def update_current_symbol(self, signal):
        self.current_symbol += signal
        print(self.current_symbol)

    def handle_symbol_end(self): #Tar for seg at vi er ferdige med et symbol, og legger dette til i vårt ord
        symbol = self.current_symbol
        if symbol not in MORSE_CODE:
            print("Error: input not recognized")
        else:
            self.update_current_word(MORSE_CODE[symbol])
        self.current_symbol = ""

    def update_current_word(self, symbol):
        self.current_word += symbol
        print(self.current_word)

    def handle_word_end(self):
        self.handle_symbol_end()
        self.current_message += (" " + self.current_word)
        self.show_message()
        self.current_word = ""

    def show_message(self):
        print(self.current_message)


def main():
    try:
        morse_decoder = MorseDecoder()
        morse_decoder.decoding_loop()
    except KeyboardInterrupt:
        print("Keyboard interrupt; quiting the program")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()