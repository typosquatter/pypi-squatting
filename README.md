# pypi-squatting

Searching for typosquatted packages in PyPi.

# Usage

~~~
usage: typo.py [-h] -p PACKAGENAME [-v] [-l LIMIT] [-var] [-ko] [-pr] [-o OUTPUT] [-fo FORMATOUTPUT] [-a] [-ada] [-add] [-cho] [-cddu] [-cm] [-hp] [-md] [-ns] [-om] [-repe] [-repl] [-sd] [-sp] [-vs]

optional arguments:
  -h, --help            show this help message and exit
  -p PACKAGENAME, --packageName PACKAGENAME
                        package name
  -v                    verbose, more display
  -l LIMIT, --limit LIMIT
                        limit of variations
  -var, --givevariations
                        give the algo that generate variations
  -ko, --keeporiginal   Keep in the result list the original package name
  -pr, --pypiresolver   Find which variations is a package on pypi
  -o OUTPUT, --output OUTPUT
                        path to ouput location
  -fo FORMATOUTPUT, --formatoutput FORMATOUTPUT
                        format for the output file, yara - regex - yaml - text. Default: text
  -a, --all             Use all algo
  -ada, --adddash       Add a dash between the first and last character in a string
  -add, --addition      Add a character
  -cho, --changeorder   Change the order of letters in word
  -cddu, --changedotdashunderscore
                        Change dot to dash
  -cm, --commonmisspelling
                        Change a word by is misspellings
  -hp, --homophones     Change word by an other who sound the same when spoken
  -md, --missingdot     Delete dots one by one
  -ns, --numeralswap    Change a numbers to words and vice versa. Ex: circlone.lu, circl1.lu
  -om, --omission       Leave out a letter
  -repe, --repetition   Character Repeat
  -repl, --replacement  Character replacement
  -sd, --stripdash      Delete of a dash
  -sp, --singularpluralize
                        Create by making a singular package name plural and vice versa
  -vs, --vowelswap      Swap vowels
~~~

# List of algorithms used

| Algo                    | Description                                                                                                                                                                                  |
|:----------------------- |:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AddDash                 | These typos are created by adding a dash between the first and last character in a string.                                                                                                   |
| Addition                | These typos are created by add a characters in the domain name.                                                                                                                              |
| ChangeDotDashUnderscore | These typos are created by changing a dot to a dash.                                                                                                                                         |
| ChangeOrder             | These typos are created by changing the order of letters in the each part of the domain.                                                                                                     |
| CommonMisspelling       | These typos are created by changing a word by is misspelling. Over 8000 common misspellings from Wikipedia. For example, www.abseil.com becomes www.absail.com.                              |
| Homophones              | These typos are created by changing word by an other who sound the same when spoken. Over 450 sets of words that sound the same when spoken. For example, www.base.com becomes www.bass.com. |
| MissingDot              | These typos are created by deleting a dot from the domain name.                                                                                                                              |
| NumeralSwap             | These typos are created by changing a number to words and vice versa. For example, circlone.lu becomes circl1.lu.                                                                            |
| Omission                | These typos are created by leaving out a letter of the domain name, one letter at a time.                                                                                                    |
| Repetition              | These typos are created by repeating a letter of the domain name.                                                                                                                            |
| Replacement             | These typos are created by replacing each letter of the domain name                                                                                                                          |
| StripDash               | These typos are created by deleting a dash from the domain name.                                                                                                                             |
| SingularPluralize       | These typos are created by making a singular domain plural and vice versa.                                                                                                                   |
| VowelSwap               | These typos are created by swapping vowels within the domain name except for the first letter. For example, www.google.com becomes www.gaagle.com.                                           |
