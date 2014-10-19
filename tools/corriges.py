#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from argparse import ArgumentParser

class Function:
    """
an object that describe one occurrence of a function solution
provided in the corrections/ pacakge
it comes with a week number, a sequence number, 
a function name, plus the code as a list of lines
    """
    def __init__ (self, week, sequence, name):
        self.week=week
        self.sequence=sequence
        self.name=name
        self.code=[]
    def add_line (self, line):
        "convenience for the parser code"
        self.code.append(line)
# corriges.py would have the ability to do sorting, but..
# I turn it off because it is less accurate
# functions appear in the right week/sequence order, but
# not necessarily in the order of the sequence..
#    @staticmethod
#    def key (self):
#        return 100*self.week+self.sequence

class Source (object):
    
    def __init__ (self, filename):
        self.filename = filename

    def parse (self):
        "return a list of Function objects"
        function = None
        functions = []
        with open(self.filename) as input:
            for line in input:
                if '@BEG@' in line:
                    index = line.find("@BEG@")
                    end_of_line = line[index+5:].strip()
                    try:
                        week, sequence, name = end_of_line.split(' ')
                        function = Function (week, sequence, name)
                    except:
                        print "ERROR - ignored {} in {}".format(line,filename)
                elif '@END@' in line:
                    functions.append(function)
                    function = None
                elif function:
                    function.add_line(line)
        return functions

class Latex (object):

    header=r"""\documentclass [12pt]{article}
\usepackage[latin1]{inputenc}
\usepackage[francais]{babel}
\usepackage{fancyvrb}
\setlength{\oddsidemargin}{0cm}
\setlength{\textwidth}{16cm}
\setlength{\topmargin}{0cm}
\setlength{\textheight}{21cm}
\setlength{\headsep}{1.5cm}
\setlength{\parindent}{0.5cm}
\begin{document}
\centerline{\huge{%(title)s}}
\vspace{2cm}
\tableofcontents
\newpage
"""

    footer=r"""
\end{document}
"""

# utiliser les {} comme un marqueur dans du latex ne semble pas
# �tre l'id�e du si�cle
    function_format=r"""
\begin{minipage}{\textwidth}
\section{\texttt{%(function_latex)s} ({\small \footnotesize{Semaine} %(week)s \footnotesize{S�quence} %(sequence)s})}
\begin{Verbatim}[frame=single,fontsize=\small]
%(code_latex)s\end{Verbatim}
\end{minipage}
\vspace{1cm}
"""

    def __init__ (self, output):
        self.output = output

    def write (self, functions,title):
        with open(self.output, 'w') as output:
            output.write (Latex.header%(dict(title=title)))
            for function in functions:
                code_latex = "".join(function.code)
                function_latex = Latex.escape (function.name)
                week = function.week
                sequence = function.sequence
                output.write (Latex.function_format %locals())
            output.write (Latex.footer)
        print "{} (over)written".format(self.output)

    @staticmethod
    def escape (str):
        return str.replace ("_",r"\_")

def main ():
    parser = ArgumentParser ()
    parser.add_argument ("-o","--output", default=None)
    parser.add_argument ("-t","--title", default="Donnez un titre avec --title")
    parser.add_argument ("files", nargs='+')
    args = parser.parse_args()

    functions = []
    for filename in args.files:
        functions += Source(filename).parse()

# see above
#    functions.sort(key=Function.key)

    output = args.output if args.output else "corriges.tex"
    Latex(output).write (functions, title=args.title)

if __name__ == '__main__':
    main ()
