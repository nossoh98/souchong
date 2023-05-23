BASE_URL = "http://165.132.172.93:8000"
SECRET_KEY = "django-insecure-21ct7f5zzqvtrutju1@ne2fvh(%c^2v#hh^x5o-32bt-gf_f4$"

# Email Validation
EMAIL_HOST_USER = 'kimsinhyun415@gmail.com' 	 # 우리가 사용할 Gmail
EMAIL_HOST_PASSWORD = 'afvtjiyzgulpcwrw'


# MongoDB Config
mongodbInputUri = "mongodb://thwhd1:thwhd1@165.132.172.93/wanted.wanted?readPreference=primaryPreferred"
mongodbOutputUri = "mongodb://thwhd1:thwhd1@165.132.172.93/test.wanted"
mongodbCollectionDB = "mongodb://165.132.172.93/wanted.wanted"


# 참고자료
# WSGI + Gunicorn 배포: https://velog.io/@jiyoung/GunicornNginx-%EB%A6%AC%EB%88%85%EC%8A%A4-%EC%84%9C%EB%B2%84%EC%97%90%EC%84%9C-%EB%B0%B0%ED%8F%AC%ED%95%98%EA%B8%B0
#   - /etc/systemd/system 안에 gunicorn.service파일

