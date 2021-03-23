%两个界比较
clear
ntimes=13;maxnrpt=10;nrpt=20;
 times=[1,2,5,10,20,50,100,150,200,250,300,350,400];
 rv=zeros(1,ntimes);
 ob=zeros(1,ntimes);
 nb=zeros(1,ntimes);
%#sample 
delta=0.1;
nx=3;ny=2; nt=2;
for in=1:ntimes
     m=5000*times(in);
    for j=1:nrpt
        ober=1;
        nber=1;
        i=0;
        while (ober==1||nber==1) && i<maxnrpt
            i=i+1;
            [a(j),b(j),c(j),ober,nber] = bound_simul(m,delta,nx,ny,nt);
        end
    end
    rv(in)=mean(a);
    ob(in)=mean(b);
    nb(in)=mean(c);
    
end
%plot
 plot(5000*times,nb,'*');
 hold on;
plot(5000*times,ob,'*');
 hold on;
   plot(5000*times,rv,'-');
  hold off;

