python3 -m venv env
source env/bin/activate
pip3 install -r ../requirements.txt
crontab -l > tmp
echo "0 */2 * * * sh /var/www/bots/lyres-dictionary/scripts/run.sh" >> tmp
crontab tmp
rm tmp
