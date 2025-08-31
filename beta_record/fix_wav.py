from struct import pack, unpack


filename = "record_save/" + str(310774525446848514) + ".wav"
with open(filename, 'rb+') as f:
    wav_header = "4si4s4sihhiihh4si"
    data = list(unpack(wav_header,f.read(44))) #assign the data format as "4s i 4s 4s i h h i i h h 4s i"
    f.seek(0,2) #start the offset from the end of file
    filesize = f.tell() #the size of the file
    datasize = filesize - 44
    data[-1] = datasize
    data[1]  = datasize+36
    f.seek(0) #start the offset from the start of file
    f.write(pack(wav_header, *data)) #repack the wav file