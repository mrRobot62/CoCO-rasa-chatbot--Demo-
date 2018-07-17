
from random import randint, uniform, random

CR = '\n'

USE_PRINT_OUT = 1

def MOCK_CreateCoBAAccountID():
    L = [randint(0, 9) for p in range(0, 10)]
    #print (''.join(str(e) for e in L))    
    return "".join(str(e) for e in L)

def MOCK_IBANAccountID():
    account = MOCK_CreateCoBAAccountID()
    return ["DE5330040000" + account, account]

def MOCK_AccountDetails(name, numberOfAccounts, numberOfSavingAccounts):
    titles = ['','Dr.','PhD','Prof', 'God']
    structure = {
                  "Owner": "Peter Pan",
                  "Title": "PhD",
                  "Accounts" : {
                    "Checking_account" : [{
                      "Number": "1234567890" ,
                      "IBAN" : "DE53300400001234567890",
                      "Created" : "10.01.2010",
                      "Balance" : 34566.00,
                      "Debit" : 10000,
                      "Currency" : "Euro"
                      },
                      {
                      "Number": "0987654321" ,
                      "IBAN" : "DE53300400000987654321",
                      "Created" : "03.05.2011",
                      "Balance" : 23053.35,
                      "Debit" : 15000,
                      "Currency" : "Euro"
                      }      
                      ],
                    "Saving_account"   : [{
                      "Number": "9912345678" ,
                      "IBAN" : "DE53300400009912345678",
                      "Created" : "10.01.2010",
                      "Balance" : 15000.00,
                      "Debit" : 0,
                      "Currency" : "Euro"
                    }]},
                  "DayOfBirth": "04.MAR.1973",
                  "CityOfBirth" : "Keras",
                  "Address": "Cloudy Street 26a",
                  "Zip": 12345,
                  "City" : "Heaven",
                  "Phone" : ["004032122453"],
                  "Mobile" : ["004015175075300"]
                }
    structure['Owner'] = name if name else "unknown"
    structure['Title'] = titles[randint(0, 4)]
    #
    # create number of accounts (only checking accounts (Girokonten))
    accounts = []
    
    if numberOfAccounts < 1: 
        numberOfAccounts = 1
    if numberOfAccounts > 10: 
        numberOfAccounts = 10
   
    #
    # create checking accounts
    for x in range (0, numberOfAccounts):
        if USE_PRINT_OUT :
            print ("Checking Account {}".format(x))
        ano = MOCK_IBANAccountID()
        maxDebit = round(randint(1,10),0) * 1000
        s = {
              "Number": ano[1] ,
              "IBAN" : ano[0],
              "Created" : "10.01.2010",
              "Balance" : round(uniform((maxDebit*-1),15000), 2),
              "Debit" : maxDebit,
              "Currency" : "Euro"            
            } 
        accounts.append(s)
    ##
    ##
    structure['Accounts']['Checking_account'] = accounts
 
    #
    # create saving accounts
    if numberOfSavingAccounts < 1: 
        numberOfSavingAccounts = 1
    if numberOfSavingAccounts > 5: 
        numberOfSavingAccounts = 5
   

    for x in range (0, numberOfSavingAccounts):
        if USE_PRINT_OUT :
            print ("Saving Account {}".format(x))
        ano = MOCK_IBANAccountID()
        s = {
              "Number": ano[1] ,
              "IBAN" : ano[0],
              "Created" : "10.01.2010",
              "Balance" : round(uniform(0,100000), 2),
              "Debit" : 0,
              "Currency" : "Euro"            
            } 
        accounts.append(s)
    ##
    ##
    structure['Accounts']['Saving_account'] = accounts

    return structure

def MOCK_Response(username, numberOfAccounts, numberOfSavingAccounts, CR):
    accounts = MOCK_AccountDetails(username, numberOfAccounts,numberOfSavingAccounts)
    #print (accounts)

    response = """Checking-Accounts"""
    response +=  CR + "-----------------"
    response += CR
    x=1
    for a in accounts['Accounts']['Checking_account']:
        response += "{:>3}. IBAN: {}, Current Balance: {:>12}{}".format(x, a["IBAN"],  a["Balance"], a['Currency'])
        if a["Balance"] < 0.0:
            response += " Your current debit is max {}{}".format(a['Debit'],a['Currency'])
        response += CR
        x = x+1
    return [accounts, response]

#
#
if USE_PRINT_OUT :
    result = MOCK_Response('CoCO',2,1, '\n')
    print (result[0])
    print (result[1])