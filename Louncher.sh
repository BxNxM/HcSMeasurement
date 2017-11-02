#!/bin/bash

#================================================= ARG PARSER =====================================================
# get arg list pcs
args_pcs=$#
# get arg list
arg_list=($@)

# script path n name
MY_PATH="`dirname \"$0\"`"
MY_NAME="`basename \"$0\"`"

# ------------------- SET ARG PARSER ----------------#
function init() {
    #__________________________!!!!!!!!!___________________________#
    ########################## SET THESE ###########################
    known_args=("man" "debug" "run" "usrun" "kill" "monitor" "cleanup" "lmess" "button_resetdatabase" "resetruntime")                             # valid arg list - add new args - call with -- expl: --man
    known_args_subs_pcs=(0 0 0 0 0 0 0 0 0 0)                                               # values for args - expl: --man -> 0, --example -> 1 etc.
    man_for_args=("--man\t\t::\tmanual"\                                        # add help text here
                  "--run\t\t::\tlounch HcSMeasurement application,  ${known_args_subs_pcs[2]} par"\
                  "--usrun\t\t::\tlounch HcSMeasurement application on safe mode(*), ${known_args_subs_pcs[3]} par"\
                  "--kill\t\t::\tstop HcSMeasurement application, ${known_args_subs_pcs[4]} par"\
                  "--monitor\t::\tmonitoring application processes, ${known_args_subs_pcs[5]} par"\
                  "--cleanup\t::\tcean database${known_args_subs_pcs[6]} par"\
                  "--lmess\t\t::\tshow realtime logs for HcS ${known_args_subs_pcs[7]} par"\
                  "--button_resetdatabase\t::\tgui button cmd for HcS ${known_args_subs_pcs[8]} par"\
                  "--resetruntime\t::\tgui button cmd for HcS ${known_args_subs_pcs[9]} par"\
                  "(*) usrun - ultra safe run - if any process dies automacly restart it.")
    #______________________________________________________________#
    ################################################################
    known_args_status=()
    known_args_value=()
    error_happened=0

    for init_value in "${known_args[@]}"
    do
        # set value to one
        known_args_status+=("0")
        known_args_value+=("")
    done
}

#--- VALIDATE LISTS SYNCRON & ERRORS & ARG VALUES ---#
function validate() {

    if [[ "${known_args_value[*]}" == *"--"* ]] || [ "$error_happened" -eq 1 ]
    then
        echo -e "[!!!] args error, use --man for more info."
        exit 400
    fi

    if [ "${#known_args[@]}" -ne "${#known_args_subs_pcs[@]}" ]
    then
        echo -e "[!!!] config error, known_args len and known_args_subs_pcs len is not equel!"
        exit 401
    fi

    validcommandwasfind=0
    for iscalled in "${known_args_status[@]}"
    do
        validcommandwasfind=$((validcommandwasfind+iscalled))
    done
    if [ "$validcommandwasfind" -eq 0 ] && [ "$args_pcs" -gt 0 ]
    then
        echo -e "[!!!] valid arg not find, use --man for more info."
        exit 402
    fi
}

