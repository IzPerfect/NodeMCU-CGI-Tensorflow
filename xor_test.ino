#include <xor_test.h> //데이터가 담기 헤더파일을 include
#include <ESP8266WiFi.h>


// 기본 와이파이 공유기에 접속하기 위한 설정
const char *ssid = "your_id";
const char *password = "your_password";
const char* host = "?.?.?.?"; // HTTP통신을 사용하여 받아올 서버 설정
const int httpPort = ??; // port번호 설정
  
int iter=0;//iter를 이용하여 데이터 순서가 1->2->3->4->1 ... 이런식으로 반복
int start_signal = 1; // 처음에 start_signal을 보내 기존에 데이터베이스 테이블을 reset 시킨다.




void setup() {
  
 //와이파이 연결부분
  Serial.begin(115200);

  WiFi.begin(ssid, password); // 공유기에 연결
  // while을 사용하여 공유기에 접속할 때까지 기다린다.
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Try to Connecting");
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());//공유기에 접속하면 해당 ip 주소를 print해준다

}



void loop() {
  delay(3000);


  //query string을 이용하여 데이터 보내기
  //?key=value&key=value 형태
  String url= "/xor_test.py?";

  //보내고 싶은 value를 노드 mcu에서 설정하여 .py파일을 통해 홈페이지와 연결하여 보냄
  url+= "input1=";
  url+= input1[iter];
  url+= "&input2=";
  url+= input2[iter];
  url+= "&start_signal=";
  url+= start_signal;
  

  // TCP통신을 위한 WiFiClient 클래스를 생성한다.
  WiFiClient client;
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }
  else{
    Serial.println("connection Success");
    Serial.print("Requesting GET: ");
    Serial.println(url);
    
    //Send request to the server:
    //여기서 형식을 따라서 작성해야 동작한다.
    client.println("GET " + url + " HTTP/1.1");
    client.print("Host: ");
    client.println(host);
    client.println("User-Agent: ESP8266/1.0");
    client.println("Connection: close\r\n\r\n");
  }
  

  // client를 체크해서 일정 시간 내에 응답이 왔는지 아닌지 체크한다. 만약 응답이 오지 않으면 Client Timeout이라는 문구 출력
 int timeout = millis() + 5000;
  while (client.available() == 0) {
    if (timeout - millis() < 0) {
      Serial.println(">>> Client Timeout !");
      client.stop();
      return;
    }
  }
  
 // HTTP통신을 통해 Response가 오면 한 라인씩 읽어 Serial통신으로 출력
  while(client.available()){
    String line = client.readStringUntil('\r');
    Serial.print(line);
  }
  
  Serial.println();
  Serial.println("closing connection");
  delay(100);


   // 여기서 반복되게 설정
   if (iter==3){
      iter=0;
    }
    else{
      iter=iter+1;
      }
      
   start_signal=0;//처음 보낼 시에 한 번만 테이블을 비운다.

 
}




