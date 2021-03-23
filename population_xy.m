function [py,pxy,px,jxy] = population_xy(ny,nx)
%生成一个总体分布,y均匀，p(x|y)为中心不同的正态分布

py=ones(ny,1)*(1/ny);


z =rand(nx,ny);
pxy=centra(z,nx,ny);

px=pxy*py;

jxy=zeros(nx,ny);%joint distribution p(x,y)
for i=1:nx
    for j=1:ny
        jxy(i,j)=pxy(i,j)*py(j);
    end
end
end

