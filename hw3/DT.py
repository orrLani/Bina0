import numpy
import sklearn
import pandas as pd
import math
import time
import pickle

DEFAULT_CLASSIFICATION = 1
class Node:
    def __init__(self, feature:str, treshold:float, children:list, classification:int):
        self.feature = feature
        self.treshold = treshold
        self.children = children
        self.classification = classification

    def getNextChild(self, obj:pd.DataFrame):
        return self.children[0] if obj[1][self.feature] <= self.treshold else self.children[1]
    def print(self):
        print(str(self.feature)+","+str(self.treshold)+","+str(self.classification))
        for child in self.children:
            child.print()


def majorityClass(data: pd.DataFrame)->int:
    # count the values that there Classification is 0
    classification_zero = len(data.loc[data['diagnosis'] == 0])
    # count the values that there Classification is 1
    classification_one = len(data.loc[data['diagnosis'] == 1])
    if classification_zero > classification_one :
        return 0
    elif classification_zero < classification_one:
        return 1
    else:
        return DEFAULT_CLASSIFICATION


def get_class_from_example(example: pd.DataFrame) -> int:
    return example['diagnosis']

def is_all_examples_have_same_class(classification:int ,examples: pandas.DataFrame) -> bool:
    # classification = get_class_from_example(examples.iloc[[0]])
    for example in examples_data.iterrows():
        if classification != example[1]['diagnosis'] :
            return None
    return True



def ID3(examples:pandas.DataFrame,features:list):
    best_feature, best_treshold, bestIG = None, 0, 0
    classification = majorityClass(examples)
    return TDIDT(examples,features,classification,MaxIG)
def MaxIG(features:list,Examples:pandas.DataFrame):
    def get_counts(df:pd.DataFrame) -> (int, int , int):
        zero_count = len(df.loc[df['diagnosis'] == 0])
        one_count = len(df.loc[df['diagnosis'] == 1])
        return zero_count,one_count,(zero_count+one_count)

    for feature in features;
        fraction = (float(numerator)/float(denominator))
        if fraction == 0:
            return 0
        return (fraction)*math.log(fraction,2)
        #print(str(feature))
    left_count_zero, left_count_one,left_count_total =get_counts(left_examples)
    right_count_zero, right_count_one, right_count_total = get_counts(right_examples)
    father_count_zero, father_count_one, father_count_total = get_counts(examples)
    left_h =- (calculate(left_count_zero,left_count_total)+calculate(left_count_one,left_count_total))
    right_h = - (calculate(right_count_zero, right_count_total) + calculate(right_count_one, right_count_total))
    father_h = - (calculate(father_count_zero, father_count_total) + calculate(father_count_one, father_count_total))
        examples_sorted_by_feature =examples_data.sort_values(by=[feature])
    return  father_h -((left_count_total/father_count_total)*left_h)- ((right_count_total/father_count_total)*right_h)



def MaxIG(examples_data:pd.DataFrame):
    best_feature, best_treshold, bestIG = None, 0, 0
    features = [f for f in examples_data.columns[1:]]
    for feature in features:
        examples_sorted_by_feature =examples_data.sort_values(by=[feature])
        feature_values_list=list(examples_sorted_by_feature[feature])
        tresholds = [(x+y)/2 for x,y in zip(feature_values_list, feature_values_list[1:])]
        for t in tresholds:
            left_examples = examples_data[examples_data[feature] <= t]
            right_examples = examples_data[examples_data[feature] > t]
            curIG = calcIG(examples_data, left_examples, right_examples)
            if curIG > bestIG:
                best_feature, best_treshold, bestIG = feature, t, curIG
    return best_feature, float(best_treshold)
    pass
def basicLeafTest(examples_data:pd.DataFrame):
    if examples_data.empty:
        return Node(None, None, [], DEFAULT_CLASSIFICATION)

    classification = majorityClass(examples_data)
def TDIDT(examples:pandas.DataFrame, features:list,classification, select_feature_function):
        return Node(None, None, [], classification)

    #not a leaf
    return None


