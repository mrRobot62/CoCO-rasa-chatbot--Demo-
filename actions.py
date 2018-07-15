
# to run this cell insert a # before %%writefile, to store content, remove #


from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

# some imports from rasa
from rasa_core.actions.action import Action
from rasa_core.events import SlotSet

#
# import our Account-MOCK - MOCK do some prints on the screen
import MOCK_AccountDetails

from random import randint, uniform, random

CR = '\n'

class ActionAccountNumber(Action):
    # via this function, we can get the action name.
    # if something is predicted, the chatbot will use this class
    def name(self):
        return 'action_accountnumber'
    
    # if this action should run, this function is called
    def run(self, dispatcher, tracker, domain):
        #
        # we create a random account number with 22 digits
        # In this example we assume, the customer have 2 different accounts
        username = tracker.get_slot('username')
        username = username if username else "ERROR_UNKNOWN_USER"
        #
        # create an account list from 1..10 checking accounts and 1..5 saving accounts
        accounts = MOCK_Response (username, randint(1,10), randint(1,5), CR)
        title = accounts[0]["Title"]
        account_list = CR + accounts[1]
        response = "Hi {} {}, I found follwing accounts : {}".format(title, username, account_list)
        
        #
        # send it out to the user
        dispatcher.utter_message(response)
        return [SlotSet('accounts', accounts)]

class ActionUsername(Action):
    def name(self):
        return 'action_username'
    
    def run(self, dispatcher, tracker, domain):
        username = tracker.get_slot('username')
        username = username if username else "ERROR_UNKNOWN_USER"

        message = "Hi {}, nice to meet you".format(username)
        dispatcher.utter_message(message)
        return [SlotSet('username', username)]
   
class ActionHelp(Action):
    def name(self):
        return 'action_help'
    
    def run(self, dispatcher, tracker, domain):
        username = tracker.get_slot('username')
        username = username if username else "ERROR_UNKNOWN_USER"

        help = 'Following things can I do fo your' + CR
        help += 'ask me for your IBAN'
        help += 'ask me for your banks BIC'
        help += 'I can collect all your accounts'
        help += 'I can give you current balance for an account'
        help += 'I can check your debit for an account'

        dispatcher.utter_message(help)
        return [SlotSet('username', username)]

        
        
        
        