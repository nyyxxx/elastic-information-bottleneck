function [ppt,ppty,iity,hhty,hht,iixt] = cal_t(ny,nx,nt,ptx,ppx,ppxy,ppy);
% for i=1:nt %pp(t)
%     ppt(i)=0;
%     for j=1:nx
%         for k=1:ny
%            ppt(i)=ppt(i)+ptx(i,j)*ppxy(j,k)*ppy(k);
%         end
%     end
% end
ppty=ptx*ppxy;
ppt=ppty*ppy;
% for i=1:nt %pp(t|y)
%      for k=1:ny
%         ppty(i,k)=0;
%         for j=1:nx       
%            ppty(i,k)=ppty(i,k)+ptx(i,j)*ppxy(j,k);
%         end
%      end
% end
[hht,hhty,iity,iixt] = cal_hi(ny,nx,nt,ppy,ppx,ppt,ptx,ppty);
end

