import sys
from unidecode import unidecode
from operator import attrgetter
import re

class Item(object):
    """
    Item object initializes with 5 attributes: type, id, creation_id for keeping track of oldest to newest items, score, and words.
    Item object has 1 method: boost_score.
    """
    def __init__(self, item_type=None, item_id=None, creation_id=None, score=None, words=None):
        self.type = item_type
        self.id = item_id
        self.creation_id = creation_id
        self.score = score
        self.words = words


    def boost_score(self, boost_list):
        """This method modifies the score attribute of the item object."""
        score = self.score
        for boost in boost_list:
            if self.type == boost[0] or self.id == boost[0]:
                score = score * float(boost[1])
        return score


class Node(object):
    """
    Node object initializes with 2 attributes: a children dictionary and items set.
    Node object has 3 methods: add, delete, query.
    """
    def __init__(self, children=None, items=None):
        self.children = {}
        self.items = set()


    def add(self, item, trie):
        """
        This method takes in an item and the trie (root node of the trie).
        It modifies the trie by creating and adding nodes from the item's words to the trie.
        """
        current_node = None  # pointer

        for word in item.words:
            clean_word = unidecode(word.decode('utf8'))
            current_node = trie
            for letter in clean_word:
                if letter not in current_node.children:
                    new_node = Node()
                    current_node.children[letter] = new_node
                    new_node.items.add(item)
                    current_node = new_node
                else:  # keep traversing the trie
                    current_node = current_node.children[letter]
                    current_node.items.add(item)


    def delete(self, item, trie):
        """
        This method takes in an item and the trie (root node of the trie).
        It modifies the trie by deleting nodes of the item's words.
        """
        current_node = None   # pointer

        for word in item.words:
            lower_word = word.lower()
            clean_word = unidecode(lower_word.decode('utf8'))
            current_node = trie
            for letter in clean_word:
                if letter not in current_node.children:
                    print "Error: Letter not found"
                else:
                    current_node = current_node.children[letter]
                    current_node.items.discard(item)  # delete item from set


    def query(self, query_word, trie):
        """
        This method takes in a query word and the trie (root node of the trie).
        It traveres the trie to match the nodes of the item's word.
        """
        current_node = None  # pointer

        clean_word = unidecode(query_word.decode('utf8'))
        current_node = trie

        for letter in clean_word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                return None
        query_items = current_node.items.copy()  # should return the last node with all the items that each word matches
        return query_items

class TypeAhead(object):
    """
    TypeAhead object initializes with no attributes.
    TypeAhead object has 3 methods: add, delete, query.
    """
    def add(self, item, trie, total_items):
        """
        This method takes in an item, trie (root node of the trie), and total_items.
        It modifies adds item.id and item to total_items and calls the trie's add method.
        """
        total_items[item.id] = item
        trie.add(item, trie)

    def delete(self, item_id, trie, total_items):
        """
        This method takes in an item_id, trie (root node of the trie), and total_items.
        It removes item.id and item from total_items and calls the trie's delete method if item is present.
        """
        item = total_items.pop(item_id, None)
        if item:
            trie.delete(item, trie)
        if item is None:
            print 'Error: Invalid Item ID'

    def query(self, res_num, trie, query_list, boost_list=None):
        """
        This method takes in res_num, trie (root node of the trie), query_list, and boost_list if present.
        It traverses the trie to match the nodes of the item's words and prints the res_num of results in descending score order.
        If boost_list is present, the score is modified by calling item.boost_score first and then printing the results.
        """
        query_items = trie.query(query_list[0], trie)
        if query_items is not None:
            for i in range(1, len(query_list)):
                new_query_items = trie.query(query_list[i], trie)
                if new_query_items is not None:
                    query_items &= new_query_items  # update set intersection
                else:
                    query_items = None  # there is no match, so set query_items = None

        if query_items is None or res_num == 0:  # there is no match or res_num to return is 0
            print ""
        elif boost_list is not None:  # if there are boosts, call item.boost_score
            boosts_sorted_query_items = sorted(query_items, key=lambda item: (item.boost_score(boost_list), item.creation_id), reverse=True)
            print " ".join([item.id for item in boosts_sorted_query_items[:res_num]])
        else:  # there are no boosts, return original score of matched items
            sorted_query_items = sorted(query_items, key=attrgetter('score', 'creation_id'), reverse=True)
            print " ".join([item.id for item in sorted_query_items[:res_num]])

def validate(line):
    """This function tests if line inputs are valid and returns a boolean."""

    VALID_COMMANDS = ['ADD', 'DEL', 'QUERY', 'WQUERY']

    if line[0] not in VALID_COMMANDS:
        print "Invalid Command"
        return False

    if line[0] == 'ADD':
        VALID_ITEM_TYPES = ['user', 'topic', 'question', 'board']
        if line[1] not in VALID_ITEM_TYPES:
            print "Invalid Item Type"
            return False

        id_match = re.search('^[\w]+$', line[2]) # test to see if the item id is an alphanumeric string
        if not id_match:
            print "Invalid Item ID"
            return False

        score_match = re.search("^[0-9.]+$", line[3])  # test to see item score contains digits
        if not score_match:
            print "Invalid Item Score"
            return False

    if line[0] == 'DEL':
        id_match = re.search('^[\w]+$', line[1])  # test to see if the item id is an alphanumeric string
        if not id_match:
            print "Invalid Item ID"
            return False

    if line[0] == 'QUERY':
        results_num = re.search("^[0-9]+$", line[1])  # test to see results_num contains digits
        if results_num is None:
            print "Invalid Number of Results"
            return False

    if line[0] == 'WQUERY':
        results_num = re.search("^[0-9]+$", line[1])  # test to see results_num contains digits
        if results_num is None:
            print "Invalid Number of Results"
            return False

        boosts_num = re.search("^[0-9]+$", line[2])  # test to see num_boosts contains digits
        if boosts_num is None:
            print "Invalid Number of Boosts"
            return False
    return True

def main():
    trie = Node()  # root of the trie
    total_items = {}  # keeps track of all items
    type_ahead = TypeAhead()
    creation_id = 1

    #returns an iterator object; if value called == sentinel, StopIteration will be raised; ignores the first command int line
    for raw_line in iter(sys.stdin.readline, ""):
        line = raw_line.strip().split()

        if validate(line):
            if line[0] == 'ADD':
                creation_id += 1
                item = Item(line[1], line[2], creation_id, float(line[3]), [word.lower() for word in line[4:]])
                type_ahead.add(item, trie, total_items)

            if line[0] == 'DEL':
                type_ahead.delete(line[1], trie, total_items)

            if line[0] == 'QUERY':
                type_ahead.query(int(line[1]), trie, [word.lower() for word in line[2:]])

            if line[0] == 'WQUERY':
                num_boosts = int(line[2])
                type_ahead.query(int(line[1]), trie, [word.lower() for word in line[3+num_boosts:]], [boost.split(':') for boost in line[3:3+num_boosts]])

if __name__ == '__main__':
    main()
