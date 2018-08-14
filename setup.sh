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
