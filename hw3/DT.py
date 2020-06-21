import numpy
import sklearn
import pandas as pd
import math
import time
import pickle

DEFAULT_CLASSIFICATION = 1
class Node:
    def __init__(self, feature:str, treshold:float, children:list, classification:int, epsilon:float=0,
                 num_of_examples_classified_true:int =0,
                 num_of_examples_classified_false:int =0):
        self.feature = feature
        self.treshold = treshold
        self.children = children
        self.classification = classification
        self.epsilon = epsilon
        self.num_of_examples_classified_true = num_of_examples_classified_true
        self.num_of_examples_classified_false = num_of_examples_classified_false

    def getNextChild(self, obj:pd.DataFrame):
        return self.children[0] if obj[1][self.feature] <= self.treshold else self.children[1]
    def print(self):
        print(str(self.feature)+","+str(self.treshold)+","+str(self.classification))
        for child in self.children:
            child.print()

    def getNextChildrenByEpsilon(self,obj:pd.DataFrame):
        next_children = []
        if obj[1][self.feature] <= self.treshold + self.epsilon:
            next_children.append(self.children[0])

        if obj[1][self.feature] > self.treshold - self.epsilon:
            next_children.append(self.children[1])

        return  next_children

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


def getClassificationCount(data: pd.DataFrame)->(int,int):
    # count the values that there Classification is 0
    num_of_examples_classified_false = len(data.loc[data['diagnosis'] == 0])
    # count the values that there Classification is 1
    num_of_examples_classified_true = len(data.loc[data['diagnosis'] == 1])

    return num_of_examples_classified_false,num_of_examples_classified_true


def get_class_from_example(example: pd.DataFrame) -> int:
    return example['diagnosis']

def allExamplesAreSameClass(classification, examples_data: pd.DataFrame) -> bool:
    # classification = get_class_from_example(examples.iloc[[0]])
    for example in examples_data.iterrows():
        if classification != example[1]['diagnosis'] :
            return None
    return True


def MaxIG(examples_data:pd.DataFrame):
    best_feature, best_treshold, bestIG = None, 0, 0
    features = [f for f in examples_data.columns[1:]]
    #print(len(examples_data))
    for feature in features:
        #print(str(feature))

        # examples_sorted_by_feature =examples_data.sort_values(by=[feature])
        # feature_values_list=list(examples_sorted_by_feature[feature])
        # feature_values_list=list(examples_sorted_by_feature[feature])

        examples_sorted_by_feature =(examples_data[feature]).sort_values(by=[feature])
        feature_values_list = list(examples_sorted_by_feature)
        tresholds = [(x+y)/2 for x,y in zip(feature_values_list, feature_values_list[1:])]
        for t in tresholds:
            left_examples = examples_data[examples_data[feature] <= t]
            right_examples = examples_data[examples_data[feature] > t]
            curIG = calcIG(examples_data, left_examples, right_examples)
            if curIG > bestIG:
                best_feature, best_treshold, bestIG = feature, t, curIG
    return best_feature, float(best_treshold)
    pass



def calcIG(examples,left_examples:pd.DataFrame,right_examples:pd.DataFrame):
    def get_counts(df:pd.DataFrame) -> (int, int , int):
        zero_count = len(df.loc[df['diagnosis'] == 0])
        one_count = len(df.loc[df['diagnosis'] == 1])
        return zero_count,one_count,(zero_count+one_count)

    def calculate(numerator,denominator) -> float :
        if float(numerator) == 0:
            return 0
        fraction = (float(numerator)/float(denominator))
        return (fraction)*math.log(fraction,2)

    left_count_zero, left_count_one,left_count_total =get_counts(left_examples)
    right_count_zero, right_count_one, right_count_total = get_counts(right_examples)
    father_count_zero, father_count_one, father_count_total = get_counts(examples)
    left_h =- (calculate(left_count_zero,left_count_total)+calculate(left_count_one,left_count_total))
    right_h = - (calculate(right_count_zero, right_count_total) + calculate(right_count_one, right_count_total))
    father_h = - (calculate(father_count_zero, father_count_total) + calculate(father_count_one, father_count_total))

    return  father_h -((left_count_total/father_count_total)*left_h)- ((right_count_total/father_count_total)*right_h)




class MakeLeaf:
    def __init__(self,x):
        self.x =x

    def lessThan(self,examples_data:pd.DataFrame):
        if len(examples_data) <= self.x:
            return True
        return False

    def basicLeafTest(self,examples_data: pd.DataFrame):
        if examples_data.empty:
            return Node(None, None, [], DEFAULT_CLASSIFICATION)

        classification = majorityClass(examples_data)
        if allExamplesAreSameClass(classification=classification, examples_data=examples_data):
            return Node(None, None, [], classification,0)

        return None

    def basicTestAndAtLeastXExamples(self,examples_data: pd.DataFrame):
        classification = majorityClass(examples_data)
        if self.lessThan(examples_data):
            num_of_examples_classified_false,num_of_examples_classified_true= getClassificationCount(examples_data)
            return Node(None, None, [], classification,0,num_of_examples_classified_false,
                        num_of_examples_classified_true)
        return self.basicLeafTest(examples_data)




