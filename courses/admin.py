from django.contrib import admin

import helpers
from .models import (Course, Likes, Category, Subject,
                      Module, Lesson, LessonVideo, Student, Enrollment, Quiz, Question, Payment)
from django.utils.html import format_html
# Customizing the Course Admin



class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1  # Number of empty rows for adding new modules


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    list_filter = ('title',)
    search_fields = ('title', 'public_id')
    
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    exclude = ('author',)

    def save_model(self, request, obj, form, change):
        if not change or not obj.author:  # Only set the author if it's a new object
            obj.author = request.user
        super().save_model(request, obj, form, change)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'public_id',
                    'access', 'status','subject', 'price',
                    'created_at', 'updated_at',
                    'image',
                   
                    )
    list_filter = ('subject', 'price')
    search_fields = ('title', 'description', 'instructor__user__username')
    readonly_fields = ['public_id', 'display_image']

    actions = ['approve_courses']
    

    inlines = [ModuleInline]

    def display_image(self, obj, *args, **kwargs):
        print(obj)
        url = helpers.get_cloudinary_image_object(
            obj, 
            field_name='image',
            width=200
        )
        return format_html(f"<img src={url} />")



    def approve_courses(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, "Selected courses have been approved")
    approve_courses.short_description = "Approve selected courses"


    def get_enrolled_courses(self, obj):
        return ", ".join([enrollment.course.title for enrollment in obj.enrollment_set.all()])
    get_enrolled_courses.short_description = 'Enrolled Courses'
# Customizing the Module Admin

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0  # Preload empty fields for adding lessons


class LikesAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'created_at')
    list_filter = ('course', 'user')
    list_display_links = ('course', 'user')


    def get_queryset(self, request):
        # Get the original queryset
        qs = super().get_queryset(request)
        
        # Filter the queryset based on the requested user (for example, filtering objects created by the user)
        if request.user.is_superuser:
            return qs  # Superuser sees all records
        else:
            return qs.filter(user=request.user)  # Regular users see only their own records

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    inlines = [LessonInline]



# Customizing the Lesson Admin
class LessonVideoInline(admin.StackedInline):
    model = LessonVideo
    extra = 0  # Preload one empty video field for adding lessons with videos
    readonly_fields = [
        'public_id', 
        'display_video',
    ]
    def display_video(self, obj, *args, **kwargs):
        video_embed_html = helpers.get_cloudinary_video_object(
            obj, 
            field_name='video',
            as_html=True,
            width=550
        )
        return video_embed_html

    display_video.short_description = "Current Video"

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order','thumbnail')
    list_filter = ('module__course',)
    search_fields = ('title', 'module__title', 'module__course__title')
    inlines = [LessonVideoInline]
   
  

  


class LessonVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'video',)



   


# Customizing the Student Admin
class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0  # Display current enrollments without extra fields

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_enrolled_courses')
    search_fields = ('user__username', 'user__email')
    inlines = [EnrollmentInline]

    def get_enrolled_courses(self, obj):
        return ", ".join([enrollment.course.title for enrollment in obj.enrollment_set.all()])
    get_enrolled_courses.short_description = 'Enrolled Courses'


# Customizing the Quiz Admin
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # Preload one question per quiz


class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'total_marks')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    inlines = [QuestionInline]


# Register all models to admin site
admin.site.register(Course, CourseAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Payment)
admin.site.register(Likes, LikesAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(LessonVideo, LessonVideoAdmin)
