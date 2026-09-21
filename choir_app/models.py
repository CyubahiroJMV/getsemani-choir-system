from django.db import models

# 1. URUTONDE RW'ABARIRIMBYI (MEMBER MODEL)
class Member(models.Model):
    VOICE_CHOICES = [
        ('Soprano', 'Soprano'),
        ('Alto', 'Alto'),
        ('Tenor', 'Tenor'),
        ('Bass', 'Bass'),
    ]
    name = models.CharField(max_length=200)
    voice = models.CharField(max_length=50, choices=VOICE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.voice})"

# 2. INBOX Y'INDIRIMBO (SONG MODEL) — HANO IKOSA RYAKUWEHO BURUNDU!
class Song(models.Model):
    title = models.CharField(max_length=200)
    lyrics = models.TextField()
    # Hano twakosoye 'upload_to' mu buryo bw'ukuri bwa Django ngenderwaho
    audio_file = models.FileField(upload_to='choir_audios/', blank=True, null=True)

    def __str__(self):
        return self.title

# 3. IMISANZU N'AMATURO (CONTRIBUTION MODEL)
class Contribution(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.name} - {self.purpose} ({self.amount} RWF)"

# 4. ATTENDANCE MODEL
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.member.name} - {self.date} ({self.status})"
