import MyUtils
import sys
import os
from tqdm import tqdm

def main():
    nSizeArg = len(sys.argv)

    if nSizeArg < 2:
        print('''잘못된 인수입니다.
        "File Path" [extension] [/Temp]
        "File Path" : 해당 폴더 포함 하위의 모든 파일이 수정 됩니다.
        "extendsion" : 세미콜론으로 구분된 확장자가 들어갑니다. 파일을 필터링 할 때 사용됩니다.
        [/Temp] : /Temp 입력 시 파일에 파일에 _Temp 을 붙여 생성합니다. 값 입력이 없을 경우 덮어쓰기 합니다.
        [/NoneRecursive] : /NoneRecursive 입력 시 하위 폴더는 제외하고 해당 경로의 파일만 검색합니다.
        ex) "C:\\MIDAS\\wbs\\src" ".cpp;.h"''')

    src_path = sys.argv[1]
    extension = []
    bMakeTemp = "/Temp" in sys.argv
    bNotFindUnder = "/NoneRecursive" in sys.argv

    if nSizeArg > 2:
        extension = sys.argv[2].split(';')

    FileList = MyUtils.GetAllFileWithExt(src_path, extension, bNotFindUnder)

    encoding_list = ['cp949', 'gb2312', 'utf-8', 'utf-8-sig']
    ErrorFiles = []
    for FilePath in tqdm(FileList):
        file_encoding = ''
        lines = []
        for encoding in encoding_list:
            file_encoding = encoding
            try:
                file = open(FilePath, 'r', encoding=encoding)
                lines = file.readlines()
            except UnicodeDecodeError:
                continue
            break

        if len(lines) == 0:
            ErrorFiles.append(FilePath)
            continue

        new_lines = MyUtils.ConvertAll(lines)

        split_list = os.path.splitext(FilePath)
        file_out = file
        if bMakeTemp == True:
            file_out = open( "".join(split_list[0:-1])+'_Temp'+split_list[-1], 'w', encoding=file_encoding )
        else:
            file_out = open( FilePath, 'w', encoding=file_encoding )

        file_out.writelines(new_lines)
    for ErrorFile in ErrorFiles:
        print("Can't Encoding This File! Path : {}".format(ErrorFile))
    
    return True

def testing():
    testing = r'FmtMessageBox(_LS(IDS_SDSw_Cannot_Find_Text_Editot_Program), sGENEdit);'
    FuncConv = MyUtils.FunctionConvertor()
    MyUtils.ConvertLiteralString2TCHARString(testing)

if __name__ == "__main__":
    main()