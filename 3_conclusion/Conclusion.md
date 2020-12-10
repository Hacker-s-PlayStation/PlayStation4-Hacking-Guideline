# 결론
우리 팀원들은 BoB Project를 통해 약 3개월 간 PS4 Jailbreak를 탐구했다. Jailbreak를 하는 가장 기본적인 방법은 WebKit 브라우저와 FreeBSD 커널의 exploit을 통한 방법이다. 3개월이라는 단기간에 둘을 exploit하기 위하여 PS4에 존재하는 WebKit과 FreeBSD가 최신버전이 아니라는 것을 이용하여 패치되지 않은 1 day 취약점을 이용하여 exploit하는 방법론을 채택했다. 그러나, 브라우저 취약점과 exploit의 큰 부분을 차지하는 WebAssembly, Garbage Collector 및 JIT 모듈이 PS4 WebKit에서는 사용할 수 없다는 점, Sony에서 자체적으로 꾸준하게 패치한다는 점으로 인해 프로젝트 기간 내에 Exploit을 하는데 실패했다.<br>

UART Log를 통해 PS4 서버와 통신을 하여 env파일을 주기적으로 전달받는 것을 확인했고, 이를 이용하여 해당 부분을 처리하는 라이브러리의 취약점을 이용하여 PS4 커널 exploit을 시도했다. 그리고 WebKit에서 사용하는 모듈 중 WebKit 내부 모듈이 아닌, 외부 라이브러리를 끌어다쓰는 모듈의 취약점을 이용하려고 했다. 따라서 PS4 내부에있는 라이브러리 파일을 분석하는 것과 PC에서 해당 라이브러리 Fuzzer를 돌리기 위해 PS4의 라이브러리 포맷인 sprx를 PC에서 사용가능한 포맷인 so로 바꾸는 것을 시도했다.<br>

WebKit 1 day를 이용한 Jailbreak시도를 통해 PS4 WebKit에서 적용될 수 있는 취약점을 찾을 수 있었던 사실로 보았을 때, WebKit 최신버전을 사용하지 않고 구버전 WebKit을 Sony에서 자체적으로 패치해 나가는 것은, 패치가 되지 않은 1 day 취약점을 통한 공격이 가능하다는 것을 보여준다. 그러나, 방대한 양의 WebKit commit과 PoC들을 follow up해야하고, 취약점을 찾았다고 하더라도 해당 취약점이 Sony의 패치를 피해가야하는 위 접근법은 0 day를 이용한 접근법에 필적한 난이도를 가지는 것으로 여겨진다.<br>

본 팀은 기간 내에 프로젝트 목표를 수행하는데 실패하였으나, 프로젝트의 진행 내용을 공유함으로써 이후 PS4를 분석하는 사람들에게 조금이나마 도움을 줄 수 있다는 사실에 의의를 두며 글을 마무리 짓는다.

---
### Contents
[메인화면](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/README.md)<br>

#### PS4 소개
[1. Jailbreak](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/1_introduction/Jailbreak.md)<br>
[2. PS4 Open Source](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/1_introduction/PS4_Open_Source.md)<br>
[3. Tools](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/1_introduction/Tools.md)<br>

#### 프로젝트 접근 방법론 <!-- omit in toc -->
[1. WebKit](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/2_methodology/WebKit.md)<br>
[2. Hardware](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/2_methodology/Hardware.md)<br>
[3. Library](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/2_methodology/Library.md)<br>

#### 결론 <!-- omit in toc -->
[결론](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/3_conclusion/Conclusion.md)