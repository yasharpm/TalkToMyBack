echo stopping

kill -9 `cat /home/opentalkz/api//talktomyback/myback_pid.txt`
rm -f /home/opentalkz/api/talktomyback/myback_pid.txt

echo stopped
