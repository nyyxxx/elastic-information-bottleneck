import numpy as np
import torch
import argparse
from utils import str2bool
from solver import Solver


def main(args):
    torch.backends.cudnn.enabled = True
    torch.backends.cudnn.benchmark = True

    seed = args.seed
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    np.random.seed(seed)

    np.set_printoptions(precision=4)
    torch.set_printoptions(precision=4)

    print()
    print('[ARGUMENTS]')
    print(args)
    print()

    net = Solver(args)
    if args.mode == 'train' : net.train()
    elif args.mode == 'test' : net.test(save_ckpt=False)
    else : return 0

if __name__ == "__main__":
    '''image = torch.load("D:\PycharmProjects\learn\VIB-pytorch-master\datasets\MNIST\MNIST\processed\\test.pt")
    print(image[0][0])
    print(0)'''

    parser = argparse.ArgumentParser(description='TOY VIB')
    print(1)
    #parser.add_argument('--epoch', default =100, type=int, help='epoch size')
    parser.add_argument('--lr', default = 1e-4, type=float, help='learning rate')
    print(2)
    #parser.add_argument('--beta', default = 8e-5, type=float, help='beta')
    parser.add_argument('--K', default = 256, type=int, help='dimension of encoding Z')
    parser.add_argument('--seed', default = 1, type=int, help='random seed')
    parser.add_argument('--num_avg', default = 12, type=int, help='the number of samples when\
            perform multi-shot prediction')
    parser.add_argument('--batch_size', default = 100, type=int, help='batch size')
    parser.add_argument('--env_name', default='main', type=str, help='visdom env name')
    parser.add_argument('--dataset', default='MNIST', type=str, help='dataset name')
    print(3)
    parser.add_argument('--dset_dir', default='datasets', type=str, help='dataset directory path')
    parser.add_argument('--summary_dir', default='summary', type=str, help='summary directory path')
    parser.add_argument('--ckpt_dir', default='checkpoints', type=str, help='checkpoint directory path')
    parser.add_argument('--load_ckpt',default='', type=str, help='checkpoint name')
    parser.add_argument('--cuda',default=True, type=str2bool, help='enable cuda')
    print(4)
    parser.add_argument('--mode',default='train', type=str, help='train or test')
    parser.add_argument('--tensorboard',default=False, type=str2bool, help='enable tensorboard')
    #args = parser.parse_args()
    parser.add_argument('--epoch', default=50, type=int, help='epoch size')
    parser.add_argument('--beta', default=1e-7, type=float, help='beta')
    args = parser.parse_args()
    for be in [1e-3]:
    #for be in [1e-8]:
        args.epoch = 50
        args.beta = be
        main(args)
    #main(args)