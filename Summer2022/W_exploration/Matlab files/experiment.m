syms a b t real

coeff = readmatrix('Stokes.csv');

ii = 1;
ix = coeff(2,1);
iy = coeff(3,1);
iz = coeff(4,1);
xi = coeff(5,1);
xx = coeff(6,1);
xy = coeff(7,1);
xz = coeff(8,1);
yi = coeff(9,1);
yx = coeff(10,1);
yy = coeff(11,1);
yz = coeff(12,1);
zi = coeff(13,1);
zx = coeff(14,1);
zy = coeff(15,1);
zz = coeff(16,1);

W1 = 1/4*(ii+zz+((cos(t))^2-(sin(t))^2)*(xx+yy)+2*sin(t)*cos(t)*(zi+iz));
W2 = 1/4*(ii-zz+((cos(t))^2-(sin(t))^2)*(xx-yy)-2*sin(t)*cos(t)*(zi-iz));
W3 = 1/4*(ii+xx+((cos(t))^2-(sin(t))^2)*(zz+yy)+2*sin(t)*cos(t)*(xi+ix));
W4 = 1/4*(ii-xx+((cos(t))^2-(sin(t))^2)*(zz-yy)-2*sin(t)*cos(t)*(xi-ix));
W5 = 1/4*(ii+yy+((cos(t))^2-(sin(t))^2)*(zz+xx)+2*sin(t)*cos(t)*(yi+iy));
W6 = 1/4*(ii-yy+((cos(t))^2-(sin(t))^2)*(zz-xx)-2*sin(t)*cos(t)*(yi-iy));

W1p = 1/4*(ii+zz+((cos(t))^2-(sin(t))^2)*(xx+yy)+2*sin(t)*cos(t)*cos(a)*(zi+iz)+2*sin(t)*cos(t)*sin(a)*(xy-yx));
W2p = 1/4*(ii-zz+((cos(t))^2-(sin(t))^2)*(xx-yy)+2*sin(t)*cos(t)*cos(a)*(zi-iz)-2*sin(t)*cos(t)*sin(a)*(xy+yx));
W3p = 1/4*((cos(t))^2*(ii+zz)+(sin(t))^2*(ii-zz)+(cos(t))^2*cos(b)*(xx+yy)...
    +(sin(t))^2*cos(2*a-b)*(xx-yy)+2*sin(t)*cos(t)*cos(a)*xi+2*sin(t)*cos(t)*cos(a-b)*ix...
    +2*sin(t)*cos(t)*sin(a)*yi+2*sin(t)*cos(t)*sin(a-b)*iy+(cos(t))^2*sin(b)*(yx-xy)...
    +(sin(t))^2*sin(2*a-b)*(yx+xy));
W4p = 1/4*(ii+xx+((cos(t))^2-(sin(t))^2)*(zz+yy)+2*sin(t)*cos(t)*cos(a)*(ix+xi)+2*sin(t)*cos(t)*sin(a)*(yz-zy));
W5p = 1/4*(ii-xx+((cos(t))^2-(sin(t))^2)*(zz-yy)+2*sin(t)*cos(t)*cos(a)*(ix-xi)-2*sin(t)*cos(t)*sin(a)*(yz+zy));
W6p = 1/4*((cos(t))^2*(cos(a))^2*(ii+zz+zi+iz)+(cos(t))^2*(sin(a))^2*(ii-zz+zi-iz) ...
    +(sin(t))^2*(cos(b))^2*(ii+zz-zi-iz)+(sin(t))^2*(sin(b))^2*(ii-zz-zi+iz)...
    +2*sin(t)*cos(t)*cos(a)*cos(b)*(xx+yy)+2*sin(t)*cos(t)*sin(a)*sin(b)*(xx-yy)...
    +2*sin(t)*cos(t)*cos(a)*sin(b)*(yz+yi)+2*sin(t)*cos(t)*sin(a)*cos(b)*(yz-yi)...
    -(cos(t))^2*2*sin(a)*cos(a)*(zy+iy)-(sin(t))^2*2*sin(b)*cos(b)*(zy-iy));
W7p = 1/4*(ii+yy+((cos(t))^2-(sin(t))^2)*(zz+xx)+2*sin(t)*cos(t)*cos(a)*(zx-xz)-2*sin(t)*cos(t)*sin(a)*(yi+iy));
W8p = 1/4*(ii-yy+((cos(t))^2-(sin(t))^2)*(zz-xx)+2*sin(t)*cos(t)*cos(a)*(zx+xz)+2*sin(t)*cos(t)*sin(a)*(yi-iy));
W9p = 1/4*((cos(t))^2*(cos(a))^2*(ii+zz+zi+iz)+(cos(t))^2*(sin(a))^2*(ii-zz+zi-iz) ...
    +(sin(t))^2*(cos(b))^2*(ii+zz-zi-iz)+(sin(t))^2*(sin(b))^2*(ii-zz-zi+iz)...
    +2*sin(t)*cos(t)*cos(a)*cos(b)*(xx+yy)+2*sin(t)*cos(t)*sin(a)*sin(b)*(xx-yy)...
    +(cos(t))^2*2*sin(a)*cos(a)*(ix+zx)+(sin(t))^2*2*sin(b)*cos(b)*(ix-zx)...
    +2*sin(t)*cos(t)*cos(a)*sin(b)*(xi+xz)+2*sin(t)*cos(t)*sin(a)*cos(b)*(xi-xz));

T = cat(1,W1,W2,W3,W4,W5,W6);
Tp = cat(1,T1p,T2p,T3p,T4p,T5p,T6p,T7p,T8p,T9p);
result = zeros(9,2);

for i = 0:5
    W = T(4*i+1:4*i+4,:);
    f = matlabFunction(real(trace(W*rho)));
    if contains(char(f),'t')
        [~,fval] = fminbnd(f,0,pi);
    else
        fval = trace(W*rho);
    end
    
    if abs(fval) < 1e-5
        fval = 0;
    end

    result(i+1,1) = fval;
end

for i = 0:8
    W = Tp(4*i+1:4*i+4,:);
    f = matlabFunction(real(trace(W*rho)));
    if contains(char(f),'a') && contains(char(f),'b')
        x0 = [0,0,0];
        [~, fval] = fminsearch(@(x)f(x(1),x(2),x(3)), x0);
    elseif contains(char(f),'a') || contains(char(f),'b')
        x0 = [0,0];
        [~, fval] = fminsearch(@(x)f(x(1),x(2)), x0);
    elseif contains(char(f),'t')
        [~,fval] = fminbnd(f,0,pi);
    else
        fval = trace(W*rho);
    end
    
    if abs(fval) < 1e-5
        fval = 0;
    end

    result(i+1,2) = fval;
end

result