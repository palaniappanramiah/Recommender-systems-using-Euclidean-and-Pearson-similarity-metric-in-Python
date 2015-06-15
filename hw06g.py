#!/usr/bin/python3
#Class    : CSCI 680-A5
#Program  : HW06 - Graduate Project
#Author   : Palaniappan Ramiah
#Z-number : z1726972
#Date Due : 04/30/2015
#Purpose  : To implement recommender systems. This takes a movie name as an
#           input & finds the 20 closest movie based on the rating of others
#           using Euclidean and Pearson similarity metrics and their relation
#Execution: ./hw06g.py
#Comments : Used the hw4 data. Didn't attach the data with the assignment.

import operator
import math

movieNamesFile = 'movie-names.txt'
movieMatrixFile = 'movie-matrix.txt'

movieNames = []
movieMatrix = []
dictMovieLists = {}
eucliMovieLists = {}

#Function to calculate the pearson value
def calcPearson(selectedList, dictMovieLists):
    dictPearson = {}
    listA = selectedList
    listB = []
    matrixLen = len(movieMatrix[0])
    for key, value in dictMovieLists.items():
        listB = value
        i = 0
        sumA = 0
        sumB = 0
        count = 0
        while i < matrixLen:
            if listA[i] != '' and listB[i] != '':
                sumA += float(listA[i])
                sumB += float(listB[i])
                count += 1
            i += 1
        meanA = sumA / count
        meanB = sumB / count
        i = 0
        stdA = 0
        stdB = 0
        count = 0
        while i < matrixLen:
            if listA[i] != '' and listB[i] != '':
                stdA += pow((meanA - float(listA[i])),2)
                stdB += pow((meanB - float(listB[i])),2)
                count += 1
            i += 1
        stdA = pow(stdA / (count-1), 0.5)
        stdB = pow(stdB / (count-1), 0.5)
        i = 0
        pearson = 0
        count = 0
        while i < matrixLen:
            if listA[i] != '' and listB[i] != '':
                try:
                    pearson += ((float(listA[i]) - meanA)/stdA)*((float(listB[i]) - meanB)/stdB)
                    count += 1
                except(ZeroDivisionError):
                    break
            i += 1
        pearson = pearson / (count-1)
        dictPearson[key] = pearson
    return dictPearson

#Function to compare the movie values
def compMovies(movieNumber):
    print("Fetching top 20 comparison movies...\n")
    movieNumber -= 1
    dictMovieLists.clear()
    eucliMovieLists.clear()
    selectedList = movieMatrix[movieNumber]
    length = len(selectedList)
    listNum = 0
    for selList in movieMatrix:
        i = 0
        personCount = 0
        dist = 0
        while i < length:
            if selList[i] != '' and selectedList[i] != '':
                dist += math.pow(int(selList[i]) - int(selectedList[i]), 2)
                personCount += 1
            i += 1
        if personCount >= 10:
            dictMovieLists[listNum] = selList
            eucliMovieLists[listNum] = 1/(1+math.sqrt(dist))
        listNum += 1
    dictPearson = calcPearson(selectedList, dictMovieLists)
    compMoviesCount = len(dictPearson)
    eucliMovieCount = len(eucliMovieLists)
    
    if compMoviesCount >= 20 and eucliMovieCount >= 20:
        dictPearsonOrdered = dict(sorted(dictPearson.items(),
                                key = lambda x : x[1], reverse=True)[:20])
        dictEuclideanOrdered = dict(sorted(eucliMovieLists.items(),
                                key = lambda x : x[1], reverse=True)[:20])
        
        similarMovies = (set(dictPearsonOrdered.keys()) & set(dictEuclideanOrdered.keys()))
        
        dictPearsonOrdered = sorted(dictPearsonOrdered.items(),
                                key=operator.itemgetter(1), reverse=True)
        dictEuclideanOrdered = sorted(dictEuclideanOrdered.items(),
                                key=operator.itemgetter(1), reverse=True)
        print("The movies that are similar to the inputed movie according to the Pearson are:")
        i = 1
        print("{:>3} {:<69} {:>7}".format("No.", "Movie Name", "Pearson value"))
        for key, value in dictPearsonOrdered:
            print("{:>3} {:<75} {:>7}".format(i,
                                        movieNames[key], round(float(value),4)))
            i += 1
        print()
        print("The movies that are similar to the inputed movie are according to the euclidean are:")
        i = 1
        print("{:>3} {:<67} {:>7}".format("No.", "Movie Name", "Euclidean value"))
        for key, value in dictEuclideanOrdered:
            print("{:>3} {:<75} {:>7}".format(i,
                                        movieNames[key], round(float(value),4)))
            i += 1
        print()
        i = 1
        print("The movies that are similar according to both the similarities are:")
        print("{:>3} {:<69}".format("No.", "Movie Name"))
        for key in similarMovies:
            print("{:>3} {:<75}".format(i,movieNames[key]))
            i += 1
        print()
    else:
        print("Insufficient comparison movies\n")

flag = True
try:
    file = open(movieNamesFile, "r", encoding="latin-1")
    for line in file:
        movie = line.split('|')[1].rstrip('\n')
        movieNames.append(movie)
except(OSError, IOError):
    print("File with the name ",  movieNamesFile, " is not found")

try:
    file = open(movieMatrixFile, "r", encoding="latin-1")
    for line in file:
        matrix = []
        matrix.append(line.rstrip('\n').split(';'))
        movieMatrix.append(matrix[0])
except(OSError, IOError):
    print("File with the name ",  movieMatrixFile, " is not found")

while flag:
    movieNum = input('Enter a movie number or q/quit to exit: ')
    if movieNum.isdigit():
        if int(movieNum) > 0 and int(movieNum) <= len(movieNames):
            print('\nYou have chosen ',movieNum,' | ',
                  movieNames[int(movieNum)-1])
            print()
            compMovies(int(movieNum))
        else:
            print('\nEnter a number from 1 - ', len(movieNames))
            print()
    elif (movieNum.isalpha() and (movieNum.lower() == 'q' or movieNum.lower() == 'quit')):
            print('Thanks!')
            flag = False
    else:
        print('\nEnter a NUMBER from 1 - ', len(movieNames))
        print()