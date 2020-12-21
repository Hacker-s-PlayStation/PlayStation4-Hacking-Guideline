import shutil
import struct



class Binary:

    __slots__ = ('EI_MAGIC', 'EI_CLASS', 'EI_DATA', 'EI_VERSION',
                 'EI_OSABI', 'EI_PADDING', 'EI_ABIVERSION', 'EI_SIZE',
                 'E_TYPE', 'E_MACHINE', 'E_VERSION', 'E_START_ADDR',
                 'E_PHT_OFFSET', 'E_SHT_OFFSET', 'E_FLAGS', 'E_SIZE',
                 'E_PHT_SIZE', 'E_PHT_COUNT', 'E_SHT_SIZE', 'E_SHT_COUNT',
                 'E_SHT_INDEX', 'E_SEGMENTS', 'E_SECTIONS')
    
    # Elf Types
    ET_NONE                   = 0x0
    ET_REL                    = 0x1
    ET_EXEC                   = 0x2
    ET_DYN                    = 0x3
    ET_CORE                   = 0x4
    ET_SCE_EXEC               = 0xFE00
    ET_SCE_REPLAY_EXEC        = 0xFE01
    ET_SCE_RELEXEC            = 0xFE04
    ET_SCE_STUBLIB            = 0xFE0C
    ET_SCE_DYNEXEC            = 0xFE10
    ET_SCE_DYNAMIC            = 0xFE18
    ET_LOPROC                 = 0xFF00
    ET_HIPROC                 = 0xFFFF
    
    # Elf Architecture
    EM_X86_64                 = 0x3E
    
    def __init__(self, f):
    
        f.seek(0)
        
        self.EI_MAGIC         = struct.unpack('4s', f.read(4))[0]
        self.EI_CLASS         = struct.unpack('<B', f.read(1))[0]
        self.EI_DATA          = struct.unpack('<B', f.read(1))[0]
        self.EI_VERSION       = struct.unpack('<B', f.read(1))[0]
        self.EI_OSABI         = struct.unpack('<B', f.read(1))[0]
        self.EI_ABIVERSION    = struct.unpack('<B', f.read(1))[0]
        self.EI_PADDING       = struct.unpack('6x', f.read(6))
        self.EI_SIZE          = struct.unpack('<B', f.read(1))[0]
        
        # Elf Properties
        self.E_TYPE           = struct.unpack('<H', f.read(2))[0]
        self.E_MACHINE        = struct.unpack('<H', f.read(2))[0]
        self.E_VERSION        = struct.unpack('<I', f.read(4))[0]
        self.E_START_ADDR     = struct.unpack('<Q', f.read(8))[0]
        self.E_PHT_OFFSET     = struct.unpack('<Q', f.read(8))[0]
        self.E_SHT_OFFSET     = struct.unpack('<Q', f.read(8))[0]
        self.E_FLAGS          = struct.unpack('<I', f.read(4))[0]
        self.E_SIZE           = struct.unpack('<H', f.read(2))[0]
        self.E_PHT_SIZE       = struct.unpack('<H', f.read(2))[0]
        self.E_PHT_COUNT      = struct.unpack('<H', f.read(2))[0]
        self.E_SHT_SIZE       = struct.unpack('<H', f.read(2))[0]
        self.E_SHT_COUNT      = struct.unpack('<H', f.read(2))[0]
        self.E_SHT_INDEX      = struct.unpack('<H', f.read(2))[0]
        
        # Prevent Other Binaries
        if self.E_MACHINE != Binary.EM_X86_64:
            return None
        
        f.seek(self.E_PHT_OFFSET)
        
        # Elf Program Header Table
        Binary.E_SEGMENTS = [Segment(f) for entry in range(self.E_PHT_COUNT)]
        
        f.seek(self.E_SHT_OFFSET)
        
        # Elf Section Header Table
        Binary.E_SECTIONS = [Section(f) for entry in range(self.E_SHT_COUNT)]
    
    def type(self):
    
        return {
            Binary.ET_NONE            : 'None',
            Binary.ET_REL             : 'Relocatable',
            Binary.ET_EXEC            : 'Executable',
            Binary.ET_DYN             : 'Shared Object',
            Binary.ET_CORE            : 'Core Dump',
            Binary.ET_SCE_EXEC        : 'Main Module',
            Binary.ET_SCE_REPLAY_EXEC : 'Replay Module',
            Binary.ET_SCE_RELEXEC     : 'Relocatable PRX',
            Binary.ET_SCE_STUBLIB     : 'SDK Stub Library',
            Binary.ET_SCE_DYNEXEC     : 'Main Module - ASLR',
            Binary.ET_SCE_DYNAMIC     : 'Shared Object PRX',
        }.get(self.E_TYPE, 'Missing Program Type!!!')



