# coding: utf-8


# バイナリファイルをCMTファイルに変換するスクリプト
# VERSION:1.0
# DATE:2023/10/22
# AUTHER:chiqlappe
# USAGE: python3 bin2cmt.py <binary file> <cmt file> <start address>


import argparse	# https://docs.python.org/ja/3/howto/argparse.html?highlight=argparse
import operator # operator.neg()
import os # os.path.isfile()

MARKER = 0x3A
FOOTER = [MARKER,0x00,0x00]

parser = argparse.ArgumentParser()
parser.add_argument("address", help="Start address 0000~FFFF")
parser.add_argument("binfile", help="Binary file name")
parser.add_argument("cmtfile", help="CMT file name")
args = parser.parse_args()

print(args.binfile,"->",args.cmtfile);

if os.path.isfile(args.binfile):

	r = open(args.binfile,'rb')
	w = open(args.cmtfile,'wb')
	
	adr = int(args.address,16);
	hi = int(adr / 256)
	lo = int(adr % 256)
	csum = operator.neg(hi+lo) % 256
	header = [MARKER,hi,lo,csum]
	w.write(bytearray(header))
	
	while True:
		b = r.read(255)
		size = len(b)
		sum = size
	
		if size == 0:
			break
	
		header = [MARKER,size]
		w.write(bytearray(header))
	
		ba = bytearray(b)
		for n in ba:
			sum += n
	
		csum = operator.neg(sum) % 256
		ba.append(csum)
		w.write(ba)
	
	w.write(bytearray(FOOTER))
	
	r.close()
	w.close()

	print("Done.")

else :

	print(args.binfile,"is not found.");

