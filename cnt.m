function n=cnt(v,m,a,b)
%����v���ڣ�a,b]�е�ֵ�ĸ���,m��v���鳤��
n=0;
for i=1:m
    if v(i)<=b &&v(i)>a  
        n=n+1;
    end
end       
end

