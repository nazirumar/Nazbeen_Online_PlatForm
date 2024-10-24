from django import forms
from courses.models import Category, Subject, Course, Module, Lesson, LessonVideo, Student, Enrollment

# Category Form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

# Subject Form
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['title', 'category', 'description', 'author']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].widget.attrs['readonly'] = True  # Only allow authors to set this

# Course Form
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'subject', 'description', 'pdf', 'image', 'access', 'status', 'is_free', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

# Module Form
class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'course']

# Lesson Form
class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'module', 'thumbnail']

# Lesson Video Form
class LessonVideoForm(forms.ModelForm):
    class Meta:
        model = LessonVideo
        fields = ['title', 'lesson', 'duration', 'video', 'url']

    def clean_video(self):
        video = self.cleaned_data.get('video')
        # Add custom validation for video files here if needed
        if video and video.size > 104857600:  # Limit to 100 MB
            raise forms.ValidationError("Video file too large ( > 100 MB )")
        return video

# Student Form (if needed for additional attributes)
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user']

# Enrollment Form
class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course']




# Initialize all forms
category_form = CategoryForm()
subject_form = SubjectForm()
course_form = CourseForm()
ModuleFormSet = forms.modelformset_factory(Module, form=ModuleForm, extra=2) # Adjust 'extra' as needed
lesson_formset = forms.modelformset_factory(Lesson, form=LessonForm, extra=1)
LessonVideoFormSet = forms.modelformset_factory(LessonVideo, fields=('video', 'lesson', 'title'), extra=2)
student_form = StudentForm()
enrollment_form = EnrollmentForm()