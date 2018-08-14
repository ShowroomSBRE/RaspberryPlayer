cd ~/Desktop/RaspberryPlayer

git pull

sudo apt-get update
sed 's/#.*//' apt-get.txt | xargs sudo apt-get -y install

pip install -r requirements.txt

python RaspberryTVShowroom/run.py ~/Desktop/RaspberryPlayer/exampleConfig.txt