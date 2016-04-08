To run the code, use 'python main.py' with one to three command line arguments.

This code was developed on Ubuntu 14.04.4 LTS and its default python verion (2.7.x) is the most compatible.

Execution requires two files: attribute file, a simple text file containing the name and domain of each attribute, and training file, a simple text file containg any number of lines, each line having one value for each of the attributes described in the attribute file. An attribute's domain may be a sequence with all possible values or the word continuous for real numbers. An optional third file can be supplied, formatted identical to the training file. The data in the third file will be used to test the classifier.

A single argument, name, means attribute file, training file and an optional test file are, respectively, name-attr.txt, name-train.txt and name-test.txt.
Two arguments specify the names for attribute and training file.
Three arguments specify the names for attribute, training file and test file.

main.py contains treats the command line arguments, reads the necessary files, calls sequential_covering and displays the output.
build.py contains sequential_covering's implementation and the implementation of every helper function it uses.
tree.py contains the class used to represent a rule in the rule set and a helper function to classify a record according to a rule set.
