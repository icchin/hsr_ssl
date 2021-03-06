#!/usr/bin/env python
#!/usr/bin/env python
#!/usr/bin/python
import tensorflow as tf

import layer
#import speech_data
#from speech_data import Source,Target

learning_rate = 0.001
training_iters = 300000
#batch_size = 64
batch_size = 128


# BASELINE toy net
def simple_dense(net): # best with lr ~0.001
	# type: (layer.net) -> None
	# net.dense(hidden=200,depth=8,dropout=False) # BETTER!!
	net.dense(400, activation=tf.nn.tanh)# 0.99 YAY
	# net.denseNet(40, depth=4)
	# net.classifier() # auto classes from labels
	return

def alex(net): # kinda
	# type: (layer.net) -> None
	print("Building Alex-net")
	net.reshape(shape=[-1, 64, 64, 1])  # Reshape input picture
	# net.batchnorm()
	net.conv([3, 3, 1, 64]) # 64 filters
	net.conv([3, 3, 64, 128])
	net.conv([3, 3, 128, 256])
	net.conv([3, 3, 256, 512])
	net.conv([3, 3, 512, 1024])
	net.dense(1024,activation=tf.nn.relu)
	net.dense(1024,activation=tf.nn.relu)


# Densely Connected Convolutional Networks https://arxiv.org/abs/1608.06993  # advanced ResNet
def denseConv(net):
	# type: (layer.net) -> None
	print("Building dense-net")
	net.reshape(shape=[-1, 128, 128, 1])  # Reshape input picture
	net.buildDenseConv(nBlocks=1)  # increase nBlocks for real data
	net.classifier() # auto classes from labels


def denseNet(net):
	# type: (layer.net) -> None
	print("Building dense-net")
	net.reshape(shape=[-1, 128, 128, 1])  # Reshape input picture
	net.fullDenseNet()
	net.classifier() # auto classes from labels

train_digits=True
if train_digits:
	width= height=128 # for pcm baby data
	#batch=speech_data.spectro_batch_generator(1000,target=speech_data.Target.digits)
        #print speech_data.spectro_batch_generator(1000,target=speech_data.Target.digits)
	classes=10 # digits
else:
	width=512 # for spoken_words overkill data
	classes=74 #
	#batch=word_batch=speech_data.spectro_batch_generator(10, width, source_data=Source.WORD_SPECTROS, target=Target.first_letter)
	raise Exception("TODO")


#---------------------------------------------------------------------------------------------------------------------------------------
#ichikawa

import numpy as np

import glob
import os
import librosa

randam = 0

tr_features = []
tr_labels = []

ichikawa_i = 0
now_i = 0

def data_make():
    while True:
        data = []
        label = []
        global randam
        length = len(tr_features)
        global now_i
        for i in range(100):
            """
            global randam
            randam = (((randam+17)%7)*13)%2
            if randam == 1 :
                data.append(np.ones((128,128)))
                label.append(np.array([1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]))
            else:
                data.append(np.zeros((128,128)))
                label.append(np.array([0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0]))
            """
            data.append(tr_features[now_i])
            label.append(tr_labels[now_i])
            now_i += 1
            if now_i == length:
                now_i = 0
        yield data,label
        data = []
        label = []

#ichikawa = data_make()

def extract_feature(file_name):
    global ichikawa_i
    print ichikawa_i
    print file_name
    ichikawa_i += 1
    X, sample_rate = librosa.load(file_name)
    stft = np.abs(librosa.stft(X))
    mel = librosa.feature.melspectrogram(X, sr=sample_rate)
    return mel

