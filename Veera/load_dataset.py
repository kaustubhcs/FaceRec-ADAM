
# coding: utf-8

# In[1]:


# Separating data into training, validation and test datasets
# and assigning labels to the data
import os
import shutil
import glob
import numpy as np
from PIL import Image


# In[2]:


# Copy data from the existing folder into train, valid and test folders
def copy_data(dir_s, fname):
    os.chdir(dir_s + '/' + fname)
    dir_train = dir_s + '/train/' + fname
    dir_valid = dir_s + '/valid/' + fname
    dir_test = dir_s + '/test/' + fname
    if not os.path.exists(dir_train):
        os.makedirs(dir_train)
    if not os.path.exists(dir_valid):
        os.makedirs(dir_valid)
    if not os.path.exists(dir_test):
        os.makedirs(dir_test)
    # Specific for orl dataset
    i = 1
    for filename in os.listdir(dir_s + '/' + fname):
        if i <= 6:
            shutil.copy(dir_s + '/' + fname + '/' + str(i) + '.pgm', dir_train)
        elif i <= 8:
            shutil.copy(dir_s + '/' + fname + '/' + str(i) + '.pgm', dir_valid)
        else:
            shutil.copy(dir_s + '/' + fname + '/' + str(i) + '.pgm', dir_test)
        i = i + 1


# In[3]:


# Assign Labels
def assign_addr_label(path):
    dirs = os.listdir(path)
    addrs = []
    labels = []
    for d in dirs:
        os.chdir(path + '/' + d)
        addr = glob.glob(path + '/' + d + '/' + '*')
        label = [d for i in range(len(addr))]
        addrs.extend(addr)
        labels.extend(label)
    return list(zip(addrs, labels))


# In[4]:


# Load images and save them
def create_data_array(data):
    # data = list(train, valid, test)
    train_addrs, train_labels = zip(*data[0])
    valid_addrs, valid_labels = zip(*data[1])
    test_addrs, test_labels = zip(*data[2])
    # Arrays to store the data
    train_storage = []
    valid_storage = []
    test_storage = []
    mean_storage = []
    # Training Images
    for i in range(len(train_addrs)):
        if i % 20 == 0 and i > 1:
            print('Train data: {}/{}'.format(i, len(train_addrs)))
        addr = train_addrs[i]
        img = Image.open(addr)
        img = np.array(img)
        train_storage.append(img)
        # print(np.array(img))
        mean_storage.append(np.sum(img) / float(len(train_labels)))
    # print(train_storage)
    # Validation Images
    for i in range(len(valid_addrs)):
        if i % 20 == 0 and i > 1:
            print('Valid data: {}/{}'.format(i, len(valid_addrs)))
        addr = valid_addrs[i]
        img = Image.open(addr)
        img = np.array(img)
        valid_storage.append(img)
        # print(np.array(img))
    # print(valid_storage)
    # Test Images
    for i in range(len(test_addrs)):
        if i % 20 == 0 and i > 1:
            print('Test data: {}/{}'.format(i, len(test_addrs)))
        addr = test_addrs[i]
        img = Image.open(addr)
        img = np.array(img)
        test_storage.append(img)
        # print(np.array(img))
    # print(test_storage)
    train_data = list(zip(train_storage, train_labels))
    valid_data = list(zip(valid_storage, valid_labels))
    test_data = list(zip(test_storage, test_labels))
    
    return [train_data, valid_data, test_data, mean_storage]


# In[5]:


# Create train, valid and test data from the dataset
def load_data_label(dir_src, create=0):
    # dir_src = '/home/dvveera/db/orl'
    if create:
        os.chdir(dir_src)
        for filename in os.listdir(dir_src):
            # Specific for orl dataset
            if filename.startswith('s'):
                copy_data(dir_src, filename)
        print('Separated Training, Validation and Test Data')
    
    # Assign labels to the data
    train_path = dir_src + '/' + 'train'
    train_addr_label = assign_addr_label(train_path)
    valid_path = dir_src + '/' + 'valid'
    valid_addr_label = assign_addr_label(valid_path)
    test_path = dir_src + '/' + 'test'
    test_addr_label = assign_addr_label(test_path)
    print('Assigned Labels to Training, Validation and Test Data')
    
    # Create train, valid and test data arrays
    data_label = create_data_array([train_addr_label, valid_addr_label, test_addr_label])
    
    return data_label

