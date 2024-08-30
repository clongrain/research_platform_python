from django.urls import path
from . import views

urlpatterns = [
    path("students", views.exportStudents, name='export-students'),
    path("teachers", views.exportTeachers, name='export-teachers'),
    path("awards", views.exportAwards, name='export-awards'),
    path("patents", views.exportPatents, name='export-patents'),
    path("projects", views.exportProjects, name='export-projects'),
    path("monographs", views.exportMonographs, name='export-monographs'),
    path("conference-papers", views.exportConferencePapers, name='export-conference-papers'),
    path("journal-papers", views.exportJournalPapers, name='export-journal-papers'),
    path("software-copyrights", views.exportSoftwareCopyrights, name='export-software-copyrights'),
    # path("<int:fileId>", views.index, name='details'),
    # path("<int:fileId>/results", views.index, name='results'),
]