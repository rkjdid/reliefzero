#!/bin/bash

set -e
set -u

DIR="$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"
project_root="$(dirname $DIR)"

options="serverdeploy.options"
init_template="init.template"
init_path="$HOME/init"
lighttpd_conf="$HOME/lighttpd/django.conf"
lighttpd_template="lighttpd.template"
vpython="$HOME/v/relief/bin/python"

appendHttpConf() {
  # $1 : lighttpd template lines
  # $2 : file to append to
  # $3 : options file
  if [ ! -f "$1" ]; then error "$1 missing"; fi
  if [ ! -f "$2" ]; then error "$2 missing"; fi
  
  tmp=$(mktemp)
  cp "$1" "$tmp"
  replaceOptions "$tmp" "$3"
  echo "#--------------------------" >> "$2"
  echo >> "$2"
  cat "$tmp" >> "$2"
  rm -f "$tmp"
}

lighttpdRestart() {
  if ! lighttest; then
    error "error in configuration file, skipping restart of lighttpd, fix your lighttpd config files before restarting webserver"
  fi
  
  lightinit restart
}

makeInitScript() {
  # $1 : template file
  # $2 : destination
  # $3 : options file
  if [ ! -f "$1" ]; then error "$1 missing"; fi
  if [ ! -f "$3" ]; then error "$3 missing"; fi
  if [ -e "$2" ]; then error "$2 exists"; fi

  # append dirname to options file
  ! grep -q "___SHORT_PROJECT_NAME___" "$3" && echo "___SHORT_PROJECT_NAME___=$(basename $2)" >> $3

  cp "$1" "$2"
  chmod +x "$2"
  replaceOptions "$2" "$3"
}

initDjango() {
  # $1 : django initscript
  cwd="$(pwd)"
  cd "$project_root"
  if [ ! -f "$vpython" ]; then
    warning "$vpython does not exist, no virtualenv used."
    vpython="python"
  fi
  $vpython ./manage.py collectstatic
  $vpython ./manage.py schemamigration relief --initial
  $vpython ./manage.py syncdb
  $vpython ./manage.py migrate relief
  $1 start
  cd "$cwd"
}

replaceOptions() {
  # $1 : file to modify
  # $2 : file containing template values
  
  egrep -o '___.+___' "$1" |while read var; do
    opt=$(grep "$var" "$2" |sed 's,.*\=\(.*\)$,\1,')
    if [ -z "$opt" ]; then warning "$var not found in $2, skipping in $1"
    else eval $(echo "sed -i 's,$var,$opt,g' \"$1\"")
    fi
  done
}

warning() {
  if [ "$1" = "-q" ]; then
    shift
    pre=""
  else
    pre="warning: "
  fi

  echo "${pre}$@" >&2
}

error() {
  if [ "$1" = "-q" ]; then
    shift
    pre=""
  else
    pre="fatal: "
  fi
  
  echo "${pre}$@" >&2
  exit 1
}


makeInitScript "$init_template" "$init_path/$(basename $project_root)" "$options"
initDjango "$init_path/$(basename $project_root)"
appendHttpConf "$lighttpd_template" "$lighttpd_conf" "$options"
lighttpdRestart

