# <strong>개요</strong>

1. Webkit 이란?
#### 1. Webkit 이란?

APPLE 에서 개발한 Safari, Chrome 등의 브라우저에서 사용되는 Open Source 렌더링 엔진이다. PS4 내부 브라우저에서도 Webkit을 사용한다. 그렇기에 우리는 해당 PS4의 웹킷을 attack vector로 삼았다.

그러나 Webkit에서 User-Agent에 나오는 버전을 <strong>Freezing</strong> 하고 있어서 정확한 버전을 확인 할 수 없었고, PS4 Webkit ChangeLog를 확인해 보니 <strong>2018-12-16</strong> 이후로 SONY에서 자체적으로 fork를 떠 커스터마이징 한 것으로 추정 된 다.

# <strong>WebKit 빌드</strong>
1. Webkit download
2. JSC 빌드
3. GTK 빌드
4. PS4 Webkit 빌드
5. Docker 환경

#### 1. Webkit download

https://github.com/WebKit/webkit.git

다음 링크는 Webkit github 링크이다.
 `git clone https://github.com/WebKit/webkit.git` 통해 Webkit을 다운 받을 수 있다.

이후 분석하고자 하는 version으로 git checkcout 해주면 된다.
해당 실습은 2018-12-16일 a5beb7c88f12c377c3347f74776d2270fbbc79a4 기준 우분투 18.04로 진행 하였다.
<br>

`git checkout a5beb7c88f12c377c3347f74776d2270fbbc79a4`

<br>
참고로 다음 Webkit을 빌드하기전에 다음 프로그램들이 사전에 설치되어 있어야 한다.

<br>

`sudo apt install cmake ruby libicu-dev gperf ninja-build`

또한 version에 따라 설치에 필요한 것들이 다를 수 있으니 그때 마다 설치해 주어야 한다.

<br>

#### 2. JSC 빌드
<br>

JSC 빌드 명령어는 다음과 같다. `./webkit/Tools/Scripts/build-webkit --jsc-only --debug`
<br>

`jsc-only` : jsc만 빌드함
<br>
`debug` : debug 모드로 빌드함 ( debug 모드가 아니면 나중에 분석 할 때 describe라는 객체 등의 주소를 알어오는 함수를 못 사용함 )

<br>
이후 빌드에 성공하면 다음과 같이 JSC를 실행하면 command line 이 뜨는 것을 확인 할 수 있다.
<br>

`./webkit/WebKitBuild/Debug/bin/jsc`
<br>
```
seohojin@ubuntu:~/Desktop$ ./webkit/WebKitBuild/Debug/bin/jsc 
>>> 1+2
3
>>> 
```
<br>

#### 3. GTK 빌드

<br>

GTK를 빌드하기 위해서는 먼저 다음과 같은 선수 작업이 필요하다.
<br><br>

`./webkit/Tools/gtk/install-dependencies`
<br>

`apt install libwoff-dev flatpak flatpak-builder python-pip`
<br>

`pip install pyyaml`

<br>

다음 명령어 실행 뒤 `xdg-dbus-proxy` 와 `bwrap 0.3.1` 도 설치하여 make 해주어야 한다.

<br>

`xdg-dbus-proxy`  : https://github.com/flatpak/xdg-dbus-proxy
<br>

`bwrap 0.3.1` : https://launchpad.net/ubuntu/+source/bubblewrap/0.3.1-1ubuntu1
<br>

다음 링크들을 참고하여 설치한 뒤 `/webkit/Source/WebKit/UIProcess/gtk/WaylandCompositor.cpp` 파일에 `#include <EGL/eglmesaext.h>` 헤더를 한 줄 추가해야 한다. 
<br><br>
EGL_WAYLAND_BUFFER_WL이 없다는 오류가 뜰 수 있기 때문이다.

<br>

다음과 같은 선수 작업을 마무리 한 뒤 `/webkit/Tools/Scripts/build-webkit --gtk --debug` 를 실행하면 된다. ( 실행 할 때 RAM 16GB 정도 할당 권장 )

<br>

`debug` : debug 모드로 빌드함 ( debug 모드가 아니면 나중에 분석 할 때 describe라는 객체 등의 주소를 알어오는 함수를 못 사용함 )
<br>

`gtk` : gtk 모드로 빌드함
<br>

#### 4. PS4 Webkit 빌드

<br>

PS4 Webkit은 `https://doc.dl.playstation.net/doc/ps4-oss/webkit.html` 이 곳에서 다운 받을 수 있다.

<br><br>

다운을 받은 뒤  열어 보면<br>
( 8.00 기준 )

<img width="278" alt="webkit" src="https://user-images.githubusercontent.com/47859343/101600855-3adf5e80-3a3f-11eb-95d7-a170b238a0dc.png">

<br>
다음과 같이 WebKit-601.2.7-800과 WebKit-606.4.6-800 두 개의 폴더가 있음을 확인 할 수 있다.<br><br>

추정상 JSTest와 LayoutTest로 분류해 둔거 같다.
<br>
또한 606 version만 빌드가 되고, GTK는 아예 빌드가 안 된다.<br>
그 외에 JSC 빌드는 기존 Webkit과 똑같다. 

<br>

#### 5. Docker 환경
<br>

`https://hub.docker.com/r/gustjr1444/webkit/tags?page=1&ordering=last_updated` 위 링크에 들가면 그동안 우리가 취약점 분석을 위해 구축해둔 Webkit Docker 환경들을 다운 받을 수 있다.
<br>
여러 CVE 취약점 발생 환경부터, Webcore 분석 , ps4 Webkit 들을 구축해 두었으니, 활용하면 좋을 것 같다.