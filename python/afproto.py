from crc8 import Crc8

import struct

start_byte = 0xA3
escape_byte = 0x85
end_byte = 0x59

crcer = Crc8()

def extract_payload(data):
	# Find start_ndx
	start_ndx = 0
	while start_ndx >= 0:
		start_ndx = data.find(chr(start_byte), start_ndx)
		if start_ndx >= 0:
			if start_ndx > 0 and data[start_ndx-1] != chr(escape_byte):
				break
			elif start_ndx == 0:
				break
		start_ndx += 1

	# If no start found trash data
	if start_ndx == -1:
		return None, ''

	# Not a full message
	if len(data) < start_ndx + 4:
		return None, data[start_ndx:]
	length, crc = struct.unpack('BB', data[start_ndx+1:start_ndx+3])

	print length, crc

	# Check end byte
	end_ndx = start_ndx + length + 3
	if data[end_ndx] != chr(end_byte) or data[end_ndx-1] == chr(escape_byte):
		return None, data[start_ndx:]

	payload = data[start_ndx+3:end_ndx]
	
	if crc == crcer.digest(payload):
		return payload, data[end_ndx+1:]

	return None, data[end_ndx+1:]

if __name__=='__main__':
	print extract_payload("\xa3\x05\xeb\x48\x65\x6c\x6c\x6f\x59")

