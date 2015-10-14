How to build book locally
----

Install asciidoctor.org and PDF plugin.
 
HTML
```
asciidoctor  elasticsearch-definitive-guide/book.asciidoc  -d book -a toc
```
 
PDF
```
asciidoctor -r asciidoctor-pdf -d book -b pdf -a toc elasticsearch-definitive-guide/book.asciidoc
```
