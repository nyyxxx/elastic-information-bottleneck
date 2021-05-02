filepath='C:\Users\Yuyan\OneDrive\new-experiment\edited\validation\classification\batch_size\k=5，分析T表示，数据加噪声，0.5好';
a=[0,0.5,1];nk=5;na=3;
numtest=1000;%test和val样本个数
times=5;%epoch=100每十个epoch记录一次T 
 t_rep=zeros(3,times,numtest,nk);%num if k dim=nk,k>=2
for i=1:na%alpha=0 0.5 1
    for t=times
        alpha=a(i);
        filename_t="save_real_test_mu"+num2str(alpha)+"-"+"2.0.txt";
        file_t=fullfile(filepath,filename_t); 
        temp=importdata(file_t);
        for j=1:numtest
            str=char(temp((t-1)*numtest+2*j-1,1));        
            where1=strfind(str,'[');
            where2=strfind(str,',');
            where3=strfind(str,']');
            t_rep(i,t,j,1)=str2num(str(where1(2)+1:where2(1)-1));
            for k=2:nk-1
                t_rep(i,t,j,k)=str2num(str(where2(k-1)+1:where2(k)-1));
            end
            t_rep(i,t,j,nk)=str2num(str(where2(nk-1)+1:where3(1)-1));
%             if j/2==ceil(j/2)
%             plot3(t_rep(i,t,j,4),t_rep(i,t,j,1),t_rep(i,t,j,2),'or');
%             hold on
%             else
%                 plot3(t_rep(i,t,j,4),t_rep(i,t,j,1),t_rep(i,t,j,2),'*b');
%                 hold on
%             end
        end        
%         for d=1:nk
%         figure
% %         scatter(t_rep(i,t,1:2:numtest,d),t_rep(i,t,2:2:numtest,d));
% %         hold on
% %         plot([min(t_rep(i,t,1:2:numtest,d)),max(t_rep(i,t,1:2:numtest,d))],[min(t_rep(i,t,1:2:numtest,d)),max(t_rep(i,t,1:2:numtest,d))]);
% %         title("alpha="+num2str(alpha)+",epoch="+num2str(t*10)+",dim="+num2str(d));
% %         hold off
%         end
         
%         hold on
%         scatter(t_rep(i,t,2:2:numtest,4),t_rep(i,t,2:2:numtest,1));      
%         hold off
%         figure
    end
           t_rep(i,t,:,:); 
end
% (t_rep(1,10,1,1)-t_rep(1,10,2,1))^2+(t_rep(1,10,1,2)-t_rep(1,10,2,2))^2