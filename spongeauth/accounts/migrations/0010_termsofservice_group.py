# Generated by Django 2.0.3 on 2018-04-28 15:05

from django.db import migrations, models
import django.db.models.deletion


def create_group_for_each_tos(apps, schema_editor):
    TermsOfService = apps.get_model("accounts", "TermsOfService")
    Group = apps.get_model("accounts", "Group")
    db_alias = schema_editor.connection.alias
    for tos in TermsOfService.objects.using(db_alias).all():
        group = Group(
            name="Accepted ToS: " + tos.name, internal_name="accepted_tos_{}".format(tos.pk), internal_only=True
        )
        group.save(using=db_alias)
        group.user_set.set(tos.agreed_users.all())
        tos.group = group
        tos.save(using=db_alias)


class Migration(migrations.Migration):

    dependencies = [("accounts", "0009_add_spongepowered_tos_2018-03-10")]

    operations = [
        migrations.AddField(
            model_name="termsofservice",
            name="group",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="accounts.Group"),
        ),
        migrations.RunPython(create_group_for_each_tos),
        migrations.AlterField(
            model_name="termsofservice",
            name="group",
            field=models.ForeignKey(null=False, on_delete=django.db.models.deletion.CASCADE, to="accounts.Group"),
        ),
    ]
