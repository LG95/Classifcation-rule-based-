To run the code, use 'python main.py' with one to three command line arguments.
A single argument, name, means attribute file, training file and an optional test file are, respectively, name-attr.txt, name-train.txt and name-test.txt.
Two arguments specify the names for attribute and training file.
Three arguments specify the names for attribute, training file and test file.

main.py contains treats the command line arguments, reads the necessary files, calls sequential_covering and displays the output.
build.py contains sequential_covering's implementation and the implementation of every helper function it uses.
tree.py contains the class used to represent a rule in the rule set and a helper function to classify a record according to a rule set.