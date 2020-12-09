### Page Contents
- [Sanitizer](#sanitizer)
  - [개요](#개요)
  - [빌드](#빌드)
    - [Step 1 : 컴파일 플래그 설정](#step-1--컴파일-플래그-설정)
      - [AddressSanitizer(ASan)](#addresssanitizerasan)
      - [MemorySanitizer(MSan)](#memorysanitizermsan)
      - [UndefinedBehaviorSanitizer(UBSan)](#undefinedbehaviorsanitizerubsan)
    - [Step 2 : 빌드 환경설정](#step-2--빌드-환경설정)
    - [Step 3 : clang 빌드](#step-3--clang-빌드)
    - [Step 4 : 트러블슈팅](#step-4--트러블슈팅)
    - [Step 5 : 테스트](#step-5--테스트)
  - [문제점](#문제점)

---

## Sanitizer
### 개요
Sanitizer는 버그를 감지해 주는 도구이다. 종류에 따라 탐지할 버그의 대상이 달라지며, 목적에 맞게 사용할 수 있다. 일반적으로 clang을 이용하여 컴파일을 할 때 Sanitizer 관련 플래그를 함께 입력해 주면 Sanitizer를 쉽게 붙일 수 있다.

### 빌드
WebKit 같은 경우는 빌드를 할 때 perl 기반의 스크립트를 이용하게 된다. 또한 스크립트 중에서 빌드 환경설정을 해주는 스크립트가 존재하는데, 여기에서 Sanitizer 옵션을 줄 수 있다. (아래 명령어 참고<sup>[1](#foot1)</sup>)
```
./Tools/Scripts/set-webkit-configuration --release --asan
./Tools/Scripts/build-webkit
```
-  `build-webkit` : WebKit 빌드 스크립트
-  `set-webkit-configuration` : WebKit 빌드 환경설정 스크립트
-  release/debug는 자유롭게 선택할 수 있다.

이제 각 Step 별로 Sanitizer를 붙여서 빌드를 시도해 볼 차례이다.

> **Environment** : Ubuntu 18.04 64bit

#### Step 1 : 컴파일 플래그 설정
컴파일 플래그를 설정할 수 있는 파일은 `/webkit/Source/cmake/WebKitCompilerFlags.cmake`이다. 이 파일의 내용을 수정하여 우리가 원하는 Sanitizer를 붙일 수 있다. 참고로 최신 버전의 `WebKitCompilerFlags.cmake` 에는 address, undefined, thread, memory, leak과 같은 flag를 적용할 수 있게끔 분기 로직이 존재한다. (아래 코드 참고)
```
foreach (SANITIZER ${ENABLE_SANITIZERS})
    if (${SANITIZER} MATCHES "address")
        WEBKIT_PREPEND_GLOBAL_COMPILER_FLAGS("-fno-omit-frame-pointer -fno-optimize-sibling-calls")
        set(SANITIZER_COMPILER_FLAGS "-fsanitize=address ${SANITIZER_COMPILER_FLAGS}")
        set(SANITIZER_LINK_FLAGS "-fsanitize=address ${SANITIZER_LINK_FLAGS}")

    elseif (${SANITIZER} MATCHES "undefined")
        WEBKIT_PREPEND_GLOBAL_COMPILER_FLAGS("-fno-omit-frame-pointer -fno-optimize-sibling-calls")
        # -fsanitize=vptr is incompatible with -fno-rtti
        set(SANITIZER_COMPILER_FLAGS "-fsanitize=undefined -frtti ${SANITIZER_COMPILER_FLAGS}")
        set(SANITIZER_LINK_FLAGS "-fsanitize=undefined ${SANITIZER_LINK_FLAGS}")

    elseif (${SANITIZER} MATCHES "thread" AND NOT MSVC)
        set(SANITIZER_COMPILER_FLAGS "-fsanitize=thread ${SANITIZER_COMPILER_FLAGS}")
        set(SANITIZER_LINK_FLAGS "-fsanitize=thread ${SANITIZER_LINK_FLAGS}")

    elseif (${SANITIZER} MATCHES "memory" AND COMPILER_IS_CLANG AND NOT MSVC)
        set(SANITIZER_COMPILER_FLAGS "-fsanitize=memory ${SANITIZER_COMPILER_FLAGS}")
        set(SANITIZER_LINK_FLAGS "-fsanitize=memory ${SANITIZER_LINK_FLAGS}")

    elseif (${SANITIZER} MATCHES "leak" AND NOT MSVC)
        set(SANITIZER_COMPILER_FLAGS "-fsanitize=leak ${SANITIZER_COMPILER_FLAGS}")
        set(SANITIZER_LINK_FLAGS "-fsanitize=leak ${SANITIZER_LINK_FLAGS}")

    else ()
        message(FATAL_ERROR "Unsupported sanitizer: ${SANITIZER}")
    endif ()
endforeach ()
```

하지만 본 프로젝트에서는 이전에 언급했듯 2018-12-16 기준으로 fork 한 WebKit을 이용했기 때문에, 과정이 다소 복잡해진다. (아래 코드 참고)

```
if (ENABLE_ADDRESS_SANITIZER)
    WEBKIT_PREPEND_GLOBAL_COMPILER_FLAGS(-fno-omit-frame-pointer
                                            -fno-optimize-sibling-calls)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fsanitize=address")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address")
    set(CMAKE_EXE_LINKER_FLAGS "-lpthread ${CMAKE_EXE_LINKER_FLAGS} -fsanitize=address")
    set(CMAKE_SHARED_LINKER_FLAGS "-lpthread ${CMAKE_SHARED_LINKER_FLAGS} -fsanitize=address")
endif ()
```
해당 버전에서는 Asan만 디폴트로 제공하기 때문에 다른 플래그를 주려면 소스코드를 직접 수정해야만 한다. WebKit 하위 디렉토리 중 Source라는 디렉토리에서 `-fsanitize=address` 로 설정해주는 부분을 찾아서 모두 원하는 옵션으로 변경해 주면 된다. `Source` 디렉토리 내부에서 grep 명령어로 검색해도 되는데, 기타 에디터를 이용하는 경우 검색 기능을 이용하여 찾는 것이 당연히 좋다. 그리고 Asan 이외의 Sanitizer로 빌드하고자 하는 경우 옵션이 상이할 수 있으므로 어떤 옵션이 필요한지 체크한 후 추가해 주어야 한다.
```
WEBKIT_PREPEND_GLOBAL_COMPILER_FLAGS(-fno-omit-frame-pointer -fno-optimize-sibling-calls)
``` 
버전에 따라 다를 수 있겠지만 2018-12-16 기준으로는 `WebKitCompilerFlags.cmake`에서 위 코드의 인자를 다른 옵션으로 변경해 주었다.


- AddressSanitizer(ASan) : `-fsanitize=address`
  - Option : 디폴트가 ASan이므로 따로 지정해 주지 않아도 된다.
- MemorySanitizer(MSan) : `-fsanitize=memory`
  - Option : `-fno-omit-frame-pointer -fsanitize-memory-track-origins`
- UndefinedBehaviorSanitizer(UBSan) : `-fsanitize=undefined`

##### AddressSanitizer(ASan)
buffer-overflow 및 heap use-after-free를 포함한 메모리 액세스 버그는 C 및 C++과 같은 프로그래밍 언어의 심각한 문제로 남아 있다. AddressSanitizer는 힙, 스택 및 전역 객체에 대한 out-of-bounds 액세스와 use-after-free 버그를 탐지해 주는 도구이다.<sup>[2](#foot2)</sup>

##### MemorySanitizer(MSan)
MemorySanitizer는 초기화 되지 않은 변수를 읽는 경우를 탐지해 주는 도구이다.<sup>[3](#foot3)</sup>

##### UndefinedBehaviorSanitizer(UBSan)
UndefinedBehaviorSanitizer는 undefined behavior를 탐지하는 빠른 도구이다. 컴파일 타임에 프로그램을 수정하며 프로그램 실행 중 정의되지 않은 다양한 행위들을 포착한다.<sup>[4](#foot4)</sup>

#### Step 2 : 빌드 환경설정
```
./Tools/Scripts/set-webkit-configuration --release --asan
```
모든 옵션을 변경했다면 Asan 빌드를 활성화 해야 한다. release/debug는 자유롭게 선택하면 된다. 해당 작업을 해줘야 Sanitizer를 붙여서 빌드가 되고, 그 과정에서 원래는 Asan이 적용되어야 했던 부분이 우리가 원하는 Sanitizer로 변경될 것이다.

#### Step 3 : clang 빌드
만약 우분투에서 해당 작업을 수행한다면 디폴트로 gcc 컴파일러를 통해 빌드가 될 것이다. 아쉽게도 gcc에서 `-fsanitize=MemorySanitizer`로 빌드시 에러가 발생한다. 이러한 옵션은 clang 컴파일러를 이용해야 하는데 환경변수로 기본 컴파일러를 지정해 주면 간단히 해결되는 문제이다.
```
export CC=/usr/bin/clang
export CXX=/usr/bin/clang++
```
컴파일러가 clang으로 잘 세팅 되었는지, ASan 빌드가 잘 활성화 되었는지 확인하기 위해서는 `CMakeCache.txt` 파일을 확인해 보면 된다.
```
❯ pwd
/home/lee/WebKit/WebKitBuild/Release
❯ code CMakeCache.txt
```
```
24 //CXX compiler
25 CMAKE_CXX_COMPILER:FILEPATH=/usr/bin/clang++

49 //C compiler
50 CMAKE_C_COMPILER:FILEPATH=/usr/bin/clang

243 //Enable address sanitizer
244 ENABLE_ADDRESS_SANITIZER:BOOL=ON
```
> **잘못된 경우**
> - C compiler : /usr/bin/cc
> - CXX compiler : /usr/bin/c++
> - ENABLE_ADDRESS_SANITIZER:BOOL=OFF

#### Step 4 : 트러블슈팅
아마도 빌드는 한 번에 되지 않을 것이다. `Could NOT find Threads (missing: Threads_FOUND)` 이런 메시지가 뜨면서 빌드에 실패할 수 있다. 이 경우 가장 최상위 디렉토리에 존재하는 `CMakeLists.txt` 파일을 수정해 주면 된다.
```
❯ pwd
/home/lee/WebKit
❯ code CMakeLists.txt
```
오류가 나는 부분이 로그에 남을텐데 해당 라인 넘버로 이동한 후 그 위에 4줄의 코드를 추가해 주면 된다.
```
set(THREADS_PREFER_PTHREAD_FLAG ON) // Where the error occurred
```
```
//////////////// Added //////////////////
set(CMAKE_THREAD_LIBS_INIT "-lpthread")
set(CMAKE_HAVE_THREADS_LIBRARY 1)
set(CMAKE_USE_WIN32_THREADS_INIT 0)
set(CMAKE_USE_PTHREADS_INIT 1)
/////////////////////////////////////////

set(THREADS_PREFER_PTHREAD_FLAG ON)
```
#### Step 5 : 테스트
마지막으로 PoC를 테스트해보거나 `testmasm` 바이너리를 한 번 실행해 보자.
```
❯ pwd
/home/lee/WebKit/WebKitBuild/Release/bin
❯ ls
jsc  LLIntOffsetsExtractor  MallocBench  testair  testapi  testapi-function-overrides.js  testapi.js  testb3  test.js  testmasm  TestWebKitAPI
❯ ./testmasm
```
![msan](https://user-images.githubusercontent.com/45416961/101595740-3adb6080-3a37-11eb-815c-8a8727ee3ee4.png)
위와 같이 메시지가 뜨면 빌드에 성공한 것이다. 만약 위 사진처럼 출력되지 않는다면 `CMakeCache.txt` 파일을 보면서 컴파일러나 Asan enable 설정이 잘 되었는지 점검해 보자.

### 문제점
> Asan 이외의 Sanitizer는 이용할 수 없을 정도로 매우 불안정하다.

아마 옛날 버전의 WebKit을 사용해서 그런 것일지도 모르겠다.*(본 프로젝트에서는 WebKit 최신 버전을 이용할 일이 없어서 빌드를 해보지 않았다.)* 2018-12-16 버전으로 Msan이나 UBSan을 붙여서 테스트를 해봤더니 오탐률이 거의 100%에 육박했다. 소위 말해 '개복치' 스럽다고도 할 수 있겠다. jsc에서 `print("hello world")`만 해줘도 Memory Leak이 발생하니 그 결과가 가히 실망스럽다. 
## Reference <!-- omit in toc -->
><b id="foot1">[1]</b> [Building WebKit with Clang Address Sanitizer(ASan)](https://trac.webkit.org/wiki/ASanWebKit)<br>
><b id="foot2">[2]</b> Konstantin Serebryany; Derek Bruening; Alexander Potapenko; Dmitry Vyukov. ["AddressSanitizer: a fast address sanity checker"(PDF)](https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf). Proceedings of the 2012 USENIX conference on Annual Technical Conference.<br>
><b id="foot3">[3]</b> [MemorySanitizer - Clang 12 Documentation](https://clang.llvm.org/docs/MemorySanitizer.html)<br>
><b id="foot4">[4]</b> [UndefinedBehaviorSanitizer - Clang 12 Documentation](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html)

---
### Contents <!-- omit in toc -->
[메인화면](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/README.md)<br>

#### PS4 소개 <!-- omit in toc -->
[1. Jailbreak](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/1_introduction/Jailbreak.md)<br>
[2. PS4 Open Source](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/1_introduction/PS4_Open_Source.md)<br>
[3. Tools](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/1_introduction/Tools.md)<br>

#### 프로젝트 접근 방법론 <!-- omit in toc -->
[1. WebKit](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/2_methodology/webkit.md)<br>
[2. Hardware](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/2_methodology/hardware.md)<br>
[3. Library](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/2_methodology/library.md)<br>

#### 결론 <!-- omit in toc -->
[결론](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/3_conclusion/conclusion.md)