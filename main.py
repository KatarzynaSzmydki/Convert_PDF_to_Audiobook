'Python script that takes a PDF file and converts it into speech.'


from TTS import say
from tkinter import *
from tkinter import ttk, scrolledtext
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import unicodedata
from time import sleep
import PyPDF2

THEME_COLOR = "#375362"
TYPES=['Text','URL','PDF']


class Text_to_Speech_App:

    def __init__(self):
        self.window = Tk()
        self.window.title("Text to Speech App")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)
        self.window.geometry("500x500")

        self.label = Label(text=f'Provide text for conversion',font=('Aerial 17'), bg=THEME_COLOR, fg='white')
        self.label.grid(row=0, column=0, columnspan=3)

        self.label_type = Label(text=f'Type of text for conversion:', font=('Aerial 12'), bg=THEME_COLOR, fg='white')
        self.label_type.grid(row=1, column=0)
        self.selected_text_type = StringVar()
        self.text_type_cb = ttk.Combobox(textvariable=self.selected_text_type)
        self.text_type_cb['values'] = TYPES
        self.text_type_cb['state'] = 'readonly'
        self.text_type_cb.grid(row=1, column=1)

        self.button_upload_pdf = Button(text='Upload pdf', command=self.upload_pdf, font=('Aerial 12'))
        self.button_upload_pdf.grid(row=1, column=3)
        self.pdf_file = None

        self.text = scrolledtext.ScrolledText(self.window, wrap=WORD,
                                              width=40, height=8,
                                              font=("Times New Roman", 15))

        self.text.grid(column=0, row=3, pady=10, padx=10, columnspan=5)

        # placing cursor in text area
        self.text.focus()

        self.button_start = Button(text='Start', command=self.start_app,font=('Aerial 13'), bg='crimson',fg='white')
        self.button_start.grid(row=12, column=0)

        self.button_clean = Button(text='Clean text editor', command=self.clean_text_editor, font=('Aerial 13'), bg='crimson', fg='white')
        self.button_clean.grid(row=12, column=1)

        self.window.mainloop()


    def upload_pdf(self):

        filename = askopenfilename()
        self.pdf_file = filename


    def start_app(self):
        cleanup = None

        if self.text_type_cb.get() == 'Text':
            cleanup = say(self.text.get("1.0", END))

        elif self.text_type_cb.get() == 'PDF':
            if self.pdf_file is not None:
                pdfFileObj = open(self.pdf_file, 'rb')
                pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                # print(pdfReader.numPages)
                pages = []
                for page in range(0,pdfReader.numPages):
                    pageObj = pdfReader.getPage(page)
                    pages.append(pageObj.extractText().replace('\n',''))
                    # print(pageObj.extractText())
                pdfFileObj.close()
                text = ' '.join(pages)


                if text is not None:
                    self.text.delete('1.0', END)
                    self.text.insert(INSERT, text)
                    self.window.update()
                    sleep(2)
                    cleanup = say(text)
            else:
                messagebox.showerror("showerror", "Upload PDF file.")
                self.upload_pdf()

        elif self.text_type_cb.get() == 'URL':
            url=self.text.get("1.0", END)
            url='https://www.bbc.com/news/business-62144776'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser', )
            title = soup.find(id='main-heading').getText()
            paragraphs = soup.find_all(name='p')
            titles = [unicodedata.normalize("NFKD", paragraph.getText()).replace("\'","'") for paragraph in
                      soup.find_all(name='p')]
            text = ' '.join(titles[:5])

            if text is not None:
                cleanup = say('Opening provided web page. Please wait.')
                sleep(5)
                self.text.delete('1.0', END)
                self.text.insert(INSERT, text)
                self.window.update()
                sleep(2)
                cleanup = say(text)

        else:
            messagebox.showerror("showerror", "Select type of conversion.")

        if cleanup:  # if block = True, function returns None
            sleep(10)
            cleanup()


    def clean_text_editor(self):
        self.text.delete('1.0', END)


if __name__=='__main__':

    app = Text_to_Speech_App()
