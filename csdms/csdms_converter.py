import fileinput
from sys import argv
from datetime import datetime
import json
import os.path

defaultCfgFileName = 'csdms_assumption_cfg.json'

cfgFileName = argv[1]
if not(os.path.isfile(cfgFileName)):
    if (cfgFileName != '-f'):
        print "Can not find file %s, will use %s instead." % (cfgFileName, defaultCfgFileName)
    cfgFileName = defaultCfgFileName

print "Getting configuration file for %s..." % cfgFileName
cfgLine = 0

# Get the appropriate configuration file for this type of output
with open(cfgFileName) as cfgFile:
    print cfgFile
    for line in cfgFile:
        # cfgLine += 1
        # print "cfgLine: %d = %s" % (cfgLine, line)
        while True:
            try:
                jfile = json.loads(line)
                break
            except ValueError:
                # Not yet a complete JSON value
                line += next(cfgFile)
        if jfile[0] == 'header_substitutions':
            header_substitutions = jfile[1]
        elif jfile[0] == 'limit_tags':
            limit_tags = jfile[1]
        elif jfile[0] == 'body_substitutions':
            body_substitutions = jfile[1]
        elif jfile[0] == 'output_file_info':
            output_file_info = jfile[1]
        else:
            print "Error, jfile[0] (%s) does not match any expected string." % jfile[0]
cfgFile.close()

# Open the desired output file for writing
ont_out = open(output_file_info['file_name'],'w')
print ont_out
write_count = 0

                     
# Replace the necessary fields in the header of the ontology (using template header)
template = open('template_hdr.owl')
headerLinesReplaced = 0
for line in template:
    for attributePattern, attributeValue in header_substitutions.items():
        if attributePattern in line:
            line = line.replace(attributePattern, attributePattern+attributeValue)
            headerLinesReplaced += 1
            # print "Replaced line with %s" % attributePattern
    ont_out.write(line)
    write_count += 1
template.close();
print "Replaced %d header elements." % headerLinesReplaced

# Replace relevant tags in the body of the source ontology. Print only the tags we care about.
stdnames = open("CSDMS_081.owl")
replaceTagCount = 0
printOn = False
lastLine = False
for line in stdnames:
    for tagItem in limit_tags['openTag']:
        if tagItem in line:
            printOn = True
    for tagItem in limit_tags['closeTag']:
        if tagItem in line:
            lastLine = True
    # ont_out.write(line + "PrintOn/LastLine = %r, %r" % (printOn, lastLine) )
    for tagPattern, tagReplace in body_substitutions.items():
        if tagPattern in line:
            line = line.replace(tagPattern, tagReplace)
            replaceTagCount += 1
    if printOn:
        ont_out.write(line)
        write_count += 1
    if lastLine:
        printOn = False
        lastLine = False

stdnames.close()

# Write the last line to the ontology file
ont_out.write("</rdf:RDF>")
ont_out.close()
doneAt = str(datetime.now())

print "Body tags replaced: %d" % replaceTagCount
print "Lines written: %d" % write_count
print "File written at %s." % doneAt