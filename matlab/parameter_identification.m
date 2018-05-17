

clear all;

get_exp_data % execute the other script


% set up function
f = @(x) residual(x(1),x(2),x(3),x(4),exp_data);

x0 = [0;0;0;0];

% use fmincon without constraints
[x,fval] = fmincon(f,x0,[],[]);

c_1 = x(1); % g/r
c_r = x(2); % friction
omega0 = x(3);
alpha0 = x(4);

fprintf('solution found! (error = %f)\n',fval);
fprintf(' c_1     = %f\n',c_1);
fprintf(' c_r     = %f\n',c_r);
fprintf(' omega_0 = %f\n',omega0);
fprintf(' alpha_0 = %f\n',alpha0);


% plot experimental data
figure(1);
plot(exp_data(:,3),exp_data(:,1:2));

% do simulation with the identified parameters
simulation;

% plot
figure(2);
plot(times,q_data);
