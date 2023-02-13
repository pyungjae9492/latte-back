from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea
from .models import *

# Register your models here.


class SceneAdmin(admin.ModelAdmin):
    list_display=('Name','pub_date','id')
    #filter_horizontal = ('NextScenes',)
    search_fields=['pub_date','id']
class Scene_textAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'40'})},
        models.TextField: {'widget': Textarea(attrs={'rows':40, 'cols':100})},
    }

admin.site.register(User,UserAdmin)
admin.site.register(Scene,SceneAdmin)
admin.site.register(Scene_picture)
admin.site.register(Scene_text,Scene_textAdmin)
admin.site.register(Question_Answer)
admin.site.register(Diverges)
admin.site.register(Item)
admin.site.register(Fact)
admin.site.register(Character)
admin.site.register(Speech_to_Text)
admin.site.register(Text_reader)
admin.site.register(Face_reader)
admin.site.register(Movie)
admin.site.register(Blog)
admin.site.register(CommentAndStar)