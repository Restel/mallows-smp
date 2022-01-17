#/bin/bash
OUT_PATH="./data/phis/"
n=15
declare -a phi_range=(0.1 0.3 0.5 0.7 0.9 1.0)
k_tau=0

for p in {1..10}
do
  name="${OUT_PATH}mallow_phi_M_W_scores_SE__${phi_m}_${phi_w}KT_${k_tau}_P{p}.csv"
  python3 write_headers.py $name P
done

inner_cycle() {
  k=$1
  i=$2
  name="${OUT_PATH}mallows_la${phi_m}_${phi_w}_${n}_${i}.csv"
  python3 mallows.py $n ${phi_m} ${phi_w} ${k_tau} $k ${name}
}

num_processes=10

for k in {1..1000}
do
  ((i=i%num_processes)); ((i++==0)) && wait
  inner_cycle $k $i &
done
