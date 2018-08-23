sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install git

cd ~/Desktop

FOLDER=RaspberryPlayer
URL=https://github.com/ShowroomSBRE/RaspberryPlayer.git

if [ ! -d "$FOLDER" ] ; then
    git clone "$URL" "$FOLDER"
fi

sudo cp $FOLDER/tvplayer.service /lib/systemd/system/tvplayer.service
sudo chmod 644 /lib/systemd/system/tvplayer.service
sudo systemctl daemon-reload
sudo systemctl enable tvplayer.service

echo "Now, edit run.sh"