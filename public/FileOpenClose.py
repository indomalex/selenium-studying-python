#coding:utf-8
import os
import csv

def openMyFile(path, way="r"):
    try:
        file = open(path, way)
    except OSError as info:
        print(str(info))
    return file

def closeMyFile(file):
    file.close()
    
def readLinesFromMyFile(file):
    return file.readlines()
        
def readLinesFromMyCSVFile(file):
    data = csv.reader(file);
    return data

def writeToMyFile(file, txt):
    file.write(txt)
    