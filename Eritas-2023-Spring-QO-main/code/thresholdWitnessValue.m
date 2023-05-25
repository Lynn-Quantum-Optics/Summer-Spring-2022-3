load('C:\Users\qiyan\Desktop\Quantum Optics\Fall 2022\Fall 2022 QO Data\undetectedW_6566.mat')
load('C:\Users\qiyan\Desktop\Quantum Optics\Fall 2022\Fall 2022 QO Data\detectedTriplet.mat')

info_1 = zeros(6566,1);
info_all = zeros(6566,1);

detected_Wp = zeros(16,6566);
for i = 1:6566
    if sum(detectedTriplet(i,:)) ~= 0
        detected_Wp(:,i) = undetectedW(:,i);
    end
end
detected_Wp(:,all(detected_Wp == 0)) = [];

% for i = 1:6566
%     if sum(detectedTriplet(i,:)) ~= 0
%         rho = reshape(undetectedW(:,i),4,4);
%         C = real(calculateC(rho));
%         info_all(i,1) = C;
%         pred_triplet = popPrediction(rho);
%         if detectedTriplet(i, pred_triplet) == 1
%             info_1(i,1) = C;
%         end
%     end
%             
% end
% 
% 
% info_1( all(~info_1,2), : ) = [];
% info_all( all(~info_all,2), : ) = [];
% edges = 0.01:0.01:0.99;
% [CDF1, ~] = histcounts(info_1,edges);
% [CDF2, ~] = histcounts(info_all,edges);
% plot(edges(1:size(CDF1,2)) + 0.01*ones(size(CDF1)), CDF1./CDF2, '.')
% xlabel('C')
% ylabel('prob of successful prediction')
% 
% function r = rotateRhoBasis(rho, basis)
% H = [1;0]; V = [0;1]; 
% D = (H+V)/sqrt(2); A = (H-V)/sqrt(2);
% R = (H+1i*V)/sqrt(2); L = (H-1i*V)/sqrt(2);
% 
% HH = kron(H,H); VV = kron(V,V); HV = kron(H,V); VH = kron(V,H); 
% HD = kron(H,D); VA = kron(V,A); HA = kron(H,A); VD = kron(V,D);
% HR = kron(H,R); VL = kron(V,L); HL = kron(H,L); VR = kron(V,R);
% DD = kron(D,D); AA = kron(A,A); DA = kron(D,A); AD = kron(A,D);
% RR = kron(R,R); LL = kron(L,L); RL = kron(R,L); LR = kron(L,R);
% 
% if basis == 'DADA'
%     r = [DD'*rho*DD, DD'*rho*DA, DD'*rho*AD, DD'*rho*AA;
%          DA'*rho*DD, DA'*rho*DA, DA'*rho*AD, DA'*rho*AA;
%          AD'*rho*DD, AD'*rho*DA, AD'*rho*AD, AD'*rho*AA;
%          AA'*rho*DD, AA'*rho*DA, AA'*rho*AD, AA'*rho*AA];
% elseif basis == 'RLRL'
%     r = [RR'*rho*RR, RR'*rho*RL, RR'*rho*LR, RR'*rho*LL;
%          RL'*rho*RR, RL'*rho*RL, RL'*rho*LR, RL'*rho*LL;
%          LR'*rho*RR, LR'*rho*RL, LR'*rho*LR, LR'*rho*LL;
%          LL'*rho*RR, LL'*rho*RL, LL'*rho*LR, LL'*rho*LL];
% elseif basis == 'HVDA'
%     r = [HD'*rho*HD, HD'*rho*HA, HD'*rho*VD, HD'*rho*VA;
%          HA'*rho*HD, HA'*rho*HA, HA'*rho*VD, HA'*rho*VA;
%          VD'*rho*HD, VD'*rho*HA, VD'*rho*VD, VD'*rho*VA;
%          VA'*rho*HD, VA'*rho*HA, VA'*rho*VD, VA'*rho*VA];
% elseif basis == 'HVRL'
%     r = [HR'*rho*HR, HR'*rho*HL, HR'*rho*VR, HR'*rho*VL;
%          HL'*rho*HR, HL'*rho*HL, HL'*rho*VR, HL'*rho*VL;
%          VR'*rho*HR, VR'*rho*HL, VR'*rho*VR, VR'*rho*VL;
%          VL'*rho*HR, VL'*rho*HL, VL'*rho*VR, VL'*rho*VL];
% end
% end
% 
% function triplet = popPrediction(rho)
%     P_hv = real(rho(1,1) + rho(4,4));
%     r_da = rotateRhoBasis(rho,'DADA');
%     P_da = real(r_da(1,1) + r_da(4,4));
%     r_rl = rotateRhoBasis(rho,'RLRL');
%     P_rl = real(r_rl(1,1) + r_rl(4,4));
%     
%     [~,triplet] = max([abs(0.5-P_hv), abs(0.5-P_da), abs(0.5-P_rl)]);
% end
