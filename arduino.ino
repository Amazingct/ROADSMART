char t;
int Speed = 255;
void setup() {
pinMode(3,OUTPUT);   //left motors forward
pinMode(4,OUTPUT);   //left motors reverse
pinMode(5,OUTPUT);   //right motors forward
pinMode(6,OUTPUT);   //right motors reverse
//FOR SPEED CONTROL
pinMode(7, OUTPUT);
pinMode(8, OUTPUT);
//leds
pinMode(13,OUTPUT);   //Led
pinMode(14,OUTPUT);   //Led
pinMode(15,OUTPUT);   //Led
Serial.begin(115200);

//turn off RGB leds
digitalWrite(13,HIGH);
digitalWrite(14,HIGH);
digitalWrite(15,HIGH);
//set speed

}

void loop()
{
analogWrite(7,Speed);
analogWrite(8,Speed);


if(Serial.available())

{
  t = Serial.read();


  if(t == 'w')
  {            //move forward(all motors rotate in forward direction)
  digitalWrite(3,LOW);
  digitalWrite(4,HIGH);

  digitalWrite(5,LOW);
  digitalWrite(6,HIGH);
  }

  else if(t == 'z')
  {      //move reverse (all motors rotate in reverse direction)
  digitalWrite(3,HIGH);
  digitalWrite(4,LOW);
  digitalWrite(5,HIGH);
  digitalWrite(6,LOW);
    digitalWrite(13,HIGH);
  digitalWrite(14,HIGH);
  digitalWrite(15,LOW);
  }

  else if(t == 'd')
  {      //turn right (left side motors rotate in forward direction, right side motors doesn't rotate)
  digitalWrite(3,LOW);
  digitalWrite(4,HIGH);
  digitalWrite(5,LOW);
  digitalWrite(6,LOW);
    digitalWrite(13,HIGH);
  digitalWrite(14,LOW);
  digitalWrite(15,HIGH);

  }

  else if(t == 'a')
  {      //turn left (right side motors rotate in forward direction, left side motors doesn't rotate)
  digitalWrite(3,LOW);
  digitalWrite(4,LOW);
  digitalWrite(5,LOW);
  digitalWrite(6,HIGH);
  digitalWrite(13,LOW);
  digitalWrite(14,HIGH);
  digitalWrite(15,HIGH);
  }

  else if(t == 's')
  {      //STOP (all motors stop)
  digitalWrite(3,LOW);
  digitalWrite(4,LOW);
  digitalWrite(5,LOW);
  digitalWrite(6,LOW);
  digitalWrite(13,HIGH);
  digitalWrite(14,HIGH);
  digitalWrite(15,HIGH);
  }


//speed control

  else if(t == 'h')
  {
  Speed += 5;
  }

  else if(t == 'l')
  {
  Speed -= 5;
  }
//limit speed to range of 100 - 255
  if (Speed>=225)
  {
  Speed = 255;
  }

  if (Speed<=100)
  {
  Speed = 100;
  }

}
}