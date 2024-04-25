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

def decode(encoded, tree):
  decoded = ""
  current = tree
  for bit in encoded:
    if bit == "0":
      current = current.left
    else:
      current = current.right
    if current.left is None and current.right is None:
      decoded += current.char
      current = tree
  return decoded

def get_ascii_data(text):
   data = ""
   for char in text:
        data += format(ord(char), '08b')
   return data

text = open("./to_code.txt", 'r').read()
freq = get_freq_dict(text)

tree = huffman_tree(freq)

codes = {}
huffman_codes(tree, codes)
print('Codes:', codes)

encoded_data = encode(text, codes)
open("./encoded.txt", 'w').write(encoded_data)
bytes_to_write = get_bytes(encoded_data)
open("./encoded.bin", 'wb').write(bytes_to_write)
decoded_data = decode(encoded_data, tree)
ascii_original_data = get_ascii_data(text)

print("Original data      :", text)
print("Ascii original data:", get_ascii_data(text), " | ", len(ascii_original_data), " bits")
print("Encoded data       :", encoded_data, " | ", len(encoded_data), " bits")
print("Decoded data       :", decoded_data)