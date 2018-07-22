# 1. 拉代码到 /var/www/yimclub
# 2. 执行 bash deploy.sh

set -ex

# 换源(云服务器不需要)
# ln -f -s /var/www/yimclub/misc/sources.list /etc/apt/sources.list
# mkdir -p /root/.pip
# ln -f -s /var/www/yimclub/misc/pip.conf /root/.pip/pip.conf
apt-get update

# 系统设置
apt-get -y install  zsh curl ufw
# sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
ufw allow 22
ufw allow 80
ufw allow 443
ufw allow 25
ufw default deny incoming
ufw default allow outgoing
ufw status verbose
ufw -f enable

# 装依赖
add-apt-repository -y ppa:deadsnakes/ppa

debconf-set-selections /var/www/yimclub/database_secret.conf
apt-get install -y mysql-server

debconf-set-selections /var/www/yimclub/postfix.conf
apt-get install -y postfix

apt-get install -y git supervisor nginx python3.6 redis-server
python3.6 /var/www/yimclub/get-pip.py
pip3 install jinja2 flask gevent gunicorn pymysql flask_sqlalchemy flask_mail redis

# 删掉 nginx default 设置
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default

# 建立一个软连接
ln -s -f /var/www/yimclub/yimclub.conf /etc/supervisor/conf.d/yimclub.conf
# 不要再 sites-available 里面放任何东西
ln -s -f /var/www/yimclub/yimclub.nginx /etc/nginx/sites-enabled/yimclub
chmod -R o+rwx /var/www/yimclub

# 初始化
cd /var/www/yimclub
python3.6 reset.py

# 重启服务器
service supervisor restart
service nginx restart

echo 'succsss'
echo 'ip'
hostname -I