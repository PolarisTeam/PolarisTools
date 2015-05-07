# -*- coding: utf-8 -*-

import struct
import binascii
import glob

def hexStr(s):
	return binascii.hexlify(s)


u32 = struct.Struct('<I')
u16 = struct.Struct('<H')
u8 = struct.Struct('<B')

class PacketReader(object):
	def __init__(self, data):
		self.data = data
		self.pos = 0

	def read(self, count):
		data = self.data[self.pos:self.pos+count]
		self.pos += count
		return data

	def readU8(self):
		value = u8.unpack_from(self.data, self.pos)[0]
		self.pos += 1
		return value

	def readU16(self):
		value = u16.unpack_from(self.data, self.pos)[0]
		self.pos += 2
		return value

	def readU32(self):
		value = u32.unpack_from(self.data, self.pos)[0]
		self.pos += 4
		return value

	def readHeader(self):
		size, type, subtype, flags = \
				struct.unpack_from('<IBBBx', self.data, self.pos)
		self.pos += 8
		return size, type, subtype, flags

	def readEntityHeader(self):
		playerID, _4, _8, _A = \
				struct.unpack_from('<IIHH', self.data, self.pos)
		self.pos += 12
		return playerID, _4, _8, _A

	def readString(self, xorVal, subVal):
		rawLength = self.readU32()
		length = (rawLength ^ xorVal) - subVal
		data = self.data[self.pos:self.pos+(length*2)]

		self.pos += (length * 2)
		if (self.pos & 3) > 0:
			self.pos = (self.pos & ~3) + 4

		data = data.decode('utf-16')
		if data and data[-1] == '\0':
			return data[:-1]
		else:
			return data


	def readStringASCII(self, xorVal, subVal):
		rawLength = self.readU32()
		length = (rawLength ^ xorVal) - subVal
		data = self.data[self.pos:self.pos+(length)]

		self.pos += (length)
		if (self.pos & 3) > 0:
			self.pos = (self.pos & ~3) + 4

		data = data.decode('utf-8')
		if data and data[-1] == '\0':
			return data[:-1]
		else:
			return data

	def readFixedLengthASCII(self, length):
		return self.read(length).rstrip('\0')


def readCharInfoPacket(packet):
	reader = PacketReader(packet)

	print('Packet Header: ' + repr(reader.readHeader()))
	print('Player Header: ' + repr(reader.readEntityHeader()))
	print('Name		 : ' + repr(reader.readString(0x5533, 1)))
	print('field_28	 : ' + hexStr(reader.read(8)))
	print('field_30	 : ' + hexStr(reader.read(4)))

	someCount = (reader.readU32() ^ 0x5533) - 1
	print('SomeCount	: ' + repr(someCount))

	for i in range(someCount):
		block = reader.read(56)
		print('[%02d] %s' % (i, hexStr(block)))

	print('Position: %d / End: %d' % (reader.pos, len(packet)))


def readChatPacket0(packet):
	reader = PacketReader(packet)

	print('Packet Header: ' + repr(reader.readHeader()))
	print('Player Header: ' + repr(reader.readEntityHeader()))
	print('field_14	 : ' + repr(reader.readU8()))
	print('field_15	 : ' + repr(reader.readU8()))
	print('field_16	 : ' + repr(reader.readU16()))
	print('Text		 : ' + repr(reader.readString(0x9D3F, 0x44)))


def readChatPacket11(packet):
	reader = PacketReader(packet)

	print('Packet Header: ' + repr(reader.readHeader()))
	print('Player Header: ' + repr(reader.readEntityHeader()))
	print('field_14	 : ' + repr(reader.readU32()))
	print('Text		 : ' + repr(reader.readString(0x7ED7, 0x41)))
	print('Text		 : ' + repr(reader.readString(0x7ED7, 0x41)))
	print('Text		 : ' + repr(reader.readString(0x7ED7, 0x41)))


