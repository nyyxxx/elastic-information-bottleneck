%initialization pxy a  max_initial  max_iterate
clear
ny=2;nx=10;nt=3;
[py,pxy,px,pyx,ixy] = initial_xy(ny,nx);
a=0; %alpha
fprintf('alpha=%f\n', a);
times_initial=2 ;% number of times to randonly initialize t
max_iterate=5; % max number of interations in BA algorism

for be=1:8% 对每个beta计算ib curve 的坐标
    b=be*100+1;%beta=b
    [ix(be),dix(be),iy(be)] = calculate_ib_quantities(py,pxy,px,pyx,ixy,a,b,ny,nx,nt,times_initial,max_iterate);
end
% 画两种ib curve
subplot(2,1,1);
cmp = jet(be); % create the color maps changed as in jet color map
scatter(ix, iy, 20, cmp, 'filled');
a=gca;
set(a,'XLim',[0, max(ix)*1.1],'YLim',[0, ixy*1.1]);
a.YAxisLocation='origin';
a.XAxisLocation='origin';
hold on;
 plot([0,ix(be)],[ixy,ixy]);
 hold off;
plot(ix,iy);
% subplot(2,1,2);
% cmp = jet(be); % create the color maps changed as in jet color map
% scatter(dix, iy, 20, cmp, 'filled');
% a=gca;
% set(a,'XLim',[0, max(ix)*1.1],'YLim',[0, ixy*1.1]);
% a.YAxisLocation='origin';
% a.XAxisLocation='origin';
% hold on;
%  plot([0,ix(be)],[ixy,ixy]);
%  hold off;