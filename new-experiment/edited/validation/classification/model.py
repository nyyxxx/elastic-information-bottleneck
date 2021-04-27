import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.init as init
from torch.autograd import Variable
from utils import cuda
import numpy as np
import time
from numbers import Number

class ToyNet(nn.Module):

    def __init__(self, K, args):
        super(ToyNet, self).__init__()
        self.K = K
        self.batch_size = args.batch_size

        self.encode = nn.Sequential(
            nn.Linear(10, 8),
            nn.ReLU(True),
            nn.Linear(8, 6),
            nn.ReLU(True),
            nn.Linear(6, 2*self.K)  )#简单网络 x-z 得z(mu,std)

        self.decode = nn.Sequential(
                nn.Linear(self.K, 2))#一层线性  z-y# dim y=2
        self.bwencode = nn.Sequential(
            nn.Linear(2, 2*self.K))# !!# dim y=2
           

    def forward(self, x, num_sample=1):
        if x.dim() > 2 : x = x.view(x.size(0),-1)
  
        statistics = self.encode(x)
        mu = statistics[:,:self.K]
        std = F.softplus(statistics[:,self.K:]-5,beta=1)

        encoding = self.reparametrize_n(mu,std,num_sample)
        logit = self.decode(encoding)
    
#        statistics = self.encode(x)
#        mu = statistics[:,:self.K]
#        std = F.softplus(statistics[:,self.K:]-5,beta=1)#1/beta*log(1+exp(beta*x))
#        encoding = self.reparametrize_n(mu,std,num_sample)#        
#        logit = self.decode(encoding)
#        logit = F.softmax(logit, dim=1).mean(0)        
#        index = logit.max(0)[1]       
#        one_hot = torch.zeros(2).scatter(0, index, 1)# dim y=2
                               # one_hot = torch.nn.functional.one_hot(logit, n)   #changed@@@
        if logit.size()[0]==self.batch_size:
            index = F.softmax(logit, dim=1).max(1)[1][:, np.newaxis]
        #print(index,'haha')
            one_hot = torch.zeros(self.batch_size, 2).scatter(1, index, 1)
        elif logit.size()[0]==1:
            index = F.softmax(logit, dim=1).max(1)[1][:, np.newaxis]
            one_hot = torch.zeros(self.batch_size, 2).scatter(1, index, 1)
        else:
            index = F.softmax(logit, dim=2).max(2)[1][:,:, np.newaxis]
            one_hot = torch.zeros(12, self.batch_size, 2).scatter(-1, index, 1)
        
#        statistics2 = self.bwencode(one_hot) #!!!
#        mu2 = statistics2[:self.K]
#        std2 = F.softplus(statistics2[self.K:]-5,beta=1)
        
        statistics2 = self.bwencode(one_hot)  # !!!
        mu2 = statistics2[:, :self.K]
        std2 = F.softplus(statistics2[:, self.K:] - 5, beta=1)
        if num_sample == 1:
            pass
        elif num_sample > 1:
            logit = F.softmax(logit, dim=2).mean(0)
            
       # if num_sample == 1 : pass
       # elif num_sample > 1 : logit = F.softmax(logit, dim=2).mean(0)   #changed@@@
       # #consistent classifier：logit=F.softmax(logit, dim=2).mean(0)
        return (mu, std), logit,(mu2, std2)#!!!

    def reparametrize_n(self, mu, std, n=1):
        # reference :
        # http://pytorch.org/docs/0.3.1/_modules/torch/distributions.html#Distribution.sample_n
        def expand(v):
            if isinstance(v, Number):
                return torch.Tensor([v]).expand(n, 1)
            else:
                return v.expand(n, *v.size())

        if n != 1 :
            mu = expand(mu)
            std = expand(std)

        eps = Variable(cuda(std.data.new(std.size()).normal_(), std.is_cuda))

        return mu + eps * std

    def weight_init(self):
        for m in self._modules:
            xavier_init(self._modules[m])


def xavier_init(ms):
    for m in ms :
        if isinstance(m, nn.Linear) or isinstance(m, nn.Conv2d):
            nn.init.xavier_uniform(m.weight,gain=nn.init.calculate_gain('relu'))
            m.bias.data.zero_()
