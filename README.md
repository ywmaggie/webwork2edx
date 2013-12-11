webwork2edx
===========

Aim to translate PG format problems to edX/XML problems

This is a partially completed translator from webwork PG format to edX XML format.

To run the translator, use python yacc_v4.py to run nonrandomized problems. Run yacc_random.py and then run yacc_combine in the same folder for randomized problems.

If you want to test the result, copy the output in output.XML and paste to the edX studio and you can see the result.
