#!/usr/bin/python 
from ctypes import *
import sys

DISK_SIZE = 0x400

def castStrcture(buf, start, cast_type):
	stream = (c_char * sizeof(cast_type))()
	stream.raw = buf[start:start+sizeof(cast_type)]
	temp = cast(stream, POINTER(cast_type))
	return (temp.contents, sizeof(cast_type))

def parseSuper(buf, offset):
	class SUPER_BLOCK(Structure):
		_pack_ = 1
		_fields_ = [
				("inodes",c_ushort),
				("zones",c_ushort),
				("imap_blocks",c_ushort),
				("zmap_blocks",c_ushort),
				("firstdata",c_ushort),
				("log_size",c_ushort),
				("max_size",c_uint),
				("magic",c_ushort),
		]

	(sb,dist) = castStrcture(buf, offset, SUPER_BLOCK)
   	offset += dist

	libc = CDLL("libc.so.6")

   	libc.printf("inode number = 0x%x\n", sb.inodes)
   	libc.printf("inode addr = 0x%x\n", DISK_SIZE * (2+sb.imap_blocks+sb.zmap_blocks))
   	libc.printf("inode map blocks = 0x%x, addr = 0x%x\n", sb.imap_blocks, DISK_SIZE * 2)
   	libc.printf("zone map blocks = 0x%x, addr = 0x%x\n", sb.zmap_blocks, DISK_SIZE * (2+sb.imap_blocks))
   	libc.printf("1st zone block addr = 0x%x\n", DISK_SIZE * sb.firstdata)
   	libc.printf("zone number = 0x%x\n", sb.zones)
   	libc.printf("log size = 0x%x\n", sb.log_size)
   	libc.printf("max file size = 0x%x\n", sb.max_size)
   	libc.printf("magic = 0x%x\n", sb.magic)
   	return offset

def analyzeFileSystem(filename):
	offset = 0x400

	# open root filesystem image
	fd = open("%s" %  filename, "rb")
	stream = fd.read()
	fd.close()

	#parse super block
	offset = parseSuper(stream, offset)

if __name__ == "__main__":
	analyzeFileSystem(sys.argv[1])
