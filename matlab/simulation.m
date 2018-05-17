


% setze schrittweite
h = 0.1^3;

duration=20;

n = floor(duration/h);


% setze startwerte
% q0 = [ 0.0  pi/2 ];

if exist('alpha0') && exist('omega0')
	q0 = [ omega0 alpha0 ];
end

% setze konstanten
g = 9.81;
r = .5;

if ~exist('c_1')
	c_1 = g/r;
end

if ~exist('c_r')
	c_r = 0.4045;
end


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
	q_derivative = [ -c_1* sin(alpha) - c_r * omega  omega ];

	new_q = q_derivative*h + old_q;

	q_data(i,:) = new_q;

end

times = h*(1:n) - h;

