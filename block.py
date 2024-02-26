# @title Block
import struct

class Block:
  def __init__(self, block_size, record_size):
    self.records = []
    self.block_size = block_size
    self.record_size = record_size
    self.capacity = (block_size-2) // record_size #two bytes are used to store the number or records

  # creates a block from a bytearray
  def create(block_size, record_size, byte_array, Record):
    block = Block(block_size, record_size)

    num_records = struct.unpack('>H', byte_array[:2])[0]
    pos = 2
    for _ in range(num_records):
      rec = Record.create(byte_array[pos:pos+record_size] )
      block.add(rec)
      pos += record_size

    return block

  def add(self, record):
    if(self.size() < self.capacity):
      self.records.append(record)
    else:
      raise ValueError("The block is full!")

  def addIndex(self, index, record):
    if(self.size() < self.capacity):
      self.records.insert(index, record)
    else:
      raise ValueError("The block is full!")

  def remove(self, keyPos, keyValue):
    if(not isinstance(keyPos, int)):
       raise TypeError(f"The keyPos must be an int!")

    rec = self.search(keyPos, keyValue)
    if(rec):
      return self.records.remove(rec)
    return None

  def removeIndex(self, index):
    if(not isinstance(index, int)):
       raise TypeError(f"The index must be int!")
    return self.records.pop(index)

  def removeLast(self):
    if len(self.records)>0:
      return self.records.pop()
    return None

  def read(self):
    str=""
    for rec in self.records:
      str += f"{rec.read()}\n"
    return str;

  #returns the position of the record within the block
  def search(self, keyPos, keyValue):
    if(not isinstance(keyPos, int)):
       raise TypeError(f"The key must be an int!")

    for i in range(len(self.records)):
      if(self.getRecord(i).read()[keyPos]==keyValue):
        return i
    return -1

  # returns the list of records, within the range keyA (inclusive) and KeyB (exclusive)
  def rangeSearch(self, keyPos, keyValueA, keyValueB):
    if(not isinstance(keyPos, int)):
       raise TypeError(f"The keyPos must be an int!")

    ret = []
    for rec in self.records:
      recValue = rec.read()[keyPos]
      if(recValue>=keyValueA and recValue<keyValueB):
        ret.append(rec)
    return ret

  def getRecord(self, index):
    return self.records[index]

  def getFirtRecord(self):
    return self.records[0]

  def getLastRecord(self):
    return self.records[-1]

  def size(self):
    return len(self.records)

  def isFull(self):
    return self.size()==self.capacity

  def isEmpty(self):
    return self.size()==0

  def bytes(self):
    byte_array = bytearray([0] * self.block_size)

    byte_array[:2] = struct.pack('>H', self.size()) #pack int into two bytes
    pos = 2
    for rec in self.records:
      byte_array[pos:pos+rec.size()] = rec.bytes()
      pos += rec.size()

    return byte_array

  
dataBlock = Block(4096, 267)
print(f"block capacity: {dataBlock.capacity}")
print(f"block size: {dataBlock.size()}")

dataBlock.add(DataEntry("Id-1", "Title-1", "UserId-1", "ProfileName-1", "5/7", 5.0, 940636700, "summary-1", "text-1"))
dataBlock.add(DataEntry("Id-2", "Title-2", "UserId-2", "ProfileName-2", "6/8", 4.0, 940636600, "summary-2", "text-2"))
dataBlock.add(DataEntry("Id-3", "Title-3", "UserId-3", "ProfileName-3", "9/10", 3.0, 940636400, "summary-3", "text-2"))


print(dataBlock.read())

print(f"getRecord(1): {dataBlock.getRecord(1)}")
print(f"search(1,'Title-2'):{dataBlock.search(1,'Title-2')}")
print(f"range search(5, 2.0, 4.5):")
for rec in dataBlock.rangeSearch(5, 2.0, 4.5):
  print(rec)
print(f"block bytes: {dataBlock.bytes()}")

block2 = Block.create(4096, 267, dataBlock.bytes(), DataEntry)
print(block2.read())