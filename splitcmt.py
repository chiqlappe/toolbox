# coding: utf-8


# 結合されたCMTファイルを分割するスクリプト
# VERSION:1.0
# DATE:2023/10/24
# AUTHER:chiqlappe
# USAGE: python3 splitcmt.py <cmt file>


import argparse	# https://docs.python.org/ja/3/howto/argparse.html?highlight=argparse
import os # os.path.isfile()

BIN_MARKER = 0x3A
BAS_MARKER = 0xD3

parser = argparse.ArgumentParser()
parser.add_argument("cmtfile", help="CMT file name")
args = parser.parse_args()

print ("File name =",args.cmtfile)

if os.path.isfile(args.cmtfile):

	serial = 1 # 出力ファイルの通し番号
	r = open(args.cmtfile,'rb')

	file = bytearray(r.read())
	size = len(file)
	print ("File size =",hex(size))

	fp = 0 # ファイルポインタ
	error_flag = False

	while fp < size :
		b = file[fp]
		if b == BAS_MARKER :
			start_fp = fp
#			print("start fp :",start_fp)
			fp = fp + 10
			name = [0] * 6
			for j in range(6) :
				name[j] = chr(file[fp])
				fp = fp + 1
			basic_name = "".join(name)
			print("BASIC ",basic_name)
			while True :
				if (file[fp] == 0x00 and file[fp+1] == 0x00 and file[fp+2] == 0x00) :
					break
				else :
					fp = fp + 1
			fp = fp + 12
			end_fp = fp - 1
#			print("end fp :",end_fp)
#			print("BASIC  END")
			w = open(str(serial)+"_bas_"+args.cmtfile,'wb')
			w.write(file[start_fp:end_fp])
			w.close()
			serial = serial + 1

		elif b == BIN_MARKER :
			start_fp = fp
			start_address = hex(file[fp+1]*256+file[fp+2]) 
#			print("start fp :",start_fp)
			print("BINARY",start_address)
			fp = fp + 4 # 次のマーカーまで進める
			while True :
				if file[fp] == BIN_MARKER :
					fp = fp + 1
					blocksize = file[fp]
					fp = fp + 2 # check sum
					if blocksize == 0 :
						end_fp = fp-1
#						print("end fp :",end_fp)
#						print("BINARY END")
						w = open(str(serial)+"_bin_"+start_address+"_"+args.cmtfile,'wb')
						w.write(file[start_fp:end_fp])
						w.close()
						serial = serial + 1
						break
					else :
						fp = fp + blocksize
					
				else :
					print("CMT FILE FORMAT ERROR");
					error_flag = True
					break

		else :
			fp = fp + 1

		if error_flag :
			break

	r.close()

	print("Done.")

else :

	print(args.cmtfile,"is not found.")

