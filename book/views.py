from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
#from django.contrib.auth import logout #accounstアプリにログイン管理を移すのでカット
from django.urls import reverse, reverse_lazy
from django.views.generic import(
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView, #モデル操作インポート
)

from .models import Book, Review #app内のmodels.pyの中のBookクラス（Bookモデル（データベーステーブル））をインポート
from django.db.models import Avg #データの平均値を得るメソッドをインポート

from django.core.paginator import Paginator
from .consts import ITEM_PER_PAGE

class ListBookView(LoginRequiredMixin, ListView): #ListViewクラスを継承してListBookViewを作る（データ一覧を表示するのに適したクラスを継承）
    #LoginRequiredMixinを継承すると、ログインしてない場合に先にログインを求めてくる
    #その際のディフォルトページはaccount/loginとなっている
    #つまりaccountsアプリのurls.pyで定義した場所と現状同じなのでこのままでOK
    #もしこれを変えたい場合はsetting.pyにてLOGIN_URL=''で定義する
    
    template_name = 'book/book_list.html' #app内のtemplatesフォルダ内のbookフォルダ>book_list.htmlを表示に使う様に定義
    #つまり、使うhtmlファイルをbook_list.htmlと指定している
    #template_name = 'book/book_old.html'
    model = Book #モデルはapp内のmodels.py内のBookクラス（モデル、データベース）を使う様に定義
    paginate_by = ITEM_PER_PAGE #クラスの場合はpaginate_byに区切る数を渡すだけでページネーションが完了する。


class DetailBookView(LoginRequiredMixin, DetailView): #DetailViewクラスを継承してDetailBookViewを作る（データ詳細を表示するのに適したクラスを継承）
    template_name = 'book/book_detail.html' #app内のtemplatesフォルダ内のbookフォルダ>book_detail.htmlを表示に使う様に定義
    model = Book #モデルはapp内のmodels.py内のBookクラス（モデル、データベース）を使う様に定義。urls.pyで宣言したid番号pkのデータが入る

    #ページネーションチャレンジ
    #context_object_name = 'book'

    def get_context_data(self, **kwargs):
        #クラス内の関数なのでselfが付く
        # 親クラスのコンテキスト（bookオブジェクトなど）を取得
        context = super().get_context_data(**kwargs)
        
        # 1. この本に紐づく全レビューを取得（星評価順）
        review_list = self.object.review_set.all().order_by('-rate') #このid番号のBookモデルに紐づいているreviewモデルの全データ取得
        #ここのモデルで定義されているBook側（親側）からForeignkeyで結びついているReviewモデル側（子側）のデータを全部とりにいくのが、
        #.review_set.all()となる
        #逆のパターンはclass CreateReviewViewのBook.objects.get(pk=self.kwargs['book_id'])でやってる
        #（こっちはReviewモデルがメインで子から親に遡っている）
        
        # 2. ページネーション設定（例: 1ページがITEM_PER_PAGE件）
        paginator = Paginator(review_list, ITEM_PER_PAGE) #DjangoのPaginatorクラスからインスタンスpaginatorを生成
                                                            #review_listをITEM_PER_PAGEの数（今回は2）で分割してグループ化する
        page_number = self.request.GET.get('page', 1) #GETに更にgetを付けると'page'というクエリパラメータが付いていればそれを返し
                                                        #付いてなければ1を返す。つまり最初のindexページならpage=は無いので1が入る
        page_obj = paginator.get_page(page_number) #paginatorインスタンスのpageメソッドを使う。引数で直前のpage_numberを渡す
                                                    #これで分割されたpaginator内グループの中のpage_number番号の要素がpage_objに渡される
        
        # 3. コンテキストに追加
        context['reviews'] = page_obj  # 'reviews'に分割された中の要求されたpage_objを入れる。テンプレートではこれを使ってループ
        context['page_obj'] = page_obj # ページナビゲーション用
        return context
    
    #ページネーションチャレンジここまで

class CreateBookView(LoginRequiredMixin, CreateView): #CreateViewクラスを継承してCreateBookViewを作る
    template_name = 'book/book_create.html' #app内のtemplatesフォルダ内のbookフォルダ>book_create.htmlを表示に使う様に定義
    model = Book #モデル（データベース）はapp内のmodels.py内のBookクラス（モデル、データベース）に保存する様に定義
    fields = ('title', 'text', 'category', 'thumbnail') #フォームの中でmodelのどの項目を表示するかを指定（今回は全部）
    success_url = reverse_lazy('list-book') #フォームの「作成する」ボタンが押されると'list-book'へ飛ぶ

    def form_valid(self, form): #CreateViewに備わってるメソッドの上書き
                                #form_valid関数はフォームが送信された際に間違いが無かった時にデータ保存前に呼び出されるメソッド
        form.instance.user = self.request.user #form.instance.userでformクラスのインスタンスにuserという属性でデータを追加している
                                                #self.request.userでユーザーがログインしている場合にrequestオブジェクトに
                                                #入っているuserの情報（つまりログインユーザーの情報）を意味している。
                                                #よって、このユーザー情報がこれがformインスタンスのuser属性に追加される
        return super().form_valid(form)

