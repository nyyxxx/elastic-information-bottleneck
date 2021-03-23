function [itx,ity,ditx,ptx,pt,pty]=dib(ptx,pt,pty,pyx,pxy,py,px,a,b,nx,ny,nt)
%执行AB算法一次更新,dib模式
for i=1:nt %p(t|x)
    if abs(pt(i)-1)<10^-3%???必须要这样？怎么解决1.0000不是1？
        itx=0;ity=0;ditx=0;
        return;
    end
end
    for j=1:nx
        for i=1:nt %p(t|x)
            %if pt(i) ~=0 && pt(i)~=1%这句位置不好，
            d=0;
            for k=1:ny
                if pty(i,k) ~=0
                d=d+pyx(k,j)*(log(pty(i,k))-log(pt(i)));
                end
            end        
            l(i)=log(pt(i))+b*d; 
            %else fprintf('error: p(t)=0 or 1,beta=%d\n',b) ;
            %end            
        end    
        ptx(:,j)=zeros(nt,1);
        [ml,index]=max(l);
        ptx(index,j)=1;
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

%output mutual information
itx=0;ity=0;
for i=1:nt %I(T,X)=H(T)
     if pt(i) ~=0 && pt(i)~=1
          itx=itx-pt(i)*log(pt(i));
       end
end
ditx=itx;
for i=1:nt %I(T,Y)
    for j=1:ny
        if pty(i,j) ~=0
           ity=ity+pty(i,j)*py(j)*(log(pty(i,j)));
        end
    end
end
    ity=itx-ity; %I(T,Y)=H(T)-H(T|Y)
end