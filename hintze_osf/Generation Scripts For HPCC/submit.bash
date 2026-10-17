#for temp in 0.1 0.3 0.5 0.9 1.1 1.3
#do
#    sbatch --array=0-99 --export=ALL,temp=$temp,save=0 newRunThis.sb
#done
#sbatch --array=0-99 --export=ALL,temp=0.7,save=1 newRunThis.sb
sbatch --array=0-2 --export=ALL,temp=0.7,save=1 newRunThis.sb
