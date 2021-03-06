#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import csv
import os
import sys
import caffe
import numpy as np
from sklearn import preprocessing
from pprint import pprint

def extractfeature(imagedir, labellistfilename, protofilename, pretrainedname,
                   meanfilename, featurefilename, labelfilename, libsvmformat=False):

    print('Start extract features.')
    mean = np.load(meanfilename)
    net = caffe.Classifier(protofilename, pretrainedname, mean=mean,
                           channel_swap=(2,1,0), image_dims=(256,256), raw_scale=255)
    
    reader = csv.reader(file(labellistfilename, 'r'),
                        delimiter='\t', lineterminator='\n')
    if libsvmformat:
        print('output: libsvm format')
        featurefile = open(featurefilename, 'w')
    else:
        print('output: npy format')
    print('image dims: %s' % (net.image_dims,))
    features = []
    labels = []
    for line in reader:
        try:
            imagepath = imagedir + '/' + line[0]
            label = int(line[1])
            print(imagepath, label)
            image = caffe.io.load_image(imagepath)
            oversampled = caffe.io.oversample([caffe.io.resize_image(image, net.image_dims)],
                                              net.crop_dims)
            inputdata = np.asarray([net.preprocess('data', in_) for in_ in oversampled])
            net.forward(data=inputdata)
            feature = net.blobs['fc6i'].data[4]
            scaledfeature = preprocessing.scale(feature.flatten().tolist())
            if libsvmformat:
                featurefile.write("%d %s\n" % (label, ' '.join(["%d:%f" % (i, fi) for i, fi in enumerate(scaledfeature, start=1)])))
            else:
                features.append(scaledfeature)
                labels.append(label)
        except IOError as e:
            print(e)

    np.save(featurefilename, features)
    np.save(labelfilename, labels)

    print('Finish extract features.')
    

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    
    IMAGE_DIR = '../../cat_images'
    LABELLIST_FILE = '../data/cat_train_labels.tsv'
    PROTO_FILE = '../data/imagenet_feature.prototxt'
    PRETRAINED_FILE = '../data/bvlc_reference_caffenet.caffemodel'
    MEAN_FILE = '../data/ilsvrc_2012_mean.npy'
    FEATURE_FILE = '../data/cat_features.txt'  ## libsvm format file
    FEATURE_FILE = '../data/cat_features.npy'
    LABEL_FILE = '../data/cat_train_labels.npy'
    if os.path.splitext(FEATURE_FILE)[-1] == '.txt':
        libsvmformat = True
    else:
        libsvmformat = False
    extractfeature(IMAGE_DIR, LABELLIST_FILE, PROTO_FILE,
                   PRETRAINED_FILE, MEAN_FILE, FEATURE_FILE, LABEL_FILE, libsvmformat)
    
