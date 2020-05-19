from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4,openpyxl,xlsxwriter,time
import pandas as pd
driver = webdriver.Chrome('C:\\Users\\faisal.ishaq\\Desktop\\chromedriver.exe')
wrbook = xlsxwriter.Workbook('FK Viewed SLA_19.xlsx')
wrsheet = wrbook.add_worksheet()
wrsheet.write(0,0,'FK FSN')
wrsheet.write(0,1,'FK SLA')
wrsheet.write(0,2,'FK Fulfilled')
wrsheet.write(0,3,'Pincode')
data=pd.read_csv('AmazonSLAcsv.csv')
newdata=pd.DataFrame()
for pin in data['Pincode'].unique():
    temp=data[data['Pincode']==pin]
    newdata=newdata.append(temp)
newdata.to_excel('tempSLA.xlsx',index=False)
wb = openpyxl.load_workbook('tempSLA.xlsx')
sheet=wb.active
ro=sheet.max_row
i=1
count=1
while True:
    try:
        for i in range(i,ro,1):
            val=sheet.cell(row=i+1,column=1).value
            if i%40==0: 
                print(i)
            driver.get('https://www.flipkart.com/butterfly-rapid-wet-grinder/p/itme4f889da7d01f?pid={}&lid=LSTWMNF8G8YE9MA9ZNNURJ2K0&marketplace=FLIPKART&srno=b_1_1&otracker=nmenu_sub_TVs%20%26%20Appliances_0_Fully%20Automatic%20Front%20Load&fm=organic&iid=8d72fe60-259d-4e25-b733-109209f6dce0.WMNF8G8YE9MA9ZNN.SEARCH&ppt=browse&ppn=browse&ssid=l54hp0gwqo0000001589653154522'.format(val))
            time.sleep(0.5)
            if sheet.cell(row=i+1,column=4).value!=sheet.cell(row=i,column=4).value:
                time.sleep(1)
                pin=driver.find_element_by_id('pincodeInputId')
                for rem in range(0,6,1):
                    pin.send_keys(Keys.BACKSPACE)
                pin.send_keys(sheet.cell(row=i+1,column=4).value)
                pin.send_keys(Keys.ENTER)
                time.sleep(2)
            r=driver.page_source
            parse=bs4.BeautifulSoup(r,'lxml')
            elem=parse.find_all('div',attrs={'class':'_29Zp1s'})
            elem3=parse.find_all('div',attrs={'class':'_3l12t9'}) 
            img=parse.find_all('span',attrs={'class':'_3V7-QV _55FW5e'})
            if elem !=[]:
                wrsheet.write(count,1,"".join(elem[x].getText() for x in range(0,len(elem))))
            elif elem3!=[]:
                wrsheet.write(count,1,"".join(elem3[n].getText() for n in range(0,len(elem3))))
            else:
                wrsheet.write(count,1,'Page not Parsed')
            if img!=[]:
                wrsheet.write(count,2,'F Assured')
            else:
                wrsheet.write(count,2,'Non FBF')
            # elem4=parse.find_all('div',attrs={'class':'a-section a-spacing-none','id':'availability'})
            # elem2=parse.find_all('div',attrs={'id':'shipsFromSoldBy_feature_div'})
            # if elem2 !=[]:
            #     wrsheet.write(count,3,elem2[0].getText()[:170])
            # else:
            #     wrsheet.write(count,3,'Not Fulfilled')
            wrsheet.write(count,0,sheet.cell(row=i+1,column=1).value)
            wrsheet.write(count,3,sheet.cell(row=i+1,column=4).value)
            count+=1
    except:
        continue
    else:
        break
    finally:
        print('done')
wrbook.close()
        
    