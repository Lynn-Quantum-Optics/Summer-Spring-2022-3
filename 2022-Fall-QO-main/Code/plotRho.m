% transform the bases of the density matrices

figure;
[rho_hv, rho_da, rho_rl, rho_hd, rho_hr] = avgRho(sample);
subplot(2,3,1)
bar3(real(rho_hv))
title('$\bar{\rho}_{HVHV}$', 'interpreter', 'latex')
subplot(2,3,2)
bar3(real(rho_da))
title('$\bar{\rho}_{DADA}$', 'interpreter', 'latex')
subplot(2,3,3)
bar3(real(rho_rl))
title('$\bar{\rho}_{RLRL}$', 'interpreter', 'latex')
subplot(2,3,4)
bar3(real(rho_hd))
title('$\bar{\rho}_{HVDA}$', 'interpreter', 'latex')
subplot(2,3,5)
bar3(real(rho_hr))
title('$\bar{\rho}_{HVRL}$', 'interpreter', 'latex')

% [rho_hv0, rho_ad0, rho_rl0] = avgRho(detectedW0);
% [rho_hv1, rho_ad1, rho_rl1] = avgRho(detectedW1);
% [rho_hv2, rho_ad2, rho_rl2] = avgRho(detectedW2);
% [rho_hv3, rho_ad3, rho_rl3] = avgRho(detectedW3);
% 
% figure;
% subplot(2,2,1)
% bar3(real(rho_hv0));
% title('real part of $\bar{\rho(W)}_{HV}$', 'interpreter', 'latex')
% subplot(2,2,2)
% bar3(real(rho_hv1));
% title('real part of $\bar{\rho(W)}_{HV}$ after transformation 1', 'interpreter', 'latex')
% subplot(2,2,3)
% bar3(real(rho_hv2));
% title('real part of $\bar{\rho(W)}_{HV}$ after transformation 2', 'interpreter', 'latex')
% subplot(2,2,4)
% bar3(real(rho_hv3));
% title('real part of $\bar{\rho(W)}_{HV}$ after transformation 3', 'interpreter', 'latex')
% 
% figure;
% subplot(2,2,1)
% bar3(real(rho_ad0));
% title('real part of $\bar{\rho(W)}_{DA}$', 'interpreter', 'latex')
% subplot(2,2,2)
% bar3(real(rho_ad1));
% title('real part of $\bar{\rho(W)}_{DA}$ after transformation 1', 'interpreter', 'latex')
% subplot(2,2,3)
% bar3(real(rho_ad2));
% title('real part of $\bar{\rho(W)}_{DA}$ after transformation 2', 'interpreter', 'latex')
% subplot(2,2,4)
% bar3(real(rho_ad3));
% title('real part of $\bar{\rho(W)}_{DA}$ after transformation 3', 'interpreter', 'latex')
% 
% figure;
% subplot(2,2,1)
% bar3(real(rho_rl0));
% title('real part of $\bar{\rho(W)}_{RL}$', 'interpreter', 'latex')
% subplot(2,2,2)
% bar3(real(rho_rl1));
% title('real part of $\bar{\rho(W)}_{RL}$ after transformation 1', 'interpreter', 'latex')
% subplot(2,2,3)
% bar3(real(rho_rl2));
% title('real part of $\bar{\rho(W)}_{RL}$ after transformation 2', 'interpreter', 'latex')
% subplot(2,2,4)
% bar3(real(rho_rl3));
% title('real part of $\bar{\rho(W)}_{RL}$ after transformation 3', 'interpreter', 'latex')

function [r_hvhv, r_dada, r_rlrl, r_hvda, r_hvrl] = avgRho(detectedW)

r_hvhv = zeros(4,4);
r_dada = zeros(4,4);
r_rlrl = zeros(4,4);
r_hvda = zeros(4,4);
r_hvrl = zeros(4,4);

for n = 1:size(detectedW,2)
    rho = reshape(detectedW(:,n),4,4);
    r_hvhv = r_hvhv + rho;
    r_dada = r_dada + rotateRhoBasis(rho,'DADA');
    r_rlrl = r_rlrl + rotateRhoBasis(rho,'RLRL');
    r_hvda = r_hvda + rotateRhoBasis(rho,'HVDA');
    r_hvrl = r_hvrl + rotateRhoBasis(rho,'HVRL');
end
r_hvhv = r_hvhv / n - 1/4*eye(4);
r_dada = r_dada / n - 1/4*eye(4);
r_rlrl = r_rlrl / n - 1/4*eye(4);
r_hvda = r_hvda / n - 1/4*eye(4);
r_hvrl = r_hvrl / n - 1/4*eye(4);
end
