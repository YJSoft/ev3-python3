

% open file and read data into matrix A
file = fopen('../ergebnisse.txt','r');
A=fscanf(file,'%d %d %f',[3 Inf ]);
fclose(file);
A=A';

rates = A(:,2);
angles= A(:,1);
times = A(:,3);

max_time=20;

data_points = size(A,1);
n = data_points;

% scale data, use radians instead of degrees
angles = (pi/180)*angles;
rates = (pi/180)*rates;

% calculate integral of rate
integrated = zeros(n,1);
integrated(1)= angles(1);
for i=2:n
	integrated(i)=integrated(i-1)+rates(i)*(times(i)-times(i-1));
end

% prepare data:
% search for most extreme index as a starting point
[m,max_index] = max(abs(rates));

start_index = max_index;
i1 = start_index;

% get index set
end_index = max(find(times <= max_time));
i2 = end_index;

exp_data=[rates(i1:i2) angles(i1:i2) times(i1:i2)];






