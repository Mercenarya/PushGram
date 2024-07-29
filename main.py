import flet as ft
import sqlite3
from flet import View
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
        
        self.Translator = ft.Dropdown(
            options=[
            ],
            width=150,
            text_size=12,
            border_color="white",
            text_style=ft.TextStyle(color="white"),
            color=ft.TextStyle(color="black"),
            bgcolor="grey"
        )
        languages = ''' SELECT * FROM langs'''
        cursor.execute(languages)
        for obj in cursor.fetchall():
            self.Translator.options.append(
                ft.dropdown.Option(f"{obj[1]}")
            )
        
        
        self.Progress = ft.Column(
            [
                ft.Text("Translating...",size=10,color="white"),
                ft.ProgressBar(width=200,color="white"),
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
        
        self.trans_text = ft.Text(color="white",size=15)

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

        self.Trans_Textline = ft.Container(
            ft.Column(
                [
                    self.trans_text
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
            bgcolor="black",
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
            bgcolor="black",
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
                    self.Trans_Textline,
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
                                        ft.ElevatedButton('Back',color="white",bgcolor="grey",on_click=self.Back_event_keyword),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),
                                margin=ft.margin.only(top=5)
                            )

                        ],
                        width=520,
                        scroll=ft.ScrollMode.HIDDEN
                        
                    )
                    
                ],
                scroll=ft.ScrollMode.HIDDEN
                
               
            ),
            
            width=450,
            bgcolor="black",
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
        self.trans_text.value = self.Edit_text.value
        self.Display_Note.visible = True
        self.Edit_Note_text.visible = False
        self.update()

    def keyword_Note(self,e):
        self.Display_Note.visible = False
        self.trans_text.value = self.Edit_text.value
        self.Keyword_Search.visible = True
        self.update()


    def Keyword_trans(self, e):
        try:
            self.loading(e)
            self.Progress.visible=False
            translation = GoogleTranslator(target=f"{self.Translator.value}")
            reavel = translation.translate(self.Edit_text.value)
            self.translated_text = ft.TextField(value=reavel,color="white",read_only=True,border_color="black",multiline=True) 
            self.Keyword_Search.height=600
            self.Translated.visible = True
            self.Translated.controls.clear()
            self.Translated.controls.append(
                ft.Column(
                    [
                        ft.Text(value=self.Translator.value,color="white",size=20,weight="bold"),
                        self.translated_text
                    ]
                )
            )
        except:
            self.translated_text.value = f"{self.Translator.value} cannot be a language,\nPlease check your corrected target language"
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
        

        self.Note_title = ft.TextField(width=400,border_color="white",hint_text="Tittle...",
                                       color="white",hint_style=ft.TextStyle(color="white"))
        self.Note_textField = ft.TextField(value="\n\n",width=400,border_color="white",hint_text="TextLine...",
                                           multiline=True,hint_style=ft.TextStyle(color="white"),
                                           min_lines=1,max_lines=4,color="white")
        self.banner = ft.Row(
            [
                ft.Text("copyright by russianb_0 - Cuu Vang Long Do Ⓒ",size=10,color="grey")
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        self.Note_list = ft.Column(
            [
                self.banner
            ],
            height=700,
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
            bgcolor="black",
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
    def Selected_page(e):
        for index, page_nav in enumerate(page_stack):
            page_nav.visible = True if index == NavBar.selected_index else False
        page.update()

    NavBar = ft.CupertinoNavigationBar(
        selected_index=0,
        on_change=Selected_page,
        bgcolor=ft.colors.BLACK,
        inactive_color=ft.colors.WHITE54,
        active_color=ft.colors.WHITE,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.HOME, label="Home"),
            ft.NavigationDestination(icon=ft.icons.SETTINGS, label="Settings"),
        ],
    )
    


    
    #SETTINGS CUSTOMIZE AND ELEMENTS
    #Annoucement
    def Open_langs_annoucement(e):
        new_lans_anounce.open = True
        page.update()
    def Open_deleted_lans_announcement(e):
        deleted_langs_anounce.open = True
        page.update()
    def Open_deleted_text_announcement(e):
        deleted_text_anounce.open = True
        page.update()
    #Interacting functions 
    def Open_language_setting_layout(e):
        open_language_button.visible = False
        close_language_button.visible = True
        Language_field.visible = True
        Submit_Result.visible = True
        Language_layout.height = 200
        page.update()
    
    def close_language_setting_layout(e):
        open_language_button.visible = True
        close_language_button.visible = False
        Language_field.visible = False
        Submit_Result.visible = False
        Language_layout.height = 80
        page.update()
    def Upload_language(e):
        try:
            new_lans = [Language_field.value]
            cursor.execute('INSERT INTO langs (lans) VALUES (?)',new_lans)
            print("new language upload")
            Open_langs_annoucement(e)
            NotedApp().update()
            db.commit()
        except sqlite3.Error as error:
            print(error)
        page.update()

    def Deleted_language(e):
        try:
            cursor.execute('DELETE FROM langs')
            page.go("/Home")
            db.commit()
            Open_deleted_lans_announcement(e)
        except sqlite3.Error as error:
            print(error)
        page.update()

    def Deleted_Text(e):
        try:
            cursor.execute('DELETE FROM note')
            page.go("/Home")
            db.commit()
            Open_deleted_text_announcement(e)
        except sqlite3.Error as error:
            print(error)
        page.update()

    def Theme_selection(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        Theme_switch.label =(
            "Light" if page.theme_mode == ft.ThemeMode.LIGHT else "Dark"
        )
        
        page.update()

    def Open_theme_setting_layout(e):
        open_theme_button.visible = False
        close_theme_button.visible = True
        Theme_switch.visible = True
        Theme_layout.height = 150
        page.update()
    
    def close_theme_setting_layout(e):
        open_theme_button.visible = True
        close_theme_button.visible = False
        Theme_switch.visible = False
        Theme_layout.height = 80
        page.update()


    def Open_storage_setting_layout(e):
        open_storage_button.visible = False
        close_storage_button.visible = True
        Storage_layout.height = 180
        page.update()
    
    def close_storage_setting_layout(e):
        open_storage_button.visible = True
        close_storage_button.visible = False
        Storage_layout.height = 80
        page.update()

    #Update Theme Elements - controls - Switch
    Theme_switch = ft.Switch(label="Dark", on_change=Theme_selection,visible=False,
                             active_color="white",label_style=ft.TextStyle(color="white"))


    #Update Language Elements - controls - selection - input
    Language_field = ft.TextField(hint_text="New Language",hint_style=ft.TextStyle(color="white"),
                                  color="white",
                                  border_color="white",visible=False)
    Submit_Result = ft.ElevatedButton("Update",color="white",bgcolor="grey",
                                      width=100,visible=False,on_click=Upload_language)
    #Update Storage - button - controls
    Delete_language = ft.IconButton(ft.icons.DELETE,icon_color="red",on_click=Deleted_language)
    Delete_Context = ft.IconButton(ft.icons.DELETE,icon_color="red",on_click=Deleted_Text)



    #User's interact with button - select options - controls
    #button - language's Selection
    open_language_button = ft. IconButton(ft.icons.ARROW_RIGHT,visible=True,
                                          icon_color="white",icon_size=30,
                                          on_click=Open_language_setting_layout)
    
    close_language_button = ft. IconButton(ft.icons.ARROW_LEFT,visible=False,
                                           icon_color="white",icon_size=30,
                                           on_click=close_language_setting_layout)
    

    #button - theme's Selection
    open_theme_button = ft. IconButton(ft.icons.ARROW_RIGHT,visible=True,
                                          icon_color="white",icon_size=30,
                                          on_click=Open_theme_setting_layout)
    close_theme_button = ft. IconButton(ft.icons.ARROW_LEFT,visible=False,
                                           icon_color="white",icon_size=30,
                                           on_click=close_theme_setting_layout)
    


    #button - Storage's Selection
    open_storage_button = ft. IconButton(ft.icons.ARROW_RIGHT,visible=True,
                                          icon_color="white",icon_size=30,
                                          on_click=Open_storage_setting_layout)
    close_storage_button = ft. IconButton(ft.icons.ARROW_LEFT,visible=False,
                                           icon_color="white",icon_size=30,
                                           on_click=close_storage_setting_layout)

    
    new_lans_anounce = ft.SnackBar(
        content=ft.Text(f"{Language_field.value} uploaded")
    )

    deleted_langs_anounce = ft.SnackBar(
        content=ft.Text(f"all languages deleted, restart your application")
    )
    deleted_text_anounce = ft.SnackBar(
        content=ft.Text(f"all text deleted, restart your application")
    )
    
    
    #container - language's Selection
    Language_layout = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Language's update", weight="bold",color="white"),
                        open_language_button,
                        close_language_button,
                        
                        
                    ],
                    alignment="spacebetween"
                ),
                Language_field,
                Submit_Result
            ]
        ),
        height=80,
        width=450,
        bgcolor="black",
        border_radius=20,
        padding=15,
        animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT), 
    )
    #container - Theme's Selection
    Theme_layout = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Theme mode", weight="bold", color="white"),
                        open_theme_button,
                        close_theme_button,
                        
                        
                    ],
                    alignment="spacebetween"
                ),
                Theme_switch
            ]
        ),
        height=80,
        width=450,
        bgcolor="black",
        border_radius=20,
        padding=15,
        animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT), 
    )

    Storage_layout = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Storage", weight="bold", color="white"),
                        open_storage_button,
                        close_storage_button,
                        
                        
                    ],
                    alignment="spacebetween"
                ),
                ft.Row(
                    [
                        ft.Text("Delete all languages",color="white"),
                        Delete_language
                    ],
                    alignment="spacebetween"
                ),
                ft.Row(
                    [
                        ft.Text("Delete all text",color="white"),
                        Delete_Context
                    ],
                    alignment="spacebetween"
                )
                
            ]
        ),
        height=80,
        width=450,
        bgcolor="black",
        border_radius=20,
        padding=15,
        animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT), 
    )


    




    

    
    page_1 = ft.Container(
        ft.Column(
            [
                NotedApp()
            ]
        ),
        visible=True
    )
    page_2 = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Settings ",size=20),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                
                Language_layout,
                Theme_layout,
                Storage_layout
                
            ]
        ),
        visible=False
    )


    page_stack = [
        page_1,
        page_2
    ]

   
    



    def route_change(e):
        page.views.clear
        page.views.append(
            View(
                "/Home",
                [
                    NavBar,
                    ft.Column(page_stack,scroll=True, expand=True)
                ]
            )
        )
        '''
            USE THIS TO UPDATE AND CREATE 
            YOUR OWN ROUTE WHEN YOU HAVE TO
            OPEN A NEW FUNCTION (OR NON-FUNCTION) FOR YOUR APP

            TRY IF PAGE.ROUTE AND THEN 
        '''
        page.update()
    def view_pop(View):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route, skip_route_change_event=True)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    page.add(new_lans_anounce,deleted_langs_anounce,deleted_text_anounce)
    page.window_width = 380
    page.window_resizable = False
    page.on_resize = False
    page.update()


    page.window_width = 380
    page.window_height = 800
    page.on_resize = False
    page.window_resizable = False
    page.window_resizable = False
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
