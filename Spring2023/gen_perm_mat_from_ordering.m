function permutation_matrix = gen_perm_mat_from_ordering(ordering)
    % generates a permutation matrix from its order representation
    permutation_matrix = zeros(length(ordering));
    for i = 1:length(ordering)
        permutation_matrix(i,ordering(i)) = 1;
    end
end