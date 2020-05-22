from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn.model_selection import RandomizedSearchCV
from random import randint
from sklearn.inspection import partial_dependence
from sklearn.inspection import plot_partial_dependence
df=pd.read_csv('nps_modelling_no_na.csv')
df_overall=df[df.columns[0:len(df.columns)-5]]
df_fsd=df[df['logistic_carrier']=="FSD"]
df_overall_clean=df_overall.dropna()
df_fsd_clean=df_fsd.dropna()


df=df_overall_clean #change the categorical database in df2 hot encode
lenArr=[]
for val in df[df.columns[0]].unique():
    lenArr.append(len(df[df[df.columns[0]]==val].index))
lenArr.sort(reverse=True)

def randlist(a,b,c):
    randList=[]
    while len(randList)<c:
        randNum=randint(a,b)
        if randNum not in randList:
            randList.append(randNum)
        else:
            continue
    return randList
        
df_train=pd.DataFrame(columns=df.columns) 
for val in df[df.columns[0]].unique():
    df_temp=df[df[df.columns[0]]==val]
    if len(df_temp.index)<=lenArr[1]:
        df_train=df_train.append(df_temp)
    else:
        randArr=randlist(0,len(df_temp.index)-1,1.40*lenArr[1])
        df_train=df_train.append(df_temp.iloc[randArr])

df_train.to_csv('normalised.csv',index=False)
df=pd.read_csv('normalised.csv')

df=pd.get_dummies(df,columns=['user_lockin_state',
                           'is_alpha_seller',
                           'analytic_super_category',
                           'Sale Flag',
                           'service_profile',
                           'analytic_category',
                           'logistic_carrier',
                           'prexo_flag',
                           'order_payment_type',
                           'city_tier',
                           'zone',
                           'jeeves_brand_name',
                           'open_box_flag',
                           'breach_3pl_bucket',
                           'returns',
                           'refund_replace_flag',
                           'return_reason',
                           'slot_adherence_flag',
                           'breach_status'
                           ])

df2=pd.get_dummies(df_overall_clean,columns=['user_lockin_state',
                           'is_alpha_seller',
                           'analytic_super_category',
                           'Sale Flag',
                           'service_profile',
                           'analytic_category',
                           'logistic_carrier',
                           'prexo_flag',
                           'order_payment_type',
                           'city_tier',
                           'zone',
                           'jeeves_brand_name',
                           'open_box_flag',
                           'breach_3pl_bucket',
                           'returns',
                           'refund_replace_flag',
                           'return_reason',
                           'slot_adherence_flag',
                           'breach_status'
                           ])

for col in df2.columns:
    if col not in df.columns:
        df2=df2.drop(col,axis=1)

df_target=df[df.columns[0]].to_numpy()
df_features=df[df.columns[1:len(df.columns)]].to_numpy()
X_train,X_test,y_train,y_test=train_test_split(df_features,df_target,random_state=3)

param_grid={
    'n_estimators':[int(x) for x in np.linspace(start=100,stop=500,num=20)],
    'max_features':['auto','sqrt'],
    'max_depth':[int(x) for x in np.linspace(50,100,num=10)],
    'min_samples_split':[int(x) for x in np.linspace(15,20,num=5)],
    'min_samples_leaf':[int(x) for x in np.linspace(5,10,num=5)]
    }

forest=RandomForestClassifier()
iter_run=RandomizedSearchCV(forest,param_grid,10,random_state=4)
iter_run.fit(X_train,y_train)
iter_run.best_estimator_.score(X_test,y_test)

df_acc=pd.DataFrame()
df_acc['actual']=df2[df2.columns[0]].to_numpy()
df_acc['predicted']=iter_run.best_estimator_.predict(df2[df2.columns[1:len(df2.columns)]].to_numpy())

def npsvals(dataset):
    actual={}
    predicted={}
    for i in dataset['actual'].unique():
        actual[i]=len(dataset[dataset['actual']==i])-1
    for i in dataset['predicted'].unique():
        predicted[i]=len(dataset[dataset['predicted']==i])-1
    detractor=0
    promoter=0
    neutral=0
    for key in actual.keys():
        if key>3:
            promoter+=actual[key]
        elif key<3:
            detractor+=actual[key]
        else:
            neutral+=actual[key]
    actualnps=(promoter-detractor)/(promoter+detractor+neutral)
    detractor=0
    promoter=0
    neutral=0
    for key in predicted.keys():
        if key>3:
            promoter+=predicted[key]
        elif key<3:
            detractor+=predicted[key]
        else:
            neutral+=predicted[key]
    predictednps=(promoter-detractor)/(promoter+detractor+neutral)
    return {'actual':actualnps,'predicted':predictednps}   
    
npsvals(df_acc)
        
impArr=[]
for i,j in zip(df.columns[1:],iter_run.best_estimator_.feature_importances_):
    impArr.append((i,j))

def secElement(elem):
    return elem[1]

impArr.sort(key=secElement,reverse=True)

#club categorical feature importance together
newFeatureArr=[]
for v in df_overall_clean.columns:
    total_sum=0
    for m in range(0,len(impArr)):
        if impArr[m][0].find(v)!=-1:
            total_sum+=impArr[m][1]       
    newFeatureArr.append((v,total_sum))

newFeatureArr.sort(key=secElement,reverse=True)

#get the most important parameters
contrib=0
finalFeatureArr=[]
x=0
while contrib<0.95:
    finalFeatureArr.append((newFeatureArr[x][0],newFeatureArr[x][1]))
    contrib+=newFeatureArr[x][1]
    x+=1

print(finalFeatureArr)


#Sensitivity analysis
verticals=[]
for m in range(0,len(df.columns)):
    if df.columns[m].find('analytic_category')!=-1:
        verticals.append(df.columns[m])
#assume current Level of Service
sensitivity=pd.DataFrame()
for v in verticals:
    vert_dat=df2[df2[v]==1][df2.columns[0]].to_numpy()
    promoter=0
    neutral=0
    detractor=0
    for l in range(0,len(vert_dat)):
        if vert_dat[l]>3:
            promoter+=1
        elif vert_dat[l]<3:
            detractor+=1
        else:
            neutral+=1
    vert_nps=(promoter-detractor)/(promoter+detractor+neutral)
    sensitivity=sensitivity.append([[v,vert_nps]])
    x_pdp=df2[df2[v]==1][df2.columns[1:len(df2.columns)]].to_numpy()
    pdp,axes=partial_dependence(iter_run.best_estimator_,x_pdp,[1])
    for i in range(0,len(pdp[0])):
        projected_val=(pdp[3][i]+pdp[4][i]-(pdp[0][i]+pdp[1][i]))/1
        sensitivity=sensitivity.append([[axes[0][i],projected_val]])
        
        