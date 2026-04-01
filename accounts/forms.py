from django.contrib.auth.forms import UserCreationForm #UserCreationFormはListView等と同じ仲間で、ユーザー登録機能の詰まったclass
#UserCreationFormはModelForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm): #UserCreationFormを継承したSignupFormクラスを作成。
                                    #views.pyのform_classで定義した(CreateView継承の)SignupViewで使われるFormとなる
    class Meta: #今回はformにmodelを組み合わせるため、forms.pyとは関係ないmodels.pyと連携させるためにclass Metaという特殊なクラスを定義する
        #つまり、一般的なformの使い方とは関係ない情報を扱うのでclass Metaの中で定義をしている
        model = User #どのmodelに保存するかを定義
        fields = ('username',) #ブラウザ上に表示する項目を定義