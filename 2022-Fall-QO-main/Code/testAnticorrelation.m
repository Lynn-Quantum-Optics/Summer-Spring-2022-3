H = [1;0]; V = [0;1]; 
D = (H+V)/sqrt(2); A = (H-V)/sqrt(2);
R = (H+1i*V)/sqrt(2); L = (H-1i*V)/sqrt(2);
HH = kron(H,H); VV = kron(V,V); HV = kron(H,V); VH = kron(V,H); 
HD = kron(H,D); VA = kron(V,A); HA = kron(H,A); VD = kron(V,D);
HR = kron(H,R); VL = kron(V,L); HL = kron(H,L); VR = kron(V,R);
DD = kron(D,D); AA = kron(A,A); DA = kron(D,A); AD = kron(A,D);
RR = kron(R,R); LL = kron(L,L); RL = kron(R,L); LR = kron(L,R);

info = zeros(5,size(detectedW3,2));
for n = 1:size(detectedW3,2)
    rho = reshape(detectedW3(:,n),4,4);
    info(1,n) = abs(HV'*rho*HV - VH'*rho*VH);
    info(2,n) = abs(HA'*rho*HA - VD'*rho*VD);
    info(3,n) = abs(HL'*rho*HL - VR'*rho*VR);
    [M,I] = max(info(1:3,n));
    info(4,n) = M;
    info(5,n) = I;
end
figure;
histogram(real(info(4,:)),'Normalization','probability')
xlabel('greatest anti-correlation')
ylabel('relative probability')
figure;
histogram(real(info(5,:)),'Normalization','probability')
xlabel('basis')
ylabel('relative probability')