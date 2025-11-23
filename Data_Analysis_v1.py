from typing import Any, List, Dict
from math import ceil, floor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math


class sample:
    def __init__(self, inDataset: pd.DataFrame, inputColumnName: str = None, inputColumnValue = None, outputColName: str = None, label: str = None, start: int = 0, end: int = None, subsetType: str = "IQR", skipInitialization: bool = False):
        self.label = label
        
        

        self.start = start
        self.end = end

        self.mainDataset = inDataset
        
        
        
        self.subsetType = subsetType
        self.subset: pd.DataFrame = pd.DataFrame()
        self.quartileIndexes = {
            "Q1": {
                "start": None,
                "end": None
            },
            "Q2": {
                "start": None,
                "end": None
            },
            "Q3": {
                "start": None,
                "end": None
            },
            "Q4": {
                "start": None,
                "end": None
            },
        }
        self.startIndex_subset: int = None
        self.endIndex_subset: int = None
        self.startQuartile_subset: str = None
        self.endQuartile_subset: str = None


        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.subsetType_main = subsetType
        self.subset_main: pd.DataFrame = pd.DataFrame()
        self.quartileIndexes_main = {
            "Q1": {
                "start": None,
                "end": None
            },
            "Q2": {
                "start": None,
                "end": None
            },
            "Q3": {
                "start": None,
                "end": None
            },
            "Q4": {
                "start": None,
                "end": None
            },
        }
        self.startIndex_subset_main: int = None
        self.endIndex_subset_main: int = None
        self.startQuartile_subset_main: str = None
        self.endQuartile_subset_main: str = None

        if outputColName != None:
            self.setQuartileIndexes_main()
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


        

        if(inputColumnName != None and inputColumnValue != None and outputColName != None):
            self.changeTargetColumns(inputColumnName, inputColumnValue, outputColName)
        else:
            self.inputColumnName = inputColumnName
            self.inputColumnValue = inputColumnValue
            self.outputColName = outputColName
            self.inputColumnInfo = {
            self.inputColumnName: self.inputColumnValue
        }
        
    

    def changeinputColumnValue_subset(self, inputColumnValue, inputColumnName:str = None):
        self.inputColumnValue = inputColumnValue

        if inputColumnName != None:
            self.inputColumnName = inputColumnName

        if math.isnan(self.inputColumnValue):
            self.data_unsorted: pd.DataFrame = self.mainDataset[self.mainDataset[self.inputColumnName].isna()]
        else:
            self.data_unsorted: pd.DataFrame = self.mainDataset[self.mainDataset[self.inputColumnName] == self.inputColumnValue]
        
        self.data: pd.DataFrame = self.data_unsorted.sort_values(by=self.outputColName)

        self.setQuartileIndexes()

        if(self.subset.empty == False):
            self.setSubset()

    def changeOutputColumn_main(self, inOutputColName):
        self.outputColName = inOutputColName

        self.mainDataset: pd.DataFrame = self.mainDataset.sort_values(by=self.outputColName)
        
        self.setQuartileIndexes_main()

        if(self.subset_main.empty == False):
            self.setSubset_main()
        
    def changeTargetColumns(self, inputColumnName: str, inputColumnValue, inOutputColName):
        self.inputColumnName = inputColumnName
        self.inputColumnValue = inputColumnValue
        self.outputColName = inOutputColName

        if math.isnan(self.inputColumnValue):
            self.data_unsorted: pd.DataFrame = self.mainDataset[self.mainDataset[self.inputColumnName].isna()]
        else:
            self.data_unsorted: pd.DataFrame = self.mainDataset[self.mainDataset[self.inputColumnName] == self.inputColumnValue]


        self.data: pd.DataFrame = self.data_unsorted.sort_values(by=self.outputColName)

        self.setQuartileIndexes()

        if(self.subset.empty == False):
            self.setSubset()

    def setQuartileIndexes(self):
        self.quartileIndexes["Q1"]["start"] = 0
        self.quartileIndexes["Q4"]["end"] = len(self.data)

        self.quartileIndexes["Q2"]["end"] = ceil((self.quartileIndexes["Q4"]["end"]+self.quartileIndexes["Q1"]["start"])/2)
        self.quartileIndexes["Q3"]["start"] = floor((self.quartileIndexes["Q4"]["end"]+self.quartileIndexes["Q1"]["start"])/2)

        self.quartileIndexes["Q1"]["end"] = ceil((self.quartileIndexes["Q1"]["start"] + self.quartileIndexes["Q2"]["end"])/2)
        self.quartileIndexes["Q2"]["start"] = floor((self.quartileIndexes["Q1"]["start"] + self.quartileIndexes["Q2"]["end"])/2)

        self.quartileIndexes["Q3"]["end"] = ceil((self.quartileIndexes["Q3"]["start"] + self.quartileIndexes["Q4"]["end"])/2)
        self.quartileIndexes["Q4"]["start"] = floor((self.quartileIndexes["Q3"]["start"] + self.quartileIndexes["Q4"]["end"])/2)
    def printQuartileIndexes(self):
        print(f"Q1[{self.quartileIndexes["Q1"]["start"]}:{self.quartileIndexes["Q1"]["end"]}]\tQ2[{self.quartileIndexes["Q2"]["start"]}:{self.quartileIndexes["Q2"]["end"]}]\tQ3[{self.quartileIndexes["Q3"]["start"]}:{self.quartileIndexes["Q3"]["end"]}]\tQ4[{self.quartileIndexes["Q4"]["start"]}:{self.quartileIndexes["Q4"]["end"]}]")


    def setSubset(self, inSubsetType: str = None, inStartQuartile: str = "Q1", inEndQuartile: str = None, inStart:int = None, inEnd:int = None):
        self.setQuartileIndexes()
        
        if inSubsetType != None:
            self.subsetType = inSubsetType

        if inStartQuartile != None:
            self.startQuartile_subset = inStartQuartile
        if inEndQuartile != None:
            self.endQuartile_subset = inEndQuartile
        
        if inStart != None:
            self.startIndex_subset = inStart
        if inEnd != None:
            self.endIndex_subset = inEnd

        if self.subsetType == "IQR ":
            self.setSubset_IQR()
        elif self.subsetType == "Quartile" or self.subsetType == "quartile":
            self.setSubset_quartile(self.startQuartile_subset, endQuartile=self.endQuartile_subset)
        elif self.subsetType == "Range" or self.subsetType == "range":
            self.setSubset_range(self.startIndex_subset, self.endIndex_subset)
        else:
            self.setSubset_IQR()


    def setSubset_quartile(self, startQuartile: str, endQuartile: str = None):
        self.setQuartileIndexes()

        if endQuartile == None:
            endQuartile = startQuartile
        self.startQuartile_subset = startQuartile
        self.endQuartile_subset = endQuartile
        
        self.subset = self.data[self.quartileIndexes[self.startQuartile_subset]["start"]:self.quartileIndexes[self.endQuartile_subset]["end"]]
        self.numUnique_outCol_subset = len(self.subset[self.outputColName].unique())
        
    def setSubset_IQR(self):
        self.setSubset_quartile("Q2", "Q3")
        self.numUnique_outCol_subset = len(self.subset[self.outputColName].unique())
        
    def setSubset_range(self, inStart:int, inEnd:int):
        self.startIndex_subset = inStart
        self.endIndex_subset = inEnd
        self.subset = self.data[self.startIndex_subset:self.endIndex_subset]
        self.numUnique_outCol_subset = len(self.subset[self.outputColName].unique())
        
    



    #[Main Dataset]
    def setQuartileIndexes_main(self):
        self.quartileIndexes_main["Q1"]["start"] = 0
        self.quartileIndexes_main["Q4"]["end"] = len(self.mainDataset)

        self.quartileIndexes_main["Q2"]["end"] = ceil((self.quartileIndexes_main["Q4"]["end"]+self.quartileIndexes_main["Q1"]["start"])/2)
        self.quartileIndexes_main["Q3"]["start"] = floor((self.quartileIndexes_main["Q4"]["end"]+self.quartileIndexes_main["Q1"]["start"])/2)

        self.quartileIndexes_main["Q1"]["end"] = ceil((self.quartileIndexes_main["Q1"]["start"] + self.quartileIndexes_main["Q2"]["end"])/2)
        self.quartileIndexes_main["Q2"]["start"] = floor((self.quartileIndexes_main["Q1"]["start"] + self.quartileIndexes_main["Q2"]["end"])/2)

        self.quartileIndexes_main["Q3"]["end"] = ceil((self.quartileIndexes_main["Q3"]["start"] + self.quartileIndexes_main["Q4"]["end"])/2)
        self.quartileIndexes_main["Q4"]["start"] = floor((self.quartileIndexes_main["Q3"]["start"] + self.quartileIndexes_main["Q4"]["end"])/2)
    def printQuartileIndexes_main(self):
        print(f"Q1[{self.quartileIndexes_main["Q1"]["start"]}:{self.quartileIndexes_main["Q1"]["end"]}]\tQ2[{self.quartileIndexes_main["Q2"]["start"]}:{self.quartileIndexes_main["Q2"]["end"]}]\tQ3[{self.quartileIndexes_main["Q3"]["start"]}:{self.quartileIndexes_main["Q3"]["end"]}]\tQ4[{self.quartileIndexes_main["Q4"]["start"]}:{self.quartileIndexes_main["Q4"]["end"]}]")

    def setSubset_main(self, inSubsetType_main: str = None, inStartQuartile_main: str = "Q1", inEndQuartile_main: str = None, inStart_main:int = None, inEnd_main:int = None):
        self.setQuartileIndexes_main()
        
        if inSubsetType_main != None:
            self.subsetType_main = inSubsetType_main

        if inStartQuartile_main != None:
            self.startQuartile_subset_main = inStartQuartile_main
        if inEndQuartile_main != None:
            self.endQuartile_subset_main = inEndQuartile_main
        
        if inStart_main != None:
            self.startIndex_subset_main = inStart_main
        if inEnd_main != None:
            self.endIndex_subset_main = inEnd_main

        if self.subsetType_main == "IQR ":
            self.setSubset_IQR_main()
        elif self.subsetType_main == "Quartile" or self.subsetType_main == "quartile":
            self.setSubset_quartile_main(self.startQuartile_subset_main, endQuartile=self.endQuartile_subset_main)
        elif self.subsetType_main == "Range" or self.subsetType_main == "range":
            self.setSubset_range_main(self.startIndex_subset_main, self.endIndex_subset_main)
        else:
            self.setSubset_IQR_main()


    def setSubset_quartile_main(self, startQuartile: str, endQuartile: str = None):
        self.setQuartileIndexes_main()

        if endQuartile == None:
            endQuartile = startQuartile
        self.startQuartile_subset_main = startQuartile
        self.endQuartile_subset_main = endQuartile
        
        self.subset_main = self.mainDataset[self.quartileIndexes_main[self.startQuartile_subset_main]["start"]:self.quartileIndexes_main[self.endQuartile_subset_main]["end"]]
        self.numUnique_outCol_subset_main = len(self.mainDataset[self.outputColName].unique())
        
    def setSubset_IQR_main(self):
        self.setSubset_quartile_main("Q2", "Q3")
        self.numUnique_outCol_subset_main = len(self.mainDataset[self.outputColName].unique())
        
    def setSubset_range_main(self, inStart_main:int, inEnd_main:int):
        self.startIndex_subset_main = inStart_main
        self.endIndex_subset_main = inEnd_main
        self.subset_main = self.mainDataset[self.startIndex_subset_main:self.endIndex_subset_main]
        self.numUnique_outCol_subset_main = len(self.mainDataset[self.outputColName].unique())
        
    
    def visualize_dataset_main(self, isProbabilityGraph = True, figureID: int = 1):
        self.numUnique_outCol_main = self.mainDataset[self.outputColName].unique()

        self.bins_main = self.numUnique_outCol_main
        for i in range(0, len(self.bins_main)):
            if math.isnan(self.bins_main[i]):
                self.bins_main[i] = -1
                break
        self.bins_main = np.sort(self.bins_main)

        indexOfLastBin = len(self.bins_main) - 1
        self.bins_main = np.append(self.bins_main, self.bins_main[indexOfLastBin] +1)

        plt.figure(figureID)
        plt.hist(self.mainDataset[self.outputColName], bins=self.bins_main, density=isProbabilityGraph, edgecolor='black')
        if isProbabilityGraph:
            plt.title(f'Probability graph of {self.outputColName} for the whole dataset (i.e. main dataset)')
            plt.ylabel('Probability')
        else:
            plt.title(f'Histogram of {self.outputColName} for the whole dataset (i.e. main dataset)')
            plt.ylabel('Frequency')
        plt.xlabel('Value')
        
        plt.show()



    
    def visualize_dataset(self, isProbabilityGraph = True, figureID: int = 1):
        self.numUnique_outCol = self.data[self.outputColName].unique()

        self.bins = self.numUnique_outCol
        for i in range(0, len(self.bins)):
            if math.isnan(self.bins[i]):
                self.bins[i] = -1
                break
        self.bins = np.sort(self.bins)

        indexOfLastBin = len(self.bins) - 1
        self.bins = np.append(self.bins, self.bins[indexOfLastBin] +1)

        plt.figure(figureID)
        plt.hist(self.data[self.outputColName], bins=self.bins, density=isProbabilityGraph, edgecolor='black')
        if isProbabilityGraph:
            plt.title(f'Probability graph of {self.outputColName} for {self.inputColumnValue}')
            plt.ylabel('Probability')
        else:
            plt.title(f'Histogram of {self.outputColName} for {self.inputColumnValue}')
            plt.ylabel('Frequency')
        plt.xlabel('Value')
        
        plt.show()

    def visualize_subset(self, isProbabilityGraph = True):
        self.numUnique_outCol_subset = self.subset[self.outputColName].unique()
        self.bins_subset = self.numUnique_outCol_subset
        for i in range(0, len(self.bins_subset)):
            if math.isnan(self.bins_subset[i]):
                self.bins_subset[i] = -1
                break
        self.bins_subset = np.sort(self.bins_subset)

        indexOfLastBin = len(self.bins_subset) - 1
        self.bins_subset = np.append(self.bins_subset, self.bins_subset[indexOfLastBin] +1)
        
        plt.hist(self.subset[self.outputColName], bins=self.bins_subset, density=isProbabilityGraph, edgecolor='black')
        if isProbabilityGraph:
            plt.title(f'Probability graph of {self.outputColName} for {self.inputColumnValue}')
            plt.ylabel('Probability')
        else:
            plt.title(f'Histogram of {self.outputColName} for {self.inputColumnValue}')
            plt.ylabel('Frequency')
        plt.xlabel('Value')
        
        plt.show()


    def visualize_dataset_overlap(self, outputColumns, isProbabilityGraph = True, figureID: int = 1, columnsTitle: str = None):
        labels = []
        colors = ['blue', 'green', 'red', 'black', 'yellow', 'purple', 'orange', 'grey']
        n_bins = 30
        plt.figure(figureID)



        if columnsTitle == None:
            columnsTitle = ""
            for outputCoumnName in outputColumns:
                columnsTitle += outputCoumnName + ", "

        #[bins]-----
        unique_outputColumn = []
        for outputCoumnName in outputColumns:
            unique_outputColumn.extend(self.data[outputCoumnName].unique())

        minVal = min(unique_outputColumn)
        for i in range(0, len(unique_outputColumn)):
            if math.isnan(unique_outputColumn[i]):
                unique_outputColumn[i] = minVal-1

        numUnique_outputColumn = set(unique_outputColumn)
        bins = numUnique_outputColumn
                        
        bins = sorted(bins)
        indexOfLastBin = len(bins) - 1
        bins = np.append(bins, bins[indexOfLastBin] +1)
        #[bins]-----


        index = -1
        for outputCoumnName in outputColumns:
            index = index + 1
            currLabel = outputCoumnName
            labels.append(currLabel)

            

            plt.hist(self.data[outputCoumnName], bins=bins, density=isProbabilityGraph,alpha=0.6, label=currLabel, color=colors[index], edgecolor='black')



        if isProbabilityGraph:
            plt.title(f'Probability graph of {outputCoumnName} for {self.inputColumnValue}')
            plt.ylabel('Probability')
        else:
            plt.title(f'Histogram of {outputCoumnName} for {columnsTitle}')
            plt.ylabel('Frequency')
        plt.xlabel('Value')

        plt.show()
        
'''
[Variables]
title/lable
input column name(s)
output col name
quartile indexes
    Q1
        start
        end
    Q2
        start
        end
    Q3
        start
        end
    Q4
        start
        end

mainDataFrame
start
end
currDataFrame
'''

'''
[Functions]
update
    set input dictionary{
        column(s): [input value(s)]
        }
    choose {output} column
    sort based on column
-------------------------
[Quartiles]


setQuartileIndexes WWW
printQuartileIndexes WWW

(set curDataFrame)
    Quartile
    IQR
    Quariles / range of quartiles
    range
--------------------------
print histogram or probabilities WWWW
???save data (i.e. save info in describe())?


'''

