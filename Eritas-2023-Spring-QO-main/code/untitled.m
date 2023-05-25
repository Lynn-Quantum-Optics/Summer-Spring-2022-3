syms r1 r2 r3 r4 real
vars;
M11 = r1;
M22 = r2*(1-r1);
M33 = r3*(1-M11-M22);
M44 = r4*(1-M11-M22-M33);

dia = [M11 M22 M33 M44];
dia = dia(1,randperm(4));

M = diag(dia);

syms e1 e2 e3 e4 e5 e6 a1 a2 a3 a4 a5 a6 b1 b2 b3 b4 b5 b6 real
K1 = [1 0 0 0; 0 1 0 0; 0 0 exp(1i*(e1+a1)) exp(1i*(e1+b1)); 0 0 -exp(1i*(e1-b1)) exp(1i*(e1-a1))];
K2 = [1 0 0 0; 0 exp(1i*(e2+a2)) exp(1i*(e2+b2)) 0; 0 -exp(1i*(e2-b2)) exp(1i*(e2-a2)) 0; 0 0 0 1];
K3 = [exp(1i*(e3+a3)) exp(1i*(e3+b3)) 0 0; -exp(1i*(e3-b3)) exp(1i*(e3-a3)) 0 0; 0 0 1 0; 0 0 0 1];
K4 = [1 0 0 0; 0 1 0 0; 0 0 exp(1i*(e4+a4)) exp(1i*(e4+b4)); 0 0 -exp(1i*(e4-b4)) exp(1i*(e4-a4))];
K5 = [1 0 0 0; 0 exp(1i*(e5+a5)) exp(1i*(e5+b5)) 0; 0 -exp(1i*(e5-b5)) exp(1i*(e5-a5)) 0; 0 0 0 1];
K6 = [1 0 0 0; 0 1 0 0; 0 0 exp(1i*(e6+a6)) exp(1i*(e6+b6)); 0 0 -exp(1i*(e6-b6)) exp(1i*(e6-a6))];

K = K1*K2*K3*K4*K5*K6;

rho = K*M*K';

p_xx = trace(xx*rho)
p_yy = trace(yy*rho)
p_zz = trace(zz*rho)
p_ix = trace(ix*rho)
p_xi = trace(xi*rho)
p_iy = trace(iy*rho)
p_yi = trace(yi*rho)
p_iz = trace(iz*rho)
p_zi = trace(zi*rho)