# spte
A command line tool to extract meaningful plaintext from .srt subtitle files, written in Python.

## Usage
Extract text for all .srt files in the current directory  
```>python spte.py``

Extract text for all .srt files in mypath  
```>python spte.py ~/mypath/```

Extract text from myfile.srt  
```>python spte.py ~/mypath/myfile.srt```

Extract text and remove style-tags  
```>python spte.py -s```

Extract text and remove blank lines  
```>python spte.py -b```
