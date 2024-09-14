% HopHacks
% Author: Christian Galvez
% Script for simple data modeling (three_factor)

clc

u = sign(randn(200,2)) % 2 inputs
y = randn(200,1); % 1 output
ts = 0.1; % Sample time

z.u = u;
z.y = y;
z.ts = ts;

figure;
plot(z.u(:,1));
title('First Input');
xlabel('Sample');
ylabel('Amplitude');

disp('Data properties:');
disp(['Number of samples: '
  num2str(size(z.y, 1))]);
disp(['Number of outputs: '
  num2str(size(z.y, 2))]);
disp(['Number of inputs: '
  num2str(size(z.u, 2))]);
