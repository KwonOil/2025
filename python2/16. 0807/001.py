print(f"__file__:{__file__}")

import os

dirinfo = os.path.abspath(__file__)

print(f"현재 파일 경로 : {dirinfo}")
print(f"디렉토리 경로 : {os.path.dirname(dirinfo)}")
print(f"파일 이름 : {os.path.basename(dirinfo)}")