clear
ntimes=20;
 times=[1:50:1000];
 rv=zeros(1,ntimes);
 ob=zeros(1,ntimes);
 nb=zeros(1,ntimes);

m=1000;%#sample 
 for in=1:ntimes
      delta=times(in)*0.0001;
nx=3;ny=2; nt=2;
%Theoretic value
py=[1/2,1/2]';
pxy=[1/2,1/2,0;0,1/2,1/2]';
px=[1/4,1/2,1/4]';
ptx=[1,0;1/2,1/2;0,1]';
pt=[1/2,1/2]';
pty=[3/4,1/4;1/4,3/4]';
ht=log(2);
hty=2*log(2)-(3/4)*log(3);
ity=(3/4)*log(3)-log(2);
ixt=1/2*log(2);
%Empirical value
v=rand(m,1);
sp=zeros(m,3);
for i=1:m
    if v(i)<1/4 sp(i,:)=[1,1,1];
    else if v(i)>3/4 sp(i,:)=[2,3,2];
        else  
            if v(i)>1/2 sp(i,1)=2;
            else sp(i,1)=1;
            end            
            if rand(1,1)>1/2 sp(i,2:3)=[2,1];
            else sp(i,2:3)=[2,2];
            end
        end
    end
end
t=count(mat2str(sp(:,1)),'1')/m;
ppy=[t,1-t];
t=count(mat2str(sp(:,2)),'1')/m;
s=count(mat2str(sp(:,2)),'2')/m;
ppx=[t,s,1-t-s];
% t=count(mat2str(sp(:,3)),'1')/m;
% ppt=[t,1-t];
ppxy=zeros(nx,ny);
%pptx=zeros(nt,nx);
for i=1:ny
    for j=1:nx
        for k=1:m
            if sp(k,1:2)==[i,j]
                ppxy(j,i)=ppxy(j,i)+1/(m*ppy(i));
            end
        end
    end
%     for j=1:nt
%         for k=1:m
%             if sp(k,2:3)==[i,j]
%                 pptx(j,i)=pptx(j,i)+1/m;
%             end
%         end
%     end
end
 [ppt,ppty,iity,hhty,hht,iixt] = cal_t(ny,nx,nt,ptx,ppx,ppxy,ppy);
%   for in=1:ntimes
%       delta=times(in)*0.0001;
 %original bound
    c=(2+sqrt(2*log((ny+2)/delta)))/sqrt(m);
    g1=c*2*sqrt(2*log(2))/min(px);%ppx or px?
    s2=2*g1*(-log(g1)*sqrt(nt*ixt)+nt^(3/4)*(ixt)^(1/4));
    s1=c*2/(min(py))*iixt;
    ob(in)=s1+s2;
 %new bound
    g2=c/sqrt(min(px));
    c1=-g2*log(g2);
    c2=g2/sqrt(min(pt));
    g3=c/sqrt(min0(pxy,nx,ny));
    c3=-g3*log(g3);
    c4=g3/sqrt(min(min(pty)));
    c5=c/sqrt(min(ppy));
    nb(in)=(c1+c3)*sqrt(nt-1)+c2*ht+c4*hty+c5*sqrt(hhty*(log(nt)-hhty));
  %real value
     rv(in)=abs(ity-iity);
 %fprintf("#sample=%d,real value=%d,original bound=%d,new bound=%d\n",m,rv,ob,nb);
 
 end
 plot(times*0.0001,nb,'*');
 hold on;
 plot(times*0.0001,rv,'-');
 hold on;
  plot(times*0.0001,ob,'o');
  hold off;