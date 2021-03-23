function [ptx,pt,pty] = initial_t(ny,nx,nt,pxy,py)
%initialization
%   此处显示详细说明
rd=rand(nt,nx);%p(t|x)
ptx=centra(rd,nt,nx);
for i=1:nt %p(t)
    pt(i)=0;
    for j=1:nx
        for k=1:ny
           pt(i)=pt(i)+ptx(i,j)*pxy(j,k)*py(k);
        end
    end
end
for i=1:nt %p(t|y)
     for k=1:ny
        pty(i,k)=0;
        for j=1:nx       
           pty(i,k)=pty(i,k)+ptx(i,j)*pxy(j,k);
        end
     end
end
end

