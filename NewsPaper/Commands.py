u1 = User.objects.create_user(username='Жорж')
u2 = User.objects.create_user(username='Вениамин')

a1 = Author.objects.create(user=u1)
a2 = Author.objects.create(user=u2)

cat1 = Category.objects.create(name='Спорт')
cat2 = Category.objects.create(name='Политика')
cat3 = Category.objects.create(name='История')
cat4 = Category.objects.create(name='Наука')

ar1 = Post.objects.create(author=a1, post_type='AR', title='Статья1', content='Первая статья')
ar2 = Post.objects.create(author=a2, post_type='AR', title='Статья2', content='Вторая статья')
ne1 = Post.objects.create(author=a1, post_type='NE', title='Новость1', content='Первая новость')

ar1.categories.add(cat1)
ar2.categories.add(cat2, cat4)
ne1.categories.add(cat3)

com1 = Comment.objects.create(post=ar1, user=a2.user, text='Норм статья')
com2 = Comment.objects.create(post=ar2, user=a1.user, text='Понравилась статейка')
com3 = Comment.objects.create(post=ne1, user=a2.user, text='Так и думал')
com4 = Comment.objects.create(post=ar2, user=a2.user, text='Спасибо')

ar1.like()
ar2.like()
ne1.like()
ne1.dislike()
ar2.like()

com1.like()
com3.dislike()
com4.like()
com2.like()

a1.update_rating()
a2.update_rating()

# Здесь я пробовал разные команды, но мне не нравился вывод,
# С коментами так и оставил в виде QuerySet
# Если нужен другой вид одной строкой через values, дайте пожалуйста знать, я поправлю

ba = Author.objects.order_by('-rating').first()
f"Username: {ba.user.username}, Рейтинг: {ba.rating}"

bp = Post.objects.order_by('-rating').first()
f"Дата:{bp.post_time.strftime('%d-%m-%Y')}, Username: {bp.author.user.username}, Рейтинг: {bp.rating}, Заголовок: {bp.title}, Превью: {bp.preview()}"

Comment.objects.filter(post=bp).values('comment_time', 'user__username', 'rating', 'text')