class DeleteBookView(LoginRequiredMixin, DeleteView): #DeleteViewクラスを継承してDeleteBookViewを作る
    template_name = 'book/book_confirm_delete.html' #app内のtemplates内のbook>book_confirm_delete.htmlを表示に使う様に定義
    model = Book #モデル（データベース）はapp内のmodels.py内のBookクラス（モデル、データベース）に保存する様に定義
    success_url = reverse_lazy('list-book') #フォームの「作成する」ボタンが押されると'list-book'へ飛ぶ

    def get_object(self, queryset = None):
        obj = super().get_object(queryset) #contextが辞書型の大規模データに対してobjectは単一データ。
        #objには編集をリクエストされたid番号のBookモデルの全データが入る。obj.項目名で中身が観れる（下記参照）
        #これでobj.userでrequestされたBook内の書籍データのUser項目を調べられる
        # print(obj)
        # print(obj.user)
        # print(obj.title)
        # print(obj.text)
        # print(obj.category)
        # print(obj.thumbnail)
        # print(self.request.user)

        if obj.user != self.request.user: #指定した書籍データのユーザーデータが、このページをリクエストしたユーザーと違っていたら
            raise PermissionDenied #raiseで例外処理を強制的に実行する
                                    #（この場合Djangoにあらかじめ用意されているPermissionDeniedが実行される
                                    #画面上には「403 Forbidden」が表示される
        return obj

class UpdateBookView(LoginRequiredMixin, UpdateView): #UpdateViewクラスを継承してUpdateBookViewを作る
    template_name = 'book/book_update.html' #app内のtemplates内のbook>book_update.htmlを表示に使う様に定義
    model = Book #モデル（データベース）はapp内のmodels.py内のBookクラス（モデル、データベース）に保存する様に定義
    fields = ('title', 'text', 'category', 'thumbnail') #フォームの中でmodelのどの項目を表示するかを指定（今回は全部）
    #success_url = reverse_lazy('list-book') #フォームの「作成する」ボタンが押されると'list-book'へ飛ぶ

    def get_object(self, queryset = None):
        obj = super().get_object(queryset) #contextが辞書型の大規模データに対してobjectは単一データ。
        #objには編集をリクエストされたid番号のBookモデルの全データが入る。obj.項目名で中身が観れる（下記参照）
        #これでobj.userでrequestされたBook内の書籍データのUser項目を調べられる
        print(obj)
        print(obj.user)
        print(obj.title)
        print(obj.text)
        print(obj.category)
        print(obj.thumbnail)
        print(self.request.user)

        if obj.user != self.request.user: #指定した書籍データのユーザーデータが、このページをリクエストしたユーザーと違っていたら
            raise PermissionDenied #raiseで例外処理を強制的に実行する
                                    #（この場合Djangoにあらかじめ用意されているPermissionDeniedが実行される
                                    #画面上には「403 Forbidden」が表示される
        return obj
    
    def get_success_url(self): #これまではsuccess-urlをreverse_lazy('-')で書いていたが、
        #今回はget_success_urlメソッドへのオーバーライドで書いてみる

        return reverse('detail-book', kwargs={'pk': self.object.id}) #第一引数に遷移するurlを書く
        #第二引数はキーワード引数に書籍のid番号を渡している（detail-bookにはidが必要なため）
        #return reverse('index') #例えばindexに戻すなら第二引数はいらない 

def index_view(request): #トップページをfunction(関数)viewで作る
    #print('index_view is successed!') #アクセスがあるとこの文字列がターミナルに表示される
    #object_list = Book.objects.all() #Book.objectsでBookモデル内のすべてのobjectsを示している。その後ろのメソッドで色々行える
    #この場合Bookモデルのすべてのobjectがobject_listに入る

    #object_list = Book.objects.order_by('category') #Book.objectsでBookモデル内のすべてのobjectsを示している。その後ろのメソッドで色々行える
    #この場合Bookモデルのすべてのobjectがcategory別に順にobject_listに入る

    object_list = Book.objects.order_by('-id') #Book.objectsでBookモデル内のすべてのobjectを取得し、object_listに代入。id降順
    ranking_list = Book.objects.annotate(avg_rating=Avg('review__rate')).order_by('-avg_rating')
    #Bookモデルのすべてのobjectに対し、annotate()で()内のデータを追加している
    #Avg('review__rate')で、__の左のモデルから右のフィールドを選択し、その平均値を出し、この場合その結果をavg_ratingに代入している
    #このデータをannotate()でBookのすべての各オブジェクトに追加している。
    #またorder_by('-avg_rating')で、それらをavg_ratingの降順に並べ、ranking_listに代入している。
    #print(ranking_list[1].avg_rating)
    #print(ranking_list[0])
    #print(ranking_list[1])
    #ranking_listの中身を観ている、[]内はid番号

    #t2 = Book.objects.get(pk=11).title
    #print(t2)

    paginator = Paginator(ranking_list, ITEM_PER_PAGE) #DjangoのPaginatorクラスからインスタンスpaginatorを生成
                                                        #ranking_listをITEM_PER_PAGEの数（今回は2）で分割してグループ化する
    page_number = request.GET.get('page',1) #GETに更にgetを付けると'page'というクエリパラメータが付いていればそれを返し、
                                            #付いてなければ1を返す。つまり最初のindexページならpage=は無いので1が入る
    page_obj = paginator.page(page_number) #paginatorインスタンスのpageメソッドを使う。引数で直前のpage_numberを渡す
                                            #これで分割されたグループのpage_number番号の要素がpage_objに渡される

    #print(page_number)
    #print(page_obj[1].text)

    # for a in object_list:
    #     print(a.title)
    #     print(a.category)

    #query = request.GET['number'] #これでリクエストURLの/?number=〇〇〇 の、〇〇〇の文字列を取得してqueryに代入出来る
    #print(query)


    return render(
        request,
        'book/index.html',
        {'object_list': object_list, 'ranking_list': ranking_list, 'page_obj': page_obj}
    )
    #{}の左の'object_list'という名前で右側のobject_list（直前の行で定義した変数）を呼び出している。
    #同様に{}の左の'lanking_list'という名前で右側のlanking_list（直前の行で定義した変数）を呼び出している。

    #return render(request, 'book/index.html',{'somedata': 100}) #render関数を使ってresponseオブジェクトを作っている
    #引数1…request(これは必ずrequestと書く決まり)
    #引数2…htmlファイルの指定（class-based viewのtemplate_name=''と同じイメージ）
    #引数3…index_view関数において使うデータ（class-based viewのmodel=Bookと同じイメージ）
    #今回は分かりやすい様にpythonの辞書型データ{}(key:somedata valueが100)をサンプルとして使っている。
    #引数3をDjangoでは一般的にcontextと呼ぶ

