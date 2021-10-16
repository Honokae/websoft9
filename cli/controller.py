import model, os, sys, subprocess, re
from model import GitOp

path_repo = "./data/application.list"
path_project = ""

# for Git clone HA
github_url = ("https://github.com", "https://hub.fastgit.org", "https://github.com.cnpmjs.org")

class Print:
    
    def __init__(self):
        pass
    
    def printRepo():
        model.FileOp.printJson(path_repo)


class Create:
    
    def __init__(self, app_name: str, project_name: str):
        
        self.folder = None
        self.app_name = app_name
        self.project_name = project_name
        
        if self.project_name != None:
            self.folder = self.project_name
        else:
            self.folder = self.app_name
    
    def downRepo(self):
        '''download repository'''
        
        geturl = model.SmoothUrl()
        gitop = model.GitOp()
        
        cmd = "git clone --depth=1 " + geturl.res(github_url) + "/websoft9/docker-" + self.app_name + " " + self.folder
        if os.path.exists("./"+self.folder):
            print(os.path.abspath(self.folder)+" folder already exists")
            sys.exit(0)
        else:
            gitop.gitClone(cmd)
            
    def setEnv(self):
        '''reset the password | port | container_name for application'''
        
        fileop=model.FileOp(self.folder+'/.env')
        securityop=model.SecurityOp()
        netop=model.NetOp()
        
        env_dict = fileop.fileToDict()
        env_str = fileop.fileToString()
        port_list = []
        
        for key in list(env_dict.keys()):
            if env_dict[key] in ["", "True", "False"]:
                del env_dict[key]

        for key,value in env_dict.items():
            # replace password
            if re.match('\w*PASSWORD',key,re.I) != None:
                env_str = env_str.replace(key+"="+value, key+"="+securityop.randomPass())
                
            # replace port
            if re.match('\w*PORT',key,re.I) != None:
                port = int(value)
                while port in port_list or not netop.checkPort(port):
                    port = port + 1
                port_list.append(port)
                env_str = env_str.replace(key+"="+value, key+"="+str(port))
            
            # replace app_container 
            if re.match('\w*APP_CONTAINER_NAME',key,re.I) != None:
                env_str = env_str.replace(key+"="+value, key+"="+self.folder)
                
            # replace app_network 
            if re.match('\w*APP_NETWORK',key,re.I) != None:
                env_str = env_str.replace(key+"="+value, key+"="+self.folder)
            
            fileop.stringToFile(env_str)
            
    def upRepo(self):
        '''docker-compose up repository'''
        
        cmd_up = "docker-compose up -d"
        cmd_down = "docker-compose down -v"
        os.chdir(self.folder)
        
        try:
            os.system(cmd_up)
        except:
            print("Create failed")
            os.system(cmd_down)
            sys.exit(0)
        
    def printResult(self):
        pass
    

class Manage(model.DockerComposeOp):
    pass

