# oEmbed Test

### Django, [oEmbed](https://oembed.com/) 를 이용하여 요청한 사이트의 embedded  content 랜더링

#### 실행
```shell
# 소스코드 받은 후
sudo docker build -t oembed-test .

sudo docker run -p 8000:8000 oembed-test

# 또는

sudo docker run -p 8000:8000 gptjddl123/oembed
```

http://127.0.0.1:8000
에 접속하여 url 입력.

예시

```https://vimeo.com/20097015``` 입력

<img src="./screenshots/vimeo.jpg">

