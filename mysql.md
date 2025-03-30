### Ubuntu에 mysql database 설치, 접속하기 

우선 Ubuntu에 mysql 설치 이후

~~~
sudo /user/bin/mysql -u root -p
~~~

를 통해 mysql에 root 권한으로 접속합니다. <br>

### 데이터베이스 생성, 테이블 생성, 권한 설정하기

~~~
CREATE DATABASE {테이블 이름}
~~~

로 테이블을 생성합니다.

~~~
SHOW DATABASES;
~~~

에서 데이터베이스가 잘 생성되었는지 확인합니다. 이후

~~~
CREATE USER '사용자'@'host' identified by '비밀번호';
~~~

를 통해 내부 접근을 허용하는 사용자를 추가한 다음,

~~~
CREATE TABLE {테이블명}
ord INT,
agentid VARCHAR(10),
emotion VARCHAR(10),
score FLOAT,
imgfile VARCHAR(100),
regdate date
);
~~~

같은 형식으로 테이블을 생성해 줍니다. 이후

~~~
GRANT SELECT, INSERT ON {DB 이름}.{테이블명} to '사용자'@'localhost';
~~~

와 같은 식으로 해당 사용자에게 권한을 부여해 줍니다.