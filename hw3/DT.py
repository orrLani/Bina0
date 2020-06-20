import numpy
import sklearn
import pandas


DEFULT = 0


class Junction:
    def __init__(self,feature:str,children:list,classes:int):
        self.feature = feature
        self.children = children
        self.classes = classes


def majorityClass(examples: pandas.DataFrame)->int:
    # count the values that there Classification is 0
    classification_zero = examples.loc[examples['diagnosis'] == 0, 'diagnosis'].sum()
    # count the values that there Classification is 1
    classification_one = examples.loc[examples['diagnosis'] == 1, 'diagnosis'].sum()
    if classification_zero> classification_one :
        return classification_zero
    return classification_one


def get_class_from_example(example: pandas.DataFrame) -> int:
    return example['diagnosis']

def is_all_examples_have_same_class(classification:int ,examples: pandas.DataFrame) -> bool:
    # classification = get_class_from_example(examples.iloc[[0]])
    for i in range(0,(data_train.shape[0]+1)):
        if classification != get_class_from_example(examples.iloc[[i]]) :
            return False

    return True


def ID3(examples:pandas.DataFrame,features:list):
    classification = majorityClass(examples)
    return TDIDT(examples,features,classification,MaxIG)


def MaxIG(features:list,Examples:pandas.DataFrame):

    for feature in features;


    pass


def TDIDT(examples:pandas.DataFrame, features:list,classification, select_feature_function):

    # if no examples in the data frame
    if examples.empty:
        return Junction(None, [], DEFULT)
    # classification = majorityClass(examples)

    #  if no features in the data frame or every example have the same classification
    if len(list(examples.columns)) == 1 or is_all_examples_have_same_class(classification=classification,
                                                                           examples= examples):
        return Junction(None,[],classification)

    feature = select_feature_function(features, examples)



if __name__ == '__main__':
    data_train:pandas.DataFrame =pandas.read_csv('train.csv')











