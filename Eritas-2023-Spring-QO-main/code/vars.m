phiP = 1/sqrt(2)*[1;0;0;1];
phiM = 1/sqrt(2)*[1;0;0;-1];
psiP = 1/sqrt(2)*[0;1;1;0];
psiM = 1/sqrt(2)*[0;1;-1;0];

syms a b t real

% % Test cases
% t1 = 1/sqrt(2)*(psiP + exp(1i*a)*psiM);
% t2 = 1/sqrt(2)*(phiP + exp(1i*a)*phiM);
% t3 = 1/sqrt(2)*(phiM + exp(1i*a)*psiM);
% t4 = 1/sqrt(2)*(phiP + exp(1i*a)*psiP);
% t5 = 1/sqrt(2)*(phiP + exp(1i*a)*psiM);
% t6 = 1/sqrt(2)*(phiM + exp(1i*a)*psiP);

% Pauli Tensor
sig0 = [1 0;0 1];
sig1 = [0 1;1 0];
sig2 = [0 -1i;1i 0];
sig3 = [1 0;0 -1];

ii = kron(sig0,sig0);
ix = kron(sig0,sig1);
iy = kron(sig0,sig2);
iz = kron(sig0,sig3);
xi = kron(sig1,sig0);
xx = kron(sig1,sig1);
xy = kron(sig1,sig2);
xz = kron(sig1,sig3);
yi = kron(sig2,sig0);
yx = kron(sig2,sig1);
yy = kron(sig2,sig2);
yz = kron(sig2,sig3);
zi = kron(sig3,sig0);
zx = kron(sig3,sig1);
zy = kron(sig3,sig2);
zz = kron(sig3,sig3);


sig = [0 0 0 -1;0 0 1 0;0 1 0 0;-1 0 0 0];

% _x -> _x,     _y -> _z,       _z -> -_y
% 
% W1 = 1/4*(ii-zy+((cos(t))^2-(sin(t))^2)*(xx+yz)+2*sin(t)*cos(t)*(zi-iy));
% W2 = 1/4*(ii+zy+((cos(t))^2-(sin(t))^2)*(xx-yz)-2*sin(t)*cos(t)*(zi+iy));
% W3 = 1/4*(ii+xx+((cos(t))^2-(sin(t))^2)*(-zy+yz)+2*sin(t)*cos(t)*(xi+ix));
% W4 = 1/4*(ii-xx+((cos(t))^2-(sin(t))^2)*(-zy-yz)-2*sin(t)*cos(t)*(xi-ix));
% W5 = 1/4*(ii+yz+((cos(t))^2-(sin(t))^2)*(-zy+xx)+2*sin(t)*cos(t)*(yi+iz));
% W6 = 1/4*(ii-yz+((cos(t))^2-(sin(t))^2)*(-zy-xx)-2*sin(t)*cos(t)*(yi-iz));
% 
% W1p = 1/4*(ii-zy+((cos(t))^2-(sin(t))^2)*(xx+yz)+2*sin(t)*cos(t)*cos(a)*(zi-iy)+2*sin(t)*cos(t)*sin(a)*(xz-yx));
% W2p = 1/4*(ii+zy+((cos(t))^2-(sin(t))^2)*(xx-yz)+2*sin(t)*cos(t)*cos(a)*(zi+iy)-2*sin(t)*cos(t)*sin(a)*(xz+yx));
% W3p = 1/4*((cos(t))^2*(ii-zy)+(sin(t))^2*(ii+zy)+(cos(t))^2*cos(b)*(xx+yz)...
%     +(sin(t))^2*cos(2*a-b)*(xx-yz)+2*sin(t)*cos(t)*cos(a)*xi+2*sin(t)*cos(t)*cos(a-b)*ix...
%     +2*sin(t)*cos(t)*sin(a)*yi+2*sin(t)*cos(t)*sin(a-b)*iz+(cos(t))^2*sin(b)*(yx-xz)...
%     +(sin(t))^2*sin(2*a-b)*(yx+xz));
% W4p = 1/4*(ii+xx+((cos(t))^2-(sin(t))^2)*(-zy+yz)+2*sin(t)*cos(t)*cos(a)*(ix+xi)+2*sin(t)*cos(t)*sin(a)*(-yy-zz));
% W5p = 1/4*(ii-xx+((cos(t))^2-(sin(t))^2)*(-zy-yz)+2*sin(t)*cos(t)*cos(a)*(ix-xi)-2*sin(t)*cos(t)*sin(a)*(-yy+zz));
% W6p = 1/4*((cos(t))^2*(cos(a))^2*(ii-zy+zi-iy)+(cos(t))^2*(sin(a))^2*(ii+zy+zi+iy) ...
%     +(sin(t))^2*(cos(b))^2*(ii-zy-zi+iy)+(sin(t))^2*(sin(b))^2*(ii+zy-zi-iy)...
%     +2*sin(t)*cos(t)*cos(a)*cos(b)*(xx+yz)+2*sin(t)*cos(t)*sin(a)*sin(b)*(xx-yz)...
%     +2*sin(t)*cos(t)*cos(a)*sin(b)*(-yy+yi)+2*sin(t)*cos(t)*sin(a)*cos(b)*(-yy-yi)...
%     -(cos(t))^2*2*sin(a)*cos(a)*(zz+iz)-(sin(t))^2*2*sin(b)*cos(b)*(zz-iz));
% W7p = 1/4*(ii+yz+((cos(t))^2-(sin(t))^2)*(-zy+xx)+2*sin(t)*cos(t)*cos(a)*(zx+xy)-2*sin(t)*cos(t)*sin(a)*(yi+iz));
% W8p = 1/4*(ii-yz+((cos(t))^2-(sin(t))^2)*(-zy-xx)+2*sin(t)*cos(t)*cos(a)*(zx-xy)+2*sin(t)*cos(t)*sin(a)*(yi-iz));
% W9p = 1/4*((cos(t))^2*(cos(a))^2*(ii-zy+zi-iy)+(cos(t))^2*(sin(a))^2*(ii+zy+zi+iy) ...
%     +(sin(t))^2*(cos(b))^2*(ii-zy-zi+iy)+(sin(t))^2*(sin(b))^2*(ii+zy-zi-iy)...
%     +2*sin(t)*cos(t)*cos(a)*cos(b)*(xx+yz)+2*sin(t)*cos(t)*sin(a)*sin(b)*(xx-yz)...
%     +(cos(t))^2*2*sin(a)*cos(a)*(ix+zx)+(sin(t))^2*2*sin(b)*cos(b)*(ix-zx)...
%     +2*sin(t)*cos(t)*cos(a)*sin(b)*(xi-xy)+2*sin(t)*cos(t)*sin(a)*cos(b)*(xi+xy));

