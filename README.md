# 무료 쿠폰 이벤트 페이지

## 실행
### pyenv + pipenv 설치

```bash
brew install pyenv pipenv
```

```bash
pipenv shell
```

```bash
pipenv install
```

### 가상환경에서 작업
```bash
pipenv shell
```

### 서버 실행
```bash
python manage.py runserver
```

## apps

### promotion
이벤트를 관리하기 위한 app.  
db 에 이벤트 정보를 저장하여 ```GET /promotion/{promotion_id}``` 등의 API 로 이벤트 정보 전체를 불러오는것을 기획 했으나, 시간 소요를 줄이고자 단일 이벤트 페이지 하나를 생성하는것으로 변경  
이벤트 기간에 해당하지 않을 경우 종료된 이벤트 처리

#### views.py
편의를 위해 쿠폰 및 이벤트 정보를 따로 불러오지 않고 고정.  
쿠폰 잔여 수량을 계산하여 제품의 정보와 함께 템플릿에 전달

### coupon
쿠폰을 관리하기 위한 app.

#### Coupon(Model)
쿠폰의 정보가 담긴 model  
할인 금액, 할인률 등 쿠폰의 목적을 구분  
최대 발급 수량을 지정할 수 있다.

#### CouponAuthority(Model)
쿠폰함.

### product
작품을 관리하기 위한 app.

## api

### POST /api/coupon_authority
쿠폰함에 쿠폰을 추가하는 API  
전달받은 쿠폰, 작품, 사용자 정보를 사용하여 해당 사용자의 쿠폰함에 쿠폰을 추가한다.  
해당 작품에 쿠폰을 발급받은 적이 있는 경우 중복으로 발급받을 수 없다.  
```Coupon``` 모델의 ```count_limit``` 을 초과하여 발급받을 수 없다. 이 경우 안내메시지를 출력한다.