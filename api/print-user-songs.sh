#!/bin/bash

SCRIPT_PATH=$(dirname $(readlink -f $0 ))
API_BASE='https://api.spotify.com/v1'
TOKEN_PATH="$SCRIPT_PATH/.token.secret"

api_call()
{
    local endpoint="$1"
    local payload="$2"
    local options=('--header' 'Content-Type: application/json' '--header' 'Accept: application/json')

    if test -n "$payload"; then
        options+=('-d' "$payload")
        options+=('-X' 'POST')
    else
        options+=('-X' 'GET')
    fi

    test -f "$TOKEN_PATH" && {
        local token=$(cat "$TOKEN_PATH")
        options+=('--header' "Authorization: Bearer $token")
    }

    curl -s "${options[@]}" "$API_BASE/$endpoint"
}

# Uncomment to debug any API
# api_call "$@" && exit

api_call "me/tracks?limit=$1"
