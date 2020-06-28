import numpy as np
import sklearn
import pandas as pd
import math
import time
import pickle
import operator
DEFAULT_CLASSIFICATION = 1
DEBUG =1
class Node:
    def __init__(self, feature:str, treshold:float, children:list, classification:int, epsilon:float=0,
                 data: pd.DataFrame = None):
        self.feature = feature
        self.treshold = treshold
        self.children = children
        self.classification = classification
        self.epsilon = epsilon
        if data is not None:
            self.num_of_examples_classified_true = data['diagnosis'].sum()
            self.num_of_examples_classified_false = len(data.index) - self.num_of_examples_classified_true
            self.examples=data

    def getNextChild(self, obj:pd.DataFrame):
        return self.children[0] if obj[1][self.feature] <= self.treshold else self.children[1]
    
	#def print(self):
    #   print(str(self.feature)+","+str(self.treshold)+","+str(self.classification))
    #   for child in self.children:
    #       child.print()

    def getAllSimplerExamples(self,obj:pd.DataFrame):
        def getSimiliarExamplesByEpsilon(tree: Node, obj: pd.DataFrame) -> list:
            if len(tree.children) == 0:
                #print("leaf ,child of "+ str(i))
                return tree.examples.values.tolist()
            similiar_examples = []
            for child in tree.getKNN_EPSILONNextChildrenByEpsilon(obj):
                # print("feature : "+str(tree.feature)+ " treshold : "+str(tree.treshold)+ " epsilon : " +str(tree.epsilon))
                child_similiar_examples = getSimiliarExamplesByEpsilon(child, obj)
                #print("child of "+ str(i)+"ok")
                similiar_examples.extend(child_similiar_examples)
            return similiar_examples

        return getSimiliarExamplesByEpsilon(self,obj)


    def getNextChildKNNEPSILON(self,obj):
        return self.children[0] if float(obj[self.feature].array[0]) <= self.treshold else self.children[1]

    def getKNN_EPSILONNextChildrenByEpsilon(self, obj:pd.DataFrame):
        if math.fabs(float(obj[self.feature].array[0]) - self.treshold) <= self.epsilon:
            return self.children
        else:
            return [self.getNextChildKNNEPSILON(obj)]
        pass


    def getNextChildrenByEpsilon(self, obj:pd.DataFrame):

        # next_children = []
        # if obj[1][self.feature] <= self.treshold + self.epsilon:
        #     next_children.append(self.children[0])
        #
        # if obj[1][self.feature] > self.treshold - self.epsilon:
        #     next_children.append(self.children[1])
        # return next_children

        if math.fabs(obj[1][self.feature]-self.treshold) <= self.epsilon:
            return self.children
        else:
            return [self.getNextChild(obj)]
        pass

    def DT_Classify(self, obj: pd.DataFrame):
        if len(self.children) == 0:
            return self.classification
        next_child = self.children[0]if obj[1][self.feature] <= self.treshold else self.children[1]
        return next_child.DT_Classify(obj)


    def DTEpsylon_Classify(self, obj: pd.DataFrame):
        def sumListAsVector(a:list, b:list) -> list:
            return [(a[0]+b[0]),(a[1]+b[1])]
        def countNumSimiliarExamplesByEpsilon(tree: Node, obj: pd.DataFrame) -> list:
            if len(tree.children) == 0:
                #print("leaf ,child of "+ str(i))
                return [tree.num_of_examples_classified_true, tree.num_of_examples_classified_false]
            total_true_false_duo = [0, 0]
            for child in tree.getNextChildrenByEpsilon(obj):
                # print("feature : "+str(tree.feature)+ " treshold : "+str(tree.treshold)+ " epsilon : " +str(tree.epsilon))
                child_true_false_duo = countNumSimiliarExamplesByEpsilon(child, obj)
                #print("child of "+ str(i)+"ok")
                total_true_false_duo = sumListAsVector(total_true_false_duo, child_true_false_duo)
            return total_true_false_duo

        total_true_false_duo = countNumSimiliarExamplesByEpsilon(self,obj)
        num_of_true_similiar_examples, num_of_false_similiar_examples =  total_true_false_duo
        if num_of_true_similiar_examples == num_of_false_similiar_examples:
            return DEFAULT_CLASSIFICATION
        else:
            return 1 if num_of_true_similiar_examples > num_of_false_similiar_examples else 0


def majorityClass(data: pd.DataFrame)->int:

    # count the values that there Classification is 1
    classification_one = data['diagnosis'].sum()
    # count the values that there Classification is 0
    classification_zero = len(data.index) - classification_one
    if classification_zero > classification_one :
        return 0
    elif classification_zero < classification_one:
        return 1
    else:
        return DEFAULT_CLASSIFICATION


