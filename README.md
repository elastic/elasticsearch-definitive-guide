elasticsearch-definitive-guide
==============================
# EPUB conversion

```bash
a2x --version > /dev/null
if [ $? != 0 ]; then
  yum install docbook2X -y # for Fedora based distro
  # apt-get install docbook2x -y # for Ubuntu based distro
  [ $? == 0 ] && echo "Error occured when installing docbook2 package... exiting" && exit 1
fi
git clone https://github.com/elasticsearch/elasticsearch-definitive-guide.git
a2x -d book -f epub book.asciidoc -v # few minutes, be patient
```
Enjoy read of book.epub (rename it by whatever you like).
