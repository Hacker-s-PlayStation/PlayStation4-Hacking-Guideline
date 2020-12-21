import os
import struct
from pwn import *
import sys
import lief
from ps4elf import *
import csv
import numpy as np
import struct
### get nid table

try :
    target = open(sys.argv[1], "rb")
except :
    print("argv[1] / file is not found")
    exit(0)

c = open("aerolib.csv")

nids_dict = dict(row for row in csv.reader(c, delimiter=' '))


class BUILDER:
    def __init__(self):
        self.MAGIC = b"\x7fELF"
        self.CLASS = p8(2)
        self.DATA = p8(1)
        self.VERSION = p8(1)
        self.OS = p8(1)
        self.abiversion = p8(0)
        self.padding = b"\x00"*7
        self.size = p8(0)

        self.type = 3
        self.MACHINE = 0x3e
        self.version = 1
        self.ENTRY_point = 0
        self.PHT_OFFSET = 64
        self.SHT_OFFSET = 0
        self.FLAGS = 0
        self.SIZE = 64
        self.PHT_SIZE = 56
        self.PHT_COUNT = 0
        self.SHT_SIZE = 64
        self.SHT_COUNT = 6
        self.SHT_INDEX = 2
    def write(self):
        elf = b""
        elf += self.MAGIC
        elf += self.CLASS
        elf += self.VERSION
        elf += self.OS
        elf += self.abiversion
        elf += self.padding
        elf += self.size
        elf += p16(self.type)
        elf += p16(self.MACHINE)
        elf += p32(self.version)
        elf += p64(self.ENTRY_point)
        elf += p64(self.PHT_OFFSET)
        elf += p64(self.SHT_OFFSET)
        elf += p32(self.FLAGS)
        elf += p16(self.SIZE)
        elf += p16(self.PHT_SIZE)
        elf += p16(self.PHT_COUNT)
        elf += p16(self.SHT_SIZE)
        elf += p16(self.SHT_COUNT)
        elf += p16(self.SHT_INDEX)
        return elf

stype = lief.ELF.SEGMENT_TYPES


def set_segment(seg, etype, flags, offset, physical_addr, physical_size, file_addr, file_size, alignment, flag = 0):
    seg.type = etype
    seg.file_offset = offset
    seg.physical_address = physical_addr
    seg.physical_size = physical_size
    seg.virtual_address = file_addr
    seg.virtual_size = file_size
    seg.alignment = alignment

    seg.add(lief.ELF.SEGMENT_FLAGS.R)
    seg.add(lief.ELF.SEGMENT_FLAGS.W)
    if(flag):
        seg.add(lief.ELF.SEGMENT_FLAGS.X)
    return seg

def search_entry(dynamic_entries, tag):
    for i in dynamic_entries:
        if(tag == i.TAG):
            return i.VALUE

def set_dynamic_entry(buf, dynamic_offset, tag, value):
    tag = p64(tag)
    value = p64(value)
    for i in range(8):
        dynamic_offset += 1
        buf[dynamic_offset] = tag[i]
    for i in range(8):
        dynamic_offset += 1
        buf[dynamic_offset] = value[i]

segment_type = {
    0 : stype.NULL,
    1 : stype.LOAD,
    2 : stype.NULL,
    3 : stype.INTERP,
    4 : stype.NOTE,
    5 : stype.SHLIB,
    6 : stype.PHDR,
    7 : stype.TLS,
    0x61000000 : stype.DYNAMIC,
    0x6474E550 : stype.GNU_EH_FRAME,
    0x6FFFFF01 : stype.NULL,
    0x61000010 : stype.LOAD,
    0x61000002 : stype.LOAD
}

def set_section(sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_size, sh_link, sh_info, sh_addralign, sh_entsize):
    with open("./complete_output_", "ab") as f:
        f.write(p32(sh_name))
        f.write(p32(sh_type))
        f.write(p64(sh_flags))
        f.write(p64(sh_addr))
        f.write(p64(sh_offset))
        f.write(p64(sh_size))
        f.write(p32(sh_link))
        f.write(p32(sh_info))
        f.write(p64(sh_addralign))
        f.write(p64(sh_entsize))

build = BUILDER()
a = build.write()
f = open("output", "wb")
f.write(a)
f.close()
binary = lief.parse("output")
ps4 = Binary(target)


