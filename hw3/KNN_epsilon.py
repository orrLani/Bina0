from KNN import KNN
import DT
import pandas as pd
from sklearn import preprocessing


def normalization(self, data: list):
    for i in range(0, len(data)):
        for j in range(1, len(data[i])):
            # print(data[i][j])
            data[i][j] = (data[i][j] - self.min_value_list[j]) / \
                         (self.max_value_list[j] - self.min_value_list[j])
            # assert data[i][j] == self.train_data_list[i][j]


class KNN_EPSILON(KNN):
    def __init__(self,k,train_data: pd.DataFrame,test_data: pd.DataFrame):
        super().__init__(k,train_data)
        self.train_data_frame = train_data
        self.test_data_frame = test_data
        self.normalization_data_frame( self.train_data_frame)
        self.normalization_data_frame(self.test_data_frame)
        self.T_9_tree= DT.getClassifier("classifier_reg_def_class_false", self.train_data_frame, min_example_limit=9, recalc=1)


    def normalization_data_frame(self,data:pd.DataFrame):
        for i in range(0,len(data.index)):
            for j in range(1,len(self.train_header_list)):
                data.at[i,self.train_header_list[j]] =(data.at[i,self.train_header_list[j]]-
                                                             self.min_value_list[j])/\
                    (self.max_value_list[j] - self.min_value_list[j])


    def run(self):
        succ =0
        faild =0
        for example in self.test_data_frame.values.tolist():
            df_example =pd.DataFrame([example],columns=self.train_header_list)
            list_of_child_examples = self.T_9_tree.getAllSimplerExamples(df_example)
            df_child_examples = pd.DataFrame(list_of_child_examples)
            len_of_examples=len(df_child_examples.index)
            if len_of_examples<9:
                example_ser=pd.Series(example,index=self.train_header_list)
                classification_result=self.T_9_tree.DTEpsylon_Classify((0,example_ser))
            else:
                knn = KNN(k=9, train_data=df_child_examples,normalization=False)
                classification_result = knn.classification(example)

            if classification_result == example[0]:
                succ+=1
            else:
                faild+=1
        print("the accuarcy is"+str(succ/(succ+faild)))

if __name__ == '__main__':
    train_data: pd.DataFrame = pd.read_csv('train.csv')
    test_data: pd.DataFrame = pd.read_csv('test.csv')
    knn_epsilon = KNN_EPSILON(k=9,train_data=train_data,test_data=test_data)
    knn_epsilon.run()



