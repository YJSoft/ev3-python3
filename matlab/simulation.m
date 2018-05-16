


% setze schrittweite
h = 0.1^3;

duration=20;

n = floor(duration/h);


% setze startwerte
q0 = [ 0.0  pi/2 ];

% setze konstanten
g = 9.81;
r = 1;
c_r = 0.2;


q_data = zeros(n, 2);


% setze q0 ein
q_data(1,1) = q0(1);
q_data(1,2) = q0(2);

for i=2:n
	% q(t+h) = q'*h + q(t)
	% lade q(t)
	old_q = q_data(i-1,:);
	omega = old_q(1);
	alpha = old_q(2);

	% berechne q't()
	q_derivative = [ -(g/r)* sin(alpha) - c_r * omega  omega ];

	new_q = q_derivative*h + old_q;

	q_data(i,:) = new_q;

end

times = h*(1:n) - h;

