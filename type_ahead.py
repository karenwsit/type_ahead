import sys
from unidecode import unidecode

class Item(object):
    def __init__(self, item_type, item_id, creation_id, score, words):
        self.type = item_type
        self.id = item_id
        self.creation_id = creation_id
        self.score = score
        self.words = words

    # def boost_score(self,)

class Node(object):
    def __init__(self, children=None, items=None):
        self.children = {}
        self.items = set()

    def add(self, item, trie):
        current_node = None  # pointer

        for word in item.words:
            clean_word = unidecode(word.decode('utf8'))
            print clean_word
            current_node = trie
            for letter in clean_word:
                if letter not in current_node.children:
                    # print "CREATING NEW NODE"
                    new_node = Node()
                    current_node.children[letter] = new_node
                    new_node.items.add(item.id)
                    current_node = new_node
                    # print "current_node.children", current_node.children
                    # print "current_node.items", current_node.items
                else:
                    # print "NO NEW NODE, KEEP TRAVERSING"
                    current_node = current_node.children[letter]
                    current_node.items.add(item.id)
                    # print "current_node.children", current_node.children
                    # print "current_node.items", current_node.items

    def delete(self, item, trie):
        current_node = None   # pointer

        for word in item.words:
            lower_word = word.lower()
            clean_word = unidecode(lower_word.decode('utf8'))
            print clean_word
            current_node = trie
            for letter in clean_word:  # [adam, black]
                if letter not in current_node.children:
                    print "Error: Letter not found"
                else:
                    current_node = current_node.children[letter]
                    print "BEFORE: current_node.items", current_node.items
                    current_node.items.discard(item.id)  # delete item from set
                    print "AFTER: current_node.items", current_node.items
                    print "CHILDREN:", current_node.children

    def query(self, query_list, trie):
        current_node = None  # pointer

        if query_list:
            for word in query_list:
                clean_word = unidecode(word.decode('utf8'))
                current_node = trie
                for letter in clean_word:
                    if letter in current_node.children:
                        current_node = current_node.children[letter]
                    else:
                        return None
                query_ids = current_node.items.copy()  # should return the last node with all the items that each word matches
            return query_ids
        else:
            return None

class TypeAhead(object):

    def add(self, item, trie, total_items):
        total_items[item.id] = item
        trie.add(item, trie)
        print "TOTAL ITEMS:", total_items
        print "FIRST LEVEL:", trie.children
        print "FIRST LEVEL ITEMS:", trie.items

    def delete(self, item_id, trie, total_items):
        item = total_items.pop(item_id, None)  # remove from total_items dictionary
        if item:
            trie.delete(item, trie)
            print "TOTAL ITEMS:", total_items
            print "FIRST LEVEL:", trie.children
            print "FIRST LEVEL ITEMS:", trie.items
        if item is None:
            print 'Error: Invalid Item ID'

    def query(self, res_num, trie, query_list):
        query_ids = trie.query(query_list[:1], trie)
        if query_ids and len(query_list) > 1:
            query_ids &= trie.query(query_list[1:], trie)  # &= set intersection update

        print "QUERY IDS:", query_ids

    # def wquery(self, res_num, boost_num, ):


def read_stdin():
    trie = Node()    # root of the trie
    total_items = {}     # keeps track of all items
    type_ahead = TypeAhead()
    creation_id = 1

    #returns an iterator object; if value called == sentinel, StopIteration will be raised; ignores the first command, the int
    for raw_line in iter(sys.stdin.readline, ""):
        line = raw_line.strip().split()
        print line

        if line[0] == 'ADD':
            creation_id += 1
            item = Item(line[1], line[2], creation_id, float(line[3]), [word.lower() for word in line[4:]])
            type_ahead.add(item, trie, total_items)

        if line[0] == 'DEL':
            type_ahead.delete(line[1], trie, total_items)

        if line[0] == 'QUERY':
            type_ahead.query(int(line[1]), trie, [word.lower() for word in line[2:]])

        # if line[0] == 'WQUERY':
        #     for word in line:
        #         if word.contains(":")
        #     type_ahead.wquery(int(line[1]), line[2], )

if __name__ == '__main__':
    read_stdin()
