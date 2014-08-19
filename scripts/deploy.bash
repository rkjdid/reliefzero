#!/bin/bash

DIR="$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"
root_dir="$(dirname $DIR)"

options="$DIR/deploy.options"
debug="true"
overwrite="false"

crawltemplates() {
  find "$root_dir" -not -path "$root_dir/scripts/*" -name "*.template" |while read template; do
    echo $template
    toreplace "$template" |while read target; do
      target=$(echo "$target" |sed 's,__$,,')
      if [ -f "$target" ]; then
        if [ "$overwrite" != "true" ]; then
          echoerr "$target exists and overwrite set to false, skipping"
          continue
        fi
        debug "removing existing $target (overwrite set to true)"
        rm -f "$target"
      fi

      cp "$template" "$target"
      [ "settings.py" = "$(basename $target)" ] && chmod og-rwx "$target"

      egrep -o '___.+___' "$target" |while read var; do
        if [ "$var" = "___SECRET_KEY___" ]; then
          opt=$(generateKey)
        else
          opt=$(grep "$var" "$options" |sed 's,.*\=\(.*\)$,\1,')
        fi

        if [ -z "$opt" ]; then
          echoerr "warning: $var found in $l, but not present $options, stays as is"
        else
          debug "sed -i 's,$var,$opt,g' $target"
          eval $(echo "sed -i 's,$var,$opt,g' \"$target\"")
        fi
      done

      if [ "config.rb" = "$(basename $target)" ]; then
        type compass > /dev/null 2>&1 || { echoerr "compass required but it's not installed. scss files won't be compiled"; continue; }
        cwd="$(pwd)"
        cd "$(dirname $target)"
        compass compile
        cd "$cwd"
      fi
    done; echo
  done
}

toreplace() {
  find $(dirname $1) -name "$(basename $1 |sed 's,\.template,__,')" |while read line; do
    debug "target: $line"
    echo "$line"
  done
}

generateKey() {
  </dev/urandom tr -dc '1234567890!@#$%qwertQWERTasdfgASDFGzxcvbZXCVB\-_' | head -c50
}

echoerr() {
  echo "$@" 1>&2
}

debug() {
  if [ "$debug" = "true" ];
    then echoerr "dbg: $@"
  fi
}

if [ ! -f "$options" ]; then
  echoerr "error: option file \"$options\" not found"
  exit 1
fi

chmod og-rwx "$options"

crawltemplates
