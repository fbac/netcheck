#!/bin/bash
#
# Netchecker
# Use: ./netcheck <path-to-file>
#

for X in `grep -v '^#' $1`;
do
        START=$(date +%s%3N)
        HST=`echo $X | awk -F: '{print $1}'`
        PRT=`echo $X | awk -F: '{print $2}'`

        nslookup $HST >> /dev/null
        case "$?" in
                1)
                        END=$(date +%s%3N)
                        DIFF=$(($END - $START))
                        echo "${HST}:${PRT} | DNS record does not exist. | $DIFF ms"
                        ;;
                0)
                        (echo quit) | telnet $HST $PRT 2> /dev/null | grep "Connected to" >> /dev/null
                        if [ $? -eq 0 ];
                        then
                                END=$(date +%s%3N)
                                DIFF=$(($END - $START))
                                echo "${HST}:${PRT} | Success | $DIFF ms"
#                       else

                        fi
                        ;;
        esac
done
