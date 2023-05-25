function phase_lists = generate_phase_lists(d, l)
    % Recursively generates all orderings of the objects
    if l == 1
        phase_lists = transpose(0:(d-1));
    else
        phase_lists = [];
        sub_phase_lists = generate_phase_lists(d, l-1);
        for i = 0:(d-1)
            object_vector = i * ones(length(sub_phase_lists),1);
            phase_lists = [phase_lists; [object_vector sub_phase_lists]];
        end
    end
end