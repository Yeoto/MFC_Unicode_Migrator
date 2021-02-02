# MFC_Unicode_Migrator
이 프로그램은 Python 3.7.5에서 개발되었습니다. 필요한 모듈은 requirements.txt에 넣어두었습니다.

Visual C++/MFC의 MultiByte 기반 프로젝트에서 Unicode 프로젝트로 변경하면서 사용되는 유틸리티 스크립트입니다.
해당 스크립트의 MFC_Unicode_Migrator에 명령인자를 입력하여 실행 할 경우, 경로 내부에 있는 모든 파일을 Unicode 동작할 수 있도록 변경합니다.

**해당 스크립트는 완벽하지 않습니다. 직접 수정해야하는 부분도 있으며, 수정되는 부분에 대해서는 아래 문단을 참고해주시면 감사하겠습니다.**

## 명령 인자
사용 명령인자는 다음과 같습니다.
"Folder Path" "extension" "/Temp"
"Folder Path" : 수정할 파일의 경로입니다. 해당 경로의 모든 하위 폴더를 검색하여 수정합니다.
"extension" : 필터링 할 확장자입니다. 세미콜론으로 구분하여 지정합니다. 비어 있을 경우 모든 파일을 대상으로 수정합니다.
"/Temp" : 수정 할 때 Temp 파일을 만들어서 수정할 지 선택합니다. 해당 커맨드가 존재하지 않을 경우 덮어쓰기 합니다.

ex) python MFC_Unicode_Migrator.py "C:\MIDASIT\wbs\src" "" "/Temp"  ==> C:\MIDASIT\wbs\src 내부의 모든 확장자의 파일을 Temp 파일을 생성하여 수정합니다.
ex2) python MFC_Unicode_Migrator.py "C:\MIDASIT\wbs\src" ".cpp;.h" ""  ==> C:\MIDASIT\wbs\src 내부의 cpp, h파일을 직접 수정합니다.

## 사용 후 파일 변경사항
1. "Literal" 로 되어있는 상수 문자열을 _T() 매크로를 이용하여 감쌉니다.
	1. 단, #include, #pragma, extern "C", 주석 인 경우 무시합니다.
	1. 기존에 _T() 매크로로 감싸여있는 경우, 새로 감싸지 않습니다.
2. sprintf, strcmp 등 MultiByte 기반의 String 함수나, swprint, wcscmp 같이 Unicode 전용의 함수들을 _stprintf, _tcscmp 같은 TCHAR 전용 함수로 변경합니다.

## 직접 수정해야하는 부분
1. char를 TCHAR로 까지는 바꾸지 않습니다. 의도했던 기능이 char를 사용해야만 하는 부분이 많을수도 있어서 (색상 같은 경우) 일부러 하지 않았습니다.
2. **모든 리터럴 문자열을 변경하기 때문에 완벽하지 않습니다. 꼭 검증이 필요합니다.**
