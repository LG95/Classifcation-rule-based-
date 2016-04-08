class Rule:
	"""
	Represents a rule for a rule-based classifier. A rule is a set of functions
	from record to boolean, a set of textual representations for each function
	and a class that this rule predicts when a record matches all of the 
	functions (conditions).
	"""

	def __init__(self, clss):
		"""
		Construct an empty rule.

		Input:
			clss - the class that this rule predicts.
		"""

		self.conditions = []	# set of functional representations
		self.labels = []	# set of textual representations
		self.predict = clss	# predicted class

	def __str__(self):
		"""
		Convert this rule into a string, in the form conjunction of conditions
		implies prediction.

		Returns the string representing this rule.
		"""

		if self.labels != []:
			antecedent = reduce(lambda x, y: x + ' & ' +  y, self.labels)
			# the labels appended with & between each two
		else:
			antecedent = '()'			

		return antecedent  + ' ---> ' + str(self.predict)

	def add_conjunct(self, condition, label):
		"""
		Adds a conjunct (function and textual representation) to this rule.

		Input:
			condition - function (record -> boolean) representing this conjunct;
			label - textual label representing this conjunct.

		"""

		self.conditions.append(condition)	# add condition to conditions
		self.labels.append('(' + label + ')')	# add label to labels

	def classify(self, record):
		"""
		Predict record's class.

		Returns the class this rule predicts when record matches the conjunction
		of all conditions and None otherwise.

		Input:
			record - record whose class will be predicted.
		"""

		try:
			iterator = iter(self.conditions)	# iterator on conditions
			match = True	# does the antecedent match the record

			while match:
				condition = iterator.next()	# obtain the next function
				match = condition(record)	# update match to this condition

			return None

		except StopIteration:	# all conditions were tested
			return self.predict

def classify(rules, record):
	"""
	Classify records according to the rule set rules.

	Return the predicted class for record.

	Input:
		rules - set of rules (Rule objects);
		record - record to classify.
	"""

	prediction = None	# predicted class

	try:
		iterator = iter(rules)	# iterator on rules

		while prediction is None:	# a rule has not yet matched
			prediction = iterator.next().classify(record)
			# classify with the next rule

	except StopIteration:
		pass

	return prediction