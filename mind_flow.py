# Contains all the flowchart representations that objects and graphs feed from

import copy
import json
from mind_registry import Registry

# TODO: Rip out all the graph specific methods.
# Keep the GUID code and all of the nexts, etc
# Each flow will be called a node
# Rip out the matching stuff and the loading from files, json, etc
# Get Rid of startnode, really don't think it's useful

class Flow_Node:
	nexts = []								# Next step in the flowchart
	guid = "";								# Unique id to provide a reference
	currentNodes = None;					# Allows an external program to store a location in this flow
	flow_data = None;						# Arbitrary Data contained by this flow

	def __init__ (self, startNodes=[], data=[]):

		# If we have more than one entry node, combine them with a boolean
		if len(startNodes) > 0:
			self.startNode = Flow_Node();
			for sn in startNodes:
				self.startNode.nexts.append(sn);
			self.currentNodes = [self.startNode];
		self.nexts = [];

	def __str__ (self):
		rv = "Flow Node " + str(self.guid) + ": "
		return rv;

	def copy_self_with_no_children (self):
		rv = Flow_Node();
		rv.startNode = self.startNode;
		rv.currentNodes = self.currentNodes;
		rv.nexts = [];
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

	def reset (self):
		self.currentNodes = [self.startNode];