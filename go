#!/bin/bash -e
 
function helptext {
    echo "Usage: ./go <command>"
    echo ""
    echo "Available commands are:"
    echo "    setup                     Build python manga_downloader image"
    echo "    run                       Run manga_downloader.py from docker image"
}
 
function setup {
  docker rmi -f manga-downloader_manga_downloader
  docker-compose build manga_downloader
}
 
function run {
  URL=$2
  KEYWORD=$3
  docker-compose run -e URL=$URL -e KEYWORD=$KEYWORD manga_downloader 
}
 
case "$1" in
    setup)
      setup
    ;;
    run)
      run $@
    ;;
    *) helptext
    ;;
esac