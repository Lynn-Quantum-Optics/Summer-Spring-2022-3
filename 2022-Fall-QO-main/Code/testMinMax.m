% phiP = 1/sqrt(2)*[1;0;0;1];
% phiM = 1/sqrt(2)*[1;0;0;-1];
% psiP = 1/sqrt(2)*[0;1;1;0];
% psiM = 1/sqrt(2)*[0;1;-1;0];
% 
% syms t p a1 a2 real
% 
% P1 = cos(t)*phiP + sin(t)*phiM; 
% W1 = partialTrans(P1*P1');
% 
% P2 = cos(t)*psiP + sin(t)*psiM;
% W2 = partialTrans(P2*P2');
% 
% P3 = cos(t)*phiP + sin(t)*psiP;
% W3 = partialTrans(P3*P3');
% 
% P4 = cos(t)*phiM + sin(t)*psiM;
% W4 = partialTrans(P4*P4');
% 
% P5 = cos(t)*phiP + 1i*sin(t)*psiM;
% W5 = partialTrans(P5*P5');
% 
% P6 = cos(t)*phiM + 1i*sin(t)*psiP;
% W6 = partialTrans(P6*P6');
% 
% % -------------------------------------
% 
% 
% a1 = rand*2*pi; a2 = rand*2*pi; a3 = rand*2*pi; p = rand*2*pi;
% t1 = 1/sqrt(2)*(psiP + exp(1i*a1)*psiM);
% t2 = 1/sqrt(2)*(phiP + exp(1i*a2)*phiM);
% T = cos(p)*t1 + exp(1i*a3)*sin(p)*t2;
% [W,~] = maxW(T*T')

load('C:\Users\qiyan\Desktop\Fall 2022 QO\Fall 2022 QO Data\undetectedW_6566.mat')
load('C:\Users\qiyan\Desktop\Fall 2022 QO\Fall 2022 QO Data\detectedTriplet.mat')
correctChoiceByFid = zeros(size(undetectedW,2),3);
for n = 1:size(undetectedW,2)
    rho = reshape(undetectedW(:,n),4,4);
    exp_rho = 1/4*(trace(xx*rho)*xx + trace(yy*rho)*yy + trace(zz*rho)*zz ...
        + trace(ix*rho)*ix + trace(xi*rho)*xi + trace(iy*rho)*iy + trace(yi*rho)*yi ...
        + trace(iz*rho)*iz + trace(zi*rho)*zi);

    [maxFid,I] = checkFid(exp_rho);

    if detectedTriplet(n,I) == 1
        correctChoiceByFid(n,1) = 1;
    end
    
    if sum(detectedTriplet(n,:)) ~= 0
        correctChoiceByFid(n,2) = 1;
    end

    correctChoiceByFid(n,3) = maxFid;
end