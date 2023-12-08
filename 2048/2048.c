#include <stdio.h>
#include <unistd.h>
#include <termios.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>

//추가로 구현한 기능
//1. 숫자에 따라 색상 다르게 하기
//2. 키 입력할 때마다 클리어 스크린
//3. 보드 꽉 차서 게임오버 되면 가장 큰 수 알려주기

void setBufferedInput(bool);
void drawboard(); //보드 그림
void addrandom(); //숫자(2 or 4) 랜덤으로 추가
bool keepplaying(); //더 움직일 수 있는지 알아보기
void move(); //키를 이용해서 움직이기
int findlargest(); //제일 크게 만든 수 알아보기
void clearscreen(); //화면 깨끗하게 하기
void storeprev(); //이전 상태 저장
bool sameasprev(); //이전 상태와 현재 상태 비교

#define SIZE 4
int board[SIZE][SIZE] = {0,};
int prevboard[SIZE][SIZE] = {0,};

int main(void) {
  addrandom();
  addrandom();
  clearscreen();
  drawboard();

  setBufferedInput(false);

  while (keepplaying()){
    storeprev();
    move();
    if(!sameasprev()){
      addrandom();
    }
    clearscreen();
    drawboard();
    keepplaying();
  }

  printf("Game over!\n");
  printf("Your largest number is %d\n", findlargest());

  setBufferedInput(true);

  return 0;
}

void storeprev(void){
  for (int x=0; x<SIZE; x++){
    for (int y=0; y<SIZE; y++){
      prevboard[x][y] = board[x][y];
    }
  }
}

bool sameasprev(void){
  for (int x=0; x<SIZE; x++){
    for (int y=0; y<SIZE; y++){
      if (prevboard[x][y] != board[x][y]){
        return false;
      }
    }
  }
  return true;
}

void drawboard(void){
  int x, y;
  printf("\t\t\t\t\t<2048 GAME>\n\n\n");
  for (x=0; x<SIZE; x++){
    for (y=0; y<SIZE; y++){
      if(board[x][y] == 0) printf("%10c", '-');
      else {
        if (board[x][y] == 2){
          printf("\033[0;20m%10d\033[0m", board[x][y]);
        }
        else if (board[x][y] == 4){
          printf("\033[0;31m%10d\033[0m", board[x][y]);
        }
        else if (board[x][y] == 8){
          printf("\033[0;32m%10d\033[0m", board[x][y]);
        }
        else if (board[x][y] == 16){
          printf("\033[0;33m%10d\033[0m", board[x][y]);
        }
        else if (board[x][y] == 32){
          printf("\033[0;34m%10d\033[0m", board[x][y]);
        }
        else if (board[x][y] == 64){
          printf("\033[0;35m%10d\033[0m", board[x][y]);
        }
        else if (board[x][y] == 128){
          printf("\033[0;36m%10d\033[0m", board[x][y]);
        }
        else if (board[x][y] == 256){
          printf("\033[0;91m%10d\033[0m", board[x][y]);
        }
        else if (board[x][y] == 512){
          printf("\033[0;92m%10d\033[0m", board[x][y]);
        }
        else if (board[x][y] == 1024){
          printf("\033[0;93m%10d\033[0m", board[x][y]);
        }
        else if (board[x][y] == 2048){
          printf("\033[0;96m%10d\033[0m", board[x][y]);
        }
        else{
          printf("%10d", board[x][y]);
        }
      }
    }
    printf("\n\n\n");
  }
  printf("\t\t\t↑, ←, ↓, →   or   w, a, s, d\n\n");
}

void addrandom(void){
  int x, y, num;
  srand(time(NULL));
  while (1){
    num = (rand()%100<70)?2:4; 
    x = rand() % 4;
    y = rand() % 4;
    if(board[x][y] == 0) {
      board[x][y] = num;
      break;
    }
  }
}

