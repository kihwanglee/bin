# [Chrome]
# app = C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
# target =     
#     http://dic.daum.net/index.do?dic=eng 
#     http://www.ktug.org
# [FreeCommander]
# app = C:\Program Files\FreeCommander XE\FreeCommander.exe
# [VS Code]
# app = C:\Users\Hoze\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd

import os, sys, configparser, subprocess, codecs
try:
    inipath = os.environ['DOCENV'].split(os.pathsep)[0]
except:
    inipath = False
if inipath is False:
    inipath = os.path.dirname(sys.argv[0])
ini = os.path.join(inipath, 'daily.ini')
if os.path.exists(ini):        
    config = configparser.ConfigParser()
    # config.read(ini)
    with codecs.open(ini, 'r', encoding='utf-8') as f:
        config.readfp(f)
    for section in config.sections():
        try:
            app = config.get(section, 'app')
        except:
            app = ''
        try: 
            target = config.get(section, 'target')
        except:
            target = ''
        cmd = '\"%s\" %s' %(app, target.replace('\n', ' '))
        # cmd.encode(encoding='euc-kr')
        subprocess.Popen(cmd)
else:
    input('Daily.ini is not found. Set the DOCENV environment variable to the directory containing daily.ini. Press any key to exit.')