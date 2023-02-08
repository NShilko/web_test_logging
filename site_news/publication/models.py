from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from .table_addon import IsPost, ChangeRate
from django.urls import reverse


class Author(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)

    @staticmethod
    def update_rating():
        author_list = Author.objects.all().values('id')
        for author in author_list:
            idx = author['id']
            comment_rate = 0
            author_user_id = Author.objects.get(pk=idx).name_id
            author_posts = Post.objects.filter(isAuthor_id=idx).values('id')
            post_rate = (Post.objects.filter(isAuthor_id=idx).aggregate(sum=Sum('rate') * 3))['sum']
            my_comment_rate = (Comment.objects.filter(isUser_id=author_user_id).aggregate(sum=Sum('rate')))['sum']
            for post in author_posts:
                comment_rate += (Comment.objects.filter(isPost_id=post['id']).aggregate(sum=Sum('rate')))['sum']
            Author.objects.filter(pk=idx).update(rate=(post_rate+my_comment_rate+comment_rate))

    @staticmethod
    def get_best_author():
        best_author = Author.objects.all().order_by('-rate').first()
        username = User.objects.get(pk=best_author.name_id).username
        print('The Best author is: [', username, '] with rating: [', best_author.rate, ']')

    @staticmethod
    def get_user_id(user):
        return Author.objects.get(name_id=User.objects.get(username=user).id).id


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='UserCategory', default='Без категории')

    def __str__(self):
        return self.name


class UserCategory(models.Model):
    isUser = models.ForeignKey(User, on_delete=models.CASCADE)
    isCategory = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
    title = models.TextField()
    main_text = models.TextField()
    isAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)
    kind = models.CharField(max_length=4, choices=IsPost.names)
    date = models.DateTimeField(auto_now_add=True)
    isCategory = models.ManyToManyField(Category, through='PostCategory', default='Без категории')
    rate = models.IntegerField(default=0)

    def like(self):
        self.rate = ChangeRate.make_like(self.rate)
        self.save()

    def dislike(self):
        self.rate = ChangeRate.make_dislike(self.rate)
        self.save()

    @staticmethod
    def preview(idx):
        return Post.objects.get(pk=idx).main_text[0:123] + ' ...'

    @staticmethod
    def show_best_post(show_comment=False):
        best_post = Post.objects.all().order_by('-rate').first()
        author_id = Author.objects.get(pk=best_post.isAuthor_id).name_id
        username = User.objects.get(pk=author_id).username
        if not show_comment:
            print(f'''Best post by [ {username} ] with rating [ {best_post.rate} ] in [ {best_post.date} ] 
            Title: {best_post.title}
            Preview: {Post.preview(best_post.id)}''')
        else:
            comment_list = Comment.objects.filter(isPost_id=best_post.id)
            for idx, comment in enumerate(comment_list):
                print(f'''№{idx}. {comment.main_text}
By [ {username} ] with rate [ {comment.rate} ]
{comment.date}''')

    @staticmethod
    def add_category(id_post, category):
        for name_category in category:
            PostCategory.objects.create(isCategory_id=name_category, isPost_id=id_post)

    @staticmethod
    def generate_text():
        for i in range(1,100):
            title = ''
            main_text = ''
            for j in range(1, 5):
                title += f'Название #{i}'
            for j in range(1, 100):
                main_text += f'Новость #{i}'
            Post.objects.create(title=title, main_text=main_text, isAuthor_id=1, kind='NEWS')
            main_text = main_text.replace('Новость', 'Статья')
            Post.objects.create(title=title, main_text=main_text, isAuthor_id=1, kind='PUBL')

    def __str__(self):
        return f'{self.title}: {self.main_text[:20]}'

    def get_absolute_url(self):
        if self.kind == 'NEWS':
            return reverse('news_detail', args=[str(self.id)])
        else:
            return reverse('articles_detail', args=[str(self.id)])


class PostCategory(models.Model):
    isPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    isCategory = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    isPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    isUser = models.ForeignKey(User, on_delete=models.CASCADE)
    main_text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0)

    def like(self):
        self.rate = ChangeRate.make_like(self.rate)
        self.save()

    def dislike(self):
        self.rate = ChangeRate.make_dislike(self.rate)
        self.save()











