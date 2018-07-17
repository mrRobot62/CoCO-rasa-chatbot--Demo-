
# to run this cell insert a # before %%writefile, to store content, remove #


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import warnings

from coco_policy import CoCO_Policy
from rasa_core import utils
from rasa_core.actions import Action
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.events import SlotSet
from rasa_core.featurizers import (
    MaxHistoryTrackerFeaturizer,
    BinarySingleStateFeaturizer)
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.policies.memoization import MemoizationPolicy

logger = logging.getLogger(__name__)

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
        return [SlotSet('matches', accounts)]

class ActionUsernameForm(Action):
    @staticmethod
    def required_fields():
        return [
            EntityFormField("username", "username"),
        ]
   
    def name(self):
        return 'action_username'
    
    def submit(self, dispatcher, tracker, domain):
        username = tracker.get_slot('username')
        username = username if username else "ERROR_UNKNOWN_USER"

        message = "Hi {}, nice to meet you".format(username)
        dispatcher.utter_message(message)
        return [SlotSet('username', username)]

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
        help = 'Following things can I do fo your' + CR
        help += '* ask me for your IBAN' + CR
        help += '* ask me for your banks BIC' + CR
        help += '* I can collect all your accounts' + CR
        help += '* I can give you current balance for an account' + CR
        help += '* I can check your debit for an account' + CR

        dispatcher.utter_message(help)
        return []

        
#------------------------------------------------------------------------------
# Training part of CoCO
#
# via parameter it is possible to train the nlu and/or the dialogue
#------------------------------------------------------------------------------
def train_dialogue(domain_file="coco_domain.yml",
                   model_path="./models/dialogue",
                   training_data_file="./data/coco_stories.md"):
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(max_history=3),
                            CoCO_Policy()])

    training_data = agent.load_data(training_data_file)
    agent.train(
            training_data,
            epochs=400,
            batch_size=100,
            validation_split=0.2
    )

    agent.persist(model_path)

    agent.visualize("data/coco_stories.md",
                    output_file="coco_graph.png", max_history=2)    
    return agent


def train_nlu():
    from rasa_nlu.training_data import load_data
    from rasa_nlu import config
    from rasa_nlu.model import Trainer

    training_data = load_data('./data/coco_data.json')
    trainer = Trainer(config.load("./config_spacy.yml"))
    trainer.train(training_data)
    model_directory = trainer.persist('./models/nlu/',
                                      fixed_model_name="coconlu")

    return model_directory

#------------------------------------------------------------------------------
# Online-Training
#------------------------------------------------------------------------------
def run_coco_online(input_channel, interpreter, 
                    domain_file='coco_domain.yml', 
                    training_data_file='data/coco_stories.md'):
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(max_history=3),
                            CoCO_Policy()],
                  interpreter=interpreter)

    training_data = agent.load_data(training_data_file)
    agent.train_online (
            training_data,
            max_history=2,
            batch_size=50,
            epochs=200,
            max_training_samples=300
    )

    #agent.persist(model_path)

    agent.visualize("data/coco_stories.md",
                    output_file="coco_graph.png", max_history=2)    
    return agent

#------------------------------------------------------------------------------
# If CoCO is trained, start him
#------------------------------------------------------------------------------

def run(serve_forever=True):
    interpreter = RasaNLUInterpreter("./models/nlu/default/coconlu")
    agent = Agent.load("./models/dialogue", interpreter=interpreter)

    if serve_forever:
        agent.handle_channel(ConsoleInputChannel())
    return agent


if __name__ == '__main__':
    utils.configure_colored_logging(loglevel="INFO")

    parser = argparse.ArgumentParser(
            description='starting CoCO')

    parser.add_argument(
            'task',
            choices=["train-online","train-nlu", "train-dialogue", "run"],
            help="what the bot should do - e.g. run or train?")
    task = parser.parse_args().task

    # decide what to do based on first parameter of the script
    if task == "train-nlu":
        train_nlu()
    elif task == "train-dialogue":
        train_dialogue()
    elif task == "train-online":
        nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/coconlu')
        run_coco_online(ConsoleInputChannel(), nlu_interpreter)

    elif task == "run":
        run()
        
        