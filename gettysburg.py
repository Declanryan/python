'''Gettysburg Address
We are going to do some simple analysis on this.
1. Count the number of words in the speech. We will exclude from our analysis a number of 'stop words', in our example
these will be the definite and indefinite articles and some personal pronouns.
2. Count the unique words in the collection produced by 1 above.
3. Count the number of occurrences of each word.'''

import string
import httplib2

def make_speech(contents):
    '''this function creates a string from the file and seperates each string into a list we then iterate through
     the list to check for stop words, it is then added to the new list and returned

    :param contents: file being passed for check
    :return: main_content_list
    '''

    main_content_list = []
    for stri in contents:
        line_list = stri.split()
        for word in line_list:

            stopwords =["a","an","the","--","i","me","he","him","she","her","it","we","us","you","they","them","who","what",
                        "this","that","these","those","mine","our","his","hers","here","have","thus","their","there","from",
                        "which","whether","might" ]
            word = word.lower()
            word.strip(string.whitespace).strip(string.punctuation)
            if word in stopwords:
                break
            else:
                word = word.strip(".,")
                main_content_list.append(word)
    return main_content_list

def make_unique_list(speech):
    '''this function checks the file for unique words within the file

    :param speech: file being passed for check
    :return: unique_speech_list
    '''
    unique_speech_list = []
    for word in speech:
        if word not in unique_speech_list:
            unique_speech_list.append(word)
    return unique_speech_list

def word_count(file_entered):
    '''counts the amount of times each word appears in the file and prints it to the console

    :param file_entered: file being passed for check
    :return:
    '''
    for word in file_entered:
        count =file_entered.count(word)
        if count ==1:
            print("The word {} appears {} time in the file".format(word,count))
        else:
            print("The word {} appears {} times in the file".format(word, count))



#accesses the file to be used
try:
    h = httplib2.Http(".cache")
    resp, content = h.request("http://mf2.dit.ie/gettysburg.txt", "GET")
    content = content.decode().split("\n")

except IOError as e:
    print(e)
    quit()

#calls the functions on the file and its results for analyses
speech_list = make_speech(content)
print("main content",speech_list)
print("length",len(speech_list))
print(" ")
unique_list = make_unique_list(speech_list)
print("unique content",unique_list)
print("length",len(unique_list))
print(" ")
word_count(speech_list)
