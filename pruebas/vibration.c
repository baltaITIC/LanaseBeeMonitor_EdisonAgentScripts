void main() {
    int HIGH=1;
    int LOW=0;
    int sensorState = digitalRead(2);
    //Serial.println(sensorState);
    delay(1000);
    print(sensorState);
    /*if(sensorState == HIGH)
    {
        digitalWrite(ledPin,HIGH);
    }
    else
    {
        digitalWrite(ledPin,LOW);
    }*/
}
