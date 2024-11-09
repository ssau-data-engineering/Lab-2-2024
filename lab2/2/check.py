import os
train = set([dI for dI in os.listdir('/data/train') if os.path.isdir(os.path.join('/data/train',dI))])
test = set([dI for dI in os.listdir('/data/test') if os.path.isdir(os.path.join('/data/test',dI))])
val = set([dI for dI in os.listdir('/data/validation') if os.path.isdir(os.path.join('/data/validation',dI))])
print(train == test == val)
