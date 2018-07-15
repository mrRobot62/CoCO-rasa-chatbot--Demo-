
# if you change something in this cell please remove from next line the #, run cell and afterwards insert # again
#

# this is needed to load our training dataset
from rasa_nlu.training_data import load_data
# this is needed to load our configuration file
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu import config
# this is our Model-Trainer
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter

def training_nlu (data, config_spacy, model_path):
    training_data = load_data(data)
    # this is our Trainer, he's responsible to train the bot due to training data
    #trainer = Trainer(RasaNLUModelConfig({"pipeline": pipeline}))
    trainer = Trainer(config.load(config_spacy))

    # start training
    trainer.train(training_data)
    # persist the training result
    model_directory = trainer.persist(model_path, fixed_model_name = "coconlu")
 
def run_nlu():
    interpreter = Interpreter.load('./models/nlu/default/coconlu')
    print (interpreter.parse(u"I would like to have my account number"))
    
    
if __name__ == '__main__':
    #training_nlu('./data/data.json', "./config_spacy.yml", './models/nlu')
    run_nlu()
