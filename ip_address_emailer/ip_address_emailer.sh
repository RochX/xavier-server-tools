# init log file
log_file="server_ip.log"
touch $log_file

# functions
# prepends the current datetime to an echo command
echo_time() {
  echo $(date) $@
}

log_current_ip() {
  touch $log_file
  echo_time "Current public ip is: " $current_ip >> $log_file
}

email_ip() {
  local mail_file="ip_address.mail"
  local mail_log="mail_history.log"
  touch $mail_file
  touch $mail_log
  printf "To: xavierwsilva+server@gmail.com\n" > $mail_file
  printf "From: xavierwsilva+server@gmail.com\n" >> $mail_file
  printf "Subject: %s IP\n\n" $(hostname) >> $mail_file
  printf "%s current public ip is: %s\n" $(hostname) $current_ip >> $mail_file
  cat $mail_file | msmtp -t -a default && echo_time "Emailed new ip: $current_ip." >> $mail_log
}

# main program
ip_website=https://ipv4.icanhazip.com/
last_ip=$(tail -n 1 server_ip.log | grep -E -o "(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}")
current_ip=$(curl $ip_website 2>/dev/null | grep -E -o "(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}")

log_current_ip

if [ -n "$current_ip" ]; then
  if [ "$current_ip" != "$last_ip" ]; then
    email_ip
    # echo "would email $current_ip here."
  fi
else
  echo_time "ERROR getting ip address from $ip_website" >> $log_file
fi
