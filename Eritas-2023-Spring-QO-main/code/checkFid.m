function [fid, maxFid, I] = checkFid(rho)

phiP = 1/sqrt(2)*[1;0;0;1];
phiM = 1/sqrt(2)*[1;0;0;-1];
psiP = 1/sqrt(2)*[0;1;1;0];
psiM = 1/sqrt(2)*[0;1;-1;0];

syms a1 a2 b t real
% Test cases
t1 = 1/sqrt(2)*(psiP + exp(1i*a1)*psiM);
t2 = 1/sqrt(2)*(phiP + exp(1i*a2)*phiM);
t3 = 1/sqrt(2)*(phiM + exp(1i*a1)*psiM);
t4 = 1/sqrt(2)*(phiP + exp(1i*a2)*psiP);
t5 = 1/sqrt(2)*(phiP + exp(1i*a1)*psiM);
t6 = 1/sqrt(2)*(phiM + exp(1i*a2)*psiP);

% superposition of orthogonal states
T1 = cos(t)*t1 + exp(1i*b)*sin(t)*t2;
T2 = cos(t)*t3 + exp(1i*b)*sin(t)*t4;
T3 = cos(t)*t5 + exp(1i*b)*sin(t)*t6;

% T = cat(1,t1,t2,t3,t4,t5,t6);
T = cat(1,T1,T2,T3);

% load('C:\Users\qiyan\Desktop\Fall 2022 QO\Fall 2022 QO Data\undetectedW_6566.mat')
% load('/home/qiyang/Downloads/theory/Data/undetectedW_6566.mat')  % lab computer

fid = zeros(3,1);
for m = 0:2
    test = T(4*m+1:4*m+4,:);
    nf = matlabFunction(real(-1*(test')*(rho*test)));
    
    % maximize w/ respect to a, b and t
    if contains(char(nf),'a1') && contains(char(nf),'a2') && contains(char(nf),'b') && contains(char(nf),'t')
        x0 = [0,0,0,0];
        [~, fmax] = fminsearch(@(x)nf(x(1),x(2),x(3),x(4)), x0);
    elseif contains(char(nf),'a') && contains(char(nf),'b') && contains(char(nf),'t')
        x0 = [0,0,0];
        [~, fmax] = fminsearch(@(x)nf(x(1),x(2),x(3)), x0);
    elseif (contains(char(nf),'a') && contains(char(nf),'t')) || (contains(char(nf),'b') && contains(char(nf),'t'))
        x0 = [0,0];
        [~, fmax] = fminsearch(@(x)nf(x(1),x(2)), x0);
    else
        [~,fmax] = fminbnd(nf,0,2*pi);
    end
    
    fid(m+1,1) = -fmax;
end

[maxFid, I] = max(fid,[],'ComparisonMethod','real');