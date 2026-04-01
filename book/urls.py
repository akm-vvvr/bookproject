from django.urls import path
from . import views #views.pyを丸ごとインポート
#hello worldアプリではfrom .views import helloworldfuncと書いていたけど、from . importとする事で
#views.py内で定義したクラスや関数を個別にimportする必要が無くなる。

urlpatterns = [
    path('', views.index_view, name='index'), #function-viewでトップページを実装

    path('book/', views.ListBookView.as_view(), name='list-book'), #まずは
    #views.pyファイルで定義するListBookViewというクラスを呼び出すために必要なコード(class-based view)
    #book/リクエストが来たらviews.pyのListBookViewクラスを開く

    path('book/<int:pk>/detail/', views.DetailBookView.as_view(), name='detail-book'),
    #同様にbook/インデックスナンバー/detailリクエストが来たら、views.pyのDetailBookViewクラスを開く

    path('book/create/',views.CreateBookView.as_view(), name='create-book'),
    #同様にbook/createリクエストが来たら、views.pyのCreateBookViewクラスを開く

    path('book/<int:pk>/delete/', views.DeleteBookView.as_view(), name='delete-book'),
    #同様にbook/インデックスナンバー/detailリクエストが来たら、views.pyのDetailBookViewクラスを開く

    path('book/<int:pk>/update/', views.UpdateBookView.as_view(), name='update-book'),
    #同様にbook/インデックスナンバー/updateリクエストが来たら、views.pyのUpdateBookViewクラスを開く

    path('book/<int:book_id>/review/', views.CreateReviewView.as_view(), name='review'),
    #同様にbook/book_idナンバー/reviewリクエストが来たら、views.pyのCreateReviewViewクラスを開く

    #path('logout/', views.logout_view, name='logout'), #function-viewで書いている。views.pyのlogout_view関数が実行される（今回はトップページを実装）
    #accountsアプリにログインログアウト管理を移行するのでカット
]
#この[]内に、空でもいいので最低限のコードを書いておかないとエラーになるので注意