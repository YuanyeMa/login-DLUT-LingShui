import requests
import os 
import sys
import re

def get_real_url():
	url = "http://auth.dlut.edu.cn"
	headers={
			'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36', 
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
	}
	try :
		respone =  requests.get(url, headers=headers, allow_redirects=True)
	except requests.exceptions.ConnectionError as e:
		sys.stderr.write("get real url failed : "+str(e))	
		return None
	else:	
		real_url = re.search('http://(.*)</script>', respone.text).group(0).rstrip('\'</script>')
		return real_url


def login(real_url, user_id, password):
	url = 'http://auth.dlut.edu.cn/eportal/InterFace.do?method=login'
	headers = {
		'Host': 'auth.dlut.edu.cn',
		'Connection': 'keep-alive',
		'Origin': 'http://auth.dlut.edu.cn',
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
		'DNT': '1',
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'Accept': '*/*',
		'Referer': real_url,
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.9',
		'Cookie': 'EPORTAL_COOKIE_OPERATORPWD=; EPORTAL_COOKIE_SERVER=; EPORTAL_AUTO_LAND=; EPORTAL_COOKIE_DOMAIN=; EPORTAL_COOKIE_USERNAME=; EPORTAL_COOKIE_PASSWORD=; EPORTAL_COOKIE_SERVER_NAME=; EPORTAL_COOKIE_SAVEPASSWORD=false; JSESSIONID=753F97619F33B13434E3FE5F31BE4D79'
	}

	query_string = re.search('wlanuserip(.*)', real_url).group(0)
	data={
		'userId': user_id,
		'password': password,
		'service':'',
		'queryString': query_string,
		'operatorPwd':'',
		'operatorUserId':'',
		'validcode':''
	}
	
	try :
		respone = requests.post(url=url, headers=headers, data=data)
	except requests.exceptions.ConnectionError as e:
		sys.stderr.write("login failed : "+str(e))	
	else :
		if ("success" in respone.text):
			print("login success")
		else:
			sys.stderr.write("login failed : "+respone.text)


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage:\n\tpython login.py user-id password\n")
	else :
		real_url = get_real_url()
		if real_url is None:
			sys.stderr.write("\nlogin failed : May be you are already online.\n")
			exit()
		login(real_url, sys.argv[1], sys.argv[2])
