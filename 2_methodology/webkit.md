### Page Contents <!-- omit in toc -->
- [1. 개요](#1-개요)
  - [1.1. WebKit 이란?](#11-webkit-이란)
- [2. WebKit 빌드](#2-webkit-빌드)
  - [2.1. WebKit download](#21-webkit-download)
  - [2.2. JSC 빌드](#22-jsc-빌드)
  - [2.3. GTK 빌드](#23-gtk-빌드)
  - [2.4. PS4 Webkit 빌드](#24-ps4-webkit-빌드)
  - [2.5. Docker 환경](#25-docker-환경)
- [3. PS4 WebKit의 특징](#3-ps4-webkit의-특징)
  - [3.1. NO JIT](#31-no-jit)
  - [3.2. NO Garbage Collector](#32-no-garbage-collector)
  - [3.3. NO WASM](#33-no-wasm)
- [4. PS4 WebKit exploit 방법론](#4-ps4-webkit-exploit-방법론)
  - [4.1. Return Oriented Programming, Jump Oriented Programming](#41-return-oriented-programming-jump-oriented-programming)
- [5. Sanitizer](#5-sanitizer)
  - [5.1. 개요](#51-개요)
    - [5.1.1. AddressSanitizer(ASan)](#511-addresssanitizerasan)
    - [5.1.2. MemorySanitizer(MSan)](#512-memorysanitizermsan)
    - [5.1.3. UndefinedBehaviorSanitizer(UBSan)](#513-undefinedbehaviorsanitizerubsan)
  - [5.2. 빌드](#52-빌드)
    - [5.2.1. Step 1 : 컴파일 플래그 설정](#521-step-1--컴파일-플래그-설정)
    - [5.2.2. Step 2 : 빌드 환경설정](#522-step-2--빌드-환경설정)
    - [5.2.3. Step 3 : clang 빌드](#523-step-3--clang-빌드)
    - [5.2.4. Step 4 : 트러블슈팅](#524-step-4--트러블슈팅)
    - [5.2.5. Step 5 : 테스트](#525-step-5--테스트)
  - [5.3. 문제점](#53-문제점)
- [6. 1-day 취약점 분석 방법론](#6-1-day-취약점-분석-방법론)
  - [6.1. Chromium](#61-chromium)
  - [6.2. exploit-db](#62-exploit-db)
  - [6.3. Bugzilla](#63-bugzilla)
  - [6.4. WebKit regression test](#64-webkit-regression-test)
- [7. Reference](#7-reference)

---


## 1. 개요

### 1.1. WebKit 이란?

APPLE 에서 개발한 Safari, Chrome 등의 브라우저에서 사용되는 Open Source 렌더링 엔진이다. PS4 내부 브라우저에서도 Webkit을 사용한다. 그렇기에 우리는 해당 PS4의 웹킷을 attack vector로 삼았다.

그러나 Webkit에서 User-Agent에 나오는 버전을 <strong>Freezing</strong> 하고 있어서 정확한 버전을 확인 할 수 없었고, PS4 Webkit ChangeLog를 확인해 보니 <strong>2018-12-16</strong> 이후로 SONY에서 자체적으로 fork를 떠 커스터마이징 한 것으로 추정 된 다.

## 2. WebKit 빌드
### 2.1. WebKit download
> 해당 실습은 우분투 18.04에서 2018-12-16 `a5beb7c88f12c377c3347f74776d2270fbbc79a4` 커밋 기준으로 진행 하였다.

https://github.com/WebKit/webkit.git

위 링크는 Webkit github 링크이다. git clone을 이용해서 가져오자.
 ```bash
 git clone https://github.com/WebKit/webkit.git
 ```

이후 분석하고자 하는 version으로 git checkcout 해주면 된다.

```bash
git checkout a5beb7c88f12c377c3347f74776d2270fbbc79a4
```

참고로 Webkit을 빌드하기전에 다음 프로그램들이 사전에 설치되어 있어야 한다.
```bash
sudo apt install cmake ruby libicu-dev gperf ninja-build
```

또한 version에 따라 설치에 필요한 것들이 다를 수 있으니 그때 마다 설치해 주어야 한다.

### 2.2. JSC 빌드
JSC 빌드 명령어는 다음과 같다. 
```bash
./webkit/Tools/Scripts/build-webkit --jsc-only --debug
```

- `jsc-only` : jsc만 빌드함
- `debug` : debug 모드로 빌드함 (debug 모드가 아니면 나중에 분석 할 때 describe라는 객체 등의 주소를 알어오는 함수를 못 사용함)

이후 빌드에 성공하면 다음과 같이 JSC를 실행하면 command line이 뜨는 것을 확인 할 수 있다.

```bash
./webkit/WebKitBuild/Debug/bin/jsc
```
```bash
seohojin@ubuntu:~/Desktop$ ./webkit/WebKitBuild/Debug/bin/jsc 
>>> 1+2
3
>>> 
```

### 2.3. GTK 빌드
GTK를 빌드하기 위해서는 먼저 다음과 같은 선수 작업이 필요하다.

```bash
./webkit/Tools/gtk/install-dependencies

apt install libwoff-dev flatpak flatpak-builder python-pip

pip install pyyaml
```

다음 명령어 실행 뒤 `xdg-dbus-proxy` 와 `bwrap 0.3.1` 도 설치하여 make 해주어야 한다.

- `xdg-dbus-proxy`  : https://github.com/flatpak/xdg-dbus-proxy
- `bwrap 0.3.1` : https://launchpad.net/ubuntu/+source/bubblewrap/0.3.1-1ubuntu1

위 링크들을 참고하여 설치한 뒤 `/webkit/Source/WebKit/UIProcess/gtk/WaylandCompositor.cpp` 파일에 `#include <EGL/eglmesaext.h>` 헤더를 한 줄 추가해야 한다. 

EGL_WAYLAND_BUFFER_WL이 없다는 오류가 뜰 수 있기 때문이다.

모든 선수 작업을 마무리 한 뒤 `/webkit/Tools/Scripts/build-webkit --gtk --debug` 를 실행하면 된다. (실행 할 때 RAM 16GB 정도 할당 권장)

- `debug` : debug 모드로 빌드함 (debug 모드가 아니면 나중에 분석 할 때 describe라는 객체 등의 주소를 알어오는 함수를 못 사용함)
- `gtk` : gtk 모드로 빌드함

### 2.4. PS4 Webkit 빌드
PS4 Webkit은 `https://doc.dl.playstation.net/doc/ps4-oss/webkit.html` 이 곳에서 다운 받을 수 있다.

다운을 받은 뒤  열어 보면 다음과 같이 `WebKit-601.2.7-800`과 `WebKit-606.4.6-800` 두 개의 폴더가 있음을 확인 할 수 있다. (8.00 기준)

<img width="278" alt="webkit" src="https://user-images.githubusercontent.com/47859343/101600855-3adf5e80-3a3f-11eb-95d7-a170b238a0dc.png">

추정상 JSTest와 LayoutTest로 분류해 둔거 같다. 또한 606 version만 빌드가 되고, GTK는 아예 빌드가 안 된다. 그 외에 JSC 빌드는 기존 Webkit과 똑같다. 

### 2.5. Docker 환경
[여기](https://hub.docker.com/r/gustjr1444/webkit/tags?page=1&ordering=last_updated)에 들어가면 그동안 우리가 취약점 분석을 위해 구축해둔 Webkit Docker 환경들을 다운 받을 수 있다. 여러 CVE 취약점 발생 환경부터, Webcore 분석 , ps4 Webkit 들을 구축해 두었으니, 활용하면 좋을 것 같다.

## 3. PS4 WebKit의 특징
### 3.1. NO JIT
Browser exploit 에서 주로 사용하는 기법이 JIT을 활용해서 fake object 와 RWX 메모리 영역을 만들어서 공격을 시도하는 것인데 해당 PS4의 브라우저에서는 JIT이 꺼져있다.

<img width="1639" alt="스크린샷 2020-12-09 오후 7 43 46" src="https://user-images.githubusercontent.com/47859343/101619723-011a5200-3a57-11eb-9e6e-d2813fca28fb.png">

다음과 같이 UART LOG로 확인해 보면 JIT이 비활성화 되있는 것을 알 수 있다.

### 3.2. NO Garbage Collector
JIT과 마찬가지로 browser exploit에서 활용되는 Garbage Collector도 PS4에서 꺼져있다.

<img width="732" alt="스크린샷 2020-12-09 오후 7 44 04" src="https://user-images.githubusercontent.com/47859343/101620296-b4834680-3a57-11eb-830f-620004bc519d.png">

마찬가지로 UART LOG를 보면 꺼져있음을 확인 할 수 있다.

### 3.3. NO WASM
WebAssembly 또한 PS4 브라우저에서 지원을 안한다. 다음과 같이 WebAssembly 객체를 만들 때 오류가 발생하면 alert로 메세지를 띄우게끔 테스트를 하면,

```javascript
<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
    <script>
        try{
          var memory = new WebAssembly.Memory({initial:10, maximum:100});
        }catch(error){
          alert(error);
        }
    </script>
  </body>
</html>
```

![nowasm](https://user-images.githubusercontent.com/47859343/101623898-73d9fc00-3a5c-11eb-85b9-52b1717e9d80.jpeg)

PS4에서 오류가 발생하여 `"ReferenceError: Can't find variable: WebAssembly"`이 출력 되는 것을 확인 할 수 있다. 즉, WebAssembly가 없다.

## 4. PS4 WebKit exploit 방법론
### 4.1. Return Oriented Programming, Jump Oriented Programming

(작성 중)

## 5. Sanitizer
### 5.1. 개요
Sanitizer는 버그를 감지해 주는 도구이다. 종류에 따라 탐지할 버그의 대상이 달라지며, 목적에 맞게 사용할 수 있다. 일반적으로 clang을 이용하여 컴파일을 할 때 Sanitizer 관련 플래그를 함께 입력해 주면 Sanitizer를 쉽게 붙일 수 있다.

#### 5.1.1. AddressSanitizer(ASan)
buffer-overflow 및 heap use-after-free를 포함한 메모리 액세스 버그는 C 및 C++과 같은 프로그래밍 언어의 심각한 문제로 남아 있다. AddressSanitizer는 힙, 스택 및 전역 객체에 대한 out-of-bounds 액세스와 use-after-free 버그를 탐지해 주는 도구이다.<sup id="head1">[1](#foot1)</sup>

#### 5.1.2. MemorySanitizer(MSan)
MemorySanitizer는 초기화 되지 않은 변수를 읽는 경우를 탐지해 주는 도구이다.<sup id="head2">[2](#foot2)</sup>

#### 5.1.3. UndefinedBehaviorSanitizer(UBSan)
UndefinedBehaviorSanitizer는 undefined behavior를 탐지하는 빠른 도구이다. 컴파일 타임에 프로그램을 수정하며 프로그램 실행 중 정의되지 않은 다양한 행위들을 포착한다.<sup id="head3">[3](#foot3)</sup>

### 5.2. 빌드
WebKit 같은 경우는 빌드를 할 때 perl 기반의 스크립트를 이용하게 된다. 또한 스크립트 중에서 빌드 환경설정을 해주는 스크립트가 존재하는데, 여기에서 Sanitizer 옵션을 줄 수 있다. (아래 명령어 참고<sup id="head4">[4](#foot4)</sup>)
```bash
./Tools/Scripts/set-webkit-configuration --release --asan
./Tools/Scripts/build-webkit
```
-  `build-webkit` : WebKit 빌드 스크립트
-  `set-webkit-configuration` : WebKit 빌드 환경설정 스크립트
-  release/debug는 자유롭게 선택할 수 있다.

이제 각 Step 별로 Sanitizer를 붙여서 빌드를 시도해 볼 차례이다.

> **Environment** : Ubuntu 18.04 64bit

#### 5.2.1. Step 1 : 컴파일 플래그 설정
컴파일 플래그를 설정할 수 있는 파일은 `/webkit/Source/cmake/WebKitCompilerFlags.cmake`이다. 이 파일의 내용을 수정하여 우리가 원하는 Sanitizer를 붙일 수 있다. 참고로 최신 버전의 `WebKitCompilerFlags.cmake` 에는 address, undefined, thread, memory, leak과 같은 flag를 적용할 수 있게끔 분기 로직이 존재한다. (아래 코드 참고)
```javascript
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

```javascript
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
```c
WEBKIT_PREPEND_GLOBAL_COMPILER_FLAGS(-fno-omit-frame-pointer -fno-optimize-sibling-calls)
``` 
버전에 따라 다를 수 있겠지만 2018-12-16 기준으로는 `WebKitCompilerFlags.cmake`에서 위 코드의 인자를 다른 옵션으로 변경해 주었다.

- AddressSanitizer(ASan) : `-fsanitize=address`
  - Option : 디폴트가 ASan이므로 따로 지정해 주지 않아도 된다.
- MemorySanitizer(MSan) : `-fsanitize=memory`
  - Option : `-fno-omit-frame-pointer -fsanitize-memory-track-origins`
- UndefinedBehaviorSanitizer(UBSan) : `-fsanitize=undefined`

#### 5.2.2. Step 2 : 빌드 환경설정
```bash
./Tools/Scripts/set-webkit-configuration --release --asan
```
모든 옵션을 변경했다면 Asan 빌드를 활성화 해야 한다. release/debug는 자유롭게 선택하면 된다. 해당 작업을 해줘야 Sanitizer를 붙여서 빌드가 되고, 그 과정에서 원래는 Asan이 적용되어야 했던 부분이 우리가 원하는 Sanitizer로 변경될 것이다.

#### 5.2.3. Step 3 : clang 빌드
만약 우분투에서 해당 작업을 수행한다면 디폴트로 gcc 컴파일러를 통해 빌드가 될 것이다. 아쉽게도 gcc에서 `-fsanitize=MemorySanitizer`로 빌드시 에러가 발생한다. 이러한 옵션은 clang 컴파일러를 이용해야 하는데 환경변수로 기본 컴파일러를 지정해 주면 간단히 해결되는 문제이다.
```bash
export CC=/usr/bin/clang
export CXX=/usr/bin/clang++
```
컴파일러가 clang으로 잘 세팅 되었는지, ASan 빌드가 잘 활성화 되었는지 확인하기 위해서는 `CMakeCache.txt` 파일을 확인해 보면 된다.
```bash
❯ pwd
/home/lee/WebKit/WebKitBuild/Release
❯ code CMakeCache.txt
```
```c
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

#### 5.2.4. Step 4 : 트러블슈팅
아마도 빌드는 한 번에 되지 않을 것이다. `Could NOT find Threads (missing: Threads_FOUND)` 이런 메시지가 뜨면서 빌드에 실패할 수 있다. 이 경우 가장 최상위 디렉토리에 존재하는 `CMakeLists.txt` 파일을 수정해 주면 된다.
```bash
❯ pwd
/home/lee/WebKit
❯ code CMakeLists.txt
```
오류가 나는 부분이 로그에 남을텐데 해당 라인 넘버로 이동한 후 그 위에 4줄의 코드를 추가해 주면 된다.
```bash
set(THREADS_PREFER_PTHREAD_FLAG ON) // Where the error occurred
```
```javascript
//////////////// Added //////////////////
set(CMAKE_THREAD_LIBS_INIT "-lpthread")
set(CMAKE_HAVE_THREADS_LIBRARY 1)
set(CMAKE_USE_WIN32_THREADS_INIT 0)
set(CMAKE_USE_PTHREADS_INIT 1)
/////////////////////////////////////////

set(THREADS_PREFER_PTHREAD_FLAG ON)
```
#### 5.2.5. Step 5 : 테스트
마지막으로 PoC를 테스트해보거나 `testmasm` 바이너리를 한 번 실행해 보자.
```bash
# Built with --jsc-only
❯ pwd
/home/lee/WebKit/WebKitBuild/Release/bin
❯ ./testmasm
```
![msan](https://user-images.githubusercontent.com/45416961/101595740-3adb6080-3a37-11eb-815c-8a8727ee3ee4.png)
위와 같이 메시지가 뜨면 빌드에 성공한 것이다. 만약 위 사진처럼 출력되지 않는다면 `CMakeCache.txt` 파일을 보면서 컴파일러나 Asan enable 설정이 잘 되었는지 점검해 보자.

### 5.3. 문제점
> Asan 이외의 Sanitizer는 이용할 수 없을 정도로 매우 불안정하다.

![image](https://user-images.githubusercontent.com/45416961/101624586-7a1ca800-3a5d-11eb-8193-689541296010.png)
아마 옛날 버전의 WebKit을 사용해서 그런 것일지도 모르겠다.*(본 프로젝트에서는 WebKit 최신 버전을 이용할 일이 없어서 빌드를 해보지 않았다.)* 2018-12-16 버전으로 Msan이나 UBSan을 붙여서 테스트를 해봤더니 오탐률이 거의 100%에 육박했다. 소위 말해 '개복치' 스럽다고도 할 수 있겠다. jsc에서 `print("hello world")`만 해줘도 Memory Leak이 발생하니 그 결과가 가히 실망스럽다. 

## 6. 1-day 취약점 분석 방법론
다음으로는 본 프로젝트에서 1-day 취약점을 분석하기 위해 수립 및 시행한 방법론을 소개하고자 한다.
### 6.1. Chromium
![image](https://user-images.githubusercontent.com/45416961/101621717-771fb880-3a59-11eb-9eca-bce3ecbad852.png)
![image](https://user-images.githubusercontent.com/45416961/101621198-c9aca500-3a58-11eb-9b20-12056b95fa12.png)
가장 먼저 [Chromium](https://bugs.chromium.org/p/project-zero/issues/list?sort=-reported&q=webkit&can=1)에서 Project-zero 팀이 report 한 취약점들을 분석하고, PS4에 포팅하고, 코드 오디팅을 수행했다. 거의 모든 취약점들을 테스트해보았지만 이미 패치가 되었거나, PoC에 사용되는 모듈이 PS4에는 존재하지 않는 경우가 대부분이었다. 특히 JSC 취약점은 대개 JIT 컴파일러를 기반으로 하기 때문에 별다른 수확은 없었다.

### 6.2. exploit-db
![image](https://user-images.githubusercontent.com/45416961/101621658-6707d900-3a59-11eb-8f9a-000d03573bc7.png)
[exploit-db](https://www.exploit-db.com/) 또한 Chromium과 함께 초반에 취약점을 찾고자 부단히 방문했던 사이트이다. 아무래도 이미 존재하는 exploit들을 모아 놓은 사이트이기 때문에 Chromium에서 이미 봤던 코드들이 대부분이었고, 비교적 최신 exploit은 존재하지 않았다. 결론적으로 exploit-db에서도 원하는 바를 달성하지는 못했다.

### 6.3. Bugzilla
![image](https://user-images.githubusercontent.com/45416961/101606281-89dcc200-3a46-11eb-9fa9-0e962243c136.png)
[WebKit Bugzilla](https://bugs.webkit.org/)에 report 되는 버그들을 모니터링 하면서 실제로 exploit에 사용될만한 취약점이 있는지 탐색할 수 있다. 다만 간단한 description과 패치 내역만 보고 특정 버그가 exploitable한지 판단할 수 있는 경험치가 요구된다. 그리고 Security issue의 경우 일반 사용자들에게 액세스 권한을 주지 않는 경우가 많다. 따라서 Bugzilla만 살펴보면서 취약성이 존재하는 케이스를 찾아내기란 모래알 속 진주 찾기와도 같다. 물론 시작하는 단계에서는 말이다.
### 6.4. WebKit regression test
> 아직 경험치가 많이 부족하다면 ChangeLog가 버그 탐색을 위한 좋은 입문 경로가 될 수 있다.

WebKit repositorty를 조금만 들여다 보면 ChangeLog 상에 패치 내역이 아주 잘 정리되어 있다는 사실을 알 수 있다. `JSTests, LayoutTests` 디렉토리는 JavaScriptCore와 WebCore 각각에 대한 테스트 코드를 담고 있는데, 물론 이 폴더 내부에도 ChangeLog가 존재한다. ChangeLog의 패턴을 살펴보고 넘어가자.
```
2020-10-28  Robin Morisset  <rmorisset@apple.com>

  DFGIntegerRangeOptimization is wrong for Upsilon (as 'shadow' nodes are not in SSA form)
  https://bugs.webkit.org/show_bug.cgi?id=218073

  Reviewed by Saam Barati.

  The only testcase I managed to get for this bug loops forever when not crashing.
  So I use a 1s timeout through --watchdog=1000.

  * stress/bounds-checking-in-cold-loop.js: Added.
  (true.vm.ftlTrue):
```
취약점에 대한 간략한 설명 및 Bugzilla 주소, 그리고 해당 버그를 테스트 하기 위한 Regression test 코드의 경로까지 상세히 기술되어 있다. 이 패턴을 이용하여 테스트 코드만 뽑아내면 탐색 범위를 상당히 줄일 수 있을 것으로 판단했다. 그래서 자동화 스크립트를 작성한 후 코드 수집 및 테스트까지 일사천리로 진행했다.
처음에는 ASan을 붙여서 빌드한 WebKit GTK 미니브라우저에서 로그들을 수집한 후 에러가 발생한 케이스들만 분석을 진행했다. 하지만 대부분이 Null Dereferencing이나 exploit에 사용하기는 애매한 취약점들이었고, 또 Sony 측에서 자체적으로 패치를 진행한 경우들이 대부분이었다. 그래서 ASan 로그 상에서 별다른 반응이 없었던 경우들에 대해서도 패치 개핑을 하면서 분석 과정을 이어 나갔다.

![image](https://user-images.githubusercontent.com/45416961/101624972-1e065380-3a5e-11eb-943e-2a6ed5273672.png)
![image](https://user-images.githubusercontent.com/45416961/101624881-f911e080-3a5d-11eb-98da-c4ceef700f57.png)

그러던 도중 WebCore 엔진에서 pc 레지스터 컨트롤이 가능한 취약점 하나를 발견할 수 있었다. 6.72 버전에서 디버깅을 통해 레지스터 값이 임의의 값으로 변경되는 것을 확인했고, 8.01 버전에서도 레지스터 값을 확인할 순 없었지만 에러 반응이 나타나는 것을 볼 수 있었다. 다만 해당 취약점 하나만으로는 exploit을 할 수 없기에 info leak 취약점을 탐색해야만 했다. 프로젝트 기간 동안 쓸만한 info leak 취약점은 발견하지 못했다. 비록 프로젝트는 끝났지만 Future work로 시도해보면 좋을 것 같다.

## 7. Reference
><b id="foot1">[[1](#head1)]</b> Konstantin Serebryany; Derek Bruening; Alexander Potapenko; Dmitry Vyukov. ["AddressSanitizer: a fast address sanity checker"(PDF)](https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf). Proceedings of the 2012 USENIX conference on Annual Technical Conference.<br>
><b id="foot2">[[2](#head2)]</b> [MemorySanitizer - Clang 12 Documentation](https://clang.llvm.org/docs/MemorySanitizer.html)<br>
><b id="foot3">[[3](#head3)]</b> [UndefinedBehaviorSanitizer - Clang 12 Documentation](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html)<br>
><b id="foot4">[[4](#head4)]</b> [Building WebKit with Clang Address Sanitizer(ASan)](https://trac.webkit.org/wiki/ASanWebKit)<br>

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