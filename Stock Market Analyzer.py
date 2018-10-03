import requests
#import module that sends HTTP/1.1 requests to a url to obtain its content
from bs4 import BeautifulSoup
#import module for pulling data out of HTML and XML files
import csv
#import module to create,read, and edit comma separated csv files
from datetime import datetime
#import module for manipulating current time
from os.path import exists
#import module for checking if a path refers to an existing path
data = []
#create a list named data
print("Welcome to Stock Market Analyzer!")
print("Obtaining stock information", end="")
#print instructions
if exists("index.csv") == True:
    #if file named index.csv execute the following
    with open('index.csv', 'r') as csvfile:
        checkFile = csv.reader(csvfile)
        header = ['Date', 'Name', 'Price', 'Change', 'Previous Close', 'Open', 'Day Price Range', '52 Week Price Range', 'Next Close Price Prediction']
        #open the file in reading mode
        if header not in checkFile:
            #executes the following if the header indicated above isn't found in the file
            clearFile = open('index.csv', "w+")
            clearFile.close()
            # opens the file with w+ mode to truncate the file and then closes it
            with open('index.csv', 'a') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['Date', 'Name', 'Price', 'Change', 'Previous Close', 'Open', 'Day Price Range', '52 Week Price Range', 'Next Close Price Prediction'])
                csv_file.close()
                #opens the file in writing mode and writes the header in one row and then closes the file
else:
    with open('index.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Date', 'Name', 'Price', 'Change', 'Previous Close', 'Open', 'Day Price Range', '52 Week Price Range', 'Next Close Price Prediction'])
        csv_file.close()
        #if the file isn't found in the folder, open/create a file named index.csv and write the header and close it
stockPages = ['https://ca.finance.yahoo.com/quote/%5EGSPTSE?p=^GSPTSE', 'https://ca.finance.yahoo.com/quote/%5EGSPC?p=^GSPC', 'https://ca.finance.yahoo.com/quote/%5EDJI?p=^DJI', 'https://ca.finance.yahoo.com/quote/%5ERUT?p=^RUT', 'https://ca.finance.yahoo.com/quote/%5EIXIC?p=^IXIC', 'https://ca.finance.yahoo.com/quote/%5EFTSE?p=^FTSE', 'https://ca.finance.yahoo.com/quote/CADEUR=X?p=CADEUR=X', 'https://ca.finance.yahoo.com/quote/CADGBP%3DX?p=CADGBP%3DX', 'https://ca.finance.yahoo.com/quote/CADCNY%3DX?p=CADCNY%3DX', 'https://ca.finance.yahoo.com/quote/CADUSD=X?p=CADUSD=X']
#list of all the url's used to retrieve informaiton
for page in stockPages:
    #for each index in the list execute the following:
    if page == stockPages[2]:
        print(".", end="")
    if page == stockPages[5]:
        print(".", end="")
    if page == stockPages[8]:
        print(".", end="")
    #depending on the iteration of the loop, print a '.'
    page = requests.get(page)
    #request the url
    soup = BeautifulSoup(page.content, 'html.parser')
    #create a variable named soup that contains the url parsed into an html
    stockName= soup.find('h1').text.strip()
    #from soup, it looks for a header tag and strips the text in the header
    for i in range(0,len(stockName)):
        if stockName[i:i+2]=="- ":
            stockName = stockName[i+2:len(stockName)]
            break
            #from the text, it finds out the location where the name of the stock starts
            #and only strips out the name of the stock
    stockCurrency = soup.find('div', class_="Fz(12px)").text.strip()
    find = stockCurrency.find('Currency')
    stockName = stockName + " (" + stockCurrency[find:] + ")"
    stockPrice = soup.find('span', class_="Fw(b)").text.strip()
    priceChange = soup.find('span', class_="Fw(500)").text.strip()
    previousClose = soup.findAll('td', class_="Lh(14px)")[0].text.strip()
    previousOpen = soup.findAll('td', class_="Lh(14px)")[1].text.strip()
    dayRange = soup.findAll('td', class_="Lh(14px)")[3].text.strip()
    yearRange = soup.findAll('td', class_="Lh(14px)")[4].text.strip()
    #like it did for the name, it finds the location of the html with a certain tag and class name
    #and strips only the text out of the content
    price = float(stockPrice.replace(',',''))
    closeFloat = float(previousClose.replace(',', ''))
    openFloat = float(previousOpen.replace(',', ''))
    dayPrice = dayRange.replace(',','')
    yearPrice = yearRange.replace(',','')
    #takes out the commas of the variables to change to float
    find = dayPrice.find(' -')
    dayLow = float(dayPrice[:find])
    dayHigh = float(dayPrice[find+3:])
    find = yearPrice.find(' -')
    yearLow = float(yearPrice[:find])
    yearHigh = float(yearPrice[find+3:])
    #separate the varaible containing two numbers
    dayAverage = (dayLow+dayHigh)/2
    yearAverage = (yearLow+yearHigh)/2
    #make average of the 24 hour price range and 52 week price range
    dayYearRangeFrom = dayAverage*0.9 + yearAverage*0.1
    dayYearRangeTo = dayAverage*0.95 + yearAverage*0.05
    #make a range of the prediction price range
    if (abs(dayYearRangeFrom-price)) > (abs(dayYearRangeTo-price)):
        change = (abs(dayYearRangeTo-price))/4
    else:
        change = (abs(dayYearRangeFrom-price))/4
    #checks if the low end or the higher end of the range is closer to the current price
    #and takes an absolute value of the difference of the current price and the closer enda nd takes a quarter of it
    #this quarter of a value becomes the change for the next day's closing price
    if '+' in priceChange:
        predictedClosePrice = price + change
    else:
        predictedClosePrice = price - change
    #depending on if the most recent price change was negative or positive,
    #the predicted price change is added or subtracted to the current price
    #this gives the predicted price change
    data.append((datetime.now(),stockName,stockPrice,priceChange,previousClose,previousOpen,dayRange,yearRange,predictedClosePrice))
    # appends all the variables to the data list in a tuple 
