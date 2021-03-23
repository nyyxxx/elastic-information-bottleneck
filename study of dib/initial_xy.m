function [py,pxy,px,pyx,ixy] = initial_xy(ny,nx)
%initialization
%   此处显示详细说明
px=centra(abs(randn(nx,1)),nx,1);%注意centra只用于列向量
pyx=centra(abs(randn(ny,nx)),ny,nx);%p(y|x)
for i=1:ny %p(y)
    py(i)=0;
      for j=1:nx
           py(i)=py(i)+pyx(i,j)*px(j);
      end
end
for j=1:nx %p(x|y)
     for i=1:ny     
         if py(i)==0
             fprintf('error: py(%d)=0',i);
         else
        pxy(j,i)=pyx(i,j)*px(j)/py(i);
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

