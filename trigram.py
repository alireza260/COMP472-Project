import nltk

myString = 'abc*def'
Trigrams = []

spaced = ''
for ch in myString:
    spaced = spaced + ch + ' '

tokenized = spaced.split(" ")
myList = list(nltk.trigrams(tokenized))

for i in myList:
    Trigrams.append((''.join([w + '' for w in i])).strip())

Trigrams = [x for x in Trigrams if "*" not in x and len(x) is 3]

print(Trigrams)