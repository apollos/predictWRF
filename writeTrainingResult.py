import os
import os.path

trainResult = "trainResult.txt"
def writeIOTraingResult(IOfeatures):
    fr = open(trainResult, 'wr')
    if not IOfeatures:
        fr.write("Empty result for IOfeatures");
    else:
        for key in IOfeatures.keys():
            str1 = "%s: " %(key)
            for subkey in IOfeatures[key].keys():
                str1 = str1 + "%s:%f; " % (subkey, IOfeatures[key][subkey])
            fr.writelines(str1+"\n")
    fr.close()
    
