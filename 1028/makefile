# criação ficheiro latex
t1 SIC-PT_seccao.tex:
	python 1028.py >saida.txt

# html monobloco
t2 SIC-PT_seccao.tex:
	pandoc SIC-PT_seccao.tex -o SIC-PT_seccao.html -t html -s --metadata title="Industrial Codes"

# criaçao site html
t3 SIC-PT_seccao.tex:
	pandoc --metadata title="Industrial Codes" SIC-PT_seccao.tex -o  -t chunkedhtml -s --toc