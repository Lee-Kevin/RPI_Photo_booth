from TakePhoto import photo

if __name__ == "__main__" :
    btn = photo.Button(photo.mybutton)
    btn.attach(photo.takephoto)

    app = photo.TakePhoto()
    app.runloop()   
