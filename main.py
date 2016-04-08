#! /usr/bin/python

from build import CLASS, sequential_covering
from rules import classify

def parse(original):
	"""
	Separates words by blanks (space, tab or newline).

	Returns a list containing each word.

	Input:
		original - string containing the separated words.
	"""

	original += '\n' # ensuring a final word is not forgotten
	words = []	# list of words to be returned
	word = ''	# currently found word

	for char in original:	# checking each character in original
		if char not in [' ', '\t', '\n']:	# char is not a blank
			word += char	# add char to word

		elif word != '':	# word has characters in it
			words.append(word)	# add word to words
			word = ''	# reset word

	return words

def calculate_accuracy(records, rules):
	"""
	Calculate the acccuracy of classifying records with rules.

	Returns the percentage of records correctly classified.

	Input:
		records - set of records to be classified;
		rules - set of rules used to classify records.
	"""
	total = len(records)	# number of records
	misclassified = 0	# number of errors

	for record in records:	# for each record
		if record[CLASS] != classify(rules, record):	# classification error
			misclassified += 1

	return 100 - float(misclassified * 100) / total

def main(filenames):
	"""
	Read attribute description, training set and test set from files. Use them
	to build a rule-based classifier and evaluate it.

	Input:
		filenames - list with the names of files containing the attribute
	description, the training set and, optionally, the test set.
	"""

	attributes = []	# set of attributes
	training = []	# training set
	testing = []	# testing set

	if len(filenames) == 2:		# file with test set not supplied
		# extracting the name of each file from filenames
		attribute_filename, train_filename  = filenames
		test_filename = None	# no test set file

	else:
		# extracting the name of each file from filenames
		attribute_filename, train_filename, test_filename = filenames

	try:
		with open(attribute_filename) as file:	# on attribute file
			for line in file:	# each line in the file
				words = parse(line)	# separate the words on that line
				attributes.append( (words[0], words[1] == 'continuous', words[1:]) )
				# add the attribute (name, continuous?, values) to attributes

	except IOError:	# treat error opening attribute file
		print('Cannot read records without knowing their attributes. ' + attribute_filename + ' could not be opened.')

	if attributes != []:	# attributes was read
		class_name, continuous, values = attributes.pop()
		attributes.append( (CLASS, continuous, values) )
		# replace the name of the class attribute (assumed to be the last)
		# with the constant CLASS

		for filename, records in [(train_filename, training), (test_filename, testing)]:
		# on training and test set
			try:
				with open(filename) as file:	# on the respective file
					for line in file:	# each line in the file
						record = {}	# record on this line

						for attribute, value in zip(attributes, parse(line)):
						# match each word in this line to its respective 
						# attribute (based on position), treating word as the
						# value for this attribute in this record
							name, continuous, values = attribute
							# decompose the attribute

							if continuous:	# continuous attribute
								record[name] = float(value)	# store as float

							else:
								record[name] = value	# store as string

						records.append(record)	# add record to records

			except IOError:	# treat error opening file
				if records is training:	# only show error message on training set's file
					print('Cannot build a decision tree without training records. ' + training_filename + ' could not be opened.')

	if attributes != [] and training != []:	# attributes and training set were read
		attributes.pop()	# remove the class from attributes
		rules = sequential_covering(training, attributes)	# generate rule set

		for i, rule in enumerate(rules):
			print('r' + str(i + 1) + ': ' + str(rule))
			
		print('Accuracy on training set: ' + str( calculate_accuracy(training, rules) )  + '%')
		
		if testing != []:
			print('Accuracy on testing set: ' + str( calculate_accuracy(testing, rules) )  + '%')

if __name__ == '__main__':
	from sys import argv

	if len(argv) == 2:	# a single word was passed as an argument
		main( [ argv[1] + end for end in ['-attr.txt', '-train.txt', '-test.txt'] ] )
		# add the necessary suffixes to the word

	elif 3 <= len(argv) <= 4:	# each filename was passed individually
		main( argv[1:] )

	else:	# show help message
		print('Usage: ' + argv[0] + ' name')
		print('       ' + argv[0] + ' attribute_file training_file [test_file]\n')
		print('       name: attribute file, training file and an optional test file are, respectively, name-attr.txt, name-train.txt and name-test.txt')