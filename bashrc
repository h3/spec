# BEGIN SPEC

# SPEC tcpdump

if $(command -v tcpdump >/dev/null 2>&1) ; then 
    _TCPDUMP=$(whereis tcpdump | cut -d" " -f2)
    alias tcpdump.nocolors="exec $_TCPDUMP $@"
    function tcpdump () {
        if [[ $1 =~ "-n" ]] ; then
            exec $_TCPDUMP -Ul $@ | spec
        else
            exec $_TCPDUMP $@
        fi
    }
fi

# SPEC tshark

if $(command -v tshark >/dev/null 2>&1) ; then 
    _TSHARK=$(whereis tshark | cut -d" " -f2)
    alias tshark.nocolor="exec $_TSHARK $@"
    function tshark () {
        if [[ $1 =~ "-n" ]] ; then
            exec $_TSHARK -l $@ | spec
        else
            exec $_TSHARK $@
        fi
    }
fi

# END SPEC
