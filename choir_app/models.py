from django.db import models
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from django.utils import timezone

# 1. URUTONDE RW'ABARIRIMBYI (MEMBER MODEL)
class Member(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    voice = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# 2. INBOX Y'INDIRIMBO (SONG MODEL) — HANO IKOSA RYAKUWEHO BURUNDU!
class Song(models.Model):
    title = models.CharField(max_length=200)
    lyrics = models.TextField()
    # Hano twakosoye 'upload_to' mu buryo bw'ukuri bwa Django ngenderwaho
    audio_file = models.FileField(
    upload_to='songs_audio/',
    storage=VideoMediaCloudinaryStorage(),
    blank=True,
    null=True
)


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
        
# 4. UBWITABIRE (Attendance MODEL)
class Attendance(models.Model):
    REASON_CHOICES = [
        ('', 'Hitamo impamvu...'),
        ('Arwaye', 'Arwaye'),
        ('Afite uruhushya', 'Afite uruhushya'),
        ("Impamvu z'akazi", "Impamvu z'akazi"),
        ('Impamvu bwite', 'Impamvu bwite'),
        ('Nta mpamvu ifatika', 'Nta mpamvu ifatika'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now)
    is_present = models.BooleanField(default=False)
    reason = models.CharField(max_length=100, choices=REASON_CHOICES, blank=True, default='')

    class Meta:
        unique_together = ('member', 'date')

    def __str__(self):
        return f"{self.member.name} - {self.date}"
