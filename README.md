elasticsearch-definitive-guide
==============================
# EPUB/XHTML conversion

```bash
a2x --version > /dev/null
if [ $? != 0 ]; then
  yum install docbook2X -y # for Fedora based distro
  # apt-get install docbook2x -y # for Ubuntu based distro
  # brew install docbook2x # for Apple 
  [ $? == 0 ] && echo "Could not install docbook2 package... please try to install yourself, now exiting." && exit 1
fi
# one may install other dependencies regarding each environment (ie. libxml2)

git clone https://github.com/elasticsearch/elasticsearch-definitive-guide.git
cd elasticsearch-definitive-guide
a2x -d book -f epub|xhtml book.asciidoc -v # few minutes, be patient
```
Enjoy read of book.epub or book.xhtml (rename it by whatever you like).
