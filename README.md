# Elastic Information Bottleneck
This is the code for *Elastic Information Bottleneck* ([paper link](https://www.mdpi.com/2227-7390/10/18/3352)).
## Abstract
Information bottleneck is an information-theoretic principle of representation learning that aims to learn a maximally compressed representation that preserves as much information about labels as possible. Under this principle, two different methods have been proposed, i.e., information bottleneck (IB) and deterministic information bottleneck (DIB), and have gained significant progress in explaining the representation mechanisms of deep learning algorithms. However, these theoretical and empirical successes are only valid with the assumption that training and test data are drawn from the same distribution, which is clearly not satisfied in many real-world applications. In this paper, we study their generalization abilities within a transfer learning scenario, where the target error could be decomposed into three components, i.e., source empirical error, source generalization gap (SG), and representation discrepancy (RD). Comparing IB and DIB on these terms, we prove that DIB’s SG bound is tighter than IB’s while DIB’s RD is larger than IB’s. Therefore, it is difficult to tell which one is better. To balance the trade-off between SG and the RD, we propose an elastic information bottleneck (EIB) to interpolate between the IB and DIB regularizers, which guarantees a Pareto frontier within the IB framework. Additionally, simulations and real data experiments show that EIB has the ability to achieve better domain adaptation results than IB and DIB, which validates the correctness of our theories.
Keywords: information bottleneck; transfer learning; generalization bound
## Code Description
The code is divided into 3 parts:

1. Implementation of IB, DIB, EIB iterative algorithms

2. Comparison of old and new generalization bounds

3. MNIST experiment: Implement IB, EIB, DIB with neural network by means of variational method of VIB and CEB.
MNIST experimental code is completed on the basis of code of (https://github.com/1Konny/VIB-pytorch)
Since the generalization bound is easy to generalize to the adversarial robust bound, PGD adversarial experiments of IB, EIB, and DIB are also done here.

For details, see the corresponding chapters of the paper.

It is expected that more experiments will be completed in the future, including tests on large-scale datasets, as well as simulation experiments to study what kind of data EIB is more suitable for (see new experiment).


## Citation
    @article{ni2022elastic,
      title={Elastic Information Bottleneck},
      author={Ni, Yuyan and Lan, Yanyan and Liu, Ao and Ma, Zhiming},
      journal={Mathematics},
      volume={10},
      number={18},
      pages={3352},
      year={2022},
      publisher={MDPI}
    }
