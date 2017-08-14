def lineID( aLine, aCommentType ):
    if aLine.find( "\n" ) != -1:
        print "ERROR: Multiple lines sent to lineID!"
        return -1
    lTagBuffer = ""
    lIndex = 0
    lIsCommented = False
    
    for i in aLine:
        if i == " " or i == "\t":
            pass
        elif i == aCommentType:
            lIsCommented = True
        elif lTagBuffer == "" and i == "<":
            lTagBuffer += i
        elif lTagBuffer + i == "</":
            return ["tag_end",lIsCommented, lIndex - 1]
        else:
            if lTagBuffer == "<":
                return ["tag_start",lIsCommented, lIndex - 1]
            else:
                return ["text",lIsCommented, lIndex]
        lIndex += 1

def xmlIndenter( aText ):
    lTabWidth = 4
    lCommentType = "#"
    
    lText = aText.replace("\r","")
    lText = lText.split("\n")
    
    # tag_start, tag_end, text
    lType = ""
    lType_Prev = ""
    lReturn = ""
    lIndent_lvl = 0
    
    for i in lText:
        lID = lineID( i, lCommentType )
        if lID == -1:
            return lID
        lType_Prev = lType
        lType = lID[0]
        
        # Figure out indentation levels
        if lType_Prev == "tag_start" and ( lType == "tag_start" or lType == "text" ):
            lIndent_lvl += 1
        elif ( lType_Prev == "tag_end" or lType_Prev == "text" ) and ( lType == "tag_end" ):
            lIndent_lvl -= 1
        
        # Add new line characters as appropriate
        if lReturn != "":
            lReturn += "\n"
        
        # Figure out spacing
        lSpace_ct = lIndent_lvl * lTabWidth
        if lID[1] and lSpace_ct > 1:
            lSpace_ct -= 2
            lReturn += lCommentType + " "
        lReturn += ( lSpace_ct * " " ) + i[lID[2]:].strip()
    return lReturn
