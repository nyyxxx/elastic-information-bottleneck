function n=cnt(v,m,a,b)
%返回v中在（a,b]中的值的个数,m是v数组长度
n=0;
for i=1:m
    if v(i)<=b &&v(i)>a  
        n=n+1;
    end
end       
end

