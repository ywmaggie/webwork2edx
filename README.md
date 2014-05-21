webwork2edx
===========

Aim to translate PG format problems to edX/XML problems

This is a partially completed translator from webwork PG format to edX XML format.

Folder 'class encapsulated' contains the most recent translator. Put all three files in the same folder. To run the translator, run 'python translate.py' and when you see '>     ', input the name of file that you want to transalte. Then you will get a XML file of the same name as the original file in the same folder.

Folder 'sample examples' contains all original PG files and the output XML files. You can see for reference.

Folder 'lex' and 'yacc' are old versions of the translator.

If you want to test the result, copy the output and paste to the edX studio and you can see the result.
