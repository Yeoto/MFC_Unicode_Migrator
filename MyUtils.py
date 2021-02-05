import os
import regex as re
import openpyxl

class FunctionConvertor:
    def __init__(self):
        self.dict_StringFunc2GenericFunc = {}
        self.MakeDictonary()

    def MakeDictonary(self):
        load_wb = openpyxl.load_workbook("FunctionMapping.xlsx")
        load_ws = load_wb['Sheet1']

        for row in load_ws.rows:
            tchar_Func = row[0].value
            for i in range(1,4):
                TgtFunc = row[i].value
                self.dict_StringFunc2GenericFunc[TgtFunc] = tchar_Func

    def ConvertStringFunc2GenericFunc(self, line):
        pattern = re.compile('([\w_]+)')
        iter = pattern.finditer(line)

        match_list = list(iter)
        match_list.reverse()

        for match in match_list:
            strFunc = match.group()
            if strFunc in self.dict_StringFunc2GenericFunc:
                start = match.start(0)
                end = match.end(0)

                substring_1 = line[:start]
                substring_2 = line[end:]
                line = substring_1 + self.dict_StringFunc2GenericFunc[strFunc] + substring_2

        return line

def GetAllFileWithExt(path, wildcard, bNotFindUnder):
    Filtered_File = []
    filenames = os.listdir(path)
    for filename in filenames:
        full_path = os.path.join(path, filename)
        if bNotFindUnder == False and os.path.isdir(full_path):
            Filtered_File += GetAllFileWithExt(full_path, wildcard, False)
        if len(wildcard) > 1:
            ext = os.path.splitext(filename)[-1]
            if ext not in wildcard:
                continue
        Filtered_File.append(full_path)
    return Filtered_File

def ConvertAll(lines : list):
    new_lines = []
    FuncConv = FunctionConvertor()

    for line in lines:
        striped_line = line.strip()
        #문자열 적용 예외
        #주석인 경우, #include인 경우, #pragma인 경우, extern "C"인 경우
        if striped_line[0:2] == r"//" or striped_line[0:8] == "#include" or striped_line[0:7] == "#pragma" or striped_line[0:10] == "extern \"C\"":
            new_lines.append(line)
            continue

        line = ConvertLiteralString2TCHARString(line)
        line = FuncConv.ConvertStringFunc2GenericFunc(line)
        new_lines.append(line)

    return new_lines

def GetContinuousBackSlashCnt(line, start):
    nCnt = 0
    while start > 0:
        if line[start] == '\\':
            nCnt += 1
        else:
            break
        start -= 1
    return nCnt

def ConvertLiteralString2TCHARString(line):
    pattern = re.compile('(".*?")')

    iter = pattern.finditer(line, overlapped=True)
    indices = [(m.start(0), m.end(0)) for m in iter]

    Delete_Idx = []
    for tuple_idx in range(len(indices)-1, -1, -1):
        if tuple_idx in Delete_Idx:
            continue

        match_tuple = indices[tuple_idx]
        start = match_tuple[0]
        end = match_tuple[1]
        if start > 0 and end < len(line):
            if line[start-1] == '\'' and line[start+1] == '\'':
                continue
            if line[end-1] == '\'' and line[end+1] == '\'':
                continue
        
        match_tuple_next = indices[tuple_idx-1]
        if start > 1:
            if GetContinuousBackSlashCnt(line, start-1) % 2 == 1:
                indices[tuple_idx-1] = (match_tuple_next[0], end)
                continue

        if start < match_tuple_next[1] and match_tuple_next[1] < end:
            Delete_Idx.append(tuple_idx-1)

        if start >= 3 and end < len(line):
            if line[start-3:start] == "_T(" and line[end:end+1] == ")":
                continue

        if start >= 5 and end < len(line):
            if line[start-5:start] == "TEXT(" and line[end:end+1] == ")":
                continue

        if start >= 7 and end < len(line):
            pattern2 = re.compile(r'TRACE\d\(')
            if pattern2.match(line[start-7:start]) != None:
                continue

        substring_1 = line[:start]
        substring_2 = line[start:end]
        substring_3 = line[end:]

        line = substring_1 + "_T(" + substring_2 + ")" + substring_3

    return line