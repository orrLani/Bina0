import numpy
import sklearn
import pandas as pd
import math

DEFAULT = 0


class Junction:
    def __init__(self, feature:str, treshold:float, children:list, classification:int):
        self.feature = feature
        self.treshold = treshold
        self.children = children
        self.classification = classification

    def getNextChild(self, obj:pd.DataFrame):
        return self.children[0] if obj[self.feature] <= self.treshold else self.children[1]


def majorityClass(data: pd.DataFrame)->int:
    # count the values that there Classification is 0
    classification_zero = len(data.loc[data['diagnosis'] == 0])
    # count the values that there Classification is 1
    classification_one = len(data.loc[data['diagnosis'] == 1])
    if classification_zero> classification_one :
        return 0
    return 1


def get_class_from_example(example: pd.DataFrame) -> int:
    return example['diagnosis']

def allExamplesAreSameClass(classification:int, examples_data: pd.DataFrame) -> bool:
    # classification = get_class_from_example(examples.iloc[[0]])
    for example in examples_data.iterrows():
        if classification != example[1]['diagnosis'] :
            return False
    return True



def ID3(examples_data:pd.DataFrame, features:list):
    classification = majorityClass(examples_data)
    return TDIDT(examples_data, classification, MaxIG)

def calcIG(examples,left_examples:pd.DataFrame,right_examples:pd.DataFrame):

    def get_counts(df:pd.DataFrame) -> (int, int , int):
        zero_count = len(df.loc[df['diagnosis'] == 0])
        one_count = len(df.loc[df['diagnosis'] == 1])
        return zero_count,one_count,(zero_count+one_count)

    def calculate(numerator,denominator) -> float :
        fraction = (float(numerator)/float(denominator))
        if fraction == 0:
            return 0
        return (fraction)*math.log(fraction,2)

    left_count_zero, left_count_one,left_count_total =get_counts(left_examples)
    right_count_zero, right_count_one, right_count_total = get_counts(right_examples)
    father_count_zero, father_count_one, father_count_total = get_counts(examples)
    left_h =- (calculate(left_count_zero,left_count_total)+calculate(left_count_one,left_count_total))
    right_h = - (calculate(right_count_zero, right_count_total) + calculate(right_count_one, right_count_total))
    father_h = - (calculate(father_count_zero, father_count_total) + calculate(father_count_one, father_count_total))

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


def TDIDT(examples_data:pd.DataFrame, selectFeatureFunction):

    # if no examples in the data frame
    if examples_data.empty:
        return Junction(None, None, [], DEFAULT)

    classification = majorityClass(examples_data)
    #  if no features in the data frame or every example have the same classification
    if allExamplesAreSameClass(classification=classification, examples_data= examples_data):
        return Junction(None, None, [], classification)
    feature, treshold = selectFeatureFunction(examples_data)
    left_child = TDIDT(examples_data[examples_data[feature] <= treshold], selectFeatureFunction)
    right_child = TDIDT(examples_data[examples_data[feature] > treshold], selectFeatureFunction)
    return Junction(feature, treshold, [left_child, right_child], classification)

def DT_Classify(obj:pd.DataFrame , tree:Junction):
    if len(tree.children)==0:
        return tree.classification
    return DT_Classify(obj, tree.getNextChild(obj))


if __name__ == '__main__':
    train_data:pd.DataFrame =pd.read_csv('train.csv')

    classifier = TDIDT(train_data, MaxIG)

    for example in train_data.itterows():
        assert(DT_Classify(example,classifier)==example['diagnosis'])











