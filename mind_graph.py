import copy
import json
from mind_registry import Registry

# A graph is a collection of Nodes that are arranged as a tree. The lowest node of a graph will match some value
class Graph:
	currentString = "";
	parsedObject = None;
	startNode = None;
	currentNodes = None;
	can_be_done = False;
	must_be_done = False;
	graphID = "";
	steps = 0;
	added_indices = [];
	matching_object = None
	nexts = []
	addedWord = True; # Says whether this node is part of the finished product or just context
	guid = "";

	def __init__ (self,graphID="", startNodes=[],matches=[]):

		if len(startNodes) > 0:
			self.startNode = Graph(graphID="Boolean",matches=True);
			for sn in startNodes:
				self.startNode.nexts.append(sn);
			self.currentNodes = [self.startNode];
		self.currentString = "";
		self.parsedObject = None;
		self.steps = 0;
		self.added_indices = [];

		# Node Logic
		# This is a file, so load the nodes from that
		if type(matches) == str or type(matches) == unicode:
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
		self.graphID = graphID;

	def __str__ (self):
		rv = "Graph " + str(self.graphID) + ": "
		if type(self.matching_object) == str:
			rv += self.matching_object + " "
		if isinstance(self.matching_object, Graph):
			rv += self.parsed_object_string(self.matching_object);
		if isinstance(self.matching_object, list):
			rv += "['"
			for l in self.matching_object:
				rv += str(l);
			rv += "']"
		rv+= " " + self.guid;

		return rv;

	def graph_from_file (self, ifile):
		f = open("graphs/"+ifile+".json");
		f = json.loads(f.read());
		rv = self.graph_from_json_list(f);
		return rv;
	
	def node_from_file (self, file_name, iid):
		rv = Graph(graphID=iid,matches=file_name);
		rv.nexts.append(None);
		return rv;

	def graph_from_json_list (self, ilist):

		# Give each item a unique identifier
		registry = Registry();
		found = {};

		first_guid = None;

		counter = 0;
		for i in ilist:
			i["guid"] = registry.get_guid();
			found[counter] = i;
			counter+=1;

		# load all the json into a dict with {"guid" : Graph}
		loaded = {};
		counter = 0;
		for i in ilist:
			g = self.graph_from_json(found[counter]);
			g.guid = i["guid"]
			loaded[found[counter]["guid"]] = copy.deepcopy(g);
			counter += 1;

		# Convert loaded to an array
		loaded_array = []
		for i in found:
			loaded_array.append(loaded[found[i]["guid"]]);

		# Go through all of the nexts and make sure they're set to the right value
		for i in found:
			nexts = found[i]["nexts"];
			new_nexts = [];
			for n in nexts:
				if (n < 0):
					new_nexts.append(None);
				else:
					new_nexts.append(loaded_array[n]);
			loaded[found[i]["guid"]].nexts = new_nexts;

		# Find the first node, the one to return
		anchor = copy.deepcopy(loaded[found[0]["guid"]]);
		# Update the start nodes to the loaded values

		start = anchor.startNode;
		new_nexts = []
		for n in start.nexts:
			if type(n) is int:
				new_nexts.append(loaded_array[n])
			else:
				new_nexts.append(n)

		start.nexts = new_nexts;

		return anchor

	def graph_from_json (self, ijson):
		rv = None;
		if "startNodes" in ijson:
			sns = []
			for sn in ijson["startNodes"]:
				# If this is a file name, load the node
				if type(sn) is str or type(sn) is unicode:
					sns.append(Graph().node_from_file(sn,sn));
				else:
					# Otherwise, its an int linking to another graph. Just return it and load it later
					sns.append(sn)

				rv = Graph(graphID=ijson["graphID"],startNodes=sns);
				rv.nexts = ijson["nexts"];
		else:
			rv = Graph(graphID=ijson["graphID"]);
			rv.nexts = ijson["nexts"];

		# Set up Matching Objects
		if "matches" in ijson:
			matches = ijson["matches"];
			parsed_matches = [];

			for m in matches:

				# If it's node a node, must be a graph, so load the graph from a file

				if not "node" in m:
					match = self.graph_from_file(m);
				else:
					node = self.node_from_file(m,m);
					node_id = m[0].upper() + m[1:-9];
					match = Graph(startNodes=[node],graphID=node_id)
				parsed_matches.append(match);
			parsed_matches[0].reset();
			parsed_matches[0].clear_guids(parsed_matches[0]);
			rv.matching_object = copy.deepcopy(parsed_matches[0]);

		if "added" in ijson:
			rv.addedWord = bool(ijson["added"])

		return rv;

	def copy_node_only (self):
		rv = Graph();
		rv.currentString = self.currentString;
		rv.parsedObject = self.parsedObject;
		rv.startNode = self.startNode;
		rv.currentNodes = self.currentNodes;
		rv.can_be_done = self.can_be_done;
		rv.must_be_done = self.must_be_done;
		rv.graphID = self.graphID;
		rv.steps = self.steps;
		rv.added_indices = self.added_indices;

		# Node Logic
		rv.matching_object = self.matching_object;
		rv.nexts = [];
		rv.addedWord = self.addedWord; # Says whether this node is part of the finished product or just context
		return rv;

	def get_graph_list_from_graph (self, node, found=None,debug=False, depth=0):

		if not node:
			return found;
		if not found:
			found = {}
			node.clear_guids(node);
			node.set_guids(node);
		try:
			found[node.guid];
			if debug:
				print("trying")
			return found;
		except KeyError:
			found[node.guid] = node;
			found = self.get_graph_list_from_graph(node.startNode,found=copy.deepcopy(found),depth=depth+1);
			for n in node.nexts:
				found = self.get_graph_list_from_graph(n, found=copy.deepcopy(found),depth=depth+1);
		return found;

	def clear_guids (self, node):

		if not node:
			return;
		if node.guid == "":
			return;
		else:
			node.guid = "";

			for n in node.nexts:
				n.clear_guids(n);
			node.clear_guids(node.startNode);
		return;

	def set_guids (self, node, registry=None):

		if (registry == None):
			registry = Registry();
			node.clear_guids(node);
		if not node:
			return;
		if not node.guid == "":
			return;
		else:
			node.guid = registry.get_guid();
			for n in node.nexts:
				if n:
					n.set_guids(n, registry=registry);
			node.set_guids(node.startNode,registry=registry);
		return;

	def parsed_object_string (self,root_object, rv=""):
		cur_obj = root_object;
		while cur_obj != None and cur_obj != []:
			if isinstance(cur_obj.matching_object, Graph):
				rv += str(cur_obj.matching_object.matching_object);
			elif type(cur_obj.matching_object) == str:
				rv += cur_obj.matching_object;
			if len(cur_obj.nexts) > 0:
				for n in cur_obj.nexts:
					rv += self.parsed_object_string(n);
				cur_obj = None;
				return rv;
			else:
				cur_obj = None;
				return rv;
		return rv

	def print_full (self):
		rv = "\n";
		rv += "ID:\t\t\t "+ str(self.graphID) + "\n"
		rv += "Current String:\t\t\t "+ str(self.currentString) + "\n"
		rv += "Parsed Object:\t\t "+ str(self.parsedObject)  + "\n"
		rv += "Start Node:\t\t "+ str(self.startNode) + "\n"
		rv += "Current Nodes:\t\t "+ str(self.currentNodes)  + "\n"
		rv += "Can be Done:\t\t "+ str(self.can_be_done) + "\n"
		rv += "Must be Done:\t\t "+ str(self.must_be_done)  + "\n"
		rv += "Steps:\t\t\t "+ str(self.steps) + "\n"
		rv += "Added Indices:\t\t "+ str(self.added_indices) + "\n"
		rv += "Matching Object:\t "+ str(self.matching_object) + "\n"
		rv += "Nexts:\t\t\t \n";
		for n in self.nexts:
			rv += "\t\t\t"+ str(n) + "\n"
		rv += "Added Word:\t\t "+ str(self.addedWord) + "\n"
		rv += "Guid:\t\t\t "+ str(self.guid) + "\n"

		print(rv);



	def print_recursive (self, new_found=None, indent=""):
		if new_found == None:
			new_found = self;
		cur_obj = new_found;
		while cur_obj != None and cur_obj != []:
			print(indent + str(cur_obj));
			if len(cur_obj.nexts) == 1:
				self.print_recursive(new_found=cur_obj.nexts[0],indent=indent);
				cur_obj = None;
			elif len(cur_obj.nexts) > 1:
				for n in cur_obj.nexts:
					self.print_recursive(new_found=n, indent=indent+"\t");
				cur_obj = None;
			else:
				cur_obj = None;

	def add_to_graph_end (self, root_object, new_object):

		if root_object == None:
			root_object = new_object;
			return root_object;

		cur_obj = root_object;
		while cur_obj != None:
			if len(cur_obj.nexts) > 0:
				cur_obj = cur_obj.nexts[0];
			else:
				new_object.nexts = [];
				cur_obj.nexts.append(new_object);
				return root_object;
		return None;

	def delete_object (self, root_object, del_object):

		cur_obj = root_object;
		while cur_obj != None:
			to_remove = [];
			for n in cur_obj.nexts:
				if del_object is n:
					to_remove.append(n);
			for t in to_remove:
				cur_obj.nexts.remove(t);

			if len(cur_obj.nexts) > 0:
				for n in cur_obj.nexts:
					self.delete_object(n, del_object);
				cur_obj = None;
			else:
				cur_obj = None;

	# Process a chain of objects: -> W -> O -> R -> D -> None
	def process_object (self, test_object):

		# reset ourselves
		self.reset();

		found = False;

		# Go through each object
		cur_obj = test_object;
		while cur_obj != None:

			found = self.step(cur_obj);
			if not found:
				return False;

			if len(cur_obj.nexts) > 0:
				cur_obj = cur_obj.nexts[0];
			else:
				cur_obj = None;
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
						if self.parsedObject:
							self.parsedObject = self.add_to_graph_end(self.parsedObject,test_object.copy_node_only());
						else:
							self.parsedObject = test_object.copy_node_only();
							self.parsedObject.nexts = [];

						self.currentString += test_object.graphID;
					
					if n.nexts == [None]:
						removeNodes.append(current)

					matches = True;
					if not n.addedWord:
						matches = test_object;
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

		# If they match but we're not using this object, return it

		return matches;

	def reset (self):
		self.currentNodes = [self.startNode];
		self.parsedObject = None;
		self.currentString = "";

		self.can_be_done = False;
		self.must_be_done = False;
		self.added_indices = [];
		self.steps = 0;

	def getObjects (self):
		obj = Graph();
		obj.graphID = self.graphID;
		matching_graph = copy.deepcopy(self);
		matching_graph.reset();
		obj.matching_graph = matching_graph;
		obj.matching_object = self.parsedObject;
		rv = obj
		return rv;

	def get_matching_string (self):
		if type(self.matching_object) is str:
			return self.matching_object;
		if isinstance(self.matching_object, Graph):
			return self.matching_object.get_matching_string();
		return "";

	# Node Logic
	# Inputs an object and checks if this Node is a match
	def matches (self, char_obj):
		# If node is a list, see if object id is in list
		if type(self.matching_object) is list:
			if isinstance(char_obj, Graph):
				if char_obj.get_matching_string() in self.matching_object:
					return True;
			return False;
		# If a graph, try to process the graph with the object
		if isinstance(self.matching_object, Graph):
			
			# If our node matches nothing and the input shares its id, they match
			if self.matching_object.graphID == char_obj.graphID:
				if len(self.matching_object.matching_object) == 0:
					return True;

			self.matching_object.reset();
			if self.matching_object.process_object(char_obj):
				return True;
		# If a boolean, return the boolean
		if isinstance(self.matching_object, bool):
			return self.matching_object;
		return False;