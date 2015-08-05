# Minimally Invasive Neural Database
# cp Cameron Johnson

import copy
class New_Object:
	start = -1; # -1 so we know it's not set
	end = -1;
	objectId = "";
	childData = [];
	childString = "";
	matching_graph = None;

	next_object = None;
	start_object = None;

	def __init__ (self, iid):
		self.objectId = iid;
		self.childData = [];

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return str(self) == str(other);
		else:
			return False

	def update(self):
		self.childString = "";
		for c in self.childData:
			if c.childString:
				self.childString += c.childString;
			else:
				self.childString += c.objectId;

	def __str__ (self):
		self.update();
		if self.matching_graph:
			return "New Object " + self.objectId + "("+ str(self.start) +","+ str(self.end) +"): " + self.matching_graph.graphID + " " + self.childString;
		else:
			return "New Object " + self.objectId + "("+ str(self.start) +","+ str(self.end) +"): Unknown " + self.childString;

class Object:
	start = -1; # -1 so we know it's not set
	end = -1;
	objectId = "";
	childData = [];
	childString = "";
	matching_graph = None;

	def __init__ (self, iid):
		self.objectId = iid;
		self.childData = [];

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return str(self) == str(other);
		else:
			return False

	def update(self):
		self.childString = "";
		for c in self.childData:
			if c.childString:
				self.childString += c.childString;
			else:
				self.childString += c.objectId;

	def __str__ (self):
		self.update();
		return "Object " + self.objectId + "("+ str(self.start) +","+ str(self.end) +"): " + self.matching_graph.graphID + " " + self.childString;

# A graph is a collection of Nodes that are arranged as a tree
class Graph:
	currentString = "";
	parsedObjects = [];
	startNode = None;
	currentNodes = None;
	can_be_done = False;
	must_be_done = False;
	graphID = "";
	steps = 0;
	added_indices = [];

	# Node Logic
	matching_object = None;
	nexts = []
	addedWord = True; # Says whether this node is part of the finished product or just context
	nodeId = "";

	def __init__ (self,nodeId="", startNodes=[],matches=[]):
		if len(startNodes) > 0:
			self.startNode = Graph(nodeId="Boolean",matches=True);
			for sn in startNodes:
				self.startNode.nexts.append(sn);
			self.currentNodes = [self.startNode];
		self.currentString = "";
		self.parsedObjects = [];
		self.steps = 0;
		self.added_indices = [];

		# Node Logic
		# This is a file, so load the nodes from that
		if type(matches) == str:
			f = open("nodes/"+matches);
			f = f.readlines();
			matches = [];
			for l in f:
				l = l.replace("\n","");
				matches.append(l);
		# Its an array of nodes, so add them all as matching
		if type(matches) == list:
			pass;
		# Its a bool, so do whatever we do there
		if type(matches) == bool:
			pass;
		self.matching_object = copy.deepcopy(matches);
		self.nexts = [];
		self.addedWord = True;
		self.nodeId = nodeId;

	def __str__ (self):
		rv = "Graph"
		return rv;

	# Process a chain of objects
	def process_object_array (self, test_objects):

		# reset ourselves
		self.reset();

		found = False;

		# loop through everything in the chain
		for o in test_objects:

			# Process each object, and if any fails then return false
			found = self.step(o);
			if not found:
				return False;
		return True;

	# Add an object to the graph and step to see if it works
	def step (self, test_object):

		# Return True if this matches, False if not
		matches = False;

		# We could have more than one current node
		addNodes = [];
		removeNodes = [];
		for current in self.currentNodes:
			# Check each possiblity for a match
			for n in current.nexts:
				if (not n == None) and n.matches(test_object):
					removeNodes.append(current);
					addNodes.append(n);

					# Add this node to our chain
					if n.addedWord:
						self.added_indices.append(self.steps)
						self.parsedObjects.append(test_object);
						self.currentString += test_object.objectId;
					if n.nexts == [None]:
						removeNodes.append(current)

					matches = True;
		for n in removeNodes:
			if n in self.currentNodes:
				self.currentNodes.remove(n);
		for n in addNodes:
			self.currentNodes.append(n);

		# Set up whether everything is done
		self.must_be_done = True;
		for n in self.currentNodes:
			if None in n.nexts:
				self.can_be_done = True;
			if not n.nexts == [None]:
				self.must_be_done = False;

		self.steps += 1;

		return matches;

	def reset (self):
		self.currentNodes = [self.startNode];
		self.parsedObjects = [];
		self.currentString = "";

		self.can_be_done = False;
		self.must_be_done = False;
		self.added_indices = [];
		self.steps = 0;

	def getObjects (self):
		obj = Object(self.graphID);
		matching_graph = copy.deepcopy(self);
		matching_graph.reset();
		obj.matching_graph = matching_graph;
		obj.childData = self.parsedObjects;
		rv = obj
		return rv;

	# Node Logic
	# Inputs an object and checks if this Node is a match
	def matches (self, char_obj):
		if self.nodeId == char_obj.objectId:
			return True;
		# If node is a list, see if object id is in list
		if type(self.matching_object) is list:
			if char_obj.childString in self.matching_object:
				return True;
			if char_obj.objectId in self.matching_object:
				return True;
		# If object, check if ids are equal
		if isinstance(self.matching_object, Object):
			return self.matching_object.objectId == char_obj.objectId;
		# If a graph, try to process the graph with the object
		if isinstance(self.matching_object, Graph):
			self.matching_object.reset();
			if self.matching_object.process_object_array([char_obj]):
				return True;
			if self.matching_object.graphID == char_obj.objectId:
				return True;
		# If a boolean, return the boolean
		if isinstance(self.matching_object, bool):
			return self.matching_object;
		return False;