% % _x -> -_z,     _y -> _y,       _z -> _x
% W1 = 1/4*(ii+zx+((cos(t))^2-(sin(t))^2)*(-xz+yy)+2*sin(t)*cos(t)*(zi+ix));
% W2 = 1/4*(ii-zx+((cos(t))^2-(sin(t))^2)*(-xz-yy)-2*sin(t)*cos(t)*(zi-ix));
% W3 = 1/4*(ii-xz+((cos(t))^2-(sin(t))^2)*(zx+yy)+2*sin(t)*cos(t)*(xi-iz));
% W4 = 1/4*(ii+xz+((cos(t))^2-(sin(t))^2)*(zx-yy)-2*sin(t)*cos(t)*(xi+iz));
% W5 = 1/4*(ii+yy+((cos(t))^2-(sin(t))^2)*(zx-xz)+2*sin(t)*cos(t)*(yi+iy));
% W6 = 1/4*(ii-yy+((cos(t))^2-(sin(t))^2)*(zx+xz)-2*sin(t)*cos(t)*(yi-iy));
% 
% W1p = 1/4*(ii+zx+((cos(t))^2-(sin(t))^2)*(-xz+yy)+2*sin(t)*cos(t)*cos(a)*(zi+ix)+2*sin(t)*cos(t)*sin(a)*(xy+yz));
% W2p = 1/4*(ii-zx+((cos(t))^2-(sin(t))^2)*(-xz-yy)+2*sin(t)*cos(t)*cos(a)*(zi-ix)-2*sin(t)*cos(t)*sin(a)*(xy-yz));
% W3p = 1/4*((cos(t))^2*(ii+zx)+(sin(t))^2*(ii-zx)+(cos(t))^2*cos(b)*(-xz+yy)...
%     +(sin(t))^2*cos(2*a-b)*(-xz-yy)+2*sin(t)*cos(t)*cos(a)*xi-2*sin(t)*cos(t)*cos(a-b)*iz...
%     +2*sin(t)*cos(t)*sin(a)*yi+2*sin(t)*cos(t)*sin(a-b)*iy+(cos(t))^2*sin(b)*(-yz-xy)...
%     +(sin(t))^2*sin(2*a-b)*(-yz+xy));
% W4p = 1/4*(ii-xz+((cos(t))^2-(sin(t))^2)*(zx+yy)+2*sin(t)*cos(t)*cos(a)*(-iz+xi)+2*sin(t)*cos(t)*sin(a)*(yx-zy));
% W5p = 1/4*(ii+xz+((cos(t))^2-(sin(t))^2)*(zx-yy)+2*sin(t)*cos(t)*cos(a)*(-iz-xi)-2*sin(t)*cos(t)*sin(a)*(yx+zy));
% W6p = 1/4*((cos(t))^2*(cos(a))^2*(ii+zx+zi+ix)+(cos(t))^2*(sin(a))^2*(ii-zx+zi-ix) ...
%     +(sin(t))^2*(cos(b))^2*(ii+zx-zi-ix)+(sin(t))^2*(sin(b))^2*(ii-zx-zi+ix)...
%     +2*sin(t)*cos(t)*cos(a)*cos(b)*(-xz+yy)+2*sin(t)*cos(t)*sin(a)*sin(b)*(-xz-yy)...
%     +2*sin(t)*cos(t)*cos(a)*sin(b)*(yx+yi)+2*sin(t)*cos(t)*sin(a)*cos(b)*(yx-yi)...
%     -(cos(t))^2*2*sin(a)*cos(a)*(zy+iy)-(sin(t))^2*2*sin(b)*cos(b)*(zy-iy));
% W7p = 1/4*(ii+yy+((cos(t))^2-(sin(t))^2)*(zx-xz)+2*sin(t)*cos(t)*cos(a)*(-zz-xx)-2*sin(t)*cos(t)*sin(a)*(yi+iy));
% W8p = 1/4*(ii-yy+((cos(t))^2-(sin(t))^2)*(zx+xz)+2*sin(t)*cos(t)*cos(a)*(-zz+xx)+2*sin(t)*cos(t)*sin(a)*(yi-iy));
% W9p = 1/4*((cos(t))^2*(cos(a))^2*(ii+zx+zi+ix)+(cos(t))^2*(sin(a))^2*(ii-zx+zi-ix) ...
%     +(sin(t))^2*(cos(b))^2*(ii+zx-zi-ix)+(sin(t))^2*(sin(b))^2*(ii-zx-zi+ix)...
%     +2*sin(t)*cos(t)*cos(a)*cos(b)*(-xz+yy)+2*sin(t)*cos(t)*sin(a)*sin(b)*(-xz-yy)...
%     +(cos(t))^2*2*sin(a)*cos(a)*(-iz-zz)+(sin(t))^2*2*sin(b)*cos(b)*(-iz+zz)...
%     +2*sin(t)*cos(t)*cos(a)*sin(b)*(xi+xx)+2*sin(t)*cos(t)*sin(a)*cos(b)*(xi-xx));

