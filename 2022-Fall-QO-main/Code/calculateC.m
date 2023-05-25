function concurrence = calculateC(rho)
sig = [0 0 0 -1;0 0 1 0;0 1 0 0;-1 0 0 0];
eval = eigs(rho*sig*rho.'*sig,4);
concurrence = max([sqrt(eval(1,1))-sqrt(eval(2,1))-sqrt(eval(3,1))-sqrt(eval(4,1)),0],[],'ComparisonMethod','real');