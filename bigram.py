import nltk

myString = 'abc*def'
Bigrams = []

spaced = ''
for ch in myString:
    spaced = spaced + ch + ' '

tokenized = spaced.split(" ")
myList = list(nltk.bigrams(tokenized))

for i in myList:
    Bigrams.append((''.join([w + '' for w in i])).strip())

Bigrams = [x for x in Bigrams if "*" not in x and len(x) is 2]

print(Bigrams)