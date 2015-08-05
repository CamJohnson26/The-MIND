import copy

from mind_graph import Graph

# Chooses the best object that matches given a string
class Machine:
	graphs = [];

	def __init__ (self):
		self.graphs = [];

	def print_results (self, new_found, indent=""):
		cur_obj = new_found;
		while cur_obj != None and cur_obj != []:
			print(indent + str(cur_obj));
			if len(cur_obj.nexts) == 1:
				self.print_results(cur_obj.nexts[0],indent=indent);
				cur_obj = None;
			elif len(cur_obj.nexts) > 1:
				for n in cur_obj.nexts:
					self.print_results(n, indent=indent+"\t");
				cur_obj = None;
			else:
				cur_obj = None;

	def last_object_of_list (self, root_object):

		cur_obj = root_object;
		while cur_obj != None:
			if len(cur_obj.nexts) > 0:
				cur_obj = cur_obj.nexts[0];
			else:
				return cur_obj;
		return None;

	def add_to_graph_end (self, root_object, new_object):

		if root_object == None:
			root_object = new_object;
			return root_object;

		cur_obj = root_object;
		while cur_obj != None:
			if len(cur_obj.nexts) > 0:
				cur_obj = cur_obj.nexts[0];
			else:
				new_object.nexts;
				cur_obj.nexts.append(new_object);
				return root_object;
		return None;

	def add_object_to_all_leaves (self, root_object, new_object, to_add=None):

		# Mark the changes and then update them all at once
		# If this is the first runthrough
		if to_add == None:

			# Fill our to add array by calling ourself
			to_add = [];
			to_add = to_add + self.add_object_to_all_leaves(root_object, new_object, to_add=to_add);

			for t in to_add:
				t.nexts = [] + new_object;
			return root_object;
		else:
			# If this is a leaf
			if root_object.nexts == []:
				return [root_object];
			else:
				new_to_add = []
				for n in root_object.nexts:
					new_to_add = new_to_add + (self.add_object_to_all_leaves(n, new_object, to_add=to_add));
				return new_to_add;
		return;

	# Pass in an object chain to parse
	def new_parse (self, iobject, debug=False):

		found = None;			# New Objects
		in_process = [];	# Graphs

		# Go through each object
		
		cur_obj = iobject;
		while cur_obj != None:
			# Continue all the graphs we have previously found
			to_remove = []
			to_delete = [];
			for t in in_process:	#(graph, place_to_append_it)
				g = t[0]
				parsed_object = g.step(cur_obj);
				if (parsed_object):

					# If the graph accepted the test object as context, add the context to found.
					if (g.must_be_done):
						to_remove.append(t);
					elif (g.can_be_done):
						t[1].nexts.append(copy.deepcopy(g.getObjects()));
				else:
					to_delete.append(t);

			# Go through each of the graphs that could apply at this point
			to_add = [];

			for g in self.graphs:
				parsed_object = g.step(cur_obj)
				if (parsed_object):
					if (g.must_be_done):
						to_add.append(copy.deepcopy(g.getObjects()));
					else:
						if (type(parsed_object) == bool):
							in_process.append([copy.deepcopy(g), self.last_object_of_list(found)]);	# (graph, end_of_found)
						else:
							# If the found node was just context, add it to found first.
							new_obj = cur_obj.copy_node_only();
							new_obj.nexts = [];
							to_add.append(new_obj);
							in_process.append([copy.deepcopy(g), new_obj]);
				g.reset();

			# Remove the ones that are no longer in progress
			for t in to_delete:
				found.delete_object(found, t[1]);
				in_process.remove(t);

			if len(to_remove) > 0:
				for t in to_remove:
					# Remove the less complex possibilities but keep the more complex ones
					g = t[0];
					t[1].nexts = [copy.deepcopy(g.getObjects())];
					in_process.remove(t);
				self.prune_results(found);

			# Only allow the first possible match. Later use a better heuristic
			if (found == None):
				found = to_add[0];
				found.nexts = [];

			else:
				found = self.add_object_to_all_leaves(found, to_add);

			if len(cur_obj.nexts) > 0:
				cur_obj = cur_obj.nexts[0];
			else:
				cur_obj = None;

		self.prune_results(found);
		return found;

	def heuristic (self, tree):
		score = 1;
		if len(tree.nexts) > 0:
			for n in tree.nexts:
				score += self.heuristic(n);
		return score;

	# Since our found object is a tree it's not good for parsing. Here we convert it to just the trunk
	def prune_results (self, found):
		if len(found.nexts) == 1:
			self.prune_results(found.nexts[0]);
		elif len(found.nexts) > 1:
			biggest = None;
			biggest_score = 0;
			for n in found.nexts:
				score = self.heuristic(n);
				if biggest == None or score < biggest_score:
					biggest = n;
					biggest_score = score;
			found.nexts = [biggest];
			self.prune_results(biggest);
		return;