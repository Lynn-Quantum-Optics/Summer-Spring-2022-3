d = 2;

B = zeros(d^2);

for i = 1:d^2
    p = mod(i-1,d);
    c = floor((i-1)/d);

    for j = 1:d^2
        k = mod(j-1,d);
        b = floor((j-1)/d);

        if c == mod(k-b,d)
            B(i,j) = 1 / sqrt(d) * exp(1i*2*pi*p*b/d);
        end
    end
end

B_inv = B';

all_phase_lists = generate_phase_lists(d, d^2);
phase_lists = all_phase_lists(1:d^(d^2-1),1:d^2);
orderings = generate_orderings(1:d^2);

record = zeros(length(orderings), 1);

disp("starting search");

tic
parfor i = 1:length(orderings)
    permutation_matrix = gen_perm_mat_from_ordering(orderings(i,1:d^2));
    
    c = false;

    for j = 1:length(phase_lists)
        phase_matrix = gen_phase_mat_from_phase_list(phase_lists(j,1:d^2));

        c = c | check_separable(B_inv * permutation_matrix * phase_matrix * B);
    end
    if c
        record(i) = 1;
    end
end
toc
