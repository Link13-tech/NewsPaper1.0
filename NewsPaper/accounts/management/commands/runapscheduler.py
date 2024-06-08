import logging
from datetime import timedelta

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.utils import timezone
from news.models import Post, Category

logger = logging.getLogger(__name__)


def my_job():
    one_week = timezone.now() - timedelta(days=7)
    categories = Category.objects.all()

    for category in categories:
        posts = Post.objects.filter(post_time__gte=one_week, categories=category)
        if not posts.exists():
            continue

        subscribers = User.objects.filter(subscribed_categories=category)
        if not subscribers.exists():
            continue

        for subscriber in subscribers:
            subject = f"Еженедельная рассылка новостей для категории {category.name}"
            message = "Новые статьи за неделю:\n\n"
            for post in posts:
                post_url = f"{settings.SITE_URL}/news/{post.pk}"
                message += f"{post.title} - {post_url}\n\n"

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [subscriber.email])
            logger.info(f"Отправлено письмо {subscriber.email} с новостями для категории {category.name}")


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10", timezone=settings.TIME_ZONE),  # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown(wait=False)
            logger.info("Scheduler shut down successfully!")
