import re, glob

replacements = {}
regexp_replacements = {}

def init():
  quotes = [re.compile('^"([^"]+)" "([^"]+)"$'), re.compile('^"([^"]+)" ([^ "]+)$'), 
            re.compile('^([^ "]+) "([^"]+)"$'), re.compile('^([^ "]+) ([^ "]+)$')]
  for filePath in glob.glob("./replacements/*.txt"):
    file = open(filePath, "r")
   
    for line in file.readlines():
      line = line.strip()
      if line.startswith('#'):
        continue
      i = 0
      found = False
      while True:
        r = quotes[i].match(line)
        if r:
          src = r.group(1)
          trg = r.group(2)
          replacements[re.escape(src)] = trg
          found = True
          break
        i = i + 1
        if i == 4:
          break
      if not found:
        print ("Error in line: ", line, "(", filePath, ")")

    quotesRegexp = re.compile('^"(.+)" "(.+)" "(.+)"$')
    for filePath in glob.glob("./replacements/*.regexp"):
      file = open(filePath, "r")
      for line in file.readlines():
        line = line.strip()
        if line.startswith('#'):
          continue
        if "#" in line:
          line = line.split("#")[0].strip()
        r = quotesRegexp.match(line)
        if r:
          src = r.group(1)
          trg = r.group(2)
          regexp_replacements[src] = trg
        else:
          print ("Error in line: ", line, "(", filePath, ")")

init()
output = open("replace-all.sh", "w")
output.write("path=$1\n")
for src in replacements:
  trg = replacements[src]
  output.write('echo "Searching: ' + src + ' in file ${path}"\n')
  output.write(u'sed -i "s/\\b'+src+'\\b/'+trg+'/g" ${path}\n')
for src in regexp_replacements:
  trg = regexp_replacements[src]
  output.write('echo "Searching: ' + src + ' in file ${path}"\n')
  output.write(u'sed -i -E "s/'+src+'/'+trg+'/g" ${path}\n')

