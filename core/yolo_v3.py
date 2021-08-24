from helper import *

class Yolo_V3:

    def change_content(self, content, path):
        import subprocess
        subprocess.call(["sed -i '" + content + "' " + path], shell=True)

    def __init__(self):
        import os
        if not os.path.exists("darknet"):
            try:
                from git import Repo
            except ModuleNotFoundError:
                self.install_module('gitpython')

            from git import Repo
            os.mkdir("darknet")
            Repo.clone_from("https://github.com/AlexeyAB/darknet", "./darknet")

        os.chdir('darknet')

        # change makefile to have GPU and OPENCV enabled
        self.change_content('s/OPENCV=0/OPENCV=1/', "Makefile")
        self.change_content('s/GPU=0/GPU=1/', "Makefile")
        self.change_content('s/CUDNN=0/CUDNN=1/', "Makefile")


    def install_module(self, module_name):
        import sys, subprocess
        print("Module 'git' is not installed ! \n Installing ...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', module_name])
        print("Finish installation !!!")


    def wget_package(self, name, url):
        import os
        if not os.path.exists(name):
            try:
                import wget
            except ModuleNotFoundError:
                self.install_module('wget')

            import wget
            wget.download(url)
            print("Finish download " + name)


    def imShow(self, path):
        try:
            import cv2
            import matplotlib.pyplot as plt

            image = cv2.imread(path)
            height, width = image.shape[:2]
            resized_image = cv2.resize(image,(3*width, 3*height), interpolation = cv2.INTER_CUBIC)

            fig = plt.gcf()
            fig.set_size_inches(18, 10)
            plt.axis("off")
            plt.imshow(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))
            plt.show()
        except AttributeError:
            raise TypeError("File not found !")

    def plot_image(self, path):
        import matplotlib.pyplot as plt
        from matplotlib.pyplot import figure
        figure(figsize=(50, 60), dpi=80)
        image = plt.imread(path)
        plt.imshow(image) 
        plt.show()