for i in range(len(ps4.E_SEGMENTS)): # skip uselsess segment
    binary.add((lief.ELF.Segment()))


counter = 0
tmp = binary.segments[counter]
tmp = set_segment(tmp, segment_type[1], 4, 0,0x8c000, 0xA00, 0x8c000, 0xA00, 0x1000) 
counter += 1
type_list = [1, 0x61000000,0x61000010,0x6100002]
code_size = 0
dynamic_size = 0

for i in ps4.E_SEGMENTS:


    if(i.TYPE==2):
            ################################################################################
        target.seek(i.OFFSET)
        dynamic_size = i.MEM_SIZE


    if(i.TYPE not in type_list):
        continue
    if(counter == 1):
        code_offset = i.OFFSET
        real_code_size = i.FILE_SIZE
        flag = 1
    else:
        flag = 0
    if(counter <=5):
        code_size += i.FILE_SIZE

    if(i.TYPE == 0x61000000): # if dynamic segment
        tmp = binary.segments[counter-1]
        alloc = tmp.file_offset + 0x4000
        i.MEM_ADDR = alloc + 0x1000000
        i.FILE_ADDR = alloc + 0x1000000
        i.MEM_SIZE = i.FILE_SIZE
        tmp = binary.segments[counter]
        tmp = set_segment(tmp, segment_type[i.TYPE], i.FLAGS, alloc,i.MEM_ADDR, 0x1000, i.FILE_ADDR, 0x1000, i.ALIGNMENT)
        counter += 1    
        data = binary.segments[counter - 3]
        ################################################################################
        dynamic_offset = i.OFFSET
        ############################################################################
        continue

        ############################################################################
    if(i.FILE_SIZE != i.MEM_SIZE):
        i.FILE_SIZE = i.MEM_SIZE


    tmp = binary.segments[counter]
    tmp = set_segment(tmp, segment_type[i.TYPE], i.FLAGS, i.OFFSET,i.MEM_ADDR, i.MEM_SIZE, i.FILE_ADDR, i.FILE_SIZE, i.ALIGNMENT,flag)
    counter += 1

tmp = binary.segments[counter]
tmp = set_segment(tmp, segment_type[1], i.FLAGS, alloc,alloc+0x1000000, 0x101b0, alloc+0x1000000, 0x101b0, 0x1000)

binary.write("complete")

offset_to_read = (data.virtual_address + data.virtual_size) - (code_offset)# offset to read for copy data(string, code...etc)
dynamic_list = []



###########################################################3

for i in range(round(dynamic_size/0x10)):
    dynamic_list.append(Dynamic(target))


# get nid tables && offset ########################
str_size = 0
nid_offset = 0

str_size = search_entry(dynamic_list, 0x61000037)
strtab = search_entry(dynamic_list, 0x61000035) # get string table 
rela =search_entry(dynamic_list, 0x6100002f)
relasz = search_entry(dynamic_list, 0x61000031) 

target.seek(strtab+dynamic_offset)
nid = (target.read(str_size)).decode('utf-8')

rela_offset = rela + dynamic_offset
target.seek(rela_offset)
rela_data = target.read(relasz)


nid_offset = nid.find("#B#C")-11 # skip string like "libc.sprx .... etc"
nid = nid[nid_offset:]
nids = nid.split("\x00")

string = []

for i in nids:
    try:
        s = nids_dict[i[:-4]]
        if(s == "Need_sceLibcInternal"):
            continue
        string.append(s)
    except:
        continue

####### get dynsym ########

dynsym_offset = search_entry(dynamic_list, 0x61000039) + dynamic_offset
dynsym_size = search_entry(dynamic_list, 0x6100003F) 

target.seek(dynsym_offset)
dynsym = target.read(dynsym_size)

###########################33

_strtab = alloc+0x1000

f = open("complete", "rb")
f2 = open("complete_output_", "wb")
buf = (f.read())
str_size = 1
buf = list(buf)

target.seek(code_offset)
code = list(target.read(code_size))

for i in range(len(code)):
    buf[code_offset + i] = code[i]

buf[_strtab] = 0

for i in string:
    for j in i:
        buf[_strtab + str_size] = ord(j)
        str_size += 1
    buf[_strtab+str_size] = 0
    str_size+=1

_symtab = ((_strtab + str_size + 16+0x100) >> 4) << 4

