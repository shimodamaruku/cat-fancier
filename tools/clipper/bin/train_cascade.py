#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import sys
import time
from pprint import pprint


def parsearguments():
    parser = argparse.ArgumentParser(description='create sample for training cascade')
    parser.add_argument('positivefilename', help='positive sample file')
    return parser.parse_args()

def createsamples(positivefile, vecdir='./vec'):
    os.environ['PATH'] = '/bin:/usr/bin:/usr/local/bin'
    if not os.path.isdir(vecdir):
        os.mkdir(vecdir)
    linecount = len(open(positivefile).readlines())
    print('samples: %d' % (linecount,))
    cmdline = ['opencv_createsamples', '-info', positivefile,
               '-vec', vecdir + '/' + positivefile + '.vec',
               '-num', str(linecount)]
    print(' '.join(cmdline))
    try:
        p = subprocess.Popen(cmdline, cwd='./', shell=False,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, close_fds=True)
    except OSError as e:
        print(e)
        sys.exit(-1)
    
    while True:
        line = p.stdout.readline()
        if not line:
            break
        print(line.rstrip())
    ret = p.wait()
    print('ret: %d' % (ret,))

def traincascade():
    cmdline = [
        'opencv_traincascade', '-data', dstdir, '-vec', vecfile,
        '-bg', bgfile, '-numPos', numpos, '-numNeg', numneg,
        '-featureType', 'LBP', '-maxFalseAlarmRate', maxfarate
    ]
    try:
        p = subprocess.Popen(cmdline, cwd='./', shell=False,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, close_fds=True)
    except OSError as e:
        print(e)
        sys.exit(-1)

    while True:
        line = p.stdout.readline()
        if not line:
            break
        print(line.rstrip())
    ret = p.wait()
    print('ret: %d' % (ret,))


if __name__ == '__main__':
    args = parsearguments()
    positivefilename = args.positivefilename
    createsamples(positivefilename)
    
