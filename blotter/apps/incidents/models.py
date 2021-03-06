from django.contrib.gis.db import models
from django.contrib.gis import geos
from django.contrib.gis.gdal import OGRGeometry, OGRGeomType
from django import forms



#infraction?
class Crime(models.Model):
	name = models.CharField(max_length = 255)
	code = models.CharField(max_length= 255, blank = True)
	arrests = models.IntegerField(default = 0)
	#fake_field = models.CharField(null = True, blank = True)
	total_count = models.IntegerField(default=0)
	nat_description = models.CharField(max_length=255, null = True, blank=True)
	

	def get_count(self):
		return self.incident_set.count()

	def arrest_count(self):
		return self.arrest_set.count()

	def save(self, *args, **kwargs):
		super(Crime, self).save(*args, **kwargs)		

	def __unicode__(self):
		return self.name

class Property(models.Model):
	loss = models.CharField(max_length = 15)
	thing = models.CharField(max_length = 50)
	def __unicode__(self):
		return self.thing

class Agency(models.Model):
	name = models.CharField(max_length = 30)

	def __unicode__(self):
		return self.name


class Location(models.Model):
	name = models.CharField(max_length = 50, null = True)
	address = models.CharField(max_length =100, null = True)
	point_location = models.PointField('GeoDjango point field of this location', null=True, geography=True, blank = True)
	point_verified = models.BooleanField(default = False)
	agency = models.ForeignKey(Agency, null = True, blank = True)
	intersection_indicator = models.BooleanField(default = False)
	block = models.BooleanField(default = False)
	city  = models.CharField(max_length = 70, null = True, blank =  True)
	
	def __unicode__(self):
		return self.address
	def save(self, *args, **kwargs):
		super(Location, self).save(*args, **kwargs)		

class Officer(models.Model):
	name = models.CharField(max_length = 70)
	badge_number = models.IntegerField(null = True)
	def __unicode__(self):
		return self.name
class Race(models.Model):
	name = models.CharField(max_length = 5)
	def __unicode__(self):
		return self.name 

class Offender(models.Model):
	race = models.ForeignKey(Race)
	description = models.CharField(max_length = 200)


class Victim(models.Model):
	age = models.IntegerField(default = 0)
	sex = models.CharField(max_length=2, null = True)
	name = models.CharField(max_length = 50, null = True)
	origin = models.CharField(max_length = 50, null = True)

class Arrestee(models.Model):
	name = models.CharField(max_length = 100)
	age = models.IntegerField(default = 0)
	sex = models.CharField(max_length=2, null = True)
	address = models.ForeignKey(Location, null = True)
	race = models.ForeignKey(Race, null = True, blank = True)

	def __unicode__(self):
		return self.name

class Arrest(models.Model):
	arrestee = models.ForeignKey(Arrestee)
	charges = models.ManyToManyField(Crime)
	location = models.ForeignKey(Location)
	officer = models.ForeignKey(Officer, null = True)
	datetime = models.DateTimeField(null = True)

	def __unicode__(self):
		return self.arrestee.name

	def save(self, *args, **kwargs):
		super(Arrest, self).save(*args, **kwargs)		

######
######Need to add related incidents model and identify these cases. 
######Need to add link to original pdf, something saved and served by us?

class Incident(models.Model):
	#native
	agency = models.ForeignKey(Agency, null = True, blank = True)
	code = models.CharField(max_length = 20)
	datetime_occurred = models.DateTimeField(null = True)
	datetime_reported = models.DateTimeField(null = True)
	summary = models.TextField()

	#singles
	officer = models.ForeignKey(Officer)
	location_occurred = models.ForeignKey(Location)

	#manyfields
	crimes = models.ManyToManyField(Crime)
	arrests = models.ManyToManyField(Arrest, null = True)
	offenders = models.ManyToManyField(Offender, null = True)
	properties = models.ManyToManyField(Property, null = True)

	raw_entry = models.TextField(null = True)

	def __unicode__(self):
		return self.code

	def save(self, *args, **kwargs):
		super(Incident, self).save(*args, **kwargs)			