def readChatPacket12(packet):
	reader = PacketReader(packet)

	print('Packet Header: ' + repr(reader.readHeader()))
	print('Player Header: ' + repr(reader.readEntityHeader()))
	print('field_14	 : ' + repr(reader.readU8()))
	print('field_15	 : ' + repr(reader.readU8()))
	print('field_16	 : ' + repr(reader.readU16()))
	print('Text		 : ' + repr(reader.readString(0x495, 0x8C)))
	print('field_2C	 : ' + hexStr(reader.read(12)))


def readChatPacket13(packet):
	reader = PacketReader(packet)

	print('Packet Header: ' + repr(reader.readHeader()))
	print('Player Header: ' + repr(reader.readEntityHeader()))
	print('field_14	 : ' + repr(reader.readU8()))
	print('field_15	 : ' + repr(reader.readU8()))
	print('field_16	 : ' + repr(reader.readU16()))
	print('Text		 : ' + repr(reader.readString(0x8A53, 0xD7)))
	print('Text		 : ' + repr(reader.readString(0x8A53, 0xD7)))
	print('Text		 : ' + repr(reader.readString(0x8A53, 0xD7)))
	print('field_54	 : ' + hexStr(reader.read(12)))


def readLoginPacket(packet):
	reader = PacketReader(packet)

	print('Packet Header: ' + repr(reader.readHeader()))
	print('Username	 : ' + repr(reader.readFixedLengthASCII(64)))
	nukeme = reader.readFixedLengthASCII(64)
	print('Password	 : [elided]')
	print('????		 : ' + hexStr(reader.read(4)))
	print('????		 : ' + repr(reader.readU8()))
	print('????		 : ' + repr(reader.readU8()))
	print('????		 : ' + repr(reader.readU16()))
	print('????		 : ' + repr(reader.readU32()))
	print('????		 : ' + repr(reader.readU32()))
	print('????		 : ' + hexStr(reader.read(32)))

	thingCount = (reader.readU32() ^ 0x5E6) - 107
	print('Thing Count  : ' + repr(thingCount))
	for i in range(thingCount):
		print('[%02d] %s' % (i, hexStr(reader.read(28))))

	print('????		 : ' + hexStr(reader.read(16)))
	print('????		 : ' + hexStr(reader.read(4)))
	print('????		 : ' + hexStr(reader.read(16)))
	print('????		 : ' + hexStr(reader.read(16)))
	print('????		 : ' + hexStr(reader.read(16)))
	print('????		 : ' + hexStr(reader.read(16)))
	print('????		 : ' + hexStr(reader.read(16)))
	print('????		 : ' + hexStr(reader.read(4)))
	print('????		 : ' + hexStr(reader.read(4)))
	print('????		 : ' + hexStr(reader.read(4)))
	print('????		 : ' + hexStr(reader.read(32)))
	print('????		 : ' + hexStr(reader.read(4)))
	print('????		 : ' + hexStr(reader.read(4)))
	print('????		 : ' + hexStr(reader.read(4)))
	print('????		 : ' + hexStr(reader.read(32)))
	print('????		 : ' + hexStr(reader.read(4)))
	print('????		 : ' + hexStr(reader.read(16)))
	print('????		 : ' + hexStr(reader.read(32)))
	print('????		 : ' + hexStr(reader.read(4)))

