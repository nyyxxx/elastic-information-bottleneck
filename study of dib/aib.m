function [itx,ity,ditx,ptx,pt,pty]=aib(ptx,pt,pty,pyx,pxy,py,px,a,b,nx,ny,nt)
%执行AB算法一次更新
    for i=1:nt %p(t|x)
        if pt(i) ~=0 && pt(i)~=1
        for j=1:nx
            d=0;
            for k=1:ny
                if pty(i,k) ~=0
                d=d+pyx(k,j)*(log(pty(i,k))-log(pt(i)));
                end
            end
            ptx(i,j)=exp(1/a*log(pt(i))+b/a*d); 
        end
        else fprintf('error: p(t)=0 ot 1') ;
        end
    end
    ptx=centra(ptx,nt,nx);
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

%output mutual information
ditx=0;itx=0;ity=0;
for i=1:nt %I(T,X)
     if pt(i) ~=0&& pt(i)~=1
    for j=1:nx
        if ptx(i,j) ~=0
           itx=itx+ptx(i,j)*px(j)*(log((ptx(i,j)))-log(pt(i)));
        end
    end
     end
end

for i=1:nt %I(T,X)(a)
     if pt(i) ~=0 && pt(i)~=1
    for j=1:nx
        if ptx(i,j) ~=0
           ditx=ditx+ptx(i,j)*px(j)*(log((ptx(i,j))^a)-log(pt(i)));
        end
    end
     end
end
for i=1:nt %I(T,Y)
    if pt(i) ~=0 && pt(i)~=1
    for j=1:ny
        if pty(i,j) ~=0
           ity=ity+pty(i,j)*py(j)*(log(pty(i,j))-log(pt(i)));
        end
    end
    end
end
end