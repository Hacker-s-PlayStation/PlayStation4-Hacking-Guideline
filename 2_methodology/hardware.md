### Page Contents
- [Hardware](#Hardware)
	- [UART Log](#uart-log)
	  - [준비물](#준비물)
	  - [Step 1 : UART 포트 확인](#step-1--uart-포트-확인)
	  - [Step 2 : UART 포트 납땜](#step-2--uart-포트-납땜)
	  - [Step 3 : USB to TTL Serial Cable 연결](#step-3--usb-to-ttl-serial-cable-연결)
	  - [Step 4 : UART Log 확인](#step-4--uart-log-확인)
	  - [결과](#결과)
	- [syscon dump](#syscon-dump)
	  - [준비물](#준비물-1)
	  - [Step 1 : syscon 디솔더링](#step-1--syscon-디솔더링)
	  - [Step 2 : syscon과 Teensy 4.0 보드 연결](#step-2--syscon과-teensy-40-보드-연결)
	  - [Step 3 : Teensy4.0 programming](#step-3--teensy40-programming)
	  - [Step 4 : syscon dump](#step-4--syscon-dump)
	  - [dump 결과](#dump-결과)
	- [sflash dump](#sflash-dump)
	  - [Step 1 : sflash 와 Teensy 2.0 보드 연결](#step-1--sflash-와-teensy-20-보드-연결)
	  - [Step 2 : NORway 환경 구성](#step-2--norway-환경-구성)
	  - [Step 3 : Teensy Loader](#step-3--teensy-loader)
	  - [Step 4 : SPIway - info](#step-4--spiway---info)
	  - [Step 5 : SPIway - dump](#step-5--spiway---dump)
	  - [dump 결과](#dump-결과-1)
	  - [추가](#추가)
	- [Reference](#reference)
	  - [Contents](#contents)
	    - [PS4 소개](#ps4-소개)
	    - [프로젝트 접근 방법론](#프로젝트-접근-방법론)
	    - [결론](#결론)
---
  
## UART Log

### 준비물
- 인두기, 납, JumperWire
- USB to TTL Serial Cable

### Step 1 : UART 포트 확인

![UART](https://user-images.githubusercontent.com/48618245/101594879-bcca8a00-3a35-11eb-925c-f4f1cb90cc11.jpeg)
PS4를 분해하여 메인보드를 보면 위 사진과 같은 곳에 UART 포트가 있다.


<img width="433" alt="UART_point" src="https://user-images.githubusercontent.com/48618245/101595248-690c7080-3a36-11eb-9b79-cee09075332b.png">

위 사진은 우리가 사용한 SAB-001 보드의 UART 포트이다.

### Step 2 : UART 포트 납땜

<img width="164" alt="UART_납땜" src="https://user-images.githubusercontent.com/48618245/101595305-7f1a3100-3a36-11eb-904c-093f6788bf5e.png">

JumperWire를 위에서 확인한 UART 포트에 납땜해서 연결을 해준다.

### Step 3 : USB to TTL Serial Cable 연결

![UART_to_Serial](https://user-images.githubusercontent.com/48618245/101595351-92c59780-3a36-11eb-9aa6-d385ec93f6bc.jpeg)
USB to TTL Serial Cable에 Step 2에서 납땜한 JumperWire를 연결해준다. GND는 GND끼리 연결해주고 UART 포트의 TX는 USB to TTL Serial Cable의 RX에 연겨해준다.

### Step 4 : UART Log 확인
<img width="723" alt="UART_Log1" src="https://user-images.githubusercontent.com/48618245/101595832-62322d80-3a37-11eb-97b5-927d3e629647.png">
<img width="179" alt="UART_Log_Blank" src="https://user-images.githubusercontent.com/48618245/101595863-6f4f1c80-3a37-11eb-9ef2-00663cae257f.png">

소니에서 UART Log를 확인하지 못하도록 공백으로만 출력하도록 해놨다.

### 결과
UART Log를 보고 싶으면 Jailbreak 해놓은 PS4에서 ps4debug.bin 파일을 bin loader로 올리면 확인할 수 있다. 하지만 이는 하드웨어적으로 연결 안해도 nc를 이용하여 포트 접속만 해도 확인할 수 있으니 하드웨어적인 성과는 없었다.


## syscon dump

### 준비물
- 열풍기, 인두기세트(납, solder wick, 플럭스)
- Jumper Wire, 저항, USB to TTL Serial Cable, pin header, 커패시터
- Teensy 4.0

### Step 1 : syscon 디솔더링

![desoldering](https://user-images.githubusercontent.com/48618245/101596857-3021cb00-3a39-11eb-8ede-48a42172527b.JPG)

syscon dump를 하기 위해서는 우선 syscon 칩을 디솔더링 해야하는데 사실 이 부분이 제일 힘들었다. 처음에 사용하던 열풍기로는 디솔더링이 잘 안됐다. 

![시스콘칩부러진거](https://user-images.githubusercontent.com/48618245/101596946-50ea2080-3a39-11eb-9d13-8e457a331a46.PNG)
이 과정에서 무리하게 디솔더링을 하다가 syscon칩이 망가져서 PS4를 새로 하나 더 구입하게 됐다. 

더 높은 온도가 가능한 열풍기를 구입한 후 syscon 주변에 플럭스를 뿌려주고 `600℃`로 열풍기를 가해주니 디솔더링이 쉽게 되었다. sflash도 이 방법으로 디솔더링하니 쉽게 되었다.

만약 가지고 있는 열풍기가 600℃ 이상 온도가 올라가지 않는다면 열풍기를 구입하는 것을 추천한다.
(디솔더링 사진)

### Step 2 : syscon과 Teensy 4.0 보드 연결

<img width="414" alt="SYSGLITCH wiring diagram by Wildcard" src="https://user-images.githubusercontent.com/48618245/101595983-a6bdc900-3a37-11eb-8e23-2c50a206643a.png">

`Wildcard`가 제공해준 sysglitch diagram대로 `Teensy 4.0 보드(이하 Teensy4.0)`와 `syscon`을 연결하여 덤프를 진행하였다. diagram과 똑같이 연결을 해야 정상적으로 dump가 가능하니 이 부분을 잘 신경써서 해야한다.

### Step 3 : Teensy4.0 programming

<img width="116" alt="Teensy_loader" src="https://user-images.githubusercontent.com/48618245/101596124-e389c000-3a37-11eb-9168-cee58b65fc63.png">

syscon glitch 하기 위해 Teensy4.0에서 동작하도록 만들어 놓은 hex 파일을 받고 `Teensy Loader`에 올린 후 Teensy4.0에 있는 버튼을 누르면 프로그래밍이 된다. 프로그래밍이 완료되면 후에 덤프가 가능해진다.

[https://www.pjrc.com/teensy/loader.html](https://www.pjrc.com/teensy/loader.html) - Teensy Loader 프로그램 다운로드 사이트
[https://github.com/VV1LD/SYSGLITCH/releases/tag/T4-1.0](https://github.com/VV1LD/SYSGLITCH/releases/tag/T4-1.0) - SYSGLITCH_TEENSY4.0.hex 다운로드 사이트

### Step 4 : syscon dump

<img width="284" alt="realterm" src="https://user-images.githubusercontent.com/48618245/101596511-8c381f80-3a38-11eb-8fd5-58499a3e25e7.png">

realterm 프로그램을 사용하여 덤프를 뜬다. 

- pulldown 연결을 해제해놓은 상태로 시리얼 포트 및 baudrate을 115200 으로 설정하고 change 버튼을 누른다.
- Capture 탭에서 Start Overwrite 버튼을 누르면 화면이 빨갛게 변한다. 
- pulldown을 다시 연결하면 덤프가 떠진다. 4Mb 이상 덤프되면 다 됐다고 보면 된다.

[https://sourceforge.net/projects/realterm/](https://sourceforge.net/projects/realterm/) - realterm 다운로드 사이트

### dump 결과

<img width="885" alt="syscon_dump" src="https://user-images.githubusercontent.com/48618245/101596616-c5708f80-3a38-11eb-92d5-e2f0c6ddf6a8.png">

실제 덤프 뜬 파일 확인해보면 `Sony Computer Entertainment`가 나와있으면 덤프가 성공한 것이다.

만약 덤프가 정상적으로 되지 않고 실패했을 때는 계속 `Not Used`만 반복해서 떴었다.

## sflash dump

### Step 1 : sflash 와 Teensy 2.0 보드 연결

<img width="433" alt="sflash_diagram" src="https://user-images.githubusercontent.com/48618245/101597589-3feddf00-3a3a-11eb-9cda-7937a48d611c.png">

![sflash](https://user-images.githubusercontent.com/48618245/101597473-1634b800-3a3a-11eb-8be7-0a5d24554cd8.jpg)


디솔더링은 syscon과 똑같이 진행하면 된다. syscon dump를 참고하면 된다. sflash를 디솔더링 하고, Teensy 2.0 보드(이하 Teensy2.0)에 연결해줬다. 연결할 때는 Wildcard가 제공해준 daigram과 위 사진을 보면서 연결하였다.

처음에 Teensy2.0을 연결하면 시리얼 포트로 인식이 되지 않을 것이다. Teensy를 COM 포트로 인식되게끔 하려면 아두이노 프로그램으로 한 번 쯤은 프로그래밍을 해 줘야 한다.
자세한 내용은 https://www.pjrc.com/teensy/troubleshoot.html 이 사이트에 잘 나와 있다.

![com_serial](https://user-images.githubusercontent.com/48618245/101597743-79bee580-3a3a-11eb-9f5f-af34885ec829.png)

이렇게 포트 정보가 나타나야 툴을 제대로 돌릴 수 있다.

### Step 2 : NORway 환경 구성

SPIway라는 툴을 이용하여 덤프를 진행하면 된다. git clone을 해 주면 그 안에 `SPIway.py` 스크립트가 존재한다.

```bash
git clone https://github.com/hjudges/NORway
```

이 스크립트를 실행하기 위해서는 Python 2.7.2 버전 및 pyserial 2.5가 필요하다. 아래 링크로 접속하여 설치해 주자.

- Python 2.7.2 ([http://www.python.org/ftp/python/2.7.2/python-2.7.2.msi](http://www.python.org/ftp/python/2.7.2/python-2.7.2.msi))
- pyserial 2.5 ([http://pypi.python.org/packages/any/p/pyserial/pyserial-2.5.win32.exe](http://pypi.python.org/packages/any/p/pyserial/pyserial-2.5.win32.exe))

### Step 3 : Teensy Loader

![Teensy_loader2](https://user-images.githubusercontent.com/48618245/101597891-abd04780-3a3a-11eb-9335-e2424986820f.png)


TeensyLoader를 다운로드 받은 뒤 실행해 준다. git clone 받은 폴더에서 `.\NORway\SPIway\Release` 이 경로로 접속하면 `SPIway.hex` 라는 파일이 존재하는데 이 파일을 TeensyLoader를 이용하여 Teensy2.0에 프로그래밍 해준다. 그래야 SPIway 툴을 이용할 수 있다.

### Step 4 : SPIway - info

![SPIWay_info](https://user-images.githubusercontent.com/48618245/101597993-d28e7e00-3a3a-11eb-9eb9-4ee60e5c0cfe.png)


```bash
.\python.exe .\NORway\SPIway.py COM12 info
```

위 명령어를 입력했을 때 info가 제대로 출력되면 모든 준비가 완료된 것이다!

### Step 5 : SPIway - dump

![SPIWay_dump](https://user-images.githubusercontent.com/48618245/101598053-e89c3e80-3a3a-11eb-8b33-8e291ecb27e0.png)


```bash
.\python.exe .\NORway\SPIway.py COM12 dump C:\Users\sugar\Desktop\orig1.bin
```

위 명령어를 입력하여 덤프를 수행한다. 한 3~5분 정도 기다리면 덤프가 완료된다.

### dump 결과

![sflash_dump](https://user-images.githubusercontent.com/48618245/101598102-ff429580-3a3a-11eb-915f-7ae364a14720.png)


`SONY COMPUTER ENTERTAINMENT INC` 가 나온다면 정상적으로 덤프가 완료된 것이다.

### 추가

```
-SPIway.py

		* Flash Teensy with "\SPIway\Release\SPIway.hex"
		At the command prompt enter "SPIway.py" to display help.

		first make sure that you are able to read the SPI chip info. Do this by using
		the info command.

		get information:
		SPIway.py COMx info

		dump:
		SPIway.py COMx dump filename

		write:
		SPIway.py COMx write filename

		write with verify:
		SPIway.py COMx vwrite filename

		erase entire chip:
		SPIway.py COMx erasechip
```

dump 뿐만 아니라 write도 가능하다. 실제로 PS4에서 NOR 칩의 일부 섹션이 손상되어 BLOD (Blue Light of Death) 문제가 발생한 경우, syscon ROM을 덤프하고 00 00 00 00.. 영역을 FF FF FF FF... 로 덮어 쓴 뒤 vwrite 해 줌으로써 수리를 하기도 했다. 이 write 기능을 추후에 이용할 수 있지 않을까 싶다.

## Reference
- [SYSGLITCH_DOWNGRADE (2).pdf](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/37e4d1b3-06ea-4ed1-ab61-ce45f6146c7b/SYSGLITCH_DOWNGRADE_(2).pdf)
  
- [https://www.psxhax.com/threads/ps4-sysglitch-tool-and-syscon-glitching-pinout-by-vvildcard777.7545/](https://www.psxhax.com/threads/ps4-sysglitch-tool-and-syscon-glitching-pinout-by-vvildcard777.7545/)

- [https://gbatemp.net/threads/ps4-nor-chip-repair-that-displays-signs-of-a-blod.569955/](https://gbatemp.net/threads/ps4-nor-chip-repair-that-displays-signs-of-a-blod.569955/)


---
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
