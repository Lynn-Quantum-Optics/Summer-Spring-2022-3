d = 2;

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

num_distinct_elements = 12;

orderings = [];

while length(orderings) < num_distinct_elements
    ordering_candidate = randperm(d^2);

    P = gen_perm_mat_from_ordering(ordering_candidate);

    if check_separable(B * P * B_inv)
        orderings = [orderings; ordering_candidate];
    end
end

cycle_string = "";

for i = 1:length(orderings)
    new_cycle_notation = cycle_notation(orderings(i));
    cycle_string = append(cycle_string, ",", new_cycle_notation);
end


