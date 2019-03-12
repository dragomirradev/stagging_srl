#!/bin/bash

cat  |
  grep -v "^\s*$" |
  sort |
  uniq -c |
  sed 's/^ *//g' |
  sort -bnr |
  awk ' { t = $1; $1 = $2; $2 = t; print } '
