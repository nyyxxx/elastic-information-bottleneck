function [ppy,ppx,ppxy] = sample_xy(m,nx,ny,py,px,pxy,jxy)
%从给定的p(x,y)中抽样
v=rand(m,1);
cumu=0;
for i=1:nx
    for j=1:ny
        l=cnt(v,m,cumu,cumu+jxy(i,j));
        jjxy(i,j)=(l)/m;
        cumu=cumu+jxy(i,j);
    end
end
ppy=sum(jjxy)';
ppx=sum(jjxy')';
ppxy=(jjxy'./ppy)';
end

