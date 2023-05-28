import json
#from readline import append_history_file
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import pandas as pd
import math


productlist = []
userlist = []
ratinglist = []


def main():
  f = open("Automotive.json", "r")

  x = 0
  
  print("parsing")

  x = 0
  for line in f:
    x += 1
    
    if x > 5*1000:
      break
      #TEST.write(line)
      
    else:
      #TRAIN.write(line)
      l = json.loads(line)
      ratinglist.append(l['overall'])
      userlist.append(l['reviewerID'])
      productlist.append(l['asin'])
  print("Creating Dataset")
  dataset = pd.DataFrame(list(zip(productlist, userlist, ratinglist))) 
  dataset.columns =['ProductID', 'UserId', 'UserRating']

  print("AVG CALC")

  truth = []

  for index, row in dataset.iterrows():
    rel = dataset[dataset['ProductID'].isin([row['ProductID']])]
    rel = rel['UserRating'].tolist()

    avg = -1

    for i in rel:
      if avg == -1:
        avg = i
      else:
        avg = (avg + i)/2

    if avg == -1:
      avg = 5

    
    truth.append(avg)



  dataset['average'] = truth

  print("SPLIT")

  train, test = train_test_split(dataset, test_size=0.2)
  train = train.reset_index(drop=True)
  test = test.reset_index(drop=True)

  print("TESTS")

  x = 0
  predicted = []
  users = []
  items = []
  for index, row in test.iterrows():
    # x += 1
    # if x>100:
    #   break
    #print(row['UserId'])
    #print(row)

    if row['UserId'] not in users:
      users.append(row['UserId'])
    #items.append(row['ProductID'])

    rel = train[train['ProductID'].isin([row['ProductID']])]
    rel = rel['UserRating'].tolist()

    avg = -1

    for i in rel:
      if avg == -1:
        avg = i
      else:
        avg = (avg + i)/2

    if avg == -1:
      avg = 5

    predicted.append(avg)


  #Mean Absolute Error (MAE) and Root Mean Square Error (RMSE) 

  test['p'] = predicted

  mse = mean_squared_error(test['UserRating'], test['p'])
  rmse = math.sqrt(mse)
  print("RootMSE")
  print(rmse)

  mae = mean_absolute_error(test['UserRating'], test['p'])
  print("MeanAbsoluteError")
  print(mae)  

  #print(len(test.index))
  #NOW Ranking
  #rank = pd.DataFrame(list(zip(users, predicted, items))) 
  #rank.columns =['UserId', 'UserRating', 'ProductID']
  predicted = []
  for index, row in train.iterrows():

    rel = train[train['ProductID'].isin([row['ProductID']])]
    rel = rel['UserRating'].tolist()

    avg = -1

    for i in rel:
      if avg == -1:
        avg = i
      else:
        avg = (avg + i)/2

    if avg == -1:
      avg = 5

    predicted.append(avg)

  train['p'] = predicted

  dataset.average = dataset.average.astype(float)

  train.p = train.p.astype(float)

  dataset = dataset.sort_values(by='average', ascending=False)
  rank = dataset['average'].tolist()
  train = train.sort_values(by='p', ascending=False)
  te = train['p'].tolist()
  #P is correct out of 10
  #R is correct out of 10
  #F is 2 (P*R)/(P+R)

  P = -1
  R = -1
  F = -1
  C = -1

  #Conversion rate is number in both
  for user in users:
    u = train[train['UserId'].isin([user])]
    usersps = u['ProductID'].tolist()
    rankc = rank.copy()
    for i in usersps:
      try:
        rankc.remove(i)
      except:
        NotImplemented

    tec = te.copy()
    for i in usersps:
      try:
        tec.remove(i)
      except:
        NotImplemented
    count = 0
    for i in range(10):
      
      if rankc[i] == tec[i]:
        count += 1
    if count == 0:
      count = 0.00000000000000001
    if P == -1:
      P = count/10
      R = count/10
      F = 2*(P*R)/(P+R)
      C = count
    else:
      P = (P +count/10)/2
      R = (R +count/10)/2
      F = (F + 2*(P*R)/(P+R))/2
      C = (C+count)/2


  print("Precision, Recall, F-measure, Conversion Rate")
  print(P,R,F,C)


  print("DONE!")

main()