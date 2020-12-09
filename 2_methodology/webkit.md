#<strong>개요</strong>

1. Webkit 이란?
####1. Webkit 이란?

APPLE 에서 개발한 Safari, Chrome 등의 브라우저에서 사용되는 Open Source 렌더링 엔진이다. PS4 내부 브라우저에서도 Webkit을 사용한다. 그렇기에 우리는 해당 PS4의 웹킷을 attack vector로 삼았다.

그러나 Webkit에서 User-Agent에 나오는 버전을 <strong>Freezing</strong> 하고 있어서 정확한 버전을 확인 할 수 없었고, PS4 Webkit ChangeLog를 확인해 보니 2018-12-16 이후로 SONY에서 자체적으로 fork를 떠 커스터마이징 한 것으로 추정 된 다.

#<strong>WebKit 빌드</strong>
1. Webkit download
2. JSC 빌드
3. GTK 빌드
4. PS4 Webkit 빌드

####1. Webkit download

https://github.com/WebKit/webkit.git

다음 링크는 Webkit github 링크이다.
 `git clone https://github.com/WebKit/webkit.git` 통해 Webkit을 다운 받을 수 있다.

이후 분석하고자 하는 version으로 git checkcout 해주면 된다.

참고로 다음 Webkit을 빌드하기전에 다음 프로그램들이 사전에 설치되어 있어야 한다.

`cmake`
`ruby`
`libicu-dev`

####2. JSC 빌드

빌드 명령어는 다음과 같다.
`./webkit/Tools/Scripts/build-webkit --jsc-only --debug`

`jsc-only` : jsc만 빌드함
`debug` : debug 모드로 빌드함 ( debug 옵션이 없으면 나중에 분석 할 때 describe라는 객체 등의 주소를 알어오는 함수를 못 사용함 )
