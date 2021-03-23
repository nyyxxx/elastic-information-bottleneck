function [hht,hhty,iity,iixt] = cal_hi(ny,nx,nt,ppy,ppx,ppt,ptx,ppty)
%计算互信息与信息熵
hht=0;hhty=0;
for i=1:nt %I(T,Y)
    if ppt(i) ~=0 && ppt(i)~=1
    for j=1:ny
        if ppty(i,j) ~=0
            hht=hht-ppty(i,j)*ppy(j)*log(ppt(i));
           hhty=hhty-ppty(i,j)*ppy(j)*log(ppty(i,j));
        end
    end
    end
end
iity=hht-hhty;
iixt=0;
for i=1:nt%I(X,T) 
     if ppt(i) ~=0&& ppt(i)~=1
    for j=1:nx
        if ptx(i,j) ~=0
           iixt=iixt+ptx(i,j)*ppx(j)*(log((ptx(i,j)))-log(ppt(i)));
        end
    end
     end
end
end

