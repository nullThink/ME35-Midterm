clear all;

load("MotorAt50.csv")
motorPosition = MotorAt50;
time = 0:0.005:99*0.005 - 0.005;
transferEstimate = tfestimate(time, motorPosition)