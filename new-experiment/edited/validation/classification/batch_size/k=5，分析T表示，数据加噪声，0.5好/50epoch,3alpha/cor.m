% mat=squeeze( t_rep(1,times,:,:));
% corrcoef(mat)
a=3;
mat5(:,1)=squeeze(t_rep(a,times,1:numtest,5));
mat5(:,2)=ones(numtest,1);
mat5(1:2:1000,2)=0;
corrcoef(mat5)
mat4(:,1)=squeeze(t_rep(a,times,1:numtest,4));
mat4(:,2)=ones(numtest,1);
mat4(1:2:1000,2)=0;
corrcoef(mat4)
mat3(:,1)=squeeze(t_rep(a,times,1:numtest,3));
mat3(:,2)=ones(numtest,1);
mat3(1:2:1000,2)=0;
corrcoef(mat3)
mat2(:,1)=squeeze(t_rep(a,times,1:numtest,2));
mat2(:,2)=ones(numtest,1);
mat2(1:2:1000,2)=0;
corrcoef(mat2)
mat1(:,1)=squeeze(t_rep(a,times,1:numtest,1));
mat1(:,2)=ones(numtest,1);
mat1(1:2:1000,2)=0;
corrcoef(mat1)