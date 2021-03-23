function [mtx2] = centra(mtx,ni,nj)
%centralization of a probability matrix:mtx,size=ni*nj
for j=1:nj
    s=sum(mtx(1:ni,j));
    for i=1:ni     
        mtx2(i,j)=(mtx(i,j))/s;
    end
end
end

