function [py,pxy,ptx,px,pyx,pt,pty,ixy] = initial_hand(ny,nx,nt)
%initialization
%   此处显示详细说明
py1=1/2;
py=[py1,1-py1];
rdd=ones(nx,ny);%p(x|y)
rdd(1:3,1)=1;
rdd(4:6,2)=2;
rdd(7:10,2)=1.5;
pxy=centra(rdd,nx,ny);
rd=rand(nt,nx);%p(t|x)
ptx=centra(rd,nt,nx);
for i=1:nx %p(x)
    px(i)=0;
      for j=1:ny
           px(i)=px(i)+pxy(i,j)*py(j);
      end
end
for j=1:ny %p(y|x)
     for i=1:nx     
        pyx(j,i)=pxy(i,j)*py(j)/px(i);
    end
end
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
ixy=0;
for i=1:nx %I(X,Y)
    for j=1:ny
           ixy=ixy+pxy(i,j)*py(j)*(log(pxy(i,j))-log(px(i)));
        end
end
end

