sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install git

cd ~/Desktop

FOLDER=RaspberryPlayer
URL=https://github.com/ShowroomSBRE/RaspberryPlayer.git

if [ ! -d "$FOLDER" ] ; then
    git clone "$URL" "$FOLDER"
fi

cd "$FOLDER"

echo "Now you need to :"
echo "sudo cp $FOLDER/tvplayer.service /lib/systemd/system/tvplayer.service"
echo "sudo chmod 644 $FOLDER/tvplayer.service "
echo "sudo systemctl daemon-reload"
echo "sudo systemctl enable tvplayer.service"