from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
#LoginViewには、あらかじめ「HTMLは(bookproject/)registration/login.htmlを使え」と定義されている
#また完了したらsetting.pyに書かれたLOGIN_REDIRECT_URLに飛べと書かれている。
#つまりこの二つを定義しておけば、LoginViewに関してここで特に何も追記する必要が無い！
#同様にLogoutViewもLOGOUT_REDIRECT_URLを定義しておけばここで特に追記する必要が無い。
#これで簡潔にログイン、ログアウトの実装が完了している。

from .views import SignupView

app_name = 'accounts' #URLのname指定の際に「このアプリのネームだよ」とはっきりさせるためにアプリ名を定義している。これでurl 'accounts:login'でこのurlsのpathを呼べる

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'), #成功時にはsetting.pyに書いたLOGIN_REDIRECT_URL=''に飛ぶ
    path('logout/', LogoutView.as_view(), name='logout'), #成功時にはsetting.pyに書いたLOGOUT_REDIRECT_URL=''に飛ぶ
    path('signup/', SignupView.as_view(), name='signup'),
]