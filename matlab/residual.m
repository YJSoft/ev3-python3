function err = residual(c_1,c_r,omega0,alpha0,bias,exp_data)

h = 0.1^3;
beta = 0.1;


q0 = [ omega0 alpha0 ];
old_q = q0;


n=size(exp_data,1);

err = 0.0;

first_time_diff = exp_data(2,3)-exp_data(1,3);
err = first_time_diff*(exp_data(1,1)-omega0)^2;


for i = 2:n
	timediff = exp_data(i,3)-exp_data(i-1,3);
	n2 = floor(timediff/h);
	h2 = timediff/n2;
	for j = 1:n2
		omega = old_q(1);
		alpha = old_q(2);
		q_derivative = [ - c_1* sin(alpha) - c_r * omega  omega ];
		new_q = q_derivative*h2 + old_q;
		old_q = new_q;
	end
	err = err + timediff* ( (bias + exp_data(i,1) - old_q(1))^2 );

end




end
