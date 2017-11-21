
## Project Overview
In 2000, Enron was one of the largest companies in the United States. By 2002, it had collapsed into bankruptcy due to widespread corporate fraud. In the resulting Federal investigation, a significant amount of typically confidential information entered into the public record, including tens of thousands of emails and detailed financial data for top executives. In this project, I am interested to put my new machine learning skills to use by building a person of interest identifier based on financial and email data made public as a result of the Enron scandal. 

## Skills Used
- Deal with an imperfect, real-world dataset
- Validate a machine learning result using test data
- Evaluate a machine learning result using quantitative metrics
- Create, select and transform features
- Compare the performance of machine learning algorithms
- Tune machine learning algorithms for maximum performance
- Communicate your machine learning algorithm results clearly

More specificly, they are :

Skills | Tasks
--- | ---
SUPERVISED CLASSIFICATION |Implement the Naive Bayes algorithm to classify text;Implement Support Vector Machines (SVMs) to generate new features independently on the fly;Implement decision trees as a launching point for more sophisticated methods like random forests and boosting
DATASETS AND QUESTIONS |Wrestle the Enron dataset into a machine-learning-ready format in preparation for detecting cases of fraud
REGRESSIONS AND OUTLIERS |Use regression algorithms to make predictions and identify and clean outliers from a dataset
UNSUPERVISED LEARNING |Use the k-means clustering algorithm for pattern-searching on unlabeled data
FEATURES, FEATURES, FEATURES |Use feature creation to take your human intuition and change raw features into data a computer can use;Use feature selection to identify the most important features of your data;Implement principal component analysis (PCA) for a more sophisticated take on feature selection;Use tools for parsing information from text-type data
VALIDATION AND EVALUATION |Implement the train-test split and cross-validation to validate and understand machine learning results;Quantify machine learning results using precision, recall, and F1 score

## Software and Libraries
- python2.7
- sklearn
- numpy
- pandas

