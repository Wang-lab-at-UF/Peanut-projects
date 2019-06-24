#!/bin/env python3
#Usage: python mstrg_prep.py stringtie_merged_se.gtf > stringtie_merged_se_IDmodified.gtf
#appending refgene name to stringtie assigned gene ID (MSTRG.*) if the gene region includes a ref gene

import re, fileinput
g = {} #gene_id => {ref_gene_ids}
prep = [] #array of [line, mstrg_id]
for line in fileinput.input():
  line = line.rstrip()
  t = line.split('\t')
  if len(t) < 9:
    print(line)
    continue
  mgid = re.search('gene_id "(MSTRG\.\d+)"', t[8])                #search if GeneID in annotation column .
  if mgid:
    gid = mgid.group(1)            #matched geneID
    prep.append([line, gid])
    #mrn = re.search('ref_gene_id "([^"]+)', t[8])
    #or if you want gene_name:
    mrn = re.search('gene_name "([^"]+)', t[8])
    if mrn:            
      rn = mrn.group(1)
      h = g.get(gid)
      if h: 
        h.add(rn)
      else: g[gid] = { rn }
  else:
    print(line)

prevgid, gadd = '', ''
for [line, gid] in prep:
  if prevgid != gid:
    gadd = ''
    h = g.get(gid)
    if h:
      gadd = '|'+'|'.join(sorted(g[gid]))
  if len(gadd) > 0:
    line=re.sub('gene_id "MSTRG\.\d+', 
       'gene_id "' + gid + gadd, line)
  print(line)
