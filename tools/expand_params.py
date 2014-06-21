import sys
try:
    l = sys.argv[1].split(":");x,s,c = l[0].strip(),l[1].strip(),l[2].strip();c = c.split("@");s = ["" if s=="" else "-s " + s.strip()];c = [["" if i=="" else "-c " + i.strip()] for i in c];
    for cc in c: cc.extend(s); cc.extend(['"%s"'%x]);
    for cc in c: print " ".join(cc)
except IndexError:
    print '"%s"'%sys.argv[1].partition(":")[0]

