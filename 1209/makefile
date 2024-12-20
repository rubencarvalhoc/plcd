verbopt.freq: lemapos.totalpt.txt
	awk '{a+= $$1} END {print a}' lemapos.totalpt.txt >verbopt.freqABS
	rg "(\(V\)|\(V-AUX\))" -r "" lemapos.totalpt.txt| rg "r "|head -n 5000 >>verbopt.freqABS
	awk 'NR==1 {t = $$1} \
		NR>1 {print $$1/t*1000000, $$2}' verbopt.freqABS >verbopt.freqREL