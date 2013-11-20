from lexer import *

data = '''
   DOCUMENT();        # This should be the first executable line in the problem.

loadMacros(
  "PGstandard.pl",
  "PGML.pl",
  "MathObjects.pl",
  "PGcourse.pl",
  "contextIntegerFunctions.pl"
);


TEXT(beginproblem);
$showPartialCorrectAnswers = 1;

######################################################################

BEGIN_PGML

*Like the previous question, suppose you have been dealt "4[`\heartsuit`], 5[`\heartsuit`]".*

*What is the conditional probability that you will get a hand at least as high as a full house, given that you have been dealt these two cards, and that the flop is "3[`\heartsuit`], 4[`\spadesuit`], K[`\diamondsuit`]"?* Note that ranks that are higher than full house are four-of-a-kind, straight flush and royal flush.
    - To make a full house or four of a kind, need to get two cards out of the remaining cards whose ranks are 4 or 5. The number of such card pairs, ignoring order, is [____________]{Compute("C(5,2)")}.
    - We can also get a 4 and either 3 or K to make a full house. The number of such card pairs, ignoring order, is [____________]{Compute("2*6")}.
    - A third possibility is to draw two K's or two 3's. The number of such card pairs, ignoring order,  is [____________]{Compute("3*2")}.
    - The final possibility is a straight flush. The number of such card pairs, ignoring order, is [____________]{Compute("3")}.
    - The conditional probability is [____________]{Compute("(C(5,2)+2*6+3*2+3)/C(52-5,2)")}

END_PGML


######################################################################

ENDDOCUMENT();        # This should be the last executable line in the problem. 
    '''
lex.input(data)

for tok in iter(lex.token, None):
    print repr(tok.type), repr(tok.value)