def readSetAreaPacket(packet):
	reader = PacketReader(packet)

	print('Packet Header :' + repr(reader.readHeader()))
	print('????	Entity:' + repr(reader.readEntityHeader()))
	print('Host Entity   :' + repr(reader.readEntityHeader()))
	# 12 DWORDs
	print('????		  :' + repr(reader.readU32()))
	print('????		  :' + repr(reader.readU32()))
	print('????		  :' + repr(reader.readU32()))
	print('????		  :' + repr(reader.readU32()))
	print('????		  :' + repr(reader.readU32()))
	print('????		  :' + repr(reader.readU32()))
	print('????		  :' + repr(reader.readU32()))
	print('????		  :' + repr(reader.readU32()))
	print('????		  :' + repr(reader.readU32()))
	print('????		  :' + repr(reader.readU32()))
	print('????		  :' + repr(reader.readU32()))
	print('????		  :' + repr(reader.readU32()))
	# BYTE, BYTE, WORD
	print('????		  :' + repr(reader.readU8()))
	print('????		  :' + repr(reader.readU8()))
	print('????		  :' + repr(reader.readU16()))
	# Three of these
	print('????	Entity:' + repr(reader.readEntityHeader()))
	print('????	Entity:' + repr(reader.readEntityHeader()))
	print('????	Entity:' + repr(reader.readEntityHeader()))
	# Area name
	print('AreaName	  :' + reader.readStringASCII(0x7542, 0x5E))


	# Things
	thingCount = (reader.readU32() ^ 0x7542) - 0x5E
	print('Thing Count 1 : ' + repr(thingCount))
	for i in range(thingCount):
		print('[%02d] %s' % (i, hexStr(reader.read(52)))) # 52 Byte object, ctor is setAreaThing_ctor() in idb

	thingCount = (reader.readU32() ^ 0x7542) - 0x5E
	print('Thing Count 2: ' + repr(thingCount))
	for i in range(thingCount):
		print('[%02d] %s' % (i, hexStr(reader.read(20)))) # 20 Byte object, ctor is YetAnotherObject_ctor() in idb

	thingCount = (reader.readU32() ^ 0x7542) - 0x5E
	print('Thing Count 3: ' + repr(thingCount))
	for i in range(thingCount):
		print('[%02d] %s' % (i, hexStr(reader.read(8)))) # 8 Byte object, ctor is HowManyObjectsDoesThisPacketHave_ctor() in idb

	thingCount = (reader.readU32() ^ 0x7542) - 0x5E
	print('Thing Count 4: ' + repr(thingCount))
	for i in range(thingCount):
		print('[%02d] %s' % (i, hexStr(reader.read(136)))) # 136 Byte object, ctor is YetAnotherStupidObject_ctor() in idb

	thingCount = (reader.readU32() ^ 0x7542) - 0x5E
	print('Thing Count 5: ' + repr(thingCount))
	for i in range(thingCount):
		print('[%02d] %s' % (i, hexStr(reader.read(224)))) # 224 Byte object, ctor is sub_7D8120() in idb

	thingCount = (reader.readU32() ^ 0x7542) - 0x5E
	print('Thing Count 6: ' + repr(thingCount))
	for i in range(thingCount):
		print('[%02d] %s' % (i, hexStr(reader.read(156)))) # 156 Byte object, ctor is sub_593180() in idb

	thingCount = (reader.readU32() ^ 0x7542) - 0x5E
	print('Thing Count 7: ' + repr(thingCount))
	for i in range(thingCount):
		print('[%02d] %s' % (i, hexStr(reader.read(224)))) # 224 Byte object, ctor is sub_7D6E30() in idb [maybe contains inline array?]

	thingCount = (reader.readU32() ^ 0x7542) - 0x5E
	print('Thing Count 8: ' + repr(thingCount))
	for i in range(thingCount):
		print('[%02d] %s' % (i, hexStr(reader.read(164)))) # 164 Byte object, ctor is sub_5931A0() in idb [maybe contains inline array?]

	thingCount = (reader.readU32() ^ 0x7542) - 0x5E
	print('Thing Count 9: ' + repr(thingCount))
	for i in range(thingCount):
		print('[%02d] %s' % (i, hexStr(reader.read(40)))) # 40 Byte object, ctor is inlined in idb

	# This should be at field_140 in RAM now (all arrays above take up 0x14 bytes in RAM when unpacked)
	print('????		  :' + repr(reader.readU32()))
	print('????		  :' + repr(reader.readU32()))
	# This is read by 60 bytes during unpack, may just be an optimazation though. (Contains MoreThing objects)
	print('????		  :' + hexStr(reader.read(60)))

	print('????		  :' + repr(reader.readU32()))
	# These are both read by 16 bytes, again may just be a optimazation
	print('????		  :' + hexStr(reader.read(16)))
	print('????		  :' + hexStr(reader.read(16)))

	thingCount = (reader.readU32() ^ 0x7542) - 0x5E
	print('Thing Count 10: ' + repr(thingCount))
	for i in range(thingCount):
		print('[%02d] %s' % (i, hexStr(reader.read(4)))) # 4 Byte object, ctor is AnotherDamnObject_ctor() in idb

	print('????		  :' + hexStr(reader.read(512))) # This is read as 512 bytes fixed; iirc in the ctor it was a bunch of dwords.

	thingCount = (reader.readU32() ^ 0x7542) - 0x5E
	print('Thing Count 11: ' + repr(thingCount))
	for i in range(thingCount):
		print('[%02d] %s' % (i, hexStr(reader.read(8)))) # 8 Byte object, ctor is HowManyObjectsDoesThisPacketHave_ctor() in idb

	print('????Str	   :' + repr(reader.readStringASCII(0x7542, 0x5E)))
	print('????Str	   :' + repr(reader.readStringASCII(0x7542, 0x5E)))

	# 8 bytes? Not an object? ¯\_(ツ)_/¯
	print('????		  :' + hexStr(reader.read(8)))
	print('????		  :' + hexStr(reader.read(8)))

	print('????		  :' + repr(reader.readU8()))
	print('????		  :' + repr(reader.readU8()))
	print('????		  :' + repr(reader.readU8()))
	print('????		  :' + repr(reader.readU8()))

	print('????		  :' + repr(reader.readU32()))

	print('????		  :' + hexStr(reader.read(12)))

	print('????		  :' + repr(reader.readU32()))
	print('????		  :' + repr(reader.readU32()))
	print('????		  :' + repr(reader.readU32()))

	print('????		  :' + repr(reader.readU8()))
	print('????		  :' + repr(reader.readU8()))
	print('????		  :' + repr(reader.readU8()))
	print('????		  :' + repr(reader.readU8()))
	print('????		  :' + repr(reader.readU8()))
	print('????		  :' + repr(reader.readU8()))
	print('????		  :' + repr(reader.readU8()))
	print('????		  :' + repr(reader.readU8()))
	print('????		  :' + repr(reader.readU8()))
	print('????		  :' + repr(reader.readU8()))
	print('????		  :' + repr(reader.readU8()))
	print('????		  :' + repr(reader.readU8()))

	print('Finished at %i' % reader.pos)

	print('')


for name in glob.iglob('./*.3-24.*.bin'):
	print('[[ %s ]]' % name)
	with open(name, 'rb') as f:
		readSetAreaPacket(f.read())
#
#
#for name in glob.iglob('packets3/*.7-0.*.bin'):
#	print('[[ %s ]]' % name)
#	with open(name, 'rb') as f:
#		readChatPacket0(f.read())
#
#for name in glob.iglob('packets3/*.7-11.*.bin'):
#	print('[[ %s ]]' % name)
#	with open(name, 'rb') as f:
#		readChatPacket11(f.read())
#
#for name in glob.iglob('packets3/*.7-12.*.bin'):
#	print('[[ %s ]]' % name)
#	with open(name, 'rb') as f:
#		readChatPacket12(f.read())
#
#for name in glob.iglob('packets3/*.7-13.*.bin'):
#	print('[[ %s ]]' % name)
#	with open(name, 'rb') as f:
#		readChatPacket13(f.read())
#
#for name in glob.iglob('packets3/*.11-0.*.bin'):
#	print('[[ %s ]]' % name)
#	with open(name, 'rb') as f:
#		readLoginPacket(f.read())
#
