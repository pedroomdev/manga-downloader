#!/bin/bash -e
 
function helptext {
    echo "Usage: ./go <command>"
    echo ""
    echo "Available commands are:"
    echo "    setup                     Build python manga_downloader image"
    echo "    run                       Run manga_downloader.py from docker image"
}
 
function setup {
  docker-compose build manga_downloader
}
 
function run {
  docker-compose run manga_downloader
}
 
case "$1" in
    setup)
      setup
    ;;
    run)
      run
    ;;
    *) helptext
    ;;
esac