# Chooses the best object that matches given a string
class Machine:
	graphs = [];

	def __init__ (self):
		self.graphs = [];

	# Pass in an array of objects to parse
	def new_parse (self, iarray):

		found = [];			# New Objects
		in_process = [];	# Graphs

		# Go through each object
		for o in iarray:
			# Continue all the graphs we have previously found
			to_remove = []
			for g in in_process:
				if (g.step(o)):
					if (g.must_be_done):
						#found.append(copy.deepcopy(g.getObjects()));
						to_remove.append(g);
					elif (g.can_be_done):
						found.append(copy.deepcopy(g.getObjects()));
				else:
					to_remove.append(g);

			# Go through each of the graphs that could apply at this point
			to_add = [];
			for g in self.graphs:
				if (g.step(o)):
					if (g.must_be_done):
						to_add.append(copy.deepcopy(g.getObjects()));
						
					else:
						in_process.append(copy.deepcopy(g));
				g.reset();

			# Only allow the first possible match. Later use a better heuristic
			if len(to_add) > 0:
				found.append(to_add[0]);

			# Remove the ones that are no longer in progress
			for g in to_remove:
				# Remove the less complex possibilities but keep the more complex ones
				new_found = [];
				found_added = False;
				for ind in range(0,g.steps):
					if (not ind in g.added_indices):
						found_length = len(found) - g.steps;
						new_found.append(found[found_length + ind]);
					else:
						if not found_added:
							new_found.append(copy.deepcopy(g.getObjects()));
							found_added = True;
				found = found[:-1*g.steps] + new_found;
				in_process.remove(g);
		return found

my_string = "|Hello world, I've found the truth 1984.|";
my_string = "|In 1974 he began his coaching career by Stella Azzurra Roma where he stayed for five seasons. The first season came out 12th in the Serie A1, also participating with the team at the FIBA Korac Cup where they arrived until the Group stage of 16. The next two seasons were his best in Stella Azzurra. In 1976 he led his team to fourth place in the regular season and won the participation rights in the Korac Cup of the next year. In the season 1976-77 the European obligations after it cost the team came in eighth in the championship. However Valerio Bianchini led the compact team of Stella Azzurra in a frantic march (undefeated for 6 consecutive games) in Korac Cup that was only interrupted in the semifinals against the subsequent winner Jugoplastika Split. In his last year with the team despite the 4th place of the regular season was not able to overcome the obstacle of Billy Milano in the playoff 2976 quarterfinals.|";
#my_string = "|t |";
#my_string = "|the world|";
my_string = "|It's all a hoax. A fable we're eager to believe, both as the pickers and the picked (and the rejected).  What would happen if we spent more time on carefully assembling the pool of 'good enough' and then randomly picking the 5%? And of course, putting in the time to make sure that the assortment of people works well together...  [For football fans: Tom Brady and Russell Wilson (late picks who win big games) are as likely outcomes as Peyton Manning (super-selected). Super Bowl quarterbacks, as high-revenue a selection choice as one can make, come as often in late rounds as they do in the first one.]  [For baseball fans: As we saw in Moneyball, the traditional scouting process was essentially random, and replacing it by actually correlated signals changed everything.]|";
my_string = my_string.lower();
my_array = [];

