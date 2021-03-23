function [mtx2] = centra(mtx,ni,nj)
%centralization of a probability matrix:mtx,size=ni*nj
%注意有inf的情况
mtx2=zeros(ni,nj);
for j=1:nj
    s=sum(mtx(1:ni,j));
    if s==inf
        for i=1:ni     
        if mtx(i,j)== inf
            mtx2(i,j)=1;
        end
        end
        mtx2(1:ni,j)=centra(mtx2(1:ni,j),ni,1);
    else
    for i=1:ni     
        mtx2(i,j)=(mtx(i,j))/s;
    end
    end
end
end

