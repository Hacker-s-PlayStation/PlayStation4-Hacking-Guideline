- [1. Hacking the PS4<sup id="head1">1</sup>](#1-hacking-the-ps4sup-idhead11sup)
  - [1.1. 요약](#11-요약)
- [2. THIS IS FOR THE PWNERS: EXPLOITING A WEBKIT 0-DAY IN PLAYSTATION 4](#2-this-is-for-the-pwners-exploiting-a-webkit-0-day-in-playstation-4)
  - [2.1. 요약](#21-요약) 
  - [2.2. 차이점](#22-차이점) 
- [3. Reference](#3-reference)



---

# Related_Work <!-- omit in toc -->

## 1. Hacking the PS4<sup id="head1">[1](#foot1)</sup>

### 1.1. 요약
CTurt가 작성하였으며, WebKit 취약점을 PS4에 포팅하는 것을 맨 처음 시도하였으며, 해당 글에서는 WebKit exploit 부터 Kernel Exploit까지 Full Chain Exploit한 것을 자세하게 기술하였다. 

CTurt는 웹킷 취약점 과 Kernel 취약점 모두 우리가 채택한 방법론과 같이 1-day를 PS4에 포팅하여 진행하였다. CTurt와 다른 점이 있다면 우리는 1-day를 통해 최신 버전 펌웨어 Exploit하는 것을 목표로 진행하였고 CTurt는 구버전 PS4를 목표로 진행하였다. 웹킷에서는 2012년에 패치된 힙 버퍼 오버플로우 취약점을 PS4에 포팅해서 Exploit하였고, 커널은 2014년에 패치된 Linux에서 발생한 BadIRET 취약점이 FreeBSD에도 똑같이 작용해서 이를 PS4에 포팅하여 Exploit 하였다.

이렇듯 과거의 취약점이 PS4에서는 패치되지 않은 부분이 있었기 때문에 우리는 CTurt와 다르게 1-day 취약점을 찾아 PS4를 Exploit하는 방법론을 채택하였다. 이 과정에서 우리는 이미 웹킷에서는 패치된 취약점이지만, 글을 작성하는 시점인 2020-12-12 기준으로 최신 버전인 PS4 8.01 버전 웹킷에서 PC Controll이 가능한 UAF 취약점을 찾아냈다.

CTurt가 작성한 글은 상당히 오래전에 작성된 것이긴 하지만 PS4 exploit을 처음 접하는 사람들에게는 좋은 글이니 읽어보는 것을 추천한다.

## 2. THIS IS FOR THE PWNERS: EXPLOITING A WEBKIT 0-DAY IN PLAYSTATION 4

### 2.1. 요약

2020년도 Black hat 컨퍼런스에서 발표된 PS4 0-Day exploit 관련 문서이다. 
<br>
해당 문서에서의 취약점은 fuzzer에 의해 발견 되었다. `ValidationMessage` 레이아웃 업데이트 중에 인스턴스를 계속 삭제시킬수 있는 문제였고, exploit은
`WebCore::ValidationMessage::buildBubbleTree` 에서 발생하는 Use-After-Free 취약점 및 heap spay를 사용한다. 또한 FreeBSD를 설치하고, Webkit PS4를 다운 받아 빌드하여 PS4 환경에 최대한 가깝게 구축하여야 한다.


<br>
해당 취약점을 사용하기 위해 ASLR 우회가 필요하고, 6.xx 버전 대 Firmware(이하 FW) 에서는 이전에 알려진 `bad-hoist`취약점에서 메모리 매핑 사용 부분이 있었기 때문에 html object Leak을 할 수 있었다. (그러나 이는 6.xx 버전 대 에서만 동작 하였기 때문에, 7.xx 버전 대 FW 에서는 brute force를 시도하여 객체의 주소 값을 찾아 내었다.)
<br>
이후 객체를 재사용하기 위해 대상 객체 할당 직전과 직후에 ValidationMessage(48 byte) 크기의 객체를 spray 한다. 이후 ValidationMessage 인스턴스와 주변 객체를 free 하여 smallPage에 캐시한다. 그리고 대상 객체와 같은 크기의 객체를 heap 에 다시 spray 해준다. 

<br>

그 후, `JSArrayBufferView` 객체의 주소를 leak 해서 해당 주소의 길이 필드를 손상 시켜 R/W 프리미티브를 설정한다. 그 다음 `JSArrayBufferView`객체의 데이터 버퍼 참조 필드를 손상 시켜 ARBITRARY R/W를 활성화 시킨다. 이후 vtable 값을 덮어 `HTMLTextAreaElement`의 제어하는 포인터를 가리키게 하고, 호출하여 제어하는 주소에 대한 호출을 발생시켜 이후 다음 단계를 구현 하기 위해 ROP, JOP를 수행한다.
해당 exploit은 [Synacktiv의 Github 저장소](https://github.com/synacktiv/PS4-webkit-exploit-6.XX)에서 확인 할 수 있다.

<br>

6.xx 버전 대 에서는 exploit을 성공하였지만, 7.xx 버전에서는 위에서 말한 이유로 좋은 결과를 얻지 못하였다.

<br>

### 2.2 차이점
우리의 프로젝트는 1-Day 취약점 탐색을 목표로 진행하였지만, Black Hat 에서 발표된 내용은 0-Day 를 연구해서 exploit을 진행하였다. 또한 본 문서에서는 환경구성을 할때 freeBSD 내부에다가 PS4 Webkit을 구축하여 최대한 PS4와 유사한 환경에서 분석을 진행했지만, 본 프로젝트는 PS4 Webkit의 ChangeLog를 이용해서 fork를 진행한 시점을  유추하여 checkout 한 후, 1-day 테스트를 진행하였다.

## 3. Reference
<b id="foot1">[[1](#head1)]</b> [Hacking the PS4](https://cturt.github.io/ps4.html)<br>
<b id="foot2">[[2](#head2)]</b> [THIS IS FOR THE PWNERS: EXPLOITING A WEBKIT 0-DAY IN PLAYSTATION 4](https://www.synacktiv.com/publications/this-is-for-the-pwners-exploiting-a-webkit-0-day-in-playstation-4.html)<br>



### Contents <!-- omit in toc -->
[메인화면](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/README.md)<br>

#### PS4 소개 <!-- omit in toc -->
[1. Jailbreak](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/1_introduction/Jailbreak.md)<br>
[2. PS4 Open Source](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/1_introduction/PS4_Open_Source.md)<br>
[3. Tools](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/1_introduction/Tools.md)<br>
[4. Related_Work](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/1_introduction/Related_Work.md)<br>

#### 프로젝트 접근 방법론 <!-- omit in toc -->
[1. WebKit](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/2_methodology/WebKit.md)<br>
[2. Hardware](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/2_methodology/Hardware.md)<br>
[3. Library](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/2_methodology/Library.md)<br>

#### 결론 <!-- omit in toc -->
[결론](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/3_conclusion/Conclusion.md)
