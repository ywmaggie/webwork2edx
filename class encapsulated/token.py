import text
import code

while 1:
	filename = raw_input('>')	
	file = open(filename)
	data = file.read()
	file.close()

	script_begin = data.find('$showPartialCorrectAnswers = 1;')+len('$showPartialCorrectAnswers = 1;')
	script_end = data.find('BEGIN_PGML')
	word_begin = script_end + 10
	word_end = data.find('END_PGML')

	script = data[script_begin:script_end]
	word = data[word_begin:word_end]



	n = text.MyText()
	n.build()
	#n.test(t)
	n.build_parser()
	t = n.test_parser(word)
	answer = n.MyAnswer()

	m = code.MyCode()
	m.build()
	#m.test(s)
	m.build_parser()
	#print script+'\n'+answer
	c = m.test_parser(script+'\n'+answer)

	filename_split = filename.find('.pg')
	write_file = open(filename[:filename_split]+'.xml','w')
	write_file.write( c+t)
	write_file.close()
	print '***'


