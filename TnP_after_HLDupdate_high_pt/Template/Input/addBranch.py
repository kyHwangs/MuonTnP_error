#!/usr/bin/env python

import argparse
import sys
import os

"""
Setup argument parser
"""


parser = argparse.ArgumentParser(description="This program adds a branch to a Tag-and-Probe tree from an expression, e.g., the expression \"abs(eta);eta\" creates a new variables which is equal to abseta. The expression must have the from \"EXPRESSION;USED_VARIABLE_1;USED_VARIABLE_2;...\". Because the expression is wrapped to Python, numpy can be used, e.g., \"numpy.log10(pt);pt\".")
parser.add_argument("filenamesInput", help="Path to the input Tag-And-Probe ROOT files")
parser.add_argument("filenameOutput", help="Path to the output Tag-And-Probe ROOT file with added branch")
parser.add_argument("expression", help="Expression which is applied on tree to create new branch. Take care, that the expression has to have the form \"EXPRESSION;USED_VARIABLE_1;USED_VARIABLE_2;...\"")
parser.add_argument("branch", help="Name of new branch")
parser.add_argument("-d", "--directory", default="tpTree", help="Directory in the input ROOT file which contains the Tag-And-Probe tree")
parser.add_argument("-t", "--tree", default="fitter_tree", help="Name of the tree holding the variables")
parser.add_argument("-v", "--verbosity", default=True, help="Set verbosity to [0, 1]")
args = parser.parse_args()

"""
Read input files
"""

from ROOT import * # import this here, otherwise it overwrites the argparse stuff
gROOT.SetBatch(True) # set ROOT to batch mode, this suppresses printing canvases
from array import array
import numpy

treePath = os.path.join(args.directory,args.tree)
if args.verbosity==1:
    print('Used path to tree in files:')
    print('---------------------------')
    print(treePath)
    print('')
trees = TChain(treePath)

if args.verbosity==1:
    print('Input files:')
    print('------------')
for filename in args.filenamesInput.split(' '):
    if args.verbosity==1:
        print(filename)
    trees.AddFile(filename)
if args.verbosity==1:
    print('')

"""
Make new branch out of expression
"""

# Wrap expression to actual expression and variable list
tmp = args.expression.split(';')
if len(tmp)<=1:
    print('[ERROR] Input expression has length less than 1, please check: {}'.format(tmp))
expression = tmp[0].strip()
usedVariables = []
for var in tmp[1:]:
    usedVariables.append(var.strip())

# Make output file and branch
fileOutput = TFile.Open(args.filenameOutput, 'recreate')
fileOutput.mkdir(args.directory).cd()

treeOutput = trees.CloneTree(0)
varBranch = array('f', [1.0])
treeOutput.Branch(args.branch, varBranch, args.branch)

progressbarWidth = 40
numEvents = trees.GetEntries()
if args.verbosity==1:
    print('Adding new branch:')
    print('------------------')
    print('Name of new branch: {}'.format(args.branch))
    print('Expression: {}'.format(expression))
    print('Used variables in expression: {}'.format(usedVariables))
    print('Number of events: {}'.format(numEvents))
    sys.stdout.write('Progress: [{}]'.format('-'*progressbarWidth))
    sys.stdout.flush() # this forces to print the stdout buffer
    sys.stdout.write('\b'*(progressbarWidth+1)) # return to start of line, after '['

for i in range(numEvents):
    # Get full event from input files
    trees.GetEntry(i)

    # Load variables, which are defined in 'usedVariables'
    # NOTE: hacky hacky, but I haven't found a better way
    # The Draw(...,TCut,...) approach is even more messy
    for var in usedVariables:
        exec(var+' = trees.'+var)

    # Set new branch
    exec('varBranch[0]='+expression)

    # Fill modified tree
    treeOutput.Fill()
    if args.verbosity==1:
        if i%int(numEvents/(progressbarWidth-1))==0:
            sys.stdout.write('+')
            sys.stdout.flush()

if args.verbosity==1:
    sys.stdout.write('\n')
    print('')

"""
Store tree to new file
"""

fileOutput.Write()
fileOutput.Close()
if args.verbosity==1:
    print('Output file:')
    print('------------')
    print(args.filenameOutput)
print('')