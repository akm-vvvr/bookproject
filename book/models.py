from django.db import models
from .consts import MAX_RATE #consts.pyからMAX_RATE変数を呼び出している。レビュー数のMAXを定義している変数（定数）

CATEGORY = (('business', 'ビジネス'), ('life', '生活'), ('other', 'その他')) #プルダウン用の文字列
#,の右がhtmlファイル上で表示される項目、左がhtmlファイルのコード上で表示される項目になる

RATE_CHOICES = [(x,str(x)) for x in range(0, MAX_RATE+1)]
#後で代入する、Reviewモデルのcategory変数の中身を作っている。上のBookモデルのCATEGORYと同じ
# for i in range(4):
#     print(RATE_CHOICES[i])
#リスト型データとしてRATE_CHOICE（レビューの数を決める変数）を定義している。
#例えばMAX_RATEが3ならRATE_CHOICES=[(0,'0'),(1,'1'),(2,'2'),(3,'3'),(4,'4')] RATE_CHOICES[0]=(0,'0')となる

# class SampleModel(models.Model): #モデル（データベーステーブル）の名前 SampleModelをクラスとして定義する
#     title = models.CharField(max_length=100) #CharFieldでtitleは文字列型データと定義される。
#     #max_length=100で文字長を最大100と定義(必ず定義が必要)

#     number = models.IntegerField() #IntegerFieldでnumberは整数型のデータと定義

class Book(models.Model): #モデル（データベーステーブル）の名前をBookと定義。modelsモジュールのModelクラスを継承
    title = models.CharField(max_length=100) #本のタイトル収納にCharFieldを定義
    text = models.TextField() #本の内容収納に、より長い文字列を収納出来るTextFieldを定義
    thumbnail = models.ImageField(null=True, blank=True) #nullはデータベースに何も入ってない事を許容するかどうか（今回は許容）
                                                        #blankはフォームに入力されたデータが空でも許容するかどうか（今回は許容）
    category = models.CharField(
        max_length=100,
        choices = CATEGORY
    )
    #引数を定義すればCharFieldを違うフィールドとして使える
    #choicesで、入力されるフィールドをプルダウンの文字列に出来る

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    #BookモデルがauthアプリのUserモデルを参照するためにForeignKeyを使う。
    #これで書籍を登録したユーザーが誰だったかもデータとして登録される。
    #引数2のon_deleteは参照先のデータが消された場合どうするかを書く（必ず指定が必要）。
    #今回はmodels.CASCADEで、authアプリのUserの参照先データが消されたらBookのデータも消す。

    def __str__(self): #管理画面で本のタイトルがBook objectからタイトル名に変更するための関数
        #__str__はオブジェクトの文字列表現を返すメソッド
        #Bookクラスから作成された個別のオブジェクトにself.title（それぞれのデータのタイトル）という文字列表現を与えている
        #つまりオブジェクトをタイトルで表現している。
        #なのでself.titleとすればタイトルを返し、仮にself.textとすればtextの中身が返る

        #return self.text
        return self.title

    # class Meta:
    #     verbose_name = '本のデータ' #管理画面での名前を変更している。verbose_nameはmodelの実装とは直接関係ないため、class Meta内で定義している

class Review(models.Model): #レビューデータベーステーブルの名前をReviewと定義。modelsモジュールのModelクラスを継承
    book = models.ForeignKey(Book, on_delete=models.CASCADE) #ReviewモデルがBookモデルを参照するためにForeignKeyを使う
                                                            #ForeignKeyは違うモデルのデータを項目として用いるときに使う
                                                            #ForeignKeyの引数1は参照するモデル（今回はBook）
                                                            #引数2のon_deleteは参照先のデータが消された場合どうするかを書く（必ず指定が必要）。
                                                            #今回はmodels.CASCADEで、Bookの参照先データが消されたらReviewのデータも消す。
    title = models.CharField(max_length=100)
    text = models.TextField()
    rate = models.IntegerField(choices=RATE_CHOICES) #chochoicesを引数として渡す（中身は上で定義したRATE_CHOICES）
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE) #ReviewモデルがUserモデルを参照するためにForeignKeyを使う。引数2はbookと同じ

    def __str__(self):
        return self.title