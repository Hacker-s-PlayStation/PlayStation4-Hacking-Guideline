### Page Contents <!-- omit in toc -->
- [1. Debugging](#1-debugging)
  - [1.1. ps4gdb_672](#11-ps4gdb_672)
  - [1.2. ps4gdb_ring0_672](#12-ps4gdb_ring0_672)
  - [1.3. PS4 Debug Watch](#13-ps4-debug-watch)
  - [1.4. PS4 Cheater](#14-ps4-cheater)
  - [1.5. PS4 Module Loader](#15-ps4-module-loader)
- [2. Hardware](#2-hardware)
  - [2.1. Teensy Loader](#21-teensy-loader)
  - [2.2. realterm](#22-realterm)
  - [2.3. SPIway](#23-spiway)

---
# Tools <!-- omit in toc -->
## 1. Debugging
### 1.1. ps4gdb_672
  * 플레이스테이션 4의 내부 프로세스를 remote gdb로 디버깅할 수 있다.
  * 장점
    * 대부분의 gdb 명령어를 사용할 수 있기 때문에 편리하게 디버깅이 가능하다.
  * 단점
    * 조금 불안정하다. ni를 하는데 continue가 될 때도 있고 가끔 자잘한 오류들이 생긴다.
  그래서 call 때 이외에는 ni 대신 si를 쓰는 것을 추천.
  * [사이트](https://www.psxhax.com/threads/ps4gdb-gdb-stub-ps4-port-to-debug-userland-apps-by-m0rph3us1987.7582/)<br><br>
### 1.2. ps4gdb_ring0_672
  * 플레이스테이션 4의 커널을 remote gdb로 디버깅할 수 있다.
  * 사용해보려고 했는데 remote gdb가 붙지 않아서 못했다.
  * [사이트](https://www.psxhax.com/threads/ps4gdb-ring-0-gdb-stub-to-debug-ps4-kernel-by-m0rph3us1987.7904/)<br><br>
### 1.3. PS4 Debug Watch
  * Debug Watch라는 윈도우 GUI 프로그램을 사용하여 내부 프로세스를 선택하고 Disassembly, Memory View, Debugging, BreakPoint, Memory Map 기능들을 사용할 수 있다.
  * 장점
    * 많은 기능들이 있어서 매우 편리하다. 
  * 단점
    * 특정 프로세스는 선택해도 안되는 경우가 있다.
  * [사이트](https://www.psxhax.com/threads/ps4-debug-watch-app-port-for-6-72-firmware-via-withmetta.7940/)<br><br>
### 1.4. PS4 Cheater
  * PS4 Cheater라는 윈도우 GUI 프로그램을 사용하여 내부 프로세스를 선택하고 Memory Map, Value Search 기능들을 사용할 수 있다.
  * 장점
     * Debug Watch보다 기능은 적지만, Debug Watch에서는 안되는 몇몇 프로세스가 Cheater에서는 된다.
  * 단점
    * 이 프로그램 또한 선택해도 안되는 프로세스는 존재한다.
    * PS4 Debug Watch보다 기능은 현저히 떨어진다.
  * [사이트](https://www.psxhax.com/threads/ps4cheater-ps4-cheater-homebrew-app-to-find-game-cheat-codes.4529/page-222#post-157094)
### 1.5. PS4 Module Loader
  * 플레이스테이션 4의 라이브러리를 아이다로 열었을 때, 심볼을 복구해주는 플러그인
  * 모든 함수들의 심볼들을 복구해주지는 않지만 그래도 꽤나 많이 복구해준다.
  * [사이트](https://github.com/SocraticBliss/ps4_module_loader)

## 2. Hardware
### 2.1. Teensy Loader
  * Tennsy 4.0, Teensy 2.0 보드에 원하는 동작을 수행하도록 프로그래밍하는 프로그램이다.
  * [사이트](https://www.pjrc.com/teensy/loader.html)
### 2.2. realterm
  * 시리얼 캡쳐 프로그램이다. PS4 하드웨어에서는 syscon dump를 할 때 사용한다.
  * 단점
    * 윈도우 운영체제만 지원한다.
  * [사이트](https://sourceforge.net/projects/realterm/)
### 2.3. SPIway
  * PS4를 위한 SPI flasher이며 sflash dump를 하는데 사용한 프로그램이다.
  * 단점
    * 실행하기 위해서는 Python 2.7.2 버전 및 pyserial 2.5가 필요하다. Python3 지원 안함.
  * [사이트](https://github.com/hjudges/NORway)<br><br>

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
