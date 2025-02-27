# -*- coding: utf-8 -*-
"""embeding.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13hURGvyLGzt1ttQqPH1iCdfX3r5p8_uk
"""

import torch
from torch.utils.data import Dataset, DataLoader
from torch import nn
from torchvision import transforms
import torchvision.datasets as datasets
import pickle
from PIL import Image
import os
import pandas as pd
from keras.preprocessing.image import load_img,img_to_array

from mobilenet import *
from dataloader import *

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

num_classes = 5
batch_size = 20
num_workers = 2
lr = 1e-3
total_epoch = 2
big_cls = 'total'

location = '/content/drive/MyDrive/14,15 추천컨퍼런스/'
img_dir = location+'img_final'
dir_weight = location + '최종_0706_emb_total_model_light9_0.001_10.pth'

df = pd.read_csv(location+'final_df_link.csv')
embeddings = []

transform = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor()])

train_data = ImageDataset(img_dir, df, transform=transform)
train_data2 = ImageDataset(img_dir, df, transform=None)

train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=False)
train_loader1 = DataLoader(train_data, batch_size=1, shuffle=False)

if __name__ == "__main__":
  model = SuperLightMobileNet(num_classes).to(device)
  model.load_state_dict(torch.load(dir_weight))
  model.eval()

  for itereation, (input, target) in enumerate(train_loader1):
    images = input.to(device)
    outputs = model.give_embedding(images).cpu().detach().numpy()
    embeddings.append(outputs)
    if itereation %100 ==0 :
      print('{}th img embedding'.format(itereation))

  with open(location+'embeddings_shuffle0707_epoch10.pickle', 'wb') as f:
    pickle.dump(embeddings, f, pickle.HIGHEST_PROTOCOL












