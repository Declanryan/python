import httplib2
import string
import time
__doc__ = ''''Using a dataset ( the "Adult Data Set") from the UCI Machine-Learning Repository we
can predict based on a number of factors whether someone's income will be greater than $50,000.

The technique:
The approach is to create a 'classifier' - a program that takes a new example record and, based
on previous examples, determines which 'class' it belongs to. In this problem we consider attributes
of records and separate these into two broad classes, <50K and >=50K. We begin with a training data
set - examples with known solutions. The classifier looks for patterns that indicate classification.
These patterns can be applied against new data to predict outcomes. If we already know the outcomes
of the test data, we can test the reliability of our model. If it proves reliable we could then use
it to classify data with unknown outcomes. We must train the classifier to establish an internal model
of the patterns that distinguish our two classes. Once trained we can apply this against the test data
- which has known outcomes. We take our data and split it into two groups - training and test - with most
of the data in the training set.

Building the classifier
Look at the attributes and, for each of the two outcomes, make an average value for each one, Then average
these two results for each attribute to compute a midpoint or 'class separation value'. For each record,
test whether each attribute is above or below its midpoint value and flag it accordingly. For each record
the overall result is the greater count of the individual results (<50K, >=50K). You should track the
accuracy of your model, i.e how many correct classifications you made as a percentage of the total number
of records.\n'''


def file_creation(file_entered):
    '''Splits the file into a training file and a testing file
    :param file_entered: file to be split
    :return: the two seperated files
    '''
    count = 0
    training_file_list = []
    testing_file_list = []
    for line_str in file_entered:
        line_str.strip(string.whitespace).strip(string.punctuation)
        if count <= int((len(file_entered))/100*75):
            training_file_list.append(line_str)
        elif int((len(file_entered))/100*75) < count <= len(file_entered):
            testing_file_list.append(line_str)
        else:
            break
        count += 1
    return training_file_list, testing_file_list


def make_data_set(list_entered):
    ''' Searches the file for band records and changes the file entered into a list of tuples
    :param list_entered: file to be changed
    :return: list of tuples and total bad records
    '''
    data_tuple_list = []
    bad_records = 0
    for line_str in list_entered:
        if '?' in line_str:
            bad_records += 1
            continue
        elif len(line_str) < 14:
            bad_records += 1
            continue
        age_str, workclass_str, fnlwgt_str, education_str, ednum_str, marital_status_str, occupation_str,\
            relationship_str, race_str, sex_str, cap_gain_str, cap_loss_str, hours_str, country_str,\
            result_str = line_str.split(',')

        fnlwgt_str, education_str, country_str = 0, 0, 0

        training_list = [int(age_str), (line_str.count(workclass_str) / len(line_str)), fnlwgt_str, education_str,
            int(ednum_str), (line_str.count(marital_status_str) / len(line_str)),
            (line_str.count(occupation_str) / len(line_str)), (line_str.count(relationship_str) / len(line_str)),
            (line_str.count(race_str) / len(line_str)), (line_str.count(sex_str) / len(line_str)), int(cap_gain_str),
            int(cap_loss_str), int(hours_str), country_str, result_str]

        data_tuple_list.append(training_list)

    return data_tuple_list, bad_records


def sum_of_lists(list_1, list_2):
    '''Adds the elements of the two lists entered together
    :param list_1: first list entered
    :param list_2: second list entered
    :return: Total of the two lists
    '''
    total_list = []
    for i in range(14):
        total_list.append(list_1[i] + list_2[i])
    return total_list


def get_average(list_entered, total_int):
    '''Averages the elements of the list by dividing each
       element by the total

    :param list_entered: file to be iterated through
    :param total_int: total for division
    :return: list of average values
    '''
    average_list = []
    for value_int in list_entered:
        average_list.append(value_int/total_int)
    return average_list


def train_classifier(list_entered):
    '''Splits the list into greater and less than lists,
       then we use the average function to obtain average values
       and the sum of function to add the lists together.

    :param list_entered:list to be used
    :return: the result of the averages and summation
    '''
    greater_than_50_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, " "]
    greater_count = 0
    less_than_50_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, " "]
    less_count = 0
    for person in list_entered:
        if person[-1] == ' <=50K':
            less_than_50_list = sum_of_lists(less_than_50_list, person)
            less_count += 1
        else:
            greater_than_50_list = sum_of_lists(greater_than_50_list, person)
            greater_count += 1

    less_than_average_list = get_average(less_than_50_list, less_count)
    greater_than_average_list = get_average(greater_than_50_list, greater_count)

    classifier_list = get_average(sum_of_lists(less_than_average_list, greater_than_average_list), 2)


    return classifier_list


