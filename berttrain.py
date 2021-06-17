#https://github.com/bert-nmt/bert-nmt/tree/master/examples/cross_lingual_language_model
#https://github.com/pytorch/fairseq
#https://github.com/bert-nmt/bert-nmt
from transformers import BertForSequenceClassification, AdamW    #importing appropriate class for classification
import numpy as np
import pandas as pd
import torch
model = BertForSequenceClassification.from_pretrained('neuralmind/bert-base-portuguese-cased')   #Importing the bert model
model.train()     #tell model its in training mode so that some layers(dropout,batchnorm) behave accordingly
#model = AutoModelForMaskedLM.from_pretrained("bert-base-multilingual-cased")
from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased')

if torch.cuda.is_available():

    # Tell PyTorch to use the GPU.

    device = torch.device('cuda')

    print('There are %d GPU(s) available.' % torch.cuda.device_count())

    print('We will use the GPU:', torch.cuda.get_device_name(0))

# If not...

else:
    print('No GPU available, using the CPU instead.')
    device = torch.device('cpu')
print("1")
df1 = pd.read_csv('train.csv')
df2 = pd.read_csv('test.csv')
combined = pd.concat([df1,df2], axis=0)
combined = combined.drop(['keyword','location'], axis=1)
encoded = tokenizer(combined.text.values.tolist(), padding=True, truncation=True, return_tensors='pt')
print("2")
input_id = encoded['input_ids']
attention_mask = encoded['attention_mask']

train_id = input_id[:len(df1)]
train_am = attention_mask[:len(df1)]
test_id = input_id[len(df1):]
test_am = attention_mask[len(df1):]
train = combined.iloc[:len(df1)]
test = combined.iloc[len(df1):]
Xtrain = train.iloc[:6800]
Xtest =  train.iloc[6800:]
Xtrain_id = train_id[:6800]
Xtrain_am = train_am[:6800]
Xtest_id = train_id[6800:]
Xtest_am = train_am[6800:]
labels = torch.tensor(Xtrain.target.values.tolist())
labels = labels.type(torch.LongTensor)
labels.shape
optimizer = AdamW(model.parameters(), lr=1e-5)
n_epochs = 1
batch_size = 32
print("3")
for epoch in range(n_epochs):
    print("4")
    permutation = torch.randperm(Xtrain_id.size()[0])

    for i in range(0,Xtrain_id.size()[0], batch_size):

        optimizer.zero_grad()

        indices = permutation[i:i+batch_size]
        batch_x, batch_y,batch_am = Xtrain_id[indices], labels[indices], Xtrain_am[indices]

        outputs = model(batch_x, attention_mask=batch_am, labels=batch_y)
        loss = outputs[0]
        print(loss)
        loss.backward()
        optimizer.step()
model_save_name = 'my_model.pt'
path = F"./meumodelo/{model_save_name}"
torch.save(model.state_dict(), path)
torch.save(Xtest_id, './meumodelo/Xtest_id.pt')
torch.save(Xtest_am,'./meumodelo/Xtest_am.pt')

print(outputs[0])
torch.save(encoded,'./meumodelo/encoded.pt')

#baseado em https://github.com/suyash2104/Disaster-detector/blob/master/Bert_model_training.ipynb
# e