class CreateReviewView(LoginRequiredMixin, CreateView): #CreateViewを継承してCreateReviewViewクラスを作る
    model = Review #Reviewモデルを使用
    fields = ('book', 'title', 'text', 'rate') #ブラウザで表示させる項目を定義
    template_name = 'book/review_form.html' #HTMLテンプレートを指定

    def get_context_data(self, **kwargs): #createViewクラス内のget_context_data関数へのオーバーライド
        context = super().get_context_data(**kwargs) #contextは辞書型データ。ここにデータを追加している
                                                    #**kwargsはキーワード引数で、この場合urlの<ink:book_id>がviewsnに渡されている
                                                    #super()で親クラスのget_context_dataを呼び出し従来のcontextデータをゲット
                                                    #get_context_dataはcontextを戻り値として返す
        
        context['book'] = Book.objects.get(pk=self.kwargs['book_id'])
        #辞書型データcontextに選んだ書籍のBookモデルのデータの追加を行うコード。
        #Book.objects.getはBookモデルのすべてのデータからgetで指定したデータを取得する
        #kwargs['book_id']はurlの<int:book_id>に対応している
        #これで辞書リストcontextに'book'が辞書型で追加され、そこには<int:book_id>のBookモデルのデータが入る
        #これでcontextには(例えばid=1なら)'book:<Book:ビジネス本>'と、キーワードbookにBookモデルのその本のデータが丸ごと入る
        #よってHTML上では{{book.title}}で本のタイトルが得られる。同様に{{book.text}}でtextデータ（説明文）を得られる

        print(context['book'])
        print(context)
        print(context['book'].title) #book内のtitleだけを表示
        print(context['book'].text) #book内のtextだけを表示
        print(context['book'].user) #book内のuserだけを表示
        print(context['book'].category) #book内のcategoryだけを表示
        print(context['book'].id) #book内のcategoryだけを表示
        return context
    
    def form_valid(self, form): #CreateViewに備わってるメソッドの上書き
                                #form_valid関数はフォームが送信された際に間違いが無かった時にデータ保存前に呼び出されるメソッド
        form.instance.user = self.request.user #form.instance.userでformクラスのインスタンスにuserという属性でデータを追加している
                                                #self.request.userでユーザーがログインしている場合にrequestオブジェクトに
                                                #入っているuserの情報（つまりログインユーザーの情報）を意味している。
                                                #よって、このユーザー情報がこれがformインスタンスのuser属性に追加される
        return super().form_valid(form)
    
    def get_success_url(self): #これまではsuccess-urlをreverse_lazy('-')で書いていたが、
        #今回はget_success_urlメソッドへのオーバーライドで書いてみる

        return reverse('detail-book', kwargs={'pk': self.object.book.id}) #第一引数に遷移するurlを書く
        #第二引数はキーワード引数に書籍のid番号を渡している（detail-bookにはidが必要なため）
        #return reverse('index') #例えばindexに戻すなら第二引数はいらない

# def logout_view(request): #Djangoの公式ドキュメントに記載されたログアウト手順をそのまま行っている。requestを引数として受け取っている
#     logout(request)
    
#     return redirect('index') #ログアウトに成功した際にどのページにリダイレクトするかを定義する必要がある（この場合indexにリダイレクトする）
    
    #以下の様にrenderでログアウト先を定義する事も出来る
    #object_list=Book.objects.order_by('title')
    #return render(request, 'book/index.html', {'object_list': object_list})