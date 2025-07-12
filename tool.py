from opcode import opmap
from colorama import Fore, init
init()

class Patch:
    def __init__(self, filename, operation, operand, replaceOpCode):
        self.file = filename
        self.opcode = opmap[operation]
        self.operand = f'{operand:x}'.zfill(2).upper()
        self.r = opmap[replaceOpCode]

    def readBinary(self, skipHeader=True):
        with open(self.file, 'rb') as i:
            if skipHeader:
                i.read(16)
            return i.read()

    def FindByte(self, data):
        lst = list()
        locations = list()
        d = list()

        for index, i in enumerate(data):
            lst.append(f'{i:x}'.zfill(2).upper())
            if i == self.opcode:
                locations.append(index)
        for n in locations:
            try:
                if lst[n+1] != self.operand:
                    d.append(n)
            except:
                pass
        for n in d:
            locations.remove(n)
        return locations

    def Show(self, data):
        out = '0'*8+'\t'
        counter = int()

        for i in [data[i:i+16] for i in range(0,len(data),16)]:
            for n in i:
                if n == self.opcode:
                    out += Fore.RED
                else:
                    out += Fore.RESET
                out += f'{n:x}'.zfill(2).upper()+' '

            counter += 16
            out += '\n'+f'{counter:x}'.zfill(8)+'\t'
        return out[:-10:]

    def Patch(self, outfile, number):
        patched = bytearray(self.readBinary(0))
        data = bytearray(self.readBinary())
        locations = self.FindByte(data)
        out = self.Show(data)
        print(out)
        for counter, n in enumerate(locations):
            if counter >= number:
                break
            patched[n+16] = self.r
        with open(outfile, 'wb') as i:
            i.write(patched)


x = Patch('FILENAME.pyc', 'OPERATION', 0000, 'OPERATION THAT YOU WANT TO REPLACE')
x.Patch('OUT_FILE.pyc', 1)