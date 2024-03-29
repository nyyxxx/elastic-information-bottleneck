import numpy as np
import torch
import argparse
import math
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.autograd import Variable
from torch.optim import lr_scheduler
from torch.utils.data import DataLoader
from torchvision import transforms
from tensorboardX import SummaryWriter
from utils import cuda, Weight_EMA_Update
#from datasets.datasets import return_data
from model import ToyNet
from pathlib import Path
import pprint

class Solver(object):

    def __init__(self, args):
        self.args = args

        self.cuda = (args.cuda and torch.cuda.is_available())
        self.epoch = args.epoch
        self.batch_size = args.batch_size
        self.lr = args.lr
        self.eps = 1e-9
        self.K = args.K
        self.beta = args.beta
        self.num_avg = args.num_avg
        self.global_iter = 0
        self.global_epoch = 0
        self.alpha=1

        # Network & Optimizer
        self.toynet = cuda(ToyNet(self.K, self.args), self.cuda)
        self.toynet.weight_init()
        self.toynet_ema = Weight_EMA_Update(cuda(ToyNet(self.K, self.args), self.cuda),\
                self.toynet.state_dict(), decay=0.999)

        self.optim = optim.Adam(self.toynet.parameters(),lr=self.lr,betas=(0.5,0.999))
        self.scheduler = lr_scheduler.ExponentialLR(self.optim,gamma=0.97)

        self.ckpt_dir = Path(args.ckpt_dir).joinpath(args.env_name)
        if not self.ckpt_dir.exists() : self.ckpt_dir.mkdir(parents=True,exist_ok=True)
        self.load_ckpt = args.load_ckpt
        if self.load_ckpt != '' : self.load_checkpoint(self.load_ckpt)

        # History
        self.history = dict()
        self.history['acc']=0.
        self.history['info_loss']=0.
        self.history['class_loss']=0.
        self.history['total_loss']=0.
        self.history['epoch']=0
        self.history['iter']=0

        # Tensorboard
        self.tensorboard = args.tensorboard
        if self.tensorboard :
            self.env_name = args.env_name
            self.summary_dir = Path(args.summary_dir).joinpath(args.env_name)
            if not self.summary_dir.exists() : self.summary_dir.mkdir(parents=True,exist_ok=True)
            self.tf = SummaryWriter(log_dir=self.summary_dir)
            self.tf.add_text(tag='argument',text_string=str(args),global_step=self.global_epoch)

        # Dataset
       # self.data_loader = return_data(args)


    def set_mode(self,mode='train'):
        if mode == 'train' :
            self.toynet.train()
            self.toynet_ema.model.train()
        elif mode == 'eval' :
            self.toynet.eval()
            self.toynet_ema.model.eval()
        elif mode == 'real_test' :###!!!!!
            self.toynet.real_test()###!!!!!
            self.toynet_ema.model.real_test()###!!!!!
        else : raise('mode error. It should be either train or eval or real_test')###!!!!!

    def train(self):
        train_data=[]
        for line in open('samples.txt', "r"):
            train_data.append(line.split('\t'))
        for entry in train_data:
            entry.remove('\n')
        for entry in train_data:
            for i in range(len(entry)):
                entry[i]=float(entry[i])
        train_label = []
        for line in open('samples_y.txt', "r"):
            train_label.append(line.split('\n'))
        for entry in train_label:
            entry.remove('')
        for entry in train_label:
            for i in range(len(entry)):
                entry[i] = float(entry[i])
        self.set_mode('train')
        for e in range(self.epoch) :
            self.global_epoch += 1

            #for idx, (images,labels) in enumerate(self.data_loader['train']):
            for num_in_batch in range(0,int(len(train_label)/self.batch_size) ):#暂时没管不整除的情况
                self.global_iter += 1
                
                images=torch.Tensor(train_data[num_in_batch*self.batch_size : (num_in_batch+1)*self.batch_size])
                labels=torch.LongTensor(train_label[num_in_batch*self.batch_size : (num_in_batch+1)*self.batch_size   ])
                x = Variable(cuda(images, self.cuda))
                y = Variable(cuda(labels, self.cuda))