# Split the string into character objects
for c in my_string:
	new_obj = Object(c);
	my_array.append(new_obj);

# Split the string into character objects
root_object = New_Object(my_string[0])
cur_obj = root_object;
for c in my_string[1:]:
	new_obj = New_Object(""); # Unknown Object
	new_obj.childString = c;
	cur_obj.next_object = new_obj;
	cur_obj = new_obj;

print(root_object);
cur_obj = root_object;
while cur_obj != None:
	print(cur_obj);
	cur_obj = cur_obj.next_object;

my_machine = Machine();

# Number Graph: One node, the number
nn = Graph(nodeId="Number Node",matches="number_node.txt");
nn.nexts.append(None)
number = Graph(startNodes=[nn]);
number.graphID = "Number";

# Letter Graph: One node, the letter
ln = Graph(nodeId="Letter Node", matches="letter_node.txt");
ln.nexts.append(None)
letter = Graph(startNodes=[ln]);
letter.graphID = "Letter";

# Space Graph: One node: the space
sn = Graph(nodeId="Space Node",matches="space_node.txt");
sn.nexts.append(None);
space = Graph(startNodes=[sn]);
space.graphID = "Space";

# Punctuation Graph: One node, the punctuation
pn = Graph(nodeId="Punctuation Node",matches="punctuation_node.txt");
pn.nexts.append(None);
punctuation = Graph(startNodes=[pn]);
punctuation.graphID = "Punctuation";

# Word Splitter Graph: One node, the word splitter
wsn = Graph(nodeId="WordSplitter Node", matches="word_splitter_node.txt");
wsn.nexts.append(None);
wordSplitter = Graph(startNodes=[wsn]);
wordSplitter.graphID = "WordSplitter"

# Since a node can be made up of a graph, we create a new node every time we want to use the graph
# We then use these nodes to build a larger, more complex graph

#-----------------
# WORD GRAPH:
# Space 1
#	Letter 1
# Punctuation 1
#	Letter 1
#
# Letter 1
#	Self
#	Space 2
#		End
#	Punctuation 2
#		End
#	Word Splitter
#		Letter 1
letterNode = Graph(nodeId="Letter",matches=letter);
spaceNode2 = Graph(nodeId="Space",matches=space);
punctuationNode2 = Graph(nodeId="Punctuation",matches=punctuation)
spaceNode = Graph(nodeId="Space",matches=space);
punctuationNode = Graph(nodeId="Punctuation",matches=punctuation)
wordSplitterNode = Graph(nodeId="WordSplitter",matches=wordSplitter);

word = Graph(startNodes=[spaceNode2, punctuationNode2]);
word.graphID = "Word";

spaceNode2.nexts.append(letterNode);
punctuationNode2.nexts.append(letterNode);
wordSplitterNode.nexts.append(letterNode);

spaceNode.nexts.append(None);
punctuationNode.nexts.append(None);

spaceNode.addedWord = False;		# The punctuations are not part of the word, but they define the boundaries
punctuationNode.addedWord = False;
spaceNode2.addedWord = False;
punctuationNode2.addedWord = False;

letterNode.nexts.append(letterNode);
letterNode.nexts.append(spaceNode);
letterNode.nexts.append(punctuationNode);
letterNode.nexts.append(wordSplitterNode);
#letterNode.nexts.append(None);

#--------------------------------
# NUMBER GRAPH
# Space 1
#	Number 1
# Punctuation 1
#	Number 1
#
# Number 1
#	Self
#	Punctuation 2
#	Space 2
long_number_node = Graph(nodeId="Number",matches=number);
number_space_node_1 = Graph(nodeId="Space",matches=space);
number_punctuation_node_1 = Graph(nodeId="Punctuation",matches=punctuation)
number_space_node_2 = Graph(nodeId="Space",matches=space)
number_punctuation_node_2 = Graph(nodeId="Punctuation",matches=punctuation)

long_number_graph = Graph(startNodes=[number_space_node_1, number_punctuation_node_1]);
long_number_graph.graphID = "Long Number";

number_space_node_1.nexts.append(long_number_node);
number_punctuation_node_1.nexts.append(long_number_node);

number_space_node_2.nexts.append(None);
number_punctuation_node_2.nexts.append(None);

number_space_node_1.addedWord = False;		# The punctuations are not part of the word, but they define the boundaries
number_space_node_2.addedWord = False;
number_punctuation_node_1.addedWord = False;
number_punctuation_node_2.addedWord = False;

