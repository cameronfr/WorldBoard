import requests
import json
import datetime
from datetime import timedelta
import csv

if __name__ == "__main__":

  def function():
      "This takes withdrawal data and creates a json file with dates and total withdrawal money"


      #ENTERPRISE DATA FUN
      response=requests.get("http://api.reimaginebanking.com/enterprise/withdrawals?key=8757eef9232e4a86c7f328e9a24925c2")
      data=response.json()

      #Setting up the processes below:
      dates = datetime.datetime.now()
      dates = dates.replace(hour=0, minute=0, second=0, microsecond=0)
      count = 0.0
      typeint = type(data[u'results'][0][u'amount'])
      typefloat = type(data[u'results'][18][u'amount'])
      typedate = type(dates)

      #Turns amounts into float values
      for x in range(0, len(data[u'results'])):
        if 'transaction_date' in data[u'results'][x].keys():
            data[u'results'][x][u'amount'] = float(data[u'results'][x][u'amount'])

      #Error: date said "false" bruh
      data[u'results'][1153][u'transaction_date'] = '2016-10-02'

      #Change values to dates if possible.
      for y in range(0, len(data[u'results'])):
        if 'transaction_date' in data[u'results'][y].keys():
            try:
                data[u'results'][y][u'transaction_date'] = datetime.datetime.strptime(data[u'results'][y][u'transaction_date'], '%m/%d/%Y %H:%M %p')
            except ValueError:
                try:
                    data[u'results'][y][u'transaction_date'] = datetime.datetime.strptime(data[u'results'][y][u'transaction_date'], '%Y-%m-%d')
                except ValueError:
                    zz=0 #Filler Value

      #Creating a new dictionaries
      newdict = {}
      count_withdrawals = {}
      for w in range(0, 365):
          string_date = dates.strftime('%m/%d/%Y')
          newdict[string_date] = 0.0
          count_withdrawals[string_date] = 0.0
          for z in range(0, len(data[u'results'])):
              if 'transaction_date' in data[u'results'][z].keys():
                  if (typedate == type(data[u'results'][z][u'transaction_date'])):
                      if (dates<=data[u'results'][z][u'transaction_date']<=dates+timedelta(days=1)):
                          newdict[string_date] = newdict[string_date] + data[u'results'][z][u'amount']
                          count_withdrawals[string_date] = count_withdrawals[string_date] + 1

          print('Date: {}, Amount Withdrawn: {}, Number of Transactions: {}'.format(string_date, newdict[string_date], count_withdrawals[string_date]))
          dates = dates - timedelta(days=1)


      #Convert newdict into json variables.  Technically not needed
      newdict_json = json.dumps(newdict)
      print("newdict_json is the name of the json file for withdrawal amounts")
      count_withdrawals_json = json.dumps(count_withdrawals)
      print("count_withdrawals_json is the name of the json file for number of withdrawals per day")

      #Export files to current directory
      with open('amounts.json', 'w') as outfile:
          json.dump(newdict, outfile)
      with open('withdrawal_count.json', 'w') as outfile:
          json.dump(count_withdrawals, outfile)
