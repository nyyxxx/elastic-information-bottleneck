function ptx = generate_a_model(nx,nt)
%理论上应当使用IB模型求ptx，由于Bound与模型无关，我们选一个更便于计算的ptx
z =rand(nt,nx);
ptx=centra(z,nt,nx);
end

