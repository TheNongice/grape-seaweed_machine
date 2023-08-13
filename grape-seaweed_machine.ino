/*
 *
 * Arduino Sensor Core Reader
 *
 * @category   IoT Device
 * @author     TheNongice
 * @copyright  2023 © Wasawat Junnasaksri and Hatsathon Sachjakul as PCSHSST
 * @license    MIT License
 * @link       https://github.com/TheNongice/grape-seaweed_machine
 * @date       13/8/2565 - 21:35
 * @editor     TheNongice Wasawat (@_ngix's)
*/

#include <OneWire.h>
#include <DallasTemperature.h>
#define PH_SENSOR A0
#define TURBIDITY A1
#define ONE_WIRE_BUS 2

#define Offset 0.00
int turbidityRead, problem;
float turbidityV, phValue, temp_water;
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature temp_sensor(&oneWire);

void setup() {
  Serial.begin(9600);
  pinMode(PH_SENSOR,INPUT);
  pinMode(TURBIDITY,INPUT);
  temp_sensor.begin();
}

float pH_avg(){
  int buf[10]; //buffer for read analog
  for(int i=0;i<10;i++){
    buf[i]=analogRead(PH_SENSOR);
    delay(10);
  }

  // Sort Value from min -> max
  for(int i=0;i<9;i++){
    for(int j=i+1;j<10;j++){
      if(buf[i]>buf[j]){
        int temp=buf[i];
        buf[i]=buf[j];
        buf[j]=temp;
      }
    }
  }

  unsigned long int avgValue=0;
  for(int i=2;i<8;i++) //take the average value of 6 center sample
    avgValue+=buf[i];
  float phValue=(float)avgValue*5.0/1024/6; //convert the analog into millivolt
  phValue=3.5*phValue+Offset;

  return phValue;
}

void loop() {
  problem = 0;
  // Check value from sensor approx every 45 seconds
  unsigned long checkTime = millis();

  if(millis() >= checkTime-45000U){
    checkTime = millis();
    // Recieve Volts & COnvert Value from Sensors
    turbidityRead = analogRead(TURBIDITY);
    turbidityV = turbidityRead * (5.0 / 1024.0);
    phValue = pH_avg();
    temp_sensor.requestTemperatures();
    temp_water = temp_sensor.getTempCByIndex(0);
  }

  // Send to Output Code
  /* pH Detector */
  if(phValue < 8){
    Serial.println("N_ACID");
    problem++;
  }else if(phValue > 9){
    Serial.println("N_ALKALINE");
    problem++;
  }

  /* Turbidity Dectector */
  if(turbidityV < 3.8){
    Serial.println("N_WATER");
    problem++;
  }

  /* Temperature Dectector */
  if(temp_water > 30){
    // RT = Reduce Temperature
    Serial.println("RT_WATER");
    problem++;
  }else if(temp_water < 25){
    // IT = Increase Temperature
    Serial.println("IT_WATER");
    problem++;
  }

  if(problem < 1){
    Serial.println("Normally")
  }
}
