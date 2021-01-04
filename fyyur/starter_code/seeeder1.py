from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Venue, Artist, Show
from sqlalchemy.ext.declarative import declarative_base
import sys


engine = create_engine('postgresql+psycopg2://@localhost/fyyurDB2')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance

#postgresql+psycopg2://username:password@localhost/dbname
#SQLALCHEMY_DATABASE_URI = 'postgresql://@localhost:5432/fyyurDB'
DBSession = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)
Base.metadata.bind = engine
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

try:
    venue1 = Venue(name="The Musical Hop", city="San Francisco", state="CA", address="1015 Folsom Street" ,
    phone="123-123-1234", image_link ="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    facebook_link="https://www.facebook.com/TheMusicalHop",website= "https://www.themusicalhop.com", seeking_talent=True ,
    seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us.",
    genres=["Jazz", "Reggae", "Swing", "Classical", "Folk"])

    venue2 = Venue(name="The Dueling Pianos Bar", city="New York", state="NY", address="335 Delancey Street" , 
    phone="914-003-1132", image_link ="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    facebook_link="https://www.facebook.com/theduelingpianos",website= "https://www.theduelingpianos.com",seeking_talent=False ,
    seeking_description="",genres=["Classical", "R&B", "Hip-Hop"])

    venue3 = Venue( name="Park Square Live Music & Coffee", city="San Francisco", state="CA", address="34 Whiskey Moore Ave" ,
    phone="415-000-1234", image_link ="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    website= "https://www.parksquarelivemusicandcoffee.com", seeking_talent=False ,
    seeking_description="", genres= ["Rock n Roll", "Jazz", "Classical", "Folk"])

    venue4 = Venue( name="Park ", city="San Francisco", state="CA", address="34  Moore Ave" ,
    phone="415-000-1234", image_link ="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    website= "https://www.parksquarelivemusicandcoffee.com", seeking_talent=False ,
    seeking_description="", genres= ["Rock n Roll", "Jazz", "Classical", "Folk"])
    session.add_all([venue1, venue2, venue3, venue4])
    session.commit()


    artist4 = Artist(name="Guns N Petals", city="San Francisco", state="CA", phone="326-123-5000" , genres="Rock n Roll", 
        image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        facebook_link="https://www.facebook.com/GunsNPetals",  website= "https://www.gunsnpetalsband.com", seeking_talent=True ,
        seeking_description="Looking for shows to perform at in the San Francisco Bay Area!")

    artist5 = Artist( name="Matt Quevedo", city="New York", state="NY", phone="300-400-5000" , genres="Jazz", 
        image_link="https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        facebook_link="https://www.facebook.com/mattquevedo923251523", website= "https://www.parksquarelivemusicandcoffee.com", seeking_talent=False ,
        seeking_description="Looking for shows to perform at in the San Francisco Bay Area!")
    
    artist6 = Artist( name="The Wild Sax Band", city="San Francisco", state="CA", phone="432-325-5432" , genres=["Jazz", "Classical"], 
        image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        facebook_link="", website= "https://www.parksquarelivemusicandcoffee.com", seeking_talent=False ,
        seeking_description="")

    session.add_all([artist4, artist5, artist6])
    session.commit()

    show1 = Show(id=1, start_time="2019-05-21T21:30:00.000Z", venue_id=2, artists_id=1, ShowType=False)#  pastshow == false or post show ==true 
    show2 = Show(id=2, start_time="2019-06-15T23:00:00.000Z", venue_id=4, artists_id=2, ShowType=False)#  pastshow == false or post show ==true 
    show3 = Show(id=3, start_time="2035-04-01T20:00:00.000Z", venue_id=4, artists_id=3, ShowType=True)#  pastshow == false or post show ==true 
    show4 = Show(id=4, start_time="2035-04-08T20:00:00.000Z", venue_id=4, artists_id=3, ShowType=True)#  pastshow == false or post show ==true 
    show5 = Show(id=5, start_time="2035-04-15T20:00:00.000Z", venue_id=4, artists_id=3, ShowType=True)#  pastshow == false or post show ==true 
    session.add_all([show1, show2, show3, show4, show5])
    session.commit()
    session.close()
except:
    session.rollback()