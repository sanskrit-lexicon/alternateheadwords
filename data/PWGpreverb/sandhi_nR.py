"""sandhi_nR.py
  Adapted from function sandhi_nR of elispsanskrit/pysanskritv1/sandhi.py.
  Inputs:  a string
           an option keyword nR_parm parameter, indicating an index
              within the string at which to start.  Defaults to 0.
  output: String adjusted for nR sandhi. (could be the same as input string)
"""
class init(object):
 # for some constants
 vowel_set = 'aiufxAIUFXeEoO'
 guttural_set = 'kKgGNhH'
 labial_set = 'pPbBmvH'

def sandhi_nR(xin,nR_parm=None):
 """ Antoine 17
  When, in the same word, 'n' is preceded by 'f', 'F', 'r', or 'z' and
  followed by a vowel or by 'n', 'm', 'y', or 'v', then it is changed to
  'R' even when there are letters between the preceding 'f' (etc) and 'n'
  provided these intervening letters be vowel, gutturals, labials, 
  'y', 'v', h', or 'M' (anusvAra).
  Returns None if no change
 """
 ifirst = nR_parm
 if not ifirst:
  ifirst = 0
 changed = False
 tokar = xin
 n = len(tokar)
 i = 0
 while ( i < n):
  x1 = tokar[i]
  i = i+1
  if x1 in 'fFrz':
   i1 = i
   i2 = None
   ok = False
   while (i < n):
    x2 = tokar[i]
    i = i+1
    if  (x2 == 'n') and (i < n):
     x3 = tokar[i]
     if (x3 in init.vowel_set) or (x3 in 'nmyv'):
      i = i - 1
      i2 = i
      i = n # break inner while loop
   i = i1
   if i2:
    # found a subsequent "n". Now check intervening letters
    ok = True
    while ok and (i < i2):
     y = tokar[i]
     if (y in init.vowel_set) or (y in init.guttural_set) or (y in init.labial_set) or (y in 'yvhM'):
      i = i + 1
     else:
      ok = False # breaks while loop
    if ok:
     if (ifirst <= i2):
      # make the change
      changed = True
      # recall tokar is a string so next does not work in Python
      #tokar[i2] = 'R'
      # rather:
      tokar = tokar[:i2]+'R'+tokar[i2+1:]
      i = i2 + 1
 return tokar
