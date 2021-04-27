filepath='C:\study\codes\git\elastic-information-bottleneck\new-experiment\edited\validation\classification\batch_size';
% a=[0,0.3 0.4 0.5 0.6 0.7 1];na=7;epc=100;
 a=[0,0.5,1];na=3;epc=100;
acc_t=zeros(na,epc);
acc_rtr=zeros(na,epc);
cmap=colormap(jet);
m=floor(linspace(1,64,na));

for i=1:na%alpha=0 0.5 1
        alpha=a(i);
%         filename_t=" test_class_loss"+num2str(alpha)+"-"+"2.0.txt";
%        filename_rtr=" real_test_class_loss"+num2str(alpha)+"-"+"2.0.txt";
        filename_t="test_accuracy"+num2str(alpha)+"-"+"2.0.txt";
        filename_rtr="real_test_accuracy"+num2str(alpha)+"-"+"2.0.txt";
        file_t=fullfile(filepath,filename_t);      % 导入.txt文件
        temp=importdata(file_t);
        len=length(temp);
        acc_t(i,:)=temp(len-epc+1:len);
        file_rtr=fullfile(filepath,filename_rtr);      % 导入.txt文件
         temp=importdata(file_rtr);
        len=length(temp);
        acc_rtr(i,:)=temp(len-epc+1:len);        
        p1(i)=plot(acc_t(i,:),'--','color',cmap(m(i),:));
        hold on
        p2(i)=plot(acc_rtr(i,:),'-','color',cmap(m(i),:));
        hold on
%         
%         legend([p1(i) p2(i)],{"α="+num2str(alpha)+",val","α="+num2str(alpha)+"test"})
end
  xlabel('epochs');
ylabel('test cross entropy loss');
ylabel('test accuracy');


hold off
% legend('alpha_t=0','alpha_t=0','alpha=0.5 ','alpha=1');