print(" Done!")
#when obtains and calculates all the information, it prints the following
while True:
    #continuous loop until break is used
    print("What would you like to do? (Enter the number corresponding to the choice")
    print("1. Check Date")
    print("2. Check Current Stock Information ")
    print("3. Exit Stock Market Analyzer")
    #prints out instruction
    choice = int(input())
    #takes user input
    if choice == 1:
        print("Right now it is: " + str(datetime.now()))
        continue
        #if user entered '1', prints out the current time and continues the loop
    elif choice ==2:
        #if user entered '2', it executes the following
        while True:
            #continuous loop until break is used
            print("Which stock would you like to view information on? (Enter the number corresponding to the choice and type 0 to go back to the main menu")
            for i in range(0,10):
                print(str((i+1)) + ". " + str(data[i][1]))
                #prints out all the names of the stock to choose from
            whichStock = int(input()) - 1
            #takes user input
            if whichStock == -1:
                break
                #breaks loop with user's input of 0
            elif whichStock <= 9 and whichStock >= 0:
                print("Stock Name: " + data[whichStock][1])
                print("Stock Price: " + data[whichStock][2])
                print("Price Change: " + data[whichStock][3])
                print("Previous Close: " + data[whichStock][4])
                print("Open: " + data[whichStock][5])
                print("Day's Price Range: " + data[whichStock][6])
                print("52 Week Price Range: " + data[whichStock][7])
                print("Predicted next close price: " + str(data[whichStock][8]))
                #prints out the information of the selected stock
                while True:
                    #continuous loop until break is used
                    print("")
                    print("What would you like to do with the stock information? (Enter the number corresponding to the choice)")
                    print("0. Go back to previous menu.")
                    print("1. Save this specific stock information to excel")
                    print("2. Save all 10 stock information to excel")
                    #prints out user instruction
                    useStock = int(input())
                    #takes user input
                    if useStock == 0:
                        break
                        #breaks loop with user's input of 0
                    if useStock == 1:
                        #with user input of 1
                        with open('index.csv', 'a') as csv_file:
                            #opens the csv file in appending mode
                            writer = csv.writer(csv_file)
                            writer.writerow(data[whichStock])
                            csv_file.close()
                            print("Saved!")
                            #appends the information of the specific stock chosen on the next row of the csv file
                    elif useStock == 2:
                        with open('index.csv', 'a') as csv_file:
                            #opens the csv file in appending mode
                            writer = csv.writer(csv_file)
                            for i in range(0,10):
                                writer.writerow(data[i])
                            csv_file.close()
                        print("Saved!")
                        #appends the information of all the stocks on each row of the csv file
                    else:
                        print("Invalid input. Please try again")
                        #if user inputted anything other than the options, instructs user to enter a valid input and repeats the input
            else:
                print("Invalid input. Please try again")
                #if user inputted anything other than the options, instructs user to enter a valid input and repeats the input
    elif choice ==3:
        print("Thank you for using the Stock Market Analyzer! Have a good day!")
        break
        #if user chooses to stop using the program, it terminates the program
    else:
        print("Invalid input. Please try again")
        #if user inputted anything other than the options, instructs user to enter a valid input and repeats the input