long_number_node.nexts.append(long_number_node);
long_number_node.nexts.append(number_space_node_2);
long_number_node.nexts.append(number_punctuation_node_2);

#--------------------------------
# ARTICLE GRAPH
#
# Punctuation
#	Word
#		Punctuation
#		Space
# Space
#	Word
#		Punctuation
#		Space
#
# Word in article_node.txt

# Article Word Graph: One node, the article word
awn = Graph(nodeId="Article Word",matches="article_node.txt");
awn.nexts.append(None)
article_word = Graph(startNodes=[awn]);
article_word.graphID = "Article Word";

# Articles
article_word_node = Graph(nodeId="Article Word",matches=article_word);

article_word_graph = Graph(startNodes=[article_word_node]);
article_word_graph.graphID = "Long Article Word";

article_word_node.nexts.append(None);


# Preposition Word Graph: One node, the preposition word
pwn = Graph(nodeId="Preposition Word Node",matches="preposition_node.txt");
pwn.nexts.append(None)
preposition_word = Graph(startNodes=[pwn]);
preposition_word.graphID = "Preposition Word";

# Prepositions
preposition_word_node = Graph(nodeId="Preposition Word",matches=preposition_word);

preposition_word_graph = Graph(startNodes=[preposition_word_node]);
preposition_word_graph.graphID = "Long Preposition Word";

preposition_word_node.nexts.append(None);

# Pronoun Word Graph: One node, the pronoun word
pwn = Graph(nodeId="Pronoun Word Node",matches="pronoun_node.txt");
pwn.nexts.append(None)
pronoun_word = Graph(startNodes=[pwn]);
pronoun_word.graphID = "Pronoun Word";

# Pronouns
pronoun_word_node = Graph(nodeId="Pronoun Word",matches=pronoun_word);

pronoun_word_graph = Graph(startNodes=[pronoun_word_node]);
pronoun_word_graph.graphID = "Long Pronoun Word";

pronoun_word_node.nexts.append(None);


# The rules above find a general object from a series of less complex ones
# Once we have found that object, however, it is only one object
# So we create a new node for everything we've found

word_word_node = Graph(nodeId="Word");		# This has no data, we only check the id
word_word_node.nexts.append(None);
word_word_graph = Graph(startNodes=[word_word_node]);
word_word_graph.graphID = "Word";

long_number_number_node = Graph(nodeId="Long Number");		# This has no data, we only check the id
long_number_number_node.nexts.append(None);
long_number_number_graph = Graph(startNodes=[long_number_number_node]);
long_number_number_graph.graphID = "Long Number";

my_machine.graphs.append(letter);	# Start the word when we see a letter?
my_machine.graphs.append(space);
my_machine.graphs.append(punctuation);
my_machine.graphs.append(number);

found = my_machine.new_parse(my_array)	# Use the machine to parse our array of letters

# Apply the object operations
for o in found:
	o.update();

space.reset();
punctuation.reset();
word.reset();
number.reset();

new_machine = Machine();
new_machine.graphs.append(space);
new_machine.graphs.append(punctuation);
new_machine.graphs.append(word);
new_machine.graphs.append(number);
new_machine.graphs.append(letter)
new_machine.graphs.append(long_number_graph);

new_found = new_machine.new_parse(found);

for o in new_found:
	o.update();

space.reset();
punctuation.reset();
word.reset();
number.reset();
letter.reset();
long_number_graph.reset();

new_machine = Machine();
new_machine.graphs.append(space);
new_machine.graphs.append(punctuation);
new_machine.graphs.append(number);
new_machine.graphs.append(letter)
new_machine.graphs.append(long_number_graph);
new_machine.graphs.append(long_number_number_graph);
new_machine.graphs.append(article_word_graph);
new_machine.graphs.append(preposition_word_graph);
new_machine.graphs.append(pronoun_word_graph);
new_machine.graphs.append(word_word_graph);

new_found = new_machine.new_parse(new_found);

for o in new_found:
	o.update();

# space.reset();
# punctuation.reset();
# word.reset();
# long_number_graph.reset();

# new_machine = Machine();
# new_machine.graphs.append(space);
# new_machine.graphs.append(punctuation);
# new_machine.graphs.append(article_word_graph);
# new_machine.graphs.append(preposition_word_graph);
# new_machine.graphs.append(word_word_graph)
# new_machine.graphs.append(long_number_number_graph);

# new_found = new_machine.new_parse(new_found);

print("Found------------------------------------------------------------");
for o in new_found:
	print(o);
