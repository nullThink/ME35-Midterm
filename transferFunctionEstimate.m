clear all;
load("motorsv502.mat")

time = motorsv502(1, :);
adjustedAngle = motorsv502(2, :);
currentAngle = [0, adjustedAngle(1:length(adjustedAngle) -1)]

deltaTheta = adjustedAngle - currentAngle;

% Voltage of Motor = Kp(desiredAngle - actualAngle)
voltage = 50 * deltaTheta;

% Plot the data points
scatter(time, adjustedAngle)

% V = Ax'' + Bx'; V = Kp(angleAdjustment)

% Quadratic Part: Ax'' = V, assume B is negligible
% x'' = V/A; x' = (V/A) t + C1; x = (V/A)t^2 + C1t + C2
% theta(t) = V/A * t^2

A_estimateThetaT = (voltage .* time.^2);
A_estimate = A_estimateThetaT / adjustedAngle

% Linear Part: Bx' = V, assume A is negligible
B_estimateThetaT = (voltage .* time);
B_estimate = B_estimateThetaT / adjustedAngle

%% Find response function and plot to find damping Kp values
syms s t
Kp = 0.1;
A = 0.0046;
B = 0.098;

estimatedTF(s) = Kp / ((A*(s^2))+(B*s) + Kp);
responseFunction(t) = ilaplace(estimatedTF);

figure(2)
fplot(responseFunction, [0, 1])
xline(0)
yline(0)