## References
- [Enron Scandal](https://en.wikipedia.org/wiki/Enron_scandal)
- [Enron Corpus](https://en.wikipedia.org/wiki/Enron_Corpus)
- [Report on Enron Scandal](http://www.nytimes.com/2006/05/25/business/25cnd-enron.html)
- [Why is feature scaling useful?](http://stackoverflow.com/questions/26225344/why-feature-scaling)

  
### 1.Project Overview and Preliminary Data Exploration 
>*Summarize for us the goal of this project and how machine learning is useful in trying to accomplish it. As part of your answer, give some background on the dataset and how it can be used to answer the project question. Were there any outliers in the data when you got it, and how did you handle those?*  

#### 1.1 Goal of Project
[Enron Scandal](https://en.wikipedia.org/wiki/Enron_scandal), revealed in 2001, is one of the most infamous bankrupcy scandal in human history. Some scholars believe it is the signal of forthcoming economic crisis, as it heavily damaged the confidence of common people in stock and capital market. This event leads to the collapse of Anderson, the bigggest accountancy back then, and pushes the release of a series of profound laws and policies in related field.  
It involves huge amount of capital and personnel, especially managing class of Enron, who earned astronomical number and greedy for even more. Now we know their crime is not made by pulse, rather they did it systematically for years. There must be  some clues we can use for detective tracking. Our goal is using economic and email features offerred in the dataset,try to draw a skech of criminals. Or more clear, build a binary classifier with supervised(labels) machine learning to differentiate criminal candidates from the innocent (POI and non-POI). 

#### 1.2 Role of Machine Learning
Unlike human beings, Machine Learning can combine huge amount of features and make sense of them by modeling. It's especially useful when the relationship between things is complicated and intangling. By clearly identifying the question and carefully deal with features, we are able to get closer and closer to truth.  



```python
import warnings
warnings.filterwarnings("ignore")

#create an overview of the dataset
#skeleton code from poi_id.py, except that I build a DataFrame to ease exploration
import sys
import pickle
sys.path.append("../tools/")

import pandas as pd
from feature_format import featureFormat, targetFeatureSplit

with open("final_project_dataset.pkl",'r') as data:
    data_dict= pickle.load(data)

#features_list: the name list of all features except 'email_address'(since it can't be computed)   
all_features= data_dict['TOTAL'].keys()
all_features.pop(all_features.index("poi"))
all_features.pop(all_features.index("email_address"))
features_list=["poi",]+all_features

#df: the data frame holding every data point from my_dataset 
#with each data point as a row and each feature (19 features + 1 label) as a column
#notice that in df all NaNs are saved
my_dataset = data_dict
data = featureFormat(my_dataset, features_list,remove_NaN=False, remove_all_zeroes=False, sort_keys = False)
df=pd.DataFrame(data,index=data_dict.keys(),columns=features_list)

df.describe()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>poi</th>
      <th>salary</th>
      <th>to_messages</th>
      <th>deferral_payments</th>
      <th>total_payments</th>
      <th>exercised_stock_options</th>
      <th>bonus</th>
      <th>restricted_stock</th>
      <th>shared_receipt_with_poi</th>
      <th>restricted_stock_deferred</th>
      <th>total_stock_value</th>
      <th>expenses</th>
      <th>loan_advances</th>
      <th>from_messages</th>
      <th>other</th>
      <th>from_this_person_to_poi</th>
      <th>director_fees</th>
      <th>deferred_income</th>
      <th>long_term_incentive</th>
      <th>from_poi_to_this_person</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>146.000000</td>
      <td>9.500000e+01</td>
      <td>86.000000</td>
      <td>3.900000e+01</td>
      <td>1.250000e+02</td>
      <td>1.020000e+02</td>
      <td>8.200000e+01</td>
      <td>1.100000e+02</td>
      <td>86.000000</td>
      <td>1.800000e+01</td>
      <td>1.260000e+02</td>
      <td>9.500000e+01</td>
      <td>4.000000e+00</td>
      <td>86.000000</td>
      <td>9.300000e+01</td>
      <td>86.000000</td>
      <td>1.700000e+01</td>
      <td>4.900000e+01</td>
      <td>6.600000e+01</td>
      <td>86.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>0.123288</td>
      <td>5.621943e+05</td>
      <td>2073.860465</td>
      <td>1.642674e+06</td>
      <td>5.081526e+06</td>
      <td>5.987054e+06</td>
      <td>2.374235e+06</td>
      <td>2.321741e+06</td>
      <td>1176.465116</td>
      <td>1.664106e+05</td>
      <td>6.773957e+06</td>
      <td>1.087289e+05</td>
      <td>4.196250e+07</td>
      <td>608.790698</td>
      <td>9.190650e+05</td>
      <td>41.232558</td>
      <td>1.668049e+05</td>
      <td>-1.140475e+06</td>
      <td>1.470361e+06</td>
      <td>64.895349</td>
    </tr>
    <tr>
      <th>std</th>
      <td>0.329899</td>
      <td>2.716369e+06</td>
      <td>2582.700981</td>
      <td>5.161930e+06</td>
      <td>2.906172e+07</td>
      <td>3.106201e+07</td>
      <td>1.071333e+07</td>
      <td>1.251828e+07</td>
      <td>1178.317641</td>
      <td>4.201494e+06</td>
      <td>3.895777e+07</td>
      <td>5.335348e+05</td>
      <td>4.708321e+07</td>
      <td>1841.033949</td>
      <td>4.589253e+06</td>
      <td>100.073111</td>
      <td>3.198914e+05</td>
      <td>4.025406e+06</td>
      <td>5.942759e+06</td>
      <td>86.979244</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.000000</td>
      <td>4.770000e+02</td>
      <td>57.000000</td>
      <td>-1.025000e+05</td>
      <td>1.480000e+02</td>
      <td>3.285000e+03</td>
      <td>7.000000e+04</td>
      <td>-2.604490e+06</td>
      <td>2.000000</td>
      <td>-7.576788e+06</td>
      <td>-4.409300e+04</td>
      <td>1.480000e+02</td>
      <td>4.000000e+05</td>
      <td>12.000000</td>
      <td>2.000000e+00</td>
      <td>0.000000</td>
      <td>3.285000e+03</td>
      <td>-2.799289e+07</td>
      <td>6.922300e+04</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>0.000000</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>0.000000</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>0.000000</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>max</th>
      <td>1.000000</td>
      <td>2.670423e+07</td>
      <td>15149.000000</td>
      <td>3.208340e+07</td>
      <td>3.098866e+08</td>
      <td>3.117640e+08</td>
      <td>9.734362e+07</td>
      <td>1.303223e+08</td>
      <td>5521.000000</td>
      <td>1.545629e+07</td>
      <td>4.345095e+08</td>
      <td>5.235198e+06</td>
      <td>8.392500e+07</td>
      <td>14368.000000</td>
      <td>4.266759e+07</td>
      <td>609.000000</td>
      <td>1.398517e+06</td>
      <td>-8.330000e+02</td>
      <td>4.852193e+07</td>
      <td>528.000000</td>
    </tr>
  </tbody>
</table>
</div>



#### 1.3 Dataset Background
[Enron Corpus](https://en.wikipedia.org/wiki/Enron_Corpus) is acquired by Federal Energy Regulatory Commission during its investigation towards the company's collapse. This dataset is later made publicly accessible and widely studied by computer scientists. 
For this project we are using the lastest May 7,2015 version of it. Our project designer Katie Malone scraped 6 important email features along with 13 ecomonic features from 146 subjects and ensembled them into a dictionary container with 18 of subjects manually labeled  as 'POI'.   

#### 1.4 How Background Understanding helps
Several big figures are found involved most in the crime, such as Enron ex-Chairman Kenneth L. Lay, ex-CEO Jeffrey K. Skilling and ex-CFO Andrew S. Fastow. I also notice a report that Lou Lung Pai, the ex-head of EES(Enron Energy Services), made 300 million dolloars by selling all his Enron stock right before the collapse. This guy finally got away from trial by a coincident divorce. Besides, Kenneth D. Rice, Greg Whalley, Rebecca Mark, Ben F. Glisan Jr., Mark E. Koenig are also accused of misconduct. 


```python

df.poi[df.poi==1]
```




    HANNON KEVIN P          1.0
    COLWELL WESLEY          1.0
    RIEKER PAULA H          1.0
    KOPPER MICHAEL J        1.0
    SHELBY REX              1.0
    DELAINEY DAVID W        1.0
    LAY KENNETH L           1.0
    BOWEN JR RAYMOND M      1.0
    BELDEN TIMOTHY N        1.0
    FASTOW ANDREW S         1.0
    CALGER CHRISTOPHER F    1.0
    RICE KENNETH D          1.0
    SKILLING JEFFREY K      1.0
    YEAGER F SCOTT          1.0
    HIRKO JOSEPH            1.0
    KOENIG MARK E           1.0
    CAUSEY RICHARD A        1.0
    GLISAN JR BEN F         1.0
    Name: poi, dtype: float64



Proofreadinging familiar names one by one, I noticed Greg Whalley, Rebecca Mark, and Lou Lung Pai aren't shown here. Dig deeper,  I found Greg and Rebecca somehow are simply not included in this dataset. While 'LOU PAI L' is labeled as non-POI:


```python
df.ix['PAI LOU L']
```




    poi                                 0.0
    salary                         261879.0
    to_messages                         NaN
    deferral_payments                   NaN
    total_payments                3123383.0
    exercised_stock_options      15364167.0
    bonus                         1000000.0
    restricted_stock              8453763.0
    shared_receipt_with_poi             NaN
    restricted_stock_deferred           NaN
    total_stock_value            23817930.0
    expenses                        32047.0
    loan_advances                       NaN
    from_messages                       NaN
    other                         1829457.0
    from_this_person_to_poi             NaN
    director_fees                       NaN
    deferred_income                     NaN
    long_term_incentive                 NaN
    from_poi_to_this_person             NaN
    Name: PAI LOU L, dtype: float64



But this guy is surely not innocent! Maybe Katie simply missed this guy out in manual labeling, or she labeled only persons with conviction. But labeling Lou Lung Pai as non-POI is very misleading since this guy is in fact a accomplice.  **So I change his 'poi' value as 1. Considering the very imbalanced classes (18 poi vs 128 non-poi), the correction is very helpful. Now poi versus non-poi is 19:127. **


```python
df.ix['PAI LOU L','poi']=1;df.ix['PAI LOU L','poi']
```




    1.0



#### 1.5 Outliers


```python
sorted(df.index)
```




    ['ALLEN PHILLIP K',
     'BADUM JAMES P',
     'BANNANTINE JAMES M',
     'BAXTER JOHN C',
     'BAY FRANKLIN R',
     'BAZELIDES PHILIP J',
     'BECK SALLY W',
     'BELDEN TIMOTHY N',
     'BELFER ROBERT',
     'BERBERIAN DAVID',
     'BERGSIEKER RICHARD P',
     'BHATNAGAR SANJAY',
     'BIBI PHILIPPE A',
     'BLACHMAN JEREMY M',
     'BLAKE JR. NORMAN P',
     'BOWEN JR RAYMOND M',
     'BROWN MICHAEL',
     'BUCHANAN HAROLD G',
     'BUTTS ROBERT H',
     'BUY RICHARD B',
     'CALGER CHRISTOPHER F',
     'CARTER REBECCA C',
     'CAUSEY RICHARD A',
     'CHAN RONNIE',
     'CHRISTODOULOU DIOMEDES',
     'CLINE KENNETH W',
     'COLWELL WESLEY',
     'CORDES WILLIAM R',
     'COX DAVID',
     'CUMBERLAND MICHAEL S',
     'DEFFNER JOSEPH M',
     'DELAINEY DAVID W',
     'DERRICK JR. JAMES V',
     'DETMERING TIMOTHY J',
     'DIETRICH JANET R',
     'DIMICHELE RICHARD G',
     'DODSON KEITH',
     'DONAHUE JR JEFFREY M',
     'DUNCAN JOHN H',
     'DURAN WILLIAM D',
     'ECHOLS JOHN B',
     'ELLIOTT STEVEN',
     'FALLON JAMES B',
     'FASTOW ANDREW S',
     'FITZGERALD JAY L',
     'FOWLER PEGGY',
     'FOY JOE',
     'FREVERT MARK A',
     'FUGH JOHN L',
     'GAHN ROBERT S',
     'GARLAND C KEVIN',
     'GATHMANN WILLIAM D',
     'GIBBS DANA R',
     'GILLIS JOHN',
     'GLISAN JR BEN F',
     'GOLD JOSEPH',
     'GRAMM WENDY L',
     'GRAY RODNEY',
     'HAEDICKE MARK E',
     'HANNON KEVIN P',
     'HAUG DAVID L',
     'HAYES ROBERT E',
     'HAYSLETT RODERICK J',
     'HERMANN ROBERT J',
     'HICKERSON GARY J',
     'HIRKO JOSEPH',
     'HORTON STANLEY C',
     'HUGHES JAMES A',
     'HUMPHREY GENE E',
     'IZZO LAWRENCE L',
     'JACKSON CHARLENE R',
     'JAEDICKE ROBERT',
     'KAMINSKI WINCENTY J',
     'KEAN STEVEN J',
     'KISHKILL JOSEPH G',
     'KITCHEN LOUISE',
     'KOENIG MARK E',
     'KOPPER MICHAEL J',
     'LAVORATO JOHN J',
     'LAY KENNETH L',
     'LEFF DANIEL P',
     'LEMAISTRE CHARLES',
     'LEWIS RICHARD',
     'LINDHOLM TOD A',
     'LOCKHART EUGENE E',
     'LOWRY CHARLES P',
     'MARTIN AMANDA K',
     'MCCARTY DANNY J',
     'MCCLELLAN GEORGE',
     'MCCONNELL MICHAEL S',
     'MCDONALD REBECCA',
     'MCMAHON JEFFREY',
     'MENDELSOHN JOHN',
     'METTS MARK',
     'MEYER JEROME J',
     'MEYER ROCKFORD G',
     'MORAN MICHAEL P',
     'MORDAUNT KRISTINA M',
     'MULLER MARK S',
     'MURRAY JULIA H',
     'NOLES JAMES L',
     'OLSON CINDY K',
     'OVERDYKE JR JERE C',
     'PAI LOU L',
     'PEREIRA PAULO V. FERRAZ',
     'PICKERING MARK R',
     'PIPER GREGORY F',
     'PIRO JIM',
     'POWERS WILLIAM',
     'PRENTICE JAMES',
     'REDMOND BRIAN L',
     'REYNOLDS LAWRENCE',
     'RICE KENNETH D',
     'RIEKER PAULA H',
     'SAVAGE FRANK',
     'SCRIMSHAW MATTHEW',
     'SHANKMAN JEFFREY A',
     'SHAPIRO RICHARD S',
     'SHARP VICTORIA T',
     'SHELBY REX',
     'SHERRICK JEFFREY B',
     'SHERRIFF JOHN R',
     'SKILLING JEFFREY K',
     'STABLER FRANK',
     'SULLIVAN-SHAKLOVITZ COLLEEN',
     'SUNDE MARTIN',
     'TAYLOR MITCHELL S',
     'THE TRAVEL AGENCY IN THE PARK',
     'THORN TERENCE H',
     'TILNEY ELIZABETH A',
     'TOTAL',
     'UMANOFF ADAM S',
     'URQUHART JOHN A',
     'WAKEHAM JOHN',
     'WALLS JR ROBERT H',
     'WALTERS GARETH W',
     'WASAFF GEORGE',
     'WESTFAHL RICHARD K',
     'WHALEY DAVID A',
     'WHALLEY LAWRENCE G',
     'WHITE JR THOMAS E',
     'WINOKUR JR. HERBERT S',
     'WODRASKA JOHN',
     'WROBEL BRUCE',
     'YEAGER F SCOTT',
     'YEAP SOON']



Firstly I inspect the row names about any suspicious. I soon find suspicious names such as 'TOTAL','THE TRAVEL AGENCY IN THE PARK', and 'YEAP SOON', which for me doesn't sounds like normal Western names. So I display them and find 'TOTAL' is invalid as it has extremely large value comparing with medians (from df.describe() above), this might lead from entry error. 'THE TRAVEL AGENCY IN THE PARK' is surely not a valid emloyee name. 'YEAP SOON' ,although unusual, is actually valid name.  So I removed the outliers:


```python
#Remove outliers
#now poi versus non-poi is 19:125
data_dict.pop('TOTAL')
data_dict.pop('THE TRAVEL AGENCY IN THE PARK')
df.drop(['TOTAL','THE TRAVEL AGENCY IN THE PARK'],inplace=True)

```

### 2. Feature Scaling and Selection  

>*What features did you end up using in your POI identifier, and what selection process did you use to pick them? Did you have to do any scaling? Why or why not? As part of the assignment, you should attempt to engineer your own feature that does not come ready-made in the dataset -- explain what feature you tried to make, and the rationale behind it. (You do not necessarily have to use it in the final analysis, only engineer and test it.) In your feature selection step, if you used an algorithm like a decision tree, please also give the feature importances of the features that you use, and if you used an automated feature selection function like SelectKBest, please report the feature scores and reasons for your choice of parameter values.*


#### 2.1 New features engineered
>**Concern about sign** 

I find all the valid deferred_income and restricted_stock_deferred values is negative, it seems Katie treat them as the owner's liability instead of wealth. I think it makes sense for deferred income ('deferred' items baiscally describes trades based on credence, in which services/goods is not delivered at the same time of payment.) However it might be inappropriate for restricted_stock_deferred. But since sign won't affect our analysis, I decide to leave them just as they are.


**Finding one: ambition** 

I searched for difference between POI and non-POI by comparing the medians (avoid impact from extreme values) of features. It turns out POIs favor high risks and high profitable approaches in managng money, such as loan_advances,bonus, total_stock_value and long_term_incentive. While both group have comparable salaries and expenses.  

**Finding two: poi_network**  

Another interesting finding is that POIs group scores higher in all email related features no matter it's from or to message. It is  especially marked when this feature is poi related ('from_poi_to_this_person','from_this_person_to_poi','shared_receipt_with_poi')



```python
df.groupby('poi').median()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>salary</th>
      <th>to_messages</th>
      <th>deferral_payments</th>
      <th>total_payments</th>
      <th>exercised_stock_options</th>
      <th>bonus</th>
      <th>restricted_stock</th>
      <th>shared_receipt_with_poi</th>
      <th>restricted_stock_deferred</th>
      <th>total_stock_value</th>
      <th>expenses</th>
      <th>loan_advances</th>
      <th>from_messages</th>
      <th>other</th>
      <th>from_this_person_to_poi</th>
      <th>director_fees</th>
      <th>deferred_income</th>
      <th>long_term_incentive</th>
      <th>from_poi_to_this_person</th>
    </tr>
    <tr>
      <th>poi</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0.0</th>
      <td>250877.0</td>
      <td>944.0</td>
      <td>260455.0</td>
      <td>1056092.5</td>
      <td>985293.0</td>
      <td>700000.0</td>
      <td>409554.0</td>
      <td>594.0</td>
      <td>-140264.0</td>
      <td>1022417.0</td>
      <td>46145.0</td>
      <td>1200000.0</td>
      <td>41.0</td>
      <td>10221.5</td>
      <td>6.0</td>
      <td>106164.5</td>
      <td>-121284.0</td>
      <td>375304.0</td>
      <td>26.5</td>
    </tr>
    <tr>
      <th>1.0</th>
      <td>276788.0</td>
      <td>1875.0</td>
      <td>202911.0</td>
      <td>1868758.0</td>
      <td>5538001.0</td>
      <td>1250000.0</td>
      <td>1116675.0</td>
      <td>1589.0</td>
      <td>NaN</td>
      <td>2493616.0</td>
      <td>46950.0</td>
      <td>81525000.0</td>
      <td>44.5</td>
      <td>150458.0</td>
      <td>15.5</td>
      <td>NaN</td>
      <td>-262500.0</td>
      <td>1134637.0</td>
      <td>62.0</td>
    </tr>
  </tbody>
</table>
</div>



**Concern about overfitting**
Considering the small size of dataset (144 effective points only), I think only a small number of features should be finally used to avoid overfitting (as small dataset with lots of features is very vulnerable to overfiting). I decide to reduce features number while save most possible infomation. PCA is a handy tool for that. And in last section I noticed lots of NaN in some fields. Intuitively I think features suffering from big chunk of data loss should be good candidates for merging.


```python
 df.isnull().sum().sort_values()
```




    poi                            0
    total_stock_value             19
    total_payments                21
    restricted_stock              35
    exercised_stock_options       43
    salary                        50
    expenses                      50
    other                         53
    from_this_person_to_poi       58
    from_messages                 58
    from_poi_to_this_person       58
    shared_receipt_with_poi       58
    to_messages                   58
    bonus                         63
    long_term_incentive           79
    deferred_income               96
    deferral_payments            106
    restricted_stock_deferred    127
    director_fees                128
    loan_advances                141
    dtype: int64



**Engineered Feature One : Ambition**  
Bonus, loan_advances and long_term_incentive are chosen to engineer Ambition. I didn't perform scaling since the units and values of three features are comparable. The old features lack infomation individually. While 'ambition' extract 97% of the total infomation. Hopefully the new feature will give us surprise.


```python
#nnz_df: a dataframe similar with df except it is without empty values
nnz_df=df.fillna(0)

# 'ambition' : created from 3 original economic features
bonus_loan_incentive=nnz_df[['bonus','long_term_incentive','loan_advances']]
from sklearn.decomposition import PCA
pca=PCA(n_components=1)
nnz_df['ambition']=pca.fit_transform(bonus_loan_incentive.values,nnz_df.poi.values)
pca.explained_variance_ratio_
```




    array([ 0.96631851])



**Engineered Feature two and three:  to_poi_fraction,  from_poi_fraction**  
to_poi_fraction = from_this_person_to_poi / from_messages   
from_poi_fraction = from_poi_to_this_person / to_messages    
The new variable is more informative in telling about how POIs  weighes in this individual's network. I think they should be more powerful than the previous variables.


```python
#create new email feature 'to_poi_fraction'
#'to_poi_fraction'='from_this_person_to_poi'/'from_messages'
poi_toall=nnz_df[['from_this_person_to_poi','from_messages']] 
nnz_df['to_poi_fraction']=0
for idx,row in zip(poi_toall.index,poi_toall.values):
    if row[0]!=0 and row[1]!=0:
        nnz_df.ix[idx,'to_poi_fraction']=row[0]/row[1]*100
        
#create new email feature 'from_poi_fraction'
#'from_poi_fraction'='from_poi_to_this_person'/'to_messages'
poi_fromall=nnz_df[['from_poi_to_this_person','to_messages']] 
nnz_df['from_poi_fraction']=0
for idx,row in zip(poi_fromall.index,poi_fromall.values):
    if row[0]!=0 and row[1]!=0:
        nnz_df.ix[idx,'from_poi_fraction']=row[0]/row[1]*100
                   
```

#### 2.2 Features Used
After trying twenty like kinds of different conditions, I found all the three engineered features are very **powerful under some circumstances**.  Their predictive power  depends a lot on what kind of feature scaling (log10 transformation, normalization or both) is done and what features are chosen for scaling before selection. Nonetheless the scores of Ambition and from_poi_fraction are always among the best 10,  **and to_poi_fraction is even more powerful than the two** (Once log10 transformation and normalization are applied, to_poi_fraction always appear as top3 out of the 22. In contrast it scored very low if preprocessing not conducted. )   
**The final features_list has only 4 features, including one engineered feature, to_poi_fraction.**  The rest are others, expenses and bonus respectively.
  

#### 2.3 Feature Scaling 
**log10 transformation and normalization**  

I have 22 features(19 original + 3 engineered), and one label ('POI'). Since distribution of some of features is so skewed while many algorithems (such as RBF kernel of support vector machines) assume the features are normally distributed and all features have variance in the same order, I plan to first conduct feature scaling  before feature selection. 
To avoid repeatitive work I decide to write pipeline functions and observe how my models respond.   


```python
import numpy as np
from sklearn.preprocessing import normalize
from math import log10
from sklearn.feature_selection import SelectKBest

def preprocess(k,translist,escape=[],lg=True):
    #return normalized and log transformed values of input columns
    def norm_log10_scaling(flist):
        temp=nnz_df[flist].copy()
        temp=abs(temp+1)
        if lg:
            for cln in flist:
                temp[cln]=temp[cln].apply(log10)
        temp=normalize(temp.values,axis=0)
        temp=pd.DataFrame(temp,columns=flist,index=nnz_df.index)
        return temp
    
    #input a feature dataframe, return a dataframe with selected features
    def kbest(df,k):
        slb=SelectKBest(k=k)
    
        #get values of the best k features
        best_features=slb.fit_transform(df.values,nnz_df.poi.values)
    
        #get names of the best k features
        scores=zip(df.columns,slb.scores_)
        top_scored=sorted(scores,key=lambda tup: tup[1],reverse=True)[:k]    
        best_names=[]    
        for feature in df.columns:
            if feature in [x for (x,y) in top_scored]:
                best_names.append(feature)    
        best=pd.DataFrame(best_features,columns=best_names,index=nnz_df.index) 
        return best,top_scored

    #log transform feature except those in escape list
    df=nnz_df[features_list].copy()
    flist=[x for x in features_list if x not in escape]
    if flist:
        transformed=norm_log10_scaling(flist)    
        escaped=df[escape].copy()
        df=pd.DataFrame(np.concatenate((transformed,escaped),axis=1),index=nnz_df.index,columns=transformed.columns+escaped.columns)

    return kbest(df,k=k)
    
```

#### 2.4 Feature Selection

**SelectKBest**  

For feature selection I used SelectKBest ( in the kbest functionality). To observe the response of the 7 chosen models I change the input features from very small numbers,3 (i.e., very strict feature filtering), to 5,10,15,and untile 22 (i.e., less strict filtering to no filtering ), I see first a gradual increase in overall performance of 7 models and then decrease, with the peak appearing at somewhere middle depends on feature scaling conditions.


```python
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.metrics import precision_recall_fscore_support,accuracy_score
from collections import defaultdict
from sklearn.grid_search import GridSearchCV

#to preprocess features accordinly, separate eco_features with email_features
#create name list for both classes
eco_features_list=[ u'salary', u'deferral_payments',\
       u'total_payments', u'exercised_stock_options', u'bonus',\
       u'restricted_stock', u'restricted_stock_deferred', u'total_stock_value', u'expenses',\
       u'loan_advances',  u'other',u'director_fees', u'deferred_income',u'long_term_incentive',u'ambition']

email_features_list=[u'to_messages',u'shared_receipt_with_poi',u'from_messages',u'from_this_person_to_poi',\
                     u'from_poi_to_this_person',u'to_poi_fraction', u'from_poi_fraction']

features_list=eco_features_list+email_features_list
labels=nnz_df.poi.values

log_diary=defaultdict(lambda:{})

def models_comparison(k,translist=features_list,escape=[],lg=True,n_iter=100,scoring='recall',aver='micro'):
    #log transform and normalize all features except those in escape 
    best,top_scored=preprocess(k=k,translist=translist,escape=escape,lg=lg)
    print '========Top {} features and their scores:'.format(k)
    for feature,score in top_scored:
        print '%-30s %s'%(feature,score)
    print    
    features=best.values
    
    def clf_score(clf,n_iter=n_iter,log=""):
        cv = StratifiedShuffleSplit(labels, n_iter=n_iter, random_state = 42)           
        results={'precision':[],'recall':[],'fscore':[],'accuracy':[]}
        for traincv, testcv in cv:
                clf.fit(features[traincv], labels[traincv])
                pred=clf.predict(features[testcv])
                prfs=precision_recall_fscore_support(labels[testcv],pred,average=aver)
                results['precision'].append(prfs[0])
                results['recall'].append(prfs[1])
                results['fscore'].append(prfs[2])
                results['accuracy'].append(accuracy_score(labels[testcv],pred))
                
        for k,v in results.iteritems():
            average=sum(v)/float(len(v))
            results[k]=average
    
        if log:
            log_diary[log]=results                                       
        return results

            
    def clf_best_params(clf,parameters,scoring=scoring):
        gd=GridSearchCV(clf,parameters,scoring=scoring)
        gd.fit(features,labels)
        return gd    
    
    from sklearn.naive_bayes import GaussianNB
    nb=GaussianNB()
    clf_score(nb,log='GaussianNB')

    from sklearn.svm import SVC
    sv=SVC(kernel='rbf',C=1,random_state=42)
    parameters={'C':[1,10,1000,100000]}
    sv=clf_best_params(sv,parameters)
    clf_score(sv,log='rbf_SVC')

    from sklearn.linear_model import LogisticRegression 
    clf=LogisticRegression(random_state=42)
    clf_score(clf,log='LogitRegression')

    from sklearn import tree
    clf=tree.DecisionTreeClassifier(random_state=42)
    clf=clf_best_params(clf,parameters={'min_samples_split':[5,10,20,40]})
    clf_score(clf,log='DecisionTree')

    from sklearn.ensemble import RandomForestClassifier
    rfc=RandomForestClassifier(random_state=42)
    parameters={'n_estimators':[1,2,5,10],'min_samples_split':[5,10,20]}
    rfc=clf_best_params(rfc,parameters)
    clf_score(rfc,log='RandomForest')
    
    from sklearn.ensemble import AdaBoostClassifier
    adc=AdaBoostClassifier(random_state=42)
    parameters={'n_estimators':[1,2,5,10]}
    adc=clf_best_params(adc,parameters)
    clf_score(adc,log='AdaBoost')

    from sklearn.neighbors import KNeighborsClassifier
    knn=KNeighborsClassifier()
    parameters={'n_neighbors':[1,2,5,10]}
    knn=clf_best_params(knn,parameters)
    clf_score(knn,log="KNeighbors")
    
    with open('my_classifier.pkl', "w") as clf_outfile:
        pickle.dump(nb, clf_outfile)

    log_sheet=pd.DataFrame.from_dict(log_diary,orient='index')
    return log_sheet

```

**economic features and email features**  
>Numbers of economic features are generally very big (1e5~1e7), while email numbers are mostly less than one thousand. Besides when I check the histogram distribution of them individually, I found all original economic features are at first right skewed, and a simple log10 scaling can drag them back to a symetric shape. (Except 'ambition', the 'unatural' economic feature.) However email features are distributed very very sparsely and extremely skewed, one log10 transformation can't work as effectively as economic features. My first thought is economic and email features are supposed to be treated differently, but the results turn to be different.



```python
#Comparing with all features being treated equally, 
#only email features escape from transformation,
#or only economic features escape from transformation,
# gives no better feature scoring report or performace report.
print "\nWhen escape=features_list"
print models_comparison(22,escape=features_list)
print "\nWhen escape=None"
print models_comparison(22)
print "\nWhen escape=email_features_list"
print models_comparison(22,escape=email_features_list)
print "\nWhen escape=eco_features_list"
print models_comparison(22,escape=eco_features_list)

```

    
    When escape=features_list
    ========Top 22 features and their scores:
    total_stock_value              34.9075976019
    exercised_stock_options        33.2879034061
    bonus                          20.6883364652
    salary                         18.6050424233
    restricted_stock               16.2334432323
    to_poi_fraction                14.4941026933
    deferred_income                10.4590114322
    long_term_incentive            8.78693453741
    total_payments                 8.6034931369
    shared_receipt_with_poi        7.35815751949
    ambition                       7.08376246925
    loan_advances                  6.78241410792
    expenses                       5.848549417
    other                          5.57983168439
    from_poi_to_this_person        4.50604520117
    from_poi_fraction              2.53715167747
    director_fees                  2.24467820956
    from_this_person_to_poi        2.08554158894
    to_messages                    1.28922024446
    deferral_payments              0.278481478789
    from_messages                  0.209348310101
    restricted_stock_deferred      0.0691453328512
    
                     recall  precision    fscore  accuracy
    AdaBoost          0.305   0.404833  0.327381  0.864000
    DecisionTree      0.405   0.345667  0.352881  0.835333
    GaussianNB        0.845   0.149287  0.252830  0.340000
    KNeighbors        0.355   0.386667  0.350333  0.848000
    LogitRegression   0.280   0.308167  0.278048  0.831333
    RandomForest      0.220   0.217595  0.205746  0.826000
    rbf_SVC           0.000   0.000000  0.000000  0.866667
    
    When escape=None
    ========Top 22 features and their scores:
    other                          19.6575366659
    to_poi_fraction                16.6636560959
    expenses                       14.9631978528
    bonus                          12.9509369506
    salary                         10.3048634375
    from_poi_to_this_person        8.35166246726
    from_this_person_to_poi        8.089761319
    total_stock_value              7.45637342328
    total_payments                 7.31584157833
    restricted_stock               7.16702125727
    deferred_income                6.79178398167
    from_poi_fraction              6.16052678785
    shared_receipt_with_poi        4.91404733638
    long_term_incentive            3.76155201143
    to_messages                    3.07016516401
    restricted_stock_deferred      2.90095588193
    director_fees                  2.72707461177
    loan_advances                  1.86899960774
    from_messages                  0.908476428726
    exercised_stock_options        0.304584036906
    ambition                       0.136286353093
    deferral_payments              0.0374545946982
    
                     recall  precision    fscore  accuracy
    AdaBoost          0.315   0.391500  0.326714  0.863333
    DecisionTree      0.420   0.363333  0.369952  0.841333
    GaussianNB        0.890   0.264493  0.402366  0.636667
    KNeighbors        0.440   0.395000  0.387524  0.837333
    LogitRegression   0.000   0.000000  0.000000  0.866667
    RandomForest      0.225   0.238786  0.213857  0.824667
    rbf_SVC           0.385   0.356833  0.347190  0.844000
    
    When escape=email_features_list
    ========Top 22 features and their scores:
    from_this_person_to_poi        19.6575366659
    from_poi_fraction              14.9631978528
    total_payments                 14.4941026933
    director_fees                  12.9509369506
    ambition                       10.3048634375
    from_messages                  7.45637342328
    salary                         7.35815751949
    deferral_payments              7.31584157833
    exercised_stock_options        7.16702125727
    long_term_incentive            6.79178398167
    to_poi_fraction                4.50604520117
    other                          3.76155201143
    expenses                       2.90095588193
    loan_advances                  2.72707461177
    total_stock_value              2.53715167747
    to_messages                    2.08554158894
    from_poi_to_this_person        1.86899960774
    restricted_stock_deferred      1.28922024446
    deferred_income                0.304584036906
    shared_receipt_with_poi        0.209348310101
    restricted_stock               0.136286353093
    bonus                          0.0374545946982
    
                     recall  precision    fscore  accuracy
    AdaBoost          0.315   0.391500  0.326714  0.863333
    DecisionTree      0.420   0.363333  0.369952  0.841333
    GaussianNB        0.825   0.246572  0.374724  0.632000
    KNeighbors        0.310   0.289167  0.279619  0.818000
    LogitRegression   0.110   0.138333  0.117667  0.842667
    RandomForest      0.225   0.238786  0.213857  0.826667
    rbf_SVC           0.085   0.024757  0.035261  0.810000
    
    When escape=eco_features_list
    ========Top 22 features and their scores:
    restricted_stock               34.9075976019
    from_this_person_to_poi        33.2879034061
    loan_advances                  20.6883364652
    from_messages                  18.6050424233
    exercised_stock_options        16.6636560959
    long_term_incentive            16.2334432323
    to_poi_fraction                10.4590114322
    total_payments                 8.78693453741
    from_poi_to_this_person        8.6034931369
    director_fees                  8.35166246726
    deferred_income                8.089761319
    total_stock_value              7.08376246925
    salary                         6.78241410792
    expenses                       6.16052678785
    restricted_stock_deferred      5.848549417
    shared_receipt_with_poi        5.57983168439
    bonus                          4.91404733638
    ambition                       3.07016516401
    to_messages                    2.24467820956
    deferral_payments              0.908476428726
    from_poi_fraction              0.278481478789
    other                          0.0691453328512
    
                     recall  precision    fscore  accuracy
    AdaBoost          0.305   0.404833  0.327381  0.864000
    DecisionTree      0.400   0.358167  0.355048  0.842667
    GaussianNB        0.900   0.156591  0.265840  0.335333
    KNeighbors        0.355   0.386667  0.350333  0.848000
    LogitRegression   0.290   0.386167  0.313524  0.855333
    RandomForest      0.275   0.279333  0.261238  0.834000
    rbf_SVC           0.000   0.000000  0.000000  0.866667



```python
#With all features escape from all transfromation,
#more features are selected, the better performance most of models give.
#When all features are selected, the performance get boost most.
#GaussianNB gives the highest Recall.

print "\nWhen  features selected= 22, escape=features_list"
print models_comparison(22,escape=features_list)
print "\nWhen features selected= 20, escape=features_list"
print models_comparison(20,escape=features_list)
print "\nWhen features selected= 10, escape=features_list"
print models_comparison(10,escape=features_list)
```

    
    When  features selected= 22, escape=features_list
    ========Top 22 features and their scores:
    total_stock_value              34.9075976019
    exercised_stock_options        33.2879034061
    bonus                          20.6883364652
    salary                         18.6050424233
    restricted_stock               16.2334432323
    to_poi_fraction                14.4941026933
    deferred_income                10.4590114322
    long_term_incentive            8.78693453741
    total_payments                 8.6034931369
    shared_receipt_with_poi        7.35815751949
    ambition                       7.08376246925
    loan_advances                  6.78241410792
    expenses                       5.848549417
    other                          5.57983168439
    from_poi_to_this_person        4.50604520117
    from_poi_fraction              2.53715167747
    director_fees                  2.24467820956
    from_this_person_to_poi        2.08554158894
    to_messages                    1.28922024446
    deferral_payments              0.278481478789
    from_messages                  0.209348310101
    restricted_stock_deferred      0.0691453328512
    
                     recall  precision    fscore  accuracy
    AdaBoost          0.305   0.404833  0.327381  0.864000
    DecisionTree      0.405   0.345667  0.352881  0.835333
    GaussianNB        0.845   0.149287  0.252830  0.340000
    KNeighbors        0.355   0.386667  0.350333  0.848000
    LogitRegression   0.280   0.308167  0.278048  0.831333
    RandomForest      0.220   0.217595  0.205746  0.826000
    rbf_SVC           0.000   0.000000  0.000000  0.866667
    
    When features selected= 20, escape=features_list
    ========Top 20 features and their scores:
    total_stock_value              34.9075976019
    exercised_stock_options        33.2879034061
    bonus                          20.6883364652
    salary                         18.6050424233
    restricted_stock               16.2334432323
    to_poi_fraction                14.4941026933
    deferred_income                10.4590114322
    long_term_incentive            8.78693453741
    total_payments                 8.6034931369
    shared_receipt_with_poi        7.35815751949
    ambition                       7.08376246925
    loan_advances                  6.78241410792
    expenses                       5.848549417
    other                          5.57983168439
    from_poi_to_this_person        4.50604520117
    from_poi_fraction              2.53715167747
    director_fees                  2.24467820956
    from_this_person_to_poi        2.08554158894
    to_messages                    1.28922024446
    deferral_payments              0.278481478789
    
                     recall  precision    fscore  accuracy
    AdaBoost          0.300   0.394833  0.320714  0.864667
    DecisionTree      0.385   0.362500  0.355333  0.843333
    GaussianNB        0.635   0.252797  0.347299  0.650000
    KNeighbors        0.355   0.386667  0.350333  0.848000
    LogitRegression   0.270   0.326500  0.278381  0.839333
    RandomForest      0.350   0.378833  0.340762  0.850000
    rbf_SVC           0.000   0.000000  0.000000  0.866667
    
    When features selected= 10, escape=features_list
    ========Top 10 features and their scores:
    total_stock_value              34.9075976019
    exercised_stock_options        33.2879034061
    bonus                          20.6883364652
    salary                         18.6050424233
    restricted_stock               16.2334432323
    to_poi_fraction                14.4941026933
    deferred_income                10.4590114322
    long_term_incentive            8.78693453741
    total_payments                 8.6034931369
    shared_receipt_with_poi        7.35815751949
    
                     recall  precision    fscore  accuracy
    AdaBoost          0.250   0.318333  0.266667  0.862000
    DecisionTree      0.435   0.447667  0.412238  0.852667
    GaussianNB        0.395   0.445000  0.397000  0.858667
    KNeighbors        0.300   0.307167  0.283929  0.823333
    LogitRegression   0.245   0.142790  0.168826  0.684000
    RandomForest      0.270   0.286500  0.258048  0.840000
    rbf_SVC           0.000   0.000000  0.000000  0.866667




**GaussianNB: The most alert, sometimes over-alert. Is this good?**  

With no log10 transformation and normalization performed,GaussianNB gives the highest recall score at K=22, which means no feature selection conducted. Althought this model gives recall as high as 0.82, it's bad in its precision(0.15), and gives a worst ever accuracy (0.34). Only 1 of the seven person supected of fraud are actually criminal candidate.  However with the highly biased recall power, it's  extremely useful in preventing crime for a precaution system (just like for a fire alarm, we would rather stand with false alarms instead of the risk of a missed reported accident. In contrast, rbf_svc here is excellent in accuracy--by giving all negative guess, which is safest. But as alarm its just useless.   


```python
#With all features log10 transformed and normalized,
#Rebundant features pose negative effect on the performance. 
#The peak appear when number of selected features equals to 4.

print "\nWhen  features selected= 10, escape=None"
print models_comparison(10)
print "\nWhen  features selected= 5, escape=None"
print models_comparison(5)
print "\nWhen  features selected= 4, escape=None (GaussianNB here gives the most satisfying performance)"
print models_comparison(4)
print "\nWhen  features selected= 3, escape=None"
print models_comparison(3)
```

    
    When  features selected= 10, escape=None
    ========Top 10 features and their scores:
    other                          19.6575366659
    to_poi_fraction                16.6636560959
    expenses                       14.9631978528
    bonus                          12.9509369506
    salary                         10.3048634375
    from_poi_to_this_person        8.35166246726
    from_this_person_to_poi        8.089761319
    total_stock_value              7.45637342328
    total_payments                 7.31584157833
    restricted_stock               7.16702125727
    
                     recall  precision    fscore  accuracy
    AdaBoost          0.295   0.353167  0.303381  0.846667
    DecisionTree      0.365   0.354833  0.335048  0.838667
    GaussianNB        0.885   0.279091  0.418977  0.657333
    KNeighbors        0.375   0.352333  0.342714  0.830000
    LogitRegression   0.000   0.000000  0.000000  0.866667
    RandomForest      0.305   0.333833  0.297429  0.842667
    rbf_SVC           0.325   0.313167  0.302381  0.845333
    
    When  features selected= 5, escape=None
    ========Top 5 features and their scores:
    other                          19.6575366659
    to_poi_fraction                16.6636560959
    expenses                       14.9631978528
    bonus                          12.9509369506
    salary                         10.3048634375
    
                     recall  precision    fscore  accuracy
    AdaBoost          0.290   0.241667  0.251286  0.830000
    DecisionTree      0.285   0.256389  0.250589  0.815333
    GaussianNB        0.885   0.320099  0.463053  0.706667
    KNeighbors        0.425   0.409167  0.390333  0.853333
    LogitRegression   0.000   0.000000  0.000000  0.866667
    RandomForest      0.235   0.241500  0.220000  0.816667
    rbf_SVC           0.205   0.200000  0.192000  0.839333
    
    When  features selected= 4, escape=None (GaussianNB here gives the most satisfying performance)
    ========Top 4 features and their scores:
    other                          19.6575366659
    to_poi_fraction                16.6636560959
    expenses                       14.9631978528
    bonus                          12.9509369506
    
                     recall  precision    fscore  accuracy
    AdaBoost          0.280   0.258667  0.251810  0.837333
    DecisionTree      0.295   0.298357  0.275873  0.832667
    GaussianNB        0.865   0.361810  0.499865  0.751333
    KNeighbors        0.365   0.334167  0.327333  0.840000
    LogitRegression   0.000   0.000000  0.000000  0.866667
    RandomForest      0.285   0.311333  0.277762  0.838000
    rbf_SVC           0.135   0.140833  0.131000  0.842000
    
    When  features selected= 3, escape=None
    ========Top 3 features and their scores:
    other                          19.6575366659
    to_poi_fraction                16.6636560959
    expenses                       14.9631978528
    
                     recall  precision    fscore  accuracy
    AdaBoost          0.425   0.411690  0.390206  0.840667
    DecisionTree      0.400   0.389333  0.371571  0.848667
    GaussianNB        0.790   0.372341  0.489501  0.785333
    KNeighbors        0.395   0.366357  0.354516  0.840000
    LogitRegression   0.000   0.000000  0.000000  0.866667
    RandomForest      0.300   0.302833  0.281143  0.847333
    rbf_SVC           0.080   0.079167  0.076667  0.836667


**In final model, selected features number = 4, classifier = GaussianN, feature scaling: all log10 transformated and normalized**   GaussianNB under this condition gives a very satisfying performance, with *recall 0.87  precision 0.36 fscore 0.50 accuracy 0.75*, looks a very nice alarm! And we use only 4 features out of the total 22 here, consistant with our speculation that such small dataset need only a few features to give best performance and avoid overfitting. 



```python
selected_transformed_df,top_scored=preprocess(4,translist=features_list)

#dump the list of features used in final_models
top_features=[]
for feature,score in top_scored:
    top_features.append(feature)
    
with open('my_feature_list.pkl', "w") as featurelist_outfile:
     pickle.dump(['poi']+top_features, featurelist_outfile)

#dump the processed dataset used in final_models
selected_transformed_dataset=defaultdict(lambda:{})

for idx in selected_transformed_df.index:
    selected_transformed_dataset[idx]['poi']=nnz_df.ix[idx,'poi']    
    for cln in selected_transformed_df.columns:
        selected_transformed_dataset[idx][cln]=selected_transformed_df.ix[idx,cln]

with open('my_dataset.pkl','w') as f:
    pickle.dump(dict(selected_transformed_dataset),f)
```


### 3.  What algorithm did you end up using? What other one(s) did you try? How did model performance differ between algorithms?  

I ended up using GaussianNB, the most alert. Besides I have tried Kneighbors, logitregression, decision trees, adaboost, randomforest, and support vector machine as well. I found that **GaussianNB** is always the most alert and most likely gives false alarm. **Logistic Regression and SVC(kernel=rbf)** tends giving non-POI guess to secure high accuracy when it's not confident in choosing which side; adaboost,random forest,decision tree and kneighbors algorithms give consistently dependable scores. 



### 4. What does it mean to tune the parameters of an algorithm, and what can happen if you don’t do this well?  How did you tune the parameters of your particular algorithm?  

Tuning parameters is to choose the most suitable setting up for our model to perform best on specific dataset. If this is not done well the potential of our model won't be exploited and we end up wasting its prediction power for nothing.  I tune the parameters using automated algorithm **GridCV**. 

### 5. What is validation, and what’s a classic mistake you can make if you do it wrong? How did you validate your analysis?  

Validation is to check the consistent performance of our model on the same probelm by testing it on a dataset different but related to our training dataset. It is a must-do to prevent overfitting, a classic mistake if validation is not done properly.  I validate it by **StratifiedShuffleSplit**. I want to take full use of all data points and avoid the random error Because my dataset is very small. StratifiedShuffleSplitsplits our data into training and test in different run and make sure every point is sampled and finally return us an averaged performance.    

### 6. Give at least 2 evaluation metrics and your average performance for each of them.  Explain an interpretation of your metrics that says something human-understandable about your algorithm’s performance.

**GaussianNB (Recall:0.87 Precision:0.36 Fscore:0.50 Accuracy:0.75)**  

Recall: GaussianNB is good at recognizing criminals and making bold identifications. When a POI appears, it can recoginize 87% of them.   
Precision: however it is too alert in POI detecting that it frequently gives false alarms. Only roughly 1 out of the 3 identified POI is actually POI, while the rest of them are in fact innocent.   
Accuracy: the accuracy of GaussianNB is almost always the lowest comparing with others under same situation. But considering its brave attempts of POI detecting, the accuracy is fairly nice. 70% of its overall claims are true.   

with the highly biased recalling power and a fairly good precision, this model is  very useful in preventing crime from bud. 


```python

```
