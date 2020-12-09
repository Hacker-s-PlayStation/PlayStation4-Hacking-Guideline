# Library
## 개요
### Uart Log
* Uart Log를 보다가 플레이스테이션 4에서 외부 사이트에서 파일을 가져오는 것을 확인
![image](https://user-images.githubusercontent.com/39231485/101589311-86880d00-3a2b-11eb-9906-aafc7b2b666e.png)
### 새로운 방법론
* 기존에 WebKit, Freebsd 취약점을 사용하는 Jailbreak와는 다르게 프로세스 안에 있는 라이브러리의 취약점을 사용하는 것을 고안해봤다.
  * 라이브러리 내의 취약점을 찾기 위해서 소스 코드 오디팅, 라이브러리 함수를 대상으로 퍼징을 시도한다.
### 파일 복호화
* 플레이스테이션 4 안의 파일들은 모두 암호화가 되어있기 때문에 아래에서 복호화된 펌웨어를 사용해야 한다.<br>
[사이트](https://darthsternie.net/ps4-decrypted-firmwares/)

## 소스코드 오디팅 준비
### 라이브러리 함수 심볼 복구
복호화된 sprx를 아이다로 열었을 때, 심볼은 존재하지 않는다.
![image](https://user-images.githubusercontent.com/39231485/101623622-0f1ea180-3a5c-11eb-8f63-9687c8a3624d.png)

하지만 심볼 대신 NID라는 것을 통하여 함수 주소와 매치시키는데, 만약 특정 NID가 어떤 함수명인지 안다면 심볼을 복구 할 수 있을 것이다.
[사이트](https://github.com/SocraticBliss/ps4_module_loader) 
## 퍼징 준비
### sprx를 so파일로 바꾸기
### ps4 라이브러리
![image](https://user-images.githubusercontent.com/39231485/101594750-8e4caf00-3a35-11eb-891e-3102d8be47be.png)
  * ps4 라이브러리는 소니가 자체적으로 만든 sprx라는 포맷을 사용한다.
    * 이를 so 파일로 만들어주기 위해서는 sprx 포맷을 elf 포맷으로 만들어줘야 한다.

### SPRX / ELF HEADER

- 두 포맷의 헤더 필드는 거의 동일하다. 각각의 요소만 조금씩 변형시켜주면 된다.

우리가 리눅스에서 사용하는 ELF의 헤더이다. 

```python
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              DYN (Shared object file)
  Machine:                           Advanced Micro Devices X86-64
  Version:                           0x1
  Entry point address:               0x4000
  Start of program headers:          64 (bytes into file)
  `:          165424 (bytes into file)
  Flags:                             0x0
  Size of this header:               64 (bytes)
  Size of program headers:           56 (bytes)
  Number of program headers:         7
  Size of section headers:           64 (bytes)
  Number of section headers:         6
  Section header string table index: 2
```

다음은 `SPRX`의 헤더를 읽어온 것이다.

```python
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 09 00 00 00 00 00 00 00 00
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - FreeBSD
  ABI Version:                       0
  Type:                              OS Specific: (fe18)
  Machine:                           Advanced Micro Devices X86-64
  Version:                           0x1
  Entry point address:               0x0
  Start of program headers:          64 (bytes into file)
  Start of section headers:          0 (bytes into file)
  Flags:                             0x0
  Size of this header:               64 (bytes)
  Size of program headers:           56 (bytes)
  Number of program headers:         9
  Size of section headers:           0 (bytes)
  Number of section headers:         0
  Section header string table index: 0
```

변경해야할 필드들과 변경할 값들을 쌍으로 나열해보면 다음과 같다.

- `OS/ABI` → 대상 운영 체제 ABI를 구별하는 필드.
    - `UNIX FreeBSD` 로 설정되어있는  값을 `0x01(HP-UX)` 로 변경시켜준다.
- `TYPE`
    - 해당 파일이 어떤 파일인지 명시하는 필드
    - `sprx` 에서는 파일을 구분하는 값이 조금 다른데 신경쓰지 않아도 된다. 우리는 sprx파일을 so 파일로 바꾸는 것이 목적이므로 해당 필드값을 `3(shared object file` 로 설정해주면 된다.
- `Entry point`
    - so파일이라 0으로 설정해주면 된다.
- `Start of section headers`
    - 추후에 섹션헤더를 추가한 뒤에 설정해줘야하는 offset. sprx에서는 이상하게 섹션 헤더를 사용하지 않았지만, 우리는 다른 프로그램에서 로딩할 수 있도록 몇몇 섹션들을 추가해주어야한다.
- `Number of program headers`
    - 프로그램 헤더의 갯수. 우리가 추가하거나 뺀만큼 조정해주면 된다.
- `Number of section headers`
    - 섹션 헤더들의 갯수. 추가한 만큼 나중에 늘려주면 됨.

### CRAFT PROGRAM HEADER

- elf(.so)의 프로그램 헤더(참고용)
    - GNU_ 가 붙은 타입들은 필수적이지 않은 요소들이라 일단 배제하고 보아도 된다.

```python
Program Headers:
  Type           Offset             VirtAddr           PhysAddr
                 FileSiz            MemSiz              Flags  Align
  LOAD           0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x0000000000000b08 0x0000000000000b08  R      0x1000
  LOAD           0x0000000000001000 0x0000000000001000 0x0000000000001000
                 0x0000000000000b25 0x0000000000000b25  R E    0x1000
  LOAD           0x0000000000002000 0x0000000000002000 0x0000000000002000
                 0x00000000000002b8 0x00000000000002b8  R      0x1000
  LOAD           0x0000000000002e08 0x0000000000003e08 0x0000000000003e08
                 0x0000000000000440 0x0000000000000448  RW     0x1000
  DYNAMIC        0x0000000000002e18 0x0000000000003e18 0x0000000000003e18
                 0x00000000000001c0 0x00000000000001c0  RW     0x8
  NOTE           0x00000000000002a8 0x00000000000002a8 0x00000000000002a8
                 0x0000000000000020 0x0000000000000020  R      0x8
  NOTE           0x00000000000002c8 0x00000000000002c8 0x00000000000002c8
                 0x0000000000000024 0x0000000000000024  R      0x4
  GNU_PROPERTY   0x00000000000002a8 0x00000000000002a8 0x00000000000002a8
                 0x0000000000000020 0x0000000000000020  R      0x8
  GNU_EH_FRAME   0x000000000000206c 0x000000000000206c 0x000000000000206c
                 0x000000000000007c 0x000000000000007c  R      0x4
  GNU_STACK      0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x0000000000000000 0x0000000000000000  RW     0x10
  GNU_RELRO      0x0000000000002e08 0x0000000000003e08 0x0000000000003e08
                 0x00000000000001f8 0x00000000000001f8  R      0x1
```

- sprx의 프로그램 헤더
    - 프로그램 헤더 타입 코드가 달라서 `readelf`로 읽어올시에 타입 이름이 이상하게 나타나지만, 대략적인 형태는 알아볼 수 있어서 다음과 같이 읽어왔다.
    - sprx에서는 elf 헤더 부분을 메모리에 로딩하지 않는다.

```python
Program Headers:
  Type           Offset             VirtAddr           PhysAddr
                 FileSiz            MemSiz              Flags  Align
  LOAD           0x0000000000004000 0x0000000000000000 0x0000000000000000
                 0x000000000001ebf0 0x000000000001ebf0  R E    0x4000
  LOOS+0x1000010 0x0000000000024000 0x0000000000020000 0x0000000000020000
                 0x0000000000000430 0x0000000000000430  R      0x4000
  LOAD           0x0000000000028000 0x0000000000024000 0x0000000000024000
                 0x0000000000000198 0x00000000000001f9  RW     0x4000
  LOOS+0x1000002 0x0000000000028000 0x0000000000024000 0x0000000000024000
                 0x0000000000000018 0x0000000000000018  R      0x8
  DYNAMIC        0x000000000002b260 0x0000000000000000 0x0000000000000000
                 0x0000000000000270 0x0000000000000270  RW     0x8
  TLS            0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x0000000000000000 0x0000000000000000  R      0x1
  GNU_EH_FRAME   0x00000000000217e4 0x000000000001d7e4 0x000000000001d7e4
                 0x000000000000140c 0x000000000000140c  R      0x4
  LOOS+0x1000000 0x00000000000281a0 0x0000000000000000 0x0000000000000000
                 0x0000000000003330 0x0000000000000000  R      0x10
  LOOS+0xfffff01 0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x0000000000000000 0x0000000000000000         0x10
```

sprx의 프로그램 헤더를 불필요한 부분을 전부 제거한 뒤에 다음과 같이 바꿀 것이다.

```python
LOAD           0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x0000000000003ff0 0x0000000000003ff0  RW     0x1000
  LOAD           0x0000000000004000 0x0000000000004000 0x0000000000004000
                 0x000000000001ebf0 0x000000000001ebf0  RWE    0x4000
  LOAD           0x0000000000024000 0x0000000000024000 0x0000000000024000
                 0x0000000000003730 0x0000000000003730  RW     0x4000
  LOAD           0x0000000000028000 0x0000000000028000 0x0000000000028000
                 0x00000000000001f9 0x00000000000001f9  RW     0x4000
  DYNAMIC        0x0000000000028400 0x0000000000228400 0x0000000000228400
                 0x0000000000000200 0x0000000000000200  RW     0x10
  LOAD           0x0000000000028400 0x0000000000228400 0x0000000000228400
                 0x0000000000001000 0x0000000000001000  RW     0x1000

....
```

추가한 부분은 

```python
LOAD           0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x0000000000003ff0 0x0000000000003ff0  RW     0x1000
```

이부분이다. 위 세그먼트는 elf header를 메모리에 로딩하기 위해 추가한 세그먼트다. 기존 세그먼트들 위에 새로운 세그먼트를 추가한 것이므로 파일 `offset, virtual/physical address`에 각각 해당 크기만큼을 더해줘야한다.

세그먼트를 추가한 뒤에는 각각 원래 `LOAD` 세그먼트들의 offset + 추가한 세그먼트의 크기에다가 

기존의 세그먼트 컨텐츠를 다 옮겨주면 된다. (코드영역, 문자열 정보 등)

이제 여기서부터 기존의 elf와 다른 부분을 차근차근 고쳐나가면 되는데, 자세한 내용은 후술하면서 같이 언급할 예정이다.

### CRAFT DYNAMIC ENTRIES

```python
LOAD:0000000000228410                 Elf64_Dyn <5, 2000h>    ; DT_STRTAB
LOAD:0000000000228420                 Elf64_Dyn <6, 24580h>   ; DT_SYMTAB
LOAD:0000000000228430                 Elf64_Dyn <0Ah, 1FF0h>  ; DT_STRSZ
LOAD:0000000000228440                 Elf64_Dyn <0Bh, 18h>    ; DT_SYMENT
LOAD:0000000000228450                 Elf64_Dyn <15h, 0>      ; DT_DEBUG
LOAD:0000000000228460                 Elf64_Dyn <9, 18h>      ; DT_RELAENT
LOAD:0000000000228470                 Elf64_Dyn <18h, 0>      ; DT_BIND_NOW
LOAD:0000000000228480                 Elf64_Dyn <7, 25B58h>   ; DT_RELA
LOAD:0000000000228490                 Elf64_Dyn <8, 818h>     ; DT_RELASZ
LOAD:00000000002284A0                 Elf64_Dyn <0>           ; DT_NULL
```

DYNAMIC 엔트리에서 필요한 정보들을 저장할 오프셋들을 미리 지정해둔 뒤에 해당 테이블을 옮겨오거나 새로 생성할 것이다. 

### Creating DT_STRTAB

일반적으로 ELF에서는 심볼 테이블에서 함수 이름이 위치한 string table의 인덱스를 가지고 있지만 

sprx에서는 함수 이름을 가진 테이블 대신에 함수 고유의 코드인 `nid` 를 가진 table이 존재한다. 

심볼 테이블은 이 nid table의 인덱스를 사용한다.

자세한 내용은 아래 링크에 설명되어있다.

[https://blog.madnation.net/ps4-nid-resolver-ida-plugin/](https://blog.madnation.net/ps4-nid-resolver-ida-plugin/) 

전부는 아니지만 이 nid가 각각 무슨 함수들을 가리키는지에 대한 데이터베이스가 존재하므로 

이 데이터베이스를 이용하여 함수 문자열을 얻어낸 다음 함수 스트링 테이블을 만들어주면 될 것이다. 그런데 이 스트링 테이블을 위한 세그먼트의 공간이 충분하지 않다면 직접 세그먼트를 추가해주면 된다. 

그리고 해당 문자열의 크기만큼 `DT_STRSZ` 을 설정해주면 된다.

#### Creating DT_SYM

- In sprx

```python
SCE_DYNLIBDATA:0000000001029250                 Symbol <240h, 12h, 0, 3, 7270h, 8> ; _ZN3sce3Xml10SimpleDataC1EPKcm | Global : Function
SCE_DYNLIBDATA:0000000001029268                 Symbol <250h, 12h, 0, 3, 7260h, 9> ; _ZN3sce3Xml10SimpleDataC1Ev | Global : Function
SCE_DYNLIBDATA:0000000001029280                 Symbol <260h, 12h, 0, 3, 7270h, 8> ; _ZN3sce3Xml10SimpleDataC2EPKcm | Global : Function
SCE_DYNLIBDATA:0000000001029298                 Symbol <270h, 12h, 0, 3, 7260h, 9> ; _ZN3sce3Xml10SimpleDataC2Ev | Global : Function
SCE_DYNLIBDATA:00000000010292B0                 Symbol <280h, 12h, 0, 3, 4830h, 12Ch> ; _ZN3sce3Xml11Initializer10initializeEPKNS0_13InitParameterE | Global : Function
SCE_DYNLIBDATA:00000000010292C8                 Symbol <290h, 12h, 0, 3, 47B0h, 72h> ; _ZN3sce3Xml11Initializer9terminateEv | Global : Function
SCE_DYNLIBDATA:00000000010292E0                 Symbol <2A0h, 12h, 0, 3, 4730h, 8> ; _ZN3sce3Xml11InitializerC1Ev | Global : Function
```

sym table의 첫번째 필드값은 nid table에서 각각 함수들이 대응하는 nid의 오프셋을 가지고 있다.

4번째 필드값은 해당 함수가 위치한 섹션의 인덱스값이다. 나중에 .text섹션을 생성한뒤에 

.text섹션이 몇번째에 위치해있는지를 적어주면 된다. 

대략 어떻게 바뀌는지를 보여주면 다음과 같다.

```python
LOAD:0000000000024820                 Elf64_Sym <offset aZn3sce3xml10si - offset unk_2000, 12h, 0, 3, \ ; "_ZN3sce3Xml10SimpleDataC1EPKcm" ...
LOAD:0000000000024820                            offset _ZN3sce3Xml10SimpleDataC2EPKcm, 8>
LOAD:0000000000024838                 Elf64_Sym <offset aZn3sce3xml10si_0 - offset unk_2000, 12h, 0, 3, \ ; "_ZN3sce3Xml10SimpleDataC1Ev" ...
LOAD:0000000000024838                            offset _ZN3sce3Xml10SimpleDataC2Ev, 9>
LOAD:0000000000024850                 Elf64_Sym <offset aZn3sce3xml10si_1 - offset unk_2000, 12h, 0, 3, \ ; "_ZN3sce3Xml10SimpleDataC2EPKcm" ...
LOAD:0000000000024850                            offset _ZN3sce3Xml10SimpleDataC2EPKcm, 8>
LOAD:0000000000024868                 Elf64_Sym <offset aZn3sce3xml10si_2 - offset unk_2000, 12h, 0, 3, \ ; "_ZN3sce3Xml10SimpleDataC2Ev" ...
LOAD:0000000000024868                            offset _ZN3sce3Xml10SimpleDataC2Ev, 9>
LOAD:0000000000024880                 Elf64_Sym <offset aZn3sce3xml11in - offset unk_2000, 12h, 0, 3, \ ; "_ZN3sce3Xml11Initializer10initializeEPK"... ...
LOAD:0000000000024880                            offset _ZN3sce3Xml11Initializer10initializeEPKNS0_13InitParameterE,\
LOAD:0000000000024880                            12Ch>
LOAD:0000000000024898                 Elf64_Sym <offset aZn3sce3xml11in_0 - offset unk_2000, 12h, 0, 3, \ ; "_ZN3sce3Xml11Initializer9terminateEv" ...
LOAD:0000000000024898                            offset _ZN3sce3Xml11Initializer9terminateEv, 72h>
LOAD:00000000000248B0                 Elf64_Sym <offset aZn3sce3xml11in_1 - offset unk_2000, 12h, 0, 3, \ ; "_ZN3sce3Xml11InitializerC1Ev" ...
LOAD:00000000000248B0                            offset _ZN3sce3Xml11InitializerC2Ev, 8>
LOAD:00000000000248C8                 Elf64_Sym <offset aZn3sce3xml11in_2 - offset unk_2000, 12h, 0, 3, \ ; "_ZN3sce3Xml11InitializerC2Ev" ...
LOAD:00000000000248C8                            offset _ZN3sce3Xml11InitializerC2Ev, 8>
```

### Creating relocation table

relocation table은 그대로 copy해오면 되는데, 몇가지 유의할 점이 있다.

- 세그먼트를 새로 추가해주었으므로  `offset` 값과 `addend` 값에 새로 추가해준 세그먼트 값을 더해줘야할 뿐만 아니라, 해당 offset에 위치한 포인터에 대해서도 값을 더해줘야함.
- 함수 포인터의 경우 sprx에서는 심볼 테이블과 같은 형태 비슷한 형태로 info를 나타내고 있는데

이 경우 다른 relocation 값들과 같이 구성해주면 된다.

```python
SCE_DYNLIBDATA:000000000102AAB0                 Relocation <offset sce::Xml::MemAllocator::~MemAllocator(), \ ; R_X86_64_64
SCE_DYNLIBDATA:000000000102AAB0                             2A00000001h, 0> 

->

LOAD:0000000000026170                 Elf64_Rela <28068h, 8, 1C357h> ; R_X86_64_RELATIVE +1C357h
```

### CREATING SECTION HEADER

섹션 헤더를 만드는 부분은 그냥 일반적인 elf 포맷에 대한 이해도만 있으면 된다.

원래 sprx 포맷에서는 섹션 헤더를 사용하지 않는데, 리눅스에서 dlopen으로 메모리에 로딩되기 위해서는 몇몇 필수적인 섹션들이 있다. 이는 몇가지 테스트를 통해 알아낸 내용이다.

섹션에 정보를 적어주는건 간단하다. 

섹션 이름을 표기해주기 위하여 여유있는 공간에( 그리 큰 공간이 필요하지도 않다.) 섹션 이름을 저장하고 저장한 곳의 정보를 `.shstrndx` 섹션 헤더에 담아주면 된다. 그리고 `.shstrndx` 가 몇번째에 위치해있는지 elf header의 `Section header string table index` 에 그 정보를 적어주면 된다.

단 여기서 `.dynstr` 이 `.shstrndx` 보다 먼저 와야한다.

`.dynstr` 은 동적 심볼을 위한 string들이 저장되어있는 섹션이다. 즉 함수 또는 전역 변수의 이름, 때에 따라서는 라이브러리의 이름등이 적혀있기도 하다. 필드값에 위에서 생성했었던 string table 주소, 오프셋, 사이즈등을 적어주면 된다.

`.dynamic` 은 dynamic entries(위에서 생성했던) 의 정보를 적어주면 된다.

필드값에  entry size, 주소, 오프셋, 사이즈등을 적어주면 된다.

`.dynsym` 또한 똑같다. 필드값에 이전에 생성했었던 symbol table의 entry size, 주소, 오프셋, 사이즈등을 적어주면 된다.

sprx에서 코드 영역은 항상 첫번째 세그먼트( 헤더가 로딩되지 않으므로 항상 첫번째 세그먼트에 코드가 위치한다고 생각해도 된다.)에 있으므로 .text 섹션에는 해당 세그먼트의 정보들을 옮겨주면 될 것이다.(offset, address, 권한, type등등)

```python
[Nr] Name              Type             Address           Offset
       Size              EntSize          Flags  Link  Info  Align
  [ 0]                   NULL             0000000000000000  00000000
       0000000000000000  0000000000000000           0     0     0
  [ 1] .dynstr           STRTAB           0000000000002000  00002000
       0000000000001ff0  0000000000000000   A       0     0     1
  [ 2] .shstrndx         STRTAB           0000000000000000  00028600
       0000000000000030  0000000000000000           0     0     1
  [ 3] .dynamic          DYNAMIC          0000000000228400  00028400
       0000000000000170  0000000000000010  WA       1     0     8
  [ 4] .dynsym           DYNSYM           0000000000024580  00024580
       0000000000001368  0000000000000018   A       1     2     8
  [ 5] .text             PROGBITS         0000000000004000  00004000
       000000000001ebf0  0000000000000000  AX       0     0     22
```
  
   

### Contents
[메인화면](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/README.md)<br>
#### PS4 소개
[1. Jailbreak](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/1_introduction/Jailbreak.md)<br>
[2. PS4 Open Source](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/1_introduction/PS4_Open_Source.md)<br>
[3. Tools](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/1_introduction/Tools.md)<br>
#### 프로젝트 접근 방법론
[1. WebKit](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/2_methodology/webkit.md)<br>
[2. Hardware](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/2_methodology/hardware.md)<br>
[3. Library](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/2_methodology/library.md)<br>
#### 결론
[결론](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/3_conclusion/conclusion.md)