class Segment:

    __slots__ = ('TYPE', 'FLAGS', 'OFFSET', 'MEM_ADDR',
                 'FILE_ADDR', 'FILE_SIZE', 'MEM_SIZE', 'ALIGNMENT')
    
    # Segment Types
    PT_NULL                = 0x0
    PT_LOAD                = 0x1
    PT_DYNAMIC             = 0x2
    PT_INTERP              = 0x3
    PT_NOTE                = 0x4
    PT_SHLIB               = 0x5
    PT_PHDR                = 0x6
    PT_TLS                 = 0x7
    PT_NUM                 = 0x8
    PT_SCE_DYNLIBDATA      = 0x61000000
    PT_SCE_PROCPARAM       = 0x61000001
    PT_SCE_MODULEPARAM     = 0x61000002
    PT_SCE_RELRO           = 0x61000010
    PT_GNU_EH_FRAME        = 0x6474E550
    PT_GNU_STACK           = 0x6474E551
    PT_SCE_COMMENT         = 0x6FFFFF00
    PT_SCE_LIBVERSION      = 0x6FFFFF01
    PT_HIOS                = 0x6FFFFFFF
    PT_LOPROC              = 0x70000000
    PT_SCE_SEGSYM          = 0x700000A8
    PT_HIPROC              = 0x7FFFFFFF
    
    # Segment Alignments
    AL_NONE                = 0x0
    AL_BYTE                = 0x1
    AL_WORD                = 0x2
    AL_DWORD               = 0x4
    AL_QWORD               = 0x8
    AL_PARA                = 0x10
    AL_4K                  = 0x4000
    
    def __init__(self, f):
    
        self.TYPE      = struct.unpack('<I', f.read(4))[0]
        self.FLAGS     = struct.unpack('<I', f.read(4))[0]
        self.OFFSET    = struct.unpack('<Q', f.read(8))[0]
        self.MEM_ADDR  = struct.unpack('<Q', f.read(8))[0]
        self.FILE_ADDR = struct.unpack('<Q', f.read(8))[0]
        self.FILE_SIZE = struct.unpack('<Q', f.read(8))[0]
        self.MEM_SIZE  = struct.unpack('<Q', f.read(8))[0]
        self.ALIGNMENT = struct.unpack('<Q', f.read(8))[0]
    
    def alignment(self):
    
        return {
            Segment.AL_NONE            : saAbs,
            Segment.AL_BYTE            : saRelByte,
            Segment.AL_WORD            : saRelWord,
            Segment.AL_DWORD           : saRelDble,
            Segment.AL_QWORD           : saRelQword,
            Segment.AL_PARA            : saRelPara,
            Segment.AL_4K              : saRel4K,
        }.get(self.ALIGNMENT, saRel_MAX_ALIGN_CODE)
    
    def flags(self):
    
        return self.FLAGS & 0xF
    
    def name(self):
    
        return {
            Segment.PT_NULL            : 'NULL',
            Segment.PT_LOAD            : 'CODE',
            Segment.PT_DYNAMIC         : 'DYNAMIC',
            Segment.PT_INTERP          : 'INTERP',
            Segment.PT_NOTE            : 'NOTE',
            Segment.PT_SHLIB           : 'SHLIB',
            Segment.PT_PHDR            : 'PHDR',
            Segment.PT_TLS             : 'TLS',
            Segment.PT_NUM             : 'NUM',
            Segment.PT_SCE_DYNLIBDATA  : 'SCE_DYNLIBDATA',
            Segment.PT_SCE_PROCPARAM   : 'SCE_PROCPARAM',
            Segment.PT_SCE_MODULEPARAM : 'SCE_MODULEPARAM',
            Segment.PT_SCE_RELRO       : 'SCE_RELRO',
            Segment.PT_GNU_EH_FRAME    : 'GNU_EH_FRAME',
            Segment.PT_GNU_STACK       : 'GNU_STACK',
            Segment.PT_SCE_COMMENT     : 'SCE_COMMENT',
            Segment.PT_SCE_LIBVERSION  : 'SCE_LIBVERSION',
        }.get(self.TYPE, 'UNK')

    def type(self):
    
        return {
            Segment.PT_LOAD            : 'CODE' if self.flags() == (SEGPERM_EXEC | SEGPERM_READ) else 'DATA',
            Segment.PT_DYNAMIC         : 'DATA',
            Segment.PT_INTERP          : 'CONST',
            Segment.PT_NOTE            : 'CONST',
            Segment.PT_PHDR            : 'CODE',
            Segment.PT_TLS             : 'BSS',
            Segment.PT_SCE_DYNLIBDATA  : 'CONST',
            Segment.PT_SCE_PROCPARAM   : 'CONST',
            Segment.PT_SCE_MODULEPARAM : 'CONST',
            Segment.PT_SCE_RELRO       : 'DATA',
            Segment.PT_GNU_EH_FRAME    : 'CONST',
            Segment.PT_GNU_STACK       : 'DATA',
        }.get(self.TYPE, 'UNK')

