function rho = pure_state()

r = rand(1,4);
r1 = r(1,1);
r2 = r(1,2)*(1-r1);
r3 = r(1,3)*(1-r1-r2);
r4 = r(1,4)*(1-r1-r2-r3);

ind1 = sqrt(r1);
ind2 = sqrt(r2)*exp(1i*unifrnd(0,2*pi));
ind3 = sqrt(r3)*exp(1i*unifrnd(0,2*pi));
ind4 = sqrt(r4)*exp(1i*unifrnd(0,2*pi));

entry = [ind1;ind2;ind3;ind4] / sqrt(r1+r2+r3+r4);
psi = entry(randperm(4),1);
rho = psi*psi';

end