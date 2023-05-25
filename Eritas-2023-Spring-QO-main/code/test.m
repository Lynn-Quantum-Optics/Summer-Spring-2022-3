% vars;
% W = zeros(21,41);
% Wp = zeros(21,41);
% W_pop = zeros(21,41);
% 
% 
% t1 = 1/sqrt(2)*(psiP + 1i*psiM);
% t2 = 1/sqrt(2)*(phiP + 1i*phiM);
% 
% row = 1;
% for a = (0:0.05:1)*pi
%     col = 1;
%     for b = (0:0.05:2)*pi
%         t = cos(a)*t1 + sin(a)*exp(1i*b)*t2;
%         rho = t*t';
%         [minW, ~] = findW(rho,1);
%         W(row,col) = minW;
%         [minWp, Wp_val] = findW(rho,2);
%         Wp(row,col) = minWp;
%         I = popPrediction(rho)*3;
%         W_pop(row,col) = min(Wp_val(I-2:I,1));
%         col = col + 1;
%     end
%     row = row + 1;
% end
% [xx, yy] = meshgrid((0:0.05:1)*pi, (0:0.05:2)*pi);
% 
% subplot(1,2,1)
% plot3(xx, yy, transpose(W), 'k.')
% hold on
% plot3(xx, yy, transpose(Wp), 'b.')
% yticks([0, pi/2, pi, 3*pi/2, 2*pi])
% yticklabels({'0', '\pi/2', '\pi', '3\pi/2', '2\pi'})
% xticks([0, pi/2, pi])
% xticklabels({'0', '\pi/2', '\pi'})
% xlabel('\alpha')
% ylabel('\beta')
% legend("W","W'")
% 
% subplot(1,2,2)
% plot3(xx, yy, transpose(W_pop), 'b.')
% yticks([0, pi/2, pi, 3*pi/2, 2*pi])
% yticklabels({'0', '\pi/2', '\pi', '3\pi/2', '2\pi'})
% xticks([0, pi/2, pi])
% xticklabels({'0', '\pi/2', '\pi'})
% xlabel('\alpha')
% ylabel('\beta')
% legend("W'_{pop}")
% 
% saveas(gcf,'last.fig')

%------------------------------------------------
clear all
vars;
W = zeros(21,41);
Wp = zeros(21,41);
W_pop = zeros(21,41);

row = 1;
for a = (0:0.05:1)*pi
    col = 1;
    for b = (0:0.05:2)*pi
        t = cos(a)*psiP + sin(a)*exp(1i*b)*psiM;
        rho = t*t';
        [minW, ~] = findW(rho,1);
        W(row,col) = minW;
        [minWp, Wp_val] = findW(rho,2);
        Wp(row,col) = minWp;
        I = popPrediction(rho)*3;
        W_pop(row,col) = min(Wp_val(I-2:I,1));
        col = col + 1;
    end
    row = row + 1;
end
[xx, yy] = meshgrid((0:0.05:1)*pi, (0:0.05:2)*pi);

subplot(1,2,1)
plot3(xx, yy, transpose(W), 'k.')
hold on
plot3(xx, yy, transpose(Wp), 'b.')
yticks([0, pi/2, pi, 3*pi/2, 2*pi])
yticklabels({'0', '\pi/2', '\pi', '3\pi/2', '2\pi'})
xticks([0, pi/2, pi])
xticklabels({'0', '\pi/2', '\pi'})
xlabel('\alpha')
ylabel('\beta')
legend("W","W'")

subplot(1,2,2)
plot3(xx, yy, transpose(W_pop), 'b.')
yticks([0, pi/2, pi, 3*pi/2, 2*pi])
yticklabels({'0', '\pi/2', '\pi', '3\pi/2', '2\pi'})
xticks([0, pi/2, pi])
xticklabels({'0', '\pi/2', '\pi'})
xlabel('\alpha')
ylabel('\beta')
legend("W'_{pop}")

saveas(gcf,'first.fig')




function r = rotateRhoBasis(rho, basis)
H = [1;0]; V = [0;1]; 
D = (H+V)/sqrt(2); A = (H-V)/sqrt(2);
R = (H+1i*V)/sqrt(2); L = (H-1i*V)/sqrt(2);
DD = kron(D,D); AA = kron(A,A); DA = kron(D,A); AD = kron(A,D);
RR = kron(R,R); LL = kron(L,L); RL = kron(R,L); LR = kron(L,R);

if basis == 'DA'
    r = [DD'*rho*DD, DD'*rho*DA, DD'*rho*AD, DD'*rho*AA;
         DA'*rho*DD, DA'*rho*DA, DA'*rho*AD, DA'*rho*AA;
         AD'*rho*DD, AD'*rho*DA, AD'*rho*AD, AD'*rho*AA;
         AA'*rho*DD, AA'*rho*DA, AA'*rho*AD, AA'*rho*AA];
elseif basis == 'RL'
    r = [RR'*rho*RR, RR'*rho*RL, RR'*rho*LR, RR'*rho*LL;
         RL'*rho*RR, RL'*rho*RL, RL'*rho*LR, RL'*rho*LL;
         LR'*rho*RR, LR'*rho*RL, LR'*rho*LR, LR'*rho*LL;
         LL'*rho*RR, LL'*rho*RL, LL'*rho*LR, LL'*rho*LL];
end
end

function triplet = popPrediction(rho)
    P_hv = real(rho(1,1) + rho(4,4));
    r_da = rotateRhoBasis(rho,'DA');
    P_da = real(r_da(1,1) + r_da(4,4));
    r_rl = rotateRhoBasis(rho,'RL');
    P_rl = real(r_rl(1,1) + r_rl(4,4));
    
    [~,triplet] = max([abs(0.5-P_hv), abs(0.5-P_da), abs(0.5-P_rl)]);
end