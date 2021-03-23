function [rv,ob,nb,ober,nber] = bound_simul(m,delta,nx,ny,nt)

%fix a model ptx
ptx = generate_a_model(nx,nt);
%Theoretic value
[py,pxy,px,jxy] = population_xy(ny,nx);
[pt,pty,ity,hty,ht,ixt] = cal_t(ny,nx,nt,ptx,px,pxy,py);
%Empirical value
[ppy,ppx,ppxy] = sample_xy(m,nx,ny,py,px,pxy,jxy);
 [ppt,ppty,iity,hhty,hht,iixt] = cal_t(ny,nx,nt,ptx,ppx,ppxy,ppy);
 %original bound
 ober=0;
    c=(2+sqrt(2*log((ny+2)/delta)))/sqrt(m);
    g1=c*2*sqrt(2*log(2))/min(px);%ppx or px?
    s2=2*g1*(-log(g1)*sqrt(nt*ixt)+nt^(3/4)*(ixt)^(1/4));
    s1=c*2/(min(py))*iixt;
    ob=s1+s2;
    if g1>1 
        ober=1;
    end
 %new bound
 	nber=0;
    g2=c/sqrt(min(px));
    c1=-g2*log(g2);
    c2=g2/sqrt(min(pt));
    g3=c/sqrt(min0(pxy,nx,ny));
    c3=-g3*log(g3);
    c4=g3/sqrt(min(min(pty)));
    c5=c/sqrt(min(ppy));
    nb=(c1+c3)*sqrt(nt-1)+c2*ht+c4*hty+c5*sqrt(hhty*(log(nt)-hhty));
     if g2>1 ||g3>1 
        nber=1;
    end
  %real value
     rv=abs(ity-iity);
% fprintf("#sample=%d,real value=%d,original bound=%d,new bound=%d\n",m,rv,ob,nb);
end