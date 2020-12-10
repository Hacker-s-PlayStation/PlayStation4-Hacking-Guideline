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


# <strong>개요</strong>

1. Webkit 이란?
#### 1. Webkit 이란?

APPLE 에서 개발한 Safari, Chrome 등의 브라우저에서 사용되는 Open Source 렌더링 엔진이다. PS4 내부 브라우저에서도 WebKit을 사용한다. 그렇기에 우리는 해당 PS4의 웹킷을 attack vector로 삼았다.

그러나 WebKit에서 User-Agent에 나오는 버전을 <strong>Freezing</strong> 하고 있어서 정확한 버전을 확인 할 수 없었고, PS4 WebKit ChangeLog를 확인해 보니 <strong>2018-12-16</strong> 이후로 SONY에서 자체적으로 fork를 떠 커스터마이징 한 것으로 추정된다. <span id="webkit">PS4 Webkit은 [이 곳](https://doc.dl.playstation.net/doc/ps4-oss/webkit.html)에서 다운 받을 수 있다.</span>

## 2. WebKit 빌드
### 2.1. WebKit download

다음 명령어를 통해 Webkit 소스 코드를 다운 받을 수 있다.
 ```bash
 git clone git://git.webkit.org/WebKit-https.git WebKit
 ```

이후 분석하고자 하는 version으로 git checkcout 해주면 된다.
해당 실습은 2018-12-16일 기준으로 checkout을 했고, 우분투 18.04로 진행 하였다.
```bash
git log --before="2018-12-16"
```

참고로 다음 Webkit을 빌드하기전에 다음 프로그램들이 사전에 설치되어 있어야 한다.

```bash
sudo apt install cmake ruby libicu-dev gperf ninja-build
```

또한 version에 따라 설치에 필요한 것들이 다를 수 있으니 그때마다 설치해 주어야 한다.

#### 2. JSC 빌드
JSC 빌드 명령어는 다음과 같다. 
```bash
./webkit/Tools/Scripts/build-webkit --jsc-only --debug
```

- `jsc-only` : jsc만 빌드함
- `debug` : debug 모드로 빌드함 (debug 모드가 아니면 나중에 분석 할 때 `describe`라는 객체 등의 주소를 알아오는 함수를 사용할 수 없다.)

이후 빌드에 성공하면 다음과 같이 JSC를 실행하면 command line 이 뜨는 것을 확인 할 수 있다.

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

다음 명령어 실행 뒤 [xdg-dbus-proxy](https://github.com/flatpak/xdg-dbus-proxy) 와 [bwrap 0.3.1](https://launchpad.net/ubuntu/+source/bubblewrap/0.3.1-1ubuntu1) 도 설치해주어야 한다.


다음 링크들을 참고하여 설치한 뒤 `/webkit/Source/WebKit/UIProcess/gtk/WaylandCompositor.cpp` 파일에 `#include <EGL/eglmesaext.h>` 헤더를 한 줄 추가해야 한다. EGL_WAYLAND_BUFFER_WL이 없다는 오류가 뜰 수 있기 때문이다.

모든 선수 작업을 마무리 한 뒤
```
./webkit/Tools/Scripts/build-webkit --gtk
```
 위 명령어를 실행하면 된다. ( 실행 할 때 RAM 16GB 정도 할당 권장 )

- `debug` : debug 모드로 빌드함 ( debug 모드가 아니면 나중에 분석 할 때 describe라는 객체 등의 주소를 알어오는 함수를 못 사용함 )
- `gtk` : gtk 모드로 빌드함

빌드가 되고 난 뒤 다음 명령어를 치면 
```bash
./webkit/Tools/Scripts/run-minibrowser --gtk
```

<img width="800" alt="스크린샷 2020-12-10 오전 10 21 20" src="https://user-images.githubusercontent.com/47859343/101708875-8cd0c480-3ad1-11eb-929e-ab7b1fafb79f.png">

다음과 같이 minibrowser가 실행됨을 알 수 있다. 만약 index.html을 미니 브라우저에서 실행시키고 싶으면

```bash
./webkit/Tools/Scripts/run-minibrowser --gtk index.html
``` 

다음과 같이 뒤에 index.html을 붙이면 된다.

### 2.4. PS4 Webkit 빌드
서론에서 [언급](#webkit)했던 PS4 WebKit을 다운 받은 뒤 열어 보면 다음과 같이 `WebKit-601.2.7-800`과 `WebKit-606.4.6-800` 두 개의 폴더가 있음을 확인 할 수 있다. (8.00 기준)

<img width="278" alt="webkit" src="https://user-images.githubusercontent.com/47859343/101600855-3adf5e80-3a3f-11eb-95d7-a170b238a0dc.png">

추정상 JSTest와 LayoutTest로 분류해 둔 것 같다. [PS4 Dev Wiki](https://www.psdevwiki.com/ps4/Working_Exploits#JiT_removed_from_webbrowser)에 1.76이후 두개의 프로세스로 분할 되었다는 내용이 언급되어 있다.
> On FW <= 1.76, you could map RWX memory from ROP by abusing the JiT functionality and the sys_jitshm_create and sys_jitshm_alias system calls. This however was fixed after 1.76, as WebKit has been split into two processes. One handles javascript compilation and the other handles other web page elements like image rendering and DOM. The second process will request JiT memory upon hitting JavaScript via IPC (Inter-Process Communication). Since we no longer have access to the process responsible for JiT, we can no longer (at least currently), map RWX memory for proper code execution unless the kernel is patched.

또한, PC 상에서 GTK는 아예 빌드가 안 되고 JSC는 606 version만 빌드가 된다.

### 2.5. Docker 환경
[여기](https://hub.docker.com/r/gustjr1444/webkit/tags?page=1&ordering=last_updated)에 들어가면 그동안 우리가 취약점 분석을 위해 구축해둔 Webkit Docker 환경들을 다운 받을 수 있다. 여러 CVE 취약점, WebCore, ps4 Webkit의 분석을 목적으로 구축해 두었으니, 활용하면 좋을 것 같다.

## 3. PS4 WebKit의 특징
### 3.1. NO JIT
Browser exploit 에서 주로 사용하는 기법이 `JIT`을 활용해서 fake object 와 RWX 메모리 영역을 만들어서 공격을 시도하는 것이다. 그러나 PS4의 브라우저에서는 JIT이 꺼져있다.

<img width="1639" alt="스크린샷 2020-12-09 오후 7 43 46" src="https://user-images.githubusercontent.com/47859343/101619723-011a5200-3a57-11eb-9e6e-d2813fca28fb.png">

다음과 같이 UART LOG로 확인해 보면 JIT이 비활성화 되있는 것을 알 수 있다.

### 3.2. NO Garbage Collector
JIT과 마찬가지로 Browser exploit에서 활용되는 Garbage Collector도 `PS4`에서는 꺼져있다.

<img width="732" alt="스크린샷 2020-12-09 오후 7 44 04" src="https://user-images.githubusercontent.com/47859343/101620296-b4834680-3a57-11eb-830f-620004bc519d.png">

마찬가지로 UART LOG를 보면 꺼져있음을 확인 할 수 있다.

### 3.3. NO WASM
`WebAssembly` 또한 PS4 브라우저에서 지원을 안한다. WebAssembly 객체를 만들 때 오류가 발생하면 alert로 메세지를 띄우게끔 테스트를 해 보았더니,

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

PS4에서 오류가 발생하여 `"ReferenceError: Can't find variable: WebAssembly"`이 출력 되는 것을 확인 할 수 있었다. 확실히 WebAssembly는 없다.

## 4. PS4 WebKit exploit 방법론
### 4.1. Return Oriented Programming, Jump Oriented Programming

(작성 중)
