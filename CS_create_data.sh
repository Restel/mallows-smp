#!/bin/bash

#mkdir -p ./data/Uniform
#mkdir -p ./data/Mallows
#mkdir -p ./data/Polar
#rm -rf ./data/Uniform/*
#rm -rf ./data/Mallows/*
#rm -rf ./data/Polar/*
#declare -a phi_range=(0.1 0.3 0.5 0.7 0.9 1.0)
#num_rep=10
  #for n in 10
#	do
    # create Uniform
    #python3 ./CS_create_instance.py "U" "$n" $num_rep
    #for phi_m in "${phi_range[@]}"
    #do
    #  for phi_w in "${phi_range[@]}"
    #  do
    #  python3 ./CS_create_instance.py "M" "$n" $num_rep "$phi_m" "$phi_w"
    #  done
    #done
#	done

phi_m=0.5
phi_w=0.7
num_rep=1000
n=1000

python3 ./CS_create_instance.py "M" "$n" $num_rep "$phi_m" "$phi_w"
