```sh
docker-compose up -d --build
```
after app started there is installed polladmin user pollsadmin with auth token 14bdb407d0d76155432f2f11bf7e81ee88df1a7d

try it:
```sh
curl http://127.0.0.1:8000/hello/ -H 'Authorization: Token 14bdb407d0d76155432f2f11bf7e81ee88df1a7d'
```
if you see "Hi there", so you succerfull auth

then open url http://127.0.0.1:8000/api/ all endpoints are there, just navigate over urls and read docs
