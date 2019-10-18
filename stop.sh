echo stopping

kill -9 `cat /home/talktome/talktomyback/myback_pid.txt`
rm -f /home/talktome/talktomyback/myback_pid.txt

echo stopped
