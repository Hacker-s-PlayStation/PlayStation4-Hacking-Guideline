# Library
## 개요
### Uart Log
* Uart Log를 보다가 플레이스테이션 4에서 외부 사이트에서 파일을 가져오는 것을 확인
![image](https://user-images.githubusercontent.com/39231485/101589311-86880d00-3a2b-11eb-9906-aafc7b2b666e.png)
### 새로운 방법론
* 기존에 WebKit, Freebsd 취약점을 사용하는 Jailbreak와는 다르게 프로세스 안에 있는 라이브러리의 취약점을 사용하는 것을 고안해봤다.<br><br>

## sprx를 so파일로 바꾸기
* 플레이스테이션 4 안의 파일들은 모두 암호화가 되어있기 때문에 아래에서 복호화된 펌웨어를 사용해야 한다.
[사이트](https://darthsternie.net/ps4-decrypted-firmwares/)
### ps4 라이브러리
![image](https://user-images.githubusercontent.com/39231485/101594750-8e4caf00-3a35-11eb-891e-3102d8be47be.png)
  * ps4 라이브러리는 소니가 자체적으로 만든 sprx라는 포맷을 사용한다.
    * 이를 so 파일로 만들어주기 위해서는 sprx 포맷을 elf 포맷으로 만들어줘야 한다.


  
   

### Contents
[메인화면](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/README.md)<br>
#### PS4 소개
[1. Jailbreak](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/1_introduction/Jailbreak.md)<br>
[2. PS4 Open Source](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/1_introduction/PS4_Open_Source.md)<br>
[3. Tools](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/1_introduction/Tools.md)<br>
#### 프로젝트 접근 방법론
[1. WebKit](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/2_methodology/webkit.md)<br>
[2. Hardware](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/2_methodology/hardware.md)<br>
[3. Library](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/2_methodology/library.md)<br>
#### 결론
[결론](https://github.com/Hacker-s-PlayStation/PlayStation4-Hacking-Guideline/blob/main/3_conclusion/conclusion.md)
