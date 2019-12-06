# 终端登陆大连理工校园网的脚本

依赖 : `python3` `requests`  `re`

```shell
python login.py user-id  password # 其中user-id为用户名(学号或者职工号)， 密码为统一身份认证密码
```



`autologin.py`是检测断线后自动重连的脚本，可以写在`crontab`中定时执行

```python
# m h  dom mon dow   command
0 * * * * python3 /pathto/autologin.py user-id password 2>>log
```

