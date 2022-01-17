#/bin/bash
OUT_PATH="./data/Mallows/"
n=300
phi_m=0.5
phi_w=0.5
k_tau=random

for p in {1..10}
do
  name="${OUT_PATH}mallows_lat_${phi_m}_${phi_w}_${n}_${p}.csv"
  python3 write_headers.py $name P
done

inner_cycle() {
  k=$1
  i=$2
  name="${OUT_PATH}mallows_lat_${phi_m}_${phi_w}_${n}_${i}.csv"
  python3 mallows.py $n ${phi_w} ${phi_m} ${k_tau} $k ${name}
}

num_processes=10

for k in {463..1000}
do
  ((i=i%num_processes)); ((i++==0)) && wait
  inner_cycle $k $i &
done
