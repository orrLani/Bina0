import csv
import numpy as np
from math import log as math_log
import matplotlib.pyplot as plt


import functools as tls
"""
Implements the IDT nodes.
for each node saves the epsilon needed, by std*0.1.
and also saves all the examples attached to the leaf.
"""
class IDT_Node():
    def __init__(self,feature,saf,left,right,c:int,epsilon,examples):
        self.feature=feature
        self.saf=saf
        self.left=left
        self.right=right
        self.c=c
        self.epsilon=epsilon
        self.examples=examples
    def is_leaf(self):
        return self.feature == None or self.saf == None
"""
Special log for entropy calculation - if x==0 need to be 0.
"""
def log(x,base):
    if x==0:
        return 0
    return math_log(x,base)
def majority_class(examples):
    count_1s=tls.reduce(lambda x,y:x+y,[x[0] for x in examples])
    return 1 if (count_1s >= (len(examples)-count_1s)) else 0

def get_epsilon(examples,feature):
    return 0.1*np.std([x[feature] for x in examples])
def all_have_same_class(examples):
    # return tls.reduce(lambda x,y:x==y,list(filter(lambda x:x[0],examples)))
    x = examples[0][0]
    for example in examples:
        if example[0]!=x:
            return False
    return True
"""
Recursive function - Implements the TDITDT Tree using ID3 select_feature.
calculates the epsilon the attached to each node and saves all the examples attached to the leaf.
returns IDT_node of the root of the tree.
"""
def TDIDT(examples, features,select_feature, x,default_classify=0):
    if len(examples)==0:
            return IDT_Node(None,None,None,None,default_classify,0,examples)
    c = majority_class(examples)
    if all_have_same_class(examples) or len(examples) <=x:
        return IDT_Node(None, None, None, None,c,0,examples)
    feature,saf = select_feature(examples,features)
    smaller_than_saf_examples=[]
    greater_than_saf_examples=[]
    epsilon =  get_epsilon(examples,feature)
    for example in examples:
        if example[feature] <= saf:
            smaller_than_saf_examples.append(example)
        else:
            greater_than_saf_examples.append(example)
    left_child = TDIDT(smaller_than_saf_examples,features,select_feature,x,c)
    right_child = TDIDT(greater_than_saf_examples, features, select_feature,x, c)
    return IDT_Node(feature,saf,left_child,right_child,c,epsilon,None)
"""
Calculates the IG value of sorted_val, if we divide the root with the value saf.
Using entropy
"""
def compute_IG_by_saf(sorted_vals,saf):
    size_smaller = 0
    smaller_positive = 0
    size_larger = 0
    larger_positive = 0
    for val in sorted_vals:
        if val[0] <= saf:
            size_smaller+=1
            if val[1] == 1:
                smaller_positive+=1
        else:
            size_larger+=1
            if val[1] ==1:
                larger_positive+=1
    size_larger = len(sorted_vals)-size_smaller
    # entropy for left child
    entropy_small = -(smaller_positive/size_smaller)*log((smaller_positive/size_smaller),2)-\
                      (1-smaller_positive/size_smaller)*log(1-smaller_positive/size_smaller,2)
    # entropy for right child
    entropy_large = -(larger_positive/size_larger)*log((larger_positive/size_larger),2)-\
                      (1-larger_positive/size_larger)*log(1-larger_positive/size_larger,2)
    # entropy for root
    probality_positive = (larger_positive+smaller_positive)/len(sorted_vals)
    entropy = -(probality_positive)*log(probality_positive,2)-\
              (1-probality_positive)*log(1-probality_positive,2)

    return entropy - entropy_small*size_smaller/len(sorted_vals) - entropy_large*size_larger/len(sorted_vals)
"""
ID3 select feature - moving through all features, sorting them by order, and checks
each seperation by IG. returns the saf value of the largest IG seperation.
"""
def ID3_select_feature(examples, features):
    max_IG_feature,max_IG_saf,max_IG=0,0,0
    for i in features:
        sorted_by_feature_list = []
        for example in examples:
            sorted_by_feature_list.append([example[i],example[0]])
        sorted_by_feature_list=sorted(sorted_by_feature_list,key=lambda x:x[0])
        for j in range(len(sorted_by_feature_list) - 2):
            saf = (sorted_by_feature_list[j][0]+sorted_by_feature_list[j+1][0])/2
            curr_IG=compute_IG_by_saf(sorted_by_feature_list,saf)
            if curr_IG > max_IG:
                max_IG = curr_IG
                max_IG_saf=saf
                max_IG_feature = i
    return max_IG_feature,max_IG_saf

"""
returns all examples in the reachable leafs, by using epsilon - decision.
"""
def get_examples_leafs(root: IDT_Node,example):
    if root.is_leaf():
        return root.examples
    if abs(example[root.feature]-root.saf)<=root.epsilon:
        return get_examples_leafs(root.right,example)+get_examples_leafs(root.left,example)
    elif example[root.feature]<=root.saf:
        return get_examples_leafs(root.left,example)
    else:
        return get_examples_leafs(root.right,example)

"""
checks all epsilon decisions and returns the value of the most leafs.
"""
def classification(root: IDT_Node, example):
    count_0 = 0
    count_1 = 0
    all_example_leafs = get_examples_leafs(root,example)
    for x in all_example_leafs:
        if x[0] == 0:
            count_0+=1
        elif x[0] == 1:
            count_1+=1
    return 1 if count_1 >= count_0 else 0


def load_data(csv_file,divide=False):
    with open(csv_file, newline='') as csvfile:
        data = list(csv.reader(csvfile))
    data.remove(data[0])
    for i in range(len(data)):
        for j in range(len(data[0])):
            data[i][j]=float(data[i][j])

    return data
def get_accuracy(root,test_data):
    count = 0
    false_predictions=[]
    for i in range(len(test_data)):
        if test_data[i][0] == classification(root,test_data[i]):
            count+=1
        else:
            false_predictions.append(i)
    return false_predictions,count / len(test_data)
def plot_graph(list_x,data,test_data):
    accuracy=[]
    for x in list_x:
        root=TDIDT(data,range(1,len(data[0])),ID3_select_feature,x)
        accuracy.append(get_accuracy(root,test_data))
    plt.scatter(list_x,accuracy)
    plt.show()

if __name__ == "__main__":
    data = load_data('train.csv',divide=True)
    test_data = load_data('test.csv',divide=True)
    root=TDIDT(data,range(1,len(data[0])),ID3_select_feature,9)
    false_predictions,accuracy=get_accuracy(root,test_data)
    print(accuracy)
    # disp = plot_confusion_matrix(dt,test_data,test_classification)
    # print(convert_format(disp.confusion_matrix))
