myString = 'abc*def'
Unigrams = []

spaced = ''
for ch in myString:
    spaced = spaced + ch + ' '

tokenized = spaced.split(" ")

for i in tokenized:
    Unigrams.append((''.join([w + '' for w in i])).strip())

Unigrams = [x for x in Unigrams if "*" not in x and len(x) is 1]

print(Unigrams)