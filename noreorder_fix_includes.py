#!/usr/bin/env python

##===----------------------------------------------------------------------===
##
##                     The LLVM Compiler Infrastructure
##
## This file is distributed under the University of Illinois Open Source
## License. See LICENSE.TXT for details.
##
## Copyright Tom Rix 2019, all rights reserved.
## 
##===----------------------------------------------------------------------===

import os.path
import sys
import xml.etree.ElementTree as xml

ret = 0

if os.path.isfile(sys.argv[1]):
  tree = xml.parse(sys.argv[1])
  root = tree.getroot()
else:
  sys.exit(ret)

ret = 1

for j in root:
  if j.tag == "files":
    for k in j:
      if k.tag == "file":
        path = k.attrib['path']
        f = open(path)
        if f:
          ln = f.readlines()
          f.close()
          f = open(path, "w")
          if f:
            # Prefix additions first
            n_lns = []
            for l in k:
              if l.tag == "prefixes":
                for m in l:
                  if m.tag == "line":
                    s = m.text + '\n'
                    n_lns.append(s)
            for n in n_lns:
              f.write(n)
            # Replacements
            n_lns = []
            cln_idx = int(1)
            for cln in ln:
              n_lns.append(cln)
              for l in k:
                if l.tag == "replacements":
                  for m in l:
                    if m.tag == "replacement":
                      line = int(m.attrib['line'])
                      if cln_idx == line:
                        n_lns = []
                        for n in m:
                          if n.tag == "lines":
                            for o in n:
                              if o.tag == "line":
                                s = o.text + '\n'
                                n_lns.append(s)
              for n in n_lns:
                f.write(n)
              n_lns = []
              cln_idx = cln_idx + 1
            f.close()
            ret = 0

sys.exit(ret)
