#!/bin/bash
input_file="./top95.txt"
file_n=1
while IFS='' read -r line || [[ -n "$line" ]]; do
    line=$(echo "$line" | sed -e 's/\(.\)/\1 /g' )
    echo "$line"
    file_name=$(echo "$file_n.txt")
    echo "$line" > "sudoku/$file_name"
    let file_n++
done < "$1"      
