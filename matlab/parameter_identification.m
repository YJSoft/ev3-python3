

clear all;

get_exp_data % execute the other script


% set up function
f = @(x) residual(x(1),x(2),x(3),x(4),x(5),exp_data);

x0 = [0;0;0;0;0];

A = [ -1 0 0 0 0; 0 -1 0 0 0];
b = [ 0 ; 0 ];

% use fmincon without constraints
[x,fval] = fmincon(f,x0,A,b);

c_1 = x(1); % g/r
c_r = x(2); % friction
omega0 = x(3);
alpha0 = x(4);
bias = x(5);

fprintf('solution found! (error = %f)\n',fval);
fprintf(' c_1     = %f\n',c_1);
fprintf(' c_r     = %f\n',c_r);
fprintf(' omega_0 = %f\n',omega0);
fprintf(' alpha_0 = %f\n',alpha0);
fprintf(' bias    = %f\n',bias);


% plot experimental data
figure(1);
plot(exp_data(:,3),exp_data(:,1:2));

% do simulation with the identified parameters
simulation;


time_offset = exp_data(1,3);
% plot
figure(2);
plot(times+time_offset,q_data);

figure(3);
plot(times+time_offset,q_data(:,1),exp_data(:,3),bias+exp_data(:,1),'+');

figure(4);
plot(times+time_offset,q_data(:,2),exp_data(:,3),bias*exp_data(:,3)+exp_data(:,2),'+');
