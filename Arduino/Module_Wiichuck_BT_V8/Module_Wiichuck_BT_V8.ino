
#include "Wire.h"
#include "WiiChuck.h"

#include <SPI.h> //Call SPI library so you can communicate with the nRF24L01+
#include <nRF24L01.h> //nRF2401 libarary found at https://github.com/tmrh20/RF24/
#include <RF24.h> //nRF2401 libarary found at https://github.com/tmrh20/RF24/

const int pinCE = 9; //This pin is used to set the nRF24 to standby (0) or active mode (1)
const int pinCSN = 10; //This pin is used to tell the nRF24 whether the SPI communication is a command or message to send out
//bool done = false; //used to know when to stop sending guesses
RF24 wirelessSPI(pinCE, pinCSN); // Create your nRF24 object or wireless SPI connection

const uint64_t wAddress = 0xB00B1E50C3LL;  //pipe for writing or transmitting data
const uint64_t rAddress = 0xB00B1E50A4LL;  //pipe for reading or recieving data

int buttonPin = 2;
int flag_zero = 0;

WiiChuck chuck = WiiChuck();

void setup() {
  
  Serial.begin(9600);   //for debugging purposes
  chuck.begin();
  chuck.update();
  
  wirelessSPI.begin();            //Start the nRF24 module
  wirelessSPI.openWritingPipe(wAddress);    // setup pipe to transmit over
  wirelessSPI.openReadingPipe(1, rAddress); //set up pipe to recieve data
  wirelessSPI.stopListening();  //turn off recieve capability so you can transmit

}

void loop() {

  char tx_data[4];
  chuck.update();

  tx_data[0] = chuck.readJoyX();
  tx_data[1] = chuck.readJoyY();
  tx_data[2] = chuck.buttonZ;
  tx_data[3] = chuck.buttonC;
 
  Serial.print(tx_data[0], DEC);
  Serial.print(",");
  Serial.print(tx_data[1], DEC);
  Serial.print(",");
  Serial.print(tx_data[2], DEC);
  Serial.print(",");
  Serial.print(tx_data[3], DEC);
  Serial.print(",");
  Serial.println();

  if (digitalRead(buttonPin) == HIGH  && ((tx_data[0] < -10 || 10 < tx_data[0] || tx_data[1] < -10 || 10 < tx_data[1] || tx_data[2] == 1 || tx_data[3] == 1) || flag_zero == 1 )) {
    flag_zero = 1;
    if (!wirelessSPI.write( &tx_data, 4 )) { //if the write fails let the user know over serial monitor
      //Serial.println("Guess delivery failed");
    }
    else { //if the write was successful
      //Serial.print("Success sending guess: ");
      if (tx_data[0] >= -10 || 10 >= tx_data[0] || tx_data[1] >= -10 || 10 >= tx_data[1] || tx_data[2] != 1 || tx_data[3] != 1)
      {
        flag_zero = 0;
      }
    }
  }
  delay(20); // adapt the speed of the communication
}


