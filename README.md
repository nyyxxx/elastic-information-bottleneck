# elastic-information-bottleneck
The code is divided into 3 parts:

1. Implementation of IB, DIB, EIB iterative algorithms

2. Comparison of old and new generalization bounds

3. MNIST experiment: Implement IB, EIB, DIB with neural network by means of variational method of VIB and CEB.
MNIST experimental code is completed on the basis of code of (https://github.com/1Konny/VIB-pytorch)
Since the generalization bound is easy to generalize to the adversarial robust bound, PGD adversarial experiments of IB, EIB, and DIB are also done here (https://github.com/cleverhans-lab/cleverhans/blob/master/cleverhans/torch /attacks/projected_gradient_descent.py)

For details, see the corresponding chapters of the paper.

It is expected that more experiments will be completed in the future, including tests on large-scale datasets, as well as simulation experiments to study what kind of data EIB is more suitable for (see new experiment).

-----------------------------------------------------
Chinese version:
代码分为3部分：

1.IB、DIB、EIB迭代算法的实现

2.新旧泛化界的比较

3.MNIST实验：用神经网络实现IB、EIB、DIB，包括VIB、CEB两种思路。
MNIST实验代码在VIB代码(https://github.com/1Konny/VIB-pytorch )基础上完成
由于该泛化界很容易推广到对抗鲁棒界，因此这里还做了IB、EIB、DIB的PGD对抗实验（https://github.com/cleverhans-lab/cleverhans/blob/master/cleverhans/torch/attacks/projected_gradient_descent.py）

详细说明见论文相应章节。

预计后续还会完成更多实验，包括大规模数据集上的测试，以及研究EIB更适合什么样的数据的模拟实验（见new experiment)。
