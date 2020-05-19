from selenium import webdriver
import bs4,openpyxl,xlsxwriter,time
import pandas as pd
driver = webdriver.Chrome('C:\\Users\\faisal.ishaq\\Desktop\\chromedriver.exe')
wrbook = xlsxwriter.Workbook('AmazonVSFKSLA_19May.xlsx')#change the name of the o/p file
wrsheet = wrbook.add_worksheet()
wrsheet.write(0,0,'FK FSN')
wrsheet.write(0,1,'Amazon ID')
wrsheet.write(0,2,'Amazon SLA')
wrsheet.write(0,3,'Amazon Fulfilled')
wrsheet.write(0,4,'Pincode')
data=pd.read_csv('AmazonSLAcsv.csv')#file that you provide
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
            val=sheet.cell(row=i+1,column=3).value
            if i%40==0:
                print(i)
            driver.get('https://www.amazon.in/gp/product/{}?pf_rd_r=Q1RQVRWPK69DNT0PEX3H&pf_rd_p=649eac15-05ce-45c0-86ac-3e413b8ba3d4'.format(val))
            time.sleep(0.5)#toggle for a faster execution
            if sheet.cell(row=i+1,column=4).value!=sheet.cell(row=i,column=4).value:
                time.sleep(2)#toggle for a faster execution
                pin=driver.find_element_by_xpath('/html/body/div[2]/header/div/div[2]/div[1]/div/span/a/div[2]/span[2]')
                pin.click()
                time.sleep(2)#toggle for a faster execution
                cell=driver.find_element_by_id('GLUXZipUpdateInput')
                cell.clear()
                cell.send_keys(sheet.cell(row=i+1,column=4).value)
                btn=driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/div[3]/div[2]/div/div[2]/span/span/input')
                btn.click()
                time.sleep(3)#toggle for a faster execution
            r=driver.page_source
            parse=bs4.BeautifulSoup(r,'lxml')
            elem=parse.find_all('div',attrs={'class':'a-section a-spacing-top-mini'})
            elem3=parse.find_all('div',attrs={'class':'a-section a-spacing-mini'})            
            if elem !=[]:
                wrsheet.write(count,2,"".join(elem[x].getText() for x in range(0,len(elem))))
            elif elem3!=[]:
                wrsheet.write(count,2,"".join(elem3[n].getText() for n in range(0,len(elem3))))
            else:
                wrsheet.write(count,2,'Not Available')
            elem4=parse.find_all('div',attrs={'class':'a-section a-spacing-none','id':'availability'})
            elem2=parse.find_all('div',attrs={'id':'shipsFromSoldBy_feature_div'})
            if elem2 !=[]:
                wrsheet.write(count,3,elem2[0].getText()[:170])
            else:
                wrsheet.write(count,3,'Not Fulfilled')
            wrsheet.write(count,0,sheet.cell(row=i+1,column=1).value)
            wrsheet.write(count,1,val)
            wrsheet.write(count,4,sheet.cell(row=i+1,column=4).value)
            count+=1
    except:
        continue
    else:
        break
    finally:
        print('done')
wrbook.close()
        