void move(){
  int l, i, j;
  int key = getchar();

  if (key == 119 || key == 65){ ///up
    for (l=0; l<SIZE; l++){
      for (i=0; i<SIZE-1; i++){
        for (j=0; j<SIZE; j++){
          if (board[i][j] == 0){
            board[i][j] = board[i+1][j];
            board[i+1][j] = 0;
          }
        }
      }
    }
    for (i=0; i<SIZE-1; i++){
      for (j=0; j<SIZE; j++){
        if (board[i][j] == board[i+1][j]){
          board[i][j] *= 2;
          board[i+1][j] = 0;
        }
      }
    }
    for (l=0; l<SIZE; l++){
      for (i=0; i<SIZE-1; i++){
        for (j=0; j<SIZE; j++){
          if (board[i][j] == 0){
            board[i][j] = board[i+1][j];
            board[i+1][j] = 0;
          }
        }
      }
    }
  }

  if (key == 115 || key == 66){ ///down
    for (l=0; l<SIZE; l++){
      for (i=SIZE-1; i>0; i--){
        for (j=0; j<SIZE; j++){
          if (board[i][j] == 0){
            board[i][j] = board[i-1][j];
            board[i-1][j] = 0;
          }
        }
      }
    }
    for (i=SIZE-1; i>0; i--){
      for (j=0; j<SIZE; j++){
        if (board[i][j] == board[i-1][j]){
          board[i][j] *= 2;
          board[i-1][j] = 0;
        }
      } 
    }
    for (l=0; l<SIZE; l++){
      for (i=SIZE-1; i>0; i--){
        for (j=0; j<SIZE; j++){
          if (board[i][j] == 0){
            board[i][j] = board[i-1][j];
            board[i-1][j] = 0;
          }
        }
      }
    }
  }

  if (key == 97 || key == 68){ ///left
    for (l=0; l<SIZE; l++){
      for (i=0; i<SIZE-1; i++){
        for (j=0; j<SIZE; j++){
          if (board[j][i] == 0){
            board[j][i] = board[j][i+1];
            board[j][i+1] = 0;
          }
        }
      }
    }
    for (i=0; i<SIZE-1; i++){
      for (j=0; j<SIZE; j++){
        if (board[j][i] == board[j][i+1]){
          board[j][i] *= 2;
          board[j][i+1] = 0;
        }
      } 
    }
    for (l=0; l<SIZE; l++){
      for (i=0; i<SIZE-1; i++){
        for (j=0; j<SIZE; j++){
          if (board[j][i] == 0){
            board[j][i] = board[j][i+1];
            board[j][i+1] = 0;
          }
        }
      }
    }
  }

  if (key == 100 || key == 67){ ///right
    for (l=0; l<SIZE; l++){
      for (i=SIZE-1; i>0; i--){
        for (j=SIZE-1; j>=0; j--){
          if (board[j][i] == 0){
            board[j][i] = board[j][i-1];
            board[j][i-1] = 0;
          }
        }
      }
    }
    for (i=SIZE-1; i>0; i--){
      for (j=SIZE-1; j>=0; j--){
        if (board[j][i] == board[j][i-1]){
          board[j][i] *= 2;
          board[j][i-1] = 0;
        }
      } 
    }
    for (l=0; l<SIZE; l++){
      for (i=SIZE-1; i>0; i--){
        for (j=SIZE-1; j>=0; j--){
          if (board[j][i] == 0){
            board[j][i] = board[j][i-1];
            board[j][i-1] = 0;
          }
        }
      }
    }
  }
}

bool keepplaying(){
  int x, y;
  for (x=0; x<SIZE; x++){
    for (y=0; y<SIZE; y++){
      if (board[x][y]==0) return true;
    }
  }
  for (x=0; x<SIZE-1; x++){
    for (y=0; y<SIZE; y++){  
      if (board[x][y]==board[x+1][y]) return true;
    }
  }
  for (x=0; x<SIZE; x++){
    for (y=0; y<SIZE-1; y++){
      if (board[x][y]==board[x][y+1]) return true;
    }
  }
  return false;
}

int findlargest(){
  int i, j;
  int largest = 0;
  for (i=0; i<SIZE; i++){
    for (j=0; j<SIZE; j++){
      if (largest < board[i][j]) largest = board[i][j];
    }
  }
  return largest;
}

void setBufferedInput(bool enable) {
   static bool enabled = true;
   static struct termios old;
   struct termios new;

   if (enable && !enabled) {
      // restore the former settings
      tcsetattr(STDIN_FILENO,TCSANOW,&old);
      // set the new state
      enabled = true;
   } else if (!enable && enabled) {
      // get the terminal settings for standard input
      tcgetattr(STDIN_FILENO,&new);
      // we want to keep the old setting to restore them at the end
      old = new;
      // disable canonical mode (buffered i/o) and local echo
      new.c_lflag &=(~ICANON & ~ECHO);
      // set the new settings immediately
      tcsetattr(STDIN_FILENO,TCSANOW,&new);
      // set the new state
      enabled = false;
   }
}

void clearscreen(){
  printf("\e[1;1H\e[2J");
}