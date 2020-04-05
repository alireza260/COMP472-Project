def containsAccents(element_list):
    try:
        for x in element_list:
            x.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return True
    else:
        return False

listOfStrings = ['Hi' , 'hello', 'at', 'this', 'there', 'from']

print(containsAccents(listOfStrings))