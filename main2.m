%不均匀的初始化对界的影响
clear
ntimes=9;nrpt=100;
 times=[1,5,10,50,100,500,1000,2000,5000];
 rv=zeros(1,ntimes);
 ob=zeros(1,ntimes);
 nb=zeros(1,ntimes);
 nber=zeros(1,ntimes);
 ober=zeros(1,ntimes);
nx=3;ny=2; nt=2;
delta=0.1;
 for in=1:ntimes
     m=10*times(in);%#sample  
    [rv(in),ob(in),nb(in),ober(in),nber(in)] = bound_simul(m,delta,nx,ny,nt);
end

%plot
 plot(10*times,nb,'*');
 hold on;
plot(10*times,ob,'*');
 hold on;
   plot(10*times,rv,'-');
  hold on;