#                print(x.shape)
#                print(y)
                
                (mu, std), logit ,(mu2, std2)= self.toynet(x)#!!!
               
                '''
                print(mu.shape)
                print(std.shape)
                print(logit.shape)'''

                '''class_loss = F.cross_entropy(logit,y).div(math.log(2))
                info_loss = -0.5*(0.25+0.5*std.log()-mu.pow(2)-std.pow(2)).sum(1).mean().div(math.log(2))
                total_loss = class_loss + self.beta*info_loss
                izy_bound = math.log(10,2) - class_loss
                izx_bound = info_loss'''
                alpha = self.alpha
#                y= torch.zeros(2).scatter(0, y, 1)
                class_loss =F.cross_entropy(logit, y.squeeze(1)).div(math.log(2))
#                class_loss = F.cross_entropy(logit, y).div(math.log(2))
#                class_loss = F.cross_entropy(logit, y).div(math.log(2))
                #info_loss = (-0.5 * alpha - alpha * std.log() + 0.5 * (mu.pow(2) + std.pow(2)) + (
                #        1 - alpha) * 0.5 * math.log(2 * math.pi)).sum(1).mean().div(math.log(2))
                info_loss = (-0.5 * alpha - alpha * std.log() + std2.log() + 0.5 * (
                            mu.pow(2) + mu2.pow(2) - 2 * mu * mu2 + std.pow(2)) / (std2.pow(2)) + (
                                     1 - alpha) * 0.5 * math.log(2 * math.pi)).sum(1).mean().div(math.log(2))
                total_loss = class_loss + self.beta * info_loss

#                izy_bound = math.log(10, 2) - class_loss
                '''print((0.5*(mu.pow(2) + std.pow(2) + math.log(2 * math.pi))).shape)
                print((0.5*(mu.pow(2) + std.pow(2) + math.log(2 * math.pi))).sum(1).shape)
                print((0.5*(mu.pow(2) + std.pow(2) + math.log(2 * math.pi))).sum(1).mean())'''
                '''ht_bound = (0.5*(mu.pow(2) + std.pow(2) + math.log(2 * math.pi))).sum(1).mean().div(math.log(2))
                htx_bound = (0.5 * math.log(2 * math.pi ) +std.log()+ 0.5).sum(1).mean().div(math.log(2))
                izx_bound = -0.5 * (1 + 2 * std.log() - mu.pow(2) - std.pow(2)).sum(1).mean().div(math.log(2))'''
                # izx_bound = info_loss
#                htx_bound = (0.5 * math.log(2 * math.pi) + std.log() + 0.5).sum(1).mean().div(math.log(2))
#                hty_bound = (0.5 * math.log(2 * math.pi) + std2.log() + 0.5).sum(1).mean().div(math.log(2))  # !!!
#                ht_bound = hty_bound + izy_bound  # H(T)=H(T|Y)+I(T,Y)!!!
#                izx_bound = ht_bound - htx_bound  # I(T,X)=H(T)-H(T|X)!!!
                '''if info_loss != ht_bound - alpha * htx_bound:
                    print(info_loss)
                    print(ht_bound-alpha*htx_bound)
                    print(".................................................")
                    break'''

                self.optim.zero_grad()
                total_loss.backward()
                self.optim.step()
                self.toynet_ema.update(self.toynet.state_dict())

                prediction = F.softmax(logit,dim=1).max(1)[1]
                accuracy = torch.eq(prediction,y).float().mean()
                #print(F.softmax(logit,dim=1)[0])

                if self.num_avg != 0 :
                    _, avg_soft_logit,_ = self.toynet(x,self.num_avg)
                    '''print(avg_soft_logit[0])
                    print(type(avg_soft_logit.max(1)))
                    print(avg_soft_logit.max(1)[1])
                    while(1):
                        a=1'''
                    avg_prediction = avg_soft_logit.max(1)[1]
                    avg_accuracy = torch.eq(avg_prediction,y).float().mean()
                else : avg_accuracy = Variable(cuda(torch.zeros(accuracy.size()), self.cuda))

                if self.global_iter % 5 == 0 :