% --------------------- W ---------------------

P1 = cos(t)*phiP + sin(t)*phiM;
W1 = partialTrans(P1*P1');

P2 = cos(t)*psiP + sin(t)*psiM;
W2 = partialTrans(P2*P2');

P3 = cos(t)*phiP + sin(t)*psiP;
W3 = partialTrans(P3*P3');

P4 = cos(t)*phiM + sin(t)*psiM;
W4 = partialTrans(P4*P4');

P5 = cos(t)*phiP + 1i*sin(t)*psiM;
W5 = partialTrans(P5*P5');

P6 = cos(t)*phiM + 1i*sin(t)*psiP;
W6 = partialTrans(P6*P6');

% --------------------- W' ---------------------

% Pair 1
P1p = 1/sqrt(2)*[cos(t)+exp(1i*a)*sin(t);0;0;cos(t)-exp(1i*a)*sin(t)];
W1p = partialTrans(P1p*P1p');

P2p = 1/sqrt(2)*[0;cos(t)+exp(1i*a)*sin(t);cos(t)-exp(1i*a)*sin(t);0];
W2p = partialTrans(P2p*P2p');

P3p = 1/sqrt(2)*[cos(t);sin(t)*exp(1i*(b-a));sin(t)*exp(1i*a);cos(t)*exp(1i*b)];
W3p = partialTrans(P3p*P3p');

% Pair 2
P4p = 1/sqrt(2)*[cos(t);sin(t)*exp(1i*a);sin(t)*exp(1i*a);cos(t)];
W4p = partialTrans(P4p*P4p');

P5p = 1/sqrt(2)*[cos(t);sin(t)*exp(1i*a);-sin(t)*exp(1i*a);-cos(t)];
W5p = partialTrans(P5p*P5p');

P6p = [cos(t)*cos(a);1i*cos(t)*sin(a);1i*sin(t)*sin(b);sin(t)*cos(b)];
W6p = partialTrans(P6p*P6p');

% Pair 3
P7p = 1/sqrt(2)*[cos(t);sin(t)*exp(1i*a);-sin(t)*exp(1i*a);cos(t)];
W7p = partialTrans(P7p*P7p');

P8p = 1/sqrt(2)*[cos(t);sin(t)*exp(1i*a);sin(t)*exp(1i*a);-cos(t)];
W8p = partialTrans(P8p*P8p');

P9p = [cos(t)*cos(a);cos(t)*sin(a);sin(t)*sin(b);sin(t)*cos(b)];
W9p = partialTrans(P9p*P9p');