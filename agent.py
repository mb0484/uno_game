import state_action_reward as sar

import pandas as pd
import numpy as np
import random

class MonteCarloAgent(object):

    def save_agent(self):
        self.q.to_csv("./monte-carlo-q.csv", sep = ";")
        self.visit.to_csv("./monte-carlo-visits.csv", sep = ";")

    def agent_init(self, agent_init_info):
        self.states      = sar.states()
        self.actions     = sar.actions()
        self.state_seen  = list()
        self.action_seen = list()
        self.q_seen      = list()
       
        self.epsilon   = agent_init_info["epsilon"]
        self.step_size = agent_init_info["step_size"]
        self.new_model = agent_init_info["new_model"]
        self.R         = sar.rewards(self.states, self.actions)
        
        
        if self.new_model == True:
            print("create new agent")
            self.q = pd.DataFrame(data    = np.zeros((len(self.states), len(self.actions))), 
                                  columns = self.actions, 
                                  index   = self.states)
            self.visit = self.q.copy()
        
        else:
            try:
                self.q            = pd.read_csv("./monte-carlo-q.csv", sep = ";", index_col = "Unnamed: 0")
                self.q.index      = self.q.index.map(lambda x: eval(x))
                self.q["IDX"]     = self.q.index
                self.q            = self.q.set_index("IDX", drop = True)
                self.q.index.name = None

                #print(self.q.columns)
                #print(self.q.actions)

                self.visit            = pd.read_csv("./monte-carlo-visits.csv", sep = ";", index_col = "Unnamed: 0")
                self.visit.index      = self.visit.index.map(lambda x: eval(x))
                self.visit["IDX"]     = self.visit.index
                self.visit            = self.visit.set_index("IDX", drop = True)
                self.visit.index.name = None
                #print(self.visit)
            
            #Create if file not found
            except:
                print ("Existing model could not be found. New model is being created.")
                self.q = pd.DataFrame(data    = np.zeros((len(self.states), len(self.actions))), 
                                      columns = self.actions, 
                                      index   = self.states)

                #print(self.q)
                self.visit = self.q.copy()
                #print(self.visit)

    
    def step(self, state_dict, actions_dict):
        state = [i for i in state_dict.values()]
        state = tuple(state)
        action = None
        
        #Random action
        if random.random() < self.epsilon:
            
            actions_possible = [key for key,val in actions_dict.items() if val != 0]

            if len(actions_possible) == 0:
                return None

            action = random.choice(actions_possible)
        
        # Greedy action
        else:
            actions_possible = [key for key,val in actions_dict.items() if val != 0]
            random.shuffle(actions_possible)
            val_max = 0
            
            for i in actions_possible:
                val = self.q.loc[[state],str(i)][0]
                if val >= val_max: 
                    val_max = val
                    action = i
        
        # (3) Add state-action pair if not seen in this simulation
        if action != None:
            if ((state),action) not in self.q_seen:
                self.state_seen.append(state)
                self.action_seen.append(action)
            
            self.q_seen.append(((state),action))
            self.visit.loc[[state], str(action)] += 1
        
        return action
    
    def update_single_action(self, state_dict, action, reward=0):
        state  = [i for i in state_dict.values()]
        state  = tuple(state)

        assert reward >= 0

        self.q.loc[[state], str(action)] += self.step_size * reward
    
    def update(self, state_dict, action):
        state  = [i for i in state_dict.values()]
        state  = tuple(state)
        reward = self.R.loc[[state], str(action)][0]
        
        for s,a in zip(self.state_seen, self.action_seen): 
            self.q.loc[[s], str(a)] += self.step_size * (reward - self.q.loc[[s], str(a)])
        
        self.state_seen, self.action_seen, self.q_seen = list(), list(), list()





class QLearningAgent(object):

    def save_agent(self):
        self.q.to_csv("./q-learning-q.csv", sep = ";")
        self.visit.to_csv("./q-learning-visits.csv", sep = ";")
    
    def agent_init(self, agent_init_info):
        self.states      = sar.states()
        self.actions     = sar.actions()
        self.prev_state  = 0
        self.prev_action = 0
        
        self.epsilon     = agent_init_info["epsilon"]
        self.step_size   = agent_init_info["step_size"]
        self.new_model   = agent_init_info["new_model"]
        self.R           = sar.rewards(self.states, self.actions)        

        
        if self.new_model == True:
            self.q = pd.DataFrame(data    = np.zeros((len(self.states), len(self.actions))), 
                                  columns = self.actions, 
                                  index   = self.states)
            
            self.visit = self.q.copy()
        
        
        else:
            try:
                self.q            = pd.read_csv("./q-learning-q.csv", sep = ";", index_col = "Unnamed: 0")
                self.q.index      = self.q.index.map(lambda x: eval(x))
                self.q["IDX"]     = self.q.index
                self.q            = self.q.set_index("IDX", drop = True)
                self.q.index.name = None

                self.visit            = pd.read_csv("./q-learning-visits.csv", sep = ";", index_col = "Unnamed: 0")
                self.visit.index      = self.visit.index.map(lambda x: eval(x))
                self.visit["IDX"]     = self.visit.index
                self.visit            = self.visit.set_index("IDX", drop = True)
                self.visit.index.name = None

            #Create if file is not found
            except:
                print ("Create new model")
                self.q = pd.DataFrame(data    = np.zeros((len(self.states), len(self.actions))), 
                                      columns = self.actions, 
                                      index   = self.states)

                self.visit = self.q.copy()
            
    
    def step(self, state_dict, actions_dict):
        state = [i for i in state_dict.values()]
        state = tuple(state)
        
        #Random action
        if random.random() < self.epsilon:
            
            actions_possible = [key for key,val in actions_dict.items() if val != 0]

            if len(actions_possible) == 0:
                return (None, False)

            action = random.choice(actions_possible)
        
        #Greedy action
        else:
            actions_possible = [key for key,val in actions_dict.items() if val != 0]

            if len(actions_possible) == 0:
                return (None, False)

            random.shuffle(actions_possible)
            val_max = 0
            
            for i in actions_possible:
                val = self.q.loc[[state],str(i)][0]
                if val >= val_max: 
                    val_max = val
                    action = i
        
        return (action, len(actions_possible) > 1)
    
    
    def update(self, state_dict, action, reward=0.0):
        state = [i for i in state_dict.values()]
        state = tuple(state)
        
        if self.prev_state != 0:
            prev_q = self.q.loc[[self.prev_state], str(self.prev_action)][0]
            this_q = self.q.loc[[state], str(action)][0]
            #reward = self.R.loc[[state], str(action)][0]

            assert reward >= 0.0 and reward <= 1.0
            
            if reward == 0.0:
                self.q.loc[[self.prev_state], str(self.prev_action)] = prev_q + self.step_size * (reward + this_q - prev_q) #if current q vecji, pol smo prsl na boljse zato se prev_q poveca, drugace se pa zmanjsa
            else:
                self.q.loc[[self.prev_state], str(self.prev_action)] = prev_q + self.step_size * (1.0 - prev_q) * reward # reward -> 0 : 1
                
            self.visit.loc[[self.prev_state], str(self.prev_action)] += 1
            
        self.prev_state  = state
        self.prev_action = action