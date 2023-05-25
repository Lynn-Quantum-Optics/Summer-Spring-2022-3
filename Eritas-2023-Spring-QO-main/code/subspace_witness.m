info_1 = zeros(3142,1);
info_2 = zeros(6566,1);
info_all = zeros(10000,1);
for i = 1:3142
    rho = reshape(undetectedWp(:,i),4,4);
    info_1(i,1) = real(trace(rho^2));
end

for i = 1:6566
    rho = reshape(undetectedW(:,i),4,4);
    info_2(i,1) = real(trace(rho^2));
end

for i = 1:10000
    rho = reshape(sample(:,i),4,4);
    info_all(i,1) = real(trace(rho^2));
end

info_1( all(~info_1,2), : ) = [];
info_all( all(~info_all,2), : ) = [];
edges = 0.01:0.02:0.99;
[CDF1, ~] = histcounts(info_1,edges);
[CDF2, ~] = histcounts(info_2,edges);
[CDF3, ~] = histcounts(info_all,edges);
plot(edges(1:size(CDF1,2)) + 0.01*ones(size(CDF1)), CDF1./CDF3,'k')
hold on
plot(edges(1:size(CDF1,2)) + 0.01*ones(size(CDF1)), CDF2./CDF3,'b')
legend("W'","W")
xlabel('purity')
ylabel('probability to be undetected')

figure;
histogram(info_all,'Normalization','probability')