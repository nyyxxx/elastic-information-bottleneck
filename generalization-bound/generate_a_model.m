function ptx = generate_a_model(nx,nt)
%������Ӧ��ʹ��IBģ����ptx������Bound��ģ���޹أ�����ѡһ�������ڼ����ptx
z =rand(nt,nx);
ptx=centra(z,nt,nx);
end

