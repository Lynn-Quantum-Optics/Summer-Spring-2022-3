load('C:\Users\qiyan\Desktop\Quantum Optics\Spring 2023\DataBase\detectedWp.mat')
load('C:\Users\qiyan\Desktop\Quantum Optics\Spring 2023\DataBase\tripletWp.mat')
load('C:\Users\qiyan\Desktop\Quantum Optics\Spring 2023\DataBase\incoming.mat')

success = 0;

for k = 4000:4020
    rho = reshape(detectedWp(:,k),4,4);
    v = stokesParam(rho);

    dis = zeros(500,1);
    for i = 1:500
        rho_db = reshape(detectedWp(:,i),4,4);
        v_db = stokesParam(rho_db);
        dis(i,1) = norm(v_db-v);
    end
    
    [~,I] = min(dis);
    predT = tripletWp(I,4);
    
    if tripletWp(k, predT) == 1
        success = success + 1;
    end
end


function param = stokesParam(rho)
vars;
param = [trace(xx*rho); trace(yy*rho); trace(zz*rho);
    trace(ix*rho); trace(xi*rho); trace(iy*rho);
    trace(yi*rho); trace(iz*rho); trace(zi*rho)];
end