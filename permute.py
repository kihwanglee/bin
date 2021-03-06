import os, argparse
from nltk.corpus import wordnet
# from nltk.corpus import words 

#>>>import nltk
#>>>nltk.download()
# wordnet/words package

parser = argparse.ArgumentParser(
    description = 'Permute letters.'
)
parser.add_argument(
    'letters',
    type = str,
    nargs = 1,
    help = 'Type letters without space.'
)
parser.add_argument(
    '-e',
    dest = 'eng',
    action = 'store_true',
    default = False,
    help = 'Show only English words of results. Note that it takes a rahter long time. Use the -r option together to remove duplicates.'
)
parser.add_argument(
    '-r',
    dest = 'row',
    action = 'store_true',
    default = False,
    help = 'Show results in a row.'
)
parser.add_argument(
    '-n',
    dest = 'number',
    action = 'store_true',
    default = False,
    help = 'Show results with number.'
)
parser.add_argument(
    '-s',
    dest = 'sort',
    action = 'store_true',
    default = False,
    help = 'Sort letters before permuting.'
)
parser.add_argument(
    '-p',
    dest = 'print',
    action = 'store_true',
    default = False,
    help = 'Print results in PDF using XeLaTeX. Only the -s option can be used with this option.'
)
parser.add_argument(
    '-heap',
    dest = 'heap',
    action = 'store_true',
    default = False,
    help = "Use Heap's algorithm. It is known as the fastest method of permutation in most cases."
)

args = parser.parse_args()
letters = list(args.letters[0])

num = 0
row = []

def permute(a, k=0):    
    global num
    global row
    if k == len(a):
        show(a)        
    else:        
        for i in range(k, len(a)):            
            a[k], a[i] = a[i] ,a[k]
            permute(a, k+1)
            a[k], a[i] = a[i], a[k]

# Heap's algorithm
def heap(a):
    n = len(a)
    idx = []
    for i in range(n):
        idx.append(0)
    show(a)
    i = 0
    c = 0
    while i < n:
        if idx[i] < i:
            if (i % 2) == 0:
                a[0], a[i] = a[i], a[0]
                # print(i, idx, a, "even")
            else:
                a[idx[i]], a[i] = a[i], a[idx[i]]
                # print(i, idx, a, "odd")
            show(a)
            idx[i] = idx[i] + 1
            i = 0
        else:
            idx[i] = 0
            i = i + 1
            # print(i, idx, a, "augment")

def show(a):
    global row
    global num
    result = ''.join(a)
    if args.eng:      
        if wordnet.synsets(result):
        # if result in words.words(): This method takes too much long
            if args.row:
                row.append(result)
            else:
                print(result)
    else:
        if args.row:
            if args.number:
                num = num + 1                
                row.append('[%d]%s' %(num, result))
            else:
                row.append(result)
        else:
            if args.number:
                num = num + 1
                print('%6d: %s' %(num, result))
            else:
                print(result)

def generate_pdf(letters):
    if os.path.exists('permute.tex'):
        os.remove('permute.tex')        
    content = """
    \\documentclass{article}
    \\usepackage{kotex}
    \\usepackage{xparse,expl3}
    \\ExplSyntaxOn
    \\tl_new:N \\l_out_tl
    \\NewDocumentCommand \\permuteword { m }
    {
        \\v_permute_word:nno { #1 } { 1 } { \\tl_count:n { #1 } }
    }
    \\cs_new:Npn \\v_permute_word:nnn #1 #2 #3
    {
        \\int_compare:nTF { #2 == #3 }
        {
            \\v_print_swapped_word:n { #1 }
        }
        {
            \\int_step_inline:nnn { #2 } { #3 }
            {
                \\v_tlswap_fn:nnnN { #2 } { ##1 } { #1 } \\l_out_tl
                \\v_permute_word:Von \\l_out_tl { \\int_eval:n { #2 + 1 } } { #3 }
            }
        }
    }
    \\cs_generate_variant:Nn \\v_permute_word:nnn { Von, nno }
    \\cs_new:Npn \\v_tlswap_fn:nnnN #1 #2 #3 #4
    {
        \\tl_clear:N #4
        \\tl_set:Nx \\l_tmpa_tl { #3 }

        \\int_step_inline:nn { \\tl_count:N \\l_tmpa_tl }
        {
            \\int_case:nnF { ##1 }
            {
                { #1 } { \\tl_put_right:Nx #4 { \\tl_item:Nn \\l_tmpa_tl { #2 } } }
                { #2 } { \\tl_put_right:Nx #4 { \\tl_item:Nn \\l_tmpa_tl { #1 } } }
            }
            {
                \\tl_put_right:Nx #4 { \\tl_item:Nn \\l_tmpa_tl { ##1 } }
            }
        }
    }
    \\cs_new:Npn \\v_print_swapped_word:n #1
    {
        \\mbox{ #1 }
        \\space\\space
    }
    \\ExplSyntaxOff
    \\setlength\\parindent{0pt}
    \\begin{document}
    \\permuteword{%s}
    \\end{document}
    """ %(letters)
    with open('permute.tex', mode='w', encoding='utf-8') as f:
        f.write(content)
    os.system('xelatex -interaction=batchmode permute.tex')

if args.sort:
    letters.sort()

if args.print:
    generate_pdf(''.join(letters))
else:
    if args.heap:
        heap(letters)
    else:
        permute(letters)
    if args.row:
        if args.eng:
            row = set(row)
        print(' '.join(row))