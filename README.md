# xavier-server-tools
A set of various tools used on my personal server.
This set is a work in progress.

## IP address emailer - Done
### Summary
This tool emails me the server's public ip address whenever it changes.

### Motivation
Most residental modems are set up to change ip address upon reboot.
This is a problem if I want to access my server via `ssh` at anytime, I have no guarantee that the ip I have for my server is correct.

### How It Works
In order to circumvent this problem, the script at `ip_address_emailer.sh` will email my personal email address if the server's public ip differs from what it has stored within the log file.
It will then be run on a set interval using `crontab`.
Currently this is every 5 minutes using the `crontab`: `*/5 * * * * cd /home/xavier/Git_Repos/xavier-server-tools/ip_address_emailer && ./ip_address_emailer.sh`


## File Sorter - WIP
### Summary
Sorts files into appropriate places based on file type and creation date.

### Motivation
I have a hard drive filled with about 4.0 TB worth of photos, movies, music, etc from a previous windows server that used iTunes to sort various files.
I want to migrate these files to my Ubuntu server.
So developing a custom script to sort these files seems like a good idea and a good personal project.
