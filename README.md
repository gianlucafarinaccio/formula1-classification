1. preprocessing --> prende i file originali, riduzione fps e dimensioni, filtri ecc --> video adattati 
2. tagger --> prende il file json, un video adattato 
	--> lista di coppie di intervalli ok
	--> nomepilota__idcurva__idframe ---> 0_1 2 3 4  
	---> mette in ogni directory i frame degli intervalli specificati
3. main ---> 