# ----------------- ARG PARSER CORE ----------------#
function arg_parse() {
    error_happened=0
    for((i=0;i<"${#arg_list[@]}";i++))
    do
        for((k=0;k<"${#known_args[@]}";k++))
        do
            buffer=""
            case "${arg_list[$i]}" in
                "--${known_args[$k]}")
                    # set value to one
                    known_args_status[$k]="1"
                    args_max=$((i + ${known_args_subs_pcs[$k]} + 1))
                    #echo -e "arg max: $args_max"
                    if [ ${#arg_list[@]} -eq $args_max ] || [ ${#arg_list[@]} -gt $args_max ]
                    then
                        for((args_val="$((i+1))"; args_val<="$i"+"${known_args_subs_pcs[$k]}"; args_val++))
                        do
                            buffer+="${arg_list["$args_val"]} "
                        done
                        known_args_value[$k]="$buffer"
                    else
                       echo -e "${arg_list[$i]} arg required ${known_args_subs_pcs[$k]} parameter, $((${known_args_subs_pcs[$k]}+args_pcs-args_max)) were given"
                        error_happened=1
                        known_args_status[$k]="0"
                    fi
                    # debug message
                    #Message="ARGS METCHED: ${arg_list[$i]} <=> ${known_args[$k]}"
                    ;;
            esac
        done
    done
}

# ------------------- GET STATUS FOR ARG -------------#
function get_arg_status() {
    key="$1"
    for((index=0;index<"${#known_args[@]}";index++))
    do
        if [ "$key" == "${known_args["$index"]}" ]
        then
            echo "${known_args_status["$index"]}"
        fi
    done
}

# ---------------- GET VALUE(S) FOR ARG ---------------#
function get_arg_value() {
    local key="$1"
    local bare_output=""
    for((index=0;index<"${#known_args[@]}";index++))
    do
        if [ "$key" == "${known_args["$index"]}" ]
        then
            bare_output=$(echo "${known_args_value["$index"]}" | sed 's/^ *//g' | sed 's/ *$//g')       # HANDLE TRAILING WHITESPACES
            echo "${bare_output}"
        fi
    done
}

# ---------------------- MAN PAGE --------------------#
function man() {
    if [ "$(get_arg_status "man")" -eq 1 ]
    then
        for manpage in "${man_for_args[@]}"
        do
            echo -e "$manpage"
        done
    fi
}

function debug_print() {
    echo -e "KNOWN ARGS: ${known_args[*]}\t\t\t:::   known arguments"
    echo -e "KNOWN ARGS SUB ELEMENTS PIECES: ${known_args_subs_pcs[*]}\t\t\t:::   known args reguired parameters pieces"
    echo -e "KNOWN ARGS STATUS: ${known_args_status[*]}\t\t\t\t:::   args status, is colled?"
    echo -e "ARGS ARGS VALUE(S): ${known_args_value[*]}\t\t\t\t:::   args reguired read parameters"
}

# ------------------- MAIN FUNCTION -------------------#
function argParseRun() {
    init
    arg_parse
    validate
    if [ "$(get_arg_status "debug")" -eq 1 ]
    then
        debug_print
    fi
    man
}
#======================================================================================================================================

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
    nohup $path_Python $path_DATA_Manager &> "${outputPath}/HcSapp.log" &
    pid=$!
    echo -e "$pid" > $path_pidfile

    sleep .1

    echo -e "Lounch $path_GUI_Manager"
    export DISPLAY=:0
    nohup $path_Python $path_GUI_Manager &> "${outputPath}/HcSapp.log" &
    pid=$!
    echo -e "$pid" >> $path_pidfile

    sleep .1

    echo -e "Lounch $path_Calculate_Manager"
    nohup $path_Python $path_Calculate_Manager &> "${outputPath}/HcSapp.log" &
    pid=$!
    echo -e "$pid" >> $path_pidfile

    sleep .1

    echo -e "Lounch $path_RunTimer"
    nohup $path_Python $path_RunTimer &> "${outputPath}/HcSapp.log" &
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
    local msg=""

    while true
    do
       clear
       msg="DATE: $(date)\n"
       for (( cnt=0; cnt<${#search_line[@]}; cnt++ ))
       do
            _PID_=${search_line[$cnt]}
            infobyPID=$(ps -p $_PID_ -o %cpu,%mem)
            namebyPID=$(ps -a $_PID_ | awk '{ print $5 }')
	    if [ "$osName" == "Linux" ]
	    then
                 namebyPID=$(ps aux | grep -v grep | grep $_PID_ | awk '{ print $12 }')
	     fi
            if [ "$namebyPID" == "" ]
            then
                namebyPID="Died process:"
            fi
            msg+="${namebyPID}\tPID:${_PID_}\n${infobyPID}\n"
        done
        echo -e "$msg"
        echo -e "$msg" >> $path_pidsMonitor

        sleep 5
    done
}

#--------------------------------------------------------------------------#
function CleanUP {

    local restart_after_cleanup="$1"
    local database="$2"
    local runtime="$3"
    local full="$4"

    local restart_after_cleanup="$1"
    if [ -z "$restart_after_cleanup" ]
    then
        restart_after_cleanup="true"
    fi
    path_database=DataBase/
    path_systemcache=systemCache/

    runState="false"
    echo -e "$runState" > $RunStateFile
    sleep 1

    Kill_HcS

    if [ "$database" == "true" ] || [ "$full" == "true" ]
    then
        echo -e "remove database ${path_database}*.txt"
        rm ${path_database}*.txt
    fi

    if [ "$full" == "true" ]
    then
        echo -e "remove systemcache ${path_systemcache}*.txt and ${path_systemcache}*.log"
        rm ${path_systemcache}*.txt
        rm ${path_systemcache}*.log
    fi

    if [ "$runtime" == "true" ]
    then
        echo -e "remove runtime ${path_systemcache}runtime.txt"
        rm ${path_systemcache}runtime.txt
    fi

    sleep 1

    if [ "$restart_after_cleanup" == "true" ]
    then
        #Lounch_HcS
        UltraStabileRun &
    fi
}

function lmess() {
    while true
    do
        echo -e "tail -f ${outputPath}/HcSapp.log"
        sleep .5
        tail -f "${outputPath}/HcSapp.log"
    done
}

#========================= LOUNCH OPTION ==================================#
function RunOption {

    argParseRun
    if [ "$args_pcs" -eq 0 ]
    then
        echo -e "No input argument! for more info use: ${MY_PATH}/${MY_NAME} --man"
    fi

    # check arg was called
    if [ "$(get_arg_status "run")" -eq 1 ]
    then
        runState="true"
        echo -e "$runState" > $RunStateFile
        Lounch_HcS
    fi

    # check arg was called
    if [ "$(get_arg_status "usrun")" -eq 1 ]
    then
            runState="true"
            echo -e "$runState" > $RunStateFile
            UltraStabileRun &
    fi

    # check arg was called
    if [ "$(get_arg_status "kill")" -eq 1 ]
    then
            runState="false"
            echo -e "$runState" > $RunStateFile
            Kill_HcS
    fi

    # check arg was called
    if [ "$(get_arg_status "monitor")" -eq 1 ]
    then
            Monitor_Performance
    fi

    # check arg was called
    if [ "$(get_arg_status "cleanup")" -eq 1 ]
    then
            CleanUP "false" "false" "false" "true"
    fi

    # check arg was called
    if [ "$(get_arg_status "lmess")" -eq 1 ]
    then
            lmess
    fi

    if [ "$(get_arg_status "button_resetdatabase")" -eq 1 ]
    then
            CleanUP "true" "true" "false" "false"               #restart, database, runtime, full
    fi

    if [ "$(get_arg_status "resetruntime")" -eq 1 ]
    then
            CleanUP "false" "false" "true" "false"
    fi
}
#--------------------------------------------------------------------------#
RunOption
