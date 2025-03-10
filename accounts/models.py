

from django.db import models

class Materiel(models.Model):
    code = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=100)
    designation = models.CharField(max_length=200)
    marque = models.CharField(max_length=100)
    caracteristique = models.TextField()
    etat = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.code} - {self.designation}"


class Employee(models.Model):
    matricule = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naiss = models.DateField()
    lieu_naiss = models.CharField(max_length=100)
    grade = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenom}"


class Etablissement(models.Model):
    nom_etablissement = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nom_etablissement


class Emplacement(models.Model):
    designation = models.CharField(max_length=200)
    id_etablissement = models.ForeignKey(Etablissement, on_delete=models.CASCADE)
    id_employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.designation


class Affectation(models.Model):
    id_materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE)
    id_emplacement = models.ForeignKey(Emplacement, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.id_materiel} - {self.id_emplacement} - {self.date}"