def classify_test_set_list(test_set_list, classifier_list):
    ''' checks each index in the tuple against its corresponding averaged
     value from the classifier list

    :param test_set_list:the list of tupples to be checked
    :param classifier_list:the list against which the tuple is compared
    :return:list of tuples with 3 elements
    '''
    result_list = []
    for person_tuple in test_set_list:
        less_than_count = 0
        greater_than_count = 0
        result_str = person_tuple[-1]
        for index in range(14):
            if person_tuple[index] > classifier_list[index]:
                greater_than_count += 1
            else:
                less_than_count += 1
        result_tuple = (less_than_count, greater_than_count, result_str)
        result_list.append(result_tuple)
    return [result_list]


def report_results(result_set_list):
    ''' sorts the results into the correct category and displays the total count of records used,
     the no of inaccurate records and the percentage accuracy rate '''
    total_count = 0
    less_than_total = 0
    greater_than_total = 0
    inaccurate_count = 0
    unclassified = 0
    for first_list in result_set_list:
        for result_tuple in first_list:
            greater_than_count, less_than_count, result_str = result_tuple[:3]
            total_count += 1
            if (less_than_count > greater_than_count) and (result_str == ' <=50K'):
                inaccurate_count += 1
            elif(greater_than_count < less_than_count) and (result_str == ' >50K'):
                inaccurate_count += 1
            elif(less_than_count < greater_than_count) and (result_str == ' <=50K'):
                less_than_total += 1
            elif(less_than_count == greater_than_count) and (result_str == ' <=50K'):
                less_than_total += 1
            elif(greater_than_count > less_than_count) and (result_str == ' >50K'):
                greater_than_total += 1
            elif(greater_than_count == less_than_count) and (result_str == ' >50K'):
                greater_than_total += 1
            else:
                unclassified += 1
    print("out of", total_count, "people, there were ", inaccurate_count, "inaccuracy's")
    print("{} people got <50K, {} got >50K, Unclassified records is {}".format(less_than_total,
                                                                                  greater_than_total, unclassified))
    one_percent = total_count / 100
    percentage = (total_count - inaccurate_count) / one_percent
    print("that gives a percentage accuracy of %{:.2f}".format(percentage))


def main():
    ''' The main function opens the file to be used for classification. It then calls the functions
    in the order required.'''

    try:    # The request method gives us http header information and the content as a bytes object.
        h = httplib2.Http(".cache")
        header, content = h.request("http://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data", "GET")
        contents_str = content.decode().split('\n')

        # time is used two keep a check on the running time of the program
        start_time = time.time()

        # section 1:- of the program is used check the no of lines in the program, it then creates two files from the
        # original one for training(66%) and one for testing(34%). The program outputs how many lines are in each file
        print('*' * 50, '\n')
        print(__doc__)
        print('*' * 50, '\n')
        input("please press ENTER to continue \n")
        print('Total lines in main file ', len(contents_str))
        print("Creating the two files")
        training_file_list, testing_file_list = file_creation(contents_str)
        print("Files created successfully")
        print('The train file has', len(training_file_list))
        print('The test file has', len(testing_file_list), '\n')
        print('*' * 50, '\n')

        # section 2:- of the program uses the make data set function to create a training list of tuples and to
        # check for bad records in the file. The bad records and the new total file size is outputted
        print("Reading in training data...")
        training_tuple, bad_train_records = make_data_set(training_file_list)
        print("Done reading training data.")
        print("Bad records total in the training set is", bad_train_records)
        print('The total no of records in the training set is', len(training_tuple), '\n')
        print('*' * 50, '\n')

        # Section 3:- of the program is used to train the classifier , which involves Splitting the list into greater
        # and less than lists. Then we use the average function to obtain average values and the sum of function to
        # add the lists together.
        print("Training classifier...")
        classifier_list = train_classifier(training_tuple)
        print("Done training classifier.", '\n')
        print('*' * 50, '\n')

        # section 4:- of the program uses the make data set function to create a testing list of tuples and to
        # check for bad records in the file. The bad records and the new total file size is outputted
        print("Reading in test data...")
        test_set_list, bad_test_records = make_data_set(testing_file_list)
        print("Done reading training data.")
        print("Bad records total in the testing set is", bad_test_records)
        print("The total no of records in the test set is", len(test_set_list), '\n')
        print('*' * 50, '\n')

        # section 5 of the program uses the classify test set function to check each index in the tuple against its
        # corresponding averaged value from the classifier list. it then creates a list of tuples with 3 elements
        # the less than count, greater than count and the result_str
        print("Classifying records...")
        result_list = classify_test_set_list(test_set_list, classifier_list)
        print("Done classifying.", '\n')
        print('*' * 50, '\n')

        # section 6:- is used sort the results in to there correct category and output the results
        print("Printing results")
        report_results(result_list)
        print("The program took {:.2f} sec to run".format(time.time() - start_time))
        print("Program finished.", '\n')
        print('*' * 50, '\n')

    # the except is used to catch any io error within the main function and output the error
    except IOError as e:
        print(e)
        quit()

# Run if stand-alone
if __name__ == '__main__':
    main()






