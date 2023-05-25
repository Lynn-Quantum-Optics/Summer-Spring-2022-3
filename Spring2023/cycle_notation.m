function cycle_notation = cycle_notation(ordering)
    % Generates a cycle notationa for the ordering provided.
    d = length(ordering);

    cycle_notation = "";
    done = [];

    for i = 1:d
        if any(done(:) == i);
            continue
        elseif ordering(i) == i
            done = [done i];
            continue
        else
            cycle_notation = append(cycle_notation, "(", int2str(i));

            start = i;
            done = [done start];

            next = ordering(i);
            while next ~= start
                cycle_notation = append(cycle_notation, ',');
                done = [done next];
                cycle_notation = append(cycle_notation, int2str(next));
                next = ordering(next);
            end

            cycle_notation = append(cycle_notation, ")");
        end
    end
end