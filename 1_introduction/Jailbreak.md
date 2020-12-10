### Page Contents <!-- omit in toc -->
- [1. 개요](#1-개요)
  - [1.1. 주의사항](#11-주의사항)
- [2. Jailbreak를 통해 무엇을 할 수 있는가](#2-jailbreak를-통해-무엇을-할-수-있는가)
  - [2.1. 임의의 binary 실행](#21-임의의-binary-실행)
  - [2.2. PS4 내 파일 탐색](#22-ps4-내-파일-탐색)
  - [2.3. UART Log 활성화](#23-uart-log-활성화)
- [3. Reference](#3-reference)

---
# Jailbreak <!-- omit in toc -->
## 1. 개요
Jailbreak란, 프로그램의 취약점을 이용하여 PS4의 높은 권한을 획득하여 기존의 서비스에서는 사용할 수 없는 기능을 사용할 수 있게 되는 것을 일컫는다. PS4의 경우, 브라우저의 취약점과 커널의 취약점을 chaining하여 Jailbreak를 하는 경우가 일반적이다. PS4는 WebKit기반의 browser를 사용하고, FreeBSD 9 기반의 OS인 Orbis OS를 사용한다.<br>
2020년 12월 9일 기준, PS4 펌웨어는 8.01까지 업데이트가 된 상황에서 Jailbreak는 PS4 펌웨어 6.72버전까지 진행이 되었다. sleirsgoevy가 6.72 Jailbreak 도구를 만들었으며 소스코드는 [여기](https://github.com/sleirsgoevy/ps4jb)에서 확인할 수 있다. Jailbreak된 PS4 펌웨어 버전 및 취약점에 대한 자세한 내용은 [PS4 developer wiki](https://www.psdevwiki.com/ps4/Working_Exploits)를 참고하면 된다.

### 1.1. 주의사항
> PS4 펌웨어 6.72버전을 기준으로 기술이 되어있다. **본 프로젝트의 목적은 PS4의 취약점을 탐색하여 최신 펌웨어에서의 Jailbreak 가능성을 확인하고 이를 패치하여 PS4 플랫폼 위에 형성되어있는 지식재산들을 보호하는 것이 목적으로, Jailbreak를 악용하는 것이 아님을 밝힌다.** 위 목적을 달성하기 위해서 참고했던 자료 및 도구들을 본 문서에 기술한다. **본 프로젝트에서 참고한 Jailbreak 도구의 악용을 통해 발생하는 불이익에 대해서 본 프로젝트 팀원들은 책임을 지지 않을 것을 분명하게 밝힌다.**

## 2. Jailbreak를 통해 무엇을 할 수 있는가
Jailbreak를 통해 어떤 기능들을 사용할 수 있는지 살펴보기 위해 6.72 Jailbreak를 진행했다. [유튜브 영상](https://www.youtube.com/watch?v=ycZg0fViWv4)을 참고하여 진행했다. Jailbreak 사이트에 접속하면 아래와 같이 여러가지 기능들이 있는데, 그 중 분석에 도움이 되는 몇가지를 소개하려고 한다.<br>
![jailbreak](https://user-images.githubusercontent.com/40509850/101586509-fec5e280-39d9-11eb-9012-09aa04601f6d.PNG "그림 1 Jailbreak 기능")

### 2.1. 임의의 binary 실행
Bin Loader 기능을 이용하여 임의의 binary payload를 PS4에서 실행할 수 있다. Bin Loader를 실행시킨 후, `nc -w 3 (PS4's ip) 9021 < (bin payload)`를 통해 Bin Loader에 binary파일을 전달하면 해당 payload가 동작한다. sleirsgoevy의 Jailbreak 도구에 있는 [8cc](https://github.com/sleirsgoevy/ps4-rop-8cc)를 이용하여 임의의 payload를 bin loader로 load가능한 bin파일을 만드는 것도 가능하다. 그러나 binary파일의 크기는 65536byte를 넘어가면 안된다.<sup id="head1">[1](#foot1)</sup>

### 2.2. PS4 내 파일 탐색
FTP 기능을 이용하면, FTP가 활성화 되면서 1337 Port가 열리게 된다. 해당 Port로 접속하면 PS4 내부의 파일 시스템을 탐색할 수 있다. [FileZilla](https://filezilla-project.org/)와 같은 프로그램을 사용하면 편리하게 접속이 가능하다. 그러나 라이브러리 및 binary 파일들이 암호화가 되어있는 것으로 여겨져 binary 파일을 바로 사용할 수는 없는 것으로 여겨진다.

### 2.3. UART Log 활성화
Mira 기능을 이용하면, PS4의 설정창에 Debug Settings가 해금이 되며 여러 개발자 도구를 사용할 수 있게 되는 동시에 UART Log가 활성화된다. 하드웨어상에 존재하는 UART 포트를 연결하여 UART Log를 볼 수도 있지만, UART Log를 출력해주는 Port가 열리기 때문에 해당 Port에 접속하면 Log를 볼 수 있다. UART Log를 볼 수 있는 Port는 9998로, `nc (PS4's IP) 9998`을 통해 볼 수 있다. PS4의 IP는 `설정 > 시스템 > 시스템 정보`에서 확인할 수 있다.<br>
UART Log를 통해 PS4에 연결된 하드웨어 정보, 게임 타이틀 코드 등 여러가지 디버깅 정보를 획득할 수 있는데, 흥미로운 점은 **Segmentation fault와 같은 crash가 날 경우, 아래와 같이 register 정보, backtrace 등 디버깅에 필요한 정보를 역시 출력해주기 때문에 분석에 용이하다.**

```
# A user thread receives a fatal signal
#
# signal: 5 (SIGTRAP)
# thread ID: 100862
# thread name: SceNKWebProcessMain
# proc ID: 66
# proc name: SceNKWebProcess
# reason: breakpoint instruction fault
#
# registers:
# rax: 00000002005bc000  rbx: 0000000201480550
# rcx: 0000000881558040  rdx: 0000000809481580
# rsi: 0000000000000001  rdi: 0000000000000000
# rbp: 00000007ef7c1ee0  rsp: 00000007ef7c1ed0
# r8 : 0000000200fe8ee4  r9 : 0000000000000001
# r10: 0000000000000080  r11: 0000000000000008
# r12: 0000000201480420  r13: 00000002014e0110
# r14: 0000000201480550  r15: 00000007ef7c49b0
# rip: 0000000815196b88  eflags: 00000246
# BrF: 0000000815196b42  BrT: 0000000815196b87
#
# backtrace:
copyin: SceNKWebProcessMain has nonsleeping lock
# 0000000814f5353b
# 00000008153d8beb
# 000000081493bd14
# 00000008140497d2
# 00000008149de9f7

... 중략 ...

# dynamic libraries:
# /bennmJ6ZWb/common/lib/NKWebProcess.self
#  text: 0000000079d40000:0000000079d48000 r-x
#  data: 000000007a140000:000000007a144000 rw-
#  fingerprint: 25fa2728c3de0a491e2f65a8e5d0f00200000000
# /bennmJ6ZWb/common/lib/libkernel_web.sprx
#  text: 000000080904c000:00000008090a0000 r-x
#  data: 000000080944c000:0000000809484000 rw-
#  fingerprint: a11940857d50c63dcc3c02c69afe729c00000000
# /bennmJ6ZWb/common/lib/libSceLibcInternal.sprx
#  text: 000000080d620000:000000080d74c000 r-x
#  data: 000000080da20000:000000080da34000 rw-
#  fingerprint: cbb57d1ff1767695f2f694455463cd9b00000000
# /bennmJ6ZWb/common/lib/libSceSysmodule.sprx
#  text: 0000000800914000:0000000800920000 r-x
#  data: 0000000800d14000:0000000800d20000 rw-
#  fingerprint: 00f67b8129f5d886f22b5a948c91e94a00000000

... 후략 ...
```
## 3. Reference
><b id="foot1">[[1](#head1)]</b> [Bin Loader binary length limit](https://github.com/sleirsgoevy/ps4jb/blob/73a8e6d8ea3c142c1b11b368935c3a51a1b14358/src/miraldr.c#L41)


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
