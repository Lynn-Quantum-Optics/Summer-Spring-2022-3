function orderings = generate_separable_orderings(d)
    % Recursively generates all orderings of the objects
    sub_orderings = generate_orderings(1:d);
    num_sub_orderings = length(sub_orderings);

    orderings = zeros((factorial(d))^2,d^2);

    for i = 1:num_sub_orderings
        for j = 1:num_sub_orderings
            for k = 1:d
                for l = 1:d
                    ordering_index = num_sub_orderings * (i - 1) + j;
                    val_1 = sub_orderings(i, (d+1)-k);
                    val_2 = sub_orderings(j, (d+1)-l);

                    orderings(ordering_index, d*(k-1)+l) = d * (val_1 - 1) + val_2;
                end
            end
        end
    end
end