class Section:
    
    __slots__ = ('NAME', 'TYPE', 'FLAGS', 'MEM_ADDR',
                 'OFFSET', 'FILE_SIZE', 'LINK', 'INFO',
                 'ALIGNMENT', 'FSE_SIZE')
    
    def __init__(self, f):
    
        self.NAME      = struct.unpack('<I', f.read(4))[0]
        self.TYPE      = struct.unpack('<I', f.read(4))[0]
        self.FLAGS     = struct.unpack('<Q', f.read(8))[0]
        self.MEM_ADDR  = struct.unpack('<Q', f.read(8))[0]
        self.OFFSET    = struct.unpack('<Q', f.read(8))[0]
        self.FILE_SIZE = struct.unpack('<Q', f.read(8))[0]
        self.LINK      = struct.unpack('<I', f.read(4))[0]
        self.INFO      = struct.unpack('<I', f.read(4))[0]
        self.ALIGNMENT = struct.unpack('<Q', f.read(8))[0]
        self.FSE_SIZE  = struct.unpack('<Q', f.read(8))[0]
    

class Dynamic:
    
    __slots__ = ('TAG', 'VALUE', 'ID', 'VERSION_MAJOR', 'VERSION_MINOR', 'INDEX')
    
    # Dynamic Tags
    (DT_NULL, DT_NEEDED, DT_PLTRELSZ, DT_PLTGOT, DT_HASH, DT_STRTAB, DT_SYMTAB,
    DT_RELA, DT_RELASZ, DT_RELAENT, DT_STRSZ, DT_SYMENT, DT_INIT, DT_FINI,
    DT_SONAME, DT_RPATH, DT_SYMBOLIC, DT_REL, DT_RELSZ, DT_RELENT, DT_PLTREL,
    DT_DEBUG, DT_TEXTREL, DT_JMPREL, DT_BIND_NOW, DT_INIT_ARRAY, DT_FINI_ARRAY,
    DT_INIT_ARRAYSZ, DT_FINI_ARRAYSZ, DT_RUNPATH, DT_FLAGS, DT_ENCODING, DT_PREINIT_ARRAY,
    DT_PREINIT_ARRAYSZ)         = range(0x22)
    DT_SCE_IDTABENTSZ           = 0x61000005
    DT_SCE_FINGERPRINT          = 0x61000007
    DT_SCE_ORIGINAL_FILENAME    = 0x61000009
    DT_SCE_MODULE_INFO          = 0x6100000D
    DT_SCE_NEEDED_MODULE        = 0x6100000F
    DT_SCE_MODULE_ATTR          = 0x61000011
    DT_SCE_EXPORT_LIB           = 0x61000013
    DT_SCE_IMPORT_LIB           = 0x61000015
    DT_SCE_EXPORT_LIB_ATTR      = 0x61000017
    DT_SCE_IMPORT_LIB_ATTR      = 0x61000019
    DT_SCE_STUB_MODULE_NAME     = 0x6100001D
    DT_SCE_STUB_MODULE_VERSION  = 0x6100001F
    DT_SCE_STUB_LIBRARY_NAME    = 0x61000021
    DT_SCE_STUB_LIBRARY_VERSION = 0x61000023
    DT_SCE_HASH                 = 0x61000025
    DT_SCE_PLTGOT               = 0x61000027
    DT_SCE_JMPREL               = 0x61000029
    DT_SCE_PLTREL               = 0x6100002B
    DT_SCE_PLTRELSZ             = 0x6100002D
    DT_SCE_RELA                 = 0x6100002F
    DT_SCE_RELASZ               = 0x61000031
    DT_SCE_RELAENT              = 0x61000033
    DT_SCE_STRTAB               = 0x61000035
    DT_SCE_STRSZ                = 0x61000037
    DT_SCE_SYMTAB               = 0x61000039
    DT_SCE_SYMENT               = 0x6100003B
    DT_SCE_HASHSZ               = 0x6100003D
    DT_SCE_SYMTABSZ             = 0x6100003F
    DT_SCE_HIOS                 = 0x6FFFF000
    DT_GNU_HASH                 = 0x6FFFFEF5
    DT_VERSYM                   = 0x6FFFFFF0
    DT_RELACOUNT                = 0x6FFFFFF9
    DT_RELCOUNT                 = 0x6FFFFFFA
    DT_FLAGS_1                  = 0x6FFFFFFB
    DT_VERDEF                   = 0x6FFFFFFC
    DT_VERDEFNUM                = 0x6FFFFFFD

    def __init__(self, f):
    
        self.TAG   = struct.unpack('<Q', f.read(8))[0]
        self.VALUE = struct.unpack('<Q', f.read(8))[0]
    
    def tag(self):
    
        return {
            Dynamic.DT_NULL                     : 'DT_NULL',
            Dynamic.DT_NEEDED                   : 'DT_NEEDED',
            Dynamic.DT_PLTRELSZ                 : 'DT_PLTRELSZ',
            Dynamic.DT_PLTGOT                   : 'DT_PLTGOT',
            Dynamic.DT_HASH                     : 'DT_HASH',
            Dynamic.DT_STRTAB                   : 'DT_STRTAB',
            Dynamic.DT_SYMTAB                   : 'DT_SYMTAB',
            Dynamic.DT_RELA                     : 'DT_RELA',
            Dynamic.DT_RELASZ                   : 'DT_RELASZ',
            Dynamic.DT_RELAENT                  : 'DT_RELAENT',
            Dynamic.DT_STRSZ                    : 'DT_STRSZ',
            Dynamic.DT_SYMENT                   : 'DT_SYMENT',
            Dynamic.DT_INIT                     : 'DT_INIT',
            Dynamic.DT_FINI                     : 'DT_FINI',
            Dynamic.DT_SONAME                   : 'DT_SONAME',
            Dynamic.DT_RPATH                    : 'DT_RPATH',
            Dynamic.DT_SYMBOLIC                 : 'DT_SYMBOLIC',
            Dynamic.DT_REL                      : 'DT_REL',
            Dynamic.DT_RELSZ                    : 'DT_RELSZ',
            Dynamic.DT_RELENT                   : 'DT_RELENT',
            Dynamic.DT_PLTREL                   : 'DT_PLTREL',
            Dynamic.DT_DEBUG                    : 'DT_DEBUG',
            Dynamic.DT_TEXTREL                  : 'DT_TEXTREL',
            Dynamic.DT_JMPREL                   : 'DT_JMPREL',
            Dynamic.DT_BIND_NOW                 : 'DT_BIND_NOW',
            Dynamic.DT_INIT_ARRAY               : 'DT_INIT_ARRAY',
            Dynamic.DT_FINI_ARRAY               : 'DT_FINI_ARRAY',
            Dynamic.DT_INIT_ARRAYSZ             : 'DT_INIT_ARRAYSZ',
            Dynamic.DT_FINI_ARRAYSZ             : 'DT_FINI_ARRAYSZ',
            Dynamic.DT_RUNPATH                  : 'DT_RUN_PATH',
            Dynamic.DT_FLAGS                    : 'DT_FLAGS',
            Dynamic.DT_ENCODING                 : 'DT_ENCODING',
            Dynamic.DT_PREINIT_ARRAY            : 'DT_PREINIT_ARRAY',
            Dynamic.DT_PREINIT_ARRAYSZ          : 'DT_PREINIT_ARRAYSZ',
            Dynamic.DT_SCE_IDTABENTSZ           : 'DT_SCE_IDTABENTSZ',
            Dynamic.DT_SCE_FINGERPRINT          : 'DT_SCE_FINGERPRINT',
            Dynamic.DT_SCE_ORIGINAL_FILENAME    : 'DT_SCE_ORIGINAL_FILENAME',
            Dynamic.DT_SCE_MODULE_INFO          : 'DT_SCE_MODULE_INFO',
            Dynamic.DT_SCE_NEEDED_MODULE        : 'DT_SCE_NEEDED_MODULE',
            Dynamic.DT_SCE_MODULE_ATTR          : 'DT_SCE_MODULE_ATTR',
            Dynamic.DT_SCE_EXPORT_LIB           : 'DT_SCE_EXPORT_LIB',
            Dynamic.DT_SCE_IMPORT_LIB           : 'DT_SCE_IMPORT_LIB',
            Dynamic.DT_SCE_EXPORT_LIB_ATTR      : 'DT_SCE_EXPORT_LIB_ATTR',
            Dynamic.DT_SCE_IMPORT_LIB_ATTR      : 'DT_SCE_IMPORT_LIB_ATTR',
            Dynamic.DT_SCE_STUB_MODULE_NAME     : 'DT_SCE_STUB_MODULE_NAME',
            Dynamic.DT_SCE_STUB_MODULE_VERSION  : 'DT_SCE_STUB_MODULE_VERSION',
            Dynamic.DT_SCE_STUB_LIBRARY_NAME    : 'DT_SCE_STUB_LIBRARY_NAME',
            Dynamic.DT_SCE_STUB_LIBRARY_VERSION : 'DT_SCE_STUB_LIBRARY_VERSION',
            Dynamic.DT_SCE_HASH                 : 'DT_SCE_HASH',
            Dynamic.DT_SCE_PLTGOT               : 'DT_SCE_PLTGOT',
            Dynamic.DT_SCE_JMPREL               : 'DT_SCE_JMPREL',
            Dynamic.DT_SCE_PLTREL               : 'DT_SCE_PLTREL',
            Dynamic.DT_SCE_PLTRELSZ             : 'DT_SCE_PLTRELSZ',
            Dynamic.DT_SCE_RELA                 : 'DT_SCE_RELA',
            Dynamic.DT_SCE_RELASZ               : 'DT_SCE_RELASZ',
            Dynamic.DT_SCE_RELAENT              : 'DT_SCE_RELAENT',
            Dynamic.DT_SCE_STRTAB               : 'DT_SCE_STRTAB',
            Dynamic.DT_SCE_STRSZ                : 'DT_SCE_STRSZ',
            Dynamic.DT_SCE_SYMTAB               : 'DT_SCE_SYMTAB',
            Dynamic.DT_SCE_SYMENT               : 'DT_SCE_SYMENT',
            Dynamic.DT_SCE_HASHSZ               : 'DT_SCE_HASHSZ',
            Dynamic.DT_SCE_SYMTABSZ             : 'DT_SCE_SYMTABSZ',
            Dynamic.DT_SCE_HIOS                 : 'DT_SCE_HIOS',
            Dynamic.DT_GNU_HASH                 : 'DT_GNU_HASH',
            Dynamic.DT_VERSYM                   : 'DT_VERSYM',
            Dynamic.DT_RELACOUNT                : 'DT_RELACOUNT',
            Dynamic.DT_RELCOUNT                 : 'DT_RELCOUNT',
            Dynamic.DT_FLAGS_1                  : 'DT_FLAGS_1',
            Dynamic.DT_VERDEF                   : 'DT_VERDEF',
            Dynamic.DT_VERDEFNUM                : 'DT_VERDEFNUM',
        }.get(self.TAG, 'Missing Dynamic Tag!!!')
    
    def lib_attribute(self):
    
        return {
            0x1  : 'AUTO_EXPORT',
            0x2  : 'WEAK_EXPORT',
            0x8  : 'LOOSE_IMPORT',
            0x9  : 'AUTO_EXPORT|LOOSE_IMPORT',
            0x10 : 'WEAK_EXPORT|LOOSE_IMPORT',
        }.get(self.INDEX, 'Missing Import Library Attribute!!!')
    
    def mod_attribute(self):
    
        return {
            0x0  : 'NONE',
            0x1  : 'SCE_CANT_STOP',
            0x2  : 'SCE_EXCLUSIVE_LOAD',
            0x4  : 'SCE_EXCLUSIVE_START',
            0x8  : 'SCE_CAN_RESTART',
            0x10 : 'SCE_CAN_RELOCATE',
            0x20 : 'SCE_CANT_SHARE',
        }.get(self.INDEX, 'Missing Module Attribute!!!')

