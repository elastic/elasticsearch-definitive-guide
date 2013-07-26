
==== Dealing with Stop-words

Stop-words are "filler" words that don't provide much information to a sentence.
Classic examples are words like "the", "and", "or", "but".  It is common to remove
stop-words in both structured and unstructured search.

Elasticsearch provides a `Stop` filter which can be configured to remove
words from the token stream.  Stop-words can be provided in the mapping itself
as an array of terms, or it can be configured in an external file.  If your
list of stop-words is large it is recommended to use the external file.

Importantly, stop-words in your list must match a token _exactly_ to be removed.
In almost all situations you should first lowercase the token stream before
removing stop-words.

If you didn't lowercase first, you may miss stop-words that have alternate case
(e.g. "The" vs "the").

An example mapping which places a `Stop` filter after `Lowercase`:


   "analysis":{
      "analyzer":{
         "default-analyzer":{
            "type":"custom",
            "tokenizer":"standard",
            "filter":[ "lowercase", "my_stop_filter" ]
         }
      },
      "filter":{
         "my_stop_filter":{
            "type":"stop",
            "stopwords":[
               "the", "a", "to", "but", "or", "and"
            ]
         }
      }
   }


