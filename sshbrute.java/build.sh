#! /bin/bash
printf "warning: the JSch package will be stored under /usr/share/jsch!\n"
printf "warning: all temporary downloads will be stored under /tmp/build-tmp!\n"

printf "\nfetching JSch package... \n"
mkdir -p /usr/share/jsch
wget https://sourceforge.net/projects/jsch/files/jsch.jar/0.1.54/jsch-0.1.54.jar/download -q --show-progress -O /usr/share/jsch/jsch.jar

printf "\ndownloading sshbrute source...\n"
mkdir /tmp/build-tmp
returndir=$(pwd)
wget http://github.com/TheDefalt/general/raw/master/sshbrute.java/sshbrute.java -q --show-progress -O /tmp/build-tmp/sshbrute.java
wget http://github.com/TheDefalt/general/raw/master/sshbrute.java/MANIFEST.MF -q --show-progress -O /tmp/build-tmp/MANIFEST.MF

printf "\ncompiling sshbrute.java... "
cd /tmp/build-tmp
javac -cp .:/usr/share/jsch/jsch.jar sshbrute.java

printf "\nbuilding executable JAR file... "
jar cfm sshbrute.jar MANIFEST.MF sshbrute.class > /dev/null
chmod +x sshbrute.jar
mv sshbrute.jar $returndir

printf "\ncleaning up... \n"
rm -r /tmp/build-tmp

printf "\ndone!\n"
