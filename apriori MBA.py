import pandas as pd
from apyori import apriori
import xlsxwriter
data=pd.read_csv('apriori.csv')
wrbook = xlsxwriter.Workbook('Apriori_mba.xlsx')

for x in data['Clusters'].unique():
    wrsheet=wrbook.add_worksheet(name=x)
    data_by_cluster=data[data['Clusters']==x]
    cluster_cols=[]
    for i in data_by_cluster['FSN'].unique():
        cluster_cols.append(i)
    apriori_matrix=pd.DataFrame(columns=cluster_cols,index=data_by_cluster['order_external_id'].unique())
    for o,f in zip(data_by_cluster['order_external_id'],data_by_cluster['FSN']):
        apriori_matrix.loc[o,f]=f
    str_list=[]
    for row_n in range(0,len(apriori_matrix.index)):
        # print(row_n)
        str_list.append([str(apriori_matrix.values[row_n,col_n]) for col_n in range(0,len(apriori_matrix.columns))])
    rules=apriori(str_list,min_support=0.025) 
    output=list(rules)
    max_length=[]
    for val in range(0,len(output)):
        max_length.append(len(output[val][0]))
    max_cols=max(max_length)
    row_count=0
    col_count=0
    for inc in range(0,max_cols):
        wrsheet.write(row_count,inc,'Item Bought {}'.format(inc))
        wrsheet.write(row_count,max_cols+inc,'Additional Item {}'.format(inc))
        wrsheet.write(row_count,2*max_cols,'Support Value')
        wrsheet.write(row_count,2*max_cols+1,'Confidence')
        wrsheet.write(row_count,2*max_cols+2,'Lift')
    row_count+=1   
    nan_test=[]
    for val in range(0,len(output)):
        nan_test=[y for y in output[val][0]]
        if "nan" not in nan_test:
            for items in range(0,len(output[val][2])):
                bought_item=[y for y in output[val][2][items][0]]
                bought_with=[y for y in output[val][2][items][1]]
                for b in range(0,len(bought_item)):
                    wrsheet.write(row_count,col_count,bought_item[b])
                    col_count+=1
                col_count=0
                for m in range(0,len(bought_with)):
                    wrsheet.write(row_count,max_cols+col_count,bought_with[m])
                    col_count+=1
                col_count=0
                wrsheet.write(row_count,2*max_cols,output[val][1])
                wrsheet.write(row_count,2*max_cols+1,output[val][2][items][2])
                wrsheet.write(row_count,2*max_cols+2,output[val][2][items][3])
                row_count+=1                
wrbook.close()
                
                