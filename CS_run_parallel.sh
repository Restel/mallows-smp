#/bin/bash
mkdir -p ../../results/outputs/Our_comparisons/parallel/
# rm ../../results/outputs/Our_comparisons/*
OUT_PATH="../../results/outputs/Our_comparisons/parallel/"
JAR_PATH="../../target/stable-marriage-1.0.jar"
SUF=""
#SUF=".zip"

inner_cycle() {
  k=$1
  declare -a ALG_LIST=("GS_MaleOpt" "GS_FemaleOpt"  "PowerBalance -c SEq" "iBiLS -c SEq -p 0.125" "exhaustive_search -c SEq" "LDS -ss 0" "LDS -ss 1" "EDS -ss 0" "EDS -ss 1" "PDB -ss 0" "PDB -ss 1")
  for n in 20 50 100 150
		do
				for impl in "${ALG_LIST[@]}"
				do
					time java -cp ${JAR_PATH} cslab.ntua.gr.algorithms.$impl -n "$n" -m "../../../SMP_python/data/Mallows/n_${n}/men${k}_n${n}${SUF}.txt" -w "../../../SMP_python/data/Mallows/n_${n}/women${k}_n${n}${SUF}.txt" >> "${OUT_PATH}outM_${n}"
					echo $impl Mallows distribution Number of agents $n , Iteration $k

          time java -cp ${JAR_PATH} cslab.ntua.gr.algorithms.$impl -n "$n" -m "../../../SMP_python/data/Polar/n_${n}/men${k}_n${n}${SUF}.txt" -w "../../../SMP_python/data/Polar/n_${n}/women${k}_n${n}${SUF}.txt" >> "${OUT_PATH}outP_${n}"
					echo $impl Polar distribution Number of agents $n , Iteration $k
					done
		done
}

num_processes=10

for k in {501..850}
do
  ((i=i%num_processes)); ((i++==0)) && wait
  inner_cycle $k &
done
