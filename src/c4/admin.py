from django.contrib import admin
from .models import Game, Step

# class StepInline(admin.TabularInline):
#     model = Step
#     extra = 0

class GameAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Game._meta.fields]

    class Meta:
        model = Game

admin.site.register(Game, GameAdmin)
