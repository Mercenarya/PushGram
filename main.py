import flet as ft
import sqlite3
from deep_translator import GoogleTranslator
import time
#Database Connection

db = sqlite3.connect('telegram-trans.db',check_same_thread=False)
cursor = db.cursor()

#Test connection



class Note(ft.Column):
    def __init__(self,Title,Text,Delete):
        super().__init__()
        self.title = Title
        self.Text = Text
        self.Delete = Delete
        self.Language = ft.TextField(width=100,border_color="white",color="white",text_size=15,height=50,border_radius=20)
        self.Translator = ft.TextField(width=100,border_color="white",color="white",text_size=15,height=50,border_radius=20)
        self.Progress = ft.Column(
            [
                ft.Text("Translating...",size=10,color="white"),
                ft.ProgressBar(width=200),
            ],
            visible=False
        )

        self.Translated = ft.Column(
            width=500,
            scroll=ft.ScrollMode.HIDDEN,
            visible=False
        )


        self.Display_title = ft.Text(value=self.title, color="white", size=20,weight="bold")
        self.Display_text = ft.Text(value=self.Text,color="white",size=15)
        self.Edit_text = ft.TextField(value=self.Display_text.value,border_color="grey",
                                      color="white",text_size=15,multiline=True)

        self.Textline = ft.Container(
            ft.Column(
                [
                    self.Display_text,
                
                ],
                height=400,
                scroll=ft.ScrollMode.HIDDEN,
            ),
            
            height=300,
            width=400,
            bgcolor="Grey",
            padding=20,
            
            
        )
        self.Edit_Textline = ft.Container(
            ft.Column(
                [
                    self.Edit_text
                ],
                width=400,
                height=300,
                scroll=ft.ScrollMode.HIDDEN,
            ),
            
            height=300,
            width=400,
            bgcolor="Grey",
            padding=15,
            border = ft.border.BorderSide(1,"grey"),
            border_radius=15
            
        )





        self.Display_Note = ft.Container(
            ft.Column(
                [
                    self.Display_title,
                    self.Textline,
                    ft.Row(
                        [
                            ft.ElevatedButton("Delete",bgcolor="grey",color="white",on_click=self.Delete_note),
                            ft.ElevatedButton("Edit",bgcolor="Grey",color="white",on_click=self.Edit_Note),
                            ft.ElevatedButton("Translate",bgcolor="grey",color="white",on_click=self.keyword_Note)
                        ]
                    )
                ]
            ),
            
            width=450,
            bgcolor="lightblue",
            padding=20,
            height=450,
            border = ft.border.BorderSide(1,"grey"),
            border_radius=15
            
        )

        self.Edit_Note_text = ft.Container(
            ft.Column(
                [
                    self.Display_title,
                    self.Edit_Textline,
                    ft.Row(
                        [
                            ft.ElevatedButton("Delete",bgcolor="grey",color="white",on_click=self.Delete_note),
                            ft.ElevatedButton("Save",bgcolor="grey",color="white",on_click=self.Save_Note)
                        ]
                    )
                ]
            ),
            
            width=450,
            bgcolor="lightblue",
            padding=20,
            height=450,
            visible=False,
            border = ft.border.BorderSide(1,"grey"),
            border_radius=15
        )
        self.Keyword_Search = ft.Container(
            ft.Column(
                [
                    self.Display_title,
                    self.Edit_Textline,
                    ft.Column(
                        [
                            
                            ft.Row(
                                [   
                                    ft.ElevatedButton("Trans",color="white",bgcolor="grey",on_click=self.Keyword_trans,
                                                      icon=ft.icons.TRANSLATE,icon_color="white"),
                                    ft.Text("To: ",size=15,color="white"),
                                    self.Translator
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.Row(
                                [
                                    self.Progress
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            self.Translated,
                            ft.Container(
                                ft.Row(
                                    [
                                        ft.ElevatedButton('Back',color="white",bgcolor="black",on_click=self.Back_event_keyword),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),
                                margin=ft.margin.only(top=20)
                            )

                        ],
                        width=500,
                        scroll=ft.ScrollMode.HIDDEN
                        
                    )
                    
                ],
                scroll=ft.ScrollMode.HIDDEN
                
               
            ),
            
            width=450,
            bgcolor="lightblue",
            padding=20,
            height=600,
            visible=False,
            border = ft.border.BorderSide(1,"grey"),
            border_radius=15,
        )
        

        self.controls = [self.Display_Note, self.Edit_Note_text, self.Keyword_Search]

    def Delete_note(self, e):
        
        Remove_Note = f''' DELETE FROM note WHERE title = '{self.Display_title.value}' '''
        try:
            cursor.execute(Remove_Note)
            print("Note Removed")
            db.commit()
        except sqlite3.Error as error:
            print(error)
        self.Delete(self)

    def Edit_Note(self, e):
        self.Display_Note.visible = False
        self.Edit_Note_text.visible = True
        self.update()

    def Save_Note(self,e):
        Edit_Query = f'''UPDATE note SET textiled = '{self.Edit_text.value}' WHERE title = '{self.Display_title.value}' '''
        try:
            cursor.execute(Edit_Query)
            print("Note Updated")
            db.commit()
        except sqlite3.Error as error:
            print(error)
        self.Display_text.value = self.Edit_text.value
        self.Display_Note.visible = True
        self.Edit_Note_text.visible = False
        self.update()

    def keyword_Note(self,e):
        self.Display_Note.visible = False
        self.Keyword_Search.visible = True
        self.update()


    def Keyword_trans(self, e):
        self.loading(e)
        
        self.Progress.visible=False
        translation = GoogleTranslator(target=f"{self.Translator.value}")
        reavel = translation.translate(self.Display_text.value)
        self.translated_text = ft.TextField(value=reavel,color="white",read_only=True,border_color="lightblue",multiline=True) 
        self.Keyword_Search.height=600
        self.Translated.visible = True
        self.Translated.controls.append(
            ft.Column(
                [
                    ft.Text(value=self.Translator.value,color="white",size=20,weight="bold"),
                    self.translated_text
                ]
            )
        )
        self.update()

    def loading(self,e):
        self.Progress.visible=True
        self.Keyword_Search.height=600
        time.sleep(3)
        self.update()

    def Back_event_keyword(self, e):
        self.Keyword_Search.visible = False
        self.Display_Note.visible = True
        self.Display_text.color = "white"
        self.update()

    def Back_event_Edit(self, e):
        self.Edit_Note_text.visible = False
        self.Display_Note.visible = True
        self.Display_text.color = "white"
        self.update()
        
        

class NotedApp(ft.Column):
    def __init__(self):
        super().__init__()
        

        self.Note_title = ft.TextField(width=400,border_color="white",hint_text="Tittle...")
        self.Note_textField = ft.TextField(value="\n\n",width=400,border_color="white",hint_text="TextLine...",
                                           multiline=True,min_lines=1,max_lines=4)
        self.banner = ft.Row(
            [
                ft.Text("copyright by russianb_0 - Cuu Vang Long Do Ⓒ",size=10,color="white")
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        self.Note_list = ft.Column(
            [
                self.banner
            ],
            height=900,
            scroll=ft.ScrollMode.HIDDEN
        )

        self.OpenNoteBar = ft.Container(width=100,height=10,bgcolor="grey",on_click=self.Note_TopBar_Open,visible=True)
        self.CloseNoteBar = ft.Container(width=100,height=10,bgcolor="grey",on_click=self.Note_TopBar_close,visible=False)



        cursor.execute("SELECT * FROM note")
        for obj in cursor.fetchall():
            title = obj[0]
            Notedtext = obj[1]
            self.Note_list.controls.append(
                Note(title,Notedtext,self.Delete_note)
            )
        self.NoteBar = ft.Container(
                ft.Column(
                    [
                        
                        ft.Row(
                            [
                                ft.IconButton(ft.icons.TELEGRAM,icon_color="white",on_click= None),
                                ft.Text("PushGram",color="white",size=25,weight="bold"),
                                ft.IconButton(ft.icons.TRANSLATE,icon_color="white")
                                
                            ],
                            alignment="spaceBetween",
                        ),
                        
                        self.Note_title,
                        self.Note_textField,
                        ft.Row(
                            [
                                ft.FloatingActionButton(
                                    icon=ft.icons.ADD, on_click=self.Add_note
                                ),
                                ft.FloatingActionButton(
                                    icon=ft.icons.DELETE, on_click=self.Clear_Field
                                ),
                                
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        
                    ]
                ),
                border_radius=ft.border_radius.vertical(
                bottom=25
            ),
            bgcolor="lightblue",
            width=400,
            height=60,
            padding=10,
            shadow= ft.BoxShadow(
                blur_radius=3,
                color="black",
                blur_style=ft.ShadowBlurStyle.OUTER
            ),
            animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT),  
        )

        self.controls = [
            self.NoteBar,
            ft.Row(
                [
                    self.OpenNoteBar,
                    self.CloseNoteBar
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            self.Note_list,
            
            
        ]

    def Add_note(self, e):
        note = Note(self.Note_title.value,self.Note_textField.value, self.Delete_note)
        
        index_tub = [self.Note_title.value, self.Note_textField.value]
        Query_index = '''INSERT INTO note (title, textiled) VALUES (?,?)'''
        try:
            cursor.execute(Query_index,index_tub)
            print("New Note Added")
            db.commit()
        except sqlite3.Error as error:
            print(error)
        
        self.Note_list.controls.append(note)
        self.Note_textField.value = "\n\n\n"
        self.update()

    def Delete_note(self, note):
        self.Note_list.controls.remove(note)
        self.update()

    def Clear_Field(self, e):
        self.Note_title.value = ""
        self.Note_textField.value = "\n\n\n"
        self.update()

    def Note_TopBar_Open(self, e):
        self.OpenNoteBar.visible = False
        self.CloseNoteBar.visible = True
        self.NoteBar.height = 350 if self.NoteBar.height == 60 else 60
        self.update()

    def Note_TopBar_close(self, e):
        self.OpenNoteBar.visible = True
        self.CloseNoteBar.visible = False
        self.NoteBar.height = 60 if self.NoteBar.height == 350 else 350
        self.update()
def main(page:ft.Page):
    page.add(NotedApp())
    page.window_width = 380
    page.on_resize = False
    page.window_resizable = False
    page.window_resizable = False
    page.update()
if __name__ == "__main__":
    ft.app(target=main)
