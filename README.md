# elastic-information-bottleneck
代码分为3部分：

1.IB、DIB、EIB迭代算法的实现

2.新旧泛化界的比较

3.MNIST实验：用神经网络实现IB、EIB、DIB，包括VIB、CEB两种思路。
MNIST实验代码在VIB代码基础上完成，感谢前人：https://github.com/1Konny/VIB-pytorch ！
PGD对抗实验：（https://github.com/cleverhans-lab/cleverhans/blob/master/cleverhans/torch/attacks/projected_gradient_descent.py）

详细说明见论文相应章节。

预计后续还会完成更多实验，包括大规模数据集上的测试，以及研究EIB更适合什么样的数据的模拟实验（见new experiment)。