def DT_Classify(obj:pd.DataFrame , tree:Node):
    if len(tree.children)==0:
        return tree.classification
    return DT_Classify(obj, tree.getNextChild(obj))



    #not a leaf
    return None




def calcEpsilon(examples_data:pd.DataFrame) ->float:
    return examples_data['diagnosis'].std

    pass
def TDIDT(examples_data:pd.DataFrame, selectFeature_f, makeLeaf=MakeLeaf(math.inf)):
    # if decision to make a leafe then a leaf node returned
    # else leaf is None


    leaf = makeLeaf.basicTestAndAtLeastXExamples(examples_data)
    if leaf is not None:
        return leaf
    # if here this is not a leaf and continue to partition to children nodes
    classification = majorityClass(examples_data)
    feature, treshold = selectFeature_f(examples_data)
    left_child = TDIDT(examples_data[examples_data[feature] <= treshold], selectFeature_f, makeLeaf)
    right_child = TDIDT(examples_data[examples_data[feature] > treshold], selectFeature_f, makeLeaf)

    return Node(feature, treshold, [left_child, right_child], classification,
                epsilon=(0.1*calcEpsilon(examples_data)))



RECALC = 1

def ID3(examples_data:pd.DataFrame,selectFeature_f=MaxIG, makeLeaf=MakeLeaf(math.inf)):
    #classification = majorityClass(examples_data)
    return TDIDT(examples_data, selectFeature_f, makeLeaf)



if __name__ == '__main__':

    train_data:pd.DataFrame =pd.read_csv('train.csv')
    test_data : pd.DataFrame= pd.read_csv('test.csv')
    start_time = time.time()
    classifier = None
   #classifier_3_27 = ID3(train_data, MaxIG, MakeLeaf(27))
    classifier_3_9 = ID3(train_data, MaxIG, MakeLeaf(9))
    classifier_3_3 = ID3(train_data, MaxIG, MakeLeaf(3))
    # classifier_2_test = ID3(train_data)

    if RECALC ==1:
        #start_time = time.time()
        #classifier = ID3(train_data, MaxIG)
        #time_ = time.time() -start_time
        #print(str(time))

        #to_file = open("classifier_build", "wb")
      #  pickle.dump(classifier, to_file)
      #  to_file.close()
      #  to_file = open("classifier_3_27_build", "wb")
      #  pickle.dump(classifier_3_27, to_file)
      #  to_file.close()

        to_file = open("classifier_3_9_build", "wb")
        pickle.dump(classifier_3_9, to_file)
        to_file.close()

        to_file = open("classifier_3_3_build", "wb")
        pickle.dump(classifier_3_3, to_file)
        to_file.close()


    else:
        from_file = open("classifier_3_3_build","rb")
        classifier = pickle.load(from_file)
        from_file.close()

    # ok =0
    # not_ok =0
    #
    # # for classifie
    # for example in test_data.iterrows():
    #     if DT_Classify(example, classifier) == example[1]['diagnosis']:
    #         ok += 1
    #     else:
    #         not_ok += 1
    #
    # total = ok + not_ok
    # print("for classifier  ok: " + str(ok / total) + " not ok: " + str(not_ok / total))
    ok = 0
    not_ok = 0
    # for classifier_3_3
    for example in test_data.iterrows():
         if DT_Classify(example,classifier_3_3)==example[1]['diagnosis']:
             ok+=1
         else:
             not_ok += 1

    total = ok+not_ok
    print("for classifier_3_3  ok: "+str(ok/total)+" not ok: "+str(not_ok/total))

    # # for classifier_3_9
    ok = 0
    not_ok = 0
    for example in test_data.iterrows():
         if DT_Classify(example, classifier_3_9) == example[1]['diagnosis']:
             ok += 1
         else:
             not_ok += 1

    total = ok + not_ok
    print("for classifier_3_9  ok: " + str(ok / total) + " not ok: " + str(not_ok / total))

    # for classifier_3_27
    #ok = 0
    #not_ok = 0
    #for example in test_data.iterrows():
    #    if DT_Classify(example, classifier_3_27) == example[1]['diagnosis']:
    #        ok += 1
    #    else:
    #        not_ok += 1

    #total = ok + not_ok
    #print("for classifier_3_27  ok: " + str(ok / total) + " not ok: " + str(not_ok / total))
    # print

    pass











