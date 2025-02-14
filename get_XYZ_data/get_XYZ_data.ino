#include <Wire.h>
#include "SparkFun_TMAG5273_Arduino_Library.h"

// TMAG5273 객체 생성
TMAG5273 sensor;

// TMAG5273 I2C Address
#define TMAG5273_ADDRESS 0x22

// TMAG5273 Register Addresses
#define TMAG5273_REG_X_MSB_RESULT 0x12
#define TMAG5273_REG_Y_MSB_RESULT 0x14
#define TMAG5273_REG_Z_MSB_RESULT 0x16
#define MAGNETIC_RANGE 80.0 

void setup() {
  Wire.begin();
  Serial.begin(115200);
  Serial.println("TMAG5273 Sensor Test Starting...");
}

float convertToMilliTesla(int16_t rawData) {
  return (rawData / 32768.0) * MAGNETIC_RANGE; 
}

float readMagneticField(uint8_t msbReg) {
  Wire.beginTransmission(TMAG5273_ADDRESS);
  Wire.write(msbReg); 
  if (Wire.endTransmission(false) != 0) {
    return 0;
  }
  Wire.requestFrom(TMAG5273_ADDRESS, 2); 
  if (Wire.available() < 2) {
    return 0;
  }
  int16_t rawData = (Wire.read() << 8) | Wire.read();  
  return convertToMilliTesla(rawData);
}

void loop() {
  float xField = readMagneticField(TMAG5273_REG_X_MSB_RESULT);
  float yField = readMagneticField(TMAG5273_REG_Y_MSB_RESULT);
  float zField = readMagneticField(TMAG5273_REG_Z_MSB_RESULT);

  Serial.print(xField);
  Serial.print(",");
  Serial.print(yField);
  Serial.print(",");
  Serial.println(zField);

  delay(10); 
}