def getClassificationCount(data: pd.DataFrame)-> list:
    # count the values that there Classification is 1
    one_count = data['diagnosis'].sum()
    total_count = len(data['diagnosis'].index)
    zero_count = total_count - one_count
    num_of_examples_classified_true = one_count
    # count the values that there Classification is 0
    num_of_examples_classified_false = zero_count

    return [num_of_examples_classified_true,num_of_examples_classified_false]


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
    for feature in features:
        #print(str(feature))

        # examples_data_sorted_by_feature =examples_data.sort_values(by=[feature])
        # feature_values_list=list(examples_data_sorted_by_feature[feature])
        # feature_values_list=list(examples_data_sorted_by_feature[feature])
        #examples_sorted_by_feature =(examples_data[feature]).sort_values(by=[feature])
        #examples_data.sort_values(by=[feature])
        examples_data_sorted_by_feature = examples_data.sort_values(by=[feature])
        feature_values_list = list(examples_data_sorted_by_feature[feature])
        tresholds = [(x+y)/2 for x,y in zip(feature_values_list, feature_values_list[1:])]
        for t in tresholds:

            left_examples = examples_data[examples_data[feature] <= t]
            right_examples = examples_data[examples_data[feature] > t]
            curIG = calcIG(examples_data, left_examples, right_examples)
            if curIG > bestIG:
                best_feature, best_treshold, bestIG = feature, t, curIG
    return best_feature, float(best_treshold)
    pass



def DT_Classify(obj: pd.DataFrame, tree: Node):
        if len(tree.children) == 0:
            return tree.classification
        return DT_Classify(obj, tree.getNextChild(obj))






def calcIG(examples,left_examples:pd.DataFrame,right_examples:pd.DataFrame):
   # start_time= time.time()
    def get_counts(df:pd.DataFrame) -> (int, int , int):
        one_count = df['diagnosis'].sum()
        total_count = len(df.index)
        zero_count=total_count-one_count
        #zero_count = len(df.loc[df['diagnosis'] == 0])
        #one_count = len(df.loc[df['diagnosis'] == 1])
        return zero_count,one_count,total_count

    def calculate(numerator,denominator) -> float :
        if float(numerator) == 0:
            return 0
        fraction = (float(numerator)/float(denominator))
        return (fraction)*math.log(fraction,2)

    left_count_zero, left_count_one,left_count_total =get_counts(left_examples)
    right_count_zero, right_count_one, right_count_total = get_counts(right_examples)
    father_count_zero, father_count_one, father_count_total = get_counts(examples)
    left_h =- (calculate(left_count_zero,left_count_total) + calculate(left_count_one,left_count_total))
    right_h = - (calculate(right_count_zero, right_count_total) + calculate(right_count_one, right_count_total))
    father_h = - (calculate(father_count_zero, father_count_total) + calculate(father_count_one, father_count_total))

    return  father_h -((left_count_total/father_count_total)*left_h)- ((right_count_total/father_count_total)*right_h)





class MakeLeaf:
    def __init__(self, minimum_example_limit):
        self.minimum_example_limit = minimum_example_limit

    def examplesLessThanLimit(self, examples_data:pd.DataFrame):
        if len(examples_data) <= self.minimum_example_limit:
            return True
        return False

    def basicLeafTest(self,examples_data: pd.DataFrame):
        if examples_data.empty:
            return Node(None, None, [], DEFAULT_CLASSIFICATION,  data = examples_data)

        classification = majorityClass(examples_data)
        if allExamplesAreSameClass(classification=classification, examples_data=examples_data):
            return Node(None, None, [], classification,  data = examples_data)
        return None

    def basicTestAndAtLeastXExamples(self,examples_data: pd.DataFrame):
        classification = majorityClass(examples_data)
        #num_of_examples_classified_false, num_of_examples_classified_true = getClassificationCount(examples_data)
        if len(examples_data) <= self.minimum_example_limit:
            #num_of_examples_classified_false,num_of_examples_classified_true= getClassificationCount(examples_data)
            return Node(None, None, [], classification, data = examples_data)
        return self.basicLeafTest(examples_data)




def DT_Classify(obj:pd.DataFrame , tree:Node):
    if len(tree.children)==0:
        return tree.classification
    return DT_Classify(obj, tree.getNextChild(obj))
    pass


