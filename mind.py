# Minimally Invasive Neural Database
# cp Cameron Johnson

import copy

from mind_graph import Graph
from mind_machine import Machine


#my_string = "||Hello world, I've found the truth 1984.|";
my_string = "|In 1974 he began his coaching career by Stella Azzurra Roma where he stayed for five seasons. The first season came out 12th in the Serie A1, also participating with the team at the FIBA Korac Cup where they arrived until the Group stage of 16. The next two seasons were his best in Stella Azzurra. In 1976 he led his team to fourth place in the regular season and won the participation rights in the Korac Cup of the next year. In the season 1976-77 the European obligations after it cost the team came in eighth in the championship. However Valerio Bianchini led the compact team of Stella Azzurra in a frantic march (undefeated for 6 consecutive games) in Korac Cup that was only interrupted in the semifinals against the subsequent winner Jugoplastika Split. In his last year with the team despite the 4th place of the regular season was not able to overcome the obstacle of Billy Milano in the playoff 2976 quarterfinals.|"
#my_string = "|t |";
#my_string = "||My name is the nightwind. The furious form of blushing bright paint that radiates the stars and sky of this grave disaster.||"
#my_string = "|the world|";
#my_string = "|It's all a hoax. A fable we're eager to believe, both as the pickers and the picked (and the rejected).  What would happen if we spent more time on carefully assembling the pool of 'good enough' and then randomly picking the 5%? And of course, putting in the time to make sure that the assortment of people works well together...  [For football fans: Tom Brady and Russell Wilson (late picks who win big games) are as likely outcomes as Peyton Manning (super-selected). Super Bowl quarterbacks, as high-revenue a selection choice as one can make, come as often in late rounds as they do in the first one.]  [For baseball fans: As we saw in Moneyball, the traditional scouting process was essentially random, and replacing it by actually correlated signals changed everything.]|";
#my_string = "1 a 2 b"
# my_string = "||We're so close to hitting our goal of 50 Twitter
# donations to celebrate my #CPAC2015 Straw Poll victory! Chip-in >>
# https://secure.randpac.com/?sr=cpacwinner ||";
my_string = "||Ah, targeted online advertising. Thank you for perpetually showing me 600 pictures of something I already bought because I Googled it a single time (in order to buy it).||"
my_string = "||Hubert Wilkins was a native of Hallett, South Australia, the last of 13 children in a family of pioneer settlers and sheep farmers. He was born at Mount Bryan, South Australia, 100miles north of Adelaide.[2] The original homestead has been restored by generous donation. He studied at the Adelaide School of Mines.[3] As a teenager, he moved to Adelaide where he found work with a traveling cinema, to Sydney as a cinematographer, and thence to England where he became a pioneering aerial photographer whilst working for Gaumont Studios. His photographic skill earned him a place on various Arctic expeditions, including the controversial 1913 Vilhjalmur Stefansson-led Canadian Arctic Expedition.||"
my_string = "||Brackish water species can 4 be kept mainly the same as standard freshwater aquaria, but a hydrometer is used to check the salinity of the water. Certain kinds of brackish water fish need to have their salinity increased slightly every six months. The tank sizes can vary widely depending on the needs of the particular species, and the temperature is usually in the tropical range of 76-82 F. The substrate can vary from sand to gravel, but many aquarists choose crushed coral or aragonite sand, both of which help raise the hardness and pH to an acceptable level. Many brackish water fish, as any fish, can jump out of the tank, so it must be covered. Some brackish water species come from estuaries. ||"
#my_string = "||William Lamb (1 June 1893 - 12 January 1951) was a Scottish sculptor and artist. He was a survivor of the 'lost generation' who came of age in 1914, and was scarred, both mentally and physically, by the First World War. Lamb completed his training in 1915 as a right-handed artist. A war wound incapacitated his right hand, so that after the war he had to retrain as a left-hander. His urge to create was in no way diminished and his preferred medium was sculpture. Lamb's most productive period was from 1924 to 1933. As a result of an education on strictly traditional lines, he developed a style of modelling that was classically accurate, but which expressed the character and background of his subject.[1] Although he modelled Queen Elizabeth II as Princess Elizabeth aged six, in 1932,[2] he generally eschewed the rich, the famous and the heroic. Instead Lamb settled permanently in his native Montrose, Angus, Scotland, and sculpted the inhabitants of the town and neighbourhood, concentrating upon working class models, especially from the fishing community.[3] Fiercely independent, Lamb despised the young modernists and pre-war baroque fashions alike. He became isolated and developed severe depression around 1935/36,[4] turning into something of a recluse. He never escaped poverty, never married and his work has been largely forgotten outside east central Scotland.||"
my_string = my_string.lower()
my_array = []