class Relocation:

    __slots__ = ('OFFSET', 'INDEX', 'INFO', 'ADDEND')
    
    # PS4 (X86_64) Relocation Codes (40)
    (R_X86_64_NONE, R_X86_64_64, R_X86_64_PC32, R_X86_64_GOT32,
    R_X86_64_PLT32, R_X86_64_COPY, R_X86_64_GLOB_DAT, R_X86_64_JUMP_SLOT,
    R_X86_64_RELATIVE, R_X86_64_GOTPCREL, R_X86_64_32, R_X86_64_32S,
    R_X86_64_16, R_X86_64_PC16, R_X86_64_8, R_X86_64_PC8, R_X86_64_DTPMOD64,
    R_X86_64_DTPOFF64, R_X86_64_TPOFF64, R_X86_64_TLSGD, R_X86_64_TLSLD,
    R_X86_64_DTPOFF32, R_X86_64_GOTTPOFF, R_X86_64_TPOFF32, R_X86_64_PC64,
    R_X86_64_GOTOFF64, R_X86_64_GOTPC32, R_X86_64_GOT64, R_X86_64_GOTPCREL64,
    R_X86_64_GOTPC64, R_X86_64_GOTPLT64, R_X86_64_PLTOFF64, R_X86_64_SIZE32,
    R_X86_64_SIZE64, R_X86_64_GOTPC32_TLSDESC, R_X86_64_TLSDESC_CALL, R_X86_64_TLSDESC,
    R_X86_64_IRELATIVE, R_X86_64_RELATIVE64) = range(0x27)
    R_X86_64_ORBIS_GOTPCREL_LOAD             = 0x28 
    
    def __init__(self, f):
    
        self.OFFSET = struct.unpack('<Q', f.read(8))[0]
        self.INFO   = struct.unpack('<Q', f.read(8))[0]
        self.ADDEND = struct.unpack('<Q', f.read(8))[0]
    
    def type(self):
    
        return {
            Relocation.R_X86_64_NONE                : 'R_X86_64_NONE',
            Relocation.R_X86_64_64                  : 'R_X86_64_64',
            Relocation.R_X86_64_PC32                : 'R_X86_64_PC32',
            Relocation.R_X86_64_GOT32               : 'R_X86_64_GOT32',
            Relocation.R_X86_64_PLT32               : 'R_X86_64_PLT32',
            Relocation.R_X86_64_COPY                : 'R_X86_64_COPY',
            Relocation.R_X86_64_GLOB_DAT            : 'R_X86_64_GLOB_DAT',
            Relocation.R_X86_64_JUMP_SLOT           : 'R_X86_64_JUMP_SLOT',
            Relocation.R_X86_64_RELATIVE            : 'R_X86_64_RELATIVE',
            Relocation.R_X86_64_GOTPCREL            : 'R_X86_64_GOTPCREL',
            Relocation.R_X86_64_32                  : 'R_X86_64_32',
            Relocation.R_X86_64_32S                 : 'R_X86_64_32S',
            Relocation.R_X86_64_16                  : 'R_X86_64_16',
            Relocation.R_X86_64_PC16                : 'R_X86_64_PC16',
            Relocation.R_X86_64_8                   : 'R_X86_64_8',
            Relocation.R_X86_64_PC8                 : 'R_X86_64_PC8',
            Relocation.R_X86_64_DTPMOD64            : 'R_X86_64_DTPMOD64',
            Relocation.R_X86_64_DTPOFF64            : 'R_X86_64_DTPOFF64',
            Relocation.R_X86_64_TPOFF64             : 'R_X86_64_TPOFF64',
            Relocation.R_X86_64_TLSGD               : 'R_X86_64_TLSGD',
            Relocation.R_X86_64_TLSLD               : 'R_X86_64_TLSLD',
            Relocation.R_X86_64_DTPOFF32            : 'R_X86_64_DTPOFF32',
            Relocation.R_X86_64_GOTTPOFF            : 'R_X86_64_GOTTPOFF',
            Relocation.R_X86_64_TPOFF32             : 'R_X86_64_TPOFF32',
            Relocation.R_X86_64_PC64                : 'R_X86_64_PC64',
            Relocation.R_X86_64_GOTOFF64            : 'R_X86_64_GOTOFF64',
            Relocation.R_X86_64_GOTPC32             : 'R_X86_64_GOTPC32',
            Relocation.R_X86_64_GOT64               : 'R_X86_64_GOT64',
            Relocation.R_X86_64_GOTPCREL64          : 'R_X86_64_GOTPCREL64',
            Relocation.R_X86_64_GOTPC64             : 'R_X86_64_GOTPC64',
            Relocation.R_X86_64_GOTPLT64            : 'R_X86_64_GOTPLT64',
            Relocation.R_X86_64_PLTOFF64            : 'R_X86_64_PLTOFF64',
            Relocation.R_X86_64_SIZE32              : 'R_X86_64_SIZE32',
            Relocation.R_X86_64_SIZE64              : 'R_X86_64_SIZE64',
            Relocation.R_X86_64_GOTPC32_TLSDESC     : 'R_X86_64_GOTPC32_TLSDESC',
            Relocation.R_X86_64_TLSDESC_CALL        : 'R_X86_64_TLSDESC_CALL',
            Relocation.R_X86_64_TLSDESC             : 'R_X86_64_TLSDESC',
            Relocation.R_X86_64_IRELATIVE           : 'R_X86_64_IRELATIVE',
            Relocation.R_X86_64_RELATIVE64          : 'R_X86_64_RELATIVE64',
            Relocation.R_X86_64_ORBIS_GOTPCREL_LOAD : 'R_X86_64_ORBIS_GOTPCREL_LOAD',
        }.get(self.INFO, 'Missing PS4 Relocation Type!!!')


