function separable = check_separable(matrix)
    % Takes a matrix and checks if it is seperable
    sz = size(matrix);
    factor_size = sqrt(sz(1));

    % could be made faster in practice by pre-allocating space and then
    % passing that space to this function to be use instead
    % of allocating a new matrix of this exact size each time
    separability_matrix = zeros(factor_size^2, factor_size^2);
    for i = 1:factor_size
        for j = 1:factor_size
            m = matrix(((i-1)*factor_size)+1:(i*factor_size),((j-1)*factor_size)+1:(j*factor_size));
            vm = m(:);
            separability_matrix((i-1)*factor_size+j,1:factor_size^2) = vm;
        end
    end
    separable = (rank(separability_matrix) == 1);
end