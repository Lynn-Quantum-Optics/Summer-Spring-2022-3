d = 7;

B = zeros(d^2);

for i = 1:d^2
    p = mod(i-1,d);
    c = floor((i-1)/d);

    for j = 1:d^2
        k = mod(j-1,d);
        b = floor((j-1)/d);

        if c == mod(k-b,d)
            B(i,j) = exp(1i*2*pi*p*b/d);
        end
    end
end

B_inv = B';

a = generate_separable_orderings(d);

good = zeros(length(a), 1);

tic
parfor i = 1:length(a)
    P = gen_perm_mat_from_ordering(a(i,1:d^2));

    c1 = check_separable(P);
    c2 = check_separable(B * P * B_inv);

    if c2
        good(i) = 1;
    end
end
toc

