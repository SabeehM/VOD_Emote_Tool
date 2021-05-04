class StringUtil:
    @staticmethod
    def stringSearch(text, substr, base):
        goalHash = hashInit(substr, base)
        currentHash = 0
        window_start = 0
        if(len(substr)>len(text)):
            return False
        for window_end in range(len(text)):
            if(goalHash == currentHash and text[window_start:window_end]==substr):
                return True
            if(window_end-window_start <= len(substr)-1):
                currentHash = hashUpdate(currentHash, text[window_end], None, base, (window_end-window_start-1))
            else:
                currentHash = hashUpdate(currentHash, text[window_end], text[window_start], base, (window_end-window_start-1))
                window_start+=1
        if(goalHash == currentHash and text[window_start:window_end+1]==substr):
                return True
        return False

def hashInit(sequence, base):
    lenSeq = len(sequence)
    baseCount = lenSeq-1
    hashVal = 0
    for x in range(lenSeq):
        hashVal+= ord(sequence[x])*(base**(baseCount-x))
    return hashVal

def hashUpdate(num, new, old, base, lenSeq):
    ordOld = 0 if old is None else ord(old)
    return(int(num-ordOld*(base**(lenSeq)))*base+ord(new))

    