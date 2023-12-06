from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import OneLineListItem
from encryption import encrypt, decrypt,create_id
from database import read_Database
from kivymd.uix.button import MDIconButton

#Next steps create JSON holding List IDs
class CustomDialogContent(MDGridLayout):
    pass

class Content(BoxLayout):
    manager = ObjectProperty()
    nav_drw = ObjectProperty()

    pass

class Demo(ScreenManager):
    #screen_manager = ObjectProperty()
    #def on_kv_post(self, *args):
        #for child in self.ids.screen_manager.children:
            #for sub_child in child.walk():
                #print(sub_child)
    pass

class PostItem(BoxLayout):
    list_view = ObjectProperty()
    pass


class Main(MDApp):

    def build(self):
        return Demo()

    def show_dialog(self):
        close_button = MDFlatButton(text='Close', pos_hint={'x': 0, 'y': -.3}, on_release=self.close_dialog)
        ok_button = MDFlatButton(text='OK', pos_hint={'x': 0, 'y': -.3}, on_release=self.ok_dialog)
        self.dialog = MDDialog(
            title="Dialog Title",
            size_hint=(0.8, 0.3),
            type="custom",
            content_cls=CustomDialogContent(),
            buttons=[ok_button, close_button],
            auto_dismiss= False

                          )
        self.dialog.open()

    def edit_dialog(self, *args):
        close_button = MDFlatButton(text='Close', pos_hint={'x': 0, 'y': -.3}, on_release=self.close_dialog)
        remove_button = MDFlatButton(text='Edit', pos_hint={'x': 0, 'y': -.3})
        self.dialog = MDDialog(
            title="Edit Tool",
            size_hint=(0.8, 0.3),
            buttons=[remove_button, close_button],
            auto_dismiss= False
                          )
        self.dialog.open()


    def post_text(self, text1, text2, *args):
        create_id(text1)
        print(create_id(text1))
        #pos=(listItem1.width/0.14, listItem1.height)
        listItem1 = OneLineListItem(text=text1, size_hint=(0.425, None),)
        icon_button = MDIconButton(
            icon='pencil-plus-outline',
            pos_hint={'right': 0.975, 'top': 0.9},
            on_release=self.edit_dialog
        )

        if text1:
            listItem1.add_widget(icon_button)
            self.root.ids.list_view.add_widget(listItem1)

            #self.root.ids.list_view.add_widget(OneLineListItem(text=text1,
            #                                                   size_hint=(0.425, None),
            #                                                   right_widget = icon_button
            #                                                   ))
            self.root.ids.list_view.add_widget(OneLineListItem(text=text2,
                                                               size_hint=(0.425, None)
                                                               ))




    def ok_dialog(self, *args):

        text_field_1 = self.dialog.content_cls.ids.text_field_1
        text_field_2 = self.dialog.content_cls.ids.text_field_2
        self.post_text(text_field_1.text, text_field_2.text)
        encrypt(text_field_2.text, "passwort")
        read_Database()
        self.close_dialog()

    def close_dialog(self, *args):
        self.dialog.dismiss()





Main().run()