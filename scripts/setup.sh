crontab -l > tmp
echo "0 */2 * * * sh /var/www/bots/lyres-dictionary/scripts/run" >> tmp
crontab tmp
