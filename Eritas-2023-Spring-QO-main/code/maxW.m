% maxW: list of maximized W
% I: index of smallest maxW

function [maxW,I] = maxW(rho)
vars;

T = cat(1,W1,W2,W3,W4,W5,W6);
maxW = zeros(6,1);
for i = 0:5
    W = T(4*i+1:4*i+4,:);
    nf = matlabFunction(-1*real(trace(W*rho)));
    if contains(char(nf),'t')
        [~,fmax] = fminbnd(nf,-pi,pi);
    else
        fmax = trace(W*rho);
    end
    maxW(i+1,1) = -1*fmax;
end

[~,I] = min(maxW);

end