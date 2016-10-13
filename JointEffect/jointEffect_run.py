# coding:utf-8
def jointEffect_run():
    try:
        filePath = __file__
        app_Path = filePath.rpartition('\\')[0]
    except:
        print "Environ Value 'nm2_RIG' not exist."
    
    else:
        import sys
        path = app_Path
        
        if not path in sys.path:
            sys.path.append(path)
        
        import mainWindow as mainWindow
        reload(mainWindow)
        mainWindow.main()

if __name__ == 'jointEffect_run':  
    jointEffect_run()