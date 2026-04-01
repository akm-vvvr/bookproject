from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('accounts/', include('django.contrib.auth.urls')), #accountsリクエストでログイン管理認証フォームアプリ「auth」のurls.pyを呼び出す
    path('accounts/', include('accounts.urls')), #accountsリクエストで「auth」のurls.pyを呼び出したのをaccountsアプリのurls.pyに変更
    path('', include('book.urls')), #/admin以外の文字列リクエストが来たらbook（アプリ）ディレクトリのurls.pyを見に行く
    #つまりadmin以外の処理はすべてbookアプリ側のurls.pyからスタートする事になる。
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#settings.MEDIA_URLはsettings.pyで定義したMEDIA_URL。これとリクエストされたURL（この場合は/media/）が合致したら、
#document_rootで定義した画像を呼び出す。この場合はMEDIA_ROOTつまりBASE_DIR / 'media'フォルダを見に行く