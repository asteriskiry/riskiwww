from django.db import models

# Kaikki uniikit tapahtumatyypit (esim. sitsit).
class EventType(models.Model):
	event_type=models.CharField(max_length=500,unique=True, verbose_name='Tapahtuman tyyppi')
	def __str__(self):
		return "Tapahtuman tyyppi: "+str(self.event_type)

# Tapahtuman järjestäjä (esim. Asteriski).
class EventOwner(models.Model):
	name=models.CharField(max_length=500, unique=True, verbose_name='Järjestävä taho')
	email=models.EmailField(verbose_name='Sähköpostiosoite')
	def __str__(self):
		return "Tapahtuman järjestäjä(t): "+str(self.name)+", Sähköposti: "+str(self.email)

# Kaikki tapahtumat koodusti.
class Events(models.Model):
	event_type=models.ForeignKey(EventType, to_field='event_type' ,on_delete=models.CASCADE)
	uid=models.PositiveIntegerField(primary_key=True)
	owner=models.ForeignKey(EventOwner, to_field='name', on_delete=models.CASCADE)
	def __str__(self):
		return "Tapahtuman tyyppi: "+str(self.event_type)+", uid: "+str(self.uid)+", tapahtuman järjestäjä(t) : "+str(self.owner)

# Eri tapahtumatyyppien yhteiset attribuutit.
# Abstrakti yläluokka.
class CommonInfo(models.Model):
#	def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#		return 'events/user_{0}/{1}'.format(instance.user.id, filename)

	#kaikki yhteiset attribuutit tähän
	uid=models.ForeignKey(Events, on_delete=models.CASCADE,editable=False)
	event_type=models.ForeignKey(EventType, to_field='event_type', on_delete=models.CASCADE,editable=False)
	owner=models.ForeignKey(EventOwner, to_field='name', on_delete=models.CASCADE,editable=False)
	name=models.CharField(max_length=500, verbose_name='Tapahtuman nimi')
	place=models.CharField(max_length=200, verbose_name='Pitopaikka')
	date=models.DateTimeField(verbose_name='Tapahtuman pitopäivä')
	start_time=models.TimeField(verbose_name='Tapahtuman alkamisaika', default='00:00:00')
	description=models.TextField(verbose_name='Tapahtuman yleiskuvaus')
	pic=models.ImageField(blank=True, null=True,verbose_name='Ilmoittautumislomakkeen kansikuva', upload_to='events/%Y/%m/')
	prize=models.CharField(max_length=500,blank=True, null=True,verbose_name='Tapahtuman hinta')
	max_participants=models.PositiveIntegerField(blank=True, null=True,verbose_name='Maksimimäärä osallistujia')
	signup_starts=models.DateTimeField(verbose_name='Tapahtumaan ilmoittautuminen avautuu')
	signup_ends=models.DateTimeField(blank=True, null=True,verbose_name='Tapahtumaan ilmoittautuminen sulkeutuu')

	def __str__(self):
		return "Tapahtuman järjestäjä: "+str(self.owner)+", Tapahtuman tyyppi: "+str(self.event_type)+", Tapahtuman nimi: "+self.name+", Pitopaikka "+self.place+", Hinta: "+str(self.prize)+", Tapahtuman pitopäivä: "+str(self.date)+", Maksimi osallistujamäärä: "+str(self.max_participants)+", Ilmoittautuminen alkaa: "+str(self.signup_starts)+", Ilmoittautuminen loppuu: "+str(self.signup_ends)+", Yleiskuvaus: "+self.description

	def genInfo(self):
		if not self.prize:
			return "<li>Mikä: "+self.name+"</li><li>Missä: "+self.place+"</li><li>Milloin: "+str(self.date)+"</li><li>Mitä maksaa: Ilmainen</li>"
		elif(self.prize==0):
			return "<li>Mikä: "+self.name+"</li><li>Missä: "+self.place+"</li><li>Milloin: "+str(self.date)+"</li><li>Mitä maksaa: Ilmainen</li>"
		else:
			return "<p>Mikä-Missä-Milloin</p><p><ul><li>Mikä: "+self.name+"</li><li>Missä: "+self.place+"</li><li>Milloin: "+str(self.date)+"</li><li>Mitä maksaa: "+str(self.prize)+"</li>"

	class Meta:
		abstract = True

# Sitsit tyyppinen tapahtuma.
class Sitz(CommonInfo):
	quotas=models.CharField(max_length=500,null=True, blank=True,verbose_name='Järjestävien tahojen osallistujakiintiöt')
#	avec=models.CharField(max_length=500,blank=True)
#	plaseerustoive=models.CharField(max_length=500,blank=True)
	def __str__(self):
		if self.quotas is None:
			return super().__str__()+", Osallistujakiintiöt: Ei ole"
		else:
			return super().__str__()+", Osallistujakiintiöt: "+self.quotas

# Vuosijuhlat tyyppinen tapahtuman.
class Annualfest(CommonInfo):
#	avec=models.CharField(max_length=500,blank=True)
#	plaseerustoive=models.CharField(max_length=500,blank=True)
	def __str__(self):
		return super().__str__()

# Ekskurisio tyyppinen tapahtuma.
class Excursion(CommonInfo):
	date=models.DateField(verbose_name='Ekskursion aloituspäivä')
	end_date=models.DateField(verbose_name='Ekskursion loppumispäivä')
	def __str__(self):
		return super().__str__()+", Päättymispäivä: "+str(self.end_date)

# Muu ennalta määrittelemätön tapahtuma.
class OtherEvent(CommonInfo):
	min_participants=models.PositiveIntegerField(blank=True, null=True,verbose_name='Minimimäärä osallistujia')
	def __str__(self):
		return super().__str__()+", Minimimäärä osallistujia: "+str(self.min_participants)

# Tapahtumaan osallistuja.
class Participant(models.Model):
	event_type=models.ForeignKey(Events, on_delete=models.CASCADE,editable=False)
	name=models.CharField(max_length=200,verbose_name='Nimi')
	email=models.EmailField(verbose_name='Sähköpostiosoite')
#	lihaton=models.NullBooleanField()
#	holiton=models.NullBooleanField()
#	is_member=models.NullBooleanField()
#	has_paid=models.NullBooleanField()
#
#	Tämä kenttä sisältää tiedot: holillinen/holiton, liha/kasvis, jäsen/ei jäsen, onko maksanut, avec, plaseeraustoive.
#	datan tulee olla muodossa {lihaton: arvo, holiton:arvo, member:arvo, hasPaid:arvo, avec:arvo, plaseeraus:arvo}
	miscInfo=models.TextField(editable=False)
	def __str__(self):
		return self.name+" ("+self.email+"), muut tiedot: "+self.miscInfo

# Arkistotaulu.
class Archive(models.Model):
	event_type=models.CharField(max_length=500,verbose_name='Tapahtuman typpi')
	name=models.CharField(max_length=500,verbose_name='Tapahtuman nimi')
	description=models.TextField(verbose_name='Tapahtuman yleiskuvaus')
	participants=models.IntegerField(verbose_name='Osallistujamäärä')
	owner=models.CharField(max_length=500,verbose_name='Tapahtuman pitäjä')
	date=models.DateTimeField(verbose_name='Tapahtuman pitopäivä')
	def __str__(self):
		return "Tapahtuman tyyppi: "+self.event_type+", Tapahtuman nimi: "+self.name+", Kokonaisosallistujamäärä: "+str(self.participants)+", Tapahtuman järjestäjä: "+self.owner+",Alkuperäinen pitopäivä: "+str(self.date)+", Yleiskuvaus: "+self.description
