function transformed_matrix = visualize_permutation(transformation)
    % Shows a dxd matrix transformed geometrically

    sz = size(transformation);
    d = sqrt(sz(1));

    input_vector = transpose(1:d^2);
    output_vector = transformation * input_vector;

    transformed_matrix = transpose(reshape(output_vector, [d, d]));
end