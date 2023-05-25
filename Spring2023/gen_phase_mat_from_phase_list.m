function phase_matrix = gen_phase_mat_from_phase_list(phase_list)
    % generates a permutation matrix from its order representation
    dsqr = length(phase_list);
    d = sqrt(dsqr);
    phase_matrix = zeros(dsqr);
    for i = 1:dsqr
        phase_matrix(i,i) = exp(1i*2*pi*(phase_list(i))/d);
    end
end