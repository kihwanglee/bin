import os, sys, glob, argparse

parser = argparse.ArgumentParser(
    description = 'Make an album with image files in the current directory.'
)
parser.add_argument(
    '-s',
    dest = 'scale',
    default = 1,
    help = 'image scale (default: 1)'
)
parser.add_argument(
    '-o',
    dest = 'output',
    default = 'album',
    help = 'output filename (default: album)'
)
parser.add_argument(
    '-k',
    dest = 'keep',
    action = 'store_true',
    default = False,
    help = 'keep collateral files'
)
args = parser.parse_args()

tex = args.output + '.tex'
pdf = args.output + '.pdf'
if os.path.exists(pdf):
    answer = input('%s already exists. Are you sure to remake it? [y/N] ' %(pdf))
    if answer.lower() == 'y':
        os.remove(pdf)
    else:
        sys.exit()

# Make a file of list of image files
image_list = []
image_type = ['pdf', 'jpg', 'png']
list_file = 't@mp.t@mp'
for i in range(len(image_type)):
    fnpattern = '*.' + image_type[i]
    for afile in glob.glob(fnpattern):
        image_list.append(afile)
image_list.sort()
image_list = '\n'.join(map(str,image_list))
with open(list_file, mode='w') as f:
    f.write(image_list)

# Make a tex file with this content
content = """
\\documentclass{hzguide}
\\usepackage{multicol}
\\LayoutSetup{paper=A4}
\\HeadingSetup{type=report}
\\begin{document}
\\begin{multicols}{2}
\\MakeAlbum[%d]{%s}
\\end{multicols}
\\end{document}""" %(args.scale, list_file)
with open(tex, mode='w') as f:
    f.write(content)

os.system('xelatex %s' %(tex))
os.system('texclean.exe')
os.system('open.exe %s' %(pdf))
if not args.keep:
    os.remove(list_file)
    os.remove(tex)