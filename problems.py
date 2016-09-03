import sudoku as sd

def top95():
	
	f = open("top95.txt")
	probs = []
	for p in f.readlines():
		probs.append(sd.Sudoku(9,p.strip()))
	return probs

def convert(f):

    return lambda: f().replace("\n","").replace("\t","").replace(" ","").replace("0",'.')

@convert
def sample():
    """
    Return a sample Problem instance0
    """
    return """000150070
        106000820
        300860040
        900400567
        004708300
        732006004
        040081009
        017000208
        050037000"""
    
@convert
def sample_hard():
    """
    Return a sample Problem instance0
    """
    return """400000805
        030000000
        000700000
        020000060
        000080400
        000010000
        000603070
        500200000
        104000000"""
    
@convert
def sample_tricky():
    """
    Return a "tricky" Problem instance from the paper0
    """
    return """003009081
        000200060
        500010700
        890000000
        005601200
        000000037
        009002008
        070004000
        250800600"""
    
@convert
def sample_moderate():
    """
    Return a "moderate" Problem instance from the paper0
    """
    return """005000700
        930504000
        840000030
        600020400
        500090008
        009080001
        050000070
        000307086
        001000900"""