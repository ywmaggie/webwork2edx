import script
import text
import code

s = '''

$x = random(1,3,1);
$y = random(1,2,1);
$z = random(5,9,1);

answer1 = 1.0*C(4($z-2),$y)C(12,$x)C(40-4($z-2),5-$y-$x)
answer2 = 1.0*C(4($z-2),$y)C(52-4($z-2),5-$y)
answer3 = 1.0*C(12,$x)C(40-4($z-2),5-$y-$x)/C(52-4($z-2),5-$y)
'''
t = '''*Find the probability that a poker hand of 5 cards from a standard deck will contain exactly [$x] face cards (i.e. J,Q,K) (event [`A`]), given that it contains exactly [$y] cards smaller than [$z] (i.e. 2,...,[$z-1])(event [`B`])"?*
    - [`|A \cap B| = `] [____________]{Compute("C(4($z-2),$y)C(12,$x)C(40-4($z-2),5-$y-$x)")}
    - [`|B| = `] [____________]{Compute("C(4($z-2),$y)C(52-4($z-2),5-$y)")}
    - The conditional probability [`P(A|B) = `] [____________]{Compute("C(12,$x)C(40-4($z-2),5-$y-$x)/C(52-4($z-2),5-$y)")}'''

'''  
m = code.MyCodeLexer()
m.build()
#m.test(s)
m.build_parser()
m.test_parser(s)
'''

n = text.MyTextLexer()
n.build()
#n.test(t)
n.build_parser()
print n.test_parser(t)