# Convert the string into a graph
root_object = Graph(graphID="Char")
root_object.matching_object = my_string[0]

cur_obj = root_object
for c in my_string[1:]:
    new_obj = Graph(graphID="Char")
    # Unknown Object
    new_obj.matching_object = c
    cur_obj.nexts.append(new_obj)
    cur_obj = new_obj

cur_obj = root_object
while cur_obj != None:
    # print(cur_obj);
    if len(cur_obj.nexts) > 0:
        cur_obj = cur_obj.nexts[0]
    else:
        cur_obj = None

my_machine = Machine()

# Number Graph: One node, the number
# nn = Graph().node_from_file("number_node.txt","Number Node");
# number = Graph(startNodes=[nn], graphID="Number");

# Letter Graph: One node, the letter
# ln = Graph().node_from_file("letter_node.txt","Letter Node");
# letter = Graph(startNodes=[ln],graphID="Letter");

# Space Graph: One node: the space
# sn = Graph().node_from_file("space_node.txt","Space Node");
# space = Graph(startNodes=[sn], graphID="Space");

# Punctuation Graph: One node, the punctuation
# pn = Graph().node_from_file("punctuation_node.txt","Punctuation Node");
# punctuation = Graph(startNodes=[pn],graphID="Punctuation");

# Word Splitter Graph: One node, the word splitter
# wsn = Graph().node_from_file("word_splitter_node.txt", "WordSplitter Node");
# wordSplitter = Graph(startNodes=[wsn], graphID="WordSplitter");

# Since a node can be made up of a graph, we create a new node every time we want to use the graph
# We then use these nodes to build a larger, more complex graph

# -----------------
# WORD GRAPH:
# Space 1
# Letter 1
# Punctuation 1
# Letter 1
# #
# Letter 1
# Self
# Space 2
# End
# Punctuation 2
# End
# Word Splitter
# Letter 1
# letterNode = Graph(graphID="Letter",matches=letter);
# spaceNode2 = Graph(graphID="Space",matches=space);
# punctuationNode2 = Graph(graphID="Punctuation",matches=punctuation)
# spaceNode = Graph(graphID="Space",matches=space);
# punctuationNode = Graph(graphID="Punctuation",matches=punctuation)
# wordSplitterNode = Graph(graphID="WordSplitter",matches=wordSplitter);

# word = Graph(startNodes=[spaceNode2, punctuationNode2], graphID="Word");

# spaceNode2.nexts.append(letterNode);
# punctuationNode2.nexts.append(letterNode);
# wordSplitterNode.nexts.append(letterNode);

# spaceNode.nexts.append(None);
# punctuationNode.nexts.append(None);

# spaceNode.addedWord = False;		# The punctuations are not part of the word, but they define the boundaries
# punctuationNode.addedWord = False;
# spaceNode2.addedWord = False;
# punctuationNode2.addedWord = False;

# letterNode.nexts.append(letterNode);
# letterNode.nexts.append(spaceNode);
# letterNode.nexts.append(punctuationNode);
# letterNode.nexts.append(wordSplitterNode);
# letterNode.nexts.append(None);

# --------------------------------
# NUMBER GRAPH
# Space 1
# Number 1
# Punctuation 1
# Number 1
# #
# Number 1
# Self
# Punctuation 2
# Space 2
# long_number_node = Graph(graphID="Number",matches=number);
# number_space_node_1 = Graph(graphID="Space",matches=space);
# number_punctuation_node_1 = Graph(graphID="Punctuation",matches=punctuation)
# number_space_node_2 = Graph(graphID="Space",matches=space)
# number_punctuation_node_2 = Graph(graphID="Punctuation",matches=punctuation)

# long_number_graph = Graph(startNodes=[number_space_node_1, number_punctuation_node_1],graphID="Long Number");

# number_space_node_1.nexts.append(long_number_node);
# number_punctuation_node_1.nexts.append(long_number_node);

# number_space_node_2.nexts.append(None);
# number_punctuation_node_2.nexts.append(None);

# number_space_node_1.addedWord = False;		# The punctuations are not part of the word, but they define the boundaries
# number_space_node_2.addedWord = False;
# number_punctuation_node_1.addedWord = False;
# number_punctuation_node_2.addedWord = False;

