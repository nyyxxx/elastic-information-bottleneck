function [ix,dix,iy]=calculate_ib_quantities(py,pxy,px,pyx,ixy,a,b,ny,nx,nt,times_initial,max_iterate)
%UNTITLED4 �˴���ʾ�йش˺�����ժҪ
%   Calculate  itx ity ditx: ѭ����Σ�ÿ���������t,���������õ���t(��ͬ�㷨������dib_L���Ƚ�ȡʹL��С��t�����ib curve���ꡣ
%   ��AB������ÿ�θ��²�������itx ity ditx,��L����L �仯С����ֵ���ж�Ϊ������������յ�itx ity ditx L
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

