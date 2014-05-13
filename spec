#!/bin/bash
#
# spec - (c) Copyright 2014, Maxime Haineault

export TERM=xterm-256color
IPR="\b([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\b"
DARK="|192|0|8|16|17|18|19|20|21|232|233|234|235|236|237|238|239|240|"

if [ "$( tty )" == 'not a tty' ]; then
    STDIN_DATA_PRESENT=1
else
    STDIN_DATA_PRESENT=0
fi

if [[ $# -ne 1 && $STDIN_DATA_PRESENT -eq 0 ]]; then
    echo "\n    Syntax: tcpdump -nUl | spec --bits=24\n"
    exit 1
fi

# Parse arguments

while test $# -gt 0; do
    case "$1" in
        -h|--help)
            echo "spec - Color IPs"
            echo " "
            echo "tcpdump | spec [options] [arguments]"
            echo " "
            echo "options:"
            echo "-h, --help            show this help message"
            echo "-b, --bits=BITS       specify the bits to color"
            echo "-m, --mode=MODE       specify a mode to use [ octets | dots ]"
            exit 0
            ;;
        -m)
            shift
            if test $# -gt 0; then
                export MODE=$1
            else
                echo "no mode specified"
                exit 1
            fi
            shift
            ;;
        --mode*)
            export MODE=`echo $1 | sed -e 's/^[^=]*=//g'`
            shift
            ;;
        -b)
            shift
            if test $# -gt 0; then
                export BITS=$1
            else
                echo "no bits specified (8, 16, 24, 32)"
                exit 1
            fi
            shift
            ;;
        --bits*)
            export BITS=`echo $1 | sed -e 's/^[^=]*=//g'`
            shift
            ;;
        *)
    esac
done

if [[ -z "$BITS" ]]; then
    BITS=8
fi

if [[ -z "$MODE" ]] || [[ $MODE == "octets" ]]; then
    while read line; do
        D1="." ; D2="." ; D3="."
        B8="\x1b[38;5;\1m\1\x1b[0m"
        if [ "$BITS" == "24" ]; then
            B16="\x1b[38;5;\1m\2\x1b[0m"
            B24="\x1b[38;5;\1m\3\x1b[0m"
            B32="\x1b[38;5;\1m\4\x1b[0m"
        else
            B16="\x1b[38;5;\2m\2\x1b[0m"
            if [ "$BITS" == "16" ]; then
                B24="\x1b[38;5;\2m\3\x1b[0m"
                B32="\x1b[38;5;\2m\4\x1b[0m"
            else
                B24="\x1b[38;5;\3m\3\x1b[0m"
                if [ "$BITS" == "8" ]; then
                    B32="\x1b[38;5;\3m\4\x1b[0m"
                else
                    B32="\x1b[38;5;\4m\4\x1b[0m"
                fi
            fi
        fi
        echo $line | sed -r "s/$IPR/$B8$D1$B16$D2$B24$D3$B32/g"
    done
fi

if [[ $MODE == "dots" ]]; then
    while read line; do
        B8="\1\x1b[38;5;\1m.\x1b[0m"
        if [ "$BITS" == "24" ]; then
            B16="\2\x1b[38;5;\1m.\x1b[0m"
            B24="\3\x1b[38;5;\1m.\x1b[0m"
            B32="\4\x1b[38;5;\1m.\x1b[0m"
        else
            B16="\2\x1b[38;5;\2m.\x1b[0m"
            if [ "$BITS" == "16" ]; then
                B24="\3\x1b[38;5;\2m3\x1b[0m"
                B32="\4\x1b[38;5;\2m4\x1b[0m"
            else
                B24="\3\x1b[38;5;\3m.\x1b[0m"
                if [ "$BITS" == "8" ]; then
                    B32="\4\x1b[38;5;\3m.\x1b[0m"
                else
                    B32="\4\x1b[38;5;\4m.\x1b[0m"
                fi
            fi
        fi
        echo $line | sed -r "s/$IPR/$B8$B16$B24$B32/g"
    done
fi
