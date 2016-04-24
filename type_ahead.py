import sys
# from pytrie import SortedStringTrie as trie

class Item(object):
    def __init__(self, item_type, item_id, score, words):
        self.type = item_type
        self.id = item_id
        self.score = score
        self.words = words

class Node(object):
    def __init__(self, children=None, item_ids=None):
        self.children = {}
        self.item_ids = set()

    def add(self, item, trie, total_items):

        current_node = None  #pointer

        for word in item.words:  #['adam', "d'angelo"]
            current_node = trie
            for letter in word:
                if letter not in current_node.children:
                    new_node = Node()
                    current_node.children[letter] = new_node
                    # print "current_node.children", current_node.children
                    # print "WHYYYYYYY"
                    new_node.item_ids.add(item.id)
                    current_node = new_node
                else:
                    current_node = current_node.children[letter]
                    current_node.item_ids.add(item.id)
                #     print "NOOOO"
                # print 'trie children:', trie.children
                # print 'trie item_ids:', trie.item_ids


class TypeAhead(object):
    def add(self, item, trie, total_items):
        total_items[item.id] = item
        trie.add(item, trie)

    def delete(self, item_id):

    def query(self, res_num, query):

    def wquery(self, res_num, boost_num, )


def read_stdin():
    trie = Node()    #root of the trie
    total_items = {}     # keeps track of all items
    type_ahead = TypeAhead()

    #returns an iterator object; if value called == sentinel, StopIteration will be raised; ignores the first command, the int
    for raw_line in iter(sys.stdin.readline, ""):
        line = raw_line.strip().split()

        if line[0] == 'ADD':
            item = Item(line[1], line[2], float(line[3]), [word.lower() for word in line[4:]])
            TypeAhead.add(item, trie, total_items)

        # if line[0] == 'DEL':

        # if line[0] == 'QUERY':

        # if line[0] == 'WQUERY':

if __name__ == '__main__':
    read_stdin()

