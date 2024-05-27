import subprocess

working_directory = '/media/liyanfeng/1TSata/trunk_proj/Tools/osg-dev-kit/lsp-server'

def get_method(lua_file:str):
    process = subprocess.Popen(['java','-jar','-Demmy.port=5007','-Dcmd=0','-Dextractor=1','-Daction=list','-DfilePath='+lua_file,'-Dfun=Create,Destroy','-Dconfig=luacompiler.json','-DMT=0','EmmyLua-LS-all.jar'], cwd=working_directory, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # 获取输出和错误
    stdout, stderr = process.communicate()
    # 打印输出
    print(stdout.decode())

    # 检查是否有错误
    if process.returncode != 0:
       print(stderr.decode())
    
    pass

def extract_file(lua_file:str,method:str,ctor:str):
    arg = '-func='+method if ctor else '-func={},{}'.format(ctor,method)
    process = subprocess.Popen(['java','-jar','filePath='+lua_file,arg,'-Dconfig=luacompiler.json','-drop_decl','-list=0'], cwd=working_directory, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # 获取输出和错误
    stdout, stderr = process.communicate()
    # 打印输出
    print(stdout.decode())

    # 检查是否有错误
    if process.returncode != 0:
       print(stderr.decode())
    with open(working_directory+'/extract_file.txt', 'r',encoding='utf-8') as file:
       content = file.read()
       return content
    
if __name__ == '__main__':
   extract_file('Logic\UISystem\Libraries\UI\UIHeroDetailInfoShowData.lua','UIHeroDetailInfoShowDataClass:tests','UIHeroDetailInfoShowDataClass:ctor')
   pass