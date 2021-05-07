# Libraries
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
import pandas as pd
import time
import csv

# Functions
def properText(string):
    return ' '.join(list(map(lambda x: x.capitalize(),string.split(' '))))

def checkItemList(list1, list2):
    result = True
    if len(list1) == 0 or list1 == ['']:
        return (result, 0)
    else:    
        for i in list1:
            if i not in list2:
                result = False
                break
    return (result, i)

#########################################
# Parameters and files
gecko_path = '/usr/local/bin/geckodriver'
url = 'https://www.kiva.org/lend?page=1'
countryListFile = 'countries.csv'
sectorListFile = 'sectors.csv'
attributeListFile = 'attributes.csv'
URLDir = 'loanURLs.csv'

#########################################
# User's paremeters input
## Read parameter files
genderDict = {'1': 'Women','2':'Men'}
typeDict = {'1': 'Individual','2':'Group'}
statusDict = {'1': 'fundRaising','2':'funded','': 'all'}
lengthDict = {'1': '8 mths or less','2':'16 mths or less','3': '2 yrs or less','4': '2 yrs or more'}
dfCountryList = pd.read_csv(countryListFile).astype(str)
dfSectorList = pd.read_csv(sectorListFile).astype(str)
dfAttributeList = pd.read_csv(attributeListFile).astype(str)

## 1. Countries
print("Please select ID of countries on the following list. For all countries, please press Enter")
print(dfCountryList.to_string(index=False))
print("Example: 1,2")
time.sleep(1)
selectedCountryIDs = list(input("Loan countries: ").replace(' ','').split(','))
while not checkItemList(selectedCountryIDs,dfCountryList.ID.tolist())[0]:
    print(checkItemList(selectedCountryIDs,dfCountryList.ID.tolist())[1], " is not in the country list to select, please input again")
    selectedCountryIDs = list(input("Loan countries: ").replace(' ','').split(','))
selectedCountryNames = list(dfCountryList[dfCountryList.ID.isin(selectedCountryIDs)].Country)

## 2. Sectors
print("Please select ID of sectors on the following list. For all sectors, please press Enter")
print(dfSectorList.to_string(index=False))
print("Example: 1,2,3")
time.sleep(1)
selectedSectorIDs = list(input("Loan sectors: ").replace(' ','').split(','))
while not checkItemList(selectedSectorIDs,dfSectorList.ID.tolist())[0]:
    print(checkItemList(selectedSectorIDs,dfSectorList.ID.tolist())[1], " is not in the sector list to select, please input again")
    selectedSectorIDs = list(input("Loan Sectors: ").replace(' ','').split(','))
selectedSectorNames = list(dfSectorList[dfSectorList.ID.isin(selectedSectorIDs)].Sector)

## 3. Loan purposes
print("Please select ID of loan purposes on the following list. For all countries, please press Enter")
print(dfAttributeList.to_string(index=False))
print("Example: 1,3,4,5")
time.sleep(1)
selectedAttributeIDs = list(input("Loan Purposes: ").replace(' ','').split(','))
while not checkItemList(selectedAttributeIDs,dfAttributeList.ID.tolist())[0]:
    print(checkItemList(selectedAttributeIDs,dfAttributeList.ID.tolist())[1], " is not in the purpose list to select, please input again")
    selectedAttributeIDs = list(input("Loan Purposes: ").replace(' ','').split(','))
selectedAttributeNames = list(dfAttributeList[dfAttributeList.ID.isin(selectedAttributeIDs)].Attribute)
    
## 4. Borrower Gender
print("\nPlease select ID of borrower's gender. For all genders, please press Enter")
print("1 Women\n2 Men")
genderOption = input("Borrower's gender option:")
while genderOption not in ['1','2','']:
    print(genderOption, 'is not in the list, please select again!')
    genderOption = input("Borrower's gender option:")
    
## 5. Loan type (individual or group)
print("\nPlease select ID of loan type (individual or group). For all loan types, please press Enter")
print("1 Individual\n2 Group")
typeOption = input("Loan type option:")
while typeOption not in ['1','2','']:
    print(typeOption, 'is not in the list, please select again!')
    typeOption = input("Loan type option:")
    
## 6. Keywords input
keyWords = input('Please input keywords to search loans: ')

## 7. Loan status
print("\nPlease select ID of loan status (fundraising or funded). For both statuses, please press Enter")
print("1 Fundraising\n2 Funded")
statusOption = input("Loan status option:")
while statusOption not in ['1','2','']:
    print(statusOption, 'is not in the list, please select again!')
    statusOption = input("Loan status option:")
    
## 8. Loan length
print("\nPlease select ID of loan length. For all loan length values, please press Enter")
print("1 8 months or less\n2 16 months or less\n3 2 years or less\n4 2 years or more")
loanLength = input("Loan length option:")
while loanLength not in ['1','2','3','4','']:
    print(loanLength, 'is not in the list, please select again!')
    loanLength = input("Loan length option:")
