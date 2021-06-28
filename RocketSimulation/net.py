from scene import Scene
from rocket import Rocket
from controller import RocketController
from extras import Vector
import torch.nn as nn
import torch
import pandas as pd
import os
import numpy as np

class Net(nn.Module):
    def __init__(self, input, hidden, output):
        super(Net,self).__init__()
        self.linear1=nn.Linear(input, hidden)
        self.linear2=nn.Linear(hidden, output)

        
    def forward(self,x):
        x=torch.sigmoid(self.linear1(x))  
        x=torch.sigmoid(self.linear2(x))
        return x
    
input_dim = 11     
hidden_dim =10
output_dim = 6

model = Net(input_dim,hidden_dim,output_dim)

# criterion=nn.CrossEntropyLoss()
criterion = nn.MSELoss()
# criterion = torch.nn.NLLLoss()

learning_rate=0.1
optimizer=torch.optim.SGD(model.parameters(), lr=learning_rate)

n_epochs=1
loss_list=[]
X = []
Y = []
trainloader = []

def data_loading():
    # DATA LOADING
    directory = 'saved_runs'

    controls = ['w',' ', 's', 'a', 'd', 'p']

    for filename in os.scandir(directory):
        if filename.is_file():
            with open(filename) as f:
                first_line = f.readline().split()
                if first_line[1] == "True":
                    train_file = pd.read_csv(filename, skiprows=2, usecols=range(11))
                    input_data = torch.tensor(np.array(train_file, dtype=np.float))
                    train_file = pd.read_csv(filename, skiprows=2, usecols=range(11, 12))
                    output_data = torch.zeros(train_file.shape[0], 6)
                    for index, row in train_file.iterrows():
                        key = row.p
                        col = controls.index(key)
                        output_data[index][col] = 1
                        
                    # print(input_data.size())
                    # print(output_data.size())
                    X.append(input_data)
                    Y.append(output_data)
                    
                    trainloader.append([input_data, output_data])  
                        


def train():
    for epoch in range(n_epochs):
        for inp, out in trainloader:
            for x, y in zip(inp, out):
        
                optimizer.zero_grad()
                sm = torch.nn.Softmax(dim=0)
                z=model(x.float())
                z = sm(z)

                loss = criterion(z, y)
                # loss = criterion(z, torch.max(y[0], 1)[1])

                loss.backward()

                optimizer.step()
                
                loss_list.append(loss.data)

            
        print('epoch {}, loss {}'.format(epoch, loss.item()))
    

def get_move(move):
    dict_output = {0: 'w', 1: ' ', 2: 's', 3: 'a', 4: 'd', 5: 'p'}
    return dict_output[move]


def main():

    scene = Scene(1000, 1000, init_target_val = 300)
    rocket = Rocket(scene, start_pos=Vector(100,100))
    controller = RocketController(rocket, physical_control = False)

    cur_frame = 0

    while(True):

        cur_frame+=1
        if cur_frame>60*20:
            print('Timeout!')
            rocket.is_dead = True

        if rocket.is_dead:
            break

        game_state = rocket.get_data_list()
        sm = torch.nn.Softmax()
        decision = model(torch.Tensor([game_state]))
        decision = sm(decision)
        maxel = torch.max(decision)

        key = get_move(((decision == maxel).nonzero(as_tuple=True)[0]).item())
        controller.control(key)
        rocket.update()
        scene.draw()


if __name__ == "__main__":
    data_loading()
    train()
    main()