def parse_audio_files(parent_dir,sub_dirs,file_ext='*.wav'):
    features, labels = np.empty((0,193)), np.empty(0)
    ichikawa = []
    for label, sub_dir in enumerate(sub_dirs):
        for fn in glob.glob(os.path.join(parent_dir, sub_dir, file_ext)):
            print "-----------------------------"
            try:
            	mel = extract_feature(fn)
            except:
                print "Error"
                continue
            #ext_features = np.hstack([mfccs,chroma,mel,contrast,tonnetz])
            #ext_features = np.hstack([mel])
            #features = np.vstack([features,ext_features])
            #features = np.vstack([mel])
            #ichikawa.append(np.r_(mel))
            if len(mel[0]) <= 128:
                continue
            ichikawa.append(mel[0:128,0:128])
            labels = np.append(labels, fn.split('/')[2].split('-')[1])
            print len(ichikawa)
            print fn.split('/')[2].split('-')[1]

    return ichikawa, np.array(labels, dtype = np.int)

def one_hot_encode(labels):
    n_labels = len(labels)
    n_unique_labels = len(np.unique(labels))
    one_hot_encode1 = np.zeros((n_labels,2))
    print "------------------------"
    print np.arange(n_labels)
    print labels
    print "------------------------"
    #print one_hot_encode1
    one_hot_encode1[np.arange(n_labels), labels-1] = 1
    return one_hot_encode1

#parent_dir = 'SSL'
#parent_dir = 'HSR_SSL'
#parent_dir = 'audio'
#parent_dir = 'SSL'
#tr_sub_dirs = ['fold1']
#tr_sub_dirs = ['test']
#tr_sub_dirs = ['akapen',"hokuyama",'busu','chinatsu','entalk','entalk2']
#tr_sub_dirs = ['konan',"hukuyama",'radio']
#tr_sub_dirs = ['konan_mini']
#tr_sub_dirs = ['orairi',"anpan","onna","robot","mensetsu","python"]
#,'fold2','fold3','fold4','fold5','fold6','fold7','fold8','fold9']
#,'fold10']

#print "file_read"

#tr_features, tr_labels = parse_audio_files(parent_dir,tr_sub_dirs)

#print "file_read fin"

#tr_labels = one_hot_encode(tr_labels)

def test_now(): #test:ichikawa
    import ichikawa_record
    import time
    while True:
        data = []
        label = []
        global randam
        length = 1
        global now_i
        for i in range(1):
            """
            global randam
            randam = (((randam+17)%7)*13)%2
            if randam == 1 :
                data.append(np.ones((128,128)))
                label.append(np.array([1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]))
            else:
                data.append(np.zeros((128,128)))
                label.append(np.array([0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0]))
            """
	    #parent_dir = 'Sound-Data_mini'
	    ichikawa_record.record()
	    time.sleep(3)
	    parent_dir = 'SSL'
	    tr_sub_dirs = ['check']
	    tr_features, tr_labels = parse_audio_files(parent_dir,tr_sub_dirs)
	    tr_labels = one_hot_encode(tr_labels)

            data.append(tr_features[now_i])
            label.append(tr_labels[now_i])
            now_i += 1
            if now_i == length:
                now_i = 0
        yield data,label
        data = []
        label = []

#-------------------------------------------------------------------------------------------------------------------------------------# CHOOSE MODEL ARCHITECTURE HERE:
# net = layer.net(simple_dense, data=batch, input_width=width, output_width=classes, learning_rate=0.01)
# net = layer.net(simple_dense, input_shape=(width,height), output_width=classes, learning_rate=0.01)
# net=layer.net(model=alex,input_shape=(width, height),output_width=10, learning_rate=learning_rate)

net = layer.net(model=denseConv, input_shape=(width, height), output_width=2, learning_rate=learning_rate)

print net

#net.train_ichikawa_2(data=ichikawa,batch_size=10,steps=20000,dropout=0.6,display_step=10,test_step=100,ckpt_name="20170904.ckpt",start_ckpt="20170817.ckpt") # debug
ichikawa=test_now() #test
net.accuracy_test(data=ichikawa,batch_size=10,steps=100,dropout=0.6,display_step=1,test_step=1,ckpt_name="20170823.ckpt")


