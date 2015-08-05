
import random

class Registry:
	guids = {};
	chars = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9"];
	guid_length = 10;
	def get_guid (self):

		guid = "";
		guid_found = False;

		while not guid_found:

			# randomly generate guid
			guid = ""
			for j in range(0,self.guid_length):
				i = int(random.random() * 36)
				guid += self.chars[i];

			# if it already exists, try another
			try:
				self.guids[guid];
			except KeyError:
				self.guids[guid] = True;
				guid_found = True;
		return guid;