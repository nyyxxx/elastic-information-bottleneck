function [a] = min0(p,n1,n2)
%����p(n1*n2)��������С�����Ԫ��
a=1;
for i=1:n1
    for j=1:n2
        if p(i,j)<a && p(i,j)~=0
            a=p(i,j);
        end
    end
    
end

