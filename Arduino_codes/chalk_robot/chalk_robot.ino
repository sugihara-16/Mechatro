#include <ros.h>
#include <geometry_msgs/Twist.h>
#include <Servo.h>

#define MOTOR_PIN1 5 // digital pinのIDを設定
#define MOTOR_PIN2 6
#define MOTOR_PIN3 7
#define MOTOR_PIN4 8

Servo groveServo;
ros::NodeHandle nh;
int dc_rpm = 0;
int dc_count=0;
int stepping_switch;
int servo_degree = 10;
int servo_count = 0;

const float step_period = 3; // step入力の時間幅 [msec]
const int MOTOR_PINS[4] = {5, 6, 7, 8};
const int SERVO_PIN = 4;
const int PULSES[4][4] = {
    {HIGH, LOW, LOW, HIGH},
    {HIGH, HIGH, LOW, LOW},
    {LOW, HIGH, HIGH, LOW},
    {LOW, LOW, HIGH, HIGH}
};
const int MOTOR_PWM = 3;
double v = 64;
int dir = 1;

void messageCb(const geometry_msgs::Twist& twist) {
  //dcモータ回転数取得
  dc_rpm = int( twist.linear.y);
  //ステッピングモータ回転数取得
  stepping_switch = int( twist.angular.z);
  char buf[100];
  sprintf(buf, "dc_rpm = %d", dc_rpm);
  nh.loginfo(buf);
  sprintf(buf, "stepping_switch = %d", stepping_switch);
  nh.loginfo(buf);
  
  //発射台回転
  if( stepping_switch == 1){
    nh.loginfo("positive_rotation");
    for(int k=0; k<10; k++){
      for(int i=0; i<4; i++){
        for(int j=0; j<4; j++){
          digitalWrite(MOTOR_PINS[j], PULSES[i][j]);
        }
      delay(step_period);
      }
    }
  }
  if( stepping_switch ==-1){
    nh.loginfo("negative_rotation");
    for(int k = 0; k<10; k++){
      for(int i=3; 0<=i; i--){
        for(int j=0; j<4; j++){
          digitalWrite(MOTOR_PINS[j], PULSES[i][j]);
        } 
      delay(step_period);
      }
    }
  }
}

ros::Subscriber<geometry_msgs::Twist> sub("cmd_vel", &messageCb);

void setup() {
  nh.getHardware()->setBaud(115200);
  nh.initNode();
  nh.subscribe(sub);
  groveServo.attach(SERVO_PIN);
  groveServo.write(servo_degree);
  for(int i =0; i<4; i++){
    pinMode(MOTOR_PINS[i], OUTPUT);
  }
  pinMode(MOTOR_PWM, OUTPUT);
}

void loop() {
  nh.spinOnce();
  analogWrite(MOTOR_PWM, constrain(dc_rpm,0,255));
  if( dc_rpm != 0){
    dc_count ++;
  }else{
    dc_count = 0;
  }
  if( dc_count > 6000){
    groveServo.write(160);
    delay(300);
    groveServo.write(10);
    delay(300);
  }
  
  delay(1);
  //以下に制御命令記述
  servo_count ++;
  
}
