import os
import pandas as pd

def createDataframe(filePath):
    inputData = pd.ExcelFile(filePath)
    print(filePath)
    df = inputData.parse()
    df = df.drop(index=df.index[[0, 1]])
    df = df.dropna(axis=1)
    return df, len(df)


if __name__ == '__main__':
    path = './data/'
    fileList = os.listdir(path)
    df = pd.DataFrame()
    dfLength = 0
    for file in fileList:
        df1, length = createDataframe(path + file)
        dfLength += length
        df = pd.concat([df, df1], ignore_index=True)
    print(df)
    df.to_csv('table2.csv', sep='\t', index=False, header=False)
    print(len(df))
    print(dfLength)