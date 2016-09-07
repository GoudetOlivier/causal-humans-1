"""
Filter out unwanted couples of variables and generate the final input file
Author : Diviyan Kalainathan
Date : 28/06/2016
"""

import numpy
import csv
import os

inputfolder = 'output/obj8/'
var_info = 'input/Variables_info.csv'

# Loading data info
print('--Loading data & parameters--')
with open('input/Variables_info.csv', 'rb') as datafile:
    var_reader = csv.reader(datafile, delimiter=',', quotechar='\'')
    header = next(var_reader)
    name_var = []
    type_var = []
    num_bool = []
    spec_note = []

    for var_row in var_reader:  # Taking flags into account
        name_var += [var_row[0], var_row[0] + '_flag']
        type_var += [var_row[1], 'B']
        num_bool += [var_row[3], str(2)]
        spec_note += [var_row[4], str(-2)]
print len(name_var)
# Generate files for all clusters
print('--Generating input files--')
cluster_n = 0
while os.path.exists(inputfolder + 'cluster_' + str(cluster_n)):
    cluster_path = inputfolder + 'cluster_c_' + str(cluster_n) + '/data_c_' + str(cluster_n) + '.csv'

    print('--- Cluster n : ', cluster_n)
    # No filtering done

    # Open datafile to get the header
    with open(cluster_path, 'rb') as inputfile:
        datareader = csv.reader(inputfile, delimiter=';', quotechar='|')
        c_data_header = next(datareader)

    # Create output files
    with open(inputfolder + 'cluster_' + str(cluster_n) + '/pairs_c_' + str(cluster_n) + '.csv',
              'wb') as sortedfile:
        datawriter = csv.writer(sortedfile, delimiter=';', quotechar='|')
        datawriter.writerow(['SampleID', 'A', 'B'])

    with open(inputfolder + 'cluster_' + str(cluster_n) + '/publicinfo_c_' + str(cluster_n) + '.csv',
              'wb') as sortedfile:
        datawriter = csv.writer(sortedfile, delimiter=';', quotechar='|')
        datawriter.writerow(['SampleID', 'A type', 'B-type'])

    with open(inputfolder + 'cluster_' + str(cluster_n) + '/predictions_c_' + str(cluster_n) + '.csv',
              'wb') as sortedfile:
        datawriter = csv.writer(sortedfile, delimiter=';', quotechar='|')
        datawriter.writerow(['SampleID', 'Target'])

    # Browse through vars
    for var_1 in range(len(c_data_header) - 1):
        for var_2 in range(var_1 + 1, len(c_data_header)):

            if not (var_1 + 1 == var_2 and c_data_header[var_2][-4:] == 'flag'):  # Useless to consider
                # the case of a var and its flag
                data_to_load = [var_1, var_2]

                # Taking flags into account when loading the data
                if c_data_header[var_1][-4:] == 'flag':
                    var_1_flag = True
                else:
                    var_1_flag = False
                    data_to_load += [var_1 + 1]

                if c_data_header[var_2][-4:] == 'flag':
                    var_2_flag = True
                else:
                    var_2_flag = False
                    data_to_load += [var_2 + 1]

                #Loading data
                data_to_load.sort()
                var_data = numpy.loadtxt(cluster_path, skiprows=1, usecols=data_to_load)

                if cluster_n == 0:
                    print(var_data.shape)

                SampleID = c_data_header[var_1] + '-' + c_data_header[var_2]
                data_A = []
                data_B = []

                # Load only data if there is no missing values
                for ppl in range(var_data.shape[0]):
                    if (var_1_flag or var_data[ppl, 1] == '1') and (
                                var_2_flag or var_data[ppl, var_data.shape[1] - 1] == '1'):
                        # if the data is valid
                        data_A += var_data[ppl, 0]

                        if var_1_flag:
                            data_B += var_data[ppl, 1]
                        else:
                            data_B += var_data[ppl, 2]

                if len(data_A) > 25:

                    # Convert data_A and data_B into the right shape
                    A_values = ''
                    B_values = ''
                    for val in range(len(data_A)):
                        A_values = A_values + ' ' + data_A[val]
                        B_values = B_values + ' ' + data_B[val]

                    #Type of A & B
                    if type_var[var_1] == 'C':
                        typeA = 'Numerical'
                    elif type_var[var_1] == 'D':
                        typeA = 'Categorical'
                    elif type_var[var_1] == 'B':
                        typeA = 'Binary'
                    else:
                        print('ERROR : No type for A at var : ', var_1, name_var[var_1])
                        typeA=''

                    if type_var[var_2] == 'C':
                        typeB = 'Numerical'
                    elif type_var[var_2] == 'D':
                        typeB = 'Categorical'
                    elif type_var[var_2] == 'B':
                        typeB = 'Binary'
                    else:
                        print('ERROR : No type for B at var : ', var_2, name_var[var_2])
                        typeB=''

                    # Updating pairs head
                    with open(inputfolder + 'cluster_' + str(cluster_n) + '/pairs_c_' + str(cluster_n) + '.csv',
                              'a') as sortedfile:
                        datawriter = csv.writer(sortedfile, delimiter=';', quotechar='|',
                                                lineterminator='\n')
                        datawriter.writerow([SampleID, A_values, B_values])

                    # Updating public info
                    with open(inputfolder + 'cluster_' + str(cluster_n) + '/publicinfo_c_' + str(
                            cluster_n) + '.csv',
                              'a') as sortedfile:
                        datawriter = csv.writer(sortedfile, delimiter=';', quotechar='|',
                                                lineterminator='\n')
                        datawriter.writerow([SampleID, typeA , typeB])

                    # Updating predictions head
                    with open(inputfolder + 'cluster_' + str(cluster_n) + '/predictions_c_' + str(
                            cluster_n) + '.csv',
                              'a') as sortedfile:
                        datawriter = csv.writer(sortedfile, delimiter=';', quotechar='|',
                                                lineterminator='\n')
                        datawriter.writerow([SampleID, '0'])

    cluster_n += 1  # Increment for the loop
