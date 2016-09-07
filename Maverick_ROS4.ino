// Serial test script
#include<MAVERICK.h>

char readString[100];

void setup()
{
   initialise();
  Serial.begin(9600);  // initialize serial communications at 9600 bps
 //delay(1500);
 clear_LCD();
 Serial3.print("Starting");
 delay(1000);
 clear_LCD();
}

int string_split(char input[],char *delimiter) //Used for parsing Serial. from PC
//int string_split(String input,char *delimiter)
/*Returns string split in global variable:
char str_split_result[20][15]; //20 strings of up to 15 characters each
first item is in str_split_result[0]
and value returned = number of strings split
*/

{
    char str_split_result[20][15];
    char *token;
    int n=0;
    int sr;
    double spd; //speed is reserved
    int led1,led2,led3;
    token=strtok(input,delimiter);
    while (token!=NULL)
    {
        strcpy(str_split_result[n],token);
        n++;
        token=strtok(NULL,delimiter);
    }
    //if n>...
  sr=(int)strtol(str_split_result[0],NULL,0);
  spd=strtod(str_split_result[1],NULL);
  led1=(int)strtol(str_split_result[2],NULL,0);
  led2=(int)strtol(str_split_result[3],NULL,0);
  led3=(int)strtol(str_split_result[4],NULL,0);

  if (led1==0) led_out(1,LOW);else led_out(1,HIGH);
  if (led2==0) led_out(2,LOW);else led_out(2,HIGH);
  if (led3==0) led_out(3,LOW);else led_out(3,HIGH);
  clear_LCD();
  Serial3.print("Cmd:");Serial3.print(sr);
  Serial3.print(',');Serial3.print(spd);
  steer(sr);
  drive(spd);
    return n;
}


char c;
int pos;
int reading;
double lt,ln;
int br;
void l2oop()
{
  //This is a main loop but is only passive and sends the lat long, bearing each second to the serial port
  Serial.flush();
  lt=get_lat();
  ln=get_lon();
  br=read_compass();
  Serial3.print(br);
  Serial.print(lt,6);Serial.print(",");Serial.print(ln,6);Serial.print(",");Serial.print(br);Serial.print("\n");
  delay(1000);
  clear_LCD();
}
void loop()
{
  pos=0;
  c=0;
  reading=0;
  while(!Serial.available()) {}
  // serial read section
  while ((Serial.available())&&(c!='$')) c = Serial.read();  //String starts with $...steer,speed..ends with a ... :
  led_out(3,HIGH);
  reading=1;pos=0;
  while (c!=':')
  {
    if (Serial.available() >0)
    {
       c = Serial.read();  //gets one byte from serial buffer
     // if (c=='$') {reading=1;pos=0;}
     
      if ((c!=':')&&(c!='$')) {readString[pos] = c; pos++;}//makes the string readString
     
    }
  }
  readString[pos]='\0';
  //Serial3.print(pos);
  //delay(500);
  if (pos>0)
  {
   
  // delay(1000);
   led_out(3,LOW);
    int n=string_split(readString,",");
  }

  Serial.flush();
  lt=get_lat();
  ln=get_lon();
  br=read_compass();
  //Serial.print("%8.6f,%8.6f,%d",lt,ln,br);
  Serial.print(lt,6);Serial.print(",");Serial.print(ln,6);Serial.print(",");Serial.print(br);Serial.print("\n");
   //write("%f,%f,%d\n",lt,ln,br);

}