class LessThenXExamples:
    def __init__(self,x):
        self.x =x
    def checkOn(self,examples_data:pd.DataFrame):
        if len(examples_data) <= self.x:
    if examples.empty:
        return Junction(None, [], DEFULT)

def ID3(examples_data:pd.DataFrame,selectFeature_f = MaxIG, ifLeafMakeLeaf_f = basicLeafTest):
    classification = majorityClass(examples_data)
    return TDIDT(examples_data, selectFeature_f, ifLeafMakeLeaf_f)
def calcIG(examples,left_examples:pd.DataFrame,right_examples:pd.DataFrame):
    if len(list(examples.columns)) == 1 or is_all_examples_have_same_class(classification=classification,
                                                                           examples= examples):
        zero_count = len(df.loc[df['diagnosis'] == 0])
        one_count = len(df.loc[df['diagnosis'] == 1])
        return zero_count,one_count,(zero_count+one_count)

    def calculate(numerator,denominator) -> float :
        if float(numerator) == 0:
            return 0
        fraction = (float(numerator)/float(denominator))
        return Junction(None,[],classification)
    left_count_zero, left_count_one,left_count_total =get_counts(left_examples)
    right_count_zero, right_count_one, right_count_total = get_counts(right_examples)
    feature = select_feature_function(features, examples)
    right_child = TDIDT(examples_data[examples_data[feature] > treshold], selectFeatureFunction)
    father_h = - (calculate(father_count_zero, father_count_total) + calculate(father_count_one, father_count_total))

    if len(tree.children)==0:
        return tree.classification
    return DT_Classify(obj, tree.getNextChild(obj))





def basicTestAndAtLeastXExamples(examples_data: pd.DataFrame, x: int):
    classification = majorityClass(examples_data)
    if LessThenXExamples(x).checkOn(examples_data):
        return Node(None, None, [], classification)
    return basicLeafTest(examples_data)


def TDIDT(examples_data:pd.DataFrame, selectFeature_f, ifLeafMakeLeaf_f = basicLeafTest):
    # if decision to make a leafe then a leaf node returned
    # else leaf is None
    leaf = ifLeafMakeLeaf_f(examples_data)
    if leaf is not None:
        return leaf
    # if here this is not a leaf and continue to partition to children nodes
    classification = majorityClass(examples_data)
    feature, treshold = selectFeature_f(examples_data)
    left_child = TDIDT(examples_data[examples_data[feature] <= treshold], selectFeature_f, ifLeafMakeLeaf_f)
    right_child = TDIDT(examples_data[examples_data[feature] > treshold], selectFeature_f, ifLeafMakeLeaf_f)
    return Node(feature, treshold, [left_child, right_child], classification)

def DT_Classify(obj:pd.DataFrame , tree:Node):
    if len(tree.children)==0:
        return tree.classification
    return DT_Classify(obj, tree.getNextChild(obj))

RECALC = 1
if __name__ == '__main__':

    train_data:pd.DataFrame =pd.read_csv('train.csv')
    test_data : pd.DataFrame= pd.read_csv('test.csv')
    start_time = time.time()
    classifier = None
    classifier_3_27 = ID3(train_data, MaxIG, basicTestAndAtLeastXExamples(27))
    classifier_3_9 = ID3(train_data, MaxIG, basicTestAndAtLeastXExamples(9))
    classifier_3_3 = ID3(train_data, MaxIG, basicTestAndAtLeastXExamples(3))
    classifier_2_test = ID3(train_data)

    if RECALC ==1:
        start_time = time.time()
        time_ = time.time() -start_time
        print(str(time))
        to_file = open("ClassifierBuild_1", "wb")
        pickle.dump(classifier, to_file)
        to_file.close()
    else:
        from_file = open("ClassifierBuild_1","rb")
        classifier = pickle.load(from_file)
        from_file.close()

    ok =0
    not_ok =0
            ok+=1
        else:
            not_ok += 1
    total = ok+not_ok
    print("ok: "+str(ok/total)+" not ok: "+str(not_ok/total))

    pass











