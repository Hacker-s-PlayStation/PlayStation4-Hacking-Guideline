# PS4 Open Source
## PS4에서 사용하는 오픈소스 라이브러리
플레이스테이션 4에서도 많은 오픈소스 라이브러리를 사용한다.<br>
어떤 라이브러리들을 사용하는지, 해당 라이브러리에 어떻게 접근할 수 있는지 안다면 해당 라이브러리들의 1day를 테스트 해볼 수도 있고 우리가 라이브러리의 0day를 찾아 적용시켜볼 수도 있을 것이다.<br>
오픈소스 리스트는 [여기](https://doc.dl.playstation.net/doc/ps4-oss/index.html)에서 확인할 수 있다.<br><br>

## 프로세스에 사용되는 오픈소스 라이브러리 탐색
PS4에서 어떤 오픈소스를 사용하는지 확인했으니, 프로세스 안에서 어떤 오픈소스 라이브러리가 사용되는지 파악해야 한다.<br>
이를 위해 프로세스에서 사용하는 라이브러리의 파일명을 통해 유추하는 방법을 사용했다.<br>PS4 Cheater를 사용하여 선택한 프로세스 내에 어떤 라이브러리가 로드 된지 확인할 수 있다.
<br>![image](https://user-images.githubusercontent.com/39231485/101725475-15605c80-3af4-11eb-8cfc-812761b34ce9.png)<br>
위 사진은 becore.elf 프로세스에 로드된 라이브러리들로 libSceFreeTypeOt.sprx를 보면 FreeType 오픈소스가 사용된다는 것을 유추할 수 있다.<br><br>
다음으로 PS4 브라우저 프로세스에서 사용하는 오픈소스 라이브러리를 찾기 위해서 사용한 방법이다.<br>
기존 브라우저와 PS4 브라우저에서 지원하는 파일 포맷들을 확인해보고 해당 파일들을 어디에서 처리해주는지 확인했다.<br>
![image](https://user-images.githubusercontent.com/39231485/101726372-c3b8d180-3af5-11eb-84c8-fa6afd5443a6.png)
위처럼 돌려보며 uart 로그를 확인해본 결과 이미지는 딱히 특별히 처리해주는게 보이지 않았지만, 오디오 파일중 m4a와 비디오 파일 mp4를 처리해주는 특별한 프로세스가 있었다.<br><br>
![image](https://user-images.githubusercontent.com/39231485/101726793-8a349600-3af6-11eb-87a1-9b7c578c2bd2.png)<br>
uart에 나오는 [VCS], [BESDK], [BECPLYR]과 같은 문자열들을 아래 사진처럼 라이브러리에서 찾아보며 어떤 라이브러리에서 오디오, 비디오 처리가 이루어지는지 확인했다.<br>
![image](https://user-images.githubusercontent.com/39231485/101728318-953cf580-3af9-11eb-88df-5446d473f891.png)<br>

이를 통해 PS4에서만 지원하는 포맷을 처리해주는 라이브러리를 알아냈다.<br>
해당 라이브러리들은 소니에서 자체적으로 만든 것일 수도 있지만, 오픈소스를 사용했을 확률이 크기 때문에, 라이브러리를 여러 오픈소스 라이브러리와 매치시키면 알아낼 수 있을 것이다.<br><br>
이 방법으로 하나의 라이브러리를 타겟으로 잡아 취약점 분석을 진행하면 좋은 방법론이 될 수 있을 것 같다.<br><br>


# Contents <!-- omit in toc -->
[메인화면](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/README.md)<br>

## PS4 소개 <!-- omit in toc -->
[1. Jailbreak](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/1_introduction/Jailbreak.md)<br>
[2. PS4 Open Source](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/1_introduction/PS4_Open_Source.md)<br>
[3. Tools](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/1_introduction/Tools.md)<br>

#### 프로젝트 접근 방법론 <!-- omit in toc -->
[1. WebKit](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/2_methodology/WebKit.md)<br>
[2. Hardware](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/2_methodology/Hardware.md)<br>
[3. Library](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/2_methodology/Library.md)<br>

#### 결론 <!-- omit in toc -->
[결론](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/3_conclusion/Conclusion.md)<br>
