clear all;

% Get Points
timeRanges = linspace(0, pi, 100);

yPoints = sin(timeRanges) - 16;
xPoints = (-2.5*cos(timeRanges))+2.5;

yPoints(1, 101:200) = -20;
xPoints(1, 101:200) = linspace(5, 0, 100);

offsetZeros = zeros(1,200);
trajectory = [offsetZeros' xPoints' yPoints'];
timeRanges(101:200) = linspace(pi, 2*pi, 100);

% figure(1);
% subplot(3,1,1);
% plot(timeRanges, xPoints);
% xlabel("Time")
% ylabel("X Position")
% subplot(3,1,2);
% plot(timeRanges, yPoints);
% xlabel("Time")
% ylabel("Y Position")
% subplot(3,1,3);
% plot(xPoints, yPoints);
% xlabel("X Position")
% ylabel("Y Position")
% xlim([-2.5, 7.5])

% Build Robot Sim
kneeLeg = rigidBody("kneeLeg");
hipLeg = rigidBody("hipLeg");

hipLeg.Joint = rigidBodyJoint("hipJoint", "revolute");
kneeLeg.Joint = rigidBodyJoint("kneeJoint", "revolute");

hipLeg.Joint.JointAxis = [1 0 0];
kneeLeg.Joint.JointAxis = [1 0 0];

arm = rigidBodyTree;
setFixedTransform(hipLeg.Joint, trvec2tform([0 0 -7]));
setFixedTransform(kneeLeg.Joint, trvec2tform([0 0 -13]));

addBody(arm, hipLeg, "base")
addBody(arm, kneeLeg, "hipLeg")
show(arm)

% Perform IK

% Assuming joints rotate along X axis, and movement is along Y and Z axis

iK = inverseKinematics('RigidBodyTree', arm);

anglesHip = [];
anglesKnee = [];

for pointIndex = 1:length(trajectory)
    transform = trvec2tform(trajectory(pointIndex, :));
    
    weight = [1 1 1 1 1 1];
    initGuess = arm.homeConfiguration;
    [configSol, solnInfo] = iK("kneeLeg", transform, weight, initGuess);
    currentConfig = configSol;
    anglesHip(pointIndex)= configSol(1).JointPosition;
    anglesKnee(pointIndex)=configSol(2).JointPosition;
end

% Convert Radians to Degrees
anglesHip = anglesHip * (180 / pi)
anglesKnee = anglesKnee * (180/pi)

% Concatenate Angle Data
angles = [anglesHip' anglesKnee'];