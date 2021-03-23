function [mtx2] = centra(mtx,ni,nj)
%centralization of a probability matrix:mtx,size=ni*nj
%注意有inf的情况
mtx2=zeros(ni,nj);
for j=1:nj
    mn=min(mtx(1:ni,j));
    if mn<0
    mtx(1:ni,j)=mtx(1:ni,j)-mn+0.01;
    end
    s=sum(mtx(1:ni,j));    
    for i=1:ni     
        mtx2(i,j)=(mtx(i,j))/s;
    end
  
end
end


