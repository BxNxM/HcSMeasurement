#!/bin/bash

#while true; do clear; ps aux | grep "Manager" && ps aux | grep "Run"; sleep 1; done
#========================= STORED VARIABLES ================================#
myPath="`dirname \"$0\"`"
outputPath=${myPath}/systemCache/
inputsOption=$1
path_Python=python3
path_GUI_Manager=${myPath}/GUI_Manager.py
path_DATA_Manager=${myPath}/DATA_Manager.py
path_Calculate_Manager=${myPath}/Calculate_Manager.py
path_RunTimer=${myPath}/moduls/Runtimelib.py

path_pidfile=${outputPath}actualpids.txt
path_pidsMonitor=${outputPath}performanceMonitor.txt
stableMode_cahche=${outputPath}usrun_cache.txt
RunStateFile=${outputPath}runstate.txt

osName=`uname`

if [ ! -d $outputPath ]
then
    mkdir $outputPath
fi

#========================= FUNCTIONS =======================================#
function SetMonitorNeverSleep {

    if [ "$osName" == "Linux" ]
    then
        xset dpms force off
        xset -dpms
        xset s off
    fi
}

#--------------------------------------------------------------------------#
function Simple_fileReader {                                                                                                                        #FILE READER, READ FROM PATH TO ARRAY: search_line

 search_line=()

     while read line || [ -n "$line" ]
     do
         search_line+=($line)

     done < "$1"
}

function UltraStabileRun {

    isPidError=0

    #Lounch
    Lounch_HcS

    while true
    do
        Simple_fileReader $RunStateFile
        local rState=${search_line[0]}
        if [ "$rState" == "false" ]
        then
            break

        else


        Simple_fileReader $path_pidfile

        for ((i=0; i<${#search_line[@]}; i++))
        do
            local p=$(ps -p ${search_line[$i]} -o pid=)
            if [ "$p" == "" ]
            then
                isPidError=1
                echo -e "ERROR IN PID: ${search_line[$i]}, isPidError state: $isPidError"
            fi
        done

        if [ $isPidError -eq 1 ]
        then
            echo -e "PID ERROR -> START AUTO RECOVERY"
            echo -e "$(date) : PID ERROR -> START AUTO RECOVERY" >> $stableMode_cahche
            Kill_HcS
            UltraStabileRun
        fi

        sleep 1

        fi
     done
}
#--------------------------------------------------------------------------#
function Lounch_HcS {

    SetMonitorNeverSleep

    echo -e "Lounch $path_DATA_Manager"
    $path_Python $path_DATA_Manager &
    pid=$!
    echo -e "$pid" > $path_pidfile

    sleep .1

    echo -e "Lounch $path_GUI_Manager"
    export DISPLAY=:0
    $path_Python $path_GUI_Manager &
    pid=$!
    echo -e "$pid" >> $path_pidfile

    sleep .1

    echo -e "Lounch $path_Calculate_Manager"
    $path_Python $path_Calculate_Manager &
    pid=$!
    echo -e "$pid" >> $path_pidfile

    sleep .1

    echo -e "Lounch $path_RunTimer"
    $path_Python $path_RunTimer &
    pid=$!
    echo -e "$pid" >> $path_pidfile

}

#--------------------------------------------------------------------------#
function Kill_HcS {

    Simple_fileReader $path_pidfile

    for ((pidCnt=0; pidCnt<${#search_line[@]}; pidCnt++))
    do
        local namebyPID=$(ps -a ${search_line[$pidCnt]} | awk '{ print $5 }')
	if [ "$osName" == "Linux" ]
	then
	    namebyPID=$(ps aux | grep -v grep | grep ${search_line[$pidCnt]} | awk '{ print $12 }')
        fi
	echo -e "$namebyPID - killed ${search_line[$pidCnt]}"
        kill ${search_line[$pidCnt]}
    done
}

#--------------------------------------------------------------------------#
function Monitor_Performance {

    Simple_fileReader $path_pidfile

    while true
    do
       actualDate=$(date)
       echo "$actualDate :" >> $path_pidsMonitor
       for (( cnt=0; cnt<${#search_line[@]}; cnt++ ))
       do
            _PID_=${search_line[$cnt]}
            infobyPID=$(ps -p $_PID_ -o %cpu,%mem)
            namebyPID=$(ps -a $_PID_ | awk '{ print $5 }')
	    if [ "$osName" == "Linux" ]
	    then
                 namebyPID=$(ps aux | grep -v grep | grep $_PID_ | awk '{ print $12 }')
	     fi
             echo $infobyPID $namebyPID >> $path_pidsMonitor
        done

        sleep 5
    done
}

#--------------------------------------------------------------------------#
function ClearDatabase {

    path_database=DataBase/
    path_perform=performanceMonitor.txt
    path_actualpids=actualpids.txt

    runState="false"
    echo -e "$runState" > $RunStateFile
    sleep 1

    Kill_HcS

    echo -e "remove ${path_database}*.txt"
    rm ${path_database}*.txt

    echo -e "remove ${path_perform}"
    rm $path_perform

    echo -e "remove ${path_actualpids}"
    rm $path_actualpids

    sleep 1

    #Lounch_HcS
    UltraStabileRun

}

#========================= LOUNCH OPTION ==================================#
function RunOption {

    if [ "$inputsOption" == "run" ]
    then
        runState="true"
        echo -e "$runState" > $RunStateFile
        Lounch_HcS

        elif [ "$inputsOption" == "usrun" ]
        then
            runState="true"
            echo -e "$runState" > $RunStateFile
            UltraStabileRun

        elif [ "$inputsOption" == "kill" ]
        then
            runState="false"
            echo -e "$runState" > $RunStateFile
            Kill_HcS

            elif [ "$inputsOption" == "monitor" ]
            then
                Monitor_Performance

                elif [ "$inputsOption" == "cleanup" ]
                then
                    ClearDatabase

                    else
                        echo -e "No Input!"
                        maunal
    fi
}

#================================ MANUAL ==================================#
function maunal {

    echo -e "================================== HcS Measurement =================================="
    echo -e "============================== HcS - Hydroculture System ============================"
    echo -e "Oprtions avaible:"

    echo -e "=> run"
    echo -e "\tLounch all the components what HcS need."

    echo -e "=> usrun &"
    echo -e "\tLounch all the components is secure (chacked pids) what HcS need."
    
    echo -e "=> kill"
    echo -e "\tKill the HcS all components"


    echo -e "=> monitor"
    echo -e "\tMonitor performance, and save it to $path_pidsMonitor"


    echo -e "=> cleanup"
    echo -e "\tDelete the existing databse and $path_pidsMonitor and $path_pidfile"
    echo -e "====================================================================================="

}
#--------------------------------------------------------------------------#
RunOption
