%不均匀的初始化对界的影响
clear
ntimes=10;nrpt=100;
 times=[1,10,50,100,500,1000,2000,5000,10000,50000];
 rv=zeros(1,ntimes);
 ob=zeros(1,ntimes);
 nb=zeros(1,ntimes);
 nber=zeros(1,ntimes);
 ober=zeros(1,ntimes);
nx=3;ny=2; nt=2;
delta=0.1;
 for in=1:ntimes
     m=10*times(in);%#sample 
     nober=0;
     nnber=0;
     for i=1:nrpt
         [rv(in),ob(in),nb(in),ober(in),nber(in)] = bound_simul(m,delta,nx,ny,nt);
         nober=nober+ober(in);
         nnber=nnber+nber(in);
     end
    er1(in)=nober/nrpt;
    er2(in)=nnber/nrpt;
end

%plot
 plot(10*times,er1,'*');
 hold on;
plot(10*times,er2,'*');
 hold on;

