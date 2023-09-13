import tkinter as tk
from tkinter import filedialog
import os
import pandas as pd
import xlrd  #读取Excel文件的包
import xlsxwriter   #将文件写入Excel的包
 
 
#打开excel
def OpenExcel(Filepath):
    try:
        file=xlrd.open_workbook(Filepath)
        return file
    except Exception as e:
        print(e)

#使用pandas读取excel
def ReadExcel(Filepath):
    try:
        data=pd.read_excel(Filepath)
        return data
    except Exception as e:
        print(e)

#获取Excel中所有的sheet
def GetAllSheets(file):
    return file.sheets()
 
#获取某个sheet表的行数
def GetAllRows(table):
    return table.nrows
 
#读取文件内容
def GetContent(excel,sheetNo):
    content=list()
    try:
        sheets=GetAllSheets(excel)
        table=sheets[sheetNo]
    except Exception as e:
        print(e)
    rows=GetAllRows(table)
    for i in range(rows):
        data=table.row_values(i)#第i行的数据
        content.append(data)
    return content
 
#所有的Excel的所有sheets变成一个sheet
def Sum1(fileName,data):
    '''
    将所有文件的sheet整合到一个sheet中
    '''
    finalFile=xlsxwriter.Workbook(fileName)#创建一个工作表文件
    sheet=finalFile.add_worksheet()#添加一个sheet
    count=0
    for sheetId in range(len(data)):
        for row in range(len(data[sheetId])):
             for col in range(len(data[sheetId][row])):
                d=data[sheetId][row][col]
                sheet.write(count,col,d)
             count=count+1
    finalFile.close()
 
if __name__=='__main__':
    root = tk.Tk()
    root.withdraw()
    folderPath = filedialog.askdirectory() #获得选择好的文件夹
    #Filepath = filedialog.askopenfilename() #获得选择好的文件
    data=list()
    fileSet=os.listdir(folderPath)
    for file in fileSet:
        if file.endswith('.xls'):
            print('OpenExcel')
            try:
                excel=OpenExcel(folderPath+'/'+file)
            except Exception as e:
                print(e)
            sheets=GetAllSheets(excel)
            for i in range(len(sheets)):
                data.append(GetContent(excel,i))
        if file.endswith('.xlsx'):
            print('ReadExcel')
            try:
                excel=ReadExcel(folderPath+'/'+file)
            except Exception as e:
                print(e)
            sheets=GetAllSheets(excel)
            for i in range(len(sheets)):
                data.append(GetContent(excel,i))
                
    fileName=str('/final.xlsx')
    finalFilePath=folderPath+fileName
    Sum1(finalFilePath,data)