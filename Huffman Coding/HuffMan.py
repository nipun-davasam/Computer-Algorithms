# Reference used: https://www.geeksforgeeks.org/huffman-coding-greedy-algo-3/

import heapq


class node:
    def __init__(self, symbol, freq, left=None, right=None):
        # frequency of symbol
        self.freq = freq
        # symbol name (character)
        self.symbol = symbol
        # left node of current node
        self.left = left
        # right node of current node
        self.right = right
        # tree direction (0/1)
        self.huffValue = ''

    def __lt__(self, nxt):
        return self.freq < nxt.freq


class Huffman:
    def __init__(self, inputData):
        self.inputData = inputData

    def frequency_generator(self):
        symbol_freq = {}
        for symbol in self.inputData:
            symbol_freq[symbol] = symbol_freq.get(symbol, 0) + 1
        return symbol_freq

    def generate_huffman_tree(self):
        tree = [node(char, freq) for char, freq in self.frequency_generator().items()]
        heapq.heapify(tree)

        # to extract the smallest element based on frequency and build up the tree by traversing the queue
        while len(tree) > 1:
            leftNode = heapq.heappop(tree)
            rightNode = heapq.heappop(tree)
            leftNode.huffValue = 0
            rightNode.huffValue = 1
            newNode = node(symbol=leftNode.symbol + rightNode.symbol, freq=leftNode.freq + rightNode.freq,
                           left=leftNode, right=rightNode)
            heapq.heappush(tree, newNode)
        return tree[0]

    def build_huffman_codes(self, treeNode, val='', codes={}):
        huffman_encoding = val + str(treeNode.huffValue)

        # condition check for left node
        if treeNode.left:
            self.build_huffman_codes(treeNode.left, huffman_encoding, codes)
        if treeNode.right:
            self.build_huffman_codes(treeNode.right, huffman_encoding, codes)

        # condition for leaf node
        if not treeNode.left and not treeNode.right:
            codes[treeNode.symbol] = huffman_encoding

        return codes

    def write_codewords_to_file(self, output_file_path):
        root = self.generate_huffman_tree()
        codes = self.build_huffman_codes(root)
        # sorting codes wrt ascii for printing
        _codes = sorted(codes.keys(), key=lambda x: ord(x))
        sorted_codes = {i: codes[i] for i in _codes}
        print(sorted_codes)
        with open(output_file_path, 'w') as file:
            for char, code in sorted_codes.items():
                if char == '\n':
                    file.write(f"[\\n] -- {code}\n")
                else:
                    file.write(f"[{char}] -- {code}\n")
        file.close()

    def huffman_encoder(self, encoded_file_path, codewords_file_path):
        root = self.generate_huffman_tree()
        codes = self.build_huffman_codes(root)
        encoded_data = ''.join(codes[char] for char in self.inputData)
        with open(encoded_file_path, 'w') as encoded_file:
            encoded_file.write(encoded_data)
        encoded_file.close()

        self.write_codewords_to_file(codewords_file_path)

    def huffman_decoder(self, encoded_file_data, decoded_file_path):
        root = self.generate_huffman_tree()
        current_node = root
        decoded_data = ""

        for bit in encoded_file_data:
            if bit == '0':
                current_node = current_node.left
            else:
                current_node = current_node.right

            if not current_node.left and not current_node.right:
                # Found a leaf node, append the corresponding symbol to the decoded data
                decoded_data += current_node.symbol
                current_node = root  # Reset to the root for the next iteration

        with open(decoded_file_path, 'w') as decoded_file:
            decoded_file.write(decoded_data)


input_file = "input.txt"
codewords_output_file = "codewords.txt"
encoded_output_file = "encoding.txt"
decoded_output_file = "decoding.txt"

# call to input file that needs to undergo huffman encoding
with open(input_file, 'r') as file:
    data = file.read()

huffMan = Huffman(data)
huffMan.huffman_encoder(encoded_output_file, codewords_output_file)
with open(encoded_output_file, 'r') as file:
    encoded_data = file.read()
huffMan.huffman_decoder(encoded_data, decoded_output_file)
