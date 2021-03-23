function [ppt,ppty,iity,hhty,hht,iixt] = cal_t(ny,nx,nt,ptx,ppx,ppxy,ppy);
for i=1:nt %pp(t)
    ppt(i)=0;
    for j=1:nx
        for k=1:ny
           ppt(i)=ppt(i)+ptx(i,j)*ppxy(j,k)*ppy(k);
        end
    end
end
for i=1:nt %pp(t|y)
     for k=1:ny
        ppty(i,k)=0;
        for j=1:nx       
           ppty(i,k)=ppty(i,k)+ptx(i,j)*ppxy(j,k);
        end
     end
end
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

