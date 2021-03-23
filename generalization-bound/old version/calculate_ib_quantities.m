function [ix,dix,iy]=calculate_ib_quantities(py,pxy,px,pyx,ixy,a,b,ny,nx,nt,times_initial,max_iterate)
%UNTITLED4 此处显示有关此函数的摘要
%   Calculate  itx ity ditx: 循环多次，每次随机生成t,算出收敛后得到的t(不同算法），算dib_L，比较取使L最小的t，输出ib curve坐标。
%   用AB迭代，每次更新参数计算itx ity ditx,求L，当L 变化小于阈值则判定为收敛，输出最终的itx ity ditx L
threshold=10^-3;minL=+inf;
for times=1:times_initial
    [ptx,pt,pty] = initial_t(ny,nx,nt,pxy,py);
    
      L_step_new=0;L_step_old=0;n_iter=0;
        while n_iter<2|| (n_iter<max_iterate && abs(L_step_old-L_step_new)>threshold)
            L_step_old=L_step_new;
            n_iter=n_iter+1; 
            if a==0
                 [itx_step,ity_step,ditx_step,ptx,pt,pty]=dib(ptx,pt,pty,pyx,pxy,py,px,a,b,nx,ny,nt);
            else
                 [itx_step,ity_step,ditx_step,ptx,pt,pty]=aib(ptx,pt,pty,pyx,pxy,py,px,a,b,nx,ny,nt);
            end
            L_step_new=ditx_step-b*ity_step;
        end
         if minL>L_step_new
             minL=L_step_new;
             ix=itx_step;
             iy=ity_step;
             dix=ditx_step;
         end
end
end

