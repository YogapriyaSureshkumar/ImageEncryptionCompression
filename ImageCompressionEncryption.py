import os
import wx
import numpy as np
import cv2
import matplotlib.image as img
import numpy as np
from PIL import Image
from numpy import asarray


class PhotoCtrl(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Photo Control')
                          
        self.panel = wx.Panel(self.frame)
        self.PhotoMaxSize = 240
        
        self.createWidgets()
        self.frame.Show()
        
    def createWidgets(self):
        instructions = 'Browse for an image'
        img = wx.EmptyImage(240,240)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.BitmapFromImage(img))
        
        instructLbl = wx.StaticText(self.panel, label=instructions)
        self.photoTxt = wx.TextCtrl(self.panel, size=(200,-1))
        browseBtn = wx.Button(self.panel, label='Browse')
        browseBtn.Bind(wx.EVT_BUTTON, self.onBrowse)
        browseBtn1 = wx.Button(self.panel, label='DCT')
        browseBtn1.Bind(wx.EVT_BUTTON, self.onDct)
        browseBtn2 = wx.Button(self.panel, label='Encryption')
        browseBtn2.Bind(wx.EVT_BUTTON, self.onEncryp)
        browseBtn3 = wx.Button(self.panel, label='Dcryption')
        browseBtn3.Bind(wx.EVT_BUTTON, self.onDcryp)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                           0, wx.ALL|wx.EXPAND, 5)
        self.mainSizer.Add(instructLbl, 0, wx.ALL, 5)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
        self.sizer.Add(self.photoTxt, 0, wx.ALL, 5)
        self.sizer.Add(browseBtn, 0, wx.ALL, 5)
        self.sizer.Add(browseBtn1, 0, wx.ALL, 5)
        self.sizer.Add(browseBtn2, 0, wx.ALL, 5)
        self.sizer.Add(browseBtn3, 0, wx.ALL, 5)
        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)
        
        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
        self.panel.Layout()
        
    def onBrowse(self, event):
        """ 
        Browse for file
        """
        wildcard = "PNG files (*.jpeg)|*.jpeg"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoTxt.SetValue(dialog.GetPath())
        dialog.Destroy() 
        self.onView()
    def onView(self):
        filepath = self.photoTxt.GetValue()
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW,NewH)
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.panel.Refresh()
    def onDct(self, event):
        # read the input image
        filepath = self.photoTxt.GetValue()
        img1 = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img1.GetWidth()
        H = img1.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img1 = img1.Scale(NewW,NewH)
        img = cv2.imread(filepath)
        # convert from BGR to RGB so we can plot using matplotlib
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # disable x & y axis
        plt.axis('off')
        # show the image
        plt.imshow(img)
        plt.show()
        # get the image shape
        rows, cols, dim = img.shape
        # transformation matrix for translation
        M = np.float32([[1, 0, 50],
                        [0, 1, 50],
                        [0, 0, 1]])
        # apply a perspective transformation to the image
        translated_img = cv2.warpPerspective(img, M, (cols, rows))
        # disable x & y axis
        plt.axis('off')
        # show the resulting image
        plt.imshow(translated_img)
        plt.show()
        # save the resulting image to disk
        plt.imsave("E:/Program Files/Python/Road1.jpg", translated_img)   
    def onEncryp(self, event):
        img3 = cv2.imread("E:/Program Files/Python/Road1.jpg",0) #Read the picture,
 
        img1 = np.float32(img3)/255.0 #Convert uint8 to float type
 
        img_dct = cv2.dct(img1) #Perform discrete cosine transform
 
        img_dct_log = np.log(abs(img_dct)) #do log processing
 
        img_recor = cv2.idct(img_dct) #Perform inverse discrete cosine transform
 
        
        recor_temp = img_dct[0:100,0:100]
        recor_temp2 = np.zeros(img3.shape)
        recor_temp2[0:100,0:100] = recor_temp
        plt.subplot(221)
        plt.imshow(img_dct_log)
        plt.title('Encrypted Image')
        plt.imsave("E:/Program Files/Python/EncryptRoad1.jpg", img_dct_log)
        plt.show()
        #print( "Hello")
    def onDcryp(self, event):
        print("hello")
        
if __name__ == '__main__':
    app = PhotoCtrl()
    app.MainLoop()
