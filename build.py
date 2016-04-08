from rules import Rule

CLASS = 'class'

def sequential_covering(records, attributes):
	"""
	Build a rule-based classifier using the sequential covering approach.

	Returns the rule set built.

	Input:
		records - set of records from which the classifier shall be built;
		attributes - set of the records' attributes.
	"""

	classes, frequencies = attribute_ocurrences(records, CLASS)
	# find the classes and their frequencies
	classes = zip(classes, frequencies) # pair each class with its frequency
	classes.sort(key = lambda p: p[1]) # sort classes by frequency (ascending)
	classes, frequencies = map(list, zip(*classes))
	# classes, frequencies = zip(*classes)
	# unpair each class from its frequency

	majority = classes.pop()	# classes - {majority class}
	rules = []	# the rule set to be returned

	for c in classes:	# each class left
		remaining = True	# are there still records of current class left?

		while remaining:	# there are still records in this class
			rule = learn_one_rule(records, attributes, c)	# generate a rule
			rules.append(rule)	# add rule to rules
			records = filter(lambda r: rule.classify(r) is None, records)
			# keep records not covered by the rule
			remaining = c in attribute_ocurrences(records, CLASS)[0]
			# update remaining to whether c can be found in records

	rules.append( Rule(majority) )	# default rule (predict majority class)

	return rules


def attribute_ocurrences(records, attribute_name):
	"""
	Finds the values of an attribute and their respective frequencies.

	Returns the values and their respective frequencies.

	Input:
		records - records used to determine values and frequencies;
		attribute_name - name of the attribute whose values and frequencies
	will be determined.
	"""

	frequencies = []	# frequencies of each value
	values = []	# values for this attribute

	for record in records:	# each record
		try:
			i = values.index( record[attribute_name] )
			# find position of this attribute's value in this record

		except ValueError:	# value not accounted for yet
			values.append( record[attribute_name] )	# add it to values
			frequencies.append(1)	# mark its frequency as 1

		else:
			frequencies[i] += 1	# update the value's frequency

	return values, frequencies

def learn_one_rule(records, attributes, clss):
	"""
	Determine a rule that best covers the input.

	Returns the rule.

	Input:
		records - set of records that the rule should try to cover best;
		attributes - set of records' attributes;
		clss - the class the rule should precdict.
	"""

	def aux_nominal(name, value):
		"""
		Creates the condition for a nominal attribute.

		Returns a function from record to boolean representing the condition.

		Input:
			name - name of the attribute;
			value - value for the attribute.
		"""

		return lambda r: r[name] == value	# name's value is equal to value


	def aux_continuous(name, value):
		"""
		Creates the condition for a continuous attribute.

		Returns a function from record to boolean representing the condition.

		Input:
			name - name of the attribute;
			value - value for the attribute.
		"""

		return lambda r: r[name] < value	# name's value is less than value

	k = len( attribute_ocurrences(records, CLASS)[0] )	# number of classes
	rule = Rule(clss)	# the generated rule
	conditions = []	# all desired attribute value relations
	strings = []	# the textual representation each element in conditions

	for name, cont, values in attributes:	# each attribute
		if cont:	# continuous attribute
			values = attribute_ocurrences(records, name)[0]	
			# the different values assumed by this attribute in records
			values.sort()	# sort the values in ascending order
			values = [ (values[i - 1] + values[i]) / 2 for i in range(1, len(values)) ]
			# replace values with the average of each consecutive pair of elements

			for value in values:	# each average
				strings.append(name + ' < ' + str(value))
				# add the text of this name to strings
				conditions.append( aux_continuous(name, value) )
				# add a continuous condition

		else:
			for value in values:	# each value
				value = value[:]	# value is a copy of an attribute value
				strings.append(name + ' = ' + str(value))
				# add the text of this name to strings
				conditions.append( aux_nominal(name, value) )
				# add a nominal condition

	better = True	# adding the best condition improved rule
	covered = records	# the records covered by the current rule
	current = 0	# the laplace of rule's current form

	while better:
		best = None	# index of the best condition
		laplace = 0	# laplace if the best condition were to be added

		for i, condition in enumerate(conditions):	# each conjunct and its index
			matches = filter(condition, covered)
			# the covered records matched by this condition

			if matches != []:	# some records in covered matches condition
				correct = len( filter(lambda r: r[CLASS] == clss, matches) )
				# number of covered records correctly classified
				total = len(matches)	# number of covered records

				l = float(correct + 1) / (total + k) # laplace with this condition

				if l >= laplace:
					best = i	# update best
					laplace = l	# update laplace

		better = laplace > current # update better

		if better:	# a best condition was found and improves laplace
			rule.add_conjunct(conditions[best], strings[best])
			# add the best condition to rule
			c = conditions.pop(best) # remove the best condition
			strings.pop(best) # remove the best condition's string
			covered = filter(c, covered)	# covered keeps records that match c
			current = laplace	# update current

	return rule