import pandas as pd
import sklearn
import math
class KNN:
    def __init__(self,k:int,train_data:pd.DataFrame,normalization=True):
        self.k = k
        self.train_header_list = train_data.columns.values.tolist()
        self.train_data_list = train_data.values.tolist()
        self.max_value_list = [train_data[header].max() for header in self.train_header_list]
        self.min_value_list = [train_data[header].min() for header in self.train_header_list]
        if normalization:
            self.normalization(self.train_data_list)

    def normalization(self,data:list):
        for i in range(0,len(data)):
            for j in range(1, len(data[i])):
               # print(data[i][j])
                data[i][j] =(data[i][j] - self.min_value_list[j])/\
                                            (self.max_value_list[j]-self.min_value_list[j])
                # assert data[i][j] == self.train_data_list[i][j]

    def classification(self,test_data_row:list)->int:
        distance_tuple = []
        zero_count = 0
        one_count  = 0
        classification_result = 0
        distance = 0
        for i in range(0,len(self.train_data_list)):
            for j in range(1,len(self.train_data_list[i])):
                distance+=(self.train_data_list[i][j] - test_data_row[j])**2
            distance=math.sqrt(distance)
            distance_tuple.append((distance,self.train_data_list[i][0]))
            distance=0
        distance_tuple.sort(key=lambda tuple:tuple[0])
        # find classification
        for i in range(0,self.k):
            if distance_tuple[i][1] == 0:
                zero_count+=1
            else:
                one_count+=1

        if one_count>=zero_count:
            classification_result=1
        else:
            classification_result=0

        return classification_result

    def test_data(self,test_data:pd.DataFrame):
        test_data_list_header = test_data.columns.values.tolist()
        test_data_list_values = test_data.values.tolist()
        accuracy_test = 0
        self.normalization(test_data_list_values)
        for i in range(0, len(test_data_list_values)):
            if test_data_list_values[i][0] ==self.classification(test_data_list_values[i]):
                accuracy_test+=1
        return accuracy_test/len(test_data_list_values)



if __name__ == '__main__':

    train_data: pd.DataFrame = pd.read_csv('train.csv')
    test_data: pd.DataFrame = pd.read_csv('test.csv')
    k_list =[1,3,9,27]
    accuracy =[]

    for k in k_list:
        knn = KNN(k=k,train_data=train_data)
        accuracy.append(knn.test_data(test_data))


    print(accuracy)








