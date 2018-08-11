## 论坛

仿CNode的论坛项目，后端使用 Flask MySQL SQLAlchemy  Redis 开发，Jinja2 模版渲染 HTML，前端使用 Bootstrap 美化样式，最后用 nginx+supervisor+gunicorn部署。

[DEMO](http://www.yim7.com/)

![image](https://github.com/yim7/yim-club/blob/master/bbs.gif)

## 功能

- [x] 用户注册、登录、注销
- [x]  用户主页/设置
- [x]  话题发表，话题删除（用户删除自己的话题），话题修改
- [x] 支持 markdown和代码高亮
- [x]  回复发表，回复删除
- [x]  用户通过在回复中 '@[用户名]' 可通知用户
- [x] 使用Token 防御CSRF攻击
- [x] 管理员功能，管理员可以修改删除话题，发送邮件
- [x] 管理后台，可以直接在后台批量管理
- [x] 给论坛发表和修改加上用户权限验证，管理后台验证管理员权限

## 部署

### 安装

```
git@github.com:yim7/yim-club.git
pip install flask sqlalchemy flask-sqlalchemy flask-admin jinja2
```
### 配置文件

需要创建两个配置文件  `secret.py` and `database_secret.conf`

```
# secret.py
secret_key = 'test'
database_password = 'test'
database_name = 'test'
test_mail = 'test@gmail.com'
admin_mail = 'admin@yim7.com'
```
```
# database_secret.conf
mysql-server mysql-server/root_password password test
mysql-server mysql-server/root_password_again password test
```
### 运行

```
# reset database
python3 reset.py

python3 app.py
```
你可以点击 http://localhost:2000 浏览论坛了

```
测试账号：test
密码：123
```



### 一键部署

```
bash deploy.sh
```