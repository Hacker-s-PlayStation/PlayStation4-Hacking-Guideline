- [1. Hacking the PS4<sup id="head1">1</sup>](#1-hacking-the-ps4sup-idhead11sup)
  - [1.1. 요약](#11-요약)
- [2. THIS IS FOR THE PWNERS: EXPLOITING A WEBKIT 0-DAY IN PLAYSTATION 4](#2-this-is-for-the-pwners-exploiting-a-webkit-0-day-in-playstation-4)
- [3. Reference](#3-reference)

---

# Related_Work <!-- omit in toc -->

## 1. Hacking the PS4<sup id="head1">[1](#foot1)</sup>

### 1.1. 요약
CTurt가 작성하였으며, WebKit 취약점을 처음으로 PS4에 포팅하였으며, WebKit exploit 부터 Kernel exploit까지 Full Chain exploit한 것을 자세하게 기술하였다. 

CTurt는 웹킷 취약점 과 Kernel 취약점 모두 우리와 같은 1-day를 PS4에 포팅하여 진행하였다. 다른 점이 있다면 우리는 1-day를 통해 최신 버전 exploit하는 것을 목표로 진행하였다. 하지만 CTurt는 패치된 1-day를 구버전 PS4에 포팅해서 Full Chain exploit을 진행하였다.

이 과정에서 우리는 이미 웹킷에서는 패치된 취약점이지만, 글을 작성하는 시점인 2020-12-12 기준으로 최신 버전인 PS4 8.01 버전에서 pc controll이 가능한 UAF 취약점을 찾아낸 성과가 있었다.

CTurt가 작성한 글은 상당히 오래전에 작성된 것이라서 KASLR 보호기법이 걸려있지 않는 등 최신 PS4에 걸려있는 보호기법이 적용되지 않은 부분이 있으나 PS4 exploit 처음 접하는 사람들에게는 좋은 글이니 읽어보는 것을 추천한다.

## 2. THIS IS FOR THE PWNERS: EXPLOITING A WEBKIT 0-DAY IN PLAYSTATION 4


## 3. Reference
><b id="foot1">[[1](#head1)]</b> [Hacking the PS4](https://cturt.github.io/ps4.html)<br>



### Contents <!-- omit in toc -->
[메인화면](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/README.md)<br>

#### PS4 소개 <!-- omit in toc -->
[1. Jailbreak](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/1_introduction/Jailbreak.md)<br>
[2. PS4 Open Source](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/1_introduction/PS4_Open_Source.md)<br>
[3. Tools](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/1_introduction/Tools.md)<br>

#### 프로젝트 접근 방법론 <!-- omit in toc -->
[1. WebKit](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/2_methodology/WebKit.md)<br>
[2. Hardware](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/2_methodology/Hardware.md)<br>
[3. Library](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/2_methodology/Library.md)<br>

#### 결론 <!-- omit in toc -->
[결론](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/3_conclusion/Conclusion.md)
