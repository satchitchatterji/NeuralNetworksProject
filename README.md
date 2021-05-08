# NeuralNetworksProject

Yo

Controls for rocket:

space <- stop engine

w <- start engine

a <- turn anti-clockwise

s <- stop turning

d <- turn clockwise


Code still needs to be commented

+++++++++++++++++++++++++++++++++++++++

Generating data 2 ways
- sequence of lists with the features of the rocket [posX, posY, etc] as we drive it
- sequences of keys as we press them [w w w w..., s s s etc.] (might be more useful in the form [w4, s3 etc.])

We still need to make the rocket land by pressing keys ourselves (for the landing dataset) which is not easy