def TDIDT(examples_data:pd.DataFrame, selectFeature_f, makeLeaf=MakeLeaf(0)):
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
    #assert ALL_TRAIN_DATA.equals(examples_data)
    return Node(feature, treshold, [left_child, right_child], classification,
                epsilon=0.1*float(np.std(ALL_TRAIN_DATA[feature].to_list())) )


RECALC = 0

def ID3(examples_data:pd.DataFrame,selectFeature_f=MaxIG, makeLeaf=MakeLeaf(0)):
    global ALL_TRAIN_DATA
    ALL_TRAIN_DATA = examples_data.copy()
    #classification = majorityClass(examples_data)
    return TDIDT(examples_data, selectFeature_f, makeLeaf)


##############################################################################
def getClassifier(name, train_data, min_example_limit=0, recalc=0):
    if recalc == 1:
        start_time = time.time()
        classifier = ID3(train_data, MaxIG, MakeLeaf(min_example_limit))

        print(str(time.time()-start_time) + " sec")
        to_file = open(name, "wb")
        pickle.dump(classifier, to_file)
        to_file.close()
        print("classifier : "+ name+ " build file was created")
        return classifier
    else:
        from_file = open(name, "rb")
        classifier = pickle.load(from_file)
        from_file.close()
        return classifier


def TestBasic(name ,classifier : Node, test_data, train_data=None):
    i=0
    if train_data is not None:
        ok=0
        not_ok=0
        for example in train_data.iterrows():
            if classifier.DT_Classify(example) == example[1]['diagnosis']:
            #if DT_Classify(example, classifier) == example[1]['diagnosis']:
                ok += 1
            else:
                not_ok += 1
            i += 1 #debug
            #print(str(i))
        total = ok + not_ok
        print("Training test results for Classifier : " + name)
        print("Correct Answers: " + str(ok / total) + "     Incorrect Answers: " + str(not_ok / total))
        print("##########################################################################################")
    ok = 0
    not_ok = 0
    for example in test_data.iterrows():
        if classifier.DT_Classify(example) == example[1]['diagnosis']:
        #if DT_Classify(example, classifier) == example[1]['diagnosis']:
            ok += 1
        else:
            not_ok += 1
        # i += 1
        # print(str(i))
    total = ok + not_ok
    print("Real Test results for Classifier : " + name)
    print("Correct Answers: " + str(ok / total) + "     Incorrect Answers: " + str(not_ok / total))
    print("##########################################################################################")

def TestEpsylon(name ,classifier : Node, test_data, train_data=None):
    if train_data is not None:
        ok=0
        not_ok=0
        DEBUG =0
        for example in train_data.iterrows():
            if classifier.DTEpsylon_Classify(example) == example[1]['diagnosis']:
                ok += 1
            else:
                not_ok += 1
            #i += 1
            # print(str(i))
        total = ok + not_ok
        print("Training test results for Epsylon Classifier : " + name)
        print("Correct Answers: " + str(ok / total) + "     Incorrect Answers: " + str(not_ok / total))
        print("##########################################################################################")
    ok = 0
    not_ok = 0
    DEBUG =1
    i = 1
    for example in test_data.iterrows():
        if classifier.DTEpsylon_Classify(example) == example[1]['diagnosis']:
            #print("example "+str(i)+" : true ")
            ok += 1
        else:
            #print("example " + str(i) + " : false")
            not_ok += 1
        i += 1
        # print(str(i))
        DEBUG =0
    total = ok + not_ok
    print("Real Test results for Epsylon Classifier : " + name)
    print("Correct Answers: " + str(ok / total) + "     Incorrect Answers: " + str(not_ok / total))
    print("##########################################################################################")




if __name__ == '__main__':

    train_data:pd.DataFrame =pd.read_csv('train.csv')
    test_data : pd.DataFrame= pd.read_csv('test.csv')
    ALL_TRAIN_DATA =train_data.copy()
    # features = [f for f in  train_data.columns[1:]]
    # for f in features:
    #     print (0.1*train_data[f].std())

  #  classifier_reg = getClassifier("classifier_reg",train_data, recalc =1)
  #  TestBasic("Basic Classifier", classifier_reg, test_data,train_data)
  #  TestEpsylon("Basic Classifier", classifier_reg, test_data,train_data)

    classifier_9 = getClassifier("classifier_reg_def_class_false",train_data,min_example_limit=9,recalc =0)
    TestBasic("classifier_reg_def_class_false",classifier_9,test_data,train_data)
   # TestBasic("classifier_9", classifier_9, test_data,train_data)
    TestEpsylon("classifier_9", classifier_9, test_data,train_data)


    pass

