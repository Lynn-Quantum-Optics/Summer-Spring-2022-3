load('C:\Users\qiyan\Desktop\Quantum Optics\Fall 2022\Fall 2022 QO Data\detectedTriplet.mat')
load('C:\Users\qiyan\Desktop\Quantum Optics\Fall 2022\Fall 2022 QO Data\undetectedW_6566.mat')
load('population_info.mat')

success = 0;
for i = 1:6566
    triplet = popPredict(population_info(i,1),population_info(i,2),population_info(i,3));
    if detectedTriplet(i,triplet) == 1
        success = success + 1;
    end
end

function triplet = popPredict(rho)


prob(1,1) = f11(P_hv);
prob(1,2) = f12(P_da);
prob(1,3) = f13(P_rl);

prob(2,1) = f21(P_hv);
prob(2,2) = f22(P_da);
prob(2,3) = f23(P_rl);

prob(3,1) = f31(P_hv);
prob(3,2) = f32(P_da);
prob(3,3) = f33(P_rl);

[~,triplet] = max([abs(0.5-P_hv), abs(0.5-P_da), abs(0.5-P_rl)]);

end