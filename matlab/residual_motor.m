function res = residual_motor(c1,c2,c3,exp_data)
% function res = residual_motor(c1,c2,c3,exp_data,plot)


% modell = 1

times=exp_data(:,1);

n=size(times,1);

% calculate fine time grid

t_x = c1;
v_x = c2;
v_0 = c3;

s_1_end = ((v_x-v_0)/(2*t_x)) * t_x^2 + v_0*t_x;

data=zeros(n,1);

for i=1:n
	t=times(i);
	s=0;
	if t<= t_x
		s=((v_x-v_0)/(2*t_x)) * t^2 + v_0*t;
	else
		s=v_x * (t-t_x) + s_1_end;
	end
	data(i)=s;
end


plot(times,data);


% modell = 2

% for i = 1:n