#                    print(' class_loss:{:.2f} info_loss:{:.2f}' 
#                            .format( class_loss.item(), info_loss.item()), end=' ')
#                    
##                    print(' IZY:{:.2f} IZX:{:.2f}'
##                            .format( izy_bound.item(), izx_bound.item()), end=' ')
                    print('acc:{:.4f} avg_acc:{:.4f}'
                            .format(accuracy.item(), avg_accuracy.item()), end=' ')
#                    print('err:{:.4f} avg_err:{:.4f}'
#                            .format(1-accuracy.item(), 1-avg_accuracy.item()))

                if self.global_iter % 100 == 0 :
                    with open(' train_class_loss'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
                        f.write(str( class_loss.item()) + '\n')
                    with open(' train_info_loss'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
                        f.write(str( info_loss.item()) + '\n')
                    with open(' train_total_loss'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
                        f.write(str( total_loss.item()) + '\n')
                    with open(' train_mu'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
                        f.write(str( mu) + '\n')
                    with open(' train_std'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
                        f.write(str( std) + '\n')
                    with open(' train_mu2'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
                        f.write(str( mu2) + '\n')
                    with open(' train_std2'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
                        f.write(str( std2) + '\n')
#                    with open('train_ht_bound'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
#                        f.write(str(ht_bound.item()) + '\n')
#                    with open('train_htx_bound'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
#                        f.write(str(htx_bound.item()) + '\n')
#                    with open('train_izy_bound'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
#                        f.write(str(izy_bound.item()) + '\n')
#                    with open('train_izx_bound'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
#                        f.write(str(izx_bound.item()) + '\n')
                    with open('train_accuracy'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
                        f.write(str(accuracy.item()) + '\n')
#                    with open('train_avg_accuracy'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
#                        f.write(str(avg_accuracy.item()) + '\n')
#                    with open('train_error'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
#                        f.write(str(1-accuracy.item()) + '\n')
#                    with open('train_avg_error'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
#                        f.write(str(1-avg_accuracy.item()) + '\n')
#                    with open('train_error'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
#                        f.write(str(1-accuracy.item()) + '\n')
#                    with open('train_class_loss'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
#                        f.write(str(class_loss.item()) + '\n')
#                    with open('train_info_loss'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
#                        f.write(str(info_loss.item()) + '\n')
#                    with open('train_total_loss'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
#                        f.write(str(total_loss.item()) + '\n')
                    if self.tensorboard :
                        self.tf.add_scalars(main_tag='performance/accuracy',
                                            tag_scalar_dict={
                                                'train_one-shot':accuracy.item(),
                                                'train_multi-shot':avg_accuracy.item()},
                                            global_step=self.global_iter)
                        self.tf.add_scalars(main_tag='performance/error',
                                            tag_scalar_dict={
                                                'train_one-shot':1-accuracy.item(),
                                                'train_multi-shot':1-avg_accuracy.item()},
                                            global_step=self.global_iter)
                        self.tf.add_scalars(main_tag='performance/cost',
                                            tag_scalar_dict={
                                                'train_one-shot_class':class_loss.item(),
                                                'train_one-shot_info':info_loss.item(),
                                                'train_one-shot_total':total_loss.item()},
                                            global_step=self.global_iter)
                        self.tf.add_scalars(main_tag='mutual_information/train',
                                            tag_scalar_dict={
                                                'I(Z;Y)':izy_bound.item(),
                                                'I(Z;X)':izx_bound.item()},
                                            global_step=self.global_iter)


            if (self.global_epoch % 2) == 0 : self.scheduler.step()
            self.test()
#        self.real_test()  #!!!!!!!  
        print(" [*] Training Finished!")

    def test(self, save_ckpt=True):
        self.set_mode('eval')

        class_loss = 0
        info_loss = 0
        total_loss = 0
        izy_bound = 0
        izx_bound = 0
        ht_bound=0
        htx_bound=0
        correct = 0
        avg_correct = 0
        total_num = 0
        import torch

        test_data=[]
        for line in open('samples_test.txt', "r"):
            test_data.append(line.split('\t'))
        for entry in test_data:
            entry.remove('\n')
        for entry in test_data:
            for i in range(len(entry)):
                entry[i]=float(entry[i])
        test_label = []
        for line in open('samples_y_test.txt', "r"):
            test_label.append(line.split('\n'))
        for entry in test_label:
            entry.remove('')
        for entry in test_label:
            for i in range(len(entry)):
                entry[i] = float(entry[i])
        #self.set_mode('train')
        #for idx, (images,labels) in enumerate(self.data_loader['test']):
        for (images,labels) in zip(test_data,test_label):
           # self.global_iter += 1
            images=torch.Tensor([images])
            labels=torch.LongTensor(labels)
            x = Variable(cuda(images, self.cuda))
            y = Variable(cuda(labels, self.cuda))
            (mu, std), logit ,(mu2, std2)= self.toynet_ema.model(x)#!!!

            '''class_loss += F.cross_entropy(logit,y,size_average=False).div(math.log(2))
            info_loss += -0.5*(0.25+0.5*std.log()-mu.pow(2)-std.pow(2)).sum().div(math.log(2))
            total_loss += class_loss + self.beta*info_loss
            total_num += y.size(0)
            izy_bound += math.log(10,2) - class_loss
            izx_bound += info_loss'''
            alpha=self.alpha
            class_loss += F.cross_entropy(logit,y,size_average=False).div(math.log(2))
            #info_loss += (-0.5 * alpha - alpha * std.log() + 0.5 * (mu.pow(2) + std.pow(2)) + (
            #            1 - alpha) * 0.5 * math.log(2 * math.pi)).sum(1).mean().div(math.log(2))
            info_loss += (-0.5 * alpha - alpha * std.log() + std2.log() + 0.5 * (
                        mu.pow(2) + mu2.pow(2) - 2 * mu* mu2 + std.pow(2))/ (std2.pow(2)) + (
                                 1 - alpha) * 0.5 * math.log(2 * math.pi)).sum(1).mean().div(math.log(2))  # ������ǲ���.* !!!
            total_loss += class_loss + self.beta * info_loss
            total_num += y.size(0)

#            izy_bound += math.log(10, 2) - class_loss
#            '''ht_bound += (0.5 * (mu.pow(2) + std.pow(2) + math.log(2 * math.pi))).sum(1).mean().div(math.log(2))
#            htx_bound += (0.5 * math.log(2 * math.pi) + std.log() + 0.5).sum(1).mean().div(math.log(2))
#            izx_bound += -0.5 * (1 + 2 * std.log() - mu.pow(2) - std.pow(2)).sum(1).mean().div(math.log(2))'''
#            htx_bound += (0.5 * math.log(2 * math.pi) + std.log() + 0.5).sum(1).mean().div(math.log(2))
#            hty_bound += (0.5 * math.log(2 * math.pi) + std2.log() + 0.5).sum(1).mean().div(math.log(2))  # !!!
#            ht_bound += hty_bound + izy_bound  # H(T)=H(T|Y)+I(T,Y)!!!
#            izx_bound += ht_bound - htx_bound  # I(T,X)=H(T)-H(T|X)!!!
            #izx_bound = info_loss

            prediction = F.softmax(logit,dim=1).max(1)[1]
            correct += torch.eq(prediction,y).float().sum()

            if self.num_avg != 0 :
                _, avg_soft_logit,_ = self.toynet_ema.model(x,self.num_avg)
                avg_prediction = avg_soft_logit.max(1)[1]
                avg_correct += torch.eq(avg_prediction,y).float().sum()
            else :
                avg_correct = Variable(cuda(torch.zeros(correct.size()), self.cuda))

        accuracy = correct/total_num
        avg_accuracy = avg_correct/total_num

        izy_bound /= total_num
        izx_bound /= total_num
        class_loss /= total_num
        info_loss /= total_num
        total_loss /= total_num
#        htx_bound/=total_num
#        ht_bound/=total_num
        with open(' test_class_loss'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
            f.write(str( class_loss.item()) + '\n')
        with open(' test_info_loss'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
            f.write(str( info_loss.item()) + '\n')
        with open(' test_total_loss'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
            f.write(str( total_loss.item()) + '\n')
        with open(' test_mu'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
            f.write(str( mu) + '\n')
        with open(' test_std'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
            f.write(str( std) + '\n')
        with open(' test_mu2'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
            f.write(str( mu2) + '\n')
        with open(' test_std2'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
            f.write(str( std2) + '\n')
        
#        with open('test_ht_bound'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
#            f.write(str(ht_bound.item()) + '\n')
#        with open('test_htx_bound'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
#            f.write(str(htx_bound.item()) + '\n')
#        with open('test_izy_bound'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
#            f.write(str(izy_bound.item()) + '\n')
#        with open('test_izx_bound'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
#            f.write(str(izx_bound.item()) + '\n')
        with open('test_accuracy'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
            f.write(str(accuracy.item()) + '\n')
#        with open('test_avg_accuracy'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
#            f.write(str(avg_accuracy.item()) + '\n')
#        with open('test_error'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
#            f.write(str(1 - accuracy.item()) + '\n')
#        with open('test_avg_error'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
#            f.write(str(1 - avg_accuracy.item()) + '\n')
#        with open('test_error'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
#            f.write(str(1 - accuracy.item()) + '\n')
#        with open('test_class_loss'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
#            f.write(str(class_loss.item()) + '\n')
#        with open('test_info_loss'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
#            f.write(str(info_loss.item()) + '\n')
#        with open('test_total_loss'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
#            f.write(str(total_loss.item()) + '\n')
        print()
        print('[TEST RESULT]')
        print(' e:{}  class_loss:{:.2f} info_loss:{:.2f} ' 
                            .format(self.global_epoch, class_loss.item(), info_loss.item()), end=' ')
#        print('e:{} IZY:{:.2f} IZX:{:.2f}'
#                .format(self.global_epoch, izy_bound.item(), izx_bound.item()), end=' ')
        print('acc:{:.4f} avg_acc:{:.4f}'
                .format(accuracy.item(), avg_accuracy.item()), end=' ')
        print('err:{:.4f} avg_erra:{:.4f}'
                .format(1-accuracy.item(), 1-avg_accuracy.item()))
        print()

        if self.history['acc'] < accuracy.item() :
            self.history['acc'] = accuracy.item()
            self.history['class_loss'] = class_loss.item()
            self.history['info_loss'] = info_loss.item()
            self.history['total_loss'] = total_loss.item()
            self.history['epoch'] = self.global_epoch
            self.history['iter'] = self.global_iter
            if save_ckpt :
                self.save_checkpoint('best_acc.tar')
                #self.load_checkpoint()

        if self.tensorboard :
            self.tf.add_scalars(main_tag='performance/accuracy',
                                tag_scalar_dict={
                                    'test_one-shot':accuracy.item(),
                                    'test_multi-shot':avg_accuracy.item()},
                                global_step=self.global_iter)
            self.tf.add_scalars(main_tag='performance/error',
                                tag_scalar_dict={
                                    'test_one-shot':1-accuracy.item(),
                                    'test_multi-shot':1-avg_accuracy.item()},
                                global_step=self.global_iter)
            self.tf.add_scalars(main_tag='performance/cost',
                                tag_scalar_dict={
                                    'test_one-shot_class':class_loss.item(),
                                    'test_one-shot_info':info_loss.item(),
                                    'test_one-shot_total':total_loss.item()},
                                global_step=self.global_iter)
            self.tf.add_scalars(main_tag='mutual_information/test',
                                tag_scalar_dict={
                                    'I(Z;Y)':izy_bound.item(),
                                    'I(Z;X)':izx_bound.item()},
                                global_step=self.global_iter)

        self.set_mode('train')

    def save_checkpoint(self,filename='best_acc.tar'):
        model_states = {
                'net':self.toynet.state_dict(),
                'net_ema':self.toynet_ema.model.state_dict(),
                }
        optim_states = {
                'optim':self.optim.state_dict(),
                }
        states = {
                'iter':self.global_iter,
                'epoch':self.global_epoch,
                'history':self.history,
                'args':self.args,
                'model_states':model_states,
                'optim_states':optim_states,
                }
        file_path = self.ckpt_dir.joinpath(filename)
        torch.save(states,file_path.open('wb+'))
        print("=> saved checkpoint '{}' (iter {})".format(file_path,self.global_iter))

    def load_checkpoint(self, filename='best_acc.tar'):
        file_path = self.ckpt_dir.joinpath(filename)
        print(file_path)
        if file_path.is_file():
            print("=> loading checkpoint '{}'".format(file_path))
            checkpoint = torch.load(file_path.open('rb'))
            print(checkpoint['history']['info_loss'])
            for key in checkpoint.keys():
                print(key)
            self.global_epoch = checkpoint['epoch']
            self.global_iter = checkpoint['iter']
            self.history = checkpoint['history']

            self.toynet.load_state_dict(checkpoint['model_states']['net'])
            self.toynet_ema.model.load_state_dict(checkpoint['model_states']['net_ema'])

            print("=> loaded checkpoint '{} (iter {})'".format(
                file_path, self.global_iter))

        else:
            print("=> no checkpoint found at '{}'".format(file_path))


    def real_test(self):
           # self.set_mode('real_test')
    
            class_loss = 0
            info_loss = 0
            total_loss = 0
            izy_bound = 0
            izx_bound = 0
            ht_bound=0
            htx_bound=0
            correct = 0
            avg_correct = 0
            total_num = 0
            import torch
    
            real_test_data=[]
            for line in open('samples_val.txt', "r"):
                real_test_data.append(line.split('\t'))
            for entry in real_test_data:
                entry.remove('\n')
            for entry in real_test_data:
                for i in range(len(entry)):
                    entry[i]=float(entry[i])
            real_test_label = []
            for line in open('samples_y_val.txt', "r"):
                real_test_label.append(line.split('\n'))
            for entry in real_test_label:
                entry.remove('')
            for entry in real_test_label:
                for i in range(len(entry)):
                    entry[i] = float(entry[i])
            #self.set_mode('train')
            #for idx, (images,labels) in enumerate(self.data_loader['test']):
            for (images,labels) in zip(real_test_data,real_test_label):
               # self.global_iter += 1
                images=torch.Tensor([images])
                labels=torch.LongTensor(labels)
                x = Variable(cuda(images, self.cuda))
                y = Variable(cuda(labels, self.cuda))
                (mu, std), logit ,(mu2, std2)= self.toynet_ema.model(x)#!!!
    
                alpha=self.alpha
                class_loss += (logit-y).pow(2).div(2)
                #info_loss += (-0.5 * alpha - alpha * std.log() + 0.5 * (mu.pow(2) + std.pow(2)) + (
                #            1 - alpha) * 0.5 * math.log(2 * math.pi)).sum(1).mean().div(math.log(2))
                info_loss += (-0.5 * alpha - alpha * std.log() + std2.log() + 0.5 * (
                            mu.pow(2) + mu2.pow(2) - 2 * mu* mu2 + std.pow(2))/ (std2.pow(2)) + (
                                     1 - alpha) * 0.5 * math.log(2 * math.pi)).sum(1).mean().div(math.log(2))  # ������ǲ���.* !!!
                total_loss += class_loss + self.beta * info_loss
                total_num += y.size(0)
    
                if self.num_avg != 0 :
                    _, avg_soft_logit,_ = self.toynet_ema.model(x,self.num_avg)
                    avg_prediction = avg_soft_logit.max(1)[1]
                    avg_correct += torch.eq(avg_prediction,y).float().sum()
                else :
                    avg_correct = Variable(cuda(torch.zeros(correct.size()), self.cuda))
    
    
            class_loss /= total_num
            info_loss /= total_num
            total_loss /= total_num
    
            with open(' real_test_class_loss'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
                f.write(str( class_loss.item()) + '\n')
            with open('  real_test_info_loss'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
                f.write(str( info_loss.item()) + '\n')
            with open('  real_test_total_loss'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
                f.write(str( total_loss.item()) + '\n')
            with open('  real_test_mu'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
                f.write(str( mu) + '\n')
            with open('  real_test_std'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
                f.write(str( std) + '\n')
            with open('  real_test_mu2'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
                f.write(str( mu2) + '\n')
            with open('  real_test_std2'+str(alpha)+str(math.log10(self.beta))+'.txt', 'a+') as f:
                f.write(str( std2) + '\n')
    
            print('[REAL TEST RESULT]')
            print(' class_loss:{:.2f} info_loss:{:.2f} ' 
                                .format( class_loss.item(), class_loss.item()), end=' ')
            print()
    
      