class Symbol:

    __slots__ = ('NAME', 'INFO', 'OTHER', 'INDEX', 'VALUE', 'SIZE')
    
    # Symbol Information
    ST_LOCAL_NONE      = 0x0
    ST_LOCAL_OBJECT    = 0x1
    ST_LOCAL_FUNCTION  = 0x2
    ST_LOCAL_SECTION   = 0x3
    ST_LOCAL_FILE      = 0x4
    ST_LOCAL_COMMON    = 0x5
    ST_LOCAL_TLS       = 0x6
    ST_GLOBAL_NONE     = 0x10
    ST_GLOBAL_OBJECT   = 0x11
    ST_GLOBAL_FUNCTION = 0x12
    ST_GLOBAL_SECTION  = 0x13
    ST_GLOBAL_FILE     = 0x14
    ST_GLOBAL_COMMON   = 0x15
    ST_GLOBAL_TLS      = 0x16
    ST_WEAK_NONE       = 0x20
    ST_WEAK_OBJECT     = 0x21
    ST_WEAK_FUNCTION   = 0x22
    ST_WEAK_SECTION    = 0x23
    ST_WEAK_FILE       = 0x24
    ST_WEAK_COMMON     = 0x25
    ST_WEAK_TLS        = 0x26
    
    def __init__(self, f):
    
        self.NAME      = struct.unpack('<I', f.read(4))[0]
        self.INFO      = struct.unpack('<B', f.read(1))[0]
        self.OTHER     = struct.unpack('<B', f.read(1))[0]
        self.INDEX     = struct.unpack('<H', f.read(2))[0]
        self.VALUE     = struct.unpack('<Q', f.read(8))[0]
        self.SIZE      = struct.unpack('<Q', f.read(8))[0]
    
    def info(self):
    
        return {
            Symbol.ST_LOCAL_NONE      : 'Local : None',
            Symbol.ST_LOCAL_OBJECT    : 'Local : Object',
            Symbol.ST_LOCAL_FUNCTION  : 'Local : Function',
            Symbol.ST_LOCAL_SECTION   : 'Local : Section',
            Symbol.ST_LOCAL_FILE      : 'Local : File',
            Symbol.ST_LOCAL_COMMON    : 'Local : Common',
            Symbol.ST_LOCAL_TLS       : 'Local : TLS',
            Symbol.ST_GLOBAL_NONE     : 'Global : None',
            Symbol.ST_GLOBAL_OBJECT   : 'Global : Object',
            Symbol.ST_GLOBAL_FUNCTION : 'Global : Function',
            Symbol.ST_GLOBAL_SECTION  : 'Global : Section',
            Symbol.ST_GLOBAL_FILE     : 'Global : File',
            Symbol.ST_GLOBAL_COMMON   : 'Global : Common',
            Symbol.ST_GLOBAL_TLS      : 'Global : TLS',
            Symbol.ST_WEAK_NONE       : 'Weak : None',
            Symbol.ST_WEAK_OBJECT     : 'Weak : Object',
            Symbol.ST_WEAK_FUNCTION   : 'Weak : Function',
            Symbol.ST_WEAK_SECTION    : 'Weak : Section',
            Symbol.ST_WEAK_FILE       : 'Weak : File',
            Symbol.ST_WEAK_COMMON     : 'Weak : Common',
            Symbol.ST_WEAK_TLS        : 'Weak : TLS',
        }.get(self.INFO, 'Missing Symbol Information!!!')
    
