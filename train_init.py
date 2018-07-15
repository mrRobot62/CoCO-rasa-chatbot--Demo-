
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import logging

# this is the trainter agent
from rasa_core.agent import Agent
# both imports are the models how to train our model
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy

if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    # our stories for for the trainging
    training_data_file = './data/coco_stories.md'
    # path where files should be stored
    model_path = './models/dialogue'
    # Create a training agent with our domain file and the training models
    agent = Agent('coco_domain.yml', policies = [MemoizationPolicy(max_history = 2), KerasPolicy()])
    # start training, with 500 epochs (iterations), use a batch size of 10, and split trainting data into 80/20
    agent.train(
            training_data_file,
            epochs = 500,
            batch_size = 10,
            validation_split = 0.2)
    # store results       
    agent.persist(model_path)