import collections
from bitarray import bitarray

from .node import Node


class HuffmanTree:
    elements_dict = {}
    encoded_elements = {}
    elements_length = 0
    garbage_bits = 0
    nodes_list = []
    base_nodes = []
    root = None
    encoded_data = bitarray()
    decoded_data = ''
    decoded_list = []

    def __init__(self, data='', elements_dict=None):
        """
        DO NOT ENTER BOTH ARGUMENTS, ONLY ONE OF THEM IS NEEDED FOR IT TO WORK
        elements_dict is the dictionary of values and their frequencies.
        :type data: str
        :type elements_dict: dict
        """

        self.data = data
        if data:
            # if user passed user_doc in constructor then create elements_dict
            self.create_elements_dict()
        else:
            self.elements_dict = elements_dict
            self.garbage_bits = self.elements_dict.pop('g_bits')

    def create_elements_dict(self):
        """Creates elements_dict based on the text"""
        for data in self.data:
            if data in self.elements_dict:
                self.elements_dict[data] += 1
                continue
            self.elements_dict[data] = 1
        self.elements_length = len(self.elements_dict)

    def sort_elements_dict(self):
        """This method sorts the elements_dict in ascending order based on the
        frequencies"""
        # Creating a sorted list of tuples of value and frequency
        sorted_list = sorted(self.elements_dict.items(), key=lambda kv: kv[1])
        # Converting the list of tuples into dictionary
        self.elements_dict = collections.OrderedDict(sorted_list)

    def create_base_nodes(self):
        """Creates base (leaf) nodes of the tree"""
        self.sort_elements_dict()
        for key in self.elements_dict:
            node = Node(value=key,
                        frequency=self.elements_dict[key],
                        is_leaf=True)
            self.nodes_list.append(node)
        self.base_nodes = self.nodes_list.copy()

    def insert_single_node(self, node):
        """Inserts a single node into the nodesList in the sorted manner"""

        for i in range(len(self.nodes_list)):
            if self.nodes_list[i].frequency > node.frequency:
                self.nodes_list.insert(i, node)
                return
        self.nodes_list.append(node)

    def create_tree(self):
        self.create_base_nodes()
        i = 0
        """Creates huffman tree based on 'elements_dict'"""
        while len(self.nodes_list) > 1:
            left_node = self.nodes_list[i]
            right_node = self.nodes_list[i + 1]
            left_node.is_left_child = True
            right_node.is_right_child = True
            combined_frequency = left_node.frequency + right_node.frequency
            current_node = Node(left=left_node,
                                right=right_node,
                                frequency=combined_frequency)
            current_node.left.parent = current_node
            current_node.right.parent = current_node
            # Deleting the first two nodes that are in the current_node
            del self.nodes_list[0:2]
            self.insert_single_node(current_node)
        self.root = self.nodes_list[0]

    def encode_elements(self):
        """Maps the binary encoding of the corresponding element into a dic"""

        for i in range(len(self.base_nodes)):
            binary_encoding = ''
            current_node = self.base_nodes[i]
            while current_node.parent is not None:
                if current_node.is_left_child:
                    # binary_encoding.insert(0, '0')
                    binary_encoding = '0' + binary_encoding
                if current_node.is_right_child:
                    # binary_encoding.insert(0, '1')
                    binary_encoding = '1' + binary_encoding
                current_node = current_node.parent

            self.encoded_elements[self.base_nodes[i].value] = binary_encoding

    def compress(self, key):
        """Compresses the string in text"""
        self.encode_elements()

        for element in self.data:
            for bit in self.encoded_elements[element]:
                if bit == '0':
                    self.encoded_data.append(False)
                    continue
                if bit == '1':
                    self.encoded_data.append(True)

        binary_key = bin(key)[2:]
        starting_bits = '0' * (8 - len(binary_key))
        binary_key = starting_bits + binary_key
        self.encoded_data = bitarray(binary_key) + self.encoded_data

        self.garbage_bits = 8 - (len(self.encoded_data) % 8)
        self.elements_dict['g_bits'] = self.garbage_bits

    def read_and_get_from_file(self, file_path):
        """ Reads data from file and returns the dict with encoded_data $ key """
        get_binary = bitarray()
        with open(file_path, 'rb') as fp:
            get_binary.fromfile(fp)
        key = get_binary[:8]
        binary_presentation = get_binary[8:]
        binary_presentation_length = len(binary_presentation)
        byte_presentation = binary_presentation.tobytes()
        byte_presentation_int = int.from_bytes(binary_presentation,
                                               byteorder='big',
                                               signed=False)
        encoded_data = bin(byte_presentation_int)[2:]
        significant_bit_length = binary_presentation_length - len(
            encoded_data)
        significant_bit = '0' * significant_bit_length
        encoded_data = significant_bit + encoded_data
        return {'key': key, 'encoded_data': encoded_data}

    def decompress(self, encoded_text_file):
        """ Decompresses the file based on elements_dict """

        self.create_tree()

        for i in range(self.garbage_bits):
            encoded_text_file = encoded_text_file[:-1]

        while len(self.decoded_data) != self.root.frequency:
            current_node = self.root
            while not current_node.is_leaf:
                if encoded_text_file[0] == '0':
                    current_node = current_node.left
                    encoded_text_file = encoded_text_file[1:]
                    continue
                if encoded_text_file[0] == '1':
                    current_node = current_node.right
                    encoded_text_file = encoded_text_file[1:]
                    continue
            self.decoded_data = self.decoded_data + current_node.value

    def image_decompress(self, encoded_text_file):
        """ Decompresses the file based on elements_dict """

        self.create_tree()

        for i in range(self.garbage_bits):
            encoded_text_file = encoded_text_file[:-1]

        while len(self.decoded_list) != self.root.frequency:
            current_node = self.root
            while not current_node.is_leaf:
                if encoded_text_file[0] == '0':
                    current_node = current_node.left
                    encoded_text_file = encoded_text_file[1:]
                    continue
                if encoded_text_file[0] == '1':
                    current_node = current_node.right
                    encoded_text_file = encoded_text_file[1:]
                    continue
            self.decoded_list.append(current_node.value)
        print(self.decoded_list)

    def get_compressed_file(self, key):
        """Returns the compressed file which contains compressed_text and
         encoded_elements"""
        self.compress(key)
        return [self.elements_dict, self.encoded_data]
