elasticsearch-definitive-guide
==============================
# EPUB/PDF conversion

```bash
#!/bin/sh 

which a2x > /dev/null 2>&1
if [ $? != 0 ]; then
  which yum > /dev/null 2>&1
  [ $? = 0 ] && manager="yum"
  which apt-get > /dev/null 2>&1
  [ $? = 0 ] && manager="apt-get"
  echo "Need to install some packages: docbook2X fop libxml2"
  if [ "$manager" = "yum" ]; then
    sudo yum install docbook2X fop libxml2-devel -y # for Fedora based distro
  elif [ "$manager" = "apt-get" ]; then
    sudo apt-get install docbook2x libxml2-utils fop -y # for Ubuntu based distro
  else 
    echo "Your package manager is not yum neither apt-get, please manually install equivalent packages of: docbook2X fop libxml2-utils" && exit 1
  fi
  [ $? != 0 ] && echo "Error occured when installing packages... exiting" && exit 1
fi

git clone https://github.com/elasticsearch/elasticsearch-definitive-guide.git elasticsearch-definitive-guide
[ $? != 0 ] && echo "Cannot clone git project, exiting" && exit 1

cd elasticsearch-definitive-guide || exit 1

ln -s ../callouts images/icons

a2x -d book -f epub book.asciidoc -v # generates book.epub in few minutes, be patient

a2x -d book -f pdf --fop book.asciidoc -v # generates book.pdf
```
Enjoy read of book.epub or book.pdf (rename it by whatever you like).