strtab = bytes(buf[_strtab:_strtab + str_size]).decode('utf-8')

set_dynamic_entry(buf, alloc-1, 5, _strtab+0x1000000) # set DT_STRTAB
set_dynamic_entry(buf, alloc-1+16, 0x6, 0x1000000+ _symtab) # set DT_SYMTAB
set_dynamic_entry(buf, alloc-1+32, 0xa, str_size) # set DT_STRSZ
set_dynamic_entry(buf, alloc-1+48, 0xb, 0x18) # set DT_SYMENT
set_dynamic_entry(buf, alloc-1+64, 0x6FFFFEF5, 0x8c000+ 0x500)
set_dynamic_entry(buf, alloc-1+80, 0x7, rela_offset+0x1000000 + 0x8000)
set_dynamic_entry(buf, alloc-1+96, 0x8, relasz)
set_dynamic_entry(buf, alloc-1+96+16, 24, 0)
set_dynamic_entry(buf, alloc-1+96+16+16, 9, 24)
symbol_table = []
# get symtab


for i in range(0, round(dynsym_size/24)):
    tmp = []
    symbol = dynsym[24*i:24*i+24]
    string_index = u32(symbol[:4])
    info = symbol[4]
    dummy = (symbol[5])
    t = u16(symbol[6:8])
    offset = u64(symbol[8:16])
    size = u64(symbol[16:24])
    tmp.append(string_index)
    tmp.append(info)
    tmp.append(dummy)
    tmp.append(t)
    tmp.append(offset)
    tmp.append(size)

    symbol_table.append(tmp)


_symtab_ = _symtab
############## add symbol table ##################
for i in range(round(dynsym_size/24)):
    idx = symbol_table[i][0] # nid offset from strtab
    nid = nids[round(idx/0x10)]
    if("module" in nid):
        break
    if(symbol_table[i][1] == 0x11 or symbol_table[i][1] == 0x3 or symbol_table[i][1] == 0):
        continue
    func = (nids_dict[nid[:-4]])
    idx = strtab.find((func))
    data = p32(idx) + p8(symbol_table[i][1]) + p8(symbol_table[i][2]) + p16(5) + p64(symbol_table[i][4]) + p64(symbol_table[i][5])
    data = list(data)

    for j in range(24):
        buf[_symtab + j] = data[j]
    _symtab += 24


########### add relocation table #############

for i in range(round(relasz/24)):
    r = rela_data[24*i:24*i+24]
    offset_ = r[:8]
    info = u64(r[8:16])
    addend = r[16:24]
    if(info > 8):
        info = 8
    data = offset_ + p64(info) + addend
    for j in range(24):
        buf[rela_offset + j + 0x8000] = data[j]
    rela_offset += 24

f2.write(bytes(buf))
f.close()
f2.close()

######### add Section hedaer ##############

with open("./complete_output_", "a") as f :
    file_len = f.tell() - 0x1b0
file_read = open("./complete_output_", "rb")
save = file_read.read(0x28)

# Change section header offset
save += p64(file_len+0x30)
file_read.seek(0x30)
save += file_read.read()
file_read.close()

file_new = open("./complete_output_", "wb+")
file_new.write(save[:-0x1b0])
file_new.write(b"\x00\x2E\x73\x68\x73\x74\x72\x6E\x64\x78\x00\x2E\x64\x79\x6E\x61\x6D\x69\x63\x00\x2E\x64\x79\x6E\x73\x74\x72\x00\x2E\x64\x79\x6E\x73\x79\x6D\x00\x2E\x74\x65\x78\x74\x00\x00\x00\x00\x00\x00\x00")
file_new.close()

set_section(0,0,0,0,0,0,0,0,0,0)
set_section(0x14,3,2,0x1000000+_strtab,_strtab,str_size,0,0,1,0)
set_section(1,3,0,0,file_len,0x30,0,0,1,0)
set_section(0xb,6,3,0x1000000+file_len-0x10000,file_len-0x10000,dynamic_size,1,0,8,16)
set_section(0x1c,0xb,2,0x1000000+_symtab_,_symtab_,_symtab - _symtab_,1,2,8,0x18)
set_section(0x24,1,6,0,0x4000,real_code_size,0,0,0x10,0)

os.remove("output")
os.remove("complete")
print("Done!")
