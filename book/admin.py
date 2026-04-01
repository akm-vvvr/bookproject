from django.contrib import admin
#from .models import SampleModel
#admin.site.register(SampleModel) #アプリで作成したデータベーステーブルを管理画面に反映させる

from .models import Book, Review #book/views.pyで定義したモデルBookをインポート

admin.site.register(Book) #アプリで作成したデータベーステーブルを管理画面に反映させる
admin.site.register(Review) #アプリで作成したデータベーステーブルを管理画面に反映させる