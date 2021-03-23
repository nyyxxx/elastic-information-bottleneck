%initialization
clear
ny=2;nx=10;nt=3;
a=0.2;
fprintf('alpha=%f\n', a);
cnt1=0;cnt2=0;
for be=1:160
    b=be*5+1;%beta=b
[py,pxy,ptx,px,pyx,pt,pty,ixy]=initial_hand(ny,nx,nt);

%iteration
n=0;
while n<4
    for i=1:nt %p(t|x)
        for j=1:nx
            d=0;
            for k=1:ny
                d=d+pyx(k,j)*(log(pty(i,k))-log(pt(i)));
            end
            ptx(i,j)=exp(1/a*log(pt(i))+b/a*d); 
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
    n=n+1;
end

%output mutual information
itx=0;ity=0;
for i=1:nt %I(T,X)(a)
    for j=1:nx
           itx=itx+ptx(i,j)*px(j)*(log((ptx(i,j))^a)-log(pt(i)));
        end
    end
for i=1:nt %I(T,Y)
    for j=1:ny
           ity=ity+pty(i,j)*py(j)*(log(pty(i,j))-log(pt(i)));
        end
end
ix(be)=itx; iy(be)=ity;  
if ity>0.001  
    cnt1=cnt1+1;
end
if ity>ixy/2 
    cnt2=cnt2+1;
end

%second order variation
%  for i=1:nt 
%         for j=1:nx
%             d=0;
%             for k=1:ny
%                 d=d+pyx(k,j)*pxy(j,k)/pty(i,k);
%             end
%             v2(i,j,be)=(b-1)*px(j)/pt(i)+a/ptx(i,j)-b*d;
%         end
%  end

% nn(be)=0;
%     for i=1:nx %tell if it is saddlepoints
%         for j=1:nt
%            if(px(i)*ptx(j,i)>a*pt(j))
%                nn(be)=nn(be)+1;
%            end
%         end
%     end

end


fprintf('#ity>0.01=%d\t #ity>ixy/2=%d\n', cnt1,cnt2);
plot(ix,iy,'+');
hold on;
 plot([ix(1),ix(be)],[iy(1),iy(be)]);
 hold on;
 %plot([0,ix(be)],[ixy,ixy]);
 hold off;