print ('\nPlease wait, Scrapping data from Kiva.org ...')

#########################################
# Data scrapping execution
options = webdriver.firefox.options.Options()
options.headless = False
driver = webdriver.Firefox(options = options, executable_path = gecko_path)
driver.get(url)
time.sleep(3)
loanURLs = []

## 1. Accept cookies
acceptButton = driver.find_element_by_xpath("//button[@id = 'onetrust-accept-btn-handler']")
acceptButton.click()
filterButton = driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/div/div[1]/div[2]/div[2]/div[1]/a")
filterButton.click()

## 2. Select Gender Filter
if genderOption in genderDict.keys():
    gender = driver.find_element_by_xpath("//div[@class = 'gender-button-box triple-state-buttons']").\
            find_element_by_xpath(".//*[text() = '{0}']".format(genderDict[genderOption]))
    gender.click()
time.sleep(1)
    
## 3. Select Borrower Type Filter
if typeOption in typeDict.keys():
    type = driver.find_element_by_xpath("//div[@class = 'isGroup-button-box triple-state-buttons']").\
            find_element_by_xpath(".//*[text() = '{0}']".format(typeDict[typeOption]))
    type.click()
time.sleep(1)

## 4. Input search keywords
driver.find_element_by_xpath("//input[@id = 'filter-keywords-search-box']").send_keys(keyWords)
time.sleep(1)

## 5. Select countries
driver.find_element_by_xpath("//a[@data-reveal-id = 'countrySelectModal']").click()
time.sleep(2)
if len(selectedCountryNames) > 0:
    for i in range(len(selectedCountryNames)):
        checkBoxList = [driver.find_element_by_xpath("//div[contains(., '{0}')][@class = 'country filter checkbox-input']".format(countryName)) for countryName in selectedCountryNames]
        time.sleep(4)
        checkBoxList[i].find_element_by_xpath(".//input[@class = 'countryCheckbox']").click()
        time.sleep(4)
driver.find_element_by_id("filter-country-submit").click()
time.sleep(1)

## 6. Select loan sectors
if len(selectedSectorNames) > 0:
    for i in range(len(selectedSectorNames)):
        checkBoxList = [driver.find_element_by_xpath("//li[contains(., '{0}')][@class = 'filter checkbox-input']".format(sectorName)) for sectorName in selectedSectorNames]
        time.sleep(3)
        checkBoxList[i].find_element_by_xpath(".//input[@name = 'filter-sector']").click()
        time.sleep(3)
time.sleep(1)
        
## 7. Select loan purposes
if len(selectedAttributeNames) > 0:
    for i in range(len(selectedAttributeNames)):
        checkBoxList = [driver.find_element_by_xpath("//li[contains(., '{0}')][@class = 'filter checkbox-input']".format(attributeName)) for attributeName in selectedAttributeNames]
        time.sleep(3)
        checkBoxList[i].find_element_by_xpath(".//input[@name = 'filter-theme']").click()
        time.sleep(3)
time.sleep(1)

## 8. Select loan length
if loanLength in lengthDict.keys():
    loanLengthDiv = driver.find_element_by_xpath("//div[@class = 'lenderTerm-button-box quintuple-state-buttons']")
    loanLengthDiv.find_element_by_xpath(".//label[text() = '{0}']".format(lengthDict[loanLength])).click()
time.sleep(1)

## 9. Select loan status
if statusOption in statusDict.keys():
    driver.find_element_by_id('filter-loan-status-dropdown').click()
    time.sleep(1)
    driver.find_element_by_xpath(".//option[@value = '{0}']".format(statusDict[statusOption])).click()
    time.sleep(3)
time.sleep(1)

## 10. Collect loan URLs on pages
pageno = 1
while True:
    try:
        while len(driver.find_elements_by_xpath("//a[@class = 'next button secondary ']")) == 0:
            time.sleep(2)
            if len(driver.find_elements_by_xpath("//div[@class = 'paging hide']")) > 0 or len(driver.find_elements_by_xpath("a[@class='last button secondary ']")) == 0:
                break
        loanURLs += [x.get_attribute('href') for x in driver.find_elements_by_xpath("//a[@class = 'loan-card-2-borrower-name']")]
        print('Page no. {0} completed'.format(pageno))
        pageno += 1
        nextPage = driver.find_element_by_xpath("//a[@class = 'next button secondary ']")   
        nextPage.click()  
        time.sleep(2)
    except Exception as e1:
        print("End of selected pages")
        break
if len(loanURLs) == 0:
    print('No loan found!')
else:
    print('{0} URLs collected'.format(len(loanURLs)))

#########################################
# Save output URLs into a csv file
outputFile = open(URLDir, "w")
for url in loanURLs:
    outputFile.write(url+'\n')
outputFile.close()