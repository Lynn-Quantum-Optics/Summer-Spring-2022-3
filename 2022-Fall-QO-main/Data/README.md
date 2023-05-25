## smaple_10000.mat
The density matrices of the 10,000 randomly generated entangled states we used as samples. Each column contains the 16 entries of one density matrix. To turn the column into a 4 by 4 matrix, use `reshape(sample(:,col),4,4);`.

## undetectedW_6566.mat
The density matrices of the 6566 states undetected by $\lbrace W \rbrace$ among the 10,000 samples.

## undetectedWp_3142.mat
The density matrices of the 3142 states undetected by $\lbrace W' \rbrace$ among the 10,000 samples.

## detectedTriplet.mat
A boolean matrix that shows whether or not each Triplet detects a state. For example, [1 1 0 1] on row 8 means that the $8^{th}$ state in our samples is detected by Triplet 1 and Triplet 2, and hence detected by $\lbrace W \rbrace$.
