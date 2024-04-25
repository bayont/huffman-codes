import pickle,os
class Node:
  def __init__(self, char, freq):
    self.char = char
    self.freq = freq
    self.left = None
    self.right = None

  def __lt__(self, other):
    return self.freq < other.freq
  def __str__(self) -> str:
    return f"({self.char}, {self.freq}, left: {self.left}, right: {self.right})"
  
def get_freq_dict(text):
    freq_dict = {}
    for char in text:
        if char in freq_dict:
            freq_dict[char] += 1
        else:
            freq_dict[char] = 1
    return freq_dict

def min_heapify(A, i):
    l = 2*i
    r = 2*i + 1
    smallest = i
    if l < len(A) and A[l] < A[i]:
        smallest = l
    if r < len(A) and A[r] < A[smallest]:
        smallest = r
    if smallest != i:
        A[i], A[smallest] = A[smallest], A[i]
        min_heapify(A, smallest)

def build_min_heap(A):
    n = len(A)
    for i in range(n//2, -1, -1):
        min_heapify(A, i)

def min_heap_extract_min(A):
    if len(A) < 1:
        return None
    min = A[0]
    A[0] = A[-1]
    A.pop()
    min_heapify(A, 0)
    return min

def min_heap_insert(A, key):
    A.append(key)
    i = len(A) - 1
    while i > 0 and A[i] < A[i//2]:
        A[i], A[i//2] = A[i//2], A[i]
        i = i//2


def huffman_tree(freq):
  pq = [Node(char, value) for char, value in freq.items()]
  build_min_heap(pq)

  while len(pq) > 1:
    left =  min_heap_extract_min(pq)
    right =  min_heap_extract_min(pq)
    root = Node(None, left.freq + right.freq)
    root.left = left
    root.right = right
    min_heap_insert(pq, root)

  return min_heap_extract_min(pq)

def huffman_codes(tree, codes, prefix=""):
  if tree.left is None and tree.right is None:
    codes[tree.char] = prefix
    return

  huffman_codes(tree.left, codes, prefix + "0")
  huffman_codes(tree.right, codes, prefix + "1")

def encode(data, codes):
  encoded = ""
  for char in data:
    encoded += codes[char]
  return encoded
def get_bytes(data):
  return bytes([int(data[i:i+8], 2) for i in range(0, len(data), 8)])

def bytes_to_binary_string(bytes):
  bin_string = ""
  for byte in bytes:
    bin_string += format(byte[0], '08b')
  return bin_string


def decode(encoded, dictionary):
  decoded = ""
  current = ""
  for bit in encoded:
    current += bit
    if current in dictionary.values():
      decoded += list(dictionary.keys())[list(dictionary.values()).index(current)]
      current = ""
  return decoded

def decode_from_file(filename, divider):
  file = open(filename, "rb")
  huffman_bytes = []
  bytes_arr = file.read()
  for b in range(len(bytes_arr)):
    if bytes_arr[b:b+len(divider)] == divider:
      break
    huffman_bytes.append(bytes_arr[b:b+1])
  dictionary = pickle.loads(bytes_arr[b+len(divider):])
  huffman_bin_str =  bytes_to_binary_string(huffman_bytes)
  return decode(huffman_bin_str, dictionary)


def encode_to_file(text, filename, divider):
  freq = get_freq_dict(text)
  tree = huffman_tree(freq)
  codes = {}
  huffman_codes(tree, codes)
  encoded_data = encode(text, codes)
  bytes_to_write = get_bytes(encoded_data)
  encoded_file = open(filename, 'wb')
  encoded_file.write(bytes_to_write)
  encoded_file.write(divider)
  dictionary = {char: codes[char] for char in codes}
  dictionary_bytes = pickle.dumps(dictionary)
  encoded_file.write(dictionary_bytes)
  encoded_file.close()

  return encoded_data

def get_file_size(filename):
  return os.path.getsize(filename)

# Ustawiamy divider
divider = b'\xff\xfa'

# Pobieramy tekst z pliku to_code.txt
original_text = open("to_code.txt", "r").read()
# Kodujemy tekst i zapisujemy do pliku encoded.bin
encoded_data = encode_to_file(original_text, "encoded.bin", divider)
# Dekodujemy tekst z pliku encoded.bin
decoded_data = decode_from_file("encoded.bin", divider)

# Wypisujemy oryginalny tekst, zakodowany tekst i odkodowany tekst
print('-'*50)
print('original file size:', get_file_size('to_code.txt'),'bytes')
print('encoded file size with dictionary:', get_file_size('encoded.bin'),'bytes')

print('-'*50)
print('decoded text from file:', decoded_data)