# long_number_node.nexts.append(long_number_node);
# long_number_node.nexts.append(number_space_node_2);
# long_number_node.nexts.append(number_punctuation_node_2);

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
awn = Graph().node_from_file("article_node.txt", "Article Word")
article_word = Graph(startNodes=[awn], graphID="Article Word")

# Articles
article_word_node = Graph().node_from_file(article_word, "Article Word")

article_word_graph = Graph(
    startNodes=[article_word_node], graphID="Long Article Word")

# Preposition Word Graph: One node, the preposition word
pwn = Graph(graphID="Preposition Word Node", matches="preposition_node.txt")
pwn.nexts.append(None)
preposition_word = Graph(startNodes=[pwn], graphID="Preposition Word")

# Prepositions
preposition_word_node = Graph(
    graphID="Preposition Word", matches=preposition_word)

preposition_word_graph = Graph(
    startNodes=[preposition_word_node], graphID="Long Preposition Word")

preposition_word_node.nexts.append(None)

# Pronoun Word Graph: One node, the pronoun word
pwn = Graph(graphID="Pronoun Word Node", matches="pronoun_node.txt")
pwn.nexts.append(None)
pronoun_word = Graph(startNodes=[pwn], graphID="Pronoun Word")

# Pronouns
pronoun_word_node = Graph(graphID="Pronoun Word", matches=pronoun_word)

pronoun_word_graph = Graph(
    startNodes=[pronoun_word_node], graphID="Long Pronoun Word")

pronoun_word_node.nexts.append(None)


# The rules above find a general object from a series of less complex ones
# Once we have found that object, however, it is only one object
# So we create a new node for everything we've found

word_word_node = Graph(graphID="Word")
# This has no data, we only check the id
word_word_node.nexts.append(None)
word_word_graph = Graph(startNodes=[word_word_node], graphID="Word")

long_number_number_node = Graph(graphID="Long Number")
# This has no data, we only check the id
long_number_number_node.nexts.append(None)
long_number_number_graph = Graph(
    startNodes=[long_number_number_node], graphID="Long Number")

letter = Graph()
letter = letter.graph_from_file("letter")

space = Graph()
space = space.graph_from_file("space")

punctuation = Graph()
punctuation = punctuation.graph_from_file("punctuation")

number = Graph()
number = number.graph_from_file("number")

long_number_graph = Graph()
word = Graph()
print("Found------------------------------------------------------------")

long_number_graph = long_number_graph.graph_from_file("longnumber")
word = word.graph_from_file("word")

found = long_number_graph.get_graph_list_from_graph(long_number_graph)

my_machine.graphs.append(letter)
# Start the word when we see a letter?
my_machine.graphs.append(space)
my_machine.graphs.append(punctuation)
my_machine.graphs.append(number)

# Use the machine to parse our array of letters
found = my_machine.new_parse(root_object)
my_machine.prune_results(found)
print("Found------------------------------------------------------------")

cur_obj = found
while cur_obj != None:
    # print(cur_obj);
    if len(cur_obj.nexts) > 0:
        cur_obj = cur_obj.nexts[0]
    else:
        cur_obj = None

space.reset()
punctuation.reset()
word.reset()
number.reset()
punctuation.reset()
letter.reset()
long_number_graph.reset()

new_machine = Machine()
new_machine.graphs.append(space)
new_machine.graphs.append(punctuation)
new_machine.graphs.append(word)
new_machine.graphs.append(number)
new_machine.graphs.append(letter)
new_machine.graphs.append(long_number_graph)

new_found = new_machine.new_parse(found)
# for o in new_found:
# 	o.update();

# space.reset();
# punctuation.reset();
# word.reset();
# number.reset();
# letter.reset();
# long_number_graph.reset();

# new_machine = Machine();
# new_machine.graphs.append(space);
# new_machine.graphs.append(punctuation);
# new_machine.graphs.append(number);
# new_machine.graphs.append(letter)
# new_machine.graphs.append(long_number_graph);
# new_machine.graphs.append(long_number_number_graph);
# new_machine.graphs.append(article_word_graph);
# new_machine.graphs.append(preposition_word_graph);
# new_machine.graphs.append(pronoun_word_graph);
# new_machine.graphs.append(word_word_graph);

# new_found = new_machine.new_parse(new_found);

# for o in new_found:
# 	o.update();

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

print("Found------------------------------------------------------------")


my_machine.print_results(new_found)
