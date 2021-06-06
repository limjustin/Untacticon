# Untacticon

### 언택티콘 (2020.10 ~ 2020.12)

**제 2회 SM AI 경진 대회 참여 프로젝트**

<img src = "https://user-images.githubusercontent.com/55044278/100981443-29eba480-358a-11eb-8723-9309025aaa73.jpg" height = "450px">

----------

**주제** : 비대면 강의 중 학습자 상태 파악 AI 모듈

**기획 배경** : 비대면 강의의 불편한 점 해소

**팀원**

- [limjustin(임재영)](https://github.com/limjustin)
- [yoonho0922(안윤호)](https://github.com/yoonho0922)
- [goodaehong(구대홍)](https://github.com/goodaehong)
- [DaGyeongChoi(최다경)](https://github.com/DaGyeongChoi)

-----

**0. 입상 및 인터뷰**

<img src = "https://user-images.githubusercontent.com/55044278/105038713-04b3e680-5aa3-11eb-85b4-0c1b9ae0f8c4.png" height = "350px">

- 제 2회 SM 경진대회 AI 부문 **최우수상** 수상 🏆

- **관련 인터뷰**

  - [상명대학교 홈페이지 상명피플](https://www.smu.ac.kr/webzine/sm-people.do?mode=view&articleNo=714722)
  
  - [상명대학교 서울캠퍼스 네이버 블로그](https://blog.naver.com/sangmyung-univ/222212482849)
  
  - [상명대학교 서울캠퍼스 인스타그램](https://www.instagram.com/p/CKN1vZXBMwC/)
  
  - [핀포인트뉴스](https://cnews.pinpointnews.co.kr/view.php?ud=202101211528393427b45d942afb_45) / [스마트경제](http://www.dailysmart.co.kr/news/articleView.html?idxno=39145) / [머니투데이](https://news.mt.co.kr/mtview.php?no=2021012114317479030) / [한국대학신문](http://news.unn.net/news/articleView.html?idxno=503419) / [베리타스알파](http://www.veritas-a.com/news/articleView.html?idxno=354093) / [브릿지경제](http://www.viva100.com/main/view.php?key=20210121010005043)

----------

**1. 프로젝트 설명**

비대면 강의의 불편한 점들을 해소하기 위해 만든 AI 모듈인 언택티콘은 'Untact'와 'Emoticon'의 합성어입니다. 언택티콘은 인공지능으로 사용자의 모습을 인식하여 사용자의 반응 및 상태를 이모티콘으로 표시해줍니다. 학습자의 반응을 즉각적으로 파악하기 때문에, 학습자의 수업 몰입도 및 집중력이 증가되며 즉각적인 피드백을 통해 강의 질을 향상할 수 있습니다. 또한 반응의 종류를 이모티콘으로 표시해주기 때문에, 화상 캠을 켜지 않고도 원활한 상호작용이 가능하며 교육자는 학습자들의 반응을 쉽고 간단하게 파악할 수 있습니다.

----------

**2. 기능**

- **학습자의 반응을 즉각적으로 파악**

  - ```긍정``` / ```부정```   : 학습자의 고개 끄덕임 / 젓는 여부
  
  - ```의문``` : 학습자의 학습 내용 이해 여부
  
  - ```졸음``` : 학습자의 졸음 여부 
  
- **반응의 종류를 이모티콘으로 표시**

- **질문 버튼을 통해 질문 의사 표시**

----------

**3. 기술 다이어그램**

![image](https://user-images.githubusercontent.com/55044278/100983892-4806d400-358d-11eb-8e0c-2008391b8b5b.png)

----------

**4. 사용 기술**

- **Python 3.7**

- **Opencv**

- **Dlib**

- **PyQt5**

----------

**5. 실행 화면**

- **긍정 표현**

  - 학습자가 현재 고개를 끄덕이고 있는 상태

    ![yes_motion.gif](https://github.com/yoonho0922/Untacticon/blob/master/readme_util/yes_motion.gif?raw=true)

- **부정 표현**

  - 학습자가 현재 고개를 젓고 있는 상태

    ![no_motion.gif](https://github.com/yoonho0922/Untacticon/blob/master/readme_util/no_motion.gif?raw=true)

 - **의문 상태**

     - 학습자가 현재 학습 내용에 의문이 있는 상태

       ![doubt_motion.gif](https://github.com/yoonho0922/Untacticon/blob/master/readme_util/doubt_motion.gif?raw=true)

- **졸음 상태**

  - 학습자가 현재 졸고 있는 상태

    ![GIF 2020-12-03 오후 7-56-05](https://user-images.githubusercontent.com/55044278/101001720-d76ab200-35a2-11eb-871d-feadc2fd5c74.gif)

- **자리 비움 상태**

  - 학습자가 현재 자리를 비 모듈이 사람을 인식하지 못하는 상태

    ![left_motion.gif](https://github.com/yoonho0922/Untacticon/blob/master/readme_util/left_motion.gif?raw=true)

- **질문 버튼**

  - 학습자가 현재 질문이 있는 상태

    ![question_motion.gif](https://github.com/yoonho0922/Untacticon/blob/master/readme_util/question_motion.gif?raw=true)

----------

**6. 기대 효과**

![image](https://user-images.githubusercontent.com/55044278/100985320-2f97b900-358f-11eb-8be6-ad5955710d16.png)

----------

**7. 설명 동영상 링크**

[![image](https://user-images.githubusercontent.com/55044278/101017572-9c21b080-35ad-11eb-894a-93fe443ab318.png)](https://youtu.be/Ry_QrVTIT5k)

