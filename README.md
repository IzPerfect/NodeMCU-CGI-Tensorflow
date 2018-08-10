NodeMCU-CGI-Tensorflow
===
NodeMCU, CGI, 파이썬, 텐서플로우, 데이터베이스를
 이용한 간단한 xor 논리연산자 구현
 
 NodeMCU를 통해 서버로 0 또는 1의 데이터를 전송하고 서버에서는
 데이터베이스에 NodeMCU에서 보낸 데이터와 보낸 데이터를 가지고
 Tensorflow를 사용한 xor연산을 실행한 뒤 결과를 데이터베이스에
 저장. NodeMCU는 Serial monitor에서 결과를 보여준다.
 
전체 시스템 구조
---
![system_architecture](/image/system.png)

Results
---
NodeMCU에서 보낸 데이터를 데이터베이스에 저장

![input](/image/xor_input_table.PNG)


xor 연산 결과 데이터베이스에 저장

![result](/image/xor_result_table.PNG)

Serial monitor 결과

![serial](/image/Serial_monitor.PNG)


Reference Implementations
---
+ http://www.hardcopyworld.com/ngine/aduino/index.php/archives/2675


