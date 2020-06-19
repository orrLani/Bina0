import numpy
import sklearn
import pandas


DEFULT = 0


class Junction:
    def __init__(self,feature:str,children:list,classes:int):
        self.feature = feature
        self.children = children
        self.classes =classes


def majorityClass(examples:pandas.DataFrame):
    pass

def TDIDT(data_train:pandas.DataFrame,features:list,select_feature:list):
    if len(examples)==0:
        return Junction(None,[],DEFULT)
    our_class = majorityClass(examples)




if __name__ == '__main__':
    data_train:pandas.DataFrame =pandas.read_csv('train.csv')
    TDIDT()










