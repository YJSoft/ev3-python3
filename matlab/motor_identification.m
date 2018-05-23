


file = fopen('../ergebnisse_wheelposition.txt','r');
A=fscanf(file,'%f %d %d', [3 Inf ]);
fclose(file);

A=A';

w1=A(:,2);
w2=A(:,3);
times=A(:,1);

w1 = w1-w1(1);
w2 = w2-w2(1);

w2 = -w2;

times = times-times(1);

exp_data=[times w1 w2];

residual_motor(0.3,200,10,exp_data)


