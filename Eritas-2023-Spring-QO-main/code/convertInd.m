function ind = convertInd(I,set)

if set == 1
    if (I == 1 || I == 2)
        ind = 1;
    elseif (I == 3 || I == 4)
        ind = 2;
    elseif (I == 5 || I == 6)
        ind = 3;
    end
end

if set == 2
    if (I == 1 || I == 2 || I == 3)
        ind = 1;
    elseif (I == 4 || I == 5 || I == 6)
        ind = 2;
    elseif (I == 7 || I == 8 || I == 9)
        ind = 3;
    end
end

end