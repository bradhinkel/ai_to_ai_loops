#for temp in 0.1 0.3 0.5 0.9 1.1 1.3
#sbatch --array=0-99 --export=ALL,temp=0.1,save=1 OSFnewRunThis.sb
#sbatch --array=0-99 --export=ALL,temp=0.3,save=1 OSFnewRunThis.sb
#sbatch --array=0-99 --export=ALL,temp=0.5,save=1 OSFnewRunThis.sb
#sbatch --array=0-99 --export=ALL,temp=0.7,save=1 OSFnewRunThis.sb
#sbatch --array=0-99 --export=ALL,temp=1.1,save=1 OSFnewRunThis.sb
#sbatch --array=0-99 --export=ALL,temp=1.3,save=1 OSFnewRunThis.sb
#sbatch --array=81 --export=ALL,temp=1.3,save=1 OSFnewRunThis.sb
#sbatch --array=80 --export=ALL,temp=1.3,save=1 OSFnewRunThis.sb
for generator in 0 1 2 3
do
    for identifier in 0 1 2 3
    do
        sbatch --array=0 --export=ALL,temp=0.7,save=1,generator=$generator,identifier=$identifier OSFnewRunThis.sb
    done
done
#sbatch --array=78 --export=ALL,temp=1.3,save=1 OSFnewRunThis.sb
#sbatch --array=38 --export=ALL,temp=1.3,save=1 OSFnewRunThis.sb
#sbatch --array=18 --export=ALL,temp=1.3,save=1 OSFnewRunThis.sb
#sbatch --array=17 --export=ALL,temp=1.3,save=1 OSFnewRunThis.sb
#sbatch --array=16 --export=ALL,temp=1.3,save=1 OSFnewRunThis.sb

#sbatch --array=64 --export=ALL,temp=1.1,save=1 OSFnewRunThis.sb
#sbatch --array=65 --export=ALL,temp=1.1,save=1 OSFnewRunThis.sb
#sbatch --array=97 --export=ALL,temp=1.1,save=1 OSFnewRunThis.sb
