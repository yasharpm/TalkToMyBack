echo starting

# nohup /usr/local/bin/python3.7 talktomyback.py > myback.log &1>2 &

cd /home/talktome/Python-3.7.0
nohup ./python /home/talktome/talktomyback/talktomyback.py > myback.log &

echo $! > /home/talktome/talktomyback/myback_pid.txt

echo started
