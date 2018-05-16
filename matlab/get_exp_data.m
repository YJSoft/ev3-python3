

% open file and read data into matrix A
file = fopen('../ergebnisse.txt','r');
A=fscanf(file,'%d %d %f',[3 Inf ]);
fclose(file);
A=A';

rates = A(:,2);
angles= A(:,1);
times = A(:,3);

data_points = size(A,1);
n = data_points;

% calculate integral of rate
integrated = zeros(n,1);
integrated(1)= angles(1);
for i=2:n
	integrated(i)=integrated(i-1)+rates(i)*(times(i)-times(i-1));
end






