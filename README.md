# Snakegame
2021-2 컴퓨터의 개념 및 실습 과제

# Bombgame
2021-2 컴퓨터의 개념 및 실습 과제

## 1. 프로그램 소개
- 한 명의 플레이어가 돌아다니면서 폭탄을 제거하는 게임입니다. (bombgame)
- 킬링타임용으로 좋은, 약간의 머리 사용이 필요한 게임입니다.
게임 화면은 왼쪽 사진과 같고, 플레이어는 흰색이며,
폭탄은 주어져 있는 grid 안에 총 25개가 숨겨져 있
습니다.
- 실행 화면 위쪽에서는 플레이어 근처에 있는 폭탄의
개수, 남아 있는(제거되지 않은) 폭탄의 개수, 남아
있는 생명의 개수, 플레이어가 움직인 횟수, 그리고
남은 시간을 알려줍니다.
- 게임을 계속 하다 보면 걸린 시간과 움직임 횟수를
줄여나갈 수 있을 겁니다. 파이팅!

### <규칙 소개>
- 플레이어 1명 – 흰색 / 폭탄 25개 – grid 곳곳에 숨겨져 있음 / grid – 20*20
- 게임을 실행할 때마다 폭탄의 위치는 랜덤으로 설정됩니다.
- 플레이어가 돌아다닐 때, 플레이어의 상하좌우에 있는 폭탄 개수(Bombs near me)를 실행 화면
위쪽에서 알려줍니다. 단, 플레이어가 폭탄 위에 있는 경우는 폭탄 개수로 카운트하지 않습니다.
(예를 들어, 플레이어 위쪽에 폭탄 1개가 있는 경우는 1, 위쪽과 오른쪽에 1개씩 있는 경우는 2, 
폭탄이 있는 좌표에 플레이어가 있고 플레이어의 상하좌우에는 폭탄이 없는 경우는 0입니다.)
- 플레이어는 arrow 키를 누를 때마다 한 칸씩 움직입니다. 이 때, arrow 키를 눌러 플레이어가
돌아다닐 때마다 움직임 횟수(Move)가 1씩 올라갑니다. 
- 폭탄이 있는 좌표 위에서 space 키를 누르면 폭탄이 제거됩니다. 폭탄이 제거된 좌표는 파란색
으로 변합니다. 단, 폭탄이 없는 좌표 위에서 space 키를 누르면 생명이 1개 차감됩니다.
- 폭탄 25개를 제거하는 데 주어진 시간은 160초이며, 주어진 생명은 3개입니다.
- 프로그램을 실행하면 time countdown이 바로 시작되니까 주의하세요. (게임이 바로 시작됩니다.)

### <게임의 목표>
- 주어진 시간 160초와 생명 3개 내에, 폭탄 25개를 다 제거하는 것이 목표입니다.
(여러 번 해보니, 150초도 가능은 하지만 너무 어려워져서, 160초로 설정하였습니다.)
- 움직임 횟수를 최소화하여 폭탄을 제거하는 것 역시 게임의 목표 중 하나입니다.
(움직임 횟수에 따른 제한은 없습니다. 단지 게임 유저들의 자기만족 및 목표 설정을 위해 추가한
기능입니다.)

### <게임 종료 조건>
- 플레이어가 테두리 바깥으로 벗어나면 fail입니다. 테두리에 닿는 것이 아닌, 벗어남을 말합니다.
- 도중에 Quit으로 게임 끌 수 있습니다. 다만 이는 도중 포기로 간주하고 fail입니다.
- 시간을 초과하면 time over로 fail입니다. 주어지는 시간은 160초입니다.
- 주어진 생명 3개를 다 쓰면 fail입니다.
- 플레이어가 폭탄 25개를 주어진 시간 내에 다 성공적으로 제거하면 게임이 끝납니다.

### <출력 메시지> 화면에 메시지가 출력된 이후 조금 기다렸다가 프로그램이 종료됩니다.
- 시간 내에 주어진 생명으로 폭탄 제거에 성공한 경우:
 생명이 3개 다 남아있으면 Excellent!, 2개면 Great!, 1개면 Good!과 함께 You succeeded! 메시
지, 그리고 움직인 횟수를 알려주는 메시지를 화면에 출력해줍니다.
- 시간이 초과된 경우:
 Time Over… Try again! 메시지를 화면에 출력해줍니다.
- 생명을 다 쓴 경우, 도중에 Quit 버튼으로 게임에 포기한 경우:
 You failed… Try again! 메시지를 화면에 출력해줍니다.

## 2. 실행 및 조작 방법
- 실행:
zip 파일을 압축 해제하고 Vscode에서 python bombgame.py를 해서 실행시키면 됩니다.
주의) 프로그램을 실행하면 time countdown이 바로 시작됩니다. (=게임이 바로 시작됩니다.)

# 2048
2021-2 프로그래밍 연습 과제