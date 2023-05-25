% TODO: optimize code to reduce runtime, add pointer
vars;

%% Pure Entangled States: max-min method
% w_count = 0;
% wp_count = 0;
% method_count = 0;
% 
% thres = 1e-5;
% k = 10000;
% 
% n = 1;
% while n < k+1
%     rho = pure_state;
%     eval = eigs(rho*sig*rho.'*sig,4);
%     concurrence = max([sqrt(eval(1,1))-sqrt(eval(2,1))-sqrt(eval(3,1))-sqrt(eval(4,1)),0],[],'ComparisonMethod','real');
%     if abs(concurrence) > thres
%         [min_w,w_val] = findW(rho,1);
%     
%         if min_w >= 0
%             w_count = w_count + 1;
%             [max_w,I] = maxW(rho);
%     
%             [min_wp,wp_val] = findW(rho,2);
%             if ((I == 1 || I == 2) && (wp_val(1,1) >= 0 && wp_val(2,1) >= 0 && wp_val(3,1) >= 0)) || ...
%                     ((I == 3 || I == 4) && (wp_val(4,1) >= 0 && wp_val(5,1) >= 0)) || ...
%                     ((I == 5 || I == 6) && (wp_val(6,1) >= 0 && wp_val(7,1) >= 0))
%                 method_count = method_count + 1;
%             end
%     
%             if min_wp >= 0
%                 wp_count = wp_count + 1;
%             end
%         end
%         n = n+1;
%     end
% 
%     if n == k/2
%         disp('------------HALFWAY----------')
%     end
% end
% 
% w_count
% method_count
% wp_count

%% Mixed Entangled States: max-min method (with histogram)
w_count = 0;
wp_count = 0;
method_count = 0;

thres = 1e-5;
k = 10000;
n = 1;

fail_w = zeros(k,2);
success_w = zeros(k,2);
fail_method = zeros(k,2);
success_method = zeros(k,2);
fail_wp = zeros(k,2);
success_wp = zeros(k,2);

while n < k+1
    rho = random_state;
    eval = eigs(rho*sig*rho.'*sig,4);
    concurrence = max([sqrt(eval(1,1))-sqrt(eval(2,1))-sqrt(eval(3,1))-sqrt(eval(4,1)),0],[],'ComparisonMethod','real');

    if real(concurrence) > thres
        purity = trace(rho^2);
        [min_w,~] = findW(rho,1);
    
        if real(min_w) >= 0
            w_count = w_count + 1;
            fail_w(w_count,:) = [concurrence purity];

            [max_w,I] = maxW(rho);
    
            [min_wp,wp_val] = findW(rho,2);
            if ((I == 1 || I == 2) && (wp_val(1,1) >= 0 && wp_val(2,1) >= 0 && wp_val(3,1) >= 0)) || ...
                    ((I == 3 || I == 4) && (wp_val(4,1) >= 0 && wp_val(5,1) >= 0 && wp_val(6,1) >= 0)) || ...
                    ((I == 5 || I == 6) && (wp_val(7,1) >= 0 && wp_val(8,1) >= 0 && wp_val(9,1) >= 0))
                method_count = method_count + 1;
                fail_method(method_count,:) = [concurrence purity];
            else
                success_method(n-method_count,:) = [concurrence purity];
            end

            if real(min_wp) >= 0
                wp_count = wp_count + 1;
                fail_wp(wp_count,:) = [concurrence purity];
            else
                success_wp(n-wp_count,:) = [concurrence purity];
            end
        else
            success_w(n-w_count,:) = [concurrence purity];
            success_method(n-method_count,:) = [concurrence purity];
            success_wp(n-wp_count,:) = [concurrence purity];
        end

        n = n+1;
    end

    if n == k/2
        disp('------------HALFWAY----------')
    end
end

fail_w = fail_w(1:w_count,:);
success_w = success_w(1:k-w_count,:);
fail_method = fail_method(1:method_count,:);
success_method = success_method(1:k-method_count,:);
fail_wp = fail_wp(1:wp_count,:);
success_wp = success_wp(1:k-wp_count,:);

w_count
method_count
wp_count
%
% C = figure;
% P = figure;
% 
% figure(C);
% histogram(real(fail_w(:,1)));
% hold on
% histogram(real(fail_method(:,1)));
% histogram(real(fail_wp(:,1)));
% xlabel('concurrence');
% ylabel({'number of undetected states','(out of 10,000 mixed entangled states)'});
% legend('W',"W'_p","W'");
% 
% figure(P);
% histogram(real(fail_w(:,2)));
% hold on
% histogram(real(fail_method(:,2)));
% histogram(real(fail_wp(:,2)));
% xlabel('purity');
% ylabel({'number of undetected states','(out of 10,000 mixed entangled states)'});
% legend('W',"W'_p","W'");

%% Mixed Entangled States: varying threshold of concurrence
% w_fail = zeros(1,11);
% wp_fail = zeros(1,11);
% method_fail = zeros(1,11);
% 
% k = 10000;
% 
% for thres = 0:0.05:0.5
%     n = 1;
%     w_count = 0;
%     wp_count = 0;
%     method_count = 0;
%     while n < k+1
%         rho = random_state;
%         eval = eigs(rho*sig*rho.'*sig,4);
%         concurrence = max([sqrt(eval(1,1))-sqrt(eval(2,1))-sqrt(eval(3,1))-sqrt(eval(4,1)),0],[],'ComparisonMethod','real');
%     
%         if real(concurrence) > thres
%             [min_w,~] = findW(rho,1);
%         
%             if real(min_w) >= 0
%                 w_count = w_count + 1;
%     
%                 [max_w,I] = maxW(rho);
%         
%                 [min_wp,wp_val] = findW(rho,2);
%                 if ((I == 1 || I == 2) && (wp_val(1,1) >= 0 && wp_val(2,1) >= 0 && wp_val(3,1) >= 0) || ...
%                     ((I == 3 || I == 4) && (wp_val(4,1) >= 0 && wp_val(5,1) >= 0 && wp_val(6,1) >= 0)) || ...
%                     ((I == 5 || I == 6) && (wp_val(7,1) >= 0 && wp_val(8,1) >= 0 && wp_val(9,1) >= 0)))
%                     method_count = method_count + 1;
%                 end
%     
%                 if real(min_wp) >= 0
%                     wp_count = wp_count + 1;
%                 end
%             end
%     
%             n = n+1;
%         end    
%     end
% 
%     w_fail(1,int32(thres*20+1)) = w_count/k;
%     wp_fail(1,int32(thres*20+1)) = wp_count/k;
%     method_fail(1,int32(thres*20+1)) = method_count/k;
% 
%     disp({'-------------------',thres,'-------------------------'})
% end
% 
% j = 0:0.05:0.5;
% err = 1/sqrt(k)*ones(1,11);
% errorbar(j,w_fail,err,'LineStyle','-','Color','k');
% ylim([-0.02 0.7])
% xlabel('\epsilon')
% ylabel('r_{FN}')
% hold on
% errorbar(j,method_fail,err,'LineStyle','--','Color','k');
% errorbar(j,wp_fail,err,'LineStyle',':','Color','k');
% legend("W","W'_p","W'")

%% Mixed Entangled States: varying threshold of witness value
% w_fail = zeros(1,11);
% wp_fail = zeros(1,11);
% method_fail = zeros(1,11);
% 
% k = 10000;
% 
% for thres = 0:-0.001:-0.01
%     n = 1;
%     w_count = 0;
%     wp_count = 0;
%     method_count = 0;
%     while n < k+1
%         rho = random_state;
%         eval = eigs(rho*sig*rho.'*sig,4);
%         concurrence = max([sqrt(eval(1,1))-sqrt(eval(2,1))-sqrt(eval(3,1))-sqrt(eval(4,1)),0],[],'ComparisonMethod','real');
%     
%         if real(concurrence) > 1e-5
%             [min_w,~] = findW(rho,1);
%         
%             if real(min_w) >= thres
%                 w_count = w_count + 1;
%     
%                 [max_w,I] = maxW(rho);
%         
%                 [min_wp,wp_val] = findW(rho,2);
%                 wp_val = real(wp_val);
%                 if ((I == 1 || I == 2) && (wp_val(1,1) >= thres && wp_val(2,1) >= thres && wp_val(3,1) >= thres)) || ...
%                     ((I == 3 || I == 4) && (wp_val(4,1) >= thres && wp_val(5,1) >= thres && wp_val(6,1) >= thres)) || ...
%                     ((I == 5 || I == 6) && (wp_val(7,1) >= thres && wp_val(8,1) >= thres && wp_val(9,1) >= thres))
%                     method_count = method_count + 1;
%                 end
%     
%                 if real(min_wp) >= thres
%                     wp_count = wp_count + 1;
%                 end
%             end
%     
%             n = n+1;
%         end    
%     end
% 
%     w_fail(1,int32(-thres*1000+1)) = w_count/k;
%     wp_fail(1,int32(-thres*1000+1)) = wp_count/k;
%     method_fail(1,int32(-thres*1000+1)) = method_count/k;
% end
% 
% j = 0:-0.001:-0.01;
% err = 1/sqrt(k)*ones(1,11);
% errorbar(j,w_fail,err,'LineStyle','-','Color','k');
% xlabel('threshold for witness value')
% ylabel('r_{FN}')
% hold on
% errorbar(j,method_fail,err,'LineStyle','--','Color','k');
% errorbar(j,wp_fail,err,'LineStyle',':','Color','k');
% legend("W","W'_p","W'")